# 🌌 anima — verification SSOT INDEX

> MAIN.tape + AXIS.tape + HYPOTHESIS.tape + PHILOSOPHY.tape 통합 index (2026-05-15)

## 🟢 핵심 4 tape

| Tape | 한 줄 설명 |
|------|-----------|
| **MAIN.tape** 🎯 | 가설 verdict 4-class (SUPPORTED / PARTIAL / INSUFFICIENT / FALSIFIED) SSOT |
| **AXIS.tape** 🧭 | MAIN.tape의 SUPPORTED-tier 만 9-axis 재구성 (32 entries, 9/9 axes covered) |
| **HYPOTHESIS.tape** 📚 | 318 가설 file inventory + naming convention + lifecycle pipeline SSOT |
| **PHILOSOPHY.tape** 📖 | anima 철학 + verdict cycle 진행 append-only ledger |

## 🧭 AXIS — 9-axis 32 SUPPORTED entries (각 한 줄)

### A1 substrate (3)
- 🟢 H_005 corpus quality > scale (Phase 1A.6 121MB CLEAN, V5.8 std_greedy 4/5)
- 🟢 H_174 phi_star aliasing CLM-v4-specific (D=192 multiple only clean)
- 🟢 Hc_1285 torch.no_grad backward-graph isolation (PyTorch ratio 1.562×)

### A2 consciousness (5)
- 🟢 Hc_1283 anima Φ★ proxy ≥ 0.5 (v5-mitosis 7 ckpt Φ=4.16-4.86)
- 🟢 Hc_1283 PyPhi RoM n=4 (cell-pair correlation TPM Φ=0.61-0.68)
- 🟢 Hc_1283 PyPhi formal n=5,6 (Φ=0.995, 1.665 monotone INCREASE)
- 🟢 H_004 consciousness hard problem (Hc_1283 anchor)
- 🟢 H_011 IIT geometry (Φ ≫ 0.5 + canonical 2.3125)
- 🟢 H_162 phi-normalized anima IIT4 lower-bound (D=384 multiple ✓ clean)

### A3 physics (1)
- 🟢 H_191 sub K_c = √(8/π) ≈ 1.5958 Kuramoto mean-field (sympy + literature 1975)

### A4 math ⭐ (8, largest cluster)
- 🟢 Hc_1282 n=6 384d closed-form unique (sympy n∈[2,30] sweep)
- 🟢 H_158 Ψ-constants closed-form (perfect-number cluster balance=1/2)
- 🟢 H_160 n=6 perfect-number meta-cluster (depth-3 11-primitive vocabulary)
- 🟢 H_153 dimension hierarchy τ(6)=4 Minkowski (divisor cascade)
- 🟢 H_176 n=28 deflationary parallel (Euclid-Euler theorem, n=6 NOT unique)
- 🟢 H_173 DD21 log-ratio Φ scale-invariant (4/6 falsifier SUPPORTED)
- 🟢 H_164 Hc_144 atom 8 cells (144 = σ(6)² = 12²)
- 🟢 H_181 psiformer 4ψ-constants zero-freedom (Ψ-cluster carry)

### A5 architecture (6)
- 🟢 Hc_1285 torch.no_grad isolation (autograd)
- 🟢 H_166 topo20 hierarchical 8×128=1024 (algebra ✓, phi_star aliasing caveat)
- 🟢 H_019 self-evolution v4→v5 (cond.5 cotrain F-V5MIT 5/5 PASS)
- 🟢 H_174 phi_star aliasing CLM-v4-specific (cross-substrate Spearman 0.31)
- 🟢 H_191 sub TRAINING CPGD 0.95 (cond.5 cotrain 220× CE reduction)
- 🟢 Hc_1276 train-vs-infer cotrain ablation (cascade-from-CPGD)

### A6 corpus (2)
- 🟢 H_005 corpus quality > scale (Phase 1A.6)
- 🟢 H_016 AN11 translation ceiling (chat-v2 measurable)

### A7 bio (1, AT-RISK)
- 🟠 H_182 V8 B-family bio (surrogate 78.5%, PyPhi formal Φ=0.358<0.5)

### A8 meta (4)
- 🟢 H_189 Red-team adversarial robustness family (Stage 3 W11)
- 🟢 Hc_1279 Red-team family member
- 🟢 Hc_1280 Red-team family member
- 🟠 H_187 V8 Trinity-TB-DOM (surrogate 100%, PyPhi formal Φ=0.359<0.5 AT-RISK)

### A9 universe (2, citation-only)
- 🟡 H_002.H2.3 Bekenstein bound area scaling (Bekenstein 1981 + Maldacena 1997)
- 🟡 H_002.H2.1 anthropic Λ fine-tuning ~10^-120 (Weinberg 1987)

## 📚 HYPOTHESIS — 318 가설 inventory (각 폴더 한 줄)

- 🅰️ `hypotheses/` (A 격리, 20) — 옵션 A 2026-05-12 burst (H_182~H_191 + Hc_1276~Hc_1285)
- 🅱️ `hypotheses_b_2026_05_15/H_promoted/` (B 격리, 107) — since 2026-04+ (옵션 B 2주+ cut)
- 🗂️ `hypotheses_legacy_2026_05_15/` (legacy, 191) — pre-Phase-1 archaeology + recent
- 🏛️ `hypotheses_archive_anima_clm_10/` (archive, 96) — 원본 양식 archaeology (panpsychism 등)
- 📦 `state/quarantine_c_d_2026_05_15/` — C/D 격리 manifest-only (B 의 narrow subset / superset)

### Naming convention
- `H_NNN` = promoted hypothesis (Stage 1+2+3 protocol 적용 대상)
- `Hc_NNNN` = candidate hypothesis (raw, pre-promotion)

