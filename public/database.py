import mysql.connector

from core.dictionary import Dictionary
from core.ngram.ngram_model import NGramModel
from core.ngram.ngram_prediction import NGramPrediction
from core.ngram.ngram import NGram


class Database:
    def __init__(self):
        self.connector = mysql.connector.connect(
            option_files="/home/jack0042/.my.cnf",
            option_groups="client",
            database="jack0042_ngram_text_generator"
        )
        self.cursor = self.connector.cursor(dictionary=True)

    def __del__(self):
        self.cursor.close()
        self.connector.close()

    # TODO Refactor: split into methods
    def get_model(self, id_):
        sql = "SELECT * FROM model WHERE id = %s"
        self.cursor.execute(sql, (id_,))
        row = self.cursor.fetchone()

        order = row["order"]

        # get all ngrams
        sql = "SELECT id FROM ngram WHERE model_id = %s"
        self.cursor.execute(sql, (id_,))
        rows = self.cursor.fetchall()

        ngrams = []

        for row in rows:
            ngram_id = row["id"]

            # get history of current ngram
            sql = "SELECT token_index FROM ngram_history WHERE ngram_id = %s"
            self.cursor.execute(sql, (ngram_id,))
            rows = self.cursor.fetchall()
            token_indices = []
            for row in rows:
                token_indices.append(row["token_index"])
            history = tuple(token_indices)

            # get predictions of current ngram
            sql = (
                "SELECT token_index, frequency, probability, probability_threshold "
                "FROM ngram_prediction WHERE ngram_id = %s"
            )
            self.cursor.execute(sql, (ngram_id,))
            rows = self.cursor.fetchall()
            predictions = []
            for row in rows:
                token_index = row["token_index"]
                frequency = row["frequency"]
                probability = row["probability"]
                probability_threshold = row["probability_threshold"]
                predictions.append(NGramPrediction(token_index, frequency, probability, probability_threshold))

            ngrams.append(NGram(history, predictions))

        return NGramModel(order, ngrams)

    # TODO Refactor: split into methods
    def add_model(self, model):
        sql = "INSERT INTO model (`order`) VALUES (%s)"
        self.cursor.execute(sql, (model.order,))
        self.connector.commit()
        model_id = self.cursor.lastrowid

        # add all ngrams
        for ngram in model.ngrams:
            sql = "INSERT INTO ngram (model_id) VALUES (%s)"
            self.cursor.execute(sql, (model_id,))
            self.connector.commit()
            ngram_id = self.cursor.lastrowid

            # add history of current ngram
            for token_index in ngram.history:
                sql = "INSERT INTO ngram_history (ngram_id, token_index) VALUES (%s, %s)"
                self.cursor.execute(sql, (ngram_id, token_index))
                self.connector.commit()

            # add predictions of current ngram
            for prediction in ngram.predictions:
                sql = ("INSERT INTO ngram_prediction "
                       "(ngram_id, token_index, frequency, probability, probability_threshold)"
                       "VALUES (%s, %s, %s, %s, %s)")
                self.cursor.execute(sql, (ngram_id, prediction.token, prediction.frequency,
                                          prediction.probability, prediction.probability_threshold))
                self.connector.commit()

        return model_id

    def get_dictionary_from_model(self, model_id):
        sql = "SELECT * FROM token WHERE model_id = %s"
        self.cursor.execute(sql, (model_id,))
        rows = self.cursor.fetchall()

        token_indices_by_text = {}
        token_texts_by_index = {}

        for row in rows:
            index = row["index"]
            text = row["text"]
            token_indices_by_text[text] = index
            token_texts_by_index[index] = text

        dictionary = Dictionary(token_indices_by_text, token_texts_by_index)

        return dictionary

    def add_dictionary_to_model(self, dictionary, model_id):
        for index, text in dictionary.token_texts_by_index.items():
            sql = "INSERT INTO token (model_id, `index`, `text`) VALUES (%s, %s, %s)"
            self.cursor.execute(sql, (model_id, index, text))
            self.connector.commit()
