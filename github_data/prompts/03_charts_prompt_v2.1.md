# 📈 차트 성과 분석 - AI 인사이트 프롬프트 v2.1

## 📋 개요
이 프롬프트는 대시보드의 **세 번째 페이지 "차트 성과 분석"**에 표시될 AI 인사이트를 생성합니다.

---

## ⚠️ 중요: CSV 포맷 규칙

### 필수 준수 사항
1. **숫자에 쉼표 금지**: `716572` (O) / `716,572` (X)
2. **큰 숫자는 K/M 단위 사용**: `+70.7K`
3. **퍼센트는 % 포함**: `35%`
4. **파이프(|) 구분자**: 여러 항목은 파이프로 구분
5. **빈 값은 빈 문자열**: `,,`

### 금지 사항
- 셀 내 쉼표 사용
- value 필드에 쉼표 포함 금지

---

## 🎯 생성 목표

| # | 파일명 | 용도 | 동적화 |
|---|--------|------|--------|
| 1 | `01_kpi_cards.csv` | 차트 성과 KPI 2개 | ✅ |
| 2 | `02_key_findings.csv` | 차트 분석 인사이트 4개 | ✅ |
| 3 | `03_chart_insights.csv` | 3종 차트 탭별 insight-box 텍스트 | ✅ **신규** |
| 4 | `05_demo_chart.csv` | 인기 체험판 차트 테이블 | ✅ |
| 5 | `06_popular_upcoming.csv` | 인기 출시 예정 차트 테이블 | ✅ |
| 6 | `07_trending_upcoming.csv` | 떠오르는 출시 예정 차트 테이블 | ✅ |

### 🔒 유지 영역 (동적화 하지 않음 - 가이드성 콘텐츠)
- **2026 전략 권장사항** 3개 카드: 인기 체험판 노리기 / 인기 출시 예정 도전 / 떠오르는 게임 진입
- Chart.js 차트 데이터 (v2.2에서 처리 예정)

---

## 📊 입력 데이터 (raw/ 폴더)

| 파일명 | 내용 | 활용 |
|--------|------|------|
| `전체 장르 - 각 게임별 SNF기간 3종 차트인 횟수*.csv` | 게임명/날짜/랭킹/차트 구분 | 모든 차트 분석 |
| `인기 체험판*.csv` | 인기 체험판 차트 (있다면) | 체험판 차트 분석 |
| `인기 출시 예정 게임*.csv` | 인기 출시 예정 (있다면) | 출시 예정 분석 |
| `떠오르는 출시 예정 게임*.csv` | 떠오르는 출시 예정 (있다면) | 신흥 게임 분석 |

---

## 📝 CSV 1: KPI 카드 (01_kpi_cards.csv)

### 스키마
```csv
id,icon,value,label,description,color
```

### 컬럼 설명
| 컬럼 | 타입 | 설명 | 예시 |
|------|------|------|------|
| id | 숫자 | 순번 1-2 | `1` |
| icon | 이모지 | KPI 아이콘 | `📊` |
| value | 문자열 | 핵심 수치 (**쉼표 금지**) | `47개` |
| label | 문자열 | 지표명 | `3종 차트 진입 게임 수` |
| description | 문자열 | 설명 | `인기 체험판/출시예정/떠오르는` |
| color | HEX | 색상 | `#0047AB` |

### 출력 예시
```csv
id,icon,value,label,description,color
1,📊,47개,3종 차트 진입 게임 수,인기 체험판/출시예정/떠오르는,#0047AB
2,👑,14회,최다 차트인,빈딕투스: 디파잉 페이트,#0047AB
```

---

## 📝 CSV 2: 핵심 발견점 (02_key_findings.csv)

### 스키마
```csv
id,icon,title,description,color
```

### 컬럼 설명
| 컬럼 | 타입 | 설명 | 예시 |
|------|------|------|------|
| id | 숫자 | 순번 1-4 | `1` |
| icon | 이모지 | 발견점 아이콘 | `📈` |
| title | 문자열 | 제목 (15자 이내) | `상위 3개 게임이 주도` |
| description | 문자열 | 상세 설명 (60-100자) | `빈딕투스 나혼자레벨업...` |
| color | HEX | 카드 테두리 색상 | `#0047AB` |

