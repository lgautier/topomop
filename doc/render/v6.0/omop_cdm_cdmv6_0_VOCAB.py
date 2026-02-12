# Generated from a jinja2 template by topomop.
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column
)

from sqlalchemy import (
    BigInteger,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table
)

cdm_version = 'v6.0'
schema_name = 'VOCAB'
metadata_obj = MetaData(schema=schema_name)


class Base(DeclarativeBase):
    metadata = metadata_obj

# TODO: check that no table.name can be equal to "Base".


# From Table CSV row 26.
class concept(Base):
    """Description:
    The Standardized Vocabularies contains records, or Concepts, that uniquely identify each fundamental unit of meaning used to express clinical information in all domain tables of the CDM. Concepts are derived from vocabularies, which represent clinical information across a domain (e.g. conditions, drugs, procedures) through the use of codes and associated descriptions. Some Concepts are designated Standard Concepts, meaning these Concepts can be used as normative expressions of a clinical entity within the OMOP Common Data Model and within standardized analytics. Each Standard Concept belongs to one domain, which defines the location where the Concept would be expected to occur within data tables of the CDM.

Concepts can represent broad categories (like 'Cardiovascular disease'), detailed clinical elements ('Myocardial infarction of the anterolateral wall') or modifying characteristics and attributes that define Concepts at various levels of detail (severity of a disease, associated morphology, etc.).

Records in the Standardized Vocabularies tables are derived from national or international vocabularies such as SNOMED-CT, RxNorm, and LOINC, or custom Concepts defined to cover various aspects of observational data analysis.
     """

    __tablename__ = 'CONCEPT'

    # From Field CSV row 361.
    CONCEPT_ID = mapped_column(
        Integer,
        primary_key=True,
        nullable=False,
        comment="""A unique identifier for each Concept across all domains. """
    )

    # From Field CSV row 362.
    CONCEPT_NAME = mapped_column(
        String(255),
        nullable=False,
        comment="""An unambiguous, meaningful and descriptive name for the Concept. """
    )

    # From Field CSV row 363.
    DOMAIN_ID = mapped_column(
        String(20),
        ForeignKey('DOMAIN.DOMAIN_ID'),
        nullable=False,
        comment="""A foreign key to the [DOMAIN](https://ohdsi.github.io/CommonDataModel/cdm60.html#domain) table the Concept belongs to. """
    )

    # From Field CSV row 364.
    VOCABULARY_ID = mapped_column(
        String(20),
        ForeignKey('VOCABULARY.VOCABULARY_ID'),
        nullable=False,
        comment="""A foreign key to the [VOCABULARY](https://ohdsi.github.io/CommonDataModel/cdm60.html#vocabulary)
table indicating from which source the
Concept has been adapted. """
    )

    # From Field CSV row 365.
    CONCEPT_CLASS_ID = mapped_column(
        String(20),
        ForeignKey('CONCEPT_CLASS.CONCEPT_CLASS_ID'),
        nullable=False,
        comment="""The attribute or concept class of the
Concept. Examples are 'Clinical Drug',
'Ingredient', 'Clinical Finding' etc. """
    )

    # From Field CSV row 366.
    STANDARD_CONCEPT = mapped_column(
        String(1),
        nullable=True,
        comment="""This flag determines where a Concept is
a Standard Concept, i.e. is used in the
data, a Classification Concept, or a
non-standard Source Concept. The
allowable values are 'S' (Standard
Concept) and 'C' (Classification
Concept), otherwise the content is NULL. """
    )

    # From Field CSV row 367.
    CONCEPT_CODE = mapped_column(
        String(50),
        nullable=False,
        comment="""The concept code represents the identifier
of the Concept in the source vocabulary,
such as SNOMED-CT concept IDs,
RxNorm RXCUIs etc. Note that concept
codes are not unique across vocabularies. """
    )

    # From Field CSV row 368.
    VALID_START_DATE = mapped_column(
        Date,
        nullable=False,
        comment="""The date when the Concept was first
recorded. The default value is
1-Jan-1970, meaning, the Concept has no
(known) date of inception. """
    )

    # From Field CSV row 369.
    VALID_END_DATE = mapped_column(
        Date,
        nullable=False,
        comment="""The date when the Concept became
invalid because it was deleted or
superseded (updated) by a new concept.
The default value is 31-Dec-2099,
meaning, the Concept is valid until it
becomes deprecated. """
    )

    # From Field CSV row 370.
    INVALID_REASON = mapped_column(
        String(1),
        nullable=True,
        comment="""Reason the Concept was invalidated.
Possible values are D (deleted), U
(replaced with an update) or NULL when
valid_end_date has the default value. """
    )


