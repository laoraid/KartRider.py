import os
from datetime import datetime
import KartRider
import pytest

try:
    key = os.environ['API_KEY']
except KeyError:
    import simpletest
    key = simpletest.key

itemsolo = ('7ca6fd44026a2c8f5d939b60a'
            'a56b4b1714b9cc2355ec5e317154d4cf0675da0')


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
        with pytest.raises(ValueError):
            api.user('124125125', 'z')
    except KartRider.UnknownStatusCode:
        pytest.skip()


def test_user_match(api: KartRider.Api):
    from KartRider import metadata

    metadata.set_metadatapath(os.path.join('tests', 'metadata'))

    # parameter tests #######
    api.getUserMatches('1560546859')

    user = api.user(nickname='한글닉네임')
    api.getUserMatches(user)

    mtypes = [itemsolo, '아이템 팀전']

    pt = api.getUserMatches('1560546859', start_date='2019-12-20 00:00:00',
                            end_date=datetime(2019, 12, 20, 23),
                            match_types=mtypes)

    assert '아이템 팀전' in pt

    # #######################
    match = api.getUserMatches('1560546859', datetime(
        2019, 12, 16, 9, 0, 0), datetime(2019, 12, 16, 23, 0, 0), 2,
        14, match_types='스피드 팀전')

    assert match.nickname == '한글닉네임'
    assert '스피드 팀전' in match

    d = match['스피드 팀전'][0]
    assert d.channelname == 'speedTeamFast'
    assert d.accountno == '1560546859'
    assert d.teamid == '1'
    assert d.starttime == datetime(2019, 12, 16, 13, 18, 44)
    assert d.endtime == datetime(2019, 12, 16, 13, 20, 45)
    assert d.character == '황금망토 배찌'
    assert d.track == '도검 야외 수련관'
    assert d.playercount == 8

    p = d.player
    assert p.character == '황금망토 배찌'
    assert p.kart == '흑기사 X'
    assert p.pet == '코코 펫'
    assert p.flyingpet == '플라잉 라이트론'

    detail = d.detail
    assert detail.channelname == "speedTeamFast"
    print(detail.endtime)
    assert detail.endtime == datetime(
        2019, 12, 16, 13, 20, second=45, microsecond=268000)
    assert detail.gamespeed == 0
    assert detail.matchid == '02f10015820b59a1'
    assert detail.matchresult == '2'
    assert detail.matchtype == '스피드 팀전'
    assert detail.playtime == 109

    assert detail.starttime == datetime(
        2019, 12, 16, 13, 18, second=43, microsecond=879000)
    assert detail.track == '도검 야외 수련관'

    p = detail.teams[1][3]
    assert p.charactername == '한글닉네임'
    assert p.kart == '흑기사 X'
    assert p.matchrank == -1


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
