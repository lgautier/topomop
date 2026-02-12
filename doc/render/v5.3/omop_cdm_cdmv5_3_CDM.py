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

cdm_version = 'v5.3'
schema_name = 'CDM'
metadata_obj = MetaData(schema=schema_name)


class Base(DeclarativeBase):
    metadata = metadata_obj

# TODO: check that no table.name can be equal to "Base".


# From Table CSV row 0.
class person(Base):
    """Description:
    This table serves as the central identity management for all Persons in the database. It contains records that uniquely identify each person or patient, and some demographic information.

    User guidance:     
    All records in this table are independent Persons.
     """

    __tablename__ = 'PERSON'

    # From Field CSV row 0.
    PERSON_ID = mapped_column(
        Integer,
        primary_key=True,
        nullable=False,
        comment="""It is assumed that every person with a different unique identifier is in fact a different person and should be treated independently. """
    )

    # From Field CSV row 1.
    GENDER_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""This field is meant to capture the biological sex at birth of the Person. This field should not be used to study gender identity issues. """
    )

    # From Field CSV row 2.
    YEAR_OF_BIRTH = mapped_column(
        Integer,
        nullable=False,
        comment="""Compute age using year_of_birth. """
    )

    # From Field CSV row 3.
    MONTH_OF_BIRTH = mapped_column(
        Integer,
        nullable=True
    )

    # From Field CSV row 4.
    DAY_OF_BIRTH = mapped_column(
        Integer,
        nullable=True
    )

    # From Field CSV row 5.
    BIRTH_DATETIME = mapped_column(
        DateTime,
        nullable=True
    )

    # From Field CSV row 6.
    RACE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""This field captures race or ethnic background of the person. """
    )

    # From Field CSV row 7.
    ETHNICITY_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""This field captures Ethnicity as defined by the Office of Management and Budget (OMB) of the US Government: it distinguishes only between "Hispanic" and "Not Hispanic". Races and ethnic backgrounds are not stored here. """
    )

    # From Field CSV row 8.
    LOCATION_ID = mapped_column(
        Integer,
        ForeignKey('LOCATION.LOCATION_ID'),
        nullable=True,
        comment="""The location refers to the physical address of the person. This field should capture the last known location of the person. """
    )

    # From Field CSV row 9.
    PROVIDER_ID = mapped_column(
        Integer,
        ForeignKey('PROVIDER.PROVIDER_ID'),
        nullable=True,
        comment="""The Provider refers to the last known primary care provider (General Practitioner). """
    )

    # From Field CSV row 10.
    CARE_SITE_ID = mapped_column(
        Integer,
        ForeignKey('CARE_SITE.CARE_SITE_ID'),
        nullable=True,
        comment="""The Care Site refers to where the Provider typically provides the primary care. """
    )

    # From Field CSV row 11.
    PERSON_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True,
        comment="""Use this field to link back to persons in the source data. This is typically used for error checking of ETL logic. """
    )

    # From Field CSV row 12.
    GENDER_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True,
        comment="""This field is used to store the biological sex of the person from the source data. It is not intended for use in standard analytics but for reference only. """
    )

    # From Field CSV row 13.
    GENDER_SOURCE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""Due to the small number of options, this tends to be zero. """
    )

    # From Field CSV row 14.
    RACE_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True,
        comment="""This field is used to store the race of the person from the source data. It is not intended for use in standard analytics but for reference only. """
    )

    # From Field CSV row 15.
    RACE_SOURCE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""Due to the small number of options, this tends to be zero. """
    )

    # From Field CSV row 16.
    ETHNICITY_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True,
        comment="""This field is used to store the ethnicity of the person from the source data. It is not intended for use in standard analytics but for reference only. """
    )

    # From Field CSV row 17.
    ETHNICITY_SOURCE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""Due to the small number of options, this tends to be zero. """
    )


# From Table CSV row 1.
class observation_period(Base):
    """Description:
    This table contains records which define spans of time during which two conditions are expected to hold: (i) Clinical Events that happened to the Person are recorded in the Event tables, and (ii) absence of records indicate such Events did not occur during this span of time.

    User guidance:     
    For each Person, one or more OBSERVATION_PERIOD records may be present, but they will not overlap or be back to back to each other. Events may exist outside all of the time spans of the OBSERVATION_PERIOD records for a patient, however, absence of an Event outside these time spans cannot be construed as evidence of absence of an Event. Incidence or prevalence rates should only be calculated for the time of active OBSERVATION_PERIOD records. When constructing cohorts, outside Events can be used for inclusion criteria definition, but without any guarantee for the performance of these criteria. Also, OBSERVATION_PERIOD records can be as short as a single day, greatly disturbing the denominator of any rate calculation as part of cohort characterizations. To avoid that, apply minimal observation time as a requirement for any cohort definition.
     """

    __tablename__ = 'OBSERVATION_PERIOD'

    # From Field CSV row 18.
    OBSERVATION_PERIOD_ID = mapped_column(
        Integer,
        primary_key=True,
        nullable=False,
        comment="""A Person can have multiple discrete Observation Periods which are identified by the Observation_Period_Id. """
    )

    # From Field CSV row 19.
    PERSON_ID = mapped_column(
        Integer,
        ForeignKey('PERSON.PERSON_ID'),
        nullable=False,
        comment="""The Person ID of the PERSON record for which the Observation Period is recorded. """
    )

    # From Field CSV row 20.
    OBSERVATION_PERIOD_START_DATE = mapped_column(
        Date,
        nullable=False,
        comment="""Use this date to determine the start date of the Observation Period. """
    )

    # From Field CSV row 21.
    OBSERVATION_PERIOD_END_DATE = mapped_column(
        Date,
        nullable=False,
        comment="""Use this date to determine the end date of the period for which we can assume that all events for a Person are recorded. """
    )

    # From Field CSV row 22.
    PERIOD_TYPE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""This field can be used to determine the provenance of the Observation Period as in whether the period was determined from an insurance enrollment file, EHR healthcare encounters, or other sources. """
    )


# From Table CSV row 2.
class visit_occurrence(Base):
    """Description:
    This table contains Events where Persons engage with the healthcare system for a duration of time. They are often also called "Encounters". Visits are defined by a configuration of circumstances under which they occur, such as (i) whether the patient comes to a healthcare institution, the other way around, or the interaction is remote, (ii) whether and what kind of trained medical staff is delivering the service during the Visit, and (iii) whether the Visit is transient or for a longer period involving a stay in bed.

    User guidance:     
    The configuration defining the Visit are described by Concepts in the Visit Domain, which form a hierarchical structure, but rolling up to generally familiar Visits adopted in most healthcare systems worldwide:

