import re
from tensorflow.keras.preprocessing.sequence import pad_sequences
from nltk.corpus import stopwords
from pymystem3 import Mystem
import fasttext
import numpy
import tensorflow
import fasttext.util
import compress_fasttext


ft = compress_fasttext.models.CompressedFastTextKeyedVectors.load('model/comprassed.cc.ru.300.bin')
# ft = fasttext.load_model('model/cc.ru.300.bin')
STOP_WORDS = stopwords.words('russian')
pymystem = Mystem()
model = tensorflow.keras.models.load_model('model/news_classification_v2.h5')
MAX_NEWS_LEN = 100000


def predict_class(text) -> int:
    prepared_text = prepare_text(text)

    # Ограничение по максимальной длине статьи
    prepared_text[0] = prepared_text[0][:MAX_NEWS_LEN]

    x_predict = pad_sequences(prepared_text, maxlen=MAX_NEWS_LEN, dtype='float32')
    x_predict = numpy.reshape(x_predict, (1, 1, MAX_NEWS_LEN))

    predicted_class = model.predict(x_predict)
    print(predicted_class)
    # 3 условие value >= 0.5 and value < 0.6:

    if predicted_class[0][0][0] > 0.55:
        return 'Истина'
    else:
        return 'Ложь'


def prepare_text(text: str) -> list:
    tokens = words_numbers_only(text)
    normalized = remove(tokens)
    lemmas = lemmatize_state(normalized)
    vectorized = [j for i in lemmas for j in vectorize(i)]

    return [vectorized]


def words_numbers_only(text: str) -> list:
    """Tokenizacia"""

    regex = re.compile(r"\b[А-Яа-яЁё0-9A-Za-z-.,:]+\b")

    try:
        return regex.findall(text.lower())
    except:
        return []
    

def remove(sentences: list) -> list:
    """Remove stopwords"""

    return [word for word in sentences if not word in STOP_WORDS]


def lemmatize_state(state: list) -> list:

    return pymystem.lemmatize(' '.join(state))


def vectorize(state: list) -> list:

    result = [j for word in state for j in ft[word]]
    return result


if __name__ == "__main__":
    predict_class('Это тестовый текст, Новости хорошие')