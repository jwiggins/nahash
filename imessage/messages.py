import subprocess
import textwrap
import time

from .tables import MESSAGE_ROWID, MESSAGE_TEXT
from .util import get_db_conn

WAIT_TIMEOUT = 5.0


def send_message(recipient, text):
    """ Send a single message to a recipient
    """
    script = textwrap.dedent("""
    on run {targetBuddyPhone, targetMessage}
        tell application "Messages"
            set targetService to 1st service whose service type = iMessage
            set targetBuddy to buddy targetBuddyPhone of targetService
            send targetMessage to targetBuddy
        end tell
    end run
    """)
    command = ['osascript', '-', recipient, text]
    proc = subprocess.Popen(command, stdin=subprocess.PIPE)
    proc.communicate(script.encode('utf8'))
    return proc.wait()


def wait_for_next_message(recipients):
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
                return row[MESSAGE_TEXT]
