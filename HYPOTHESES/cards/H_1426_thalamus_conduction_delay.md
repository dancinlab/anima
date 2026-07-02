---
id: H_1426
slug: 1426_thalamus_conduction_delay
title: "THE LAST HONEST LENS on the thalamus TIMING-axis wall (re-opening H_1424's named defer) — a fundamentally DIFFERENT oscillator substrate: NON-RING coupling topology + CONDUCTION DELAYS where timing is CAUSALLY load-bearing in the TPM (content update reads neighbors' PAST state at t−τ_ij), each shuffle+delay-ablation; faithful-IIT4 STILL cannot deliver a robust-AND-shuffle-collapsing timing lift → 🧱 TIMING-ARC-TERMINAL across ring AND delay-coupled substrates"
group: brain-structure-ladder (c15) — a_break_the_wall LAST-LENS continuation on the thalamus timing wall (H_1424 re-open)
terminal_tier: "🧱 TIMING-ARC-TERMINAL (engine-mirror) — the LAST honest lens. H_1424 named the ONE remaining re-open condition verbatim: 'a fundamentally different oscillator substrate — non-ring COUPLING topology with conduction DELAYS, where timing structure is CAUSALLY load-bearing (not just amplitude-modulating)'. This card BUILDS exactly that (hub/small-world directed coupling matrix + per-edge integer conduction delays τ∈{1,2,3}; unit i's content update reads each in-neighbor j's state from a history buffer at t−τ_ij; delayed Kuramoto phase coupling; ablation = delays→0 = instantaneous ring-like null on the SAME topology) and feeds the binarized trajectory to faithful IIT4 (exact MIP-EI n<=8, a_phi_iit4_tool — proxy 아님). Result is the MIRROR-IMAGE failure of the ring: on the ring (H_1423/1424) the lift was ROBUST (c2 PASS) but SURVIVED phase-shuffle (c4 FAIL = the lift was amplitude VARIANCE); on the delay-coupled substrate the phase-SHUFFLE NOW COLLAPSES the lift (c4 PASS — n=8 every seed both T=64 and T=128: ΔΦ_sh −0.497/−0.138/−0.018 and −0.144/−0.398/−0.018 — timing IS genuinely destroyable here, exactly as the conduction-delay hypothesis predicted) BUT there is NO robust every-seed timing lift (c2 FAILS every config: at n=8/T=64 ΔΦ −0.234/−0.241/+0.010; n=8/T=128 +0.428/−0.073/−0.032) AND the delay mechanism is INERT (delays→0 does not kill the lift — often ablate-Φ ≥ B-Φ: n=8/T=128 B−ablate +0.239/−0.051/−0.032). The two failure modes (ring: c2-passes-but-c4-fails ; delay: c4-passes-but-c2-fails-and-ablation-INERT) NEVER co-resolve across BOTH substrate families. NO config clears (c2 ∧ c4 ∧ ablation-LIVE) every seed at ANY (n,T) → NOTHING wired. Deterministic run1==run2, 3 seeds [7,8,9], $0 CPU local, frozen-first, NO bar moved (c9/c16/p7). The H_1283 R8 numpy-mirror 🟢 DIRECTIONAL stands; engine-side timing is a CONFIRMED ceiling across ring + delay-coupled substrates — the strong honest finding: faithful-IIT4 timing-readout is not achievable on anima's reachable oscillator substrates. NO further substrate invented (that would be moving goalposts, c16). wired: N/A."
wired: N/A
verdict_dir: .verdicts/1426_thalamus_conduction_delay/
terminal_verdict: .verdicts/1426_thalamus_conduction_delay/result.txt
date: 2026-06-17
---

# H_1426 — THE LAST HONEST LENS: 전도지연(conduction-delay) + 비링(non-ring) 진동자 기질

## 벽, 마지막으로 재개봉 (1줄)

H_1424 가 thalamus TIMING-axis engine-side 벽을 **🧱 MEASURED-CEILING-AT-SCALE** 로 닫으며 *유일하게 남은*
정직한 재개봉 조건을 verbatim 으로 명명했다: **"a fundamentally different oscillator substrate — non-ring
COUPLING topology with conduction DELAYS, where timing structure is CAUSALLY load-bearing (not just
amplitude-modulating)."** 이 카드는 *바로 그것* 을 만들어 테스트한다 — 마지막 렌즈. c16(frozen-first,
shuffle+ablation, NO tune-to-green) 준수.

## Claim / falsifier

