"""
The OMOP Common Data Model (CDM) is defined in CSV files. Each release
of the OMOP CDM consists of a pair of files: one that lists tables,
each assigned to a schema, and one that lists all fields in those tables.

The CSV files are currently distributed in the R package CommonDataModel,
distributed through CRAN and with a source repository on Github
(https://github.com/OHDSI/CommonDataModel).

This module provides simple utility code to support reading the CSV files using
Python natively, and as robustly as possible. It includes checks to trigger errors
or warnings when the content of the CSV file does not fully align with assumptions
made in this package.

Specifics to different versions of the CDM are delegated to
version-specific modules. The CSV file names follow the pattern in OMOP_FILENAME_PATTERN,
and each have their version mangled in their file name. `SUPPORTED_VERSIONS` is a Python dict
that maps the CDM version names as present in the file names to the name of the corresponding
Python module.
"""

import abc
import attrs
import collections
import csv
import enum
import importlib
import itertools
import os
import re
import typing
import types
import warnings
import io

# Filenames 
OMOP_FILENAME_PATTERN = re.compile(
    'OMOP_CDM(?P<version>.*)_(?P<component>Field|Table)_Level.csv'
)
OMOP_FILENAME_TEMPLATE = 'OMOP_CDM{version}_{component}_Level.csv'

SUPPORTED_VERSIONS = {
    'v5.3': 'cdmv5_3',
    'v5.4': 'cdmv5_4',
    'v6.0': 'cdmv6_0',
}

SUPPORTED_EXTENSIONS = {
    '_Oncology_Ex': 'cdm_Oncology_Ex'
}

type _TYPE_PATCH_COMPOSITE_PRIMARY_KEY = dict[
    str,  # table name.
    tuple[str, ...]
]

type _TYPE_PATCH_OVERRIDE_ATTRIBUTES = dict[
    str,  # table name.
    dict[
        str,  # field name.
        tuple[tuple[str,  object], ...]  # CDM attribute name, new value.
    ]
]


def _bool(obj: str|bool):
    if isinstance(obj, bool):
        res = obj
    elif obj == 'Yes':
        res = True
    elif obj == 'No':
        res = False
    elif obj in ('', 'NA'):
        # TODO: OMOP CDM's definition appear inconsistent.
        # Until this fixed (see
        # https://github.com/OHDSI/CommonDataModel/pull/769),
        # we assume that "" and "NA" mean "No" -> False.
        warnings.warn(
            f'Expected "Yes" or "No" and got {repr(obj)}. Assuming it means "No".'
        )
        res = False
    else:
        raise ValueError(
            'Acceptable values are a string that is '
            '"Yes" or "No", or a boolean. '
            f'Not {repr(obj)}.'
        )
    return res


class Schema(enum.StrEnum):
    """Database schema.

    This is currently CDM version-agnostic, but may not always be so.

    The fields list the schemas in the order they should be created
    to avoid table declaration issues with foreign keys across schemas.
    """
    VOCAB = 'VOCAB'
    CDM  = 'CDM'
    RESULTS = 'RESULTS'


@attrs.define
class CdmInfo:
    version: str
    csvpath_table: str
    csvpath_field: str


@attrs.define
class DataFromRow[T]:
    row_i: int
    data: T


CDM_TYPE_NONPARAMETRIC = {'bigint', 'integer', 'date', 'datetime', 'float'}
# TODO: The pattern for varmax parameters should be MAX. This is lower case
# because of a workaround elsewhere in the code that is required because of
# inconsistent upper/lower case in type definitions (most of the time
# "varchar", rarely "Varchar").
CDM_VARCHAR_PATTERN = re.compile('varchar\\(([0-9]+|MAX|max)\\)')


def _cdmdatatype(obj: str):
    # TODO: types in OHDSI's CSV definitions are not consistent
    # with casing.
    obj = obj.lower()
    if not (
            obj in CDM_TYPE_NONPARAMETRIC
            or
            CDM_VARCHAR_PATTERN.match(obj)
    ):
        raise ValueError(
            'Data types must be equal to one of the elements in CDM_TYPE_NONPARAMETRIC '
            'or match the pattern in CDM_TYPE_NONPARAMETRIC.'
        )
    return obj


