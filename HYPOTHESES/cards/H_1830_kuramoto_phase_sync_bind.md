# H_1830 — Kuramoto 위상-동기 bind (N5)

**id:** H_1830
**slug:** kuramoto_phase_sync_bind
**tier:** 🔵 PROPOSAL (anima-native novel lever · 고갈 brainstorm 산출 · HE pre-screen gated)
**date:** 2026-06-30
**source:** UNIVERSE (anima-native novel 레버 고갈 brainstorm)
**렌즈:** `a_no_llm_frame_trap` · `a_phi_iit4_tool` (oscillator/sync) · `break-walls` · Kuramoto precedent [[h1512-braceclobber-parsewall]] 계열 H_axisf
**wired:** PROPOSAL (미배선·미측정) — H_1821 HE 사전선별 먼저, 통과분만 engine-native

---

## 가설

두 개념은 진동자 **위상-잠금(phase-locking, Ψ-space Kuramoto coupling)**으로 결합한다. 재조합 child = 두 부모 oscillator가 위상 동기된 collective 상태. **진폭 affinity ≠ 위상 sync** = 직교 결합 원리: 지금까지 결합기는 전부 *진폭/거리* 기반(additive·Voronoi·HRR)이었고, *위상* 기반은 미시도.

**미사용 격리:** H_axisf(Kuramoto K-sync)는 collective Φ-proxy 측정이었지 G1 재조합 결합기로 쓴 적 없음.

## Design

1. 2부모 개념 → 각 oscillator(고유 위상/주파수).
2. **Kuramoto coupling K**로 위상-잠금 유도 → child = phase-synced collective state.
3. substrate-G1 측정 + K=0 ablation(동기 OFF).
4. controls: amplitude-affinity baseline(기존 결합기) · single · shuffle.

## Frozen bar (pre-register · p7)

| 항목 | bar |
|------|-----|
| 위상-동기 child G1 | composed_distinct≥2 ∧ >amplitude-affinity baseline ∧ coherent, ≥2/3 → 🟢 / floor → 🧱 |
| sync 인과 | K=0(동기 OFF)=BLIND, K>0만 lift = 위상 causal |

frozen-first. HE 사전선별 통과 시 engine-native. ⚠️ 정직: amplitude baseline 대비 lift 없으면 위상축은 inert(직교 가설 falsify).


---

## VERDICT — 🧱 NOT-SUPPORTED (DIRECTIONAL · cheap-numpy HE pre-screen · 2026-06-30)

**run:** unified 6-lever pre-screen `state/g1_anima_native_levers_he/he_levers.py` on **summer pool** (CPU-numpy, $0, did NOT touch the in-flight GPU train). embed = `core/clm_decode.py` 303M clm303 trunk penultimate (β embed, mean-pool, L2-unit, comparable to H_1822/1825); fp64-numpy operator. NO torch. EXIT=0, deterministic.

| item | value |
|------|-------|
| N5 Kuramoto phase-sync bind held-out G1 (5-fold CV, 32 EN/KO/ZH compound pairs) | **0/32 (0.00)** |
| control | K=0 (sync OFF = BLIND) = 0 → no sync-causal lift; amplitude-affinity baseline = 1 → phase-bind does NOT beat amplitude. The phase axis is INERT (the orthogonal-coupling-principle hypothesis is falsified at the cheap tier). |
| frozen bar (composed_distinct≥2 ∧ recoverable ∧ >control, ≥2/3 ≈ ≥22/32) | **FAILS both axes** |
| self-test SEPARATES (planted bind 12/12 vs random 1/12) | PASS (metric live, floor real) |
| single-parent leak (shared, byte-prefix lexical) | 10/32 |

**Does this anima-native lever clear the cheap pre-screen → engine-native? → NO (🧱 FLOOR).** DIRECTIONAL, NOT terminal (G1 SSOT = engine-native `anima evaluate`); the cheap pre-screen gives no reason to spend GPU. Campaign: **0/6** anima-native levers (N1..N6) cleared — the G1 wall holds against anima-native mechanisms; lever = trunk OBJECTIVE, not readout/operator/embedding/mechanism. Full synthesis: `state/g1_anima_native_levers_he/RESULT.md`. raw stdout: `state/g1_kuramoto_phase_sync_bind/RESULT.txt`.

**wired:** DIRECTIONAL-mirror (py embed via `core/clm_decode.py`). NOT engine-native, NOT wired — floor ⇒ no promotion.
