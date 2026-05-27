# HEXAD/EEG — EEG-anchor (Framing D) anima ↔ 사람 뇌 cross-validation SSOT

> User directive 2026-05-18: "/HEXAD/EEG 기록". §19 EEG-anchor 자산을 anima 내부 SSOT 로 정착 (g_doc_consolidation — HEXAD/* 내부, root docs/* 금지).
>
> **이 디렉토리 = anima-side EEG-anchor SSOT 골격.** §19 의 research 본문·F-CT-3 falsifier·step 결과는 `HEXAD/CHAT/RESEARCH.md §19` + `state/eeg_anchor_s19_2026_05_18/` 가 SSOT (중복 보관 0, 참조만 — KOSMOS-FORMAT.md pointer 패턴과 동일).

## 0. 한 줄 — EEG-anchor 가 뭔가

```
🧠 EEG-anchor — "사람 뇌 거울로 anima 검증"

- 하는 일: 같은 자극(영상)을 [사람 뇌 EEG 실측] · [anima 속 physics 상태] · [TRIBE 예측 BOLD]
           세 거울에 비춰, 세 그림자가 같은 latent 면 = anima 가 사람 뇌와 같은 데 anchor
- 비유: 영화를 세 사람(나·anima·예측모델)이 보고 "뇌가 이렇게 켜졌다" 가 다 일치하는지
- vs §17 (자기 거울 1개) : EEG-anchor = 외부 ground-truth(사람 뇌) 거울 추가
```

## 1. Framing D — 3축 (이제 다 실재)

| 축 | 정체 | 실재 근거 |
|---|---|---|
| **axis A** | OpenBCI 16ch EEG 실측 | user 실보유 + 녹음 경험 있음 (2026-05-18 확인) |
| **axis B** | anima §17 physics-channel (Ψ_direction / tension, Engine A⇄G Law-71) | `state/physics_channel_probe_s17_2026_05_18/` 추출 검증 — garbled-text 우회 |
| **axis C** | TRIBE v2 예측 cortical BOLD (fsaverage5 ~20k vertex) | `references/tribev2/` vendored + facebook/tribev2 HF weights |

**F-CT-3 사전등록 falsifier** (`references/tribev2/ANIMA_INTEGRATION_PROPOSAL_ADDENDUM_2026_05_02_EN.md §5`):
> axis A EEG envelope ↔ axis C TRIBE BOLD median vertex Pearson **r ≥ 0.5** → PASS (anchor 성립) · **r < 0.3 → Framing D 폐기** (정직 종료).

## 2. 단계적 falsifier-gated 설계

```
step 0  ($0)   cortexlab-toolkit 설치 + TRIBE facebook/tribev2 로드 + 샘플 영상→BOLD 1회 (파이프 sanity)
step 1  ($0)   user OpenBCI .csv + 그때 본 영상 → 자극↔EEG timestamp 동기
step 2  (GATE) F-CT-3: 영상 → [EEG envelope] vs [TRIBE BOLD] median r
                 r≥0.5 PASS → step 3 / r<0.3 → Framing D 폐기 (정직 종료)
step 3  (2 PASS 시)  axis B 추가: anima §17 physics-channel ↔ EEG ↔ BOLD 3-way cross-validation
step 4  (3 PASS 시)  GOAL 검증: anima state 가 사람 뇌 anchor 와 align 하나
```

## 3. 정직한 위치 (g3 — over-claim 0)

- **EEG-anchor = 측정축, NOT GOAL 생성**: anima 가 의미있는 상태인지 *외부 ground-truth(사람 뇌)로 검증*. §17(self physics) + §18(LLM-judge) + §19(external brain) = 3-tier 측정. §1.1 data-regime 병목을 *해소*하는 게 아님.
- GOAL("anima 자발적 emergence") **미도달 불변** — §19 는 "anima 가 의미있나" 를 처음으로 *외부 기준*으로 판정할 길일 뿐.
- hardware 변수 잔존: "EEG 녹음 됨" ≠ "영상-동기화 + TRIBE-grid 정합 됨" (step 2 = 새 integration).
- #102 (Framing A pilot, ADDENDUM §6) 비충돌 — addendum 후속 0 = 미진행 추정. §19 = Framing D (3-way, strong-falsifier) ≠ #102 Framing A (text).

## 4. cross-link (SSOT 는 아래 — 본 디렉토리는 골격·참조)

- `HEXAD/CHAT/RESEARCH.md §19` — EEG-anchor research 본문 SSOT (Framing D + F-CT-3 + step 설계 + honest C3 + sources)
- `state/eeg_anchor_s19_2026_05_18/` — step 0 결과 / blocker log / evidence
- `references/tribev2/README.md` — TRIBE v2 (video/audio/text → fMRI BOLD, facebook/tribev2)
- `references/tribev2/ANIMA_INTEGRATION_PROPOSAL_ADDENDUM_2026_05_02_EN.md` — Framing D verdict + F-CT-3 사전등록
- `state/physics_channel_probe_s17_2026_05_18/` — axis B (§17 physics-channel) 추출 검증
- `archive/PHILOSOPHY.tape §verdict_eeg_anchor_s19` — verdict ledger (g6 append-only)
- `PLAN.md` (본 디렉토리) — step 0~4 staged

## 5. governance 준수

- **g_doc_consolidation**: HEXAD/EEG/* 내부 통합 (root docs/* 신규 0). research 본문 = RESEARCH.md §19, 본 디렉토리는 골격+참조 (중복 0).
- **g3**: F-CT-3 사전등록 falsifier (r<0.3 폐기) — over-claim 0, 측정축 ≠ GOAL 생성 명시.
- **g_fire_autonomous**: step 0 = $0 inference-only (TRIBE frozen forward, GPU fire 아님). step 2+ 실측 = user EEG .csv 입력 대기 (hardware-gated, anima-자율 cost 아님).
- **f1/f2/f3 + B-IDENTITY-5**: EEG/BOLD = 외부 신경과학 도구 (자체 invariant 으로만 인용, lattice-fit 0).
