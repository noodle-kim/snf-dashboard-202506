# 🏆 TOP 게임 분석 - AI 인사이트 프롬프트 v2.1

## 📋 개요
이 프롬프트는 대시보드의 **두 번째 페이지 "TOP 게임 분석"**에 표시될 AI 인사이트를 생성합니다.

---

## ⚠️ 중요: CSV 포맷 규칙

### 필수 준수 사항
1. **숫자에 쉼표 금지**: `716572` (O) / `716,572` (X)
2. **큰 숫자는 K/M 단위 사용**: `+70.7K`, `+151K`
3. **퍼센트는 % 포함**: `50%`, `+25.6%`
4. **파이프(|) 구분자**: 여러 항목은 파이프로 구분
5. **빈 값은 빈 문자열**: `,,` (O) / `,null,` (X)

### 금지 사항
- 셀 내 쉼표 사용 (CSV 파싱 오류 유발)
- value 필드에 쉼표 포함 금지 (`+716,572` → `+716K`)

---

## 🎯 생성 목표

| # | 파일명 | 용도 | 동적화 |
|---|--------|------|--------|
| 1 | `01_kpi_cards.csv` | TOP 게임 핵심 KPI 2개 | ✅ |
| 2 | `02_key_findings.csv` | 핵심 성과 요약 4개 | ✅ |
| 3 | `03_top10_insight.csv` | TOP 10 탭 insight-box 텍스트 | ✅ **신규** |
| 4 | `03_top10_table.csv` | TOP 10 게임 상세 테이블 | ✅ |
| 5 | `04_top50_insight.csv` | TOP 50 탭 insight-box 텍스트 | ✅ **신규** |
| 6 | `05_top50_summary.csv` | TOP 50 요약 카드 3개 | ✅ **신규** |
| 7 | `05_top50_table.csv` | TOP 50 게임 테이블 | ✅ |

### 🔒 유지 영역 (동적화 하지 않음)
- Chart.js 차트 데이터 (v2.2에서 처리 예정)

---

## 📊 입력 데이터 (raw/ 폴더)

| 파일명 | 내용 | 활용 |
|--------|------|------|
| `TOP10 게임 종합 평가*.csv` | 순위/리뷰/찜 수/유저 국적 | TOP 10 분석/KPI |
| `가장 많이 플레이한 TOP50*.csv` | 장르/체험판/멀티플레이/출시일 | TOP 50 분석/트렌드 |

---

## 📝 CSV 1: KPI 카드 (01_kpi_cards.csv)

### 스키마
```csv
id,icon,value,label,sublabel,highlight
```

### 컬럼 설명
| 컬럼 | 타입 | 설명 | 예시 |
|------|------|------|------|
| id | 숫자 | 순번 1-2 | `1` |
| icon | 이모지 | KPI 아이콘 | `📈` |
| value | 문자열 | 핵심 수치 (**쉼표 금지**) | `+716K 찜` |
| label | 문자열 | 지표명 | `SNF 기간 총 찜 수 증가` |
| sublabel | 문자열 | 부가 설명 | `TOP 10 합계` |
| highlight | 문자열 | 강조할 게임명 (선택) | `빈딕투스` |

### 출력 예시
```csv
id,icon,value,label,sublabel,highlight
1,📈,+716K 찜,SNF 기간 총 찜 수 증가,TOP 10 합계,
2,🚀,+151K 찜,1위 게임 성과,+25.6% 증가,빈딕투스
```

---

## 📝 CSV 2: 핵심 성과 요약 (02_key_findings.csv)

### 스키마
```csv
id,icon,title,description,border_color
```

### 컬럼 설명
| 컬럼 | 타입 | 설명 | 예시 |
|------|------|------|------|
| id | 숫자 | 순번 1-4 | `1` |
| icon | 이모지 | 발견점 아이콘 | `🎮` |
| title | 문자열 | 제목 (10자 이내) | `체험판이 성공의 열쇠` |
| description | 문자열 | 상세 설명 (50-80자) | `TOP 10 중 5개 게임이...` |
| border_color | HEX | 카드 테두리 색상 | `#0047AB` |

