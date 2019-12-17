import os
import datetime
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


def test_api_user(api: KartRider.Api):
    with pytest.raises(ValueError):
        api.user(None, None)
    try:
        assert '1560546859' == api.user(nickname='한글닉네임').accessid
        assert '한글닉네임' == api.user(accessid='1560546859').name
        api.user(accessid='1560546859', nickname='한글닉네임')
    except KartRider.UnknownStatusCode:
        pytest.skip()


def test_user_match(api: KartRider.Api):
    from KartRider import metadata

    metadata.set_metadatapath(os.path.join('tests', 'metadata'))

    api.getUserMatches('1560546859')

    match = api.getUserMatches('1560546859', datetime.datetime(
        2019, 12, 16, 9, 0, 0), datetime.datetime(2019, 12, 16, 23, 0, 0), 2,
        14, match_types='스피드 팀전')

    assert match.nickname == '한글닉네임'

    t = match.matches[0]
    assert t.matchType == '스피드 팀전'

    d = t.matchesinfo[0]
    assert d.channelName == 'speedTeamFast'
    assert d.character == '황금망토 배찌'
    assert d.track == '도검 야외 수련관'
    assert d.playerCount == 8

    p = d.player
    assert p.character == '황금망토 배찌'
    assert p.kart == '흑기사 X'
    assert p.pet == '코코 펫'
    assert p.flyingPet == '플라잉 라이트론'

    detail = d.detail

    assert detail.matchId == '02f10015820b59a1'
    assert detail.channelName == 'speedTeamFast'
    assert detail.matchType == '스피드 팀전'
