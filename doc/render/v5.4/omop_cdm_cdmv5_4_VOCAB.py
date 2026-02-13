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

cdm_version = 'v5.4'
schema_name = 'VOCAB'
metadata_obj = MetaData(schema=schema_name)


class Base(DeclarativeBase):
    metadata = metadata_obj

# TODO: check that no table.name can be equal to "Base".


# From Table CSV row 27.
class concept(Base):
    """Description:
    The Standardized Vocabularies contains records, or Concepts, that uniquely identify each fundamental unit of meaning used to express clinical information in all domain tables of the CDM. Concepts are derived from vocabularies, which represent clinical information across a domain (e.g. conditions, drugs, procedures) through the use of codes and associated descriptions. Some Concepts are designated Standard Concepts, meaning these Concepts can be used as normative expressions of a clinical entity within the OMOP Common Data Model and standardized analytics. Each Standard Concept belongs to one Domain, which defines the location where the Concept would be expected to occur within the data tables of the CDM. Concepts can represent broad categories ('Cardiovascular disease'), detailed clinical elements ('Myocardial infarction of the anterolateral wall'), or modifying characteristics and attributes that define Concepts at various levels of detail (severity of a disease, associated morphology, etc.). Records in the Standardized Vocabularies tables are derived from national or international vocabularies such as SNOMED-CT, RxNorm, and LOINC, or custom OMOP Concepts defined to cover various aspects of observational data analysis.

    User guidance:     
    The primary purpose of the CONCEPT table is to provide a standardized representation of medical Concepts, allowing for consistent querying and analysis across the healthcare databases. Users can join the CONCEPT table with other tables in the CDM to enrich clinical data with standardized Concept information or use the CONCEPT table as a reference for mapping clinical data from source terminologies to Standard Concepts.
     """

    __tablename__ = 'CONCEPT'

    # From Field CSV row 360.
    CONCEPT_ID = mapped_column(
        Integer,
        primary_key=True,
        nullable=False,
        comment="""A unique identifier for each Concept across all domains. """
    )

    # From Field CSV row 361.
    CONCEPT_NAME = mapped_column(
        String(255),
        nullable=False,
        comment="""An unambiguous, meaningful and descriptive name for the Concept. """
    )

    # From Field CSV row 362.
    DOMAIN_ID = mapped_column(
        String(20),
        ForeignKey('DOMAIN.DOMAIN_ID'),
        nullable=False,
        comment="""A foreign key to the [DOMAIN](https://ohdsi.github.io/CommonDataModel/cdm54.html#domain) table the Concept belongs to. """
    )

    # From Field CSV row 363.
    VOCABULARY_ID = mapped_column(
        String(20),
        ForeignKey('VOCABULARY.VOCABULARY_ID'),
        nullable=False,
        comment="""A foreign key to the [VOCABULARY](https://ohdsi.github.io/CommonDataModel/cdm54.html#vocabulary)
table indicating from which source the
Concept has been adapted. """
    )

    # From Field CSV row 364.
    CONCEPT_CLASS_ID = mapped_column(
        String(20),
        ForeignKey('CONCEPT_CLASS.CONCEPT_CLASS_ID'),
        nullable=False,
        comment="""The attribute or concept class of the
Concept. Examples are 'Clinical Drug',
'Ingredient', 'Clinical Finding' etc. """
    )

    # From Field CSV row 365.
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

    # From Field CSV row 366.
    CONCEPT_CODE = mapped_column(
        String(50),
        nullable=False,
        comment="""The concept code represents the identifier
of the Concept in the source vocabulary,
such as SNOMED-CT concept IDs,
RxNorm RXCUIs etc. Note that concept
codes are not unique across vocabularies. """
    )

    # From Field CSV row 367.
    VALID_START_DATE = mapped_column(
        Date,
        nullable=False,
        comment="""The date when the Concept was first
recorded. The default value is
1-Jan-1970, meaning, the Concept has no
(known) date of inception. """
    )

    # From Field CSV row 368.
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

    # From Field CSV row 369.
    INVALID_REASON = mapped_column(
        String(1),
        nullable=True,
        comment="""Reason the Concept was invalidated.
Possible values are D (deleted), U
(replaced with an update) or NULL when
valid_end_date has the default value. """
    )


