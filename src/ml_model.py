import sqlite3
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB 
from sklearn.linear_model import SGDClassifier

class JarvisModel:
    def __init__(self):
        self.pipeline = Pipeline([
            ('count_vect', CountVectorizer()),
            ('tf_transformer', TfidfTransformer(use_idf=False))
        ])
        self.label_encoder = LabelEncoder()
        self.clf = SGDClassifier()

    def import_db(self, db_path="data/jarvis.db"):
        """ Load training data from SQLite database """
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM training_data")
            data = c.fetchall()
            X, y = zip(*data)
        return list(X), list(y)

    def train(self, X_train, y_train):
        """ Train classifier with preprocessing """
        X_train_tf = self.pipeline.fit_transform(X_train)
        y_train_encoded = self.label_encoder.fit_transform(y_train)
        self.clf.fit(X_train_tf, y_train_encoded)

    def predict(self, X_test):
        """ Predicts text category """
        X_test_tf = self.pipeline.transform(X_test)
        y_pred = self.clf.predict(X_test_tf)
        return self.label_encoder.inverse_transform(y_pred)
