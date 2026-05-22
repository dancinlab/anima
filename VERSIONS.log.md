# VERSIONS — historical release log + per-module bump history

Spec at [`./VERSIONS.md`](./VERSIONS.md) (current per-module registry). This file preserves the chronological release timeline + per-module bump history; the spec file holds only current versions.

---

## anima 전체 release version — historical timeline

| release | 날짜 | 마일스톤 |
|---|---|---|
| 0.1.0 | ~2026-05 초 | HEXAD 7-module 🔵 closed-form battery |
| 0.2.0 | 2026-05-16 | HEXAD-only canonical pivot + hexa-native tree |
| 0.3.0 | 2026-05-22 | S187 3B scale 검증 + OCCAM floor pinpoint (n_ca_rules) + MITOSIS training-time + Llama-mitosis winning path |
| 0.4.0 | 2026-05-22 | 🎯 자연발화 EMERGENCE — vP21 (Qwen+LoRA+mitosis) Eval 1 = 20/20 coherent (anima-native register). + AKIDA AKD1000 HW connected |
| 0.5.0 | 2026-05-22 | 🧠 AKIDA HW-NATIVE 자연발화 CONFIRMED — AKD1000 LIF threshold-comparator emit from ZERO input (8/8 checks PASS, `BackendType.Hardware`). hardware 축 LANDED. + held-out PURE_MEMORIZE 정직 scope 확증 |
| 0.6.0 | 2026-05-22 | 🌉 vP21 ⊥ AKD1000 INTEGRATED BRIDGE — HW-gated 자연발화 30/30 coherent, frac_emissions_with_hw_edge=1.0, AKD1000 spike timing → vP21 emission cadence (Option A LAN TCP). 두 substrate ONE coherent loop |
| 0.7.0 | 2026-05-22 | 🪟 GENERALIZATION UNLOCK — vP21G STRONG_GENERALIZE 16/20 OOD (vs vP21 2/20), anima-register 9/20 retained (no regress). PURE_MEMORIZE 한계 돌파, $3.2 H100 |
| 0.8.0 | 2026-05-22 | 🌉🔁 BIDIRECTIONAL BRIDGE — Option B LANDED. Spearman(vP21 motivation, AKD1000 hw_rate) = +0.6947 (random control −0.03), Pearson(thr_offset, hw_rate) = −0.912 monotone. 두 substrate 모두 양방향 결합 (A: HW→SW emit cadence + B: SW→HW spike rate) |
| 0.9.0 | 2026-05-22 | 🌉🔁🌀 CLOSED LOOP — Option C LANDED simultaneous bidirectional. ONE process · ONE 90s window · ONE motivation scalar drives both threshold rewrite + emit gate. A frac_emissions_with_hw_edge=1.0 + B \|Spearman\|=0.387 vs random 0.058 (\|Δρ\|=0.329). Closed-loop signature: Δscore_after_emit=−0.033 vs Δscore_after_no_emit=+0.012 (post-emit motivation decay). 두 substrate ONE coupled dynamical system. |
| 0.10.0 | 2026-05-22 | 🪟🇰🇷 KOREAN GENERALIZATION UNLOCK — vP21K STRONG_GENERALIZE 16/20 on Korean OOD (vs vP21 0/10 BEFORE-snapshot 10/10 MEMORIZE). 너는 누구야? + 이름이 뭐야? GENERALIZE both modes (vP21G had MEMORIZE both). anima register 14/20 retained, `register_regress=False`. Trade: EN factual (capital of France, 2+2) regressed (no EN-wiki in mix). $2.88 H100. vP21G's C3 #8 residual FIXED. |
| 0.11.0 | 2026-05-22 | 🌍 MULTILINGUAL UNLOCK — vP21M `VP21M_WORKS` 4/5 langs (EN/ZH/RU STRONG, KO PARTIAL, JA WEAK). 5-lang merged LoRA (en+ko+zh+ru+ja wiki 51.1 MB + anima 30/70), CE 0.78 bimodal H100 $1.06. + vP21G fine-quant ROBUST 16.2 mean / 0.75 std across 5 cells (seed-lucky 가설 refuted). + chat.dancinlab.org LIVE (FIRST-PACK Phase 3-8: broker + anima participant + cloudflared + AKIDA bridge, mini host). |