- [Inpatient Visit](https://athena.ohdsi.org/search-terms/terms/9201): Person visiting hospital, at a Care Site, in bed, for duration of more than one day, with physicians and other Providers permanently available to deliver service around the clock 
- [Emergency Room Visit](https://athena.ohdsi.org/search-terms/terms/9203): Person visiting dedicated healthcare institution for treating emergencies, at a Care Site, within one day, with physicians and Providers permanently available to deliver service around the clock
- [Emergency Room and Inpatient Visit](https://athena.ohdsi.org/search-terms/terms/262): Person visiting ER followed by a subsequent Inpatient Visit, where Emergency department is part of hospital, and transition from the ER to other hospital departments is undefined
- [Non-hospital institution Visit](https://athena.ohdsi.org/search-terms/terms/42898160): Person visiting dedicated institution for reasons of poor health, at a Care Site, long-term or permanently, with no physician but possibly other Providers permanently available to deliver service around the clock
- [Outpatient Visit](https://athena.ohdsi.org/search-terms/terms/9202): Person visiting dedicated ambulatory healthcare institution, at a Care Site, within one day, without bed, with physicians or medical Providers delivering service during Visit
- [Home Visit](https://athena.ohdsi.org/search-terms/terms/581476): Provider visiting Person, without a Care Site, within one day, delivering service
- [Telehealth Visit](https://athena.ohdsi.org/search-terms/terms/5083): Patient engages with Provider through communication media
- [Pharmacy Visit](https://athena.ohdsi.org/search-terms/terms/581458): Person visiting pharmacy for dispensing of Drug, at a Care Site, within one day
- [Laboratory Visit](https://athena.ohdsi.org/search-terms/terms/32036): Patient visiting dedicated institution, at a Care Site, within one day, for the purpose of a Measurement.
- [Ambulance Visit](https://athena.ohdsi.org/search-terms/terms/581478): Person using transportation service for the purpose of initiating one of the other Visits, without a Care Site, within one day, potentially with Providers accompanying the Visit and delivering service
- [Case Management Visit](https://athena.ohdsi.org/search-terms/terms/38004193): Person interacting with healthcare system, without a Care Site, within a day, with no Providers involved, for administrative purposes

The Visit duration, or 'length of stay', is defined as VISIT_END_DATE - VISIT_START_DATE. For all Visits this is <1 day, except Inpatient Visits and Non-hospital institution Visits. The CDM also contains the VISIT_DETAIL table where additional information about the Visit is stored, for example, transfers between units during an inpatient Visit.
     """

    __tablename__ = 'VISIT_OCCURRENCE'

    # From Field CSV row 23.
    VISIT_OCCURRENCE_ID = mapped_column(
        Integer,
        primary_key=True,
        nullable=False,
        comment="""Use this to identify unique interactions between a person and the health care system. This identifier links across the other CDM event tables to associate events with a visit. """
    )

    # From Field CSV row 24.
    PERSON_ID = mapped_column(
        Integer,
        ForeignKey('PERSON.PERSON_ID'),
        nullable=False
    )

    # From Field CSV row 25.
    VISIT_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""This field contains a concept id representing the kind of visit, like inpatient or outpatient. All concepts in this field should be standard and belong to the Visit domain. """
    )

    # From Field CSV row 26.
    VISIT_START_DATE = mapped_column(
        Date,
        nullable=False,
        comment="""For inpatient visits, the start date is typically the admission date. For outpatient visits the start date and end date will be the same. """
    )

    # From Field CSV row 27.
    VISIT_START_DATETIME = mapped_column(
        DateTime,
        nullable=True
    )

    # From Field CSV row 28.
    VISIT_END_DATE = mapped_column(
        Date,
        nullable=False,
        comment="""For inpatient visits the end date is typically the discharge date. """
    )

    # From Field CSV row 29.
    VISIT_END_DATETIME = mapped_column(
        DateTime,
        nullable=True
    )

    # From Field CSV row 30.
    VISIT_TYPE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""Use this field to understand the provenance of the visit record, or where the record comes from. """
    )

    # From Field CSV row 31.
    PROVIDER_ID = mapped_column(
        Integer,
        ForeignKey('PROVIDER.PROVIDER_ID'),
        nullable=True,
        comment="""There will only be one provider per visit record and the ETL document should clearly state how they were chosen (attending, admitting, etc.). If there are multiple providers associated with a visit in the source, this can be reflected in the event tables (CONDITION_OCCURRENCE, PROCEDURE_OCCURRENCE, etc.) or in the VISIT_DETAIL table. """
    )

    # From Field CSV row 32.
    CARE_SITE_ID = mapped_column(
        Integer,
        ForeignKey('CARE_SITE.CARE_SITE_ID'),
        nullable=True,
        comment="""This field provides information about the Care Site where the Visit took place. """
    )

    # From Field CSV row 33.
    VISIT_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True,
        comment="""This field houses the verbatim value from the source data representing the kind of visit that took place (inpatient, outpatient, emergency, etc.) """
    )

    # From Field CSV row 34.
    VISIT_SOURCE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True
    )

    # From Field CSV row 35.
    ADMITTING_SOURCE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""Use this field to determine where the patient was admitted from. This concept is part of the visit domain and can indicate if a patient was admitted to the hospital from a long-term care facility, for example. """
    )

    # From Field CSV row 36.
    ADMITTING_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True
    )

    # From Field CSV row 37.
    DISCHARGE_TO_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""Use this field to determine where the patient was discharged to after a visit. This concept is part of the visit domain and can indicate if a patient was discharged to home or sent to a long-term care facility, for example. """
    )

    # From Field CSV row 38.
    DISCHARGE_TO_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True
    )

    # From Field CSV row 39.
    PRECEDING_VISIT_OCCURRENCE_ID = mapped_column(
        Integer,
        ForeignKey('VISIT_OCCURRENCE.VISIT_OCCURRENCE_ID'),
        nullable=True,
        comment="""Use this field to find the visit that occurred for the person prior to the given visit. There could be a few days or a few years in between. """
    )


# From Table CSV row 3.
class visit_detail(Base):
    """Description:
    The VISIT_DETAIL table is an optional table used to represents details of each record in the parent VISIT_OCCURRENCE table. A good example of this would be the movement between units in a hospital during an inpatient stay or claim lines associated with a one insurance claim. For every record in the VISIT_OCCURRENCE table there may be 0 or more records in the VISIT_DETAIL table with a 1:n relationship where n may be 0. The VISIT_DETAIL table is structurally very similar to VISIT_OCCURRENCE table and belongs to the visit domain.

    User guidance:     
    The configuration defining the Visit Detail is described by Concepts in the Visit Domain, which form a hierarchical structure. The Visit Detail record will have an associated to the Visit Occurrence record in two ways: <br> 1. The Visit Detail record will have the VISIT_OCCURRENCE_ID it is associated to 2. The VISIT_DETAIL_CONCEPT_ID  will be a descendant of the VISIT_CONCEPT_ID for the Visit.
     """

    __tablename__ = 'VISIT_DETAIL'

    # From Field CSV row 40.
    VISIT_DETAIL_ID = mapped_column(
        Integer,
        primary_key=True,
        nullable=False,
        comment="""Use this to identify unique interactions between a person and the health care system. This identifier links across the other CDM event tables to associate events with a visit detail. """
    )

    # From Field CSV row 41.
    PERSON_ID = mapped_column(
        Integer,
        ForeignKey('PERSON.PERSON_ID'),
        nullable=False
    )

    # From Field CSV row 42.
    VISIT_DETAIL_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""This field contains a concept id representing the kind of visit detail, like inpatient or outpatient. All concepts in this field should be standard and belong to the Visit domain. """
    )

    # From Field CSV row 43.
    VISIT_DETAIL_START_DATE = mapped_column(
        Date,
        nullable=False,
        comment="""This is the date of the start of the encounter. This may or may not be equal to the date of the Visit the Visit Detail is associated with. """
    )

    # From Field CSV row 44.
    VISIT_DETAIL_START_DATETIME = mapped_column(
        DateTime,
        nullable=True
    )

    # From Field CSV row 45.
    VISIT_DETAIL_END_DATE = mapped_column(
        Date,
        nullable=False,
        comment="""This the end date of the patient-provider interaction. """
    )

    # From Field CSV row 46.
    VISIT_DETAIL_END_DATETIME = mapped_column(
        DateTime,
        nullable=True
    )

    # From Field CSV row 47.
    VISIT_DETAIL_TYPE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""Use this field to understand the provenance of the visit detail record, or where the record comes from. """
    )

    # From Field CSV row 48.
    PROVIDER_ID = mapped_column(
        Integer,
        ForeignKey('PROVIDER.PROVIDER_ID'),
        nullable=True,
        comment="""There will only be one provider per  **visit** record and the ETL document should clearly state how they were chosen (attending, admitting, etc.). This is a typical reason for leveraging the VISIT_DETAIL table as even though each VISIT_DETAIL record can only have one provider, there is no limit to the number of VISIT_DETAIL records that can be associated to a VISIT_OCCURRENCE record. """
    )

    # From Field CSV row 49.
    CARE_SITE_ID = mapped_column(
        Integer,
        ForeignKey('CARE_SITE.CARE_SITE_ID'),
        nullable=True,
        comment="""This field provides information about the Care Site where the Visit Detail took place. """
    )

    # From Field CSV row 50.
    VISIT_DETAIL_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True,
        comment="""This field houses the verbatim value from the source data representing the kind of visit detail that took place (inpatient, outpatient, emergency, etc.) """
    )

    # From Field CSV row 51.
    VISIT_DETAIL_SOURCE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True
    )

    # From Field CSV row 52.
    ADMITTING_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True
    )

    # From Field CSV row 53.
    ADMITTING_SOURCE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""Use this field to determine where the patient was admitted from. This concept is part of the visit domain and can indicate if a patient was admitted to the hospital from a long-term care facility, for example. """
    )

    # From Field CSV row 54.
    DISCHARGE_TO_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True
    )

    # From Field CSV row 55.
    DISCHARGE_TO_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""Use this field to determine where the patient was discharged to after a visit detail record. This concept is part of the visit domain and can indicate if a patient was discharged to home or sent to a long-term care facility, for example. """
    )

    # From Field CSV row 56.
    PRECEDING_VISIT_DETAIL_ID = mapped_column(
        Integer,
        ForeignKey('VISIT_DETAIL.VISIT_DETAIL_ID'),
        nullable=True,
        comment="""Use this field to find the visit detail that occurred for the person prior to the given visit detail record. There could be a few days or a few years in between. """
    )

    # From Field CSV row 57.
    VISIT_DETAIL_PARENT_ID = mapped_column(
        Integer,
        ForeignKey('VISIT_DETAIL.VISIT_DETAIL_ID'),
        nullable=True,
        comment="""Use this field to find the visit detail that subsumes the given visit detail record. This is used in the case that a visit detail record needs to be nested beyond the VISIT_OCCURRENCE/VISIT_DETAIL relationship. """
    )

    # From Field CSV row 58.
    VISIT_OCCURRENCE_ID = mapped_column(
        Integer,
        ForeignKey('VISIT_OCCURRENCE.VISIT_OCCURRENCE_ID'),
        nullable=False,
        comment="""Use this field to link the VISIT_DETAIL record to its VISIT_OCCURRENCE. """
    )


# From Table CSV row 4.
class condition_occurrence(Base):
    """Description:
    This table contains records of Events of a Person suggesting the presence of a disease or medical condition stated as a diagnosis, a sign, or a symptom, which is either observed by a Provider or reported by the patient.

    User guidance:     
    Conditions are defined by Concepts from the Condition domain, which form a complex hierarchy. As a result, the same Person with the same disease may have multiple Condition records, which belong to the same hierarchical family. Most Condition records are mapped from diagnostic codes, but recorded signs, symptoms and summary descriptions also contribute to this table. Rule out diagnoses should not be recorded in this table, but in reality their negating nature is not always captured in the source data, and other precautions must be taken when when identifying Persons who should suffer from the recorded Condition. Record all conditions as they exist in the source data. Any decisions about diagnosis/phenotype definitions would be done through cohort specifications. These cohorts can be housed in the [COHORT](https://ohdsi.github.io/CommonDataModel/cdm531.html#payer_plan_period) table. Conditions span a time interval from start to end, but are typically recorded as single snapshot records with no end date. The reason is twofold: (i) At the time of the recording the duration is not known and later not recorded, and (ii) the Persons typically cease interacting with the healthcare system when they feel better, which leads to incomplete capture of resolved Conditions. The [CONDITION_ERA](https://ohdsi.github.io/CommonDataModel/cdm531.html#condition_era) table addresses this issue. Family history and past diagnoses ('history of') are not recorded in this table. Instead, they are listed in the [OBSERVATION](https://ohdsi.github.io/CommonDataModel/cdm531.html#observation) table. Codes written in the process of establishing the diagnosis, such as 'question of' of and 'rule out', should not represented here. Instead, they should be recorded in the [OBSERVATION](https://ohdsi.github.io/CommonDataModel/cdm531.html#observation) table, if they are used for analyses. However, this information is not always available.
     """

    __tablename__ = 'CONDITION_OCCURRENCE'

    # From Field CSV row 59.
    CONDITION_OCCURRENCE_ID = mapped_column(
        Integer,
        primary_key=True,
        nullable=False,
        comment="""The unique key given to a condition record for a person. Refer to the ETL for how duplicate conditions during the same visit were handled. """
    )

    # From Field CSV row 60.
    PERSON_ID = mapped_column(
        Integer,
        ForeignKey('PERSON.PERSON_ID'),
        nullable=False,
        comment="""The PERSON_ID of the PERSON for whom the condition is recorded. """
    )

    # From Field CSV row 61.
    CONDITION_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""The CONDITION_CONCEPT_ID field is recommended for primary use in analyses, and must be used for network studies. This is the standard concept mapped from the source value which represents a condition """
    )

    # From Field CSV row 62.
    CONDITION_START_DATE = mapped_column(
        Date,
        nullable=False,
        comment="""Use this date to determine the start date of the condition """
    )

    # From Field CSV row 63.
    CONDITION_START_DATETIME = mapped_column(
        DateTime,
        nullable=True
    )

    # From Field CSV row 64.
    CONDITION_END_DATE = mapped_column(
        Date,
        nullable=True,
        comment="""Use this date to determine the end date of the condition """
    )

    # From Field CSV row 65.
    CONDITION_END_DATETIME = mapped_column(
        DateTime,
        nullable=True
    )

    # From Field CSV row 66.
    CONDITION_TYPE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""This field can be used to determine the provenance of the Condition record, as in whether the condition was from an EHR system, insurance claim, registry, or other sources. """
    )

    # From Field CSV row 67.
    CONDITION_STATUS_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""This concept represents the point during the visit the diagnosis was given (admitting diagnosis, final diagnosis), whether the diagnosis was determined due to laboratory findings, if the diagnosis was exclusionary, or if it was a preliminary diagnosis, among others. """
    )

    # From Field CSV row 68.
    STOP_REASON = mapped_column(
        String(20),
        nullable=True,
        comment="""The Stop Reason indicates why a Condition is no longer valid with respect to the purpose within the source data. Note that a Stop Reason does not necessarily imply that the condition is no longer occurring. """
    )

    # From Field CSV row 69.
    PROVIDER_ID = mapped_column(
        Integer,
        ForeignKey('PROVIDER.PROVIDER_ID'),
        nullable=True,
        comment="""The provider associated with condition record, e.g. the provider who made the diagnosis or the provider who recorded the symptom. """
    )

    # From Field CSV row 70.
    VISIT_OCCURRENCE_ID = mapped_column(
        Integer,
        ForeignKey('VISIT_OCCURRENCE.VISIT_OCCURRENCE_ID'),
        nullable=True,
        comment="""The visit during which the condition occurred. """
    )

    # From Field CSV row 71.
    VISIT_DETAIL_ID = mapped_column(
        Integer,
        ForeignKey('VISIT_DETAIL.VISIT_DETAIL_ID'),
        nullable=True,
        comment="""The VISIT_DETAIL record during which the condition occurred. For example, if the person was in the ICU at the time of the diagnosis the VISIT_OCCURRENCE record would reflect the overall hospital stay and the VISIT_DETAIL record would reflect the ICU stay during the hospital visit. """
    )

    # From Field CSV row 72.
    CONDITION_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True,
        comment="""This field houses the verbatim value from the source data representing the condition that occurred. For example, this could be an ICD10 or Read code. """
    )

    # From Field CSV row 73.
    CONDITION_SOURCE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""This is the concept representing the condition source value and may not necessarily be standard. This field is discouraged from use in analysis because it is not required to contain Standard Concepts that are used across the OHDSI community, and should only be used when Standard Concepts do not adequately represent the source detail for the Condition necessary for a given analytic use case. Consider using CONDITION_CONCEPT_ID instead to enable standardized analytics that can be consistent across the network. """
    )

    # From Field CSV row 74.
    CONDITION_STATUS_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True,
        comment="""This field houses the verbatim value from the source data representing the condition status. """
    )


# From Table CSV row 5.
class drug_exposure(Base):
    """Description:
    This table captures records about the exposure to a Drug ingested or otherwise introduced into the body. A Drug is a biochemical substance formulated in such a way that when administered to a Person it will exert a certain biochemical effect on the metabolism. Drugs include prescription and over-the-counter medicines, vaccines, and large-molecule biologic therapies. Radiological devices ingested or applied locally do not count as Drugs.

    User guidance:     
    The purpose of records in this table is to indicate an exposure to a certain drug as best as possible. In this context a drug is defined as an active ingredient. Drug Exposures are defined by Concepts from the Drug domain, which form a complex hierarchy. As a result, one DRUG_SOURCE_CONCEPT_ID may map to multiple standard concept ids if it is a combination product. Records in this table represent prescriptions written, prescriptions dispensed, and drugs administered by a provider to name a few. The DRUG_TYPE_CONCEPT_ID can be used to find and filter on these types. This table includes additional information about the drug products, the quantity given, and route of administration.
     """

    __tablename__ = 'DRUG_EXPOSURE'

    # From Field CSV row 75.
    DRUG_EXPOSURE_ID = mapped_column(
        Integer,
        primary_key=True,
        nullable=False,
        comment="""The unique key given to records of drug dispensings or administrations for a person. Refer to the ETL for how duplicate drugs during the same visit were handled. """
    )

    # From Field CSV row 76.
    PERSON_ID = mapped_column(
        Integer,
        ForeignKey('PERSON.PERSON_ID'),
        nullable=False,
        comment="""The PERSON_ID of the PERSON for whom the drug dispensing or administration is recorded. This may be a system generated code. """
    )

    # From Field CSV row 77.
    DRUG_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""The DRUG_CONCEPT_ID field is recommended for primary use in analyses, and must be used for network studies. This is the standard concept mapped from the source concept id which represents a drug product or molecule otherwise introduced to the body. The drug concepts can have a varying degree of information about drug strength and dose. This information is relevant in the context of quantity and administration information in the subsequent fields plus strength information from the DRUG_STRENGTH table, provided as part of the standard vocabulary download. """
    )

    # From Field CSV row 78.
    DRUG_EXPOSURE_START_DATE = mapped_column(
        Date,
        nullable=False,
        comment="""Use this date to determine the start date of the drug record. """
    )

    # From Field CSV row 79.
    DRUG_EXPOSURE_START_DATETIME = mapped_column(
        DateTime,
        nullable=True
    )

    # From Field CSV row 80.
    DRUG_EXPOSURE_END_DATE = mapped_column(
        Date,
        nullable=False,
        comment="""The DRUG_EXPOSURE_END_DATE denotes the day the drug exposure ended for the patient. """
    )

    # From Field CSV row 81.
    DRUG_EXPOSURE_END_DATETIME = mapped_column(
        DateTime,
        nullable=True
    )

    # From Field CSV row 82.
    VERBATIM_END_DATE = mapped_column(
        Date,
        nullable=True,
        comment="""This is the end date of the drug exposure as it appears in the source data, if it is given """
    )

    # From Field CSV row 83.
    DRUG_TYPE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""You can use the TYPE_CONCEPT_ID to delineate between prescriptions written vs. prescriptions dispensed vs. medication history vs. patient-reported exposure, etc. """
    )

    # From Field CSV row 84.
    STOP_REASON = mapped_column(
        String(20),
        nullable=True,
        comment="""The reason a person stopped a medication as it is represented in the source. Reasons include regimen completed, changed, removed, etc. This field will be retired in v6.0. """
    )

    # From Field CSV row 85.
    REFILLS = mapped_column(
        Integer,
        nullable=True,
        comment="""This is only filled in when the record is coming from a prescription written this field is meant to represent intended refills at time of the prescription. """
    )

    # From Field CSV row 86.
    QUANTITY = mapped_column(
        Float,
        nullable=True
    )

    # From Field CSV row 87.
    DAYS_SUPPLY = mapped_column(
        Integer,
        nullable=True,
        comment="""The number of days of supply of the medication as recorded in the original prescription or dispensing record. Days supply can differ from actual drug duration (i.e. prescribed days supply vs actual exposure). """
    )

    # From Field CSV row 88.
    SIG = mapped_column(
        String,
        nullable=True,
        comment="""This is the verbatim instruction for the drug as written by the provider. """
    )

    # From Field CSV row 89.
    ROUTE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True
    )

    # From Field CSV row 90.
    LOT_NUMBER = mapped_column(
        String(50),
        nullable=True
    )

    # From Field CSV row 91.
    PROVIDER_ID = mapped_column(
        Integer,
        ForeignKey('PROVIDER.PROVIDER_ID'),
        nullable=True,
        comment="""The Provider associated with drug record, e.g. the provider who wrote the prescription or the provider who administered the drug. """
    )

    # From Field CSV row 92.
    VISIT_OCCURRENCE_ID = mapped_column(
        Integer,
        ForeignKey('VISIT_OCCURRENCE.VISIT_OCCURRENCE_ID'),
        nullable=True,
        comment="""The Visit during which the drug was prescribed, administered or dispensed. """
    )

    # From Field CSV row 93.
    VISIT_DETAIL_ID = mapped_column(
        Integer,
        ForeignKey('VISIT_DETAIL.VISIT_DETAIL_ID'),
        nullable=True,
        comment="""The VISIT_DETAIL record during which the drug exposure occurred. For example, if the person was in the ICU at the time of the drug administration the VISIT_OCCURRENCE record would reflect the overall hospital stay and the VISIT_DETAIL record would reflect the ICU stay during the hospital visit. """
    )

    # From Field CSV row 94.
    DRUG_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True,
        comment="""This field houses the verbatim value from the source data representing the drug exposure that occurred. For example, this could be an NDC or Gemscript code. """
    )

    # From Field CSV row 95.
    DRUG_SOURCE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""This is the concept representing the drug source value and may not necessarily be standard. This field is discouraged from use in analysis because it is not required to contain Standard Concepts that are used across the OHDSI community, and should only be used when Standard Concepts do not adequately represent the source detail for the Drug necessary for a given analytic use case. Consider using DRUG_CONCEPT_ID instead to enable standardized analytics that can be consistent across the network. """
    )

    # From Field CSV row 96.
    ROUTE_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True,
        comment="""This field houses the verbatim value from the source data representing the drug route. """
    )

    # From Field CSV row 97.
    DOSE_UNIT_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True,
        comment="""This field houses the verbatim value from the source data representing the dose unit of the drug given. """
    )


