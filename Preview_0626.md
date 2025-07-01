# Research 0626

## 검토한 Test Framework
- nRF Connect for Mobile (Nordic), LightBlue Explorer, BlueSee
  - BLE 관련 테스트에 국한
  - 기능 제한
- PostMan/Android, RESTer
  - HTTP 테스트에 국한
- RxAndroidBle
  - BLE 테스트, RxJava, ?
  - 좀 더 검토 필요
- OkHttp
  - HTTP API 라이브러리
- JUnit
  - Java 에서 널리 사용되는 Test Framework
- Android Instrumented Test (JUnit + Android API)
  - BLE Test 가 가능한 방식 (좀 더 검토)
- Expresso, Appium
  - JUnit 과 함께 사용하는 UI Test Automation
- AllureReport, TestRail, ReportPortal
  - Test 리포트 및 기록 플랫폼
  - 좀 더 검토 필요
- Firebase Test Lab
  - Firebase Console 에서 스크린샷, 로그, 비디오 등 확인. ?


## 일반 테스트 개발과 다른 점
- JUnit 으로 개발된 TestCase 들은 개발툴 (Android Studio) 에서 별도 View 로 실행됨
- BLE 테스트는 반드시 실기기 필요
- 테스터마다 다른 기기에 접속해야 하는 등 설정 필요하며 역시 기기에서 실행

## 조합 제안
### (1차)
- JUnit 기반 테스트 프레임웍 개발
- Android App 을 개발하여 다음 화면으로 분기
  - BLE 기기/HTTP 주소 등 개별 설정 혹은 Scan
  - JUnit 기반 테스트 진행
    - 일반 App 에서 JUnit Runner 실행 및 결과 취합
    - 가능하다고는 알려져 있으나 좀 더 검토 필요
    - => JUnit 의 장점을 살릴 수 없음. (폐기)
  - 테스트 종류 구분
    - UI 없이 할 수 있는 테스트
    - 사용자 확인이 필요한 테스트
      - 확인이 필요한 테스트만 따로 만들고 나머지는 JUnit 만으로 만들지 좀 더 검토
  - 결과 Report 및 전송(?)
- Allure 등 조사후 적용 가능한 경우 리포트 생성 및 이력 관리

### 조합 제안 (수정안)
- JUnit 기반 테스트 프레임웍 개발
- Android Studio 에서 실기기 연결 후 테스트 수행
  - Android Studio 내 JUnit View 에서 각종 결과 확인
- 사용자 UI 확인이 필요한 항목은 별도 App 으로 개발

## Tutorial base
Connect BLE
TLV Commands/Responses/Queries
Protobuf Operations
WIFI Connection
Commands
Media List
Home Network (COHN)
- Cert?

## SDK
in Kotlin


## GPMF
Sensor Data Parsing
- in C Language

## Protocols

### BLE

* Setup
  - Scan
  - Finish Paring
  - Advertised Services
  - 기기별 Advertised Data 검증, TLV 검증
    - BLE Spec 에 맞는지 검증하는 것은 Nordic 등이 더 적합할 수 있음.
    - GoPro BLE Spec 에 정의된 것 검증 필요
  
* State
  - Camera Readiness
  - Keep Alive
  - Camera Control

* Control
  - KeepAlive, Reboot, Analytics, AP Control, Camera Control, Date/Time, Paring State, Shutter, TurboTransfer, Sleep

* Query
  - Date/Time, HW Info, Media, Version, Settings/Status/Capabilities, Register/Unregister

* Access Point
  - Scan, ScanResult, Connect, Disconnect

* Live Streaming
  - Set Mode, Get Status

* Highlights
* Presets
* Settings (약 50여개)
* Status (약 100여개)

### HTTP
* Overview
  - Capture photo/video media
  - Get media list
  - Change settings
  - Get and set the date/time
  - Get camera status
  - Get media metadata (file size, width, height, duration, tags, etc)

* COHN
* Control
* Hilights
* Media
  - Delete, Download, Capture, GPMF, Telemetry, File Info, Screennail, Thumbnail, List

* OTA Update
* Preview Stream
* Query (매우많음)
* Settings (매우많음)

* Webcam?

## TODO
* USB Connections?
