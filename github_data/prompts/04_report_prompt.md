# 📋 SNF 결산 리포트 - AI 인사이트 프롬프트 v2.1

## 📋 개요
이 프롬프트는 대시보드의 **네 번째 페이지 "SNF 결산 리포트"**에 표시될 AI 인사이트를 생성합니다.

---

## ⚠️ 중요: CSV 포맷 규칙

### 필수 준수 사항
1. **숫자에 쉼표 금지**: `716572` (O) / `716,572` (X)
2. **큰 숫자는 K/M 단위 사용**: `+70.7K`
3. **퍼센트는 % 포함**: `92%`
4. **파이프(|) 구분자**: 여러 항목은 파이프로 구분
5. **빈 값은 빈 문자열**: `,,`

### 금지 사항
- 셀 내 쉼표 사용
- value 필드에 쉼표 포함 금지

---

## 🎯 생성 목표

| # | 파일명 | 용도 | 동적화 |
|---|--------|------|--------|
| 1 | `01_checklist.csv` | SNF 준비 체크리스트 4개 | ✅ |
| 2 | `02_kpi_cards.csv` | 리포트 KPI 4개 | ✅ |
| 3 | `03_tab_insights.csv` | 각 탭별 insight-box 텍스트 | ✅ **신규** |
| 4 | `03_tags_analysis.csv` | 태그 분석 (TOP 20 태그만) | ✅ |
| 5 | `04_language_support.csv` | 언어 지원 (인터페이스 언어만) | ✅ |
| 6 | `05_community.csv` | 커뮤니티 (채널별 운영률만) | ✅ |

### 🔒 유지 영역 (동적화 하지 않음 - 가이드성 콘텐츠)
- **장르별 필수 태그 추천**: 액션/RPG, 슈팅, 로그라이크별 태그 목록
- **필수 언어 5종 / 전략 포인트**: 언어 지원 전략 가이드
- **지역별 플랫폼 선호도**: 북미/유럽, 동아시아, 한국, 일본별 플랫폼
- **SNF 전후 커뮤니티 타임라인**: 준비/실행/정리 단계별 활동

---

## 📊 입력 데이터 (raw/ 폴더)

| 파일명 | 내용 | 활용 |
|--------|------|------|
| `결산 페이지*.csv` | 게임별 태그/언어/커뮤니티/업데이트 | 전체 분석 |
| `가장 많이 플레이한 TOP50*.csv` | 장르/체험판/멀티플레이 | 보조 데이터 |

---

## 📝 CSV 1: 준비 체크리스트 (01_checklist.csv)

### 스키마
```csv
id,icon,title,description,detail_items
```

### 컬럼 설명
| 컬럼 | 타입 | 설명 | 예시 |
|------|------|------|------|
| id | 숫자 | 순번 1-4 | `1` |
| icon | 이모지 | 체크 아이콘 | `🎮` |
| title | 문자열 | 항목명 (10자 이내) | `체험판 준비` |
| description | 문자열 | 한줄 설명 (20자 이내) | `TOP 10의 50%가 체험판 제공` |
| detail_items | 파이프 구분 | 4개 세부항목 | `항목1\|항목2\|항목3\|항목4` |

### 출력 예시
```csv
id,icon,title,description,detail_items
1,🎮,체험판 준비,TOP 10의 50%가 체험판 제공,1~2시간 플레이 분량|버그 없는 안정 빌드|SNF 2주 전 준비 완료|핵심 게임플레이 포함
2,🌍,다국어 지원,최소 7개 언어 중국어 간체 필수,영어 100% 필수|중국어 간체 92%|한국어 70% 권장|일본어 68% 고려
3,💬,커뮤니티 구축,Discord YouTube X 필수 3종,Discord 서버 운영|YouTube 채널 활성화|X 계정 주기적 업데이트|Dev Log 주 1회 이상
4,👥,멀티플레이 고려,TOP 10의 70%가 멀티 지원,Co-op 모드 바이럴 효과|친구 초대 시스템|싱글이면 리더보드 추가|스트리머 협업 용이
```

---

## 📝 CSV 2: KPI 카드 (02_kpi_cards.csv)

### 스키마
```csv
id,icon,value,label,sublabel,highlight
```

### 컬럼 설명
| 컬럼 | 타입 | 설명 | 예시 |
|------|------|------|------|
| id | 숫자 | 순번 1-4 | `1` |
| icon | 이모지 | KPI 아이콘 | `🏷️` |
| value | 문자열 | 핵심 수치 (**쉼표 금지**) | `2600개` |
| label | 문자열 | 지표명 | `참가 게임 수` |
| sublabel | 문자열 | 부가 설명 | `2025년 6월` |
| highlight | 문자열 | 강조 텍스트 | `▲ +16% (전년 대비)` |

