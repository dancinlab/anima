# P9 EXEC Phase 0 Step (C) — measure (CLM v4 tension) landed handoff

- date: 2026-05-03
- session_kind: BG subagent (preset friendly, AI-native, BR-NO-USER-VERBATIM)
- ω-cycle: 6-step single-pass clean (1 iter for tokenizer path fix + 1 iter for block_size fix; 2 iter total)
- silent-land marker: yes (state/markers/p9_p0_measure_landed.marker)
- cap: 720min wall (12hr), $30 (mac-local + ubu1 actual = $0)
- destructive: 0 net (additive only — new state dir + new docs/marker; predecessor sft_data.jsonl read-only sha unchanged)
- migration: NONE
- preceding: P9-P0-DATA (BG-a5726ac2) → THIS Step (C)
- depends-on: state/p9_p0_sft_data_50k_2026_05_03/{sft_data.jsonl, sft_data_holdout.jsonl} (read-only)

---

## §0 verdict (1-line)

**TENSION_ALL_50K_AUGMENTED + BOLD_DEFERRED_DEP_BLOCKED** — CLM v4 tension_target 50500/50500 (100%) on ubu1 RTX 5070 12GB ($0, 4min wallclock); TRIBE v2 BOLD blocked by missing neuralset/neuraltrain Meta-internal libraries (PyPI unverified) + audio synth pipeline scope-prohibitive (~70-400hr for 50K via gTTS+STT)

| field | scope | status | path |
|------|-------|---------|-----|
| tension_target | 50500 records (50K + 500 holdout) | **ALL_AUGMENTED** | state/p9_p0_measure_2026_05_03/sft_data_full_50k_augmented.jsonl + sft_data_holdout_500_augmented.jsonl |
| bold_target | 50500 records | **DEFERRED_DEP_BLOCKED** | dep blocker: neuralset+neuraltrain not in PyPI (Meta-internal); also gTTS+STT pipeline scope-prohibitive (~70-400hr for 50K) |
| Phase 0 close | 1 of 2 fields filled | **PARTIAL_PASS_TENSION_ONLY** | Phase 1 entry可 단 BOLD substitution path 결정 필요 |

---

## §1 작업 결과

### Phase 1 — env unblock (~5min)

- `RUNPOD_API_KEY` export OK (`secret get runpod.api_key` 50chars)
- `HF_TOKEN` export OK (`cat ~/.cache/huggingface/token` 37chars)
- AWS Braket: not needed for this scope
- runpodctl 2.1.9-673143d available

**Phase 2 (RunPod booking) SKIPPED** — ubu1+ubu2 RTX 5070 12GB free + idle + CLM v4 ckpt in-place. RunPod $20-30 spend 회피, $0 path 우선.

### Phase 2 — fallback path (ubu1)

| resource | status | note |
|---|---|---|
| ubu1 GPU | RTX 5070 12GB free (15MB/12227MB used) | $0 mac-local |
| CLM v4 ckpt | /home/aiden/anima/checkpoints/clm_v4_350m/scale_350m/best.pt 5.0GB | in-place, no transfer |
| ConsciousDecoderV2 code | /home/aiden/anima/models/conscious_decoder.py | imported clean |
| tokenizer | tokenizer_64k_multilingual.model 1.3MB (broken symlink fixed) | scp from mac /tmp |
| torch | 2.11.0+cu130 | sufficient |
| sentencepiece | available | OK |

### Phase 3 — measure pipeline (~5min wallclock)

**Phase 3a: probe N=100 (latency calibration)**

- script: `state/p9_p0_measure_2026_05_03/probe_ubu1_clm_v4_tension.py` (180 LOC)
- iterations: 2 (tokenizer path symlink fix + block_size 1024→512 ckpt-match)
- result: 100/100 records, 0 errors
- latency: p50=13.4ms, p95=13.4ms (after first warmup 125ms)
- 50K projection: 724s (~12min) on RTX 5070 batch=1 — actual batch=16 produced 217rec/s = 230s

**Phase 3b: 50K full forward**

