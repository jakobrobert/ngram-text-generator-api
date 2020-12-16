import mysql.connector


class Database:
    def __init__(self):
        self.connector = mysql.connector.connect(
            option_files="/home/jack0042/.my.cnf",
            option_groups="client",
            database="jack0042_ngram_text_generator"
        )
        self.cursor = self.connector.cursor()

    def get_dictionary(self):
        sql = "SELECT * FROM dictionary"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()

        for row in rows:
            print(row)
