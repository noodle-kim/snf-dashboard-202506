# -*- coding: utf-8 -*-
"""
SNF 대시보드 데이터 검증 및 CSV 생성 스크립트
원본 CSV 데이터를 분석하여 정확한 통계 생성
"""

import csv
import os
from collections import Counter

BASE_DIR = r"c:\Users\miyeun\2025년 6월 SNF 조사"
RAW_DIR = os.path.join(BASE_DIR, "github_data", "raw")
OUTPUT_DIR = os.path.join(BASE_DIR, "github_data")

# ============================================================
# 1. 원본 데이터 로드
# ============================================================

def load_top10_evaluation():
    """TOP10 게임 종합 평가 로드"""
    file_path = os.path.join(RAW_DIR, "TOP10 게임 종합 평가 215dadb56b2f80ccac70c9987aa5ea5c.csv")
    games = []
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('랭킹') == '*참고':
                continue
            
            before = row.get('참여 전 찜 수(GDCo) ', '0').replace(',', '').strip()
            after = row.get('참여 후 찜 수(GDCo)', '0').replace(',', '').strip()
            
            before_num = int(before) if before else 0
            after_num = int(after) if after else 0
            increase = after_num - before_num
            pct = (increase / before_num * 100) if before_num > 0 else 0
            
            games.append({
                'rank': int(row.get('랭킹', 0)),
                'url': row.get('게임명', ''),
                'review_status': row.get('리뷰 상황', ''),
                'review_count': row.get('리뷰 수', ''),
                'review_lang': row.get('리뷰 언어 등록 유저 국적 (좌측부터 비중 높음)', ''),
                'wishlist_before': before_num,
                'wishlist_after': after_num,
                'wishlist_increase': increase,
                'wishlist_pct': pct
            })
    return games


def load_top50_games():
    """TOP50 게임 로드"""
    file_path = os.path.join(RAW_DIR, "가장 많이 플레이한 TOP50 게임 215dadb56b2f807da72ccd2272f6d889.csv")
    games = []
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            games.append({
                'rank': int(row.get('순위', 0)),
                'url': row.get('게임명', ''),
                'demo': row.get('DEMO페이지 접속(6/17기준)(', ''),
                'multiplayer': row.get('멀티 플레이', ''),
                'genre': row.get('장르', ''),
                'release': row.get('정식 출시일', ''),
                'chart_count': row.get('차트인 횟수', '')
            })
    return games


def load_chart_data():
    """3종 차트 데이터 로드"""
    file_path = os.path.join(RAW_DIR, "전체 장르 - 각 게임별 SNF기간 3종 차트인 횟수 215dadb56b2f80cd97edca2349184566.csv")
    entries = []
    with open(file_path, 'r', encoding='utf-8-sig') as f:  # utf-8-sig로 BOM 처리
        reader = csv.DictReader(f)
        for row in reader:
            entries.append({
                'game': row.get('게임명', ''),
                'date': row.get('날짜', ''),
                'rank': int(row.get('랭킹', 0)) if row.get('랭킹', '').isdigit() else 0,
                'chart_type': row.get('차트 구분', '')
            })
    return entries


# ============================================================
# 2. 통계 계산
# ============================================================

