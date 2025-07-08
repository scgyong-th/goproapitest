# Test Framework 조사 07/08

## 조사 조전
- 테스트 케이스 작성 및 등록
- 등록 시 자동으로 일련번호(ID) 부여
- UI에서 그룹/카테고리/모델로 분류 가능
- UI에서 지정한 필터(모델/그룹) 기준으로 테스트 실행
- 테스트 결과는 리포트 형태로 확인 가능

## 조사 대상 목록
- Allure TestOps
- TestRail
- Xray (Jira Plugin)
- TestLink
- Zephyr Scale (Jira 기반)
- Katalon TestOps
- ReportPortal

## TestLink
- 장점: 무료 및 Open Source
- 단점
  - 조건 실행 Filter 없음
  - 결과 기반 자동 등록 없음
  - csv 는 TestSuite 단위로만 export 가능
  - 마지막 업데이트: 2018년 11월
  - PHP8 과 호환안됨, PHP7 는 지원 중단됨

## Allure TestOps
- 단점: 가격 ($39/월/사용자, Cloud 및 OnPremise 모두 지원)
- 장점
  - 테스트 결과 등록시 case 자동 생성
  - 새로 등록된 case 등 자동 파악
  - Section, Tag 등을 이용한 필터링 가능, 개별 case 선택 가능, Smart Suite 로 선택 도움
- 각 Test 단위를 Launch 로 부르며 Launch 단위를 csv export 할 수 있음
- 요구사항들을 대부분 충족

### Allure TestOps 선택시 시나리오
- 개발자가 Test Case 를 만듬
  - Test 는 Suite, Mark, 기능 등으로 분류되어 있음
- Test 결과를 allure report 로 만들어 TestOps 에 올림
- Test Case 목독 및 Suite/그룹 등 Filter 생성됨
- A 모델용 Launch 구성
  - BLE Marker 포함, API Set XX 포함, 특정파일의 특정테스트 포함
  - Launch 를 .csv 로 export
- A 모델 테스터
  - .csv 를 받아 Test Runner 에서 지정 (Runner 배포시 함께 배포)
  - 환경에 model= `A1234-Model` 등으로 설정
  - 테스트 결과를 전달
- 테스트 결과를 Allure TestOps 에 올리고 변화 감지
- B 모델용도 위와 같은 과정으로 처리
- TestOps UI 에서 다음 결과 확인 가능
  - 전체 테스트 결과 및 변화
  - 각 모델별 테스트 결과 추이
 
### 추후 개발 가능 연동
- Test Runner
  - Allure TestOps 에 접속하여 Launch 목록을 다운로드
  - Test 결과를 TestOps 에 자동 전송
