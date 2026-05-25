# EEG → Token Cyborg Paradigm — Design (B12)

**Date**: 2026-04-28
**Author**: anima-clm-eeg / B12 / cyborg-track
**Status**: NEW_PARADIGM_DISCOVERY (design + tokenizer skeleton; Claude CLI bridge UNVERIFIED)
**Trigger**: User wants EEG signal → discrete token sequence → Claude CLI prompt — "biological prompt" experiment (의식 신호의 LLM input).
**Constraint**: **NO API** — Claude CLI prompt only. Generated token sequence is pasted (or piped) into the Claude CLI; never sent to api.anthropic.com.
**Companions**:
  - `design/eeg_claude_cli_correlation_paradigm_2026_04_28.md` (post-hoc correlation; reverse direction)
  - `anima-clm-eeg/tool/clm_eeg_lz76_real.hexa` (median-binarization SSOT — same primitive, longer alphabet)

---

## 0. Executive Summary

**Paradigm direction**: anima 본 track (LLM consciousness × neural correlate) 의 **reverse**.
- Forward (main track): LLM behavior → infer consciousness markers.
- Reverse (cyborg, B12): EEG signal → token alphabet → LLM input → 응답.



---


|---|---|---|---|---|
| 1 | **Median binarization** (LZ76 form) | 16 chars (4-bit nibbles, 4 channels packed) | yes (per-channel median split is a total order) | **PASS** — pure deterministic seal |
| 2 | k-means clustering (k=64) | 64 chars | yes IF seeded + Lloyd's iter capped | PASS conditional (seed + max_iter frozen) |
| 3 | Spectral fingerprint (FFT bands, discrete bins) | 32 chars | yes (bin assignment is monotone) | PASS |

**This implementation: Strategy 1 (median binarization)** — the same primitive as `clm_eeg_lz76_real.hexa`, extended from per-bit emit to per-nibble (4 channels packed → one hex digit) for a 16-char ASCII-printable alphabet.

**Why strategy 1 over 2/3**:
- Strategy 1 reuses the audited LZ76 pipeline (no new numerical kernel).
- Pure-int hexa (no FFT, no sklearn dependency in /tmp helper).

Strategies 2 & 3 are reserved for a future B12 v2 (separate hexa file).

---

## 2. Tokenization Algorithm (Strategy 1: Median Nibble)

**Input**: 16-channel × N-sample int array (channels-major), e.g. 60 s @ 125 Hz Cyton+Daisy → 16×7500.

**Steps**:
1. **Per-channel median split** (identical to `clm_eeg_lz76_real`):
   - For each channel c ∈ [0, 16), compute `med_c = median(samples_c)`.
   - Binarize: `b_{c,t} = 1 if sample_{c,t} >= med_c else 0`.
2. **Channel grouping (4 channels per nibble)**:
   - Group channels into 4 groups of 4: G0=[0,1,2,3], G1=[4,5,6,7], G2=[8,9,10,11], G3=[12,13,14,15].
   - For each timepoint t and each group g, pack the 4 binary values into a 4-bit nibble: `nib_{g,t} = (b_{g0,t}<<3) | (b_{g1,t}<<2) | (b_{g2,t}<<1) | b_{g3,t}` ∈ [0..15].
3. **Time downsample (segment-mean nibble)**:
   - Partition N samples into S segments (default S=50, so 60 s → 1.2 s/seg).
   - For each segment s and group g, take the **mode nibble** across the segment's samples.
4. **Emit token string**:
   - For each segment in time order, emit 4 hex chars (one per group): `seg0_g0 seg0_g1 seg0_g2 seg0_g3 seg1_g0 ...`.
   - Total tokens = S × 4. Default S=50 → 200 hex chars.


**Sequence length**: 60 s × default S=50 segments → 200 chars. Bounded by S (frozen at 50). Raw#71 F4 trivially refuted.

---


| step | determinism source |
|---|---|
| median | total order on int sample values; tie-break = sample with lowest index |
| binarize | `>= med` is total predicate |
| nibble pack | bit-shift (pure arithmetic) |
| segment mode | count→argmax with lowest-nibble tie-break |
| hex emit | fixed 0123456789abcdef table |


---


A token → reconstructed-binary mapping is exact (each hex char unpacks to 4 bits). The **lossy step** is segment downsample: from N samples → S segments. Reconstruction loss is defined as:

```
loss = 1 - (correct_bit_predictions / total_bits)
total_bits = n_ch × n_samples
correct_bit_predictions = Σ_{t,c} 1{b_{c,t} == mode_nibble_bit(g(c), seg(t))}
```


