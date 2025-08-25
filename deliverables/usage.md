# Test Framework 실행 방법

## 실행 준비
* Android Phone
  * `agw` 설치해 둘 것
   * 방법 1: Binary Release Folder 를 Android Phone 에서 열고 .APK 파일 링크를 열어 직접 설치
   * 방법 2: 아래 adb 설치 후 adb 를 이용하여 설치
    * `adb` 가 `c:/Users/scgyong/AppData/Local/Android/Sdk/platform-tools/adb` 에 설치되어 있고
    * app-release.apk 가 현재 폴더에 다운로드되어 있다고 가정하면 다음과 같이 `adb install` 명령어를 사용하여 설치 가능
      ```
       C:\Users\scgyong\Downloads>c:/Users/scgyong/AppData/Local/Android/Sdk/platform-tools/adb install app-release.apk
       C:\Users\scgyong\Downloads>
      ```
  * 설치 후 폰의 `설정`-`애플리케이션`-`XianGatewayPilot`-`권한` 으로 들어가서 위치 포함 모든 권한이 허용으로 되어 있도록 조정.
  * 개발자 모드를 활성화해 두는 것이 좋음
    * `개발자 모드`는 `설정`-`휴대전화 정보`-`소프트웨어 정보` 에 들어가서 `빌드 넘버` 를 7번 터치하면 활성화됨
    * 충전 중에 화면이 꺼지지 않도록 하면 더 좋음
* GoPro 또는 이에 준하는 Device
* Windows PC
  * Test Runner 를 다운로드받아 파일 이름을 `main.ex_` 에서 `main.exe` 로 변경
    * 한 번 실행하면 같은 폴더에 test_config.json 이 생성됨. 
  * Android Platform Tools 설치
  * test_config.json 의 `"adb"` 부분에 PC 에 설치된 `adb` 의 경로를 넣고 저장
 
## Bluetooth 연결
* GoPro 기기를 Pairing 준비 상태에 둠
 * 화면을 아래로 쓸어내려 `메뉴`가 나오게 함
  * 초기화
   * `메뉴` 에서 오른쪽으로 이동하여 `기본 설정` 진입
   * `무선 연결` - `연결 초기화` 로 기존 연결 삭제
  * `메뉴` 에서 `+페어링` 버튼을 눌러 Pairing 준비 상태로 진입
* `agw` 를 실행시킨 뒤 `Scan` 을 하고 해당 디바이스가 나오면 `Connect`
  * 잘 연결된 후에는
    * `Device: { "modelNumber": "HERO13 Black", ... ` 등의 정보가 화면에 표시됨
    * 3초마다 Keep Alive BLE 시간이 표시됨
    * WiFi AP Mode 를 enable 시켜주고 (화면에 표시됨) Phone 을 Camera 의 WiFi 에 접속시킴
      * 기기에 따라 최초 연결시 연결을 허가하겠냐는 질문이 나올 수 있음.
  * 연결을 한번만 하면 다음부터는 Scan 을 할 필요가 없으며 바로 Connect 를 할 수 있음
    * 앱 실행이나 Connect 도 Runner 가 요청하기 때문에 화면을 조작할 일이 별로 

## PC-AGW 연결
* USB-Data 케이블을 사용하여 Windows PC 와 Android Phone 을 연결. (충전 케이블로는 안됨)
* USB Driver Software 를 설치해 두어야 함
  * 삼성 폰인 경우: https://developer.samsung.com/android-usb-driver
  * 기타 폰의 경우 구글 드라이버 혹은 제조사 안내 확인 필요
    * 구글 드라이버: https://developer.android.com/studio/run/win-usb?hl=ko
* 연결 후 Android Phone 에서 연결 허용을 묻는 질문에 `허용` 을 선택해야 하며, MTP 모드가 활성화되어야 함 (미디어 전송 프로토콜, 파일 전송/MPT)
* Windows `내PC` 에 Android 가 나오고 파일 목록이 보이더라도 USB Driver 가 설치되지 않으면 `adb` 연결이 실패할 수도 있음
* `adb devices` 로 연결된 Phone 의 정보가 나오면 정상
 * `adb` 가 PATH 에 잡혀 있지 않으면 상단의 설명처럼 full path 로 적어야 할 수도 있음

## Runner 실행
* `xian.0.4.exe` 실행.
   * <img width="300" alt="image" src="https://github.com/user-attachments/assets/6572c8dc-dea3-4bbf-9fdd-2d7043296cdf" />
   * 최초 실행시 Windows Defender 등에 의해 실행을 허용할지 여부를 물을수 있음. 
* `adb` 설정이 제대로 되었다면 `Android:` 부분에 Serial Number 및 Model Name 이 표시됨
  * 설정이 제대로 되지 않았거나 연결되지 않았다면 `Device Not Found` 가 나옴
* `App` 부분에 AGW App 에 대한 정보가 나옴. 안 나온다면 `Android` 오른쪽의 `Connect` 버튼을 눌러 재시도해볼 수 있음
  * `"connected"` 부분이 `"false"` 로 나온다면 `Cam:` 항목에 카메라로부터 받은 정보가 나옴. 
  * Android 기기상에서 `agw` 를 kill 시켰을 경우에도 위의 `Connect` 를 누르면 폰 상에서 앱이 실행됨.
* `Cam:` 항목에 접속시 받아온 정보가 표시됨. 이 정보는 `agw` 화면상에 나타나는 정보와 같음.
  * 카메라가 꺼졌거나 연결을 잃은 경우 아래쪽의 `Connect` 를 눌러 앱이 카메라에 재접속하도록 할 수 있음
  * 연결되고 나면 Phone 에서 계속 Keep Alive 메시지를 보내기 때문에 앱을 종료하지 않는한 연결은 끊어지지 않음.
 
## Test 실행
* `Start Test` 버튼을 눌러 모든 테스트케이스들을 실행시킴
* 진행 과정은 Progress Bar 및 하단 Test Log 에 표시됨.
* 성공한 테스트는 `.` 으로 표시되며 실패한 테스트는 `F` 로 표시됨
* 결과는 `results/report.html` 에 저장되며 Progress 오른쪽의 `Report` 버튼을 누르면 시스템 브라우저를 사용하여 해당 파일이 열림.
