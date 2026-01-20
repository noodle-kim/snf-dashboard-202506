# Editorial Light Theme 디자인 가이드
> Steam SNF 대시보드 - 2026년 1월 기준

---

## 1. 색상 팔레트

### Primary Colors
| 용도 | 색상 | HEX | Tailwind |
|------|------|-----|----------|
| 배경 (메인) | Stone | `#EBEAE6` | `bg-[#EBEAE6]` |
| 배경 (사이드바) | Off-white | `#F5F4F0` | `bg-[#F5F4F0]` |
| 텍스트 (메인) | Navy/Slate | `#0F172A` | `text-slate-900` |
| 텍스트 (보조) | Slate | `#64748B` | `text-slate-500` |
| 액센트 | Cobalt Blue | `#0047AB` | `text-[#0047AB]` |
| 액센트 (hover) | Deep Cobalt | `#003380` | `hover:bg-[#003380]/15` |

### Dark Section Colors (인사이트 영역)
| 용도 | 색상 | HEX | Tailwind |
|------|------|-----|----------|
| 배경 | Navy | `#0F172A` | `bg-[#0F172A]` |
| 텍스트 (메인) | White | `#FFFFFF` | `text-white` |
| 텍스트 (보조) | Slate Light | `#CBD5E1` | `text-slate-300` |
| 액센트 | Light Blue | `#60A5FA` | `text-[#60A5FA]` |
| 구분선 | White 20% | - | `border-white/20` |

### Chart Colors (Chart.js)
```javascript
const chartColors = {
    primary: '#0047AB',      // Cobalt Blue
    secondary: '#3B82F6',    // Blue 500
    tertiary: '#60A5FA',     // Blue 400
    quaternary: '#93C5FD',   // Blue 300
    grid: '#E2E8F0',         // Slate 200
    text: '#475569'          // Slate 600
};
```

---

## 2. 타이포그래피

### 폰트 패밀리
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
```

### 텍스트 스타일

| 용도 | 클래스 | 예시 |
|------|--------|------|
| 페이지 제목 | `text-3xl font-bold text-slate-900` | 🏆 TOP 게임 분석 |
| 섹션 제목 | `text-sm font-bold mb-4 text-slate-900` | 📈 차트 성과 요약 |
| 라벨 (대문자) | `text-[10px] font-bold uppercase tracking-widest text-slate-500` | CHART ENTRY |
| KPI 숫자 (대) | `text-4xl font-extrabold text-slate-900 tracking-tight` | 47 |
| KPI 숫자 (중) | `text-3xl font-extrabold text-slate-900 tracking-tight` | 빈딕투스 |
| KPI 숫자 (소) | `text-lg font-extrabold text-slate-900` | 744K |
| 본문 | `text-sm text-slate-600` | 설명 텍스트 |
| 보조 텍스트 | `text-xs text-slate-500` | 부가 정보 |

### Sub-text 스타일 (CSS 정의 필요)
```css
.sub-text {
    font-size: 11px;
    color: #64748b;
    padding-top: 8px;
    margin-top: 8px;
    border-top: 1px solid #e2e8f0;
}
```

---

## 3. 레이아웃 컴포넌트

### 3.1 Content Panel (기본 컨테이너)
**원칙**: 배경 없음, 투명하게
```html
<div class="content-panel p-8">
    <!-- 컨텐츠 -->
</div>
```
```css
.content-panel {
    background: transparent;
    border-radius: 0;
    box-shadow: none;
}
```

### 3.2 KPI 그리드 (핵심 요약 스타일)
**원칙**: gap-0, 외곽 border, 내부 border-r로 구분

**라벨 스타일 (위쪽 영문)**:
- `text-[11px] font-medium uppercase tracking-wide text-slate-900 opacity-50 mb-3`
- reference의 sub-text 스타일 적용 (연한 네이비, 반투명)

**숫자 스타일**:
- `text-4xl font-extrabold text-slate-900 mb-1 tracking-tight`

**설명 텍스트 스타일 (아래쪽 한글)**:
- `sub-text` 클래스 + `font-size: 13px` (기본 11px에서 +2px)
- 회색톤 유지 (`#64748b`)

