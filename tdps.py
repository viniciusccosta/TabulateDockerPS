import re
import sys

from tabulate import tabulate


def format_ports_column(port_mappings):
    """Splits port mappings into separate lines if they exist."""
    return "\n".join(port_mappings.split(", ")) if port_mappings else ""


def process_docker_ps_output(lines):
    """Processes the input lines, finding the Ports column and formatting it."""
    # Headers:
    headers = re.sub(r"\s{2,}", "\t", lines[0]).strip()
    headers = headers.split("\t")

    # Columns divisions:
    indexes = [lines[0].index(header) for header in headers]

    data = []

    for line in lines[1:]:
        columns = [
            line[indexes[i] : indexes[i + 1]].strip() for i in range(len(indexes) - 1)
        ]
        formatted_columns = []

        for i, column in enumerate(columns):
            if headers[i].strip().lower() == "ports":
                formatted_columns.append(format_ports_column(column))
            else:
                formatted_columns.append(column.strip())

        data.append(formatted_columns)

    return headers, data


def main():
    # Step 1: Read the input from stdin
    lines = sys.stdin.read().splitlines()

    if not lines:
        print("No input received.")
        return

    # Step 2: Process the docker ps output
    headers, data = process_docker_ps_output(lines)

    # Step 3: Use `tabulate` to display the data
    table = tabulate(data, headers=headers, tablefmt="grid")
    print(table)


if __name__ == "__main__":
    # docker ps | python tdps.py
    # docker ps | python tdps.py --debug

    if "--debug" in sys.argv:
        import debugpy

        debugpy.listen(("localhost", 5678))
        print("Waiting for debugger to attach...")
        debugpy.wait_for_client()

    main()
