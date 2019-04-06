

import src.similarity.word_util 
import multiprocessing

from src import *
from src.util import log

def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_file', type=str)
    parser.add_argument('output_path', type=str)
    return parser.parse_args()

def _config_w2v():
    articles2vector = w2v.Word2Vec(
        sg=1,
        seed=2,
        workers=multiprocessing.cpu_count(),
        size=NUM_FEATURES,
        min_count=MIN_WORD_COUNT,
        window=CONTEXT_SIZE,
        model='simple'
        sample=DOWNSAMPLING
    )
    return articles2vector

    

def _generate_word2vec_model():
    docs = load_csv(args.csv_file)

    log.info('articles.csv loaded - Starting to clean paragrahs...')
    text_corpus = docs.apply(word_util.clean_paragraph)
    log.info('Done! Now calling w2v library to configure the model.')
    articles2vector = _config_w2v()
    
    log.info('That seems very good :) Now the magic, I am going to start introducing the vocabulary...')
    articles2vector.build_vocab(text_corpus)
    log.info('Awesome. Finally... I am going to train the model. It will take a while hehe')
    articles2vector.train(text_corpus)
    log.info('READY TO SAVE!')

    return articles2vector

if __name__ == '__main__':
    args = _parse_args()
    articles2vector = _generate_word2vec_model()
    output_path = args.output_path
    word_util.save_model(output_path, articles2vector)
    log.info('Model saved in:', output_path)
