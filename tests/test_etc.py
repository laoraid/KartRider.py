import os
import pytest
from KartRider import metadata
from KartRider.user import User
from KartRider import utils


metadata.set_metadatapath(os.path.join('tests', 'metadata'))


def test_get():
    id = '1f438b9f6939d01b396acb96648c72a57f781b0dc8871bb84b3e2ff8da7ec0f2'
    name = '폭스 9 XE'

    assert name == metadata._getname('kart', id)
    assert id == metadata._getid('kart', name)


def test_getimage():
    id = '1f438b9f6939d01b396acb96648c72a57f781b0dc8871bb84b3e2ff8da7ec0f2'
    name = '폭스 9 XE'

    path = os.path.join(metadata._path, 'kart', id + '.png')

    assert path == metadata.getImagePath(id, 'kart')
    assert path == metadata.getImagePath(name, 'kart')


def test_exception():
    with pytest.raises(FileNotFoundError):
        metadata.set_metadatapath('asdafegewgweg')

    with pytest.raises(FileNotFoundError):
        metadata._getid('asdsadaw', 'gegeg')


def test_user():
    with pytest.raises(ValueError):
        User()

    with pytest.raises(ValueError):
        u = User(name='asd')
        print(u.accessid)
        u = User(accessid='asf')
        print(u.name)
        u.getMatches()


def test_gets():
    nme = 'ee483cbf01cdc544e22b5837c59f80624477ddda9480789bec759c2faedb810a'
    itlo = '7ca6fd44026a2c8f5d939b60aa56b4b1714b9cc2355ec5e317154d4cf0675da0'

    assert nme in metadata.getCharacters()
    assert itlo in metadata.getgameTypes()


def test_isid():
    c = metadata.getCharacters()
    f = metadata.getflyingPets()
    t = metadata.getTracks()

    keys = []
    keys.extend(c.keys())
    keys.extend(f.keys())
    keys.extend(t.keys())

    values = []
    values.extend(c.values())
    values.extend(f.values())
    values.extend(t.values())

    for k, v in zip(keys, values):
        assert utils._isId(k)
        assert not utils._isId(v)
