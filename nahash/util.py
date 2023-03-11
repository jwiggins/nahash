import pathlib
import sqlite3


def get_db_conn():
    """ The current logged-in user's Messages sqlite database is found at:
    ~/Library/Messages/chat.db
    """
    path = pathlib.Path('~').expanduser() / 'Library' / 'Messages' / 'chat.db'
    return sqlite3.connect(path)
