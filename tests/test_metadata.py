import os
import pytest
from KartRider import metadata


metadata.set_metadatapath(os.path.join('tests', 'metadata'))


def test_get():
    id = '1f438b9f6939d01b396acb96648c72a57f781b0dc8871bb84b3e2ff8da7ec0f2'
    name = '폭스 9 XE'

    assert name == metadata._getname('kart', id)
    assert id == metadata._getid('kart', name)


def test_exception():
    with pytest.raises(FileNotFoundError):
        metadata.set_metadatapath('asdafegewgweg')

    with pytest.raises(FileNotFoundError):
        metadata._getid('asdsadaw', 'gegeg')

    with pytest.raises(KeyError):
        metadata._getid('kart', 'asdwef')
