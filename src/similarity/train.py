import os
import tqdm
import argparse

from multiprocessing.dummy import Pool as ThreadPool

from src import *
from src.util import log
from src.similarity.util import helper


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('output_path', type=str)
    return parser.parse_args()


def _generate_word2vec_model():
    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)

    log.info('Loading CSV...')
    csv_path = os.path.join(args.output_path, CSV_FILE_NAME)
    paragraphs = helper.load_csv(csv_path)

    log.info('CSV loaded - Starting to clean paragraphs...')
    text_corpus = []
    for paragraph in tqdm.tqdm(paragraphs, total=len(paragraphs)):
        text_corpus.append(helper.clean_paragraph(paragraph))
    log.info('Done! Now calling w2v library to configure the model.')
    articles2vec = helper.config_w2v()
    
    log.info('That seems very good :) Now the magic, I am going to start introducing the vocabulary...')
    articles2vec.build_vocab(text_corpus)
    log.info('Awesome. Finally... I am going to train the model. It will take a while hehe')
    sentences_count = articles2vec.corpus_count
    epochs_count = articles2vec.epochs
    log.info('Number of unique sentences: {}'.format(sentences_count))
    log.info('Number of unique epochs: {}'.format(epochs_count))
    articles2vec.train(text_corpus, total_examples=sentences_count, epochs=epochs_count)
    log.info('Trained!')

    helper.save_w2v(args.output_path, articles2vec)
    log.info('Model saved in: {}'.format(args.output_path))


if __name__ == '__main__':
    args = _parse_args()
    _generate_word2vec_model()
