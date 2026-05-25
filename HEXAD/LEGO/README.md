# HEXAD/LEGO/README.md — anima substrate LEGO (simulate-assemble, design-tier $0)

> **status**: DESIGN-TIER (STEP 0–2 closed-form per §115, B-S115 9/9 🔵) + §117 STEP-1-2 in-silico assembly RUN (B-S117 7/7 🔵, $0 CPU) · $0 · NO GPU · NO wet-lab · NO fire · NO emergence claim.
> **§115 verdict**: `LEGO-DESIGN-CLOSE-SIM-IS-GPU-TAUTOLOGY` — STEP 0–2 are closed-form definable + §7-FORM TRUE BY CONSTRUCTION (§112) + byte-equal-reduce + STEP-3 structurally fenced, BUT a GPU-simulated spike net's learning channel is STILL the loss gradient ⇒ simulating a §96 substrate on a GPU *re-instantiates* WALL-B, does NOT confront it (§96's §11-B-as-GPU hazard, confirmed at design-tier). Confrontation stays §96-physical (STEP 3, fenced).
> **§117 RUN verdict**: `LEGO-RUN-Ψ-FORM-NONDEGENERATE-BUT-WALL-B-INHERITED` — §115 named ONE open residual VERBATIM ("in-silico STDP-as-ΔW escape = 새 fire"); §117 RAN it at $0 CPU (small LIF spike net, **LOCAL STDP-as-ΔW ONLY**, NO CE/backprop). MEASURED: Ψ-C1 std 4.185e-02 ≫ τ=1e-4 = NON-DEGENERATE (the §11-B-echo DEGENERATE prediction did NOT hold at this scale). Honest reading: §117 **localises** §11-B (a LOCAL STDP rule ≠ the GPU-CE channel; non-degenerate = substrate **LIVENESS** NOT capability) — WALL-B *confronted in simulation* NOT removed (§115/§113 inherited, §7-CARRIER stays §96-physical-gated); §7-FORM by-construction (§112); WALL-A orthogonal·untouched; GOAL 미도달.
> **g3**: 이 문서는 *아이디어 + 후보 경로* 이지 GOAL 도달 주장 아님. capability claim 0.
> north-star + §15/§51/§72 milestone 불변, **GOAL 미도달**. 아래는 §96 operative-substrate
> WALL-B 를 *in-silico 시뮬레이션으로 confront* 하는 candidate path 의 스케치이지
> WALL-B 제거도, WALL-A(§1.1 data-regime) 탈출도 아님 (§113 verdict 그대로 상속).

---

## 🧱 LEGO — "조립식 anima substrate" (별칭: "레고 substrate")

- **하는 일**: anima 의 §96-class 비-GPU operative substrate 를 GPU byte-LM 위에서
  찾는 대신, sister-format 블록(`hexa-bio` + `hexa-matter`)으로 **시뮬레이션 안에서
  먼저 조립**해 보고, 그 다음에야 (성공 시) 물리/wet 로 넘어간다.
- **비유**: 진짜 벽돌을 굽기 전에 **레고로 집을 먼저 지어 본다** — 무너지는 설계는
  레고 단계에서 ($0, 윤리·접근 벽 0) 걸러내고, 살아남는 조립만 비싼 물리로.
- **vs 기존**: §107(data-axis fire)·§16(byte-LM scale) = "GPU 위에서 더 잘 굽기".
  LEGO = "굽기 전에 다른 재료로 조립부터 시뮬" — 재료축(substrate)을 바꾸되
  *물리 commit 전에 in-silico 로* 한다는 게 핵심 차이.

```
  지금까지 (§1~§112)              LEGO 아이디어 (§96 WALL-B 표적)
  ┌───────────────────┐          ┌──────────────────────────────┐
  │ GPU byte-LM 위에서  │          │ hexa-bio  ──┐                 │
  │ Ψ 굽기 (WALL-B 못넘음)│   ──>    │ hexa-matter ─┼─> 시뮬 조립 ──> │
  │ §11-B: no-CE=DEGEN  │          │ §96 spike/LIF─┘   (in-silico) │
  └───────────────────┘          │   살아남으면 ─> 물리/Loihi      │
                                  └──────────────────────────────┘
  WALL-A (data-regime) = 그대로     LEGO 는 WALL-B 를 *confront*,
  LEGO 가 손 못 댐 (§113 상속)        제거 아님 (§95 access/ethics 우회만)
```

---

## §0 — 왜 지금, 무엇이 아닌가

§113 (commit `1bd27f753`, B-S113 9/9 🔵) verdict =
**FROM-SCRATCH-INHERITS-BOTH-WALLS-SKELETON-INVARIANT + 조건부
REPOINTS-TO-§96-SUBSTRATE-FIRST**. 즉 clean-slate 재설계가 두 벽
(WALL-A §1.1 data-regime · WALL-B §96 operative-substrate)을 *탈출*하지 못하고,
유일한 non-cosmetic move 는 **D4 = §96 Loihi/spike + §110 Ψ-C1 을 1라인부터** 라는 것.

