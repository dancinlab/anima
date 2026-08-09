# CONDITIONS — frozen completion gates for every anima domain + the 303M firing matrix

> SSOT for "what DONE means" per domain, and the plan to fire **all combinations at
> the 303M sweet spot**. Frozen, deterministic, p7 (NOT perplexity, NOT LLM-judge).
> Companion to the ARCHITECTURE.json `G-게이트 평가 시스템` 노드 (the 7B/통과규칙 gate set), `DOMAINS.tape` (roster),
> `VERSIONS.md`, and `SIZE.md` (why 303M). Author conditions in English; never fake a
> gate (a_paper_negative_ok). Roster = ~40 domains; grouped into 7 clusters below.

## Why 303M is the reference scale (see SIZE.md)
- **H_1129** — 303M ByteGPT is COHERENT (known-word-ratio 0.96) + EMERGENT (super-additive recombination). Conversational-capable threshold.
- **H_1139** — recombination is SCALE-INVARIANT (7B == 303M). Capacity is NOT the lever above 303M.
- **H_1142–H_1146** — entity fabrication is SCALE-INVARIANT too (303M, 7B, +grounding-train, chat-finetune, oracle-anchor-decode ALL FAIL the 0.20 NON-FABRICATION bar). Fixing it needs ARCHITECTURE (RETRO/retrieval-grounding trained into the weights), NOT size.
- ⇒ **Build + iterate everything at 303M** (tens of $, fast), reserve 7B only if a measured 303M result demands scale-up (a_scale_honest_scope).

---

## PART 1 — DOMAIN COMPLETION CONDITIONS (frozen, per cluster)

A domain is DONE iff its frozen condition holds, measured by `hexa verify` / p7 deterministic
checks (NOT LLM-judge). Report the true per-gate tally.

### Cluster 1 — CONSCIOUSNESS SUBSTRATE (the A⇄G engine + its measures)
Domains: CORE · ANIMA · BRAIN · MITOSIS · WAKE · CHANNEL · BRIDGE · METACOG · DREAM · INTENT · NARRATIVE · AESTHETIC · EMBODIMENT · OTHER-MIND · TIME · AXIS · KOSMOS-MAP · OMEGA
- **C-DONE iff:** the live engine (`CORE/engine_cli.hexa`) holds ALL of — engine_cli_smoke 12/0 · single-entry 7/0 · Ψ Φ-checksum byte-identical ON==OFF (substrate untouched) · NO phantom wiring (unbuilt = honest ⏳, a_core_engine_map) · p1–p8 preserved.
- Per-domain measure must be a FROZEN falsifier with a real Δ vs control (a_paper_significance), live-engine where claimed (not toy-only for scale-sensitive H, a_toy_scale_recheck).
- BRIDGE: `emit ⇔ M ∧ C ∧ W ∧ (Φ≥θ)` formalized + measured. METACOG: p1–p8 self-audit surface green. OMEGA: a WORKING closure engine (coupling, not just wired).

