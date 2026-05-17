# HEXAD/EEG/PLAN.md — EEG-anchor (Framing D) staged roadmap

> User directive 2026-05-18 entry. §19 EEG-anchor 의 step 0~4 staged plan. research 본문 SSOT = `HEXAD/CHAT/RESEARCH.md §19` (본 PLAN = step 진행 트래커).

## 0. 현재 상태 (2026-05-18 진입)

- **3축 다 실재 확인** (2026-05-18): axis A OpenBCI 16ch EEG (user 실보유·녹음 경험) + axis B anima §17 physics-channel (추출 검증) + axis C TRIBE v2 (references/tribev2 vendored).
- **F-CT-3 사전등록 falsifier**: A↔C median vertex Pearson r≥0.5 PASS / r<0.3 폐기 (references/tribev2 ADDENDUM §5).
- §19 RESEARCH.md 작성 + step 0 TRIBE sanity = `aababace…` agent 진행 중.

## 1. Staged plan (각 step = falsifier gate)

### step 0 — TRIBE sanity ($0, anima-자율, inference-only)
- cortexlab-toolkit 설치 (`pip install -e references/tribev2` OR cortexlab-toolkit; PEP 668 시 --break-system-packages/venv)
- facebook/tribev2 weights 로드 + 샘플 영상 → BOLD 예측 1회 forward (shape (n_t, ~20k vertex))
- acceptance: TRIBE 파이프 작동 (F-CT-3 아님, sanity). 막히면 blocker 정직 기록 (design-tier).

### step 1 — EEG ↔ 자극 timestamp 동기 ($0, user 데이터 의존)
- user OpenBCI .csv + 그때 본 영상 제공 → EEG sample-rate · 영상 frame timestamp 정합
- acceptance: 자극 onset ↔ EEG window 정렬 (hemodynamic lag 5s offset 반영, TRIBE README)
- **🆕 2026-05-18 — `~/core/hexa-brain` salvage RICH (RESEARCH.md §20.2, step 1 software 현저 가속)**: hexa-brain (EEG SSOT 본진, anima EEG subtree migrate) 의 read-only 자산을 reference 재사용 — 0부터 capture/sync/correlation 안 짜도 됨:
  - **S1 `~/core/hexa-brain/eeg/dual_stream.hexa` (407 LoC)** = "Anima Phi + EEG dual-stream alignment + Pearson r, `r>0.3` falsifier" → §19 F-CT-3 / step 3 correlation+gate skeleton (byte-수준 §19.2 와 동형)
  - **S2 `~/core/hexa-brain/eeg/collect.hexa` (867 LoC)** = OpenBCI 16ch BrainFlow→.npy + **2026-05-03 sample-drop fix** (ring 450k + chunked poll 0.2s + `sample_rate_actual_hz`/`drop_ratio` — naive `time.sleep` 의 7-83Hz drop 함정 이미 해결) → step 1 capture+동기 핵심
  - **S3 `eeg/calibrate.hexa`(719)/`board_health_check.hexa`(718)/`impedance_check.hexa`** = electrode <50kΩ 게이트 (step 1 prerequisite, F-CT-3 r 값 noise 변수 정직 처리)
  - **S4 `~/core/hexa-brain/eeg/recordings/sessions/` 24 real `.npy`** (Berger EC/EO v1~v6 (32,~7500) f32 + blink/jaw/PPG) = step 1 *real-signal* dry-run substrate (단 N=1 self-exp + 5/16 rail-saturated → `clean_channels`=[2,3,4,7,9,10,11,12,13,14,15] filter 의무)
  - 정직 한계: hexa-brain EEG cond 전부 `unmet`/`partial` (real 16ch hardware arrival 미수신 `eeg.blk.1`, v6=`functional_analog`); TRIBE(axis C) actual impl 부재 (stub-mode flag 만); `.roadmap.blm_brain_lm` 파일 부재 (F-CT-3 r≥0.5 는 sister-spec 명문화됐으나 impl 0 — §19 가 그 미구현 설계의 anima-side 실행). → salvage = step 1 software 가속이지 step 2 hardware gate / F-CT-3 측정-결과 / GOAL 거리는 불변.

