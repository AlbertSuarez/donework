import glob
import numpy as np
import os
import random
import tensorflow as tf
from multiprocessing.dummy import Pool as ThreadPool

def _get_file(files):
    raw_text = ''
    token_chunks = []
    path = files[0]
 

    # Plain text
    with open(path, 'r') as fp:
        raw_text += fp.read()
    if len(raw_text) >= files[1]:
        tokens = np.stack(files[2].encode(raw_text))
        print(tokens)
        token_chunks.append(tokens)
        raw_text = ''
    else:
        raw_text += '<|endoftext|>'
    return raw_text, token_chunks

def load_dataset(enc, path, combine):
    paths = []
    if os.path.isfile(path):
        # Simple file
        paths.append(path)
    elif os.path.isdir(path):
        # Directory
        for (dirpath, _, fnames) in os.walk(path):
            for fname in fnames:
                paths.append(os.path.join(dirpath, fname))
    else:
        # Assume glob
        paths = glob.glob(path)

    raw_text = ''
    token_chunks = []
    files = [(f,combine,enc) for f in paths]
    with ThreadPool(14) as pool:
        print("crea threads, voy a hacer cosas paralelas")
        result = list(pool.imap(_get_file,files,1))
  


    llista_raw_text = [result[i][0] for i in range(0,len(result))]
    llista_raw_text = [item for sublist in llista_raw_text for item in sublist ]
    raw_text.join = llista_raw_text[0]
    print(raw_text)

    token_chunks = [result[i][1] for i in range(0,len(result))]
    token_chunks = [item for sublist in token_chunks for item in sublist]
    print(token_chunks)
    

    if raw_text:
        tokens = np.stack(enc.encode(raw_text))
        token_chunks.append(tokens)
    return token_chunks


def binary_search(f, lo, hi):
    if f(lo) or not f(hi):
        return None
    while hi > lo + 1:
        mid = (lo + hi) // 2
        if f(mid):
            hi = mid
        else:
            lo = mid
    return hi


class Sampler(object):
    """Fairly samples a slice from a set of variable sized chunks.

    'Fairly' means that the distribution is the same as sampling from one concatenated chunk,
    but without crossing chunk boundaries."""

    def __init__(self, chunks):
        self.chunks = chunks
        self.total_size = sum(chunk.shape[0] for chunk in chunks)
        self.boundaries = [0]
        for i in range(len(chunks)):
            self.boundaries.append(self.boundaries[-1] + chunks[i].shape[0])

    def sample(self, length):
        assert length < self.total_size // len(
            self.chunks
        ), "Dataset files are too small to sample {} tokens at a time".format(
            length)
        while True:
            index = random.randint(0, self.total_size - length - 1)
            i = binary_search(lambda j: self.boundaries[j] > index, 0,
                              len(self.boundaries) - 1) - 1
            if self.boundaries[i + 1] > index + length:
                within_chunk = index - self.boundaries[i]
                return self.chunks[i][within_chunk:within_chunk + length]
