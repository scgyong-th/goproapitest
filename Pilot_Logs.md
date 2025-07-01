### Logs
- python module 설치
  - `pytz` : 시간대(time zone)를 정확하게 처리하기 위한 라이브러리
  - `construct` : 바이너리 데이터 파싱/생성을 쉽게 도와주는 라이브러리
  - `pydantic` : 데이터 유효성 검사 및 파싱을 위한 라이브러리
  - `tzlocal` : 현재 시스템(local) 시간대 정보를 자동으로 감지해서 Python 코드에서 쓸 수 있게 해주는 라이브러리. `pytz`, `datetime`, `dateutil` 같은 시간대 관련 도구와 함께 자주 사용됨.
  - `rich` : 터미널에 컬러풀하고 깔끔한 출력을 쉽게 할 수 있게 해주는 라이브러리
  - `requests` : HTTP 요청(GET, POST 등)을 매우 간단하게 보낼 수 있게 해주는 라이브러리
  - `returns` : 함수형 프로그래밍(functional programming) 스타일을 쓸 수 있게 도와주는 라이브러리
  - `bleak` : Bluetooth Low Energy (BLE) 기기와 통신할 수 있게 해주는 비동기 기반 BLE 클라이언트 라이브러리입니다.
  - `pexpect` : 터미널 프로그램을 자동으로 제어할 수 있게 해주는 라이브러리입니다
  - `packaging` : 프로젝트의 버전 지정, 종속성, 설치 요구사항 등을 다룰 때 사용되는 핵심 라이브러리. 특히 패키지 배포, 버전 비교, 의존성 검사 등에 널리 쓰임.
  - `protobuf` : Google에서 제공하는 Protocol Buffers (직렬화 포맷) Python 구현체
  - `wrapt` : 데코레이터와 함수 래핑(wrapper)을 안전하고 유연하게 구현할 수 있게 도와주는 라이브러리
  - `asyncstdlib` : Python의 비동기(async) 환경에서 사용하기 좋은 표준 라이브러리 함수들(itertools, functools, operator 등)의 비동기 버전을 모아둔 라이브러리
  - `tinydb` : Python용 경량 NoSQL 데이터베이스. 파일 기반(기본적으로 JSON)이며 별도의 서버 설치 없이도 쉽게 데이터를 저장하고 조회할 수 있음
  - `zeroconf` : 로컬 네트워크 상에서 서비스 자동 발견(서비스 디스커버리)을 구현하는 Python 라이브러리
- Requirements.txt
  - `requirements.txt` 파일로 저장한 뒤 `pip install -r requirements.txt` 로 한번에 설치 가능

    ```
    pytz
    construct
    pydantic
    tzlocal
    rich
    requests
    returns
    bleak
    pexpect
    packaging
    protobuf
    wrapt
    asyncstdlib
    tinydb
    zeroconf
    ```