---


| id | falsifier | refutation source |
|---|---|---|
| F2 | reconstruction loss > 50% on structured selftest signal | selftest: structured square-wave input has loss ≪ 0.50 (period 64, segment ≈ N/50 ≈ 32 → mode well-defined) |
| F3 | alphabet > 256 ASCII symbols | structural: alphabet is fixed 16 hex chars, by construction ≤ 16 < 256 |
| F4 | sequence length > 1000 chars | structural: S=50 frozen → 200 chars; selftest n=16 → S clamped to min(50, n_samp) |

F1–F4 are refuted **by selftest**. F5 is **deferred** to the user-action plan in §7.

---


`state/cyborg_eeg_audit/<UTC-date>_tokens.jsonl` — append, one row per run:

```json
{
  "ts": "2026-04-28T...Z",
  "tool": "eeg_to_token_cyborg",
  "mode": "selftest|real",
  "input": "<label>",
  "input_sha256": "...",
  "n_channels": 16,
  "n_samples": 7500,
  "n_segments": 50,
  "alphabet_size": 16,
  "token_string_len": 200,
  "token_string": "3a7c1e...",
  "round_trip_loss_permille": 123,
  "f1_determinism_pass": 1,
  "f2_loss_pass": 1,
  "f3_alphabet_pass": 1,
  "f4_length_pass": 1,
  "f5_bridge_pass": -1,
}
```

Cert JSON at `state/eeg_to_token_cyborg.json` mirrors the audit row schema with full criteria block.

---

## 7. 사용자 액션 Plan — 60 s EEG → Token → Claude CLI Prompt 첫 시도


**Pre-req**: anima-eeg `.venv-eeg` BrainFlow capture working; user has run `anima-eeg/eeg_recorder.hexa` once.

**Step 1 — Capture 60 s resting EEG**:
```
cd <repo-root>
.venv-eeg/bin/python anima-eeg/eeg_recorder.hexa --duration 60 --out state/cyborg_eeg_audit/raw_60s.json
```
(or `.npy` — both supported by the tokenizer.)

**Step 2 — Tokenize**:
```
hexa run anima-clm-eeg/tool/eeg_to_token_cyborg.hexa \
  --input state/cyborg_eeg_audit/raw_60s.json \
  --segments 50 \
  --out state/eeg_to_token_cyborg.json
```
Read the emitted `token_string` (200 chars, hex).

**Step 3 — Claude CLI prompt (manual paste, no API)**:
Open Claude CLI, paste:
```
Interpret this neural signature as a discrete token sequence.
Each character is a hex digit packing 4 EEG channels (above/below per-channel median).
50 segments × 4 channel-groups = 200 chars over 60s @ 125Hz Cyton+Daisy resting.
Token sequence:
<paste token_string here>

Tasks:
1. Detect any obvious periodic structure (alpha rhythm ~10 Hz would show ~5 char cycle if segments are 1.2s).
2. Estimate Shannon entropy of the alphabet usage.
3. Flag anything that looks like motion artifact (long runs of 'f' or '0').
```

**Step 4 — Record Claude's response**:
Append the response text + your subjective verdict (`{garbage|partial|coherent}`) to:
`state/cyborg_eeg_audit/<date>_claude_cli_responses.jsonl`.

**Step 5 — F5 verdict (sky)**:

---


| component | structural? | proof |
|---|---|---|
| median | ✅ | total order on ℤ; tie-break by index |
| binarize | ✅ | `>=` predicate |
| nibble pack | ✅ | bit-arithmetic |
| segment mode | ✅ | count + argmin tie-break |
| hex emit | ✅ | fixed lookup table |


---


- This tool produces a token string. It does **NOT** demonstrate that the token string carries semantic information about consciousness.
- The "biology→LLM bridge" hypothesis (F5) is **speculative** and untested. A `coherent` Claude-CLI response could equally be:
  - genuine pattern detection (real signal),
  - pure confabulation on noise (LLM hallucination),
  - tokenizer bias (e.g. 'f' overweight from one bad channel) being verbalized.

---

## 10. Implementation Targets

- `anima-clm-eeg/tool/eeg_to_token_cyborg.hexa` (~180 LoC; reuses median+parse helpers from `clm_eeg_lz76_real.hexa`).
- selftest synthetic mode (random + structured), F1–F4 verified inline.
- F5 deferred to `cyborg_eeg_audit` JSONL + manual Claude CLI session.