### 출력 예시
```csv
id,icon,title,description,border_color
1,🎮,체험판이 성공의 열쇠,TOP 10 중 4개 게임이 체험판 페이지 접속 가능. 체험판을 제공하면 유저 관심도가 크게 높아집니다.,#0047AB
2,👥,멀티플레이가 대세,TOP 10 중 8개가 멀티플레이 게임. 협동/경쟁 요소가 SNF에서 강력한 경쟁력이 됩니다.,#3B82F6
3,⭐,긍정 리뷰가 중요,TOP 10 중 3개가 긍정적 이상 리뷰. 긍정적 평가가 게임 성공에 큰 영향을 미칩니다.,#F59E0B
4,🌏,중국어권이 핵심,TOP 10 중 4개 게임 리뷰에 간체 중국어가 포함. 중국 시장 공략이 잠재 고객 확보에 중요합니다.,#8B5CF6
```

---

## 📝 CSV 3: TOP 10 탭 insight-box (03_top10_insight.csv) **신규**

### 스키마
```csv
id,tab_name,insight_text
```

### 용도
- TOP 10 탭 상단의 insight-box (`💡 이 차트의 특징:`) 텍스트
- 하드코딩된 텍스트를 동적으로 변경

### 컬럼 설명
| 컬럼 | 타입 | 설명 | 예시 |
|------|------|------|------|
| id | 숫자 | 순번 | `1` |
| tab_name | 문자열 | 탭 식별자 | `top10` |
| insight_text | 문자열 | 인사이트 텍스트 (100자 내외) | `SNF 기간 중 실제로...` |

### 출력 예시
```csv
id,tab_name,insight_text
1,top10,SNF 기간 중 실제로 가장 많이 플레이된 게임들입니다. 리뷰 수와 찜 수 증가가 모두 뛰어난 검증된 타이틀들이에요. 간체 중국어 유저들의 활동이 특히 활발했습니다.
```

---

## 📝 CSV 4: TOP 10 테이블 (03_top10_table.csv)

### 스키마
```csv
rank,name,genre,review_status,review_count,wishlist_increase,wishlist_percent,chart_count,steamdb_rank
```

### 컬럼 설명
| 컬럼 | 타입 | 설명 | 예시 |
|------|------|------|------|
| rank | 숫자 | 순위 1-10 | `1` |
| name | 문자열 | 게임명 | `빈딕투스: 디파잉 페이트` |
| genre | 문자열 | 장르 | `액션 RPG` |
| review_status | 문자열 | 리뷰 상태 | `복합적` / `매우 긍정적` / `압도적 긍정` / `확인불가` |
| review_count | 문자열 | 리뷰 수 (쉼표 금지) | `5200` / `-` |
| wishlist_increase | 문자열 | 찜 증가량 | `+151605` |
| wishlist_percent | 문자열 | 증가율 | `+25.6%` |
| chart_count | 숫자 | 차트인 횟수 | `14` |
| steamdb_rank | 문자열 | 스팀DB 찜 랭크 | `31위` |

### 출력 예시
```csv
rank,name,genre,review_status,review_count,wishlist_increase,wishlist_percent,chart_count,steamdb_rank
1,빈딕투스: 디파잉 페이트,액션 RPG,복합적,5200,+151605,+25.6%,14,31위
2,Jump Ship,슈팅 (1인칭),확인불가,1811,+59726,+20.1%,9,96위
3,와일드게이트,슈팅 (1인칭),매우 긍정적,3297,+89715,+43.2%,15,18위
4,MIMESIS,공포,확인불가,-,+53825,+43.2%,6,211위
5,Dead Rising Deluxe Remaster,액션,압도적 긍정,2207,+71933,+85.4%,9,109위
6,나 혼자만 레벨업: Arise,액션 RPG,확인불가,-,+72929,+18.7%,12,43위
7,PIONER,MMORPG,확인불가,336,+82890,+27.3%,5,90위
8,Zoochosis,공포,압도적 긍정,1197,+90281,+134.6%,12,60위
9,UFL,스포츠 (축구),확인불가,-,+20482,+12.8%,5,203위
10,Starlight Re:Volver,로그라이크,확인불가,-,+13209,+58.4%,1,286위
```

