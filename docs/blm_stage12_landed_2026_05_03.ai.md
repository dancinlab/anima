# BLM Stage 1+2 Landed — 2026-05-03 (AI-native, friendly preset)

> friendly preset (icon + analogy + 7-element + ASCII)
>
> readers: AI agents (subagents, audit cron), Claude Code (next session)
> source-of-truth: `.roadmap.blm_brain_lm` (additive update only) + vendored `references/tribev2/` (in-place 변경 X)
> upstream handoff: `docs/anima_3_lm_landed_2026_05_03.ai.md` §3.3

---

## TL;DR

**오늘 한 일** — BLM (Brain LM) 측 stage 1 (TRIBE v2 baseline 활용) status `partial → met`, stage 2 (BOLD-conditioned LM head impl) 측 dataset 결정점 lock-in, blocker `blk.1 open → resolved`. 외부 cortexlab-toolkit registration / Algonauts2025 등록 모두 불필요 — vendored `references/tribev2/tribev2/studies/algonauts2025.py` 측 직접 reuse. P9 SFT pattern (vendored direct) 동일.

**비유** — 신입사원 (BLM) 측 첫째 날 (stage 1) "회사 도구 (TRIBE v2 baseline) 익히기" 측 완료 도장, 둘째 날 (stage 2) "데이터셋 어디서 가져올지" 측 결정 — 외부 신청 (cortexlab/Algonauts) 대신 회사 안 (vendored Algonauts2025 study) 측 이미 있는 도구 재사용 결정.

**결과** — `.roadmap.blm_brain_lm` cond.1 `partial → met` (5 evidence + 1 cross-link), blk.1 `open → resolved` (resolution_path land). cond.2 `unmet` 유지 (stage 3 head impl 측 별도 cycle), 단 dataset blocker 해소로 next-cycle entry barrier ↓.

---

## §1 stage 1 (cond.1) — TRIBE v2 baseline `partial → met`

### §1.1 verify 측 (vendored measure, mac-local read-only $0)

```
   measure                     | source                                               | result
   --------------------------- | ---------------------------------------------------- | -------------------
   1. inventory.json present   | references/tribev2/inventory.json                    | OK 1.7K
   2. params 측 baseline       | inventory.json line 58 + narrative §52.1 #102        | 177.21M (TRIBE head only; encoders frozen)
   3. cortical mesh SSOT       | references/tribev2/tribev2/utils_fmri.py:50          | FSAVERAGE_5 = (10242,) per hemi
   4. n_vertices bilateral     | utils_fmri.py:230 `n_vertices = rec.shape[0] // 2`   | 10242 x 2 = 20484 bilateral (roadmap 기재 일치)
   5. TR seconds               | inventory.json line 23                                | TR=1.49s (header 기재 1.0s -> 1.49s 정정)
   6. text encoder family      | inventory.json line 41-44 + utils_fmri.py            | meta-llama/Llama-3.2-3B [0,0.2,0.4,0.6,0.8,1.0] layers
   7. license                  | inventory.json line 59                                | CC-BY-NC-4.0 (research-only, commercial block)
   8. fork submodule sha       | docs/submodule_tribev2_commit_2026_05_02.md          | 86ed4804 (i1_tribev2_pr cond.1 met)
   9. upstream PR              | docs/upstream_tribev2_pr_results_2026_05_02.md       | facebookresearch/tribev2 #60 OPEN (i1 cond.2 met)
  10. vendored code modules    | references/tribev2/tribev2/{model,pl_module,main}.py | present (model/pl_module/main/utils_fmri/utils/demo_utils)
