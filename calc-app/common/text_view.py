def display_table(columns, rows):

    headers = [c[0].ljust(c[2]) for c in columns]

    header_output = " | ".join(headers)

    output = header_output + "\n"
    output += "-" * len(header_output) + "\n"

    for row in rows:
        row_data = [str(row[c[1]]).ljust(c[2]) for c in columns]
        output += " | ".join(row_data) + "\n"

    return output