```html
<div class="grid grid-cols-1 md:grid-cols-4 gap-0 border border-slate-300">
    <div class="p-6 border-r border-b border-slate-300 hover:bg-slate-100/50 transition-all">
        <div class="text-[11px] font-medium uppercase tracking-wide text-slate-900 opacity-50 mb-3">Total Games</div>
        <p class="text-4xl font-extrabold text-slate-900 mb-1 tracking-tight">2,600</p>
        <div class="sub-text" style="font-size: 13px;">총 SNF 참가 게임 · +16%</div>
    </div>
    <!-- 마지막 셀은 border-r 없음 -->
</div>
```

### 3.3 발견점 카드 (border-l 강조)
**원칙**: 왼쪽 4px 강조선, 아이콘+제목+설명 구조
```html
<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    <div class="bg-transparent p-5 border-b border-slate-300 rounded-none border-l-4 border-[#0047AB] hover:bg-[#003380]/15 transition-all">
        <div class="flex items-start gap-3">
            <span class="text-2xl">🎮</span>
            <div>
                <h4 class="font-bold text-[#0047AB] mb-1">제목</h4>
                <p class="text-sm text-slate-600">설명 텍스트</p>
            </div>
        </div>
    </div>
</div>
```

### 3.4 2열 그리드 (장르분포 + 가이드)
**원칙**: gap-0, 외곽 border, 가운데 border-r
```html
<div class="grid grid-cols-1 md:grid-cols-2 gap-0 border border-slate-300">
    <div class="p-6 border-r border-slate-300">
        <!-- 왼쪽 컨텐츠 -->
    </div>
    <div class="p-6">
        <!-- 오른쪽 컨텐츠 -->
    </div>
</div>
```

---

## 4. 인사이트 섹션 (다크 영역)

### 4.1 성공 전략 박스
**원칙**: 다크 네이비 배경, 세로 구분선, 흰색 텍스트 + 코발트 배경 라벨
```html
<div class="bg-[#0F172A] p-6 rounded-none mb-8">
    <h4 class="text-lg font-bold mb-4 text-white flex items-center gap-2">
        <span>🚀</span> 제목
    </h4>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-0">
        <div class="p-4 md:border-r md:border-white/20">
            <h5 class="font-bold mb-3">
                <span class="text-white bg-[#0047AB] px-2 py-0.5 font-medium">라벨 텍스트</span>
            </h5>
            <ul class="text-sm text-slate-300 space-y-1.5">
                <li>• 항목 1</li>
                <li>• 항목 2</li>
            </ul>
        </div>
    </div>
</div>
```

### 4.2 하이라이트 라벨 (텍스트 강조 스타일)
**원칙**: reference의 "MODERN GRID" 스타일 - 흰색 텍스트 + 코발트 블루 배경
```html
<!-- 다크 배경에서 (성공 전략 라벨 등) -->
<span class="text-white bg-[#0047AB] px-2 py-0.5 font-medium">라벨 텍스트</span>

<!-- 라이트 배경에서 -->
<span class="text-white bg-[#0047AB] px-2 py-0.5 font-medium">라벨 텍스트</span>
```

**CSS 참고 (reference.html)**:
```css
.highlight {
    color: #fff;
    background: var(--color-cobalt);  /* #0047AB */
    padding: 2px 8px;
    font-weight: 500;
    border-radius: 0;
}
```

### 4.3 핵심 성과 요약 (인사이트 박스)
```html
<div class="bg-[#0F172A] p-6 rounded-none">
    <h4 class="text-sm font-bold mb-4 text-[#60A5FA] flex items-center gap-2">
        <span>💡</span> 핵심 성과 요약
    </h4>
    <ul class="text-slate-300 text-sm space-y-2">
        <li class="flex items-start gap-2">
            <span class="text-[#60A5FA]">→</span>
            <span>내용</span>
        </li>
    </ul>
</div>
```

---

## 5. 버튼 스타일

