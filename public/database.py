import mysql.connector


class Database:
    def __init__(self):
        self.db = mysql.connector.connect(
            option_files="/home/jack0042/.my.cnf",
            option_groups="client"
        )
