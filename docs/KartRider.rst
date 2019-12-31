=============================
KartRider.py
=============================

---------------------
시작하기 전에
---------------------

이 라이브러리는 카트라이더의 OpenAPI를 파이썬으로 래핑한 라이브러리입니다.
사용하기 위해선 OpenAPI 의 API Key가 필요합니다.
`OpenAPI docs <https://developers.nexon.com/kart/apiList>`__ 도 참고해 보세요.

라이브러리의 모든 날짜는 UTC 기준입니다.

| 파라미터로 입력되는 날짜(startTime, endTime 등)의 포맷은 '%Y-%m-%d %H:%M:%S' 입니다.
| 예시 : 2020-01-01 13:03:33

설치하기
====================

::

   > pip install KartRider
   > python -m KartRider -d DOWNLOAD_DIR

경로를 지정해서 메타데이터를 다운로드 받으세요.

::

   import KartRider
   KartRider.set_metadatapath(DOWNLOAD_DIR)

위와 같이 메타데이터의 경로를 설정합니다.

::

   api = KartRider.Api(API_KEY)

API KEY는 공개적으로 저장하지 마세요.

----------------------------
레퍼런스
----------------------------


Api 클래스
===========================

.. automodule:: KartRider.apiwrapper
   :members:
   :undoc-members:
   :show-inheritance:

매치 데이터
==========================

.. automodule:: KartRider.match
   :members:
   :undoc-members:
   :show-inheritance:

유저 데이터
==========================

.. automodule:: KartRider.user
   :members:
   :undoc-members:
   :show-inheritance:

메타 데이터
===========================

.. automodule:: KartRider.metadata
   :members:
   :undoc-members:
   :show-inheritance:
