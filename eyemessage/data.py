""" Retrieves messages from Messages db for further analysis """

import logging
import csv
from DbClient import DbClient
import utils
import data

logging.basicConfig()
log = logging.getLogger("eyemessage")
log.setLevel(logging.INFO)


all_messages_query = """SELECT \
    m.ROWID AS message_id, cmj.chat_id AS chat_id, m.handle_id AS handle_id, \
    h.id AS phone_number, text, is_from_me, \
    style AS chat_style, m.service AS service," \
    "group_id, person_centric_id AS person_id, \
    datetime((date/1000000000) + strftime('%s', '2001-01-01 00:00:00'), 'unixepoch', 'localtime') AS date \
FROM message AS m \
INNER JOIN chat_message_join AS cmj ON cmj.message_id = m.ROWID \
INNER JOIN chat AS c ON cmj.chat_id = c.ROWID \
LEFT JOIN handle AS h ON m.handle_id = h.ROWID \
WHERE text IS NOT NULL \
GROUP BY message_id
"""

DEFAULT_QUERIES = {
    'all_messages': all_messages_query,
    'sample_all_messages': all_messages_query + ' LIMIT 5'
}

FIELDNAMES = ['message_id', 'chat_id', 'handle_id', 'phone_number', 'text', 'is_from_me', 'chat_style', 'service', 'group_id', 'person_id', 'date']


def csv_messages(messages, outfile, fieldnames):
    """ writes messages to csv file """

    with open(outfile, 'w+') as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()

        for msg in messages:
            writer.writerow(msg)


if __name__ == "__main__":
    from datetime import date
    outfile = "./data/Message_Backup_{}.csv".format(str(date.today()))
    query_key = "all_messages"

    log.info("Running {} query".format(query_key))
    client = DbClient(utils.db_filepath(), utils.dict_row_factory)
    messages = client.query(DEFAULT_QUERIES[query_key])

    log.info("Writing {} result to {}".format(query_key, outfile))
    csv_messages(messages, outfile, FIELDNAMES)
    log.info('Successful back up, closing connection')
    client.close_connection()
