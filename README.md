# ScrapeStackInfo

- 특정 기업의 주식을 평가하기 위한 데이터를 자동으로 스크랩하는 프로젝트



**Update history**

- 온라인 기업정보 http://companyinfo.stock.naver.com/company/c1010001.aspx?cmp_cd=005930&cn= 에서 필요한 정보 가져오기

- 크롬 개발자도구를 통해 데이터를 가져오는 api추출 후 GET 요청 응답 받아서 파싱

  - 매출액 the total sales - Done
  - 영업이익 business profits - Done
  - 3년 당기순이익 current income - Done
  - 시가총액 market capitalization - Done
  - 3년 시가배당률 현금배당수률 dividend rate - Done
  - PBR - Done
  - 부채비율 Debt ratio - Done
  - 유보율 reverseratio - Done
  - 당좌비율 quick ratio - Done
  - 매출채권회전율 Receivables Turnover Ratio - Done
  - 재고자산 회전율 inventory Turnover - Done

  

**To-do-list**

- DB 컬럼 추가해서 데이터 삽입
- 코스피 200 항복 검색해서 DB 채우기

