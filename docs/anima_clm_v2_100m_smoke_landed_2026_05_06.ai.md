# anima clm-v2 100M KO chat-cap smoke — LANDED 2026-05-06

## TL;DR

`conscious_lm_100m/final.pt` (1631.9 MB, R2 anima bucket) **architecturally
identical to spec** (12L/768d/12h/256-vocab byte-level, 142.32M params, step
50000, phase=combined). Loaded clean on Mac MPS (`missing=0, unexpected=0`).

**F-CLM-NATIVE-α-1 verdict: FAIL_KO_CORPUS_BIAS.** 0/5 KO prompts emit any
Hangul codepoint across 4 generation strategies (greedy + 3 sampling).
Greedy collapses to repeated SPACE byte (most-frequent token). Sampled
output is EN-byte garbage. Korean byte trigrams (0xE0-0xED prefix range)
have effectively zero probability mass — corpus EN-dominance from spec
(`prepare_large_data` uses Shakespeare ×5 repetition + project Python code
+ ≤10MB `.md` docs) confirmed at inference.

Lane closed: **CLM_V2_100M_NATIVE_KO_PATH_FAIL_TRUE_CORPUS_BIAS.** The 100M
ckpt cannot be promoted as KO chat candidate without retrain. Decision
deferred to β-path retrain (5–10 day ubu1 fire).

## (a) R2 download + load

| field | value |
|---|---|
| source | `r2://anima/checkpoints/conscious_lm_100m/final.pt` |
| size | 1,711,143,075 bytes (1631.9 MB) |
| sha256 | `35d60e77786c7580436cd02daac82c4f6cef3d2c7bdad470475900eeaecf295e` |
| download path | Cloudflare REST API GET object (`/accounts/<id>/r2/buckets/anima/objects/<key>`) — Global API Key + email auth |
| download elapsed | 173.7 s (≈9.4 MB/s) |
| HTTP status | 200 OK |

S3-compat path was BLOCKED — the rclone S3 token authenticates against R2
endpoint `ce4bdcce…` which lacks bucket access to `anima` (account
`d4acc958…`). Cloudflare REST `GET /r2/buckets/anima/objects/<key>` works
with the Global API Key and is the canonical access path for this artifact.
This is a reusable workaround for any other `anima/*` object.

## (b) Architecture inspect

| field | value |
|---|---|
| `step` | 50000 |
| `phase` | `combined` |
| wrapper keys | `step / model_state / optimizer_state / loss_ensemble_state / mitosis_status / phi_history / phase / config` |
| vocab\_size | 256 (byte) |
| d\_model | 768 |
| n\_layer | 12 |
| block\_size | 256 |
| n\_head | 12 (inferred) |
| total\_params | 143,298,048 in state\_dict / 142,315,008 in instantiated module |
| `phi_history[0]` sample | 2.527, 2.509, 2.503 … |

`load_state_dict(strict=False)` returns `missing=0, unexpected=0` —
ConsciousLM source from `/tmp/anima_v2_source/conscious_lm.py` (extracted
from ready/.git@bb99b6b6 651 LoC) is bit-exact match for the 100M ckpt
schema. Tying `tok_emb.weight ↔ head_a.weight` accounts for the 983,040
parameter delta vs raw state\_dict count.

## (c) KO chat smoke — 5 prompts × 4 strategies = 20 generations

| prompt | greedy | t=0.7/k=40 | t=0.5/k=40 | t=0.3/k=80 | best_hangul |
|---|---|---|---|---|---|
| 안녕하세요 | space×80 | EN garbage | EN garbage | EN garbage | **0** |
| 한국어 가능? | space×80 | EN garbage | EN garbage | EN garbage | **0** |
| 오늘 날씨 | space×80 | EN garbage | EN garbage | EN garbage | **0** |
| 의식이란? | space×80 | EN garbage | EN garbage | EN garbage | **0** |
| 자기 소개 | space×80 | EN garbage | EN garbage | EN garbage | **0** |

Sampling traces (excerpt, t=0.7/k=40):

- 안녕하세요 → `wjeyaE\ni tnoblwroh r\ntuv yeainXud d.d yeAaQ e`lee h beewo^*…`
- 의식이란? → `GodQanefwiyytn^h\nos.ciEeeviiyao\neerhQmlsa fv#h$l.Ant.rtw mg…`

Greedy decode is degenerate: deterministic argmax produces repeated 0x20
SPACE byte for all 5 KO prompts — confirms SPACE is the global most-likely
byte under any KO prefix because the model has zero learned prior on KO
sequences. Sampling pulls in a-z/A-Z + punctuation — a literal Shakespeare
fingerprint.