# From Table CSV row 6.
class procedure_occurrence(Base):
    """Description:
    This table contains records of activities or processes ordered by, or carried out by, a healthcare provider on the patient with a diagnostic or therapeutic purpose.

    User guidance:     
    Lab tests are not a procedure, if something is observed with an expected resulting amount and unit then it should be a measurement. Phlebotomy is a procedure but so trivial that it tends to be rarely captured. It can be assumed that there is a phlebotomy procedure associated with many lab tests, therefore it is unnecessary to add them as separate procedures. If the user finds the same procedure over concurrent days, it is assumed those records are part of a procedure lasting more than a day. This logic is in lieu of the procedure_end_date, which will be added in a future version of the CDM.
     """

    __tablename__ = 'PROCEDURE_OCCURRENCE'

    # From Field CSV row 98.
    PROCEDURE_OCCURRENCE_ID = mapped_column(
        Integer,
        primary_key=True,
        nullable=False,
        comment="""The unique key given to a procedure record for a person. Refer to the ETL for how duplicate procedures during the same visit were handled. """
    )

    # From Field CSV row 99.
    PERSON_ID = mapped_column(
        Integer,
        ForeignKey('PERSON.PERSON_ID'),
        nullable=False,
        comment="""The PERSON_ID of the PERSON for whom the procedure is recorded. This may be a system generated code. """
    )

    # From Field CSV row 100.
    PROCEDURE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""The PROCEDURE_CONCEPT_ID field is recommended for primary use in analyses, and must be used for network studies. This is the standard concept mapped from the source value which represents a procedure """
    )

    # From Field CSV row 101.
    PROCEDURE_DATE = mapped_column(
        Date,
        nullable=False,
        comment="""Use this date to determine the date the procedure occurred. """
    )

    # From Field CSV row 102.
    PROCEDURE_DATETIME = mapped_column(
        DateTime,
        nullable=True
    )

    # From Field CSV row 103.
    PROCEDURE_TYPE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""This field can be used to determine the provenance of the Procedure record, as in whether the procedure was from an EHR system, insurance claim, registry, or other sources. """
    )

    # From Field CSV row 104.
    MODIFIER_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""The modifiers are intended to give additional information about the procedure but as of now the vocabulary is under review. """
    )

    # From Field CSV row 105.
    QUANTITY = mapped_column(
        Integer,
        nullable=True,
        comment="""If the quantity value is omitted, a single procedure is assumed. """
    )

    # From Field CSV row 106.
    PROVIDER_ID = mapped_column(
        Integer,
        nullable=True,
        comment="""The provider associated with the procedure record, e.g. the provider who performed the Procedure. """
    )

    # From Field CSV row 107.
    VISIT_OCCURRENCE_ID = mapped_column(
        Integer,
        nullable=True,
        comment="""The visit during which the procedure occurred. """
    )

    # From Field CSV row 108.
    VISIT_DETAIL_ID = mapped_column(
        Integer,
        nullable=True,
        comment="""The VISIT_DETAIL record during which the Procedure occurred. For example, if the Person was in the ICU at the time of the Procedure the VISIT_OCCURRENCE record would reflect the overall hospital stay and the VISIT_DETAIL record would reflect the ICU stay during the hospital visit. """
    )

    # From Field CSV row 109.
    PROCEDURE_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True,
        comment="""This field houses the verbatim value from the source data representing the procedure that occurred. For example, this could be an CPT4 or OPCS4 code. """
    )

    # From Field CSV row 110.
    PROCEDURE_SOURCE_CONCEPT_ID = mapped_column(
        Integer,
        nullable=True,
        comment="""This is the concept representing the procedure source value and may not necessarily be standard. This field is discouraged from use in analysis because it is not required to contain Standard Concepts that are used across the OHDSI community, and should only be used when Standard Concepts do not adequately represent the source detail for the Procedure necessary for a given analytic use case. Consider using PROCEDURE_CONCEPT_ID instead to enable standardized analytics that can be consistent across the network. """
    )

    # From Field CSV row 111.
    MODIFIER_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True,
        comment="""This field houses the verbatim value from the source data representing the modifier code for the procedure that occurred. """
    )


# From Table CSV row 7.
class device_exposure(Base):
    """Description:
    The Device domain captures information about a person's exposure to a foreign physical object or instrument which is used for diagnostic or therapeutic purposes through a mechanism beyond chemical action. Devices include implantable objects (e.g. pacemakers, stents, artificial joints), medical equipment and supplies (e.g. bandages, crutches, syringes), other instruments used in medical procedures (e.g. sutures, defibrillators) and material used in clinical care (e.g. adhesives, body material, dental material, surgical material).

    User guidance:     
    The distinction between Devices or supplies and Procedures are sometimes blurry, but the former are physical objects while the latter are actions, often to apply a Device or supply.
     """

    __tablename__ = 'DEVICE_EXPOSURE'

    # From Field CSV row 112.
    DEVICE_EXPOSURE_ID = mapped_column(
        Integer,
        primary_key=True,
        nullable=False,
        comment="""The unique key given to records a person's exposure to a foreign physical object or instrument. """
    )

    # From Field CSV row 113.
    PERSON_ID = mapped_column(
        Integer,
        ForeignKey('PERSON.PERSON_ID'),
        nullable=False
    )

    # From Field CSV row 114.
    DEVICE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""The DEVICE_CONCEPT_ID field is recommended for primary use in analyses, and must be used for network studies. This is the standard concept mapped from the source concept id which represents a foreign object or instrument the person was exposed to. """
    )

    # From Field CSV row 115.
    DEVICE_EXPOSURE_START_DATE = mapped_column(
        Date,
        nullable=False,
        comment="""Use this date to determine the start date of the device record. """
    )

    # From Field CSV row 116.
    DEVICE_EXPOSURE_START_DATETIME = mapped_column(
        DateTime,
        nullable=True
    )

    # From Field CSV row 117.
    DEVICE_EXPOSURE_END_DATE = mapped_column(
        Date,
        nullable=True,
        comment="""The DEVICE_EXPOSURE_END_DATE denotes the day the device exposure ended for the patient, if given. """
    )

    # From Field CSV row 118.
    DEVICE_EXPOSURE_END_DATETIME = mapped_column(
        DateTime,
        nullable=True
    )

    # From Field CSV row 119.
    DEVICE_TYPE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""You can use the TYPE_CONCEPT_ID to denote the provenance of the record, as in whether the record is from administrative claims or EHR. """
    )

    # From Field CSV row 120.
    UNIQUE_DEVICE_ID = mapped_column(
        String(50),
        nullable=True,
        comment="""This is the Unique Device Identification number for devices regulated by the FDA, if given. """
    )

    # From Field CSV row 121.
    QUANTITY = mapped_column(
        Integer,
        nullable=True
    )

    # From Field CSV row 122.
    PROVIDER_ID = mapped_column(
        Integer,
        ForeignKey('PROVIDER.PROVIDER_ID'),
        nullable=True,
        comment="""The Provider associated with device record, e.g. the provider who wrote the prescription or the provider who implanted the device. """
    )

    # From Field CSV row 123.
    VISIT_OCCURRENCE_ID = mapped_column(
        Integer,
        ForeignKey('VISIT_OCCURRENCE.VISIT_OCCURRENCE_ID'),
        nullable=True,
        comment="""The Visit during which the device was prescribed or given. """
    )

    # From Field CSV row 124.
    VISIT_DETAIL_ID = mapped_column(
        Integer,
        ForeignKey('VISIT_DETAIL.VISIT_DETAIL_ID'),
        nullable=True,
        comment="""The Visit Detail during which the device was prescribed or given. """
    )

    # From Field CSV row 125.
    DEVICE_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True,
        comment="""This field houses the verbatim value from the source data representing the device exposure that occurred. For example, this could be an NDC or Gemscript code. """
    )

    # From Field CSV row 126.
    DEVICE_SOURCE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""This is the concept representing the device source value and may not necessarily be standard. This field is discouraged from use in analysis because it is not required to contain Standard Concepts that are used across the OHDSI community, and should only be used when Standard Concepts do not adequately represent the source detail for the Device necessary for a given analytic use case. Consider using DEVICE_CONCEPT_ID instead to enable standardized analytics that can be consistent across the network. """
    )


# From Table CSV row 8.
class measurement(Base):
    """Description:
    The MEASUREMENT table contains records of Measurements, i.e. structured values (numerical or categorical) obtained through systematic and standardized examination or testing of a Person or Person's sample. The MEASUREMENT table contains both orders and results of such Measurements as laboratory tests, vital signs, quantitative findings from pathology reports, etc. Measurements are stored as attribute value pairs, with the attribute as the Measurement Concept and the value representing the result. The value can be a Concept (stored in VALUE_AS_CONCEPT), or a numerical value (VALUE_AS_NUMBER) with a Unit (UNIT_CONCEPT_ID). The Procedure for obtaining the sample is housed in the PROCEDURE_OCCURRENCE table, though it is unnecessary to create a PROCEDURE_OCCURRENCE record for each measurement if one does not exist in the source data. Measurements differ from Observations in that they require a standardized test or some other activity to generate a quantitative or qualitative result. If there is no result, it is assumed that the lab test was conducted but the result was not captured.

    User guidance:     
    Measurements are predominately lab tests with a few exceptions, like blood pressure or function tests. Results are given in the form of a value and unit combination. When investigating measurements, look for operator_concept_ids (<, >, etc.).
     """

    __tablename__ = 'MEASUREMENT'

    # From Field CSV row 127.
    MEASUREMENT_ID = mapped_column(
        Integer,
        primary_key=True,
        nullable=False,
        comment="""The unique key given to a Measurement record for a Person. Refer to the ETL for how duplicate Measurements during the same Visit were handled. """
    )

    # From Field CSV row 128.
    PERSON_ID = mapped_column(
        Integer,
        ForeignKey('PERSON.PERSON_ID'),
        nullable=False,
        comment="""The PERSON_ID of the Person for whom the Measurement is recorded. This may be a system generated code. """
    )

    # From Field CSV row 129.
    MEASUREMENT_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""The MEASUREMENT_CONCEPT_ID field is recommended for primary use in analyses, and must be used for network studies. This is the standard concept mapped from the source value which represents a measurement. """
    )

    # From Field CSV row 130.
    MEASUREMENT_DATE = mapped_column(
        Date,
        nullable=False,
        comment="""Use this date to determine the date of the measurement. """
    )

    # From Field CSV row 131.
    MEASUREMENT_DATETIME = mapped_column(
        DateTime,
        nullable=True
    )

    # From Field CSV row 132.
    MEASUREMENT_TIME = mapped_column(
        String(10),
        nullable=True
    )

    # From Field CSV row 133.
    MEASUREMENT_TYPE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""This field can be used to determine the provenance of the Measurement record, as in whether the measurement was from an EHR system, insurance claim, registry, or other sources. """
    )

    # From Field CSV row 134.
    OPERATOR_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""The meaning of Concept [4172703](https://athena.ohdsi.org/search-terms/terms/4172703) for '=' is identical to omission of a OPERATOR_CONCEPT_ID value. Since the use of this field is rare, it's important when devising analyses to not to forget testing for the content of this field for values different from =. """
    )

    # From Field CSV row 135.
    VALUE_AS_NUMBER = mapped_column(
        Float,
        nullable=True,
        comment="""This is the numerical value of the Result of the Measurement, if available. Note that measurements such as blood pressures will be split into their component parts i.e. one record for systolic, one record for diastolic. """
    )

    # From Field CSV row 136.
    VALUE_AS_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""If the raw data gives a categorial result for measurements those values are captured and mapped to standard concepts in the 'Meas Value' domain. """
    )

    # From Field CSV row 137.
    UNIT_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""At present, there isn't a prescribed unit for individual measurements, such as Hemoglobin A1C, meaning it's not obligatory to express these measurements as a percentage. UNIT_SOURCE_VALUES should be linked to a Standard Concept within the Unit domain that most accurately reflects the unit provided in the source data. """
    )

    # From Field CSV row 138.
    RANGE_LOW = mapped_column(
        Float,
        nullable=True,
        comment="""Ranges have the same unit as the VALUE_AS_NUMBER. These ranges are provided by the source and should remain NULL if not given. """
    )

    # From Field CSV row 139.
    RANGE_HIGH = mapped_column(
        Float,
        nullable=True,
        comment="""Ranges have the same unit as the VALUE_AS_NUMBER. These ranges are provided by the source and should remain NULL if not given. """
    )

    # From Field CSV row 140.
    PROVIDER_ID = mapped_column(
        Integer,
        ForeignKey('PROVIDER.PROVIDER_ID'),
        nullable=True,
        comment="""The provider associated with measurement record, e.g. the provider who ordered the test or the provider who recorded the result. """
    )

    # From Field CSV row 141.
    VISIT_OCCURRENCE_ID = mapped_column(
        Integer,
        ForeignKey('VISIT_OCCURRENCE.VISIT_OCCURRENCE_ID'),
        nullable=True,
        comment="""The visit during which the Measurement occurred. """
    )

    # From Field CSV row 142.
    VISIT_DETAIL_ID = mapped_column(
        Integer,
        ForeignKey('VISIT_DETAIL.VISIT_DETAIL_ID'),
        nullable=True,
        comment="""The VISIT_DETAIL record during which the Measurement occurred. For example, if the Person was in the ICU at the time the VISIT_OCCURRENCE record would reflect the overall hospital stay and the VISIT_DETAIL record would reflect the ICU stay during the hospital visit. """
    )

    # From Field CSV row 143.
    MEASUREMENT_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True,
        comment="""This field contains the exact value from the source data that represents the measurement that occurred. """
    )

    # From Field CSV row 144.
    MEASUREMENT_SOURCE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""This is the concept representing the MEASUREMENT_SOURCE_VALUE and may not necessarily be standard. This field is discouraged from use in analysis because it is not required to contain Standard Concepts that are used across the OHDSI community, and should only be used when Standard Concepts do not adequately represent the source detail for the Measurement necessary for a given analytic use case. Consider using MEASUREMENT_CONCEPT_ID instead to enable standardized analytics that can be consistent across the network. """
    )

    # From Field CSV row 145.
    UNIT_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True,
        comment="""This field contains the exact value from the source data that represents the unit of measurement used. """
    )

    # From Field CSV row 146.
    VALUE_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True,
        comment="""This field houses the verbatim result value of the Measurement from the source data . """
    )


# From Table CSV row 9.
class observation(Base):
    """Description:
    The OBSERVATION table captures clinical facts about a Person obtained in the context of examination, questioning or a procedure. Any data that cannot be represented by any other domains, such as social and lifestyle facts, medical history, family history, etc. are recorded here.

    User guidance:     
    Observations differ from Measurements in that they do not require a standardized test or some other activity to generate clinical fact. Typical observations are medical history, family history, the stated need for certain treatment, social circumstances, lifestyle choices, healthcare utilization patterns, etc. If the generation clinical facts requires a standardized testing such as lab testing or imaging and leads to a standardized result, the data item is recorded in the MEASUREMENT table. If the clinical fact observed determines a sign, symptom, diagnosis of a disease or other medical condition, it is recorded in the CONDITION_OCCURRENCE table. Valid Observation Concepts are not enforced to be from any domain but they must not belong to the Condition, Procedure, Drug, Device, Specimen, or Measurement domains and they must be Standard Concepts. <br><br>The observation table usually records the date or datetime of when the observation was obtained, not the date of the observation starting. For example, if the patient reports that they had a heart attack when they were 50, the observation date or datetime is the date of the report, the heart attack observation can have a value_as_concept which captures how long ago the observation applied to the patient.
     """

    __tablename__ = 'OBSERVATION'

    # From Field CSV row 147.
    OBSERVATION_ID = mapped_column(
        Integer,
        primary_key=True,
        nullable=False,
        comment="""The unique key given to an Observation record for a Person. Refer to the ETL for how duplicate Observations during the same Visit were handled. """
    )

    # From Field CSV row 148.
    PERSON_ID = mapped_column(
        Integer,
        ForeignKey('PERSON.PERSON_ID'),
        nullable=False,
        comment="""The PERSON_ID of the Person for whom the Observation is recorded. This may be a system generated code. """
    )

    # From Field CSV row 149.
    OBSERVATION_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""The OBSERVATION_CONCEPT_ID field is recommended for primary use in analyses, and must be used for network studies. """
    )

    # From Field CSV row 150.
    OBSERVATION_DATE = mapped_column(
        Date,
        nullable=False,
        comment="""The date of when the Observation was obtained. Depending on what the Observation represents this could be the date of a lab test, the date of a survey, or the date a patient's family history was taken. """
    )

    # From Field CSV row 151.
    OBSERVATION_DATETIME = mapped_column(
        DateTime,
        nullable=True
    )

    # From Field CSV row 152.
    OBSERVATION_TYPE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""This field can be used to determine the provenance of the Observation record, as in whether the measurement was from an EHR system, insurance claim, registry, or other sources. """
    )

    # From Field CSV row 153.
    VALUE_AS_NUMBER = mapped_column(
        Float,
        nullable=True,
        comment="""This is the numerical value of the Result of the Observation, if applicable and available. It is not expected that all Observations will have numeric results, rather, this field is here to house values should they exist. """
    )

    # From Field CSV row 154.
    VALUE_AS_STRING = mapped_column(
        String(60),
        nullable=True,
        comment="""This is the categorical value of the Result of the Observation, if applicable and available. """
    )

    # From Field CSV row 155.
    VALUE_AS_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""It is possible that some records destined for the Observation table have two clinical ideas represented in one source code. This is common with ICD10 codes that describe a family history of some Condition, for example. In OMOP the Vocabulary breaks these two clinical ideas into two codes; one becomes the OBSERVATION_CONCEPT_ID and the other becomes the VALUE_AS_CONCEPT_ID. It is important when using the Observation table to keep this possibility in mind and to examine the VALUE_AS_CONCEPT_ID field for relevant information. """
    )

    # From Field CSV row 156.
    QUALIFIER_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""This field contains all attributes specifying the clinical fact further, such as as degrees, severities, drug-drug interaction alerts etc. """
    )

    # From Field CSV row 157.
    UNIT_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""There is currently no recommended unit for individual observation concepts. UNIT_SOURCE_VALUES should be mapped to a Standard Concept in the Unit domain that best represents the unit as given in the source data. """
    )

    # From Field CSV row 158.
    PROVIDER_ID = mapped_column(
        Integer,
        ForeignKey('PROVIDER.PROVIDER_ID'),
        nullable=True,
        comment="""The provider associated with the observation record, e.g. the provider who ordered the test or the provider who recorded the result. """
    )

    # From Field CSV row 159.
    VISIT_OCCURRENCE_ID = mapped_column(
        Integer,
        ForeignKey('VISIT_OCCURRENCE.VISIT_OCCURRENCE_ID'),
        nullable=True,
        comment="""The visit during which the Observation occurred. """
    )

    # From Field CSV row 160.
    VISIT_DETAIL_ID = mapped_column(
        Integer,
        ForeignKey('VISIT_DETAIL.VISIT_DETAIL_ID'),
        nullable=True,
        comment="""The VISIT_DETAIL record during which the Observation occurred. For example, if the Person was in the ICU at the time the VISIT_OCCURRENCE record would reflect the overall hospital stay and the VISIT_DETAIL record would reflect the ICU stay during the hospital visit. """
    )

    # From Field CSV row 161.
    OBSERVATION_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True,
        comment="""This field houses the verbatim value from the source data representing the Observation that occurred. For example, this could be an ICD10 or Read code. """
    )

    # From Field CSV row 162.
    OBSERVATION_SOURCE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""This is the concept representing the OBSERVATION_SOURCE_VALUE and may not necessarily be standard. This field is discouraged from use in analysis because it is not required to contain Standard Concepts that are used across the OHDSI community, and should only be used when Standard Concepts do not adequately represent the source detail for the Observation necessary for a given analytic use case. Consider using OBSERVATION_CONCEPT_ID instead to enable standardized analytics that can be consistent across the network. """
    )

    # From Field CSV row 163.
    UNIT_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True,
        comment="""This field houses the verbatim value from the source data representing the unit of the Observation that occurred. """
    )

    # From Field CSV row 164.
    QUALIFIER_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True,
        comment="""This field houses the verbatim value from the source data representing the qualifier of the Observation that occurred. """
    )


# From Table CSV row 10.
class death(Base):
    """Description:
    The death domain contains the clinical event for how and when a Person dies. A person can have up to one record if the source system contains evidence about the Death, such as: Condition in an administrative claim, status of enrollment into a health plan, or explicit record in EHR data.
     """

    __tablename__ = 'DEATH'

    # From Field CSV row 165.
    PERSON_ID = mapped_column(
        Integer,
        ForeignKey('PERSON.PERSON_ID'),
        primary_key=True,
        nullable=False
    )

    # From Field CSV row 166.
    DEATH_DATE = mapped_column(
        Date,
        nullable=False,
        comment="""The date the person was deceased. """
    )

    # From Field CSV row 167.
    DEATH_DATETIME = mapped_column(
        DateTime,
        nullable=True
    )

    # From Field CSV row 168.
    DEATH_TYPE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""This is the provenance of the death record, i.e., where it came from. It is possible that an administrative claims database would source death information from a government file so do not assume the Death Type is the same as the Visit Type, etc. """
    )

    # From Field CSV row 169.
    CAUSE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""This is the Standard Concept representing the Person's cause of death, if available. """
    )

    # From Field CSV row 170.
    CAUSE_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True
    )

    # From Field CSV row 171.
    CAUSE_SOURCE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True
    )


