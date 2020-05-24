import os
import pytest
from KartRider import metadata
from KartRider.user import User
from KartRider import utils


metadata.set_metadatapath(os.path.join('tests', 'metadata'))


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


def test_isid():
    c = metadata.getCharactersDict()
    f = metadata.getflyingPetsDict()
    t = metadata.getTracksDict()

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


def test_mergedict():
    from KartRider.basedata import MergeAbleDict

    tc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']

    mdict = MergeAbleDict(abc=['a', 'b', 'c'], wegh=['d', 'e'],
                          wegweg=['f', 'g', 'h', 'i'])

    assert tc == list(mdict.mergeValues())
