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
schema_name = 'RESULTS'
metadata_obj = MetaData(schema=schema_name)


class Base(DeclarativeBase):
    metadata = metadata_obj

# TODO: check that no table.name can be equal to "Base".


# From Table CSV row 37.
class cohort(Base):
    """Description:
    The subject of a cohort can have multiple, discrete records in the cohort table per cohort_definition_id, subject_id, and non-overlapping time periods. The definition of the cohort is contained within the COHORT_DEFINITION table. It is listed as part of the RESULTS schema because it is a table that users of the database as well as tools such as ATLAS need to be able to write to. The CDM and Vocabulary tables are all read-only so it is suggested that the COHORT and COHORT_DEFINTION tables are kept in a separate schema to alleviate confusion.
     """

    __tablename__ = 'COHORT'

    __mapper_args__ = {
        'primary_key': ('COHORT_DEFINITION_ID', 'SUBJECT_ID')
    }

    # From Field CSV row 421.
    COHORT_DEFINITION_ID = mapped_column(
        Integer,
        primary_key=True,
        nullable=False
    )

    # From Field CSV row 422.
    SUBJECT_ID = mapped_column(
        Integer,
        primary_key=True,
        nullable=False
    )

    # From Field CSV row 423.
    COHORT_START_DATE = mapped_column(
        Date,
        nullable=False
    )

    # From Field CSV row 424.
    COHORT_END_DATE = mapped_column(
        Date,
        nullable=False
    )


# From Table CSV row 38.
class cohort_definition(Base):
    """Description:
    The COHORT_DEFINITION table contains records defining a Cohort derived from the data through the associated description and syntax and upon instantiation (execution of the algorithm) placed into the COHORT table. Cohorts are a set of subjects that satisfy a given combination of inclusion criteria for a duration of time. The COHORT_DEFINITION table provides a standardized structure for maintaining the rules governing the inclusion of a subject into a cohort, and can store operational programming code to instantiate the cohort within the OMOP Common Data Model.
     """

    __tablename__ = 'COHORT_DEFINITION'

    # From Field CSV row 425.
    COHORT_DEFINITION_ID = mapped_column(
        Integer,
        primary_key=True,
        nullable=False,
        comment="""This is the identifier given to the cohort, usually by the ATLAS application """
    )

    # From Field CSV row 426.
    COHORT_DEFINITION_NAME = mapped_column(
        String(255),
        nullable=False,
        comment="""A short description of the cohort """
    )

    # From Field CSV row 427.
    COHORT_DEFINITION_DESCRIPTION = mapped_column(
        String,
        nullable=True,
        comment="""A complete description of the cohort. """
    )

    # From Field CSV row 428.
    DEFINITION_TYPE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""Type defining what kind of Cohort Definition the record represents and how the syntax may be executed. """
    )

    # From Field CSV row 429.
    COHORT_DEFINITION_SYNTAX = mapped_column(
        String,
        nullable=True,
        comment="""Syntax or code to operationalize the Cohort Definition. """
    )

    # From Field CSV row 430.
    SUBJECT_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""This field contains a Concept that represents the domain of the subjects that are members of the cohort (e.g., Person, Provider, Visit). """
    )

    # From Field CSV row 431.
    COHORT_INITIATION_DATE = mapped_column(
        Date,
        nullable=True,
        comment="""A date to indicate when the Cohort was initiated in the COHORT table. """
    )