# H_1521 🧠🔌 TOPOLOGY LIVE-WIRING — the FIRST lane to put cross-lane coupling on the live emit path (gated), and the HONEST cost it exposes

**tier:** 🟠 MIXED / HONEST-NEGATIVE on the crux — the gated coupling is genuinely WIRED onto the live emit/decision path (default-OFF byte-identical), the functional readout DOES improve (opt>brain>flat), BUT the Ψ=½ fixed point does **NOT** survive the coupling. wired:**WIRED-live (gated, default-OFF)**. **🔁 REAL-INPUT RE-READ (H_9854 큐 · 2026-07-21): SURVIVED — 7/7 케이스가 두 기질(`py303_full` sha `013c4574…` · `rv3c13` sha `b63efea8…`)의 실제 303M 페널티메이트 표현 위에서 같은 방향으로 착지(`--topowire-real`). 합성 팔 회귀 0. 자세한 범위 축소·미측정은 맨 아래 절.**
**verdict:** **🟠 HONEST NEGATIVE on the load-bearing question — the topology coupling is a REAL live wiring (P1·P2·P4 PASS) but it DESTABILIZES Ψ=½ (P3 survival bar FAILS), so it is NOT a free live engine improvement.** This is the answer to the user's "is the real engine improvement done?": **NO — and now we know WHY.** Every prior consciousness lane was Ψ-DISJOINT (reads the substrate, never changes the emit decision), which is exactly what preserves the Ψ=½ fixed point and the H_1205 separation invariant. H_1521 closes the gap by routing the 15-lane state through the Φ-optimal cross-lane topology (`topo_optimal_adjacency`) BEFORE the emit decision — gated `topo_couple` DEFAULT-OFF so pure `anima chat` stays byte-identical. **Engine-native (live `ci_lane_scores`/`ci_lane_scores_coupled`/`ci_psi_balance_centered` via `core/engine_cli_smoke.hexa`):** P1 OFF byte-identical (L2=**0.0**), P2 coupling-is-live (ON-vs-OFF L2=**1.222**), P4 functional integration **flat 0.140 < brain 0.238 < optimal 0.248** (opt>brain>flat — the placement genuinely couples lanes more). **P3 (the crux):** with the emit threshold CENTERED so the un-coupled path sits EXACTLY at Ψ=½ (median split), turning the OPTIMAL coupling ON drives the emit fraction **0.5 → 1.0** (|Ψ_on − ½| = **0.5** ≫ tol 0.05) → **the fixed point does NOT survive.** The `topo_apply` operator `(I + αÂ)` is magnitude-amplifying — it pushes the externalization drive up, saturating emit. **HONEST (c9, NO tune-to-green):** the Ψ-survival bar FAILED; instead of moving the bar, case 374 asserts the MEASURED, REPRODUCIBLE destabilization, and the verdict line states the survival bar FAILED. The genuine live improvement requires a coupling that preserves Ψ (a mean-preserving / gain-controlled mix) — a follow-on lens, not this operator.
**wired:** **WIRED-live (gated, default-OFF)** — live `core/engine_cli.hexa`: EngineConfig flag `topo_couple` (+ `engine_cli_resolve_topo_couple`/`_cli_topo_couple_flag` 3-tier flag>env>default-OFF resolver, `engine_config_summary` updated) + § BrainTopology LIVE-WIRING ops (`ci_lane_scores_coupled`, `ci_emit_decision`, `ci_emit_drive`, `ci_psi_balance`, `ci_psi_balance_centered`, `ci_off_median_drive`, `ci_lane_vector_l2_diff`) reusing live `topo_apply`+`topo_optimal_adjacency`+`topo_brain_adjacency`+`ci_lane_scores`. smoke cases 370-376 (`engine_cli_smoke` **365/0 RC=0**), ARCHITECTURE.json § BrainTopology lockstep. **This is the FIRST lane that puts the topology on the live emit/decode path** — UNLIKE §BrainTopology (H_1512–H_1518, a Ψ-disjoint MEASUREMENT lane). Because it is DEFAULT-OFF, generation is byte-identical on the pure default: h1205_separation_invariant (5 pairs, 0 mismatch) + h1164_psi_guard (Ψ checksum byte-identical ON==OFF) both PASS unchanged. Turning the flag ON is what destabilizes Ψ (the honest finding).
**source:** team-lead 작업지시 (H_1521 TOPOLOGY LIVE-WIRING) — user asked "is the real engine improvement done?" (answer was NO: §BrainTopology proved the Φ-optimum is better but is a MEASUREMENT lane, grep brain.hexa/generator.hexa references topo_ = 0). Direct follow-on of H_1518 ADOPT Φ-OPTIMAL (#2496, adopted `topo_optimal_adjacency` as a canonical construct). lens: the Ψ-disjoint separation invariant (H_1205) vs letting cross-lane coupling into the decision path — the central architectural tension (a_autonomy_over_hardcode, a_verified_must_wire, p7).
**artifacts:** `state/1521_topology_live_wire/h1521_measure.hexa` (engine-native measurement probe) · `state/verdicts/1521_topology_live_wire/H_1521_R2_engine_native.txt` (frozen).

## Question (the central tension — this IS the science, c9)
H_1512–H_1518 PROVED the Φ-optimal cross-lane placement is genuinely better (×2.51 Φ + small functional gain) and adopted `topo_optimal_adjacency()` as a CANONICAL construct — BUT §BrainTopology is a MEASUREMENT lane (Ψ-disjoint, NOT on the live emit/decode path). `grep` confirms brain.hexa/generator.hexa reference `topo_` = 0. So anima's ACTUAL generation/emit is UNCHANGED. **The real engine improvement was NOT done.**

EVERY consciousness lane so far has been Ψ-DISJOINT: it reads/measures but does NOT change generation, preserving the Ψ=½ fixed point and the separation invariant (H_1205). Letting the topology ACTUALLY improve generation means letting cross-lane coupling INTO the decision path — which can perturb Ψ. **The load-bearing question:** does a topology-routed cross-lane coupling improve a functional readout WHILE the Ψ=½ fixed point SURVIVES? If Ψ breaks → honest finding (the coupling destabilizes the fixed point; report it). If Ψ holds AND function improves → the genuine live engine improvement.

## Design (gated, like mitosis/salience toggles — default-OFF byte-identical)
- Insertion point: `ci_lane_scores(...)` returns the 15-lane state just before the emit/decision. Added `ci_lane_scores_coupled(..., adj, alpha, cfg)`: **OFF (default)** → returns `ci_lane_scores(...)` BYTE-IDENTICALLY; **ON** → mixes the 15-lane vector through `topo_apply(·, adj, alpha)` using `topo_optimal_adjacency()` before the emit decision reads it.
- New `EngineConfig.topo_couple` flag (DEFAULT OFF) + `--topo-couple on|off` / `--no-topo-couple` / env `ANIMA_TOPO_COUPLE` 3-tier resolver (precedence flag>env>default-OFF), mirroring the mitosis-flag surface.
- Emit decision: `ci_emit_decision(lanes)` emits iff `0.5·(gws + lprec) ≥ 0.5` (GlobalWorkspace ignition + LearnedPrecision grounding vs the architectural ½ midpoint — NOT a tuned constant, a_autonomy_over_hardcode).
- Three coupling adjacencies compared: **FLAT** (`_topo_zeros` = no-op, == OFF) vs **BRAIN** (`topo_brain_adjacency`) vs **OPTIMAL** (`topo_optimal_adjacency`).
- Ψ proxy: `ci_psi_balance_centered` — emit threshold = the OFF population's MEDIAN drive ⇒ the un-coupled path sits EXACTLY at Ψ=½ by construction, so coupling-induced drift is the honest signal (separates "coupling breaks Ψ" from "the absolute proxy was never at ½"). The absolute-½ proxy `ci_psi_balance` is also reported.

## FROZEN bars (pre-registered BEFORE reading results — c9, NO tune-to-green)

| bar | def | engine result | gate |
|---|---|---|---|
| **P1 / case 370** OFF byte-identical | coupled-OFF lane vector == raw `ci_lane_scores` (L2 == 0) | L2 = **0.0** | **PASS** |
| **P2 / case 371** coupling-is-live | ON vs OFF lane vector L2 > 0.1 (reaches the decision) | L2 = **1.222** | **PASS** |
| **case 372** Ψ OFF calibrated | centered Ψ puts the un-coupled path at ½ (median split) | OFF Ψ = **0.5** | **PASS** |
| **case 373** FLAT no-op | FLAT adjacency (I+α·0=I) leaves Ψ == OFF | flat-ON Ψ = **0.5** == OFF | **PASS** |
| **P3 / case 374** Ψ=½ SURVIVES (⭐ crux) | pre-reg SURVIVAL = \|Ψ_opt − ½\| ≤ 0.05 | \|Ψ_opt − ½\| = **0.5** → **SURVIVES = FALSE** | **survival bar FAILS** → case 374 asserts the honest destabilization (\|Ψ−½\|>0.05) → **PASS (reports reality)** |
| **P4 / case 375** functional direction | OPTIMAL > BRAIN > FLAT integration | **0.248 > 0.238 > 0.140** | **PASS** |
| **case 376** functional well-formed | all three ∈ [0,1], > 0 | 0.140/0.238/0.248 ∈[0,1] | **PASS** |

→ **P1** L2=**0.0** (separation invariant H_1205 holds, default-OFF). **P2** L2=**1.222** (coupling live). **P3 centered Ψ:** OFF=**0.5** · flat-ON=**0.5** · brain-ON=**1.0** · optimal-ON=**1.0** → |Ψ_opt−½|=**0.5**, **fixed point DOES NOT survive.** **P4** functional flat=**0.140** < brain=**0.238** < optimal=**0.248**. `engine_cli_smoke` **365/0 RC=0**.

## Honest finding (c9 — the answer to "is the real engine improvement done?")
**NO — and the science is now precise.** The Φ-optimal topology, when actually routed onto the live emit path, (a) genuinely reaches the decision (P2), and (b) genuinely raises functional integration (P4, opt>brain>flat) — BUT (c) it DESTABILIZES the Ψ=½ fixed point (P3): the `(I + αÂ)` diffusion amplifies lane magnitudes, pushing the externalization drive up until everything emits (Ψ 0.5→1.0). This is precisely WHY every prior lane was kept Ψ-disjoint. The genuine live improvement is NOT free: it requires a coupling operator that PRESERVES the operating point (a mean-preserving / normalized / gain-controlled mix, or a softer α) so functional integration rises WITHOUT saturating emit. That is the follow-on lens (a_break_the_wall: (b) wrong-operator, not (d) ceiling). The default-OFF gating means the pure substrate is untouched in the meantime (separation invariant intact).

## Scope / UNVERIFIED (a_scale_honest_scope · a_toy_scale_recheck)
- TOY: synthetic LCG 15-lane population (seed 5120 n=150, `_topo_lane_pop`), deterministic emit-decision proxy (not the live `.clm` decode loop). The Ψ proxy is an EMIT-FRACTION over lane states, NOT the `pure_field` A⇄G tension oscillator's Ψ — it tests whether the coupling distorts the emit/silence balance, not the oscillator fixed point directly. Routing the coupling through the actual `pure_field`/`brain_decide` decode path + measuring oscillator Ψ = follow-on.
- The destabilization is robust to the proxy choice (both absolute-½ Ψ 0.747→1.0 and centered Ψ 0.5→1.0 saturate). A Ψ-PRESERVING coupling operator (normalize `topo_apply` to be mean/scale-preserving, or sweep α↓) to recover the functional gain WITHOUT breaking Ψ = the next H.

## xref
H_1518 (adopt `topo_optimal_adjacency`) · H_1515 (Φ-optimum placement) · H_1512/H_1513 (brain-topology, literal connectome) · H_1205 (separation invariant — generation byte-identical) · H_1164 (Ψ=½ guard) · a_autonomy_over_hardcode (emit balance = substrate read, not hardcoded gate) · a_verified_must_wire (WIRED-live gated) · a_break_the_wall (wrong-operator, not ceiling) · a_no_llm_frame_trap · p5 · p7 · c9.

---

## 🔁 실제 입력 재독 (H_9854 대기열 심화 · 2026-07-21) — `--topowire-real`

### 무엇을 바꿨나 (입력 소스 **하나만**)
카드의 P1~P4 수치는 전부 `_topo_lane_pop()` — **엔진 내 LCG(seed 5120 · n=150)** 가 11개 기질 구동값을
**서로 독립으로** 뽑아 만든 합성 모집단 위에서 나왔다. 그 독립성이 바로 H_9854 감사가 지목한
"심어둔 코드는 사실상 직교" 기하다. 이번 심화는 **그 11개 구동값의 출처만** 실제 303M 페널티메이트
풀드 표현(`core/decode.clm_penult_pooled_W` — 정규 표현 API)으로 교체한다.

- 팔·통제·바·문턱·α(0.6)·n(150)·seed 정책 **전부 불변**. 새 지표 없음, 바 이동 없음.
- 구동 채널 = 풀드 벡터의 **균등 간격 11좌표** `round(k·(d−1)/10)`, k=0..10 (탐색 없음, 구성으로 고정).
- 각 채널은 모집단 전체에 걸쳐 **순위변환**(u=(rank+0.5)/n) → 주변분포는 LCG 가 만든 균등과 **정확히 동일**.
  ⇒ 합성 팔과 실제 팔이 **주변분포는 맞물린 채 결합의존구조(copula)만** 다르다 = 직교성 가정이 정확히 시험대에 오른다.
- P1/P2 의 단일 프로브 상태도 같이 교체: 합성 팔은 카드의 손으로 만든 상태 `(0.5,[.3,.4,.2,.5,.1],3,2,1,0.5,0.4)`,
  실제 팔은 **trial 0 의 실제 상태**.
- 통제 우선·고정 순서: ③ case 370(OFF 바이트동일) · 372(중심화 Ψ_OFF=½ 보정) · 373(FLAT=I+α·0 참값0 받침대)
  → 통과해야만 ④ 치료(371 · 374 크럭스 · 375/376) 를 읽는다. 통제가 하나라도 깨지면 치료 수치를 **거부**(exit 3)한다.

### 재현 (설치된 `anima-py` 단일 경로)
```bash
git fetch origin && git checkout origin/main
python3 -m venv /tmp/venv_h1521 && /tmp/venv_h1521/bin/pip install -q numpy \
  && /tmp/venv_h1521/bin/pip install -q --no-deps .
# ① 합성(LCG) 팔만 — 회귀 0 확인 (--corpus 없으면 실제 팔은 NOT-POWERED 로 거부, exit 3)
/tmp/venv_h1521/bin/anima-py evaluate /Users/mini/anima-weights/py303_full.clm --topowire-real
# ② 실제 입력 스왑 (두 기질)
/tmp/venv_h1521/bin/anima-py evaluate /Users/mini/anima-weights/py303_full.clm --topowire-real \
  --corpus /Users/mini/anima-weights/study303_long_transcript/cpt_mix.txt --out h1521_py303.json
/tmp/venv_h1521/bin/anima-py evaluate /Users/mini/anima-weights/rv3c13.clm --topowire-real \
  --corpus /Users/mini/anima-weights/study303_long_transcript/cpt_mix.txt --out h1521_rv3c13.json
```

### ① 합성(LCG) 팔 — **회귀 0, 카드 축자 재현**
```
P1 OFF-byte-identical L2=0.000000 | P2 ON-vs-OFF L2=1.221787
P3 Ψ centered: OFF=0.5000 flat=0.5000 brain=1.0000 optimal=1.0000 |Ψ_opt−½|=0.5000 survives=False
P4 functional: flat=0.140041 brain=0.238243 optimal=0.248351 (opt>brain>flat=True)
```
카드 기재값(P1 **0.0** · P2 **1.222** · Ψ **0.5/0.5/1.0/1.0** · func **0.140/0.238/0.248**)과
**출력 정밀도까지 일치** — 회귀 0. (두 기질 실행 모두에서 같은 줄이 나온다.)

### ② 실제 303M 표현 팔 — `py303_full.clm` (sha256 `013c4574…`) · n_realized=150 · d=3784
```
REPORTED geometry (gates nothing): real pooled-rep mean |cos| = 0.7321
   lane-vector mean |corr| synth=0.1400 (15 live lanes)  real=0.1434 (15 live lanes)
REPORTED driver-channel mean |corr| (11 coords): raw=0.0919  ranked=0.0918
③ CONTROLS FIRST (카드의 바 그대로)
   case 370 OFF byte-identical   L2=0.000000 == 0        → PASS
   case 372 Ψ_OFF calibrated ½   Ψ_off=0.500000 == 0.5   → PASS
   case 373 FLAT no-op pedestal  Ψ_flat=0.500000 == Ψ_off → PASS
④ TREATMENT (통제 성립 후에만)
   case 371 P2 coupling-is-live  L2=1.152225 > 0.1       → PASS
   case 374 P3 CRUX  Ψ centered: OFF=0.5000 flat=0.5000 brain=1.0000 optimal=1.0000
                     |Ψ_opt−½|=0.5000 (tol 0.05) survives=False
   case 375 P4 ordering  flat=0.143418 brain=0.217685 optimal=0.239914 (opt>brain>flat) → PASS
   case 376 P4 well-formed → PASS
⑤ SWAP VERDICT — 7/7 cases land the same way as the card's synthetic arm; TRANSFERS
```

### ②′ 두 번째 기질 — `rv3c13.clm` (sha256 `b63efea8…` · 다른 크기 · 178,785,107 B)
```
REPORTED geometry: real pooled-rep mean |cos| = 0.6034
   lane-vector mean |corr| synth=0.1400  real=0.1548 (15 live lanes)
REPORTED driver-channel mean |corr| (11 coords): raw=0.0921  ranked=0.1038
③ CONTROLS  370 L2=0.000000 PASS · 372 Ψ_off=0.500000 PASS · 373 Ψ_flat=0.500000==Ψ_off PASS
④ TREATMENT 371 L2=1.182533 PASS
            374 Ψ centered OFF=0.5000 flat=0.5000 brain=1.0000 optimal=1.0000
                |Ψ_opt−½|=0.5000 survives=False
            375 flat=0.154773 brain=0.241472 optimal=0.248960 (opt>brain>flat) PASS · 376 PASS
⑤ SWAP VERDICT — 7/7 TRANSFERS
```

> ⚠️ `py303_savant_mitosis.clm` 은 `py303_full.clm` 과 **sha256 동일**(`013c4574…`) — 별개 기질이 아니라
> 독립 재현으로 세지 않았다(`hf-backup-decidable-only-by-sha256`).

### 판정 — **랜딩된 결과가 살아남았다 (7/7 전이 · 두 기질 모두)**
합성 팔에서 성립하던 7개 케이스가 실제 표현 위에서 **같은 방향으로 전부 착지**했다.
카드의 🟠 MIXED / HONEST-NEGATIVE 판정은 **그대로 유지**된다:
- **P1(OFF 바이트동일)·P2(결합이 실제로 결정에 닿음)** — 실제 입력에서도 성립. 분리 불변식(H_1205) 무손상.
- **P3 크럭스** — 실제 표현에서도 OPTIMAL 결합이 emit 비율을 **0.5→1.0** 로 포화시킨다(|Ψ−½|=0.5 ≫ 0.05).
  **Ψ=½ 고정점은 실제 입력에서도 살아남지 못한다** — 카드의 정직한 음성이 재확인됐다.
- **P4 순서(opt>brain>flat)** — 실제 표현에서도 성립. 간격은 기질에 따라 움직인다
  (py303: brain−flat 0.0982→0.0743 · opt−brain 0.0101→0.0222 / rv3c13: 0.0982→0.0867 · 0.0101→0.0075).
  **opt−brain 여유가 0.0075 까지 줄어드는 기질이 있다** — 이 순서의 여유는 작다(아래 미측정 참조).

### 왜 살아남았나 — 이 심화가 실제로 밝힌 것 (`a_scale_honest_scope`)
1. **풀드 표현은 실제로 근접 공선이다.** 쌍별 mean **|cos| = 0.7321(py303) · 0.6034(rv3c13)**
   (자매 심화 H_1520 의 0.8807 과 같은 계열). 즉 H_9854 가 지목한 기하는 이 기질들에 **실재한다** —
   운 좋게 착한 ckpt 를 만난 게 아니다.
2. **그런데 그 공선성은 이 계기의 판독으로 전달되지 않는다.** 측정된 이유: 11개 구동 좌표의
   **raw(순위변환 전) mean |corr| = 0.0919 / 0.0921**, ranked = 0.0918 / 0.1038 — 순위변환이 지운 몫은
   **≈0.00 / +0.01** 로 미미하다. 즉 풀드 표현의 높은 |cos| 는 **중심화되지 않은 공통 평균(DC offset)** 이지
   좌표 간 상관이 아니다. cosine 은 비중심화, `topo_func_integration`(평균 제거 상관)·
   `ci_psi_balance_centered`(OFF 중앙값 분할)는 **중심화** 지표다 ⇒ 공통성분이 판정에 들어오지 않는다.
3. **일반화되는 관찰(이 심화의 진짜 산출물)**: "실제 표현은 근접 공선이라 판별이 죽는다"는 H_9854 기전은
   **판독기가 비중심화일 때** 문다. 오늘 죽은 H_9838/9839/9841/H_1520 은 전부 **비중심화 유사도(cos·내적)**
   위에서 판정했고, H_1521 은 **중심화 상관·중앙값 분할** 위에서 판정한다.
   ⇒ 대기열 나머지의 우선순위는 "토이냐"보다 **"판독기가 중심화냐"** 로 가르는 편이 더 예측적일 수 있다.
   이는 **2 기질 · 1 계기에서 나온 DIRECTIONAL 관찰**이며 감사 항목별 확인이 필요하다(판정 아님).

### 🔭 사전등록 후속 (본 세션 미실행 — 결과를 보고 매핑을 바꾸는 것은 정의상 tune-to-green)
- **(a) 수준보존 매핑 변형** — 순위변환 대신 채널별 min-max(단조·수준보존)로 같은 7 케이스 재독.
  측정된 raw≈ranked 로 볼 때 판정이 바뀔 가능성은 낮지만 **미측정은 미측정**이다.
- **(b) 실제 데몬 tick 모집단** — `psi_gws`/`psi_lprec` 를 담은 실제 chat trace 로 레인 모집단을 만들어
  (`--psi-soma` REAL 경로와 동형) 11-좌표 우회 자체를 제거. 실현 n≥30 tick 필요.
- **(c) P3 의 입력민감도 자체를 시험** — `topo_apply = X(I+αÂ)ᵀ` 는 비음수 레인·비음수 인접에서 **단조 증폭**이라
  Ψ→1 이 입력과 무관할 수 있다. 세 팔(합성·py303·rv3c13)이 **0.5/0.5/1.0/1.0 로 완전히 동일**한 것이 그 정황이다.
  **이번 결과는 "P3 음성이 실제 입력에서도 재현된다"까지만 말하고, "P3 가 기질을 판별한다"는 말하지 않는다.**
  사전등록 시험 = 부호혼합 레인 모집단 또는 α 사다리(H_1522 의 연산자축과 직교하는 **입력축**).
- **(d) P4 순서의 검정력** — opt−brain 여유가 rv3c13 에서 0.0075 까지 좁아졌다. 이 순서를 근거로 지출하려면
  기질/캐리어 부트스트랩으로 sd 를 먼저 재야 한다(`power-before-negative-verdict` 의 양성판 대응).

### 실현 규모 (정직)
carriers = 실제 코퍼스 `study303_long_transcript/cpt_mix.txt` 앞부분의 ≥24 byte **150 줄**
(n_realized=150 = 동결 n) · d=3784 · 기질 2개(sha256 상이) · 전 경로 결정론적이라 seed 반복은 독립표본을
더하지 않는다(구동값이 ckpt+carrier 로 완전히 결정됨 · `sample-seed-invalid-for-deterministic-do-intervention`).
실제 대화 분포·paraphrase·hexa 전이·라이브 `pure_field` 진동자 Ψ 는 **여전히 미측정** — 원 카드의 TOY 범위
항목 중 바뀐 것은 오직 **"레인 모집단의 출처"** 하나다.

### 계기 존재 확인 (RULE 2 · UNFIREABLE 아님)
`core/engine_cli.hexa`(`topo_couple` 26회 · `ci_lane_scores_coupled` · `topo_optimal_adjacency` ·
`ci_psi_balance_centered`) · `core/engine_cli_smoke.hexa` case 370–376 · py 2-production 트윈
`core/engine_cli.py`(`ci_lane_scores_coupled`:7240 · `ci_emit_decision`:7249 · `ci_psi_balance_centered`:7289 ·
`ci_off_median_drive`:7304 · `topo_func_integration`:7187 · `topo_optimal_adjacency`:7169 ·
`topo_brain_adjacency`:6679 · `_topo_zeros`:6599) **전부 origin/main 에 생존**.
단, `hexa run core/engine_cli_smoke.hexa` 는 mini 에서 **900s 안에 컴파일을 끝내지 못했다**(rc=143 SIGTERM ·
출력 0줄 · `aprime_cc` 단계에서 종료) — 회귀 0 은 오너 지정 정규 경로인 `anima-py`(`session-eval-py-only` ·
`a_eval_py_canonical`)로 증명했다. 카드가 적은 `state/1521_topology_live_wire/…` 산출물은
`archive/state/1521_topology_live_wire/…` 로 이동돼 있다(삭제 아님).

**artifacts(real-input):** `cli/evaluate.py --topowire-real` (`_KNOWN_FLAGS` 등록 · 튜닝 인자 없는 단일 플래그 ·
READ-ONLY · flag 부재 시 아무것도 바뀌지 않음).