# From Table CSV row 11.
class note(Base):
    """Description:
    The NOTE table captures unstructured information that was recorded by a provider about a patient in free text (in ASCII, or preferably in UTF8 format) notes on a given date. The type of note_text is CLOB or varchar(MAX) depending on RDBMS.
     """

    __tablename__ = 'NOTE'

    # From Field CSV row 172.
    NOTE_ID = mapped_column(
        Integer,
        primary_key=True,
        nullable=False,
        comment="""A unique identifier for each note. """
    )

    # From Field CSV row 173.
    PERSON_ID = mapped_column(
        Integer,
        ForeignKey('PERSON.PERSON_ID'),
        nullable=False
    )

    # From Field CSV row 174.
    NOTE_DATE = mapped_column(
        Date,
        nullable=False,
        comment="""The date the note was recorded. """
    )

    # From Field CSV row 175.
    NOTE_DATETIME = mapped_column(
        DateTime,
        nullable=True
    )

    # From Field CSV row 176.
    NOTE_TYPE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""The provenance of the note. Most likely this will be EHR. """
    )

    # From Field CSV row 177.
    NOTE_CLASS_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""A Standard Concept Id representing the HL7 LOINC
Document Type Vocabulary classification of the note. """
    )

    # From Field CSV row 178.
    NOTE_TITLE = mapped_column(
        String(250),
        nullable=True,
        comment="""The title of the note. """
    )

    # From Field CSV row 179.
    NOTE_TEXT = mapped_column(
        String,
        nullable=False,
        comment="""The content of the note. """
    )

    # From Field CSV row 180.
    ENCODING_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""This is the Concept representing the character encoding type. """
    )

    # From Field CSV row 181.
    LANGUAGE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""The language of the note. """
    )

    # From Field CSV row 182.
    PROVIDER_ID = mapped_column(
        Integer,
        ForeignKey('PROVIDER.PROVIDER_ID'),
        nullable=True,
        comment="""The Provider who wrote the note. """
    )

    # From Field CSV row 183.
    VISIT_OCCURRENCE_ID = mapped_column(
        Integer,
        ForeignKey('VISIT_OCCURRENCE.VISIT_OCCURRENCE_ID'),
        nullable=True,
        comment="""The Visit during which the note was written. """
    )

    # From Field CSV row 184.
    VISIT_DETAIL_ID = mapped_column(
        Integer,
        ForeignKey('VISIT_DETAIL.VISIT_DETAIL_ID'),
        nullable=True,
        comment="""The Visit Detail during which the note was written. """
    )

    # From Field CSV row 185.
    NOTE_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True
    )


