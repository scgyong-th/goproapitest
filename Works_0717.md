# Works ~07/17

## BLE
- Notify Subscription 문제 해결
  - `0072` (Command Request) 에 대한 응답 `0073` (Command Response) 은 잘 오는데 `0076` (Query Request) 에 대한 응답 `0077` (Query Response) 는 오지 않는 문제 있었음
  - 여러 시도 끝에 Desriptor Write 도 성공 결과를 확인한 후에 다음 것을 해야 하는 것을 알게되어 문제 해결
- Response Hierarchy 및 Factory 가 알맞은 Response 를 찾아가도록
    ```
    NotifiedResponse
     └ CommandResponse
       └ GetHardwareInfoResponse
     └ QueryResponse
    ```
- 용어 및 ID 정리
  ```
  - Characteristics
    - Read
      - WifiSsid: `String`
      - WifiPassword: `String`
    - Command Request/Response
      - GetHardwareInfo: `GetHardwareInfoResponse`
      - SetAPControl: `NotifiedResponse`
    - Setting Request/Response
    - Query Request/Response
      - GetSettingValues
      - GetStatusValues
        - GetAPModeEnabled: `QueryResponse`
  ```
- Response 조합 구조 Spec 에 맞추어 구현
  - Payload Type
    - General (<= 20 bytes): 1번째 바이트에 크기, 2번째 바이트부터 데이터
    - Ext-13bit: 1,2 번째 바이트에 크기, 3번째 바이트부터 데이터
    - Ext-16bit: 2,3 번째 바이트에 크기, 4번째 바이트부터 데이터
  - Continuation Packet
    - index 로 `0x80` 부터 `0x8F` 까지 순환하는 구조
  - 

## HTTPD
- API 정리
  - `/app/connect` : BLE 접속 시도
  - `/app/status/ap_mode` : AP Mode 얻어 오기
  - `/app/set/ap_mode/true` or `/app/set/ap_mode/false` : AP Mode 켜고 끄기
  - `/app/wifi/connect` : Wifi 접속 시도
 
## HTTP

- Wifi 접속
  - SSID, PW 를 이용하여 Camera 에 접속
  - GoPro 는 기본 설정이 5GHz 로 되어 있어서 테스트 폰에서 보이지 않음
    - GoPro 설정에서 변경해야 접속 가능
  - API Level 에 따라 접속방법이 다름
    - API29 이후에는 사용자 동의도 필요
- HttpClient 라이브러리 시도
  - `Ktor` 사용
    - 버전 문제로 시간 많이 허비
    - `CIO` 버전과 `OkHttp` 버전을 사용할 수 있음
    - 결국 `CIO` 는 API24 이후에만 사용할 수 있는 것을 알아냄
    - `OkHttp` 버전으로 전환하여 정상 동작 확인
  - Coroutine 기반 `suspend fun` 활용 (`Ktor`)
  - `KeepAlive`
    - API Spec 에 따라 GET: `/gopro/camera/keep_alive` 로 요청
      - Error Response (Bad Request) 를 받다가 여러번의 시도 끝에 성공

## UI
- AP Mode 상태 표기: `enabled`, `disabled`, `timeout`
- Keep Alive: HTTP/Wifi 로 Keep Alive 송수신한 시각 표시

## TODO
- pytest testcase 와 연결

