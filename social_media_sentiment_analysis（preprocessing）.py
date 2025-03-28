# -*- coding: utf-8 -*-
"""Social Media Sentiment Analysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/11jxvI0D5wJRtXCB133rmw3QjIa940KDb
"""

pip install pandas numpy scikit-learn nltk

from google.colab import files

uploaded = files.upload()

import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

nltk.download('stopwords')

df = pd.read_csv("sentiment_analysis.csv")
df.dropna(inplace=True)

stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = ' '.join([word for word in text.split() if word not in stop_words])
    return text

df['clean_text'] = df['text'].apply(clean_text)

vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(df['clean_text'])

df['sentiment'] = df['sentiment'].astype('category').cat.codes
y = df['sentiment']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification reports:\n", classification_report(y_test, y_pred))

import os

if not os.path.exists("dataset"):
    os.makedirs("dataset")

import shutil

shutil.move("sentiment_analysis.csv", "dataset/sentiment_analysis.csv")

!ls dataset/

import os
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

os.makedirs("dataset", exist_ok=True)
os.makedirs("models", exist_ok=True)

nltk.download('stopwords')

data_path = "dataset/sentiment_analysis.csv"
if not os.path.exists(data_path):
    raise FileNotFoundError(f"❌ Dataset not found {data_path}，Please check the dataset/ directory！")

df = pd.read_csv(data_path)
df.dropna(inplace=True)

stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = ' '.join([word for word in text.split() if word not in stop_words])
    return text

df['clean_text'] = df['text'].apply(clean_text)

label_encoder = LabelEncoder()
df['sentiment'] = label_encoder.fit_transform(df['sentiment'])

joblib.dump(label_encoder, "models/label_encoder.pkl")

vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(df['clean_text'])
y = df['sentiment']

joblib.dump(vectorizer, "models/tfidf_vectorizer.pkl")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

joblib.dump((X_train, X_test, y_train, y_test), "dataset/split_data.pkl")

print("The data preprocessing is complete and the file has been saved to dataset/split_data.pkl！")

!python src/preprocess.py

!python src/train_ml.py

import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

X_train, X_test, y_train, y_test = joblib.load("dataset/split_data.pkl")

model = LogisticRegression()
model.fit(X_train, y_train)

joblib.dump(model, "models/logistic_regression.pkl")

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print("Accuracy:", accuracy)
print("Classification reports:\n", report)

with open("results/classification_report.txt", "w") as f:
    f.write(report)

print("The machine learning model is trained！")

import joblib
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
import matplotlib.pyplot as plt

X_train, X_test, y_train, y_test = joblib.load("dataset/split_data.pkl")

tokenizer = Tokenizer(num_words=5000)
X_train_seq = pad_sequences(X_train.toarray(), maxlen=100)
X_test_seq = pad_sequences(X_test.toarray(), maxlen=100)

model = Sequential([
    Embedding(input_dim=5000, output_dim=128, input_length=100),
    LSTM(64, return_sequences=True),
    LSTM(32),
    Dense(32, activation='relu'),
    Dropout(0.5),
    Dense(3, activation='softmax')
])

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

history = model.fit(X_train_seq, y_train, batch_size=32, epochs=5, validation_data=(X_test_seq, y_test))

model.save("models/lstm_model.h5")

plt.plot(history.history['accuracy'], label='train_accuracy')
plt.plot(history.history['val_accuracy'], label='val_accuracy')
plt.legend()
plt.savefig("results/accuracy_plot.png")
plt.show()

print("The training of the deep learning model is complete！")

import joblib
import tensorflow as tf
from sklearn.metrics import accuracy_score, classification_report

X_train, X_test, y_train, y_test = joblib.load("dataset/split_data.pkl")

ml_model = joblib.load("models/logistic_regression.pkl")
y_pred_ml = ml_model.predict(X_test)

print("Machine learning model accuracy:", accuracy_score(y_test, y_pred_ml))
print("Machine Learning Classification Report:\n", classification_report(y_test, y_pred_ml))

dl_model = tf.keras.models.load_model("models/lstm_model.h5")
X_test_seq = pad_sequences(X_test.toarray(), maxlen=100)
y_pred_dl = dl_model.predict(X_test_seq).argmax(axis=1)

print("Depth learning model accuracy:", accuracy_score(y_test, y_pred_dl))
print("In-depth study classification report:\n", classification_report(y_test, y_pred_dl))

import os

os.system("python src/preprocess.py")

os.system("python src/train_ml.py")

os.system("python src/train_dl.py")

os.system("python src/evaluate.py")

!python3 main.py
!ls /content/