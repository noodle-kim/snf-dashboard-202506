"""
SNF Dashboard AI Insights Generator (v2.0)
==========================================
고도화된 프롬프트 기반으로 모든 대시보드 데이터를 생성합니다.

생성되는 CSV 파일:
- 01_executive/: 7개 파일 (전략, KPI, 인사이트, TOP5, 차트요약, 장르분포, 가이드)
- 02_top_games/: 6개 파일 (KPI, 핵심성과, TOP10 테이블/차트, TOP50 테이블/차트)
- 03_charts/: 7개 파일 (KPI, 발견점, 통계, 전략, 체험판/출시예정/떠오르는 상세)
- 04_report/: 5개 파일 (체크리스트, KPI, 태그분석, 언어지원, 커뮤니티)

사용법:
    python generate_insights.py

API 키 설정 (택 1):
    1. scripts/.env 파일에 GEMINI_API_KEY=your-key 저장 (추천)
    2. 환경변수: $env:GEMINI_API_KEY = "your-key"
"""

import os
import csv
import time
from pathlib import Path
from datetime import datetime
import glob
import re

# .env 파일 자동 로드
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ .env 파일 로드됨: {env_path}")
except ImportError:
    pass  # python-dotenv 없으면 환경변수만 사용

# Gemini API
try:
    from google import genai
    from google.genai.errors import ClientError
except ImportError:
    print("❌ google-genai 패키지가 설치되지 않았습니다.")
    print("   실행: pip install google-genai")
    exit(1)

# ============================================
# 설정
# ============================================
SCRIPT_DIR = Path(__file__).parent
BASE_DIR = SCRIPT_DIR.parent
GITHUB_DATA_DIR = BASE_DIR / "github_data"
RAW_DIR = GITHUB_DATA_DIR / "raw"
PROMPTS_DIR = GITHUB_DATA_DIR / "prompts"

MODEL_NAME = "gemini-2.0-flash"
MAX_RETRIES = 3
RETRY_DELAY = 60
API_DELAY = 15  # API 호출 간 대기 시간

# 게임명 매핑 (Steam URL → 한글명)
GAME_NAME_MAP = {
    "3576170": "빈딕투스: 디파잉 페이트",
    "3504780": "와일드 게이트",
    "2841820": "Jump Ship",
    "2827200": "MIMESIS",
    "3763830": "Zoochosis",
    "2373990": "나 혼자만 레벨업: 어라이즈",
    "3105890": "PIONER",
    "3640000": "Holstin",
    "3023930": "UFL",
    "3201010": "Starlight ReVolver",
}

# 원본 CSV 파일 패턴
RAW_FILES = {
    "top10_evaluation": "TOP10 게임 종합 평가*.csv",
    "top10_chart_count": "TOP10 차트인 횟수*.csv",
    "top50_games": "가장 많이 플레이한 TOP50 게임*.csv",
    "report_page": "결산 페이지*.csv",
    "trending_upcoming": "떠오르는 출시 예정 게임*.csv",
    "popular_demo": "인기 체험판*.csv",
    "popular_upcoming": "인기 출시 예정 게임*.csv",
    "chart_integration": "전체 장르 - 각 게임별 SNF기간 3종 차트인 횟수*.csv",
}


def setup_gemini():
    """Gemini API 설정"""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY 환경변수가 설정되지 않았습니다.")
        print('   Windows: $env:GEMINI_API_KEY = "your-api-key"')
        return None
    client = genai.Client(api_key=api_key)
    print(f"✅ Gemini API 연결 완료 (모델: {MODEL_NAME})")
    return client


def call_gemini(client, prompt):
    """API 호출 (재시도 로직 포함)"""
    for attempt in range(MAX_RETRIES):
        try:
            response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
            return response.text if response else None
        except ClientError as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                if attempt < MAX_RETRIES - 1:
                    wait_time = RETRY_DELAY * (attempt + 1)
                    print(f"   ⏳ API 제한. {wait_time}초 후 재시도... ({attempt + 1}/{MAX_RETRIES})")
                    time.sleep(wait_time)
                else:
                    raise
            else:
                raise
    return None


def find_csv_file(pattern):
    """패턴에 맞는 CSV 파일 찾기"""
    search_path = str(RAW_DIR / pattern)
    files = glob.glob(search_path)
    return Path(max(files, key=os.path.getmtime)) if files else None


def read_csv_content(file_path, max_lines=100):
    """CSV 파일 내용 읽기"""
    if not file_path or not file_path.exists():
        return "데이터 없음"
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.rstrip() for i, line in enumerate(f) if i < max_lines]
    return '\n'.join(lines)


def read_csv_as_dicts(file_path):
    """CSV를 딕셔너리 리스트로 읽기"""
    if not file_path or not file_path.exists():
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def save_csv(rows, output_path):
    """CSV 저장 (UTF-8 BOM)"""
    if not rows:
        return False
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"   💾 저장: {output_path.name} ({len(rows)}행)")
    return True


