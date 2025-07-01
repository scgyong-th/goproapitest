# Preview @07/01

## PyTest 조사

* python module 로 간단히 설치, python 코드 이용.
* `test_` 로 시작하는 파일명, 함수명 등 자동 감지
* `assert` 구문만으로 테스트 작성
* Fixture/Parameter/반복테스트 등 가능
* `pytest` 명령어 및 parameter 로 다양한 형태의 테스트 실행 가능

## Test 구성
```
+-----------------+     WiFi/USB/ADB    +-----------------+     BLE      +--------------------+
|   PyTest Runner |  <----------------> | Android Gateway |  <---------> |  BLE Device (DUT)  |
+-----------------+                     +-----------------+              +--------------------+
     |     ^                                 |
     |     |  Test Scripts (PyTest)          |
     |     |                                 |
     |     +-------------------------------> |
     |
     |    +-------------+
     +--> | Test Server |
          +-------------+
```

### PyTest Runner
- Case 개발을 위해 필수적인 공통 라이브러리 개발
- Python 을 사용하여 다양한 TestCase 개발/구현
  - 초기 버전에는 일부만 구현, 향후 늘려 나감
- CLI based.
  - 향후 GUI 도입 가능
  - 향후 PyInstaller 등으로 python 설치 없이도 동작하게 가능
- 결과 정리
  - pytest-html : 1 HTML 로 정리
  - pytest+AllureReport
    - Allure TestOps는 JetBrains가 만든 엔터프라이즈 테스트 관리 플랫폼
      - 가격은 대략 인원수x월x$39
      - AllureReport 만은 Open.
    - HTML+JSON 으로 결과 생성
- Test Server 에 결과 Upload

### Android Gateway (AGW)
- Test Runner 로부터 Test Case 들을 전달받아 BLE/Wifi 통신을 통해 카메라에 전달하는 역할
- Setup 과정은 1차 구현에서는 간단하게 구현
  - Connection 관련 테스트는 추후 개발
- 간단한 Web Server 를 `8080` Port 에 띄움 (`adb` 를 사용할 경우)

### TestRunner <-(USB)-> Android
- `adb` 를 활용할 경우 별다른 구현이 필요없음
  - `adb reverse tcp:8080 tcp:8080` 만 실행시키면 연결됨
  - `adb` 를 배포하는 것은 문제가 있을 수 있으므로 Android 개발툴 설치 권장
    - 설치 링크 안내: https://developer.android.com/tools/releases/platform-tools

- 어려운 방법들
  - 항시 Wifi 이용: COHN 모드일 때만 가능하므로 Test Device 가 AP Mode 일 때에는 Test Runner 가 AGW 에 접속할 방법이 없음
  - USB Device/USB Accessory 이용
    - PC가 USB Accessory 역할을, Android는 USB Device 역할을 하거나 Android가 Host가 되어 USB 장치(DUT 등) 제어 가능.
    - 구현량이 상당하고, 직접 매우 저수준의 USB 프로토콜 설계가 필요함
  - 하나의 Wifi 연결을 번갈아 활용할 경우
    - 구현 진행
      - AGW 에게 Test 내용을 전달한 뒤
      - Wifi 를 끊고 Test Device 에 접속해서 Test 진행 후
      - 결과를 받으면 다시 네트웍을 끊고 Local AP 에 접속한 뒤
      - Test Runner 에 결과 전송
    - 구현량이 많고 AGW 와 Test Device 사이 연결이 불안정해지거나 Test Device 의 AP Mode 해제 등 다수 문제
  
### Test Server
- 기능
  - Case 개발 후 배포
  - 결과 취합, 누적, History
- 구현
  - 간단한 웹서버 및 Metadata 저장/검색용 간단한 DB
  - 기기별, 테스트케이스 버전별, 날짜별 테스트 기록 열람
 
## 실행 시나리오

### PyTest 실행기
- CLI Based. GUI 기반은 추후 구현
- 접속할 기기 정보 설정
  - `json` 등 설정 파일 활용. GUI 설정 화면은 추후 구현
- 서버에서 최신 테스트케이스 확인
  - 다운로드 및 압축 해제
  - TODO: 위조 방지 암호화
  - 예시
    ```
    test_case_pack_v25.7.1.zip
    ├── tests/
    │   ├── test_ble_connect.py
    │   ├── test_http_status.py
    │   └── ...
    ├── requirements.txt
    ├── README.md
    └── config.json   ← 테스트 시나리오 설명, 기대값 등
    ``` 
- AGW 가 실행중인지 등 상태 확인
  - 버전 체크. 최신 테스트케이스의 경우 높은 버전의 AGW 가 필요할 수도 있음
- Test 실행
  - `pytest downloaded_tests/`
- 결과 수집 및 리포트 생성
  - allure report 활용
  - .html, .json 파일 생성
- Report 서버에 업로드

### Test Server 구현
- Flask+SQLite 사용
  - 구성
    ```
    ┌──────────────┐    HTTP   ┌─────────────────────┐
    │  테스트러너     │──────────▶│  테스트 서버 (Flask)  │
    │ (PyTest+실행기)│           │ - 케이스 배포         │
    └──────────────┘           │ - 결과 수집 API       │
                               │ - 결과 DB 저장        │
                               │ - HTML 리포트 호스팅   │
                               └─────────────────────┘
                                       │
                               🔍 결과 웹 뷰어 (Flask)
    ```
  - Why Flask?
    - Python 생태계, 단순한 REST, 빠른 개발, 가벼움
    - 다른 선택지: FastAPI, Django, Express.js 등 모두 overspec
- 구현 기능
  - 리포트 업로드
    - `POST /upload-report` API
      - Body: multipart/form-data
      - Fields: report.html, tester_id, device_id, version, timestamp, ...?
  - 테스트 히스토리 페이지
    -  `/history/<model>`, `/report/<id>` 등
    -  모델별, 테스터별, 시기별, ...?
  - 배포 파일 관리
    - `/get-latest-case` API
  - 인증
    - https, login, 암호화, 테스터토큰, ...?
- 추가 확장: 추후 구현
  - 결과 diff 비교: 이전 결과와 비교하여 리그레션 확인
  - 인증 / 권한 시스템: OAuth, 토큰 등
  - 테스터용 실행기 자동 업데이터: 실행기 버전도 서버에서 배포
  - 리포트 자동 이메일 전송: SMTP 연동 등으로 결과 알림



