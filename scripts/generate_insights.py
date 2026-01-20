"""
SNF Dashboard AI Insights Generator
===================================
노션에서 내보낸 CSV 파일을 읽고,
Gemini AI를 사용해 인사이트를 생성하여 github_data/ 폴더에 저장합니다.

사용법:
    python generate_insights.py

필요한 환경변수:
    GEMINI_API_KEY: Google Gemini API 키
"""

import os
import csv
import json
import time
from pathlib import Path
from datetime import datetime
import glob

# Gemini API 사용을 위한 라이브러리
try:
    from google import genai
    from google.genai import types
    from google.genai.errors import ClientError
except ImportError:
    print("❌ google-genai 패키지가 설치되지 않았습니다.")
    print("   실행: pip install google-genai")
    exit(1)

# ============================================
# 설정
# ============================================
SCRIPT_DIR = Path(__file__).parent
BASE_DIR = SCRIPT_DIR.parent  # 프로젝트 루트 (2025년 6월 SNF 조사)
GITHUB_DATA_DIR = BASE_DIR / "github_data"
RAW_DIR = GITHUB_DATA_DIR / "raw"  # 노션 CSV 파일들이 있는 폴더

# Gemini 모델 설정
MODEL_NAME = "gemini-2.0-flash"

# API 재시도 설정
MAX_RETRIES = 3
RETRY_DELAY = 60  # 초

# ============================================
# 원본 CSV 파일 매핑 (노션에서 내보낸 파일들)
# ============================================
RAW_FILES = {
    "top10_evaluation": "TOP10 게임 종합 평가*.csv",          # TOP10 게임 상세 정보
    "top10_chart_count": "TOP10 차트인 횟수*.csv",            # TOP10 차트인 횟수
    "top50_games": "가장 많이 플레이한 TOP50 게임*.csv",      # TOP50 게임
    "report_page": "결산 페이지*.csv",                        # 결산 페이지
    "trending_upcoming": "떠오르는 출시 예정 게임*.csv",      # 떠오르는 출시 예정
    "popular_demo": "인기 체험판*.csv",                       # 인기 체험판
    "popular_upcoming": "인기 출시 예정 게임*.csv",           # 인기 출시 예정
    "chart_integration": "전체 장르 - 각 게임별 SNF기간 3종 차트인 횟수*.csv",  # 통합 차트
}


def call_gemini_with_retry(client, prompt):
    """API 호출 (재시도 로직 포함)"""
    for attempt in range(MAX_RETRIES):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )
            return response
        except ClientError as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                if attempt < MAX_RETRIES - 1:
                    wait_time = RETRY_DELAY * (attempt + 1)
                    print(f"   ⏳ API 제한 도달. {wait_time}초 후 재시도... ({attempt + 1}/{MAX_RETRIES})")
                    time.sleep(wait_time)
                else:
                    print(f"   ❌ API 제한으로 실패 (최대 재시도 횟수 초과)")
                    raise
            else:
                raise
    return None


def setup_gemini():
    """Gemini API 설정"""
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ GEMINI_API_KEY 환경변수가 설정되지 않았습니다.")
        print("")
        print("📌 설정 방법:")
        print("   1. Google AI Studio에서 API 키 발급: https://aistudio.google.com/app/apikey")
        print("   2. 환경변수 설정:")
        print('      Windows PowerShell: $env:GEMINI_API_KEY = "your-api-key"')
        print('      Mac/Linux: export GEMINI_API_KEY=your-api-key')
        print("")
        return None
    
    client = genai.Client(api_key=api_key)
    print(f"✅ Gemini API 연결 완료 (모델: {MODEL_NAME})")
    return client


def find_csv_file(pattern):
    """패턴에 맞는 CSV 파일 찾기"""
    search_path = str(RAW_DIR / pattern)
    files = glob.glob(search_path)
    if files:
        # 가장 최근 파일 반환 (여러 개인 경우)
        return Path(max(files, key=os.path.getmtime))
    return None


def read_csv_as_text(file_path, max_lines=50):
    """CSV 파일을 텍스트로 읽기 (최대 줄 수 제한)"""
    if not file_path or not file_path.exists():
        return None
    
    lines = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= max_lines:
                break
            lines.append(line.rstrip())
    
    return '\n'.join(lines)


def read_csv_as_dicts(file_path):
    """CSV 파일을 딕셔너리 리스트로 읽기"""
    if not file_path or not file_path.exists():
        return []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


