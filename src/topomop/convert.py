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
            """Destination for the conversion (a path where files
            will be saved)."""
        )
    )
    parser.add_argument(
        '-f', '--force',
        action='store_true',
        help=textwrap.dedent(
            "Force overwriting existing files."
        )
    )
    parser.add_argument(
        '--style',
        choices=('declarative', 'imperative'),
        default='imperative',
        help=textwrap.dedent(
            """SQLAlchemy style for class mapping (default: %(default)s)."""
        )
    )
    parser.add_argument(
        '--no-comment-origin',
        action='store_true',
        help=textwrap.dedent(
            """Do not add the origin of the data definition as a comment."""
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
        (
            name2schema,
            schema_defs,
            _patch_composite_primary_keys,
            _patch_override_attributes
         ) = cdm.schemas()
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
        if args.force:
            print(
                f'Warning: Output files overwritten in {args.destination}: '
                f'{repr(output_already_exist)}.'
            )
        else:
            print(
                f'Error: Output files already exist in {args.destination}: '
                f'{repr(output_already_exist)}.'
            )
            sys.exit(1)

    for schema_name, tables in schema_defs.items():
        source_code = topomop.translate.render_sqlalchemy(
            args.cdm_version,
            schema_name,
            name2schema,
            tables,
            style=args.style,
            comment_origin=not args.no_comment_origin,
            _patch_composite_primary_keys_schema=_patch_composite_primary_keys.get(schema_name, {}),
            _patch_override_attributes_schema=_patch_override_attributes.get(schema_name, {})
        )
        output_file_path = os.path.join(
            args.destination,
            f'omop_cdm_{cdm_modulename}_{schema_name}.py'
        )
        with open(output_file_path, 'w') as fh:
            fh.write(source_code)
        print(f'Generated code saved to {output_file_path}')

