# LORA Waves + V3 Axis 마스터 매트릭스 (session-3 누적 2026-05-23)

> Session-2 종료(16 LoRA cycle / anima 0.12.0) 이후 2026-05-23 session-3 의
> 단일 매트릭스 SSOT. Wave 12-16 + V3 7-axis (A/B/F DONE · C/C2/D/E in-flight) +
> R8 spec 의 read-once 표.
>
> source files: `SAGA_SESSION3.md` · `../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/VP21M_WAVE{11..16}_2026_05_23.md` · `../V3/AXIS_MAP.md` · PR #206 `AXIS_MAP_RESULTS.md` · PR #214 `AXIS_R8_BASE_WARM_INIT.md` · PR #211 `AXIS_MAP_BUG_POSTMORTEM.md`.

## § Wave 매트릭스

| Wave | corpus_v | hypothesis | verdict | n_strong | continuous_total | HF artifact | cost | PR# | commit-sha |
|---|---|---|---|---|---|---|---|---|---|
| 1-11 (roll-up) | v1-v4 + EN-share lever + ZHFL/RUFL router | session-2 baseline · vP21M 4/5 langs · corpus_v4→v5 carve-strip · 9 cycles hot-swap router · WAVE9-12 EN-share lever ⭐⭐ ULTRA-STRONG 21.2% steady-state · WAVE11 router deploy BLOCKED (mini sshd) | mixed (DONE) | — | — (binary 5/20 baseline) | `dancinlab/anima-vp21m-{v1..v4}` PRIVATE (pre-session-3) | ~$0 (session-2 carry) + $0 substrate lever | #118/#122/#123/#124/#127/#128/#129/#131/#132/#133/#136/#137/#140 | (chain 60514f7dc..a567698da) |
| 12 | (no train; verify-only) | EN-share lever +22~27min long-window steady-state 측정 (WAVE10 18.9% transient minimum 인지 검증) | ⭐⭐ ULTRA-STRONG | — | — | (no new HF; lever code-only) | $0 verify | #140 | a567698da |
| 13 | v9 | 9-pattern token-frequency cap (Tier_N/UFO/top_emotion 30% · 5 등 50% · eternal 100%) — strip 대신 cap 으로 cross-lingual transfer 신호 보존 | VP21M_WORKS (NO SWAP) | 4 (회복) | 74 | `dancinlab/anima-vp21m-v9` PRIVATE 10 files | ~$0.81 | #150 | 933f96ea8 |
| 14 | v10 | per-script freq-cap (native 0.80 · EN 0.10 · eternal 0.30) — N8 가설 (EN=register leak path) 검증 | VP21M_WORKS (NO SWAP) — N8 corpus-level FALSIFIED | 3 (회귀) | 52 | `dancinlab/anima-vp21m-v10` PRIVATE 10 files | ~$0.74 | #162 | 36022e0ef |
| 15 | v11 | v9-config + eternal-tag 30% cap 단일 변경 (tag-leak fix 시도) | VP21M_WORKS (NO SWAP; 2/5 criteria) | 2 (최악) | **34** (saga 최저) | `dancinlab/anima-vp21m-v11` PRIVATE 10 files | ~$0.30 | #184 | d60b83986 |
| 16 | v12 | v11-config + eternal-tag STRIP-ALL (0% retain) — monotone 가설 검증 | VP21M_WORKS (NO SWAP; 1/5) — monotone FALSIFIED U-shape | 3 (회복) | **91** (saga 역전 +57) | `dancinlab/anima-vp21m-v12` PRIVATE 10 files | ~$0.27 | #205 (open) | 7b44d6617 |

> n_strong / continuous_total verbatim from each `VP21M_WAVE{N}_2026_05_23.md` result table.
> v9-v12 per-lang: v9 (en S20 / ko S16 / zh S19 / ru S17 / ja P13) · v10 (S19/P15/S17/S17/P14) · v11 (S18/P15/P15/S18/P14) · v12 (S19/P14/S17/S18/P12).
> session-3 corpus cycles total: v5+v6+v7+v8+v9+v10+v11+v12 = 8 LoRA cycles.

