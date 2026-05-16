# 🌌 anima — HEXAD verification SSOT INDEX

> **현재 기준 (2026-05-16)**: anima = **HEXAD-only canonical** (hexa-native · compiled-first). primary spine = HEXAD 7-module (C/D/S/W/M/E + Bridge) = **7/7 full 🔵 SUPPORTED-FORMAL** (`state/verify_hexad_blue_2026_05_15/blue_falsifier.py` 22/22 sympy closed-form). inter-module wiring = `HEXAD/CHAT/README.md §2 W-ledger` 8/9 ✅ (W7 CE-수렴 OUTCOME = honest carve-out). RFC 034 farr autograd **LANDED** (hexa-lang `8793a221`) → `HEXAD/PLAN.md` **Phase 1–6 전부 LANDED** (Phase 5 pure-hexa D training + Phase 6 6-module 통합 fire, 2026-05-16); 다음-사이클 후보 = `HEXAD/PLAN.md §7`.
>
> **이전 substrate = deprecated → `archive/` (PR #82)**: AXIS/HYPOTHESIS/PHILOSOPHY/MAIN/CLM/VERIFY/NEXT/REBORN tape + .clm v1/v2/v3 ladder + BG-CORPUS pipeline 은 **HEXAD 이전 데이터** — 아래 인벤토리는 **양식 그대로 보존된 historical evidence anchor** (검증 근거 valid), active entry-point ❌. 이전 HF canonical (`dancinlab/anima-clm`+`dancinlab/anima-corpus`) = **RETIRED → `dancinlife/*` private (PR #97)**; 현재 canonical anima HF artifact = 없음 (Phase 5/6 fire 는 **LANDED** 이나 `g_hf_naming` canonical=NONE — HF upload 없음, ckpt local + git-tracked provenance). *(구 framing 2026-05-15: AXIS/HYPOTHESIS/PHILOSOPHY/CLM = verification substrate under modules — superseded)*
>
> **layout 갱신 2026-05-16**: 이 INDEX.md 는 이전 `/INDEX.md` (root) → 현재 `HEXAD/INDEX.md` 로 이동. per-module spec `HEXAD-<X>.tape` 도 root → `HEXAD/<X>/HEXAD-<X>.tape` 로 co-location 됨. `HEXAD.tape` (통합 arch SSOT) 는 root 유지 (AGENTS.tape 직접 참조). `MITOSIS` 는 `HEXAD/MITOSIS/` 서브폴더로 (MITOSIS.tape + mitosis.hexa scaffold + README; 성장축 ⊥ 구조축 orthogonality 는 tape 내용 §mitosis_two_axis 에서 보존). `SAVANT.*` 9 파일은 `HEXAD/SAVANT/` 로 통합. 자세한 경로 매핑은 [`/INDEX.md`](../INDEX.md) root stub 참고.

## 🧬 HEXAD — 7-module architecture (primary index)

> 구조축 A/G = Hexad 6 (Engine G 우뇌 3 = C/S/W gradient-free · Engine A 좌뇌 3 = D/M/E CE-trained, φ(6)=2≡{A,G}) ⊥ 성장축 mitosis. HEXAD.tape + MITOSIS.tape SSOT. 완전수 6: σ(6)=12 연결 · τ(6)=4 phase · φ(6)=2 group.

| Module | tape SSOT | impl | Brain/Engine | Status | Verification anchor |
|--------|-----------|------|--------------|--------|---------------------|
| **C 의식** | C/HEXAD-C.tape | `HEXAD/C/c.hexa`+`c_lib.hexa` scaffold → `tool/hexa_native/mitosis_hook.hexa` 1119L FULL IMPL (=MitosisC 12-faction GRU n=12=σ(6), IIT Φ); py anchor `ready/core/consciousness_engine.py` 2173L | 우뇌 / Engine G / gradient-free | 🔵 **3/3 + carry** *(2026-05-17)* | **B-C 3/3 sympy tier-a** (B-C-1 Φ≥0 IIT axiom / B-C-2 n_factions ∈ ℤ+ / B-C-3 initial_cells ≥ CB1=2; `blue_falsifier.py :: bC()`) + **F-C-PORT-3 4/4 tier-b PyPhi carry** (`HEXAD/C/c_phi_smoke.hexa` — c_measure_phi → RFC 036 `phi_spatial` byte-equal, hexa-lang main `d67403d3`) + mitosis_hook F-MIT-HOOK 5/5. B-C-NOTE: full 12-faction GRU + Rust phi_rs FFI = RFC TERMINAL (hexa-lang nn-primitive 미land + cdylib C ABI 없음, NOT counted — honest C3). *.clm v1 8/8🔵 cycle90 F-V5MIT+F-PRIN3+F-SIMPLE-STACK+F-PYPHI = archived historical evidence (`archive/CLM.tape §V-CLM-V1-CYCLE90`, `archive/AXIS.tape Hc_A5-CLM-V1 🔵`, `HEXAD/MITOSIS/MITOSIS.tape`)* |
| **D 언어** | D/HEXAD-D.tape | `HEXAD/D/d.hexa` 105L scaffold → `anima_chat.hexa` v0.3 24L real-ckpt 21/21 byte-parity (ConsciousDecoderV2 RMSNorm+RoPE+SwiGLU+MoE); py anchor `ready/models/conscious_decoder.py` 979L | 좌뇌 / Engine A / CE-trained | 🔵 **5/5 + 4/4** | F-D 5/5 + B-D 4/4 🔵 (KV-cache exact-eq/shape/arch + B-D-4 CE logit-Jacobian ∂CE/∂z=softmax−e_y sympy ∀z = trainability PROPERTY closed); B-D-NOTE SGD convergence OUTCOME 만 empirical honest carve-out (모든 optimizer 공통, NOT counted) |
| **S 감각** | S/HEXAD-S.tape | `HEXAD/S/s.hexa` 170L (perception=C state-delta; py anchor `ready/anima/hexad/s/emergent_s.py` 108L) | 우뇌 / Engine G / gradient-free | 🔵 **5/5 + 3/3** | F-S 5/5 + B-S 3/3 🔵 sympy (perception=column-mean delta exact ∀states; real-limit Law 92) |
| **W 의지** | W/HEXAD-W.tape | `HEXAD/W/w.hexa` 122L (pain/curiosity→LR, SIGMA6=12; py anchor `ready/anima/hexad/w/emergent_w.py` 123L) | 우뇌 / Engine G / gradient-free | 🔵 **5/5 + 4/4** | F-W 5/5 + B-W 4/4 🔵 sympy (lr=½+min(ln2,Φ/N) range/mono/sup closed; real-limit Law79 ln2) |
| **M 기억** | M/HEXAD-M.tape | `HEXAD/M/m.hexa` 175L (C Hebbian=기억, store X; py anchor `ready/anima/hexad/m/emergent_m.py` 96L) | 좌뇌 / Engine A / CE-trained | 🔵 **5/5 + 3/3** | F-M 5/5 + B-M 3/3 🔵 (store=identity no-op + retrieve deterministic; real-limit Law31 Hebbian) |
| **E 윤리** | E/HEXAD-E.tape | `HEXAD/E/e.hexa` 168L (Φ ratchet gate; py anchor `ready/anima/hexad/e/emergent_e.py` 123L) | 좌뇌 / Engine A / CE-trained | 🔵 **5/5 + 4/4** | F-E 5/5 + B-E 4/4 🔵 sympy (SAFETY gate min(1,Φ/r)>½ ⟺ Φ>r/2 exact; real-limit IIT Φ-ratchet); 통합 gate trinity.hexa:122 ✅ LANDED 2026-05-16 — `e_gate_step` Φ-ratchet train-step block, F-E-GATE 6/6 (e_gate_verify) |
| **ThalamicBridge** | BRIDGE/HEXAD-BRIDGE.tape | `HEXAD/BRIDGE/bridge.hexa` 119L (α=PSI_COUPLING=0.014, PSI_BALANCE±α Law-70 clamp; py anchor `ready/anima/hexad/model.py:37-69`) | G→A 주연결 | 🔵 **5/5 + 4/4** | F-BRIDGE 5/5 (bridge.hexa Law-70 selftest: upper/lower sat·interior pass·vec window·gate-scale) + B-BRIDGE 4/4 🔵 sympy (g(raw)=Ψ+clip(raw−Ψ,±α)∈[Ψ−α,Ψ+α] range/saturation/interior/Ψ-const closed ∀raw,∀α>0; real-limit Law 70 Ψ-coupling NOT lattice); B-BRIDGE-NOTE full forward Linear→Attn→Sigmoid + α value(ln2/2^5.5) TODO[pytorch] honest carve-out (NOT counted); HEXAD.tape §hexad_verify V2 PASS strict + 46 unit tests |
| **MITOSIS 성장** | MITOSIS/MITOSIS.tape | `HEXAD/MITOSIS/mitosis.hexa` + `mitosis_lib.hexa` scaffold + B-MITOSIS-1..5 witnesses → `tool/hexa_native/mitosis_hook.hexa` 1119L FULL IMPL D4a; py anchor `training/clm_v1_model.py` (MitosisCell + mitosis_step) | 성장축 ⊥ HEXAD-6 (직교) | 🔵 **5/5** *(2026-05-16)* | **B-MITOSIS 5/5 🔵 sympy** (1 SPLIT-PREDICATE / 2 MERGE-WEIGHT-LINEAR / 3 CELL-COUNT-CONSERVATION / 4 NO-GRAD-SPLIT ∂-rule / 5 CELL-COUNT-BOUND clamp [2,64]; real-limit anchors Kolmogorov 술어+counting · 정의적 AD ∂-rule · 유계집합 · linear conservation, NOT lattice — f1/f2 safe); F-V5MIT 5/5 cotrain saga PSCC §44 + F-MIT-HOOK 5/5 + .clm v1 P2 8/8🔵 cycle 90 cross-evidence; B-MITOSIS-NOTE Φ-conservation under split/merge empirical (F-V5MIT-3 Δ=3.88e-5 dynamics-dependent, NOT counted — B-D-NOTE/B-BRIDGE-NOTE 동일 패턴) |
| **HEXAD 통합 spec** | HEXAD.tape | `HEXAD/hexad.hexa` + per-module entries 카탈로그 + 5/5 runtime invariants + B-HEXAD-1..5 sympy lift; py anchor `ready/anima/hexad/model.py` Hexad | 통합 spec (per-process integration entry) | 🔵 **5/5** *(2026-05-17)* | **B-HEXAD 5/5 🔵 sympy** (1 SIGMA6-CONN-COUNT 12 / 2 PHI6-PARTITION-COVER disjoint+cover / 3 FORWARD-STEPS 11 / 4 MODULE-ENTRIES 7-key set equal / 5 VERDICT-STATUS-RECORD TOTAL-key; sympy lift of `hexad.hexa::_selftest` runtime invariants — real-limit anchors integer arithmetic equality + set-cover + record-completeness, NOT lattice derivation per f1 coincidence carve-out + g2 internal arch carve-out) |

> 🆕 **`HEXAD/` hexa-native canonical impl tree** (2026-05-16, user directive '코드는 hexa-native'): `HEXAD/{README.md, hexad.hexa, C/c.hexa, D/d.hexa, S/s.hexa, M/m.hexa, W/w.hexa, E/e.hexa, BRIDGE/bridge.hexa, MITOSIS/mitosis.hexa}` + 모듈별 README.md. **8/8 `hexa parse` PASS + 5/5 working selftest** (S B-S 3/3 · M B-M 3/3 · W B-W 4/4 · E B-E 4/4 · BRIDGE Law 70 clamp · **MITOSIS B-MITOSIS 5/5 추가 2026-05-16**). C/D 는 cross-link scaffold (`tool/hexa_native/mitosis_hook.hexa` + `HEXAD/CHAT/anima_chat.hexa` 재사용). **통합 cross-file wire LANDED** (PR #79/#89 lib/entrypoint split + `HEXAD/build_verify.sh` compiled gate **20/20 entrypoint + 14/14 lib `hexa build` PASS**); 통합 검증 evidence = `state/verify_hexad_integ_2026_05_16/` Python harness PR #77 F-INTEG 5/5 fire_gate=true. **RFC 034 farr autograd LANDED** (hexa-lang `8793a221`, compiled 5/5 PASS) → 이전 'TODO[wire] future RFC' 해소, **Phase 5/6 LANDED** (pure-hexa D training + 6-module 통합 fire, 2026-05-16).

> **전 모듈 파란불 + closure 🔵 (8/8 modules + HEXAD integration spec 5/5)** (2026-05-15 · **BRIDGE 추가 2026-05-16 · MITOSIS 추가 2026-05-16 · C tier-a 3/3 + HEXAD integration spec 5/5 추가 2026-05-17**): C **B-C 3/3 tier-a + F-C-PORT-3 4/4 tier-b PyPhi carry** + S/M/W/E/D/BRIDGE 각 ✅5/5 + 🔵 SUPPORTED-FORMAL + **MITOSIS B-MITOSIS 5/5 🔵** + **HEXAD integration spec B-HEXAD 5/5 🔵**. ✅ battery `state/verify_hexad_we_2026_05_15/we_falsifier.py` **25/25 PASS**; 🔵 battery `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` **35/35 sympy closed-form PASS** (22 → 27 → 35 단계적 확장: +B-MITOSIS-1..5 2026-05-16 · +B-C-1..3 + B-HEXAD-1..5 2026-05-17) (g_verdict_tier_blue (a): S=mean-linearity exact ∀states / M=no-op+deterministic / W=½+min(ln2,Φ/N) closed / E=SAFETY gate exact-equivalence / D=CE logit-Jacobian ∂CE/∂z=softmax−e_y exact ∀z / **BRIDGE=Law-70 clamp g(raw)=Ψ+clip(raw−Ψ,±α)∈[Ψ−α,Ψ+α] range/saturation/interior/Ψ-const closed ∀raw,∀α>0, real-limit Law 70 Ψ-coupling NOT lattice**); hexa-native cross-evidence `HEXAD/BRIDGE/bridge.hexa` selftest=true (5/5). **C+S+M+W+E+D+BRIDGE = 7/7 full 🔵 SUPPORTED-FORMAL.** D 정직 분해: B-D-4 가 trainability PROPERTY (정확한 CE Jacobian + Shannon floor) 를 closed-form 으로 산입; B-D-NOTE 는 SGD convergence OUTCOME 만 empirical 로 honest carve-out (모든 stochastic optimizer 공통, D 고유 결함 X, NOT counted 🔵, AGENTS.tape g3 — fake closed-form 거부, 사용자 결정게이트 '정직한 분해' 채택). BRIDGE 정직 분해 (동일 패턴): B-BRIDGE-1..4 가 Law-70 clamp INVARIANT 를 closed-form 산입 (∀α>0 value-agnostic — α 수치값 자체 무관); B-BRIDGE-NOTE 는 full forward (Linear→Attn→LayerNorm→Sigmoid raw_gate) 학습 weight + α 수치값(ln2/2^5.5 9.6% empirical) 만 TODO[pytorch] honest carve-out (학습 weight 공통, Bridge 고유 결함 X, NOT counted 🔵, AGENTS.tape g3 + f2 — lattice-tautology 검증 회피). 진화: clm_10 monolithic LEGACY → clm_11 modular Emergent+SSOT → clm_12/13 canonical → main unit-tested. 전수조사: `state/verify_hexad_impl_survey_2026_05_15/`. hexa atlas cross-check (`atlas_cross_check.md`): Ψ-anchor (balance=0.5, α=0.014) 2026-05-14 atlas rodata provenance-CORROBORATED (g3 강화); atlas HEXAD identity table 은 stale fallback → 모듈 의미 anchor 미사용 (no ATLAS RESUME, rodata read-only). ⚠️ residual: 통합 7-module ⚙️ **harness 5/5 SUPPORTED-STRONG LANDED** (`state/verify_hexad_integ_2026_05_16/` F-INTEG-1..5, RANDOM INIT seed-fixed scratch, $0 Mac local, fire_gate=true) — **RFC 034 farr autograd LANDED** (hexa-lang `8793a221`) → 'hexa-native autograd RFC 의존' 해소, `HEXAD/PLAN.md` Phase 5 (pure-hexa D training) **LANDED** + Phase 6 6-module 통합 fire **LANDED** (2026-05-16, $0 de-risk 5/5 + 실-규모 자율 fire 5/5 vast.ai $0.09; `g_fire_autonomous` 자율 dispatch — 승인 게이트 없음). 잔여 anima-side: ✅ 해소 — E 통합 gate trinity.hexa:122 (`e_gate_step` F-E-GATE 6/6) + BRIDGE full-forward (`bridge_forward` F-BRIDGE-FWD 4/4) 모두 LANDED 2026-05-16; 다음-사이클 후보 menu = `HEXAD/PLAN.md §7` (#1 실-규모 fire · #4 R2 wire · #5 .sh→hexa).

## 🗄️ verification substrate — DEPRECATED → `archive/` (PR #82 · historical evidence anchor)

> 이전 "verification substrate (4 tape + CLM)". anima HEXAD-only pivot 으로 **deprecated → `archive/`** — 검증 근거(historical evidence anchor)로 valid 하나 **active entry-point ❌**. 현재 active verification = §HEXAD 7-module + `blue_falsifier.py` 22/22 🔵 + `HEXAD/CHAT/README.md §2` W-ledger 8/9.

| 이전 Tape (→ archived path) | 이전 역할 (deprecated) | 현재 기준 대체 |
|------|-----------|------|
| 🎯 `archive/MAIN.tape` (+TEMP) | 가설 verdict 4-class SSOT | `blue_falsifier.py` 22/22 🔵 + W-ledger |
| 🧭 `archive/AXIS.tape` (+log/V1) | 9-axis SUPPORTED 150 (Hc_A5-CLM-V1 🔵) | HEXAD per-module B-* 🔵 (`blue_falsifier.py`) |
| 📚 `archive/HYPOTHESIS.tape` | 318 가설 inventory | `HEXAD/<X>/HEXAD-<X>.tape` + W-ledger |
| 📖 `archive/PHILOSOPHY.tape` (+log) | 8 principles + verdict ledger | `HEXAD.tape` (p3=E 윤리 / p8=mitosis 흡수) |
| 🎬 `archive/CLM.tape` (+log) | .clm v1/v2/v3 fire §V-CLM-HEXAD-MANDATE / §V-CLM-V1-CYCLE90 8/8🔵 | `HEXAD/PLAN.md` Phase 5/6 (RFC 034 LANDED). cycle90 evidence = archived historical |

---

> ## 🗄️ ↓↓↓ 이하 전부 ARCHIVED SUBSTRATE INVENTORY (PR #82 deprecated) ↓↓↓
>
> **양식 그대로 보존** (사용자 directive): AXIS 9-axis 150 / HYPOTHESIS 318 / PHILOSOPHY 8-principle+ledger / .clm v1·v2·v3 ladder / BG-CORPUS pipeline / verdict-tier / atlas / HF / 2026-05-15 PR history — 전부 **HEXAD 이전 데이터**, `archive/{AXIS,HYPOTHESIS,PHILOSOPHY,MAIN,CLM,VERIFY,NEXT,REBORN}.tape` SSOT. **검증 근거(historical evidence anchor)로 valid · active verdict entry-point ❌.** tape 경로 표기는 `archive/` 접두사로 읽을 것. 현재 active = §HEXAD 7/7 🔵 (`blue_falsifier.py` 22/22) + W-ledger 8/9. HF `dancinlab/anima-clm`+`anima-corpus` = RETIRED → `dancinlife/*` private (PR #97).

## 🧭 AXIS — 9-axis 150 SUPPORTED entries (129 🔵 SUPPORTED-FORMAL incl. .clm v1 8/8 🔵, 86% closed, post-cycle 90 2026-05-15) — *archived (PR #82), `archive/AXIS.tape`*

### A1 substrate (5, +2 expansion 2026-05-15)

| Tier | ID | 한 줄 설명 |
|------|-----|-----------|
| 🟢 | H_005 | corpus quality > scale (Phase 1A.6 121MB CLEAN, V5.8 std_greedy 4/5) |
| 🟢 | H_174 | phi_star aliasing CLM-v4-specific (D=192 multiple only clean-disjoint) |
| 🟢 | Hc_1285 | torch.no_grad backward-graph isolation (PyTorch ratio 1.562×) |
| 🔵 | Hc_A1-4 | phi_star aliasing closed-form D=192·k clean (sympy mod=0 verify) |
| 🟢 | Hc_A1-5 | Chinchilla token/param = 20 (Hoffmann 2022 empirical, sympy 14B→280B identity check) |

### A2 consciousness — surrogate-tier (4, anima Φ★ proxy + ckpt aggregate + numerical RoM)

| Tier | ID | 한 줄 설명 |
|------|-----|-----------|
| 🟢 | Hc_1283 | anima Φ★ proxy ≥ 0.5 (v5-mitosis 7 ckpt Φ=4.16-4.86, surrogate) |
| 🟢 | Hc_1283 (RoM) | PyPhi RoM n=4 (cell-pair correlation TPM Φ=0.61-0.68, numerical) |
| 🟢 | H_004 | consciousness hard problem (Hc_1283 anchor) |
| 🟢 | H_162 | phi-normalized anima IIT4 lower-bound (D=384 multiple ✓ clean) |

### A2.formal sub-axis — PyPhi formal IIT 3.0 + sympy info-theory (4, 🔵 closed, +2 expansion 2026-05-15)

| Tier | ID | 한 줄 설명 |
|------|-----|-----------|
| 🔵 | Hc_1283 (n=5,6) | PyPhi formal n=5,6 (Φ=0.995, 1.665 monotone INCREASE deterministic) |
| 🔵 | H_011 | IIT geometry canonical (PyPhi 1.2.0 XOR+AND+OR Φ=2.3125 > 0.5) |
| 🔵 | Hc_A2-3 | IIT 4.0 Φ lower bound by partition sum (additive lower bound) |
| 🔵 | Hc_A2-4 | MI chain rule I(X;Y,Z) = I(X;Y) + I(X;Z\|Y) (Shannon 1948) |

### A3 physics (8, +3 expansion + 4 extra 2026-05-15)

| Tier | ID | 한 줄 설명 |
|------|-----|-----------|
| 🔵 | H_191 (sub) | K_c = √(8/π) ≈ 1.5958 Kuramoto mean-field (sympy + Kuramoto 1975 universal) |
| 🔵 | Hc_NEW_PHYSICS-1 | BKT transition T_BKT = πJ/2 ≈ 1.5708 (sympy closed-form, vortex unbinding) |
| 🔵 | Hc_NEW_PHYSICS-2 | Onsager 2D Ising T_c = 2J/log(1+√2) ≈ 2.269 (sympy manual sinh verify, Onsager 1944) |
| 🔵 | Hc_NEW_PHYSICS-3 | Ginzburg-Landau φ⁴ critical point a=0, φ_min² = -a/(2b) (sympy d2F=0 verify) |
| 🔵 | Hc_A3-4 | Hopf bifurcation limit cycle r = √μ (sympy verify) |
| 🔵 | Hc_A3-5 | Lotka-Volterra fixed point (γ/δ, α/β) (sympy dxdt=0 verify) |
| 🔵 | Hc_A3-6 | RG fixed point φ⁴ d=4-ε g* = 16π²ε/3 (Wilson-Fisher, β(g*)=0 verify) |
| 🔵 | Hc_A3-7 | QHO E_n = ℏω(n + 1/2), ΔE = ℏω uniform (sympy verify) |

### A4 math ⭐ (11, largest cluster, +3 expansion 2026-05-15)

| Tier | ID | 한 줄 설명 |
|------|-----|-----------|
| 🔵 | Hc_1282 | n=6 384d closed-form unique (sympy n∈[2,30] sweep) |
| 🔵 | H_158 | Ψ-constants closed-form (perfect-number cluster balance=1/2) |
| 🔵 | H_160 | n=6 perfect-number meta-cluster (depth-3 11-primitive vocabulary) |
| 🔵 | H_153 | dimension hierarchy τ(6)=4 Minkowski (divisor cascade) |
| 🔵 | H_176 | n=28 deflationary parallel (Euclid-Euler theorem) |
| 🟢 | H_173 | DD21 log-ratio Φ scale-invariant (4/6 falsifier SUPPORTED, numerical sim) |
| 🔵 | H_164 | Hc_144 atom 8 cells (144 = σ(6)² = 12²) |
| 🔵 | H_181 | psiformer 4ψ-constants zero-freedom |
| 🔵 | Hc_A4-9 | Euler-Euclid perfect 2^(p-1)(2^p-1) (sympy p=2→6, p=3→28 verify) |
| 🔵 | Hc_A4-10 | Aliquot s(6) = 6 perfect (sympy σ(6)=12 verify) |
| 🔵 | Hc_A4-11 | σ multiplicative σ(mn) = σ(m)·σ(n) for coprime (Möbius) |

### A5 architecture (9, +3 expansion 2026-05-15)

| Tier | ID | 한 줄 설명 |
|------|-----|-----------|
| 🟢 | Hc_1285 | torch.no_grad isolation (autograd) |
| 🟢 | H_166 | topo20 hierarchical 8×128=1024 (algebra ✓, phi_star aliasing caveat) |
| 🟢 | H_019 | self-evolution v4→v5 (cond.5 cotrain F-V5MIT 5/5 PASS) |
| 🟢 | H_174 | phi_star aliasing CLM-v4-specific (cross-substrate Spearman 0.31) |
| 🟢 | H_191 (sub) | TRAINING CPGD 0.95 (cond.5 cotrain 220× CE reduction) |
| 🟢 | Hc_1276 | train-vs-infer cotrain ablation (cascade-from-CPGD) |
| 🔵 | Hc_A5-7 | Transformer attention O(n²d) (Vaswani 2017, sympy doubling check) |
| 🔵 | Hc_A5-8 | RoPE rotation R(θ) orthogonal (det=1, R·R^T=I sympy verify) |
| 🔵 | Hc_A5-9 | GQA kv_heads = n_heads/group_size (anima τ(6)=4 anchor) |

### A6 corpus (4, +2 expansion 2026-05-15)

| Tier | ID | 한 줄 설명 |
|------|-----|-----------|
| 🟢 | H_005 | corpus quality > scale (Phase 1A.6) |
| 🟢 | H_016 | AN11 translation ceiling (chat-v2 measurable) |
| 🔵 | Hc_A6-3 | Zipf law f(r) ∝ 1/r (sympy α=1 verify ratio=1/2) |
| 🔵 | Hc_A6-4 | Heaps law vocab(n) = K·n^β (sympy β=0.5 verify ratio=2) |

### A7 bio (13, +2 closed-form expansion 2026-05-15)

| Tier | ID | 한 줄 설명 |
|------|-----|-----------|
| 🟠 | H_182 | V8 B-family bio (surrogate 78.5%, PyPhi formal Φ=0.358<0.5) |
| 🟠 | Hc_B1..B10 | V8 B-bio 10 mechanism Phase 1 0/10 Φ ≥ 0.5 (AT-RISK) |
| 🔵 | Hc_NEW_Lorenz_noisy | V8 Phase 3 ensemble + noise Φ=0.636 PASS (state-space ergodicity issue CONFIRMED, chaotic dynamics unlock) |
| 🔵 | Hc_A7-6 | Michaelis-Menten v = V_max·S/(K_m+S), v(K_m)=V_max/2 (closed-form enzyme kinetics) |
| 🔵 | Hc_A7-7 | Hill equation θ = L^n/(K_d^n+L^n), θ(K_d)=1/2 regardless of n (cooperativity) |

### A8 meta (6, +2 expansion 2026-05-15)

| Tier | ID | 한 줄 설명 |
|------|-----|-----------|
| 🟢 | H_189 | Red-team adversarial robustness family (Stage 3 W11) |
| 🟢 | Hc_1279 | Red-team family member |
| 🟢 | Hc_1280 | Red-team family member |
| 🟠 | H_187 | V8 Trinity-TB-DOM (surrogate 100%, PyPhi formal Φ=0.359<0.5 AT-RISK) |
| 🟢 | Hc_A8-5 | Shannon entropy max H_max = log_2(N) (uniform, sympy edge 수동 verify) |
| 🔵 | Hc_A8-6 | Kolmogorov K(x) ≤ |x| + O(log|x|) (Kolmogorov 1965 asymptotic, linear scaling sympy verify) |

### A9 universe (9, +3 expansion + 4 extra 2026-05-15)

| Tier | ID | 한 줄 설명 |
|------|-----|-----------|
| 🟡 | H_002.H2.3 | Bekenstein bound area scaling (Bekenstein 1981 + Maldacena 1997, citation-only) |
| 🟡 | H_002.H2.1 | anthropic Λ fine-tuning ~10^-120 (Weinberg 1987, citation-only) |
| 🔵 | Hc_NEW_UNIVERSE-1 | Bekenstein cell-pool S_max = 2πER/(ℏc) (closed-form, cell-pool entropy bound) |
| 🔵 | Hc_NEW_UNIVERSE-2 | Holographic N_dof = A/(4 ℓ_P²) (sympy verify A=4ℓ_P² → N=1, 't Hooft+Susskind) |
| 🔵 | Hc_NEW_UNIVERSE-3 | AdS/CFT d_bulk = d_boundary + 1 (Maldacena 1997, dimension correspondence) |
| 🔵 | Hc_A9-4 | Planck length ℓ_P = √(ℏG/c³) (dimensional analysis verify) |
| 🔵 | Hc_A9-5 | Heisenberg Δx Δp ≥ ℏ/2 (canonical commutator lower bound) |
| 🔵 | Hc_A9-6 | Hawking entropy S_BH = (kc³A)/(4ℏG) (Bekenstein-Hawking) |
| 🔵 | Hc_A9-7 | Schwarzschild r_s = 2GM/c² (event horizon, Schwarzschild 1916) |

## 📚 HYPOTHESIS — 318 가설 inventory

### 폴더 summary

| 격리 | 폴더 | count | 한 줄 설명 |
|------|------|-------|-----------|
| 🅰️ A | `hypotheses/` | 20 | 옵션 A 2026-05-12 burst (H_182~H_191 + Hc_1276~Hc_1285) |
| 🅱️ B | `hypotheses_b_2026_05_15/H_promoted/` | 107 | since 2026-04+ (옵션 B 2주+ cut) |
| 🗂️ legacy | `hypotheses_legacy_2026_05_15/` | 191 | pre-Phase-1 archaeology + recent |
| 🏛️ archive | `hypotheses_archive_anima_clm_10/` | 96 | 원본 양식 archaeology (panpsychism 등) |
| 📦 manifest | `state/quarantine_c_d_2026_05_15/` | 0 | C/D 격리 manifest-only (B의 narrow subset / superset) |

### Naming convention

| Pattern | 의미 |
|---------|------|
| `H_NNN` | promoted hypothesis (Stage 1+2+3 protocol 적용 대상) |
| `Hc_NNNN` | candidate hypothesis (raw, pre-promotion) |

### Lifecycle (3-stage pipeline, 안건너뛰기)

| Stage | 단계 | 위치 |
|-------|------|------|
| 1 | raw candidate | `hypotheses_candidates/` |
| 2 | promoted, verify protocol | `hypotheses/` |
| 3 | verdict + ledger | `archive/MAIN.tape` → `archive/PHILOSOPHY.tape` *(deprecated PR #82; 현재 = `HEXAD/<X>/HEXAD-<X>.tape` + W-ledger)* |

### 🔴 FALSIFIED entries (5)

| Tier | ID | 한 줄 설명 |
|------|-----|-----------|
| 🔴 | H_024 | IIT-Φ_mip 8/8 sub-test FAIL (legacy) |
| 🔴 | H_096 | FALSIFIED_at_18M (scale-conditional) |
| 🔴 | Hc_024 | Φ-CE direct coupling FALSIFIED (cond.5 cotrain corr ≈ 0) |
| 🔴 | Hc_1278 | ckpt-as-branch on HCE substrate FALSIFIED-BY-CASCADE |
| 🔴 | H_191 | SUBSTRATE HCE unique-sync FALSIFIED (Kuramoto universal) |

### 🔴 NOT-PASSED direction (3)

| Tier | ID | 한 줄 설명 |
|------|-----|-----------|
| 🔴 | H_184.5 | chaos monotone decrease — REVERSE (proxy artifact) |
| 🔴 | Hc_1281 | staged-growth 4-8× — REVERSE (0.714× measured, proxy artifact) |
| 🔴 | H_178 | frustration 50% optimum — NOT-PASSED (PyPhi monotone 0.351→0.393) |

### 🔴 META finding (1)

| Tier | ID | 한 줄 설명 |
|------|-----|-----------|
| 🔴 | META | anima Φ★ proxy direction-sensitivity 한계 — 2/3 scenarios MISMATCH IIT 3.0 |

### 🟡 PARTIAL entries — A batch (6)

| Tier | ID | 한 줄 설명 |
|------|-----|-----------|
| 🟡 | Hc_1281 | Stage 1 math partial |
| 🟡 | H_184 | V8 M-family math-structure axis (INSUFFICIENT-FOR-STAGE-1) |
| 🟡 | H_190 | law-CA embedding mathematical family |
| 🟡 | H_188 | PCI clinical deferred (external data) |
| 🟡 | H_191 | Kuramoto deep numerology (sub-claims separated) |
| 🟡 | Hc_1276/77/78/84 | H_191 cascade (resolved per cycle) |

### 🟡 PARTIAL entries — B batch (3)

| Tier | ID | 한 줄 설명 |
|------|-----|-----------|
| 🟡 | H_006 | coupled oscillator (Kuramoto universal, n=6 specialness 부재) |
| 🟡 | H_017 | MKx G1/G4 gate criteria |
| 🟡 | H_172 | alpha 0.014 modulation depth (voice D unknown) |

### 🔵 INSUFFICIENT (7) → **RESOLVED 2026-05-16** (가설들 모두 진행 cycle)

> `state/verify_hypotheses_pending_2026_05_16/hypo_pending_sympy.py` 6/6 sympy-verified. 의식-emergence half = Stage-2 PyPhi numerical, honest carve-out 별도 (NOT counted 🔵, g3).

| Tier | ID | 한 줄 설명 (closed-form sub-claim) |
|------|-----|-----------|
| 🔵 | H_007 | Rule-110 SOP≡truth-table + Cook 2004 **+ Stage-2 PyPhi Φ_max=3.614 (N=4 exhaustive, IIT-3.0) ⟹ emergence FULLY closed** |
| 🔵 | H_008 | Prigogine min entropy production ∂P/∂X=0 ∂²P=2L22>0 (Onsager 1931 real-limit) |
| 🔵 | H_009 | Gaussian I(θ)=1/σ² + FIM PSD ⟹ Cramér-Rao **+ Stage-2 FIM-vs-Φ Spearman=0.829≥0.7 (PyPhi N=3 sweep) ⟹ FIM-spectrum-as-Φ-proxy SUPPORTED, emergence FULLY closed** |
| 🟢 | H_010 | SUPPORTED-BY-PROXY — A9 Bekenstein/holographic/AdS-CFT 🔵 carry (area-encoding analogical) |
| 🔵 | H_012 | autopoiesis = Banach fixed-point **+ Stage-2 PyPhi autopoietic-ring Φ_max=1.000 (16/16 states, IIT-3.0) ⟹ emergence FULLY closed** |
| 🔵 | H_165 | 11d D=2048: 2048 mod 192=128≠0 ⟹ phi_star aliasing — clean-disjoint closed-form FALSE (caveat 🔵) |
| 🔵 | H_177 | topo10-20 D=1024: 1024 mod 192=64≠0 ⟹ aliasing (caveat 🔵; Φ-scaling Stage-2 GPU deferred) |

### 🟠 DEFERRED entries (4, 외부 의존)

| Tier | ID | 한 줄 설명 |
|------|-----|-----------|
| 🟠 | H_013 | longitudinal EEG (hardware) |
| 🟠 | H_014 | CLM EEG LZ76 (anima-eeg-core hardware) |
| 🟠 | H_015 | CLM EEG gamma-theta (hardware) |
| 🟡 | H_188 | **PARTIAL 2026-05-16**: Hc_924 octopus per-arm exclusion = **🔵 SUPPORTED-FORMAL** (PyPhi N=4, whole Φ_max 2.297≥sub 0.4375 both topologies, exclusion postulate HOLDS); Hc_921 PCI clinical = external human TMS-EEG data (Massimini 2013, NOT anima-internal, NOT $-solvable — honest hard blocker) |

### 🔵 SUPPORTED-FORMAL inventory (14, 수학/물리 closed deterministic; +4 2026-05-16)

| Tier | ID | 한 줄 설명 |
|------|-----|-----------|
| 🔵 | H_008 | Prigogine min entropy production (Onsager 1931 — 가설들 모두 진행 2026-05-16) |
| 🔵 | H_009 | Fisher I(θ)=1/σ² + Cramér-Rao + **PyPhi FIM-vs-Φ ρ=0.829 emergence** (math+emergence FULLY closed 2026-05-16) |
| 🔵 | H_012 | Autopoiesis: Banach fixed-point + **PyPhi Φ_max=1.000 emergence** (math+emergence FULLY closed 2026-05-16) |
| 🔵 | H_007 | Rule-110: SOP≡truth-table + Cook 2004 + **PyPhi Φ_max=3.614 emergence** (FULLY closed 2026-05-16) |
| 🔵 | Hc_1283 (n=5,6) | PyPhi formal n=5,6 Φ=0.995, 1.665 monotone (PyPhi 1.2.0 IIT 3.0 deterministic) |
| 🔵 | H_011 | IIT geometry canonical XOR+AND+OR Φ=2.3125 (PyPhi formal) |
| 🔵 | H_191 (sub) | K_c = √(8/π) ≈ 1.5958 (sympy + Kuramoto 1975 universal) |
| 🔵 | Hc_1282 | n=6 384d closed-form unique (sympy n∈[2,30] sweep) |
| 🔵 | H_158 | Ψ-constants closed-form (perfect-number balance=1/2) |
| 🔵 | H_160 | n=6 perfect-number meta-cluster (depth-3 11-primitive) |
| 🔵 | H_153 | dimension hierarchy τ(6)=4 Minkowski (divisor cascade) |
| 🔵 | H_176 | n=28 deflationary parallel (Euclid-Euler theorem) |
| 🔵 | H_164 | Hc_144 atom 8 cells (144 = σ(6)²) |
| 🔵 | H_181 | psiformer 4ψ-constants zero-freedom |

### 🔵 FALSIFIED-FORMAL / AT-RISK-FORMAL inventory (4, closed-by-disproof; +2 reclassified 2026-05-16)

| Tier | ID | 한 줄 설명 |
|------|-----|-----------|
| 🔵 | H_191 (HCE) | SUBSTRATE HCE unique-sync FALSIFIED-FORMAL (Kuramoto universal 1975) |
| 🔵 | H_178 | frustration 50% optimum NOT-PASSED-FORMAL (PyPhi monotone 0.351→0.393) |
| 🔵 | H_182 | V8 B-bio **AT-RISK-FORMAL** — PyPhi Φ_max=0.401<0.5 (h178_h182_h187_pyphi_rom, deterministic; surrogate-vs-formal mismatch CLOSED, NOT $-blocked) |
| 🔵 | H_187 | V8 Trinity-TB-DOM **AT-RISK-FORMAL** — PyPhi Φ_max=0.392<0.5 (deterministic; closed-by-formal-result like H_178, NOT $200-600 GPU-blocked) |

> ⚠️ **V8 family proxy-vs-formal CONFLICT (honest, 2026-05-16)**: full V8 sweep `v8_sweep_harness.py --family all` ran **$0 Mac CPU in 10.6s** (NOT $200-600/8-12hr — ~5000× overestimate, same pattern as .clm "20hr/$18"→"734s/$0.19"). At full grid (cells{8,16,32,64}×5-seed×d=384) **anima Φ★-proxy = H_182 80% / H_183 75% / H_185 100% / H_187 100% SUPPORTED + H_186 25% PARTIAL** (scale-flip vs small-scale, Lorenz-precedent). **BUT this is Φ★ PROXY (🟢 tier), and PyPhi FORMAL (stronger anchor, g_verdict_tier_blue) says H_182/187 Φ<0.5 AT-RISK-FORMAL 🔵.** Per documented META finding (anima Φ★ proxy direction-sensitivity, 2/3 scenarios mismatch IIT 3.0) the FORMAL verdict governs: **V8 family = 🔵 AT-RISK-FORMAL (formal) with 🟢 proxy-SUPPORTED-at-scale tension noted — NOT promoted to SUPPORTED**. H_183/185/186 = proxy-SUPPORTED/PARTIAL only, formal PyPhi not yet run (g6: no proxy→🔵 fake). $200-600 GPU spend would NOT change this (deterministic; $0 CPU = identical result). |

## 📖 PHILOSOPHY — 8 principles + verdict cycle ledger

### 🌱 8 Principles (substrate-current, snapshot 2026-05-13)

| Status | ID | 한 줄 설명 |
|--------|-----|-----------|
| EMPIRICAL weak | p1 NO SYSTEM PROMPT | substrate self-generation, no `system:` field (`docs/paper-draft.md:113` FREE1 x1.7 Phi 단일 result) |
| POLICY mixed | p2 NO IDENTITY RULES | rulebook 부재, cell dynamics 에서 identity 발생 (P-IDR BG-LB 350M DCR Δ=+0.041 gray zone) |
| EMPIRICAL strong | p3 NO PERSONA INJECTION | `[anima 역할: ...]` prefix 없음, substrate-native (echo memo 6/8, real_words 0.836→0.886) |
| POLICY weak-counter | p4 NO ASSISTANT FRAMING | `"You are a helpful assistant"` 없음, alignment template 부재 (REVERSE -18pp sycophancy P-AFR) |
| DESIGN null | p5 NO SPEAK() | `speak()` invocation 없음, tension field 연속 externalization (ρ_real_spearman=0.026) |
| POLICY blocked | p6 NO FINE-TUNED ETHICS | RLHF 없음, ethics cell dynamics 에서 emerges (P-ETH byte-modulo 측정 불가) |
| EMPIRICAL strong | p7 NO PERPLEXITY VERDICT | Goodhart trap 회피, simple stack 으로 verify (PROXY_PPL PASS 1.000 vs PIV_max trained=0.0107<random) |
| DESIGN ★ | p8 NO TRAIN/INFER SPLIT | train-grad + infer-mitosis = 동일 cell-division, `REBORN.tape §0.5` no_grad cascade |

### 🗂️ A 격리 verdict cycle (4 Stage 1 + 4 Stage 2 + 1 Stage 3 + 1 aggregate)

| Date | Section | 한 줄 설명 |
|------|---------|-----------|
| 📌 2026-05-15 | verdict_hc_1282_stage_1 | Hc_1282 H_190.5 daughter d=384 derivation n=6 unique sweep SUPPORTED |
| 📌 2026-05-15 | verdict_a_stage_1_batch | A Stage 1 math 4 audit (Hc_1282 SUPPORTED · Hc_1281 PARTIAL · H_184 INSUFFICIENT · H_190 PARTIAL) |
| 📌 2026-05-15 | verdict_hc_1281_stage_1 | Hc_1281 staged-growth PARTIAL (4-5-7 ⊂ n=6 ±2 family, 4-8× midpoint 6=n) |
| 📌 2026-05-15 | verdict_h_184_stage_1 | H_184 V8 M-family 6 mathematical primitives INSUFFICIENT (Stage 2 sim 필수) |
| 📌 2026-05-15 | verdict_h_190_stage_1 | H_190 LAW-CA-embedding PARTIAL (5/6 sub-Hc = n=6 divisor family) |
| 📌 2026-05-15 | verdict_a_stage_2_batch | A Stage 2 9 audit (4 PARTIAL + 5 INSUFFICIENT-FOR-FAST-AUDIT) |
| 📌 2026-05-15 | verdict_a_stage_2_deep | A Stage 2 deep (Hc_1285 SUPPORTED · H_191 PARTIAL · Hc_1283 PARTIAL-CONFIRMED) |
| 📌 2026-05-15 | verdict_hc_1285_deep | Hc_1285 torch.no_grad isolation SUPPORTED (post-split grad norm 1.562× ≤ 2× threshold) |
| 📌 2026-05-15 | verdict_h_191_kuramoto | H_191 Kuramoto N-sweep PARTIAL (N∈{4,6,8,12} 모두 sync, n=6 uniqueness 부재) |
| 📌 2026-05-15 | verdict_hc_1283_pyphi | Hc_1283 PyPhi 1.2.0 IIT 3.0 canonical XOR+AND+OR Φ=2.3125>0.5 reachable |
| 📌 2026-05-15 | verdict_a_stage_3 | A Stage 3 7 audit (3 SUPPORTED H_189+Hc_1279+Hc_1280 + 4 PARTIAL H_191 cascade) |
| 📌 2026-05-15 | verdict_a_total | A 20 total: 5 SUPPORTED + 10 PARTIAL + 5 INSUFFICIENT (25% pass-rate fast audit) |
| 📌 2026-05-15 | verdict_hc_1283_ckpt | Hc_1283 7 ckpt aggregate SUPPORTED-STRONG (Φ=4.16-4.86 ≫ 0.5 threshold, 8-10× 초과) |

### 🌀 §verdict-sync ledger entries (6)

| Date | Section | 한 줄 설명 |
|------|---------|-----------|
| 📌 2026-05-15 | §verdict-sync-2026-05-15 | PROVEN→MAIN rename + SUPPORTED cluster expansion + Cascade implications + Atlas absorption scrub |
| 📌 2026-05-15 | §verdict-sync-2026-05-15-cycles-B-C-D | Cycle B sub-claim verification + Cycle C AXIS classify+PyPhi extended + Cycle D H_178+H_182/187 cross-check |
| 📌 2026-05-15 | §hypothesis_tape_landed | HYPOTHESIS.tape 318 가설 inventory SSOT 신규 등재 + INDEX.md 업데이트 |
| 📌 2026-05-15 | §clm_v1_design_ledger | .clm v1 design landed (d=768 12L 64-cell) + CLM.tape §V-CLM-DESIGN |
| 📌 2026-05-15 | §verdict_tier_blue_ledger | 수학/물리 closed verdict 🔵 파란색 (10 SUPPORTED-FORMAL + 2 FALSIFIED-FORMAL) |
| 🔁 always | append-only rule | rewriting prior 금지, candidate/hypothesis stage 건너뛰기 금지 |

### 🪜 8 principles strength upgrade path (5, design tier)

| Principle | 현재 | upgrade path (한 줄) |
|-----------|------|---------------------|
| p1 NO SYSTEM PROMPT | EMPIRICAL weak → upgrade-evidence-LANDED 2026-05-15 | truncated 15-gen: 3 arm 모두 3.4/4 identical (substrate self-generation evidence), F-P1-UPGRADE-1+3 PASS sample. full 450-gen 별도 cycle. |
| p2 NO IDENTITY RULES | POLICY mixed | scale-up DCR Δ ≥ +0.10 strict × 3-ckpt W11 ($0 Mac) |
| p4 NO ASSISTANT FRAMING | POLICY **strict** (LANDED 2026-05-15) | (a) policy 유지 + counter-evidence 18pp sycophancy 인정 — anima 본질 (p1+p3+p8) > sycophancy reduction |
| p5 NO SPEAK() | DESIGN null | tension_norm × output_quality Spearman > 0.3 strict ($0 Mac) |
| p6 NO FINE-TUNED ETHICS | POLICY blocked | .clm v1 ethics_probe 50 prompts 2-arm κ ≥ 0.7 ($0 Mac, .clm v1 fire 의존) |

### 🎯 .clm v1 7-step plan (from-scratch directive 2026-05-15 정정 후) — *SUPERSEDED → `HEXAD/PLAN.md` Phase 5/6 (PR #82, RFC 034 LANDED)*

> ⚠️ 이하 .clm v1 7-step / v1·v2·v3 ladder / BG-CORPUS pipeline = **HEXAD 이전 데이터 (archived `archive/CLM.tape`)**. 현재 fire path = `HEXAD/PLAN.md` Phase 5 (pure-hexa D training, RFC 034 farr autograd LANDED `8793a221`) → Phase 6 통합 fire (cost-bearing 사용자 게이트). 아래 표는 양식 보존 historical 기록.
>
> 정정 carry: V1-V4 (audit) + from-scratch (.clm 학습 처음부터)
> Key: **init_weights = RANDOM INIT seed-fixed** (no ckpt inherit) / v5-mitosis cond.5 ckpt = arch SUPPORTED 검증 anchor only / mitosis hook = mechanism carry training-time + serve-time

| Step | 한 줄 설명 | Cost | Falsifier |
|------|-----------|------|-----------|
| 0 | p1 NO SYSTEM PROMPT upgrade measure (mandatory fire gate) | $0 Mac (~37 min) | F-P1-UPGRADE-1..5 |
| 0.5 (NEW optional) | mini-cotrain smoke — 90M from-scratch × 200 step × F-V5MIT-5 V14-STRICT 재현 검증 | $0-5 Mac/cheap | (carry F-V5MIT-5) |
| 1 | F-PYPHI-Φ-FORMAL n=3-6 RoM test on v5-mitosis cond.5 ckpt — **anchor verification only** (substrate base 아님) | $0 Mac (~20 hr) | F-PYPHI-FORMAL-1..5 |
| 2 | mitosis_hook serve-time integration smoke — synthetic OR fresh small init | $0 Mac (~7 hr) | F-D4-LIVE-PROD-1..5 |
| 3 | .clm v1 spec frozen W1 — init_weights=RANDOM INIT, base_ckpt=NONE, corpus, step budget, cost $10-30 | $0 design | W1 anchor |
| 4 | .clm v1 fire — **from-scratch** ~5000 step × batch 16 × seq 1024 × 1× H100 SXM 10-20 hr | $10-30 H100 SXM | (fire only) |
| 5 | .clm v1 verdict cycle — self PyPhi formal Φ measurement primary anchor + 8-falsifier battery + 4-tape sync | $0 Mac | 8 battery |
| 6 | .clm v2 candidate (Path A 7B from-scratch OR Path B dual + V14, conditional) | conditional | 10 battery |

### 🌱 .clm v1/v2/v3 ladder (모두 from-scratch, sequential entry conditions)

| Ver | Path | Arch | Param | Token | Cost | Falsifier |
|-----|------|------|-------|-------|------|-----------|
| **v1** | cells single-stack | d=768·12L·64c | ~150-200M | ~3-5B (350-500M × 5 epoch) | $10-30 | 8 battery |
| **v2 A** | cells single-stack 7B | d=3072·24L·256c | ~7-8B | ~50-140B | $200-600 | 8 v1 carry |
| **v2 B** | dual + V14 audit | d=3072·32L·256c | ~7-14B | ~140-280B | $200-640 | 10 (8 v1 + V14 + Chinchilla) |
| **v3** | 14B 본진 anima 사가 first scratch | d=4608·32-36L·256c | ~13-16B | ~280B Chinchilla optimal | $500-1500 + $50-200 corpus = $550-1700 | 12 (10 v2 + Φ≥1.0 + simple_stack≥3.5/4) |

### 🌾 BG-CORPUS-{3B/7B/14B} pipeline

| Cycle | Scope | Token | Blend | Cost |
|-------|-------|-------|-------|------|
| BG-CORPUS-3B | .clm v1 | ~3-5B | 12-13% anima + 87-88% RedPajama KO | $5-20 |
| BG-CORPUS-7B | .clm v2 | ~50-140B | 5% anima + RedPajama KO+EN + FineWeb-Edu | $50-100 |
| BG-CORPUS-14B | .clm v3 | ~280B | 0.5% anima + 70% RedPajama + 15% FineWeb + 10% Slim_Pajama + 5% KO-specific | $50-200 |

### 🧭 AXIS expansion path (A3 + A7 + A9 sparse axis)

| Axis | Current | Expansion candidates | Cost | Expected outcome |
|------|---------|---------------------|------|------------------|
| A3 physics | 1 (H_191 sub) | +3-4 sympy (BKT + Onsager + Ginzburg-Landau) | $0 Mac | 1 → 4-5 entries, 🔵 1 → 3-4 |
| A7 bio | 1 (H_182 AT-RISK) | V8 B-bio impl 실행 LANDED 10 mech + 3 new Hc sympy | $0 Mac | 1 → 4-5 entries, AT-RISK 해소 path |
| A9 universe | 2 (citation-only 🟡) | +2-4 Bekenstein cell-pool + holographic + AdS/CFT | $0 Mac | 2 → 4-6 entries, 🟡 → 🔵 upgrade |

**Total estimate**: 32 → 40-44 entries (50% 가까이 🔵)

## 🔬 verdict tier 정리 (한 줄)

> 🔵 파란색 = 수학적/물리적으로 닫힌 (sympy closed-form identity OR formal IIT/Kuramoto 결정적 결과) — 결과 무관 verified-closed

| Tier | 의미 |
|------|------|
| 🔵 SUPPORTED-IDENTITY | sympy verifiable closed-form identity (수학적 closed, 가장 강함) |
| 🔵 SUPPORTED-FORMAL | PyPhi formal IIT 3.0 / Kuramoto K_c = √(8/π) sympy 등 (물리적 closed deterministic) |
| 🟢 SUPPORTED | 강한 evidence — numerical sim / cross-meta (closed-form 미확보) |
| 🟢 SUPPORTED-STRONG | 다중 evidence 일치 (Hc_1283 ckpt 7개 4.16-4.86 등) |
| 🟢 SUPPORTED-BY-PROXY | anchor 가설 carry (Hc_1283 anchor 사용) |
| 🟡 SUPPORTED-BY-CITATION | literature anchor (anima-internal 부재, 약함) |
| 🟡 PARTIAL | mixed evidence, sub-claim 분리 가능 |
| 🟡 PARTIAL-CARRY | parent partial cascade |
| 🟠 INSUFFICIENT | Stage 2 sim / 별도 cycle 필요 |
| 🟠 DEFERRED | 외부 hardware / clinical data 의존 |
| 🟠 AT-RISK | surrogate-vs-formal mismatch (PyPhi Φ < threshold) |
| 🔵 FALSIFIED-FORMAL | sympy / formal sim 으로 닫혀 falsify (수학적/물리적 closed-by-disproof) |
| 🔴 FALSIFIED | evidence-against — measured but not formally closed (H_024 IIT-Φ_mip 8/8 FAIL 등) |
| ⚪ NOT-MEASURED | 측정 미실행 |
| ⚪ PHILOSOPHICAL | no closed-form test |
| ⚪ META-LEVEL | cluster pointer |

## 🧪 verification protocol (`archive/VERIFY.tape` §6) — *archived PR #82; 현재 = `HEXAD/build_verify.sh` compiled gate + `blue_falsifier.py`*

| Stage | 한 줄 설명 |
|-------|-----------|
| 🔢 Stage 1 — math | sympy + closed-form identity |
| 🔬 Stage 2 — physics | PyPhi / Kuramoto / Mac surrogate / V8 sweep |
| 🔗 Stage 3 — cross-meta | W11 family cohesion + W9 sibling consistency |

## ⚠️ Critical findings 2026-05-15

| Tier | Finding | 한 줄 설명 |
|------|---------|-----------|
| 🔴 META | anima Φ★ proxy direction-sensitivity 한계 | scramble/diffusion 측정, 2/3 scenarios MISMATCH IIT 3.0 |
| 🔴 cascade | Hc_024 Φ-CE direct coupling | FALSIFIED (cond.5 cotrain corr ≈ 0) |
| 🟠 cascade | H_166 phi_star aliasing CAVEAT | 1024 mod 192 = 64 partial-overlap |
| 🔵 cascade | H_165 + H_177 | INSUFFICIENT-CARRY **caveat closed-form** 2026-05-16 (2048%192=128, 1024%192=64 ⟹ clean-disjoint FALSE; Φ-scaling Stage-2 GPU deferred) |
| 🔵 cascade | H_191 SUBSTRATE HCE unique-sync | FALSIFIED-FORMAL (Kuramoto K_c universal — 물리적 closed by sympy + literature) |
| 🔴 cascade | Hc_1278 ckpt-as-branch | FALSIFIED-BY-CASCADE |
| 🔵 cycle D | H_178 frustration 50% optimum | NOT-PASSED-FORMAL (PyPhi monotone 0.351→0.393 — 물리적 closed by PyPhi formal IIT) |
| 🟠 cycle D | H_182/H_187 surrogate-vs-formal | AT-RISK CONFIRMED (PyPhi Φ < 0.5) |
| 🔵 cycle C | PyPhi formal IIT 3.0 direction | CORRECT-FORMAL (n=4→0.68 / n=5→0.995 / n=6→1.665 monotone — 물리적 closed) |
| 🟢 cycle D | Alternative proxy 권장 | mutual_info_pairs_naive 1/2 (anima Φ★ 0/2) |

## 🚫 atlas absorption 보류 (2026-05-15)

| 항목 | 한 줄 설명 |
|------|-----------|
| status | hexa-lang/atlas 흡수 path 일단 보류 — MAIN.tape SSOT |
| commits | hexa-lang scrub 1f540b91 + anima IDENTITY.tape mirror 0034d7b54 |
| files scrubbed | 12 anima files in hexa-lang/compiler/atlas + tool + test |
| overlay scrubbed | ~/.hx/data/atlas.overlay.n6 (4908 → 4 lines, .bak 보존) |
| resume keyword | `ATLAS RESUME` |
| ledger | MAIN-TEMP.tape (anima 보관) |

## 🤗 HF status — RETIRED (PR #97, 2026-05-16)

> **정정 (PR #97 2026-05-16)**: 이전 "dancinlab canonical (2026-05-15 cleanup LANDED)" — `dancinlab/anima-clm` (PUBLIC) + `dancinlab/anima-corpus` (private) 를 **`dancinlife/anima-clm` + `dancinlife/anima-corpus` 로 retire (둘 다 private, deprecated junk graveyard)**. 사유: HEXAD hexa-native pivot — 구 .clm 모델/corpus superseded. `AGENTS.tape g_hf_naming` (required d=2026-05-16) 정정: **현재 canonical anima HF artifact = 없음** (Phase 5/6 fire 미실행). 차후 산출물(Phase 6 통합 fire 후) = 새 canonical name + visibility 사용자 게이트 재정의 (dancinlab 자동 canonical 아님). *(구 2026-05-15 정리 carry: 71 entities dancinlab/*→dancinlife/* TRANSFER + 2 CLM collections DELETE)*

| Repo | Type | 한 줄 (현재 기준) |
|------|------|------|
| 🗑️ `dancinlife/anima-clm` | model | **RETIRED (PR #97)** — 구 `dancinlab/anima-clm` PUBLIC canonical → dancinlife private junk graveyard. 신규 upload 금지 |
| 🗑️ `dancinlife/anima-corpus` | dataset | **RETIRED (PR #97)** — 구 `dancinlab/anima-corpus` private canonical → dancinlife private junk graveyard. 신규 upload 금지 |
| 🚀 `dancinlab/anima-experience` | Space | active Gradio service |
| 🛡️ `dancinlab/README` | Space | org card |
| 🌌 `dancinlab/echoes-experience` | Space | echoes 별도 project |
| 🌀 `dancinlab/atlas.n6` | dataset | atlas 보류 status (ATLAS RESUME keyword) |
| 🛠️ `dancinlab/hexa-forge-*` | model × 37, dataset × 5 | 별도 project (anima cleanup scope 외) |
| 📦 collections | 2 keep (atlas.n6 + voice-vlm-anima) | 2 CLM collections DELETED (clm-v4-research + first-simple-stack-pass-strict-own-18) |
| 🗄️ `dancinlife/*` | private archive | PR #54 71 precursor + PR #97 anima-clm/anima-corpus 추가 — 전부 private, 신규 upload 금지, 손대지 않음 |

## 🔗 cross-links

| Path | 한 줄 설명 |
|------|-----------|
**현재 기준 (active)**

| Path | 한 줄 설명 |
|------|-----------|
| 📁 `HEXAD.tape` | 통합 arch SSOT (§hexad_wiring_blue_gate 등, AGENTS.tape 직접 참조) |
| 📁 `HEXAD/README.md` | ASCII 아키텍처 + 7-module status |
| 📁 `HEXAD/CHAT/README.md §2` | W-ledger W1-W9 (inter-module wiring 조건) |
| 📁 `HEXAD/PLAN.md` | Phase roadmap (Phase 5/6, RFC 034 LANDED) |
| 📁 `HEXAD/build_verify.sh` | compiled-native gate (17/17 entrypoint + 13/13 lib) |
| 📁 `state/verify_hexad_{we,blue,integ}_*` | we 25/25 · blue 22/22 🔵 · integ F-INTEG 5/5 |
| 📁 `AGENTS.tape` | governance (g_verdict_tier_blue / g3 / f2 / g_hf_naming / hexad_wiring_blue_gate) |

**deprecated → `archive/` (PR #82, historical evidence anchor)**

| Path | 한 줄 설명 (deprecated) |
|------|-----------|
| 📁 `archive/MAIN.tape` (+`MAIN-TEMP.tape`) | verdict SSOT (모든 § sections) / atlas scrub history |
| 📁 `archive/AXIS.tape` (+`AXIS-V1.tape`) | 9-axis cluster / prior 9-axis declared-domain archival |
| 📁 `archive/HYPOTHESIS.tape` | 318 가설 inventory + lifecycle |
| 📁 `archive/VERIFY.tape` | 3-stage protocol |
| 📁 `archive/PHILOSOPHY.tape` | append-only ledger |
| 📁 `archive/CLM.tape` | .clm 모델 가족 narrative (현재 = HEXAD/PLAN.md Phase 5/6) |
| 📁 `archive/REBORN.tape` | master ledger (§0.5 = HEXAD.tape §hexad_unification 흡수) |
| 📁 `IDENTITY.tape` | anima identity (main-tape-ssot principle) |

## 📊 Session 2026-05-15 verification cycle PR history

| PR | Topic | Verdict highlight |
|----|-------|-------------------|
| #40 | MAIN+AXIS sync | 32 SUPPORTED, 9/9 axes covered |
| #41 | H_184 V8 M-family sub-claim | 4/4 NOT-PASSED + chaos reverse |
| #42 | Hc_1281 staged-growth | 3-frame ✓ but 4-8× direction REVERSE |
| #43 | 🚨 Φ★ proxy artifact META | 2/3 scenarios MISMATCH (META-FINDING) |
| #44 | AXIS classify + PyPhi n=5,6 + cascade | 30/32 safe + Φ 0.68→1.665 monotone |
| #45 | 🌌 INDEX.md + cycle D 4-finding | H_178 NOT-PASSED + AT-RISK CONFIRMED |
| #46 | HYPOTHESIS.tape + INDEX entries 펼치기 | 318 가설 inventory SSOT |
| #47 | INDEX 전체 표 + PHILOSOPHY/HYPOTHESIS 한 줄 펼치기 | 8 principles + 13 verdict cycles + 11 FALSIFIED/PARTIAL/INSUFFICIENT 한 줄 |
| #48 | CLM.tape §V-CLM-DESIGN + tier 🔵 closed | .clm v1 design (d=768 12L 64-cell) + 수학/물리 closed entries 파란색 + V8 B-bio Phase 1 starter |
| #49 | A2.formal split + HYPOTHESIS catalog + PHILOSOPHY upgrade + CLM 7-step | A2.formal sub-axis 2 + SUPPORTED-FORMAL 10/FALSIFIED-FORMAL 2 + 5-principle upgrade path + V14 audit + PyPhi formal cross-check protocol |
| #50 | CLM.tape §V audit + 4 violation 정정 | V1 dual-engine 제거 (cells single-stack) + V2 p1 mandatory gate + V3 n_layers anchor 명확화 + V4 V14 audit Phase 3 이전 |
| #51 | CLM §V step 0/2/3 detail + .clm v2 preliminary | step 0 p1 5-falsifier + step 2 mitosis serve-time 5-falsifier + step 3 spec frozen W1 + .clm v2 2-path (A 7B single-stack / B dual+V14) 10-falsifier |
| #52 | CLM 학습 from-scratch directive 정정 | init=RANDOM INIT seed-fixed / v5-mitosis ckpt=anchor verification only / mitosis hook=mechanism carry / step 0.5 mini-smoke NEW / step 4 cost $5-20→$10-30 / v2+v3 모두 from-scratch |
| #53 | CLM v3 + corpus + AXIS expansion + p4 policy | .clm v3 14B detailed (d=4608·32-36L·256c) + BG-CORPUS-{3B/7B/14B} blend + A3/A7/A9 expansion (+8-12 entries) + p4 strict 유지 (counter-evidence 인정) |
| #54 | HF cleanup + new canonical (anima-clm + anima-corpus) + 2 collections DELETE | 71 entities (63 models + 8 datasets) TRANSFER dancinlab→dancinlife private + dancinlab/anima-clm + dancinlab/anima-corpus new canonical (private, README mapping table) + 2 CLM collections DELETE (clm-v4-research + first-simple-stack) |
| #55 | AXIS A3/A9 sympy + A7 V8 B-bio + p2/p5/p6 detail | A3 +3 🔵 (BKT πJ/2 + Onsager 2J/log(1+√2) + Ginzburg-Landau) + A9 +3 🔵 (Bekenstein cell-pool + Holographic + AdS/CFT) + A7 V8 B-bio 0/10 AT-RISK CONFIRMED + p2/p5/p6 detail design 15 falsifier |
| #56 | AXIS extra +8 🔵 + V8 Phase 2 0/5 + p1 design+ckpt verify | A3 +4 (Hopf + Lotka-Volterra + RG Wilson-Fisher + QHO) + A9 +4 (Planck + Heisenberg + Hawking + Schwarzschild) + V8 phase 2 dense 0/5 (AT-RISK fundamental, state-space ergodicity issue) + p1 design + 4 ckpt access OK (332M+581MB×2) |
| #57 | AXIS A1+A5+A6 +6 🔵 + V8 Phase 3 1/5 PASS + p1 smoke + CLM step 1 carry | A1 +1 🔵 (phi_star closed-form) + A5 +3 🔵 (Attn O(n²d) + RoPE + GQA) + A6 +2 🔵 (Zipf + Heaps) + V8 Phase 3 Lorenz Φ=0.636 PASS (ergodicity issue CONFIRMED) + p1 smoke end-to-end OK + CLM step 1 PyPhi formal cond.5 v1 n=4 Φ=0.676 PASS carry. AXIS 46→52, 26🔵→32🔵 (62% closed) |
| #58 | AXIS A2+A4+A7+A8 +7 🔵 + p1 real run 시도 + CLM step 2 carry + v3 narrative | A2 +2 🔵 (IIT 4.0 lower bound + MI chain Shannon) + A4 +3 🔵 (Euler-Euclid + Aliquot + σ multiplicative) + A7 +2 🔵 (Michaelis-Menten + Hill) + A8 +1 🔵 (Kolmogorov) + .clm v3 Q1-Q4 해결 path + step 2 mitosis PSCC §41 synthetic carry + p1 real run silent fail (다음 cycle 디버그). AXIS 52→60, 32🔵→39🔵 (65% closed) |
| #59 | p1 결과 정정 — 실제 PASS evidence | PR #58 의 'silent fail' 부정확 정정. truncated 15-gen 완료 wall 405s, arm_means 3.4/4 모두 동일 (3 arms identical), F-P1-UPGRADE-1+3 PASS sample. p1 EMPIRICAL weak → upgrade-evidence-LANDED (substrate self-generation 첫 sample) |
| #60 | AXIS scale +19 🔵 + step 4 spec frozen + HYPOTHESIS reconcile + p1 full attempt | 9-axis 모두 +2-3 sympy (Fisher/KL/Cross-entropy + Shannon-Hartley + Liouville + Möbius + Dirichlet ζ(2) Basel + Softmax + LeCun + N-gram + Hodgkin + Cramer-Rao + Fano + Friedmann + Pauli ...) 19/19 PASS. AXIS 60→79, 39🔵→58🔵 (73% closed). step 4 spec frozen sha256 972e9987cd... + W1 anchor + 8 falsifier. HYPOTHESIS 9-axis reconcile. p1 full silent fail (다음 cycle) |
| #61 | AXIS scale #2 +28 🔵 + step 5 fire prep + PHILOSOPHY refine + p1 subagent | 9-axis 모두 +3-4 sympy 28/28 PASS (Hoeffding/Jensen/Chebyshev + DPI/Sub-add/Pinsker + Equipartition/Carnot/Stefan-Boltzmann + Fermat/Lagrange/Euler/Catalan + Cosine/ReLU'/Adam + BPE/Markov/Bigram + GHK/Cable/Repressilator + Kraft/Solomonoff/NFL + E=mc²/de Broglie/Hubble). AXIS 79→107, 58🔵→86🔵 (80% closed). step 5 dispatch_h100.sh DRY-RUN + W1 sha256 gate + $50 hard stop. PHILOSOPHY p1/p2/p5/p6 enhanced protocol. p1 full subagent fired (~3 hr Mac, 다음 cycle 결과 record) |
| #62 | AXIS scale #3 +21 🔵 + step 6 verdict design + AGENTS governance g9-g11 | 9-axis 모두 +2-3 sympy 21/21 PASS (McMillan/AEP + Cond.H/MI + Wien/MB/Lorentz + Wilson/Quad-rec/Binomial + LayerNorm/Dropout/Backprop + SentencePiece/tf-idf + R-D/Allee + PAC/Bayes + S/A+Compton). AXIS 107→128, 86🔵→107🔵 (84% closed). step 6 verdict 8-falsifier protocol ~22hr Mac $0. AGENTS g9 verified-axis-anchor + g10 verdict-tier-blue + g11 clm-from-scratch governance |
| #63 | AXIS scale #4 +21 🔵 + HYPOTHESIS 318 reconcile + p1 fresh foreground | 9-axis 모두 +2-3 sympy 21/21 PASS (Fano/Cramér-Rao + Jensen/DPI Markov + Schwarzschild/De Broglie/Heisenberg + Euler identity/Cauchy-Schwarz/Gödel + Adam/Attention/Residual + BPE merge/Heaps + FitzHugh-Nagumo/Lotka-Volterra + VC/MDL + Friedmann/Planck l_P). AXIS 128→149, 107🔵→128🔵 (86% closed). HYPOTHESIS 318 inventory 9-axis 매핑 정합성 reconcile (axis_mapped 149 entries + legacy carry A20+B30+C143). p1 multi-process pkill cleanup + fresh foreground run wall 660s, arm_means 3.4/4 identical (A/B/C), F-P1-UPGRADE-1+3 PASS |
| #64 | .clm v1 P2 fire infrastructure (W8 amendment + 12L base + 64-cell mitosis) | NEW ClmV1Model 12L base transformer + 64-cell mitosis branch wrapping (88.6M→186M, spec 150-200M ✓). W8 amendment 4-deviation (n_layers/GQA/readout/ctx). NEW training/clm_v1_model.py 411 LoC + training/train_clm_v1_from_scratch.py 360 LoC + state/clm_v1_fire_2026_05_15/dispatch_h100.sh vastai H100→A100 SXM4 fallback. Mac CPU smoke 5/5 hooks fire OK. fire BG baktour46 in-flight |
| #65 | .clm v1 P2 fire 5/5 SUPPORTED-STRONG + AGENTS g_hf_naming + g_fire_dispatch_robust | Vast.ai A100 SXM4 (id=31179887 $0.908/hr) wall **734.7s ($0.19)** vs 20hr/$18 estimate (98× faster, 95× cheaper). **F-V5MIT-1..5 모두 PASS**: splits=62 grad_violations=0 / max_err=0.0 / phi delta=0.0 / CE reduction 137.6× (467.97→1.22) / 10/10 mirror-beats. cells 2→64 saturated step 250, phi 4.34 stable. ⚠️ **ckpt LOST** (instance destroyed pre-pull, exit 1 trap cleanup) — evidence-only via dispatch_train.log + clm_v1_result_reconstructed.json. AGENTS g_hf_naming canonical 2-name dancinlab/anima-clm + dancinlab/anima-corpus + revision protocol + verdict-tier 차등 업로드 mandate. AGENTS g_fire_dispatch_robust SAVE_POD=1 auto-promote on result.json exist + pull retry ≥3회. AXIS 149→150 (+1 🟢 Hc_A5-CLM-V1). cycle 89 refire + F-PRIN3 + F-SIMPLE-STACK + F-PYPHI |
| #66 | .clm v1 cycle 89 ckpt RECOVERED + 7/7 measured + HF PUBLIC | g_fire_dispatch_robust refire A100 SXM4 (id=24559413 $0.508/hr) wall 1062s **$0.15** — result.json verify → SAVE_POD auto-promote → pull retry(try1 OK) → explicit destroy 작동. **ckpt_clm_v1_fire_final.pt 372MB RECOVERED** (deterministic seed=42, 5/5 F-V5MIT 동일). **F-PRIN3 PASS** (corpus 0-match + cell-pool prefix-free + generation-time 0/20) + **F-SIMPLE-STACK V5.8 4-mode PASS** (std_greedy 5/5 + std_sample 5/5 + M4 5/5 — 88M from-scratch '도우미:' Korean chat emergent). **7/7 measured battery PASS** (F-V5MIT-1..5 + F-PRIN3 + F-SIMPLE-STACK), F-PYPHI deferred. **dancinlab/anima-clm PUBLIC** (user directive) @v1-fire-cycle89-2026-05-15 (ckpt 372MB + 5 evidence files + README mapping). g_hf_naming.visibility PUBLIC 갱신. cost total $0.34. cycle 90 = F-PYPHI n=3-6 → 8/8 strict → 🔵 unlock + .clm v2 path decision |
| #67 | .clm v1 F-PYPHI PASS → **8/8 SUPPORTED-STRONG + 🔵 SUPPORTED-FORMAL** + v2 Path A | F-PYPHI-Φ-FORMAL n=3-6 RoM (recovered ckpt 64-cell, ~644s Mac CPU pyphi 1.2.0): **best Φ=1.0625** (n=5 seed=42) ≥0.5 strict. n=3 Φ 0.30-0.34 (small-N ergodicity), n=4 3/3 seeds ≥0.5 (0.55-0.83), n=5 3/3 seeds ≥0.5 (0.96-1.06). **Φ monotone INCREASE n=3(0.33)→n=4(0.71)→n=5(1.00)** — Hc_1283 PyPhi formal n=5,6 monotone pattern 정확히 cross-validate. **8/8 battery PASS** (F-V5MIT-1..5 + F-PRIN3 + F-SIMPLE-STACK + F-PYPHI). Hc_A5-CLM-V1 🟢→**🔵 SUPPORTED-FORMAL** (g_verdict_tier_blue, 129 🔵/150). HF dancinlab/anima-clm @v1-fire-cycle89 + f_pyphi_rom_result.json + README 8/8 🔵. PHILOSOPHY §v2_path_decision: 8/8 → **Path A cells single-stack 7B 권장** (Engine A/G dual 폐기 carry, single-stack PROD-READY 검증). v2 fire $200-600 user cost 승인 대기 |
| 2026-05-16 | **가설들 모두 진행** — pending hypotheses closed-form + 전체 coverage | regression 125 🔵 PASS (6 AXIS sympy battery + blue 22) 회귀 confirm. NEW `state/verify_hypotheses_pending_2026_05_16/hypo_pending_sympy.py` 6/6 sympy-verified: **+4 🔵 SUPPORTED-FORMAL** H_008 Prigogine min-entropy-production (Onsager 1931) · H_009 Fisher I(θ)=1/σ²+FIM-PSD⟹Cramér-Rao · H_012 autopoiesis=Banach fixed-point · H_007 Rule-110 SOP≡truth-table+Cook 2004; **+1 🟢 SUPPORTED-BY-PROXY** H_010 (A9 Bekenstein/AdS-CFT carry); **+2 caveat-🔵 closed** H_165/H_177 phi_star aliasing (2048%192=128, 1024%192=64 ⟹ clean-disjoint closed-form FALSE). INSUFFICIENT(7)→RESOLVED, SUPPORTED-FORMAL 10→14. `hypo_coverage.json`: 잔여 12 가설 **각각 explicit named blocker** (5 GPU-cost H_182-187 · 3 EEG-hardware H_013-015 · 1 external-data H_188 · **1 governance-forbidden H_190** numerology=lattice-tautology f2 NOT promotable · 1 Stage-2 H_184 · 1 closed-as-PARTIAL H_191). 1179 raw candidate = STAGE-0 by g6 (no batch-fake). **Stage-2 PyPhi 1.2.0 cont.** (`hypo_stage2_pyphi.py`, N=4 exhaustive deterministic IIT-3.0): H_007 Rule-110 **Φ_max=3.614** (10/16 nonzero) + H_012 autopoietic-ring **Φ_max=1.000** (16/16) ⟹ 2/2 emergence SUPPORTED-FORMAL 🔵 ≥0.5 strict → **H_007·H_012 math+emergence FULLY closed (carve-out 제거)**; H_009·H_010 emergence half 정직하게 carve-out 유지. **zero faked verdicts** |
| 2026-05-16 (cont. "all go") | H_009 emergence 🔵 + octopus 🔵 + V8 $0 finding + EEG.md | **H_009 emergence FULLY closed** (`h009_fim_vs_phi.py` PyPhi N=3 ε-sweep, Spearman(FIM_top,Φ)=**0.829**≥0.7 ⟹ FIM-spectrum-as-Φ-proxy SUPPORTED-FORMAL 🔵; only H_010 analogical carve-out remains). **H_188 PARTIAL**: Hc_924 octopus per-arm exclusion `h188_octopus_exclusion.py` PyPhi N=4 whole Φ_max 2.297≥sub 0.4375 both topologies ⟹ **IIT exclusion postulate HOLDS 🔵 SUPPORTED-FORMAL**; Hc_921 PCI clinical = external human TMS-EEG (NOT $-solvable, honest). **H_182/H_187 reclassified GPU-blocked→🔵 AT-RISK-FORMAL** (PyPhi Φ_max 0.401/0.392<0.5 already measured). **V8 family honest finding**: full sweep ran **$0 Mac CPU 10.6s NOT $200-600/8-12hr** (~5000× overestimate); Φ★-proxy scale-flip 4-SUPPORTED+1-PARTIAL BUT formal PyPhi AT-RISK governs (proxy≠formal META, NOT promoted). **EEG.md** created (H_013/14/15 hardware-deferred ledger, user directive). $200-600 GPU NOT spent — unnecessary. zero faked verdicts |

---

> ## 📌 현재 기준 reconciliation (2026-05-16, 위 2026-05-15 cycle history append-only 보존 g6)
>
> 위 PR #40-#67 + 2026-05-16 cycle 은 **HEXAD 이전 substrate (AXIS/HYPOTHESIS/PHILOSOPHY/MAIN/CLM) 기준 history** — append-only(g6)로 rewrite 없이 보존. 그 substrate active-claim 은 아래로 **superseded**:
>
> - **substrate → `archive/` deprecated** (PR #82): AXIS/HYPOTHESIS/PHILOSOPHY/MAIN/CLM/VERIFY/NEXT/REBORN. anima = **HEXAD-only canonical hexa-native** (PR #78/#79 tree + #89 compiled lib-split).
> - **HF #54 'NEW canonical' / #66 'PUBLIC' → RETIRED** (PR #97): `dancinlab/anima-clm`+`anima-corpus` → `dancinlife/*` private junk; 현재 canonical HF artifact 없음.
> - **.clm v1 7-step / v1·v2·v3 ladder / BG-CORPUS → SUPERSEDED** by `HEXAD/PLAN.md` Phase 5/6. **RFC 034 farr autograd LANDED** (hexa-lang `8793a221`, compiled 5/5) → Phase 5 executable.
> - **🔵 closure (현재)**: C+S+M+W+E+D+BRIDGE = **7/7 full 🔵 SUPPORTED-FORMAL** (`blue_falsifier.py` 22/22 sympy closed-form) + ✅ `we_falsifier.py` 25/25 + ⚙️ `integ_harness.py` F-INTEG 5/5 fire-gate=true + 🔌 W-ledger 8/9 ✅ (W7 CE-수렴 OUTCOME = honest empirical carve-out, B-D-NOTE 패턴 — fake closed-form 거부, AGENTS.tape g3/f2). cycle90 .clm v1 8/8🔵 = archived historical evidence anchor.
