# 🏆 TOP 게임 분석 - AI 인사이트 프롬프트

## 📋 개요
이 프롬프트는 대시보드의 **두 번째 페이지 "TOP 게임 분석"**에 표시될 AI 인사이트를 생성합니다.

---

## 🎯 생성 목표
TOP 10 / TOP 50 게임 데이터를 분석하여 **6개의 CSV 파일**을 생성합니다:
1. `01_kpi_cards.csv` - TOP 게임 핵심 KPI 2개
2. `02_key_findings.csv` - 핵심 성과 요약 4개
3. `03_top10_table.csv` - TOP 10 게임 상세 테이블
4. `04_top10_charts.csv` - TOP 10 차트 데이터 (찜 수, 리뷰, 장르)
5. `05_top50_table.csv` - TOP 50 게임 테이블
6. `06_top50_charts.csv` - TOP 50 차트 데이터 (장르, 멀티/싱글, 체험판)

---

## 📊 입력 데이터 (raw/ 폴더)

| 파일명 | 내용 | 활용 |
|--------|------|------|
| `TOP10 게임 종합 평가*.csv` | 순위, 리뷰, 찜 수, 유저 국적 | TOP 10 분석, KPI |
| `가장 많이 플레이한 TOP50*.csv` | 장르, 체험판, 멀티플레이, 출시일 | TOP 50 분석, 트렌드 |

---

## 📝 프롬프트 1: KPI 카드 (01_kpi_cards.csv)

```
TOP10 게임 종합 평가 데이터에서 **핵심 KPI 2개**를 추출해주세요.

### 출력 형식 (CSV):
id,icon,value,label,sublabel,highlight
1,📈,{값},{지표명},{부가설명},{강조할 게임명}
2,🚀,{값},{지표명},{부가설명},{강조할 게임명}

### 필수 KPI:
1. TOP 10 총 찜 수 증가량 (예: +70만 찜)
2. 1위 게임의 찜 수 증가량 (예: +15만 찜, 빈딕투스)

### 계산 방법:
- 찜 증가량 = 참여 후 찜 수 - 참여 전 찜 수
- 증가율 = (찜 증가량 / 참여 전 찜 수) × 100
```

---

## 📝 프롬프트 2: 핵심 성과 요약 (02_key_findings.csv)

```
TOP 10 및 TOP 50 게임 데이터를 분석하여 **핵심 성과 요약 4개**를 도출해주세요.

### 출력 형식 (CSV):
id,icon,title,description,border_color
1,🎮,{제목},{50자 이상 상세 설명},#0047AB
2,👥,{제목},{50자 이상 상세 설명},#3B82F6
3,⭐,{제목},{50자 이상 상세 설명},#F59E0B
4,🌏,{제목},{50자 이상 상세 설명},#8B5CF6

### 분석 포인트:
1. **체험판 제공 여부**와 성과의 상관관계
2. **멀티플레이 vs 싱글플레이** 비율 및 성과 차이
3. **리뷰 상태**(긍정적/복합적/확인불가)와 순위의 관계
4. **지역별 유저 분포** (중국어권 비중)

### 작성 가이드:
- title: 7단어 이내의 명확한 제목 (예: "체험판이 성공의 열쇠")
- description: 반드시 구체적 수치 포함 (예: "TOP 10 중 5개가...", "70%가...")
```

---

## 📝 프롬프트 3: TOP 10 테이블 (03_top10_table.csv)

```
TOP10 게임 종합 평가 데이터를 정제하여 **테이블 형식**으로 출력해주세요.

### 출력 형식 (CSV):
rank,name,genre,review_status,review_count,wishlist_before,wishlist_after,wishlist_increase,wishlist_percent,top_language,chart_count
1,{게임명},{장르},{리뷰상태},{리뷰수},{참여전찜},{참여후찜},{증가량},{증가율%},{1위언어},{차트인횟수}

### 게임명 매핑:
- app/3576170 → 빈딕투스: 디파잉 페이트
- app/3504780 → 와일드 게이트  
- app/2841820 → Jump Ship
- app/2827200 → MIMESIS
- app/3763830 → Zoochosis
- app/2373990 → 나 혼자만 레벨업: 어라이즈
- app/3105890 → PIONER
- app/3640000 → Holstin
- app/3023930 → UFL
- app/3201010 → Starlight ReVolver

### 장르 매핑 (TOP50 데이터 참조):
- 순위 1 → 액션 RPG
- 순위 2 → 슈팅
- 순위 3 → 슈팅
- 순위 4 → 공포
- ... (TOP50 데이터의 장르 컬럼 참조)
```

---

## 📝 프롬프트 4: TOP 10 차트 데이터 (04_top10_charts.csv)

```
TOP 10 게임의 시각화용 차트 데이터를 생성해주세요.

### 출력 형식 (CSV):
chart_type,label,value,color
wishlist_top5,{게임명},{찜증가량},#0047AB
wishlist_top5,{게임명},{찜증가량},#3B82F6
review_dist,압도적 긍정,{개수},#003380
review_dist,매우 긍정적,{개수},#0047AB
review_dist,복합적,{개수},#60A5FA
review_dist,확인불가,{개수},#94A3B8
genre_dist,{장르명},{개수},#색상코드

### 차트 종류:
1. wishlist_top5: 찜 수 증가 TOP 5 (막대 차트)
2. review_dist: 리뷰 상황 분포 (도넛 차트)
3. genre_dist: 장르 분포 (도넛 차트)
```

