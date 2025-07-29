# GoPro API List

## Summary

### BLE
* 7/25 까지 구현 완료된 항목
  * BLE Handshake 및 초기 메시지
  * Read
    * `WiFi SSID`
    * `WiFi Password`
  * Commands
    * `GetHardwareInfo`
    * `GetDateTime`
    * `SetApControl`
  * Settings
    * `Keep Alive`
  * Query
    * `Get Status Values` - 자동 생성
    * `Get Setting Values` - 자동 생성
* 8/1 까지 완료할 항목
  * BLE Setup
    * Finish Paring
    * Set Paring State
  * Control
    * Set Date Time, Set Local Date Time 등 비교적 간단한 Setter
  * Query
    * 비교적 간단한 Getter
    * `Get Setting Capability`
  * Set Setting
    * 40여개 SettingId 에 대하여 자동 Setter 자동 생성 Script 작성
* 이번 구현에 어려운 항목들
  * 자동화하기 어려운 테스트
    * Reboot, Sleep 등
  * 시간이 필요하거나 사용자가 개입되어야 하는 테스트
    * 변화 감지 Register/Unregister
  * 시간관계상 어려운 테스트
    * COHN (AP 에 접속하는 기능) 관련
    * Live Streaming 관련
    * Hilight 관련 (녹화중에만 가능)
    * Preset 관련

### HTTP
* 간단한 Getter 들에 대하여 Request/Response 중계하는 기능만 구현
  * Status Getter test case 만 추가

## GoPro BLE API
* 출처
  * https://gopro.github.io/OpenGoPro/ble/protocol.html

### Protocol
* **BLE Setup** -> `AGW 에 구현 완료`
  * Pairing Mode 
  * Advertisements
  * Finish Pairing -> ✅ 구현 예정
  * Configure GATT Characteristics
  * GoPro Setup
* **Data Protocol** -> 🆗 일부 `AGW` 에 구현 / Runner Module 로 구현 완료
  * Packetization
  * Decipher Message Payload Type
  * Message Payload
* State Management -> AGW 에 일부 구현. Test case 추후 추가 필요
  * Camera Readiness
  * **Keep Alive** -> 🆗 `AGW`
  * Camera Control
 
### Control
* **Keep Alive** -> 🆗 `AGW` 에 구현 완료. Test Case 추가 필요
* Reboot the Camera -> ⚠️ Test 어려움
* Set Analytics -> ⚠️ Third-party Analytic Tracking 에 대한 설명 부족
* **Set AP Control** -> 🆗 `AGW` 에 구현. Set On 후 Wi-fi 접속까지 성공.
* Set Camera Control -> ⚠️ Camera 화면 확인 필요
* Set Date Time -> ✅ 구현 예정
* Set Local Date Time -> ✅ 구현 예정
* Set Pairing State -> ✅ `AGP` 에 구현 예정
* Set Shutter -> ✅ 구현 예정
* Set Turbo Transfer -> ⚠️ Camera 화면 확인 필요
* Sleep -> ⚠️ Test 어려움

### Query
* **Get Date Time** -> 🆗 Test Case 구현 완료.
* **Get Hardware Info** -> 🆗 Test Case 구현 완료.
* Get Local Date Time -> ✅ 구현 예정
* Get Last Captured Media -> ✅ 구현 예정
* Get Open GoPro Version -> ✅ 구현 예정
* **Get Setting Values** -> 🆗 Test Case 자동 생성 완료. (47종)
* **Get Status Values** -> 🆗 Test Case 자동 생성 완료. (61종)
* Get Setting Capabilities -> ✅ 자동 생성 구현 예정
* ⚠️ Test 어려운 항목들
  * Register for Setting Value Updates
  * Register for Status Value Updates
  * Register for Setting Capability Updates
  * Unregister for Setting Value Updates
  * Unregister for Status Value Updates
  * Unregister for Setting Capability Updates

### Access Point -> ⚠️ Test 어려움
* Scan for Access Points
* Get AP Scan Results
* Connect to Provisioned Access Point
* Connect to a New Access Point
* Disconnect from Access Point

### Live Streaming -> ⚠️ Test 어려움
* Metadata
* Set Livestream Mode
* Get Livestream Status

### Camera on the Home Network -> ⚠️ Test 어려움
* Verifying Certificate
* View Certificate Details
* Provisioning Procedure
* Clear COHN Certificate
* Create COHN Certificate
* Get COHN Certificate
* Get COHN Status
* Set COHN Setting

### Hilights
* Hilight Moment -> ⚠️ Test 어려움. Encoding 중에만 할 수 있음

### Presets -> ⚠️ Test 어려움. 
* Get Available Presets
* Load Preset
* Load Preset Group
* Update Custom Preset

### Settings -> ✅ 구현 예정
* Set Setting -> ✅ 구현 예정
  * **Getter (Query)** 는 🆗 Test Case 자동 생성 완료. (47종)
  * 가능한 값들로 변경하고 변경 된 값 확인
  * 불가능한 값들 넘겨주고 결과 확인
  * 하위 항목이 없는 값들은 위와 같이 확인
