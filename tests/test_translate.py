import jinja2
import os
import pytest
import textwrap

import topomop.cdm_csv
import topomop.translate

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


@pytest.mark.parametrize(
    'sqlalchemy_style',
    ('imperative', 'declarative')
)
@pytest.mark.parametrize(
    'cdm_version, cdm_modulename',
    topomop.cdm_csv.SUPPORTED_VERSIONS.items()
)
def test_translation_alchemy_importable(sqlalchemy_style, cdm_version, cdm_modulename):
    if cdm_modulename == 'cdmv5_4':
            pytest.xfail(
                'Field definition in CDM v5.4 has an invalid row index 353. '
                'See https://github.com/OHDSI/CommonDataModel/pull/766.'
            )

    cdm = topomop.cdm_csv.Cdm(OMOP_CDM_CSV_DIR, f'topomop.{cdm_modulename}')
    (name2schema, schema_defs,
     _patch_composite_primary_keys, _patch_override_attributes) = cdm.schemas()

    for schema_name, tables in schema_defs.items():
        source_code = topomop.translate.render_sqlalchemy(
            cdm_version,
            schema_name,
            name2schema,
            tables,
            style=sqlalchemy_style,
            comment_origin=True,
            _patch_composite_primary_keys_schema=_patch_composite_primary_keys.get(
                schema_name, {}
            ),
            _patch_override_attributes_schema=_patch_override_attributes.get(
                schema_name, {}
            )
        )
        context = {}
        exec(source_code, context)


@pytest.mark.parametrize(
    'sqlalchemy_style',
    ('imperative', 'declarative')
)
@pytest.mark.parametrize(
    'cdm_version, cdm_modulename',
    topomop.cdm_csv.SUPPORTED_VERSIONS.items()
)
def test_translation_sql(sqlalchemy_style, cdm_version, cdm_modulename):
    if cdm_modulename == 'cdmv5_4':
            pytest.xfail(
                'Field definition in CDM v5.4 has an invalid row index 353. '
                'See https://github.com/OHDSI/CommonDataModel/pull/766.'
            )

    cdm = topomop.cdm_csv.Cdm(OMOP_CDM_CSV_DIR, f'topomop.{cdm_modulename}')
    (name2schema, schema_defs,
     _patch_composite_primary_keys, _patch_override_attributes) = cdm.schemas()

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
            tables,
            style=sqlalchemy_style,
            comment_origin=True,
            _patch_composite_primary_keys_schema=_patch_composite_primary_keys.get(
                schema_name, {}
            ),
            _patch_override_attributes_schema=_patch_override_attributes.get(
                schema_name, {}
            )
        )
        exec(source_code, context)