def calculate_stats():
    """모든 통계 계산"""
    top10_eval = load_top10_evaluation()
    top50_games = load_top50_games()
    chart_data = load_chart_data()
    
    # TOP 10 상세 (TOP 50에서 상위 10개)
    top10_from_50 = [g for g in top50_games if g['rank'] <= 10]
    
    stats = {}
    
    # TOP 10 통계
    stats['top10_multi'] = len([g for g in top10_from_50 if g['multiplayer'] == '멀티플레이'])
    stats['top10_single'] = len([g for g in top10_from_50 if g['multiplayer'] == '싱글 플레이'])
    stats['top10_demo'] = len([g for g in top10_from_50 if g['demo'] == '가능'])
    stats['top10_no_demo'] = len([g for g in top10_from_50 if g['demo'] == '불가능'])
    
    # TOP 10 리뷰 통계
    positive_reviews = [g for g in top10_eval if '긍정' in g['review_status']]
    stats['top10_positive_review'] = len(positive_reviews)
    
    # TOP 10 간체 중국어
    chinese_games = [g for g in top10_eval if '간체' in g.get('review_lang', '')]
    stats['top10_chinese'] = len(chinese_games)
    
    # TOP 10 찜 수 통계
    stats['top10_total_wishlist_increase'] = sum(g['wishlist_increase'] for g in top10_eval)
    stats['top10_avg_wishlist_increase'] = stats['top10_total_wishlist_increase'] // 10
    
    # TOP 10 차트인 횟수 평균
    chart_counts = []
    for g in top10_from_50:
        if g['chart_count'] and g['chart_count'].isdigit():
            chart_counts.append(int(g['chart_count']))
    stats['top10_avg_chart_count'] = sum(chart_counts) / len(chart_counts) if chart_counts else 0
    
    # TOP 50 통계
    stats['top50_multi'] = len([g for g in top50_games if g['multiplayer'] == '멀티플레이'])
    stats['top50_demo'] = len([g for g in top50_games if g['demo'] == '가능'])
    stats['top50_total'] = len(top50_games)
    
    # 장르 분포
    genres = Counter([g['genre'] for g in top50_games])
    stats['genres'] = genres.most_common(10)
    
    # 차트 데이터 통계
    stats['chart_total_entries'] = len(chart_data)
    chart_types = Counter([e['chart_type'] for e in chart_data])
    stats['chart_types'] = dict(chart_types)
    
    # 게임별 차트인 횟수
    game_chart_counts = Counter([e['game'] for e in chart_data])
    stats['top_chart_games'] = game_chart_counts.most_common(10)
    
    # 각 차트별 1위 기록
    for game_name, count in game_chart_counts.most_common(5):
        game_entries = [e for e in chart_data if e['game'] == game_name]
        first_places = {}
        for ct in ['인기 체험판', '인기 출시 예정 게임', '떠오르는 출시 예정 게임']:
            first_count = len([e for e in game_entries if e['chart_type'] == ct and e['rank'] == 1])
            if first_count > 0:
                first_places[ct] = first_count
        stats[f'first_places_{game_name}'] = first_places
    
    return stats


# ============================================================
# 3. 검증 및 출력
# ============================================================

def print_verification():
    """검증 결과 출력"""
    stats = calculate_stats()
    
    print("=" * 60)
    print("📊 SNF 2025년 6월 데이터 검증 결과")
    print("=" * 60)
    
    print("\n[TOP 10 통계]")
    print(f"  멀티플레이: {stats['top10_multi']}개 ({stats['top10_multi']*10}%)")
    print(f"  싱글플레이: {stats['top10_single']}개 ({stats['top10_single']*10}%)")
    print(f"  체험판 가능: {stats['top10_demo']}개 ({stats['top10_demo']*10}%)")
    print(f"  체험판 불가: {stats['top10_no_demo']}개")
    print(f"  긍정 리뷰: {stats['top10_positive_review']}개 ({stats['top10_positive_review']*10}%)")
    print(f"  간체 중국어 유저: {stats['top10_chinese']}개 ({stats['top10_chinese']*10}%)")
    print(f"  총 찜 수 증가: {stats['top10_total_wishlist_increase']:,} ({stats['top10_total_wishlist_increase']/10000:.1f}만)")
    print(f"  평균 찜 증가: {stats['top10_avg_wishlist_increase']:,}")
    print(f"  평균 차트인 횟수: {stats['top10_avg_chart_count']:.1f}회")
    
    print("\n[TOP 50 통계]")
    print(f"  멀티플레이: {stats['top50_multi']}개 ({stats['top50_multi']*2}%)")
    print(f"  체험판 가능: {stats['top50_demo']}개 ({stats['top50_demo']*2}%)")
    
    print("\n[차트 통계]")
    print(f"  총 차트 노출: {stats['chart_total_entries']}회")
    for ct, count in stats['chart_types'].items():
        print(f"  - {ct}: {count}회")
    
    print("\n[차트인 횟수 TOP 5]")
    for game, count in stats['top_chart_games'][:5]:
        first_places = stats.get(f'first_places_{game}', {})
        first_str = ', '.join([f"{k[:4]}1위:{v}회" for k, v in first_places.items()])
        print(f"  - {game}: {count}회 {f'({first_str})' if first_str else ''}")
    
    print("\n[장르 분포 TOP 5]")
    for genre, count in stats['genres'][:5]:
        print(f"  - {genre}: {count}개")
    
    return stats


