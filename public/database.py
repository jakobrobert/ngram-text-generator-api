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
        sql = "SELECT * FROM token WHERE model_id = %s"
        self.cursor.execute(sql, (model_id,))
        rows = self.cursor.fetchall()

        # retrieve token ids from database rather than creating own id
        # this is important to keep the relation between tokens and ngrams
        token_texts_by_id = {}
        token_ids_by_text = {}

        for row in rows:
            id_ = row["id"]
            text = row["text"]
            token_texts_by_id[id_] = text
            token_ids_by_text[text] = id_

        dictionary = Dictionary(token_texts_by_id, token_ids_by_text)

        return dictionary

    def add_dictionary_to_model(self, dictionary, model_id):
        # TODO might optimize by batching sql commands
        for id_, text in dictionary.token_texts_by_id.items():
            # do not use the token ids of dictionary object
            # instead, let database generate the ids
            sql = "INSERT INTO token (text, model_id) VALUES (%s, %s)"
            self.cursor.execute(sql, (text, model_id))
            self.connector.commit()
