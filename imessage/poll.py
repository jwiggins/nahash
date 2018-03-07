import time

from .tables import MESSAGE_ROWID
from .util import get_db_conn

WAIT_TIMEOUT = 5.0


def get_next_message(recipients):
    """ Poll forever until a message arrives from any of `recipients`.
    """
    if not isinstance(recipients, (list, tuple)):
        recipients = (recipients,)

    condition = 'is_from_me=0 AND handle_id IN ( {} )'
    condition = condition.format(', '.join(str(r) for r in recipients))
    sql = ('SELECT * FROM `message` '
           'WHERE ' + condition +
           'ORDER BY ROWID DESC '
           'LIMIT 1')

    connection = get_db_conn()
    with connection:
        c = connection.cursor()
        last_rowid = 0

        while True:
            time.sleep(WAIT_TIMEOUT)

            c.execute(sql)
            row = c.fetchone()

            # Nothing there yet
            if row is None:
                continue

            if last_rowid == 0:
                last_rowid = row[MESSAGE_ROWID]
            elif row[MESSAGE_ROWID] > last_rowid:
                return row