def _is_varchar(obj: str):
    return CDM_VARCHAR_PATTERN.match(obj) is not None


def _str_optional(obj: str | None) -> str | None:
    assert isinstance(obj, str) or obj is None
    if obj == 'NA':
        res = None
    else:
        res = obj
    return res


class FieldAbstract(abc.ABC):
    cdmFieldName: str
    isRequired: bool
    cdmDatatype: str
    isPrimaryKey: bool
    isForeignKey: bool
    fkTableName: str | None
    fkFieldName: str | None

    def is_primarykey(self):
        return self.isPrimaryKey

    def is_required(self):
        return self.isRequired

    def foreignkey(self):
        if self.isForeignKey:
            return (self.fkTableName, self.fkFieldName)
        else:
            return None

    @property
    def name(self):
        return self.cdmFieldName


class TableAbstract(abc.ABC):
    cdmTableName: str

    @property
    def name(self):
        return self.cdmTableName

    
def match_omop_csv(fn: str):
        m = OMOP_FILENAME_PATTERN.match(fn)
        if m is None:
            warnings.warn(
                f"{fn} is not named like an OMOP CDM's CSV file."
            )
        return m


def scan(path):
    res = collections.defaultdict(dict)
    for fn in os.listdir(path):
        if not os.path.isfile(os.path.join(path, fn)):
            warnings.warn(f'Skipping "{fn}" (not a file).')
        m = match_omop_csv(fn)
        if m:
            res[m.group('version')][m.group('component')] = fn
        else:
            warnings.warn(
                f"{fn} is not named like an OMOP CDM's CSV file."
            )
    return res


def _read_csv(path, cls, _patch_row={}):
    with open(path, newline='') as fh:
        reader = csv.reader(fh)
        header = next(reader)

        header = tuple(
            'uniqueDQidentifiers' if _ == 'unique DQ identifiers' else _
            for _ in header
        )

        cls_fields = tuple(_.name for _ in attrs.fields(cls))
        if header != cls_fields:
            if len(header) != len(cls_fields):
                msg = (
                    f'CSV header has {len(header)} elements '
                    f'and class has {len(cls_fields)} data attributes.'
                )
            else:
                msg = (
                    'Mismatching names in CSV header and data class '
                    'attributes.'
                )
            raise ValueError(msg)

        final_empty_row_i = None
        for row_i, row in enumerate(reader):
            if len(row) == 0:
                warnings.warn(f'Empty row index {row_i}')
                final_empty_row_i = row_i
                continue
            elif final_empty_row_i and final_empty_row_i < row_i:
                raise ValueError(
                    f'Empty row(s) in the middle of the file (around row index {row_i}).'
                )
            if row_i in _patch_row:
                check_tuple, patched_str, issue = _patch_row[row_i]

                # TODO: Allow to skip the row patch if mismatch?
                if len(row) < len(check_tuple):
                    raise ValueError(
                        f'Row {row_i} has only {len(row)} elements (and check tuple needs {len(check_tuple)}).'
                    )
                elif check_tuple != tuple(row[:len(check_tuple)]):
                    raise ValueError(
                        f'Check tuple expected {repr(check_tuple)} '
                        f'but got {repr(tuple(row[:len(check_tuple)]))}).'
                    )

                in_memory_file = io.StringIO(patched_str)
                singlerow_reader = csv.reader(in_memory_file)
                row = next(singlerow_reader)

                warnings.warn(
                    f'{row_i} was patched to address and issue ({issue}).'
                )

            try:
                yield cls(*row)
            except (TypeError, ValueError) as err:
                err.add_note(f'Occurred on row index {row_i}.')
                raise err
    