### 출력 예시
```csv
id,icon,title,description,color
1,📈,상위 3개 게임이 주도,빈딕투스 나혼자레벨업 Jump Ship 3개 게임이 전체 차트 노출의 25%를 차지했습니다. 상위권 게임들의 독주가 두드러졌습니다.,#0047AB
2,🎮,체험판이 가장 효과적,인기 체험판 차트가 전체 노출의 35%를 차지해 가장 효과적인 홍보 채널입니다. 체험판 준비를 최우선으로 고려하세요.,#0047AB
3,🎯,10회 이상 진입 = 성공,10회 이상 차트에 오른 게임은 4개뿐. 이 기준을 달성하면 성공적인 SNF입니다. 연속 노출 전략이 핵심입니다.,#0047AB
4,🚀,3종 차트 동시 공략이 핵심,세 종류의 차트에 모두 진입한 게임들이 평균 12회 이상 노출되며 높은 성과를 기록했습니다.,#3B82F6
```

---

## 📝 CSV 3: 3종 차트 탭별 insight-box (03_chart_insights.csv) **신규**

### 스키마
```csv
id,chart_type,insight_text
```

### 용도
- 각 탭(인기 체험판/인기 출시 예정/떠오르는 출시 예정)의 상단 insight-box 텍스트
- 하드코딩된 `💡 이 차트의 특징:` 텍스트를 동적으로 변경

### 컬럼 설명
| 컬럼 | 타입 | 설명 | 예시 |
|------|------|------|------|
| id | 숫자 | 순번 1-3 | `1` |
| chart_type | 문자열 | 차트 종류 | `demo` / `popular` / `trending` |
| insight_text | 문자열 | 인사이트 텍스트 (80-120자) | `체험판 차트는 가장 안정적입니다...` |

### 출력 예시
```csv
id,chart_type,insight_text
1,demo,체험판 차트는 가장 안정적입니다. 상위권 게임들이 5일 내내 꾸준히 순위를 유지했어요. 빈딕투스와 나혼자레벨업 같은 한국 게임이 강세를 보였고 중국 퍼블리셔 bilibili도 적극 참여했습니다.
2,popular,대형 타이틀들의 격전지입니다. 빈딕투스와 나혼자레벨업이 1~2위를 두고 치열하게 경쟁했어요. Nacon 같은 서양 퍼블리셔와 한국 퍼블리셔가 맞붙는 흥미로운 구도가 펼쳐졌습니다.
3,trending,가장 변화가 빠른 차트입니다. 매일 1위가 바뀔 정도로 역동적이에요. Moonlighter 2처럼 인디 게임도 1위에 오를 수 있어서 바이럴 마케팅의 효과가 가장 큰 차트입니다.
```

---

## 📝 CSV 4: 인기 체험판 차트 (05_demo_chart.csv)

### 스키마
```csv
rank,name,developer,publisher,appearances,best_rank,consecutive_days
```

### 컬럼 설명
| 컬럼 | 타입 | 설명 | 예시 |
|------|------|------|------|
| rank | 숫자 | 순위 1-10 | `1` |
| name | 문자열 | 게임명 | `빈딕투스: 디파잉 페이트` |
| developer | 문자열 | 개발사 | `NEXON` |
| publisher | 문자열 | 배급사 | `NEXON` |
| appearances | 숫자 | 등장 횟수 | `5` |
| best_rank | 문자열 | 최고 순위 | `1위` |
| consecutive_days | 문자열 | 5일 연속 여부 | `✓` / `-` |

### 출력 예시
```csv
rank,name,developer,publisher,appearances,best_rank,consecutive_days
1,빈딕투스: 디파잉 페이트,NEXON,NEXON,5,1위,✓
2,PIONER,GFAGAMES,GFAGAMES,5,2위,✓
3,Escape from Duckov,Team Soda,bilibili,5,3위,✓
4,나 혼자만 레벨업,Netmarble Neo,Netmarble,2,8위,-
5,MIMESIS,Unknown,Unknown,5,4위,✓
```

---

## 📝 CSV 5: 인기 출시 예정 차트 (06_popular_upcoming.csv)

