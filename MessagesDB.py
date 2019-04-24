import sqlite3
from os import getlogin


class MessagesDB(object):

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)

            try:
                current_user = getlogin()
                db_file = "/Users/{}/Library/Messages/chat.db".format(current_user)

                print('Connecting to Messages database file', db_file)
                connection = MessagesDB._instance.connection = sqlite3.connect(db_file, timeout=10)
                connection.row_factory = cls.dict_factory
                MessagesDB._instance.cursor = connection.cursor()

                print('Successfully connected -- booyah')
            except Exception as e:
                print('Error: Connection Failed {}'.format(e))

        return cls._instance


    def __init__(self):
        self.connection = self._instance.connection
        self.cursor = self._instance.cursor


    def __del__(self):
        self.connection.close()


    def query(self, query):
        try:
            result = self.cursor.execute(query)
        except Exception as e:
            print('Error: Query Failed\n{}\n{}'.format(query, e))
            return None
        else:
            return result


    def dict_factory(cursor, row):
        """
            helper fxn that creates column name -> row value dict
        """
        return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}