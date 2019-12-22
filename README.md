# KartRider.py
[![Build Status](https://travis-ci.com/laoraid/KartRider.py.svg?branch=master)](https://travis-ci.com/laoraid/KartRider.py) [![codecov](https://codecov.io/gh/laoraid/KartRider.py/branch/master/graph/badge.svg)](https://codecov.io/gh/laoraid/KartRider.py) [![PyPI version](https://badge.fury.io/py/KartRider.svg)](https://badge.fury.io/py/KartRider)

[카트라이더 OpenAPI](https://developers.nexon.com/kart)를 Python으로 래핑한 라이브러리입니다.

## 설치
```console
> pip install KartRider
> python -m KartRider -d DOWNLOAD_DIR
```
로 메타데이터를 다운로드 합니다.

```python
import KartRider
KartRider.set_metadatapath(메타데이터 경로)
```
메타데이터 경로를 위와 같이 설정합니다.

## 사용법


## 사용권
[MIT 라이센스](LICENSE)를 따르고, NEXON DEVELOPERS 의 api를 사용했습니다.