### Lifecycle (3-stage pipeline, 안건너뛰기)
1. `hypotheses_candidates/` (raw)
2. `hypotheses/` (promoted, verify protocol)
3. `MAIN.tape` (verdict) → `PHILOSOPHY.tape` (append-only ledger)

## 📖 PHILOSOPHY — verdict cycle ledger (각 cycle 한 줄)

- 📌 §verdict-sync-2026-05-15 — PROVEN→MAIN rename + 4-path BG cycle aggregate
- 📌 §verdict-sync-2026-05-15-cycles-B-C-D — sub-claim verification + META-finding + INDEX.md
- 🔁 append-only ledger (rewriting prior entries 금지, candidate/hypothesis stage 건너뛰기 금지)

## 🔬 verdict tier 정리 (한 줄)

| Tier | 의미 |
|------|------|
| 🟢 SUPPORTED | 강한 evidence — sympy identity / numerical sim / cross-meta |
| 🟢 SUPPORTED-IDENTITY | sympy verifiable closed-form identity (가장 강함) |
| 🟢 SUPPORTED-STRONG | 다중 evidence 일치 (Hc_1283 ckpt 7개 4.16-4.86 등) |
| 🟢 SUPPORTED-BY-PROXY | anchor 가설 carry (Hc_1283 anchor 사용) |
| 🟡 SUPPORTED-BY-CITATION | literature anchor (anima-internal 부재, 약함) |
| 🟡 PARTIAL | mixed evidence, sub-claim 분리 가능 |
| 🟡 PARTIAL-CARRY | parent partial cascade |
| 🟠 INSUFFICIENT | Stage 2 sim / 별도 cycle 필요 |
| 🟠 DEFERRED | 외부 hardware / clinical data 의존 |
| 🟠 AT-RISK | surrogate-vs-formal mismatch (PyPhi Φ < threshold) |
| 🔴 FALSIFIED | evidence-against (H_024 IIT-Φ_mip 8/8 FAIL 등) |
| ⚪ NOT-MEASURED | 측정 미실행 |
| ⚪ PHILOSOPHICAL | no closed-form test |
| ⚪ META-LEVEL | cluster pointer |

## 🧪 verification protocol (VERIFY.tape §6, 각 stage 한 줄)

- 🔢 **Stage 1 — math** (sympy + closed-form identity)
- 🔬 **Stage 2 — physics** (PyPhi / Kuramoto / Mac surrogate / V8 sweep)
- 🔗 **Stage 3 — cross-meta** (W11 family cohesion + W9 sibling consistency)

## ⚠️ Critical findings 2026-05-15

### 🔴 anima Φ★ proxy direction-sensitivity 한계 (META-FINDING)
- anima Φ★ = scramble/diffusion 측정 (IIT 3.0 integration 아님)
- 2/3 scenarios MISMATCH IIT direction
- magnitude-only 사용 OK (Hc_1283 anchor 유효), direction-sensitive 에 alt-proxy 필요

### 🔴 cascade FALSIFIED
- 🔴 Hc_024 Φ-CE direct coupling FALSIFIED (cond.5 corr ≈ 0)
- 🟠 H_166 phi_star aliasing CAVEAT (1024 mod 192 = 64)
- 🟠 H_165 + H_177 INSUFFICIENT-CARRY (D=2048/1024 aliasing)
- 🔴 H_191 SUBSTRATE HCE unique-sync FALSIFIED (Kuramoto universal)
- 🔴 Hc_1278 ckpt-as-branch FALSIFIED-BY-CASCADE

### 🟠 H_178 frustration 50% optimum NOT-PASSED (cycle D)
- PyPhi formal sweep: 0.351→0.355→0.389→0.393 monotone INCREASE
- HIGH risk cascade prediction validated

### 🟠 H_182/H_187 surrogate-vs-formal mismatch (cycle D)
- H_182 surrogate 78.5% PASS, PyPhi formal Φ=0.358 (<0.5)
- H_187 surrogate 100% PASS, PyPhi formal Φ=0.359 (<0.5)
- AT-RISK CONFIRMED

### 🟢 PyPhi formal IIT 3.0 direction CORRECT
- n=4 Φ=0.68 → n=5 Φ=0.995 → n=6 Φ=1.665 monotone INCREASE
- PyPhi 본체 = direction-correct, proxy 한계와 분리

### 🟢 Alternative proxy 권장
- mutual_info_pairs_naive: 1/2 IIT match (anima Φ★ 0/2)
- predictive_integrated_info_pc1_var: 1/2 IIT match
- direction-sensitive sub-claim 에 채택 권장

## 🚫 atlas absorption 보류 (2026-05-15)

- hexa-lang/atlas 흡수 path 일단 보류 — MAIN.tape 가 SSOT
- 12 anima files hexa-lang scrubbed (commit 1f540b91)
- MAIN-TEMP.tape (anima 보관) = scrub ledger
- resume keyword: `ATLAS RESUME`

## 🔗 cross-links

- 📁 `MAIN.tape` — verdict SSOT
- 📁 `AXIS.tape` — 9-axis cluster
- 📁 `AXIS-V1.tape` — prior 9-axis (declared-domain 기반, archival)
- 📁 `HYPOTHESIS.tape` — 318 가설 inventory + lifecycle
- 📁 `VERIFY.tape` — 3-stage protocol
- 📁 `PHILOSOPHY.tape` — append-only ledger
- 📁 `MAIN-TEMP.tape` — atlas scrub history
- 📁 `CLM.tape` — .clm 모델 가족 narrative
- 📁 `REBORN.tape` — master ledger
- 📁 `IDENTITY.tape` — anima identity (main-tape-ssot principle)

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
