# Test Framework 실행 방법

## 실행 준비
* Android Phone
  * `agw` 설치해 둘 것
  * 개발자 모드를 활성화해 두는 것이 좋음
    * 충전 중에 화면이 꺼지지 않도록 하면 더 좋음
* GoPro 또는 이에 준하는 Device
* Windows PC
  * Test Runner 를 다운로드받아 파일 이름을 `main.ex_` 에서 `main.exe` 로 변경
    * 한 번 실행하면 같은 폴더에 test_config.json 이 생성됨. 
  * Android Platform Tools 설치
  * test_config.json 의 `"adb"` 부분에 PC 에 설치된 `adb` 의 경로를 넣고 저장
 
## Bluetooth 연결
* GoPro 기기를 Pairing 준비 상태에 둠
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
* `adb devices` 로 연결된 Phone 의 정보가 나오면 정상

## Runner 실행
* `main.exe` 실행.
   * <img width="300" alt="image" src="https://github.com/user-attachments/assets/6572c8dc-dea3-4bbf-9fdd-2d7043296cdf" />
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
