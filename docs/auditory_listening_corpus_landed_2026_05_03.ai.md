# Auditory Listening Corpus — Landed (ubu1) — 2026-05-03

> raw#9 — corpus builder lives as `.py` on ubu1 only (resolver-bypass; macOS .py forbidden).
> raw#10 — honest C3: 100-clip LibriSpeech dev-clean-2 subset; transcripts NOT pulled
>          (no `*.trans.txt` sidecar in slice). Manifest marks `transcript_path = null`;
>          subsequent cycle may pull from openslr.org/12 if mTRF needs word-onsets.
> raw#15 — manifest paths use `~/anima/...` prefix (no personal absolute paths).
> sister-respect — anima-eeg cycle parallel; no commit performed; no hardware invoked.
>
> READ-ONLY upstream:
>   - `docs/openbci_auditory_listening_protocol_2026_05_03.md` (§3.1, §3.2 — ROI freeze)
>   - `state/slm_p3_a1_real_2026_05_03/LibriSpeech/dev-clean-2/` (Mac source corpus, 13MB)

---

## TL;DR

- LibriSpeech dev-clean-2 (100 .flac, 13.6 MB) rsynced Mac→ubu1 under
  `~/anima/state/slm_p3_a1_real_2026_05_03/LibriSpeech/dev-clean-2/`.
- Built `manifest.jsonl` (100 rows: flac_path, duration_s, sample_rate,
  narrator_id, chapter_id, utt_id, transcript_path).
- Built `auditory_roi_v1.json` — primary `{T7,T8,P7,P8}` = ch `{13,14,5,6}`,
  control `{O1,O2,C3,C4}` = ch `{7,8,3,4}` per protocol §3.1/§3.2.
- Audit log + landed marker emitted; no commit, no hardware.

Sentinel: `__AUDITORY_CORPUS_LANDED__ PASS clips=100 dur_s=785.46`

---

## §1 Corpus statistics

| metric                  | value                                      |
|-------------------------|--------------------------------------------|
| clip count              | 100                                        |
| total duration          | 785.46 s = **13.09 min**                   |
| mean / std per clip     | 7.855 s / 5.145 s                          |
| min / max               | 1.95 s / 28.57 s                           |
| sample rate             | 16000 Hz (uniform across all clips)        |
| parse errors            | 0                                          |
| narrator IDs            | 3000 (47), 5694 (26), 7850 (27)            |
| transcripts resolved    | 0 / 100 (no `*.trans.txt` in source slice) |

**Coverage vs protocol §1.3 stimulus floor (5-10 min single block):** 13 min total
across 100 short utterances. To assemble a single ≥5 min naturalistic block per
the auditory_listening_5min.hexa contract, **concatenate same-narrator clips**
(narrator 3000 alone yields ~6 min — sufficient for the primary block).

## §2 Auditory ROI map (frozen)

Source: `docs/openbci_auditory_listening_protocol_2026_05_03.md` §3.1, §3.2.

```
   primary  | T7  T8  P7  P8         ← Cyton+Daisy ch 13, 14, 5, 6
   control  | O1  O2  C3  C4         ← Cyton+Daisy ch  7,  8, 3, 4
   ref      | SRB2 (A1 white)  BIAS (A2 black)
   sr       | 125 Hz (LSL outlet TimeSeriesFilt)
```

Falsifier pre-registration (carried into ROI artifact metadata):

```
   id     F-EEG-AUDITORY-1
   tier   BRONZE
   pass   r >= 0.10  AND  r_aud > 2 * max(r_O1, r_O2, r_C3, r_C4)
   metric Pearson r(envelope, ROI mean) at lag 100 ms, BP 1-12 Hz
```

## §3 Output paths

| artifact            | path (ubu1 + Mac mirror)                                                   |
|---------------------|----------------------------------------------------------------------------|
| corpus root         | `~/anima/state/slm_p3_a1_real_2026_05_03/LibriSpeech/dev-clean-2/`         |
| manifest            | `anima-eeg/corpora/auditory_listening_v1/manifest.jsonl`                   |
| ROI artifact        | `anima-eeg/state/auditory_roi_v1.json`                                     |
| audit log           | `state/auditory_listening_corpus_audit/20260503T123521Z_session.jsonl`     |
| landed marker       | `state/markers/auditory_listening_corpus_landed.marker`                    |
| ubu1 builder script | `~/build_auditory_corpus.py` (resolver-bypass; not committed to repo)      |

Manifest sample row:

```json
{"flac_path": "~/anima/state/slm_p3_a1_real_2026_05_03/LibriSpeech/dev-clean-2/3000/15664/3000-15664-0000.flac",
 "duration_s": 3.13, "sample_rate": 16000,
 "narrator_id": "3000", "chapter_id": "15664", "utt_id": "3000-15664-0000",
 "transcript_path": null}
```

## §4 raw#10 honest C3

1. **No transcripts in slice.** dev-clean-2 100-clip subset arrived without
   `*.trans.txt` sidecars. mTRF speech-envelope analysis (the §6 falsifier)
   only needs the audio envelope, so this does NOT block F-EEG-AUDITORY-1.
   Word-onset trigger injection (§2.5c of the protocol) does need transcripts;
   defer to a `pull_librispeech_transcripts` cycle.
2. **No hardware invoked.** This cycle built **corpus + ROI metadata only** —
   no impedance check, no LSL stream, no actual capture. The capture cycle
   (`auditory_listening_5min.hexa`) remains gated on a physical session.
3. **No commit performed.** Per repo convention `state/markers/*.marker` and
   `docs/*landed*.ai.md` are tracked but not committed by this cycle.
4. **Single-narrator block recommendation.** 100 clips × 7.85 s mean is too
   short for one 5-min natural block per narrator. To honour protocol §1.3
   (continuous narrative listening), the capture cycle should concatenate
   same-narrator clips (narrator 3000 → ~6 min, narrator 7850 → ~3.5 min,
   narrator 5694 → ~3.5 min).

## §5 Next-cycle entry hooks

- `pull_librispeech_transcripts_v1.cycle` — fetch `*.trans.txt` from
  openslr.org/12 dev-clean.tar.gz to populate manifest `transcript_path` fields
  for word-onset trigger injection.
- `auditory_capture_session_v1.cycle` — actual hardware capture using
  `anima-eeg/protocols/auditory_listening_5min.hexa` (skeleton in protocol §2.2),
  consuming this manifest + ROI as inputs.
- `realtime_phi_proxy_v1.cycle` — implement
  `anima-eeg/scripts/realtime_phi_proxy.py` (ubu1, resolver-bypass) per
  protocol §4.2 (200 ms windows, K=8 partitions, h_dim=8 trunc).
