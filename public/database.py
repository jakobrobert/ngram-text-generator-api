import mysql.connector

from core.dictionary import Dictionary


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

    # TODO add model id
    def get_dictionary(self):
        sql = "SELECT * FROM dictionary"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()

        dictionary = Dictionary()
        for row in rows:
            token = row["token"]
            dictionary.add_token(token)

        return dictionary

    # TODO add model id
    def add_dictionary(self, dictionary):
        for token in dictionary.tokens:
            sql = "INSERT INTO dictionary (token) VALUES (%s)"
            self.cursor.execute(sql, (token,))  # trailing comma very important so it is a tuple, else sql syntax error
            self.connector.commit()
