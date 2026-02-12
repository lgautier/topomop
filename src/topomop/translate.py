from topomop import cdm_csv
import jinja2
import os
import typing
import warnings

cdm_nonparametric_to_sqlalchemy = {
    'bigint': 'BigInteger',
    'float': 'Float',
    'integer': 'Integer',
    'date': 'Date',
    'datetime': 'DateTime',
}
if cdm_csv.CDM_TYPE_NONPARAMETRIC != set(cdm_nonparametric_to_sqlalchemy):
    only_sqlalchemy = set(cdm_nonparametric_to_sqlalchemy) - cdm_csv.CDM_TYPE_NONPARAMETRIC
    if only_sqlalchemy:
        warnings.warn(
            f'Only defined in SQL Alchemy translation: {only_sqlalchemy}'
        )
    else:
        only_omop = cdm_csv.CDM_TYPE_NONPARAMETRIC - set(cdm_nonparametric_to_sqlalchemy)
        raise ImportError(
            f'OMOP CDM types without an SQLAlchemy translation: {only_omop}'
        )


def to_alchemy_typestr(omop_cdm_type: str):
    if cdm_csv._is_varchar(omop_cdm_type):
        m = cdm_csv.CDM_VARCHAR_PATTERN.match(omop_cdm_type)
        if m is None:
            raise ValueError(f'Invalid cdmDataType {omop_cdm_type}')
        if m.groups()[0] in {'MAX', 'max'}:
            alchemy_typestr = 'String'
        else:
            varchar_len = int(m.groups()[0])
            alchemy_typestr = f'String({varchar_len})'
    else:
        alchemy_typestr = cdm_nonparametric_to_sqlalchemy.get(omop_cdm_type)
    return alchemy_typestr
    

class FieldAlchemyAdapter:
    row_i: int
    cdm: cdm_csv.FieldAbstract

    def __init__(self,
                 obj: cdm_csv.DataFromRow[cdm_csv.FieldAbstract]):
        self.row_i = obj.row_i
        self.cdm = obj.data

    @property
    def name(self) -> str:
        return self.cdm.cdmFieldName

    @property
    def alchemytype(self) -> str:
        return to_alchemy_typestr(self.cdm.cdmDatatype)

    @property
    def is_primarykey(self) -> bool:
        return self.cdm.isPrimaryKey

    def foreignkey(self, curr_schema, name2schema) -> str | None:
        fk = self.cdm.foreignkey()
        if fk:
            fk_schema = name2schema[fk[0].lower()]
            if fk_schema != curr_schema:
                # TODO: use named attributes.
                fk = '.'.join((fk_schema, fk[0], fk[1]))
            else:
                fk = '.'.join(fk)
        return fk

    @property
    def is_required(self) -> bool:
        return self.cdm.isRequired


class TableAlchemyAdapter:
    row_i: int
    cdm: cdm_csv.TableAbstract
    _varname: str | None
    _fields: typing.Sequence[FieldAlchemyAdapter]
    _patch_composite_primary_keys: tuple[str, ...] | None

    def __init__(
            self,
            obj: cdm_csv.DataFromRow[cdm_csv.TableAbstract],
            fields: typing.Sequence[FieldAlchemyAdapter],
            varname: str | None = None,
            _patch_composite_primary_keys: tuple[str, ...] | None = None
    ):
        self.row_i = obj.row_i
        self.cdm = obj.data
        self._varname = varname
        self._fields = fields
        self._patch_composite_primary_keys = _patch_composite_primary_keys

    @property
    def fields(self):
        return self._fields

    @property
    def varname(self) -> str:
        if self._varname:
            return self._varname
        else:
            return self.name

    @property
    def name(self) -> str:
        return self.cdm.cdmTableName


def escape_tripleq(obj: str):
    return obj.replace('"""', r'\"""')


_STYLE_TEMPLATE = {
    'declarative': 'sqlalchemy_declarative.py.jinja2',
    'imperative': 'sqlalchemy_imperative.py.jinja2'
}

def render_sqlalchemy(
        cdm_version: str,
        schema_name: str,
        name2schema: dict[str, str],
        tables: dict[
            str, tuple[cdm_csv.DataFromRow[cdm_csv.TableAbstract],
                       tuple[cdm_csv.DataFromRow[cdm_csv.FieldAbstract], ...]]
        ],
        comment_origin: bool = True,
        style: str = "imperative",
        _patch_composite_primary_keys_schema: (
            cdm_csv._TYPE_PATCH_COMPOSITE_PRIMARY_KEY | None) = None,
        _patch_override_attributes_schema: (
            cdm_csv._TYPE_PATCH_OVERRIDE_ATTRIBUTES | None) = None
):
    if _patch_composite_primary_keys_schema is None:
        _patch_composite_primary_keys_schema = {}
    if _patch_override_attributes_schema is None:
        _patch_override_attributes_schema = {}

    tables_prepared = []
    for tbl, fields in tables.values():
        fields_prepared = []
        _patch_attrs: dict[str, tuple[tuple[str, object], ...]] | None = (_patch_override_attributes_schema
                                                              .get(tbl.data.name.upper()))
        _patch_prim_keys = _patch_composite_primary_keys_schema.get(tbl.data.cdmTableName.upper())
        if _patch_prim_keys:
            warnings.warn(
                f'{tbl.data.name.upper()}: '
                f'setting a composite primary key with {repr(_patch_prim_keys)}'
            )
        for fld in fields:
            if _patch_prim_keys and (fld.data.name.upper() in _patch_prim_keys):
                setattr(fld.data, 'isPrimaryKey', True)
                warnings.warn(
                    f'{tbl.data.name.upper()}.{fld.data.name.upper()}: '
                    'setting isPrimaryKey to True,'
                )

            if _patch_attrs and (fld.data.name.upper() in _patch_attrs):
                for key, value in _patch_attrs[fld.data.name.upper()]:
                    orig_value = getattr(fld.data, key)
                    setattr(fld.data, key, value)
                    warnings.warn(
                        f'{tbl.data.name.upper()}.{fld.data.name.upper()}: '
                        f'field {key} in OMOP CDM changed from {repr(orig_value)} to {repr(value)}.'
                    )
            fields_prepared.append(
                FieldAlchemyAdapter(fld)
            )

        tables_prepared.append(
            TableAlchemyAdapter(
                tbl,
                fields_prepared,
                _patch_composite_primary_keys = _patch_prim_keys
            )
        )
    data = {
        'cdm_version': cdm_version,
        'schema_name': schema_name,
        'name2schema': name2schema,
        'tables': tables_prepared,
        'comment_origin': comment_origin
    }

    # TODO: template current in the same directory as the modules.
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
        undefined=jinja2.StrictUndefined
    )
    env.filters['repr'] = repr
    env.filters['escape_tripleq'] = escape_tripleq
    template = env.get_template(_STYLE_TEMPLATE[style])

    return template.render(data)