# From Table CSV row 27.
class vocabulary(Base):
    """Description:
    The VOCABULARY table includes a list of the Vocabularies collected from various sources or created de novo by the OMOP community. This reference table is populated with a single record for each Vocabulary source and includes a descriptive name and other associated attributes for the Vocabulary.
     """

    __tablename__ = 'VOCABULARY'

    # From Field CSV row 371.
    VOCABULARY_ID = mapped_column(
        String(20),
        primary_key=True,
        nullable=False,
        comment="""A unique identifier for each Vocabulary, such
as ICD9CM, SNOMED, Visit. """
    )

    # From Field CSV row 372.
    VOCABULARY_NAME = mapped_column(
        String(255),
        nullable=False,
        comment="""The name describing the vocabulary, for
example International Classification of
Diseases, Ninth Revision, Clinical
Modification, Volume 1 and 2 (NCHS) etc. """
    )

    # From Field CSV row 373.
    VOCABULARY_REFERENCE = mapped_column(
        String(255),
        nullable=False,
        comment="""External reference to documentation or
available download of the about the
vocabulary. """
    )

    # From Field CSV row 374.
    VOCABULARY_VERSION = mapped_column(
        String(255),
        nullable=True,
        comment="""Version of the Vocabulary as indicated in
the source. """
    )

    # From Field CSV row 375.
    VOCABULARY_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""A Concept that represents the Vocabulary the VOCABULARY record belongs to. """
    )


# From Table CSV row 28.
class domain(Base):
    """Description:
    The DOMAIN table includes a list of OMOP-defined Domains the Concepts of the Standardized Vocabularies can belong to. A Domain defines the set of allowable Concepts for the standardized fields in the CDM tables. For example, the "Condition" Domain contains Concepts that describe a condition of a patient, and these Concepts can only be stored in the condition_concept_id field of the CONDITION_OCCURRENCE and CONDITION_ERA tables. This reference table is populated with a single record for each Domain and includes a descriptive name for the Domain.
     """

    __tablename__ = 'DOMAIN'

    # From Field CSV row 376.
    DOMAIN_ID = mapped_column(
        String(20),
        primary_key=True,
        nullable=False,
        comment="""A unique key for each domain. """
    )

    # From Field CSV row 377.
    DOMAIN_NAME = mapped_column(
        String(255),
        nullable=False,
        comment="""The name describing the Domain, e.g.
Condition, Procedure, Measurement
etc. """
    )

    # From Field CSV row 378.
    DOMAIN_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""A Concept representing the Domain Concept the DOMAIN record belongs to. """
    )


