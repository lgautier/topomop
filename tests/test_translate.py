import jinja2
import pytest
import textwrap

import topomop.cdm_csv
import topomop.translate

CSVS_PATH = 'tmp/CommonDataModel/inst/csv'


@pytest.mark.parametrize(
    'cdm_version, cdm_modulename',
    topomop.cdm_csv.SUPPORTED_VERSIONS.items()
)
def test_translation_alchemy_importable(cdm_version, cdm_modulename):
    cdm = topomop.cdm_csv.Cdm(CSVS_PATH, f'topomop.{cdm_modulename}')
    name2schema, schema_defs = cdm.schemas()
    for schema_name, tables in schema_defs.items():
        source_code = topomop.translate.render_sqlalchemy(
            cdm_version,
            schema_name,
            name2schema,
            tables
        )
        context = {}
        exec(source_code, context)


@pytest.mark.parametrize(
    'cdm_version, cdm_modulename',
    topomop.cdm_csv.SUPPORTED_VERSIONS.items()
)
def test_translation_sql(cdm_version, cdm_modulename):
    cdm = topomop.cdm_csv.Cdm(CSVS_PATH, f'topomop.{cdm_modulename}')
    name2schema, schema_defs = cdm.schemas()

    context = {}
    exec(textwrap.dedent("""
    import sqlalchemy
    engine = sqlalchemy.create_engine("sqlite:///:memory:")
    """), context)

    for schema_name in topomop.cdm_csv.Schema:
        tables = schema_defs[schema_name.value]
        if len(tables) == 0:
            continue
        context['schema_name'] = schema_name.value

        template = jinja2.Template(
            textwrap.dedent(
                """
                @sqlalchemy.event.listens_for(engine, "connect")
                def connect(dbapi_conn, rec):
                    dbapi_conn.execute("ATTACH DATABASE ':memory:' AS {{ schema_name }}")
                """
            )
        )
        source_code_connect_callback = template.render(context)
        exec(
            source_code_connect_callback,
            context
        )

        source_code = topomop.translate.render_sqlalchemy(
            cdm_version,
            schema_name.value,
            name2schema,
            tables
        )
        exec(source_code, context)
