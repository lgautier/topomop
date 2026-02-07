import argparse
import os
import sys
import textwrap
import topomop.cdm_csv
import topomop.translate


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'cdm_version',
        choices=tuple(topomop.cdm_csv.SUPPORTED_VERSIONS.keys()),
        help='Version of the OMOP CDM to work with.'
    )
    parser.add_argument(
        '-s', '--source',
        help=textwrap.dedent(
            """Source for CDM definitions as a path (directory)
            that contains the CSV files for the requested version"""
        )
    )
    parser.add_argument(
        '-d', '--destination',
        help=textwrap.dedent(
            """Destination for the converstion (a path where files
            will be saved)."""
        )
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    # TODO: add checks and informative error messages.
    cdm_modulename = topomop.cdm_csv.SUPPORTED_VERSIONS[args.cdm_version]
    cdm = topomop.cdm_csv.Cdm(args.source, f'topomop.{cdm_modulename}')

    try:
        name2schema, schema_defs = cdm.schemas()
    except FileNotFoundError as err:
        print(err)
        sys.exit(1)

    output_already_exist = []
    for schema_name in schema_defs.keys():
        output_file_path = os.path.join(
            args.destination,
            f'omop_cdm_{cdm_modulename}_{schema_name}.py'
        )
        if os.path.exists(output_file_path):
            output_already_exist.append(output_file_path)

    if output_already_exist:
        print(
            f'Error: Output files already exist in {args.destination}: '
            f'{repr(output_already_exist)}.'
        )
        sys.exit(1)

    name2schema, schema_defs = cdm.schemas()
    for schema_name, tables in schema_defs.items():
        source_code = topomop.translate.render_sqlalchemy(
            args.cdm_version,
            schema_name,
            name2schema,
            tables
        )
        output_file_path = os.path.join(
            args.destination,
            f'omop_cdm_{cdm_modulename}_{schema_name}.py'
        )
        with open(output_file_path, 'w') as fh:
            fh.write(source_code)
        print(f'Generated code saved to {output_file_path}')

