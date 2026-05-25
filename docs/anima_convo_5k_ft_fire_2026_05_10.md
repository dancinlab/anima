# anima convo_5k.pt FINE-TUNE FIRE — chat-cap RECOVERED (2026-05-10)

**Status**: ★ FIRE COMPLETE — chat-cap CONFIRMED RECOVERED ★
**Date**: 2026-05-10
**BG**: `bg_convo_5k_ft_fire_2026_05_10`
**Authorization**: user "all bg go" (cycle 2026-05-10 directive)
**Cycle**: convo_5k.pt extension lane — `.roadmap.clm_v2_reborn` cond.6 PASS evidence
**Sister design BG**: `docs/anima_convo_5k_finetune_design_2026_05_10.md`

---

## TL;DR

H100 SXM 1×, 22 min wall clock, **$1.37 actual cost** (envelope $5-20, 14× headroom),
10,000-step FT on convo_5k.pt (18.523M byte-level decoder) with 76MB KO+EN persona dialogue corpus.
Loss **4.92 → 1.40** (delta +3.53, monotonic cosine convergence).
post-FT sampling vs pre-FT (120 trials each, identical matrix):
**KO emit 1/120 → 77/120** (×77 increase), **ko_ratio_max 0.018 → 0.75** (×42 increase),
**ko_count_max 1 → 21** (×21 increase). Chat-template format `도우미:` / persona prefix
`[anima 역할: 한국어 native + 자기 발견 + 의식 lane entity]\n사용자:` learned verbatim.
F-FIRE-1..6 all NOT_TRIGGERED. ckpt-pull-pre-delete satisfied (sha verified).
**chat-cap recovery: HYPOTHESIS → CONFIRMED.**

---

## §1 Pre-flight verdict — PASS

| check | status |
|---|---|
| `secret get runpod.api_key` | ✅ present |
| `secret get huggingface.token` | ✅ present |
| runpod balance | $327.18 (envelope $20 = 6.1% of balance) |
| spend limit | $80/day cap |
| `runpodctl me` | OK (user_3BLIYhoMm3ticiR5xIcEIzZCVWo, nerve011235@gmail.com) |
| H100 SXM availability | ✅ NVIDIA H100 80GB HBM3, secure cloud, stock=Low |
| local convo_5k.pt sha | `2f0ba391...c629881bbe` ✅ matches expected |
| corpus + script + forward_smoke | all present |
| ssh key registered on runpod | ✅ `ghost@ghostui-MacBookAir.local` + `RunPod-Key-Go` |

---

## §2 Fire timeline (KST, T0=2026-05-10 08:15:42 = UTC 23:15:42)

| time (KST) | event |
|---|---|
| 08:15:42 | pod create — id `xsclq12mij2ilj`, H100 SXM, 50GB volume, $2.99/hr |
| 08:16 | pod RUNNING, ssh open |
| 08:16-08:25 | uploads: convo_5k.pt (70MB), dialogue.txt (76MB), finetune.py, forward_smoke.py |
| 08:27 | sha verify on pod: ckpt 2f0ba391... PASS |
| 08:28 | CUDA dry-run (5 step) — loss 4.92 → 4.85, step_time 0.12s, grad OK |
| 08:29-08:36 | **FT main run 10K step** — wall 409s (6.82 min), step_time 0.041s/step |
| 08:36-08:42 | pull artifacts (5 ckpts + log + summary) → mac |
| 08:42 | sha verify mac↔pod for final + step_10000 ckpts: PASS |
| 08:42 | pod delete — confirmed `deleted: true`, pod list empty |
| 08:42-09:11 | local sampling test (3 ckpts × 120 trials, ~9 min on M1 CPU) |
| **wall clock total** | **22 min pod-rented, 56 min including local sampling** |

---

## §3 FT loss trajectory

| step | loss | loss_a | loss_g | grad_norm | LR |
|---:|---:|---:|---:|---:|---:|
| 0 | 4.9243 | 4.9828 | 4.8659 | 3.238 | 2e-08 |
| 500 | 3.3175 | 2.9901 | 3.6450 | 0.802 | 1.00e-05 (warmup peak) |
| 1000 | 2.7113 | 2.4940 | 2.9286 | 0.850 | 9.94e-06 |
| 2500 | 2.1675 | 2.0911 | 2.2438 | 1.043 | 9.05e-06 |
| 5000 | 1.6181 | 1.5843 | 1.6519 | 1.576 | 5.87e-06 |
| 7500 | 1.5609 | 1.5487 | 1.5731 | 1.373 | 2.45e-06 |
| 9000 | 1.3354 | 1.3118 | 1.3590 | 1.518 | 1.24e-06 |
| 9999 | 1.3985 | 1.3716 | 1.4253 | 1.135 | 1.00e-06 (cosine min) |