def parse_csv_response(response_text):
    """AI 응답에서 CSV 파싱"""
    if not response_text:
        return []
    
    # CSV 블록 찾기
    csv_match = re.search(r'```csv\s*(.*?)\s*```', response_text, re.DOTALL)
    if csv_match:
        csv_text = csv_match.group(1).strip()
    else:
        # 코드블록 없이 바로 CSV인 경우
        csv_text = response_text.strip()
        if csv_text.startswith('```'):
            csv_text = csv_text.split('```')[1] if '```' in csv_text else csv_text
    
    lines = [line.strip() for line in csv_text.split('\n') if line.strip()]
    if len(lines) < 2:
        return []
    
    # 헤더와 데이터 파싱
    headers = [h.strip() for h in lines[0].split(',')]
    rows = []
    for line in lines[1:]:
        # CSV 파싱 (쉼표가 포함된 값 처리)
        values = []
        in_quote = False
        current = ""
        for char in line:
            if char == '"':
                in_quote = not in_quote
            elif char == ',' and not in_quote:
                values.append(current.strip().strip('"'))
                current = ""
            else:
                current += char
        values.append(current.strip().strip('"'))
        
        if len(values) >= len(headers):
            rows.append(dict(zip(headers, values[:len(headers)])))
    
    return rows


def extract_game_name(url_or_name):
    """Steam URL에서 게임명 추출"""
    if not url_or_name:
        return ""
    # app/숫자 패턴 찾기
    match = re.search(r'app/(\d+)', str(url_or_name))
    if match:
        app_id = match.group(1)
        return GAME_NAME_MAP.get(app_id, f"Game_{app_id}")
    return str(url_or_name)


def load_all_raw_data():
    """모든 원본 데이터 로드"""
    print("\n📂 원본 데이터 로드 중...")
    raw_data = {}
    for key, pattern in RAW_FILES.items():
        file_path = find_csv_file(pattern)
        if file_path:
            raw_data[key] = {
                'path': file_path,
                'content': read_csv_content(file_path),
                'data': read_csv_as_dicts(file_path)
            }
            print(f"   ✅ {key}: {file_path.name}")
        else:
            raw_data[key] = {'path': None, 'content': '데이터 없음', 'data': []}
            print(f"   ⚠️ {key}: 파일 없음")
    return raw_data


