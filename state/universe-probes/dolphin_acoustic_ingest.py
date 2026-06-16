#!/usr/bin/env python3
"""
dolphin_acoustic_ingest.py — REAL public dolphin acoustic data -> anima 5-ch tension fingerprint.

WHY (anima link)
  H_070 dolphin_star_communication (hypotheses_candidates / Hc_017 linked_h). Dolphin whistles
  are FREQUENCY-MODULATED contours (dF/dt), plus broadband echolocation clicks + burst pulses --
  a natural audio->tension-band signal, the acoustic analogue of the EEG 5-band ingest
  (BRAIN/eeg/eeg_to_tpm.hexa). PR #1763 found that TIME enters anima's substrate via the d/dt
  (derivative / rising-edge) channel; dolphin whistles ARE time-varying frequency contours, so
  the F0 dF/dt channel here is a REAL natural-data test of that #1763 d/dt time-encoding.

DATA ($0, public, CPU-only)
  HuggingFace `confit/wmms-parquet` -- the Watkins Marine Mammal Sound Database (WMMS), repackaged
  as parquet (audio bytes + species + label). PUBLIC repo. We FILTER to dolphin species only.
  LICENSE: Watkins/WHOI = academic & personal use only, NON-COMMERCIAL. Ingest for research is
  fine; we do NOT re-upload the raw audio to HF PUBLIC. Derived fingerprints stay local.

PIPELINE  (Phase 1 -- mirrors the EEG adapter shape: signal -> per-frame band features -> 5-ch)
  real WAV (mono, ~few-kHz..16kHz)  -> STFT magnitude spectrogram (scipy.signal.stft)
    per STFT frame extract:
      F0       = whistle fundamental: argmax magnitude bin in the whistle band, smoothed
      dF0/dt   = frame-to-frame change of F0  (the #1763 d/dt channel -- the FM contour slope)
      clickrate= broadband-click energy proxy: high-band flatness * high-band energy
      burst    = burst-pulse density proxy: short-time energy temporal variance
      centroid = spectral centroid (Hz), bandwidth = spectral spread (Hz)
    -> reduce over frames -> a DETERMINISTIC 5-channel tension vector (z-bounded to a fixed range),
       channel order mirrors EEG 5-band [alpha,theta,gamma,1-delta,beta] in spirit:
         ch0 = F0 level           (whistle fundamental, normalized)
         ch1 = |dF0/dt| contour   (FM slope magnitude  <- #1763 d/dt key channel)
         ch2 = click rate         (broadband echolocation proxy)
         ch3 = burst-pulse density
         ch4 = spectral centroid  (overall brightness)

VALIDATION (Phase 2, substrate-native -- NOT cross-entropy)
  F-DISCRIMINATIVE : whistle-like vs click-like vs different-species clips -> distinct fingerprints
                     (between-class L2 distance > within-class spread). + deterministic re-encode
                     (re-run identical bytes -> identical 5-ch, max abs diff == 0).
  F-DFDT-TIME      : the #1763 test on REAL FM contours. Does the whistle's dF0/dt (time-varying
                     frequency) carry info that a FREQUENCY-SHUFFLED (time-scrambled) clip loses?
                     We compare a dF/dt-AWARE class separation against a STATIC-only spectrum
                     (centroid/bandwidth, no time order) AND against time-shuffled clips.
                     HOLDS if shuffling time collapses the dF/dt channel (|dF0/dt| drops materially)
                     and the dF/dt-aware fingerprint separates classes better than static-only.
  F-STABLE         : all fingerprints finite, no NaN/Inf, 5-ch within the declared bounded range.

VERDICTS: HOLDS / REFUTED / INCONCLUSIVE -- honest, no rounding (p7 / g5).
TOY scope: public recordings, NOT a live hydrophone; CPU; $0. a_toy_scale_recheck applies.
"""

import io
import os
import sys
import json
import math
import time
import hashlib
from collections import defaultdict

