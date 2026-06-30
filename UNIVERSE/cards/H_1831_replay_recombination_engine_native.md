# H_1831 — 꿈/REM replay 재조합 engine-native REOPEN (N6)

**id:** H_1831
**slug:** replay_recombination_engine_native
**tier:** 🔵 PROPOSAL · 🔓 REOPEN of H_987 (anima-native novel lever · 고갈 brainstorm 산출)
**date:** 2026-06-30
**source:** UNIVERSE (anima-native novel 레버 고갈 brainstorm)
**렌즈:** `a_chat_sleep_imagination` (WAKE/REM stage) · `a_mitosis_train` (replay-bind tick) · `a_break_the_wall` (proxy verdict ≠ engine-native)
**wired:** PROPOSAL (미배선·미측정) — H_1821 HE 사전선별 먼저, 통과분만 engine-native

---

## 가설

꿈/REM 단계의 **오프라인 replay-bind**가 재조합을 만든다. 생물에서 해마 replay는 *기억 재조합*의 무대(offline consolidation). anima의 dream stage(emit-free 내부 리허설, `anima_dream_stage.hexa`)에서 두 기억을 replay하고 mitosis tick이 BIND하면 child가 창발한다 — forward pass가 아니라 *오프라인 consolidation*에서 G1.

**🔓 REOPEN 근거(a_break_the_wall):** H_987(replay_recombination)은 **옛 Φ-proxy era** verdict다. proxy≠engine-native(UNIVERSE 교훈 #1·#7: torch/proxy GREEN은 DIRECTIONAL). 같은 메커니즘을 **frozen engine-native G1 bar**로 재측정 = 정당한 reopen(측정경로 무결성).

## Design

1. dream stage(REM)에서 2기억 replay → mitosis tick bind(`core/engine_cli.hexa` MITOSIS).
2. **engine-native G1**(Φ-proxy 아님): composed_distinct≥2 ∧ held-out.
3. controls: no-replay baseline · WAKE(replay 없는 단계) · shuffle-replay.

## Frozen bar (pre-register · p7)

| 항목 | bar |
|------|-----|
| replay-bind child | engine-native G1 distinct≥2 ∧ >no-replay ∧ held-out, ≥2/3 → 🟢 / floor → 🧱 |
| stage 인과 | WAKE(no-replay)=floor, REM-replay만 lift |

frozen-first. ⚠️ 정직: H_987이 proxy로 GREEN이었어도 engine-native에서 floor면 H_987도 RETRACT(measurement-path 정정). HE 사전선별 통과 시 engine-native(live MITOSIS).


---

## VERDICT — 🧱 NOT-SUPPORTED (DIRECTIONAL · cheap-numpy HE pre-screen · 2026-06-30)

**run:** unified 6-lever pre-screen `state/g1_anima_native_levers_he/he_levers.py` on **summer pool** (CPU-numpy, $0, did NOT touch the in-flight GPU train). embed = `core/clm_decode.py` 303M clm303 trunk penultimate (β embed, mean-pool, L2-unit, comparable to H_1822/1825); fp64-numpy operator. NO torch. EXIT=0, deterministic.

| item | value |
|------|-------|
| N6 replay recombination (REOPEN H_987) held-out G1 (5-fold CV, 32 EN/KO/ZH compound pairs) | **1/32 (0.03)** |
| control | no-replay baseline = 1 → replay does NOT beat no-replay. On a completely different substrate/metric (303M trunk embed) this REPRODUCES H_987's 'replay ≈ idle' null (proxy↔cheap AGREE — the proxy≠engine divergence the card warned of does NOT appear; both say replay adds no recombination). Terminal RETRACT of H_987 would need engine-native MITOSIS-replay, but the cheap floor warrants no such spend. |
| frozen bar (composed_distinct≥2 ∧ recoverable ∧ >control, ≥2/3 ≈ ≥22/32) | **FAILS both axes** |
| self-test SEPARATES (planted bind 12/12 vs random 1/12) | PASS (metric live, floor real) |
| single-parent leak (shared, byte-prefix lexical) | 10/32 |

**Does this anima-native lever clear the cheap pre-screen → engine-native? → NO (🧱 FLOOR).** DIRECTIONAL, NOT terminal (G1 SSOT = engine-native `anima evaluate`); the cheap pre-screen gives no reason to spend GPU. Campaign: **0/6** anima-native levers (N1..N6) cleared — the G1 wall holds against anima-native mechanisms; lever = trunk OBJECTIVE, not readout/operator/embedding/mechanism. Full synthesis: `state/g1_anima_native_levers_he/RESULT.md`. raw stdout: `state/g1_replay_recombination_engine_native/RESULT.txt`.

**wired:** DIRECTIONAL-mirror (py embed via `core/clm_decode.py`). NOT engine-native, NOT wired — floor ⇒ no promotion.
