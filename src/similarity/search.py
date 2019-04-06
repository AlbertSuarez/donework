import os
import argparse

from src import *
from src.util import log
from src.similarity.nmslib_util import Nmslib
from src.similarity.word_util import load_csv


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
    paragraphs = load_csv(csv_path)
    return paragraphs


def _extract_features():
    return []


def _search(index, features, paragraphs):
    results = index.knnQueryBatch(features, NEIGHBOURHOOD_AMOUNT)
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
    features = _extract_features()
    log.info('Features extracted.')


if __name__ == '__main__':
    args = _parse_args()
    search('Introduction', 'Few concepts about the whale characteristics.')