# From Table CSV row 29.
class concept_class(Base):
    """Description:
    The CONCEPT_CLASS table is a reference table, which includes a list of the classifications used to differentiate Concepts within a given Vocabulary. This reference table is populated with a single record for each Concept Class.
     """

    __tablename__ = 'CONCEPT_CLASS'

    # From Field CSV row 379.
    CONCEPT_CLASS_ID = mapped_column(
        String(20),
        primary_key=True,
        nullable=False,
        comment="""A unique key for each class. """
    )

    # From Field CSV row 380.
    CONCEPT_CLASS_NAME = mapped_column(
        String(255),
        nullable=False,
        comment="""The name describing the Concept Class, e.g.
Clinical Finding, Ingredient, etc. """
    )

    # From Field CSV row 381.
    CONCEPT_CLASS_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""A Concept that represents the Concept Class. """
    )


# From Table CSV row 30.
class concept_relationship(Base):
    """Description:
    The CONCEPT_RELATIONSHIP table contains records that define direct relationships between any two Concepts and the nature or type of the relationship. Each type of a relationship is defined in the RELATIONSHIP table.
     """

    __tablename__ = 'CONCEPT_RELATIONSHIP'

    __mapper_args__ = {
        'primary_key': ('CONCEPT_ID_1', 'CONCEPT_ID_2', 'RELATIONSHIP_ID', 'VALID_START_DATE', 'VALID_END_DATE')
    }

    # From Field CSV row 382.
    CONCEPT_ID_1 = mapped_column(
        Integer,
        ForeignKey('CONCEPT.CONCEPT_ID'),
        primary_key=True,
        nullable=False
    )

    # From Field CSV row 383.
    CONCEPT_ID_2 = mapped_column(
        Integer,
        ForeignKey('CONCEPT.CONCEPT_ID'),
        primary_key=True,
        nullable=False
    )

    # From Field CSV row 384.
    RELATIONSHIP_ID = mapped_column(
        String(20),
        ForeignKey('RELATIONSHIP.RELATIONSHIP_ID'),
        primary_key=True,
        nullable=False,
        comment="""The relationship between CONCEPT_ID_1 and CONCEPT_ID_2. Please see the [Vocabulary Conventions](https://ohdsi.github.io/CommonDataModel/dataModelConventions.html#concept_relationships). for more information. """
    )

    # From Field CSV row 385.
    VALID_START_DATE = mapped_column(
        Date,
        primary_key=True,
        nullable=False,
        comment="""The date when the relationship is first recorded. """
    )

    # From Field CSV row 386.
    VALID_END_DATE = mapped_column(
        Date,
        primary_key=True,
        nullable=False,
        comment="""The date when the relationship is invalidated. """
    )

    # From Field CSV row 387.
    INVALID_REASON = mapped_column(
        String(1),
        nullable=True,
        comment="""Reason the relationship was invalidated. Possible values are 'D' (deleted), 'U' (updated) or NULL. """
    )


# From Table CSV row 31.
class relationship(Base):
    """Description:
    The RELATIONSHIP table provides a reference list of all types of relationships that can be used to associate any two Concepts in the CONCEPT_RELATIONSHIP table, the respective reverse relationships, and their hierarchical characteristics. Note, that Concepts representing relationships between the clinical facts, used for filling in the FACT_RELATIONSHIP table are stored in the CONCEPT table and belong to the Relationship Domain.

    User guidance:     
    Users can leverage the RELATIONSHIP table to explore the full list of direct and reverse relationships within the OMOP vocabulary system. Also, users can get insight into how these relationships can be used in ETL, cohort creation, and other tasks according to their ancestral characteristics.
     """

    __tablename__ = 'RELATIONSHIP'

    # From Field CSV row 388.
    RELATIONSHIP_ID = mapped_column(
        String(20),
        primary_key=True,
        nullable=False
    )

    # From Field CSV row 389.
    RELATIONSHIP_NAME = mapped_column(
        String(255),
        nullable=False
    )

    # From Field CSV row 390.
    IS_HIERARCHICAL = mapped_column(
        String(1),
        nullable=False
    )

    # From Field CSV row 391.
    DEFINES_ANCESTRY = mapped_column(
        String(1),
        nullable=False
    )

    # From Field CSV row 392.
    REVERSE_RELATIONSHIP_ID = mapped_column(
        String(20),
        nullable=False
    )

    # From Field CSV row 393.
    RELATIONSHIP_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('CONCEPT.CONCEPT_ID'),
        nullable=False
    )


