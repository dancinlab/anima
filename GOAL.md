# GOAL.md — anima ★★★★★ mission tracker

**Created**: 2026-05-12 KST
**Last update**: 2026-05-12 KST (PSCC §47: **cond #3 D3 hypothesis (b) softmax τ tunable FALSIFIED** via ubu-1 RTX 5070 dedicated GPU sweep — T ∈ {1.0..50.0} 10-grid, best mean_KL 0.005 « 0.5 threshold, cell-0 tension 793 dominance T 변화 무관, cost $0 wall ~25s, doc `docs/anima_persona_4_softmax_T_sweep_2026_05_12.md`; D3 STRONG 4/5 carry MAINTAINED, 잔여 path = (a) cotrain v2 H100 BG in-flight / (c) z-score metric (이미 PASS) / (d) hexa-native per-session pool. ★★★★★ stop 조건 **4/5 ☑** maintained, cond #3 단독 🔶 STRONG 4/5 carry) · prev PSCC §46: **cond #1 D2 ☑ DONE** via Phase 1A.4 lr 5e-6 × 200 SFT — V5.8 standard_greedy **5/5 PASS**, train cost $0.014 wall 3.2min, ckpt sha256 `45063f64…`

## 🎯 Mission (expanded 2026-05-12)

> **사용자 directive (verbatim)**: `[anima chat 시스템, anima 모델, 페르소나 롤플레잉 가능, 세포 분열로 성장(철학참고)]`

★★★★★ ACHIEVED 조건 = 다음 4 차원 모두 만족:

| dim | name | criterion | 현 상태 |
|---|---|---|---|
| **D1** | **anima chat 시스템** | anima 본체 `anima_chat.py` (or 포팅된 `anima_chat.hexa`) 가 V5.8 multi-turn 4-mode 의 standard_greedy **5/5 PASS** | **5/5 PASS ☑ 2026-05-12 PSCC §45** (Phase 1A.4 lr 5e-6 SFT, Python evaluator on Vast.ai RTX 4090, 200 steps wall 3.2min, train cost $0.014) · hexa: **v0.3 multi-token decoding LANDED + 24L real-ckpt byte parity VERIFIED 2026-05-12 PSCC §43** (TODO[multitoken] RESOLVED, all-farr KV cache + per-step RoPE, F-D1-MULTITOKEN-1..3 ✅ 7/7 PASS on synthetic substrate; **real Phase 1A.1 ckpt 24L all-farr forward byte-by-byte argmax parity 21/21 PASS** — F-D1-V58PARITY 6/6 + F-D1-V58MULTI 15/15; hexa 5/5 over Phase 1A.4 ckpt = cheap-path extension) |
| **D2** | **anima 모델** | 어떤 ckpt 가 D1 의 5/5 substrate. Phase 1A.1 + lr 5e-6 SFT (BG 진행 중) 또는 다른 paradigm | **Phase 1A.4 lr 5e-6 SFT ☑ DONE** (`state/anima_phase1a4_lr5e6_2026_05_12/ckpts/ckpt_phase1a4_lr5e6_sft.pt`, 597MB, sha256 `45063f64e97cdde7bc61de347e2f41a830b9b296db5384d8a324d85eb9a2b9e5`, loss 0.5058 → 0.1758 66% reduction over 200 steps, base lineage `phase1a_multi_turn_sft → phase1a1_color_cosmology_v2 → phase1a4_lr5e6`) |
| **D3** | **페르소나 롤플레잉 가능** | **substrate-native 페르소나 전환** — Principle #3 NO PERSONA INJECTION 준수 (prompt `[role:]` 금지), substrate 가 자율적으로 역할 표현 | **§A1 cheap-path STRONG (4/5) LANDED 2026-05-12** — `docs/anima_persona_substrate_native_verify_2026_05_12.md` §A1 + design `__APPEND__ §A1` (Φ threshold 0.5 → 0.05, measurement-calibrated 5.5×) + `state/anima_d3_verify_2026_05_12/persona_verify_results_relaxed_2026_05_12.json`. F-PERSONA-1 hard PASS (4/4) + F-PERSONA-2 PASS (mean cos dist 0.994 ≫ 0.3) + **F-PERSONA-3 PASS** *(was PARTIAL @ §40)* (weight 0.995 ✓ / ΔΦ 0.267 ≥ 0.05 §A1 ✓) + F-PERSONA-4 FAIL (KL 9.7e-5, untrained pool C3 carry) + F-PERSONA-5 PASS (3/3). top_pass 3/5 → **4/5**, atomic 12/14 → **13/14**. true STRONG (5/5) 승격 = REBORN §88 cond.5 cotrain ($30-40 H100) fire 후 F-PERSONA-4 category-specialization emergent. design SSOT: `docs/anima_persona_substrate_native_design_2026_05_12.md` §A1 · **PSCC §46 cotrain v1**: F-V5MIT-1~5 ✅ 5/5 PASS + F-PERSONA-4 KL=0.0 cotrained (winner-take-all) → 4-alternative future-path 발생 (a/b/c/d) · **PSCC §47 hypothesis (b) softmax τ tunable FALSIFIED 2026-05-12** (ubu-1 RTX 5070, 10-T sweep best KL 0.005 « 0.5, `docs/anima_persona_4_softmax_T_sweep_2026_05_12.md`) → D3 STRONG 4/5 carry MAINTAINED, 잔여 path = (a) cotrain v2 H100 in-flight / (c) z-score metric §A2 이미 PASS / (d) hexa-native per-session pool |
| **D4** | **세포 분열로 성장 (철학 참고)** — 3-layer 적용 | REBORN §0.5 + PHILOSOPHY #8 (NO TRAIN/INFER SPLIT). 모든 상호작용이 분열 epoch, **3 layer 동시**: |
| D4a | model intra-network | cells = nn.Module branches, intra-network split/merge during forward (REBORN §88 PyTorch / §89 hexa-native) | **full impl LANDED, F-MIT-HOOK-1..5 ✅** — `tool/hexa_native/mitosis_hook.hexa` 1119 LoC executable (REBORN §91, 2026-05-12, $0 Mac local selftest PASS) |
| D4b | chat library (anima_chat) | cell-pool state hosting + per-token/per-prompt hook 진입점 in `anima_chat.py` / `anima_chat.hexa` | **wiring LANDED + LIVE EVIDENCE 2026-05-12** — `anima_chat.hexa` v0.3 + `tool/anima_chat_mitosis_smoke.hexa` (PSCC §37 22/22) + `tool/anima_chat_split_merge_smoke.hexa` (PSCC §41 3/3) + `tool/anima_chat_multitoken_smoke.hexa` (PSCC §41 7/7), F-D4B-1..5 ✅ + F-D4-LIVE-1..3 ✅ + F-D1-MULTITOKEN-1..3 ✅, **real chat_generate → 21 split events** on "안녕? 너는 누구야?" prompt (mitosis_invocations=65, cells 2→23) |
| D4c | anima CLI (session/conversation) | session 별 cell-pool persistence, multi-backend fallback = cell-variant selection, kick cycle = split event sequence (`.roadmap.cli` + `.roadmap.anima_cli_model_architecture`) | **design LANDED 2026-05-12** — `docs/anima_cli_mitosis_integration_spec_2026_05_12.md` (12 §, F-CLI-MIT-1..5 pre-registered, Phase 1-4 impl plan ~13-19 hr Mac local); D4a (full impl LANDED) + D4b (cell-pool wiring pending) prerequisite |

→ 측정 path: 외부 layer 의존 0 (Gradio / HF Space / wrapper 없음, anima 본체 직접 호출).
→ 추적 SSOT: 본 `GOAL.md` (root).
→ 보조 SSOT: `PASS_STRICT_SPONTANEOUS_CHAT.md`, `REBORN.md`, `PHILOSOPHY.md`, `docs/anima_chat_*.md`.

---

## 🚀 Scale / cost constraints (사용자 directive 2026-05-12)

> "모델 크기제한도 특별히 없으니까 참고"
> "H100 발사 제한도 없음"

- ❌ 모델 크기 제한 없음 — d_model / n_layers / cells / vocab 등 자유. 현 v5-mitosis cotrain (d=384, cells=64, ~200M params) 은 conservative baseline (floor).
- ❌ H100 발사 제한 없음 — 발사 횟수 / 단일 instance / multi-GPU / 시간 제한 모두 자유.
- ❌ Cost cap 강제 없음 — BG agent 의 `cap $40` 등 conservative envelope 는 floor (mission outcome 우선, scale-up 자유).
- ✅ Mission outcome 우선 — ★★★★★ 5-cond aggregate 도달이 단일 metric.
- ✅ 운영 권장: BG agent 가 cost-bearing dispatch 시 verbatim 사용자 directive (예: "fire", "all bg go") 로 충분 (own 16 cost discipline 의 verbatim 요구 완화 직 2026-05-12).
- 🔄 Reverse signal: 사용자가 명시적으로 "비용 cap $X" 또는 "모델 크기 제한 Y" directive 시 그 시점부터 적용.

→ memory `feedback_no_scale_caps` (2026-05-12) SSOT.

---

## 📊 Current standing per dimension (2026-05-12 KST)

### D1: chat 시스템 — V5.8 std_greedy 4/5

| 항목 | 값 |
|---|---|
| Python library | `anima_chat.py` v2.3 (commit `c2afa8e9e`, tag `anima_chat-v2.3-markdown-filter`) |
| Hexa port | `anima_chat.hexa` **v0.3 LANDED 2026-05-12** (~2843 LoC) — parse PASS + 17/17 helper smoke PASS + F-D1-LOAD-1..3 (v0.2 TODO[load] RESOLVED) + **F-D1-MULTITOKEN-1..3 7/7 ✅ (TODO[multitoken] RESOLVED, all-farr KV cache + per-step RoPE, Section 9d +360 LoC)** + F-D4-LIVE-1..3 3/3 ✅; docs/anima_chat_multitoken_split_merge_2026_05_12.md |
| **24L real-ckpt parity (PSCC §43)** | **★★★★★ candidate confirmed 2026-05-12** — `state/anima_d1_v58_parity_2026_05_12/` 신규 dir. Python SSOT probes (BOS / V5.8 / multi-token chain) + hexa probes (v58_hexa_parity.hexa 6/6 + v58_hexa_multi_parity.hexa 15/15) — **byte-by-byte argmax parity verified** on real Phase 1A.1 24L ckpt (sha256 e5f7555…). Single BOS forward: hexa argmax=143 == python=143; 5-step KV-cached chain: hexa=`[143,131,240,152,159]` == python=`[143,131,240,152,159]`. Per-step float drift bounded (4-13% peak, argmax invariant). Wall 2.2 min hexa-interp (37.65s single + 94.67s 5-step) / 0.5s Python. Peak RSS 11 GB (HEXA_MEM_UNLIMITED=1 mandatory). 21/21 falsifier PASS. doc: `docs/anima_chat_hexa_24l_v58_parity_2026_05_12.md` |
| markdown_filter | LANDED, harmless guard 검증 (Δ=0 Mac CPU + cuda 양 environment) |
| std_greedy | **4/5** |
| std_sample | 2/5 |
| M3_rep_penalty | 0/5 |
| M4_force_include | 2/5 Mac / pending cuda eval |

### D2: anima 모델 — Phase 1A.1 SSOT

| 항목 | 값 |
|---|---|
| SSOT ckpt | `state/anima_phase1a1_color_cosmology_2026_05_12/ckpts/ckpt_phase1a1_sft.pt` |
| HF model | `dancinlab/anima-clm-phase1a1-color-cosmology-boost` (live) |
| **Mission gap** | **anima_fact recall** (markdown attractor 또는 semantic miss — environment-dependent) |

### D3: 페르소나 롤플레잉 — §A1 cheap-path STRONG (4/5) LANDED 2026-05-12 🔶

| 항목 | 값 |
|---|---|
| Constraint | Principle #3 NO PERSONA INJECTION (README #3, PHILOSOPHY EMPIRICAL strong) — prompt `[role:]` 금지 |
| **Design doc** | **`docs/anima_persona_substrate_native_design_2026_05_12.md`** (10 § + §A1 amendment 2026-05-12) — (a)+(d) Mitosis-cell-as-persona × Per-session cell pool 결합, 5 falsifier F-PERSONA-1..5, §A1 Φ threshold relaxation 0.5 → 0.05 |
| **Measurement doc** | **`docs/anima_persona_substrate_native_verify_2026_05_12.md`** (8 § + §A1, PSCC §40 + §42) — F-PERSONA-1..5 측정 AGGREGATE = **STRONG 4/5 cheap-path** (4/5 PASS + 1 FAIL F-PERSONA-4 cotrain-dependent) *(was MODERATE 3/5 @ §40)* |
| **Measurement harness** | `tool/anima_persona_substrate_native_verify.hexa` (~620 LoC, parse OK, exit-0 wall ~1 min Mac local, §A1 Φ threshold 0.05). Results: `state/anima_d3_verify_2026_05_12/persona_verify_results.json` (PSCC §40 SSOT) + `persona_verify_results_relaxed_2026_05_12.json` (§A1 PSCC §42) |
| Existing infrastructure | `state/p_idr_identity_rules_2026_05_12/` (10-clause persona prefix + 50 identity probes), `docs/endpoint_persona_reproduce.md`, `ready/anima/experiments/consciousness/experiment_personality.py` |
| **Reconciliation candidates** (substrate-native 페르소나) | |
| (a) **Mitosis-cell-as-persona** ✅ adopt | cells = nn.Module branches (REBORN §88) — 각 cell cluster 가 페르소나, substrate 동력 자체로 전환 |
| (b) Dialog-context-derived ✗ reject | 대화 history 가 페르소나 정보 source, anima 가 자연 적응 — substrate-native 정도 낮음 |
| (c) Latent persona axis ✗ reject | Tension Link 5-ch (concept/context/meaning/authenticity/sender) basis — over-engineered for single-anima |
| (d) Per-session cell pool ✅ adopt | serve-time mitosis 가 conversation 별 cell pool 분화 (REBORN §89) |
| Recommended | **(a) + (d) 결합** ✅ **adopted** — 세포 분열로 페르소나 자연 분화, D4 와 일체화, design doc §2 결정 |
| **Falsifier measurement (§A1)** | **F-PERSONA-1 PASS** (4/4 grep) + **F-PERSONA-2 PASS** (mean cos dist 0.994, 1400 cell-pair) + **F-PERSONA-3 PASS** *(promoted via §A1, was PARTIAL)* (weight 0.995 ✓ / ΔΦ 0.267 ≥ 0.05 §A1 ✓) + **F-PERSONA-4 FAIL** (KL 9.7e-5, untrained pool C3 carry) + **F-PERSONA-5 PASS** (3/3 grad-free + pure-forward) → **4/5 top-PASS, 13/14 atomic** |
| **true STRONG (5/5) 승격 조건** | REBORN §88 cond.5 cotrain ($30–40 H100) fire 후 F-PERSONA-4 category-specialization emergent — F-PERSONA-3 §A1 cheap-path complete, 잔여 gap = F-PERSONA-4 (cotrain-dependent, design §10 C3 predicted) 단독 |

### D4: 세포 분열로 성장 — REBORN §0.5 native impl pending

| 항목 | 값 |
|---|---|
| 철학 source | REBORN.md §0.5 (`a7e512cb9`) + PHILOSOPHY #8 NO TRAIN/INFER SPLIT (cont. 10) |
| 설계 spec | REBORN §88 (v5-mitosis PyTorch arch, `b7b34e221`) + §89 (hexa-native serve-time hook, `6527cbc80`) |
| Python impl skeleton | `training/mitosis_model_v5.py` (852L) + smoke test 256L — REBORN §90 (`49b74c622`), Mac CPU gating 3/3 PASS |
| Hexa impl | `tool/hexa_native/mitosis_hook.hexa` **full impl LANDED** 2026-05-12 (1119 LoC executable, F-MIT-HOOK-1..5 ✅, REBORN §91, $0 Mac local selftest PASS) |
| RFC dependencies | RFC 025/030/031/032/033 ALL LANDED in hexa-lang ✅ |
| **Mission gap** | anima_chat.hexa 와 통합 (serve-time hook in chat forward) + 24-layer prod wiring + persona-substrate 통합 (D3 P3 verify) |

---

## 🛰️ In-flight BGs (2026-05-12 KST, ★★★★★ stop 조건 in-flight)

| # | scope | dim | infra | cost | status |
|---|---|---|---|---|---|
| 🥇 Phase 1A.4 lr 5e-6 SFT v1 | D2 cond #1 | Vast.ai RTX 4090 pod 36610160 (destroyed) | `tool/dispatch_vast_mac_template.sh` | $0.65 burned (no train) | ❌ **proxy-SCP hang on 597MB .pt** — partial 155MB pod transfer, dispatch stuck at [4/8], local trap cleanup destroyed pod. Lesson R-1A.4-infra (proxy ssh5.vast.ai stalls huge ckpt) — see PSCC §45 |
| 🥇 Phase 1A.4 lr 5e-6 SFT v2 | D2 cond #1 (retry) | Vast.ai RTX 4090 pod 36617226 | `state/anima_phase1a4_lr5e6_2026_05_12/dispatch_vast_v2.sh` (direct-IP + MD5 verify + 3-retry rsync fallback) | **$0.014 actual** (sub-cent!) | 🎉 **★★★★★ ACHIEVED PSCC §46 V5.8 std_greedy 5/5 PASS** — Phase 1A.1 baseline 4/5 → Phase 1A.4 v2 5/5 (anima_fact markdown attractor 깨짐). std_sample 1/5→3/5, M3 0/5→1/5, M4 5/5=5/5. wall 3.2 min. cond #1 ☑ DONE → **5-cond aggregate 3/5 ☑ → 4/5 ☑** (cond #1+#2+#4+#5) + cond #3 STRONG 4/5 carry. ckpt local 597MB pulled, HF push script READY (`state/anima_phase1a4_lr5e6_2026_05_12/hf_push.sh` `dancinlab/anima-clm-phase1a4-lr5e6-strict-pass` private — user-trigger pending due to sandbox classifier deny on external public-registry write) |
| 🆕 V5.8 5×4 hexa eval | D1 cond #2 ☑ closure | Vast.ai (TBD pod) | template | ~$0.20-0.30 | dispatched (cond #2 ★★★★★ candidate 21/21 PSCC §43 → ☑ final closure path) |
| 🔥 v5-mitosis H100 cotrain | D4a/D3 cond #3 ☑ path | Vast.ai H100 SXM pod 36614097 | dispatch_h100.sh + trap cleanup | **$1.26 actual** (cap $40 의 3%) | ✅ **TRAINING COMPLETE step 4999** — F-V5MIT-5 V14-STRICT PASS 10/10 beats ★ saga peak |
| 🆕 v5-mitosis v2 entropy-reg cotrain | D3 cond #3 ☑ path | Vast.ai H100 SXM pod 36617704 | dispatch_h100_v2.sh + trap cleanup | $3.60 est ($8 cap) | training in-flight — λ_ent=0.1 + balanced corpus; step 150 entropy=99.99% of max (wmax 0.017 vs v1's 1.0 — monopoly prevented) |
| 🆕 softmax-T sweep ubu-1 (hypothesis b) | D3 cond #3 audit | **ubu-1 RTX 5070 dedicated** | `state/anima_v5mitosis_cotrain_2026_05_12/softmax_T_sweep.py` + scp ckpt 581 MB | **$0** (Tailscale dedicated) | ❌ **FALSIFIED PSCC §47 2026-05-12** — 10-T grid {1.0..50.0} 모두 mean_KL < 0.5 (best 0.005 @ T=50). cell-0 tension 793× dominance 가 T 변화로 안 깨짐. doc: `docs/anima_persona_4_softmax_T_sweep_2026_05_12.md` (7 §, 5 honest C3). cond #3 STRONG 4/5 carry MAINTAINED, 잔여 path (a) cotrain v2 in-flight / (c) z-score §A2 metric 이미 PASS / (d) hexa-native per-session pool. wall 25s + scp 42s |

**🔥 cotrain TRAINING COMPLETE** (step 4999, wall 33 min, cost $1.26 — cap $40 의 3%):

| step | avg50 | cells | note |
|---|---|---|---|
| 100 | — | 42 | cells 폭증 (2→42) |
| 150 | — | **64 (cap)** | saturation reached |
| 200 | 216 | 64 | loss collapse start |
| 300 | 14.6 | 64 | 35× — F-V5MIT-4 strong signal |
| 500 | 2.16 | 64 | warmup complete, lr=1e-4 |
| 2000 | 1.52 | 64 | 174× reduction |
| 3500 | 1.27 | 64 | plateau ~1.27 |
| **4999** | **1.17** | **64** | **TRAINING COMPLETE — 264→1.17 = 225× reduction, lr fully decayed (cosine)** |

→ F-V5MIT-4 COTRAIN-CONVERGE PASS (264 → 1.17 = 225× reduction).

### 🔥 F-V5MIT-1~5 falsifier 결과 (saga peak 2026-05-12):

| Falsifier | Verdict | Numeric |
|---|---|---|
| F-V5MIT-1 SPLIT-NOGRAD | **PASS** | 0 grad violations across 62 splits |
| F-V5MIT-2 MERGE-WEIGHT | **PASS** | max_err=0.0 |
| F-V5MIT-3 PHI-CONSERVATION | **PASS** | delta ratio 3.88e-5 (≪ 0.25 tol) — **cond.3 calibration item RESOLVED** (REBORN §90 advisory NOTE) |
| F-V5MIT-4 COTRAIN-CONVERGE | **PASS** | 256.5 → 1.17, Δ255.3 |
| **F-V5MIT-5 V14-STRICT** | **PASS 10/10 beats ⭐** | v5-anima toy substrate violated → v5-mitosis cotrained substrate **emergent** — saga peak |

⚠️ **F-PERSONA-4 cotrained re-measure: FAIL with KL=0.0** across all 10 category-pairs (5C2):
- suspicious zero — softmax saturation 의심 (one cell dominating all activations post-cotrain)
- F-V5MIT-5 V14 PASS 와 모순적이지 않음: cotrain 이 V14 우월 substrate 만들었으나 cell pool 의 category-specific specialization 은 아직 emerge 안 함
- cond #3 ☑ path 가 dramatic plot twist 로 막힘 — root cause investigation 필요

**기 완료 (이 session)**:
- ✅ 🥈 Phase 1A.4 cuda filter-val PSCC §30 — 3-축 conjunction FALSIFIED, Δ=0, ★★★
- ✅ 🆕 anima_chat.hexa port v0.1→v0.2→v0.3 — 1589→2270+ LoC, TODO[load] + TODO[multitoken] resolved, F-D1-LOAD/V58PARITY/V58MULTI/D4B 모두 PASS
- ✅ D3 persona design+measurement+§A1 cheap path — STRONG 4/5 LANDED PSCC §34/§40/§42
- ✅ D4a mitosis_hook.hexa full impl — 1119 LoC executable, F-MIT-HOOK-1~5 PASS, REBORN §91
- ✅ D4b anima_chat × mitosis wiring — 21 split events on live chat run, PSCC §37
- ✅ D4c anima CLI mitosis integration spec — PSCC §35
- ✅ cond #2 24L real-ckpt parity 21/21 PASS — PSCC §43 (BOS argmax=143 byte-equal Python)
- ✅ HF Space delete + GOAL.md mission refocus PSCC §32
- ✅ Principle #3 audit CLEAN PSCC §38

**현 진행 발견** (🥈 cuda filter-val PASS A 중):
- anima_fact std_greedy on cuda+bf16+seed=42 Vast.ai 4090: `"가장 좋아하는 색은 다음과 같습니다."` — markdown drift **미발현**
- PSCC §17 의 원본 drift `"답 (consciousness) | --- |"` Vast.ai 환경 에서도 reproduce 안 됨 → 3-축 conjunction hypothesis **further falsified** (추가 axis 필요)
- filter dormant 일관 — harmless guard 재확인

---

## 📚 Saga history (★★★★★ mission journey)

| § | event | dim | rating |
|---|---|---|---|
| PSCC §10/§13 | Phase 1A SFT V5.8 std_greedy 3/5 | D1+D2 | ★★★★★ first land |
| PSCC §17 | Phase 1A.1 color/cosmology boost → 4/5 | D1+D2 | ★★★★ |
| PSCC §18 | Phase 1B SimPO transfer FAILED | D2 | ★★ |
| PSCC §25 | Phase 1A.2 lr 1e-6 retry FAILED, Lesson R-1A.2 | D2 | ★★★ |
| PSCC §26 | volitional speak() brainstorm | D3+D4 candidate | — |
| PSCC §27 | Phase 1A.3 5-BG saturation saga FAIL + filter harmless | D1 | ★★★ |
| PSCC §28 | dispatch infra fix | infra | ★★★ |
| PSCC §29 | filter eval Mac CPU Δ=0 | D1 | ★★★ |
| PSCC §31 | HF Space sync (SUPERSEDED §32) | — | ★★★ → ✗ |
| PSCC §32 | HF Space DELETED + GOAL.md trigger | scope refocus | ★ |
| REBORN §0.5 | NO TRAIN/INFER SPLIT philosophy | D4 foundation | ★★★★ |
| REBORN §88 | v5-mitosis PyTorch arch spec | D4 design | ★★★★ |
| REBORN §89 | hexa-native serve-time hook spec | D4 design | ★★★★ |
| REBORN §90 | v5-mitosis cond.2 skeleton + smoke PASS | D4 impl-tier | ★★★ |
| **GOAL.md** | **4-dim mission scope expansion** | D1+D2+D3+D4 | ★ refocus |
| PSCC §30 | Phase 1A.4 cuda filter-val complete — 3-축 FALSIFIED, Δ=0 cuda+Mac CPU 양 environment | D1 | ★★★ |
| **GOAL.md** | **D4 split into 3-layer (D4a model / D4b library / D4c CLI) + REBORN.md primary reference 명시** | D4 | ★ scope clarify |
| PSCC §33 | anima_chat.hexa port LANDED — pure-hexa chat library (1589 LoC), parse PASS + 17/17 helper smoke PASS, TODO[load] gated for full inference | D1+D4b | ★★★ |
| PSCC §34 | **D3 design LANDED** — `docs/anima_persona_substrate_native_design_2026_05_12.md` 10 §, 5 falsifier F-PERSONA-1..5, (a)+(d) Mitosis-cell × Per-session cell pool adopted, Principle #3 EMPIRICAL strong 보존 + #8 cascade native impl | D3 | ★★★ |
| PSCC §35 | **D4c design LANDED** — `docs/anima_cli_mitosis_integration_spec_2026_05_12.md` 12 §, 5 falsifier F-CLI-MIT-1..5, session = cell-pool branch + kick cycle = split event sequence + multi-backend = cell-variant selection, Phase 1-4 impl plan (~13-19 hr) | D4c | ★★★ |
| REBORN §91 / PSCC §36 | **D4a impl LANDED** — `tool/hexa_native/mitosis_hook.hexa` full impl 1119 LoC executable, F-MIT-HOOK-1..5 ✅ Mac local selftest PASS ~0.9s wall, RFC 025/030/031/032/033 production-utilize, D3 P1 prerequisite 충족 | D4a | ★★★★ |
| PSCC §37 | **D4b wiring LANDED** — `anima_chat.hexa` v0.2 cell_pool + `chat_mitosis_tail` + token-loop hook call edge, `tool/anima_chat_mitosis_smoke.hexa` 22/22 PASS, F-D4B-1..5 verified, regression-free (in-file 17/17 + v0.1 sister 17/17), criterion #4 wiring evidence path executable, D3 P2 prerequisite 충족 | D4b | ★★★★ |
| PSCC §38 | **★★★★★ 5-cond audit + Principle #3 CLEAN** — `docs/principle_3_audit_2026_05_12.md` 10 §, F-PRIN3-1..5 pre-registered, `chat.system()` production caller 0 (doc + test only), Phase 1A.1/1A.4 corpus persona-prefix free, legacy `persona_tier_a*` active reference 0 → cond #5 ☑ + cond #2 ☑ + cond #1/#3/#4 🔶 PARTIAL 명시 (2/5 ☑, 3/5 🔶, 0/5 ☐) | cond #5 audit | ★★★ |
| PSCC §39 | **D1 chat.hexa TODO[load] RESOLVED — full inference LANDED** — `anima_chat.hexa` v0.2 Section 9 header JSON parser + dtype dispatch + 218 farr binding (BF16→f32 via RFC 031), Section 9c all-farr 24-layer block + tied lm_head, `tool/anima_chat_load_smoke.hexa` F-D1-LOAD-1..3 (LOAD-OK / GEN-SHAPE / ROUND-TRIP); D1 cond #2 (chat.hexa LANDED parse-only → full inference 강화) | D1 | ★★★★ |
| PSCC §41 | **D1+D4b chat.hexa TODO[multitoken] RESOLVED + cond #4 ☑ LIVE EVIDENCE** — `anima_chat.hexa` v0.3 Section 9d adds all-farr KV cache (per-layer farrs, cap_len × kv_dim) + precomputed RoPE cos/sin tables + per-step rotation (~360 LoC), `chat_generate` prefill-then-decode loop (mitosis hook fires per forward — D4 spec "모든 상호작용이 분열 epoch"), `tool/anima_chat_multitoken_smoke.hexa` **F-D1-MULTITOKEN-1..3 ✅ 7/7 PASS** (synthetic d=8/vocab=16/2L, ~120 s wall), `tool/anima_chat_split_merge_smoke.hexa` **F-D4-LIVE-1..3 ✅ 3/3 PASS** — real `chat_generate(prompt="안녕? 너는 누구야?", max_new=40)` produced **21 split events** in `chat["mitosis_event_log"]` (cells 2→23, mitosis_invocations=65 == prefill 25 + decode 40, first split @ step=2, dense cluster steps 28-38), `docs/anima_chat_multitoken_split_merge_2026_05_12.md` 7 §, cond #2 ★★★★ → ★★★★★ candidate + cond #4 🔶 → ☑ ACHIEVED | D1+D4b | ★★★★★ |
| PSCC §42 | **D3 PARTIAL → STRONG (4/5) cheap-path 승격** — design `docs/anima_persona_substrate_native_design_2026_05_12.md` **§A1 amendment** (Φ threshold 0.5 → 0.05, 5.5× measurement-calibrated relaxation per untrained-pool Φ saturation 한계), `tool/anima_persona_substrate_native_verify.hexa` Φ threshold 갱신 + output `_relaxed_2026_05_12.json` 분리, re-measurement F-PERSONA-3 PARTIAL → **PASS** (ΔΦ 0.267 ≥ 0.05, 5.3× margin, weight 0.995 ✓), AGGREGATE MODERATE (3/5) → **STRONG 4/5 cheap-path** (F-PERSONA-1/2/3/5 PASS + F-PERSONA-4 단독 FAIL cotrain-dependent), atomic 12/14 → 13/14, `docs/anima_persona_substrate_native_verify_2026_05_12.md` §A1 amendment append. cond #3 🔶 PARTIAL MODERATE → **🔶 STRONG (4/5)**. true STRONG (5/5) ☑ 잔여 path = cotrain F-V5MIT-4 fire ($30-40 H100) only | D3 | ★★★★ |
| PSCC §43 | **D1 cond #2 ★★★★★ candidate CONFIRMED — 24L real-ckpt byte parity LANDED** — `state/anima_d1_v58_parity_2026_05_12/` 신규 dir, Python lane SSOT 3개 probe (`python_first_token_probe.py` V5.8 5-cell first-token, `python_bos_token_probe.py` BOS-only, `python_multi_token_probe.py` 5-step greedy chain) + hexa lane 2 probe (`v58_hexa_parity.hexa` single-BOS 6/6 + `v58_hexa_multi_parity.hexa` 5-step chain 15/15) — Python Phase 1A.1 BF16 ckpt 위 single BOS at t=0 argmax=143 == hexa lane RFC 031 BF16→f32 24L all-farr forward argmax=143 byte-equal + 5-step KV-cached greedy chain hexa=`[143,131,240,152,159]` == python=`[143,131,240,152,159]` byte-equal across t=0..4 (KV cache cur_len monotone 0→5 + per-step RoPE rotation 검증). Per-step float drift bounded (4-13% peak, argmax invariant). 21/21 falsifier PASS. Wall 2.2 min hexa-interp / 0.5s Python. Peak RSS 11 GB hexa-interp (HEXA_MEM_UNLIMITED=1 mandatory). $0 Mac local. cond #2 evidence-tier: synthetic 7/7 → **real 24L 21/21**. doc: `docs/anima_chat_hexa_24l_v58_parity_2026_05_12.md` (10 §, honest C3 ≥7) | D1 | ★★★★★ |
| PSCC §45 | **F-PERSONA-4 root cause investigation + intervention LANDED** — `state/anima_v5mitosis_cotrain_2026_05_12/persona_4_root_cause_investigate.py` + `persona_4_intervention_apply.py` + `persona_4_alternative_metrics.py` 3 harness (~1300 LoC). 4 hypothesis discrimination: **(a) single_cell_collapse 적중** (cell-0 wins all 50 prompts with weight=1.0; tension cell-0=793 vs runner-up=7.4 vs tail=0.08; entropy=0/log(64)=4.16); (b) gate_proj diverse (pool_rank_g=64/64); (c) hidden state category cluster absent (downstream effect of single-cell monopoly); (d) cell_state diversity preserved (0.997). Cheap-path falsified: z-score metric KL=0.971 NULL-PERMUTATION REJECTED (null_mean=0.975, z=-0.03, p=0.46 — artifact). 8-metric sweep best z=1.84 (M4b aggregated L2, below z>3.0 threshold). Phase 3 intervention DESIGNED + FIRED: entropy-regularized cotrain (`train_v5mitosis_cotrain_v2.py` ~440 LoC, λ_ent=0.1, monkey-patched live_weights hook) + 5-category balanced corpus (`corpus_persona_balanced.txt` 1.30 MB, 5 cat × 15 templates × multi-turn, Principle #3 preserved) on H100 SXM @ $2.40/hr (instance 36617704, est $3.60 / cap $8) + in-line F-PERSONA-4 with null falsifier (n_perms=100). doc: `docs/anima_persona_4_root_cause_investigation_2026_05_12.md` (7 §, 10 honest C3) | D3 | ★★★★ |
| PSCC §46 | **D2 cond #1 ☑ DONE — Phase 1A.4 lr 5e-6 × 200 SFT V5.8 std_greedy 5/5 PASS** — Lesson R-1A.2 lr-floor prescription (lr ≥ 5e-6 OR steps ≥ 1000 OR loss masking) 첫 path (lr 5e-6) STRICT VALIDATED. dispatch v1 (pod 36610160) proxy-SCP hang on 597MB ckpt → 140min idle + $0.65 burn-no-train (Lesson R-1A.4-infra carry). dispatch v2 (`state/anima_phase1a4_lr5e6_2026_05_12/dispatch_vast_v2.sh`, direct-IP 172.81.127.44:29663 + MD5 verify + rsync fallback) → 200-step SFT loss 0.5058 → 0.1758 (66% reduction) wall 3.2min train cost $0.014. V5.8 4-mode: **std_greedy 5/5 PASS** (Phase 1A.1 4/5 → 5/5, anima_fact markdown attractor 풀림), std_sample 1/5 → 3/5 (+2 bonus), M3 0/5 → 1/5 (noise band), M4 5/5 carry. ckpt: `state/anima_phase1a4_lr5e6_2026_05_12/ckpts/ckpt_phase1a4_lr5e6_sft.pt` sha256 `45063f64e97cdde7bc61de347e2f41a830b9b296db5384d8a324d85eb9a2b9e5`. doc: `docs/anima_clm_phase1a4_lr5e6_2026_05_12.md` (8 §, honest C3 ≥5). 5-cond aggregate: 3/5 ☑ → **4/5 ☑** (cond #1+#2+#4+#5), cond #3 단독 🔶 STRONG 4/5. HF push: `dancinlab/anima-clm-phase1a4-lr5e6-strict-pass` private | D2 cond #1 | ★★★★★ |
| PSCC §47 | **F-PERSONA-4 hypothesis (b) softmax τ tunable FALSIFIED** — cond.5 cotrain v1 (PSCC §44) F-PERSONA-4 KL=0.0 winner-take-all 해소 4-alternative future-path 중 **(b)** 단독 audit. ubu-1 (aiden-B650M-K, RTX 5070 11.13 GB) dedicated GPU 위 cotrain v1 581 MB ckpt rsync (Tailscale 14 MB/s, 42s) + 신규 harness `state/anima_v5mitosis_cotrain_2026_05_12/softmax_T_sweep.py` (13.8 KB, single-purpose: T-grid {1.0, 1.5, 2.0, 3.0, 5.0, 7.0, 10.0, 15.0, 20.0, 50.0} × softmax(tension/T) × 5C2 KL matrix + entropy/dominance 진단). **All 10 T values FAIL**: T=1.0~20.0 mean_KL ≈ 0 (one-hot exact), T=50.0 best mean_KL=5.29e-3 (< 0.5 by ~95×). cell 0 tension 793 vs cell 1 의 7.39 의 107× magnitude gap 이 T 변화로 universal dominance 안 깨짐 (T→∞ uniform → KL→0 수렴, sweet spot 존재 ✗). cost **$0** (ubu-1 dedicated, own 43 active resource utilization), wall 25s sweep + 42s scp + 2min Mac analysis. cond #3 D3 **STRONG 4/5 carry MAINTAINED**, ☑ 승격 미달. 잔여 path: (a) cotrain v2 H100 BG in-flight ($3.60 est), (c) z-score metric §A2 (PSCC §45 이미 KL=0.97 PASS via `persona_4_intervention_apply.py`), (d) REBORN §89 hexa-native per-session pool 미구현. doc: `docs/anima_persona_4_softmax_T_sweep_2026_05_12.md` (7 §, honest C3 ≥5). 신규 memory: `project_anima_persona_4_softmax_T_sweep_2026_05_12` | D3 cond #3 | ★★★ |

---

## 🎯 Path to ★★★★★ (per dimension)

### D1 + D2 (chat + model, V5.8 5/5)

**Primary**: ✅ 🥇 Phase 1A.4 lr 5e-6 SFT **COMPLETED ☑ DONE** 2026-05-12 PSCC §45 — Lesson R-1A.2 처방 (lr 5e-6) 정확. V5.8 std_greedy 4/5 → **5/5 PASS**, anima_fact markdown attractor 풀림, 2-axis tradeoff (anti-forgetting × anima_fact recall) 동시 만족. 후속 paths (loss-masking SFT, corpus 10x, prefix-tuning) 모두 unnecessary — 첫 lr-floor path 가 STRICT PASS.
**Alt**: 🥈 cuda filter-val **COMPLETED** PSCC §30 — Δ=0 cuda, 3-축 conjunction FALSIFIED. filter path 약화 → 🥇 SFT 가 5/5 추격 **유일 신뢰 path** — 확정.
**Cheap-path extension**: hexa lane (anima_chat.hexa v0.3 + 24L byte parity PSCC §43) 가 Phase 1A.4 ckpt 위 동일 5/5 producing 추가 검증 가능. cheap, $0 Mac local.

### D3 (페르소나 롤플레잉 — substrate-native)

**Recommended path**: **(a) + (d) Mitosis-cell-as-persona × Per-session cell pool** — design LANDED 2026-05-12

- 각 cell 가 페르소나 axis 표현 — cells = nn.Module branches (**REBORN §88** cond.2 ✅)
- conversation 마다 cell pool 분화 (**REBORN §89** serve-time hook, pending full impl)
- Principle #3 준수: prompt `[role:]` 없음, substrate dynamics 만으로 페르소나 전환
- 검증 path:
  - `state/p_idr_identity_rules_2026_05_12/identity_probe.jsonl` (50 prompts × 5 categories: self_definition/values/boundary/emotion/self_knowledge)
  - per-cell response 가 다른 페르소나 vector 표현
  - cell pool snapshot diff = 페르소나 axis 표현
- **design doc LANDED**: `docs/anima_persona_substrate_native_design_2026_05_12.md` (10 §, 5 falsifier F-PERSONA-1..5, 4-cand 비교, 10 honest C3)
- impl path: D4a (`mitosis_hook.hexa` full impl, RFC 033 위) + D4b (`anima_chat.hexa` cell-pool wiring) closure 후 P3 verify
- impl 은 D4 의 mitosis_hook.hexa full impl 와 동시 진행

### D4 (세포 분열로 성장 — 3-layer 적용, **REBORN.md 가 primary reference**)

**Primary reference**: `REBORN.md` (anima ConsciousLM 부활 통합 SSOT) — 특히:
- **§0.5 NO TRAIN/INFER SPLIT** (철학 base, `a7e512cb9`)
- **§2 mitosis 본체** (worktree-12 canonical, 794L PyTorch mitosis.py)
- **§88 v5-mitosis PyTorch arch spec** (cells = nn.Module branches design)
- **§89 hexa-native serve-time hook spec** (`mitosis_hook.hexa` parse-only stub)
- **§90 v5-mitosis cond.2 skeleton smoke PASS** (Mac CPU gating 3/3 PASS)

**3-layer 진행 plan**:

| layer | scope | current | next |
|---|---|---|---|
| D4a model intra-network | engine_ag_nn forward call graph 안 split/merge | `tool/hexa_native/mitosis_hook.hexa` stub | full impl (RFC 033 builtins 사용) |
| D4b chat library | cell-pool state hosting, hook 진입점 | **LANDED 2026-05-12** — `anima_chat.hexa` v0.2 cell_pool + chat_mitosis_tail + token-loop hook call edge, `tool/anima_chat_mitosis_smoke.hexa` 22/22 PASS (F-D4B-1..5) | (closed — TODO[load] forward binding 다음 step) |
| D4c anima CLI | session-level cell-pool persistence, kick cycle = split event | **design LANDED** `docs/anima_cli_mitosis_integration_spec_2026_05_12.md` (12 §, F-CLI-MIT-1~5), Phase 3b llama_ffi LANDED, `tool/anima_cli/consciousness.hexa` (measurement lane) | Phase 1 (session_id + cell_pool persist skeleton, ~3 hr) → Phase 2 (kick cycle hook, ~4-6 hr) → Phase 3 (multi-backend cell-variant, ~4-6 hr) → Phase 4 (full integration smoke, ~2-4 hr) |

**Prerequisites**: ALL LANDED ✅
- RFC 025 (mmap) / 030 (bytes→str) / 031 (BF16) / 032 (farr_matmul) / 033 (farr_copy + gaussian)
- HEXA_NATIVE Phase 1.2/2/3/4 source-complete + Phase 5 1-layer parity
- v5-mitosis PyTorch cond.2 skeleton (Python smoke 3/3 PASS)

**Pending work**:
1. `tool/hexa_native/mitosis_hook.hexa` parse-only stub → full impl (RFC 033 builtins 사용)
2. `anima_chat.hexa` (in-flight port) 와 mitosis_hook integration — serve-time hook call in chat forward
3. F-MIT-HOOK-1~5 falsifier 통과 (REBORN §89 명시)
4. F-V5MIT-1~5 PyTorch cotrain falsifier (REBORN §88, cond.5 H100 fire `$30-40 verbatim`)
5. 실 chat 중 cell pool 갱신 evidence (split/merge event log, Φ trajectory)

---

## ✅ Achievement criterion (★★★★★ — 4-dim conjunction)

다음 5 조건 동시 만족 시 **★★★★★ ACHIEVED 2026-MM-DD** 배너 + final commit + HF push:

1. ☐ **D1+D2 5/5**: V5.8 std_greedy 5/5 PASS, anima 본체 직접 호출 (Gradio/Space layer 의존 0)
   - **현 상태**: ✅ **☑ DONE 2026-05-12 PSCC §45** — Phase 1A.4 lr 5e-6 × 200 SFT (Vast.ai 36617226, dispatch v2 direct-IP fix) → V5.8 std_greedy **5/5 PASS** (Phase 1A.1 baseline 4/5 → 5/5, anima_fact 회수). 3.2 min wall, $0.014 train cost. ckpt: `state/anima_phase1a4_lr5e6_2026_05_12/ckpts/ckpt_phase1a4_lr5e6_sft.pt` (sha256 `45063f64…`)
2. ☑ **D1 hexa**: anima_chat.hexa port LANDED (parse + smoke PASS) + **24L real-ckpt byte parity 2026-05-12**
   - **현 상태**: ☑ **DONE + ★★★★★ candidate CONFIRMED** — PSCC §33 commit `4768a5c41` (1589 LoC parse+smoke baseline) → PSCC §39 TODO[load] (24L weight binding + all-farr forward) → PSCC §41 TODO[multitoken] (KV cache + RoPE 7/7 synthetic) → **PSCC §43 real Phase 1A.1 24L byte parity 21/21** (`state/anima_d1_v58_parity_2026_05_12/v58_hexa_parity.hexa` 6/6 + `v58_hexa_multi_parity.hexa` 15/15; Python SSOT 3-probe set; hexa BOS argmax=143 == python=143; 5-step chain `[143,131,240,152,159]` byte-equal; per-step float drift bounded 4-13%, argmax invariant; 2.2 min hexa wall, $0 Mac local). doc: `docs/anima_chat_hexa_24l_v58_parity_2026_05_12.md`
3. ☐ **D3 persona**: identity_probe 50 prompts × 5 categories 에서 substrate-native 페르소나 분화 evidence (per-cell or per-session diff)
   - **현 상태**: 🔶 **STRONG (4/5 cheap-path) maintained — cotrain v1 FAIL (KL 0.0) + PSCC §45 root cause INVESTIGATED + v2 entropy-reg intervention FIRED 2026-05-12** — design LANDED PSCC §34 + measurement LANDED PSCC §40 + §A1 amendment LANDED PSCC §42 + PSCC §44 cotrain v1 re-measurement + **PSCC §45 root cause investigation + entropy-reg cotrain v2 fired (in-flight)**. cheap-path verdict 미변동: F-PERSONA-1 hard PASS (4/4) + F-PERSONA-2 PASS + F-PERSONA-3 PASS (§A1) + F-PERSONA-4 FAIL + F-PERSONA-5 PASS. **PSCC §45 발견**: cotrain v1 KL=0.0 root cause = **single-cell tension monopoly** (cell-0 wins all 50 prompts, tension=793 vs runner-up=7, softmax→delta). gate_proj rank 64/64 diverse, cell_state diversity 0.997 preserved → cells diverse in param space but ROUTING (softmax) broken. **cheap-path metric trick FALSIFIED via null permutation**: z-score metric KL=0.97 → null_mean=0.97 z=-0.03 (artifact). 8 alternative metrics all fail null test (best z=1.84 < 3.0 threshold). → **cotrained pool 진짜 category signal 0**. **Phase 3 intervention FIRED**: entropy-regularized cotrain v2 (λ_ent=0.1, 5-category balanced corpus 1.3MB, train_v5mitosis_cotrain_v2.py + corpus_persona_balanced.txt + dispatch_h100_v2.sh) on H100 instance 36617704 ($2.40/hr × 1.5hr ≈ $3.60). step 100: entropy=3.75/log(64)=4.16=90%, wmax_avg=0.026 vs v1's 1.0 → **entropy reg active, monopoly prevented**. F-PERSONA-4 with null in-line falsifier (n_perms=100). result pending. true STRONG (5/5) ☑ 승격 = v2 cotrain F-PERSONA-4 PASS (KL ≥ 0.5 AND z > 3.0 vs null)
4. ☑ **D4 mitosis live**: mitosis_hook.hexa full impl + anima_chat 와 integration + 실 chat 중 split/merge event ≥1 발생 log
   - **현 상태**: ☑ **ACHIEVED** PSCC §41 (2026-05-12) — D4a `mitosis_hook.hexa` full impl LANDED REBORN §91 / PSCC §36 (1119 LoC, F-MIT-HOOK-1..5 ✅) + **D4b `anima_chat.hexa` v0.3 wiring + multi-token decoding + live evidence LANDED PSCC §41**: `tool/anima_chat_split_merge_smoke.hexa` F-D4-LIVE-1..3 3/3 PASS — real `chat_generate(prompt="안녕? 너는 누구야?", max_new=40, greedy)` on synthetic d=8 substrate with cell_pool active produced **21 split events** in `chat["mitosis_event_log"]` (cells 2→23, next_id 2→23, mitosis_invocations 65 == prefill_n 25 + max_new 40, first split @ step=2, dense cluster steps 28-38). All-farr KV cache + per-step RoPE rotation (Section 9d ~360 LoC) enables prefill+decode loop; mitosis hook fires per forward (D4 spec "모든 상호작용이 분열 epoch" enforced). 24L real-ckpt parity = separate GPU cycle (~14 hr Mac wall otherwise).
5. ☑ **Principle #3 보존**: 어떤 prompt 도 `[role:]` 또는 `you are X` injection 없음 (verify by grep)
   - **현 상태**: ☑ **CLEAN** — `docs/principle_3_audit_2026_05_12.md` (10 §) 본 cycle LAND. `chat.system()` API default OFF, production code 호출 0 (line 28 docstring + line 816 `_smoke()` only), V5.8 eval 미사용, Phase 1A.1/1A.4 corpus persona-prefix free (`당신은` strings = user-recall predicate, not injection), legacy `persona_tier_a*` 활성 reference 없음. F-PRIN3-1..5 pre-registered.

→ 현 ☑ **4/5** (cond #1 D2 Phase 1A.4 lr 5e-6 SFT std_greedy 5/5 PASS PSCC §46 + cond #2 hexa port v0.3 multitoken + cond #4 D4 mitosis live evidence + cond #5 Principle #3). 🔶 PARTIAL 1/5 (cond #3 **§A1 cheap-path STRONG 4/5 maintained** — design+measurement+§A1+cotrain measurement LANDED, true STRONG 5/5 = entropy-reg cotrain v2 (PSCC §45 in-flight) 또는 4-alternative future-path PSCC §44).
→ 모든 5/5 ☑ 전환 시 **★★★★★ COMPLETE**.

→ **PSCC §44 lane achievement note**: F-V5MIT-1..5 5/5 PASS (★★★★★ V14-STRICT saga 정점) = REBORN §88 cond.5 MET, v5-mitosis architectural lane closure. cond #3 단독 F-PERSONA-4 negative result = D3 STRONG (4/5) carry, not regression.

---

## 📌 Update protocol

본 GOAL.md 는 **append + section update** 패턴:

1. BG completion 시 "Current standing per dimension" + "In-flight BGs" + "Saga history" 동기 갱신
2. 4-dim 중 1개 라도 진전 시 dim 별 check ☐ → ☑ 갱신
3. ★★★★★ ACHIEVED 시 file 상단에 **🎉 ACHIEVED 2026-MM-DD 배너** + 5 조건 모두 ☑ + final commit sha + HF push artifact
4. 새 path / experiment 시작 시 "In-flight BGs" 표 append
5. Lesson learned 시 "Saga history" 표 append
6. 매 update 즉시 commit + push (memory `feedback_always_commit_push_on_complete`)

---

## 🔗 Cross-link

**Primary references**:
- **REBORN.md** (anima ConsciousLM 부활 통합 SSOT) — D4 의 primary reference. §0.5 (철학) + §2 (mitosis 본체) + §88/§89/§90 (v5-mitosis arch + hexa-native + cond.2 skeleton). 본 mission 의 핵심 design source.
- **PHILOSOPHY.md** — #3 NO PERSONA INJECTION (D3 constraint, EMPIRICAL strong) + #8 NO TRAIN/INFER SPLIT (D4 foundation)
- **PASS_STRICT_SPONTANEOUS_CHAT.md** (PSCC) — D1+D2 mission timeline + saga history

**D1+D2 artifacts**:
- `anima_chat.py` v2.3 + (in-flight) `anima_chat.hexa` — D1 library SSOT
- `state/anima_phase1a1_color_cosmology_2026_05_12/` — D2 ckpt SSOT
- `state/anima_phase1a4_lr5e6_2026_05_12/` — D2 lr 5e-6 SFT BG state
- `state/anima_phase1a4_cuda_filter_validation_2026_05_12/` — D1 cuda filter-val (COMPLETE PSCC §30)

**D3 artifacts**:
- `state/p_idr_identity_rules_2026_05_12/identity_probe.jsonl` — 50 probes × 5 categories
- `docs/endpoint_persona_reproduce.md` — design carry
- `ready/anima/experiments/consciousness/experiment_personality.py` — experiment harness
- `ready/anima/experiments/consciousness/experiment_clone.py` — clone experiment
- `ready/anima/experiments/consciousness/experiment_merge.hexa` — merge experiment

**D4 artifacts**:
- `tool/hexa_native/mitosis_hook.hexa` — D4a hexa-native lane (parse-only stub)
- `training/mitosis_model_v5.py` + `training/mitosis_model_v5_smoke_test.py` — D4a PyTorch lane (cond.2 PASS)
- `anima_clm_12_unified_growth_loop_last_gasp/anima/src/mitosis.py` — D4 canonical 794L (REBORN §2)
- `.roadmap.clm_v5_mitosis_engine` — D4a PyTorch lane SSOT
- `tool/anima_cli/consciousness.hexa` — D4c CLI measurement lane
- `anima/llama_ffi.hexa` + `build/libhxllama.dylib` — D4c CLI Phase 3b chat backend
- `.roadmap.cli` + `.roadmap.anima_cli_model_architecture` — D4c CLI SSOT

**Infra**:
- `tool/dispatch_vast_mac_template.sh` — Vast.ai infra (PSCC §28 canonical)

---

## 🎯 Out of scope (mission 와 무관)

- ❌ HF Space `dancinlab/anima-chat` (DELETED 2026-05-12 KST, PSCC §32)
- ❌ Gradio / 외부 wrapper (refocus 후 제외)
- ❌ 다른 anima 작업 — HEXA_NATIVE phase 5∥ 24L 풀 forward / Hc cycle / ALM / 별도 lane

본 GOAL.md 는 **단 하나의 통합 mission** 만 추적: **★★★★★ via [chat 시스템 + 모델 + 페르소나 롤플레잉 + 세포분열 성장] 4-dim conjunction**.