---

## 📝 CSV 5: TOP 50 탭 insight-box (04_top50_insight.csv) **신규**

### 스키마
```csv
id,tab_name,insight_text
```

### 출력 예시
```csv
id,tab_name,insight_text
1,top50,TOP 50까지 확장하면 다양한 인디 게임들도 포함됩니다. 로그라이크 장르가 압도적으로 많고 멀티플레이 게임이 싱글플레이보다 약간 더 많습니다. 체험판 제공 여부가 성공에 큰 영향을 미쳤어요.
```

---

## 📝 CSV 6: TOP 50 요약 카드 (05_top50_summary.csv) **신규**

### 스키마
```csv
id,icon,title,value,description,color
```

### 용도
- TOP 50 탭 상단의 3개 요약 카드 데이터

### 컬럼 설명
| 컬럼 | 타입 | 설명 | 예시 |
|------|------|------|------|
| id | 숫자 | 순번 1-3 | `1` |
| icon | 이모지 | 카드 아이콘 | `🎮` |
| title | 문자열 | 카드 제목 | `체험판 접속 가능` |
| value | 문자열 | 핵심 수치 | `29개` |
| description | 문자열 | 부가 설명 | `TOP 50 중 58%` |
| color | HEX | 제목 색상 | `#0047AB` |

### 출력 예시
```csv
id,icon,title,value,description,color
1,🎮,체험판 접속 가능,29개,TOP 50 중 58%,#0047AB
2,👥,멀티플레이,27개,54% (싱글 23개),#3B82F6
3,🎯,최다 장르,로그라이크,14개 게임 (28%),#8B5CF6
```

---

## 📝 CSV 7: TOP 50 테이블 (05_top50_table.csv)

### 스키마
```csv
rank,name,genre,demo_available,play_type,release_date,chart_count
```

### 컬럼 설명
| 컬럼 | 타입 | 설명 | 예시 |
|------|------|------|------|
| rank | 숫자 | 순위 1-50 | `1` |
| name | 문자열 | 게임명 | `빈딕투스: 디파잉 페이트` |
| genre | 문자열 | 장르 | `액션 RPG` |
| demo_available | 문자열 | 체험판 여부 | `✓` / `✗` |
| play_type | 문자열 | 플레이 타입 | `멀티` / `싱글` |
| release_date | 문자열 | 출시일 | `출시예정` / `2025.07.23` |
| chart_count | 숫자 | 차트인 횟수 | `14` |

### 출력 예시 (처음 10개만)
```csv
rank,name,genre,demo_available,play_type,release_date,chart_count
1,빈딕투스: 디파잉 페이트,액션 RPG,✓,멀티,출시예정,14
2,Jump Ship,슈팅 (1인칭),✗,멀티,2025.07.23,9
3,와일드게이트,슈팅 (1인칭),✓,멀티,2025년,15
4,MIMESIS,공포,✗,멀티,2025년 3분기,6
5,Dead Rising Deluxe Remaster,액션,✓,싱글,출시예정,9
6,나 혼자만 레벨업: Arise,액션 RPG,✗,멀티,2025년,12
7,PIONER,MMORPG,✗,멀티,2025년,5
8,Zoochosis,공포,✓,싱글,2025년 3분기,12
9,UFL,스포츠 (축구),✗,멀티,출시예정,5
10,Starlight Re:Volver,로그라이크,✗,멀티,2025년 3분기,1
```

---

## 🔄 갱신 주기
- SNF 기간 동안 **매일 1회** 또는 순위 변동 시 갱신
- TOP10 순위 변동 시 우선 갱신
