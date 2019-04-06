import argparse
import sklearn
import numpy as np
import gensim.models.word2vec as w2v

from tqdm import tqdm
from multiprocessing.dummy import Pool as ThreadPool

from src.util import log
from src.similarity.nmslib_util import Nmslib
from src.similarity.word_util import clean_paragraph, load_csv


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_file', type=str)
    parser.add_argument('w2v_file', type=str)
    parser.add_argument('index_file', type=str)
    return parser.parse_args()


def _load_features():
    return w2v.Word2Vec.load(args.w2v_file)


def _normalize(paragraph):
    vector_sum = 0
    paragraph = clean_paragraph(paragraph)
    words = paragraph.split()
    for word in words:
        vector_sum = vector_sum + paragraphs2vec[word]
    vector_sum = vector_sum.reshape(1, -1)
    normalised_vector_sum = sklearn.preprocessing.normalize(vector_sum)
    return normalised_vector_sum


def _build():
    log.info('Loading CSV...')
    rows = load_csv(args.csv_file)
    log.info('CSV loaded. Paragraphs: {}'.format(len(rows)))

    log.info('Normalizing...')
    with ThreadPool(20) as pool:
        paragraphs_vector = list(tqdm(pool.imap(_normalize, rows, 1), total=len(rows)))
    log.info('Normalized. Vectors: {}'.format(len(paragraphs_vector)))

    log.info('Reshaping...')
    x = np.array(paragraphs_vector).reshape((47, 50))
    log.info('Reshaped. Shape: {}'.format(x.shape))

    log.info('Building index...')
    index = Nmslib()
    index.fit(x)
    index.save(args.index_file)
    log.info('Index built')


if __name__ == '__main__':
    args = _parse_args()
    paragraphs2vec = _load_features()
    _build()