def load_all_raw_data():
    """모든 원본 CSV 데이터 로드"""
    print("\n📂 원본 데이터 파일 로드 중...")
    raw_data = {}
    
    for key, pattern in RAW_FILES.items():
        file_path = find_csv_file(pattern)
        if file_path:
            raw_data[key] = {
                'path': file_path,
                'text': read_csv_as_text(file_path, max_lines=30),  # 토큰 절약
                'data': read_csv_as_dicts(file_path)
            }
            print(f"   ✅ {key}: {file_path.name} ({len(raw_data[key]['data'])}행)")
        else:
            print(f"   ⚠️ {key}: 파일을 찾을 수 없음 ({pattern})")
            raw_data[key] = {'path': None, 'text': None, 'data': []}
    
    return raw_data


def save_csv(data, output_path):
    """데이터를 CSV로 저장"""
    if not data:
        return False
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        if isinstance(data, list) and len(data) > 0:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
            print(f"   💾 저장: {output_path.name}")
            return True
    return False


def parse_json_response(response_text):
    """AI 응답에서 JSON 파싱"""
    try:
        # JSON 블록 찾기
        if "```json" in response_text:
            json_str = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            json_str = response_text.split("```")[1].split("```")[0].strip()
        else:
            json_str = response_text.strip()
        
        data = json.loads(json_str)
        return data
        
    except (json.JSONDecodeError, IndexError) as e:
        print(f"   ⚠️ JSON 파싱 실패: {e}")
        return None


# ============================================
# 1. Executive Summary 인사이트 생성
# ============================================
def generate_executive_insights(client, raw_data):
    """Executive Summary 인사이트 생성"""
    print("\n🎯 1/4 Executive Summary 생성 중...")
    
    prompt = f"""
당신은 Steam Next Fest 데이터 분석 전문가입니다.
아래 데이터를 분석하여 핵심 인사이트를 생성해주세요.

## TOP10 게임 종합 평가
```csv
{raw_data.get('top10_evaluation', {}).get('text', '데이터 없음')}
```

## TOP50 게임 목록
```csv
{raw_data.get('top50_games', {}).get('text', '데이터 없음')}
```

## 출력 형식 (JSON만 출력, 설명 없이)
```json
{{
  "insights": [
    {{"id": "1", "icon": "🎯", "title": "인사이트 제목", "description": "50자 내외 설명", "border_color": "#0047AB"}},
    {{"id": "2", "icon": "📈", "title": "인사이트 제목", "description": "설명", "border_color": "#10B981"}},
    {{"id": "3", "icon": "🎮", "title": "인사이트 제목", "description": "설명", "border_color": "#8B5CF6"}},
    {{"id": "4", "icon": "💡", "title": "인사이트 제목", "description": "설명", "border_color": "#F59E0B"}}
  ],
  "kpi_cards": [
    {{"id": "total_games", "label": "총 분석 게임", "value": "50", "subtext": "TOP50 기준", "icon": "🎮", "color": "#0047AB"}},
    {{"id": "korean_games", "label": "한국 게임사", "value": "N", "subtext": "개 진출", "icon": "🇰🇷", "color": "#10B981"}},
    {{"id": "top_genre", "label": "1위 장르", "value": "장르명", "subtext": "비율%", "icon": "⚔️", "color": "#8B5CF6"}},
    {{"id": "avg_rating", "label": "평균 리뷰", "value": "상태", "subtext": "TOP10 기준", "icon": "⭐", "color": "#F59E0B"}}
  ],
  "strategies": [
    {{"id": "1", "icon": "🎯", "title": "전략 제목", "description": "전략 설명"}},
    {{"id": "2", "icon": "📊", "title": "전략 제목", "description": "전략 설명"}},
    {{"id": "3", "icon": "🚀", "title": "전략 제목", "description": "전략 설명"}}
  ]
}}
```
"""
    
    try:
        response = call_gemini_with_retry(client, prompt)
        if response and response.text:
            result = parse_json_response(response.text)
            if result:
                if 'insights' in result:
                    save_csv(result['insights'], GITHUB_DATA_DIR / "01_executive" / "03_insights.csv")
                if 'kpi_cards' in result:
                    save_csv(result['kpi_cards'], GITHUB_DATA_DIR / "01_executive" / "02_kpi_cards.csv")
                if 'strategies' in result:
                    save_csv(result['strategies'], GITHUB_DATA_DIR / "01_executive" / "01_strategies.csv")
                return result
    except Exception as e:
        print(f"   ❌ 에러: {e}")
    
    return None


