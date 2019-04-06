import os
import string
import multiprocessing
import numpy as np
import gensim.models.word2vec as w2v

from src import *


def load_csv(csv_filename):
    with open(csv_filename, 'r', encoding='utf-8', errors='ignore') as f:
        rows = list(f.read().splitlines())
    return rows


def load_w2v(w2v_path):
    return w2v.Word2Vec.load(w2v_path)


def clean_paragraph(paragraph):
    translator = str.maketrans('', '', string.punctuation)
    paragraph = paragraph.translate(translator)
    return paragraph.lower().split()


def normalize(arguments):
    paragraph, paragraphs2vec = arguments
    vector_sum = 0
    paragraph = clean_paragraph(paragraph)
    n_words = 0
    for word in paragraph:
        if word in paragraphs2vec:
            vector_sum = vector_sum + paragraphs2vec[word]
            n_words += 1
    return vector_sum/n_words


def re_shape(paragraphs_vector):
    paragraphs_vector = np.array(paragraphs_vector)
    x = np.array(paragraphs_vector).reshape((paragraphs_vector.shape[0], NUM_FEATURES))
    return x


def config_w2v():
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


def save_w2v(output_path, model):
    try:
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        model.save(os.path.join(output_path, W2V_FILE_NAME))
        return True
    except IOError as e:
        print('Error saving the model:', str(e))
