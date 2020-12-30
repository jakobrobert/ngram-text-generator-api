import mysql.connector

from core.dictionary import Dictionary
from core.ngram.ngram_model import NGramModel


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

    def get_model(self, id_):
        sql = "SELECT * FROM model WHERE id = %s"
        self.cursor.execute(sql, (id_,))
        row = self.cursor.fetchone()

        order = row["order"]
        # TODO include ngrams (separate table, find by model id)

        return NGramModel(order)

    def add_model(self, model):
        sql = "INSERT INTO model (`order`) VALUES (%s)"
        self.cursor.execute(sql, (model.order,))
        self.connector.commit()
        model_id = self.cursor.lastrowid

        for ngram in model.ngrams:
            sql = "INSERT INTO ngram (model_id) VALUES (%s)"
            self.cursor.execute(sql, (model_id,))
            self.connector.commit()
            ngram_id = self.cursor.lastrowid

            for token_index in ngram.history:
                sql = "INSERT INTO ngram_history (ngram_id, token_index) VALUES (%s, %s)"
                self.cursor.execute(sql, (ngram_id, token_index))
                self.connector.commit()

            for prediction in ngram.predictions:
                sql = ("INSERT INTO ngram_prediction "
                       "(ngram_id, token_index, frequency, probability, probability_threshold)"
                       "VALUES (%s, %s, %s, %s, %s)")
                self.cursor.execute(sql, (ngram_id, prediction.token_index, prediction.frequency,
                                          prediction.probability, prediction.probability_threshold))
                self.connector.commit()

        return model_id

    def get_dictionary_from_model(self, model_id):
        sql = "SELECT * FROM token WHERE model_id = %s"
        self.cursor.execute(sql, (model_id,))
        rows = self.cursor.fetchall()

        # retrieve existing token indices from database rather than creating new indices
        # this is important to keep the relation between tokens and ngrams
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
