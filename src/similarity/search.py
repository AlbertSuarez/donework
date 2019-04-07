import os

from src import *
from src.similarity import paragraphs, nmslib_index
from src.util import log
from src.similarity.util import helper


def _extract_features(title, description):
    new_paragraph = title + description

    w2v_path = os.path.join(OUTPUT_PATH, W2V_FILE_NAME)
    new_paragraph_model = helper.load_w2v(w2v_path)

    paragraphs_vector = helper.normalize((new_paragraph, new_paragraph_model))
    x = paragraphs_vector.reshape((1, NUM_FEATURES))

    return x


def _search(index, features):
    results = index.batch_query(features, NEIGHBOURHOOD_AMOUNT)
    closest, distances = results[0]

    duplicate_text = None
    for paragraph_id, dist in zip(closest, distances):
        paragraph_text = paragraphs[paragraph_id]
        if not duplicate_text and dist <= DISTANCE_THRESHOLD:
            duplicate_text = paragraph_text
        log.info('Searching... Distance: {} | ID: {} | Length: {}'.format(dist, paragraph_id, len(paragraph_text)))
        log.info(paragraph_text)

    return duplicate_text


def search(title, description):
    log.info('Extracting features...')
    features = _extract_features(title, description)
    log.info('Features extracted.')

    log.info('Searching...')
    duplicate_text = _search(nmslib_index, features)
    log.info('Done! {}'.format(duplicate_text))

    return duplicate_text


if __name__ == '__main__':
    log.info(search('Introduction', 'The history is always important'))
