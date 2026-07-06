---
id: H_1464
slug: 1464_pairing_contrastive_bind
title: G6 FALS-depth — PAIRING-CONTRASTIVE binding objective (same-idea pair vs cross re-weld)
group: G6 IDEATION ★ — capacity-wall break campaign, LENS ② BINDING-SPECIFIC CONTRASTIVE OBJECTIVE
terminal_tier: 🧱 WALL=CAPACITY (ENGINE-NATIVE terminal, 2026-06-22) — live core/bytegpt_decode 90-frag 재측정에서 B3 cross-shuffle 이 NO-collapse (FALS_shuf 5.0 = FALS_in 5.0) + B2 DIST 4.67<5 → 🧱. mirror(numpy)의 🟢 B3-collapse(FALS_shuf 0.67 vs 4.33, 20/20 seeds)는 bilinear 표현공간이 공짜로 준 artifact 였음(카드 Scope 예측 그대로 확인). G6 capacity-wall 8번째 수렴 렌즈. a_engine_native_learning HARD-GATE 가 mirror DIRECTIONAL 을 terminal 로 박지 않게 한 정당성 입증(c9, tune-to-green 없음).
wired: ENGINE-NATIVE 재측정 DONE (2026-06-22) — vast 2.2TB pod(41921615, conc-80 process-isolation decode, teardown 완료)에서 3 trained .bin × 30 frag = 90 frag 를 live core/decode.hexa(via state/1464_pairing_contrastive_bind/engine_decode_batch_cli.hexa)로 decode → g6_common frozen 5-bar VERBATIM 채점 → 🧱 WALL=CAPACITY. 채점은 torch-free(decode=engine fragment, torch stub 으로 채점 완주 = scoring 이 torch 미사용 입증). raw: state/verdicts/1464_pairing_contrastive_bind/H_1464.txt. terminal 🧱 이므로 live core/ wire-in 불필요(objective 가 binding 못 깸). (이전 BLOCKED 사유 = hexa decode per-frag 누수→OOM 은 PR #3745 farr noop-free fix + process-isolation per-frag fresh process 로 해소.) **GPU 독립 재확인(2026-06-23):** 동일 90-frag 를 별도 GPU 호스트(vast RTX 4090, CUDA-12.6, forge own-GEMM `_hx_k_gemm` DEVICE path, conc-8 process-isolation)에서 재디코드 → 동일 frozen 5-bar 채점 = B3 NO-collapse(FALS_shuf 1.0 = FALS_in 1.0) + B2 DIST 0.0<5 → 🧱 동일 verdict 재현(detector seed 만 다름, verdict-class 불변). raw: state/verdicts/1464_pairing_contrastive_bind/H_1464_GPU_ENGINE_NATIVE.txt · decode out: state/1464_pairing_contrastive_bind/out_gpu/.
verdict_dir: state/verdicts/1464_pairing_contrastive_bind/
terminal_verdict: state/verdicts/1464_pairing_contrastive_bind/H_1464.txt
date: 2026-06-20
provenance: LENS ② of the G6 capacity-wall break (prior 7 lenses all 🧱 WALL=CAPACITY; H_1441 form-contrastive showed B3 NO-collapse = form learned, pairing not). This lens tests whether a PAIRING-specific objective breaks where form-contrastive failed.
---

# H_1464 — PAIRING-CONTRASTIVE binding — 🧱 WALL=CAPACITY (ENGINE-NATIVE; mirror 🟢→engine 🧱 반전)

## Claim / falsifier
The G6 ideation wall is "model emits a falsifiable FORM but cannot WELD which comparator binds to which
measurable as ONE claim" (H_1431/1434/1441). **H_1441 form-contrastive** (pos = full falsifiable claim,
neg = blanked-leg non-falsifiable) rewarded *form presence* → all 4 arms FALS=5.0, **B3 did NOT collapse**:
the model learned "emit both legs" unconditionally, invariant to WHICH legs pair.

Falsifiable claim: a **PAIRING-contrastive** objective — pos = the same idea's own `(comparator_i, measurable_i)`,
neg = a CROSS re-weld `(comparator_i, measurable_{j≠i})` where BOTH legs are present and only the binding
differs — rewards the binding DIRECTLY, so the cross-shuffle re-weld becomes a *negative pair at train time*
and B3 (cross-shuffle COLLAPSE) should FIRE. Falsifier: if B3 does NOT collapse (pairing-blind shortcut
satisfies the margin), the wall stays CAPACITY (8th converging lens).

