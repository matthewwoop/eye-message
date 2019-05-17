""" creates setup/teardown fixture for DbClient """

from eyemessage.DbClient import DbClient
import eyemessage.utils as utils
import pytest

@pytest.fixture(scope="module")
def db_client():
    fp = utils.db_filepath()
    db_client = DbClient(utils.db_filepath(), utils.dict_row_factory)
    yield db_client
    db_client.close_connection()