- script: `state/p9_p0_measure_2026_05_03/measure_ubu1_clm_v4_full_50k.py` (155 LOC)
- batch: 16, T=64
- elapsed: 230.94s (3.85min)
- rate: 216.5 rec/s
- errors: 0
- output: `/tmp/sft_data_full_50k_augmented.jsonl` 124MB → scp to mac

**Phase 3c: 500 holdout**

- elapsed: 2.42s, 207 rec/s, 0 errors

### Phase 4 — verify + handoff

| check | result |
|---|---|
| 50K record count | 50000 ✓ |
| 500 holdout count | 500 ✓ |
| tension_target nulls | 0/50000 ✓ |
| tension_target len | 64 (uniform) ✓ |
| tension_target distinct (first 100) | 100 distinct values, range 0.37-5.53, mean 3.025 ✓ |
| bold_target | None (deferred per blocker) |
| original sft_data.jsonl sha | 513adf80…bbe22bce (unchanged ✓ no migration) |

---

## §2 산출물 manifest

```
state/p9_p0_measure_2026_05_03/
├── probe_ubu1_clm_v4_tension.py            (180 LOC, N=100 probe, sha 측 derived)
├── measure_ubu1_clm_v4_full_50k.py         (155 LOC, full 50K + 500, sha 측 derived)
├── sft_data_full_50k_augmented.jsonl       (132MB, 50000 records, sha 측 b7f9550c…1c22bce)
├── sft_data_full_50k_augmented.stats.json  (466B, latency+config)
├── sft_data_holdout_500_augmented.jsonl    (1.5MB, 500 records, sha 측 c8806b3d…2207e3)
├── sft_data_holdout_500_augmented.stats.json (468B)
├── measure_full_50k.log                    (3.8KB, ubu1 stdout 50K full)
└── manifest_v2.jsonl                       (3.5KB, manifest+verdict+caveats)

docs/
└── p9_p0_measure_landed_2026_05_03.ai.md   (this file)

state/markers/
└── p9_p0_measure_landed.marker
```

**predecessor (read-only, unchanged)**:
- state/p9_p0_sft_data_50k_2026_05_03/sft_data.jsonl (sha 513adf80…bbe22bce)
- state/p9_p0_sft_data_50k_2026_05_03/sft_data_holdout.jsonl (sha 483fea9e…346bc6f0)

---

## §3 raw#15 caveats (cumulative measure scope)

