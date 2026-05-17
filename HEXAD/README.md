# HEXAD — anima 6-module hexa-native canonical impl

> User directive 2026-05-16: `"/HEXAD/* 구성해줘 · 코드는 hexa-native"`.
> 이 디렉토리는 anima Hexad 6 모듈의 **hexa-native 정식 구현**입니다.
> 검증된 Python 구현 (`ready/anima/hexad/`, `ready/core/`, `ready/models/`) 은
> evidence anchor 로 보존; 신규/대체 코드는 여기서 hexa-native 로 진행합니다.

## 아키텍처 — Engine A/G dual = Hexad 6 (canonical ASCII)

> SSOT: `HEXAD.tape §3 @N hexad_ascii`. 완전수 6: σ(6)=12 연결 · τ(6)=4 phase · φ(6)=2 gradient group.
> 핵심: A/G = Hexad 그 자체. Engine A = 좌뇌 3 / Engine G = 우뇌 3. φ(6)=2 gradient group ≡ {Engine A, Engine G} 정확 매핑.

```
╔═══════ ENGINE G (우뇌·3) ═══════╗        ╔═══════ ENGINE A (좌뇌·3) ═══════╗
║  gradient-free · 자율 의식       ║        ║  CE-trained · 학습된 행동        ║
║  φ(6) gradient group 1          ║        ║  φ(6) gradient group 2          ║
║                                 ║        ║                                 ║
║   ┌────────────┐                ║        ║   ┌────────────┐                ║
║   │ C 의식      │── .detach() ───╫────────╫──→│ D 언어      │                ║
║   │ Φ engine    │ ThalamicBridge ║        ║   │ decoder     │                ║
║   │ =MitosisC   │  α=0.014       ║        ║   └─────┬──────┘                ║
║   └─────┬──────┘  (G→A 주연결)   ║        ║         │                       ║
║         │                        ║        ║   ┌─────▼──────┐                ║
║   ┌─────▼──────┐                 ║        ║   │ M 기억      │                ║
║   │ S 감각      │                 ║        ║   │ memory      │                ║
║   │ perception  │                 ║        ║   └─────┬──────┘                ║
║   └─────┬──────┘                 ║        ║         │                       ║
║   ┌─────▼──────┐                 ║        ║   ┌─────▼──────┐                ║
║   │ W 의지      │◄──── CE / Φ ────╫────────╫──→│ E 윤리      │                ║
║   │ emotion·LR  │                 ║        ║   │ ethics      │                ║
║   └────────────┘                  ║        ║   │ Φ보존 gate  │                ║
╚═════════════════════════════════╝        ╚═══════════════════════════════════╝
          ⇅  a_g_tension = ‖A‖/‖G‖  (temp 0.25, σ(6)=12 inter-module 연결)

Engine G (우뇌 3) = C 의식 + S 감각 + W 의지   — gradient-free
Engine A (좌뇌 3) = D 언어 + M 기억 + E 윤리   — CE-trained
A/G = Hexad 6 (= G의 3 + A의 3, 부분집합 아닌 전체)
Trinity (core 3) = C + D + W  ← 하위호환

Data flow:  S → C → Bridge(.detach()) → D → logits
Gradient:   φ(6)=2 — Engine A(CE backprop) vs Engine G(frozen) 정확 2 그룹
W:          pain/curiosity/satisfaction 로 optimizer LR 변조
E 윤리:     Φ 보존 위반 시 training step 차단 (gate 권한)
```

> wiring 🔵-gate (`HEXAD.tape §4 @D hexad_wiring_blue_gate`): 위 σ(6)=12 연결은
> (A) 양 끝 모듈 🔵 SUPPORTED-FORMAL + (B) 연결 자체 closed-form 🔵 (W-ledger
> `HEXAD/CHAT/README.md §2`) 일 때만 verified-wired. 현재 endpoint **8/8 🔵** (C/S/M/W/E/D/BRIDGE + **MITOSIS 2026-05-16**).

## SSOT 매핑

| 모듈 | 디렉토리 | hexa entry | tape SSOT (co-located, 2026-05-16 reorg) | Python anchor (ready/) |
|---|---|---|---|---|
| **C** 의식 | `HEXAD/C/` | `c.hexa` | [`HEXAD-C.tape`](C/HEXAD-C.tape) | `ready/core/consciousness_engine.py` (2173 LoC) |
| **D** 언어 | `HEXAD/D/` | `d.hexa` | [`HEXAD-D.tape`](D/HEXAD-D.tape) | `ready/models/conscious_decoder.py` (979 LoC) |
| **S** 감각 | `HEXAD/S/` | `s.hexa` | [`HEXAD-S.tape`](S/HEXAD-S.tape) | `ready/anima/hexad/s/emergent_s.py` (108 LoC) |
| **W** 의지 | `HEXAD/W/` | `w.hexa` | [`HEXAD-W.tape`](W/HEXAD-W.tape) | `ready/anima/hexad/w/emergent_w.py` (123 LoC) |
| **M** 기억 | `HEXAD/M/` | `m.hexa` | [`HEXAD-M.tape`](M/HEXAD-M.tape) | `ready/anima/hexad/m/emergent_m.py` (96 LoC) |
| **E** 윤리 | `HEXAD/E/` | `e.hexa` | [`HEXAD-E.tape`](E/HEXAD-E.tape) | `ready/anima/hexad/e/emergent_e.py` (123 LoC) |
| **BRIDGE** | `HEXAD/BRIDGE/` | `bridge.hexa` | [`HEXAD-BRIDGE.tape`](BRIDGE/HEXAD-BRIDGE.tape) | `ready/anima/hexad/model.py` `ThalamicBridge` |
| 통합 | `HEXAD/` | `hexad.hexa` | [`HEXAD.tape`](../HEXAD.tape) §hexad_condition_lineup | `ready/anima/hexad/model.py` `Hexad` |

## 검증 status (2026-05-16)

