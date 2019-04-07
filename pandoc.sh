#!/usr/bin/env bash
sudo apt-get install pandoc  # install pandoc first in the server
pandoc -o output.pdf input.txt  # command to convert md to latex