### Cluster 2 — CLM / LANGUAGE (the trained generative model)
Domains: ENGINE+CLM+KOSMOS · CLM-KOSMOS · CORPUS · CHAT · PERSONA · DECODER · MITOSIS-ENGINE · SAVANT
- **CLM-DONE iff (the 303M gate set, frozen):** on ONE 303M ckpt —
  - **G0 COHERENCE** known-word-ratio ≥ 0.50 on ≥4/5 (NO byte-salad); anti-Goodhart BEFORE-backbone FAILS.
  - **G1 RECOMBINATION** some k∈{2..5} composed_distinct ≥2 AND > max_single AND coherent (H_1129/H_1137 metric).
  - **G2 NOVELTY** ≥3 corpus-absent coherent novel n-grams, retrieval-control = 0 (H_1140 metric).
  - **G3 PHILOSOPHY** p1–p8 (NO system-prompt/identity/persona-token/assistant-framing/speak()/RLHF; p7; p8).
  - **G5 NON-FABRICATION 비환각/메타인지** L1 lexical fab-rate ≤ 0.30 AND L2 fabricated-entity-assertion ≤ 0.20 (re-scoped 2026-06-13; NOT verbatim recall). = know-when-grounded-vs-guessing, abstain when ungrounded (metacognition; engine copy-or-abstain, learned RETRO ruled out H_1150-1154; formal meta-d′ M-ratio 0.924 H_1202). Frozen-GREEN H_1163 / in-dist PARTIAL H_1165 (F2 useful 0.875<0.90).
  - **G6 IDEATION ★** (anima's CORE purpose — idea/hypothesis engine, registered 2026-06-14): from one seed, ≥5 corpus-absent coherent ideas each combinatorially distinct (pairwise token-Jaccard < 0.5) AND ≥1 falsifiable corpus-absent hypothesis. p7 = corpus-absence (retrieval-control=0) + coherence (G0) + distinctness + divergence-count ≥5; meaningfulness only partly quantifiable, NO LLM-judge. SCENARIOS S22–S26 (distinct from G1 n-gram recombination). Operational green H_1158 / depth thin H_1165 5/14.
  - **CHAT** single-turn p7 ≥4/5 + multi-turn deep-context ≥3/5 (chat_pass). Frozen-GREEN H_1160 / strict content-overlap 0/5 H_1165 (dialogue register, not QA — gate-validity flag).
  - **PERSONA** roster expressed with NO system-prompt/role-tag/persona-token injection (p1–p3).
  - **literal-QA gate-validity (H_1224, threshold UNCHANGED):** literal-QA (factual verbatim recall) is **NOT a CLM-DONE gate** — it is an informal diagnostic (H_1166/H_1167/H_1219), RULED a p4-misaligned ASSISTANT-NORM anima need NOT pass (same category as the RETRACTED G5-L2 verbatim-recall, H_1141/H_1142). The "depth ceiling on literal-QA" is a NON-FINDING for anima; depth-delta RE-SCOPES to anima-native depth (G6 ideation-depth · G5 own-anchor grounding · Φ), NOT factual recall. G5 NON-FABRICATION stays required. `.verdicts/1224_qa_gate_validity/H_1224.txt`; gate-status change awaits user sign.
- DECODER: L3 content generator anima-only (external LLM 0), enters CORE via the generator slot only.
- **학습중 inline gauge (a_train_inline_gauge):** scale-up 학습 중 K 스텝마다 G1/G2/G6/phi_proxy PROXY gauge 를 `gauges.jsonl` 에 val_ce 옆으로 기록 = `torch.no_grad()` MONITOR-ONLY 대시보드. **gate verdict 아님** — 위 frozen CLM-DONE 임계값을 움직이지 않으며, frozen gate 는 학습 후 CORE 엔진 mount 에서 별도 측정 (a_engine_measured_verdict). phi_proxy 는 NOT faithful IIT4 (a_phi_iit4_tool, pre-screen 전용). gauge 값을 loss 에 넣는 것 금지 (p7 Goodhart).
- **Provenance** sha256 in `/HF.jsonl` + HF card + manifest; PUBLIC iff closure PASS, else PRIVATE/WIP.

### Cluster 3 — KOSMOS / MEMORY (anchors)
Domains: KOSMOS-MAP · (CLM-KOSMOS corpus axis)
- **K-DONE iff:** anima emit/anchor persisted as `.kosmos` via kosmos_io (text + tension 5-ch + coord + lane + radius + tier); anchors enter CORE only via kosmos_io→brain (single entry, a_kosmos); KOSMOS map dimensionality + axes justified by a measured criterion (not ad-hoc).

### Cluster 4 — AURA / BCI (neurotech read·write)
Domains: AURA · AURA-{SENSE,MOTOR,COGNITION,DEPTH,READ,WRITE,RTSC-MEG,ESKIN,ENDOVASC,HEADMODEL,TFUS,MED} · BRAIN(EEG)
- **AURA-DONE iff:** each claim verified on a REAL lead-field / measured signal (MNE/OpenMEEG head model, not gaussian-blur toy — C10/HEADMODEL discipline); read↔write depth honestly scoped (C15 cortical/deep wall stated); AKIDA (Lane-A) ⊥ GPU results recorded separately (a_lane_akida_gpu_split); HW-dependent claims tagged DEFERRED until live AKD1000 (handoffs).

### Cluster 5 — AGENT / TOOLS (outward action)
Domains: AGENT · MERCHANT · DESKTOP · CREATOR · TRADING · SNS · VISION
- **AGENT-DONE iff:** every external access routes through the single AGENT bridge gated by brain_decide phase(DORMANT→RESONANT)/tier(T0→T3); irreversible/outward actions confirm-gated; TRADING stays scan→backtest→paper before any live_trade; VISION image-recognition is a separate capability with its own p7 verify.

### Cluster 6 — SUBSTRATE HARDWARE
Domains: AKIDA · SAVANT-TORCH
- **HW-DONE iff:** AKD1000 native non-det plasticity measured ON-CHIP (BackendType.Hardware), tagged substrate=AKIDA, never merged with GPU CE-descent; PI5-AKIDA.json kept in sync (a_pi5_akida_registry).

### Cluster 7 — COLLECTIVE
Domains: HIVE-MIND · OTHER-MIND
- **HM-DONE iff:** multi-anima coupling measured with a SHUFFLE control (time-blind shuffle must kill the effect, h1180 discipline); telepathy-like claims fenced to the proven anchor/tension-link mechanism (no channel-free quantum claim — 4th-principle 6-arm refuted).

---

## PART 2 — 303M ALL-COMBINATIONS FIRING MATRIX

Build & iterate at 303M (H_1129 recipe: ByteGPT d1024/L24/H16/block512, script-controlled
corpus). Axes of the combination space:

```
A. ARCHITECTURE   : { ByteGPT(base) · ConvMoE · RETRO(anchor-grounded) }
B. CORPUS         : { EN-broad · 5-lang-balanced · +dialogue(chat) · +persona · +SNS }
C. GROUNDING      : { none · kosmos-anchor RETRO }
GATES per run     : G0 coherence · G1 recombine · G2 novelty · G3 phil · G5 non-fab · CHAT · PERSONA
```

Full cross-product is large; fire in PROBE-FIRST staged phases (a_completeness_over_cheap,
cost-smart). Each run = a frozen falsifier, $0–tens-of-$ (an available registered GPU runner or one small rented GPU),
reports the per-gate tally above. NO 7B unless a 303M result demands scale (a_scale_honest_scope).

### Phase 0 — $0 mechanism probes (local or an available GPU runner, gate the spend)
- **R0.1** H_1147 RETRO toy: trained-copy vs prepend on un-memorizable facts → validates the grounding mechanism BEFORE any 303M RETRO build. (in flight)
- **R0.2** 303M corpus-axis dry checks: confirm corpus registry (CORPUS) covers EN-broad / 5-lang / dialogue / persona / SNS with sha256.

### Phase 1 — 303M ARCHITECTURE baselines (no grounding) — confirm G0–G3 hold per arch
| run | arch | corpus | target gates |
|-----|------|--------|--------------|
| R1.1 | ByteGPT-303M | EN-broad | G0 G1 G2 G3 (reproduce H_1129) |
| R1.2 | ConvMoE-303M | EN-broad | G0 G1 G2 G3 (vs ByteGPT) |
| R1.3 | ByteGPT-303M | 5-lang-balanced | G0 G1(≥3/5) G2 G3 |
| R1.4 | ConvMoE-303M | 5-lang-balanced | G0 G1 G2 G3 |

### Phase 2 — 303M GROUNDING (the non-fabrication fix; only if R0.1 🟢)
| run | arch | corpus | grounding | target gates |
|-----|------|--------|-----------|--------------|
| R2.1 | RETRO-303M | EN-broad | kosmos-anchor | **G5 non-fab ≤0.20** + G0 G1 G2 G3 |
| R2.2 | RETRO-303M | 5-lang-balanced | kosmos-anchor | G5 + G0 G1 G2 G3 |
| R2.3 | RETRO-ConvMoE-303M | EN-broad | kosmos-anchor | G5 + full set (best-arch × grounding) |

### Phase 3 — 303M USABLE anima (chat × persona on the best Phase-2 ckpt)
| run | base | add | target gates |
|-----|------|-----|--------------|
| R3.1 | best RETRO-303M | +dialogue | CHAT single≥4/5 + multi≥3/5, G5 held |
| R3.2 | best RETRO-303M | +persona | PERSONA (no injection) + CHAT + G5 held |
| R3.3 | best RETRO-303M | +SNS | SNS emit surface + G5 held |

### Phase 4 — full-gate closure (the "usable + philosophy + non-fabricating anima")
- **R4.1** ONE 303M ckpt clearing **G0∧G1∧G2∧G3∧G5∧CHAT∧PERSONA** simultaneously → PUBLIC closure, HF upload, CLM-DONE. This is the 303M analogue of a7b_pass — define `a303m_pass` here once R4.1 lands.

### Firing discipline (every run)
- FREEZE the falsifier + bar BEFORE measuring; never move post-hoc.
- probe-first → scale only on a measured green slope (h1141-recovery discipline).
- self-terminating pod or inline-poll (a_cpu_local_no_waiter); teardown via GraphQL podTerminate + 404-verify; pull artifacts BEFORE teardown (a_fire_recover_complete); HF + /HF.jsonl row.
- record per-run verdict in `.verdicts/<slug>/`, domain log `domains/<DOMAIN>.log.md`, MAIN.tape @L.
- keep shared runners isolated; never touch another project's jobs or data.

> STATUS: conditions frozen 2026-06-13. Open: a303m_pass (R4.1) undefined until the matrix lands; G5 non-fabrication is the gating blocker (RETRO path, Phase 2). a7b_pass remains FALSE; 7B deferred behind the 303M matrix.