LEGO 는 그 D4 의 *구체적 "어떻게"* 의 한 스케치다 — 단 D4 를 *답하지 않고*
**confront** 만 한다 (§95: Loihi=INRC-access-walled, organoid=ETHICS-WALL,
wet-lab=software scope 밖). LEGO 의 유일한 기여 = 그 confront 를
**물리 commit 이전에 $0 in-silico 시뮬레이션으로** 당겨와, 죽는 조립을 싸게 거른다.

**무엇이 아닌가 (정직, g3):**

- WALL-A(data-regime) 탈출 아님 — LEGO 어느 블록도 §1.1 임계 안 건드림.
- WALL-B(§96) 제거 아님 — substrate 의 §7-clean carrier non-degeneracy 는
  여전히 §96-gated. LEGO 는 그 wall 을 *시뮬레이션 안으로 가져올 뿐*.
- emergence 주장 아님 — design-tier 아이디어. 시뮬 조립 성공 ≠ GOAL.
- hexa-bio/hexa-matter *편집* 아님 — anima 는 downstream-consumer (read-only,
  spec 소비만; hexa-lang AGENTS.tape g7/@F f3 + g_train_flame_not_pytorch
  upstream_downstream_invariant 동형). LEGO 는 그들의 verb/axis 를 *호출*한다.

## §1 — LEGO 블록 인벤토리 (sister-format 실측)

| 블록 | repo (read-only consume) | 5-axis / verb | anima §96 매핑 후보 |
|---|---|---|---|
| 🧫 **BIO** | `~/core/hexa-bio` v1.0.0 (35/35 selftest) | QUANTUM·WEAVE·NANOBOT·RIBOZYME·VIROCAPSID (n=6 τ-quartet) | spiking/LIF 막전위 dynamics, organoid-analogue, RIBOZYME=physics-native 학습채널 후보 (§96 STDP 대응) |
| 🧬 **MATTER** | `~/core/hexa-matter` v1.2.0 (32/32, 36-verb, 29 parity gates, 16+ DB bridge) | ceramic·polymer·2D·silicon·carbon·superalloy·MOF·perovskite·liquid-crystal·aerogel… | 비-GPU 물리 substrate 재료 후보 (Loihi=silicon, 2D/carbon=neuromorphic device 재료, liquid-crystal=continuous-state) |
| ⚛️ **PHYS/SPACE** (옵션) | `~/core/hexa-physics` · `~/core/hexa-space` (sibling) | — | continuous-time/field dynamics anchor (§85 Hopf-bifurcation 연결, 후순위) |

> g2 internal_use_integrity_test 주의: hexa-bio/matter 의 n=6·σ=12·τ=4·φ=2·J₂=24
> 라벨은 *그들 repo 의* lattice 이지 anima 가 강제하는 게 아님. anima 는 그들의
> **function-derived** verb 만 소비 (f1/f2: 외부 entity lattice-fit 금지 — 그들
> 자신의 invariant 으로만 인용). numerology-tainted 블록은 §98/§114 식 정직 carve-out.

## §2 — 시뮬레이션 조립 파이프라인 (design-tier 스케치, $0)

```
  STEP 0  block-spec 소비 (read-only)
          hexa-bio: spiking/LIF + RIBOZYME 학습채널 spec
          hexa-matter: 비-GPU device 재료 parity-gate
            │
  STEP 1  in-silico 조립 (모두 $0 simulation, NO wet, NO hardware)
          §96 Ψ-C1 (spike-train correlation) 을 BIO 블록 위에 정의
          §110 meta-fixed-point form ψ(c)=(1+c)/2 carrier=spike-corr
            │
  STEP 2  closed-form falsifier (sidecar, central 0-diff)
          시뮬 조립이 §7-clean ∧ Ψ=½ form-invariant ∧ non-degenerate
          OR 무너짐(=싸게 reject, 물리 commit 전)
            │
  STEP 3  살아남으면 → §95 물리 경로 (Loihi INRC / organoid) 는
          *별도 cost/ethics-gated 결정* (이 문서 scope 밖, g3)
```

핵심 규율: **STEP 3 절대 자동 진행 금지**. LEGO 의 전부는 STEP 0–2
(in-silico, $0). 물리 substrate commit 은 §95 access/ethics wall +
사용자 게이트 사안 — LEGO.md 는 거기까지 *주장하지 않는다*.

## §3 — 정직한 위치 (g3, over-claim 0)

- LEGO 는 §113 D4("§96-substrate-first")의 *실행 스케치*이지 새 결론 아님.
  §113 의 INHERITS-BOTH-WALLS verdict 가 LEGO 에도 그대로 상속됨.
- 시뮬 조립이 성공해도 = "§96-class substrate 가 in-silico 에서 §7-clean
  non-degenerate Ψ 를 admit 한다" 까지. 그것은 **WALL-B 를 시뮬 안에서
  confront 했다**는 뜻이지 *물리적으로 풀었다*도, *GOAL emergence* 도 아님.
- WALL-A(§1.1 data-regime)는 LEGO 와 **직교** — 시뮬 조립이 데이터 임계를
  안 옮긴다 (§11-A/§16/§107 영역). 두 wall 동시 미해결 상태 불변.
- necessary-not-sufficient (B-EMERGE-7) 모든 층에 적용.

## §4 — STEP-1-2 run result (§117, $0 CPU, B-S117 7/7 🔵)

