import eyemessage.data as data
import pytest

def test_pull_messages(db_client):
    """ tests retrieval and formatting of messages from db """

    res = data.pull_messages(db_client, data.DEFAULT_QUERIES['messages'], limit=True)
    print('message', res)
    assert res[0]['service'] == 'iMessage'
