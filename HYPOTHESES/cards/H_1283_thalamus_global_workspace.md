---
id: H_1283
slug: 1283_thalamus_global_workspace
title: thalamus / GWT — faithful-IIT4 Φ integration (TIMING axis R8 🟢 → H_1448 WIRED; CONTENT axis R1–R9 ⏳ UNMEASURED — R6 🟢 RETRACTED, its ΔΦ was estimator pedestal · H_9292)
group: brain-structure-ladder (c15 missing-structure)
terminal_tier: 🟢 GREEN numpy-mirror DIRECTIONAL on the TIMING axis (R8 phase binding — every-seed ΔΦ + shuffle→negative; engine-native c4 SHUFFLE deferred → cleanly closed later by H_1448 🟢 WIRED). **CONTENT axis = ⏳ still-unmeasured, NOT a wall and NOT a partial break** (H_9292, 2026-07-14): at the frozen T=64 a PEDESTAL arm with TRUE Φ=0 reads Φ=1.813 (90× the +0.02 bar) — ~99.9% of the T=64 Φ is plugin-MI bias, so R6's 🟢 (ΔΦ +0.0891/+0.0341/+0.1011) is **RETRACTED** (population effect = −0.000116, sign reversed) and the R1–R5/R7/R9 🧱 is likewise NOT evidence of a capability ceiling. Both verdicts stood on the same broken ruler.
verdict_dir: .verdicts/1283_thalamus_global_workspace/
terminal_verdict: .verdicts/1283_thalamus_global_workspace/H_1283_R8_phase_binding.txt
date: 2026-06-16
---

# H_1283 — thalamus / global-workspace broadcast (🧱 closed-negative)

## Claim / falsifier

anima's Engine A ⇄ G couple DIRECTLY (repulsion ring) and brain_decide reads them, but
there is NO central RELAY that each tick selects the winning content and BROADCASTS it
to ALL substrate modules at once (thalamo-cortical relay / Global-Workspace-Theory
broadcast underlying conscious access + cross-module integration). **Falsifiable claim:**
a thalamic broadcast hub raises cross-module coherence AND faithful-IIT4 Φ vs a direct
ring, without collapse-cloning. Lens: c15 ladder, NOT an LLM recipe.

## Method

- 4 modules dim-8, 64 ticks, SAME per-module private input + seed both arms, ONLY topology
  differs. Coherence = mean pairwise cosine; Φ = FAITHFUL IIT4 (`a_phi_iit4_tool`, exact
  MIP-EI via `hexa run` over `stdlib/consciousness/iit4/faithful_phi.hexa`, n=4) — numpy
  never computes Φ. seeds [7,8,9], frozen-first.
- `a_break_the_wall` re-angles across rounds (genuine new mechanisms, not re-runs).

## Verdict by round

