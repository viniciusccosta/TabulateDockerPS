import argparse
import re
import sys

import tabulate


def validate_format(format):
    """Validate if the format is one of tabulate's available formats."""
    formats_list = tabulate._table_formats.keys()

    if format not in formats_list:
        print(f"Invalid format: {format}. Available formats: {', '.join(formats_list)}")
        sys.exit(1)

    return format


def enable_debug():
    import debugpy

    debugpy.listen(("localhost", 5678))
    print("Waiting for debugger to attach...")
    debugpy.wait_for_client()


def format_ports_column(port_mappings):
    """Splits port mappings into separate lines if they exist."""
    return "\n".join(port_mappings.split(", ")) if port_mappings else ""


def process_docker_ps_output(lines):
    """Processes the input lines, finding the Ports column and formatting it."""
    # Extract and process headers
    headers = re.sub(r"\s{2,}", "\t", lines[0]).strip().split("\t")
    indexes = [lines[0].index(header) for header in headers]

    data = []
    for line in lines[1:]:
        columns = [
            line[indexes[i] : indexes[i + 1]].strip() for i in range(len(indexes) - 1)
        ]
        formatted_columns = [
            (
                format_ports_column(column)
                if headers[i].strip().lower() == "ports"
                else column.strip()
            )
            for i, column in enumerate(columns)
        ]

        data.append(formatted_columns)

    return headers, data


def main(tablefmt="grid"):
    # Step 1: Read the input from stdin
    lines = sys.stdin.read().splitlines()

    if not lines:
        print("No input received.")
        sys.exit(1)

    # Step 2: Process the docker ps output
    headers, data = process_docker_ps_output(lines)

    # Step 3: Use `tabulate` to display the data
    table = tabulate.tabulate(data, headers=headers, tablefmt=tablefmt)
    print(table)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Process 'docker ps' output.",
        usage="docker ps | python tdps.py [--debug] [--format FORMAT]",
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument(
        "--format",
        type=validate_format,
        default="grid",
        help="Specify the output format",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    if args.debug:
        enable_debug()

    main(args.format)
