# Works ~ 07/22

## ~07/19

### BLE
- `KeepAlive` 메시지를 Wi-Fi 로 보내던 것을 BLE 로 보내는 것으로 수정.

### Runner (`pytest`)
- `BleRequest` 기본 클래스 생성
  - Android 에서 구현했던 클래스들 구현
    - `GetHardwareInfo`
    - `GetWifiApSsid`
    - `GetWifiApPassword`
    - `SetApControl`
  - 간단한 Unit Test 구현
  - Request 별로 Forward URL 생성
    - `http://localhost:6502/fw/0072/013C`
      - `0072` : Comman Request Characteristic
      - `01` : 1 byte
      - `3C` : `GetHardwareInfo` 요청
- 상수 정의
  - 2-byte Characteristic
  - `QueryId`, `CommandId`, `SettingId`, `StatusId`
- `conftest`
  - session scope fixture 로 test_config.json 파일 읽어들임
  - server base_url (`http://localhost:6502`)
- 실행 방법 정리
  - [Test 실행 방법](testrunner/)

### Android
- BleRequest Refactoring
  - 기존 `Read`/`Write` 로만 되어 있던 것에서 `Forward` 가 둘 중 어느 것도 될 수 있는 구조로 재편
- `ForwardRequest` 구현
  - `pytest` test case 로부터 넘어온 요청을 BLE Request 로 변형하도록
  - Notify Message 를 parse 하지 않고 Array of Array of Byte 로 쌓아서 그대로 `pytest` test case 에게 전달
- `SimpleHttpServer`
  - `/fw` 로 시작할 경우 `MainModel` 에게 전달, 응답을 json 형태로 send.
  - 2초 timeout 적용
- Terminal 에서 다음 사항 확인
    ```
    (myenv) scgyong@tw-reca:[~]$ curl http://localhost:6502/fw/0072/013C
    {"id2":"0073","packets":["205B3C0004000000410C4845524F313320426C61","80636B04307830350F4832342E30312E30322E30","81322E30300E4333353331333235313531383935","820A475032353135313839350C30363537343735","836637613761010001010100025B5D0101"],"error":""}
    (myenv) scgyong@tw-reca:[~]$ curl http://localhost:6502/fw/0076/02121E
    {"id2":"0077","packets":["0812001E040000006E"],"error":""}
    (myenv) scgyong@tw-reca:[~]$ 
    ```
- 

### Test cases
- `Video Resolution` Status Getter 시험 구현. Video Resolution=1
    ```
    Request: http://localhost:6502/fw/0076/021202
    Response: {'id2': '0077', 'packets': ['051200020101'], 'error': ''}
    ```
    - Value `01` = 4K 확인.
      - <img width="217" height="193" alt="image" src="https://github.com/user-attachments/assets/87eb95d9-60ea-42a0-8169-31d5955b884f" />

## ~07/20

### Runner (`pytest`)
- Packet Assembler 구현
  - Array of Array of Byte 형식으로 전달되는 BLE Packet 들을 하나의 Array of Byte 로 조립
  - Android 로부터 넘어온 characteristic uuid 가 기대한 것과 같은지 `assert`
- `GetHardwareInfo` Parser 구현
  - Command Response 들(15종)은 구조체 형식이어서 Parser 구현이 필요함.
  - 공통으로 사용할 수 있는 Parser 함수들 분리
  - Parser 를 Response Char / Id 에 따라 등록 / 검색 할 수 있는 Factory 구현
  - Parser 는 초기버전 function 기반으로 구현했다가 class 기반으로 변경

### Android
- `ForwardRequest` 응답 전달시 notify characteristic 정보를 함께 전달. test 에서 `assert` 할 수 있도록
  - json 에 대한 관리를 `SimpleHttpServer` 가 하지 않고 `ForwardRequest` 가 하도록.

### Test cases
- `Video Resolution` 구현
- `Get Hardware Info` 구현
    ```
    Request: http://localhost:6502/fw/0072/013C
    Response: {'id2': '0073', 'packets': [
      '205B3C0004000000410C4845524F313320426C61',
      '80636B04307830350F4832342E30312E30322E30',
      '81322E30300E4333353331333235313531383935',
      '820A475032353135313839350C30363537343735',
      '836637613761010001010100025B5D0101'
    ], 'error': ''}
    Payload type=0x20. Expected message size=91
    Assembled bytes: 3c0004000000410c4845524f313320426c61636b04307830350f4832342e30312e30322e30322e30300e43333533313332353135313839350a475032353135313839350c303635373437356637613761010001010100025b5d0101
    ```
## ~7/21

### Runner (`pytest`)
- Parser
  - Factory 등록시 ID 와 없이 등록/검색 가능하도록.
    - `QueryResponse` 의 경우 많은 ID 들의 Parser 가 거의 동일한 것으로 확인되었기 때문
  - `CommandParser` Skeleton 추가
    - `GetHardwareInfo` 도 `CommandParser` 상속
    - `GetDateTime` Parser 구현 : 총 15종 중 2개째
  - `QueryParser` Skeleton 추가
    - `setting` 요청
      - Query - Setting - VideoResolution 요청 및 응답 파싱
    - `status` 요청
      - Query - Status - ApModeEnabled 요청 및 응답 파싱
  - Response 에서 TLV Array 를 파싱할 수 있는 구조 구현
    - 많은 곳에서 사용됨

### `pytest`
- `pytest-html` 설치. [Test 실행 방법](testrunner/) 에 설치/실행법 추가

### Test cases
- `get_date_time`, `get_hardware_info`, `status_ap_mode_enabled`, `setting_video_resolution` 을 구현해 보니 `assert` 해야 하는 항목에 공통점이 많음을 발견
- `proceed_agw_test()` 로 리팩토링
  - 스크립팅을 적용하기에 적당하도록


## ~7/22

### 자동 생성
- status test generator
  - Query - Command - (`SettingId`, `StatusId`) 의 응답에 대한 테스트 케이스를 자동 생성하는 스크립트
  - `SettingId` 51종, `StatusId` 72종, 총 123종 test case 자동 생성
  - `13Black` 에서 지원하지 않는 항목(4+11)이 테스트에서 Fail 나옴
    - 제외하여 총 108종 test case 자동 생성

### Runner
- Parser
  - TLV 의 V 를 bytes 에서 int 로 변경. 1/2/4/8 byte 중 하나로 읽게.
    - 아닌 것은 Fail 이 나오게 한 다음 해당 항목을 찾아 예외케이스로 등록
  - GoPro Status 문서에서 API 별로 가능한 값들을 적시한 경우가 있음.
    - html 을 복사하여 `testrunner/util/status_api.txt` 로 저장
    - `testrunner/util/possible_value_extractor.py` 작성
      - `StatusId` 별로 가능한 값들을 `set` 으로 생성하도록
      - `QueryParser` 가 TLV 를 읽을 때 해당 ID 가 `possible_values` 의 key 로 존재하면 해당 값 중 하나인지 `assert`
   
### 특이점
- curl 로 단일 요청은 잘 성공하는데 100여개 test 를 돌렸을 때 대부분 timeout 이 나오는 현상이 발견됨
  - 1회 발견되고 이후 증상 없었지만 기록차원에서 적어둠.