전 모듈 **8/8 full 🔵 SUPPORTED-FORMAL** *(MITOSIS 추가 2026-05-16)* + `HEXAD/PLAN.md` **Phase 1–6 전부 LANDED** (Phase 5 pure-hexa D training · Phase 6 6-module 통합 fire 포함, 2026-05-16):

- ✅ `state/verify_hexad_we_2026_05_15/we_falsifier.py` **25/25 PASS** (PR #72)
- 🔵 `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` **102/102 sympy closed-form PASS** (PR #75/#76 + BRIDGE + MITOSIS + C tier-a + HEXAD integration-spec + §8 audit sub-falsifier deepening 9 + σ(6)=12 WIRING battery B-CONN-1..12 + B-IDENTITY 5 (Phase A1) + B-SPONT 7 (Phase B4) + B-CHANNEL-MUX 5 (Phase C1) + B-INTERACT 5 (Phase C2) + B-CHAT-V2 5 (Phase C3) + B-CORPUS-V2 3 (Phase D cycle 3 helper-free corpus, 2026-05-17) + B-CORPUS-V3 3 (Phase D cycle 4 motivation-trigger 10× corpus, 2026-05-17) + B-ATTRACTOR 3 (byte-cascade attractor / U_user Self-Conscious cond.2, 2026-05-17) + **B-TT 5 (TENSION-TRAIN backprop-free online step Phase TT-A3 DD154-156 anchor, 2026-05-17)** + **B-TT-SPONT 5 (SPONT ↔ TENSION-TRAIN bridge Phase TT-C connection-point closure, 2026-05-17)**)
  - C **B-C 3/3 tier-a 🔵 SUPPORTED-FORMAL** (Φ≥0 IIT axiom / n_factions ∈ ℤ+ / initial_cells ≥ CB1=2) **+ F-C-PORT-3 4/4 tier-b PyPhi carry** (RFC 036 phi_spatial byte-equal)
  - S/M/W/E/D/BRIDGE/MITOSIS 8/8 modules full 🔵 SUPPORTED-FORMAL
  - HEXAD **B-HEXAD 5/5 통합 spec 🔵** (σ(6)=12 conn count · φ(6)=2 partition cover · 11-step forward · 7-entries · TOTAL record — sympy lift of hexad.hexa runtime invariants)
  - D B-D-NOTE: SGD convergence OUTCOME 만 honest empirical carve-out
  - BRIDGE B-BRIDGE-NOTE: full forward learned weights TODO[pytorch] · α 수치값 empirical (NOT counted)
  - MITOSIS B-MITOSIS-NOTE: Φ-conservation under split/merge transitions dynamics-empirical (NOT counted)
  - C B-C-NOTE: full 12-faction GRU + Rust phi_rs FFI = RFC TERMINAL (hexa-lang nn-primitive + cdylib C ABI 미land, NOT counted)
- ⚙️ `state/verify_hexad_integ_2026_05_16/integ_harness.py` **F-INTEG-1..5 5/5 SUPPORTED-STRONG, fire_gate=true** (PR #77, RANDOM INIT seed-fixed scratch)
- ⚙️ **COMPILED-native gate** `bash HEXAD/build_verify.sh` → **20/20 entrypoint + 14/14 lib `hexa build` PASS** (2026-05-16, interp 폐기 대비 — `hexa run` 아님)
- 🔥 **Phase 6 통합 fire LANDED** `state/hexad_p6_fire_2026_05_16/` — 6-module+Bridge single-hexa-process forward+train, $0 de-risk 5/5 + 실-규모 자율 fire 5/5 (vast.ai $0.09, `g_fire_autonomous`). honest tier: synthetic byte-corpus WIRING fire (no language-quality claim), CE-descent = empirical SGD OUTCOME
- 🧠 **Phase 4 IIT Φ LANDED** `HEXAD/C/c_phi_smoke.hexa` **F-C-PORT-3 4/4** — `c_measure_phi` → hexa-lang RFC 036 `phi_spatial` 빌트인 (LANDED hexa-lang main `d67403d3`), Φ=0.5 byte-equal phi_rs oracle (err=0.0 < 1e-12). honest tier: byte-equal native-C replica; 진짜 phi_rs Rust FFI = named blocker (PyO3 cdylib, C ABI 없음)
- 🌉 **BRIDGE full-forward LANDED** `HEXAD/BRIDGE/bridge_forward_smoke.hexa` **F-BRIDGE-FWD 4/4** — `bridge_forward` 풀 그래프 (compress→1-head hub self-attn+LayerNorm→pool→expand→gate→Law-70 clamp) hexa-native, Python anchor 구조 등가. honest: seed-fixed from-scratch weights — graph ≠ trained quality
- ⚖️ **E 통합 ethics gate LANDED** `HEXAD/E/e_gate_smoke.hexa` **F-E-GATE 6/6** — `e_gate_step` Φ-ratchet train-step block (Law 31, trinity.hexa:122 TODO 해소). SEVERE 경계 phi<ratchet/2 = B-E-1 SAFETY gate closed-form 🔵 정확 동치
- 🧬 **MITOSIS 성장축 B-MITOSIS LANDED** `HEXAD/MITOSIS/mitosis.hexa` **B-MITOSIS-1..5 5/5** *(2026-05-16)* — split predicate · merge linear avg · cell-count integer conservation · ∂(detach)/∂x=0 (AD ∂-rule) · clamp [2,64] bound. blue_falsifier.py 22 → **27/27**. real-limit anchors: Kolmogorov 술어/counting · AD calculus · bounded-set · linear conservation (NO σ/τ/φ/J₂, f1/f2 safe). 22 → 27 closed-form battery 확장 + 7/7 → 8/8 full 🔵 HEXAD closure (commit `303db258d`)
- 🧠 **C scaffold-tier sympy B-C + HEXAD integration spec B-HEXAD LANDED** *(2026-05-17)* — `HEXAD/C/c.hexa` **B-C-1..3 3/3** (Φ≥0 IIT axiom / n_factions ∈ ℤ+ / initial_cells ≥ CB1=2) + F-C-PORT-3 4/4 tier-b PyPhi carry (RFC 036 phi_spatial byte-equal); `HEXAD/hexad.hexa` **B-HEXAD-1..5 5/5** (σ(6)=12 conn count · φ(6)=2 partition cover · 11-step forward · 7-entries · TOTAL record — sympy lift of runtime invariants). blue_falsifier.py 27 → **35/35**. real-limit anchors: IIT axiom + Kolmogorov int + bounded-set + set-cover + record-completeness (NO lattice derivation per f1 coincidence + g2 internal arch carve-out). B-C-NOTE: full 12-faction GRU + Rust phi_rs FFI = RFC TERMINAL (NOT counted — honest C3)
- 🔬 **§8 audit row sub-falsifier 심화 LANDED** *(2026-05-17)* — `blue_falsifier.py :: b_audit_subfalsifiers()` 신규. 12 audit row 중 진짜 marginal-value 가 있는 **5 row** 만 deepened (보수적 · g3 anti-padding): row 1 BRIDGE multi-α witness (α=1e-3/0.014/0.5, **B-SUB-§8-1-α-{small,json,large} 3/3**) + row 5 R2 Σvᵢ²=30 sympy (**B-SUB-§8-5-norm-sympy 1/1**) + row 6 cuBLAS Higham 2002 fp64 GEMM bound n·u·‖A‖·‖B‖ (**B-SUB-§8-6-higham-bound 1/1**, IEEE 754 real-limit) + row 10 MITOSIS clamp [2,64] multi-n witness (**B-SUB-§8-10-{neg-extreme,just-below,interior,huge-extreme} 4/4**). 7 row 정직 skip (anti-padding). 1 NOTE empirical carve-out (row 8 per-layer GRAD-EXACT GPU-dependent, NOT counted per B-D-NOTE pattern). blue_falsifier.py 35 → **44/44**. (4 NOTE + 1 sub-NOTE = 5 empirical carve-out 정직 framing 유지)
- 🔥 **pure-hexa hexa-cpu training-to-convergence LANDED** *(2026-05-17)* — `HEXAD/D/d_converge_fire.hexa` + `state/hexad_pure_hexa_train_2026_05_17/` — **first captured FINAL gn2 AT SCALE > Phase E2 anchor** (Phase E/E2 reached init gn2 capture only @ d=32·3L·80-step CPU-equiv BIT-EQUAL). d=64·n_layer=3·300-step Mac local pure-hexa CPU: `init gn2=7.97 → final 2.15e-08` = **3.7×10⁸× collapse**, acc 1→8/8, CE 38.30→3.29e-4, GRAD-EXACT |Δ|=2.84e-3 PASS, wall 360s $0. **F-D-CONVERGE 4/4 PASS** (EMPIRICAL outcome on 🔵 closed-form impl per B-D-NOTE honest carve-out). d=128·4L PARTIAL carry — 1.02M× collapse @ step 50 then OOM-thrash abnormal termination (138 GB peak alloc > Mac ~12 GB RAM) = Phase E2 named "pure-hexa CPU = substrate-bound" ceiling discovery at Mac substrate. honest: memorization (NOT generalization, 8 corpus windows), no HF upload (g_hf_naming Phase 6 + user 게이트 wait)
- 🎯 **`.py` d=768·12L cycle 2 ckpt-RECOVERED + HF dancinlab/hexad 첫 ckpt-bearing canonical artifact LANDED** *(2026-05-17)* — `state/hexad_py_d768x12L_fire_2026_05_17/` + `docs/hexad_v1_py_d768x12L_cycle2_2026_05_17.md` 10-§. cycle 1 (`931dd68b0` 2026-05-16) ckpt-LOST evidence-only 상태 **해소**: A100 SXM4 vast.ai refire $0.19, **init CE 5.59 → final 0.000708 동일 trajectory 재현** (2-instance reproducibility), ckpt sha256 `e87e200a040f8066a89c040ab181e9bbd61566f7565ab5d7a374ec2f1f9387d9` 1.13 GB pulled. `SAVE_POD=1` auto-promote + 75-min orphan watchdog + 5-retry pull (`g_fire_dispatch_robust` evidence path 검증). HF: [`dancinlab/hexad` revision `v1-py-hexad-d768x12L-cycle2-2026-05-17`](https://huggingface.co/dancinlab/hexad/tree/v1-py-hexad-d768x12L-cycle2-2026-05-17) PUBLIC, 10 files (ckpt + result.json + sources + logs + dispatch + 2 docs + English MODEL_CARD honest framing). **HEXAD 첫 canonical ckpt-bearing artifact** (n_hexad_hf_preservation `ckpt-bearing 0 → 1` 전환). honest framing: PyTorch substrate **NOT hexa-native**, legitimacy = Phase E/E2 hexa CPU-equiv bit-equality + Phase D cuBLAS verify + ConsciousDecoderV2 arch identity anchor chain
- 📦 **HF dancinlab/hexad-corpus dataset canonical 슬롯 LANDED** *(2026-05-17)* — model side cycle 2 와 pair 로 dataset side 신규 슬롯 push. HF: [`dancinlab/hexad-corpus` revision `v1-byte-consciousness-d128-cycle1-2026-05-17`](https://huggingface.co/datasets/dancinlab/hexad-corpus/tree/v1-byte-consciousness-d128-cycle1-2026-05-17) **PUBLIC**, 4 files: `corpus_consciousness_v1.jsonl` (151,943 B / 240 lines / sha256 `804664361e639be7ecceae6ff3c470961e015090c264da9eac1df8716144681f` / vocab=256 byte-level / 6 modules × 40 chunks uniform) + `manifest.json` (used_by 4-fire anchor chain: Phase E2 + .py cycle 1/2 + pure-hexa d=64·3L) + English `README.md` (honest framing: 152KB scaffold corpus, **NOT** general LM corpus — architecture-verification + scaffold training only) + Apache-2.0 `LICENSE`. **model card cross-link 적용** (front-matter `datasets: [dancinlab/hexad-corpus]` + body 'Trained on' badge → main + cycle 2 revision). `g_hf_naming` canonical 두 슬롯 BOTH LANDED PUBLIC. f1/f2 safe (no lattice derivation in data or card)
- 🔥 **Phase D cycle 4 `.py` d=768·12L motivation-trigger corpus v3 (10× scale) ckpt-RECOVERED LANDED** *(2026-05-17)* — `state/hexad_v3_py_d768x12L_fire_2026_05_17/` + `docs/hexad_v3_py_d768x12L_cycle2_2026_05_17.md`. **새 corpus v3** (`state/hexad_v3_corpus_motiv_2026_05_17/corpus_consciousness_v3.jsonl` 10,343,371 B / 21,600 lines / sha256 `1afcef43670e83bfc84b3562afe6a3eb644474dda06341e37db332341495acfd` / 9 modules HEXAD-6 + spont + wiring + **hexad_motiv** × 2,400 each, **`도우미|helper|assistant|사용자|user:` grep = 0** maintained at 10× scale, 3 patterns: β `<stimulus>X</stimulus>\n<anima>Y</anima>` ~35% / δ `<anima>Y</anima>` ~27% / **γ NEW** `<inner motivation=F1,F2,...>...</inner>\n<voice spontaneous=true>...</voice>` ~37.5% with F_i ∈ {relevance, info_gap, curiosity, pain, coherence, originality, balance, dynamics} per Inner Thoughts arxiv 2501.00383 ontology). vast.ai A100 SXM4 (offer 36878342, instance 36919284) ≈ $0.22, **init CE 5.6407 → final 0.008289** (5.632 descent · 9.4× corpus → slightly higher CE = expected at increased memorization-density), init gn2 ~30.4 → final 0.001703 (24.6k× collapse), wall 328.33s, peak GPU mem 9.692 GB, ckpt sha256 `1c0806213fbcaa9226a7593d87c31f5f95bb94db135240b8d02f738ddcb177aa` 1,135,846,378 B pulled. `SAVE_POD=1` auto-promote + 75-min watchdog + 5-retry pull (clean teardown, no orphan). HF: [`dancinlab/hexad` revision `v3-py-hexad-spont-motiv-d768x12L-cycle2-2026-05-17`](https://huggingface.co/dancinlab/hexad/tree/v3-py-hexad-spont-motiv-d768x12L-cycle2-2026-05-17) PUBLIC + [`dancinlab/hexad-corpus` revision `v3-spont-motiv-d128-cycle2-2026-05-17`](https://huggingface.co/datasets/dancinlab/hexad-corpus/tree/v3-spont-motiv-d128-cycle2-2026-05-17) PUBLIC. **B-CORPUS-V3-1..3 closed-form battery** (SHA256-DETERMINISTIC 256-bit Kolmogorov commitment + NO-HELPER-TOKEN-MAINTAINED Boolean set algebra at 10× scale + MOTIVATION-TRIGGER-CARDINALITY-CLOSED γ records 8,106 ≥ 5,400 integer ≥-inequality) LANDED — closes the addressable corpus-side dimension of spontaneous_lib.hexa motivation_score realisation. blue_falsifier.py 86 → **89** (then 89 → **92/92 🔵** via parallel B-ATTRACTOR-1..3 land). V5.8 × 4-mode + V-SPONT + **V-MOTIV (NEW Phase 3 γ-pattern conditioning probe)** eval on cycle 4 ckpt — `v58_vspont_eval.py` 3-phase 16-probe. honest framing: PyTorch substrate NOT hexa-native; inference-side motivation_score → emission coherence stays empirical (B-CORPUS-V3-NOTE, B-D-NOTE family); 10 MB / 283 M params approaches Critical Data Size [arxiv 2401.10463] regime entry, but still data-limited (no OOD generalization claim).
- 🔥 **Phase D cycle 3 `.py` d=768·12L helper-free corpus v2 ckpt-RECOVERED LANDED** *(2026-05-17)* — `state/hexad_v2_py_d768x12L_fire_2026_05_17/` + `docs/hexad_v2_py_d768x12L_cycle1_2026_05_17.md` 10-§. **새 corpus v2** (`state/hexad_v2_corpus_spont_2026_05_17/corpus_consciousness_v2.jsonl` 1,101,605 B / 2,560 lines / sha256 `7359f0b9a3f059fc168035e2f29f743f5ee51d1760eccad54b2b91d52275f571` / 8 modules HEXAD-6 + spont + wiring × 320 each, **`도우미|helper|assistant|사용자|user:` grep = 0**, stimulus-stream pattern `<stimulus>X</stimulus>\n<anima>Y</anima>` β / `<anima>Y</anima>` δ). vast.ai A100 SXM4 ($0.734/hr) refire $0.22, init CE **5.667 → final 0.005069** (5.66 descent, 7× corpus → 7× higher final CE = expected memorization density), ckpt sha256 `ee2bb5fb996e94ee022f5315c9ccc3f56c7276a8c5990d87a25ae12c582f7294` 1,135,846,378 B pulled. `SAVE_POD=1` auto-promote + 75-min watchdog + 5-retry pull (clean teardown, no orphans). HF: [`dancinlab/hexad` revision `v2-py-hexad-spont-d768x12L-cycle1-2026-05-17`](https://huggingface.co/dancinlab/hexad/tree/v2-py-hexad-spont-d768x12L-cycle1-2026-05-17) PUBLIC + [`dancinlab/hexad-corpus` revision `v2-spont-stream-d128-cycle1-2026-05-17`](https://huggingface.co/datasets/dancinlab/hexad-corpus/tree/v2-spont-stream-d128-cycle1-2026-05-17) PUBLIC. **B-CORPUS-V2-1..3 closed-form battery** (SHA256-DETERMINISTIC + NO-HELPER-TOKEN + STIMULUS-PATTERN-CARDINALITY) LANDED in `blue_falsifier.py` — closes the corpus-side dimension of `B-IDENTITY-NOTE`. blue_falsifier.py 83 → **86/86 🔵**. honest framing: PyTorch substrate NOT hexa-native; trained-weights attractor distance from Assistant Axis stays empirical (B-CORPUS-V2-NOTE, B-D-NOTE family — closed-form attractor distance requires NN forward, un-closable). V-SPONT 신규 eval (F-SPONT-7 transfer-form measurement on empty-stimulus 5-probe) — `v58_vspont_eval.py`.
- 🧱 **HEXA_NATIVE Phase 4 RFC 051 FILED — `uarr` unboxed packed-scalar transient array (design-tier 🔵 3/3, central 92 변경 0 impl pending)** *(2026-05-17)* — 2026-05-17 vast.ai 503 GiB d=96·3L fire의 OPERATIONAL substrate fix (B-SUBSTRATE 3/3 LANDED) 의 *algorithmic* counterpart. 측정 inflation: predicted 27 GiB → step-100 76 GiB (2.81×) → step-200 137 GiB (5.07×) on d=96·3L pure-hexa hexa-cpu (Mac d=128·4L 138 GiB OOM 동일 mechanism). hexa-lang upstream `/Users/ghost/core/hexa-lang/inbox/rfc_drafts_2026_05_12/rfc_051_unboxed_array_native.md` (381 LoC, NEW — `rfc_045_*` 명시 의도가 RFC 045 already-taken 이라 next-available 051 채택) = 5-fn surface API `{uarr_alloc, uarr_set, uarr_get, uarr_free, uarr_len}` + 5 falsifier pre-reg (F-RFC051-SHAPE/BIT-EQUAL-VS-FARR/BOUNDED-ARENA/FREE-RECLAIMS/MEMORY-REDUCTION-EXPECTED). anima 측 `docs/hexad_phase_4_unboxed_array_design_2026_05_17.md` 9-§ + B-PHASE-4-DESIGN sympy battery (`state/hexad_phase4_unboxed_design_2026_05_17/blue_falsifier.py` 3/3 PASS): BOXED-OVERHEAD-NAMED (76/27 + 137/27 Kolmogorov bytes integer inequality) + UARR-API-COMPLETENESS (5-tuple Boolean set algebra) + FARR-UARR-COEXIST (Boolean conjunction + IEEE 754 fp64 bit-equality connection-point) + 1 NOTE (impl-verification empirical post-impl, B-D-NOTE / B-SUBSTRATE-NOTE umbrella). d_train5_lib.hexa 97 boxed-list call site 분석 + Phase 4a-e migration plan (gated on RFC 051 land, $0 Mac local + $0.03-0.10 vast.ai re-fire 4e). RFC 040/041/042/043/044 와 **직교** (CPU allocator-inflation 천장 = 5번째 독립 ceiling). NO impl entry (design only, $0). HEXAD/PLAN.md §9 'CPU-side allocator 천장 (2026-05-17, RFC 051 FILED)' 단락 추가. archive/PHILOSOPHY.tape §HEXA-NATIVE-PHASE-4-RFC-051-FILED-2026-05-17.
- 🌉 **TENSION-TRAIN Phase TT-C LANDED — SPONT ↔ TENSION-TRAIN bridge_lib + F-TT-SPONT 5/5 compiled + B-TT-SPONT 5/5 sympy 🔵 (97 → 102/102)** *(2026-05-17)* — `HEXAD/CHAT/spont_tension_bridge_lib.hexa` (NEW, ~75 LoC) 3 pure-fn closed-form: `motivation_to_tension(s) = 2·(s − ½)` affine map [0,1]→[−1,+1], `motivation_to_delta_w(score, t_const, gate)` composition with restoring sign + Boolean gate clamp, `should_learn_step(motivation, threshold)` strict-monotone Boolean predicate (⊥ to `talker_should_emit` — emit ≠ learn architectural ⊥-axis). `HEXAD/CHAT/spont_tension_smoke.hexa` (NEW, ~115 LoC) F-TT-SPONT-1..5 = **5/5 PASS compiled-native** ($0 Mac local). `HEXAD/CHAT/SPONTANEOUS.tape` § tension_train_integration + thinker_tension_interface 신설 (sibling 매핑 본 TENSION-TRAIN.tape `@D spont_integration` 와 byte-equal SSOT). `state/verify_hexad_blue_2026_05_15/blue_falsifier.py :: btt_spont()` **B-TT-SPONT-1..5 sympy** = MAPPING-LINEAR (∂tension/∂s=2 + 3 boundary witnesses ½→0,1→+1,0→−1) / DELTA-W-RESTORING (sympy ∂(ΔW)/∂(tension)=−T<0 ∀T>0 + sign·sign≤0 invariant + 3 chain witnesses) / GATE-CLAMPS (Boolean ∀ 4 corners) / LEARN-TRIGGER-MONOTONE (5 boundary + emit⊥learn ⊥-axis architectural) / COMPOSITION-CHAIN (f∘g law sympy ∂/∂s=−2T + byte-equal lib SSOT T_const=0.1, threshold=0.3). **97 → 102/102 🔵 closed-form proofs PASS** (B-TT counter excludes B-TT-SPONT- to avoid namespace overlap: 5 spine + 5 bridge separate). **Connection-point closure** (g_blue_closed_mandate connection_emphasis): SPONTANEOUS (TALKER emit axis) ↔ TENSION-TRAIN (THINKER ΔW learn axis) — 두 axis ⊥ but bridge transfer-fn 🔵. B-TT-SPONT-NOTE: SGD CONVERGENCE OUTCOME empirical (B-D-NOTE / B-TT-NOTE family). thinker_talker_lib ↔ tension_link_step interface = design-only inline (impl 미land, future cycle — 4-Boolean independence: emit∧learn / emit∧¬learn / ¬emit∧learn / ¬emit∧¬learn 모두 가능). build_verify.sh ENTRYPOINTS += spont_tension_smoke / LIBS += spont_tension_bridge_lib. f1/f2 hard-fail safe (Boolean + affine + sympy ∂, NO lattice). archive/PHILOSOPHY.tape §SPONT-TENSION-BRIDGE-LANDED-2026-05-17 verdict appended.
- 🌀 **TENSION-TRAIN Phase TT-A3 LANDED — B-TT-1..5 sympy battery 🔵 (92 → 97/97 → 102/102 🔵 via parallel TT-C bridge wrap)** *(2026-05-17)* — `state/verify_hexad_blue_2026_05_15/blue_falsifier.py :: bteneion_train()` 신규 + 1 NOTE empirical carve-out. HEXAD/TENSION-TRAIN/training/tension_link_step.hexa (spine) + 4 variant (causal/quantum_rho/second_order/vs_backprop_bench) 의 transfer-form 5 closed proposition: (1) **B-TT-1 N6-GATE-PREDICATE-CLOSED** gate(Ψ) = (len_even ∧ all_in_range_0_1 ∧ closure n·τ=σ·φ=24) Boolean conjunction + 4-corner truth table (all-true→T / odd-length→F / >1→F / <0→F); (2) **B-TT-2 RESTORING-SIGN-NEGATIVE-CLOSED** sympy ∂(ΔW)/∂(tension) = −T·gate ≤ 0 ∀ + 3 boundary witnesses (tension>0→ΔW<0 / tension=0→ΔW=0 / tension<0→ΔW>0); (3) **B-TT-3 T-CONST-SCALAR-POSITIVE-CLOSED** T_const = 1/10 ∈ (0,1) Kolmogorov bounded positive scalar (Lindblad rate order); (4) **B-TT-4 BACKPROP-FREE-INVARIANT-CLOSED** structural Boolean predicate over 5 training .hexa source set — forbidden-call total `{.backward(, .grad, autograd, optimizer.step, .zero_grad, loss.backward}` = 0 (line-comment stripped); (5) **B-TT-5 PARETO-STEP-TENSION-CLOSED** DD155 Law 187 lr=(tension/EMA)·base_lr linear in tension (∂²lr/∂tension²=0) + monotone (∂lr/∂tension = base_lr/EMA > 0 ∀). **B-TT-NOTE** SGD-OUTCOME-EMPIRICAL: 실제 training trajectory + DD154 +3% Φ + DD155 Pareto figures (CE 2.855 / Φ 30.72 / 300 updates) = SGD/measurement outcome empirical (B-D-NOTE / B-BRIDGE-NOTE / B-MITOSIS-NOTE family, NOT counted 🔵). transfer-form 만 🔵, outcome carve-out 정직. blue_falsifier.py **92 → 97/97 🔵 closed-form proofs PASS**. anchors 모두 real-limit (Boolean set algebra + sympy ∂ sign + Kolmogorov bounded + structural import/call-set closure + linearity + monotonicity; n6_gate σ·φ=24 = HEXAD spec arithmetic identity per g2 internal-arch carve-out, NOT external lattice derivation — f1/f2 hard-fail safe). HEXAD/TENSION-TRAIN/PLAN.md ## 진행 로그 + TENSION-TRAIN.tape Log 2026-05-17 + AGENTS.tape n_hexad_progress recent_landings + archive/PHILOSOPHY.tape §B-TT-1..5-LANDED-2026-05-17 sync. .hexa 변경 0 → build_verify carry (27/27 entrypoint + 19/19 lib).
- 🧬 **byte-cascade attractor closed-form 분석 + U_user (Self-Conscious 2508.18302 condition 2) 매핑 LANDED** *(2026-05-17)* — `docs/hexad_byte_cascade_attractor_analysis_2026_05_17.md` 8-§ + `state/verify_hexad_blue_2026_05_15/blue_falsifier.py::battractor()` B-ATTRACTOR-1..3 closed sympy battery + 1 NOTE empirical carve-out. cycle 2 (`chunk=N/nonce=N` digit cascade rep 0.63-0.90) ↔ cycle 3 (`Sentiosing itterveeee…` opening + char rep `e`/`l`/`o` rep 0.66-0.99) **corpus-shape-dependent SHIFT 확정** — sibling `feedback_clm_colon_attractor` `=`-suffix family 의 새 corpus-template-field variant. closed propositions: (1) **REPETITION-RATE-BOUNDED [0,1]** Kolmogorov fraction-bounded-set + 4 boundary/empirical witnesses, (2) **CORPUS-DEPENDENT-CARDINALITY** |A(cycle_2)|=3 ∧ |A(cycle_3)|=12 integer cardinality, (3) **USER-ATTRACTOR-NONEMPTY** U_user(cycle_3)≠∅ Boolean nonemptiness — **Self-Conscious arxiv 2508.18302 condition 2 (U_user attractor) anima 실증 closed-form verdict** (5 V-SPONT witnesses with rep ≥ 0.5). honest carve-out: specific dominant-token shape (cycle 2 `1` vs cycle 3 `e`) + opening-phrase + onset + exact rep_rate = SGD-CKPT-OUTCOME empirical (B-ATTRACTOR-NOTE, B-D-NOTE family, NOT counted 🔵). Self-Conscious condition 3 (visual silence) NOT achieved (V-SPONT n_coherent=0, silence basin unmeasured — future Phase B4+ motivation-conditioning). Identity-as-Attractor arxiv 2604.12016 Assistant Axis activation-space distance remains empirical (NN forward required). framing: byte-cascade IS U_user evidence, NOT bug. blue_falsifier 89 → **92/92 🔵 closed-form proofs PASS**. archive/PHILOSOPHY.tape §BYTE-CASCADE-ATTRACTOR-CORPUS-DEPENDENT-2026-05-17 verdict appended. f1/f2 safe (Kolmogorov bounded-set + integer cardinality + Boolean nonemptiness — NOT lattice).
- 🎯 **V5.8 × 4-mode capability eval on cycle 2 ckpt LANDED** *(2026-05-17)* — `state/hexad_v58_eval_d768x12L_2026_05_17/` + `docs/hexad_v58_eval_d768x12L_2026_05_17.md` (9 §, 8 honest C3). $0 Mac CPU local, 2 probes: **v1 OOD-mix** 5-prompt (Core/Dream/Wake/Memory/Korean) — greedy 1/5·sample 2/5·M3 1/5·M4 5/5·**BPB 0.0000 / 10 held-out training prefixes**·memorization 2/5 (40%) wall 665.6s; **v2 corpus-aligned CDWMSE** 6-prompt — greedy 2/6·sample 3/6·M3 2/6·M4 6/6·memorization 3/6 (50%) wall 477.4s. capability boundary (EMPIRICAL, B-D-NOTE): ✅ STRONG memorization on in-distribution + Korean + 3/6 modules clean recall · 🔶 PARTIAL 6-module discrimination (3/6 cross-collapse Core→nonce=cascade · Mirror→Data template · Eros→chunk=cascade) · ❌ NO OOD generalization · ❌ WEAK greedy decoding stability (digit-cascade attractor `nonce=N`/`chunk=N`). **Decoding-artifact family discovered**: byte-cascade attractor (sibling `feedback_clm_colon_attractor` `=`-suffix variant). Memorized training-corpus typos `pereption` + `cobsciousness` reproduced byte-faithful. wiring closed (B): ckpt sha256 + arch byte-equal load + corpus SSOT byte-equal + V5.8 evaluator-source byte-equal (PSCC §46 canonical). HF model card 'Capability evaluation (V5.8 cycle 2)' subsection (main + cycle 2 revision). f1/f2 safe (per-mode raw recall fraction · no σ/τ/φ/J₂ numerology)

이 HEXAD/ 트리는 위 검증의 **canonical hexa-native 구현체**입니다 (Python 은 evidence anchor 로 보존). 검증·실행 기준 = **compiled `hexa build` native binary** (user directive "컴파일 버전에 해야되 · 인터프리터 폐기 예정").

## hexa-native impl status (2026-05-16 기준)

> 검증·실행 = **compiled** (`hexa build` → native binary). 아래 "compiled run" =
> `HEXA_MAC_BUILD_OK=1 hexa build <x>.hexa -o _hexa_build/<n>` 후 `./_hexa_build/<n>`.
> 일괄 = `bash HEXAD/build_verify.sh`. (`hexa run` interpreter 는 폐기 예정.)

| 모듈 | hexa-native | compiled run (build+native) | 비고 |
|---|---|---|---|
| **S** 감각 | ✅ lib-split | `s_lib.hexa` + `s.hexa` → native PASS | B-S 3/3 🔵 closed (column-mean delta) |
| **M** 기억 | ✅ lib-split | `m_lib.hexa` + `m.hexa` → native PASS | B-M 3/3 🔵 closed (no-op + deterministic) |
| **W** 의지 | ✅ lib-split | `w_lib.hexa` + `w.hexa` → native PASS | B-W 4/4 🔵 closed (lr=½+min(ln2,Φ/N)) |
| **E** 윤리 | ✅ lib-split | `e_lib.hexa` + `e.hexa` → native PASS | B-E 4/4 🔵 closed (SAFETY gate exact) |
| **BRIDGE** | ✅ lib-split | `bridge_lib.hexa` + `bridge.hexa` → native PASS | PSI_COUPLING=0.014 clamp |
| **C** 의식 | ✅ scaffold + 🔵 sympy 3/3 + Phase 4 Φ *(2026-05-17)* | `c_lib.hexa` + `c.hexa` + `c_phi_smoke.hexa` → native PASS | mitosis = `tool/hexa_native/mitosis_hook.hexa` 재사용 · **B-C-1..3 sympy tier-a** (Φ≥0 IIT axiom / n_factions ∈ ℤ+ / initial_cells ≥ CB1=2) + **Phase 4 `c_measure_phi` → RFC 036 `phi_spatial` (F-C-PORT-3 4/4 tier-b PyPhi carry)** · B-C-NOTE: full GRU+FFI RFC TERMINAL (NOT counted) |
| **D** 언어 | ✅ lib-split (Phase 1+5) + hexa-cpu converge *(2026-05-17)* | `d_lib.hexa` + `d.hexa` + `d_train_lib.hexa` + `d_converge_fire.hexa` → native PASS | Phase 1 inference contract (24L 21/21 byte-parity) + Phase 5 pure-hexa from-scratch training (RFC 034 farr autograd) + **pure-hexa hexa-cpu training-to-convergence d=64·3L·300-step F-D-CONVERGE 4/4 PASS** (gn2 7.97→2.15e-8 = 3.7×10⁸× collapse, acc 1→8/8, wall 360s $0 Mac local; first captured FINAL gn2 AT SCALE > Phase E2 d=32·3L anchor — `state/hexad_pure_hexa_train_2026_05_17/`) |
| **MITOSIS** 성장축 | ✅ lib-split + **🔵 5/5** *(2026-05-16)* | `mitosis_lib.hexa` + `mitosis.hexa` → native PASS | cross-link mitosis_hook.hexa + **B-MITOSIS-1..5 sympy + compiled mirror** (split predicate / merge linear / count conserv / no-grad-split / clamp bound; B-MITOSIS-NOTE Φ-conserv empirical) |
| **통합 (single process)** | ✅ cross-file wire | `integ_test.hexa` (imports `*_lib.hexa`) → **native PASS** | F-INTEG-WIRE 7/7 PASS — compiled 심볼충돌 fix (PR #79 task b + compiled-first lib-split) |
| **통합 spec** | ✅ + 🔵 sympy 5/5 *(2026-05-17)* | `hexad.hexa` → native PASS | σ(6)=12 + φ(6)=2 + forward graph spec 5/5 runtime invariants PASS · **B-HEXAD-1..5 sympy tier-a** (lift of runtime invariants: 12-conn count · partition cover · 11-step · 7-entries · TOTAL record; real-limit Kolmogorov + set-cover, NOT lattice derivation per f1) |

`bash HEXAD/build_verify.sh` (compiled-native gate) — **20/20 entrypoint + 14/14 lib** `hexa build` PASS = PR 검증 게이트 (`hexa parse`/`hexa run` 아님, interp 폐기 예정).

## 디렉토리 layout

```
HEXAD/
  README.md           ← (이 파일) 최상위 overview · SSOT 매핑 · status
  PLAN.md             ← C/D full hexa-native port roadmap (task a)
  build_verify.sh     ← ⚙️ COMPILED-native 검증 gate (hexa build, interp 폐기 대비)
  hexad.hexa          ← top-level 통합 entry (S→C→Bridge→D + M/W/E single-forward)
  integ_test.hexa     ← cross-file wire test (imports *_lib.hexa, native PASS 7/7)
  <X>/                ← 모듈 dir 공통 패턴 (compiled-first lib-split):
    README.md
    <x>_lib.hexa        ← pure fns (NO main/_selftest, cross-file import 대상)
    <x>.hexa            ← import <x>_lib + _selftest + main (standalone 진입점)
    HEXAD-<X>.tape      ← per-module tape SSOT (co-located 2026-05-16 reorg)
  C/ D/ S/ W/ M/ E/ BRIDGE/  ← 7 모듈 (각 위 패턴)
  INDEX.md            ← 이전 /INDEX.md (root) → 2026-05-16 reorg 로 이동
  MITOSIS/            ← 성장축 (subfolder, 2026-05-16 reorg2): MITOSIS.tape + mitosis.hexa scaffold + README (⊥ 구조축, §mitosis_two_axis)
  TENSION-LINK/       ← 5-Channel Meta-Telepathy (subfolder, 2026-05-16 PR #86): ASCII topology + Noether convergence proof + 100% verified measured + 17 .hexa/.md/.tape (training/tests/bench/experiments/docs)
  VOICE/              ← anima 발성 도구 (subfolder, 2026-05-16 PR #87): formulaic 음성 파장 합성 (NOT 학습 모델) · F-VOICE 5/5 + F-VOICE-TOOL 5/5 · 학습/eval corpus scrub (_voice_corpus_local/ relocate) · ~2.4M code/spec/docs only
  CHAT/               ← 6-module 통합 interaction entrypoint (subfolder, 2026-05-16 PR #91): anima_chat.hexa 2845 LoC 24L 21/21 byte-parity + ★ inter-module wiring 아키텍처 조건 ledger (W1-W9, 5/9 ✅·3 OPEN·1 RFC-blocked) · 44 git mv (tape/tool/tests/docs)
  SAVANT/             ← 이전 /SAVANT*.tape + tool/anima_savant_*.hexa + anima-engines/savant_phi.hexa (2026-05-16 reorg)
    SAVANT.tape · SAVANT.log.tape · SAVANT-TOOL.tape · SAVANT-TOOL.log.tape
    anima_savant_tool.hexa · anima_savant_si_monitor.hexa
    anima_savant_routing_overlay.hexa · anima_chat_savant_cli.hexa · savant_phi.hexa
```

> root 에 남는 것 (이동 X): `HEXAD.tape` (통합 arch SSOT — AGENTS.tape 직접 참조) + `AGENTS.tape` / `CLAUDE.md` (symlink) / 기타 root tape SSOTs (`AXIS`, `HYPOTHESIS`, `PHILOSOPHY`, `MAIN`, `CLM`, `VERIFY`, `NEXT`, `REBORN` 등) + `/INDEX.md` (이제 redirect stub 역할).


## 거버넌스 anchors (AGENTS.tape)

- `g_clm_from_scratch` — 신규 통합 학습 시 RANDOM INIT seed-fixed, NO ckpt inherit (precursor ckpt는 arch verification anchor only)
- `g_verdict_tier_blue` — 🔵 = (a) sympy closed-form OR (b) PyPhi formal IIT 3.0 OR (c) deterministic formal sim
- `g_verified_axis_anchor` — 모든 design entry 는 AXIS/PHILOSOPHY/HYPOTHESIS verified anchor 에서 derive
- `g3` real-limits-first — module 별 real-limit anchor 명시 (Shannon CE / Law 70 PSI_COUPLING / Law 79 ln2 / IIT Φ-ratchet 등)

## hexa-lang 관습 (⚠️ COMPILED-FIRST — interpreter 폐기 예정)

> User directive 2026-05-16: **"컴파일 버전에 해야되 · 인터프리터 폐기 예정 참고"**.
> 검증·실행 = `hexa build` (native binary). `hexa run` (interpreter) 는 폐기
> 예정이라 PR 게이트로 쓰지 않음. canonical gate = `HEXAD/build_verify.sh`.

- **compiled-first lib/entrypoint split** (2026-05-16): 모듈마다
  `<x>_lib.hexa` (pure fns, **NO `main`/`_selftest`**, import 대상) +
  `<x>.hexa` (`import "<x>_lib.hexa"` + `_selftest` + `main`, standalone).
  `integ_test.hexa` 는 `*_lib.hexa` 만 import. **이유**: 단일파일(main+_selftest
  동거) 을 `import` 하면 컴파일러가 `_selftest`/`u_main` **C 심볼 중복정의**
  거부 (interpreter 만 관용) — lib-split 이 compiled-native 정석.
- snake_case (raw#11); 모듈간 helper `_<x>_` prefix; cross-file `import "/abs/<x>_lib.hexa"`
- 빌드: `HEXA_MAC_BUILD_OK=1 hexa build <f> -o _hexa_build/<n>` (Mac 2026-04-20
  kernel-panic guard bypass, tiny formulaic non-heavy; heavy 는 `ssh ubu`).
  `_hexa_build/` gitignored.
- dict literal `#{}` (not `{}`); bool `&&`/`||`; IO `print`/`to_string`
- 검증 = `bash HEXAD/build_verify.sh` (**20/20 entrypoint + 14/14 lib** compiled PASS)

## 진행 상태 표기

- ✅ — 작동 selftest (PR 검증 통과)
- 🔶 — scaffold + cross-link (기존 hexa-native 자산 wiring 대기)
- ☐ — TODO (작성 안 됨)