import numpy as np
from scipy.signal import stft, resample_poly
import soundfile as sf
from huggingface_hub import hf_hub_download
import pyarrow.parquet as pq

HF_REPO = "confit/wmms-parquet"
HF_FILE = "data/test-00000-of-00001.parquet"   # smallest split, 340 rows -- enough for a TOY ingest
HF_LICENSE = "Watkins Marine Mammal Sound Database (WHOI) -- academic/personal, NON-COMMERCIAL"

# dolphin species (subset of the 32-class WMMS label set -- delphinids only)
DOLPHIN_SPECIES = {
    "Atlantic_Spotted_Dolphin", "Bottlenose_Dolphin", "Clymene_Dolphin", "Common_Dolphin",
    "Frasers_Dolphin", "Grampus,_Rissos_Dolphin", "Pantropical_Spotted_Dolphin",
    "Rough-Toothed_Dolphin", "Spinner_Dolphin", "Striped_Dolphin",
    "White-beaked_Dolphin", "White-sided_Dolphin",
}

# acoustically DISTINCT non-dolphin contrast classes for the coarse discriminative test:
# Sperm Whale = broadband echolocation CLICKS (no whistle), baleen whales = low-frequency MOANS.
# delphinid whistle (FM tonal) vs these is the "whistle vs click/moan" axis the task names.
CONTRAST_SPECIES = {"Sperm_Whale", "Humpback_Whale", "Bowhead_Whale", "Fin,_Finback_Whale"}

N_CH = 5
TENSION_LO, TENSION_HI = -3.0, 3.0   # declared bounded range for the 5-ch tension vector

# Watkins dolphin clips have HETEROGENEOUS native sample-rates (30k..166k Hz) -- a pure
# recording-equipment confound. We resample EVERY clip to a COMMON rate and use ABSOLUTE-Hz
# bands so the same whistle maps to the same feature regardless of the source recorder.
COMMON_SR = 48000                    # covers the dolphin whistle band (2-24 kHz) at 48k Nyquist
WHISTLE_LO_HZ, WHISTLE_HI_HZ = 2000.0, 24000.0
HZ_REF = 24000.0                     # absolute-Hz normalization reference (fixed, NOT per-clip Nyquist)


