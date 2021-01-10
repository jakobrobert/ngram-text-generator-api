import mysql.connector
import time

from core.dictionary import Dictionary
from core.ngram.ngram_model import NGramModel
from core.ngram.ngram_prediction import NGramPrediction
from core.ngram.ngram import NGram


class Database:
    def __init__(self):
        self.connector = mysql.connector.connect(option_files="./mysql.cnf", option_groups="client")
        self.cursor = self.connector.cursor(dictionary=True)

    def __del__(self):
        self.cursor.close()
        self.connector.close()

    def delete_tables(self):
        sql = """
            DROP TABLE IF EXISTS `ngram_prediction`;
            DROP TABLE IF EXISTS `ngram_history`;
            DROP TABLE IF EXISTS `ngram`;
            DROP TABLE IF EXISTS `token`;
            DROP TABLE IF EXISTS `model`;
        """
        self.cursor.execute(sql, multi=True)
        self.connector.commit()

    def create_tables(self):
        self.create_model_table()
        self.create_token_table()
        self.create_ngram_table()
        self.create_ngram_history_table()
        self.create_ngram_prediction_table()

    def create_model_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS `model` (
                `id` int(11) NOT NULL AUTO_INCREMENT,
                `order` tinyint(3) NOT NULL,
                PRIMARY KEY (`id`)
            )
            """
        self.cursor.execute(sql)
        self.connector.commit()

    def create_token_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS `token` (
                `id` int(11) NOT NULL AUTO_INCREMENT,
                `model_id` int(11) NOT NULL,
                `index` int(11) NOT NULL,
                `text` varchar(255) NOT NULL,
                PRIMARY KEY (`id`),
                FOREIGN KEY (`model_id`) REFERENCES `model` (`id`)
            )
            """
        self.cursor.execute(sql)
        self.connector.commit()

    def create_ngram_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS `ngram` (
                `id` int(11) NOT NULL AUTO_INCREMENT,
                `model_id` int(11) NOT NULL,
                PRIMARY KEY (`id`),
                FOREIGN KEY (`model_id`) REFERENCES `model` (`id`)
            )
            """
        self.cursor.execute(sql)
        self.connector.commit()

    def create_ngram_history_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS `ngram_history` (
                `id` int(11) NOT NULL AUTO_INCREMENT,
                `ngram_id` int(11) NOT NULL,
                `token_index` int(11) NOT NULL,
                PRIMARY KEY (`id`),
                FOREIGN KEY (`ngram_id`) REFERENCES `ngram` (`id`)
            )
            """
        self.cursor.execute(sql)
        self.connector.commit()

    def create_ngram_prediction_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS `ngram_prediction` (
                `id` int(11) NOT NULL AUTO_INCREMENT,
                `ngram_id` int(11) NOT NULL,
                `token_index` int(11) NOT NULL,
                `frequency` int(11) NOT NULL,
                `probability` double NOT NULL,
                `probability_threshold` double NOT NULL,
                PRIMARY KEY (`id`),
                FOREIGN KEY (`ngram_id`) REFERENCES `ngram` (`id`)
            )
            """
        self.cursor.execute(sql)
        self.connector.commit()

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
        start_time = time.perf_counter()

        sql = "INSERT INTO model (`order`) VALUES (%s)"
        self.cursor.execute(sql, (model.order,))
        self.connector.commit()
        model_id = self.cursor.lastrowid

        # add all ngrams using only one query
        sql = "INSERT INTO ngram (model_id) VALUES (%s)"
        values = []
        for _ in model.ngrams:
            values.append((model_id,))
        self.cursor.executemany(sql, values)
        self.connector.commit()

        # for executemany, lastrowid returns the id of the first row
        # can get the other ids just by incrementing
        ngram_start_id = self.cursor.lastrowid

        # add history for all ngrams using only one query
        sql = "INSERT INTO ngram_history (ngram_id, token_index) VALUES (%s, %s)"
        values = []
        ngram_id = ngram_start_id
        for ngram in model.ngrams:
            for token_index in ngram.history:
                values.append((ngram_id, token_index))
            ngram_id += 1
        self.cursor.executemany(sql, values)
        self.connector.commit()

        # add predictions for all ngrams using only one query
        sql = ("INSERT INTO ngram_prediction "
               "(ngram_id, token_index, frequency, probability, probability_threshold)"
               "VALUES (%s, %s, %s, %s, %s)")
        values = []
        ngram_id = ngram_start_id
        for ngram in model.ngrams:
            for prediction in ngram.predictions:
                values.append((ngram_id, prediction.token, prediction.frequency,
                               prediction.probability, prediction.probability_threshold))
            ngram_id += 1
        self.cursor.executemany(sql, values)
        self.connector.commit()

        elapsed_time = int((time.perf_counter() - start_time) * 1000.0)
        print("add_model (ms): " + str(elapsed_time))

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
        start_time = time.perf_counter()
        # add all tokens using only one query
        sql = "INSERT INTO token (model_id, `index`, `text`) VALUES (%s, %s, %s)"
        values = []
        for index, text in dictionary.token_texts_by_index.items():
            values.append((model_id, index, text))
        self.cursor.executemany(sql, values)
        self.connector.commit()

        elapsed_time = int((time.perf_counter() - start_time) * 1000.0)
        print("add_dictionary_to_model (ms): " + str(elapsed_time))