# From Table CSV row 28.
class vocabulary(Base):
    """Description:
    The VOCABULARY table includes a list of the Vocabularies integrated from various sources or created de novo in OMOP CDM. This reference table contains a single record for each Vocabulary and includes a descriptive name and other associated attributes for the Vocabulary.

    User guidance:     
    The primary purpose of the VOCABULARY table is to provide explicit information about specific vocabulary versions and the references to the sources from which they are asserted. Users can identify the version of a particular vocabulary used in the database, enabling consistency and reproducibility in data analysis. Besides, users can check the vocabulary release version in their CDM which refers to the vocabulary_id = 'None'.
     """

    __tablename__ = 'VOCABULARY'

    # From Field CSV row 370.
    VOCABULARY_ID = mapped_column(
        String(20),
        primary_key=True,
        nullable=False,
        comment="""A unique identifier for each Vocabulary, such
as ICD9CM, SNOMED, Visit. """
    )

    # From Field CSV row 371.
    VOCABULARY_NAME = mapped_column(
        String(255),
        nullable=False,
        comment="""The name describing the vocabulary, for
example, International Classification of
Diseases, Ninth Revision, Clinical
Modification, Volume 1 and 2 (NCHS) etc. """
    )

    # From Field CSV row 372.
    VOCABULARY_REFERENCE = mapped_column(
        String(255),
        nullable=True,
        comment="""External reference to documentation or
available download of the about the
vocabulary. """
    )

    # From Field CSV row 373.
    VOCABULARY_VERSION = mapped_column(
        String(255),
        nullable=True,
        comment="""Version of the Vocabulary as indicated in
the source. """
    )

    # From Field CSV row 374.
    VOCABULARY_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""A Concept that represents the Vocabulary the VOCABULARY record belongs to. """
    )


# From Table CSV row 29.
class domain(Base):
    """Description:
    The DOMAIN table includes a list of OMOP-defined Domains to which the Concepts of the Standardized Vocabularies can belong. A Domain represents a clinical definition whereby we assign matching Concepts for the standardized fields in the CDM tables. For example, the Condition Domain contains Concepts that describe a patient condition, and these Concepts can only be used in the condition_concept_id field of the CONDITION_OCCURRENCE and CONDITION_ERA tables. This reference table is populated with a single record for each Domain, including a Domain ID and a descriptive name for every Domain.

    User guidance:     
    Users can leverage the DOMAIN table to explore the full spectrum of health-related data Domains available in the Standardized Vocabularies. Also, the information in the DOMAIN table may be used as a reference for mapping source data to OMOP domains, facilitating data harmonization and interoperability.
     """

    __tablename__ = 'DOMAIN'

    # From Field CSV row 375.
    DOMAIN_ID = mapped_column(
        String(20),
        primary_key=True,
        nullable=False,
        comment="""A unique key for each domain. """
    )

    # From Field CSV row 376.
    DOMAIN_NAME = mapped_column(
        String(255),
        nullable=False,
        comment="""The name describing the Domain, e.g.
Condition, Procedure, Measurement
etc. """
    )

    # From Field CSV row 377.
    DOMAIN_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""A Concept representing the Domain Concept the DOMAIN record belongs to. """
    )