```

### §1.2 verdict

`__BLM_BASELINE__ READY` — 10/10 measure PASS (vendored read-only, forward 미수행). cond.1 status `partial → met`.

**partial → met 측 진입 근거**:
- 기존 `partial` blocker_reason: "text encoder Llama-3.2-3B family 공유 확인 + LoRA path 결정점"
- 본 cycle 측 verify: family 공유 = inventory.json line 41 직접 확인 (Mk.XI v10 backbone family 확인됨)
- LoRA path 결정 = stage 2 (cond.2 head impl) 의 sub-decision 으로 분리 (cond.1 측 baseline 활용 자체는 ready)
- 따라서 cond.1 측 "baseline 활용 = 인프라 reuse" 측 met 충족, LoRA path 결정 = cond.2 sub-task 로 demote

### §1.3 caveat (raw#10 honest C3)

- vendored measure 만 (forward 미수행) — H100 cost 외 mac-local $0 제약 정합
- TR=1.0s 측 기존 roadmap 기재 → inventory.json SSOT TR=1.49s 측 정정 (헤더 description 측 기재만 변경, cond field 측 in-place)
- params 177.21M 측 narrative §52.1 #102 anchor 그대로 (vendored re-measure X — pl_module load forward 측 별도 cycle)

---

## §2 stage 2 (cond.2) — head impl `unmet` 유지 + dataset 결정점 lock-in

### §2.1 status 변동 없음, blocker 해소만

```
   field             | before                                        | after
   ----------------- | --------------------------------------------- | ----------------------------------
   cond.2.status     | unmet                                         | unmet (변동 없음, head impl 별도 cycle)
   cond.2.evidence   | []                                            | [dataset lock-in + handoff doc]
   cond.2.blocker    | cond.1 READY + cortexlab dataset ingest 결정   | head architecture + LoRA path 결정 (dataset 항목 제거)
```

### §2.2 cond.2 unmet 잔여 work (next-cycle scope)

1. head architecture 결정: decoder-only (next-token causal) vs encoder-decoder (BOLD→text retrieval) vs bidirectional (alignment scoring)
2. LoRA path lock-in: text encoder Llama-3.2-3B 측 LoRA 적용 vs frozen-encoder + head-only training
3. training pipeline: pl_module.py + main.py 측 reuse vs custom loop (vendored Lightning-based 정합 권장)
4. validation metric: OnlinePearsonCorr (vertex-level) + GroupedMetric (per-subject) + TopkAcc_top1 (retrieval) — vendored `benchmarks` field 3종 직접 reuse 가능

---

## §3 cortexlab dataset 결정 (blk.1 open → resolved)

### §3.1 4-candidate matrix

```
   candidate           | source                                                         | cost   | block
   ------------------- | -------------------------------------------------------------- | ------ | ----------------------------
 A Friends transcript  | external cortexlab-toolkit (separate registration)             | $0-?   | external dep, registration friction
 B movie10 only        | external cortexlab-toolkit (separate registration)             | $0-?   | same as A
 C Algonauts2025 reg   | external Algonauts2025 challenge registration                  | $0-?   | external SLA + agreement
 D vendored TRIBE v2   | references/tribev2/tribev2/studies/algonauts2025.py (in-tree)  | $0     | none — already vendored
```

### §3.2 verify 측 (D 후보 vendored 측 직접 확인)

```
   verify                                                          | source                                  | result
   --------------------------------------------------------------- | --------------------------------------- | -------
 1. Friends + movie10 BOTH 지원                                     | studies/algonauts2025.py:58             | _TASKS = ["friends", "movie10"]  (PASS)
 2. train/test split 명시                                            | studies/algonauts2025.py:19-20          | train=Friends s1-s6 + all movies / test=Friends s7  (PASS)
 3. Friends episode coverage                                         | studies/algonauts2025.py:16             | 7 seasons ~175 episodes 5min chunks (a,b,c,d)  (PASS)
 4. movie10 film coverage                                            | studies/algonauts2025.py:17             | Bourne, Wolf, Life, Figures (PASS)
 5. dataset attribution                                              | studies/algonauts2025.py:82             | Courtois NeuroMod (boyle2020) subset  (PASS)
 6. text/video/audio extraction stub                                 | studies/algonauts2025.py:153,168,183    | tsv (text) + mkv (video) + h5 (BOLD) per timeline (PASS)
