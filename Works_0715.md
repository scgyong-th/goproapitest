# Works ~ 7/15

## 07/11
- Android Project 생성
  - Activity 생성
    - Kotlin Compose 이용
    - BLE Device Scan 결과 목록 보여주기
    - GoPro Serice ID 로 Filter 정해서 Scan
      - GoPro 기기 확인
      - Manufacturer Info 표시
    - BLE Connect
    - Service Discover
    - Characteristic 확인
      - READ/WRITE/NOTIFY 정보 확인
      - NOTIFY 인 경우 Listen (Subscription) 등록
        - 약 10여 개 Char 에 대해 등록
      - `Assets/uuid.json` 만들어 char 이름 확인할 수 있도록
  - Service 생성
    - NanoHttpd 상속하여 Web Service
    - adb forward 를 통해 mac terminal 에서 접속되는 것 확인
   
## 7/12
### UI
- Scan 한 결과로 Connect 를 했다면 이름/주소 등을 Prefs 에 저장
- 저장된 Device 로 바로 접속할 수 있도록
- Serialization 이용

### BLE
- `GetHardwareInfo`
  - 접속 후 첫번째 메시지
  - 이 응답이 올때까지 재시도해야 한다고 함
- `BleMessage` class 작성
  - `GoProUUID` enum class 로 UUID 제공
  - 확장을 기대했으나 추후 폐기
- `Command` (`0072`) characteristic 에 write 후 `Command Response` (`0073`) notify 받기 성공
  - `GetHardwareInfo` 의 응답은 5개의 20 byte packet 에 나뉘어 오므로 조합 구현
  - Response Parser 구조
    - Parser Factory: Notification message 의 ID 를 보고 어느 class 로 parse 해야 하는지 결정
   
## 7/14
### UI
- Activity 분리
  - MainActivity
    - 최근 접속 Device 보여주고 Connect 버튼
    - Scan 버튼 -> ScanActivity
    - 접속 후 각종 상태 정보
      - Connected
      - HardwareInfo
      - WifiSsid
      - WifiPassword
  - ScanActivity
    - Scan 만 전문
    - 최근 접속한 Device 가 있을 때에는 Scan 을 할 필요 없음
    - 5초 후 Scan 자동 중지
   
### BLE
- `WiFiSsid` 및 `WiFiPassword` 얻기
  - `Read` Characteristic 사용
  - `Read`, `Write`/`Notify` Request 를 Queue 에 넣고 한 번에 하나만 요청하는 구조
- AP Enable Command 구현
- Connection Scenario 완성
  - `getHardwareInfo`
  - `WiFiSsid`
  - `WiFiPassword`
  - `Set Seetting` : `SET_AP_CONTROL`, `true`
- Request 에 Respoonse Callback 붙이는 구조 완성

### HTTPD
- `/app/connect` API 를 받아 최근 Device 로 접속하는 구조 완성
  - 실제 터미널에서 `curl` request 로 접속 성공
  - Service -> Activity 로 Intent Broadcast
  - 값을 리턴받기 어려운 구조라 폐기

## 7/15
### HTTPD
- Service 에서 운용하던 것을 Activity 에서 하는 것으로 변경
  - Activity 의 ViewModel 을 공유하여 사용
  - `Latch` 를 이용하여 BLE 로 메시지 보내고 그 응답을 http response 로 보내는 구조 완성
  - 추후 http API 도 이 방식 이용
 
### BLE
- `CommmandId`, `QueryId`, `StatusId` 정리
  - template 만 주고 GoPro API 문서 넘겨주니 ChatGPT 가 잘 생성
- Query 실패
  - Query (`0076`) 을 보냈는데 (write success) Query Response (`0077`) 이 오지 않음
  - 원인 파악 중