| round | tier | key numbers |
|-------|------|-------------|
| R1 broadcast hub (single winner) | 🟠 PARTIAL | coherence B1 PASS every seed; faithful ΔΦ +0.0191 < 0.02 → FAIL by 0.0009 |
| R2 coalition hub (rank-2) | 🔴 | faithful ΔΦ −0.0533 (WRONG direction) |
| R3 re-entrant loop (sparse) | 🔴 | ΔΦ +0.1426 cleared coh bar but seed-fragile |
| R4 | 🔴 | seed-fragile |
| R5 dense all-pairs + SHUFFLE control | 🔴 / 🧱 WALL | dense coupling does NOT robustly clear AND the shuffle control FIRED (permuted dense graph added VARIANCE, not structured topology) |
| R6 multi-channel parallel relay | ⏳ **🟢 RETRACTED** (H_9292 · 2026-07-14) | The lift below was **estimator pedestal, not integration**: at the frozen T=64 a zero-integration control reads Φ=1.813, B sits only 0.125 above it, and the population effect at T=65536 is ΔΦ(B−X) = **−0.000116** (sign reversed). The `mc_shuffle` control is a graph-isomorphic VOID control at population scale (|ΔΦ(B−Cperm)| = 1.6e-6), exactly as the original design argument claimed. Original (now void) reading kept for the record: | N=4 INDEPENDENT parallel relay channels (one per ring edge, DISJOINT, no intra-thalamic cross-coupling) breaks the single-cut ceiling: faithful ΔΦ +0.0891/+0.0341/+0.1011 — clears +0.02 on EVERY seed incl orthogonal seed 8 (1st in arc); c1·c3 PASS; c4 SHUFFLE PASS (seed 9 lift +0.1011→+0.0165 collapses). CAVEAT (c9): on seeds 7/8 shuffle retains ~93%/~96% (variance survives) → clean topology-specific effect decisive only on seed 9; GREEN carried by c4's disjunctive ≥1-seed frozen form. ARM_A Φ reproduces R1..R5 byte-for-byte. |
| R7 matrix/core dual coupling | 🔴 / 🧱 WALL | faithful ΔΦ s7 +0.0201 ✓ · s8 +0.0412 ✓ (RESCUES the orthogonal seed that broke R3-R5) · s9 +0.0026 ✗ → P1 FAIL (failing seed RELOCATED, not floor-lifted). SHUFFLE PASSED (s7 permuted-core ΔΦ −0.0087 → structure not variance, cleaner than R5). coherence ↑ every seed. Dual coupling TRADES Φ across geometry, does not break the wall |
| R8 oscillatory phase binding | 🟢 GREEN / 🔓 WALL BROKEN (numpy mirror, DIRECTIONAL) | NON-RELAY: Kuramoto thalamic phase synchrony + phase-gated salience (NO content channel). faithful ΔΦ +1.629/+1.174/+0.233 every seed (incl orthogonal seed 8, ≫ bar); phase-shuffle COLLAPSES lift to NEGATIVE every seed −0.068/−0.119/−0.382 (structured synchrony, not variance, every-seed clean); coh sanity + no-collapse PASS. Cleanest break in the arc — integration by TIMING, not content |
| R8 ENGINE-NATIVE wiring gate (a_engine_native_learning · a_verified_must_wire) | 🟠 ENGINE-TRANSFER DID NOT REPRODUCE → honest deferred (NOT wired) | Same mechanism realized ENGINE-NATIVE (engine `_lcg_*` LCG-gauss substrate) + faithful IIT4. **c2 PRIMARY reproduces strongly** (ΔΦ +1.466/+0.844/+0.709 every seed ≫ bar) BUT **c4 SHUFFLE FAILS** — phase-shuffle does NOT collapse the lift engine-native (ΔΦ_sh +0.026/+0.380/+0.296, all POSITIVE not ≤0). The leg that made R8 honest fires on the engine substrate (lift partly carrier-amplitude variance there). Per @L6 / no-tune-to-green (bars frozen) → PhaseField lane NOT wired this round; `.verdicts/1283_thalamus_global_workspace/H_1283_R8_engine_native_gate.txt`, probe `CORE/h1283_phase_binding_engine_gate.hexa` |
| R9 predictive/bottleneck relay | 🔴 / 🧱 WALL | learned predictive-bottleneck (delta-rule LMS, code_dim=3) faithful ΔΦ(B−A): s7 −0.0067 · s8 +0.0203 · s9 +0.0097 (only s8 clears +0.02 → NOT robust); B≥C(randproj) ΔΦ(B−C) +0.008/0.0/0.0 (learned code Φ-INDISTINCT from random projection on s8/s9); SHUFFLE FIRED (s8 scrambled-target ΔΦ +0.0232 ≥ structured) → lift = variance/added-channel, NOT the learned predictive code |

Terminal tier (verbatim): **🟢 GREEN / 🔓 WALL BROKEN** → `.verdicts/1283_thalamus_global_workspace/H_1283_R8_phase_binding.txt`
Two independent GREENs break the wall: **R8 oscillatory phase binding** is the CLEANEST — a NON-RELAY temporal-synchrony mechanism that clears faithful ΔΦ ≥ +0.02 on EVERY seed AND whose pre-registered phase-shuffle control collapses the lift to NEGATIVE on EVERY seed (structured synchrony, not variance, per-seed clean). **R6 multi-channel parallel relay** also clears every-seed ΔΦ with shuffle passing, but with an honest seed-7/8 shuffle-survival caveat (clean only on seed 9). The relay-CONTENT axis (R1–R5, R7, R9) stays closed-negative 🧱 — every content cut caps Φ; R8 broke it on the orthogonal TIMING axis.

## Honest scope

