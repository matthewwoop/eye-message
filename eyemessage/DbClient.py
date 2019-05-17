import logging
import sqlite3


# logging config
logging.basicConfig()
log = logging.getLogger("eyemessage")
log.setLevel(logging.INFO)


class DbClient(object):
    """ Client interface for iMessages sqlite database """

    def __init__(self, fp, custom_row_factory=None, timeout=10):
        """ Creates db connection and creates db cursor """

        self.connection = self.create_connection(fp, timeout)
        if custom_row_factory:
            self.connection.row_factory = custom_row_factory

        self.cursor = self.connection.cursor()

    def __del__(self):
        """ Ensures connection closes on deletion """

        self.close_connection()

    def create_connection(self, fp, timeout):
        """ creates connection to sqlite db """

        try:
            connection = sqlite3.connect(fp, timeout=timeout)
            logging.info('Connected to db')
        except sqlite3.Error as e:
            logging.error('Error connecting to sqlite db: {}'.format(e))
            raise e

        return connection

    def query(self, query):
        """ executes query and returns executed result NOTE: read only """

        try:
            log.info('Executing query: {}'.format(query))
            self.cursor.execute(query)
        except sqlite3.Exception as e:
            logging.error('Error executing query {}:\n{}'.format(query, e))
            raise e

    def close_connection(self):
        """ Closes db connection """

        try:
            self.connection.close()
        except sqlite3.Error as e:
            logging.error('Error closing connection to sqlite db: {}'.format(e))
            raise e