import sqlite3
from os import getlogin


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


dictify = dictify = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


def connect():

    """
        Connects to sqlite db storing Messages

        Returns
            con -- sqlite Connection
            NOTE: conn method implicitly creates cursor objects for conn.execute
    """

    current_user = getlogin()
    db_file = "/Users/{}/Library/Messages/chat.db".format(current_user)

    try:
        con = sqlite3.connect(db_file, timeout=10)
        con.row_factory = dict_factory
        cur = con.cursor()
        return con, cur
    except sqlite3.Error as e:
        print('Error connecting to sqlite db located at {} \n{}'.format(db_file, e))


def close(con):

    """
        Closes connection to sqlite db
    """
    return con.close()


def count_rows(cur, table_name, print_out=False):

    """
        Counts number of rows in a given table

        Returns
            count -- int -- Number of rows
    """

    # NOTE: can't substite parameter for table name
    # pull this out later
    if table_name not in ['chat', 'message', 'handle', 'chat_handle_join', 'chat_message_join']:
        raise Exception('Invalid table name: {}'.format(table_name))

    count = cur.execute('SELECT COUNT(*) AS {}_count FROM {}'.format(table_name, table_name)).fetchone()
    if print_out:
        print('\nTotal rows in {} table: {}', table_name, count)

    return count


def get_schema(con, table_name, print_out=False):

    """
        Retrieves schema of a given table
    """

    table_schema = con.execute('.schema ?', table_name).fetchone()
    if print_out:
        print('\n{} Schema:\n{}', table_name, table_schema)

    return table_schema


def get_messages(cur, limit=None):

    """
        Retrieves text messages
    """

    msg_query = 'SELECT \
                    cmj.chat_id AS chat_id, cmj.message_id, chj.handle_id AS handle_id, \
                    message_date AS date,m.text AS text, m.is_from_me \
                FROM chat_message_join AS cmj \
                    INNER JOIN message AS m \
                        ON cmj.message_id = m.ROWID \
                    INNER JOIN chat_handle_join AS chj \
                         ON cmj.chat_id = chj.chat_id \
                    ORDER BY chj.handle_id DESC'

    if limit:
        msg_query += ' LIMIT ?'
        cur.execute(msg_query, (limit, ))
    else:
        cur.execute(msg_query)

    column_vals = [description[0] for description in cur.description]
    print(column_vals, '\n')
    for row in cur.fetchall():
        print(row)

    return