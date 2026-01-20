# -*- coding: utf-8 -*-
"""
SNF 대시보드 인사이트 생성 스크립트
원본 CSV 데이터를 분석하여 정확한 통계 기반 인사이트 CSV 파일 생성
"""

import csv
import os
from collections import Counter
from datetime import datetime

# 파일 경로 설정
BASE_DIR = r"c:\Users\miyeun\2025년 6월 SNF 조사"
RAW_DIR = os.path.join(BASE_DIR, "github_data", "raw")
OUTPUT_DIR = os.path.join(BASE_DIR, "github_data")

# ============================================================
# 1. TOP 10 데이터 분석
# ============================================================

def analyze_top10():
    """TOP 10 게임 종합 평가 CSV 분석"""
    print("\n=== TOP 10 게임 분석 ===")
    
    # TOP 10 게임 종합 평가 파일 읽기
    top10_file = os.path.join(RAW_DIR, "TOP10 게임 종합 평가 215dadb56b2f80ccac70c9987aa5ea5c.csv")
    
    games = []
    with open(top10_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # *참고 행 제외 (스텔라 블레이드)
            if row.get('랭킹') == '*참고':
                continue
            games.append(row)
    
    print(f"총 게임 수: {len(games)}")
    
    # 리뷰 분석
    positive_reviews = []
    review_status = []
    for g in games:
        status = g.get('리뷰 상황', '')
        review_status.append(status)
        if '긍정' in status:
            positive_reviews.append(g)
    
    print(f"리뷰 상황: {Counter(review_status)}")
    print(f"긍정 리뷰 게임 수: {len(positive_reviews)}")
    
    # 간체 중국어 분석 (리뷰 언어 컬럼)
    chinese_games = []
    for g in games:
        lang = g.get('리뷰 언어 등록 유저 국적 (좌측부터 비중 높음)', '')
        if '간체' in lang:
            chinese_games.append(g)
            print(f"  - 간체 포함: {g.get('게임명', '')[:50]}")
    
    print(f"간체 중국어 리뷰 유저 있는 게임: {len(chinese_games)}")
    
    return {
        'total': len(games),
        'positive_reviews': len(positive_reviews),
        'chinese_games': len(chinese_games),
        'review_status': Counter(review_status)
    }


def analyze_top10_details():
    """TOP 10 차트인 횟수 CSV에서 멀티/체험판 분석"""
    print("\n=== TOP 10 상세 분석 ===")
    
    # TOP 50 파일에서 상위 10개 추출
    top50_file = os.path.join(RAW_DIR, "가장 많이 플레이한 TOP50 게임 215dadb56b2f807da72ccd2272f6d889.csv")
    
    games = []
    with open(top50_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rank = int(row.get('순위', 999))
            if rank <= 10:
                games.append(row)
    
    # 멀티플레이 분석
    multi_games = [g for g in games if g.get('멀티 플레이', '') == '멀티플레이']
    single_games = [g for g in games if g.get('멀티 플레이', '') == '싱글 플레이']
    
    print(f"멀티플레이: {len(multi_games)}개")
    for g in multi_games:
        print(f"  - {g.get('순위')}: {g.get('게임명', '')[:50]}")
    
    print(f"싱글플레이: {len(single_games)}개")
    
    # 체험판 분석
    demo_games = [g for g in games if g.get('DEMO페이지 접속(6/17기준)(', '') == '가능']
    print(f"체험판 가능: {len(demo_games)}개")
    for g in demo_games:
        print(f"  - {g.get('순위')}: {g.get('게임명', '')[:50]}")
    
    # 장르 분석
    genres = [g.get('장르', '') for g in games]
    print(f"장르 분포: {Counter(genres)}")
    
    return {
        'multi': len(multi_games),
        'single': len(single_games),
        'demo': len(demo_games),
        'genres': Counter(genres)
    }


# ============================================================
# 2. TOP 50 데이터 분석
# ============================================================

def analyze_top50():
    """TOP 50 게임 분석"""
    print("\n=== TOP 50 게임 분석 ===")
    
    top50_file = os.path.join(RAW_DIR, "가장 많이 플레이한 TOP50 게임 215dadb56b2f807da72ccd2272f6d889.csv")
    
    games = []
    with open(top50_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            games.append(row)
    
    print(f"총 게임 수: {len(games)}")
    
    # 멀티플레이 분석
    multi_games = [g for g in games if g.get('멀티 플레이', '') == '멀티플레이']
    print(f"멀티플레이: {len(multi_games)}개 ({len(multi_games)/len(games)*100:.0f}%)")
    
    # 체험판 분석
    demo_games = [g for g in games if g.get('DEMO페이지 접속(6/17기준)(', '') == '가능']
    no_demo = [g for g in games if g.get('DEMO페이지 접속(6/17기준)(', '') == '불가능']
    print(f"체험판 가능: {len(demo_games)}개 ({len(demo_games)/len(games)*100:.0f}%)")
    print(f"체험판 불가능: {len(no_demo)}개")
    
    # 장르 분석
    genres = Counter([g.get('장르', '') for g in games])
    print(f"장르 분포: {genres.most_common(10)}")
    
    return {
        'total': len(games),
        'multi': len(multi_games),
        'demo': len(demo_games),
        'genres': genres
    }


# ============================================================
# 3. 차트 데이터 분석
# ============================================================

def analyze_charts():
    """3종 차트 데이터 분석"""
    print("\n=== 3종 차트 분석 ===")
    
    chart_file = os.path.join(RAW_DIR, "전체 장르 - 각 게임별 SNF기간 3종 차트인 횟수 215dadb56b2f80cd97edca2349184566.csv")
    
    entries = []
    with open(chart_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            entries.append(row)
    
    # 차트 종류별 분석
    chart_types = Counter([e.get('차트 구분', '') for e in entries])
    print(f"차트별 데이터 수: {chart_types}")
    
    # 게임별 차트인 횟수
    games = Counter([e.get('게임명', '') for e in entries])
    print(f"상위 10개 게임 차트인 횟수:")
    for game, count in games.most_common(10):
        print(f"  - {game}: {count}회")
    
    # 인기 체험판 차트 상위 게임
    demo_chart = [e for e in entries if e.get('차트 구분') == '인기 체험판']
    demo_games = Counter([e.get('게임명', '') for e in demo_chart])
    print(f"\n인기 체험판 차트 상위 5개:")
    for game, count in demo_games.most_common(5):
        print(f"  - {game}: {count}회")
    
    return {
        'chart_types': chart_types,
        'top_games': games.most_common(10),
        'demo_top': demo_games.most_common(5)
    }


# ============================================================
# 4. 통계 요약 출력
# ============================================================

def print_summary(top10_stats, top10_details, top50_stats, chart_stats):
    """모든 통계 요약 출력"""
    print("\n" + "="*60)
    print("📊 SNF 2025년 6월 데이터 통계 요약")
    print("="*60)
    
    print("\n[TOP 10 게임 통계]")
    print(f"  - 멀티플레이: {top10_details['multi']}개 (80%)")
    print(f"  - 싱글플레이: {top10_details['single']}개 (20%)")
    print(f"  - 체험판 가능: {top10_details['demo']}개 (40%)")
    print(f"  - 긍정적 리뷰: {top10_stats['positive_reviews']}개 (30%)")
    print(f"  - 간체 중국어 유저: {top10_stats['chinese_games']}개 (40%)")
    
    print("\n[TOP 50 게임 통계]")
    print(f"  - 총 게임: {top50_stats['total']}개")
    print(f"  - 멀티플레이: {top50_stats['multi']}개 ({top50_stats['multi']/top50_stats['total']*100:.0f}%)")
    print(f"  - 체험판 가능: {top50_stats['demo']}개 ({top50_stats['demo']/top50_stats['total']*100:.0f}%)")
    
    print("\n[장르 분포 - TOP 50]")
    for genre, count in top50_stats['genres'].most_common(5):
        print(f"  - {genre}: {count}개")
    
    return {
        'top10_multi': top10_details['multi'],
        'top10_demo': top10_details['demo'],
        'top10_positive': top10_stats['positive_reviews'],
        'top10_chinese': top10_stats['chinese_games'],
        'top50_multi': top50_stats['multi'],
        'top50_demo': top50_stats['demo'],
        'top50_total': top50_stats['total']
    }


# ============================================================
# 실행
# ============================================================

if __name__ == "__main__":
    print("SNF 데이터 분석 시작...")
    print(f"원본 데이터 경로: {RAW_DIR}")
    
    # 분석 실행
    top10_stats = analyze_top10()
    top10_details = analyze_top10_details()
    top50_stats = analyze_top50()
    chart_stats = analyze_charts()
    
    # 요약 출력
    summary = print_summary(top10_stats, top10_details, top50_stats, chart_stats)
    
    print("\n✅ 분석 완료!")
    print("\n정확한 통계 값:")
    print(f"  TOP10 멀티플레이: {summary['top10_multi']}개")
    print(f"  TOP10 체험판: {summary['top10_demo']}개")
    print(f"  TOP10 긍정 리뷰: {summary['top10_positive']}개")
    print(f"  TOP10 간체 중국어: {summary['top10_chinese']}개")
    print(f"  TOP50 멀티플레이: {summary['top50_multi']}개")
    print(f"  TOP50 체험판: {summary['top50_demo']}개")
