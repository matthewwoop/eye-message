def get_messages(messages_db):

    # Selects all messages w/ accompanying chat & handle info
    messages_query = "SELECT \
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
                     GROUP BY message_id"

    messages_db.query(messages_query)
    result = messages_db.cursor.fetchall()
    print('messages result', len(result), result[0])

    return result


def get_chats(messages_db):

    # SELECTs all chats and builds a dictionary of chat_id --> chat_info
    chat_query = "SELECT ROWID AS id, account_id, \
                service_name AS service \
                FROM chat"
    messages_db.query(chat_query)
    return messages_db.cursor.fetchall()


def get_handles(messages_db):

    # Selects all handles builds a dictionary mapping handle_ids to handle info (phone number)
    handle_query = "SELECT ROWID AS id, id AS full_number, country, service, \
                    uncanonicalized_id AS local_number, person_centric_id AS person_id \
                    FROM handle"

    messages_db.query(handle_query)
    return messages_db.cursor.fetchall()
