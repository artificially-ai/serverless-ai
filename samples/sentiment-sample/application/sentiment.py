from nltk.tokenize import word_tokenize

import numpy as np

from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model

import json


def classify(context, event):
    message_body = event.body.decode('utf-8')
    context.logger.info(f"Message body extracted: '{message_body}'")

    n_unique_words = 10000
    max_review_length = 200
    pad_type = trunc_type = 'pre'

    word_index = imdb.get_word_index()
    word_index = {k: (v + 3) for k, v in word_index.items()}
    word_index['PAD'] = 0
    word_index['START'] = 1
    word_index['UNK'] = 2

    review_tokens = word_tokenize(message_body)

    review_index = [v if v <= n_unique_words else 3 for k, v in word_index.items() if k in review_tokens]
    review_index = np.array([review_index], dtype='int32')
    review_index.reshape((len(review_index[0])))

    review_index = pad_sequences(review_index, maxlen=max_review_length, padding=pad_type, truncating=trunc_type,
                                 value=0)

    model = load_model('/opt/nuclio/model/imdb-deep-net.hdf5')
    prediction = model.predict_proba(review_index).ravel()
    result = {'review': message_body, 'sentiment': f'{(prediction[0] * 100):.2f}% positive.'}

    return context.Response(body=json.dumps(result),
                            headers={},
                            content_type='application/json',
                            status_code=200)
