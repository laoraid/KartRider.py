import os
import KartRider
import pytest

try:
    key = os.environ['API_KEY']
except KeyError:
    import simpletest
    key = simpletest.key


@pytest.fixture()
def api():
    return KartRider.Api(key)


def test_api_user(api):
    try:
        api.user(None, None)
    except ValueError:
        try:
            assert '1560546859' == api.user(nickname='한글닉네임').accessid
            assert '한글닉네임' == api.user(accessid='1560546859').name
        except KartRider.UnknownStatusCode:
            pytest.skip()