# ============================================================
# 4. CSV 파일 생성
# ============================================================

def generate_csv_files(stats):
    """정확한 통계 기반 CSV 파일 생성"""
    
    # 1. Executive Summary KPI Cards
    kpi_csv = os.path.join(OUTPUT_DIR, "01_executive", "02_kpi_cards.csv")
    with open(kpi_csv, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'icon', 'value', 'label', 'sublabel', 'color'])
        writer.writerow([1, '📊', f'{stats["chart_total_entries"]}회', '총 차트 노출', 'SNF 기간 3종 차트', '#0047AB'])
        writer.writerow([2, '🏆', f'+{stats["top10_total_wishlist_increase"]/10000:.1f}만 찜', '총 찜 수 증가', 'TOP 10 합계', '#10B981'])
        writer.writerow([3, '🎮', f'{stats["top10_multi"]*10}%', '멀티플레이 비율', 'TOP 10 기준', '#8B5CF6'])
        writer.writerow([4, '📈', f'{stats["top10_demo"]*10}%', '체험판 제공율', 'TOP 10 기준', '#F59E0B'])
    print(f"✅ 생성: {kpi_csv}")
    
    # 2. Chart Summary (Executive)
    chart_summary_csv = os.path.join(OUTPUT_DIR, "01_executive", "05_chart_summary.csv")
    top_game, top_count = stats['top_chart_games'][0]
    with open(chart_summary_csv, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'icon', 'value', 'label', 'description'])
        writer.writerow([1, '📊', f'{stats["chart_total_entries"]}회', '총 차트 노출', f'3종 차트 총 노출 횟수'])
        writer.writerow([2, '🎯', f'{top_count}회', '최다 차트인', f'{top_game}이 SNF 기간 중 가장 많이 노출'])
        writer.writerow([3, '🎮', f'{stats["top10_demo"]*10}%', '체험판 비율', f'TOP 10 중 {stats["top10_demo"]}개 게임이 체험판 제공'])
    print(f"✅ 생성: {chart_summary_csv}")
    
    # 3. Charts Section KPI
    charts_kpi_csv = os.path.join(OUTPUT_DIR, "03_charts", "01_kpi_cards.csv")
    
    # Champion 게임의 1위 기록 확인
    champion_tags = []
    first_places = stats.get(f'first_places_{top_game}', {})
    if '인기 출시 예정 게임' in first_places:
        champion_tags.append('인기 출시 예정 1위')
    if '떠오르는 출시 예정 게임' in first_places:
        champion_tags.append('떠오르는 출시 예정 1위')
    if '인기 체험판' in first_places:
        champion_tags.append('인기 체험판 1위')
    
    tags_str = '|'.join(champion_tags) if champion_tags else ''
    
    with open(charts_kpi_csv, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'icon', 'value', 'label', 'description', 'color', 'game_name', 'tags'])
        writer.writerow([1, '📊', f'{stats["chart_total_entries"]}회', '총 차트 노출', 'SNF 기간 3종 차트 총 노출', '#0047AB', '', ''])
        writer.writerow([2, '🎯', f'{top_count}회 차트 진입', '최다 차트인 게임', top_game, '#10B981', top_game, tags_str])
        writer.writerow([3, '🎮', '33%', '차트 균등 배분', '각 차트별 동일한 비율', '#8B5CF6', '', ''])
    print(f"✅ 생성: {charts_kpi_csv}")
    
    print("\n✅ 모든 CSV 파일 생성 완료!")


# ============================================================
# 실행
# ============================================================

if __name__ == "__main__":
    stats = print_verification()
    print("\n" + "=" * 60)
    print("CSV 파일 생성 중...")
    generate_csv_files(stats)
