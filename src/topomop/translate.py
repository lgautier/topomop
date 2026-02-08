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

    def __init__(
            self,
            obj: cdm_csv.DataFromRow[cdm_csv.TableAbstract],
            fields: typing.Sequence[FieldAlchemyAdapter],
            varname: str | None = None
    ):
        self.row_i = obj.row_i
        self.cdm = obj.data
        self._varname = varname
        self._fields = fields

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

_STYLE_TEMPLATE =  {
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
        style: str = "imperative"
):
    tables_prepared = []
    for tbl, fields in tables.values():
        fields_prepared = []
        for fld in fields:
            fields_prepared.append(FieldAlchemyAdapter(fld))

        tables_prepared.append(
            TableAlchemyAdapter(tbl, fields_prepared)
        )

    data = {
        'cdm_version': cdm_version,
        'schema_name': schema_name,
        'name2schema': name2schema,
        'tables': tables_prepared
    }

    # TODO: template current in the same directory as the modules.
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
        undefined=jinja2.StrictUndefined
    )
    template = env.get_template(_STYLE_TEMPLATE[style])

    return template.render(data)
