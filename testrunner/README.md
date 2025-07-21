# `pytest` Test Runner

## Prerequisites

- Allure
  - `pip install allure-pytest`
  - ✅ mac
    - `brew install allure`
  - ✅ Windows
    - `https://docs.qameta.io/allure/` 에서 ZIP 다운로드
    - bin 경로를 PATH에 추가
- `pytest-html`
  - Allure 는 다음 과정을 거쳐야 해서 개발 중에 간단히 테스트하기에는 부적합.
    - pytest 를 실행하며 result 를 생성
    - result 를 report 로 변환 (`generate`)
    - `allure open` 을 통해 Web Server 동작시키고 Browser 로 보기
  - 다음 명령어 실행
    - `PYTHONPATH=. pytest --html=results/report.html`
  - 결과는 다음을 브라우저에서 열면 됨 (macOS 기준)
    - `open results/report.html`

  - 
## Running `pytest`
- `pytest` 실행

  - `PYTHONPATH=. pytest --alluredir=results/res_250719_0422/`
    - `camera` module 을 import 하기 위해서는 현재 폴더 (`.`) 가 path 에 추가되어야 한다.
  - `pytest` 를 실행하며 `*.json` 파일을 남김
  - 결과를 저장하는 폴더에 날짜/시각 을 적기로 결정
- Result 로부터 Report 생성
  - `allure generate results/res_250719_0422/ --clean -o results/res_250719_0422_report`
- Browser 에서 Report 열기
  - `allure open results/res_250719_0422_report/`
  - allure 가 web server 로 동작하며 browser 가 열림
    - `Ctrl+C` 로 서버 중지
  - 다음 메뉴들을 볼 수 있음
    - Overview
    - Categories
    - Suites
    - Graphs
    - Timeline
    - Behaviors
    - Packages
  - 이전 Report 와의 비교 등은 Allure TestOps (유료) 버전에서만 가능
    - 현재 보고 있는 Report 에 대해서만 나옴