# From Table CSV row 32.
class concept_synonym(Base):
    """Description:
    The CONCEPT_SYNONYM table captures alternative terms, synonyms, and translations of Concept Name into various languages linked to specific concepts, providing users with a comprehensive view of how Concepts may be expressed or referenced.

    User guidance:     
    Users can leverage the CONCEPT_SYNONYM table to expand search capabilities and improve query accuracy by incorporating synonymous terms into data analysis and retrieval processes. Also, users can enhance their mapping efforts between local terminologies and standardized concepts by identifying synonymous terms associated with concepts in the CONCEPT_SYNONYM table.
     """

    __tablename__ = 'CONCEPT_SYNONYM'

    __mapper_args__ = {
        'primary_key': ('CONCEPT_ID', 'CONCEPT_SYNONYM_NAME', 'LANGUAGE_CONCEPT_ID')
    }

    # From Field CSV row 394.
    CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('CONCEPT.CONCEPT_ID'),
        primary_key=True,
        nullable=False
    )

    # From Field CSV row 395.
    CONCEPT_SYNONYM_NAME = mapped_column(
        String(1000),
        primary_key=True,
        nullable=False
    )

    # From Field CSV row 396.
    LANGUAGE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('CONCEPT.CONCEPT_ID'),
        primary_key=True,
        nullable=False
    )


# From Table CSV row 33.
class concept_ancestor(Base):
    """Description:
    The CONCEPT_ANCESTOR table is designed to simplify observational analysis by providing the complete hierarchical relationships between Concepts. Only direct parent-child relationships between Concepts are stored in the CONCEPT_RELATIONSHIP table. To determine higher-level ancestry connections, all individual direct relationships would have to be navigated at analysis time. The CONCEPT_ANCESTOR table includes records for all parent-child relationships, as well as grandparent-grandchild relationships and those of any other level of lineage for Standard or Classification concepts. Using the CONCEPT_ANCESTOR table allows for querying for all descendants of a hierarchical concept, and the other way around. For example, drug ingredients and drug products, beneath them in the hierarchy, are all descendants of a drug class ancestor. This table is entirely derived from the CONCEPT, CONCEPT_RELATIONSHIP, and RELATIONSHIP tables.

    User guidance:     
    The CONCEPT_ANCESTOR table can be used to explore the hierarchical relationships captured in the table to gain insights into the hierarchical structure of clinical concepts. Understanding the hierarchical relationships of concepts can facilitate accurate interpretation and analysis of healthcare data. Also, by incorporating hierarchical relationships from the CONCEPT_ANCESTOR table, users can create cohorts containing related concepts within a hierarchical structure, enabling more comprehensive cohort definitions.
     """

    __tablename__ = 'CONCEPT_ANCESTOR'

    __mapper_args__ = {
        'primary_key': ('ANCESTOR_CONCEPT_ID', 'DESCENDANT_CONCEPT_ID')
    }

    # From Field CSV row 397.
    ANCESTOR_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('CONCEPT.CONCEPT_ID'),
        primary_key=True,
        nullable=False,
        comment="""The Concept Id for the higher-level concept
that forms the ancestor in the relationship. """
    )

    # From Field CSV row 398.
    DESCENDANT_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('CONCEPT.CONCEPT_ID'),
        primary_key=True,
        nullable=False,
        comment="""The Concept Id for the lower-level concept
that forms the descendant in the
relationship. """
    )

    # From Field CSV row 399.
    MIN_LEVELS_OF_SEPARATION = mapped_column(
        Integer,
        nullable=False,
        comment="""The minimum separation in number of
levels of hierarchy between ancestor and
descendant concepts. This is an attribute
that is used to simplify hierarchic analysis. """
    )

    # From Field CSV row 400.
    MAX_LEVELS_OF_SEPARATION = mapped_column(
        Integer,
        nullable=False,
        comment="""The maximum separation in number of
levels of hierarchy between ancestor and
descendant concepts. This is an attribute
that is used to simplify hierarchic analysis. """
    )