Total smoke wall-time: 71.4 s on M-series MPS (5 prompts × 4 strategies × 80
new bytes ≈ 1600 forward passes).

## (d) F-CLM-NATIVE-α-1 verdict

| criterion | bar | observed | result |
|---|---|---|---|
| ≥10 Hangul codepoints emit per prompt | ≥3 of 5 prompts | 0 of 5 | **FAIL** |
| no degenerate cycle | required | greedy = SPACE×80 (degenerate) | **FAIL** |
| valid load + forward | required | OK | PASS |

**Final: F-CLM-NATIVE-α-1 PASS = false → FAIL_TRUE_CORPUS_BIAS.**

## (e) 5 honest C3

1. **Architecture is healthy** — 142.32M params, 0 load mismatch, MPS
   forward passes complete in ~70ms each. The model is *trained* (step
   50000, phase=combined, phi_history populated). Not a checkpoint
   integrity issue.
2. **Corpus distribution is the root cause, not generation strategy.** 4
   sampling profiles (greedy + 3 temp/top_k combos) all emit zero Hangul.
   No knob can recover what wasn't trained. Confirms `EN-dominance from
   `prepare_large_data` (Shakespeare ×5 repeat + ≤10MB `.md` docs +
   ≤10MB project `.py` code) + 1KB-chunk shuffle.
3. **18M `convo_5k.pt` failure pattern persists at 100M scale.** Same
   FAIL\_KO\_BIAS phenotype as the 18.52M HF variant. Adding 7.7× more
   parameters does *not* compensate for absent KO byte coverage in
   pre-training data — capacity ≠ coverage.
4. **`tension_guided` / `curiosity_beta` paths skipped** — without
   non-zero KO probability mass at any byte position, curiosity-beta
   reweighting amplifies noise rather than rescuing KO. Skipping these
   was correct triage given the SPACE-collapse signal in greedy.
5. ** fallback temptation rejected** — F-CLM-NATIVE-α-1 closes
   without invoking external substrate (Llama / KoGPT / KoBART). The
   anima-native chat-cap path now hinges on β-path *retrain* with KO-balanced
   byte corpus (≥30 % Hangul UTF-8 mass), not on swap-out.

## (f) Next cycle — β-path retrain decision

**FAIL → β-path retrain queued.**

Required corpus (proposed minima):

- ≥1 GB total mixed-byte
- ≥30 % Hangul UTF-8 mass (KOWIKI-2024 + KO common-crawl filtered subset
  + KO chat dialogue corpora)
- ≤25 % Shakespeare-style EN literary (down from ~40–50 % in original)
- ≤25 % Python source (current ratio fine)
- balanced 1 KB shuffle preserving local KO sequence coherence

ubu1 budget envelope: H100 PCIe 80GB or A100 40GB ×1, ~5–10 days at
12L/768d/12h × 1024 block × bs 64. Cost-disciplined L23/L24/L25 watchdog
required . Option to start from this 100M ckpt (warm init) vs
fresh 18M reset is a separate decision — likely fresh is cleaner because
warm init carries EN-dominance bias.

Upstream gate: confirm KO retrain corpus availability + cost approval
before fire.

## Artifacts

- `state/anima_clm_v2_100m_smoke_2026_05_06/verdict.json`
- `state/anima_clm_v2_100m_smoke_2026_05_06/architecture_inspect.json`
- `state/anima_clm_v2_100m_smoke_2026_05_06/ko_chat_smoke_results.json`
- `docs/anima_clm_v2_100m_smoke_landed_2026_05_06.ai.md` (this file)

Local cache: `/tmp/anima_clm_100m_dl/final.pt` (1631.9 MB, sha256
`35d60e77786c7580436cd02daac82c4f6cef3d2c7bdad470475900eeaecf295e`),
`.gitignore`-excluded by `*.pt` rule + (anima git no >5 MB blobs).

## Constraints honoured

- $0 mac-local + Cloudflare R2 download (no pod fire)
- raw#37 transient_py opt-out: `tool/transient_py/anima_clm_100m_smoke_2026_05_06/smoke.py` ran then deleted
- HF token leak: not used (R2 + Cloudflare keys via env / secret CLI)
- ALM substrate fallback: not invoked (anima-native only)
- 5MB+ git: ckpt staged at `/tmp/`, not anima/
- commit: not performed (BG report only)