### 스키마
```csv
rank,name,developer,publisher,appearances,best_rank,consecutive_days
```

### 출력 예시
```csv
rank,name,developer,publisher,appearances,best_rank,consecutive_days
1,빈딕투스: 디파잉 페이트,NEXON,NEXON,5,1위,✓
2,나 혼자만 레벨업,Netmarble Neo,Netmarble,5,1~2위,✓
3,Hell is Us,Nacon,Nacon,5,3위,✓
4,Dead Rising,Ramjet Studios,Ramjet Studios,4,4위,-
5,PIONER,GFAGAMES,GFAGAMES,5,3~5위,✓
```

---

## 📝 CSV 6: 떠오르는 출시 예정 차트 (07_trending_upcoming.csv)

### 스키마
```csv
rank,name,developer,publisher,appearances,best_rank,trend_direction
```

### 컬럼 설명
| 컬럼 | 타입 | 설명 | 예시 |
|------|------|------|------|
| rank | 숫자 | 순위 1-10 | `1` |
| name | 문자열 | 게임명 | `Moonlighter 2` |
| developer | 문자열 | 개발사 | `Digital Sun` |
| publisher | 문자열 | 배급사 | `11 bit studios` |
| appearances | 숫자 | 등장 횟수 | `5` |
| best_rank | 문자열 | 최고 순위 | `1위` |
| trend_direction | 문자열 | 추세 | `안정` / `상승` / `변동` / `급상승` |

### 출력 예시
```csv
rank,name,developer,publisher,appearances,best_rank,trend_direction
1,Moonlighter 2,Digital Sun,11 bit studios,5,1위,안정
2,나 혼자만 레벨업,Netmarble Neo,Netmarble,4,1위,상승
3,PIONER,GFAGAMES,GFAGAMES,4,3위,안정
4,Jump Ship,Unknown,Unknown,4,1위,변동
5,Date Everything,Unknown,Unknown,2,2~3위,급상승
```

---

## 🔒 유지 영역 안내 (가이드성 콘텐츠) → **v2.1에서 동적화됨**

### ~~2026 전략 권장사항 - 변경하지 않음~~ → **이제 동적화됨!**

## 📝 CSV 7: SNF 준비 전략 (09_snf_strategy.csv) **v2.1 신규**

### 스키마
```csv
id,icon,title,color,details
```

### 용도
- "2026년 2월 SNF, 어떻게 준비할까?" 섹션의 3개 전략 카드
- AI가 데이터 기반으로 전략 권장사항 도출

### 컬럼 설명
| 컬럼 | 타입 | 설명 | 예시 |
|------|------|------|------|
| id | 숫자 | 순번 1-3 | `1` |
| icon | 이모지 | 전략 아이콘 | `🔥` |
| title | 문자열 | 전략명 (15자 이내) | `인기 체험판 노리기` |
| color | HEX | 제목 색상 | `#0047AB` / `#3B82F6` |
| details | 문자열 | 세부 전략 (파이프 구분) | `항목1|항목2|항목3|항목4` |

### 출력 예시
```csv
id,icon,title,color,details
1,🔥,인기 체험판 노리기,#0047AB,가장 안정적인 노출 채널|완성도 높은 체험판이 필수|5일 연속 TOP 10 유지가 목표|멀티플레이 요소가 있으면 유리
2,⭐,인기 출시 예정 도전,#0047AB,대형 타이틀과 경쟁해야 함|SNF 전 사전 마케팅 중요|찜 목록 추가를 적극 유도|게임 미디어 커버리지 확보
3,🚀,떠오르는 게임 진입,#3B82F6,입소문 마케팅이 효과적|차별화된 컨셉으로 승부|인디 게임에게 기회가 많음|커뮤니티 반응에 빠르게 대응
```

### 💡 AI 인사이트 생성 가이드
- **데이터 기반** 전략을 도출하세요
- 실제 차트 데이터에서 확인된 패턴을 반영
- 각 차트별 특성에 맞는 구체적인 전략 제시
- 한국 게임사에 실질적으로 도움되는 조언

---

## 🔄 갱신 주기
- SNF 기간 동안 **매일 1회** (차트는 하루에도 여러 번 변동)
- 차트 데이터 수집 시점에 맞춰 갱신