# From Table CSV row 12.
class note_nlp(Base):
    """Description:
    The NOTE_NLP table encodes all output of NLP on clinical notes. Each row represents a single extracted term from a note.
     """

    __tablename__ = 'NOTE_NLP'

    # From Field CSV row 186.
    NOTE_NLP_ID = mapped_column(
        Integer,
        primary_key=True,
        nullable=False,
        comment="""A unique identifier for the NLP record. """
    )

    # From Field CSV row 187.
    NOTE_ID = mapped_column(
        Integer,
        nullable=False,
        comment="""This is the NOTE_ID for the NOTE record the NLP record is associated to. """
    )

    # From Field CSV row 188.
    SECTION_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True
    )

    # From Field CSV row 189.
    SNIPPET = mapped_column(
        String(250),
        nullable=True,
        comment="""A small window of text surrounding the term """
    )

    # From Field CSV row 190.
    OFFSET = mapped_column(
        String(50),
        nullable=True,
        comment="""Character offset of the extracted term in the input note """
    )

    # From Field CSV row 191.
    LEXICAL_VARIANT = mapped_column(
        String(250),
        nullable=False,
        comment="""Raw text extracted from the NLP tool. """
    )

    # From Field CSV row 192.
    NOTE_NLP_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True
    )

    # From Field CSV row 193.
    NOTE_NLP_SOURCE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True
    )

    # From Field CSV row 194.
    NLP_SYSTEM = mapped_column(
        String(250),
        nullable=True
    )

    # From Field CSV row 195.
    NLP_DATE = mapped_column(
        Date,
        nullable=False,
        comment="""The date of the note processing. """
    )

    # From Field CSV row 196.
    NLP_DATETIME = mapped_column(
        DateTime,
        nullable=True,
        comment="""The date and time of the note processing. """
    )

    # From Field CSV row 197.
    TERM_EXISTS = mapped_column(
        String(1),
        nullable=True
    )

    # From Field CSV row 198.
    TERM_TEMPORAL = mapped_column(
        String(50),
        nullable=True
    )

    # From Field CSV row 199.
    TERM_MODIFIERS = mapped_column(
        String(2000),
        nullable=True
    )


