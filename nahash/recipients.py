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

from .tables import RECIPIENTS_ID, RECIPIENTS_ROWID, RECIPIENTS_SERVICE_ID
from .util import get_db_conn


class Recipient(object):
    """ Represents a user that iMessages can be exchanged with.

    Each user has...
    - an `index` property that uniquely identifies him or her in the Messages
      database
    - a `phone_or_email` property that is either the user's phone number or
      iMessage-enabled email address
    - a `service` property that is the service type associated with the
      recipient
    """
    def __init__(self, index, phone_or_email, service):
        self.index = index
        self.phone_or_email = phone_or_email
        self.service = service

    def __repr__(self):
        return 'ID: {} Phone or email: {} ({})'.format(
            self.index, self.phone_or_email, self.service)


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
            recipients.append(Recipient(row[RECIPIENTS_ROWID],
                                        row[RECIPIENTS_ID],
                                        row[RECIPIENTS_SERVICE_ID]))

    return recipients
