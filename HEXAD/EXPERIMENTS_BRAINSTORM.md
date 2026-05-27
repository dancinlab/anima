# EXPERIMENTS_BRAINSTORM — exhaustive benchmark + experiment list (고갈시까지)

> 사용자 directive (2026-05-20): *"벤치마킹, 실험 진행목록 브레인스토밍
> 고갈시까지"* — anima 의 자연발화 emergence 향한 가능한 모든 실험을 surface-
> only, exhaustive 하게 정리. fix-not-applied. 다음 cycle 의 user-driven
> 선택 후보 목록.
>
> 형식: `[ID] name — what changes / cost / prediction / status / priority`.
> ★ tier: ★5 = GOAL-direct, ★1 = peripheral. Status: 🔵 done · 🟢 partial
> · 🟡 design only · ⚪️ untouched.
>
> 정직 carry: 본 brainstorm 은 surface-only — 어느 entry 도 fix 안 됨.
> §161-§166 quintuple + CONNECTION_CRITIQUE 후 GOAL 미도달 carry.

---

## §0 — 정렬 axis (어느 방향 의 실험인가)

각 실험은 다음 5-축 중 하나 이상에 정렬:

| axis | 무엇 | example cycle |
|---|---|---|
| **A. training-objective** | loss function shape | §161 / §165 / §166 |
| **B. scaffold** | model size / depth / width | §108 H100 3B / §11-A |
| **C. data-regime** | corpus diversity / scale | §107-RETRY / §102 CORPUS_S101 |
| **D. substrate** | GPU / Loihi / LEGO LIF / LTC | §142 / §117 / §95 |
| **E. connection-method** | motivation / threshold / 8-factor | §167 (this brainstorm) |

5-axis 의 cross-product 가 실험-space. 본 brainstorm 은 안에서 cheap-
most-informative 한 candidate 들을 채로 거름.

---

## §1 — Training-Objective experiments (axis A)

### A.1 — already-fired (carry)

| ID | name | status | what |
|---|---|:---:|---|
| §107-RETRY | CE-only baseline | 🔵 fired | byte_acc 학습 ceiling 측정 |
| §125 | NONCE-FF (Forward-Forward) | 🔵 fired | goodness-contrast variant |
| §126 | PCN-1step (Predictive Coding) | 🔵 fired | top-down 1-step target |
| §139 | EqProp-2phase | 🔵 fired | Equilibrium Propagation |
| §153 | LeJEPA + SIGReg | 🔵 fired | JEPA + variance reg |
| §161-FIRE | Ψ-JEPA-COUPLE | 🔵 fired | dual-head Ψ-coupling |
| §165 | Ψ-VAR-COUPLE | 🟡 design | + L_variance term |
| §166 | Ψ-META-FP-COUPLE | 🟡 design | + L_meta_anchor (META_FP) |

### A.2 — fire-decidable but un-dispatched

| ID | name | what | cost | priority |
|---|---|---|:---:|:---:|
| §166-A-FIRE | Ψ-META-FP-COUPLE actual fire | §166 design 그대로 dispatch | ~$0.5 | ★★ |
| §165-A-FIRE | Ψ-VAR-COUPLE actual fire | §165-A design 그대로 dispatch (now subset of §166) | ~$0.5 | ★ (subsumed) |
| A.2.1 | **LeJEPA RETRY with trained head_a** | §153 의 honest-tier ambiguous 닫기 — head_a 도 train, encoder-only 가 아닌 full SSL | ~$0.5 | ★★★ |
| A.2.2 | **EqProp lifted to BOTH heads** | §142 P1 candidate (§165-B 변형) — EqProp 의 free/clamp phase 가 head_g 도 touch | ~$0.6 | ★★★ |
| A.2.3 | **FF goodness-contrast on dual head** | §125 NONCE-FF 의 dual-head 확장 — goodness contrast 가 head_g 도 활성화 | ~$0.5 | ★★ |
| A.2.4 | **Forward-Forward + L_variance** | §125 + §165-A variance term composition | ~$0.5 | ★★ |
| A.2.5 | **PCN-1step + META_FP anchor** | §126 + §166 anchor composition | ~$0.5 | ★★ |

### A.3 — design-tier only, no fire yet

