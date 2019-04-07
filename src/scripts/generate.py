import argparse

from tqdm import tqdm

from src.similarity.search import search
from src.util import log


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('md_file', type=str)
    parser.add_argument('output_path', type=str)
    return parser.parse_args()


def generate(md_text):
    paragraphs_generated = []
    content = [line for line in md_text.splitlines() if line]

    for c in range(0, len(content), 2):
        paragraphs_generated.append([content[c], content[c + 1]])

    for idx, data in tqdm(enumerate(paragraphs_generated), total=len(paragraphs_generated)):
        paragraphs_generated[idx].append(search(data[0], data[1]))

    return paragraphs_generated


if __name__ == '__main__':
    args = _parse_args()
    with open(args.md_file, 'r', encoding='utf-8') as f:
        md_text_file = f.read()
    log.info(generate(md_text_file))
