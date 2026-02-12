import attrs
from .cdm_csv import (
    _bool,
    _cdmdatatype,
    _str_optional,
    CdmInfo,
    FieldAbstract,
    Schema,
    TableAbstract,
    _TYPE_PATCH_OVERRIDE_ATTRIBUTES,
    _TYPE_PATCH_COMPOSITE_PRIMARY_KEY
)


INFO = CdmInfo(
    'v5.4',
    'OMOP_CDMv5.4_Table_Level.csv',
    'OMOP_CDMv5.4_Field_Level.csv'
)


@attrs.define
class Field(FieldAbstract):
    cdmTableName: str
    cdmFieldName: str
    isRequired: bool = attrs.field(converter=_bool)
    cdmDatatype: str = attrs.field(converter=_cdmdatatype)
    userGuidance: str | None = attrs.field(converter=_str_optional)
    etlConventions: str | None = attrs.field(converter=_str_optional)
    isPrimaryKey: bool = attrs.field(converter=_bool)
    isForeignKey: bool = attrs.field(converter=_bool)
    fkTableName: str | None = attrs.field(converter=_str_optional)
    fkFieldName: str | None = attrs.field(converter=_str_optional)
    fkDomain: str | None = attrs.field(converter=_str_optional)
    fkClass: str | None = attrs.field(converter=_str_optional)
    uniqueDQidentifiers: str | None


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


_PATCH_ROW = {
    'fields': {
        204: (
            ('note_nlp', '"offset"'),
            'note_nlp,offset,No,varchar(50),Character offset of the extracted term in the input note,NA,No,No,NA,NA,NA,NA,NA',
            'See https://github.com/OHDSI/CommonDataModel/pull/773'
        ),
        353: (
            ('cdm_source', 'source_documentation_reference'),
            'cdm_source,source_documentation_reference,No,varchar(255),"Refers to a publication or web resource describing the source data, e.g. a data dictionary.",NA,No,No,NA,NA,NA,NA,NA',
            'See https://github.com/OHDSI/CommonDataModel/pull/766'
        )
    },
    'tables': {
    }
}

_PATCH_COMPOSITE_PRIMARY_KEYS: dict[str, _TYPE_PATCH_COMPOSITE_PRIMARY_KEY] = {
    'VOCAB': {
        'CONCEPT_RELATIONSHIP': (
            'CONCEPT_ID_1', 'CONCEPT_ID_2', 'RELATIONSHIP_ID', 'VALID_START_DATE', 'VALID_END_DATE'
        ),
        'CONCEPT_SYNONYM': (
            'CONCEPT_ID', 'CONCEPT_SYNONYM_NAME', 'LANGUAGE_CONCEPT_ID'
        ),
        'CONCEPT_ANCESTOR': (
            'ANCESTOR_CONCEPT_ID', 'DESCENDANT_CONCEPT_ID'
        ),
        'SOURCE_TO_CONCEPT_MAP': (
                'SOURCE_CONCEPT_ID', 'SOURCE_VOCABULARY_ID',
                'TARGET_CONCEPT_ID', 'TARGET_VOCABULARY_ID',
                'VALID_START_DATE', 'VALID_END_DATE', 'INVALID_REASON'
        ),
        'DRUG_STRENGTH': tuple()
    },
    'CDM': {
        'FACT_RELATIONSHIP': (
            'DOMAIN_CONCEPT_ID_1', 'FACT_ID_1',
            'DOMAIN_CONCEPT_ID_2', 'FACT_ID_2',
            'RELATIONSHIP_CONCEPT_ID'
        ),
        'EPISODE_EVENT': (
            'EPISODE_ID', 'EVENT_ID', 'EPISODE_EVENT_FIELD_CONCEPT_ID'
        ),
        'CDM_SOURCE': (
            'CDM_SOURCE_NAME',
            'CDM_SOURCE_ABBREVIATION',
            'CDM_HOLDER',
            'CDM_VERSION'
        )
    },
    'RESULTS': {
        'COHORT': (
            'COHORT_DEFINITION_ID', 'SUBJECT_ID'
        )
    }
}

_PATCH_OVERRIDE_ATTRIBUTES: dict[str, _TYPE_PATCH_OVERRIDE_ATTRIBUTES] = {
    'CDM': {  # schema.
        'DEATH': {  # table name.
            'PERSON_ID': (  # column/field name.
                ('isPrimaryKey', True),  # (CDM attribute name, new value).
            )
        }
    },
    'RESULTS': {
        'COHORT_DEFINITION': {
            'COHORT_DEFINITION_ID': (
                ('isPrimaryKey', True),
            )
        }
    }
}
