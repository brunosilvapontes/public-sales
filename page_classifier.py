import json
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.svm import LinearSVC


class PageClassifier:
    def __init__(self, homepage_name):
        self.page_path = f'crawled pages/{homepage_name}'
        self.confusion_matrix = ''
        self.accuracy_score = ''
        self.classification_report = ''

        with open(self.page_path, 'r') as f:
            self.json_dict = json.loads(f.read())


    def fit(self):
        df = pd.DataFrame(self.json_dict['pages'])
        X = df['text']
        y = df['label']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
        page_classifier = Pipeline([('tfidf', TfidfVectorizer()), ('cls', LinearSVC())])
        page_classifier.fit(X_train, y_train)
        predictions = page_classifier.predict(X_test)
        self.confusion_matrix = confusion_matrix(y_test, predictions)
        self.accuracy_score = accuracy_score(y_test, predictions)
        self.classification_report = classification_report(y_test, predictions)

    def predict(self, page):




pageIdentifier = PageClassifier('capital_leiloes.json')
