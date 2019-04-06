import os
import argparse

from src import *
from src.util import log
from src.similarity.util import helper
from src.similarity.util.nmslib import Nmslib


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('output_path', type=str)
    return parser.parse_args()


def _load_index():
    index_path = os.path.join(args.output_path, INDEX_FILE_NAME)
    index = Nmslib()
    index.load(index_path)
    return index


def _load_csv():
    csv_path = os.path.join(args.output_path, CSV_FILE_NAME)
    paragraphs = helper.load_csv(csv_path)
    return paragraphs


def _extract_features(title, description):
    new_paragraph = title + description

    w2v_path = os.path.join(args.output_path, W2V_FILE_NAME)
    new_paragraph_model = helper.load_w2v(w2v_path)

    paragraphs_vector = helper.normalize((new_paragraph, new_paragraph_model))
    x = paragraphs_vector.reshape((1, NUM_FEATURES))

    return x


def _search(index, features, paragraphs):
    results = index.batch_query(features, NEIGHBOURHOOD_AMOUNT)
    closest, distances = results[0]

    duplicate_text = ''
    for paragraph_id, dist in zip(closest, distances):
        m = paragraphs[paragraph_id]
        paragraph_text = '{}'.format(m[1])
        if not duplicate_text:
            duplicate_text = paragraph_text
        log.info('Searching... Distance: {} | Paragraph: {}'.format(dist, paragraph_text))

    return duplicate_text


def search(title, description):
    log.info('Loading index...')
    index = _load_index()
    log.info('Index loaded. Index: {}'.format(index))

    log.info('Loading CSV...')
    paragraphs = _load_csv()
    log.info('CSV loaded. Rows: {}'.format(len(paragraphs)))

    log.info('Extracting features...')
    features = _extract_features(title, description)
    log.info('Features extracted.')

    log.info('Searching...')
    duplicate_text = _search(index, features, paragraphs)
    log.info('Done! {}'.format(duplicate_text))

    return duplicate_text


if __name__ == '__main__':
    args = _parse_args()
    log.info(search('Aristocrats', 'Jesters and their masters.'))
