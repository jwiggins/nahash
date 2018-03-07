# The MIT License (MIT)

# Copyright (c) 2016 Matt Rajca

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import datetime

from .util import get_db_conn

OSX_EPOCH = 978307200


class Recipient(object):
    """ Represents a user that iMessages can be exchanged with.

    Each user has...
    - an `id` property that uniquely identifies him or her in the Messages
      database
    - a `phone_or_email` property that is either the user's phone number or
      iMessage-enabled email address
    """
    def __init__(self, _id, phone_or_email):
        self.id = _id
        self.phone_or_email = phone_or_email

    def __repr__(self):
        return ('ID: ' + str(self.id) +
                ' Phone or email: ' + self.phone_or_email)


class Message(object):
    """ Represents an iMessage message.

    Each message has:
    - a `text` property that holds the text contents of the message
    - a `date` property that holds the delivery date of the message
    """
    def __init__(self, text, date):
        self.text = text
        self.date = date

    def __repr__(self):
        return 'Text: ' + str(self.text) + ' Date: ' + str(self.date)


def get_all_recipients():
    """ Fetches all known recipients.

    The `id`s of the recipients fetched can be used to fetch all messages
    exchanged with a given recipient.
    """
    connection = get_db_conn()

    with connection:
        c = connection.cursor()

        # The `handle` table stores all known recipients.
        c.execute('SELECT * FROM `handle`')
        recipients = []
        for row in c:
            recipients.append(Recipient(row[0], row[1]))

    return recipients


def get_messages_for_recipient(recipient):
    """ Fetches all messages exchanged with a given recipient. """
    connection = get_db_conn()

    with connection:
        c = connection.cursor()

        # The `message` table stores all exchanged iMessages.
        c.execute('SELECT * FROM `message` WHERE handle_id=' + str(recipient))
        messages = []
        for row in c:
            text = row[2]
            if text is None:
                continue
            date = datetime.datetime.fromtimestamp(row[15] + OSX_EPOCH)

            # Strip any special non-ASCII characters (e.g., the special
            # character that is used as a placeholder for attachments such as
            # files or images).
            encoded_text = text.encode('ascii', 'ignore')
            messages.append(Message(encoded_text, date))

    return messages
