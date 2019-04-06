import os
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


def save_w2v(output_path, model):
    try:
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        model.save(os.path.join(output_path, "articles2vector.w2v"))
        return True
    except IOError as e:
        print('Error saving the model:', str(e))