class Cdm:
    """Common Data Model (as described in the OMOP CSV files).

    :param:csvdir_path: the path of the directory with CSV files.
    :param:cdm_modulename: the name of the module with CDM version-specific definitions.
    """

    __cdm_mod: types.ModuleType

    @property
    def cdm_module(self):
        return self.__cdm_mod

    @property
    def version(self):
        return self.__cdm_mod.INFO.version

    def __init__(self, csvdir_path: str, cdm_modulename: str):

        cdm_mod = importlib.import_module(cdm_modulename)

        m_field = match_omop_csv(
            cdm_mod.INFO.csvpath_field
        )
        assert m_field.group('component') == 'Field'        

        m_table = match_omop_csv(
            cdm_mod.INFO.csvpath_table
        )
        assert m_table.group('component') == 'Table'        

        assert (
            cdm_mod.INFO.version
            ==
            m_field.group('version')
            ==
            m_table.group('version')
        )       
        self.__cdm_mod = cdm_mod
        self.csvdir_path = csvdir_path

    def iter_tables(self) -> typing.Iterator[TableAbstract]:
        return _read_csv(
            os.path.join(
                self.csvdir_path,
                self.cdm_module.INFO.csvpath_table
            ),
            self.cdm_module.Table,
            self.cdm_module._PATCH_ROW['tables']
        )

    def iter_fields(self) -> typing.Iterator[tuple[str, FieldAbstract]]:
        return _read_csv(
            os.path.join(
                self.csvdir_path,
                self.cdm_module.INFO.csvpath_field
            ),
            self.cdm_module.Field,
            self.cdm_module._PATCH_ROW['fields']
        )

    def schemas(
            self
    ) -> tuple[
        dict[str, str],
        dict[
            str,
            dict[str, tuple[DataFromRow[TableAbstract],
                            tuple[DataFromRow[FieldAbstract], ...]]]
        ],
        # _PATCH_COMPOSITE_PRIMARY_KEY
        dict[str, _TYPE_PATCH_COMPOSITE_PRIMARY_KEY],
        # _PATCH_OVERRIDE_ATTRIBUTES
        dict[str, _TYPE_PATCH_OVERRIDE_ATTRIBUTES]
    ]:
        all_fields = list(DataFromRow(*_) for _ in enumerate(self.iter_fields()))
        all_fields.sort(key=lambda x: x.data.cdmTableName)

        all_tables = list(DataFromRow(*_) for _ in enumerate(self.iter_tables()))
        all_tables.sort(key=lambda x: x.data.schema.value)

        schemas = collections.defaultdict(dict)
        name2schema = dict()
        for schemaname, tables in itertools.groupby(
                all_tables, key=lambda x: x.data.schema.value
        ):
            for row_table in tables:
                if (
                        row_table.data.cdmTableName
                        in
                        schemas[row_table.data.schema.value]
                ):
                    raise ValueError(
                        f'{row_table.row_i}: duplicated table '
                        f'{row_table.data.cdmTableName} '
                        f'in {row_table.data.schema.value}'
                    )
                # Add the table, and set the associated fields to None. They are
                # populated later.
                (schemas[row_table.data.schema.value]
                 [row_table.data.cdmTableName]) = [row_table, None]
                name2schema[row_table.data.cdmTableName] = row_table.data.schema.value

        for tablename, fields in itertools.groupby(
                all_fields, key=lambda x: x.data.cdmTableName
        ):
            if tablename not in name2schema:
                warnings.warn(
                    f'Table {tablename} has fields but is not defined under a schema. '
                    f'Row indices {repr(tuple(_.row_i for _ in fields))}.'
                )
                continue
            table_tuple = schemas[
                name2schema[tablename]
            ][tablename]
            table_tuple[1] = tuple(fields)
            schemas[
                name2schema[tablename]
            ][tablename] = tuple(table_tuple)

        return (name2schema, schemas,
                self.cdm_module._PATCH_COMPOSITE_PRIMARY_KEYS,
                self.cdm_module._PATCH_OVERRIDE_ATTRIBUTES)