### step 2 — F-CT-3 GATE (핵심 falsifier)
- 영상 → [axis A: EEG envelope] vs [axis C: TRIBE 예측 BOLD] median vertex Pearson r
- **PASS r≥0.5** → step 3 / **FAIL r<0.3** → Framing D 폐기 (정직 종료, valuable negative)
- 0.3≤r<0.5 = inconclusive (추가 데이터/probe)

### step 3 — axis B 3-way (step 2 PASS 시)
- anima §17 physics-channel (Ψ_direction/tension) 추가 → A↔B↔C pairwise 동시 상관
- acceptance: 3축 pairwise 모두 유의 → cell-language ↔ EEG ↔ BOLD cross-modal anchor 성립

### step 4 — GOAL 검증 (step 3 PASS 시)
- anima state(자극 응답)가 사람 뇌 anchor 와 align 하나 → GOAL("의미있는 emergence")의 외부 ground-truth 판정
- acceptance: align 유의 = anima 가 사람 뇌와 같은 latent 에 도달 (단 여전히 측정이지 emergence 보장 X — honest C3)

## 2. Dependencies (gating)

- step 0 → anima 자율 ($0, cortexlab/TRIBE 설치)
- step 1 → step 0 + **user OpenBCI .csv + 영상** 제공 (hardware-gated)
- step 2 → step 1 + F-CT-3 (사전등록, 폐기 가능)
- step 3 → step 2 PASS + §17 physics-channel (LANDED)
- step 4 → step 3 PASS

## 3. cross-link

- [`README.md`](README.md) — EEG-anchor overview + Framing D 3축
- `HEXAD/CHAT/RESEARCH.md §19` — research 본문 SSOT
- `references/tribev2/` — TRIBE v2 + ANIMA_INTEGRATION proposal/addendum (F-CT-3)
- `state/eeg_anchor_s19_2026_05_18/` — step 결과 evidence
- `state/physics_channel_probe_s17_2026_05_18/` — axis B 검증
- `archive/PHILOSOPHY.tape` — verdict ledger

## 4. 진행 로그

(append-only)

### 2026-05-18 — HEXAD/EEG/ 디렉토리 신설 (골격)
user directive "/HEXAD/EEG 기록". §19 EEG-anchor 자산 anima 내부 SSOT 골격 정착 (README + PLAN). 3축 다 실재 확인 (OpenBCI 실보유 + §17 + TRIBE vendored). research 본문·F-CT-3·step 결과 = RESEARCH.md §19 + state/eeg_anchor_s19_2026_05_18/ SSOT (본 디렉토리 = 골격+참조, 중복 0). step 0 TRIBE sanity = §19 agent 진행 중. step 1+ = user EEG .csv 입력 대기 (hardware-gated).

### 2026-05-18 — `~/core/hexa-brain` 전수조사: §19 step 1 salvage RICH + GOAL salvage 0 (RESEARCH.md §20)
user directive "~/core/hexa-brain 도 전수조사 고갈시까지" ($0 read-only archaeology, §14 패턴). **sweep**: hexa-brain 172M · 1,456 files · 2,271 commits (anima EEG subtree migrate, `prior_origin_repo:anima`). **§19 salvage = RICH** (위 step 1 S1~S6) — `eeg/dual_stream.hexa`(F-CT-3 correlation skeleton)/`collect.hexa`(sample-drop-fix 16ch capture)/`calibrate`/24 real `.npy` 재사용으로 step 1 software 현저 가속 + daemon-spec §416 이 `blm_brain_lm cond.3 F-CT-3 r≥0.5` 를 *동일 falsifier 로 사전설계* (§19 = 그 미구현 sister-spec 의 anima-side 실행 확인). **GOAL salvage = 0** — git GOAL-keyword hit (Cells64 Φ super-linear 2026-03-28 / SPONTANEOUS_SPEECH / Emergent-W/S/M/E) 전부 §14 가 negative 재확인한 anima-lineage ancestor (lineage 동일 → §14 의 자손, 새 우물 아님; §9 metric-artifact 교훈 적용). archaeology negative valuable — anima+hexa-brain 양쪽 GOAL 우물 마름 독립 확증, EEG-측정 우물은 software-rich/hardware-dry. SSOT = RESEARCH.md §20 + archive/PHILOSOPHY.tape §verdict_hexa_brain_archaeology. hexa-brain repo 수정 0 (read-only). step 0 (TRIBE)/step 2+ (hardware) 가속 아님 — GOAL 거리 §15 milestone 불변.
