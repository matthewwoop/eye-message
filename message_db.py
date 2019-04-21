import sqlite3
from os import getlogin

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
        return con
    except sqlite3.Error as e:
        print('Error connecting to sqlite db located at {} \n{}'.format(db_file, e))


def close(con):

    """
        Closes connection to sqlite db
    """
    return con.close()


def count_rows(con, table_name, print_out=False):

    """
        Counts number of rows in a given table

        Returns
            count -- int -- Number of rows
    """

    # NOTE: can't substite parameter for table name
    # pull this out later
    if table_name not in ['chat', 'message', 'handle', 'chat_handle_join', 'chat_message_join']:
        raise Exception('Invalid table name: {}'.format(table_name))

    count = con.execute('SELECT COUNT(*) FROM {}'.format(table_name)).fetchone()
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