### 5.1 서브탭 네비게이션
**원칙**: 하단 border로 구분, active 상태는 코발트 블루 border-b-2
```html
<div class="flex gap-0 mb-6 border-b border-slate-300">
    <!-- Active 탭 -->
    <button class="text-sm font-bold px-6 py-3 transition-all border-b-2 border-[#0047AB] text-[#0047AB]">
        TOP 10 종합 평가
    </button>
    <!-- Inactive 탭 -->
    <button class="text-sm font-bold px-6 py-3 transition-all border-b-2 border-transparent text-slate-500 hover:text-[#0047AB]">
        TOP 50 플레이 순위
    </button>
</div>
```

**탭 스타일 요약**:
| 상태 | 폰트 | 색상 | Border |
|------|------|------|--------|
| Active | `text-sm font-bold` | `text-[#0047AB]` | `border-b-2 border-[#0047AB]` |
| Inactive | `text-sm font-bold` | `text-slate-500` | `border-b-2 border-transparent` |

### 5.2 Primary Button (자세히 보기)
```html
<button class="text-[12px] font-bold uppercase tracking-widest px-4 py-2 text-[#0047AB] border border-[#0047AB]/30 hover:bg-[#0047AB]/10 rounded-none transition-all flex items-center gap-2">
    자세히 보기 <span>→</span>
</button>
```

### 사이드바 네비게이션
```html
<button class="nav-btn w-full text-left px-4 py-3 rounded-none text-slate-600 hover:bg-[#0047AB]/10 hover:text-[#0047AB] transition-all flex items-center gap-3">
    <span>아이콘</span> 메뉴명
</button>

<!-- Active 상태 -->
<button class="nav-btn active ... bg-[#0047AB]/10 text-[#0047AB] border-l-2 border-[#0047AB]">
```

---

## 6. 테이블/데이터 그리드

### 기본 테이블
```html
<table class="data-table w-full">
    <thead>
        <tr>
            <th class="text-center">순위</th>
            <th>게임명</th>
            <th>장르</th>
            <th>리뷰 상황</th>
            <th class="text-right">찜 수 증가</th>
        </tr>
    </thead>
    <tbody>
        <tr class="border-b border-slate-200 hover:bg-slate-100/50 transition-all">
            <td class="text-center font-bold text-[#0047AB]">1</td>
            <td class="font-semibold">게임명</td>
            <td>액션 RPG</td>
            <td><span class="badge badge-positive">매우 긍정적</span></td>
            <td class="text-right text-[#0047AB]">+151,605</td>
        </tr>
    </tbody>
</table>
```

### 가로 막대 그래프 (장르 분포)
**원칙**: 그라데이션 없음, slate 단색 계열
```html
<div class="genre-bar-item">
    <div class="flex justify-between items-center mb-1">
        <span class="text-sm font-medium text-slate-900">🎮 액션 RPG</span>
        <span class="text-sm font-bold text-slate-700">28%</span>
    </div>
    <div class="w-full bg-slate-200 h-2 overflow-hidden">
        <div class="h-full bg-slate-900 transition-all duration-1000" style="width: 28%;"></div>
    </div>
</div>
```
색상 순서: `bg-slate-900` → `bg-slate-700` → `bg-slate-600` → `bg-slate-500` → `bg-slate-400`

---

## 7. 배지/태그

### 배지 스타일 (CSS)
```css
.badge {
    display: inline-block;
    padding: 0;
    font-size: 12px;
    font-weight: 600;
    background: transparent;
    border: none;
}

.badge-positive {
    color: #0047AB;  /* 코발트 블루 */
}

.badge-negative {
    color: #DC2626;  /* 빨간색 */
}

.badge-neutral {
    color: #64748b;  /* 슬레이트 그레이 */
}
```

### 텍스트 강조 배지 (리뷰 상황, 스팀DB 랭크)
**원칙**: 네모 박스 없음, 색상 + 굵기로만 강조
```html
<!-- 긍정적 -->
<span class="badge badge-positive">매우 긍정적</span>
<span class="badge badge-positive">31위</span>

<!-- 중립/확인불가 -->
<span class="badge badge-neutral">확인불가</span>
<span class="badge badge-neutral">복합적</span>
```

