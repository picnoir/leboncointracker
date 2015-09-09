import sqlite3
from datetime import datetime

class Appartment:
    """This class contains the data describing an Appartment"""
    def __init__(self, url, price, surface, zip_code,
                 nb_rooms=None, type=None, post_date=datetime.now()):
        self.url = url
        self.price = price
        self.surface = surface
        self.zip_code = zip_code
        self.nb_rooms = nb_rooms
        self.type = type
        self.post_date = post_date

    def save(self, cursor):
        request_params = (self.price, self.surface, self.zip_code,
                          self.nb_rooms, self.type, self.url, self.post_date)
        cursor.execute('''INSERT INTO appartments (price, surface,
                          zip_code, nb_rooms, type, url, post_date)
                          VALUES (?,?,?,?,?,?,?)''',
                       request_params)

    @staticmethod
    def createDB(dbName):
        """This function initializes the database with the correct scheme"""
        connection = sqlite3.connect(dbName)
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE appartments
                            (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            price INT NOT NULL, surface INT NOT NULL,
                            zip_code INT NOT NULL, url VARCHAR(200) NOT NULL,
                            nb_rooms VARCHAR(10), type VARCHAR(30),
                            post_date DATETIME)''')
        cursor.execute('''CREATE UNIQUE INDEX appartmentsUrl
                       on appartments(url)''')
        connection.commit()
        connection.close()

    @staticmethod
    def appartment_already_in_db(cursor, url):
        parameters = (url, )
        return_value = False
        cursor.execute('''SELECT count(id)
                          FROM appartments
                          WHERE url = ?''', parameters)
        if cursor.fetchone()[0] > 0:
            return_value = True
        return return_value