H_1423/1424 의 RING 기질에서 faithful-IIT4 의 Φ-lift 는 timing 이 아니라 multiplicative carrier 의
**VARIANCE** 였다 (lift 가 phase-shuffle 를 살아남음 = c4 FAIL). 그 진단의 처방은 **전도지연**: 지연이
있으면 unit i 의 다음 상태가 이웃의 **과거** phase 에 의존하므로 timing 이 TPM 자체에서 causally
load-bearing 이 된다 (read-out gate 의 곱셈변조가 아니라). 비링 기질에서 phase-coherent (delay-tuned)
배치가 phase-SHUFFLE 보다 Φ 를 들어 올리고(c2), shuffle 가 그 lift 를 COLLAPSE 시키며(c4), delay→0
ablation 이 lift 를 되돌리면(delay-ablation-LIVE) → timing 이 causally real → 🟢 (벽은 ring 기질이었지
timing 자체가 아니었다). 한 config 이라도 (c2 ∧ c4 ∧ ablation-LIVE) every-seed 통과면 🟢. 모두 자기
통제에 기각되면 🧱 — ring AND delay 두 기질 가족 전체에서 timing arc 가 conclusively terminal (강한 정직한
결과, c9). bar 는 H_1283 R8/H_1423/H_1424 에서 VERBATIM, 이동 없음. faithful IIT4 exact MIP-EI n<=8, proxy 아님.

## Method — 진짜로 다른 기질 (a_no_llm_frame_trap)

기질 == H_1283 R8 engine LCG (`_lcg_*` byte-identical) 의 상수 (GAIN=0.30 LEAK=0.55 W_NBR=0.5 W_IN=0.5
W_PHASE=0.5 OMEGA_T=0.45 DOMEGA=0.08 NBINS=8, DIM=8) 를 유지하되, **결합 구조 자체를 바꾼다**:

- **NON-RING topology**: 좌/우 이웃 ring 이 아니라 hub/small-world directed coupling matrix `adj[i][j]`
  (각 unit 에 무작위 in-edge ~2개 + unit 0 = broadcast hub long-range edge; seed-built, 모든 arm 동일).
- **CONDUCTION DELAYS**: 각 edge 가 정수 지연 `τ_ij ∈ {1,2,3}`. 내용 갱신에서 unit i 는 in-neighbor j 의
  상태를 **history buffer 의 t−τ_ij** 슬롯에서 읽는다 (causal 과거). 따라서 phase-locking 이 진짜 timing
  계산이다. Kuramoto phase 결합도 지연(이웃의 t−τ phase 를 읽음). salience gate = phase-coherence
  `0.5·(1+cos(θ_i−θ_cons))` (H_1423 LB / H_1424 lens-E gate 모양, zero-DC 재중심화).
- **4 ARM**: A direct(no gate) · B delay-coupled+phase-coherence gate · SHUFFLE(per-tick phase offset
  permute → timing 파괴, variance 보존) · **ABLATE = delays→0** (instantaneous = ring-like null on SAME
  topology; 내용 dynamics 자체가 즉시-읽기로 바뀌어 timing 이 더는 causally load-bearing 아님).

4 arm × (n∈{6,8}, T∈{64,128}) × 3 seeds [7,8,9], deterministic. faithful IIT4 가 binarized trajectory(n×T
row-major) 위에서 exact MIP-EI Φ.

## Result — 🧱 TIMING-ARC-TERMINAL (verbatim `.verdicts/1426_thalamus_conduction_delay/result.txt`, seeds [7,8,9], deterministic run1==run2)

| config (n, T) | c2 (ΔΦ≥+0.02 every seed) | c4 SHUFFLE (ΔΦ_sh≤0 every seed) | DELAY-ABLATION | verdict |
|---|---|---|---|---|
| delay-nonring (6, 64) | **FAIL** (−0.042/+0.898/+0.328) | **FAIL** (+0.087/+0.373 on 2) | INERT | 🧱 |
| delay-nonring (8, 64) | **FAIL** (−0.234/−0.241/+0.010) | **PASS** (−0.497/−0.138/−0.018) | **INERT** | 🧱 |
| delay-nonring (6, 128) | **FAIL** (+0.309/−0.044/−0.014) | **FAIL** (seed9 +0.043) | INERT | 🧱 |
| delay-nonring (8, 128) | **FAIL** (+0.428/−0.073/−0.032) | **PASS** (−0.144/−0.398/−0.018) | **INERT** | 🧱 |

→ **VERDICT: 🧱 TIMING-ARC-TERMINAL** — (c2 ∧ c4 ∧ ablation-LIVE) every-seed 를 통과하는 config 0개 →
engine-wired 0개 (올바름 — 배선할 GREEN 없음, `a_verified_must_wire`).