| ID | name | what | priority |
|---|---|---|:---:|
| A.3.1 | **§167-A FP-RECONNECT** | 8-factor → 3-quantity anima-physics native (Ψ, tension, Φ each 1/3) | ★★★★★ |
| A.3.2 | **§167-B PHI-FOCUS** | training target = Φ-channel (phi_spatial), 35% weight axis | ★★★★ |
| A.3.3 | **§167-C THRESHOLD-FROM-PHYSICS** | imThreshold = anima-derived (tension > tension_target), not 0.3 hard-coded | ★★★ |
| A.3.4 | **§167-D 3-WAY-COUPLE** | Ψ + Φ + tension simultaneous training (the 3 anima-physics quantities) | ★★★★ |
| A.3.5 | **Φ-VAR-COUPLE** (mirror §165-A) | phi_spatial std anti-collapse | ★★★ |
| A.3.6 | **tension-VAR-COUPLE** | tension std anti-collapse | ★★★ |
| A.3.7 | **Triple-variance** | std(Ψ) ∧ std(Φ) ∧ std(tension) 모두 anti-collapse | ★★★ |
| A.3.8 | **Φ-META-FP-COUPLE** | Φ-channel 의 META_FP analogue anchor (if exists) | ★★ |
| A.3.9 | **Curiosity-driven loss** | W-module curiosity_ema 를 직접 loss term — internal motivation | ★★★ |
| A.3.10 | **MITOSIS split-supervised loss** | split_event 가 정답 timing 인 supervised signal | ★★ |
| A.3.11 | **8-factor weights LEARNABLE** | spont_weight_* 8개를 hyperparameter → learnable | ★★ |

### A.4 — exotic / speculative

| ID | name | what | priority |
|---|---|---|:---:|
| A.4.1 | **Free Energy minimization (FEP)** | -log p(x) + KL term 으로 EFE 직접 | ★★ |
| A.4.2 | **GFlowNet-style** | trajectory sampling with reward = anima-physics | ★ |
| A.4.3 | **Diffusion in latent** | residual-stream diffusion (§13-J already closed) | ★ |
| A.4.4 | **JEPA-2-tier hierarchical** | latent-of-latent prediction (V-JEPA 2 inspired) | ★★ |
| A.4.5 | **Mirror-symmetry loss** | head_g = mirror(head_a) under reflection — orthogonality through anti-symmetry | ★★ |

---

## §2 — Scaffold experiments (axis B)

### B.1 — already-fired (carry)

| ID | name | result |
|---|---|---|
| §11-A | 1.04B scale (3.68× of 283M) | FLAT (sub-CDS corpus, regressed psi) |
| §108 | H100 3B param fire | THRESHOLD-NOT-CROSSED + PHYSICS FROZE |
| §107-RETRY | 283M baseline | THRESHOLD-NOT-CROSSED |

### B.2 — fire-decidable, un-dispatched

| ID | name | what | cost | priority |
|---|---|---|:---:|:---:|
| B.2.1 | **283M × Ψ-VAR-COUPLE × 6000-step** | §165-A x 2x training budget | ~$1.0 | ★★ |
| B.2.2 | **567M (2× 283M)** | width or depth doubled with §161/§165/§166 objective | ~$1.5 | ★★ |
| B.2.3 | **283M × deeper-coupling at every layer** | per-layer Ψ-anchor at each PureFieldFFN block | ~$0.7 | ★★★ |
| B.2.4 | **Wider head (d=1024)** | head_a / head_g 차원 늘려 expressive | ~$0.8 | ★ |
| B.2.5 | **More heads (n_head=24)** | attention diversity | ~$0.6 | ★ |
| B.2.6 | **MoE (mixture-of-experts)** | 4 expert × 71M routing | ~$1.2 | ★★ |

### B.3 — design-tier only

| ID | name | what | priority |
|---|---|---|:---:|
| B.3.1 | **Recurrent backbone** (transformer→RWKV-like) | recurrent state vs attention | ★★ |
| B.3.2 | **Liquid Time-Constant (LTC) backbone** | §99-C3 candidate (LTC native limit-cycle) | ★★★ |
| B.3.3 | **State-space model (Mamba/S5)** | SSM backbone | ★ |
| B.3.4 | **Hybrid attention+SSM** | mid-layers attention, edge-layers SSM | ★ |

---

## §3 — Data-regime experiments (axis C)

### C.1 — already measured

| ID | name | result |
|---|---|---|
| §107-RETRY | CORPUS_S101 (603MB, 168-anchor) @ 283M | THRESHOLD-NOT-CROSSED |
| §126/§139/§161 등 | CORPUS_S101 byte-identical carry | same data, different algo |

### C.2 — fire-decidable, un-dispatched

