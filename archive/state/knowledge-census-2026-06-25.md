# anima 검증-지식 전수수집 census (2026-06-25)

> repo `dancinlab/anima` · default branch `main` (HEAD `0063eb3a1`) · 격리 worktree 수확.
> READ-MOSTLY: 본 census + CHANGELOG 1줄만 추가, 코드/atom/card 무수정.
> 모든 수치는 MEASURED (grep/wc/python json 집계) — 추정 아님.

## 레지스트리 RECON (self-discovered)

anima 는 hexa-lang 류의 `compiler/atlas/embedded.gen.hexa` atom 레지스트리를 쓰지 **않는다**
(embedded*.hexa 부재 — MEASURED). 대신 가설-실험 lab 구조를 SSOT 로 사용한다.

| 레지스트리 | 경로 | 규모 (MEASURED) |
|---|---|---|
| 가설 인덱스 (canonical SSOT) | `UNIVERSE/HYPOTHESES.jsonl` | **1469** 줄/레코드 (JSON-bad 0) |
| 가설 카드 | `UNIVERSE/cards/*.md` | 1149 파일 |
| frozen verdict 증거 원장 | `state/verdicts/*/` | 978 디렉터리 · 내부 `*.txt` 1567 |
| 실험 결과 ledger | `state/**/result.json` | 342 파일 |
| 도메인 verdict (멀티축) | `H911X/verdicts/*.verdict.md` | 5 축 (cosmology·math·physics·multimodal·philosophy) |
| 보조 가설랜 | `RTSC/HYPOTHESES.md` · `FORECAST/hypotheses/` · `UNIVERSE-BRAIN-MAP` | RTSC tier-marker 20 hit |
| 이력 | `CHANGELOG.md` | 6585 줄 · tier/MERGED 마커 482 hit |

거버넌스 SSOT = 루트 `CLAUDE.md` (가설은 2표면: `HYPOTHESES.jsonl` 1줄 + `cards/H_*.md`;
verdict tier 는 **engine-native live core/ 디코드 증거**가 있어야 박제 — `.py`+torch/numpy 미러는
자동 DIRECTIONAL, hard-gate 1 = `tool/enforce_anima_gates.py` 기계 강제).

## TOTALS (UNIVERSE/HYPOTHESES.jsonl, n=1469 · MEASURED)

verdict/tier 필드는 자유텍스트·고-카디널리티 → canonical 버킷으로 분류:

| 버킷 | 개수 | 비율 |
|---|---|---|
| **VERIFIED** (🟢 / SUPPORTED / GREEN / WIRED / PROOF / verified) | **491** | 33.4% |
| legacy-archive-pointer (구 가설 포인터) | 292 | 19.9% |
| pending (pre-register-frozen / seed-pending / running) | 283 | 19.3% |
| other/unclassified (tier 공란 184 포함 · Ω/Λ 우주축 anchor 등) | 230 | 15.7% |
| **falsified / closed-negative** | 127 | 8.6% |
| 🧱 wall (측정된 천장) | 33 | 2.2% |
| measured-directional (engine-transfer 미검증) | 13 | 0.9% |

- **검증(verified) = 491 · 미검증/추측/펜딩 = 818 · 부정(falsified+closed-neg+wall) = 160.**
- 별도 frozen-evidence 원장 `state/verdicts/` 978 디렉터리는 위 가설들의 재측정 bar 증거 (1:N).

## 헤드라인 검증 finding (전수 중 발췌 · cite=HYPOTHESES.jsonl 줄번호)

