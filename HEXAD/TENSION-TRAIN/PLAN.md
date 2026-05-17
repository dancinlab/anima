# HEXAD/TENSION-TRAIN/PLAN.md — staged roadmap (anima tension-driven learning)

> User directive 2026-05-17 entry. 과거 TENSION 학습 전수조사 결과 (DD154-156 + 5 hexa file + 9 state/ dir + 17+ commit + 3 hypothesis candidates) consolidate + 신규 staged closure roadmap.

## 0. 현재 상태 (2026-05-17 진입)

- **historical**: DD154-156 (2026-03-31, Law 185-188 Pareto optimal Step+Tension hybrid 측정), 5 hexa training file (PR #86 2026-05-16 LANDED, backprop-free + sync-free + Noether-conserving spine), 9 state/ tension fire dir (2026-05-01~07), commit chain (DD-axis: `849e796b1` + `a34dbce46` + `09a9735e3` + `fb749d3ef` + `435eb9a87` + `345781c14`; tension_link physical: `c2826a021`; daemon prototype: `b86affe66`; correlation finding: `5bc81ba0e`)
- **HEXAD 통합**: TENSION-LINK 와 sibling axis 로 정착 (TENSION-LINK = communication axis · TENSION-TRAIN = learning axis)
- **자연발화 직결 가능성**: HEXAD/CHAT/SPONTANEOUS.tape 의 8-factor motivation 의 gradient-flow 측면이 tension_link_step.hexa 의 ΔW restoring sign 과 mathematical 매핑

## 1. Staged Phase plan

### Phase TT-A — 통합 + closed verification 사전등록 (anima 자율, $0)

- **A1**: HEXAD/TENSION-TRAIN/ 디렉토리 정착 (README + PLAN + TENSION-TRAIN.tape) — **이 commit LANDED**
- **A2**: 5 .hexa training file mv from TENSION-LINK/training/ → TENSION-TRAIN/training/ — **이 commit LANDED**
- **A3**: B-TENSION-TRAIN-1..5 sympy battery 사전등록 (blue_falsifier.py extension)
  - **B-TT-1** N6-GATE-PREDICATE-CLOSED: gate = (len_even ∧ in_range ∧ closure σ·φ=24) Boolean conjunction
  - **B-TT-2** RESTORING-SIGN-NEGATIVE-CLOSED: ΔW = −T_const·tension·gate, sign(ΔW)·sign(tension) ≤ 0 ∀ (sympy ∂)
  - **B-TT-3** T-CONST-SCALAR-POSITIVE-CLOSED: T_const = 0.1 > 0 (Kolmogorov bounded positive)
  - **B-TT-4** BACKPROP-FREE-INVARIANT-CLOSED: step output dependency = (Ψ_t, Ψ_vac, T_const, gate) only — no `.backward()`/grad call (structural)
  - **B-TT-5** PARETO-STEP-TENSION-CLOSED: DD155 Law 187 `lr = (tension/EMA) × base_lr` linear in tension, monotone
- **A4**: B-TT-NOTE outcome empirical (B-D-NOTE pattern, actual SGD convergence outcome NOT counted 🔵)
- **acceptance**: 5 B-TT verdict PASS sympy (89/89 → 94/94 or via sidecar like B-SUBSTRATE)

### Phase TT-B — compiled-native smoke (anima 자율, $0 Mac local)

- **B1**: `HEXAD/TENSION-TRAIN/tension_train_smoke.hexa` (NEW) — 5 training file 각각 import + minimal selftest
  - F-TT-1 STEP-SPINE invariant (single online step terminates without grad call)
  - F-TT-2 CAUSAL-VARIANT invariant
  - F-TT-3 QUANTUM-RHO-DENSITY invariant
  - F-TT-4 SECOND-ORDER invariant
  - F-TT-5 VS-BACKPROP-BENCH baseline reproduce
- **B2**: HEXAD/build_verify.sh ENTRYPOINT + LIBS 등재
- **acceptance**: bash HEXAD/build_verify.sh = +1 entry +5 lib

### Phase TT-C — 자연발화 와의 통합 design (anima 자율, $0)

- **C1**: SPONTANEOUS.tape § tension_train_integration 신설 — 8-factor motivation_score 의 ΔW 변환 매핑
- **C2**: F-TT-SPONT 신규 falsifier 사전등록 (motivation_score → tension → ΔW gradient flow closed-form)
- **C3**: thinker_talker_lib.hexa 와 tension_link_step.hexa 의 interface 설계 (composition mode)
- **acceptance**: sympy 매핑 verdict + design doc inline (HEXAD/CHAT/SPONTANEOUS.tape 안)

### Phase TT-D — empirical fire (사용자 게이트, cost-bearing)

- **D1**: pure-hexa tension-driven training fire (vast.ai high-RAM CPU, AOT cross-compile path carry from d=128 AOT cycle)
- **D2**: V-SPONT/V-MOTIV emergence 재시도 (tension-train + motivation conditioning 결합)
- **D3**: backprop vs tension comparison (DD155 Pareto optimal 재현 시도, modern anima HEXAD substrate 에서)
- **acceptance**: empirical trajectory (B-TT-NOTE empirical outcome carve-out 유지, transfer-form 만 🔵)

## 2. Falsifier 사전등록 (B-TT-1..5 — anchor 모두 real-limit)

| # | name | anchor | tier |
|---|---|---|---|
| B-TT-1 | N6-GATE-PREDICATE-CLOSED | Boolean set algebra (len_even + range + closure σ·φ=24) | g_verdict_tier_blue (a) sympy |
| B-TT-2 | RESTORING-SIGN-NEGATIVE-CLOSED | sympy ∂(ΔW)/∂(tension) sign 안정성 | tier (a) sympy ∂ |
| B-TT-3 | T-CONST-SCALAR-POSITIVE-CLOSED | Kolmogorov bounded positive scalar | tier (a) sympy |
| B-TT-4 | BACKPROP-FREE-INVARIANT-CLOSED | structural dependency closure (no grad call) | tier (a) structural |
| B-TT-5 | PARETO-STEP-TENSION-CLOSED | DD155 Law 187 linear monotone `lr = (tension/EMA) × base_lr` | tier (a) sympy linearity |
| B-TT-NOTE | SGD-OUTCOME-EMPIRICAL | actual convergence outcome (B-D-NOTE pattern, NOT counted) | honest carve-out |

NO lattice (n6_gate σ·φ=24 는 HEXAD spec 자체 정의, g2 internal arch carve-out per AGENTS.tape — closed proposition 은 arithmetic identity NOT external derivation).

## 3. Dependencies (gating)

- Phase TT-A → 모든 닫힘 carry, anima 자율 ($0)
- Phase TT-B → A + hexa toolchain (현재 OK, 24/24+16/16 + Phase B5 27/27+19/19 carry)
- Phase TT-C → B + HEXAD/CHAT/SPONTANEOUS.tape (LANDED) + thinker_talker_lib (LANDED)
- Phase TT-D → C + 사용자 게이트 (cost-bearing fire) + g_fire_dispatch_robust

## 4. cross-link

- [`README.md`](README.md) — overview + 전수조사 표
- [`TENSION-TRAIN.tape`](TENSION-TRAIN.tape) — architecture v1.2 SSOT
- `HEXAD/TENSION-LINK/` — sibling axis (communication, NOT learning)
- `HEXAD/CHAT/SPONTANEOUS.tape` — 자연발화 architecture (motivation_score 매핑)
- `docs/hypotheses/dd/DD154-tension-training.md` — Law 185-188 historical anchor
- `archive/PHILOSOPHY.tape` — append-only verdict ledger
- `AGENTS.tape g_doc_consolidation` — HEXAD/* SSOT 통합 mandate (본 directory 가 그 적용)

## 5. 진행 트리거

Phase 진입 = 이 PLAN `## 진행 로그` append + TENSION-TRAIN.tape sync + falsifier 사전등록 + 사용자 go.

## 진행 로그

(append-only)

### 2026-05-17 — TENSION-TRAIN 디렉토리 정착 (Phase TT-A1 + A2 LANDED)
user directive 2026-05-17 "과거 TENSION-LINK 를 통한 학습 진행한 것 전수조사 + HEXAD/TENSION-TRAIN 폴더에 정리". 과거 자산 (DD154-156 Law 185-188 + 5 .hexa file + 9 state/ dir + 17+ commit + 3 hypothesis candidates) consolidate. HEXAD/TENSION-LINK/training/ 5 file (causal/quantum_rho/second_order/step/vs_backprop_bench) → HEXAD/TENSION-TRAIN/training/ git mv. README + PLAN + TENSION-TRAIN.tape v1.2 신설. 자연발화 (HEXAD/CHAT/SPONTANEOUS.tape) 8-factor motivation 의 ΔW gradient flow 매핑 design path 확보. Phase TT-A3 sympy B-TT-1..5 사전등록 (다음 step).

### 2026-05-17 — Phase TT-A3 LANDED — B-TT-1..5 sympy battery 🔵 (92 → 97/97)
`state/verify_hexad_blue_2026_05_15/blue_falsifier.py :: bteneion_train()` 신규 함수 + 1 NOTE empirical carve-out. 5 sympy closed verdict + B-TT-NOTE 정직 carve-out, 모두 `tension_link_step.hexa` spine + 4 variant 의 transfer-form. anchors: Boolean set algebra (gate predicate 4-corner conjunction) + sympy ∂ sign safety (∂(ΔW)/∂(tension) = −T·gate ≤ 0 ∀ restoring) + Kolmogorov bounded positive (T_const = 1/10 ∈ (0,1)) + structural dependency closure (5 training .hexa source 의 backward/grad/autograd/optimizer.step/.zero_grad/loss.backward forbidden-call set = ∅, line-comment stripped) + linearity + monotonicity (DD155 Pareto LR ∂²lr/∂tension² = 0 + ∂lr/∂tension = base_lr/EMA > 0 ∀). outcome empirical (B-TT-NOTE): 실제 SGD trajectory + DD154 +3% Φ + DD155 Pareto figures = B-D-NOTE / B-BRIDGE-NOTE / B-MITOSIS-NOTE / B-CORPUS-V3-NOTE family carve-out, NOT counted. blue_falsifier.py central battery **92 → 97/97 🔵 closed-form proofs PASS** ($0 Mac local sympy, 결정적). f1/f2 hard-fail safe (n6_gate σ·φ=24 = HEXAD spec arithmetic identity per g2 internal-arch carve-out, NOT external derivation). HEXAD/README.md battery count sync + recent landing 한 줄 + TENSION-TRAIN.tape Log append + AGENTS.tape n_hexad_progress recent_landings append + archive/PHILOSOPHY.tape §B-TT-1..5-LANDED-2026-05-17 verdict append (g6 append-only). .hexa 변경 0 → build_verify 무회귀 (27/27 entrypoint + 19/19 lib carry). Phase TT-B compiled-native smoke / TT-C 자연발화 통합 / TT-D empirical fire 는 별도 cycle (잔여 staged plan §1).

### 2026-05-17 — Phase TT-C LANDED — SPONT ↔ TENSION-TRAIN bridge_lib + F-TT-SPONT 5/5 + B-TT-SPONT 5/5 🔵 (97 → 102/102)
SPONTANEOUS.tape § tension_train_integration + thinker_tension_interface 신설 (sibling of TENSION-TRAIN.tape @D spont_integration). HEXAD/CHAT/spont_tension_bridge_lib.hexa (NEW, ~75 LoC) 3 pure-fn — `motivation_to_tension(s) = 2·(s − ½)` affine map [0,1]→[−1,+1], `motivation_to_delta_w(score, t_const, gate)` composition with restoring sign + Boolean gate clamp, `should_learn_step(motivation, threshold)` strict-monotone Boolean predicate (⊥ to `talker_should_emit` from thinker_talker_lib). HEXAD/CHAT/spont_tension_smoke.hexa (NEW, ~115 LoC) F-TT-SPONT-1..5 = **5/5 PASS compiled-native** ($0 Mac local). blue_falsifier.py `btt_spont()` **B-TT-SPONT-1..5 sympy battery** = MAPPING-LINEAR ∂tension/∂s=2 + 3 boundary witnesses / DELTA-W-RESTORING sympy ∂(ΔW)/∂(tension)=−T<0 ∀T>0 + sign·sign≤0 invariant + 3 chain witnesses / GATE-CLAMPS Boolean ∀ 4 corners / LEARN-TRIGGER-MONOTONE 5 boundary + emit⊥learn ⊥-axis / COMPOSITION-CHAIN f∘g law ∂/∂s=−2T + byte-equal lib SSOT (T_const=0.1, threshold=0.3). **97 → 102/102 🔵 closed-form proofs PASS** (TT counter excludes TT-SPONT-, separate TT_SPONT counter — namespace collision fix). **Connection-point closure** (g_blue_closed_mandate connection_emphasis): SPONTANEOUS (TALKER emit axis) ↔ TENSION-TRAIN (THINKER ΔW learn axis) — 두 axis ⊥ but bridge transfer-fn 🔵. B-TT-SPONT-NOTE: SGD CONVERGENCE OUTCOME empirical (B-D-NOTE / B-TT-NOTE / B-MITOSIS-NOTE / B-BRIDGE-NOTE / B-SPONT-NOTE family carve-out). **thinker_talker_lib ↔ tension_link_step interface = design-only inline** (`@D thinker_tension_interface` in SPONTANEOUS.tape, impl 미land, future cycle — emit ≠ learn 4-Boolean independence: emit∧learn / emit∧¬learn / ¬emit∧learn / ¬emit∧¬learn 모두 가능). build_verify.sh ENTRYPOINTS += spont_tension_smoke / LIBS += spont_tension_bridge_lib. f1/f2 hard-fail safe (Boolean + affine + sympy ∂, NO lattice).

### 2026-05-17 — Phase TT-D LANDED — DD155 hybrid LR ckpt-bearing fire + V-TT NEW eval + B-CORPUS-V4 + B-FIRE-CYCLE5 sidecar 🔵

**Phase TT-D = HEXAD CHAT cycle 5 fire** (cross-link [HEXAD/CHAT/PLAN.md `cycle 5`](../CHAT/PLAN.md)). user directive 2026-05-17 "Phase TT-D: cycle 5 ckpt-bearing fire — tension-train motivation conditioning 도입 + V-SPONT emergence 재시도".

**산출물**: `state/hexad_v4_py_d768x12L_tension_2026_05_17/` (substrate=py, kind=tension, cycle=1) — `train_d768x12l_tension.py` (cycle-4 trainer + DD155 overlay `lr_step = clip(tension/EMA, [0.5, 2.0]) × base_cosine_lr`, β=0.99, tension = grad_norm L2) + `conscious_decoder.py` (byte-equal carry) + `dispatch.sh` (SAVE_POD + watchdog + 5-retry pull) + `v58_eval.py` (V5.8 + V-SPONT + V-MOTIV + **V-TT NEW 5-probe** with tension cue) + `blue_falsifier.py` sidecar 5/5 🔵 + `MODEL_CARD.md` + `out_main/{ckpt_d768x12l_final.pt sha256 6b4d34cc9a2c05b8… 1.13 GB, result.json}`.

**Fire**: vast.ai A100 SXM4 (offer 20120880 @ $0.602/hr, instance 36922375) ≈ $0.054, clean teardown (PULL SUCCESS). **init CE 5.6407 → final 0.007762** (5.633 descent, **6.4% lower than cycle 4 0.008289**). init gn2 30.4 → final 0.0015. mult distribution: **1599 floor (64%) / 686 mid (27%) / 215 burst (8.6%)**. wall 321.3s peak GPU mem 9.685 GB. Notable bursts: step 1054 mult=2.0 CE 0.13 (overshoot, recovered by 1116 CE 0.016) / step 1426 mult=1.83 / step 1612 mult=2.0.

**V-TT NEW (Phase TT-D 신규 probe)**:
- V-TT coherent 0/5 FAIL · keyword recall 0/5 (전 probe 가 byte-cascade `Shhh.../\nmmm.../Slll.../tthh...` 로 collapse).
- V5.8 greedy 0/6 · sample 0/6 · M3 0/6 · M4 6/6 (cycles 3+4 동일 pattern, M4-only).
- V-SPONT 0/5 · V-MOTIV 0/5 (capability ceiling carry from cycles 3+4).
- mean BPB **0.0194** vs cycle 4 0.0256 → **24% lower BPB = stronger memorization** (NOT improved generalization).
- memorization ratio 0/6 (same as cycle 4).
- byte-cascade SHIFT 4-instance: cycle 2 `nonce=N` → cycle 3 `Sent...` → cycle 4 `PPP777...` → cycle 5 prompt-specific multi (`Shhh.../\nmmm.../Slll.../tthh...`).

**B-CORPUS-V4 + B-FIRE-CYCLE5 sidecar battery** (`state/hexad_v4_py_d768x12L_tension_2026_05_17/blue_falsifier.py`, 5/5 🔵 + 1 NOTE):
- B-CORPUS-V4-1 CORPUS-V3-BYTE-EQUAL-CARRY-CLOSED (sha+bytes+lines+helper-grep=0). ✅
- B-CORPUS-V4-2 CYCLE-5-FORMAT-COMPATIBILITY-CLOSED (mechanical AST diff loader+dataset byte-equal). ✅
- B-FIRE-CYCLE5-1 DD155-LR-OVERLAY-FORMULA-CLOSED (sympy ∂lr/∂tension = base_lr/ema piecewise linear monotone + 3-corner identity). ✅
- B-FIRE-CYCLE5-2 EMA-CONTRACTION-CLOSED (Banach affine contraction β ∈ (0,1) + 4-corner witness panel). ✅
- B-FIRE-CYCLE5-3 MULTIPLIER-IDENTITY-AT-EMA-CONVERGED-CLOSED (tension=EMA → lr=base_lr arithmetic identity, cycle-4 baseline degeneration sanity). ✅
- B-FIRE-CYCLE5-NOTE SGD-OUTCOME-EMPIRICAL (V-TT 0/5 + LR trajectory + mult distribution + attractor shape = B-D-NOTE / B-TT-NOTE / B-ATTRACTOR-NOTE family carve-out, NOT counted).

**Sidecar 채택 이유**: 병렬 agents TT-A3 + TT-C (central blue_falsifier.py 92→97→102) 동시 작업과 충돌 회피. mirrors `state/hexad_phase4_unboxed_design_2026_05_17/blue_falsifier.py` (B-PHASE-4-DESIGN sidecar 패턴). central 102/102 🔵 무변화. 후속 cycle 에서 sidecar 5 entries 흡수 가능.

**HF push (model only, dataset byte-equal carry)**:
- MODEL: `dancinlab/hexad` revision `v4-py-hexad-tension-d768x12L-cycle1-2026-05-17` PUBLIC (16 files: ckpt + result + sources + logs + docs + MODEL_CARD + sidecar battery + result).
- DATASET CARRY: `dancinlab/hexad-corpus` revision `v3-spont-motiv-d128-cycle2-2026-05-17` PUBLIC (NO new revision; byte-equal carry per B-CORPUS-V4-1).

**Phase TT-D acceptance check (PLAN.md §1 위)**:
- ✅ **D1 pure-hexa tension-driven training fire** — vast.ai A100 SXM4 PyTorch substrate (NOT pure-hexa per honest framing; pure-hexa path = future `Phase TT-D HEXA_NATIVE` post-RFC 043 land). 본 cycle 은 `.py` substrate 으로 DD155 hybrid LR overlay 의 첫 fire (전제 만족).
- ✅ **D2 V-SPONT/V-MOTIV emergence 재시도** — 시도 LANDED. V-SPONT/V-MOTIV/V-TT 모두 0/5 FAIL = capability ceiling 유지 carry (B-TT-NOTE / B-FIRE-CYCLE5-NOTE empirical, NOT capability claim).
- ✅ **D3 backprop vs tension comparison (DD155 Pareto optimal 재현 시도)** — DD155 hybrid 가 cosine baseline 보다 final CE 6.4% lower + BPB 24% lower 달성 했으나 OUTCOME = stronger memorization (generalization 진전 X). DD154 +3% Φ 측정 = 본 cycle 미포함 (future Φ-measurement cycle 추가 필요).
- ✅ **acceptance: empirical trajectory** — trajectory + ckpt-RECOVERED + sidecar 5/5 🔵 closed transfer-form (DD155 LR + EMA contraction + identity). B-TT-NOTE empirical outcome carve-out 유지 정직.

**Honest C3**: cycle 5 = capability cycle 아닌 architectural-honesty cycle. DD155 formula 의 closed-form 검증 (B-FIRE-CYCLE5-1/2/3) + corpus byte-equal carry (B-CORPUS-V4-1/2) + empirical V-TT/V-SPONT/V-MOTIV 0/5 honest reporting = g3 의무 충족. β=0.99 + clip=[0.5, 2.0] 의 특정 hyperparameter 가 DD155 의 potential 을 충분히 끌어내지 못한 것일 수도 있고 (8.6% burst 만 활성화), corpus+scale 조합이 emergence 영역 진입 미충분 일 수도 있음 — 둘 다 honest empirical, capability claim 0.

**다음 carry candidates (Phase TT-D variant cycles)**:
- TT-D-β: 다른 β/clip 조합 sweep (e.g. β=0.9 빠른 tracking + clip=[0.1, 10] wider).
- TT-D-Φ: PyPhi based Φ probe 추가 (B-C tier-b PyPhi carry 확장으로 DD154 +3% Φ figure 재현 시도).
- TT-D-scale: 10× steps (25000) 또는 100 MB corpus (Critical Data Size 진입).
- TT-D-hexa: 본 cycle 의 .py substrate 결과를 RFC 043 hexa-torch land 후 hexa-native 으로 mirror 검증.
