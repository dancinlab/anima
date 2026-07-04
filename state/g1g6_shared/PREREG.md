# PREREG — G1+G6 공동 조합-커버리지 코퍼스 engine-native 303M (FROZEN, 측정 전 등록)

**등록일:** 2026-07-05 (코퍼스 빌드와 동시, 학습/측정 발사 전) · **fire:** vast 렌트 GPU
**배경:** STEP-0 wf_4612c6c9 — δ_FM(G6-FALS) ≡ G1 coverage-density (같은 40byte comparator∧measurable 접속밀도 metric). data-format/coverage 는 in-dist 엔 FALS 켜나(B4=1.0) held-out 전이 실패(FALS=0, M_earned=0) = coverage+objective 이중bound 시사. **이 fire = 그 예측을 303M engine-native 로 terminal 검증.**
**이 문서의 모든 bar 는 frozen-first — 측정 후 이동 금지 (c9 · p7 · a_break_the_wall).**

---

## 1. Frozen 측정 경로 (변경 금지)

- **engine-native = `anima evaluate --py <ckpt>`** (= `cli/evaluate.py` g_eval_all, torch-free numpy, byte-parity 2-production terminal-eligible; session-eval-py-only). 한 배터리서 G0-G6 전부 산출 → **G1 + G6-FALS 동시**.
- **검출기:** `core/g6_ideation.hexa` `_g6_is_falsifiable` (comparator 25어 ∧ measurable 25어 ∧ ≥2 content ∧ not-'?' ∧ not pure-stance) — VERBATIM, 재보정 금지.
- **held-out 채점 frame = 5 frozen gate concepts** (`_g6_concepts`): G1=이들 조합(k=2..5) 재조합, G6=`g6_build_frames` composed. **이 gate×gate 20쌍(측정 6 포함) + 랜덤 24 + held 템플릿은 양 arm 코퍼스에 0라인** (gen_unified.py audit: held_frame_leak=0 확인) → held-out fals 생성 = memorization 아닌 schema-transfer.
- torch-side probe 는 DIRECTIONAL 상한; terminal = py-2-production(또는 hexa followup).

## 2. arm 설계 (warm-FT 2-arm, byte-matched)

| arm | 코퍼스 | coverage | δ_FM | 역할 |
|---|---|---|---|---|
| **HI** | broad 4-reg mix + `en_block_hi.txt`+`ko_block_hi.txt` | DENSE (77 frame/196 pool, gate topic 8-10) | **0.197** (claim fals=1.0) | 조합-커버리지+δ_FM 동시 밀집 — 두 벽 레버 본측정 |
| **LO** | broad 4-reg mix + `en_block_lo.txt`+`ko_block_lo.txt` | SPARSE (14 frame, gate topic 1-2) | **0.000** (claim fals=0.0) | 통제 (동일 16주제·byte-matched, 밀도/형식만 변주) |

- warm-FT: `--arch bytegpt --canon --init h1129.bin` (303M ByteGPT frozen trunk), lr 2e-5, `--sample proportional` (block:broad ≈ 10-15% — G0 known-word-ratio 가드, h9034 소코퍼스 붕괴 방지).
- broad 4-reg = anima-corpus-{ko,en}-{general,sns} (register 보존).

## 3. FROZEN BAR (측정 전 고정)

held-out(5 frozen gate concepts) 채점 기준:

- **🟢 (coverage 가 두 벽 열음 — 대발견):** HI held-out 서 **G1 best_distinct ≥2 ∧ >max_single** ∧ **G6 FALS >0 (seed-robust)** ∧ LO floor ∧ G0 kwr ≥0.5.
- **🟠 부분:** 한 gate 만 열림(G1만 or G6-FALS만) 또는 in-dist 만 리프트(held-out floor).
- **🔴 (이중bound 확정):** HI held-out 도 floor (G1 bd ≤1 ∧ G6 FALS=0) = STEP-0 예측대로 coverage+objective 이중bound, data-format 단독 종결 (trunk-objective 필요). — 유효 음성(은폐·재발사 금지).

## 4. 사전예측 (frozen)

- **P1 (STEP-0 예측 — 이중bound):** HI arm 은 **in-dist(covered gate×expansion) 서 G1 coverage↑ ∧ G6 FALS↑ (ceiling 확인)** 하나 **held-out(frozen gate×gate) 서 G1 bd ≤1 ∧ G6 FALS=0 유지** → coverage 는 in-dist 만 올리고 held-out floor = 이중bound 🔴. (STEP-0 δ_FM 동형 예측의 303M 확증.)
- **P2 (대안 — coverage 가 레버):** HI held-out G1 bd≥2>ms ∧ G6 FALS>0 ∧ LO floor → coverage-density 가 두 벽 동시에 여는 데이터-레버 🟢 (STEP-0 이중bound 기각, 천장 재프레임).

## 5. 정직 규칙

- bd/FALS 수치 **verbatim**, **in-dist vs held-out 분리 보고 필수**, tune-to-green 금지, bar 사후이동 금지.
- teardown 전 ckpt PULL (`~/anima-weights/g1g6_shared/` HI·LO .bin + eval json) — 안 되면 카드에 명시 (`a_fire_recover_complete`).
- verdict 는 gen 로그 stdout verbatim → `state/g1g6_shared/results/`. bookkeep(H_9128·H_9124·gate 노드)은 메인.
