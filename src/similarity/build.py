import os
import argparse

from tqdm import tqdm
from multiprocessing.dummy import Pool as ThreadPool

from src import *
from src.util import log
from src.similarity.util import helper
from src.similarity.util.nmslib import Nmslib


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('output_path', type=str)
    return parser.parse_args()


def _build():
    log.info('Loading CSV...')
    csv_path = os.path.join(args.output_path, CSV_FILE_NAME)
    rows = helper.load_csv(csv_path)
    log.info('CSV loaded. Paragraphs: {}'.format(len(rows)))

    log.info('Loading features...')
    w2v_path = os.path.join(args.output_path, W2V_FILE_NAME)
    paragraphs2vec = helper.load_w2v(w2v_path)
    log.info('Features loaded')

    log.info('Normalizing...')
    with ThreadPool(20) as pool:
        rows = [(row, paragraphs2vec) for row in rows]
        paragraphs_vector = list(tqdm(pool.imap(helper.normalize, rows, 1), total=len(rows)))
    log.info('Normalized. Vectors: {}'.format(len(paragraphs_vector)))

    log.info('Reshaping...')
    x = helper.re_shape(paragraphs_vector)
    log.info('Reshaped. Shape: {}'.format(x.shape))

    log.info('Building index...')
    index_path = os.path.join(args.output_path, INDEX_FILE_NAME)
    index = Nmslib()
    index.fit(x)
    index.save(index_path)
    log.info('Index built')


if __name__ == '__main__':
    args = _parse_args()
    _build()