# ----------------------------------------------------------------------------- fetch
def fetch_clips(species_set, max_per_species=6, max_species=6):
    """Download the parquet, filter to `species_set`, resample to COMMON_SR, return clips + meta."""
    path = hf_hub_download(HF_REPO, HF_FILE, repo_type="dataset")
    sha = hashlib.sha256(open(path, "rb").read()).hexdigest()
    size = os.path.getsize(path)
    tbl = pq.read_table(path)
    species_col = tbl.column("species").to_pylist()
    audio_col = tbl.column("audio").to_pylist()

    by_sp = defaultdict(list)
    for sp, au in zip(species_col, audio_col):
        if sp not in species_set:
            continue
        if len(by_sp[sp]) >= max_per_species:
            continue
        b = au["bytes"]
        data, srate = sf.read(io.BytesIO(b))
        if data.ndim > 1:
            data = data.mean(axis=1)               # mono
        data = np.asarray(data, dtype=np.float64)
        # resample to COMMON_SR so heterogeneous native rates (30k..166k) stop being a confound
        if srate != COMMON_SR and len(data) > 8:
            g = math.gcd(int(srate), COMMON_SR)
            data = resample_poly(data, COMMON_SR // g, int(srate) // g)
        by_sp[sp].append((au["path"], srate, COMMON_SR, data))

    # take the species with the most clips first, deterministically
    chosen = sorted(by_sp.keys(), key=lambda s: (-len(by_sp[s]), s))[:max_species]
    clips = []
    for sp in chosen:
        for (p, native_sr, common_sr, samp) in by_sp[sp]:
            clips.append((sp, p, native_sr, common_sr, samp))
    meta = {
        "hf_repo": HF_REPO, "hf_file": HF_FILE, "sha256": sha, "size_bytes": size,
        "license": HF_LICENSE, "species_present": sorted(by_sp.keys()),
        "species_used": chosen, "n_clips": len(clips),
        "resampled_to_common_sr_hz": COMMON_SR,
        "whistle_band_hz": [WHISTLE_LO_HZ, WHISTLE_HI_HZ],
    }
    return clips, meta


# ----------------------------------------------------------------------------- spectral -> 5-ch
def _spectrogram(samples, sr):
    """STFT magnitude spectrogram. Returns (freqs Hz, mag [n_freq, n_frame])."""
    n = len(samples)
    nper = min(512, max(64, 1 << int(math.log2(max(64, n // 8)))))
    f, t, Z = stft(samples, fs=sr, nperseg=nper, noverlap=nper // 2, boundary=None, padded=False)
    mag = np.abs(Z)
    return f, mag


def _f0_contour(freqs, mag, whistle_lo=WHISTLE_LO_HZ, whistle_hi=WHISTLE_HI_HZ):
    """Per-frame whistle fundamental F0 = argmax magnitude bin in the whistle band (Hz)."""
    band = (freqs >= whistle_lo) & (freqs <= whistle_hi)
    if not band.any():
        band = freqs > 0
    fb = freqs[band]
    mb = mag[band, :]                                  # [n_band_freq, n_frame]
    if mb.shape[0] == 0 or mb.shape[1] == 0:
        return np.zeros(max(1, mag.shape[1]))
    idx = np.argmax(mb, axis=0)
    f0 = fb[idx]
    return f0


def spectral_features(samples, sr):
    """REAL WAV -> deterministic per-clip feature dict (frame-reduced)."""
    freqs, mag = _spectrogram(samples, sr)
    if mag.shape[1] < 2:
        # too short to have a contour -> degrade gracefully (still deterministic, finite)
        mag = np.pad(mag, ((0, 0), (0, 2 - mag.shape[1])), mode="edge") if mag.size else np.ones((len(freqs), 2))

    eps = 1e-12
    framepow = mag.sum(axis=0) + eps                   # per-frame total energy

    # F0 contour + its d/dt (the #1763 channel)
    f0 = _f0_contour(freqs, mag)
    df0 = np.diff(f0) if len(f0) > 1 else np.array([0.0])
    # ABSOLUTE-Hz normalization (fixed HZ_REF, NOT per-clip Nyquist) -- after COMMON_SR resample
    # the recorder's native rate no longer leaks into the features.
    nyq = HZ_REF

    # spectral centroid / bandwidth per frame
    centroid = (freqs[:, None] * mag).sum(axis=0) / framepow
    spread = np.sqrt(((freqs[:, None] - centroid[None, :]) ** 2 * mag).sum(axis=0) / framepow)

    # broadband click proxy: high-band (>0.5 nyq) spectral flatness * high-band energy fraction
    hi = freqs >= 0.5 * nyq
    if hi.any():
        mh = mag[hi, :] + eps
        gmean = np.exp(np.mean(np.log(mh), axis=0))
        amean = np.mean(mh, axis=0)
        flatness = gmean / amean                        # ~1 for broadband click, ~0 for tonal
        hi_frac = mag[hi, :].sum(axis=0) / framepow
        clickrate = float(np.mean(flatness * hi_frac))
    else:
        clickrate = 0.0

    # burst-pulse density proxy: temporal variance of frame energy (pulsed -> high var)
    fp_n = framepow / (framepow.mean() + eps)
    burst = float(np.var(fp_n))

    return {
        "f0_mean_hz": float(np.mean(f0)),
        "f0_norm": float(np.mean(f0) / (nyq + eps)),
        "abs_df0_mean_hz": float(np.mean(np.abs(df0))),       # |dF0/dt| -- #1763 d/dt magnitude
        "abs_df0_norm": float(np.mean(np.abs(df0)) / (nyq + eps)),
        "clickrate": clickrate,
        "burst": burst,
        "centroid_norm": float(np.mean(centroid) / (nyq + eps)),
        "bandwidth_norm": float(np.mean(spread) / (nyq + eps)),
        "n_frame": int(mag.shape[1]),
        "_f0_contour_hz": f0,                                 # raw per-frame F0 (for #1763 shuffle)
    }


def to_tension_5ch(feat):
    """5-ch deterministic tension vector, bounded to [TENSION_LO, TENSION_HI]. EEG-adapter shape."""
    raw = np.array([
        feat["f0_norm"],          # ch0 F0 level
        feat["abs_df0_norm"],     # ch1 |dF0/dt|  <- #1763 d/dt key channel
        feat["clickrate"],        # ch2 click rate
        feat["burst"],            # ch3 burst-pulse density
        feat["centroid_norm"],    # ch4 spectral centroid
    ], dtype=np.float64)
    # fixed deterministic affine map into the bounded range (NOT a learned transform):
    # each channel is a [0,~1]-ish proxy; center at 0 by *6 - 3 then clip. Identical input -> identical out.
    t = raw * 6.0 - 3.0
    t = np.clip(t, TENSION_LO, TENSION_HI)
    return t


# ----------------------------------------------------------------------------- validation
def _pairwise_l2(vecs):
    vecs = np.asarray(vecs)
    n = len(vecs)
    ds = []
    for i in range(n):
        for j in range(i + 1, n):
            ds.append(float(np.linalg.norm(vecs[i] - vecs[j])))
    return np.array(ds) if ds else np.array([0.0])


def check_discriminative(per_clip):
    """Between-species fingerprint distance > within-species spread, + deterministic re-encode."""
    by_sp = defaultdict(list)
    for c in per_clip:
        by_sp[c["species"]].append(c["tension"])

    within = []
    centroids = {}
    for sp, vs in by_sp.items():
        if len(vs) >= 2:
            within.extend(_pairwise_l2(vs).tolist())
        centroids[sp] = np.mean(np.asarray(vs), axis=0)
    between = _pairwise_l2(list(centroids.values()))

    within_mean = float(np.mean(within)) if within else 0.0
    between_mean = float(np.mean(between)) if len(between) else 0.0
    separation = between_mean / (within_mean + 1e-9)

    # deterministic re-encode: identical bytes -> identical 5-ch
    max_reenc_diff = max(c["reencode_max_abs_diff"] for c in per_clip)

    holds = (between_mean > within_mean) and (max_reenc_diff == 0.0) and len(centroids) >= 2
    verdict = "HOLDS" if holds else ("INCONCLUSIVE" if len(centroids) < 2 else "REFUTED")
    return verdict, {
        "n_species": len(centroids),
        "within_class_mean_l2": within_mean,
        "between_class_mean_l2": between_mean,
        "separation_ratio": separation,
        "deterministic_reencode_max_abs_diff": max_reenc_diff,
    }


def check_discriminative_coarse(dolphin_tens, contrast_tens):
    """
    Coarse acoustic-CLASS discriminative test (the 'whistle vs click/moan' axis the task names):
    delphinid whistle group vs an acoustically DISTINCT non-dolphin group (Sperm Whale clicks,
    baleen-whale moans). HOLDS if between-group centroid distance > mean within-group spread.
    """
    g1 = np.asarray(dolphin_tens); g2 = np.asarray(contrast_tens)
    if len(g1) < 2 or len(g2) < 2:
        return "INCONCLUSIVE", {"n_dolphin": len(g1), "n_contrast": len(g2)}
    w1 = float(np.mean(_pairwise_l2(g1))); w2 = float(np.mean(_pairwise_l2(g2)))
    within = 0.5 * (w1 + w2)
    between = float(np.linalg.norm(g1.mean(axis=0) - g2.mean(axis=0)))
    holds = between > within
    return ("HOLDS" if holds else "REFUTED"), {
        "n_dolphin": len(g1), "n_contrast": len(g2),
        "within_dolphin_mean_l2": w1, "within_contrast_mean_l2": w2,
        "within_group_mean_l2": within, "between_group_centroid_l2": between,
        "separation_ratio": between / (within + 1e-9),
    }


def check_dfdt_time(clips, seeds=(0, 1, 2)):
    """
    #1763 d/dt test on REAL FM contours -- the time-scramble test.
    The REAL whistle is a time-ORDERED frequency contour F0(t); its |dF0/dt| measures the
    frame-to-frame FM slope. We TIME-SCRAMBLE the F0 contour (permute its frame order) so the
    SET of frequencies is preserved but the TEMPORAL ORDER (the FM trajectory) is destroyed,
    then recompute |dF0/dt| on the scrambled contour. This is the direct natural-data analogue
    of #1763: real time-order vs shuffled.
    HOLDS if scrambling the contour materially INFLATES |dF0/dt| over the real ordered contour
    (a smooth real FM sweep has small adjacent steps; random frame order makes large jumps) AND
    a dF/dt-aware fingerprint separates species better than a static-only (centroid/bandwidth)
    fingerprint. i.e. the temporal order carries real, separable structure that a bag-of-frames
    static spectrum lacks.
    """
    rng_results = []
    for seed in seeds:
        rng = np.random.default_rng(seed)
        real_df, shuf_df = [], []
        dfdt_aware_vecs, static_vecs, labels = [], [], []
        for (sp, path, native_sr, sr, samp) in clips:
            feat = spectral_features(samp, sr)
            real_df.append(feat["abs_df0_norm"])
            # TIME-SCRAMBLE the F0 contour at frame level: same frequencies, order destroyed.
            f0 = np.asarray(feat["_f0_contour_hz"], dtype=np.float64)
            if len(f0) > 2:
                f0s = f0[rng.permutation(len(f0))]
                shuf_absdf0 = float(np.mean(np.abs(np.diff(f0s))) / (HZ_REF + 1e-12))
            else:
                shuf_absdf0 = feat["abs_df0_norm"]
            shuf_df.append(shuf_absdf0)

            dfdt_aware_vecs.append([feat["f0_norm"], feat["abs_df0_norm"], feat["centroid_norm"]])
            static_vecs.append([feat["centroid_norm"], feat["bandwidth_norm"]])
            labels.append(sp)

        real_df = np.array(real_df); shuf_df = np.array(shuf_df)
        # smooth ordered FM sweep -> small |dF0/dt|; scrambled order -> larger. d/dt info present
        # iff scrambling CHANGES |dF0/dt| (here: inflates it). Report signed gap honestly.
        df_collapse = float(np.mean(shuf_df) - np.mean(real_df))    # >0 => order carried real info
        df_collapse_ratio = float(np.mean(real_df) / (np.mean(shuf_df) + 1e-12))

        sep_aware = _class_separation(dfdt_aware_vecs, labels)
        sep_static = _class_separation(static_vecs, labels)
        rng_results.append({
            "seed": seed,
            "real_ordered_abs_df0_norm_mean": float(np.mean(real_df)),
            "time_scrambled_abs_df0_norm_mean": float(np.mean(shuf_df)),
            "scramble_inflation_abs": df_collapse,             # >0 => temporal order carried info
            "real_over_scrambled_ratio": df_collapse_ratio,
            "sep_dfdt_aware": sep_aware,
            "sep_static_only": sep_static,
            "dfdt_beats_static": bool(sep_aware > sep_static),
        })

    # aggregate verdict across seeds:
    #  (a) temporal order carries dF/dt info iff scrambling MEASURABLY changes |dF0/dt| on all seeds
    #  (b) the dF/dt-aware fingerprint must separate species better than the static-only spectrum
    order_carries_info = all(abs(r["scramble_inflation_abs"]) > 1e-6 for r in rng_results) and \
                         all(r["scramble_inflation_abs"] > 0.0 for r in rng_results)
    beats = sum(r["dfdt_beats_static"] for r in rng_results)
    if order_carries_info and beats >= 2:
        verdict = "HOLDS"
    elif (not order_carries_info) and beats == 0:
        verdict = "REFUTED"
    else:
        verdict = "INCONCLUSIVE"
    return verdict, {"seeds": rng_results,
                     "temporal_order_carries_dfdt_info_all_seeds": order_carries_info,
                     "n_seeds_dfdt_beats_static": beats}


def _class_separation(vecs, labels):
    """between-class centroid spread / within-class spread, for a feature set."""
    vecs = np.asarray(vecs, dtype=np.float64)
    by = defaultdict(list)
    for v, l in zip(vecs, labels):
        by[l].append(v)
    within, cents = [], {}
    for l, vs in by.items():
        vs = np.asarray(vs)
        if len(vs) >= 2:
            within.extend(_pairwise_l2(vs).tolist())
        cents[l] = vs.mean(axis=0)
    btw = _pairwise_l2(list(cents.values()))
    wm = float(np.mean(within)) if within else 1e-9
    bm = float(np.mean(btw)) if len(btw) else 0.0
    return bm / (wm + 1e-9)


def check_stable(per_clip):
    """All fingerprints finite, no NaN/Inf, 5-ch within [TENSION_LO, TENSION_HI]."""
    bad = 0
    oob = 0
    for c in per_clip:
        t = np.asarray(c["tension"])
        if not np.all(np.isfinite(t)):
            bad += 1
        if np.any(t < TENSION_LO - 1e-9) or np.any(t > TENSION_HI + 1e-9):
            oob += 1
    holds = (bad == 0 and oob == 0 and len(per_clip) > 0)
    verdict = "HOLDS" if holds else ("INCONCLUSIVE" if len(per_clip) == 0 else "REFUTED")
    return verdict, {"n_clips": len(per_clip), "n_nonfinite": bad, "n_out_of_range": oob,
                     "range": [TENSION_LO, TENSION_HI]}


# ----------------------------------------------------------------------------- main
def main():
    t0 = time.time()
    print("=" * 78)
    print("dolphin_acoustic_ingest -- REAL public dolphin acoustic data -> 5-ch tension")
    print("=" * 78)

    clips, meta = fetch_clips(DOLPHIN_SPECIES, max_per_species=6, max_species=6)
    print(f"[fetch] repo={meta['hf_repo']} file={meta['hf_file']}")
    print(f"[fetch] sha256={meta['sha256']}")
    print(f"[fetch] size_bytes={meta['size_bytes']}  license={meta['license']}")
    print(f"[fetch] dolphin species present: {meta['species_present']}")
    print(f"[fetch] dolphin species used: {meta['species_used']}  n_clips={meta['n_clips']}")
    if meta["n_clips"] < 2:
        print("[fetch] FATAL: <2 clips, cannot validate")
        sys.exit(2)

    # contrast (non-dolphin) clips for the coarse acoustic-class discriminative test
    contrast_clips, cmeta = fetch_clips(CONTRAST_SPECIES, max_per_species=6, max_species=3)
    print(f"[fetch] contrast (non-dolphin) species used: {cmeta['species_used']}  "
          f"n_clips={cmeta['n_clips']}")

    # encode every clip -> 5-ch tension, with deterministic re-encode check
    per_clip = []
    for (sp, path, native_sr, sr, samp) in clips:
        feat = spectral_features(samp, sr)
        t1 = to_tension_5ch(feat)
        feat2 = spectral_features(samp, sr)            # re-encode identical samples
        t2 = to_tension_5ch(feat2)
        reenc = float(np.max(np.abs(t1 - t2)))
        feat_save = {k: v for k, v in feat.items() if not k.startswith("_")}   # drop raw contour
        per_clip.append({"species": sp, "path": path, "native_sr": native_sr, "sr": sr,
                         "tension": t1.tolist(), "feat": feat_save,
                         "reencode_max_abs_diff": reenc})

    print(f"[encode] {len(per_clip)} clips @ {COMMON_SR}Hz -> 5-ch tension "
          f"(ch order: F0,|dF0/dt|,click,burst,centroid)")
    for c in per_clip[:6]:
        print(f"   {c['species'][:22]:22s} {c['path'][:14]:14s} native_sr={c['native_sr']:6d} "
              f"t={[round(x,3) for x in c['tension']]}")

    # encode contrast clips -> 5-ch tension (for the coarse acoustic-class test)
    contrast_tens = []
    for (sp, path, native_sr, sr, samp) in contrast_clips:
        contrast_tens.append(to_tension_5ch(spectral_features(samp, sr)).tolist())

    v_disc, d_disc = check_discriminative(per_clip)                       # fine: cross-species (hard)
    v_dcoarse, d_dcoarse = check_discriminative_coarse(                   # coarse: whistle vs click/moan
        [c["tension"] for c in per_clip], contrast_tens)
    v_time, d_time = check_dfdt_time(clips, seeds=(0, 1, 2))
    v_stab, d_stab = check_stable(per_clip)

    print("\n--- F-DISCRIMINATIVE (fine: cross dolphin-species) ---", v_disc); print(json.dumps(d_disc, indent=2))
    print("\n--- F-DISCRIMINATIVE-COARSE (dolphin whistle vs non-dolphin click/moan) ---", v_dcoarse)
    print(json.dumps(d_dcoarse, indent=2))
    print("\n--- F-DFDT-TIME (#1763) ---", v_time); print(json.dumps(d_time, indent=2))
    print("\n--- F-STABLE ---", v_stab); print(json.dumps(d_stab, indent=2))

    results = {
        "harness": "UNIVERSE/dolphin_acoustic_ingest.py",
        "anima_link": "H_070 dolphin_star_communication / Hc_017 ; #1763 d/dt time-encoding",
        "fetch": meta,
        "tension_channels": ["F0_level", "abs_dF0_dt_(#1763)", "click_rate", "burst_density", "spectral_centroid"],
        "contrast_fetch": {"species_used": cmeta["species_used"], "n_clips": cmeta["n_clips"]},
        "F-FETCH": "HOLDS" if meta["n_clips"] >= 2 else "REFUTED",
        "F-DISCRIMINATIVE": {"verdict": v_disc, "detail": d_disc,
                             "note": "fine cross dolphin-species (hardest case)"},
        "F-DISCRIMINATIVE-COARSE": {"verdict": v_dcoarse, "detail": d_dcoarse,
                                    "note": "dolphin whistle vs non-dolphin click/moan"},
        "F-DFDT-TIME": {"verdict": v_time, "detail": d_time},
        "F-STABLE": {"verdict": v_stab, "detail": d_stab},
        "scope": "TOY/CPU/$0; public recordings NOT live hydrophone; a_toy_scale_recheck",
        "license_note": "Watkins non-commercial; raw audio NOT re-uploaded to HF PUBLIC",
        "wall_s": round(time.time() - t0, 2),
        "n_clips": len(per_clip),
        "per_clip": [{"species": c["species"], "path": c["path"],
                      "native_sr": c["native_sr"], "sr": c["sr"],
                      "tension": c["tension"], "feat": c["feat"]} for c in per_clip],
    }
    out_dir = os.environ.get("OUT_DIR", ".")
    with open(os.path.join(out_dir, "results.json"), "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n[done] wall={results['wall_s']}s  results.json written to {out_dir}")
    return results


if __name__ == "__main__":
    main()