# ============================================
# 2. TOP Games 인사이트 생성
# ============================================
def generate_top_games_insights(client, raw_data):
    """TOP Games 인사이트 생성"""
    print("\n🏆 2/4 TOP Games 인사이트 생성 중...")
    
    prompt = f"""
Steam Next Fest TOP 10/50 게임 데이터를 분석해주세요.

## TOP 10 게임 종합 평가
```csv
{raw_data.get('top10_evaluation', {}).get('text', '데이터 없음')}
```

## TOP 50 게임 목록
```csv
{raw_data.get('top50_games', {}).get('text', '데이터 없음')}
```

## 출력 형식 (JSON만 출력)
```json
{{
  "kpi_cards": [
    {{"id": "top1_wishlists", "label": "1위 찜 수", "value": "744K", "subtext": "+25%", "icon": "🏆", "color": "#FFD700"}},
    {{"id": "multi_ratio", "label": "멀티플레이", "value": "70%", "subtext": "TOP10", "icon": "👥", "color": "#0047AB"}},
    {{"id": "top_genre", "label": "최다 장르", "value": "액션 RPG", "subtext": "N개", "icon": "⚔️", "color": "#10B981"}},
    {{"id": "korean_rank", "label": "한국 게임", "value": "N위", "subtext": "최고순위", "icon": "🇰🇷", "color": "#E11D48"}}
  ],
  "key_findings": [
    {{"id": "1", "icon": "🎯", "title": "발견 제목", "description": "설명", "importance": "high"}},
    {{"id": "2", "icon": "📊", "title": "발견 제목", "description": "설명", "importance": "medium"}}
  ]
}}
```
"""
    
    try:
        response = call_gemini_with_retry(client, prompt)
        if response and response.text:
            result = parse_json_response(response.text)
            if result:
                if 'kpi_cards' in result:
                    save_csv(result['kpi_cards'], GITHUB_DATA_DIR / "02_top_games" / "01_kpi_cards.csv")
                if 'key_findings' in result:
                    save_csv(result['key_findings'], GITHUB_DATA_DIR / "02_top_games" / "02_key_findings.csv")
                return result
    except Exception as e:
        print(f"   ❌ 에러: {e}")
    
    return None


# ============================================
# 3. Charts 인사이트 생성
# ============================================
def generate_charts_insights(client, raw_data):
    """Charts 인사이트 생성"""
    print("\n📊 3/4 Charts 인사이트 생성 중...")
    
    prompt = f"""
Steam 3가지 차트 데이터를 분석해주세요.

## 인기 체험판 차트
```csv
{raw_data.get('popular_demo', {}).get('text', '데이터 없음')}
```

## 인기 출시 예정 게임
```csv
{raw_data.get('popular_upcoming', {}).get('text', '데이터 없음')}
```

## 출력 형식 (JSON만 출력)
```json
{{
  "kpi_cards": [
    {{"id": "demo_count", "label": "인기 체험판", "value": "50+", "subtext": "개 게임", "icon": "🎮", "color": "#0047AB"}},
    {{"id": "korean_support", "label": "한국어 지원", "value": "N", "subtext": "개 게임", "icon": "🇰🇷", "color": "#10B981"}},
    {{"id": "multi_chart", "label": "복수 차트", "value": "N", "subtext": "개 게임", "icon": "📈", "color": "#8B5CF6"}},
    {{"id": "top_tag", "label": "인기 태그", "value": "태그명", "subtext": "최다", "icon": "🏷️", "color": "#F59E0B"}}
  ],
  "key_findings": [
    {{"id": "1", "icon": "🎯", "title": "발견 제목", "description": "설명"}},
    {{"id": "2", "icon": "📊", "title": "발견 제목", "description": "설명"}}
  ]
}}
```
"""
    
    try:
        response = call_gemini_with_retry(client, prompt)
        if response and response.text:
            result = parse_json_response(response.text)
            if result:
                if 'kpi_cards' in result:
                    save_csv(result['kpi_cards'], GITHUB_DATA_DIR / "03_charts" / "01_kpi_cards.csv")
                if 'key_findings' in result:
                    save_csv(result['key_findings'], GITHUB_DATA_DIR / "03_charts" / "02_key_findings.csv")
                return result
    except Exception as e:
        print(f"   ❌ 에러: {e}")
    
    return None