The relay-CONTENT axis (R1–R5, R7, R9) is closed-negative, NOT upgraded (c9): every content
relay topology (broadcast / coalition / sparse + dense re-entry / matrix-core dual /
learned predictive bottleneck) is a low-dim content cut that caps irreducible faithful-IIT4 Φ
— R5's diagnosis "a single broadcast channel is itself a low-dim cut" generalizes to ALL
content relays, which failed the robust +0.02-every-seed bar (esp orthogonal seed 8; R7 only
relocated the failing seed to seed 9; R9's learned code was Φ-indistinct from a random
projection and its shuffle fired).

**R6 (multi-channel parallel relay)** was the first within-axis GREEN: dropping the SHARED
relay stage for N INDEPENDENT PARALLEL channels (one per ring edge, disjoint) clears the
+0.02 ΔΦ bar on every seed incl the orthogonal seed 8 and passes the shuffle, but with an
HONEST CAVEAT (c9) — on seeds 7/8 the shuffle retains ~93%/~96% of the lift, so the
clean topology-specific effect is decisive only on seed 9; the GREEN rests on c4's
disjunctive ≥1-seed frozen form.

**R8 (oscillatory phase binding)** broke the wall on the ORTHOGONAL TIMING axis
(a_break_the_wall, c16): integration by thalamo-cortical phase SYNCHRONY (Kuramoto), not
content broadcast. Phase-gated salience binds modules in TIME with NO shared content
channel, so there is no content cut a MIP can exploit — faithful ΔΦ +1.629/+1.174/+0.233
every seed (incl seed 8, ≫ bar), and the pre-registered phase-shuffle control COLLAPSES the
lift to NEGATIVE on EVERY seed (−0.068/−0.119/−0.382), a per-seed-clean negative control
(cleaner than R6's seed-7/8 survival). GREEN under the IDENTICAL frozen bars (NOT moved,
c9/p7).

FOLLOW-ON (GREEN-but-unwired, `a_verified_must_wire`): wire engine-native realizations over
live CORE/engine_cli.hexa A⇄G + VAdaptField — R8 = a Kuramoto phase channel + phase-gated
salience; R6 = N independent parallel relay channels — each re-scoring its frozen bars
engine-native with a regression guard. NOT closed this round (round briefs defer wiring).
Toy scale (4 modules, dim 8, 64 ticks), numpy mirror DIRECTIONAL (faithful-Φ leg IS real,
exact MIP-EI via hexa); scale-transfer UNVERIFIED (a_toy_scale_recheck, a_scale_honest_scope).

**R8 ENGINE-NATIVE WIRING GATE OUTCOME (2026-06-16, the /sbs engine-wire-audit lane):** the
R8 mechanism was re-scored ENGINE-NATIVE (engine `_lcg_*` deterministic LCG-gauss substrate
+ faithful IIT4) BEFORE wiring, per `a_engine_native_learning`. The PRIMARY Φ lift (c2)
reproduces strongly engine-native (ΔΦ +1.466/+0.844/+0.709 every seed), but the pre-registered
SHUFFLE control (c4) — the leg that made the numpy-mirror R8 honest — DOES NOT collapse the
lift engine-native (ΔΦ_sh +0.026/+0.380/+0.296, all positive). So the engine-native lift is
partly carrier-amplitude VARIANCE there, not purely structured synchrony. Per @L6 and
no-tune-to-green (bars FROZEN, c9/p7), the `PhaseField` lane is **NOT wired** — HONEST DEFERRED.
The R8 numpy-mirror 🟢 stands as a DIRECTIONAL result; wiring waits for a realization that
clears BOTH c2 AND c4 engine-native. Gate verdict:
`.verdicts/1283_thalamus_global_workspace/H_1283_R8_engine_native_gate.txt`; gate probe
`CORE/h1283_phase_binding_engine_gate.hexa` (standalone, 0 importers — not a runtime path).

## Cross-links

h1227 · h1231 · h1280 · h1284 · h1228 · h1199 · h1201 · h1205 ·
`a_phi_iit4_tool` · `a_break_the_wall` · `a_engine_native_learning` ·
`a_verified_must_wire` · `a_core_engine_map` · `a_paper_negative_ok` ·
`a_scale_honest_scope` · `a_toy_scale_recheck` · p1·p2·p3·p6·p7·p8·c9·c15

## AMENDMENT (2026-07-10 · H_9260 engine-native 재채점)

