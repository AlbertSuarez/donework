<br>
<p align="center">
  <img alt="Donework" src="donework.png" width="50%"/>
</p>
<br>

# Donework

[![HitCount](http://hits.dwyl.io/AlbertSuarez/donework.svg)](http://hits.dwyl.io/AlbertSuarez/donework)
[![GitHub stars](https://img.shields.io/github/stars/AlbertSuarez/donework.svg)](https://GitHub.com/AlbertSuarez/donework/stargazers/)
[![GitHub forks](https://img.shields.io/github/forks/AlbertSuarez/donework.svg)](https://GitHub.com/AlbertSuarez/donework/network/)
[![GitHub repo size in bytes](https://img.shields.io/github/repo-size/AlbertSuarez/donework.svg)](https://github.com/AlbertSuarez/donework)
[![GitHub contributors](https://img.shields.io/github/contributors/AlbertSuarez/donework.svg)](https://GitHub.com/AlbertSuarez/donework/graphs/contributors/)
[![GitHub license](https://img.shields.io/github/license/AlbertSuarez/donework.svg)](https://github.com/AlbertSuarez/donework/blob/master/LICENSE)

📚 Content generator given a table of content using Machine Learning and search similarity.

## Inspiration
We do love technology, but when it comes to writing essays, reports or compositions we tend to be a little lazy. Our writing skills can be really outrageous. So we decided to create something that allowed us to do all that boring stuff automatically. No more boring reports for students!

## What it does
**It creates content from an index, that is to say, it generates text.** Yeah, we know that it sounds really crazy but that's actually what it does.
The user writes a tiny index with a small description of each section. Then we look into a 50-dimensional feature (previously reduced) index with 1M Wikipedia paragraphs indexed. We take the nearest one and with that output, we generate the rest of the text using a Deep Learning model. The user can choose the level of randomness that is going to be used in the text generation. Moreover,  images can be added automatically to the text.

Finally, the user has the option to generate a LaTeX file with the content in a pdf.

## How we built it

All the project is built in Python with several libraries that makes this project possible.

As a phase one of the processing pipeline, the application receives a bunch of titles and descriptions that allows the user to search into a nmslib index. This is index was built thanks to the famous library called Word2Vec where we get all the features from a dataset from Wikipedia. That dataset was cleaned and formatted in order to get the best results as we can. We initially get a dataset of 5.2M of paragraphs but we finally decided to reduce it to 1M in order to train it faster.

As a phase two, we used the recent Unsupervised Learning Model developed by OpenAi **GPT2**. That model, among other things, is able to generate text by calculating the word that has the highest probability to go next by giving a context. We took the pre-trained model and trained with **Wikipedia data** in **Google Colab**, using tools like **Pandas** to see if we could make it generate better results. Then we took the output given by the index of paragraphs and generated text.
After that, we used **TextBlob** to analyze the output: that information was useful to generate an image of the text. The search of the image is done using **Google Custom Search API** and the output latex file is done using **Pandoc**.

We've hosted all this stack in a Google Engine thanks to Google Cloud Platform.

## Challenges we ran into

We are truly lovers of new technology and some of us are really interested in deep learning or natural language processing. However, we are not, by far, experts. Actually we are newbies in those topics, so we had to deal with a lot of stuff to finally accomplish what we wanted.

Specially we had problems with the size of datasets we wanted to deal with (we started with the idea of using **ALL WIKIPEDIA DATASET**) we did not have computing power for that. Also, we wanted to train the GPT-2 model, developed by OpenAI, taking advantage of the pretrained models, to see if we saw an improvement in the word predictions.

## Accomplishments that we're proud of

We are really proud of the final result. Even though it seemed impossible to get kinda good results and merge everything we finally could make something and add all the work that was done separately.

## What we learned

We've learned stuff about writing multithreading code, how to use Google Colab, about doing good Flask APIs, Unsupervised Learning Methods and organizing stuff correctly (which is really important guys :D).

## What's next for Donework
Trying to create a bigger index of paragraphs and spend more time with GPT-2 in order to get better results and understand completely those nasty and mysterious hyperparameters.

## Requirements

1. Python 3.6+

## Recommendations

Usage of [virtualenv](https://realpython.com/blog/python/python-virtual-environments-a-primer/) is recommended
for package library / runtime isolation.

## Usage

To run the server, please execute the following from the root directory:

1. Setup virtual environment

    ```bash
    virtualenv -p /usr/bin/python3.5 env
    source env/bin/activate
    ```

2. Install dependencies

    ```bash
    pip3 install -r requirements.txt
    ```

4. Run Flask server as a python module

    ```bash
    python3 -m src
    ```

## Authors

- [Adrià Cabeza](https://github.com/adriacabeza)
- [Xavier Lacasa](https://github.com/xlacasa)
- [Albert Suàrez](https://github.com/AlbertSuarez)
- [Elena Ruiz](https://github.com/elena20ruiz)

## License

MIT © Donework