### 출력 예시
```csv
id,icon,value,label,sublabel,highlight
1,🎮,2600개,참가 게임 수,2025년 6월,▲ +16% (전년 대비)
2,🏷️,18개,게임당 태그 수,평균,TOP 10 기준
3,🌍,7.8개,평균 언어 지원,인터페이스,자막은 평균 8.2개
4,📣,4.2개,커뮤니티 채널 수,평균,Discord/YouTube/X 필수
```

---

## 📝 CSV 3: 각 탭별 insight-box (03_tab_insights.csv) **신규**

### 스키마
```csv
id,tab_name,insight_text
```

### 용도
- 각 탭(태그/언어/커뮤니티)의 상단 insight-box 텍스트
- 하드코딩된 `💡 핵심 발견:` 텍스트를 동적으로 변경

### 컬럼 설명
| 컬럼 | 타입 | 설명 | 예시 |
|------|------|------|------|
| id | 숫자 | 순번 1-3 | `1` |
| tab_name | 문자열 | 탭 식별자 | `tags` / `languages` / `community` |
| insight_text | 문자열 | 인사이트 텍스트 (80-120자) | `TOP 10 게임의 90%가...` |

### 출력 예시
```csv
id,tab_name,insight_text
1,tags,TOP 10 게임의 90%가 Action 태그를 사용하고 있습니다. 평균 18개의 태그를 활용하며 Multiplayer Singleplayer RPG 태그가 가장 빈번하게 등장했습니다.
2,languages,영어는 100% 필수이며 중국어 간체 지원률이 92%로 압도적입니다. 음성 지원은 42%만 제공하지만 인터페이스와 자막은 평균 7~8개 언어를 지원합니다.
3,community,TOP 게임들은 평균 4.2개의 커뮤니티 채널을 운영합니다. Discord(90%) YouTube(85%) X(80%)가 필수 3종 세트이며 주 2회 이상 업데이트하는 게임이 차트 상위권을 차지했습니다.
```

---

## 📝 CSV 4: 태그 분석 (03_tags_analysis.csv)

### 스키마
```csv
analysis_type,rank,tag_name,count,percentage
```

### 용도
- TOP 20 인기 태그 데이터만 (태그 차트용)
- 장르별 필수 태그는 가이드로 유지

### 컬럼 설명
| 컬럼 | 타입 | 설명 | 예시 |
|------|------|------|------|
| analysis_type | 문자열 | 분석 타입 | `top_tags` |
| rank | 숫자 | 순위 1-20 | `1` |
| tag_name | 문자열 | 태그명 | `Action` |
| count | 숫자 | 사용 게임 수 | `45` |
| percentage | 문자열 | 비율 | `90%` |

### 출력 예시
```csv
analysis_type,rank,tag_name,count,percentage
top_tags,1,Action,45,90%
top_tags,2,Multiplayer,27,54%
top_tags,3,Singleplayer,35,70%
top_tags,4,RPG,22,44%
top_tags,5,Indie,40,80%
top_tags,6,Adventure,30,60%
top_tags,7,Horror,18,36%
top_tags,8,Shooter,16,32%
top_tags,9,Co-op,15,30%
top_tags,10,Roguelike,14,28%
```

---

## 📝 CSV 5: 언어 지원 분석 (04_language_support.csv)

### 스키마
```csv
support_type,rank,language,game_count,percentage,priority,note
```

### 용도
- 인터페이스 언어 TOP 7 (언어 차트용)
- 요약 통계 (음성 지원률, 평균 언어 수)
- 전략 포인트 (인디/AA/AAA급 가이드)

### 컬럼 설명
| 컬럼 | 타입 | 설명 | 예시 |
|------|------|------|------|
| support_type | 문자열 | 지원 타입 | `interface` / `summary` / `strategy` |
| rank | 숫자/문자열 | 순위 또는 ID | `1` / `voice` / `인디` |
| language | 문자열 | 언어명 또는 설명 | `영어` / `음성 지원` |
| game_count | 숫자 | 지원 게임 수 또는 권장 수 | `50` / `3` |
| percentage | 문자열 | 비율 | `100%` / `42%` / `7.8개` |
| priority | 문자열 | 우선순위 | `필수` / `권장` / `선택` |
| note | 문자열 | 부가 설명 | `글로벌 기본` / `TOP 10 기준` |

