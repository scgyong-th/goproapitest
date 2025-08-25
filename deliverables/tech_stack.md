# Technology Stack
![GitHub tag (latest)](https://img.shields.io/github/v/tag/scgyong-th/goproapitest)

## Overview

```
+-----------------+       USB/ADB       +-----------------+   BLE/Wifi   +--------------------+
|   PyTest Runner |  <----------------> | Android Gateway |  <---------> |  BLE Device (DUT)  |
+-----------------+                     +-----------------+              +--------------------+
           ^                                 |
           |  Test Scripts (PyTest)          |
           +-------------------------------> |
```

## Android Gateway (agw)

* Test Runner 로부터 Test Case 에 사용되는 요청을 HTTP 로 전달받아 BLE/Wifi 통신을 통해 카메라에 전달하는 역할
* Kotlin 을 사용하여 작성되었으며, Kotlin Compose Application Model 을 사용하였음

### BLE

* Main Class
  * [MainModel.kt](../../tree/main/agw/pilot/app/src/main/java/com/example/xiangatewaypilot/model/main/MainModel.kt)
  * Kotlin Compose 의 ViewModel 로서 동작
* Scan
  * GoPro BLE Spec 에 따라 Service UUID 를 Filter 로 Scan 및 Connect.
  * [BleScannerVM.kt](../../tree/main/agw/pilot/app/src/main/java/com/example/xiangatewaypilot/model/scan/BleScannerVM.kt)
  * 이 클래스는 Scan 만 담당하고, Connect 및 Discover 와 나머지 모두는 `MainModel` 에서 진행
* Services/Characteristics
  * Read
    * WiFi SSID / Password
  * Write/Notification
    * Command/Query/Setting 에 대한 Request 와 Response
* 기본적인 Request/Response 에 대한 구현
  * [BleRequest.kt](../../tree/main/agw/pilot/app/src/main/java/com/example/xiangatewaypilot/data/requests/BleRequest.kt) 에
    `BleRequest`, `BleRequest.Read`, `BleRequest.WRite` 가 구현되어 있으며,
    [Messages.kt](../../tree/main/agw/pilot/app/src/main/java/com/example/xiangatewaypilot/data/requests/Messages.kt) 에
    `CommandRequest`, `QueryRequest` 및 기본 정보를 제공하기 위하여 이를 상속하는 여러 구체적인 클래스들(`KeepAliveRequest`, `GetHardwareInfo`, ...) 을 정의하였다
* Handshake: 최초 접속시 진행하는 시나리오 구현
  1. `PairingFinishRequest`
  2. `GetHardwareInfo`
  3. `GetWifiApSsid`
  4. `GetWifiApPassword`
  5. `QueryRequest` - `QueryId.GET_STATUS_VALUES`, `StatusId.AP_MODE_ENABLED`
  6. `SetApControl(true)`
  7. `QueryRequest` - `QueryId.GET_STATUS_VALUES`, `StatusId.AP_MODE_ENABLED`
  8. connect to WiFi
* Message Queue 및 3회 재전송 구현
* n 초 동안 아무런 Request 가 없으면 Keep Alive 를 보내도록 구현
* Multiple Packet Composition
  * GoPro Spec 상 20바이트가 넘는 메시지들 (`GetHardwareInfo` 등) 은 여러 패킷에 나뉘어 오기 때문에 이를 조합하는 구조가 필요
  * Continuation Packet 처리
    * [NotifyReassembler.kt](../../tree/main/agw/pilot/app/src/main/java/com/example/xiangatewaypilot/data/NotifyReassembler.kt
    * Payload 가 일반 (19바이트 이내), 확장 13비트 (8K 이내), 확장 16비트 (그 이상) 으로 구별되므로 이에 따라 후속 메시지들을 조합
    * Payload index 는 4비트만 사용하므로 0x00 ~ 0x0F 사이로 순환됨.
  * Forwarded Response (`ForwardedRequest.Response`)
    * [ForwardedRequest](../../tree/main/agw/pilot/app/src/main/java/com/example/xiangatewaypilot/data/requests/ForwardedRequest.kt) 가 직접 처리
    * 직접 Parsing 할 메시지는 `NotificationReassembler` 가 조합해야 하지만 Test Runner 에게 전달할 Packet 은 그대로 `val byteArrayMap = mutableMapOf<Int, ByteArray>()` 에 쌓음
    * JSON String array 형태로 만들어서 Runner 에게 전달. 조합 및 파싱을 모두 Runner 가 할 수 있도록.
* Protobuf
  * 거의 모든 패킷을 그대로 Runner 에게 전달하므로 Protobuf 를 많이 사용하지는 않는다
  * `PairingFinishRequest` 에서 간단히 사용한다
  * GoPro 에서 배포한 `.proto` 파일들을 소스에 포함하고 있으며 ([proto](../../tree/main/agw/pilot/app/src/main/proto/)) proto 플러그인에 의해 `.java` 파일이 생성되어 빌드에 포함된다
    * 생성된 `.java` 파일은 `git` 에 올리지 않아도 되도록 하고 있다

### WiFi

* [WifiHttpClient](../../tree/main/agw/pilot/app/src/main/java/com/example/xiangatewaypilot/model/main/WifiHttpClient.kt) 
* HTTP over wifi 로 메시지 전달
* `OkHttp` 라이브러리 이용
* BLE 로 얻어 온 SSID 및 Password 로 카메라에 접속
  * `Build.VERSION_CODES.Q` 이상과 미만일 경우 다르게 구현
* Keep Alive 를 구현해 두었지만 BLE 것을 사용하면서 WiFi 의 것은 사용하지 않음
* Runner 로부터 온 요청이 http 인 경우 (`/http/*`) 이곳을 통해 카메라에 전달
* Kotlin CoRoutine 사용 (`suspend fun`), `async` 로 동작.

### Http Server
* [SimpleHttpServer](../../tree/main/agw/pilot/app/src/main/java/com/example/xiangatewaypilot/httpd/SimpleHttpServer.kt)
* `NanoHTTPD` 라이브러리 이용
* `fun serve(session)` 에서 `session.url` 로 분기
* 서비스 종류
  * 즉각응답
    * `/app/info`: static 정보와 함께 Main Model 이 BLE 연결 되어 있는지 여부를 포함하여 전달 (`connected`: `true`/`false`)
    * `/app/get_hardwar_info`: BLE 가 카메라에 접속되어 있었다면 해당 값을, 아니면 `not connected` 정보를 전달.
    * `/app/connect`: 연결을 시작시킴. 이미 연결되어 있다면 아무 일도 하지 않음.
    * `/app/wifi/connect`: WiFi 연결을 시작시킴. 현재 사용하지 않음.
  * Test Message
    * PC/Mac 의 Terminal 에서 `curl` 을 이용하여 BLE 메시지가 잘 가는제 테스트할 목적으로 만든 메시지
    * `/app/status/ap_mode`: Camera 가 AP Mode 를 활성화했는지 문의 후 답함. `Enabled: true` 혹은 `Enabled: false` 로 응답.
    * `/app/set/ap_mode/true`, `/app/set/ap_mode/false`: Camera 의 AP Mode 를 활성화하거나 비활성화한다
  * BLE Forward:  `/fw/{char}/{msg}`
    * char 는 2 byte (이하 `ID2` 로 부름) 로 표현되는 characteristic. `0072`, `0074`, `0076` 등이 올 수 있다
    * msg 는 1바이트당 2글자의 hex string 으로 표현된 패킷 데이터이다
    * `SetApContol` 의 경우 `/fw/0072/03170101` (enable) 혹은 `/fw/0072/03170100` (disable) 이 된다. (`0x17` = `CommandId.SET_AP_CONTROL`)
  * Wifi Forward: `/http/*`
    * `*` 의 모든 메시지는 `MainModel` 및 `WifiHttpClient` 를 통해 HTTP over Wifi 로 카메라에 전달된다
    * 카메라가 응답한 메시지를 그대로 Runner 에게 답한다
* Response Message
  * 테스트 메시지를 제외하면 모든 응답은 JSON 형태로 이루어진다
  * BLE Response 는 다음 형태로 구성된다
    ```
    {
      "id2": "0073",
      "packets": [
          "205B3C0004000000410C4845524F313320426C61",
          "80636B04307830350F4832342E30312E30322E30",
          "81322E30300E4333353331333235313531383935",
          "820A475032353135313839350C30363537343735",
          "836637613761010001010100025B5D0101"
      ],
      "error": ""
    }
    ```

### Permissions

* Bluetooth Scan/Connect, Wifi Connect, Internet 등을 위해 다음 Permission 들이 필요하다
  
    ```
    <uses-permission android:name="android.permission.BLUETOOTH" />
    <uses-permission android:name="android.permission.BLUETOOTH_ADMIN" />
    <uses-permission android:name="android.permission.BLUETOOTH_SCAN" />
    <uses-permission android:name="android.permission.BLUETOOTH_CONNECT" />
    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.CHANGE_WIFI_STATE" />
    <uses-permission android:name="android.permission.CHANGE_NETWORK_STATE" />
    <uses-permission android:name="android.permission.WRITE_SETTINGS" />
    <uses-permission android:name="android.permission.INTERNET" />
    ```

### Libraries
* compose: 기본 골격
* plugin.serialization: `SimpleHttpServer` 에서 map Object 를 JSON 으로 변환하기 위해 사용
* nanohttpd: `SimpleHttpServer`
* okhtt, cio: `WifiHttpClient`
* protobuf: `PairingFinishRequest` 등에서 사용. 원래는 GoPro API 전반적으로 사용되나 대부분 Runner 쪽에서 사용.

## PyTest Runner
* `pywebbrowser` 모듈로 UI 를 보여주고 `adb` 를 사용하여 `agw` 와 통신한다.

### Runner UI
* `pywebbrowser` 를 이용한 FrontEnd
  * `res/main.html` 및 `res/main.css` 로 화면 drawing.
  * `bootstrap`, `jquery` 이용
  * `WebBrowser2` (Microsoft Edge Runtime) 가 설치되어 있어야 하지만 대부분의 PC 에 설치되어 있음
* `adb` 를 이용한 BackEnd
  * `adb_bridge.py` 가 주로 담당.
  * `adb` 를 `subprocess.run()` 을 호출하여 실행
    * `adb devices -l` 로 기기 (Serial, Model) 발견
    * TCP forward 설정
    * `adb shell monkey` 로 기기에서 `agw` 앱 실행
* FrontEnd `<->` BackEnd
  * `web_api.py` 가 주로 담당
  * `webview.create_window(..., js_api=webApi, ...)` 를 통해 frontend 에게 bridge 전달
    * frontEnd 에서는 `window.pywebview.api.some_func()` 로 `webApi.some_func()` 실행
      * `connect_age()`, `connect_ble()`, `get_app_info()` 등 호출 (`main.html` 내의 `<script ...`)
    * backEnd 에서는 `window.evaluate_js('script')` 로 web contents 함수 호출
      * `appendLog()` 등 호출
* `pytest` 실행
  * 시간이 걸리는 작업이므로 별도 thread 를 만들어 실행
  * `Tee` class 를 정의하고 `pytest` 를 실행하기 전에 `sys.stdout` 과 `sys.stderr` 를 `Tee` 객체로 치환, 실행 끝난 후 원래의 것으로 되돌림
  * `Tee` 의 `write()` 에서 `window.evaluate_js(appendLog(...))` 실행
  * `agw` App 정보와 접속된 Cam 정보를 metadata 로 넘겨서 `report.html` 에서 확인 가능하도록
* Report
  * `results/report.html` 에 pytest-html 플러그인을 사용하여 결과를 저장
  * `Report` 버튼 누를시 System Web Browser 로 띄움.

### Camera Module

* test 에서 이용할 수 있도록 제공되는 Utility
* `constants.py`
  * `ID2`, `ID2_map.service`, `ID2_map.resonse`: Characteristic 관련
  * `QueryId`, `CommandId`, `SettingId`, `StatusId`: 각종 상수들
  * `SettingId_possible_values`, `StatusId_possible_values`: Setting 과 Status ID 별로 설정 가능한 값들 모음
* `ble_request.py`
  * `BleRequest`, `BleReadRequest`, `BleWriteRequest`: Base 메시지들
  * `CommandRequest`, `QueryRequest`, `SetSettingValue`, `GetSettingValues` : 종류별 1단계 메시지들
  * 그 외 Requests: 2단계 이상 구체적인 메시지들 (`GetHardwareInfo` 등)
* `parsers`
  * 각종 메시지들의 Response Parser 구현
  * Continuation Packet 조합하는 코드 포함
* `test_steps.py`: 많은 테스트에서 공통으로 사용할만한 진행을 제공. BLE Forward 의 경우 다음 순서로 되어 있다.
   1. `/fw/{char}/{msg}` 형태로 URL 생성
   2. http 요청
   3. JSON 응답 파싱
   4. 응답 ID2 확인
   5. Continuation Packet Accumulation
   6. Parser 호출
   7. 파싱
 
### proto Module

* `*.proto` 파일을 컴파일하여 python 소스로 생성시킨 파일들
* protobuf compiler 를 쓸 수도 있지만, OpenGopro 의 Python 버전에 들어있는 생성된 소스를 그대로 복사하여 프로젝트에 추가함

## Test Cases

### 개발 및 실행 환경

* 개발시 python 에 여러 module 들을 설치해야 하므로 `venv` 사용을 권장한다. `mingw`/`bash` 기준으로 다음과 같이 한다.
  * venv 생성
    ```
    python -m venv ~/thenv
    ```
  * venv 활성화
    ```
    source ~/thenv/Scripts/activate
    ```
  * 개발시 필요한 모듈 설치
    ```
    pip install -r requirements.txt
    ```
* `runner_ui/requirements.txt` 에는 다음 모듈들이 포함되어 있다
  * `pywebview` : runner 의 UI 를 HTML/CSS/Javascript 를 이용해서 보여줄 수 있도록한다
  * `requests` : Runner `<->` AGW 사이에 http 호출을 할 때 이용한다
  * `protobuf` : `.proto` binary 를 encode/decode 한다
  * `construct` : `protubuf` 관련 활용
  * `pytest` : Test Framework
  * `pytest-html` : Test 결과물을 Formatting 할 때 사용하는 pytest plugin
  * `allure-pytest` : Test 결과물 Formatting 옵션 (현재 버전에서 사용하지는 않음)
  * `pyinstaller` : python 파일들을 windows exe 로 build

### tests 폴더 구조
* `tests` 는 다음 폴더 구조를 가진다
```
├─00_init
├─01_gateway
├─ble
│  ├─control
│  ├─query
│  │  ├─command
│  │  ├─generated
│  │  ├─query
│  │  ├─setting
│  │  └─status
│  └─setting
├─http
│  └─query
└─zz_last
```
* `tests` Root: session scope 의 config 를 읽어 오는 fixture 가 들어 있다. 개발시에는 `tests` 폴더의 `test_config.json` 을 읽고, 컴파일된 exe 에서는 exe 와 같은 폴더에서 읽는다
* `00_init`: 가장 먼저 실행될 수 있도록 `00` 을 붙였다.
* `01_gateway`: `agw` 에게 `/app/info` 를 요청한 결과를 출력만 한다. `report.html` 에 app info 가 포함되게 하려는 목적이었는데, 지금은 `--metadata` 로 html 앞부분에 나오기도 한다.
* `ble`: BLE 관련 테스트들
  * `ble/query/generated`: 생성된 테스트들
* `http`: HTTP 관련 테스트들
* `zz_last`: 마지막에 실행되어야 하는 테스트로 sleep 상태로 들어가게 하는 명령을 전송한다

### util 
* 개발 도중 사용한 utility script 들이다
* `setting_status_tests_generator.py`
  * `SettingId`, `StatusId` 에 정의된 상수들을 가지고 test case 들을 생성해 낸다
  * `special_cases.py` 에서 제한하는 것들을 제외하고 생성한다
* `possible_value_extractor.py`: `status_api.txt` 의 값을 활용하여 코드 생성. 이렇게 생성된 코드는 `camera` 모듈의 `constants.py` 에 포함되었다.
* `possible_setting_value_extractor.py`: `setting_api.txt` 의 값을 활용하여 코드 생성. 이렇게 생성된 코드는 `camera` 모듈의 `constants.py` 에 포함되었다.
* 위 txt 파일은 OpenGoPro API HTML 문서로부터 복사/붙여넣기 한 파일이다
* `possible_hero13_setting_test_generator.py`: `tests/ble/setting/test_set_setting.py` 에 parametrize 된 항목을 생성하기 위한 코드. 현재 많은 case 들은 comnent out 되어 있다.

### Test Case 추가 개발
기존에 개발해 놓은 테스트 케이스들을 유형별로 분류해 보았다. 이 중 유사한 구조를 택해 적당한 폴더 내에 추가하면 된다
* `tests/ble/control/test_keep_alive.py`
  * `camera.KeepAliveRequest()` 가 제공된다
  * Request 를 만들고 `proceed_agw_test()` 만 호출하면 대부분 해결된다
* `tests/ble/control/test_date_time.py`
  * `camera.GetDateTime()`, `camera.GetLocalDatTime()`, `camera.SetDateTime()`, `camera.SetLocalDatTime()` 등을 이용하여 조합을 테스트한다
* `tests/ble/control/test_camera_control.py`
  * `camera.SetCameraControl()` 가 제공된다
  * Request Param 및 Response 는 Protobuf 로 되어 있다
  * x 로 요청시 y 로 응답해야 한다를 목록으로 만들어 `parametrize` 한다. 여러 개의 sub test 로 진행된다
* `tests/ble/control/test_turbo_active.py`
  * parametrize(True, False) 를 하여 sub test 로 만든다
  * 설정 Request 는 `camera.SetTurboActive()` 가 제공되며 Response 는 Protobuf 이다
  * 확인 Request 메시지는 범용 `camera.GetStatusValues()` 를 사용하며 상수 `camera.StatusId.TURBO_TRANSFER_ACTIVE` 를 전달한다
  * 설정한 값이 확인한 값과 같은지 `assert` 한다
* `tests/ble/query/command/test_turbo_active.py`
  * `SetShutter(True)` 를 호출하고 1초 Sleep 한 후 `SetShutter(False)` 를 호출한다.

* 추가한 테스트의 폴더는 어디가 되어도 상관 없지만, 기존 개발 케이스들은 다음 구조를 따랐다
  * `tests/ble/` 아래의 폴더 선택 (control/query/setting)
    * OpenGoPro 문서 내의 좌측 분류를 따름
  * 그 아래 폴더 (`tests/ble/분류/*`)
    * 사용하는 Characteristic 에 따라 command/setting/status 등으로 구별
* test case 에서 import 하는 module 은 exe 에 자동으로 포함되지 않기 때문에, 후술하는 방법에 따라 `main.spec` 에 추가시켜주어야 한다. 유지보수를 위해서 `requirements.txt` 에도 추가해 주는 것이 좋다.

### Runner 빌드

* Runner 는 `PyInstaller` Module 을 사용하여 Windows exe 로 빌드한다
* Windows Machine 에서만 빌드 가능하다
* pyinstaller 에 여러 옵션을 주면 `.spec` 파일이 만들어지지만, 그 옵션이 `main.spec` 파일에 기록되어 생성되며, 이 파일에 옵션들을 유지한다.
  * 옵션들 중 일부는 다음과 같다
    * `datas` : 빌드에 포함된 뒤, 실행 직전에 _MEI 임시 폴더에 풀린 채로 시작한다. _MEI 폴더는 실행 후 삭제된다.
    * `hiddenimports` : pyinstaller 는 `main.py` 로부터 import 되는 모듈들은 자동으로 추적하지만 test case 에서는 아니다. 따라서 test case 에서 import 할 모듈이 있다면 이곳에 포함시켜 주어야 한다.
    * `console=True` : 기본적으로 콘솔을 포함한 빌드이다. 이것을 `False` 로 하여 끌 수 있다
    * `icon` : Windows Exe 의 아이콘 파일을 지정한다
* 다음 명령어로 빌드한다
    ```
    (thenv)
    scgyong@scGyonG-PC MINGW64 /d/Develop/Thinkware/xian (main)
    $ pyinstaller main.spec
    ```
* 빌드 후 `dist/main.exe` 파일이 만들어지므로, 버전명 등을 적용하여 배포한다