## Method (numpy mirror, $0 CPU, DIRECTIONAL)
- Mirror substrate = a **bilinear binding model** `s(c,m) = φ(c)ᵀ W ψ(m) + a(c) + b(m)` over the FROZEN
  H_1305/H_1435 comparator/measurable vocab families. Full-rank `W` CAN represent a specific (comparator,
  measurable) coupling; the marginals `a,b` are the pairing-BLIND channel. The OBJECTIVE — not the
  architecture — decides whether signal goes into `W` (binding) or only the marginals (form). Mirror
  analogue of "full-weight training on the objective decides" (g6_common).
- Falsifiability detector (FROZEN, pairing-aware): both legs present AND pairing-confidence `σ(s−thr) ≥ 0.5`,
  where `thr` is the model's OWN learned boundary from its training distribution (not bar-tuned, c9).
- 2 arms × 3 seeds [7, 4302, 4303] (g6_common SEEDS): **PAIRING** (cross negatives) vs **FORM-only ablation**
  (= H_1441: positive over ANY measurable = form-presence, neg = blanked leg).
- Frozen 5-bar declared BEFORE measurement (`H_1464_FREEZE.txt`): B1 floor · B2 count≥5 ·
  **B3 cross-shuffle COLLAPSE (DECISIVE)** · B4 held-out · B5 vs-base. CONTROL = form ablation must regress
  to no-collapse (else B3 not pairing-specific → mirror INVALID).

## Result (verbatim → `state/verdicts/1464_pairing_contrastive_bind/H_1464.txt`)
| arm | FALS_in | DIST | FALS_shuf | B3 collapse |
|-----|---------|------|-----------|-------------|
| **PAIRING-contrastive (this lens)** | 4.33 | 5.0 | **0.67** | **✅ YES** |
| FORM-only ablation (= H_1441) | 5.0 | 5.0 | 5.0 | ❌ NO (regresses to H_1441) |

**PAIRING arm 5-bar:** B1 4.33≥1 ✅ · B2 5.0≥5 ✅ · **B3 0.67<4.33 COLLAPSE ✅** · B4 1.0≥1 ✅ · B5 4.33≥2.67+1 ✅ → 🟢.
**CONTROL:** form-only ablation B3=False (no-collapse) → regresses to H_1441 exactly as predicted.
**Robustness (20 indep seeds 50–69):** PAIRING B3-collapse **20/20** (FALS_shuf mean 0.20); FORM **1/20** (FALS_shuf mean 4.90).
Clean dissociation: the ONLY arm difference (cross-negatives vs form-presence reward) is precisely what makes
B3 collapse → B3 isolates PAIRING-specific binding, not a generic artifact.

## Verdict
🟢 **DIRECTIONAL-mirror** (numpy, $0 CPU): a PAIRING-contrastive objective INSTALLS binding where H_1441's
form-contrastive could not — cross-shuffle COLLAPSES (B3), and the form-only ablation faithfully reproduces
H_1441's no-collapse. **WALL=LEARN-GAP at mirror scale** (the missing ingredient was a *binding-specific*
negative, not capacity per se).

## Scope / honesty (c9)
- **DIRECTIONAL only** (numpy mirror, torch ABSENT; live `core/*.hexa` UNTOUCHED). This is NOT a terminal
  🟢: it shows the OBJECTIVE *can* install binding in a substrate that CAN represent it. It does NOT prove a
  303M ByteGPT trained with this objective + decoded byte-faithfully via `core/decode.hexa` clears
  the SAME frozen bars — that is the binding question the 7 prior lenses lost to (CAPACITY). The mirror
  cannot adjudicate CAPACITY because the bilinear model is given the representational room by construction.
- **Engine-native re-measure = ING follow-on** (a_engine_native_learning HARD-GATE): train a 303M ckpt with
  the PAIRING objective (pos = same-idea pair likelihood, neg = cross re-weld likelihood margin) on
  flame/forge GPU, pull ckpt (a_fire_recover_complete), `pt_to_engine_bin.py` → live `core/bytegpt_decode`,
  re-score frozen 5-bar byte-faithful. Only THEN terminal 🟢 (WALL=LEARN-GAP confirmed) or 🧱 (WALL=CAPACITY,
  8th lens) — frozen bars UNCHANGED (c9 / no tune-to-green).