---

## 📝 프롬프트 5: TOP 50 테이블 (05_top50_table.csv)

```
가장 많이 플레이한 TOP50 게임 데이터를 정제해주세요.

### 출력 형식 (CSV):
rank,name,genre,play_type,demo_available,release_date,chart_count,notes
1,{게임명},{장르},{멀티/싱글},{가능/불가능},{출시일},{차트인횟수},{참고사항}

### 데이터 정제 규칙:
- name: Steam URL에서 게임명 추출 (알려진 게임은 한글명 사용)
- demo_available: "가능" → true, "불가능" → false
- play_type: "멀티플레이" → "멀티", "싱글 플레이" → "싱글"
- chart_count: 빈 값은 0으로 처리
```

---

## 📝 프롬프트 6: TOP 50 차트 데이터 (06_top50_charts.csv)

```
TOP 50 게임의 시각화용 통계 데이터를 생성해주세요.

### 출력 형식 (CSV):
chart_type,label,value,color,percentage
genre_dist,{장르명},{개수},{색상},{비율%}
play_type,멀티플레이,{개수},#0047AB,{비율%}
play_type,싱글플레이,{개수},#60A5FA,{비율%}
demo_avail,체험판 제공,{개수},#0047AB,{비율%}
demo_avail,체험판 없음,{개수},#94A3B8,{비율%}

### 분석 항목:
1. genre_dist: 장르별 분포 (로그라이크, 슈팅, 액션, 시뮬레이션, 공포, 기타)
2. play_type: 멀티플레이 vs 싱글플레이 비율
3. demo_avail: 체험판 제공 vs 미제공 비율
```

---

## 📤 출력 파일 목록

| 파일명 | 용도 | 대시보드 위치 |
|--------|------|--------------|
| `01_kpi_cards.csv` | KPI 2개 | TOP Games - 상단 |
| `02_key_findings.csv` | 핵심 성과 4개 | TOP Games - 요약 영역 |
| `03_top10_table.csv` | TOP 10 테이블 | TOP Games - TOP 10 탭 |
| `04_top10_charts.csv` | TOP 10 차트 | TOP Games - TOP 10 차트 |
| `05_top50_table.csv` | TOP 50 테이블 | TOP Games - TOP 50 탭 |
| `06_top50_charts.csv` | TOP 50 차트 | TOP Games - TOP 50 차트 |

---

## ✅ 출력 예시

### 01_kpi_cards.csv
```csv
id,icon,value,label,sublabel,highlight
1,📈,+70만 찜,SNF 기간 총 찜 수 증가,TOP 10 합계,
2,🚀,+15만 찜,1위 게임 성과,+25.6% 증가,빈딕투스
```

### 02_key_findings.csv
```csv
id,icon,title,description,border_color
1,🎮,체험판이 성공의 열쇠,TOP 10 중 5개 게임이 체험판 페이지 접속 가능. 체험판을 제공하면 유저 관심도가 크게 높아집니다.,#0047AB
2,👥,멀티플레이가 대세,TOP 10 중 7개가 멀티플레이 게임. 협동/경쟁 요소가 SNF에서 강력한 경쟁력이 됩니다.,#3B82F6
3,⭐,긍정 리뷰가 증명,TOP 10 중 4개가 긍정적 이상 리뷰. 품질이 검증된 게임들이 상위권을 차지했습니다.,#F59E0B
4,🌏,중국어권이 핵심,대부분의 TOP 게임 리뷰 언어 1위가 간체 중국어. 중국 시장 공략이 성공의 필수 요소입니다.,#8B5CF6
```

### 04_top10_charts.csv
```csv
chart_type,label,value,color
wishlist_top5,빈딕투스,151605,#0047AB
wishlist_top5,Jump Ship,89715,#3B82F6
wishlist_top5,Zoochosis,90281,#0047AB
wishlist_top5,나혼자레벨업,72929,#0047AB
wishlist_top5,PIONER,82890,#8B5CF6
review_dist,압도적 긍정,2,#003380
review_dist,매우 긍정적,1,#0047AB
review_dist,복합적,1,#60A5FA
review_dist,확인불가,6,#94A3B8
genre_dist,액션 RPG,2,#003380
genre_dist,슈팅,2,#0047AB
genre_dist,공포,2,#3B82F6
genre_dist,기타,4,#94A3B8
```

### 06_top50_charts.csv
```csv
chart_type,label,value,color,percentage
genre_dist,로그라이크,14,#003380,28%
genre_dist,슈팅,8,#0047AB,16%
genre_dist,액션,6,#3B82F6,12%
genre_dist,시뮬레이션,6,#60A5FA,12%
genre_dist,공포,5,#93C5FD,10%
genre_dist,기타,11,#94A3B8,22%
play_type,멀티플레이,27,#0047AB,54%
play_type,싱글플레이,23,#60A5FA,46%
demo_avail,체험판 제공,29,#0047AB,58%
demo_avail,체험판 없음,21,#94A3B8,42%
```

---

## 🔄 갱신 주기
- SNF 기간 동안 **매일 1회** 또는 순위 변동 시 갱신
- TOP10 순위 변동 시 우선 갱신
