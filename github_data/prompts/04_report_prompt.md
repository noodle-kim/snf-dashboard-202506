# 📋 SNF 결산 리포트 - AI 인사이트 프롬프트

## 📋 개요
이 프롬프트는 대시보드의 **네 번째 페이지 "SNF 결산 리포트"**에 표시될 AI 인사이트를 생성합니다.

---

## 🎯 생성 목표
태그, 언어 지원, 커뮤니티 데이터를 종합 분석하여 **5개의 CSV 파일**을 생성합니다:
1. `01_checklist.csv` - SNF 준비 체크리스트 4개
2. `02_kpi_cards.csv` - 리포트 KPI 4개
3. `03_tags_analysis.csv` - 태그 분석 데이터
4. `04_language_support.csv` - 언어 지원 분석
5. `05_community.csv` - 커뮤니티 운영 분석

---

## 📊 입력 데이터 (raw/ 폴더)

| 파일명 | 내용 | 활용 |
|--------|------|------|
| `결산 페이지*.csv` | 게임별 태그, 언어, 커뮤니티, 업데이트 이력 | 전체 분석 |
| `가장 많이 플레이한 TOP50*.csv` | 장르, 체험판, 멀티플레이 | 보조 데이터 |

---

## 📝 프롬프트 1: 준비 체크리스트 (01_checklist.csv)

```
전체 데이터를 종합하여 **SNF 참가 준비 체크리스트 4개**를 만들어주세요.

### 출력 형식 (CSV):
id,icon,title,description,detail_items
1,🎮,{항목명},{한줄 설명},{세부항목1}|{세부항목2}|{세부항목3}|{세부항목4}
2,🌍,{항목명},{한줄 설명},{세부항목1}|{세부항목2}|{세부항목3}|{세부항목4}
3,💬,{항목명},{한줄 설명},{세부항목1}|{세부항목2}|{세부항목3}|{세부항목4}
4,👥,{항목명},{한줄 설명},{세부항목1}|{세부항목2}|{세부항목3}|{세부항목4}

### 필수 체크리스트 항목:
1. **체험판 준비** - TOP 10의 50%가 체험판 제공, 안정적 빌드 필수
2. **다국어 지원** - 최소 7개 언어, 중국어 간체 필수, 영어 100%
3. **커뮤니티 구축** - Discord + YouTube + X 필수 3종 세트
4. **멀티플레이어 고려** - TOP 10의 70%가 멀티, Co-op 효과 검증

### 작성 가이드:
- title: 간결한 카테고리명 (3~5단어)
- description: 왜 중요한지 한줄 설명
- detail_items: 파이프(|)로 구분된 4개 구체적 실행 항목
```

---

## 📝 프롬프트 2: KPI 카드 (02_kpi_cards.csv)

```
결산 데이터에서 **핵심 KPI 4개**를 추출해주세요.

### 출력 형식 (CSV):
id,icon,value,label,sublabel,highlight
1,🏷️,{값},{지표명},{부가설명},{강조텍스트}
2,🌍,{값},{지표명},{부가설명},{강조텍스트}
3,💬,{값},{지표명},{부가설명},{강조텍스트}
4,📊,{값},{지표명},{부가설명},{강조텍스트}

### 필수 KPI:
1. 평균 태그 수 (예: 18개)
2. 평균 언어 지원 수 (예: 7.8개 언어)
3. 평균 커뮤니티 채널 수 (예: 4.2개)
4. 중국어 간체 지원률 (예: 92%)
```

---

## 📝 프롬프트 3: 태그 분석 (03_tags_analysis.csv)