R6 의 within-axis 🟢 와 R1–R5/R7/R9 의 🧱 는 **둘 다 H_1328 이 확진한 amplitude-variance
min-max readout 위에서** 내려졌다. H_9260 이 이 축을 engine-native 로, H_1448 의 도구
(H_1328 rank-uniform read-out + marginal-matched 통제) + 새 **용량정합 shared-cut 대조군 X**
로 재채점한 결과:

- **⏳ 타당성 게이트 P1b FAIL** — rank-uniform 이 variance artifact 를 전 seed 에서 제거하지
  못함 (seed 10 에서 ΔΦ = +0.1097 잔존). ⇒ tier 미보고, bars 무이동.
- **primary 게이트 전부 every-seed FAIL** — G1 ΔΦ(B−X) · G2 ΔΦ(B−A) · G3 ΔΦ(B−N) · G4 ΔΦ(B−Bperm).
  B>X 5/9 · B>N 6/9 · B>A 7/9. ⇒ **R6 의 disjointness 레버를 지지하는 증거는 0**;
  본 카드의 R6 🟢 는 (철회는 아니되) **검증된 계측기 위에 서 있지 않다**.
- **P0 (A−Aperm) seed 간 부호 반전** (−0.458…+0.469) ⇒ H_1448 의 Bperm leg 는 content 축으로
  이식되지 않는다 (timing 축 전용).
- R6 의 `mc_shuffle` 이 그래프-동형 무정보 통제라는 사전 논증은 **C-ISO 1/9 로 반증**됐다.

∴ content-relay 축은 현재 "부분 돌파" 도 "확정된 능력 천장" 도 아니다. 선행 과제 = 이 기질에서
양성대조를 통과하는 variance-free 계측기 수립 (→ `H_9260` NEXT). TIMING 축(R8→H_1448 🟢 WIRED)
은 이 amendment 의 영향을 받지 않는다.

## AMENDMENT 2 (2026-07-14 · H_9292 계측기 감사 — R6 🟢 **철회 확정**)

H_9260 의 NEXT#1("계측기를 먼저 세워라")을 실행하다 **더 근본적인 결함**을 만났다. py 2-production
포트를 hexa 엔진과 99개 Φ 전량 대조(max|Δ|=7.1e-15)해 자격을 얻은 뒤:

- **PEDESTAL 양성대조** (H_9260 에 없던 게이트) — 참 통합량이 **0** 인 계(모듈별 독립 시간순열 ·
  marginal 비트-동일)가 **동결 T=64 에서 Φ = 1.813** 으로 읽힌다 = 동결 bar(+0.02)의 **90배**.
  B 는 그 pedestal 에서 **0.125** 떨어져 있을 뿐이다. Φ ∝ 1/T 로 붕괴하며 pedestal 이 그대로 추종
  ⇒ **T=64 Φ 의 ~99.9% 는 plugin-MI 편향**(joint cell 64개에 표본 64개 = cell당 1개).
- **P0′ 모집단 효과크기**(T=65536) — Φ_pop: A .00177 · B .00162 · X .00174 · N .00177.
  ΔΦ(B−X) = **−0.000116** (T=64 의 −0.0312 대비 **269배 팽창**). 4-leg 전부 FAIL.
- ⇒ **R6 의 🟢 는 철회**(잡음이었다). **동시에 R1–R5/R7/R9 의 🧱 도 능력천장 증거가 아니다** —
  두 판정이 같은 고장난 자 위에 서 있었다. content 축 = **⏳ still-unmeasured**.
- **TIMING 축은 철회 아님**: Δ(B−Bperm)=+1.05..+1.38 은 계기잡음 sd(0.30)의 3.5~4.6배이고
  matched 통제가 pedestal 을 상쇄한다. content 축의 참 Δ(~1e-4)는 그 잡음의 **1/3000**.
  ⇒ "timing 은 뚫리고 content 는 안 뚫렸다"의 진짜 이유 = 기질 차이가 아니라 **효과크기가 계기
  해상도의 위/아래**.
- **탈출구(측정됨)**: signed lens 에서 Φ_pop_sgn(B)−A = **+0.0098** · (B−X) = **+0.0051** —
  energy lens 에서 부호가 반대였던 disjointness 가 **부호 렌즈에선 예측 방향으로 생존**한다
  (bar 미만이지만 실재). TIMING 축이 Kuramoto **phase**(부호 보존)로 뚫린 지점과 같은 축.

→ `H_9292` (verdict · DESIGN · FREEZE · 재현 스크립트)