# ============================================
# 4. Report 인사이트 생성
# ============================================
def generate_report_insights(client, raw_data):
    """Report/결산 인사이트 생성"""
    print("\n📋 4/4 Report 인사이트 생성 중...")
    
    prompt = f"""
게임 마케팅/커뮤니티 분석을 해주세요.

## 결산 페이지 (커뮤니티/업데이트 현황)
```csv
{raw_data.get('report_page', {}).get('text', '데이터 없음')}
```

## 출력 형식 (JSON만 출력)
```json
{{
  "kpi_cards": [
    {{"id": "active_community", "label": "활발한 커뮤니티", "value": "N/10", "subtext": "게임", "icon": "💬", "color": "#0047AB"}},
    {{"id": "korean_voice", "label": "한국어 음성", "value": "N", "subtext": "개 게임", "icon": "🎙️", "color": "#10B981"}},
    {{"id": "update_freq", "label": "평균 업데이트", "value": "주 N회", "subtext": "TOP10", "icon": "🔄", "color": "#8B5CF6"}}
  ],
  "checklist": [
    {{"id": "1", "category": "커뮤니티", "item": "체크 항목", "importance": "필수", "description": "설명"}},
    {{"id": "2", "category": "로컬라이징", "item": "체크 항목", "importance": "권장", "description": "설명"}},
    {{"id": "3", "category": "마케팅", "item": "체크 항목", "importance": "필수", "description": "설명"}}
  ]
}}
```
"""
    
    try:
        response = call_gemini_with_retry(client, prompt)
        if response and response.text:
            result = parse_json_response(response.text)
            if result:
                if 'kpi_cards' in result:
                    save_csv(result['kpi_cards'], GITHUB_DATA_DIR / "04_report" / "02_kpi_cards.csv")
                if 'checklist' in result:
                    save_csv(result['checklist'], GITHUB_DATA_DIR / "04_report" / "01_checklist.csv")
                return result
    except Exception as e:
        print(f"   ❌ 에러: {e}")
    
    return None


# ============================================
# 메인 실행
# ============================================
def main():
    print("=" * 60)
    print("🚀 SNF Dashboard AI Insights Generator")
    print(f"   실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 1. Gemini API 설정
    client = setup_gemini()
    if not client:
        return
    
    # 2. 원본 데이터 로드
    raw_data = load_all_raw_data()
    
    # 로드된 파일 확인
    loaded_count = sum(1 for v in raw_data.values() if v['path'])
    if loaded_count == 0:
        print("\n❌ 로드된 데이터 파일이 없습니다.")
        print("   프로젝트 루트에 노션 CSV 파일이 있는지 확인해주세요.")
        return
    
    print(f"\n✅ {loaded_count}/{len(RAW_FILES)} 파일 로드 완료")
    
    # 3. 인사이트 생성 (API 제한 방지를 위해 간격 두기)
    results = {}
    
    # Executive Summary
    results['executive'] = generate_executive_insights(client, raw_data)
    print("   ⏳ API 제한 방지를 위해 20초 대기...")
    time.sleep(20)
    
    # TOP Games
    results['top_games'] = generate_top_games_insights(client, raw_data)
    print("   ⏳ API 제한 방지를 위해 20초 대기...")
    time.sleep(20)
    
    # Charts
    results['charts'] = generate_charts_insights(client, raw_data)
    print("   ⏳ API 제한 방지를 위해 20초 대기...")
    time.sleep(20)
    
    # Report
    results['report'] = generate_report_insights(client, raw_data)
    
    # 4. 결과 요약
    print("\n" + "=" * 60)
    print("📊 생성 완료 요약")
    print("=" * 60)
    
    success_count = sum(1 for v in results.values() if v)
    print(f"   ✅ 성공: {success_count}/4 섹션")
    
    if success_count > 0:
        print(f"\n💾 파일 저장 위치: {GITHUB_DATA_DIR}")
        print("\n🔄 다음 단계:")
        print("   1. 생성된 CSV 파일 확인")
        print("   2. git add . && git commit -m 'Update insights' && git push")
        print("   3. 대시보드에서 새로고침하여 확인")
    
    print("\n✨ 완료!")


if __name__ == "__main__":
    main()