* Video Resolution (2)
* Frames Per Second (3)
* Video Timelapse Rate (5)
* Photo Timelapse Rate (30)
* Nightlapse Rate (32)
* Webcam Digital Lenses (43)
* Auto Power Down (59)
* GPS (83)
* LCD Brightness (88) ⚠️
  * 10~100 까지 설정
* LED (91)
* Video Aspect Ratio (108)
* Video Lens (121)
* Photo Lens (122)
* Time Lapse Digital Lenses (123)
* Photo Output (125)
* Media Format (128)
* Anti-Flicker (134)
* Hypersmooth (135)
* ~~Video Horizon Leveling (150)~~ 🔐 Hero13 미지원
* ~~Photo Horizon Leveling (151)~~ 🔐 Hero13 미지원
* Video Duration (156)
* Multi Shot Duration (157)
* ~~Max Lens (162)~~ 🔐 Hero13 미지원
* HindSight (167)
* Scheduled Capture (168)
* Photo Single Interval (171)
* Photo Interval Duration (172)
* ~~Video Performance Mode (173)~~ 🔐 Hero13 미지원
* Control Mode (175)
* Easy Mode Speed (176)
  * Mode 가 100 여개 있음 😓
* ~~Enable Night Photo (177)~~ 🔐 Hero13 미지원
* Wireless Band (178)
* Star Trails Length (179)
* System Video Mode (180)
* Video Bit Rate (182)
* Bit Depth (183)
* Profiles (184)
* Video Easy Mode (186)
* Lapse Mode (187)
* Max Lens Mod (189)
* ~~Max Lens Mod Enable (190)~~ 🔐 Hero13 미지원
* Easy Night Photo (191)
* Multi Shot Aspect Ratio (192)
* Framing (193)
* Camera Volume (216)
* Setup Screen Saver (219)
* Setup Language (223)
* Photo Mode (227)
* Video Framing (232)
* Multi Shot Framing (233)
* Frame Rate (234)

### Statuses
* 🆗 Test Case 자동 생성 완료. (61종)
  * 가능한 값 중 하나가 들어있는지 확인하도록만 구현 완료

* Battery Present (1)
* Internal Battery Bars (2)
* Overheating (6)
* Busy (8)
* Quick Capture (9)
* Encoding (10)
* LCD Lock (11)
* Video Encoding Duration (13)
* Wireless Connections Enabled (17)
* Pairing State (19)
* Last Pairing Type (20)
* ~~Last Pairing Success (21)~~ 🔐 Hero13 미지원
* Wifi Scan State (22)
* Last Wifi Scan Success (23)
* Wifi Provisioning State (24)
* ~~Remote Version (26)~~ 🔐 Hero13 미지원
* Remote Connected (27)
* ~~Pairing State (Legacy) (28)~~ 🔐 Hero13 미지원
* Connected WiFi SSID (29)
* Access Point SSID (30)
* Connected Devices (31)
* ~~Preview Stream (32)~~ 🔐 Hero13 미지원
* Primary Storage (33)
* Remaining Photos (34)
* Remaining Video Time (35)
* Photos (38)
* Videos (39)
* OTA (41)
* Pending FW Update Cancel (42)
* Locate (45)
* Timelapse Interval Countdown (49)
* SD Card Remaining (54)
* Preview Stream Available (55)
* Wifi Bars (56)
* Active Hilights (58)
* Time Since Last Hilight (59)
* Minimum Status Poll Period (60)
* Liveview Exposure Select Mode (65)
* Liveview Y (66)
* Liveview X (67)
* GPS Lock (68)
* AP Mode (69)
* Internal Battery Percentage (70)
* Microphone Accessory (74)
* Zoom Level (75)
* Wireless Band (76)
* Zoom Available (77)
* ~~Mobile Friendly (78)~~ 🔐 Hero13 미지원
* ~~FTU (79)~~ 🔐 Hero13 미지원
* 5GHZ Available (81)
* Ready (82)
* OTA Charged (83)
* Cold (85)
* Rotation (86)
* Zoom while Encoding (88)
* Flatmode (89)
* Video Preset (93)
* Photo Preset (94)
* Timelapse Preset (95)
* Preset Group (96)
* Preset (97)
* Preset Modified (98)
* ~~Remaining Live Bursts (99)~~ 🔐 Hero13 미지원
* ~~Live Bursts (100)~~ 🔐 Hero13 미지원
* Capture Delay Active (101)
* Media Mod State (102)
* Time Warp Speed (103)
* ~~Linux Core (104)~~ 🔐 Hero13 미지원
* ~~Lens Type (105)~~ 🔐 Hero13 미지원
* Hindsight (106)
* Scheduled Capture Preset ID (107)
* Scheduled Capture (108)
* Display Mod Status (110)
* SD Card Write Speed Error (111)
* SD Card Errors (112)
* Turbo Transfer (113)
* Camera Control ID (114)
* USB Connected (115)
* USB Controlled (116)
* SD Card Capacity (117)
* Photo Interval Capture Count (118)
