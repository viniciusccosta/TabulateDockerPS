#!/usr/bin/env python

import argparse
import re
import sys
import select

import tabulate

class NoInputException(Exception):
    pass

def validate_format(format):
    """Validate if the format is one of tabulate's available formats."""
    formats_list = tabulate._table_formats.keys()

    if format not in formats_list:
        print(f"Invalid format: {format}. Available formats: {', '.join(formats_list)}")
        sys.exit(1)

    return format

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
            line[indexes[i]:indexes[i + 1]].strip() if i < len(indexes) - 1 else line[indexes[i]:].strip()
            for i in range(len(indexes))
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
    # TODO: What if we execute `docker ps` instead of piping the output?
    
    # Step 1: Check if there's input available on stdin
    if not select.select([sys.stdin], [], [], 0.1)[0]:
        # TODO: Add a check for the `docker ps` command
        raise NoInputException()
    
    # Step 2: Read the input from stdin
    lines = sys.stdin.read().splitlines()

    if not lines:
        raise NoInputException()

    # Step 3: Process the docker ps output
    headers, data = process_docker_ps_output(lines)

    # Step 4: Use `tabulate` to display the data
    table = tabulate.tabulate(data, headers=headers, tablefmt=tablefmt)
    print(table)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Process 'docker ps' output.",
        usage="docker ps | tdps [--tablefmt TABLEFMT]",
    )
    
    # Get the list of available formats
    available_formats = ", ".join(tabulate._table_formats.keys())
    
    parser.add_argument(
        "--tablefmt",
        type=validate_format,
        default="grid",
        help=f"Table format to use. Available formats: {available_formats}",
        # choices=list(tabulate._table_formats.keys()),
        
    )
    
    return parser


def entry_point():
    parser = parse_arguments()
    args = parser.parse_args()
    
    try:
        main(tablefmt=args.tablefmt,)
    except NoInputException:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    entry_point()