# ============================================
# 1. Executive Summary 생성
# ============================================
def generate_executive(client, raw_data):
    """Executive Summary 섹션의 모든 CSV 생성"""
    print("\n" + "="*50)
    print("🎯 1/4 Executive Summary 생성")
    print("="*50)
    
    output_dir = GITHUB_DATA_DIR / "01_executive"
    
    # --- 01_strategies.csv ---
    print("\n   📝 전략 카드 생성...")
    prompt = f"""
당신은 Steam Next Fest 전략 컨설턴트입니다.
아래 데이터를 분석하여 다음 SNF 성공 전략 3개를 도출해주세요.

## TOP10 게임 종합 평가
{raw_data['top10_evaluation']['content']}

## TOP50 게임 (장르, 체험판, 멀티플레이 정보)
{raw_data['top50_games']['content']}

정확히 아래 CSV 형식으로만 출력하세요. 다른 설명 없이 CSV만:

```csv
id,icon,title,description,details
1,🎮,체험판 필수 제공,체험판이 찜 수 증가의 핵심,TOP 10의 50%가 체험판 제공|SNF 최소 2주 전 준비|1~2시간 분량|버그 없는 빌드
2,👥,멀티플레이 요소,협동/경쟁이 바이럴 효과 극대화,TOP 10의 70%가 멀티플레이|Co-op 효과 검증|스트리머 관심 유도|리더보드 추가
3,🌏,중국 시장 공략,리뷰 언어 1위가 간체 중국어,92%가 중국어 지원|Bilibili 마케팅|중국 스트리머 협업|번체도 지원
```

데이터에서 발견한 실제 수치와 트렌드를 반영해주세요.
"""
    response = call_gemini(client, prompt)
    if response:
        rows = parse_csv_response(response)
        save_csv(rows, output_dir / "01_strategies.csv")
    
    time.sleep(API_DELAY)
    
    # --- 02_kpi_cards.csv ---
    print("   📝 KPI 카드 생성...")
    prompt = f"""
TOP10/TOP50 게임 데이터에서 핵심 KPI 4개를 추출해주세요.

## TOP10 게임 종합 평가 (찜 수 정보 포함)
{raw_data['top10_evaluation']['content']}

## TOP50 게임 목록
{raw_data['top50_games']['content']}

정확히 아래 CSV 형식으로만 출력 (설명 없이 CSV만):

```csv
id,icon,value,label,sublabel,color
1,📊,47개,차트 진입 게임,SNF 기간 중,#0047AB
2,🏆,+70만,총 찜 수 증가,TOP 10 합계,#10B981
3,🎮,70%,멀티플레이 비율,TOP 10 기준,#8B5CF6
4,📈,50%,체험판 제공율,TOP 10 기준,#F59E0B
```

실제 데이터 수치를 계산하여 반영해주세요:
- 찜 증가량 = 참여 후 찜 수 - 참여 전 찜 수
- 멀티플레이 비율 = 멀티플레이 게임 수 / 전체 수
"""
    response = call_gemini(client, prompt)
    if response:
        rows = parse_csv_response(response)
        save_csv(rows, output_dir / "02_kpi_cards.csv")
    
    time.sleep(API_DELAY)
    
    # --- 03_insights.csv ---
    print("   📝 인사이트 생성...")
    prompt = f"""
데이터를 분석하여 개발사가 알아야 할 주요 발견점 4개를 도출해주세요.

## TOP10 게임 종합 평가
{raw_data['top10_evaluation']['content']}

## TOP50 게임 (장르, 체험판, 멀티플레이)
{raw_data['top50_games']['content']}

정확히 아래 CSV 형식으로만 출력:

```csv
id,icon,title,description,border_color
1,🎮,체험판이 성공의 열쇠,TOP 10 중 5개 게임이 체험판 페이지 접속 가능. 체험판을 제공하면 유저 관심도가 크게 높아집니다.,#0047AB
2,👥,멀티플레이가 대세,TOP 10 중 7개가 멀티플레이 게임. 협동/경쟁 요소가 SNF에서 강력한 경쟁력이 됩니다.,#3B82F6
3,⭐,긍정 리뷰가 증명,TOP 10 중 4개가 긍정적 이상 리뷰. 품질이 검증된 게임들이 상위권을 차지했습니다.,#F59E0B
4,🌏,중국어권이 핵심,대부분의 TOP 게임 리뷰 언어 1위가 간체 중국어. 중국 시장 공략이 성공의 필수 요소입니다.,#8B5CF6
```

각 인사이트는:
- 데이터 기반 수치 필수 포함
- 50자 이상의 상세 설명
- 개발사 액션 포인트 암시
"""
    response = call_gemini(client, prompt)
    if response:
        rows = parse_csv_response(response)
        save_csv(rows, output_dir / "03_insights.csv")
    
    time.sleep(API_DELAY)
    
    # --- 04_top5_games.csv ---
    print("   📝 TOP 5 게임 추출...")
    prompt = f"""
TOP10 게임 종합 평가 데이터에서 상위 5개 게임 정보를 추출해주세요.

## 데이터
{raw_data['top10_evaluation']['content']}

## TOP50 데이터 (장르 참조)
{raw_data['top50_games']['content']}

정확히 아래 CSV 형식으로만 출력:

```csv
rank,name,genre,wishlist_increase,wishlist_percent,review_status
1,빈딕투스: 디파잉 페이트,액션 RPG,151605,+25.6%,복합적
2,와일드 게이트,슈팅,59726,+20.1%,확인불가
3,Jump Ship,슈팅,89715,+10.1%,매우 긍정적
4,MIMESIS,공포,53825,+43.2%,확인불가
5,Zoochosis,액션,71933,+26.3%,압도적 긍정
```

게임명 매핑:
- app/3576170 → 빈딕투스: 디파잉 페이트
- app/3504780 → 와일드 게이트
- app/2841820 → Jump Ship
- app/2827200 → MIMESIS
- app/3763830 → Zoochosis
- app/2373990 → 나 혼자만 레벨업: 어라이즈
- app/3105890 → PIONER
- app/3640000 → Holstin

계산: wishlist_increase = 참여 후 찜 수 - 참여 전 찜 수
"""
    response = call_gemini(client, prompt)
    if response:
        rows = parse_csv_response(response)
        save_csv(rows, output_dir / "04_top5_games.csv")
    
    time.sleep(API_DELAY)
    
    # --- 05_chart_summary.csv ---
    print("   📝 차트 성과 요약 생성...")
    prompt = f"""
3종 차트인 횟수 데이터를 분석하여 차트 성과 요약 3개를 도출해주세요.

## 차트인 데이터
{raw_data['chart_integration']['content']}

정확히 아래 CSV 형식으로만 출력:

```csv
id,icon,value,label,description
1,📊,47개,차트 진입,총 47개 게임이 3종 차트에 진입
2,🎯,15회,최다 차트인,Jump Ship이 SNF 기간 중 가장 많이 노출
3,🎮,50%,체험판 비율,TOP 10 중 절반이 체험판 제공
```

데이터에서 실제 수치를 계산해주세요:
- 고유 게임 수 (중복 제외)
- 최다 차트인 게임과 횟수
- 인기 체험판 차트 비율
"""
    response = call_gemini(client, prompt)
    if response:
        rows = parse_csv_response(response)
        save_csv(rows, output_dir / "05_chart_summary.csv")
    
    time.sleep(API_DELAY)
    
    # --- 06_genre_distribution.csv ---
    print("   📝 장르 분포 생성...")
    prompt = f"""
TOP50 게임 데이터에서 장르별 분포를 계산해주세요.

## TOP50 게임 데이터
{raw_data['top50_games']['content']}

정확히 아래 CSV 형식으로만 출력:

```csv
id,icon,genre,percentage,color
1,⚔️,액션 RPG,28%,#0047AB
2,🔫,슈팅,22%,#3B82F6
3,🎲,로그라이크,18%,#8B5CF6
4,👻,공포,15%,#F59E0B
5,📦,기타,17%,#64748B
```

장르 분류:
- 액션 RPG: 액션 RPG, MMORPG, RPG 포함
- 슈팅: 슈팅, FPS, 1인칭 슈팅 포함
- 로그라이크: 로그라이크, 로그라이트 포함
- 공포: 공포, 호러 포함
- 기타: 나머지 모든 장르
"""
    response = call_gemini(client, prompt)
    if response:
        rows = parse_csv_response(response)
        save_csv(rows, output_dir / "06_genre_distribution.csv")
    
    time.sleep(API_DELAY)
    
    # --- 07_snf_guide.csv ---
    print("   📝 SNF 가이드 생성...")
    prompt = f"""
전체 데이터를 종합하여 SNF 참가 준비 체크리스트 4개를 만들어주세요.

## TOP50 게임 (체험판, 멀티플레이 현황)
{raw_data['top50_games']['content']}

정확히 아래 CSV 형식으로만 출력:

```csv
id,icon,title,description,status
1,🎮,체험판 준비,TOP 10의 50%가 체험판 제공,ready
2,🌍,다국어 지원,최소 7개 언어 중국어 간체 필수,ready
3,💬,커뮤니티 구축,Discord YouTube X 필수,ready
4,👥,멀티플레이어,TOP 10의 70%가 멀티 지원,ready
```

데이터 기반으로 구체적인 수치를 반영해주세요.
"""
    response = call_gemini(client, prompt)
    if response:
        rows = parse_csv_response(response)
        save_csv(rows, output_dir / "07_snf_guide.csv")
    
    print("   ✅ Executive Summary 완료!")