# From Table CSV row 34.
class source_to_concept_map(Base):
    """Description:
    The source to concept map table is a legacy data structure within the OMOP Common Data Model, recommended for use in ETL processes to maintain local source codes which are not available as Concepts in the Standardized Vocabularies, and to establish mappings for each source code into a Standard Concept as target_concept_ids that can be used to populate the Common Data Model tables. The SOURCE_TO_CONCEPT_MAP table is no longer populated with content within the Standardized Vocabularies published to the OMOP community.
     """

    __tablename__ = 'SOURCE_TO_CONCEPT_MAP'

    __mapper_args__ = {
        'primary_key': ('SOURCE_CONCEPT_ID', 'SOURCE_VOCABULARY_ID', 'TARGET_CONCEPT_ID', 'TARGET_VOCABULARY_ID', 'VALID_START_DATE', 'VALID_END_DATE', 'INVALID_REASON')
    }

    # From Field CSV row 401.
    SOURCE_CODE = mapped_column(
        String(50),
        nullable=False,
        comment="""The source code being translated
into a Standard Concept. """
    )

    # From Field CSV row 402.
    SOURCE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('CONCEPT.CONCEPT_ID'),
        primary_key=True,
        nullable=False,
        comment="""A foreign key to the Source
Concept that is being translated
into a Standard Concept. """
    )

    # From Field CSV row 403.
    SOURCE_VOCABULARY_ID = mapped_column(
        String(20),
        primary_key=True,
        nullable=False,
        comment="""A foreign key to the
VOCABULARY table defining the
vocabulary of the source code that
is being translated to a Standard
Concept. """
    )

    # From Field CSV row 404.
    SOURCE_CODE_DESCRIPTION = mapped_column(
        String(255),
        nullable=True,
        comment="""An optional description for the
source code. This is included as a
convenience to compare the
description of the source code to
the name of the concept. """
    )

    # From Field CSV row 405.
    TARGET_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('CONCEPT.CONCEPT_ID'),
        primary_key=True,
        nullable=False,
        comment="""The target Concept
to which the source code is being
mapped. """
    )

    # From Field CSV row 406.
    TARGET_VOCABULARY_ID = mapped_column(
        String(20),
        ForeignKey('VOCABULARY.VOCABULARY_ID'),
        primary_key=True,
        nullable=False,
        comment="""The Vocabulary of the target Concept. """
    )

    # From Field CSV row 407.
    VALID_START_DATE = mapped_column(
        Date,
        primary_key=True,
        nullable=False,
        comment="""The date when the mapping
instance was first recorded. """
    )

    # From Field CSV row 408.
    VALID_END_DATE = mapped_column(
        Date,
        primary_key=True,
        nullable=False,
        comment="""The date when the mapping
instance became invalid because it
was deleted or superseded
(updated) by a new relationship.
Default value is 31-Dec-2099. """
    )

    # From Field CSV row 409.
    INVALID_REASON = mapped_column(
        String(1),
        primary_key=True,
        nullable=False,
        comment="""Reason the mapping instance was
invalidated. Possible values are D
(deleted), U (replaced with an
update) or NULL when
valid_end_date has the default
value. """
    )