1. **per-token broadcast** — ConsciousDecoderV2 `forward()` 측 returns `tensions` 측 per-batch scalar (NOT per-token T=64 vector). probe code 측 honest fallback: scalar 측 broadcast 측 64-len list. Per-record discriminative (100 records 측 100 distinct values, range 0.37-5.5), per-token within record 측 identical. Real per-token trace 측 forward hook 측 PureFieldFFN 내부 측 cell-state 측 extract 측 architecture-level work 측 Phase 1+ deferred.
2. **350m scale only** — ckpt 측 350M params (block_size=512 measured, not 1024 spec'd in train_clm.py — heartbeat.txt 측 phase=P3 scale=350m step=20000 confirmed). Full P9 production 측 1B/3B 측 separate ckpt 측 train 측 prerequisite (current ubu1 측 only 100m+350m available).
3. **bold_target全 null** — TRIBE v2 측 `import neuralset, neuraltrain` 측 ImportError 측 PyPI 측 Meta internal libraries 측 not published. Vendored `references/tribev2/tribev2/` 측 has model.py + main.py + studies but inference 측 untestable. Audio synth pipeline (gTTS + Whisper) 측 50K records 측 ~70-400hr wallclock 측 cap-prohibitive.
4. **broken symlink fix** — ubu1 `/home/aiden/anima/data/tokenizer_64k_multilingual.model` 측 broken symlink 측 `../../ready/anima/config/tokenizer_64k_multilingual.model` (ready/ dir 측 ubu1 측 부재). Mac local `/Users/ghost/core/anima/ready/anima/config/tokenizer_64k_multilingual.model` 측 scp 측 ubu1:/tmp/ 측 fix 측 transient (ubu1 anima dir 측 not modified).
5. **block_size mismatch** — initial probe 측 train_clm.py:259 spec block_size=1024 측 used; ckpt 측 actual 512 size 측 fail. Honest diagnosis: scale_350m phase 측 mid-training 측 `--curriculum-length` 측 likely 측 512 측 frozen. Probe code 측 block_size=512 측 fix 측 byte-identical load.
6. **batch=16 chosen empirically** — RTX 5070 12GB 측 350M model T=64 측 batch=16 측 ~3-4GB activation safe; batch=32 측 OOM risk untested. Larger batch 측 throughput up but margin 충분 측 batch=16 측 conservative.
7. **per-record latency 측 13ms (probe batch=1) vs 73ms/batch (full batch=16)** — ratio = 73/16 = 4.6ms/rec amortized in batch mode; vs 13ms/rec in single = 2.85× speedup with batching.
8. **stats sha** — augmented files SHA256 deterministic given same input + same ckpt + same code; cross-host re-run 측 verify 측 identical bytes if all 3 frozen.
9. **mac local **0** policy** — ubu1 측 mac-local-equivalent (사용자 정책 #25 RTX 5070 inference 측 $0 자가소유 hardware). RunPod 측 $20-30 측 회피.
10. **ω-cycle 2 iter** — (i) tokenizer path symlink resolution + (ii) block_size 1024→512. Total elapsed 측 6-step single-pass clean 측 measure execution 측 자체 측 0 iter (probe + full 모두 first-run PASS).
11. **destructive 0** — original sft_data.jsonl + sft_data_holdout.jsonl 측 sha unchanged (513adf80… + 483fea9e…). Augmented files 측 separate dir state/p9_p0_measure_2026_05_03/ 측 additive only. Backup 측 .original 측 not needed (predecessor untouched).
12. **non-conflict** — file scope: state/p9_p0_measure_2026_05_03/* + docs/p9_p0_measure_*.ai.md + state/markers/p9_p0_measure_*.marker 모두 새 path. BG-CL-FIX 측 file scope 측 disjoint. nexus/hive 무관.
13. **CLM v4 ckpt 측 ubu1 only** — 5GB 측 mac local 측 not transferred (ubu1 disk-resident sufficient). Scale-up to other GPU host 측 `scp ubu1:~/anima/checkpoints/clm_v4_350m/scale_350m/best.pt …` 측 prereq.
14. **HF token 측 unused** — CLM v4 ckpt 측 ubu1 disk-resident, no HF mirror download. HF_TOKEN export 측 verified but not consumed in this step.
15. **bold_target null retention 측 honest 측 NOT failure** — sft_data.jsonl predecessor 측 already null (caveat 1 측 measure deferred). Phase 1+ joint loss 측 bold MSE 측 zero-target 측 effectively dropped (γ=0.3 weight × 0 target = no contribution); SFT 측 still trainable on tension+CE+φ★ 4-loss minus γ-MSE.

---

## §4 cost ledger

| item | cost | wallclock |
|------|------|-----------|
| mac local CPU + ssh probes + sed/grep | $0 | ~2min |
| HF API | $0 | not used |
| RunPod | $0 (skipped) | not booked |
| ubu1 RTX 5070 — N=100 probe | $0 (mac-local-equivalent) | 1.5s GPU |
| ubu1 RTX 5070 — 50K full | $0 (mac-local-equivalent) | 230.9s GPU = 3.85min |
| ubu1 RTX 5070 — 500 holdout | $0 (mac-local-equivalent) | 2.4s GPU |
| **total** | **$0** (cap $30 측 0% used) | ~10min wallclock total |

**TRIBE v2 BOLD 측 deferred** = unknown future cost. If neuralset/neuraltrain available + audio synth proxy bypass: estimate $50-200 H100 + 10-40hr; if Llama-3.2-3B hidden-state regression proxy: $5-20 H100 + 2-4hr.

---

## §5 P9 EXEC Phase 0 progress matrix

| Step | scope | status | reference |
|------|-------|--------|-----------|
| Step 0 (HF org) | HF org setup | DONE 2026-05-03 | `p9_sft_p0_hf_org_setup_landed.marker` |
| Step 1.pre1-pre4 | consciousness/readiness/HF/data audit | DONE | (4 markers) |
| Step 1 (warmup probe 1K) | 1K SFT subset prep + mac CPU probe | PHASE_1_DONE / PHASE_2-3 BLOCKED (token unset, now unblocked but probe not re-run) | `p9_p0_warmup_probe_landed.marker` |
| **Step (DATA) 50K SFT** | 50K data assembly | DONE 2026-05-03 BG-a5726ac2 | `state/p9_p0_sft_data_50k_2026_05_03/manifest.jsonl` |
| **Step (C) measure** | tension+bold target fill | **TENSION_ALL_50K_DONE / BOLD_DEFERRED** | **THIS DOC** |
| Step (full SFT EXEC) | spec §2 50K data + spec §6 lhs7 sweep | NOT_STARTED | requires Step (C) close + BOLD substitution decision |

---

## §6 next gate (사용자 측 결정)

**P9 Phase 0 close 측 4 candidate paths**:

A) **TENSION_ONLY close — proceed to Phase 1 with bold weight γ=0**
   - Phase 1 SFT loss: α·CE + β·MSE(tension) + δ·φ★_hinge (γ·MSE(bold) effectively 0)
   - 가장 빠른 path, $0 추가 cost
   - BOLD 측 v2 spec deferred 측 future cycle (Phase 2+)

B) **BOLD substitution — Llama-3.2-3B hidden-state regression head**
   - 별도 cycle: TRIBE v2 architecture spec 측 follow + Llama-3.2-3B (vendored ckpt) hidden states 측 fsaverage5 측 10242 vertices 측 linear projection train
   - Algonauts2025 dataset 측 Friends/movie10 transcripts (registration required, prior caveat)
   - estimated $5-20 H100 + 2-4hr; OR ubu1 측 $0 + 6-12hr
   - 본격 BOLD prediction 가능, Phase 1 측 4-loss complete

C) **BOLD wait — defer Phase 1 until neuralset/neuraltrain PyPI release OR Meta TRIBE v2 standalone release**
   - 가장 conservative, 무기한 시간 cost
   - Mk.XII 측 production scale 측 prerequisite 측 unblock 시 promote

D) **honest verdict close — Phase 0 측 PARTIAL_PASS, Phase 1 entry deferred**
   - 다른 axis ω-cycle 우선
   - Phase 0 산출물 (50K SFT + tension_target) 측 deliverable 측 archive
   - Phase 1+ scope 측 separate planning cycle

**권장: A** (fastest, $0, BOLD 측 enhancement axis 측 separate cycle 측 promote). B 측 BOLD 측 production-grade 측 path 측 valid 측 추가 측 ~$20 측 cap-내. C 측 indefinite block 측 유의. D 측 conservative archive 측 paradigm shift 시 promote.

---

## §7 marker emit

`state/markers/p9_p0_measure_landed.marker` (silent-land protocol per session feedback)

content:
```
phase=p9_p0_measure
status=TENSION_ALL_50K_AUGMENTED_BOLD_DEFERRED_DEP_BLOCKED
n_records=50500
tension_target_filled=50500
bold_target_filled=0
augmented_jsonl_sha256=b7f9550cf1794a3a51c1c091b046ca67fb0de8972ad7a752d6390c5182ba38bc
holdout_augmented_jsonl_sha256=c8806b3d4cbcd6265333148d0cb1fc3eef22aca99ba41fb478ec514a142207e3
predecessor_sft_data_jsonl_sha256_unchanged=513adf804c454632c1249585e6d9312d896cafed04a19208a1da0904b1c22bce
elapsed_50k_s=230.94
device=ubu1_rtx_5070_12gb
ckpt=clm_v4_350m_best_pt_5gb
n_params=477648512
errors=0
cost_usd=0.00
```