# ============================================
# 2. TOP Games 생성
# ============================================
def generate_top_games(client, raw_data):
    """TOP Games 섹션의 모든 CSV 생성"""
    print("\n" + "="*50)
    print("🏆 2/4 TOP Games 생성")
    print("="*50)
    
    output_dir = GITHUB_DATA_DIR / "02_top_games"
    
    # --- 01_kpi_cards.csv ---
    print("\n   📝 KPI 카드 생성...")
    prompt = f"""
TOP10 게임 종합 평가 데이터에서 핵심 KPI 2개를 추출해주세요.

## 데이터
{raw_data['top10_evaluation']['content']}

정확히 아래 CSV 형식으로만 출력:

```csv
id,icon,value,label,sublabel,highlight
1,📈,+70만 찜,SNF 기간 총 찜 수 증가,TOP 10 합계,
2,🚀,+15만 찜,1위 게임 성과,+25.6% 증가,빈딕투스
```

실제 데이터 계산:
- TOP 10 총 찜 증가량 합계
- 1위 게임의 찜 증가량과 증가율
"""
    response = call_gemini(client, prompt)
    if response:
        rows = parse_csv_response(response)
        save_csv(rows, output_dir / "01_kpi_cards.csv")
    
    time.sleep(API_DELAY)
    
    # --- 02_key_findings.csv ---
    print("   📝 핵심 성과 요약 생성...")
    prompt = f"""
TOP 10/50 게임 데이터를 분석하여 핵심 성과 요약 4개를 도출해주세요.

## TOP10 종합 평가
{raw_data['top10_evaluation']['content']}

## TOP50 게임
{raw_data['top50_games']['content']}

정확히 아래 CSV 형식으로만 출력:

```csv
id,icon,title,description,border_color
1,🎮,체험판이 성공의 열쇠,TOP 10 중 5개 게임이 체험판 페이지 접속 가능. 체험판을 제공하면 유저 관심도가 크게 높아집니다.,#0047AB
2,👥,멀티플레이가 대세,TOP 10 중 7개가 멀티플레이 게임. 협동/경쟁 요소가 SNF에서 강력한 경쟁력이 됩니다.,#3B82F6
3,⭐,긍정 리뷰가 증명,TOP 10 중 4개가 긍정적 이상 리뷰. 품질이 검증된 게임들이 상위권을 차지했습니다.,#F59E0B
4,🌏,중국어권이 핵심,대부분의 TOP 게임 리뷰 언어 1위가 간체 중국어. 중국 시장 공략이 성공의 필수 요소입니다.,#8B5CF6
```

데이터 기반 수치를 정확히 반영해주세요.
"""
    response = call_gemini(client, prompt)
    if response:
        rows = parse_csv_response(response)
        save_csv(rows, output_dir / "02_key_findings.csv")
    
    time.sleep(API_DELAY)
    
    # --- 03_top10_table.csv ---
    print("   📝 TOP 10 테이블 생성...")
    prompt = f"""
TOP10 게임 종합 평가 데이터를 테이블 형식으로 정제해주세요.

## 데이터
{raw_data['top10_evaluation']['content']}

## 장르 참조 (TOP50)
{raw_data['top50_games']['content']}

정확히 아래 CSV 형식으로만 출력:

```csv
rank,name,genre,review_status,review_count,wishlist_before,wishlist_after,wishlist_increase,wishlist_percent,top_language
1,빈딕투스: 디파잉 페이트,액션 RPG,복합적,5200,592569,744174,151605,+25.6%,간체 중국어
2,와일드 게이트,슈팅,확인불가,1811,296446,356172,59726,+20.1%,간체 중국어
3,Jump Ship,슈팅,매우 긍정적,3297,891839,981554,89715,+10.1%,간체 중국어
4,MIMESIS,공포,확인불가,0,124569,178394,53825,+43.2%,
5,Zoochosis,액션,압도적 긍정,2207,273244,345177,71933,+26.3%,러시아어
6,나 혼자만 레벨업: 어라이즈,액션 RPG,확인불가,0,516086,589015,72929,+14.1%,
7,PIONER,MMORPG,확인불가,336,283902,366792,82890,+29.2%,러시아어
8,Holstin,공포,압도적 긍정,1197,412647,502928,90281,+21.9%,간체 중국어
9,UFL,스포츠,확인불가,0,234225,254707,20482,+8.7%,
10,Starlight ReVolver,로그라이크,확인불가,0,94879,108088,13209,+13.9%,
```

게임명 매핑 적용하고, 찜 증가량과 증가율 계산해주세요.
"""
    response = call_gemini(client, prompt)
    if response:
        rows = parse_csv_response(response)
        save_csv(rows, output_dir / "03_top10_table.csv")
    
    time.sleep(API_DELAY)
    
    # --- 04_top10_charts.csv ---
    print("   📝 TOP 10 차트 데이터 생성...")
    prompt = f"""
TOP 10 게임의 시각화용 차트 데이터를 생성해주세요.

## TOP10 종합 평가
{raw_data['top10_evaluation']['content']}

정확히 아래 CSV 형식으로만 출력:

```csv
chart_type,label,value,color
wishlist_top5,빈딕투스,151605,#0047AB
wishlist_top5,Jump Ship,89715,#3B82F6
wishlist_top5,Zoochosis,90281,#0047AB
wishlist_top5,PIONER,82890,#8B5CF6
wishlist_top5,나혼자레벨업,72929,#0047AB
review_dist,압도적 긍정,2,#003380
review_dist,매우 긍정적,1,#0047AB
review_dist,복합적,1,#60A5FA
review_dist,확인불가,6,#94A3B8
genre_dist,액션 RPG,2,#003380
genre_dist,슈팅,2,#0047AB
genre_dist,공포,2,#3B82F6
genre_dist,기타,4,#94A3B8
```

데이터에서 실제 수치를 계산해주세요.
"""
    response = call_gemini(client, prompt)
    if response:
        rows = parse_csv_response(response)
        save_csv(rows, output_dir / "04_top10_charts.csv")
    
    time.sleep(API_DELAY)
    
    # --- 05_top50_table.csv ---
    print("   📝 TOP 50 테이블 생성...")
    prompt = f"""
TOP50 게임 데이터를 정제해주세요.

## 데이터
{raw_data['top50_games']['content']}

정확히 아래 CSV 형식으로만 출력 (처음 15개만):

```csv
rank,name,genre,play_type,demo_available,release_date,chart_count,notes
1,빈딕투스: 디파잉 페이트,액션 RPG,멀티,가능,출시예정,14,NEXON
2,와일드 게이트,슈팅,멀티,불가능,2025.07.23,9,1인칭 슈팅
3,Jump Ship,슈팅,멀티,가능,2025년,15,1인칭 슈팅
4,MIMESIS,공포,멀티,불가능,2025년 3분기,6,
5,Zoochosis,액션,싱글,가능,출시예정,9,
```

알려진 게임명은 한글로 매핑해주세요.
"""
    response = call_gemini(client, prompt)
    if response:
        rows = parse_csv_response(response)
        save_csv(rows, output_dir / "05_top50_table.csv")
    
    time.sleep(API_DELAY)
    
    # --- 06_top50_charts.csv ---
    print("   📝 TOP 50 차트 데이터 생성...")
    prompt = f"""
TOP 50 게임의 통계 데이터를 생성해주세요.

## 데이터
{raw_data['top50_games']['content']}

정확히 아래 CSV 형식으로만 출력:

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

실제 데이터 수치를 계산하여 반영해주세요.
"""
    response = call_gemini(client, prompt)
    if response:
        rows = parse_csv_response(response)
        save_csv(rows, output_dir / "06_top50_charts.csv")
    
    print("   ✅ TOP Games 완료!")