```
결산 페이지의 태그 데이터를 분석해주세요.

### 출력 형식 (CSV):
analysis_type,rank,tag_name,count,percentage,category
top_tags,1,{태그명},{사용게임수},{비율%},{카테고리}
top_tags,2,{태그명},{사용게임수},{비율%},{카테고리}
...
genre_required,액션RPG,{필수태그1}|{필수태그2}|{필수태그3}|{필수태그4},,
genre_required,슈팅,{필수태그1}|{필수태그2}|{필수태그3}|{필수태그4},,
genre_required,로그라이크,{필수태그1}|{필수태그2}|{필수태그3},,
tag_category,장르,{태그목록},,,
tag_category,플레이 스타일,{태그목록},,,
tag_category,테마,{태그목록},,,

### 분석 항목:
1. TOP 20 인기 태그 (사용 빈도순)
2. 장르별 필수 태그 추천
3. 태그 카테고리별 분포

### 태그 카테고리:
- 장르: Action, RPG, Roguelike, Horror, Simulation 등
- 플레이 스타일: Multiplayer, Singleplayer, Co-op, PvP 등
- 테마: Sci-fi, Fantasy, Horror, Anime 등
- 기타: Indie, Early Access, Free to Play 등
```

---

## 📝 프롬프트 4: 언어 지원 분석 (04_language_support.csv)

```
결산 페이지의 언어 지원 데이터를 분석해주세요.

### 출력 형식 (CSV):
support_type,rank,language,game_count,percentage,priority
voice,1,{언어명},{지원게임수},{비율%},{필수/권장/선택}
voice,2,{언어명},{지원게임수},{비율%},{필수/권장/선택}
interface,1,{언어명},{지원게임수},{비율%},{필수/권장/선택}
interface,2,{언어명},{지원게임수},{비율%},{필수/권장/선택}
subtitle,1,{언어명},{지원게임수},{비율%},{필수/권장/선택}
subtitle,2,{언어명},{지원게임수},{비율%},{필수/권장/선택}
strategy,인디,{언어목록},{최소개수},,
strategy,AA급,{언어목록},{최소개수},,
strategy,AAA급,{언어목록},{최소개수},,

### 분석 항목:
1. 음성 지원 TOP 5 언어
2. 인터페이스 언어 TOP 7
3. 자막 언어 TOP 7
4. 게임 규모별 언어 지원 전략

### 언어 우선순위:
- 필수: 영어(100%), 중국어 간체(92%)
- 권장: 한국어(70%), 일본어(68%), 중국어 번체(54%)
- 선택: 러시아어, 스페인어, 프랑스어, 독일어, 포르투갈어
```

---

## 📝 프롬프트 5: 커뮤니티 운영 분석 (05_community.csv)

```
결산 페이지의 커뮤니티 데이터를 분석해주세요.

### 출력 형식 (CSV):
analysis_type,platform,usage_rate,priority,region_target
channel_usage,Discord,{비율%},{필수/권장},{글로벌}
channel_usage,YouTube,{비율%},{필수/권장},{글로벌}
channel_usage,X,{비율%},{필수/권장},{글로벌/일본}
channel_usage,Reddit,{비율%},{권장},{북미/유럽}
channel_usage,bilibili,{비율%},{권장},{중국}
channel_usage,Weibo,{비율%},{권장},{중국}
region_strategy,글로벌,{채널목록},,
region_strategy,중국,{채널목록},,
region_strategy,한국,{채널목록},,
region_strategy,일본,{채널목록},,
timeline,준비단계,{활동목록},{시기},SNF 3개월 전
timeline,실행단계,{활동목록},{시기},SNF 기간 중
timeline,정리단계,{활동목록},{시기},SNF 종료 후

### 분석 항목:
1. 커뮤니티 채널별 운영률
2. 지역별 플랫폼 선호도
3. SNF 전후 커뮤니티 운영 타임라인
```

---

## 📤 출력 파일 목록

| 파일명 | 용도 | 대시보드 위치 |
|--------|------|--------------|
| `01_checklist.csv` | 체크리스트 4개 | Report - 상단 |
| `02_kpi_cards.csv` | KPI 4개 | Report - KPI 영역 |
| `03_tags_analysis.csv` | 태그 분석 | Report - 태그 탭 |
| `04_language_support.csv` | 언어 지원 | Report - 언어 탭 |
| `05_community.csv` | 커뮤니티 | Report - 커뮤니티 탭 |