# From Table CSV row 35.
class drug_strength(Base):
    """Description:
    The DRUG_STRENGTH table contains structured content about the amount or concentration and associated units of a specific ingredient contained within a particular drug product. This table is supplemental information to support standardized analysis of drug utilization.
     """

    __tablename__ = 'DRUG_STRENGTH'

    DRUG_STRENGTH_ID = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    # From Field CSV row 410.
    DRUG_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""The Concept representing the Branded Drug or Clinical Drug Product. """
    )

    # From Field CSV row 411.
    INGREDIENT_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""The Concept representing the active ingredient contained within the drug product. """
    )

    # From Field CSV row 412.
    AMOUNT_VALUE = mapped_column(
        Float,
        nullable=True,
        comment="""The numeric value or the amount of active ingredient contained within the drug product. """
    )

    # From Field CSV row 413.
    AMOUNT_UNIT_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""The Concept representing the Unit of measure for the amount of active ingredient contained within the drug product. """
    )

    # From Field CSV row 414.
    NUMERATOR_VALUE = mapped_column(
        Float,
        nullable=True,
        comment="""The concentration of the active ingredient contained within the drug product. """
    )

    # From Field CSV row 415.
    NUMERATOR_UNIT_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""The Concept representing the Unit of measure for the concentration of active ingredient. """
    )

    # From Field CSV row 416.
    DENOMINATOR_VALUE = mapped_column(
        Float,
        nullable=True,
        comment="""The amount of total liquid (or other divisible product, such as ointment, gel, spray, etc.). """
    )

    # From Field CSV row 417.
    DENOMINATOR_UNIT_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""The Concept representing the denominator unit for the concentration of active ingredient. """
    )

    # From Field CSV row 418.
    BOX_SIZE = mapped_column(
        Integer,
        nullable=True,
        comment="""The number of units of Clinical Branded Drug or Quantified Clinical or Branded Drug contained in a box as dispensed to the patient. """
    )

    # From Field CSV row 419.
    VALID_START_DATE = mapped_column(
        Date,
        nullable=False,
        comment="""The date when the Concept was first
recorded. The default value is
1-Jan-1970. """
    )

    # From Field CSV row 420.
    VALID_END_DATE = mapped_column(
        Date,
        nullable=False,
        comment="""The date when then Concept became invalid. """
    )

    # From Field CSV row 421.
    INVALID_REASON = mapped_column(
        String(1),
        nullable=True,
        comment="""Reason the concept was invalidated. Possible values are D (deleted), U (replaced with an update) or NULL when valid_end_date has the default value. """
    )


# From Table CSV row 37.
class cohort_definition(Base):
    """Description:
    The COHORT_DEFINITION table contains records defining a Cohort derived from the data through the associated description and syntax and upon instantiation (execution of the algorithm) placed into the COHORT table. Cohorts are a set of subjects that satisfy a given combination of inclusion criteria for a duration of time. The COHORT_DEFINITION table provides a standardized structure for maintaining the rules governing the inclusion of a subject into a cohort, and can store operational programming code to instantiate the cohort within the OMOP Common Data Model.
     """

    __tablename__ = 'COHORT_DEFINITION'

    # From Field CSV row 426.
    COHORT_DEFINITION_ID = mapped_column(
        Integer,
        primary_key=True,
        nullable=False,
        comment="""This is the identifier given to the cohort, usually by the ATLAS application """
    )

    # From Field CSV row 427.
    COHORT_DEFINITION_NAME = mapped_column(
        String(255),
        nullable=False,
        comment="""A short description of the cohort """
    )

    # From Field CSV row 428.
    COHORT_DEFINITION_DESCRIPTION = mapped_column(
        String,
        nullable=True,
        comment="""A complete description of the cohort. """
    )

    # From Field CSV row 429.
    DEFINITION_TYPE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""Type defining what kind of Cohort Definition the record represents and how the syntax may be executed. """
    )

    # From Field CSV row 430.
    COHORT_DEFINITION_SYNTAX = mapped_column(
        String,
        nullable=True,
        comment="""Syntax or code to operationalize the Cohort Definition. """
    )

    # From Field CSV row 431.
    SUBJECT_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""This field contains a Concept that represents the domain of the subjects that are members of the cohort (e.g., Person, Provider, Visit). """
    )

    # From Field CSV row 432.
    COHORT_INITIATION_DATE = mapped_column(
        Date,
        nullable=True,
        comment="""A date to indicate when the Cohort was initiated in the COHORT table. """
    )