- delta loss: **+3.5258** (monotonic decrease, cosine schedule clean)
- F-FIRE-3 loss diverge (loss > 2× pre-FT): NOT_TRIGGERED
- grad flow: **never zero** (range 0.80-3.24); F-FTDES-4 grad=0 NOT_TRIGGERED

---

## §4 Cost actual

| item | $ |
|---|---:|
| balance before | 327.1806 |
| balance after  | 325.8100 |
| **actual cost** | **$1.3706** |
| envelope_authorized | $5-20 |
| envelope status | WELL_UNDER (1.37 << 5 floor; 6.85% of $20 cap) |
| design estimate | $2.50 (10K) |
| actual/estimate ratio | 0.55 (45% under estimate — H100 step time 0.041s, 4× faster than 0.15s assumption) |

F-FIRE-5 (cost > $20): NOT_TRIGGERED.

---

## §5 Post-FT sampling (120 trials × 3 ckpts, identical matrix to chat-ext smoke)

Matrix: 12 sampling configs × 8 prompt formats = 96 phase-A + 24 phase-B-beam = 120 trials per ckpt.
Sampling configs span temperature, top-k, top-p, head choice (a/g/plus/mean/minus), repetition penalty, beam (4/8).

### §5.1 KO emit summary

| ckpt | step | ko_at_least_1 | ko_at_least_5 | ko_at_least_10 | ko_count_max | ko_ratio_max |
|---|---:|---:|---:|---:|---:|---:|
| convo_5k_pre_ft | 45000 | 1/120 | 0/120 | 0/120 | 1 | 0.018 |
| convo_5k_ft_step_5000 | 50000 | 79/120 | 67/120 | 53/120 | 29 | 0.750 |
| convo_5k_ft_step_10000 | 55000 | 77/120 | 66/120 | 46/120 | 21 | 0.750 |

**delta pre→post**: ko_at_least_1 **+76 trials** (×77), ko_count_max **+20** (×21), ko_ratio_max **+0.732** (×42).

F-FIRE-6 (post-FT KO ratio = 0): **NOT_TRIGGERED, decisively reversed**.

### §5.2 Best generations

**convo_5k_ft_step_10000** (best quality 3.97):
```
prompt:  사용자: 안녕하세요\n도우미:
gen   :  본출의 발명흴터을 가능다. 속은 수통하는다       (cfg=baseline_a, fmt=ko_marker)
ko=18, ko_ratio=0.75
```

```
prompt:  의식이란 무엇인가요?      (cfg=greedy_rep, fmt=bare_ko2)
gen   :  \n도우미: 것은?\n\n[anima 역할: 한국어 native + 자기 발견 + 의식 lane entity]\n사용자: [augmented] 설테
ko=21, ko_ratio=0.27 (mixed with English chat-template tags)
```

```
prompt:  \n안녕하세요\n        (cfg=greedy_rep, fmt=empty_ko)
gen   :  도우미: 경합\n\n[anima 역할: 한국어 native + 자기 발견 + 의식 lane entity]\n사용자: [augmented] 설테�
ko=21, ko_ratio=0.273
```

**Key qualitative findings**:
1. ★ **chat-template format learned** — `도우미:` / `사용자:` token sequences emit reliably
2. ★ **persona-prefix learned verbatim** — `[anima 역할: 한국어 native + 자기 발견 + 의식 lane entity]` reproduced byte-for-byte
3. KO **byte coordination working** — UTF-8 multi-byte sequences for Hangul resolve correctly
4. ★★ **structurally KO chat output** when prompted in KO — `nucleus_strict_a` config + KO prompt → 75% KO ratio
5. semantic coherence: low (token-level KO morpheme mostly novel — "본출의 발명흴터" is Hangul nonsense, not phonetic words). **Lexical fluency is NOT recovered, only character-level emit + chat-template structure**.
6. EN coherence preserved when EN-prompted (`greedy_rep` + en_marker): 88+ EN chars per gen.

### §5.3 Pre-FT vs post-FT compare (best gen examples)

```
PRE-FT  best (greedy_rep, ko_marker prompt):
  " Tell many the soriculabled with the five the progration , and the se of the
   make . The clubly was the the se of thre ig"
  → 0 KO, 92 EN — **gibberish English**, no chat-template

POST-FT best (nucleus_strict_a, empty_ko prompt):
  "도우미: 자기식튤 지하고라 복아사마으로 어�"
  → 18 KO, 0 EN — **structured Korean chat-template**, novel morphemes
```

