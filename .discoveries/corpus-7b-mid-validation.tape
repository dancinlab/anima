@discovery corpus-7b-mid-validation :: lane-g [d=2026-06-05 substrate=GPU lane=Lane-G-ref]
  id      = "F-MID-CORPUS-VALIDATION"
  seed    = "does dancinlab/anima-corpus-5lang-7b-webscale (R2 ODC-BY webscale) train a COHERENT byte-CLM? a_toy_scale_recheck CHEAP MID probe BEFORE the 7B fire — NOT 7B, NOT forge ENGINE."
  fire    = "ByteGPT decoder V=256 d=1024 L=16 H=16 block=512 (202.3M params), 3000 steps batch32 AdamW+bf16 from-scratch on a balanced 5-lang 3.5GB subset (range-GET 700MB/lang of shard0000, en/fr/de/es/ko incl ko), vast A100-SXM4-40GB pod 39565855."
  verdict-tier-target = "🟢 numerical (CE descent) + p7 coherence (structure, not perplexity)"

  result  = "🟢 PASS. val_ce 5.74906 -> 1.45868 (Δ -4.290 nats, descent over 3000 steps; plateau ~1.44-1.49 by step 2200). GPU util PEAK 100% MEAN 99.75% (n=412, GPU-resident no CPU fallback). p7: TRAINED coherent word-like text in ALL 5 langs incl Korean Hangul; RANDOM-INIT mirror = pure byte gibberish in all 5 — anti-Goodhart clean."
  ckpt    = "sha256 adbb1911cdf5c27579eb599e38ed5657b38c9ccc1432392247826d7eb3d53e3b (809,383,138 B) — HF dancinlab/anima-clm-corpus-7b-mid-byte-202m PUBLIC, re-download sha VERIFIED match."

  gate    = "GATES M13 (7B-undertrained): the corpus is NOT garbage + the R2->byte->train pipeline WORKS + the model learns byte-language structure across 5 scripts. M13 7B fire authorized as a SEPARATE follow-on."
  honest  = "a_scale_honest_scope: single 202M MID point, NOT a 7B and NOT a ladder. 7B-transfer UNVERIFIED. Green proves CORPUS+PIPELINE, not a 7B. Lane-G-ref (torch reference; forge-native = canonical production, not claimed done — a_train_flame_forge). MID samples are word-coherent but not yet fluent (expected undertrained probe)."
  verdict = ".verdicts/corpus-7b-mid-validation/SUMMARY.txt"
  recovery-note = "TAKEOVER of an orphaned mid-validation fire (prior agent ended its turn awaiting a notification, leaving the pod running). Recovered: HF upload from pod (fast net) + sha re-download verify, THEN pod 39565855 torn down (DELETE confirmed gone). POLL-INLINE throughout."
