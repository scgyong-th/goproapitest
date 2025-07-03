# Preview 07/03

## WBS

### Android Gateway

- 설계
  - UX
  - 기능 명세
  - 통신 Spec 정리
  - Service/Activity 간 데이터 흐름
- 구현
  - Device
    - Wi-Fi Scan / List / Select
    - API 호출 구조
    - Alive 전달
    - Device 상태 관리
  - Test Runner
    - API Server Service 생성 및 실행
    - BLE/Wifi 에 따른 test routing
  - UI
    - Device/Runner 접속 상태
    - 데이터 흐름
  - Service
    - HTTP Server
    - Connect to Camera (추후 BLE)
   
### Test Runner

- Test 설계
  - 전체 API 목록/분석
  - Test case baseclass
- 상수 정의
  - GoPro Python API 로부터 가져오기

- UX
  - 설정 화면
    - 테스트할 카메라, 네트웍에 대한 정보
  - 테스트 케이스 관려
    - 테스트 케이스 버전 관리
      - 서버로부터 다운로드 등은 추후 개발
      - 케이스 루트 폴더를 지정할 수 있는 UI 제공
    - 테스트 케이스들 중 실행할 tree 선택
  - 테스트 진행화면
    - 전체/선택 진행 과정 표시
    - 선택된 테스트케이스의 로그 표시
  - 결과 확인 화면
    - ~~테스트 실행 목록~~
    - 실행 시각 기반으로 결과 폴더 생성
    - 결과 폴더를 열어 주는 버튼 정도
    - 선택된 테스트의 결과 화면
      - Test Report 활용 (Allure Report)
- 

## TODO (~7/9)

### 환경 구축
- GoPro 카메라 수급
  - (dongja) 주말 중 구매. 월요일부터 사용 가능하도록 할 예정. 모델명 정해주세요 (hoon)
- Android 기기 수급
  - 소하동 사무실에 있는 기기 이용. 모델명 Galaxy J5.
  - S10 쓸 수도.
- Git Repo

### Android Gateway
- Service
- HttpServer
- TestRunner HTTP API 설계 및 구현
  - 전체 테스트 시작/진행/종료 등 진행 상황 UX 에 알림
  - Camera 정보 및 네트웍 설정, SSID Connection 실행 등
  - 등록된 API 이외의 요청은 모두 Camera 에게 Forward
- UX(Activity)
  - TestGroup Name, Progress
  - Test Name, Progress
  - Network Status (SSID, RSSI)
  - Device Status (?)
  - Settings (?)

### Test Runner
- Python 환경에서 `adb` 실행 가능성 확인
- GUI Toolkit 결정
- Test Cases
  - Get Camera State
    - Request: `http://10.5.5.9:8080/gopro/camera/state`
    - Response: `{ "settings": {...}, "status": { ... }` 약 140 줄
  - Set Settings
    - Video Resolution (setting=2)
      - Query: `http://10.5.5.9:8080/gopro/camera/setting?setting=2`
      - Setting: `http://10.5.5.9:8080/gopro/camera/setting?option=100&setting=2`
      - Options: `1` = 4k, `4` = 2.7k, `6` = 2.7k 4:3, ...
      - 모델별 설정 가능한 항목이 다르므로 각 항목을 설정 가능한지 테스트
      - 설정 후 다시 얻어서 잘 설정되고 읽는지 확인
    - Video Timelapse Rate (setting=5)
      - Query: `http://10.5.5.9:8080/gopro/camera/setting?setting=5`
      - Setting: `http://10.5.5.9:8080/gopro/camera/setting?option=4&setting=5`
      - Options: `0` = 0.5sec, `1` = 1 sec, `4` = 10 sec, `5` = 30 sec, ...
        - `0` ~ `10` 까지는 모든 모델, `11`(3sec) 는 일부 모델만 지원
      - 설정 후 다시 얻어서 잘 설정되고 읽는지 확인
  - Settings 통합
    - GetCameraState 와 개별 Settings 에서 얻어 온 값이 같은지 확인
  - 위 case 까지 만들어 보고 고려해야 하는 상황 확인
  - `pytest-html` 혹은 `AllureReport` 의 결과 확인
 