# From Table CSV row 13.
class specimen(Base):
    """Description:
    The specimen domain contains the records identifying biological samples from a person.
     """

    __tablename__ = 'SPECIMEN'

    # From Field CSV row 200.
    SPECIMEN_ID = mapped_column(
        Integer,
        primary_key=True,
        nullable=False,
        comment="""Unique identifier for each specimen. """
    )

    # From Field CSV row 201.
    PERSON_ID = mapped_column(
        Integer,
        ForeignKey('PERSON.PERSON_ID'),
        nullable=False,
        comment="""The person from whom the specimen is collected. """
    )

    # From Field CSV row 202.
    SPECIMEN_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=False
    )

    # From Field CSV row 203.
    SPECIMEN_TYPE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=False
    )

    # From Field CSV row 204.
    SPECIMEN_DATE = mapped_column(
        Date,
        nullable=False,
        comment="""The date the specimen was collected. """
    )

    # From Field CSV row 205.
    SPECIMEN_DATETIME = mapped_column(
        DateTime,
        nullable=True
    )

    # From Field CSV row 206.
    QUANTITY = mapped_column(
        Float,
        nullable=True,
        comment="""The amount of specimen collected from the person. """
    )

    # From Field CSV row 207.
    UNIT_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""The unit for the quantity of the specimen. """
    )

    # From Field CSV row 208.
    ANATOMIC_SITE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""This is the site on the body where the specimen is from. """
    )

    # From Field CSV row 209.
    DISEASE_STATUS_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True
    )

    # From Field CSV row 210.
    SPECIMEN_SOURCE_ID = mapped_column(
        String(50),
        nullable=True,
        comment="""This is the identifier for the specimen from the source system. """
    )

    # From Field CSV row 211.
    SPECIMEN_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True
    )

    # From Field CSV row 212.
    UNIT_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True
    )

    # From Field CSV row 213.
    ANATOMIC_SITE_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True
    )

    # From Field CSV row 214.
    DISEASE_STATUS_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True
    )


# From Table CSV row 14.
class fact_relationship(Base):
    """Description:
    The FACT_RELATIONSHIP table contains records about the relationships between facts stored as records in any table of the CDM. Relationships can be defined between facts from the same domain, or different domains. Examples of Fact Relationships include: [Person relationships](https://athena.ohdsi.org/search-terms/terms?domain=Relationship&standardConcept=Standard&page=2&pageSize=15&query=) (parent-child), care site relationships (hierarchical organizational structure of facilities within a health system), indication relationship (between drug exposures and associated conditions), usage relationships (of devices during the course of an associated procedure), or facts derived from one another (measurements derived from an associated specimen).
     """

    __tablename__ = 'FACT_RELATIONSHIP'

    __mapper_args__ = {
        'primary_key': ('DOMAIN_CONCEPT_ID_1', 'FACT_ID_1', 'DOMAIN_CONCEPT_ID_2', 'FACT_ID_2', 'RELATIONSHIP_CONCEPT_ID')
    }

    # From Field CSV row 215.
    DOMAIN_CONCEPT_ID_1 = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        primary_key=True,
        nullable=False
    )

    # From Field CSV row 216.
    FACT_ID_1 = mapped_column(
        Integer,
        primary_key=True,
        nullable=False
    )

    # From Field CSV row 217.
    DOMAIN_CONCEPT_ID_2 = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        primary_key=True,
        nullable=False
    )

    # From Field CSV row 218.
    FACT_ID_2 = mapped_column(
        Integer,
        primary_key=True,
        nullable=False
    )

    # From Field CSV row 219.
    RELATIONSHIP_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        primary_key=True,
        nullable=False
    )


# From Table CSV row 15.
class location(Base):
    """Description:
    The LOCATION table represents a generic way to capture physical location or address information of Persons and Care Sites.
     """

    __tablename__ = 'LOCATION'

    # From Field CSV row 220.
    LOCATION_ID = mapped_column(
        Integer,
        primary_key=True,
        nullable=False,
        comment="""The unique key given to a unique Location. """
    )

    # From Field CSV row 221.
    ADDRESS_1 = mapped_column(
        String(50),
        nullable=True,
        comment="""This is the first line of the address. """
    )

    # From Field CSV row 222.
    ADDRESS_2 = mapped_column(
        String(50),
        nullable=True,
        comment="""This is the second line of the address """
    )

    # From Field CSV row 223.
    CITY = mapped_column(
        String(50),
        nullable=True
    )

    # From Field CSV row 224.
    STATE = mapped_column(
        String(2),
        nullable=True
    )

    # From Field CSV row 225.
    ZIP = mapped_column(
        String(9),
        nullable=True
    )

    # From Field CSV row 226.
    COUNTY = mapped_column(
        String(20),
        nullable=True
    )

    # From Field CSV row 227.
    LOCATION_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True
    )


