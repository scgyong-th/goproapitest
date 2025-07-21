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

### test cases
- `Video Resolution` Status Getter 시험 구현. Video Resolution=1
    ```
    Request: http://localhost:6502/fw/0076/021202
    Response: {'id2': '0077', 'packets': ['051200020101'], 'error': ''}
    ```
    - Value `01` = 4K 확인.
      - <img width="217" height="193" alt="image" src="https://github.com/user-attachments/assets/87eb95d9-60ea-42a0-8169-31d5955b884f" />

- 