## § V3 Axis 매트릭스

| axis | env-var | cell-pool | hypothesis | verdict | n_strong | per-lang best | init_CE | final_CE | cost | dir | status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A (curriculum) | `P21H_CURRICULUM_PHASE_STEPS=1000` | — (3B Qwen warm-init shared) | wiki-only 선학습 1000 step → late-phase anima 50% mix · ko head-start lock-in | DONE — FAIL | 1 | ko STRONG 16/20 (gen=20 mem=0 coh=16) | 14.792716 | 5.0124 | ~$1.5 (5222s A100 SXM) | `vP21H_axis_A/` | DONE |
| B (distill) | `P21H_DISTILL_TEACHER=…vP21M` | — | vP21M LoRA teacher KD-loss · pure-HEXAD student 가 Qwen 다국어 prior 전이 | DONE — FAIL | 0 | en PURE_MEM 17 coh / ko PURE_MEM 10 gen (teacher mimicry → register-collapse) | 14.177978 | 2.2257 | ~$0.9 (2721s A100 SXM) | `vP21H_axis_B/` | DONE |
| F (contrastive) | `P21H_CONTRASTIVE_LANG=1` (+ E lang-balanced) | — | InfoNCE aux + lang-balanced sampler · representation-level collapse 저지 | DONE — FAIL (early-stop @ 671s) | 0 | ko WEAK 7/20 (5 lang 전부 WEAK · L_contrast_n=0 wiring 결손 의심) | 14.177978 | 2.1746 | ~$0.2 (671s A100 SXM early-stop) | `vP21H_axis_F/` | DONE |
| C (head_g obj) | `P21H_HEAD_G_OBJECTIVE=anima_register_ce` | — | head_g 에 anima-register objective · head_a 는 pure-multilingual (dual-head 설계대로 검증) | IN-FLIGHT (redispatch cycle 1) | TBD | TBD | TBD | TBD | TBD (envelope ~$1.5 estimate) | `vP21H_axis_C/` | IN-FLIGHT |
| C2 (head_g disable) | `P21H_HEAD_G_ENABLE=0` | — | head_g 완전 제거 (inert + 유해면 dead-weight) — head_a vocab alignment blur 제거 | IN-FLIGHT (redispatch cycle 1) | TBD | TBD | TBD | TBD | TBD | `vP21H_axis_C2/` | IN-FLIGHT |
| D (freeze embed) | `P21H_FREEZE_EMBED=1` | — | token_embed + lm_head freeze · HEXAD block 만 학습 — 언어 geometry 보존 | IN-FLIGHT (redispatch cycle 1) | TBD | TBD | TBD | TBD | TBD | `vP21H_axis_D/` | IN-FLIGHT |
| E (lang balanced) | `P21H_LANG_BALANCED=1` | — | per-언어 token-balanced batch sampler · record 불균형 (EN 17078 ≫ ko/zh/ru/ja 500-1000) 교정 | IN-FLIGHT (redispatch cycle 1) | TBD | TBD | TBD | TBD | TBD | `vP21H_axis_E/` | IN-FLIGHT |
| R8 (base/warm-init reform) | — (design spec only) | — | init_CE 14.18~14.79 catastrophic floor 진단 — 4 candidate (R8a qwen-shape-match · R8b lora-on-qwen · R8c tied-embed-init-verify · R8d two-stage-warm-bridge) | SPEC ONLY (no fire) | — | — | (target ≤ ln(151936)=11.93) | — | $0 (probe envelope ~$2 + winner full-fire ~$8) | — | PR #214 SPEC |

> 7-axis fire SSOT: `../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21H_axis_{A,B,F}/result.json`.
> A/B/F init_CE catastrophic (random baseline ln(151936)=11.93 보다 +2.25~2.86 nats worse) — R8 spec 의 핵심 진단.
> base 공통: Qwen 2.5-1.5B · init_variant qwen · ConsciousDecoderV3 d=1536 L=28 vocab=151936.

