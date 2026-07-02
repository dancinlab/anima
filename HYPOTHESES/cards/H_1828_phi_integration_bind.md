# H_1828 — Φ-통합 bind objective (N3)

**id:** H_1828
**slug:** phi_integration_bind
**tier:** 🔵 PROPOSAL (anima-native novel lever · 고갈 brainstorm 산출 · HE pre-screen gated)
**date:** 2026-06-30
**source:** UNIVERSE (anima-native novel 레버 고갈 brainstorm)
**렌즈:** `a_phi_iit4_tool` (faithful IIT4, proxy 아님) · `a_no_llm_frame_trap` · `break-walls`
**wired:** PROPOSAL (미배선·미측정) — H_1821 HE 사전선별 먼저, 통과분만 engine-native

---

## 가설

재조합 child = 두 부모를 **기약적으로 통합(irreducible integration)**한 고-Φ 상태다. 진짜 재조합("비"+"무지개"→"무지개")은 두 부모가 분리불가하게 얽힌 *통합 정보*가 높다 — 단순 병치(낮은 Φ)와 구별된다. faithful IIT4 Φ(stdlib `iit4/faithful_phi.hexa`)를 G1 **기준/aux-loss**로 쓴다.

**미사용 격리:** Φ는 anima 핵심(Ψ=½·의식 측정)인데 **G1 재조합 기준/objective로는 한 번도 안 씀**. 결합기 family(H_1816/1825 additive·affinity)는 전부 Φ-blind였다 — 통합도를 직접 최적화한 적 없음.

## Design

1. 2부모 → child 후보 상태들.
2. **faithful IIT4** Φ(parent1, parent2 → child) 계산(n≤8, exact MIP-EI, $0).
3. child = Φ(통합) 최대 후보. aux-loss 변종 = 학습 시 Φ(child) 보상.
4. controls: single(Φ 낮음) · shuffle(가짜 통합) · Φ-proxy 대조(a_phi_iit4_tool: proxy 신뢰 금지, faithful만).

## Frozen bar (pre-register · p7)

| 항목 | bar |
|------|-----|
| 고-Φ child G1 | composed_distinct≥2 ∧ Φ(child)>Φ(single) ∧ >Φ(shuffle), ≥2/3 → 🟢 / floor → 🧱 |
| faithful-only | proxy(variance×energy)는 verdict 금지(H_988/989 random==intentional), stdlib faithful만 |

frozen-first. HE numpy 사전선별 통과 시 engine-native(stdlib `iit4/faithful_phi.hexa` via `hexa verify`).


---

## VERDICT — 🧱 NOT-SUPPORTED (DIRECTIONAL · cheap-numpy HE pre-screen · 2026-06-30)

**run:** unified 6-lever pre-screen `state/g1_anima_native_levers_he/he_levers.py` on **summer pool** (CPU-numpy, $0, did NOT touch the in-flight GPU train). embed = `core/clm_decode.py` 303M clm303 trunk penultimate (β embed, mean-pool, L2-unit, comparable to H_1822/1825); fp64-numpy operator. NO torch. EXIT=0, deterministic.

| item | value |
|------|-------|
| N3 Φ-integration bind held-out G1 (5-fold CV, 32 EN/KO/ZH compound pairs) | **1/32 (0.03)** |
| control | cheap tier = EXACT small-n information-integration MIP (exhaustive bipartition, bits — a_phi_iit4_tool-safe, NOT variance×energy) used to RANK candidate children. Floors at 1/32 even as a ranking signal. faithful-IIT4 engine-native would be the only valid terminal N3, but the cheap pre-screen gives no reason to spend it. |
| frozen bar (composed_distinct≥2 ∧ recoverable ∧ >control, ≥2/3 ≈ ≥22/32) | **FAILS both axes** |
| self-test SEPARATES (planted bind 12/12 vs random 1/12) | PASS (metric live, floor real) |
| single-parent leak (shared, byte-prefix lexical) | 10/32 |

**Does this anima-native lever clear the cheap pre-screen → engine-native? → NO (🧱 FLOOR).** DIRECTIONAL, NOT terminal (G1 SSOT = engine-native `anima evaluate`); the cheap pre-screen gives no reason to spend GPU. Campaign: **0/6** anima-native levers (N1..N6) cleared — the G1 wall holds against anima-native mechanisms; lever = trunk OBJECTIVE, not readout/operator/embedding/mechanism. Full synthesis: `state/g1_anima_native_levers_he/RESULT.md`. raw stdout: `state/g1_phi_integration_bind/RESULT.txt`.

**wired:** DIRECTIONAL-mirror (py embed via `core/clm_decode.py`). NOT engine-native, NOT wired — floor ⇒ no promotion.