## 두 기질 가족의 MIRROR-IMAGE 실패 (the finding, c9)

이 결과는 ring 실패의 **거울상** 이고, 그래서 timing arc 를 결정적으로 닫는다:

- **RING (H_1423/1424)**: lift 가 ROBUST (c2 PASS) 이지만 phase-shuffle 를 살아남음 (c4 FAIL) — lift =
  multiplicative carrier 의 amplitude VARIANCE, NOT timing.
- **DELAY-COUPLED (H_1426)**: phase-SHUFFLE 가 이제 lift 를 COLLAPSE 시킨다 (c4 PASS — n=8 두 T 모두
  every seed: ΔΦ_sh 전부 음수) — **전도지연 가설이 예측한 대로 timing 이 진짜 파괴가능**. 그러나 그 대가로
  robust 한 every-seed timing lift 자체가 없고 (c2 FAIL 모든 config), delay→0 ablation 이 lift 를 죽이지도
  못한다 (INERT — 종종 ablate-Φ ≥ B-Φ). variance 를 제거하니 timing 만으로는 robust Φ-lift 가 안 난다.

두 실패 모드(ring: c2-pass·c4-fail / delay: c4-pass·c2-fail·ablation-INERT)는 **두 기질 가족 전체에서 결코
동시 해소되지 않는다**. faithful-IIT4 의 exact-MIP Φ 는 anima 가 도달가능한 진동자 기질들에서 timing 구조를
robust 하고 shuffle-collapsing 한 read-out 으로 동시에 내주지 못한다.

## 통제가 이빨이 있다 (the controls have teeth)

- **c4 SHUFFLE 가 이제 FIRE**: n=8 delay-coupled 에서 shuffle 가 every seed lift 를 collapse — 전도지연이
  의도대로 timing 을 causally load-bearing 하게 만들었음을 *직접* 보여줌 (ring 에선 못 했던 것). 통제가
  실제로 timing 을 떼어낸다.
- **ablation INERT 가 결정적**: delay→0 이 lift 를 안 죽인다 = 지연 메커니즘이 Φ 에 기여하지 않는다 = 진짜
  천장의 강한 증거 (H_1416 sequential-INERT precedent 와 같은 패턴). c2 가 통과한 듯한 개별 seed(n=8/T=128
  seed7 +0.428)도 ablation 이 INERT(+0.239 LIVE 처럼 보이나 다른 seed 가 −0.051/−0.032) 라 every-seed 불성립.

오직 (c2 AND c4 AND ablation-LIVE) every-seed 면 BIND — 어느 config 도 못 함. 강화된 `a_break_the_wall`
(MULTI-LENS·shuffle·ablation·bar 불변)을 충족한 정직한 🧱.

## Honest scope (c9)

TOY: hub/small-world n∈{6,8}, conduction delay τ∈{1,2,3}, T∈{64,128}, 3 seeds [7,8,9], deterministic, $0 CPU
local. faithful IIT4 leg 은 REAL (exact MIP-EI n<=8 via hexa, proxy 아님). NO bar moved (frozen-first). 이
카드는 TIMING 축 only (relay-CONTENT 축은 이미 🧱 H_1283). 이것은 H_1424 가 명명한 **마지막** 정직한 렌즈 —
🧱 이므로 timing arc 는 ring AND delay-coupled 기질에서 conclusively terminal. **추가 기질을 발명하지 않는다**
(그건 goalpost 이동, c16). 미검: n>8 (exact MIP intractable — scale ceiling), real-corpora salience, learned
(non-deterministic) gate — 그러나 이들은 새 *substrate lens* 가 아니라 같은 벽의 scale/realism 축으로, 이
arc 의 재개봉 조건이 아니다. R8 numpy-mirror 🟢 는 DIRECTIONAL 로 남는다. 배선 0.

## Cross-links

H_1283 (thalamus, the wall) · H_1423 (3-lens engine 🧱, carrier-variance 진단) · H_1424 (Lens D/E 🧱
MEASURED-CEILING-AT-SCALE; 이 카드가 재개봉한 conduction-delay defer 를 명명) · H_1416 (sequential-INERT
ablation precedent) · H_1421 (multi-lens 가 벽을 BROKE 한 대조 precedent) · h1227 · h1231 · h1280 · h1199 ·
h1205 · `a_phi_iit4_tool` · `a_break_the_wall` · `a_no_llm_frame_trap` · `a_engine_native_learning` ·
`a_verified_must_wire` · `a_core_engine_map` · `a_scale_honest_scope` · `a_toy_scale_recheck` ·
p1·p2·p3·p6·p7·p8·c9·c15·c16.