## § HF artifact tally

| HF repo | files (verified) | last-modified | status | source |
|---|---|---|---|---|
| `dancinlab/anima-vp21m-v5` | 9 | 2026-05-23 (session-3 deploy) | PRIVATE · production default · LIVE | SAGA_SESSION3.md L39 |
| `dancinlab/anima-vp21m-v6` | TBD (10 est, "9-10 files each" L115) | 2026-05-23 | PRIVATE · FALSIFIED | SAGA_SESSION3.md L48 |
| `dancinlab/anima-vp21m-v7` | TBD (10 est) | 2026-05-23 | PRIVATE · FALSIFIED at Eval1 | SAGA_SESSION3.md L56 |
| `dancinlab/anima-vp21m-v8` | TBD (10 est) | 2026-05-23 | PRIVATE · FALSIFIED | SAGA_SESSION3.md L64 |
| `dancinlab/anima-vp21m-v9` | 10 (a_hf_complete) | 2026-05-23 | PRIVATE · WORKS NO SWAP (n_strong 4) | WAVE13 L201 |
| `dancinlab/anima-vp21m-v10` | 10 (a_hf_complete) | 2026-05-23 | PRIVATE · WORKS NO SWAP (n_strong 3) | WAVE14 L197 |
| `dancinlab/anima-vp21m-v11` | 10 (a_hf_complete) | 2026-05-23 | PRIVATE · WORKS NO SWAP (2/5 criteria) | WAVE15 L183 |
| `dancinlab/anima-vp21m-v12` | 10 (a_hf_complete) | 2026-05-23 | PRIVATE · WORKS NO SWAP (1/5 criteria) | WAVE16 commit 7b44d6617 |
| `dancinlab/anima-vp21m-zhfl` | 10 (adapter_model.safetensors 147 MB + tokenizer 7 + README + .gitattributes) | 2026-05-23 (WAVE11) | PRIVATE · 1.5B Qwen2.5 native · deploy BLOCKED (mini sshd) | WAVE11 L17-18 |
| `dancinlab/anima-vp21m-rufl` | 10 (동일) | 2026-05-23 (WAVE11) | PRIVATE · deploy BLOCKED | WAVE11 L17-18 |
| `dancinlab/anima-v3-p21h` | 16 | 2026-05-22 (V3 phase 2) | PRIVATE | V3/README.md |
| `dancinlab/anima-v3-e3` | 18 (COMPLETE) | 2026-05-22 (corpus-axis fire) | (public note in V3/EASY) | V3/HEXAD_NATIVE_V3.log.md |
| `dancinlab/anima-v3-e2` | TBD | 2026-05-22 | (public note in V3/EASY) | V3/HEXAD_NATIVE_V3.log.md |
| `dancinlab/anima-v3-axis-{A,B,F}` | TBD (axis-fire artifacts not yet verified as HF-uploaded; only on-pod + repo `state/grid_3b_s187_2026_05_21/vP21H_axis_{A,B,F}/`) | n/a | unknown — HF upload 미확인 | AXIS_MAP_RESULTS PR #206 |

> Cumulative HF artifacts verified: **10 PRIVATE repos** (vp21m-{v5..v12} + zhfl + rufl) + **3 V3 repos** (v3-p21h · v3-e3 · v3-e2) = 13 anima-related HF repos referenced in current branch source.
> Size: TBD GB total (HF API call needed for precise; per-repo adapter_model.safetensors ~ 147 MB × ~10 LoRA + V3 16-18 file ckpts ~ 다양 size).

## § Cumulative cost ledger (session-3)