### 체험판 배지 (네모 박스 스타일)
**원칙**: 체험판 열만 네모 박스로 시각적 구분
```css
.badge-demo {
    padding: 4px 10px;
    font-size: 11px;
    font-weight: 700;
}

.badge-demo.badge-positive {
    background: rgba(0, 71, 171, 0.1);
    color: #0047AB;
    border: 1px solid #0047AB;
}

.badge-demo.badge-neutral {
    background: rgba(100, 116, 139, 0.1);
    color: #64748b;
    border: 1px solid #94a3b8;
}
```
```html
<!-- 체험판 있음 -->
<span class="badge badge-demo badge-positive">✓</span>

<!-- 체험판 없음 -->
<span class="badge badge-demo badge-neutral">✗</span>
```

### 순위 표시
```html
<!-- 1위 (강조) -->
<span class="text-2xl font-extrabold text-[#0047AB]">1</span>

<!-- 2위 이하 -->
<span class="text-xl font-bold text-slate-700">2</span>
```

---

## 8. 페이지별 적용 체크리스트

각 페이지 작업 시 아래 순서로 확인:

### Step 1: 기본 구조
- [ ] `content-panel` 배경 투명 처리
- [ ] 페이지 제목 스타일 (`text-3xl font-bold text-slate-900`)
- [ ] 섹션 구분 (gap-0, border 라인)

### Step 2: 섹션 제목
- [ ] `text-sm font-bold mb-4 text-slate-900` 통일
- [ ] 이모지 + 텍스트 구조
- [ ] "자세히 보기" 버튼 스타일

### Step 3: 데이터 표시
- [ ] KPI 그리드 → gap-0, border 라인, uppercase 라벨
- [ ] 테이블 → slate 계열 border, hover 효과
- [ ] 차트 → Cobalt Blue 계열 색상

### Step 4: 인사이트 영역
- [ ] 다크 섹션 → `bg-[#0F172A]`
- [ ] 하이라이트 라벨 → `text-[#60A5FA] font-semibold` (네모 박스 ❌)
- [ ] 리스트 → `text-slate-300`, `→` 화살표

### Step 5: 인터랙션
- [ ] hover 효과 → `hover:bg-slate-100/50` 또는 `hover:bg-[#003380]/15`
- [ ] 버튼 → uppercase, tracking-widest, border
- [ ] transition-all 적용

---

## 9. 금지 사항 (하지 말 것)

| ❌ 하지 말 것 | ✅ 대신 이렇게 |
|--------------|---------------|
| 그라데이션 배경 | 단색 또는 투명 |
| 둥근 모서리 (rounded-lg) | 직각 (rounded-none) |
| 그림자 (shadow) | border 라인만 |
| Steam Blue (#1a9fff) | Cobalt Blue (#0047AB) |
| 카드 배경색 | 투명 + border |
| gap-4 분리된 그리드 | gap-0 + border 연결 |
| 배지 네모 박스 (텍스트용) | 색상 + 굵기로 강조 |
| 초록색 차트 | 블루 계열 차트 |

---

## 10. 적용 완료 페이지

| 페이지 | 상태 | 비고 |
|--------|------|------|
| Executive Summary | ✅ 완료 | 성공 전략, 주요 발견점, TOP5, 차트 성과 요약 등 |
| TOP 게임 분석 | ✅ 완료 | KPI 그리드, 핵심 성과 요약, 테이블 배지 스타일 |
| 차트 성과 분석 | ✅ 완료 | KPI 그리드, 핵심 성과 요약, 3종 차트 분석 |
| SNF 결산 리포트 | ✅ 완료 | 성공 체크리스트, 태그/언어/커뮤니티 탭 |

---

## 11. 파일 구조

```
📁 2025년 6월 SNF 조사/
├── dashboard_editorial.html    ← 메인 작업 파일
├── reference.html              ← 디자인 참조 파일
├── DESIGN_GUIDE.md            ← 이 문서
└── [CSV 데이터 파일들]
```

---

*Last Updated: 2026-01-19 (Editorial Light Theme v2 - 전체 페이지 완료)*
