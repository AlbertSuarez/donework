import tqdm
import argparse
import multiprocessing

import gensim.models.word2vec as w2v

from src import *
from src.util import log
from src.similarity import word_util


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_file', type=str)
    parser.add_argument('output_path', type=str)
    return parser.parse_args()


def _config_w2v():
    articles2vec = w2v.Word2Vec(
        sg=1,
        seed=2,
        workers=multiprocessing.cpu_count(),
        size=NUM_FEATURES,
        min_count=MIN_WORD_COUNT,
        window=CONTEXT_SIZE,
        sample=DOWNSAMPLING
    )
    return articles2vec


def _generate_word2vec_model():
    docs = word_util.load_csv(args.csv_file)
    paragraphs = [d[1] for d in docs]

    log.info('articles.csv loaded - Starting to clean paragraphs...')
    text_corpus = []
    for paragraph in tqdm.tqdm(paragraphs):
        text_corpus.append(word_util.clean_paragraph(paragraph))
    log.info('Done! Now calling w2v library to configure the model.')
    articles2vec = _config_w2v()
    
    log.info('That seems very good :) Now the magic, I am going to start introducing the vocabulary...')
    articles2vec.build_vocab(text_corpus)
    log.info('Awesome. Finally... I am going to train the model. It will take a while hehe')
    unique_words = len(articles2vec.wv.vocab)
    log.info('Number of unique words: {}'.format(unique_words))
    articles2vec.train(text_corpus, total_words=unique_words, epochs=1)
    log.info('READY TO SAVE!')

    return articles2vec


if __name__ == '__main__':
    args = _parse_args()
    articles2vector = _generate_word2vec_model()
    word_util.save_w2v(args.output_path, articles2vector)
    log.info('Model saved in: {}'.format(args.output_path))