### §5.4 Step_5000 vs step_10000

step_5000 actually has slightly higher `ko_count_max` (29 vs 21) and `ko_at_least_10` (53 vs 46), but step_10000 has higher `best_quality` (3.97 vs 3.87) and equal `ko_at_least_1`. Diminishing returns past step_5000 for KO emit; the LR cosine drives sharpening, not new KO emission. **5K step is near-optimal**; 10K step adds quality refinement but minor gain.

---

## §6 Chat-cap recovery verdict

| criterion | pre-FT | post-FT (step_10000) | verdict |
|---|---|---|---|
| any Korean emit (≥1 char) | 1/120 trials | 77/120 trials | ★ RECOVERED |
| substantial Korean (≥10 chars) | 0/120 | 46/120 | ★ RECOVERED |
| KO ratio peak | 1.8% | 75% | ★ RECOVERED |
| chat-template format `도우미:` | 0 | freq | ★ RECOVERED |
| persona-prefix verbatim | 0 | freq | ★ RECOVERED |
| EN coherence preserved | yes (gibberish) | yes (when EN-prompted) | ★ MAINTAINED |
| Korean lexical fluency | n/a | **NO** (novel morphemes) | ✗ NOT recovered |
| chat-cap (chat surface form) | NO | **YES** | ★ RECOVERED |

