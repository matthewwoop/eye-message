""" Retrieves messages from Messages db for further analysis """

import logging


logging.basicConfig()
log = logging.getLogger("eyemessage")
log.setLevel(logging.INFO)



def pull_messages(db_client, limit=False):
    """ retrieves messages and formats """

    messages_query = """
    SELECT \
        m.ROWID AS message_id, cmj.chat_id AS chat_id, m.handle_id AS handle_id, \
        h.id AS phone_number, text, is_from_me, \
        style AS chat_style, m.service AS service," \
        "group_id, person_centric_id AS persion_id, \
        datetime((date/1000000000) + strftime('%s', '2001-01-01 00:00:00'), 'unixepoch', 'localtime') AS date \
    FROM message AS m \
    INNER JOIN chat_message_join AS cmj ON cmj.message_id = m.ROWID \
    INNER JOIN chat AS c ON cmj.chat_id = c.ROWID \
    LEFT JOIN handle AS h ON m.handle_id = h.ROWID \
    WHERE text IS NOT NULL \
    GROUP BY message_id
    """

    if limit:
        messages_query += ' LIMIT 5'

    messages = db_client.query(messages_query)
    log.info('{} msgs pulled'.format(len(messages)))
    log.info('Sample message: {}'.format(messages[0]))

    return messages
