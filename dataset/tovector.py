import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DIplom.settings")
django.setup()
import pandas as pd
import pickle
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from main.models import Book, BookVector


df = pd.read_csv('filtered_books.csv')


def lover_case(text):
    return text.lower()


def delete_punctuation(text):
    tokenizer = RegexpTokenizer(r'\w+')
    text = tokenizer.tokenize(text)
    text = " ".join(text)
    return text



df['description'] = df['description'].fillna('')
df['description'] = df['description'].apply(lover_case)
df['description'] = df['description'].apply(delete_punctuation)


vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(df['description'])

# Отримання вектора для книжки з ID 10
book_id = 10
book_vector = vectors[df[df['id'] == book_id].index[0]]

# Серіалізація вектора
serialized_vector = pickle.dumps(book_vector)

# Збереження вектора у базі даних
book_instance = Book.objects.get(id=book_id)
BookVector.objects.create(book=book_instance, vector=serialized_vector)