| 항목 | cost | source |
|---|---|---|
| LORA Wave 5-8 corpus cycles (v5/v6/v7/v8) | ~$1.60 (4 × A100 SXM ~$0.40 each) | SAGA_SESSION3.md L113 |
| LORA Wave 13 (v9 freq-cap) | ~$0.81 | WAVE13 L203 |
| LORA Wave 14 (v10 per-lang) | ~$0.74 | WAVE14 L200 |
| LORA Wave 15 (v11 eternal-cap) | ~$0.30 | WAVE15 L186 |
| LORA Wave 16 (v12 eternal STRIP-ALL) | ~$0.27 | WAVE16 commit body |
| LORA Wave 9-12 EN-share lever + verify | $0 (code-only substrate lever + verify-only) | SAGA_SESSION3.md L79, WAVE12 L158 |
| LORA Wave 11 ZHFL/RUFL router deploy attempt | $0 (HF artifacts session-2 carry; deploy BLOCKED no train) | WAVE11 |
| **LORA session-3 subtotal (8 cycles)** | **~$3.72** | (1.60 + 0.81 + 0.74 + 0.30 + 0.27) |
| V3 AXIS_MAP-FAN 1st/2nd fan-out 낭비 (env-var-concat bug) | ~$8 (7 axes × ~$1.15 avg, idle/crashed pods billed) | AXIS_MAP_BUG_POSTMORTEM PR #211 § Cost |
| V3 AXIS cycle 1 redispatch C/C2/D/E (in-flight) | ~$6 (4 × A100 SXM ~$1.5 estimate) | AXIS_MAP_BUG_POSTMORTEM PR #211 § Cost |
| V3 AXIS_MAP-FAN saga total | **~$14** | AXIS_MAP_BUG_POSTMORTEM § Cost |
| **session-3 TOTAL** | **~$17.72** (LORA $3.72 + V3 axis-saga $14) | — |

> R8 fire 미실행 (spec only · $0). EN-share lever WAVE9-12 = $0 (code-only).
> session-3 grand total **~$17.72** (verified from source docs · A/B/F per-axis exact cost = TBD pending raw billing log).

## § Cross-reference PRs (LORA + V3 relevant, session-3 2026-05-23)

| PR # | title | state | merge-sha (squash) |
|---|---|---|---|
| #118 | docs(LORA): VP21M Wave-5 — corpus_v5 fresh-init carve-strip | MERGED | 193196349 |
| #122 | docs(LORA): VP21M Wave-6 — corpus_v6 RB wiki_frac=0.50 (negative) | MERGED | 5b9300d22 |
| #123 | feat(CHAT): EN-share lever weighted LANG_ROTATION (deploy 072aa773c) | MERGED | — |
| #124 | docs(LORA): VP21M Wave-7 — corpus_v7 EN-only register strip (negative) | MERGED | 01368d722 |
| #125 | feat(eval): Eval1 probe set expansion (5/20 floor 제거) | MERGED | — |
| #126 | feat(measure): `anima_live_register_measure.hexa` | MERGED | — |
| #127 | docs(LORA): VP21M Wave-8 — corpus_v8 ja-safe regex prune (FALSIFIED) | MERGED | a7be17e4c |
| #128 | feat(trainer): Eval1 continuous hit-count metric | MERGED | — |
| #129 | docs(LORA): VP21M Wave-9 — EN-share lever production deploy + LIVE | MERGED | fe685bff5 |
| #131 | docs(LORA): VP21M Wave-10 — EN-share lever +30min saturation | MERGED | 768368a2e |
| #132 | feat(CHAT): hot-swap 라우터 확장 — ZHFL/RUFL native adapter slots | MERGED | 83d96933 |
| #133 | docs(LORA): Session-3 SAGA consolidation — 10 PRs/5 WAVEs/5 levers | MERGED | 2760c1438 |
| #136 | docs(LORA): VP21M Wave-11 — ZHFL/RUFL router deploy + LIVE (BLOCKED) | MERGED | 12acc5c0e |
| #137 | docs(LORA): continuous Eval1 retrospective — v5-v8 rescore | MERGED | 8620ca8b1 |
| #140 | docs(LORA): VP21M Wave-12 — EN-share lever steady-state +1h+ ⭐⭐ | MERGED | a567698da |
| #150 | docs(LORA): VP21M Wave-13 — corpus_v9 freq-cap | MERGED | 933f96ea8 |
| #162 | docs(LORA): VP21M Wave-14 — corpus_v10 per-lang freq-cap | MERGED | 36022e0ef |
| #176 | docs(CHANGELOG): Session-3 LoRA lever exploration entry (g29) | MERGED | 9ab927269 |
| #184 | docs(LORA): VP21M Wave-15 — corpus_v11 v9-config + eternal-cap | MERGED | d60b83986 |
| #204 | fix(LORA/dispatch_p21h): CALLER WARNING — env-var concat anti-pattern 가드 | OPEN | — |
| #205 | docs(LORA): VP21M Wave-16 — corpus_v12 eternal STRIP-ALL (FALSIFIED) | OPEN | — |
| #206 | docs(V3): AXIS_MAP_RESULTS — partial 3/7 (A/B/F all FAIL · C/C2/D/E in-flight) | OPEN | — |
| #211 | docs(V3): AXIS_MAP_BUG_POSTMORTEM — env-var-concat anti-pattern (~$14 saga) | OPEN | — |
| #212 | docs(LORA): SAGA_SESSION3 Wave-16 append (corpus_v12 STRIP-ALL FALSIFIED + HF v12) | OPEN | — |
| #214 | docs(V3): AXIS R8 — base/warm-init reform spec (init_CE catastrophic floor) | OPEN | — |