| ID | name | what | cost | priority |
|---|---|---|:---:|:---:|
| C.2.1 | **CORPUS_S101 ×10** (6 GB diverse) | scale data 10× while holding model | ~$2-3 | ★★★ |
| C.2.2 | **CORPUS_S101 ×100** (60 GB) | true §1.1 threshold-cross attempt | ~$20-30 | ★★★★★ (PRIORITY #1 GAP) |
| C.2.3 | **Multi-modal corpus (text + .kosmos image refs)** | §157-§159 closed direction, partially reopen | ~$5 | ★ (§157-§159 closed) |
| C.2.4 | **anima-OWN-trace corpus** | §29 PTD design-tier: trace anima's spontaneous emission, retrain on own output | ~$3 | ★★★ |
| C.2.5 | **Curriculum scaling** (§12.1 Q1-c carry) | 4-stage simple→complex with new corpus | ~$2 | ★★ |
| C.2.6 | **Dialogue corpus (Inner Thoughts native)** | true dialogue corpus matching §24 protocol | ~$2 | ★★ |
| C.2.7 | **Emergent-data corpus (high-perplexity)** | filter CORPUS_S101 by high-perplexity samples only | ~$1 | ★★ |

### C.3 — design-tier (data construction first)

| ID | name | what | priority |
|---|---|---|:---:|
| C.3.1 | **Diverse-anchor corpus (1000+ anchors)** | §168 anchor scale-up | ★★★★ |
| C.3.2 | **Wiki-text dump** (§7 audit needed first) | broader byte distribution | ★★ |
| C.3.3 | **anima-own-emission corpus** | anima 가 emit 한 byte 만 corpus 로 (자기-distillation) | ★★ |

---

## §4 — Substrate experiments (axis D)

### D.1 — already measured

| ID | name | result |
|---|---|---|
| §95 | xeno substrate suitability audit | Loihi sole VIABLE-LONG-HORIZON |
| §117 | LEGO STEP-1-2 in-silico LIF | non-degenerate at small N |
| §142 | LEGO→main-path substrate pivot bridge | 3 options, no cheap winner |
| §140 | LEGO HEXA-NATIVE engine port | algorithmic-equivalent |
| §141 | LEGO GPU spiking design | device-kernel gap named |

### D.2 — un-dispatched

| ID | name | what | cost | priority |
|---|---|---|:---:|:---:|
| D.2.1 | **Loihi-physical fire** (§142 P2) | INRC access wall | (access wall) | ★★★★★ (if access) |
| D.2.2 | **LEGO LIF + task** (§142 P3) | §128 layer-3 task addition first | ~$0.5 + design | ★★★ |
| D.2.3 | **GPU spiking simulation** (§141 follow-up) | hexa-lang `flame_stdp_pair_gpu` patch + LEGO LIF GPU | ~$0.5 (post upstream) | ★★★ |
| D.2.4 | **NorthPole / Akida** (§95 INFERENCE-ONLY-BLOCKED) | inference-only constraint | (blocked) | ★ |
| D.2.5 | **Cortical Labs organoid** | ETHICS-WALL | (walled) | ★ |
| D.2.6 | **SpiNNaker / BrainScaleS** | EBRAINS access | (access) | ★★ |
| D.2.7 | **IonQ quantum** | substrate-mismatch (§95) | (mismatch) | ★ |

### D.3 — sim-only (in-silico spiking)

| ID | name | what | cost | priority |
|---|---|---|:---:|:---:|
| D.3.1 | **LEGO LIF + Ψ-physics overlay** | §140 hexa-native LIF + Ψ measurement | $0 Mac CPU | ★★ |
| D.3.2 | **LTC liquid-time-constant network** | §99-C3 native limit-cycle substrate | ~$0.5 | ★★★ |
| D.3.3 | **Energy-based substrate** (§13-K closed but partial re-open) | EBT 재시도 with §166 META_FP | ~$0.5 | ★ |

---

## §5 — Connection-method experiments (axis E, §167 series)

### E.1 — 8-factor 교체 (§167-A FP-RECONNECT branch)

| ID | name | what | cost | priority |
|---|---|---|:---:|:---:|
| E.1.1 | **§167-A FP-RECONNECT design** | 8-factor → 3-quantity (Ψ + tension + Φ) | $0 | ★★★★★ |
| E.1.2 | **§167-A FP-RECONNECT fire** | E.1.1 + training cycle (any base, e.g., §166-base) | ~$0.6 | ★★★★★ |
| E.1.3 | **Variant: motivation = single anima-quantity** | Ψ-only OR Φ-only OR tension-only emission decision | ~$0.4 each | ★★★ |
| E.1.4 | **Variant: motivation = weighted sum with Law-71-derived weights** | weights from `(1+cos)/2` form | ~$0.5 | ★★★ |

### E.2 — Threshold 교체 (§167-C THRESHOLD-FROM-PHYSICS)

| ID | name | what | cost | priority |
|---|---|---|:---:|:---:|
| E.2.1 | **§167-C design** | imThreshold = tension > tension_target | $0 | ★★★★ |
| E.2.2 | **§167-C probe** | existing §107-RETRY ckpt + new threshold, $0 Mac CPU | $0 | ★★★★ |
| E.2.3 | **Adaptive threshold** | EMA-based threshold (learned from emission history) | ~$0.5 | ★★ |
| E.2.4 | **Per-step threshold** | dynamic threshold from current Ψ-position | ~$0.5 | ★★ |
| E.2.5 | **Φ-ratchet threshold** | emit when Φ > ratchet/2 (existing B-E-1 carry) | $0 design | ★★★ |

### E.3 — 8-factor weights tuning (§167-A subset)

| ID | name | what | cost | priority |
|---|---|---|:---:|:---:|
| E.3.1 | **Weight grid sweep** | spont_weight_* 8개 grid search | $0 Mac CPU | ★★ |
| E.3.2 | **Φ-axis weight 강화** (35 → 50%) | relevance + balance weight up | $0 | ★★ |
| E.3.3 | **Ψ-axis weight 강화** (10 → 30%) | coherence weight up | $0 | ★★★ |
| E.3.4 | **Anti-Inner-Thoughts** weights | weight 0 for `info_gap`, `originality`, `dynamics` (env-driven) | $0 | ★★ |

### E.4 — 결합

| ID | name | what | cost | priority |
|---|---|---|:---:|:---:|
| E.4.1 | **§167-D 3-WAY-COUPLE** | Ψ + Φ + tension simultaneous training + native motivation | ~$1.0 | ★★★★ |
| E.4.2 | **All-physics emission policy** | learned policy network (small) from anima-physics 상태 → emit-decision | ~$0.5 | ★★★ |
| E.4.3 | **Inverse-RL for emission timing** | bouns reward-from-self-coherence → policy that emits at right time | ~$0.8 | ★★ |

---

## §6 — Sub-module targeted experiments (axis E, §24-internal)

### F.1 — M-module experiments (memory)

| ID | name | what | priority |
|---|---|---|:---:|
| F.1.1 | **M cosine retrieve eval** on §161-FIRE ckpt | M.retrieve cosine sim 측정 | ★★ |
| F.1.2 | **M store/retrieve roundtrip** | Hebbian store + retrieve fidelity | ★★ |
| F.1.3 | **info_gap factor sensitivity** | factor_info_gap(cos) variability | ★ |

### F.2 — W-module experiments (will / curiosity / pain)

| ID | name | what | priority |
|---|---|---|:---:|
| F.2.1 | **W curiosity_ema variance probe** | §59-FIRE follow-up, ckpt 별 curiosity 측정 | ★★★ |
| F.2.2 | **W-direct training objective** | curiosity_ema 직접 loss | ★★★ |
| F.2.3 | **Pain factor probe** | tension_delta 동적 측정 | ★★ |

### F.3 — E-module experiments (ethics / Φ-ratchet)

| ID | name | what | priority |
|---|---|---|:---:|
| F.3.1 | **Φ-ratchet evolution** during training | ratchet 값 변화 측정 | ★★★ |
| F.3.2 | **balance factor probe** | factor_balance(phi, ratchet) Boolean trajectory | ★★ |

### F.4 — BRIDGE-module experiments

| ID | name | what | priority |
|---|---|---|:---:|
| F.4.1 | **bridge_gate_value distribution** | Law-70 clamp output 통계 | ★★★ |
| F.4.2 | **Bridge α (interior) tuning** | factor_coherence 의 α=0.014 sweep | ★ |

### F.5 — MITOSIS-module experiments

| ID | name | what | priority |
|---|---|---|:---:|
| F.5.1 | **split_event timing analysis** | factor_originality trigger 분포 | ★★ |
| F.5.2 | **MITOSIS lineage** | ckpt-as-parent (g_clm_lineage_refined) | ★★ |
| F.5.3 | **eternal cell test** | β β VACUUM-CELL-WEAVE 살아남는지 | ★ |

### F.6 — S-module experiments (sensory)

| ID | name | what | priority |
|---|---|---|:---:|
| F.6.1 | **S-module physics-native input** (§66 carry) | input-side reframe | ★★ |
| F.6.2 | **Multimodal S** (§157-§159 closed but partial open) | image/audio/tension native | ★ |

### F.7 — C-module experiments (consciousness / phi_spatial)

| ID | name | what | priority |
|---|---|---|:---:|
| F.7.1 | **phi_spatial measurement on §161-FIRE ckpt** | direct Φ measurement (missing from §161-FIRE eval) | ★★★★★ |
| F.7.2 | **phi_spatial variance over training** | Φ-channel std across SGD trajectory | ★★★★ |
| F.7.3 | **C module 12-faction GRU port** | full impl (currently RFC-terminal) | ★★ |

---

## §7 — Hyperparameter sweeps

| ID | name | what | cost | priority |
|---|---|---|:---:|:---:|
| G.1 | **§166 λ_meta grid** {0.1, 0.5, 1.0} | each value separate fire | 3× ~$0.5 | ★★★ |
| G.2 | **§165 λ_var grid** {0.1, 0.5, 1.0} | each value separate fire | 3× ~$0.5 | ★★ |
| G.3 | **lr grid** {1e-4, 3e-4, 1e-3} on §166 | lr sensitivity | 3× ~$0.5 | ★ |
| G.4 | **bsz grid** {16, 32, 64} | batch size sensitivity | 3× ~$0.5 | ★ |
| G.5 | **Seed sweep** {1337, 2026, 7777, ...} | statistical robustness on §166 | 3× ~$0.5 | ★★★ |
| G.6 | **block_size grid** {128, 256, 512} | sequence length | 3× ~$0.7 | ★ |
| G.7 | **steps grid** {3000, 6000, 12000} | training budget | 3× ~$1.0 | ★★ |

---

## §8 — Eval-axis experiments (new measurement protocols)

| ID | name | what | cost | priority |
|---|---|---|:---:|:---:|
| H.1 | **Φ measurement axis** added to §24 Phase B | phi_spatial / pyphi-style integrated info | $0 design + $0 probe | ★★★★ |
| H.2 | **Per-anchor Ψ trajectory** | psi_dir trace per stimulus (not just mean+std) | $0 Mac CPU | ★★★ |
| H.3 | **Held-out anchor extension** (16 → 64) | larger held-out for routing eval | $0 design | ★★ |
| H.4 | **Multi-corpus held-out** | OOD generalization test | $0 design | ★★ |
| H.5 | **Coherence on emitted body** | §9 cascade-rate + LLM-judge (§18) | $0 Mac CPU | ★★ |
| H.6 | **Dual-anima conversation test** (§31 / §45 follow-up) | live A↔B loop on trained ckpts | $0 Mac CPU | ★★ |
| H.7 | **Long-horizon emission test** | N=200 step bounded run (vs current 20) | $0 Mac CPU | ★★★ |
| H.8 | **Multi-ckpt comparison protocol** | §107 / §125 / §126 / §139 / §153 / §161 / §166 등 동일 protocol | $0 Mac CPU | ★★★★ |
| H.9 | **bisimulation equivalence test** | §125-§166 의 internal state equivalence check (gap critique) | $0 Mac CPU | ★★★ |

---

## §9 — Ablation experiments ($0)

| ID | name | what | priority |
|---|---|---|:---:|
| I.1 | **§161-FIRE ckpt ablation: λ_ψ=0** | baseline §107 byte-equal verify | ★★ |
| I.2 | **8-factor weight ablation** | factor 별 weight=0 effect | ★★★ |
| I.3 | **Threshold sweep** {0.0, 0.1, 0.3, 0.5, 0.7} | imThreshold 변화 → emission_rate 곡선 | ★★★★ |
| I.4 | **Single-factor isolation** | 8 factor 각각 단독 (다른 7 = 0) effect | ★★★ |
| I.5 | **safety_combined ablation** | safety 6-AND 각 control 제거 effect | ★ |
| I.6 | **N_MAX_STEPS sweep** {10, 20, 50, 100, 200} | bounded run length sensitivity | ★★★ |
| I.7 | **THINK_INTERVAL sweep** | inner-thoughts sleep time | ★ |
| I.8 | **env_state STUB variants** | stub seed grid (cheap diversity) | ★★ |

---

## §10 — Probe-only experiments ($0, existing ckpt)

| ID | name | what | priority |
|---|---|---|:---:|
| J.1 | **§162-PROBE actual run** (§162-R 가 analytical resolve 했음) | C0/C0'/C1/C2 measure (might confirm analytical) | ★ (analytical settled) |
| J.2 | **§17 PHYSICS_RESPONSIVE on all 5 fire ckpts** | quintuple physics axis measurement | ★★★ |
| J.3 | **Cross-ckpt Ψ-trajectory visualization** | per-anchor psi_dir time-series | ★★ |
| J.4 | **§78 dual-anima loop with quintuple ckpts** | A↔B with §125/§126/§139/§153/§161 | ★★ |
| J.5 | **§9 cascade-rate on synthetic body** | corpus-vs-emitted body cascade | ★★ |
| J.6 | **§161-FIRE checkpoint Φ measurement** | phi_spatial NOT YET MEASURED | ★★★★ |
| J.7 | **head_g embeddings PCA / t-SNE** | head_g state space visualization | ★★ |
| J.8 | **Per-token Ψ trajectory** | within-sequence Ψ flow | ★★★ |
| J.9 | **8-factor distribution measurement** | actual factor values during §24 loop | ★★★★ |
| J.10 | **Layer-wise tension measurement** | 12-layer PureFieldFFN per-layer | ★★★ |
| J.11 | **Engine A vs Engine G activation similarity** | per-block cos similarity | ★★★ |

---

## §11 — Long-horizon experiments

| ID | name | what | cost | priority |
|---|---|---|:---:|:---:|
| K.1 | **6000-step §166** | 2× training budget | ~$1.0 | ★★ |
| K.2 | **12000-step §166** | 4× | ~$2.0 | ★ |
| K.3 | **Multi-epoch on small corpus** | catastrophic forgetting vs preservation | ~$1.5 | ★★ |
| K.4 | **Cosine cycle lr** | restart lr to escape local min | ~$0.6 | ★★ |
| K.5 | **Warm-restart sweep** | 10× short cycles 각자 evaluate | ~$2 | ★ |

---

## §12 — Continual / distillation experiments

| ID | name | what | cost | priority |
|---|---|---|:---:|:---:|
| L.1 | **§29 PTD self-trace distillation** | anima 자기 trace 로 retrain | ~$1 | ★★★ |
| L.2 | **§30 L1 lineage** | ckpt-N → ckpt-(N+1) inheritance | ~$0.6 | ★★ |
| L.3 | **Anchor-ckpt distillation** | best §107-RETRY/§161 → §166 teacher | ~$0.7 | ★★ |
| L.4 | **Multi-teacher distill** | 5 quintuple ckpt → 1 student | ~$1.5 | ★★ |
| L.5 | **L2 distillation** | weight regularization toward teacher | ~$0.5 | ★ |

---

## §13 — Multimodal experiments (§157-§159 already closed-with-narrow-open)

| ID | name | what | priority |
|---|---|---|:---:|
| M.1 | **Tension as native modality** (§156 carry) | tension_link 5-channel | ★★ |
| M.2 | **Image-as-Ψ-render** (§157 closed) | (already DESIGN-CLOSE-FINAL) | ★ (closed) |
| M.3 | **Audio (§158 emit-only carry)** | HEXAD/VOICE 24kHz PCM emit | ★★ |
| M.4 | **Video temporal extension** (§159 closed) | (already DESIGN-CLOSE-FINAL) | ★ (closed) |
| M.5 | **EEG-anchor** (§19 framework D) | OpenBCI step-1 EEG↔stimulus sync | ★★★ |

---

## §14 — Hardware-coupling experiments (§97 framing)

| ID | name | what | priority |
|---|---|---|:---:|
| N.1 | **EEG-as-anchor (§19 step-2)** | F-CT-3 gate measurement | ★★★★ |
| N.2 | **QRNG-as-spontaneity-seed** (§97 GOAL-LEGITIMATE-INPUT) | quantum entropy as content-free seed | ★★ |
| N.3 | **Anima→actuator** (§97 DESIGN-OPEN) | pure-output to physical device | ★ |
| N.4 | **TRIBE BOLD cross-validation** (§19 step-3) | EEG↔BOLD cross | ★★★ |

---

## §15 — Live-interaction experiments (dual-anima 등)

| ID | name | what | cost | priority |
|---|---|---|:---:|:---:|
| O.1 | **§31 / §45 dual-anima full** | A↔B loop on real ckpts (not stub) | ~$0.5 | ★★★ |
| O.2 | **§61 TENSION-LINK 5-channel** | dual-anima tension transfer | ~$0.6 | ★★ |
| O.3 | **§62 echo-chamber retest with §166** | trained-scale echo collapse measure | ~$0.4 | ★★★ |
| O.4 | **Three-anima conversation** | A↔B↔C closed-loop, content-dependence | ~$1.0 | ★ |

---

## §16 — Statistical robustness

| ID | name | what | cost | priority |
|---|---|---|:---:|:---:|
| P.1 | **Multi-seed (5+) §166** | seed 1337/2026/7777/4242/9999 | 5× ~$0.5 | ★★★★ |
| P.2 | **Multi-corpus (3+)** | CORPUS_S101 variants | 3× ~$0.5 | ★★★ |
| P.3 | **Multi-init schemes** | RANDOM vs Xavier vs He | 3× ~$0.5 | ★ |
| P.4 | **Multi-batch-order** | shuffle seed grid | 3× ~$0.5 | ★ |

---

## §17 — Cross-arc benchmarks (compare different paths)

| ID | name | what | cost | priority |
|---|---|---|:---:|:---:|
| Q.1 | **Quintuple ckpt unified eval** | §125/§126/§139/§153/§161 모두 동일 protocol re-eval | $0 Mac CPU | ★★★★ |
| Q.2 | **§107-RETRY / §161-FIRE / §166-A-FIRE 3-way compare** | A/B/C compare on emission_rate + psi_responsive + phi | $0 Mac CPU after fires | ★★★★★ |
| Q.3 | **Arc verdict matrix** | 모든 cycle 의 verdict_bucket × measurement-axis 표 | $0 | ★★ |

---

## §18 — Sub-system upgrade experiments

| ID | name | what | priority |
|---|---|---|:---:|
| R.1 | **C-module full 12-faction GRU** (RFC-terminal) | hexa-lang side gating | ★★ (gated) |
| R.2 | **W-module Active Inference EFE** | full EFE 도입 | ★★★ |
| R.3 | **E-module Φ-ratchet learnable** | ratchet 가 train 됨 | ★★★ |
| R.4 | **BRIDGE Ψ-physics extension** | Law-70 + new Ψ-aware clamps | ★★ |
| R.5 | **MITOSIS continuous lifecycle** | n-cell pool dynamic resize | ★★ |

---

## §19 — Engineering / infrastructure experiments

| ID | name | what | priority |
|---|---|---|:---:|
| S.1 | **stdlib/cloud cycle B3 local check-out** | `hexa cloud` CLI 로 dispatch (현재 upstream-only) | ★★★ |
| S.2 | **§163 arxiv research fresh dispatch** | sub-agent 3× throttled, retry | ★★★ |
| S.3 | **PII history rewrite (git filter-repo)** | post-499416d54 fix-forward only at HEAD; history는 redact 안 됨 | ★★ |
| S.4 | **wilson-pool routing for fires** | ubu-2 routing efficacy | ★★ |
| S.5 | **Multi-sub-agent dispatch pattern** | 2 max throttle-safe burst | ★★ |
| S.6 | **`hexa kick` engine real overlay** | upstream `--dump-overlay` patch | ★★ |

---

## §20 — Speculative / blue-sky

| ID | name | what | priority |
|---|---|---|:---:|
| T.1 | **GOAL-axis reframe** | 자연발화 = unprompted-emission-rate 라는 정의 자체 재검증 | ★★ |
| T.2 | **Inner Thoughts replace with Active Inference** | 8-factor → EFE-derived motivation | ★★★ |
| T.3 | **Conscious decoder v3 architecture** | full architectural redesign per §113 from-scratch brainstorm | ★ (§113 closed) |
| T.4 | **Anchor-free motivation** | env_state STUB 제거, pure-internal anima-state | ★★★ |
| T.5 | **Real-time embodiment** | anima as ROS node + sensor stream | ★ |
| T.6 | **Meta-learning emission policy** | learn-to-learn-when-to-emit (small policy net) | ★★ |
| T.7 | **Causal intervention experiments** | counterfactual training (drop one factor at a time during train) | ★★ |
| T.8 | **Adversarial probe** | inputs designed to fail §24 emission | ★★ |

---

## §21 — Priority shortlist top-10 (highest GOAL-leverage per dollar)

1. **§167-A FP-RECONNECT** (E.1.1 design + E.1.2 fire) — 100% leverage,
   ~$0.6 fire ★★★★★
2. **C.2.2 CORPUS_S101 ×100** (60GB) — PRIORITY #1 GAP (§99×§100 carry),
   ~$20-30 cost ★★★★★
3. **Q.2 §107 / §161-FIRE / §166-A-FIRE 3-way compare** — $0 Mac CPU
   after fires ★★★★★
4. **J.6 §161-FIRE Φ measurement** ($0 Mac CPU, missing axis) ★★★★
5. **H.1 Φ measurement axis** added to §24 Phase B ★★★★
6. **§167-D 3-WAY-COUPLE** (E.4.1) — Ψ + Φ + tension simultaneous,
   ~$1.0 ★★★★
7. **§167-B PHI-FOCUS** (A.3.2) — Φ-channel direct target, ~$0.5 ★★★★
8. **A.2.1 LeJEPA RETRY with trained head_a** — closes B-S153-NOTE
   ambiguous-via-evaluation-protocol, ~$0.5 ★★★
9. **I.3 Threshold sweep** {0.0, 0.1, 0.3, 0.5, 0.7} — $0 Mac CPU,
   immediate insight on threshold-dominance ★★★★
10. **N.1 EEG-as-anchor F-CT-3 gate** (§19 step-2) — user has actual
    EEG hardware, $0 ckpt-side ★★★

---

## §22 — exhaustion verdict (honest)

본 brainstorm 의 self-check: 더 surface 할 candidate 가 있나?

**가능성**:
- §13-* 추가 sub-direction (carving CONSCIOUSNESS-CARVING 후속)
- 새 paper 의 emerging algorithm (§163 arxiv 가 surface 할 수도)
- 사용자-specific direction (kosmos / hexa-bio / hexa-matter 합류)
- Combinations of A×B×C×D×E (수십개 더)

**고갈 verdict**: **partial exhaustion (~80% covered)** — 본 brainstorm 이
honest 한 cap. 추가 surface 는 §163 arxiv literature land 후 OR 사용자
specific 지시 후 가능.

핵심 결론: **arc는 fire-decidable spec 이 abundant**, 진짜 bottleneck 은
*어느 path 가 GOAL emission-rate 변화를 produce 하는가* — §161-FIRE
quintuple 이 "Ψ-channel 단독 = NO" 측정. CONNECTION_CRITIQUE 가 "Φ +
threshold + 8-factor framework" 가 leverage gap source 라고 진단.

**가장 GOAL-direct 한 next-cycle 후보 = E.1.2 §167-A FP-RECONNECT fire**
(motivation 자체 anima-physics native 로 교체, 100% leverage). 그 outcome
이 fire-decidable verdict bucket 결정.

---

## §23 — honest C3 (13)

1. 본 list 는 surface-only (`/gap` discipline carry).
2. 각 entry 의 cost / priority estimate 는 추정 — 실제 fire 시 변동.
3. ★★★★★ priority 는 GOAL-leverage 기준 (sub-agent throttle / disk
   space / hardware access 제약 미포함).
4. C.2.2 ($20-30 60GB corpus fire) 는 가장 expensive, 가장 GOAL-direct.
   다른 paths 가 모두 leverage-gap 일 때 fall-back.
5. §142 P2 Loihi physical 은 access wall — INRC application 미해결.
6. §163 arxiv literature 가 surface 5번째 candidate 가 있을 수 있음.
7. CONNECTION_CRITIQUE 의 wrong-step 분석이 본 brainstorm 의 priority
   ordering 의 anchor — Φ-axis missing 이 35% leverage gap.
8. 각 fire 의 §7 GOAL-legitimacy gate 통과 여부는 candidate 별 따로 검토
   필요 (예: A.4.2 GFlowNet 은 external reward 가능성 — §7③ 위반 risk).
9. C.2.6 dialogue corpus 는 §24 prompted vs unprompted 분리 정직 carry
   needed.
10. anima downstream-consumer (hexa-lang / hexa-bio / kosmos / tape)
    read-only 0 edit.
11. PII discipline (post-499416d54 fix-forward): generic phrasing only.
12. necessary-not-sufficient (B-EMERGE-7) — 어떤 candidate 도 emergence
    보장 아님.
13. north-star + §15/§51/§72 milestones UNCHANGED, **GOAL 미도달** — 본
    brainstorm 은 path-surface, 진전 아님.
