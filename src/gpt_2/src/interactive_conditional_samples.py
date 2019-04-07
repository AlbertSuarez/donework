#!/usr/bin/env python3
import fire
import json
import os
import numpy as np
import tensorflow as tf

from src import *
import src.gpt_2.src.model as model
import src.gpt_2.src.sample as sample
import src.gpt_2.src.encoder as encoder


generatedText = ""
inputText = ""
randomness = 85


def interact_model(model_name='117M', seed=None, nsamples=1, batch_size=1, length=None, temperature=0.85, top_k=100):
    global generatedText
    global inputText

    if batch_size is None:
        batch_size = 1
    assert nsamples % batch_size == 0

    enc = encoder.get_encoder(model_name)
    hparams = model.default_hparams()
    with open(os.path.join(MODEL_PATH, model_name, 'hparams.json')) as f:
        hparams.override_from_dict(json.load(f))

    if length is None:
        length = hparams.n_ctx // 2
    elif length > hparams.n_ctx:
        raise ValueError("Can't get samples longer than window size: %s" % hparams.n_ctx)

    with tf.Session(graph=tf.Graph()) as sess:
        context = tf.placeholder(tf.int32, [batch_size, None])
        np.random.seed(seed)
        tf.set_random_seed(seed)
        global randomness
        output = sample.sample_sequence(
            hparams=hparams, 
            length=length,
            context=context,
            batch_size=batch_size,
            temperature=randomness/100, top_k=100-randomness+1
        )

        saver = tf.train.Saver()
        ckpt = tf.train.latest_checkpoint(os.path.join(MODEL_PATH, model_name))
        saver.restore(sess, ckpt)

        raw_text = inputText
        context_tokens = enc.encode(raw_text)
        generated = 0
        for _ in range(nsamples // batch_size):
            out = sess.run(output, feed_dict={
                context: [context_tokens for _ in range(batch_size)]
            })[:, len(context_tokens):]
            for i in range(batch_size):
                generated += 1
                text = enc.decode(out[i])
                text = text.split("<|endoftext|>", 1)[0]
                generatedText += text


if __name__ == '__main__':
    fire.Fire(interact_model)


def generate_sample(input_text, rand):
    global generatedText
    global inputText
    global randomness
    randomness = rand
    inputText = input_text
    generatedText = ""
    fire.Fire(interact_model)
    return generatedText