---

## ✅ 출력 예시

### 01_checklist.csv
```csv
id,icon,title,description,detail_items
1,🎮,체험판 준비,TOP 10의 50%가 체험판 제공,1~2시간 플레이 분량|버그 없는 안정 빌드|SNF 2주 전 준비 완료|핵심 게임플레이 포함
2,🌍,다국어 지원,최소 7개 언어 중국어 간체 필수,영어 100% 필수|중국어 간체 92%|한국어 70% 권장|일본어 68% 고려
3,💬,커뮤니티 구축,Discord YouTube X 필수 3종,Discord 서버 운영|YouTube 채널 활성화|X 계정 주기적 업데이트|Dev Log 주 1회 이상
4,👥,멀티플레이 고려,TOP 10의 70%가 멀티 지원,Co-op 모드 바이럴 효과|친구 초대 시스템|싱글이면 리더보드 추가|스트리머 협업 용이
```

### 02_kpi_cards.csv
```csv
id,icon,value,label,sublabel,highlight
1,🏷️,18개,평균 태그 수,TOP 10 기준,Action 태그 90%
2,🌍,7.8개,평균 언어 수,인터페이스 기준,중국어 간체 필수
3,💬,4.2개,커뮤니티 채널,평균,Discord/YouTube/X 필수
4,📊,92%,중국어 지원률,간체 기준,최대 시장
```

### 03_tags_analysis.csv
```csv
analysis_type,rank,tag_name,count,percentage,category
top_tags,1,Action,45,90%,장르
top_tags,2,Multiplayer,27,54%,플레이 스타일
top_tags,3,Singleplayer,35,70%,플레이 스타일
top_tags,4,RPG,22,44%,장르
top_tags,5,Indie,40,80%,기타
genre_required,액션RPG,Action|RPG|Combat|Story Rich,,
genre_required,슈팅,FPS|Shooter|Multiplayer|PvP,,
genre_required,로그라이크,Roguelike|Procedural|Difficult,,
```

### 04_language_support.csv
```csv
support_type,rank,language,game_count,percentage,priority
interface,1,영어,50,100%,필수
interface,2,중국어 간체,46,92%,필수
interface,3,한국어,35,70%,권장
interface,4,일본어,34,68%,권장
interface,5,중국어 번체,27,54%,권장
interface,6,러시아어,28,56%,선택
interface,7,프랑스어,26,52%,선택
strategy,인디,영어+중국어+한국어,3,,
strategy,AA급,영어+중국어+한국어+일본어+러시아어,5,,
strategy,AAA급,10개 이상 다국어,10,,
```

### 05_community.csv
```csv
analysis_type,platform,usage_rate,priority,region_target
channel_usage,Discord,90%,필수,글로벌
channel_usage,YouTube,85%,필수,글로벌
channel_usage,X,80%,필수,글로벌/일본
channel_usage,Reddit,45%,권장,북미/유럽
channel_usage,bilibili,30%,권장,중국
channel_usage,Weibo,25%,권장,중국
region_strategy,글로벌,Discord|YouTube|X|Reddit,,
region_strategy,중국,Discord|bilibili|Weibo|TikTok,,
region_strategy,한국,Discord|YouTube|네이버|인벤,,
region_strategy,일본,Discord|YouTube|X,,
timeline,준비단계,Discord 서버 오픈|YouTube 채널 생성|X 계정 활동|Dev Log 시작,SNF 3개월 전,
timeline,실행단계,실시간 Q&A 스트리밍|핫픽스 즉시 공지|피드백 수집|매일 커뮤니티 확인,SNF 기간 중,
timeline,정리단계,설문조사 진행|개선 로드맵 공개|지속적 소통|출시일 확정 발표,SNF 종료 후,
```

---

## 🔄 갱신 주기
- SNF **종료 후 1회** 최종 결산용
- 또는 SNF 기간 중 **Day 3, Day 5** 중간 점검용
