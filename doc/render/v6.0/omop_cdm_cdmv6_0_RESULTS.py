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
schema_name = 'RESULTS'
metadata_obj = MetaData(schema=schema_name)


class Base(DeclarativeBase):
    metadata = metadata_obj

# TODO: check that no table.name can be equal to "Base".


# From Table CSV row 36.
class cohort(Base):
    """Description:
    The COHORT table contains records of subjects that satisfy a given set of criteria for a duration of time. The definition of the cohort is contained within the COHORT_DEFINITION table. It is listed as part of the RESULTS schema because it is a table that users of the database as well as tools such as ATLAS need to be able to write to. The CDM and Vocabulary tables are all read-only so it is suggested that the COHORT and COHORT_DEFINTION tables are kept in a separate schema to alleviate confusion.
     """

    __tablename__ = 'COHORT'

    __mapper_args__ = {
        'primary_key': ('COHORT_DEFINITION_ID', 'SUBJECT_ID')
    }

    # From Field CSV row 422.
    COHORT_DEFINITION_ID = mapped_column(
        Integer,
        primary_key=True,
        nullable=False
    )

    # From Field CSV row 423.
    SUBJECT_ID = mapped_column(
        Integer,
        primary_key=True,
        nullable=False
    )

    # From Field CSV row 424.
    COHORT_START_DATE = mapped_column(
        Date,
        nullable=False
    )

    # From Field CSV row 425.
    COHORT_END_DATE = mapped_column(
        Date,
        nullable=False
    )