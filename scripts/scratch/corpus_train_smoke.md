# corpus → trainer pipeline SMOKE ($0, CPU, no GPU rent)

De-risks the eventual **cost-gated 7B GPU fire** on `dancinlab/anima-corpus-5lang-7b-webscale`
by proving the **data → trainer plumbing** end-to-end on a TINY slice, $0, local CPU.

Run: `python3 scripts/scratch/corpus_train_smoke.py`
(R2 creds read INLINE from the secret store `r2.phanes.*`, header-only, NEVER hardcoded — c7.)

## Result — all 3 steps PASS · GREEN-LIGHT: YES

### Step 1 — R2 reachable + manifest match ✅
- Bucket `phanes`, prefix `anima-7b/web/`: **21 objects = 20 `.bytes` shards + `MANIFEST.json`**.
- Live-listed byte sum = R2-`MANIFEST.json` per-shard sum = **154,187,454,007 B = 143.60 GiB** —
  matches the HF corpus card exactly (143.60 GiB · 20 shards · 22.0 tok/param).
- Per-lang shards: `en 8 · fr 3 · de 3 · es 3 · ko 3` (matches manifest).
- Note: the **R2 `MANIFEST.json` is a lean schema** (`total_gb · tok_per_param_7b · shards · manifest[]`);
  the HF-repo `serving/corpus/anima_7b_webscale_MANIFEST.json` is a superset (adds `total_bytes`,
  `per_lang`, …). The load-bearing shared part — the per-shard `key/bytes/sha256` array — is identical.

### Step 2 — tiny-slice real byte text ✅
- Partial-object **Range GET** of first **8 MB** of `anima-7b/web/kor/shard0000.bytes` (Korean, ko).
- 193/256 distinct byte values; **81.1% high bytes** (multibyte UTF-8); **Hangul (가-힣) present**.
- **Control bytes 0xFE / 0xFF: both ABSENT** → confirms the card's "stripped → V=256" claim.
- **PII scrub markers present**: `[EMAIL]`=212, `[PHONE]`=562 (expected scrub tokens, not raw PII).
- Sample lines decode as real Korean + English web text (public-domain image page, Hangul caption).

### Step 3 — trainer glue (data → tok → batch → forward → loss-drop → ckpt) ✅
- Byte-tokenized 8 MB slice (V=256, no tokenizer) → batches → forward → **CE dropped
  5.5452 (uniform ln256) → 5.4406** over 40 steps → checkpoint written.
- **Mode = LABELED numpy byte-LM PROXY** (not the production CLMConvMoE). The proxy exercises the
  SAME data → loader → CE-descent → checkpoint glue; it is NOT the production architecture.
- **HONEST**: the production trainer `CLM/train/train_lane_p.py` **imports torch and asserts
  `torch.cuda.is_available()` (g63: no silent CPU)** — it is a **GPU-ONLY Lane-P path**. The forge
  `.hexa` trainers (`a_train_flame_forge`) likewise **require GPU**. **Neither is CPU-smokeable**
  on this $0 host (torch is not even installed locally). The proxy therefore validates the
  **R2 → byte-stream → loader → loss → ckpt plumbing**, NOT the CLMConvMoE forward itself.
  If run on a torch+CUDA host, the script auto-switches to the **REAL CLMConvMoE** forward/loss path.

## Cost / feasibility ESTIMATE for the eventual GPU fire (NOT measured)

Assumptions: 6·N·D FLOPs, 1 epoch over **D = 154.2 B byte-tokens**, H100 SXM BF16 peak
**989 TFLOP/s @ 40% MFU**, **$2.0–3.5 / H100-hr**. R2 egress = **FREE** (Cloudflare).

| rung | N | 6ND FLOPs | 1×H100 wall | 8×H100 wall | $ range (8×) |
|---|---:|---:|---:|---:|---:|
| 303M | 303 M | 2.80e20 | 8.2 d | 24.6 h | $394–689 |
| 1B | 1.0 B | 9.25e20 | 27.1 d | 3.4 d | $1,299–2,274 |
| 3B | 3.0 B | 2.78e21 | 81.2 d | 10.1 d | $3,898–6,821 |
| 7B | 7.0 B | 6.48e21 | 189.5 d | 23.7 d | $9,094–15,915 |

> **ESTIMATE only** — wall/$ scale ~linearly with MFU and GPU count; more parallel H100s shorten
> wall time at ~constant total $ (`a_wall_first`). The 303M rung is the cheap first real-corpus
> checkpoint (sub-$1k, ~1 day on 8×H100). Full 7B at 1 epoch is a multi-thousand-$, multi-week fire.

## GREEN-LIGHT

Pipeline plumbing is **READY for a cost-gated GPU fire**: R2 auth + streaming works, bytes are real
V=256 text matching the manifest, and the data→loader→loss→ckpt glue runs. **Recommended single next
rung: 303M on the real 143.6 GiB corpus** (cheapest real-corpus checkpoint; validates the full
forge/Lane-P GPU path + R2 streaming at scale before committing to 3B/7B). The forge GPU forward path
itself remains un-smoked here (GPU-only) — first real fire doubles as its first end-to-end test.

c7: 0 secret leakage (creds via `harness secret get` inline, header-only; grep-clean).
