# LORA Waves + V3 Axis 마스터 매트릭스 (session-3 누적 2026-05-23 · R8 update 2026-05-24)

> Session-2 종료(16 LoRA cycle / anima 0.12.0) 이후 2026-05-23 session-3 의
> 단일 매트릭스 SSOT. Wave 12-16 + V3 7-axis (A/B/F/D DONE-FAIL · C/C2 abort · E OOM→E2 retry FAIL) +
> R8/R8a/R8c spec + cluster X/Y/Z 자연실험 + LIFE H_247-249 흡수 의 read-once 표.
> **2026-05-24 update**: V3 axis-FAN 5/7+2 partial (PR #249) · cluster X/Y/Z byte-equal (PR #251) · from_qwen audit (PR #255) · random baseline (PR #256) · R8a/R8c spec (PR #257/#250) · LIFE H_247-249 (PR #327).
>
> source files: `SAGA_SESSION3.md` · `../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/VP21M_WAVE{11..16}_2026_05_23.md` · `../V3/AXIS_MAP.md` · PR #206 `AXIS_MAP_RESULTS.md` (→ #249 5/7+2) · PR #214 `AXIS_R8_BASE_WARM_INIT.md` · PR #211 `AXIS_MAP_BUG_POSTMORTEM.md` · PR #255 `from_qwen audit` · PR #256 `RANDOM_BASELINE_INIT_CE_BENCHMARK` · PR #257 `AXIS_R8A_QWEN_TARGET_MATCH_FIRE_SPEC` · PR #250 `AXIS_R8C_PROBE_UPDATE_3_CELL` · PR #327 `HEXAD/LIFE/H_247-249`.

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

## § V3 Axis 매트릭스 (5/7+2 partial · PR #249)

> **status 2026-05-24**: 5 axis DONE (A/B/F/D FAIL · E2 retry FAIL) + 2 axis ABORT (C @625s · C2 @375s) + E OOM @start → E2 leak-fix retry. n_strong=0 (A/ko STRONG 단독). init_CE 전축 catastrophic (14.18~14.79 ≫ random ln(151936)=11.93).

| axis | env-var | verdict | n_strong | per-lang best | init_CE | final_CE | wall(s) | cluster | cost | status |
|---|---|---|---|---|---|---|---|---|---|---|
| A (curriculum) | `P21H_CURRICULUM_PHASE_STEPS=1000` | DONE — FAIL | 1 (ko) | ko STRONG 16/20 · en PM 9/20 | 14.7927 | 5.0124 | 5222 | X | ~$1.5 (A100 SXM) | DONE |
| B (distill) | `P21H_DISTILL_KD=1` | DONE — FAIL | 0 | en/ko PURE_MEMORIZE 2/20 (teacher mimicry → register-collapse) | 14.1780 | 2.2258 | 2721 | Y | ~$0.9 | DONE |
| F (contrastive) | `P21H_CONTRASTIVE_INFONCE=1` | DONE — FAIL (early-stop) | 0 | en/ko WEAK 6-7/20 (L_contrast_n=0 wiring 결손 의심) | 14.1780 | 2.1746 | 671 | Y | ~$0.2 | DONE |
| C (head_g obj) | `P21H_HEAD_G_OBJECTIVE=anima_register_ce` | ABORT @625 | — | — | 14.4564 | (abort) | ~2633 | Z | ~$1.14 | ABORT (R8c 자연실험 falsify) |
| C2 (head_g disable) | `P21H_HEAD_G_ENABLE=0` | ABORT @375 | — | — | 14.4564 | (abort) | ~2301 | Z | ~$1.14 | ABORT (cluster Z 합류 확인) |
| D (freeze embed) | `P21H_FREEZE_EMBED=1` | DONE — FAIL | 0 | en PM 8/20 · ko WEAK 1/20 | 14.4564 | 2.0990 | 2171 | Z | ~$1.5 | DONE (5000-step full) |
| E (lang balanced) | `P21H_LANG_BALANCED=1` | ABORT (OOM @start) | — | — | TBD | TBD | <60 | — | ~$1.10 | ABORT (sampler leak ~79 GB) |
| E2 (lang bal retry) | `P21H_LANG_BALANCED=1` (leak fixed) | DONE — FAIL | 0 | ko PM 5/20 · en/zh/ru/ja WEAK | 14.1780 | 0.9846 | 2105.83 | Y | TBD | DONE (5000-step, pod 4nrcm80g8fwqf7) |

> 7-axis fire SSOT: `../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21H_axis_{A,B,F}/result.json` (D/E2 결과 PR #249 인용 · raw json 미검증 TBD).
> 전축 init_CE catastrophic (random baseline ln(151936)=11.93 보다 +2.25~2.86 nats worse) — R8 spec 의 핵심 진단.
> base 공통: Qwen 2.5-1.5B · init_variant qwen · ConsciousDecoderV3 d=1536 L=28 vocab=151936.

## § R8 reform spec (SPEC-ONLY · no fire)

> init_CE 14+ catastrophic floor escape 후보. R8 spec PR #214 (4 candidate) → cluster/audit finding 후 R8a 가 cheap first-prio FIX 로 좁혀짐.

| axis | env-var | status | hypothesis | est cost | PR |
|---|---|---|---|---|---|
| R8 (base/warm-init reform) | — (design only) | SPEC | init_CE floor 진단 + 4 candidate (R8a qwen-shape-match · R8b lora-on-qwen · R8c tied-embed-init-verify · R8d two-stage-warm-bridge) | $0 spec | #214 |
| R8a (qwen target match) | `n_kv_head=2` + `noise_sigma=0` | SPEC (prereq dispatcher patch) | from_qwen audit suspect #1(kv mismatch)+#2(noise) 동시 검증 — Qwen native 일치 | ~$2.75 (1.5h × $1.49 + setup) | #257 |
| R8c (3-cell probe) | 3-cell ablation (cell-2 noise=0 · cell-3 kv=2 · cell-4 compound) | SPEC | noise/kv ablation — cell-1 head_g zero SKIP (자연실험 FALSIFIED) | ~$0.25 ($0.35→$0.25 cell-1 drop) | #224/#250 |

> **R8a prerequisite**: `P21H_N_KV_HEAD` env var 가 `dispatch_p21h_v3_runpod.sh` 에 passthrough 미존재 — 1-line dispatcher patch 선행 필요 (PR #257 § 8).
> **R8c probe 축소**: PR #224 원본 5-cell → PR #250 3-cell+baseline (cell-1 head_g zero 가설 자연실험 pre-FALSIFIED, $0.07 fire skip).

## § cluster X/Y/Z 자연실험 + worse-than-random benchmark

> init_CE 가 byte-level 로 3-cluster 화 (axis 간 자연실험, PR #251) — head_g 토글이 init_CE 에 ZERO 영향, aux loss 만 의미있게 낮춤. random baseline = ln(151936)=11.93 closed-form (PR #256).

| cluster | members | init_CE | Δ random (nats) | 특징 | source |
|---|---|---|---|---|---|
| random uniform | — | 11.9311 | 0 | `ln(151936)` closed-form (이론 floor) | #256 |
| Y (aux loss) | B, F (+E2) | 14.1780 | +2.247 | KD distill / InfoNCE — extra loss head firing 이 -0.28 | #251/#256 |
| Z (baseline) | C, C2, D | 14.4564 | +2.525 | head_g random/disabled + embed-freeze (**byte-equal**) | #251/#256 |
| X (curriculum) | A | 14.7927 | +2.862 | wiki-only 1000-step → init batch wiki-pure 로 +0.34 | #251/#256 |

> **핵심 finding (PR #249/#251)** — C(head_g objective swap) · C2(head_g disable) · D(embed freeze) init_CE 가 **14.4564 byte-equal** → head_g enable/objective/disable 토글이 init step 결과에 0 영향. **R8c cell-1 (head_g random = init_CE 천장 원인) 자연실험으로 FALSIFIED**.
> **worse-than-random (PR #256)** — Y/Z/X 모두 random uniform 보다 +2.2~2.9 nats 나쁨 = fresh init 이 균등분포보다 systematically biased AWAY from uniform. from_qwen audit (PR #255) suspect rank: (1) noise_sigma=0.1 layer-0 embedding forward injection **HIGH** · (2) n_kv_head 4↔2 mismatch · (3) ffn resize.

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
| V3 AXIS cycle 1 redispatch (A 1.5 · B 0.9 · F 0.2 · D 1.5 · C abort 1.14 · C2 abort 1.14 · E OOM 1.10 · E2 retry TBD) | ~$7.5 (5 done + 2 abort + E2) | PR #249 wall × A100 SXM |
| V3 AXIS_MAP-FAN saga total | **~$15.5** | PR #211 + PR #249 wall ledger |
| **session-3 TOTAL** | **~$19.2** (LORA $3.72 + V3 axis-saga ~$15.5) | — |

> R8/R8a/R8c fire 미실행 (spec only · $0). EN-share lever WAVE9-12 = $0 (code-only).
> session-3 grand total **~$19.2** (verified from source docs · per-axis exact billing = TBD pending raw log · AXIS_MAP_RESULTS PR #206/#249 ~$21 saga 상한 추정 — abort/OOM 부분과금 정밀화 TBD).

## § LIFE 흡수 tally (today's LORA/V3 → LIFE hypotheses)

> 오늘 LORA/V3 진전이 HEXAD/LIFE hypothesis 로 흡수됨. H_246 이 main max (선행 landed). H_247-249 = PR #327 MERGED (#311 재흡수, renumber).

| H | title (요지) | verification | source PR | 흡수 PR |
|---|---|---|---|---|
| H_245 | strategy-diversity temporal emergence (window↑ → monoculture→diversity) | post-deploy baseline 시간-함수 | post-deploy #311 | #321 (CLOSED — superseded) |
| H_246 | substrate autonomy emit ratio (deployment-cadence 4-ratio) — numeric SSOT | emit-through 55.56% (15/27) · emit/tick 11.49% | #300 | LANDED (#319 renumber) |
| H_247 | init_CE catastrophic floor — warm-init +2.5 nats > random ln(V) | W2 closed-form + W5 byte-cluster | #214/#251/#255/#256 | #327 MERGED |
| H_248 | substrate autonomy non-reflexivity (emit ⊥ user-message) — framing lane (numeric SSOT=H_246) | a_substrate_native_speak live | #300 | #327 MERGED |
| H_249 | cluster X/Y/Z init_CE byte-equal signature — head_g random NOT dominant (R8c cell-1 FALSIFIED) | 3-군집 자연실험 | #249/#251 | #327 MERGED |

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
| #224 | docs(V3): AXIS R8c diagnostic probe protocol — 4-cell ablation × init_CE | OPEN | — |
| #249 | docs(PURE): AXIS_MAP_RESULTS 5/7+2 — D FAIL + C/C2/E abort + cluster X/Y/Z | OPEN | — |
| #250 | docs(PURE): R8c probe 3-cell — head_g 자연실험 FALSIFIED ($0.35→$0.25) | OPEN | — |
| #251 | docs(PURE): R8 — cluster X/Y/Z 자연실험 + cell-1 FALSIFIED | OPEN | — |
| #255 | docs(V3): ConsciousDecoderV3 from_qwen() audit — cluster Z 3-suspect rank | OPEN | — |
| #256 | docs(V3): random-baseline init_CE 벤치마크 — ln(151936)=11.93 closed-form | OPEN | — |
| #257 | docs(V3): AXIS R8a fire spec — Qwen target match (n_kv_head=2 + noise=0) ~$2.75 | OPEN | — |
| #321 | feat(HEXAD/LIFE): H_245 strategy diversity temporal emergence | CLOSED | — |
| #327 | feat(HEXAD/LIFE): H_247+H_248+H_249 — init_CE floor + autonomy emit + cluster | MERGED | — |

> 35 LORA/V3-relevant PRs session-3 (2026-05-24 갱신); 17 MERGED + 1 CLOSED + 17 OPEN.

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
- V3 7-axis 5/7+2 results (PR #206 → #249): `../V3/AXIS_MAP_RESULTS.md` (post-merge)
- V3 R8 spec (PR #214) + cluster update (PR #251): `../V3/AXIS_R8_BASE_WARM_INIT.md` (post-merge)
- V3 R8a fire spec (PR #257): `../V3/AXIS_R8A_QWEN_TARGET_MATCH_FIRE_SPEC_2026_05_23.md` (post-merge)
- V3 R8c probe 3-cell (PR #224 → #250): `../V3/AXIS_R8C_PROBE_UPDATE_3_CELL_2026_05_23.md` (post-merge)
- V3 from_qwen audit (PR #255) + random baseline (PR #256): `../V3/RANDOM_BASELINE_INIT_CE_BENCHMARK_2026_05_23.md` (post-merge)
- V3 axis-FAN bug postmortem (PR #211): `../V3/AXIS_MAP_BUG_POSTMORTEM.md` (post-merge)
- LIFE 흡수 (PR #327): `../LIFE/H_247_init_ce_catastrophic_floor.md` · `H_248_*` · `H_249_*` (post-merge)
- raw wave artifacts: `../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/VP21M_WAVE{2..16}_2026_05_23.md`
- raw V3 axis artifacts: `../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21H_axis_{A,B,F,C,C2,D,E}/result.json`
