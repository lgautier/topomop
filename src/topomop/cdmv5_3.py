import attrs
import dataclasses
from topomop.cdm_csv import (
    _bool,
    _cdmdatatype,
    _str_optional,
    CdmInfo,
    FieldAbstract,
    Schema,
    TableAbstract
)


INFO = CdmInfo(
    'v5.3',
    'OMOP_CDMv5.3_Table_Level.csv',
    'OMOP_CDMv5.3_Field_Level.csv'
)


@attrs.define
class Field(FieldAbstract):
    cdmTableName: str
    cdmFieldName: str
    isRequired: bool = attrs.field(converter=_bool)
    cdmDatatype: str = attrs.field(converter=_cdmdatatype)
    userGuidance: str | None = attrs.field(converter=_str_optional)
    etlConventions: str | None = attrs.field(converter=_str_optional)
    isPrimaryKey: str | None = attrs.field(converter=_bool)
    isForeignKey: bool = attrs.field(converter=_bool)
    fkTableName: str | None = attrs.field(converter=_str_optional)
    fkFieldName: str | None = attrs.field(converter=_str_optional)
    fkDomain: str | None = attrs.field(converter=_str_optional)
    fkClass: str | None = attrs.field(converter=_str_optional)
    uniqueDQidentifiers: str | None = attrs.field(converter=_str_optional)


@attrs.define
class Table(TableAbstract):
    cdmTableName: str
    schema: Schema = attrs.field(converter=Schema)
    isRequired: bool = attrs.field(converter=_bool)
    conceptPrefix: str | None = attrs.field(converter=_str_optional)
    measurePersonCompleteness: bool = attrs.field(converter=_bool)
    measurePersonCompletenessThreshold: str | None = attrs.field(converter=_str_optional)
    validation: str | None = attrs.field(converter=_str_optional)
    tableDescription: str
    userGuidance: str | None = attrs.field(converter=_str_optional)
    etlConventions: str | None = attrs.field(converter=_str_optional)
