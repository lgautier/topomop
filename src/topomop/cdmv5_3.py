import attrs
from .cdm_csv import (
    _bool,
    _cdmdatatype,
    _str_optional,
    CdmInfo,
    FieldAbstract,
    Schema,
    TableAbstract,
    _TYPE_PATCH_COMPOSITE_PRIMARY_KEY,
    _TYPE_PATCH_OVERRIDE_ATTRIBUTES
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
    isPrimaryKey: bool = attrs.field(converter=_bool)
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


_PATCH_ROW = {
    'fields': {
        190: (
            ('note_nlp', '"offset"'),
            'note_nlp,offset,No,varchar(50),Character offset of the extracted term in the input note,NA,No,No,NA,NA,NA,NA,NA',
            'See https://github.com/OHDSI/CommonDataModel/pull/773'
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
        'METADATA': tuple(),
        'CDM_SOURCE': (
            'CDM_SOURCE_NAME',
            'CDM_SOURCE_ABBREVIATION',
            'CDM_HOLDER',
            'CDM_VERSION'
        )
    }
}

_PATCH_OVERRIDE_ATTRIBUTES: dict[str, _TYPE_PATCH_OVERRIDE_ATTRIBUTES] = {
    'VOCAB': {
        'COHORT_DEFINITION': {
            'COHORT_DEFINITION_ID': (
                (
                    ('isPrimaryKey', True),
                ),
                'See https://github.com/OHDSI/CommonDataModel/issues/772'
            )
        },
        'ATTRIBUTE_DEFINITION': {
            'ATTRIBUTE_DEFINITION_ID': (
                (
                    ('isPrimaryKey', True),
                ),
                ''
            )
        }
    },
    'CDM': {
        'DEATH': {
            'PERSON_ID': (
                (
                    ('isPrimaryKey', True),
                ), 'See https://github.com/OHDSI/CommonDataModel/issues/770'
            )
        },
        'PROCEDURE_OCCURRENCE': {
            'PROVIDER_ID': (
                (
                    ('isForeignKey', True),  # fkTableName and fkFieldName are already set.
                ),
                'See https://github.com/OHDSI/CommonDataModel/issues/774'
            ),
            'VISIT_OCCURRENCE_ID': (
                (
                    ('isForeignKey', True),  # fkTableName and fkFieldName are already set.
                ),
                'See https://github.com/OHDSI/CommonDataModel/issues/776'
            ),
            'VISIT_DETAIL_ID': (
                (
                    ('isForeignKey', True),  # fkTableName and fkFieldName are already set.
                ),
                'See https://github.com/OHDSI/CommonDataModel/issues/777'
            ),
            'PROCEDURE_SOURCE_CONCEPT_ID': (
                (
                    ('isForeignKey', True),
                    
                ),
                'See https://github.com/OHDSI/CommonDataModel/issues/778'
            )
        }
    }
}