# From Table CSV row 30.
class concept_class(Base):
    """Description:
    The CONCEPT_CLASS table includes semantic categories that reference the source structure of each Vocabulary. Concept Classes represent so-called horizontal (e.g. MedDRA, RxNorm) or vertical levels (e.g. SNOMED) of the vocabulary structure. Vocabularies without any Concept Classes, such as HCPCS, use the vocabulary_id as the Concept Class. This reference table is populated with a single record for each Concept Class, which includes a Concept Class ID and a fully specified Concept Class name.


    User guidance:     
    Users can utilize the CONCEPT_CLASS table to explore the different classes or categories of concepts within the OHDSI vocabularies.
     """

    __tablename__ = 'CONCEPT_CLASS'

    # From Field CSV row 378.
    CONCEPT_CLASS_ID = mapped_column(
        String(20),
        primary_key=True,
        nullable=False,
        comment="""A unique key for each class. """
    )

    # From Field CSV row 379.
    CONCEPT_CLASS_NAME = mapped_column(
        String(255),
        nullable=False,
        comment="""The name describing the Concept Class, e.g.
Clinical Finding, Ingredient, etc. """
    )

    # From Field CSV row 380.
    CONCEPT_CLASS_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""A Concept that represents the Concept Class. """
    )


# From Table CSV row 31.
class concept_relationship(Base):
    """Description:
    The CONCEPT_RELATIONSHIP table contains records that define relationships between any two Concepts and the nature or type of the relationship. This table captures various types of relationships, including hierarchical, associative, and other semantic connections, enabling comprehensive analysis and interpretation of clinical concepts. Every kind of relationship is defined in the RELATIONSHIP table.

    User guidance:     
    The CONCEPT_RELATIONSHIP table can be used to explore hierarchical or attribute relationships between concepts to understand the hierarchical structure of clinical concepts and uncover implicit connections and associations within healthcare data. For example, users can utilize mapping relationships ('Maps to') to harmonize data from different sources and terminologies, enabling interoperability and data integration across disparate datasets.
     """

    __tablename__ = 'CONCEPT_RELATIONSHIP'

    __mapper_args__ = {
        'primary_key': ('CONCEPT_ID_1', 'CONCEPT_ID_2', 'RELATIONSHIP_ID', 'VALID_START_DATE', 'VALID_END_DATE')
    }

    # From Field CSV row 381.
    CONCEPT_ID_1 = mapped_column(
        Integer,
        ForeignKey('CONCEPT.CONCEPT_ID'),
        primary_key=True,
        nullable=False
    )

    # From Field CSV row 382.
    CONCEPT_ID_2 = mapped_column(
        Integer,
        ForeignKey('CONCEPT.CONCEPT_ID'),
        primary_key=True,
        nullable=False
    )

    # From Field CSV row 383.
    RELATIONSHIP_ID = mapped_column(
        String(20),
        ForeignKey('RELATIONSHIP.RELATIONSHIP_ID'),
        primary_key=True,
        nullable=False,
        comment="""The relationship between CONCEPT_ID_1 and CONCEPT_ID_2. Please see the [Vocabulary Conventions](https://ohdsi.github.io/CommonDataModel/dataModelConventions.html#concept_relationships). for more information. """
    )

    # From Field CSV row 384.
    VALID_START_DATE = mapped_column(
        Date,
        primary_key=True,
        nullable=False,
        comment="""The date when the relationship is first recorded. """
    )

    # From Field CSV row 385.
    VALID_END_DATE = mapped_column(
        Date,
        primary_key=True,
        nullable=False,
        comment="""The date when the relationship is invalidated. """
    )

    # From Field CSV row 386.
    INVALID_REASON = mapped_column(
        String(1),
        nullable=True,
        comment="""Reason the relationship was invalidated. Possible values are 'D' (deleted), 'U' (updated) or NULL. """
    )


# From Table CSV row 32.
class relationship(Base):
    """Description:
    The RELATIONSHIP table provides a reference list of all types of relationships that can be used to associate any two Concepts in the CONCEPT_RELATIONSHIP table, the respective reverse relationships, and their hierarchical characteristics. Note, that Concepts representing relationships between the clinical facts, used for filling in the FACT_RELATIONSHIP table are stored in the CONCEPT table and belong to the Relationship Domain.

    User guidance:     
    Users can leverage the RELATIONSHIP table to explore the full list of direct and reverse relationships within the OMOP vocabulary system. Also, users can get insight into how these relationships can be used in ETL, cohort creation, and other tasks according to their ancestral characteristics.
     """

    __tablename__ = 'RELATIONSHIP'

    # From Field CSV row 387.
    RELATIONSHIP_ID = mapped_column(
        String(20),
        primary_key=True,
        nullable=False,
        comment="""The type of relationship captured by the
relationship record. """
    )

    # From Field CSV row 388.
    RELATIONSHIP_NAME = mapped_column(
        String(255),
        nullable=False
    )

    # From Field CSV row 389.
    IS_HIERARCHICAL = mapped_column(
        String(1),
        nullable=False,
        comment="""Defines whether a relationship defines
concepts into classes or hierarchies. Values
are 1 for hierarchical relationship or 0 if not. """
    )

    # From Field CSV row 390.
    DEFINES_ANCESTRY = mapped_column(
        String(1),
        nullable=False,
        comment="""Defines whether a hierarchical relationship
contributes to the concept_ancestor table.
These are subsets of the hierarchical
relationships. Valid values are 1 or 0. """
    )

    # From Field CSV row 391.
    REVERSE_RELATIONSHIP_ID = mapped_column(
        String(20),
        nullable=False,
        comment="""The identifier for the relationship used to
define the reverse relationship between two
concepts. """
    )

    # From Field CSV row 392.
    RELATIONSHIP_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""A foreign key that refers to an identifier in
