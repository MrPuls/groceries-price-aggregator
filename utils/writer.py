import csv


def write_to_csv(filename, header, data):
    with open(f'{filename}.csv', 'w', newline='', encoding="utf-8") as csvfile:
        fieldnames = header
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)