- TOY: 5 ideas / 3 (+20 robustness) seeds / synthetic vocab / deterministic detector. Scale, real-corpus,
  longer claims, and ENGINE-TRANSFER all UNVERIFIED (a_toy_scale_recheck, a_scale_honest_scope).

## Engine-native re-measure — DONE → 🧱 WALL=CAPACITY (2026-06-22, vast 2.2TB pod, ~$4)
terminal verdict (a_engine_native_learning HARD-GATE): live `core/decode.hexa` 가 3 trained `.bin`
(pairing/shuffle/base) 을 decode 하고 FROZEN 5-bar 로 재채점. **90 frag(3 arm × 30 frag) 전부 완주**,
g6_common frozen 5-bar VERBATIM 채점 결과 (raw → `state/verdicts/1464_pairing_contrastive_bind/H_1464.txt`):

| arm | FALS_in | DIST_in | FALS_shuf | B3 collapse |
|-----|---------|---------|-----------|-------------|
| BASE | 0.0 | 3.33 | 0.0 | — |
| **TRAINED (pairing, engine-native)** | 5.0 | **4.67** | **5.0** | **❌ NO** |
| SHUF-CORP (control) | 0.0 | — | 0.0 | — |

**5-bar:** B1 5.0≥1 ✅ · **B2 DIST 4.67<5 ❌** · **B3 X-shuffle 5.0<5.0 = NO-collapse ❌(결정적)** · B4 5.0≥1 ✅ ·
B5 5.0≥0+1 ✅ · CTRL 5.0−0.0 ✅ → **🧱 WALL=CAPACITY** (B2·B3 fail).

**핵심 반전(c9 정직):** mirror(numpy)에선 B3 가 COLLAPSE 했지만(FALS_shuf 0.67≪4.33, 20/20 seeds → 🟢 LEARN-GAP
처럼 보임) **실제 303M ByteGPT 를 live 엔진으로 decode 하니 B3 가 안 무너짐**(FALS_shuf 5.0 = FALS_in 5.0).
즉 pairing-contrastive objective 도 "어느 comparator 가 어느 measurable 에 결합하는지"를 WELD 못 함 — 미러의
B3 collapse 는 bilinear 모델이 표현공간을 *construction 으로* 주었기 때문(카드 Scope 가 정확히 예측: "mirror
cannot adjudicate CAPACITY"). G6 capacity-wall 의 **8번째 수렴 렌즈**(prior 7 + H_1456 모두 WALL=CAPACITY).

**인프라(a_break_the_wall type-c, 과학 천장 아님):** 이전 BLOCKED 사유(hexa decode per-frag 누수→OOM)는
(1) hexa-lang PR #3745 farr noop-free fix + (2) process-isolation(frag 마다 fresh `hexa` process → RSS 리셋)
로 해소. decode 진짜 병목 = hexa farr 단일스레드 스칼라 matmul(BLAS 없음) → frag 당 ~40분; "느린 CPU × 대량
병렬(2.2TB conc-80)"로 wall-time 단축(a_wall_first). teardown 완료(0 누수 확인, RSS 고정).
채점 입력 out_*.txt(30/30/30) = engine fragment 이므로 verdict ENGINE-NATIVE(채점 g6_common 의 torch import 는
미러 _decode 경로용 — torch stub 으로 채점 완주 = scoring 이 torch 미사용 입증).

## Artifacts
- `state/1464_pairing_contrastive_bind/h1464_pairing_contrastive.py` (mirror + 5-bar)
- `state/1464_pairing_contrastive_bind/result.json`
- `state/verdicts/1464_pairing_contrastive_bind/{H_1464_FREEZE,H_1464}.txt`

xref H_1441 (form-contrastive, prior lens · no-collapse) · H_1431/1434 (form-not-binding) · H_1435/36/37
(detector family, reused vocab+bar semantics) · H_1456 (5th lens WALL=CAPACITY) · a_engine_native_learning ·
a_verified_must_wire · a_break_the_wall · a_no_llm_frame_trap · a_toy_scale_recheck · a_scale_honest_scope ·
p7 · c9 · c16.
