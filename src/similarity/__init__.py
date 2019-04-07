import os

from src import *
from src.similarity.util import helper
from src.similarity.util.nmslib import Nmslib


csv_path = os.path.join(OUTPUT_PATH, CSV_FILE_NAME)
paragraphs = helper.load_csv(csv_path)

index_path = os.path.join(OUTPUT_PATH, INDEX_FILE_NAME)
nmslib_index = Nmslib()
nmslib_index.load(index_path)


__all__ = [
    'paragraphs',
    'nmslib_index'
]
