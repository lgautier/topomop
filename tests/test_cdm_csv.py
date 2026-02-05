import os
import pytest

import topomop.cdm_csv

CSVS_PATH = 'tmp/CommonDataModel/inst/csv'


def test_scan():
    definitions = topomop.cdm_csv.scan(CSVS_PATH)
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
        cdm = topomop.cdm_csv.Cdm(CSVS_PATH, f'topomop.{cdm_modulename}')

    def test_iter_by_schema(self, cdm_modulename):
        cdm = topomop.cdm_csv.Cdm(CSVS_PATH, f'topomop.{cdm_modulename}')
        tuple(cdm.schemas())
