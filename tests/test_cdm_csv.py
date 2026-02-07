import os
import pytest

import topomop.cdm_csv

OMOP_CDM_CSV_DIR = os.environ.get('OMOP_CDM_CSV_DIR')
if not (
        OMOP_CDM_CSV_DIR
        and os.path.exists(OMOP_CDM_CSV_DIR)
        and os.path.isdir(OMOP_CDM_CSV_DIR)
):
    raise ValueError(
        'The environment variable OMOP_CDM_CSV_DIR must be the path '
        'to a directory where CSV files with OMOP CDM definitions '
        f'are located, not: {repr(OMOP_CDM_CSV_DIR)}.'
    )


def test_scan():
    definitions = topomop.cdm_csv.scan(OMOP_CDM_CSV_DIR)
    assert (
        set(topomop.cdm_csv.SUPPORTED_VERSIONS.keys())
        .issubset(set(definitions.keys()))
    )
    for version in topomop.cdm_csv.SUPPORTED_VERSIONS.keys():
        assert {'Table', 'Field'} == set(definitions[version].keys())


@pytest.mark.parametrize(
    'cdm_modulename',
    topomop.cdm_csv.SUPPORTED_VERSIONS.values()
)
class TestCdm:

    def test_cdm(self, cdm_modulename):
        cdm = topomop.cdm_csv.Cdm(OMOP_CDM_CSV_DIR, f'topomop.{cdm_modulename}')

    def test_iter_by_schema(self, cdm_modulename):
        cdm = topomop.cdm_csv.Cdm(OMOP_CDM_CSV_DIR, f'topomop.{cdm_modulename}')
        tuple(cdm.schemas())
