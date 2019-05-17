import eyemessage.utils as utils
from eyemessage.DbClient import DbClient

def test_DbClient():
    """ tests connection & querying NOTE need to add setup & takedown """

    fp = utils.db_filepath()
    client = DbClient(fp, utils.dict_row_factory)

    res = client.query('SELECT * FROM handle LIMIT 1')
    client.close_connection()

    assert res[0]['service'] == 'iMessage'