### 출력 예시
```csv
support_type,rank,language,game_count,percentage,priority,note
interface,1,영어,50,100%,필수,글로벌 기본
interface,2,중국어 간체,46,92%,필수,최대 시장
interface,3,한국어,35,70%,권장,아시아 주요
interface,4,일본어,34,68%,권장,AAA 필수
interface,5,중국어 번체,27,54%,권장,대만/홍콩
interface,6,러시아어,28,56%,선택,
interface,7,프랑스어,26,52%,선택,
summary,voice,음성 지원,5,42%,,TOP 10 기준
summary,interface_avg,인터페이스 평균,,7.8개,,
summary,subtitle_avg,자막 평균,,8.2개,,
strategy,인디,영어+중국어+한국어,3,,,최소 필수
strategy,AA급,위 3개 + 일본어/러시아어 추가,5,,,권장
strategy,AAA급,10개 이상 다국어,10,,,필수
strategy,유럽,스페인어/프랑스어/독일어,3,,,유럽 공략 시
strategy,남미,포르투갈어(브라질),1,,,남미 공략 시
```

### 📌 대시보드 동적 요소
- **필수 언어 5종 목록**: `interface` 상위 5개 → `#essential-languages-list`
- **전략 포인트**: `strategy` 데이터 → `#language-strategy-list`
- **요약 통계**: `summary` 데이터 → `#voice-support-stat`, `#interface-lang-stat`, `#subtitle-lang-stat`

---

## 📝 CSV 6: 커뮤니티 운영 분석 (05_community.csv)

### 스키마
```csv
analysis_type,platform,usage_rate,priority,region_target
```

### 용도
- 채널별 운영률만 (커뮤니티 차트용)
- 지역별 플랫폼/타임라인은 가이드로 유지

### 컬럼 설명
| 컬럼 | 타입 | 설명 | 예시 |
|------|------|------|------|
| analysis_type | 문자열 | 분석 타입 | `channel_usage` |
| platform | 문자열 | 플랫폼명 | `Discord` |
| usage_rate | 문자열 | 운영률 | `90%` |
| priority | 문자열 | 우선순위 | `필수` / `권장` |
| region_target | 문자열 | 타겟 지역 | `글로벌` |

### 출력 예시
```csv
analysis_type,platform,usage_rate,priority,region_target
channel_usage,Discord,90%,필수,글로벌
channel_usage,YouTube,85%,필수,글로벌
channel_usage,X,80%,필수,글로벌/일본
channel_usage,Reddit,45%,권장,북미/유럽
channel_usage,bilibili,30%,권장,중국
channel_usage,Weibo,25%,권장,중국
channel_usage,TikTok,40%,권장,글로벌
channel_usage,Instagram,20%,선택,글로벌
```

---

## 🔒 유지 영역 안내 (가이드성 콘텐츠)

### 다음 영역은 **정적 가이드 콘텐츠**로 유지됩니다:

#### 1. 장르별 필수 태그 추천 (HTML 하드코딩)
- 액션/RPG: Action, RPG, Combat, Story Rich
- 슈팅: FPS, Shooter, Multiplayer, PvP
- 로그라이크: Roguelike, Procedural, Difficult

#### 2. ~~필수 언어 5종 / 전략 포인트~~ → **이제 동적화됨!**
- `04_language_support.csv`의 `interface` (상위 5개) → 필수 언어 목록
- `04_language_support.csv`의 `strategy` → 전략 포인트
- `04_language_support.csv`의 `summary` → 요약 통계 (42%, 7.8개, 8.2개)

#### 3. 지역별 플랫폼 선호도 (HTML 하드코딩)
- 북미/유럽: Discord, Reddit, X, YouTube
- 동아시아: Discord, bilibili, 微博, TikTok
- 한국: Discord, YouTube, 네이버, 인벤
- 일본: Discord, YouTube, X

#### 4. SNF 전후 커뮤니티 타임라인 (HTML 하드코딩)
- 준비 단계 (SNF 3개월 전): Discord 서버 오픈, YouTube 채널 생성, X 계정 활동, Dev Log 시작
- 실행 단계 (SNF 기간 중): 실시간 Q&A, 핫픽스 공지, 피드백 수집, 매일 확인
- 정리 단계 (SNF 종료 후): 설문조사, 로드맵 공개, 지속 소통, 출시일 발표

---

## 🔄 갱신 주기
- SNF **종료 후 1회** 최종 결산용
- 또는 SNF 기간 중 **Day 3, Day 5** 중간 점검용