# ============================================
# 3. Charts 생성
# ============================================
def generate_charts(client, raw_data):
    """Charts 섹션의 모든 CSV 생성"""
    print("\n" + "="*50)
    print("📊 3/4 Charts 생성")
    print("="*50)
    
    output_dir = GITHUB_DATA_DIR / "03_charts"
    
    # --- 01_kpi_cards.csv ---
    print("\n   📝 KPI 카드 생성...")
    prompt = f"""
3종 차트인 횟수 데이터를 분석하여 핵심 KPI 3개를 추출해주세요.

## 차트 데이터
{raw_data['chart_integration']['content']}

정확히 아래 CSV 형식으로만 출력:

```csv
id,icon,value,label,description,color
1,📊,47개,차트 진입 게임,SNF 기간 중 3종 차트 진입 고유 게임,#0047AB
2,🎯,15회,최다 차트인,Jump Ship이 가장 많이 노출,#10B981
3,🎮,35%,체험판 차트 비율,인기 체험판이 전체 노출의 35%,#8B5CF6
```

데이터에서 실제 수치를 계산해주세요.
"""
    response = call_gemini(client, prompt)
    if response:
        rows = parse_csv_response(response)
        save_csv(rows, output_dir / "01_kpi_cards.csv")
    
    time.sleep(API_DELAY)
    
    # --- 02_key_findings.csv ---
    print("   📝 핵심 발견점 생성...")
    prompt = f"""
차트 데이터를 분석하여 핵심 발견점 4개를 도출해주세요.

## 차트 데이터
{raw_data['chart_integration']['content']}

정확히 아래 CSV 형식으로만 출력:

```csv
id,icon,title,description,color
1,📈,상위 3개 게임이 주도,빈딕투스 나혼자레벨업 Jump Ship 3개 게임이 전체 차트 노출의 25%를 차지했습니다.,#0047AB
2,🎮,체험판이 가장 효과적,인기 체험판 차트가 전체 노출의 35%를 차지해 가장 효과적인 홍보 채널입니다.,#0047AB
3,🎯,10회 이상 진입 = 성공,10회 이상 차트에 오른 게임은 4개뿐. 이 기준을 달성하면 성공적인 SNF입니다.,#0047AB
4,🚀,3종 차트 동시 공략이 핵심,세 종류의 차트에 모두 진입한 게임들이 평균 12회 이상 노출되며 높은 성과를 기록했습니다.,#3B82F6
```
"""
    response = call_gemini(client, prompt)
    if response:
        rows = parse_csv_response(response)
        save_csv(rows, output_dir / "02_key_findings.csv")
    
    time.sleep(API_DELAY)
    
    # --- 03_chart_data.csv ---
    print("   📝 차트별 통계 생성...")
    prompt = f"""
3종 차트의 통계 데이터를 생성해주세요.

## 차트 데이터
{raw_data['chart_integration']['content']}

정확히 아래 CSV 형식으로만 출력:

```csv
chart_type,stat_type,label,value,percentage
인기 체험판,count,총 노출 횟수,52,35%
인기 출시 예정 게임,count,총 노출 횟수,48,32%
떠오르는 출시 예정 게임,count,총 노출 횟수,51,33%
top_games,Jump Ship,차트인 횟수,15,10%
top_games,빈딕투스,차트인 횟수,14,9%
top_games,나혼자레벨업,차트인 횟수,12,8%
top_games,Holstin,차트인 횟수,12,8%
top_games,와일드 게이트,차트인 횟수,9,6%
```

데이터에서 실제 수치를 계산해주세요.
"""
    response = call_gemini(client, prompt)
    if response:
        rows = parse_csv_response(response)
        save_csv(rows, output_dir / "03_chart_data.csv")
    
    time.sleep(API_DELAY)
    
    # --- 04_strategy_cards.csv ---
    print("   📝 차트 전략 카드 생성...")
    prompt = f"""
차트 데이터 분석을 바탕으로 차트 진입 전략 3개를 도출해주세요.

## 차트 데이터
{raw_data['chart_integration']['content']}

정확히 아래 CSV 형식으로만 출력:

```csv
id,icon,title,description,details
1,🎯,체험판 차트 집중 공략,체험판 차트가 가장 효과적,전체 노출의 35% 차지|실제 플레이로 전환율 높음|스트리머 콘텐츠로 바이럴|체험판 품질이 핵심
2,📊,연속 노출로 인지도 확보,3일 연속 차트 유지가 목표,첫날 10위권 진입 필수|매일 업데이트 진행|커뮤니티 활성화|스트리머 협업 분산
3,🚀,3종 차트 동시 진입,모든 차트에 노출되면 평균 12회 이상,체험판+찜 동시 마케팅|출시 예정일 설정|떠오르는 차트는 바이럴|Day 1-2에 집중
```
"""
    response = call_gemini(client, prompt)
    if response:
        rows = parse_csv_response(response)
        save_csv(rows, output_dir / "04_strategy_cards.csv")
    
    time.sleep(API_DELAY)
    
    # --- 05_demo_chart.csv ---
    print("   📝 인기 체험판 차트 상세 생성...")
    prompt = f"""
인기 체험판 차트 데이터만 필터링하여 분석해주세요.

## 차트 데이터 (차트 구분 = 인기 체험판)
{raw_data['chart_integration']['content']}

정확히 아래 CSV 형식으로만 출력:

```csv
rank,name,appearances,best_rank,first_date,last_date,consecutive_days
1,Jump Ship,6,1,2025-06-10,2025-06-16,5
2,빈딕투스,5,1,2025-06-11,2025-06-16,4
3,와일드 게이트,4,1,2025-06-11,2025-06-16,3
4,스텔라 블레이드,3,3,2025-06-11,2025-06-13,3
5,PIONER,3,5,2025-06-11,2025-06-13,2
```

차트 구분이 "인기 체험판"인 데이터만 분석해주세요.
"""
    response = call_gemini(client, prompt)
    if response:
        rows = parse_csv_response(response)
        save_csv(rows, output_dir / "05_demo_chart.csv")
    
    time.sleep(API_DELAY)
    
    # --- 06_popular_upcoming.csv ---
    print("   📝 인기 출시 예정 차트 상세 생성...")
    prompt = f"""
인기 출시 예정 게임 차트 데이터를 분석해주세요.

## 차트 데이터 (차트 구분 = 인기 출시 예정 게임)
{raw_data['chart_integration']['content']}

정확히 아래 CSV 형식으로만 출력:

```csv
rank,name,appearances,best_rank,first_date,last_date
1,나 혼자만 레벨업,6,3,2025-06-10,2025-06-16
2,빈딕투스,4,1,2025-06-12,2025-06-16
3,Dispatch,3,4,2025-06-13,2025-06-16
4,Anvil Empires,4,6,2025-06-10,2025-06-12
5,Holstin,3,9,2025-06-13,2025-06-16
```

차트 구분이 "인기 출시 예정 게임"인 데이터만 분석해주세요.
"""
    response = call_gemini(client, prompt)
    if response:
        rows = parse_csv_response(response)
        save_csv(rows, output_dir / "06_popular_upcoming.csv")
    
    time.sleep(API_DELAY)
    
    # --- 07_trending_upcoming.csv ---
    print("   📝 떠오르는 출시 예정 차트 상세 생성...")
    prompt = f"""
떠오르는 출시 예정 게임 차트 데이터를 분석해주세요.

## 차트 데이터 (차트 구분 = 떠오르는 출시 예정 게임)
{raw_data['chart_integration']['content']}

정확히 아래 CSV 형식으로만 출력:

```csv
rank,name,appearances,best_rank,trend_direction,notes
1,Jump Ship,5,1,상승,6일 연속 상위권
2,Moonlighter 2,3,1,유지,첫날 1위
3,나 혼자만 레벨업,4,4,유지,꾸준한 상위권
4,와일드 게이트,3,7,상승,후반 상승세
5,스텔라 블레이드,2,2,하락,초반 강세
```

차트 구분이 "떠오르는 출시 예정 게임"인 데이터만 분석해주세요.
"""
    response = call_gemini(client, prompt)
    if response:
        rows = parse_csv_response(response)
        save_csv(rows, output_dir / "07_trending_upcoming.csv")
    
    print("   ✅ Charts 완료!")


