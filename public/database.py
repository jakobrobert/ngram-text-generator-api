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

        # TODO add ngrams (separate table, link to model by id)

        return model_id

    def get_dictionary_from_model(self, model_id):
        sql = "SELECT * FROM dictionary WHERE model_id = %s"
        self.cursor.execute(sql, (model_id,))
        rows = self.cursor.fetchall()

        dictionary = Dictionary()
        for row in rows:
            token = row["token"]
            dictionary.add_token(token)

        return dictionary

    def add_dictionary_to_model(self, dictionary, model_id):
        for token in dictionary.tokens:
            sql = "INSERT INTO dictionary (token, model_id) VALUES (%s, %s)"
            self.cursor.execute(sql, (token, model_id))
            self.connector.commit()