the [CONCEPT](https://ohdsi.github.io/CommonDataModel/cdm54.html#concept) table for the unique
relationship concept. """
    )


# From Table CSV row 33.
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

    # From Field CSV row 393.
    CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('CONCEPT.CONCEPT_ID'),
        primary_key=True,
        nullable=False
    )

    # From Field CSV row 394.
    CONCEPT_SYNONYM_NAME = mapped_column(
        String(1000),
        primary_key=True,
        nullable=False
    )

    # From Field CSV row 395.
    LANGUAGE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('CONCEPT.CONCEPT_ID'),
        primary_key=True,
        nullable=False
    )


# From Table CSV row 34.
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

    # From Field CSV row 396.
    ANCESTOR_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('CONCEPT.CONCEPT_ID'),
        primary_key=True,
        nullable=False,
        comment="""The Concept Id for the higher-level concept
that forms the ancestor in the relationship. """
    )

    # From Field CSV row 397.
    DESCENDANT_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('CONCEPT.CONCEPT_ID'),
        primary_key=True,
        nullable=False,
        comment="""The Concept Id for the lower-level concept
that forms the descendant in the
relationship. """
    )

    # From Field CSV row 398.
    MIN_LEVELS_OF_SEPARATION = mapped_column(
        Integer,
        nullable=False,
        comment="""The minimum separation in number of
levels of hierarchy between ancestor and
descendant concepts. This is an attribute
that is used to simplify hierarchic analysis. """
    )

    # From Field CSV row 399.
    MAX_LEVELS_OF_SEPARATION = mapped_column(
        Integer,
        nullable=False,
        comment="""The maximum separation in number of
levels of hierarchy between ancestor and
descendant concepts. This is an attribute
that is used to simplify hierarchic analysis. """
    )


# From Table CSV row 35.
class source_to_concept_map(Base):
    """Description:
    The source to concept map table is recommended for use in ETL processes to maintain local source codes which are not available as Concepts in the Standardized Vocabularies, and to establish mappings for each source code into a Standard Concept as target_concept_ids that can be used to populate the Common Data Model tables. The SOURCE_TO_CONCEPT_MAP table is no longer populated with content within the Standardized Vocabularies published to the OMOP community. **There are OHDSI tools to help you populate this table; [Usagi](https://github.com/OHDSI/Usagi) and [Perseus](https://github.com/ohdsi/Perseus). You can read more about OMOP vocabulary mapping in [The Book of OHDSI Chapter 6.3](https://ohdsi.github.io/TheBookOfOhdsi/ExtractTransformLoad.html#step-2-create-the-code-mappings).**
     """

    __tablename__ = 'SOURCE_TO_CONCEPT_MAP'

    __mapper_args__ = {
        'primary_key': ('SOURCE_CONCEPT_ID', 'SOURCE_VOCABULARY_ID', 'TARGET_CONCEPT_ID', 'TARGET_VOCABULARY_ID', 'VALID_START_DATE', 'VALID_END_DATE', 'INVALID_REASON')
    }

    # From Field CSV row 400.
    SOURCE_CODE = mapped_column(
        String(50),
        nullable=False,
        comment="""The source code being translated
into a Standard Concept. """
    )

    # From Field CSV row 401.
    SOURCE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('CONCEPT.CONCEPT_ID'),
        primary_key=True,
        nullable=False,
        comment="""A foreign key to the Source
Concept that is being translated
into a Standard Concept. """
    )

    # From Field CSV row 402.
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

    # From Field CSV row 403.
    SOURCE_CODE_DESCRIPTION = mapped_column(
        String(255),
        nullable=True,
        comment="""An optional description for the
source code. This is included as a
convenience to compare the
description of the source code to
the name of the concept. """
    )

    # From Field CSV row 404.
    TARGET_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('CONCEPT.CONCEPT_ID'),
        primary_key=True,
        nullable=False,
        comment="""The target Concept
to which the source code is being
mapped. """
    )

    # From Field CSV row 405.
    TARGET_VOCABULARY_ID = mapped_column(
        String(20),
        ForeignKey('VOCABULARY.VOCABULARY_ID'),
        primary_key=True,
        nullable=False,
        comment="""The Vocabulary of the target Concept. """
    )

    # From Field CSV row 406.
    VALID_START_DATE = mapped_column(
        Date,
        primary_key=True,
        nullable=False,
        comment="""The date when the mapping
instance was first recorded. """
    )

    # From Field CSV row 407.
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

    # From Field CSV row 408.
    INVALID_REASON = mapped_column(
        String(1),
        primary_key=True,
        nullable=False,
        comment="""Reason the mapping instance was invalidated. Possible values are D (deleted), U (replaced with an update) or NULL when valid_end_date has the default value. """
    )


# From Table CSV row 36.
class drug_strength(Base):
    """Description:
    The DRUG_STRENGTH table contains structured content about the amount or concentration and associated units of a specific ingredient contained within a particular drug product. This table is supplemental information to support standardized analysis of drug utilization.
     """

    __tablename__ = 'DRUG_STRENGTH'

    DRUG_STRENGTH_ID = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )

    # From Field CSV row 409.
    DRUG_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""The Concept representing the Branded Drug or Clinical Drug Product. """
    )

    # From Field CSV row 410.
    INGREDIENT_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""The Concept representing the active ingredient contained within the drug product. """
    )

    # From Field CSV row 411.
    AMOUNT_VALUE = mapped_column(
        Float,
        nullable=True,
        comment="""The numeric value or the amount of active ingredient contained within the drug product. """
    )

    # From Field CSV row 412.
    AMOUNT_UNIT_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""The Concept representing the Unit of measure for the amount of active ingredient contained within the drug product. """
    )

    # From Field CSV row 413.
    NUMERATOR_VALUE = mapped_column(
        Float,
        nullable=True,
        comment="""The concentration of the active ingredient contained within the drug product. """
    )

    # From Field CSV row 414.
    NUMERATOR_UNIT_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""The Concept representing the Unit of measure for the concentration of active ingredient. """
    )

    # From Field CSV row 415.
    DENOMINATOR_VALUE = mapped_column(
        Float,
        nullable=True,
        comment="""The amount of total liquid (or other divisible product, such as ointment, gel, spray, etc.). """
    )

    # From Field CSV row 416.
    DENOMINATOR_UNIT_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""The Concept representing the denominator unit for the concentration of active ingredient. """
    )

    # From Field CSV row 417.
    BOX_SIZE = mapped_column(
        Integer,
        nullable=True,
        comment="""The number of units of Clinical Branded Drug or Quantified Clinical or Branded Drug contained in a box as dispensed to the patient. """
    )

    # From Field CSV row 418.
    VALID_START_DATE = mapped_column(
        Date,
        nullable=False,
        comment="""The date when the Concept was first
recorded. The default value is
1-Jan-1970. """
    )

    # From Field CSV row 419.
    VALID_END_DATE = mapped_column(
        Date,
        nullable=False,
        comment="""The date when then Concept became invalid. """
    )

    # From Field CSV row 420.
    INVALID_REASON = mapped_column(
        String(1),
        nullable=True,
        comment="""Reason the concept was invalidated. Possible values are D (deleted), U (replaced with an update) or NULL when valid_end_date has the default value. """
    )