# From Table CSV row 16.
class care_site(Base):
    """Description:
    The CARE_SITE table contains a list of uniquely identified institutional (physical or organizational) units where healthcare delivery is practiced (offices, wards, hospitals, clinics, etc.).
     """

    __tablename__ = 'CARE_SITE'

    # From Field CSV row 228.
    CARE_SITE_ID = mapped_column(
        Integer,
        primary_key=True,
        nullable=False
    )

    # From Field CSV row 229.
    CARE_SITE_NAME = mapped_column(
        String(255),
        nullable=True,
        comment="""The name of the care_site as it appears in the source data """
    )

    # From Field CSV row 230.
    PLACE_OF_SERVICE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""This is a high-level way of characterizing a Care Site. Typically, however, Care Sites can provide care in multiple settings (inpatient, outpatient, etc.) and this granularity should be reflected in the visit. """
    )

    # From Field CSV row 231.
    LOCATION_ID = mapped_column(
        Integer,
        ForeignKey('LOCATION.LOCATION_ID'),
        nullable=True,
        comment="""The location_id from the LOCATION table representing the physical location of the care_site. """
    )

    # From Field CSV row 232.
    CARE_SITE_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True,
        comment="""The identifier of the care_site as it appears in the source data. This could be an identifier separate from the name of the care_site. """
    )

    # From Field CSV row 233.
    PLACE_OF_SERVICE_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True
    )


# From Table CSV row 17.
class provider(Base):
    """Description:
    The PROVIDER table contains a list of uniquely identified healthcare providers; duplication is not allowed. These are individuals providing hands-on healthcare to patients, such as physicians, nurses, midwives, physical therapists etc.

    User guidance:     
    Many sources do not make a distinction between individual and institutional providers. The PROVIDER table contains the individual providers. If the source only provides limited information such as specialty instead of uniquely identifying individual providers, generic or 'pooled' Provider records are listed in the PROVIDER table.
     """

    __tablename__ = 'PROVIDER'

    # From Field CSV row 234.
    PROVIDER_ID = mapped_column(
        Integer,
        primary_key=True,
        nullable=False,
        comment="""It is assumed that every provider with a different unique identifier is in fact a different person and should be treated independently. """
    )

    # From Field CSV row 235.
    PROVIDER_NAME = mapped_column(
        String(255),
        nullable=True,
        comment="""This field contains information that describes a healthcare provider. """
    )

    # From Field CSV row 236.
    NPI = mapped_column(
        String(20),
        nullable=True,
        comment="""This is the National Provider Number issued to health care providers in the US by the Centers for Medicare and Medicaid Services (CMS). """
    )

    # From Field CSV row 237.
    DEA = mapped_column(
        String(20),
        nullable=True,
        comment="""This is the identifier issued by the DEA, a US federal agency, that allows a provider to write prescriptions for controlled substances. """
    )

    # From Field CSV row 238.
    SPECIALTY_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""This field either represents the most common specialty that occurs in the data or the most specific concept that represents all specialties listed, should the provider have more than one. This includes physician specialties such as internal medicine, emergency medicine, etc. and allied health professionals such as nurses, midwives, and pharmacists. """
    )

    # From Field CSV row 239.
    CARE_SITE_ID = mapped_column(
        Integer,
        ForeignKey('CARE_SITE.CARE_SITE_ID'),
        nullable=True,
        comment="""This is the CARE_SITE_ID for the location that the provider primarily practices in. """
    )

    # From Field CSV row 240.
    YEAR_OF_BIRTH = mapped_column(
        Integer,
        nullable=True
    )

    # From Field CSV row 241.
    GENDER_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""This field represents the recorded gender of the provider in the source data. """
    )

    # From Field CSV row 242.
    PROVIDER_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True,
        comment="""Use this field to link back to providers in the source data. This is typically used for error checking of ETL logic. """
    )

    # From Field CSV row 243.
    SPECIALTY_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True,
        comment="""This refers to the specific type of healthcare provider or field of expertise listed in the source data, encompassing physician specialties like internal medicine, emergency medicine, etc., as well as allied health professionals such as nurses, midwives, and pharmacists. It covers medical specialties like surgery, internal medicine, and radiology, while other services like prosthetics, acupuncture, and physical therapy fall under the domain of "Service." """
    )

    # From Field CSV row 244.
    SPECIALTY_SOURCE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""This is often zero as many sites use proprietary codes to store physician speciality. """
    )

    # From Field CSV row 245.
    GENDER_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True,
        comment="""This is provider's gender as it appears in the source data. """
    )

    # From Field CSV row 246.
    GENDER_SOURCE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""This is often zero as many sites use proprietary codes to store provider gender. """
    )


# From Table CSV row 18.
class payer_plan_period(Base):
    """Description:
    The PAYER_PLAN_PERIOD table captures details of the period of time that a Person is continuously enrolled under a specific health Plan benefit structure from a given Payer. Each Person receiving healthcare is typically covered by a health benefit plan, which pays for (fully or partially), or directly provides, the care. These benefit plans are provided by payers, such as health insurances or state or government agencies. In each plan the details of the health benefits are defined for the Person or her family, and the health benefit Plan might change over time typically with increasing utilization (reaching certain cost thresholds such as deductibles), plan availability and purchasing choices of the Person. The unique combinations of Payer organizations, health benefit Plans and time periods in which they are valid for a Person are recorded in this table.

    User guidance:     
    A Person can have multiple, overlapping, Payer_Plan_Periods in this table. For example, medical and drug coverage in the US can be represented by two Payer_Plan_Periods. The details of the benefit structure of the Plan is rarely known, the idea is just to identify that the Plans are different.
     """

    __tablename__ = 'PAYER_PLAN_PERIOD'

    # From Field CSV row 247.
    PAYER_PLAN_PERIOD_ID = mapped_column(
        Integer,
        primary_key=True,
        nullable=False,
        comment="""A unique identifier for each unique combination of a Person, Payer, Plan, and Period of time. """
    )

    # From Field CSV row 248.
    PERSON_ID = mapped_column(
        Integer,
        ForeignKey('PERSON.PERSON_ID'),
        nullable=False,
        comment="""The Person covered by the Plan. """
    )

    # From Field CSV row 249.
    PAYER_PLAN_PERIOD_START_DATE = mapped_column(
        Date,
        nullable=False,
        comment="""Start date of Plan coverage. """
    )

    # From Field CSV row 250.
    PAYER_PLAN_PERIOD_END_DATE = mapped_column(
        Date,
        nullable=False,
        comment="""End date of Plan coverage. """
    )

    # From Field CSV row 251.
    PAYER_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""This field represents the organization who reimburses the provider which administers care to the Person. """
    )

    # From Field CSV row 252.
    PAYER_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True,
        comment="""This is the Payer as it appears in the source data. """
    )

    # From Field CSV row 253.
    PAYER_SOURCE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True
    )

    # From Field CSV row 254.
    PLAN_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""This field represents the specific health benefit Plan the Person is enrolled in. """
    )

    # From Field CSV row 255.
    PLAN_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True,
        comment="""This is the health benefit Plan of the Person as it appears in the source data. """
    )

    # From Field CSV row 256.
    PLAN_SOURCE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True
    )

    # From Field CSV row 257.
    SPONSOR_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""This field represents the sponsor of the Plan who finances the Plan. This includes self-insured, small group health plan and large group health plan. """
    )

    # From Field CSV row 258.
    SPONSOR_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True,
        comment="""The Plan sponsor as it appears in the source data. """
    )

    # From Field CSV row 259.
    SPONSOR_SOURCE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True
    )

    # From Field CSV row 260.
    FAMILY_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True,
        comment="""The common identifier for all people (often a family) that covered by the same policy. """
    )

    # From Field CSV row 261.
    STOP_REASON_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True,
        comment="""This field represents the reason the Person left the Plan, if known. """
    )

    # From Field CSV row 262.
    STOP_REASON_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True,
        comment="""The Plan stop reason as it appears in the source data. """
    )

    # From Field CSV row 263.
    STOP_REASON_SOURCE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True
    )


# From Table CSV row 19.
class cost(Base):
    """Description:
    The COST table captures records containing the cost of any medical event recorded in one of the OMOP clinical event tables such as DRUG_EXPOSURE, PROCEDURE_OCCURRENCE, VISIT_OCCURRENCE, VISIT_DETAIL, DEVICE_OCCURRENCE, OBSERVATION or MEASUREMENT.

Each record in the cost table account for the amount of money transacted for the clinical event. So, the COST table may be used to represent both receivables (charges) and payments (paid), each transaction type represented by its COST_CONCEPT_ID. The COST_TYPE_CONCEPT_ID field will use concepts in the Standardized Vocabularies to designate the source (provenance) of the cost data. A reference to the health plan information in the PAYER_PLAN_PERIOD table is stored in the record for information used for the adjudication system to determine the persons benefit for the clinical event.

    User guidance:     
    When dealing with summary costs, the cost of the goods or services the provider provides is often not known directly, but derived from the hospital charges multiplied by an average cost-to-charge ratio.
     """

    __tablename__ = 'COST'

    # From Field CSV row 264.
    COST_ID = mapped_column(
        Integer,
        primary_key=True,
        nullable=False
    )

    # From Field CSV row 265.
    COST_EVENT_ID = mapped_column(
        Integer,
        nullable=False
    )

    # From Field CSV row 266.
    COST_DOMAIN_ID = mapped_column(
        String(20),
        ForeignKey('VOCAB.DOMAIN.DOMAIN_ID'),
        nullable=False
    )

    # From Field CSV row 267.
    COST_TYPE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=False
    )

    # From Field CSV row 268.
    CURRENCY_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True
    )

    # From Field CSV row 269.
    TOTAL_CHARGE = mapped_column(
        Float,
        nullable=True
    )

    # From Field CSV row 270.
    TOTAL_COST = mapped_column(
        Float,
        nullable=True
    )

    # From Field CSV row 271.
    TOTAL_PAID = mapped_column(
        Float,
        nullable=True
    )

    # From Field CSV row 272.
    PAID_BY_PAYER = mapped_column(
        Float,
        nullable=True
    )

    # From Field CSV row 273.
    PAID_BY_PATIENT = mapped_column(
        Float,
        nullable=True
    )

    # From Field CSV row 274.
    PAID_PATIENT_COPAY = mapped_column(
        Float,
        nullable=True
    )

    # From Field CSV row 275.
    PAID_PATIENT_COINSURANCE = mapped_column(
        Float,
        nullable=True
    )

    # From Field CSV row 276.
    PAID_PATIENT_DEDUCTIBLE = mapped_column(
        Float,
        nullable=True
    )

    # From Field CSV row 277.
    PAID_BY_PRIMARY = mapped_column(
        Float,
        nullable=True
    )

    # From Field CSV row 278.
    PAID_INGREDIENT_COST = mapped_column(
        Float,
        nullable=True
    )

    # From Field CSV row 279.
    PAID_DISPENSING_FEE = mapped_column(
        Float,
        nullable=True
    )

    # From Field CSV row 280.
    PAYER_PLAN_PERIOD_ID = mapped_column(
        Integer,
        nullable=True
    )

    # From Field CSV row 281.
    AMOUNT_ALLOWED = mapped_column(
        Float,
        nullable=True
    )

    # From Field CSV row 282.
    REVENUE_CODE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True
    )

    # From Field CSV row 283.
    REVENUE_CODE_SOURCE_VALUE = mapped_column(
        String(50),
        nullable=True,
        comment="""Revenue codes are a method to charge for a class of procedures and conditions in the U.S. hospital system. """
    )

    # From Field CSV row 284.
    DRG_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True
    )

    # From Field CSV row 285.
    DRG_SOURCE_VALUE = mapped_column(
        String(3),
        nullable=True,
        comment="""Diagnosis Related Groups are US codes used to classify hospital cases into one of approximately 500 groups. """
    )


