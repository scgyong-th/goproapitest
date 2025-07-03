# Pilot Log 7/1

## Logs
- `main.py` 만들어 실행해본다

    ``` python
    import open_gopro as gopro
    print("Done")
    ```
  - 설치되지 않는 module 때문에 많은 에러가 나온다
    
### GoPro Python API Import
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

### Android Gateway Pilot

- Kotlin Compose Activity 로 Pilot 시작
- Service 생성
  - pilot 이므로 bind 는 하지 않음.
- Activity 실행시 Service 가 실행되도록 구현
- NanoHttpd import
  - ```kotlindsl
    dependencies {
    implementation(libs.nanohttpd)
    ```

  - ```toml
    [libraries]
    nanohttpd = { module = "org.nanohttpd:nanohttpd", version = "2.3.1" }

    ```
- `NanoHTTPD` 상속하여 `SimpleHttpServer` 생성 후 특정 port (5050) listen.
- Emulator 실행 후 `adb forward tcp:5050 tcp:5050` 실행
  - Emulator 나 실기기나 동일하게 동작한다고 되어 있으나 아직 실기기에서는 테스트해보지 못함
  - Emulator 가 종료되기 전까지는 유효. 실기기라면 USB 연결이 끊길때까지 유효
  - 실행한 후에만 접속이 제대로 되며, `adb forward --remove tcp:5050` 를 한 후에는 연결되지 않는것도 확인
- Mac Terminal 에서 `curl` 로 결과 받기 성공
  - ```bash
    (myenv) scgyong@MBP16:[~]$ curl http://localhost:6502/hello
    Hello from NanoHTTPD!
    (myenv) scgyong@MBP16:[~]$ curl http://localhost:6502/hellox
    404 Not Found
    (myenv) scgyong@MBP16:[~]$ 
    ```
- 이후 테스트
  - 호출할 API Server 의 baseurl 을 전달하고 http 연결에 필요한 path, method, args 등을 전달하여 결과 받아오기
  - Request 를 그대로 forward 할 수 있는지 확인
    - 된다면, 일부 테스트는 `노트북 -> 카메라` 로 연결된 상태로도 진행 가능
  - GoPro 기기에 연결해서 받아오기
  - `Service` <-> `Activity` 데이터 흐름 보여주기