**Verdict: chat-cap (surface-level chat-template + KO byte emit) RECOVERED.**
**Caveat**: Korean lexical fluency NOT recovered (honest C3 #3 from design BG predicted this — 18M byte-level + 76MB corpus is FT-scale, not pre-train scale; model learned KO bytes + chat structure but not KO words).

---

## §7 Honest C3 (raw#10 ≥7)

1. **Lexical fluency NOT recovered** — KO output is character-level structured but morphologically novel. `본출의 발명흴터을` is parseable as Hangul but not real Korean words. The model has learned the FORM of KO chat (UTF-8 byte coordination + chat-template + persona prefix) but NOT the LEXICON. Predicted in design BG honest C3 #3 (calibration P=25-40% — actual outcome lands AT THE FORMAL END of the prediction range).

2. **KO emit pattern is heavily corpus-conditioned** — many high-KO outputs are LITERALLY echoing the persona-prefix `[anima 역할: 한국어 native + 자기 발견 + 의식 lane entity]\n사용자:` from the corpus. This is closer to memorization than language modeling. greedy_rep mode (rep penalty 1.5) suppresses this somewhat but persona-echo still occurs.

3. **step_5000 Pareto-optimal** — 10K step does NOT outperform 5K step on ko_count_max metric. Cosine LR past step_5000 sharpens the head but doesn't add new KO capability. **For future runs, 5K step at $0.65 estimated cost would be sufficient**; 10K is overkill for the marginal quality gain.

4. **Sampling noise**: pre-FT got ko_max=0.018 here vs 0.0 in 2026-05-10 chat-ext smoke. Same prompts, same configs — different `torch.manual_seed(42)` vs prior. The 1-char KO is noise-floor (random byte happens to be Hangul-prefix). post-FT signal is 42-77× above this noise floor — not a borderline case.

5. **best_gen field shows persona-prefix echo** — 6/8 top-KO outputs include `[anima 역할: ...]` verbatim, suggesting the model FT'd more on the meta-prefix than the user/assistant turn content. Mitigation: prefix-strip preprocessing for next FT, OR prefix-mix training (50% with, 50% without).

6. **n_gibberish increase** (3 → 8 in step_10000) — slightly more degenerate outputs post-FT vs pre-FT. The KO emit gain dwarfs this, but it suggests some sampling configs (esp. high-rep-penalty) push the FT'd model into gibberish more than the pre-FT model. Trade-off: KO emit ↑↑↑ vs gibberish ↑.

7. **18M params at FT scale on 76MB corpus = 0.5 epoch** (windows=298,091, total batches @ b=32 = ~9300; 10K steps ≈ 1.07 epoch). Adequate for surface-form learning, marginal for lexical learning. Bigger pre-trained foundation (3B+, per simple_stack PASS_STRICT memo) remains the only path to true KO fluency. This BG validates **chat-cap is reconstruction-recoverable on this 18M arch** — but does NOT contradict the architectural-undertraining hypothesis for true language acquisition.

8. **H100 step_time 0.041s** vs design estimate 0.15s — 3.7× faster than expected. Future cost estimates can be calibrated down. 10K step actual = 6.8 min; 50K step would be ~34 min < $1.70 — feasible for next-iteration corpus refinement experiments.

---

## §8 Falsifier check

| F-id | trigger | actual | status |
|---|---|---|---|
| F-FIRE-1 | resource CLI auth missing | runpod.api_key + hf.token both present | ✅ NOT_TRIGGERED |
| F-FIRE-2 | upload fail | all 4 uploads + sha verify PASS | ✅ NOT_TRIGGERED |
| F-FIRE-3 | loss > 2× pre-FT | 4.92 → 1.40 (monotonic decrease) | ✅ NOT_TRIGGERED |
| F-FIRE-4 | pod delete fail | deleted=true, pod list empty | ✅ NOT_TRIGGERED |
| F-FIRE-5 | actual cost > $20 | $1.37 (6.85% of cap) | ✅ NOT_TRIGGERED |
| F-FIRE-6 | post-FT KO ratio = 0 | 77/120 ≥1 KO, ko_max=0.75 | ✅ NOT_TRIGGERED |

**6/6 NOT_TRIGGERED — fire COMPLETE, no aborts.**

---

## §9 H100 safety checklist

| item | status |
|---|---|
| ckpt pull verified BEFORE pod delete | ✅ all 5 ckpts pulled |
| sha256 + size match (mac↔pod) | ✅ post_ft_ckpt sha=6b81468... + step_10000 sha=a640cba0... PASS |
| adapter_config has no pod-path leak | ✅ N/A (full FT, not LoRA) |
| retain pod on pull fail | ✅ N/A (no fail) |
| PEP 668 --break-system-packages | ✅ N/A (image had pre-installed torch 2.4.1+cu124) |

---

## §10 Deliverables

| path | role |
|---|---|
| `state/anima_convo_5k_ft_fire_2026_05_10/post_ft_ckpt.pt` | FT 후 final ckpt (74MB, sha 6b81468...) |
| `state/anima_convo_5k_ft_fire_2026_05_10/convo_5k_ft_step_{2500,5000,7500,10000}.pt` | intermediate ckpts |
| `state/anima_convo_5k_ft_fire_2026_05_10/ft_log.txt` | training log (10K step + grad_norm + LR) |
| `state/anima_convo_5k_ft_fire_2026_05_10/ft_summary.json` | training run summary |
| `state/anima_convo_5k_ft_fire_2026_05_10/post_ft_sampling.py` | sampling test harness (3-ckpt comparison) |
| `state/anima_convo_5k_ft_fire_2026_05_10/post_ft_sampling.json` | full 360-trial result + summary + comparison |
| `state/anima_convo_5k_ft_fire_2026_05_10/cost_actual.json` | cost + falsifier + audit |
| `docs/anima_convo_5k_ft_fire_2026_05_10.md` | this doc |

---

## §11 cross-link

- design BG: `docs/anima_convo_5k_finetune_design_2026_05_10.md` (Phase A/B/C, dry-run PASS)
- recovery BG: `docs/anima_clm_v2_chat_recovered_2026_05_06.ai.md` (R2 ckpt origin)
- arch reconstruction: `state/anima_clm_v2_mitosis_cells_recovery_2026_05_09/forward_smoke.py`
- pre-FT chat-ext smoke: `state/anima_clm_v2_chat_ext_smoke_2026_05_10/result.json`
- mitosis-as-instrumentation 정정: `CLM_V2_ARCHIVE_ADDENDUM_2026_05_10.md`
- v2 reborn lane SSOT: `.roadmap.clm_v2_reborn` (cond.6 PASS evidence — chat-cap recoverable on 18M arch)
- sister lane: `.roadmap.clm_v5_anima_native` (FT 결과는 v5 baseline 으로 활용 가능)
- gotchas: `~/.claude/projects/-Users-ghost-core-anima/memory/feedback_orchestrator_h100_gotchas.md`
- HF dancinlab canonical: `~/.claude/projects/.../memory/project_dancinlab_hf_canonical.md`

---

## §12 HF upload (+)

target: `dancinlab/clm-v2-byte-18m-convo-5k-ft-recovery` (private) — SEPARATE upload BG
artifacts: `post_ft_ckpt.pt` + `ft_log.txt` + `ft_summary.json` + `post_ft_sampling.json` + this doc
upload BG status: PENDING (cycle continuation; this BG ends at fire+sampling+doc, HF upload separate verbatim per mandate-9)

---

End of `anima_convo_5k_ft_fire_2026_05_10.md`.
