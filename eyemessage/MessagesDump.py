import os
import csv
from MessagesDB import MessagesDB
from data_helpers import messages_query


class MessagesPull:

    def __init__(self):
        self.messages_db = MessagesDB()
        self.csv_filename = 'messages.csv'
        self.csv_path = os.path.join(os.getcwd(), 'data', self.csv_filename)
        return

    def check_for_update(self):
        # if count of rows in old file < current rows in db
        #   self.write_csv()
        pass

    def write_csv(self):

        # backup messages to csv
        with open(self.csv_filename, 'w') as csvfile:

            messages = self.messages_db.query(messages_query).fetchall()

            fieldnames = list(messages[0].keys())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in self.messages_db.query(messages_query):
                writer.writerow(row)

        return