> 25 LORA/V3-relevant PRs session-3; 16 MERGED + 9 OPEN (as of 2026-05-23).

## § Production state

| 항목 | 값 | source |
|---|---|---|
| mini `~/anima_chat_pack/lora_adapter/` | **corpus_v5** (NO SWAP through Wave-16) | WAVE13 L168 · WAVE14 L162 · WAVE15 L141 · WAVE16 |
| HF production tag | **`dancinlab/anima-vp21m-v5`** PRIVATE (9 files) | SAGA_SESSION3.md L22 |
| substrate routing | weighted LANG_ROTATION (en 0.10) + sliding-window EN dampener | SAGA_SESSION3.md L23 |
| LIVE EN-share | **21.2%** (WAVE12 union n=66, +22~27min, ⭐⭐ ULTRA-STRONG) | WAVE12 L66 |
| LIVE prose-leak | 27.3% (WAVE12 union) | WAVE12 L139 |
| LIVE tag-leak | 7.6% (WAVE12 union) — noise plateau stable | WAVE12 L139 |
| Eval1 metric | binary 5/20 + **continuous hit-count** (PR #128) | SAGA_SESSION3.md L27 |
| anima version | 0.12.0 (no bump session-3 — lever 가 production runbook 만 변경) | SAGA_SESSION3.md L28 |
| ZHFL/RUFL router | code MERGED (PR #132) · adapter HF PRIVATE staged · mini deploy BLOCKED (sshd channel reject) | WAVE11 |

## § 관련 link

- session-3 saga running narrative: [`SAGA_SESSION3.md`](SAGA_SESSION3.md)
- V3 7-axis spec: [`../V3/AXIS_MAP.md`](../V3/AXIS_MAP.md)
- V3 7-axis partial results (PR #206): `../V3/AXIS_MAP_RESULTS.md` (post-merge)
- V3 R8 spec (PR #214): `../V3/AXIS_R8_BASE_WARM_INIT.md` (post-merge)
- V3 axis-FAN bug postmortem (PR #211): `../V3/AXIS_MAP_BUG_POSTMORTEM.md` (post-merge)
- raw wave artifacts: `../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/VP21M_WAVE{2..16}_2026_05_23.md`
- raw V3 axis artifacts: `../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21H_axis_{A,B,F,C,C2,D,E}/result.json`