# From Table CSV row 20.
class drug_era(Base):
    """Description:
    A Drug Era is defined as a span of time when the Person is assumed to be exposed to a particular active ingredient. A Drug Era is not the same as a Drug Exposure: Exposures are individual records corresponding to the source when Drug was delivered to the Person, while successive periods of Drug Exposures are combined under certain rules to produce continuous Drug Eras. Every record in the DRUG_EXPOSURE table should be part of a drug era based on the dates of exposure. 
     """

    __tablename__ = 'DRUG_ERA'

    # From Field CSV row 286.
    DRUG_ERA_ID = mapped_column(
        Integer,
        primary_key=True,
        nullable=False
    )

    # From Field CSV row 287.
    PERSON_ID = mapped_column(
        Integer,
        ForeignKey('PERSON.PERSON_ID'),
        nullable=False
    )

    # From Field CSV row 288.
    DRUG_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""The drug_concept_id should conform to the concept class 'ingredient' as the drug_era is an era of time where a person is exposed to a particular drug ingredient. """
    )

    # From Field CSV row 289.
    DRUG_ERA_START_DATE = mapped_column(
        Date,
        nullable=False
    )

    # From Field CSV row 290.
    DRUG_ERA_END_DATE = mapped_column(
        Date,
        nullable=False
    )

    # From Field CSV row 291.
    DRUG_EXPOSURE_COUNT = mapped_column(
        Integer,
        nullable=True,
        comment="""The count of grouped DRUG_EXPOSURE records that were included in the DRUG_ERA row """
    )

    # From Field CSV row 292.
    GAP_DAYS = mapped_column(
        Integer,
        nullable=True
    )


# From Table CSV row 21.
class dose_era(Base):
    """Description:
    A Dose Era is defined as a span of time when the Person is assumed to be exposed to a constant dose of a specific active ingredient.
     """

    __tablename__ = 'DOSE_ERA'

    # From Field CSV row 293.
    DOSE_ERA_ID = mapped_column(
        Integer,
        primary_key=True,
        nullable=False
    )

    # From Field CSV row 294.
    PERSON_ID = mapped_column(
        Integer,
        ForeignKey('PERSON.PERSON_ID'),
        nullable=False
    )

    # From Field CSV row 295.
    DRUG_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""The Concept Id representing the specific drug ingredient. """
    )

    # From Field CSV row 296.
    UNIT_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""The Concept Id representing the unit of the specific drug ingredient. """
    )

    # From Field CSV row 297.
    DOSE_VALUE = mapped_column(
        Float,
        nullable=False,
        comment="""The numeric value of the dosage of the drug_ingredient. """
    )

    # From Field CSV row 298.
    DOSE_ERA_START_DATE = mapped_column(
        Date,
        nullable=False,
        comment="""The date the Person started on the specific dosage, with at least 31 days since any prior exposure. """
    )

    # From Field CSV row 299.
    DOSE_ERA_END_DATE = mapped_column(
        Date,
        nullable=False
    )


# From Table CSV row 22.
class condition_era(Base):
    """Description:
    A Condition Era is defined as a span of time when the Person is assumed to have a given condition. Similar to Drug Eras, Condition Eras are chronological periods of Condition Occurrence and every Condition Occurrence record should be part of a Condition Era. Combining individual Condition Occurrences into a single Condition Era serves two purposes:

- It allows aggregation of chronic conditions that require frequent ongoing care, instead of treating each Condition Occurrence as an independent event.
- It allows aggregation of multiple, closely timed doctor visits for the same Condition to avoid double-counting the Condition Occurrences.
For example, consider a Person who visits her Primary Care Physician (PCP) and who is referred to a specialist. At a later time, the Person visits the specialist, who confirms the PCP's original diagnosis and provides the appropriate treatment to resolve the condition. These two independent doctor visits should be aggregated into one Condition Era.
     """

    __tablename__ = 'CONDITION_ERA'

    # From Field CSV row 300.
    CONDITION_ERA_ID = mapped_column(
        Integer,
        primary_key=True,
        nullable=False
    )

    # From Field CSV row 301.
    PERSON_ID = mapped_column(
        Integer,
        nullable=False
    )

    # From Field CSV row 302.
    CONDITION_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=False,
        comment="""The Concept Id representing the Condition. """
    )

    # From Field CSV row 303.
    CONDITION_ERA_START_DATE = mapped_column(
        Date,
        nullable=False,
        comment="""The start date for the Condition Era
constructed from the individual
instances of Condition Occurrences.
It is the start date of the very first
chronologically recorded instance of
the condition with at least 31 days since any prior record of the same Condition. """
    )

    # From Field CSV row 304.
    CONDITION_ERA_END_DATE = mapped_column(
        Date,
        nullable=False,
        comment="""The end date for the Condition Era
constructed from the individual
instances of Condition Occurrences.
It is the end date of the final
continuously recorded instance of the
Condition. """
    )

    # From Field CSV row 305.
    CONDITION_OCCURRENCE_COUNT = mapped_column(
        Integer,
        nullable=True,
        comment="""The number of individual Condition
Occurrences used to construct the
condition era. """
    )


# From Table CSV row 23.
class metadata(Base):
    """Description:
    The METADATA table contains metadata information about a dataset that has been transformed to the OMOP Common Data Model.
     """

    __tablename__ = 'METADATA'

    METADATA_ID = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    # From Field CSV row 306.
    METADATA_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=False
    )

    # From Field CSV row 307.
    METADATA_TYPE_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=False
    )

    # From Field CSV row 308.
    NAME = mapped_column(
        String(250),
        nullable=False
    )

    # From Field CSV row 309.
    VALUE_AS_STRING = mapped_column(
        String(250),
        nullable=True
    )

    # From Field CSV row 310.
    VALUE_AS_CONCEPT_ID = mapped_column(
        Integer,
        ForeignKey('VOCAB.CONCEPT.CONCEPT_ID'),
        nullable=True
    )

    # From Field CSV row 311.
    METADATA_DATE = mapped_column(
        Date,
        nullable=True
    )

    # From Field CSV row 312.
    METADATA_DATETIME = mapped_column(
        DateTime,
        nullable=True
    )


# From Table CSV row 24.
class cdm_source(Base):
    """Description:
    The CDM_SOURCE table contains detail about the source database and the process used to transform the data into the OMOP Common Data Model.
     """

    __tablename__ = 'CDM_SOURCE'

    __mapper_args__ = {
        'primary_key': ('CDM_SOURCE_NAME', 'CDM_SOURCE_ABBREVIATION', 'CDM_HOLDER', 'CDM_VERSION')
    }

    # From Field CSV row 313.
    CDM_SOURCE_NAME = mapped_column(
        String(255),
        primary_key=True,
        nullable=False,
        comment="""The name of the CDM instance. """
    )

    # From Field CSV row 314.
    CDM_SOURCE_ABBREVIATION = mapped_column(
        String(25),
        primary_key=True,
        nullable=False,
        comment="""The abbreviation of the CDM instance. """
    )

    # From Field CSV row 315.
    CDM_HOLDER = mapped_column(
        String(255),
        primary_key=True,
        nullable=False,
        comment="""The holder of the CDM instance. """
    )

    # From Field CSV row 316.
    SOURCE_DESCRIPTION = mapped_column(
        String,
        nullable=True,
        comment="""The description of the CDM instance. """
    )

    # From Field CSV row 317.
    SOURCE_DOCUMENTATION_REFERENCE = mapped_column(
        String(255),
        nullable=True
    )

    # From Field CSV row 318.
    CDM_ETL_REFERENCE = mapped_column(
        String(255),
        nullable=True
    )

    # From Field CSV row 319.
    SOURCE_RELEASE_DATE = mapped_column(
        Date,
        nullable=True,
        comment="""The date the data was extracted from the source system. In some systems that is the same as the date the ETL was run. Typically the latest even date in the source is on the source_release_date. """
    )

    # From Field CSV row 320.
    CDM_RELEASE_DATE = mapped_column(
        Date,
        nullable=True,
        comment="""The date the ETL script was completed. Typically this is after the source_release_date. """
    )

    # From Field CSV row 321.
    CDM_VERSION = mapped_column(
        String(10),
        primary_key=True,
        nullable=False,
        comment="""Version of the OMOP CDM used as string. e.g. v5.4 """
    )

    # From Field CSV row 322.
    VOCABULARY_VERSION = mapped_column(
        String(20),
        nullable=True
    )