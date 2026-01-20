# 🤖 AI 인사이트 생성 스크립트 실행 가이드

## 📋 목차
1. [사전 준비](#-사전-준비)
2. [스크립트 실행 방법](#-스크립트-실행-방법)
3. [GitHub 업로드](#-github-업로드)
4. [문제 해결](#-문제-해결)

---

## 🔧 사전 준비

### 1단계: Python 설치 확인

Windows 터미널(또는 PowerShell)에서:
```powershell
python --version
```

결과가 `Python 3.x.x`로 나오면 OK! 
안 나오면 [Python 공식 사이트](https://www.python.org/downloads/)에서 설치하세요.

### 2단계: 필요한 패키지 설치

```powershell
cd "c:\Users\miyeun\2025년 6월 SNF 조사\scripts"
pip install -r requirements.txt
```

### 3단계: Gemini API 키 발급

1. **Google AI Studio 접속**: https://aistudio.google.com/app/apikey
2. **"Create API Key" 클릭**
3. **키 복사** (예: `AIzaSyB1234567890abcdef...`)

### 4단계: API 키 환경변수 설정

**Windows PowerShell에서:**
```powershell
$env:GEMINI_API_KEY = "여기에-복사한-API-키-붙여넣기"
```

⚠️ **주의**: 이 설정은 터미널을 닫으면 사라집니다. 
매번 실행 전에 다시 설정하거나, 아래처럼 영구 설정하세요:

**영구 설정 (선택사항):**
```powershell
[System.Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "여기에-API-키", "User")
```

---

## 🚀 스크립트 실행 방법

### 기본 실행

```powershell
cd "c:\Users\miyeun\2025년 6월 SNF 조사\scripts"
python generate_insights.py
```

### 예상 출력

```
==================================================
🤖 SNF Dashboard AI Insights Generator
==================================================
📅 실행 시간: 2026-06-10 18:00:00
✅ Gemini API 연결 완료 (모델: gemini-1.5-flash)

📂 Raw 데이터 로딩 중...
   ✅ 9/9 파일 로드됨

🧠 AI 인사이트 생성 중...

   [1/4] Executive Summary 인사이트...
   ✅ 01_executive_insights.csv 저장 완료

   [2/4] TOP Games 인사이트...
   ✅ 02_top_games_insights.csv 저장 완료

   [3/4] Charts 인사이트...
   ✅ 03_charts_insights.csv 저장 완료

   [4/4] Report 체크리스트...
   ✅ 04_report_checklist.csv 저장 완료

==================================================
✅ 모든 인사이트 생성 완료!
==================================================
```

---

## 📤 GitHub 업로드

스크립트 실행 후, 생성된 인사이트를 GitHub에 올려야 대시보드에 반영됩니다.

```powershell
cd "c:\Users\miyeun\2025년 6월 SNF 조사"
git add -f github_data/insights/*
git commit -m "Update AI insights - 2026-06-10"
git push origin main
```

그 후 대시보드를 **Ctrl+Shift+R** (강력 새로고침)하면 반영됩니다!

---

## ❓ 문제 해결

### "GEMINI_API_KEY 환경변수가 설정되지 않았습니다"

→ 3단계, 4단계를 다시 확인하세요.

```powershell
# 확인 방법
echo $env:GEMINI_API_KEY
```

### "google-generativeai 패키지가 설치되지 않았습니다"

```powershell
pip install google-generativeai
```

### "파일을 찾을 수 없습니다"

→ `github_data/raw/` 폴더에 CSV 파일이 있는지 확인하세요.
→ `RAW_DATA_GUIDE.md`를 참고해서 데이터를 넣어주세요.

### API 요청 제한 오류

Gemini API는 무료 티어에서 분당 요청 제한이 있습니다.
잠시 후 다시 실행하거나, 유료 플랜을 고려하세요.

---

## 📅 SNF 기간 일일 루틴

1. **오후 6시**: Steam 차트에서 데이터 수집
2. **데이터 입력**: `github_data/raw/` 폴더의 CSV 파일 업데이트
3. **스크립트 실행**: `python generate_insights.py`
4. **GitHub 업로드**: `git add`, `commit`, `push`
5. **확인**: 대시보드 새로고침

---

## 🎯 한 줄 요약

```powershell
# 매일 이것만 실행하면 됩니다!
cd "c:\Users\miyeun\2025년 6월 SNF 조사\scripts"
$env:GEMINI_API_KEY = "your-api-key"
python generate_insights.py
cd ..
git add -f github_data/insights/*
git commit -m "Update AI insights"
git push origin main
```
