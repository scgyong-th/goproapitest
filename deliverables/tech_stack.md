# Technology Stack

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
