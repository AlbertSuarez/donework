import argparse

from tqdm import tqdm
from os import listdir
from os.path import isfile, join
from multiprocessing.dummy import Pool as ThreadPool

from src import *


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('xml_folder', type=str)
    parser.add_argument('output_file', type=str)
    return parser.parse_args()


def _get_file(xml_filename):
    paragraphs = []
    with open(xml_filename, 'r', encoding='utf-8', errors='ignore') as xml_file:
        xml_string = xml_file.read()
        xml_lines = xml_string.splitlines()
        for line in xml_lines:
            if not line.startswith('<doc id=') and len(line) >= PARAGRAPH_LENGTH:
                paragraphs.append(line.replace('\n', ''))
    return paragraphs


def generate_dataset():
    xml_files = [join(args.xml_folder, f) for f in listdir(args.xml_folder) if isfile(join(args.xml_folder, f))]
    xml_files = [f for f in xml_files if f.endswith('.xml')]

    with ThreadPool(20) as pool:
        result_articles = list(tqdm(pool.imap(_get_file, xml_files, 1), total=len(xml_files)))

    paragraph_id = 0
    with open(args.output_file, 'w') as file:
        for article in tqdm(result_articles, total=len(result_articles)):
            for paragraph in article:
                file.write('{}\n'.format(paragraph))
                paragraph_id += 1
                if paragraph_id >= DATASET_LIMIT:
                    return


if __name__ == '__main__':
    args = _parse_args()
    generate_dataset()