# ============================================
# 4. Report 생성
# ============================================
def generate_report(client, raw_data):
    """Report 섹션의 모든 CSV 생성"""
    print("\n" + "="*50)
    print("📋 4/4 Report 생성")
    print("="*50)
    
    output_dir = GITHUB_DATA_DIR / "04_report"
    
    # --- 01_checklist.csv ---
    print("\n   📝 체크리스트 생성...")
    prompt = f"""
전체 데이터를 종합하여 SNF 참가 준비 체크리스트 4개를 만들어주세요.

## 결산 페이지 (태그, 언어, 커뮤니티)
{raw_data['report_page']['content']}

## TOP50 게임 (체험판, 멀티플레이)
{raw_data['top50_games']['content']}

정확히 아래 CSV 형식으로만 출력:

```csv
id,icon,title,description,detail_items
1,🎮,체험판 준비,TOP 10의 50%가 체험판 제공,1~2시간 플레이 분량|버그 없는 안정 빌드|SNF 2주 전 준비 완료|핵심 게임플레이 포함
2,🌍,다국어 지원,최소 7개 언어 중국어 간체 필수,영어 100% 필수|중국어 간체 92%|한국어 70% 권장|일본어 68% 고려
3,💬,커뮤니티 구축,Discord YouTube X 필수 3종,Discord 서버 운영|YouTube 채널 활성화|X 계정 주기적 업데이트|Dev Log 주 1회 이상
4,👥,멀티플레이 고려,TOP 10의 70%가 멀티 지원,Co-op 모드 바이럴 효과|친구 초대 시스템|싱글이면 리더보드 추가|스트리머 협업 용이
```
"""
    response = call_gemini(client, prompt)
    if response:
        rows = parse_csv_response(response)
        save_csv(rows, output_dir / "01_checklist.csv")
    
    time.sleep(API_DELAY)
    
    # --- 02_kpi_cards.csv ---
    print("   📝 KPI 카드 생성...")
    prompt = f"""
결산 데이터에서 핵심 KPI 4개를 추출해주세요.

## 결산 페이지
{raw_data['report_page']['content']}

정확히 아래 CSV 형식으로만 출력:

```csv
id,icon,value,label,sublabel,highlight
1,🏷️,18개,평균 태그 수,TOP 10 기준,Action 태그 90%
2,🌍,7.8개,평균 언어 수,인터페이스 기준,중국어 간체 필수
3,💬,4.2개,커뮤니티 채널,평균,Discord/YouTube/X 필수
4,📊,92%,중국어 지원률,간체 기준,최대 시장
```

데이터에서 실제 수치를 계산해주세요.
"""
    response = call_gemini(client, prompt)
    if response:
        rows = parse_csv_response(response)
        save_csv(rows, output_dir / "02_kpi_cards.csv")
    
    time.sleep(API_DELAY)
    
    # --- 03_tags_analysis.csv ---
    print("   📝 태그 분석 생성...")
    prompt = f"""
결산 페이지의 태그 데이터를 분석해주세요.

## 결산 페이지
{raw_data['report_page']['content']}

정확히 아래 CSV 형식으로만 출력:

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
"""
    response = call_gemini(client, prompt)
    if response:
        rows = parse_csv_response(response)
        save_csv(rows, output_dir / "03_tags_analysis.csv")
    
    time.sleep(API_DELAY)
    
    # --- 04_language_support.csv ---
    print("   📝 언어 지원 분석 생성...")
    prompt = f"""
결산 페이지의 언어 지원 데이터를 분석해주세요.

## 결산 페이지
{raw_data['report_page']['content']}

정확히 아래 CSV 형식으로만 출력:

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
"""
    response = call_gemini(client, prompt)
    if response:
        rows = parse_csv_response(response)
        save_csv(rows, output_dir / "04_language_support.csv")
    
    time.sleep(API_DELAY)
    
    # --- 05_community.csv ---
    print("   📝 커뮤니티 분석 생성...")
    prompt = f"""
결산 페이지의 커뮤니티 데이터를 분석해주세요.

## 결산 페이지
{raw_data['report_page']['content']}

정확히 아래 CSV 형식으로만 출력:

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
timeline,실행단계,실시간 Q&A|핫픽스 공지|피드백 수집|매일 커뮤니티 확인,SNF 기간 중,
timeline,정리단계,설문조사|로드맵 공개|지속적 소통|출시일 발표,SNF 종료 후,
```
"""
    response = call_gemini(client, prompt)
    if response:
        rows = parse_csv_response(response)
        save_csv(rows, output_dir / "05_community.csv")
    
    print("   ✅ Report 완료!")


