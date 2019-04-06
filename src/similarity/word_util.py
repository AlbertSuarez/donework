import csv
import string


translator = str.maketrans('', '', string.punctuation)


def clean_paragraph(paragraph):
    paragraph = paragraph.translate(translator)
    return paragraph.lower()


def load_csv(csv_filename):
    with open(csv_filename, newline='', encoding='utf-8') as f:
        rows = [row for row in csv.reader(f)]
    return rows