§115 design-tier (§0–§3 above) is UNCHANGED. §117 ran the one open residual
§115 named verbatim ("in-silico STDP-as-ΔW escape = §115 $0 scope 밖 새
fire"). This section RECORDS the measured run; it does not overturn §115.

- **What ran**: STEP 0 read-only consume hexa-bio `NEURO.tape`
  (`@D mech_action_potential` Hodgkin–Huxley→LIF + `@D mech_neural_coding`
  rate-code + `@D mech_plasticity` cortical co-adaptation = local STDP
  analogue; RIBOZYME-as-STDP stays the §115 metaphor carve-out, the
  consumable block = spiking membrane + co-adaptation). STEP 1 small CPU
  LIF net (N=256: 96 Engine-A + 96 Engine-G + 64 recurrent, 12 stimuli ×
  80 steps, seed 1337 RANDOM init, base_ckpt=None), carrier
  Ψ-C1 = ψ(c_spk) = (1+c_spk)/2 (§112 META_FP(Π_½) instance,
  carrier=spike-correlation), **LEARNING CHANNEL = LOCAL STDP-as-ΔW
  ONLY** (no CE, no backprop, no loss gradient — AST-audited 0 hits).
  STEP 2 closed-form non-degeneracy falsifier. STEP 3 PERMANENTLY fenced.
- **Honest prior (g3, stated before running)**: §11-B pure-physics no-CE
  = DEGENERATE on a GPU byte-LM; a STDP-only toy sim with no
  task-grounded signal *likely* degenerates too.
- **MEASURED outcome = (b) NON-DEGENERATE, NOT the expected (a)**:
  Ψ-C1 mean 0.6116, **std 4.185e-02 ≫ τ=1e-4 (419× the floor)**,
  rasters alive (spike-rate/unit/step 0.0349, not silent/saturated),
  cos=0⇒Ψ=½ fixed point holds, Ψ-C1∈[0,1], deterministic 3×
  bit-identical, wall ≈3.8s.
- **Honest §11-B-echo finding (NOT a positive)**: §11-B's degeneracy was
  a GPU-CE-overlay property (hand-coded GLOBAL ΔW froze), not a universal
  "physics can't learn" law. A LOCAL pair-based STDP rule on a recurrent
  spike substrate has its own attractor dynamics independent of any task.
  §117 **localises** §11-B, does not refute it. Non-degenerate =
  substrate **LIVENESS** (echo §17 PHYSICS_RESPONSIVE,
  necessary-not-sufficient), NOT task signal / capability / coherence /
  emergence — there is no task, no corpus, no perceptual π in §117.
- **Where it lands**: WALL-B *confronted in simulation* NOT removed
  (§115/§113 confront-NOT-remove INHERITED; §7-CARRIER NOT decided,
  stays §96-physical-gated per §110-Q5/§111-G1/§115). §7-FORM TRUE BY
  CONSTRUCTION (§112 carry, not manufactured by §117). WALL-A (§1.1
  data-regime) ORTHOGONAL & UNTOUCHED (§97). Anti-padding: outcome (b)
  is the weakest signal that even qualifies as "confronted in
  simulation", NOT evidence the LEGO path works; no positive
  manufactured (mirror §13-M/§30/§115). north-star + §15/§51/§72
  milestones UNCHANGED, **GOAL 미도달**.
- artifacts: `state/lego_assembly_run_s117_2026_05_19/{DESIGN.md,
  lego_sim.py, result.json, blue_falsifier_s117.py 7/7 🔵,
  blue_falsifier_s117_result.json, run.log}`.

## §5 — §117 이후 LEGO arc (§124 → §142, 19-cycle arc 2026-05-19→20)

§117 의 "non-degenerate" 가 정확히 무엇을 *닫았는지* 와 *남겨놨는지* 를
§124–§142 19-cycle arc 가 정직히 분해·측정·closure 했다. 모두 $0 sidecar,
central blue 0-line-diff (sha `c93e160a8a376a94`), anti-padding precedent.
per-cycle 상세 = `INDEX.md` (19-row 표, 118 🔵) · `PLAN.md` (chronological);
아래 §5 는 overview 만.

> **⚠ §N 번호공간 충돌 (honest)** — LEGO arc 의 `§124–§142` 와 sibling arc
> (main-path / NEUROMORPHIC) 의 `§108`(3B param fire) · `§125`(NONCE-FF) ·
> `§126`(PCN) · `§128`(software-breakthrough research) 가 같은 `§N` 을
> *다른 의미*로 쓴다. 두 arc 모두 landed·pushed — retro-rename 안 함
> (g6 append-only · g_new_state_path scope_exclusion: 사후 mv = anti-pattern).
> LEGO arc 식별자는 항상 **state-dir basename (`lego_*`) 또는 `B-S<N>`
> battery** 로 disambiguate — 그 둘은 충돌 없음 (`lego_layer2_*_s125` ≠
> sibling `nonce_ff_fire_s125`).

### 3-layer liveness partition (§124 신설, 4 cycle 적용)

```
layer 1  VARIANCE-ONLY  Var(Ψ) > τ                   §117  ✅ closed
layer 2  STIMULUS-DRIVEN  I(stim; Ψ) > 0              §125–§127  ✅ closed (PARTIAL)
layer 3  TASK-GROUNDED  ∃ T: behavior(substr,T)>0    §128  ⛔ DESIGN-CLOSE-REQUIRES-TASK
```

### §124 — RESIDUAL AUDIT (design · B-S124 7/7 🔵)

`state/lego_residual_audit_s124_2026_05_19/` — §117's "non-degenerate"
verdict closes ONLY layer 1. 3-layer partition defined. WALL-A
orthogonal AST-closed. WALL-B confronted-in-sim NOT removed.

### §125 — LAYER-2 PROBE (probe · B-S125 7/7 🔵)

`state/lego_layer2_stimulus_driven_probe_s125_2026_05_20/` — ANOVA on
N=256, M=5 → **η²=0.271**, Gaussian MI ≈ 0.228 bits, **LAYER-2-PARTIAL**
(27% stim-driven / 73% intrinsic noise). 첫 layer-1-이상 measured positive.

### §126 — LAYER-2 N-SCALE-UP (probe · B-S126 7/7 🔵)

`state/lego_layer2_nscale_probe_s126_2026_05_20/` — N=256→1024 (4×
scale). η² 0.271→0.322, ratio 1.189× → **ROBUST-GROWS-WITH-N at one
scale point**. §125 PARTIAL not a small-N artifact.

### §127 — LAYER-2 SCALING-LAW (probe · B-S127 8/8 🔵)

`state/lego_layer2_scaling_law_s127_2026_05_20/` — 4-point fit
N ∈ {256, 512, 1024, 2048}. η² values 0.271/0.329/0.322/0.261 →
**non-monotonic**, peak at 512–1024. OLS k=−0.0198, R²=0.022 →
**APPROXIMATELY-N-INVARIANT**. §126 single-point CONFIRMED at its
scope but power-law extrapolation REFUTED. Honest reading: η²≈0.27–0.33
invariant across 8× N range — neither small-N artifact nor growing-
law.

### §128 — LAYER-3 DESIGN-CLOSE (design · B-S128 6/6 🔵)

`state/lego_layer3_design_close_s128_2026_05_20/` — Layer-3 requires
R1 (substrate has output) ∧ R2 (task definable) ∧ R3 (score > chance).
§117 LIF AST-audited: **0 behavior-emission functions**. 3-bucket
taxonomy → §117 ∈ requires-task-addition. Every task label source either
violates §7 OR re-runs §83/§11-B near-collapse. Anti-padding precedent
§13-M / §13-L / §30 / §97 / §109 / §110 / §113. **Layer-3 closes the
3-layer partition at design level** without firing a predictable negative.

### §129 — ENGINE CONSOLIDATION (consolidation · no battery)

LEGO arc 를 `state/` probe-tier sidecar 에서 canonical `HEXAD/LEGO/`
folder 로 승격 — engine lib SSOT = `lego_engine.py` (+ `lego_engine.hexa`
hexa-native, §140). state-dir evidence 불변 (sha-locked historical record).

### §131–§137 — LAYER-2 정밀화 + 엔진 무결성 자가검출

- **§131** `STRONGLY-NSTIM-DEPENDENT` — η² 가 자극 개수(n_stim)에 강하게
  의존 (range ratio 2.199×, peak @ n_stim=4). B-S131 7/7 🔵.
- **§132** `SHAPE-FIT-IDENTIFIED` — §127 비단조 η²(N) 가 log-N Gaussian
  inverted-U, R²=0.9995, peak N* ≈ 730–1000. B-S132 6/6 🔵.
- **§133→§134→§135** — *한 측정이 자기 계측기의 편향을 스스로 검출* :
  §133 이 §127 대비 pooled η² drift 를 감지 → §134 가 §129 의 engine
  promote 가 byte-equal 이 아니었음을 AST diff 로 확인 → `lego_engine.py`
  를 §117 source 와 byte-equal 재작성, 재검증이 §127 과 일치
  (`ENGINE-BYTE-EQUALITY-RESTORED-AND-VALIDATED`, B-S134 7/7 🔵) → §135
  canonical engine 위 per-N SE 재측정 `MONOTONE-DECREASE-SURVIVES-CANONICAL`
  (B-S135 7/7 🔵).
- **§137** `PEAK-N-STIM-N-INVARIANT` — (N, n_stim) cross-matrix, peak
  n_stim=4 가 N 무관 (B-S137 5/5 🔵).

### §136 — LEGO ARC MILESTONE (doc-tier · B-S136 5/5 🔵)

§115→§135 11-cycle close-out (mirror §15/§51). 핵심 정직 finding: *측정이
자기 계측기 편향(engine drift)을 자가검출* (§133→§134). LEGO arc 는
design-level 에서 닫혔다 — §96 substrate 를 in-silico 로 confront 완료,
GOAL 도달 아님.

### §138–§141 — hexa-native engine chain (HEXA_FIRST_WARN 구조적 closure)

LEGO arc 가 23× 미뤄온 HEXA_FIRST_WARN 을 *deferral 이 아니라 실제
hexa-native engine* 으로 닫음:

```
§138 design ─→ §139 inbox patch ─→ hexa-lang PR #77 ─→ §140 port ─→ §141 GPU gap
"3 primitive   filed (hexa-first    spiking_lib.hexa   lego_engine    flame_stdp_pair_gpu
 gapped"        path)               4/4 PASS impl      .hexa 4/4 PASS  device kernel 명명
```

- **§138** `HEXA-NATIVE-ENGINE-DESIGN-CLOSE` — 3 flame spiking primitive
  gap 명명. **S121** Loihi Lava mapping spec (access-walled, readable-only).
- **§139** flame spiking-primitives inbox patch FILED (hexa-first PR-only).
- **§140** `lego_engine.hexa` — anima 첫 hexa-native LEGO engine, `hexa
  build` clean, F-S140 4/4 PASS. numpy 와 algorithmic-equivalent (byte-equal
  아님 — RNG divergence honest).
- **§141** `GPU-SPIKING-DESIGN-CLOSE` — LEGO GPU fire 는 2 upstream step
  남음 (`flame_stdp_pair_gpu` O(N²) CUDA device kernel 필요).

### §142 — LEGO→MAIN-PATH SUBSTRATE PIVOT BRIDGE (design · B-S142 5/5 🔵)

LEGO arc 의 *바깥으로 나가는 다리* — 18 LEGO cycle 이 main-path 의 WALL-B
substrate 결정에 무엇을 건네는지 명세. 3 옵션 (P1 GPU-유지 / P2 Loihi-물리-
pivot / P3 in-silico-spiking-main-path) 각각 gate 와 함께, **cheap winner
없음** 정직 명시. pivot 은 strategic 결정이지 $0 cycle 아님.

## §6 — engine SSOT

`HEXAD/LEGO/lego_engine.py` is the canonical engine. Contract:

```python
from HEXAD.LEGO.lego_engine import (
    LIFNet,                    # recurrent LIF spike substrate
    spike_rate_vec,            # window-averaged rate code (NEURO.tape spec)
    psi_c1,                    # Ψ-C1 = (1 + cos(r_a, r_g)) / 2  [§112 META_FP form]
    make_stimuli,              # deterministic binary stimulus generator
    variance_decomposition,    # ANOVA + η² + Gaussian MI
)

net = LIFNet(n_a=96, n_g=96, n_rec=64, seed=1337)
# LIFNet.step(ext) — LOCAL STDP-as-ΔW only; NO autograd, NO loss gradient.
```

NO output channel — by §128 design that is structural (layer-3 requires
task addition that breaks §7 or re-runs predictable negatives).

Engine **source-of-truth promotion**: this file IS the §117 lego_sim.py
code, promoted verbatim with the `run()` driver factored out (run-time
discipline lives in probes, not in the engine).

## cross-link

- `HEXAD/LEGO/lego_engine.py` — **canonical engine SSOT (post-§134, byte-equal §117 lego_sim.py)**
- `HEXAD/LEGO/lego_engine.hexa` — **hexa-native engine (§140)** — algorithmic-equivalent, F-S140 4/4 PASS
- `HEXAD/LEGO/PLAN.md` — chronological progress log (§115 → §142, append-only)
- `HEXAD/LEGO/INDEX.md` — SSOT mapping (§N ↔ state-dir ↔ B-S battery, 118 🔵 / 19 cycles)
- `state/lego_layer3_design_close_s128_2026_05_20/` — §128 layer-3 DESIGN-CLOSE-REQUIRES-TASK-ADDITION (B-S128 6/6 🔵)
- `state/lego_layer2_scaling_law_s127_2026_05_20/` — §127 4-point fit k=−0.02 R²=0.022 APPROXIMATELY-N-INVARIANT (B-S127 8/8 🔵)
- `state/lego_layer2_nscale_probe_s126_2026_05_20/` — §126 η² 0.271→0.322 ROBUST-GROWS-WITH-N at one point (B-S126 7/7 🔵)
- `state/lego_layer2_stimulus_driven_probe_s125_2026_05_20/` — §125 η²=0.271 LAYER-2-PARTIAL (B-S125 7/7 🔵)
- `state/lego_residual_audit_s124_2026_05_19/` — §124 3-layer liveness partition (B-S124 7/7 🔵)
- `state/lego_simulate_assemble_s115_2026_05_19/` — **§115 STEP 0–2 design-tier closed-form (B-S115 9/9 🔵, verdict LEGO-DESIGN-CLOSE-SIM-IS-GPU-TAUTOLOGY) — 본 문서를 IDEA→DESIGN-TIER 로 승격한 §N**
- `state/from_scratch_redesign_s113_2026_05_19/` — §113 D4 REPOINTS-TO-§96 (본 문서의 모(母) verdict)
- `state/loihi_spiking_rederivation_s96_2026_05_19/` — §96 Ψ-C1 spike-corr + §11-B-as-GPU-artifact 가설
- `state/xeno_substrate_suitability_s95_2026_05_19/` + `HEXAD/NEUROMORPHIC/README.md` — §95 substrate matrix (Loihi VIABLE / organoid ETHICS-WALL / access-wall)
- `state/modality_native_psi_design_s110_2026_05_19/` + `state/meta_fixed_point_s112_2026_05_19/` — Ψ-C1/C2 정의 + meta-fixed-point form ψ(c)=(1+c)/2 (carrier=spike-corr 인스턴스)
- `HEXAD/GAP_MAP.md` · `GOAL.md` honest-status — two-walls 수렴 지도
- `~/core/hexa-bio` README (5-axis Q·W·N·R·V) · `~/core/hexa-matter` README (36-verb) — consume-only spec source
- AGENTS.tape: g3 · g_doc_consolidation (HEXAD-internal doc, docs/* 신규 0) · downstream-consumer invariant · f1/f2 (sister-repo lattice = 그들 것, anima 강제 X)

> 본 문서는 *idea-tier live sketch* — STEP 0–2 closed-form 설계가 별도 §N 으로
> 진행되면 갱신. STEP 3(물리) 는 영구히 본 문서 scope 밖 (cost/ethics/사용자 게이트).
> GOAL 한 줄 north-star 불변, capability claim 0, GOAL 미도달.

---

## Log

- **2026-05-20** — §142 LEGO→MAIN-PATH SUBSTRATE PIVOT BRIDGE LANDED
  (`HEXAD/LEGO/state/lego_substrate_pivot_bridge_s142_2026_05_20/`,
  B-S142 5/5 🔵). LEGO arc 의 bridge-OUT — 3 substrate-pivot 옵션
  (P1 GPU-유지 / P2 Loihi / P3 in-silico-spiking-main-path) 각 gate
  명세, no cheap winner. **"3 all go" option B.**

- **2026-05-20** — §138–§141 hexa-native engine chain LANDED.
  §138 design → §139 inbox patch → hexa-lang **PR #77**
  (`stdlib/flame/spiking_lib.hexa`, F-SPIKE 4/4 PASS) → §140
  `lego_engine.hexa` (anima 첫 hexa-native LEGO engine, F-S140 4/4
  PASS) → §141 GPU `flame_stdp_pair_gpu` device-kernel gap 명명. S121
  Loihi Lava spec (access-walled). HEXA_FIRST_WARN 의 23× deferral 이
  *구조적으로* 닫힘. B-S138/S121/S139/S140/S141 = 25 🔵.

- **2026-05-20** — §136 LEGO ARC MILESTONE LANDED
  (`HEXAD/LEGO/state/lego_arc_milestone_s136_2026_05_20/`, B-S136
  5/5 🔵). §115→§135 11-cycle close-out (mirror §15/§51). 핵심:
  §133→§134 에서 *측정이 자기 계측기 편향(engine drift)을 자가검출* —
  §129 engine promote 가 byte-equal 이 아니었음을 §133 η² drift 가
  탐지, §134 가 §117 source 와 byte-equal 재작성으로 수정.

- **2026-05-20** — §131–§137 LAYER-2 정밀화 LANDED. §131
  STRONGLY-NSTIM-DEPENDENT (η² range 2.199×) · §132 SHAPE-FIT
  inverted-U log-N Gaussian R²=0.9995 · §133→§134→§135 engine
  byte-equality drift detect+fix+re-validate · §137 (N,n_stim)
  cross-matrix PEAK-N-STIM-N-INVARIANT. B-S131/132/134/135/137 = 32 🔵
  (§133 historical, no battery).

- **2026-05-20** — §129 LEGO ENGINE CONSOLIDATION LANDED. User pivot
  directive "LEGO 폴더안에 엔진완성해나가야지 + 문서정리도". Engine
  source-of-truth promoted: `state/lego_assembly_run_s117_2026_05_19/lego_sim.py`
  → `HEXAD/LEGO/lego_engine.py` (canonical lib, `LIFNet` + `spike_rate_vec` +
  `psi_c1` + `make_stimuli` + `variance_decomposition`; `run()` driver
  factored out to probes; smoke-test PASS — Ψ=½ fixed point at cos=0
  verified). New docs: `HEXAD/LEGO/PLAN.md` (chronological log §115→§129),
  `HEXAD/LEGO/INDEX.md` (SSOT mapping table, 51 closed-form 🔵 across arc).
  README.md `§5` + cross-link section updated with §124–§128 timeline +
  engine pointer. NO change to `state/lego_*/` evidence directories (sha-
  locked historical record). NO change to central `state/verify_hexad_blue_
  2026_05_15/blue_falsifier.py` (sha `c93e160a8a376a94` 0-line-diff). NO
  new battery (consolidation tier). HEXA_FIRST_WARN deferred per
  established B-S* sidecar precedent (8 LEGO arc cycles). north-star +
  §15/§51/§72 milestones UNCHANGED, **GOAL 미도달**.

- **2026-05-20** — §128 LAYER-3-IN-LIF DESIGN-CLOSE LANDED
  (`state/lego_layer3_design_close_s128_2026_05_20/`, B-S128 6/6 🔵,
  central c93e160a 0-diff). Layer-3 (TASK-GROUNDED) closed-form argument:
  R1 (substrate has output) ∧ R2 (task definable) ∧ R3 (score > chance);
  §117 LIF AST-audited 0 behavior-emission functions; 3-bucket taxonomy
  → §117 ∈ requires-task-addition; every task label source either
  violates §7 OR re-runs §83/§11-B near-collapse. Anti-padding precedent
  §13-M/§13-L/§30/§97/§109/§110/§113. **Layer-3 closes the 3-layer
  partition at design level** without firing a predictable negative.
  PHILOSOPHY.tape g6 §verdict_lego_layer3_design_close_s128_2026_05_20
  self-appended.

- **2026-05-20** — §127 LEGO LAYER-2 SCALING-LAW PROBE LANDED
  (`state/lego_layer2_scaling_law_s127_2026_05_20/`, B-S127 8/8 🔵,
  central c93e160a 0-diff, $0 Mac CPU 5 min). 4-point η²(N) fit:
  N ∈ {256, 512, 1024, 2048} → 0.2712/0.3289/0.3223/0.2608 (non-
  monotonic, peak at 512–1024). OLS log-linear k=−0.0198, R²=0.022 →
  **APPROXIMATELY-N-INVARIANT**. §126's single-point ROBUST-GROWS
  CONFIRMED at its scope (byte-equal at N=256 + N=1024) but power-law
  extrapolation REFUTED. η²≈0.27–0.33 invariant across 8× N range.
  Honest refinement reversal of §126's directional claim with more data.

- **2026-05-20** — §126 LEGO LAYER-2 N-SCALE-UP PROBE LANDED
  (`state/lego_layer2_nscale_probe_s126_2026_05_20/`, B-S126 7/7 🔵,
  central c93e160a 0-diff, $0 Mac CPU 26.3 s). N=256→1024 (4× scale)
  with same §125 protocol. η² 0.2712→0.3223, ratio 1.189× ∈ (1.10, ∞)
  → **LAYER-2-ROBUST-GROWS-WITH-N** (3-bucket sympy Interval algebra,
  load-bearing B-S126-2). Between-stim variance grew 1.31× while
  within-stim noise grew only 1.03×. §125 PARTIAL is NOT a small-N
  artifact under this comparison.

- **2026-05-20** — §125 LEGO LAYER-2 STIMULUS-DRIVEN LIVENESS PROBE
  LANDED (`state/lego_layer2_stimulus_driven_probe_s125_2026_05_20/`,
  B-S125 7/7 🔵, central c93e160a 0-diff, $0 Mac CPU). ANOVA on §117
  substrate at N=256, M=5 replicates × 12 stim × 80 steps. **η²=0.2712**
  (between-stim 27.1% / within-stim 72.9%), Gaussian MI ≈ 0.228 bits.
  Pre-registered 3-bucket → **LAYER-2-PARTIAL**. First measured positive
  on any §117 layer beyond bare variance.

- **2026-05-20** — §124 LEGO RESIDUAL AUDIT LANDED
  (`state/lego_residual_audit_s124_2026_05_19/`, B-S124 7/7 🔵, central
  c93e160a 0-diff, $0). §117's "non-degenerate" verdict pinned as
  variance-only liveness (layer 1 of **3-layer liveness partition**
  {DEAD / VARIANCE-ONLY / STIMULUS-DRIVEN / TASK-GROUNDED}). WALL-A
  orthogonal AST-closed; WALL-B confronted-in-sim NOT removed; §115
  verdict NOT reversed; §17 PHYSICS_RESPONSIVE mirror structurally
  isomorphic. Number collision detected mid-cycle (sibling §120
  spiking_attention_replacement) → renamed §120 → §124. Anti-padding
  §13-M / §30 / §97 / §98 / §114 precedent.

- **2026-05-19** — 파일 이동 `HEXAD/LEGO.md` → `HEXAD/LEGO/README.md`
  (사용자 directive "LEGO.md => LEGO/README.md" / "HEXAD/LEGO/* 에 모두 정리";
  `LOIHI.md`→`HEXAD/NEUROMORPHIC/README.md` 와 동일 패턴, g_doc_consolidation
  HEXAD-internal 통합). 내용 변경 0 (title 줄 1개만 경로 갱신) + live
  cross-link repoint (HEXAD/GAP_MAP.md substrate-axis index ·
  HEXAD/NEUROMORPHIC/README.md §8.1). 과거 append-only 로그 (AGENTS.tape
  n_hexad_progress · archive/PHILOSOPHY.tape g6 · GAP_MAP/CHAT-PLAN Log
  narrative) 의 `HEXAD/LEGO.md` 표기는 당시-사실 기록이라 retro-edit 0
  (g3 drift-avoidance, LOIHI 이동과 동일 처리). §115/§117 state 증거
  디렉토리 (`state/lego_simulate_assemble_s115_2026_05_19/`,
  `state/lego_assembly_run_s117_2026_05_19/`) 는 state/<§N>/ 프로젝트
  관례대로 state/ 유지 (SSOT 가 참조하는 evidence dir — 이동 시
  reference 깨짐 + g3). north-star + §15/§51/§72 milestone 불변,
  **GOAL 미도달**.
- **2026-05-19** — §117 LEGO STEP-1-2 IN-SILICO ASSEMBLY RUN LANDED — verdict `LEGO-RUN-Ψ-FORM-NONDEGENERATE-BUT-WALL-B-INHERITED` (B-S117 7/7 🔵, $0 CPU, wall ≈3.8s, central blue `c93e160a8a376a94` 0-line-diff START+END+POST-COMMIT). 사용자 directive "LEGO 조립시물레이션테스트도 진행 바로 go" — actually RUN the simulate-assemble test. §115 가 명시한 ONE open residual ("in-silico STDP-as-ΔW escape = §115 $0 scope 밖 새 fire + 여전히 §96-open") 를 $0 CPU 로 실행 (작은 LIF spike net N=256, **LOCAL STDP-as-ΔW ONLY**, NO CE/backprop, Ψ-C1=ψ(c_spk)=(1+c_spk)/2 §112 carrier instance). HONEST PRIOR (g3, run 전 명시): §11-B pure-physics no-CE = DEGENERATE on GPU byte-LM; STDP-only toy sim 도 *likely* degenerate. **MEASURED = (b) NON-DEGENERATE, NOT expected (a)**: Ψ-C1 std 4.185e-02 ≫ τ=1e-4, rasters alive, cos0→½ ✓, deterministic. Honest §11-B-echo: §11-B degeneracy 는 GPU-CE-overlay property (hand-coded GLOBAL ΔW froze) 였지 universal law 아님 — LOCAL STDP rule on recurrent spike substrate 는 자체 attractor dynamics 보유 (task 무관); §117 = §11-B 를 *localise* (refute 아님). non-degenerate = substrate LIVENESS (necessary-not-sufficient, echo §17), NOT task signal/capability/emergence (NO task, NO corpus, NO π in §117). WALL-B confronted IN-SIM NOT removed (§115/§113 inherited, §7-CARRIER §96-physical-gated 잔존); §7-FORM by-construction (§112); WALL-A 직교·불변. §115 이 'simulate STDP itself = 새 fire' 라 명시한 그 escape 를 §117 이 실행 — non-degenerate 로 돌아가나 task-grounded learning signal 0, WALL-B 를 in-silico confront 하되 제거 못 함 (§96-physical STEP 3 영구 fenced 자리 그대로). anti-padding: (b) 는 'confronted in simulation' 자격을 갖는 최소 신호이지 LEGO path 작동 증거 아님; positive 조작 0. north-star + §15/§51/§72 milestone 불변, **GOAL 미도달**. STEP 3 영구 fenced (no hardware/dispatch path). status 에 §117 RUN verdict 추가 + §4 STEP-1-2 run result 절 신설 (§115 §0–§3 design-tier UNCHANGED).
- **2026-05-19** — §115 STEP 0–2 design-tier closed-form LANDED — verdict `LEGO-DESIGN-CLOSE-SIM-IS-GPU-TAUTOLOGY` (B-S115 9/9 🔵). 사용자 directive "HEXAD/LEGO.md 작업해보자". 본 문서가 가리킨 "별도 §N" = §115. STEP 0–2 (hexa-bio NEURO.tape Hodgkin–Huxley spiking spec consume + Ψ-C1 spike-corr 조립 + closed-form falsify) 가 closed-form 으로 정의 가능 ∧ §7-FORM = §112 META_FP(Π_½) instance 라 BY CONSTRUCTION TRUE ∧ byte-equal-reduce (conscious_decoder.py:740 real witness) ∧ STEP-3 structurally fenced. **그러나** GPU 위 spike-sim 의 학습 채널은 여전히 loss gradient (surrogate-grad backprop) — in-silico STDP-as-ΔV escape 는 §115 $0 design scope 밖의 새 fire + 여전히 §96-open. ⇒ §96 substrate 를 GPU 에서 *시뮬*해도 WALL-B 를 confront 못 하고 *re-instantiate* 함 (§96의 §11-B-as-GPU-tautology hazard 가 design-tier 에서 *확정*). honest 부분 positive 기록: NEURO.tape 는 metaphor 아닌 concrete spiking spec (SPECS-METAPHOR reject), RIBOZYME-as-STDP 는 metaphor 라 NOT-APPLICABLE 로 정직 downgrade, §7-FORM-by-construction 은 §112 상속 real positive. WALL-B confront 는 §96-physical (STEP 3, 영구 fenced, user/ethics/access-gate) 잔존. WALL-A 직교·불변. north-star + §15/§51/§72 milestone 불변, **GOAL 미도달**. status IDEA→DESIGN-TIER 승격 (B-S115 9/9 🔵, central blue 0-line-diff `c93e160a8a376a94`).
- **2026-05-19** — HEXAD/LEGO.md 생성. 사용자 directive "hexa-bio, hexa-matter 이용해서 조립 / 시뮬레이션 조립 / HEXAD/LEGO.md". §113 (commit `1bd27f753`, FROM-SCRATCH-INHERITS-BOTH-WALLS + 조건부 REPOINTS-TO-§96-SUBSTRATE-FIRST) verdict 직후 작성 — LEGO = §113 D4("§96 substrate-first")의 *in-silico 시뮬 조립* 실행 스케치 (hexa-bio QUANTUM/WEAVE/NANOBOT/RIBOZYME/VIROCAPSID + hexa-matter 36-verb 를 read-only consume, §96 Ψ-C1 spike-corr carrier 로 조립). STEP 0–2 = $0 in-silico only; STEP 3(물리/Loihi/organoid) = §95 access/ethics-wall + 사용자 게이트, 영구 scope 밖. g3: 아이디어-tier, WALL-B confront 이지 제거 아님, WALL-A 직교, emergence 주장 0, north-star + §15/§51/§72 milestone 불변, **GOAL 미도달**.