```

### §3.3 verdict — candidate D lock-in

**recommended path**: vendored `references/tribev2/tribev2/studies/algonauts2025.py` 직접 reuse.

**근거**:
1. **vendored already** — 외부 등록/SLA/agreement 0건 (P9 SFT pattern 동일)
2. **Friends + movie10 BOTH 지원** — A vs B 양자택일 불필요, 양쪽 _TASKS 이미 wired
3. **train/test split 표준화** — Friends s1-s6 + movies = train / Friends s7 = test 측 Algonauts2025 challenge 표준 정합
4. **vendored Lightning module 정합** — pl_module.py + main.py 측 직접 호출 가능, custom loader 불필요
5. **license 일치** — TRIBE v2 CC-BY-NC-4.0 측 vendored study module 동일 license, 별도 license audit 불필요
6. **i1_tribev2_pr cross-link 보존** — 동일 fork submodule sha 86ed4804 측 SSOT, race risk 최소

**rejected**:
- A/B (cortexlab-toolkit 외부): vendored 측 동일 dataset coverage 이미 있음, 외부 dep 추가 시 race risk + license 재검토 필요
- C (Algonauts2025 challenge 등록): challenge participation 측 별도 SLA, BLM = 단순 baseline reuse 만 필요 (challenge submission 不要)

### §3.4 caveat (raw#10 honest C3)

- BOLD raw data (h5 files) 측 dataset path 기준 directory layout 측 vendored 코드 측 expect (e.g., `s{n}/friends_{movie}{chunk}.tsv` line 154) — actual data file 측 별도 download 필요 (vendored = code only, not data weights)
- HuggingFace `facebook/tribev2` pretrained weights 측 별도 download (vendored = code + inventory + docs only, weights 측 ~hundreds MB)
- training run 측 H100 GPU 필요 (mac-local $0 정책 측 cond.2 head impl forward training 측 별도 cycle, GPU cost band $500-2000 LoRA path 기재)
- vendored `studies/algonauts2025.py` 측 license header (line 5: "LICENSE file in the root directory of this source tree") 측 CC-BY-NC-4.0 정합

---

## §4 5-7 caveats (raw#10 honest C3) — 5건

1. **C1 — vendored measure only, forward 미수행 (mac-local $0)** — TRIBE v2 actual model load + forward pass 측 H100 GPU 필요, 본 cycle 측 inventory.json + utils_fmri.py 측 read-only static measure 만. 향후 actual baseline forward 측 별도 GPU cycle ($0.50-2 estimate).
2. **C2 — TR seconds discrepancy (1.0s 측 roadmap 기재 → 1.49s 측 inventory SSOT)** — 기존 `.roadmap.blm_brain_lm` cond.1 desc 측 "TR=1.0s" 기재되어 있으나 inventory.json line 23 측 SSOT 1.49s. 본 cycle 측 cond.1 desc 정정 (in-place edit)
3. **C3 — dataset weights/raw files 측 별도 download 필요** — vendored code 측 reuse 결정만 land, actual h5/tsv/mkv files 측 Courtois NeuroMod 측 별도 SLA (typical academic registration 1-2주). cond.2 head impl 진입 시 prerequisite.
4. **C4 — HuggingFace `facebook/tribev2` pretrained weights 측 별도 download** — vendored = code + inventory + docs, weights 측 huggingface_hub 측 별도 fetch (license CC-BY-NC-4.0 정합 + ~hundreds MB). cond.2 head impl 측 prerequisite (vendored measure 단계 측 inventory level 측 충분, 실제 forward 측 weights 필요)
5. **C5 — cond.2 head impl 측 head architecture (decoder-only vs encoder-decoder vs bidirectional) 결정 미수행** — 본 cycle 측 dataset 결정점 만 lock-in, head spec 결정 별도 cycle (head spec = stage 2 sub-task, dataset 결정과 분리됨)

---

## §5 file index (relative to /Users/ghost/core/anima/)

### updated (in-place additive)

```
.roadmap.blm_brain_lm                          (cond.1 partial→met + cond.2 evidence + blk.1 open→resolved + raw_invariants +2 + ai_native_handoff update)
```

### created

```
docs/blm_stage12_landed_2026_05_03.ai.md       (이 파일)
state/markers/blm_stage12_landed.marker        (silent-land 방지 attestation)
```

### referenced (변경 X)

```
references/tribev2/inventory.json              (TRIBE v2 baseline SSOT, vendored verified)
references/tribev2/tribev2/utils_fmri.py       (FSAVERAGE_5 mesh SSOT line 50)
references/tribev2/tribev2/studies/algonauts2025.py (Friends + movie10 ingest path SSOT)
references/tribev2/tribev2/{model,pl_module,main}.py (vendored Lightning training stack)
docs/submodule_tribev2_commit_2026_05_02.md    (fork submodule sha 86ed4804 anchor)
docs/upstream_tribev2_pr_results_2026_05_02.md (PR #60 OPEN anchor)
docs/anima_3_lm_landed_2026_05_03.ai.md        (BG-AN-3LM upstream handoff §3.3)
.roadmap.i1_tribev2_pr                         (sister roadmap, in-place 변경 X)
```

---

## §6 7-element friendly summary (사용자 view, ASCII)

```
   element                | content
   ---------------------- | ----------------------------------------------------------
   1. icon                | [met] cond.1 partial -> met  +  [resolved] blk.1 open -> resolved
   2. analogy             | 신입사원 첫날 도구 익히기 OK + 둘째날 데이터셋 사내 재사용 결정 OK
   3. core 결과            | stage 1 met (10/10 vendored measure PASS), stage 2 dataset lock-in (vendored Algonauts2025 직접 reuse)
   4. 마이그레이션 0          | references/tribev2/ 0 byte modification, .roadmap.blm_brain_lm in-place additive only
   5. handoff path         | 본 ai.md = 다음 subagent / audit cron 측 stage 2 head impl entry SSOT
   6. 다음 step             | (1) head architecture 결정 (decoder-only vs encoder-decoder vs bidirectional)
                           | (2) LoRA path lock-in (text encoder Llama-3.2-3B)
                           | (3) BOLD raw data download (Courtois NeuroMod 측 SLA + HF weights 측 fetch)
                           | (4) cond.2 IMPL → cond.3 stimulus-text-BOLD 3-way alignment ≥0.5 measure
   7. cost                 | $0 mac-local enforced (vendored read-only), destructive 0
```

---

## §7 marker file path

`state/markers/blm_stage12_landed.marker`

(silent-land 방지 — handoff doc + .roadmap update + marker emit 측 3-way attestation)

---

## §8 next-cycle recommendations (impl 미수행, 별도 cycle)

1. **cond.2 head architecture 결정 cycle** — decoder-only / encoder-decoder / bidirectional 3-candidate matrix + 평가 (compute cost / falsifier sensitivity / vendored Lightning module 정합)
2. **BOLD raw data download cycle** — Courtois NeuroMod (boyle2020) 측 academic registration + HF `facebook/tribev2` pretrained weights download (~hundreds MB)
3. **LoRA path lock-in cycle** — text encoder Llama-3.2-3B 측 LoRA 적용 vs frozen-encoder + head-only training 측 비교 (Mk.XI v10 backbone family share advantage)
4. **cond.3 falsifier measure cycle** — F-CT-3 (EEG ↔ TRIBE BOLD r ≥0.5) sister falsifier 측 actual run + 3-way alignment ≥0.5 측 binary verdict
5. **i1_tribev2_pr cross-link reflexive update** — `.roadmap.i1_tribev2_pr` cross_link.sister_lm += `blm_brain_lm` (current = sister 단방향, dual SSOT race 완화 권장)