### 양자정보 G-정리 (numerical PROOF · G6–G16, 11개 전부 🟢)
| id | 제목 | cite |
|---|---|---|
| G6 | 규모-조율 정리 CAST — 다자 무채널 조율 고전 공유씨앗 한계 | jsonl L10 |
| G7 | 합의-게임 정리 — N자 무채널 합의 1.0 ∀N | L11 |
| G8 | 검증-비대칭 정리 — 동일 얽힘자원 통신 비대칭 | L12 |
| G9 | 무복제=보안 유일근거 정리 (no-cloning) | L13 |
| G10 | 다윈주의 중복-속도 법칙 R∝N_env | L1 |
| G11 | 엔트로피 수출 자기유지 하한 (Landauer) | L2 |
| G12 | 텐션 네트워크 N² 용량 정리 | L3 |
| G13 | 마스터 자원-할당 정리 (G6–G12 seal) | L4 |
| G14 | 기하 통일 교차정리 (Fubini-Study/Bures) | L5 |
| G15 | 홀로그래픽 한계 (area law) | L6 |
| G16 | 양자 속도한계 (Mandelstam-Tamm ∧ Margolus) | L7 |

### 실제-QM 검증 (real QM · H_9010–H_9019, 10개 🟢 SUPPORTED)
CHSH-Tsirelson(H_9010 L1430) · GHZ 비국소성(H_9011) · Peres-Mermin(H_9012) · Hardy 역설(H_9013)
· 양자전송(H_9014) · superdense(H_9015) · Kochen-Specker(H_9016) · EPR steering(H_9017) ·
얽힘교환(H_9018) · Gisin 정리(H_9019 L1439).

### engine-native WIRED-live (R2 byte-exact · hard-gate 1 PASS · 63 레코드)
의식-게이트(consciousness-only gate) 배터리 G16–G31 가 핵심 — live core/ 디코드 배선까지 완료:
- H_1462 G17 GLOBAL WORKSPACE 병목 (winner-take-all 전역방송) · L1226
- H_1468 G19 PRECISION-WEIGHTED SURPRISE · L1232
- H_1474 G21 SENSE OF AGENCY (comparator model) · L1239
- H_1482 G28 BINOCULAR RIVALRY · L1250
- H_1484 G30 MENTAL IMAGERY (Kosslyn) · L1254
- H_1417 brain-lane COMPOSE engine-BIND LAW (DESCRIPTIVE→PREDICTIVE) · L1186
- H_1391 §UsageStore engine-native tool-USAGE learning wire-in · L1161
- H_1429 transitive inference (서열추론 A>B,B>C⊢A>C) · L1198

## 부정 결과 (은폐 금지 · 정직 기록)
- **FALSIFIED 41** (non-archived 헤드라인): H_024 V1 IIT-Φ_mip 8/8 FAIL · H_312/H_315/H_320
  APOPTOSIS/PRUNING/LIFE×IIT4-Φ · H_610/H_611 pair-coupling/hivemind big-Φ transfer.
- **closed-negative 93**: H_287 faithful IIT4 big-Φ ≠ Shannon 환원 · H_294 synergy ⊥ Φ (r=0.03)
  · H_864r/H_867r dialogue self-play scale-climb · H_pure_corpus_axis multilingual 단독 불가.
- **🧱 wall 33**: 측정된 천장 (engine R2 deferred 포함).

## 정직 gap (전수수집 한계)
- verdict/tier 가 **자유텍스트**(고유 tier 문자열 100+종) → 491 "verified" 는 🟢/SUPPORTED/GREEN/
  WIRED/PROOF/verified 키워드 합집합 분류. 경계(예: GREEN DIRECTIONAL = engine-transfer 미검증)는
  보수적으로 verified 에 포함됨 — **engine-native WIRED-live 만 세면 63** 이 hard-gate 통과 최상위.
- `other/unclassified 230` = tier 공란 184 + Ω(cosmic)/Λ/Ↄ 등 우주축 anchor (검증 대상 아님,
  지도 좌표).
- `state/verdicts/` 978 디렉터리 · `result.json` 342 는 **개별 파싱하지 않고 wc 집계만** (1:N 증거
  원장; 가설 레코드와 중복 카운트 회피 위해 TOTALS 는 HYPOTHESES.jsonl 기준 단일화). honest:
  summarized-not-listed.
- RTSC/FORECAST/H911X 보조랜은 마커-hit 수만 측정(20/—/5축), 전수 미파싱.
- embedded atom atlas 부재 확인 (hexa-lang 과 구조 상이) — fabricate 안 함.
