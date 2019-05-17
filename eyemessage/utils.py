import sys
import logging
from pathlib import Path
from os import getlogin
from typing import Optional


# logging config
logging.basicConfig()
log = logging.getLogger("eyemessage")
log.setLevel(logging.INFO)


def db_filepath(username: Optional[str] = getlogin()):
    """ Constructs filepath to Messages db """

    fp = '/Users/{}/Library/Messages/chat.db'.format(username)

    if Path(fp).exists():
        logging.info('Messages db filepath: {}'.format(fp))
        return fp
    else:
        logging.error('Messages db file does not exit at path: {}'.format(fp))
        sys.exit()


def dict_row_factory(cursor, row):
    """ creates dict mapping column name -> row value """

    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
