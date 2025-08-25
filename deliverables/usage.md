# Test Framework 실행 방법

![GitHub tag (latest)](https://img.shields.io/github/v/tag/scgyong-th/goproapitest)

## 실행 준비

### Binary Download
* Binary Folder 로부터 파일들을 다운로드해 둔다. `C:/Users/think/xian` 에 다운로드해 두었다고 가정해 본다
  * `xian.0.4.ex_` : Windows Runner. 다운로드 후 확장자를 `.exe` 로 변경한다
  * `app-release.apk` : Android Binary. Phone 에서 직접 다운로드받아 설치할 수도 있지만 후술할 `adb` 이용 방법도 이용 가능하다
* ADB (Android Platform Tools)
  * Android Studio 가 설치되어 있다면 다음과 유사한 곳에 이미 adb 가 존재한다
    * `c:/Users/scgyong/AppData/Local/Android/Sdk/platform-tools/adb`
  * Android Studio 가 없다면 다음 링크에서 다운로드 받는다
    * https://developer.android.com/tools/releases/platform-tools
    * 다운로드 받아 `C:/Users/think/xian/platform-tools/` 에 압축해제 해 두었다고 가정한다
  * 이하 문서에서 `adb` 의 언급은 위 설치 혹은 다운로드된 것을 가리키므로, path 에 추가하거나 full path 로 명령어를 작성한다

### Android Phone
* 개발자 모드를 활성화해 두어야 한다
  * `개발자 모드`는 `설정`-`휴대전화 정보`-`소프트웨어 정보` 에 들어가서 `빌드 넘버` 를 7번 터치하면 활성화됨
  * 충전 중에 화면이 꺼지지 않도록 하면 더 좋음
* USB-Data 케이블을 사용하여 Windows PC 와 Android Phone 을 연결. (충전 케이블로는 안됨)
* USB Driver Software 를 설치해 두어야 함
  * 삼성 폰인 경우: https://developer.samsung.com/android-usb-driver
  * 기타 폰의 경우 구글 드라이버 혹은 제조사 안내 확인 필요
    * 구글 드라이버: https://developer.android.com/studio/run/win-usb?hl=ko
  * Windows `내PC` 에 Android 가 나오고 파일 목록이 보이더라도 USB Driver 가 설치되지 않으면 `adb` 연결이 실패할 수도 있음
* 연결 후 Android Phone 에서 연결 허용을 묻는 질문에 `허용` 을 선택해야 하며, MTP 모드가 활성화되어야 함 (미디어 전송 프로토콜, 파일 전송/MPT)
* 개발자 모드가 잘 활성화 되었다면 PC 연결시 디버깅을 허용하겠느냐는 질문도 나오며, 허용해야 한다.
  * `이 컴퓨터에서 항상 적용` 을 켜 두면 좋다
* `adb devices` 명령에 디바이스가 목록에 나와야 한다

### AGW 설치
* `adb` 를 이용하여 다음과 같이 설치한다
    ```
    C:\Users\think\xian>C:/Users/think/xian/platform-tools/adb install app-release.apk
    C:\Users\think\xian>
    ```
* 설치 후 폰의 `설정`-`애플리케이션`-`XianGatewayPilot`-`권한` 으로 들어가서 모든 권한이 허용으로 되어 있도록 조정.
  * 근처 기기 검색 허용
  * 위치 허용
  * 거부된 권한이 없어야 함

### Bluetooth 연결
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
  * 앱 실행이나 Connect 도 Runner 가 요청하기 때문에 화면을 조작할 일이 별로 없음

### test_config.json 생성
* Runner (`xian.0.4.exe`) 을 처음 실행시키면 `test_config.json` 파일이 생성된다. 생성되면 프로그램은 바로 종료시킨다
* 생성된 파일 내의 `adb` 항목을 PC 에 설치된 위치로 수정한다
  * Android Studio 와 함께 설치된 경우 다음과 유사: `c:/Users/scgyong/AppData/Local/Android/Sdk/platform-tools/adb`
  * 위의 방법대로 다운로드한 경우 다음과 유사: `C:/Users/think/xian/platform-tools/adb`
* 폴더 구분은 `\` 로 해도 되지만 원 `₩` 기호로 표시되는 경우가 많으므로 `/` 를 권장한다


## Runner 

### Runner 실행

* `xian.0.4.exe` 실행.
   * <img width="300" alt="image" src="https://github.com/user-attachments/assets/6572c8dc-dea3-4bbf-9fdd-2d7043296cdf" />
   * 최초 실행시 Windows Defender 등에 의해 실행을 허용할지 여부를 물을수 있음.
     * `SmartScreen 에서 인식할 수 없는 앱의 시작을 차단했습니다` 와 같은 메시지가 나오면 `추가 정보` 를 클릭하면 나타나는 `실행` 버튼을 누른다
     * 한 번만 허용하면 이후에는 나오지 않는다
* `test_config.json` 에 `adb` 설정이 제대로 되었다면 `Android:` 부분에 Serial Number 및 Model Name 이 표시됨
  * 설정이 제대로 되지 않았거나 연결되지 않았다면 `Device Not Found` 가 나옴
* `App` 부분에 AGW App 에 대한 정보가 나옴. 안 나온다면 `Android` 오른쪽의 `Connect` 버튼을 눌러 재시도해볼 수 있음
  * `"connected"` 부분이 `"true"` 로 나온다면 `Cam:` 항목에 카메라로부터 받은 정보가 나옴. 
  * Android 기기상에서 `agw` 를 kill 시켰을 경우에도 위의 `Connect` 를 누르면 폰 상에서 앱이 실행됨.
* `Cam:` 항목에 접속시 받아온 정보가 표시됨. 이 정보는 `agw` 화면상에 나타나는 정보와 같음.
  * 카메라가 꺼졌거나 연결을 잃은 경우 아래쪽의 `Connect` 를 눌러 앱이 카메라에 재접속하도록 할 수 있음
  * 연결되고 나면 Phone 에서 계속 Keep Alive 메시지를 보내기 때문에 앱을 종료하지 않는한 연결은 끊어지지 않음.
 
### Test 실행
* `Start Test` 버튼을 눌러 모든 테스트케이스들을 실행시킴
* 진행 과정은 Progress Bar 및 하단 Test Log 에 표시됨.
* 성공한 테스트는 `.` 으로 표시되며 실패한 테스트는 `F` 로 표시됨
* 결과는 `results/report.html` 에 저장되며 Progress 오른쪽의 `Report` 버튼을 누르면 시스템 브라우저를 사용하여 해당 파일이 열림.