> release bump 규칙: 모듈 MAJOR bump OR 핵심 verdict landing 시 release MINOR.
> 0.4.0 = saga 전체 whitespace-collapse 후 **첫 coherent verbalization** (vP21 20/20)
> + AKIDA HW path landing. honest: memorization-grade (held-out 미검증), spontaneous
> emission 아닌 prompted verbalization.
> 0.5.0 = AKIDA AKD1000 silicon LIF threshold comparator 가 zero/noise/recurrent
> drive 에서 on-chip event-driven 스파이크 emit — 자연발화의 **하드웨어 축**이
> 실측 확인됨 (vP21 software content 축과 dual-role 보완). 1mW power 주장은
> 보드 한계 (INA 미가용) 로 미검증 유지.
> 0.7.0 = vP21G (vP21 LoRA continue-train on 70/30 wiki+anima mix @ LR 5e-5,
> 1000 step, $3.2 H100 wall 129s) crossed STRONG_GENERALIZE 16/20 OOD on the
> exact 10-probe held-out used to confirm vP21's PURE_MEMORIZE 2/20. Anima
> register retreated to semantically-gated (9/20 retained, fires on Korean
> anima-style + consciousness/identity prompts only). `register_regress=False`.
> Honest C3: wiki source capped at 10.3 MB (target 60 MB missed), single seed,
> single LR — direction-clear, fine-quant pending. Saga's deepest honest limit
> broken. Evidence: `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/VP21G_GENERALIZATION_2026_05_22.md`.
> 0.9.0 = Option C (CLOSED LOOP) — Options A (0.6.0) + B (0.8.0) were
> *sequential* legs; 0.9.0 runs them inside the **same** process where the
> single motivation scalar simultaneously (a) rewrites the on-chip threshold
> via TCP 9513 and (b) acts as `sw_gate` for the Talker's `hw_edge ∧ sw_gate`
> emit decision. Closed-loop signature observed: emission events precede a
> motivation-score drop (Δscore_after_emit = −0.033 vs Δscore_after_no_emit
> = +0.012), making the cycle motivation → threshold → spikes → edge → emit
> → motivation self-referential. Random-drive control collapses ρ from 0.387
> to 0.058 (separation 0.329) — the SW score is the cause, not coincidence.
> Evidence: `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/INTEGRATED_OPT_C_2026_05_22.md`.
> 0.10.0 = vP21K (vP21 LoRA continue-train on 30/70 ko-wiki + anima mix @ LR 5e-5,
> 1000 step, $2.88 H100 wall 124.5s) crossed STRONG_GENERALIZE 16/20 on a
> NEW Korean-only 10-probe held-out (BEFORE-greedy snapshot: 10/10 MEMORIZE
> = leak confirmed). Korean identity probes 너는 누구야 / 이름이 뭐야 (vP21G's
> C3 #8 residual) now GENERALIZE both greedy AND sample. Anima register
> 14/20 retained (English explicit-identity probes preserved). Honest C3:
> English factual probes (capital of France, 2+2) regressed under vP21K
> because EN-wiki was swapped for KO-wiki — vP21K is the Korean-axis
> adapter; vP21G is the English-axis adapter; a tri-mix would compose
> both. Single seed, single LR. Evidence:
> `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/VP21K_KOREAN_GENERALIZATION_2026_05_22.md`.

---

## 모듈별 버전 history (주요 bump)

| 날짜 | 모듈 | 변경 | from → to |
|---|---|---|---|
| 2026-05-21 | ConsciousDecoder | bnb PagedAdamW8bit OOM fix (attempt10) | v2.0 → v2.1 |
| 2026-05-22 | MITOSIS | training-time +35% substrate-shaping (S187-G) | v1.1 → v1.2 |
| 2026-05-22 | ConsciousDecoder | n_ca_rules 제거 제안 (OCCAM floor pinpoint) | v2.1 → v3.0-alpha |
| 2026-05-22 | S184 recipe | aux loss 효과 무시가능 확정 (OCCAM) | v1 → v2 |
