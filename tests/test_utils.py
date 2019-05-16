from eyemessage import utils

def test_func():
    result = utils.version()
    assert result == "1.0"
