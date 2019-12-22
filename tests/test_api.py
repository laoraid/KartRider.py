import os
from datetime import datetime
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

    match = api.getUserMatches('1560546859', datetime(
        2019, 12, 16, 9, 0, 0), datetime(2019, 12, 16, 23, 0, 0), 2,
        14, match_types='스피드 팀전')

    assert match.nickname == '한글닉네임'
    assert '스피드 팀전' in match

    d = match['스피드 팀전'][0]
    assert d.channelName == 'speedTeamFast'
    assert d.accountNo == '1560546859'
    assert d.teamId == '1'
    assert d.startTime == datetime(2019, 12, 16, 13, 18, 44)
    assert d.endTime == datetime(2019, 12, 16, 13, 20, 45)
    assert d.character == '황금망토 배찌'
    assert d.track == '도검 야외 수련관'
    assert d.playerCount == 8

    p = d.player
    assert p.character == '황금망토 배찌'
    assert p.kart == '흑기사 X'
    assert p.pet == '코코 펫'
    assert p.flyingPet == '플라잉 라이트론'

    detail = d.detail
    assert detail.channelName == "speedTeamFast"
    print(detail.endTime)
    assert detail.endTime == datetime(
        2019, 12, 16, 13, 20, second=45, microsecond=268000)
    assert detail.gameSpeed == 0
    assert detail.matchId == '02f10015820b59a1'
    assert detail.matchResult == '2'
    assert detail.matchType == '스피드 팀전'
    assert detail.playTime == 109

    assert detail.startTime == datetime(
        2019, 12, 16, 13, 18, second=43, microsecond=879000)
    assert detail.track == '도검 야외 수련관'

    p = detail.teams[1][3]
    assert p.characterName == '한글닉네임'
    assert p.kart == '흑기사 X'
    assert p.matchRank == -1


def test_getAllMatches(api: KartRider.Api):
    a = api.getAllMatches()

    for _, v in a.items():
        assert type(v[0]) == KartRider.match.MatchDetail


def test_matchtypes(api: KartRider.Api):
    types = ['스피드 팀전', '스피드 개인전']
    a = api.getUserMatches('1560546859',
                           datetime(2019, 12, 1), datetime(2019, 12, 15),
                           0, 30, types)

    for type in types:
        assert type in a