# ============================================
# 메인 실행
# ============================================
def main():
    print("=" * 60)
    print("🚀 SNF Dashboard AI Insights Generator v2.0")
    print(f"   실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 1. Gemini API 설정
    client = setup_gemini()
    if not client:
        return
    
    # 2. 원본 데이터 로드
    raw_data = load_all_raw_data()
    
    loaded_count = sum(1 for v in raw_data.values() if v['path'])
    if loaded_count == 0:
        print("\n❌ 로드된 데이터 파일이 없습니다.")
        print(f"   {RAW_DIR} 폴더에 노션 CSV 파일을 넣어주세요.")
        return
    
    print(f"\n✅ {loaded_count}/{len(RAW_FILES)} 파일 로드 완료")
    
    # 3. 각 섹션별 인사이트 생성
    print("\n" + "="*60)
    print("🤖 AI 인사이트 생성 시작 (총 25개 CSV 파일)")
    print("="*60)
    
    try:
        generate_executive(client, raw_data)
        print("\n   ⏳ API 제한 방지를 위해 30초 대기...")
        time.sleep(30)
        
        generate_top_games(client, raw_data)
        print("\n   ⏳ API 제한 방지를 위해 30초 대기...")
        time.sleep(30)
        
        generate_charts(client, raw_data)
        print("\n   ⏳ API 제한 방지를 위해 30초 대기...")
        time.sleep(30)
        
        generate_report(client, raw_data)
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 4. 결과 요약
    print("\n" + "="*60)
    print("📊 생성 완료!")
    print("="*60)
    
    # 생성된 파일 카운트
    csv_count = 0
    for folder in ["01_executive", "02_top_games", "03_charts", "04_report"]:
        folder_path = GITHUB_DATA_DIR / folder
        if folder_path.exists():
            count = len(list(folder_path.glob("*.csv")))
            csv_count += count
            print(f"   📁 {folder}/: {count}개 CSV")
    
    print(f"\n   ✅ 총 {csv_count}개 CSV 파일 생성")
    print(f"\n💾 저장 위치: {GITHUB_DATA_DIR}")
    
    print("\n🔄 다음 단계:")
    print("   1. 생성된 CSV 파일 확인")
    print("   2. git add . && git commit -m 'Update AI insights' && git push")
    print("   3. 대시보드에서 새로고침하여 확인")
    
    print("\n✨ 완료!")


if __name__ == "__main__":
    main()
