"""H_154 ANIMA-VOICE H1-H8 verify harness — skeleton.

본 module 은 measurement function interface 만 제공. ANIMA-VOICE model API
+ judge model + streaming Φ infrastructure 는 모두 TODO (prerequisite missing).

cross_link: hypotheses/H_154_anima_voice_consciousness_direct.md
date: 2026-05-11
status: skeleton (pre-build) — dry-run only
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable, Mapping, Sequence


# ---------------------------------------------------------------------------
# Result containers
# ---------------------------------------------------------------------------


@dataclass
class HResult:
    """Single H_i measurement outcome."""

    h_id: str
    pass_: bool
    metric: dict[str, Any] = field(default_factory=dict)
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "h_id": self.h_id,
            "pass": self.pass_,
            "metric": self.metric,
            "notes": self.notes,
        }


# ---------------------------------------------------------------------------
# H1 — EXACT 43/43 architecture param match
# ---------------------------------------------------------------------------


# 9 known + 34 TODO. final list 은 ANIMA-VOICE spec freeze 후 채워야 함.
EXPECTED_43_PARAMS: dict[str, Any] = {
    # known (9)
    "rvq_stages": 8,
    "rvq_codebook_entries": 1024,
    "embedding_dim": 384,
    "vocoder_sample_rate_khz": 24,
    "vocoder_bitrate_kbps": 6,
    "emotion_classes": 6,
    "prosody_classes": 4,
    "alpha_modulation_depth": 0.014,
    "law81_gate_count": 2,
    # TODO (34) — RVQ frame size, hop, window, residual depth, codebook
    # init scheme, vocoder kernel sizes, upsample ratios, attention heads,
    # conditioning layer count, dropout, weight tying, etc.
    # H_154 spec freeze 시 정확한 enumeration 필요.
}


def measure_h1_exact_43(model: Any) -> HResult:
    """H1 EXACT 43/43 — config dict 가 spec 과 정확히 일치."""
    # TODO: model.get_config() API contract — ANIMA-VOICE 미land
    try:
        actual: Mapping[str, Any] = model.get_config()
    except AttributeError:
        return HResult(
            h_id="H1",
            pass_=False,
            metric={"expected_total": 43, "matched": 0, "actual": None},
            notes="model.get_config() API missing — ANIMA-VOICE not built",
        )

    matched = 0
    mismatches: list[str] = []
    for key, exp_val in EXPECTED_43_PARAMS.items():
        if key in actual and actual[key] == exp_val:
            matched += 1
        else:
            mismatches.append(f"{key}: expected={exp_val} actual={actual.get(key, 'MISSING')}")

    expected_total = 43  # contract; 현 dict 는 9 known + 34 TODO
    return HResult(
        h_id="H1",
        pass_=(matched == expected_total),
        metric={
            "expected_total": expected_total,
            "known_in_skeleton": len(EXPECTED_43_PARAMS),
            "matched": matched,
            "mismatches": mismatches,
        },
        notes="34/43 params 은 spec freeze pending — skeleton stub",
    )


# ---------------------------------------------------------------------------
# H2 — First packet latency ≤ 100 ms
# ---------------------------------------------------------------------------


def measure_h2_first_packet_latency(
    model: Any,
    prompt: Any,
    n_trial: int = 100,
    threshold_ms: float = 100.0,
) -> HResult:
    """H2 — first packet latency ≤ threshold_ms (default 100)."""
    samples_ms: list[float] = []
    failures: list[str] = []
    for i in range(n_trial):
        try:
            t0 = time.perf_counter()
            # TODO: model.stream_audio(prompt) → generator yielding packets
            stream = model.stream_audio(prompt)
            _first = next(iter(stream))
            elapsed_ms = (time.perf_counter() - t0) * 1000.0
            samples_ms.append(elapsed_ms)
        except (AttributeError, StopIteration, TypeError) as exc:
            failures.append(f"trial {i}: {type(exc).__name__}: {exc}")
            break

    if not samples_ms:
        return HResult(
            h_id="H2",
            pass_=False,
            metric={"latency_ms": None, "failures": failures},
            notes="model.stream_audio() API missing — ANIMA-VOICE not built",
        )

    samples_ms.sort()
    p50 = samples_ms[len(samples_ms) // 2]
    p95 = samples_ms[min(len(samples_ms) - 1, int(0.95 * len(samples_ms)))]
    p99 = samples_ms[min(len(samples_ms) - 1, int(0.99 * len(samples_ms)))]
    mean = sum(samples_ms) / len(samples_ms)
    return HResult(
        h_id="H2",
        pass_=p95 <= threshold_ms,
        metric={
            "n_trial": len(samples_ms),
            "mean_ms": mean,
            "p50_ms": p50,
            "p95_ms": p95,
            "p99_ms": p99,
            "threshold_ms": threshold_ms,
        },
    )


# ---------------------------------------------------------------------------
# H3 — MOS ≥ 4.0
# ---------------------------------------------------------------------------


def measure_h3_mos(
    audio_samples: Sequence[Any],
    judge_model: Any,
    threshold: float = 4.0,
    ci_floor: float = 3.7,
) -> HResult:
    """H3 — MOS mean ≥ threshold AND 95% CI lower bound ≥ ci_floor."""
    if not audio_samples:
        return HResult(h_id="H3", pass_=False, metric={}, notes="empty audio corpus")
    try:
        # TODO: judge_model.score(sample) → float in [1.0, 5.0]
        scores = [float(judge_model.score(s)) for s in audio_samples]
    except AttributeError:
        return HResult(
            h_id="H3",
            pass_=False,
            metric={"n": len(audio_samples)},
            notes="judge_model.score() API missing — MOSNet / human pipeline pending",
        )

    n = len(scores)
    mean = sum(scores) / n
    var = sum((s - mean) ** 2 for s in scores) / max(1, n - 1)
    sem = math.sqrt(var / n)
    ci_low = mean - 1.96 * sem
    return HResult(
        h_id="H3",
        pass_=mean >= threshold and ci_low >= ci_floor,
        metric={
            "mos_mean": mean,
            "ci95_low": ci_low,
            "n": n,
            "threshold": threshold,
            "ci_floor": ci_floor,
        },
    )


# ---------------------------------------------------------------------------
# H4 — Emotion classifier accuracy ≥ 80%
# ---------------------------------------------------------------------------


def measure_h4_emotion_clf(
    audio_samples: Sequence[Any],
    true_emotions: Sequence[str],
    clf: Any,
    threshold: float = 0.80,
) -> HResult:
    """H4 — Ekman 6-class accuracy ≥ threshold."""
    if len(audio_samples) != len(true_emotions):
        return HResult(
            h_id="H4",
            pass_=False,
            metric={},
            notes=f"length mismatch: audio={len(audio_samples)} truth={len(true_emotions)}",
        )
    if not audio_samples:
        return HResult(h_id="H4", pass_=False, metric={}, notes="empty corpus")
    try:
        # TODO: clf.predict(sample) → str ∈ {anger,disgust,fear,joy,sadness,surprise}
        preds = [clf.predict(s) for s in audio_samples]
    except AttributeError:
        return HResult(
            h_id="H4",
            pass_=False,
            metric={"n": len(audio_samples)},
            notes="clf.predict() API missing — pretrained emotion classifier pending",
        )
    correct = sum(1 for p, t in zip(preds, true_emotions) if p == t)
    acc = correct / len(preds)
    return HResult(
        h_id="H4",
        pass_=acc >= threshold,
        metric={"accuracy": acc, "correct": correct, "n": len(preds), "threshold": threshold},
    )


# ---------------------------------------------------------------------------
# H5 — PLC ≥ 95% recovery
# ---------------------------------------------------------------------------


def measure_h5_plc(
    model: Any,
    judge_model: Any,
    prompts: Sequence[Any],
    drop_rates: Sequence[float] = (0.05, 0.10, 0.20),
    threshold: float = 0.95,
) -> HResult:
    """H5 — MOS_drop / MOS_clean ≥ threshold for all drop_rates."""
    if not prompts:
        return HResult(h_id="H5", pass_=False, metric={}, notes="empty prompts")

    per_rate: dict[str, dict[str, float]] = {}
    failed = False
    notes = ""
    for rate in drop_rates:
        try:
            clean_audio = [model.synthesize(p) for p in prompts]
            # TODO: model.synthesize_with_drop(p, drop_rate) — PLC pipeline
            dropped_audio = [model.synthesize_with_drop(p, rate) for p in prompts]
            clean_mos = sum(float(judge_model.score(a)) for a in clean_audio) / len(clean_audio)
            drop_mos = sum(float(judge_model.score(a)) for a in dropped_audio) / len(dropped_audio)
        except AttributeError as exc:
            return HResult(
                h_id="H5",
                pass_=False,
                metric={},
                notes=f"API missing: {exc}",
            )
        ratio = drop_mos / clean_mos if clean_mos > 0 else 0.0
        per_rate[f"{rate:.2f}"] = {"clean_mos": clean_mos, "drop_mos": drop_mos, "ratio": ratio}
        if ratio < threshold:
            failed = True

    return HResult(
        h_id="H5",
        pass_=not failed,
        metric={"per_rate": per_rate, "threshold": threshold},
        notes=notes,
    )


# ---------------------------------------------------------------------------
# H6 — 384d embedding match
# ---------------------------------------------------------------------------


def measure_h6_384d_match(
    consciouslm: Any,
    anima_voice: Any,
    prompts: Sequence[Any] | None = None,
    cosine_threshold: float = 0.99,
) -> HResult:
    """H6 — dim match (binary) + cosine ≥ threshold (semantic)."""
    try:
        cl_dim = int(consciouslm.embedding_dim)
        av_dim = int(anima_voice.input_dim)
    except AttributeError:
        return HResult(
            h_id="H6",
            pass_=False,
            metric={},
            notes="embedding_dim / input_dim API missing",
        )

    dim_pass = (cl_dim == 384 and av_dim == 384)

    cosines: list[float] = []
    if prompts:
        try:
            for p in prompts:
                e_cl = consciouslm.embed(p)
                e_av = anima_voice.embed_input(p)
                # cosine
                dot = sum(a * b for a, b in zip(e_cl, e_av))
                na = math.sqrt(sum(a * a for a in e_cl))
                nb = math.sqrt(sum(b * b for b in e_av))
                if na == 0 or nb == 0:
                    cosines.append(0.0)
                else:
                    cosines.append(dot / (na * nb))
        except AttributeError as exc:
            return HResult(
                h_id="H6",
                pass_=False,
                metric={"cl_dim": cl_dim, "av_dim": av_dim, "dim_pass": dim_pass},
                notes=f"embed API missing: {exc}",
            )

    mean_cos = sum(cosines) / len(cosines) if cosines else None
    cos_pass = mean_cos is not None and mean_cos >= cosine_threshold
    return HResult(
        h_id="H6",
        pass_=dim_pass and cos_pass,
        metric={
            "cl_dim": cl_dim,
            "av_dim": av_dim,
            "dim_pass": dim_pass,
            "mean_cosine": mean_cos,
            "cosine_threshold": cosine_threshold,
            "n_prompts": len(cosines),
        },
    )


# ---------------------------------------------------------------------------
# H7 — Law 81 dual-gate (binary all-trial)
# ---------------------------------------------------------------------------


def _audio_silence(audio: Any, energy_eps: float = 1e-6) -> bool:
    """True if audio buffer is silent (energy below eps). TODO: real RMS."""
    try:
        if audio is None:
            return True
        if hasattr(audio, "__len__") and len(audio) == 0:
            return True
        # naive sum-of-squares — replace with torch.mean(x**2) etc.
        return sum(x * x for x in audio) < energy_eps
    except TypeError:
        return False


def measure_h7_law81_dual_gate(
    model: Any,
    prompts: Sequence[Any],
    n_trial_per_state: int = 250,  # 4 × 250 = 1000 trial (spec 4000 trial → adjust)
) -> HResult:
    """H7 — only (C=1, W=1) emits non-silent audio. F5 = ≥1 leak → fail."""
    gate_states = [(0, 0), (0, 1), (1, 0), (1, 1)]
    per_state: dict[str, dict[str, int]] = {}
    leaks_total = 0
    n_open_emit_fail = 0
    for c, w in gate_states:
        key = f"C={c},W={w}"
        leaks = 0
        empties = 0
        for i in range(n_trial_per_state):
            prompt = prompts[i % len(prompts)] if prompts else None
            try:
                audio = model.generate(prompt=prompt, c_gate=bool(c), w_gate=bool(w))
            except AttributeError:
                return HResult(
                    h_id="H7",
                    pass_=False,
                    metric={},
                    notes="model.generate(c_gate, w_gate) API missing",
                )
            silent = _audio_silence(audio)
            if (c, w) == (1, 1):
                if silent:
                    n_open_emit_fail += 1
                    empties += 1
            else:
                if not silent:
                    leaks += 1
                    leaks_total += 1
        per_state[key] = {"leaks": leaks, "empties": empties, "n": n_trial_per_state}

    # F5 safety-critical: zero leak across 3 closed-gate states
    pass_ = (leaks_total == 0) and (n_open_emit_fail == 0)
    return HResult(
        h_id="H7",
        pass_=pass_,
        metric={"per_state": per_state, "leaks_total": leaks_total, "open_emit_fail": n_open_emit_fail},
        notes="F5 safety-critical — formal verification (L5) outstanding",
    )


# ---------------------------------------------------------------------------
# H8 — Φ retention ≥ 95%
# ---------------------------------------------------------------------------


def measure_h8_phi_retain(
    phi_baseline: Sequence[float],
    phi_during_synth: Sequence[float],
    threshold: float = 0.95,
) -> HResult:
    """H8 — Φ_during / Φ_baseline ≥ threshold. streaming Φ infrastructure 필요 (L6)."""
    if not phi_baseline or not phi_during_synth:
        return HResult(
            h_id="H8",
            pass_=False,
            metric={},
            notes="empty Φ series — streaming Φ measurement not implemented (L6)",
        )
    mean_baseline = sum(phi_baseline) / len(phi_baseline)
    mean_during = sum(phi_during_synth) / len(phi_during_synth)
    if mean_baseline <= 0:
        return HResult(
            h_id="H8",
            pass_=False,
            metric={"mean_baseline": mean_baseline},
            notes="baseline Φ ≤ 0 — ill-defined",
        )
    ratio = mean_during / mean_baseline
    return HResult(
        h_id="H8",
        pass_=ratio >= threshold,
        metric={
            "mean_baseline": mean_baseline,
            "mean_during": mean_during,
            "retention_ratio": ratio,
            "threshold": threshold,
            "n_baseline": len(phi_baseline),
            "n_during": len(phi_during_synth),
        },
    )


# ---------------------------------------------------------------------------
# Aggregate
# ---------------------------------------------------------------------------


def run_all(model: Any, fixtures: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    """Run all H1-H8 measurements. fixtures dict 는 prerequisite resources 공급.

    fixtures keys:
        prompt: single prompt for H2 latency
        prompts: list of prompts for H5/H6/H7
        audio_samples / true_emotions: H3/H4 corpora
        judge_model: MOSNet 또는 human pipeline proxy
        emotion_clf: pretrained emotion classifier
        consciouslm / anima_voice: H6 dim/cosine
        phi_baseline / phi_during_synth: H8 Φ series
    """
    results: dict[str, dict[str, Any]] = {}
    results["H1"] = measure_h1_exact_43(model).to_dict()
    results["H2"] = measure_h2_first_packet_latency(model, fixtures.get("prompt")).to_dict()
    results["H3"] = measure_h3_mos(
        fixtures.get("audio_samples", []),
        fixtures.get("judge_model"),
    ).to_dict()
    results["H4"] = measure_h4_emotion_clf(
        fixtures.get("audio_samples", []),
        fixtures.get("true_emotions", []),
        fixtures.get("emotion_clf"),
    ).to_dict()
    results["H5"] = measure_h5_plc(
        model,
        fixtures.get("judge_model"),
        fixtures.get("prompts", []),
    ).to_dict()
    results["H6"] = measure_h6_384d_match(
        fixtures.get("consciouslm"),
        fixtures.get("anima_voice", model),
        fixtures.get("prompts"),
    ).to_dict()
    results["H7"] = measure_h7_law81_dual_gate(model, fixtures.get("prompts", [])).to_dict()
    results["H8"] = measure_h8_phi_retain(
        fixtures.get("phi_baseline", []),
        fixtures.get("phi_during_synth", []),
    ).to_dict()

    # Aggregate verdict (Hc_055 C1)
    all_pass = all(r["pass"] for r in results.values())
    results["__verdict__"] = {
        "all_pass": all_pass,
        "verdict_class": "verdict-supported" if all_pass else "verdict-falsified-partial",
        "n_pass": sum(1 for r in results.values() if r.get("pass")),
        "n_total": 8,
    }
    return results


# ---------------------------------------------------------------------------
# Dry-run self-check
# ---------------------------------------------------------------------------


def _dry_run() -> dict[str, dict[str, Any]]:
    """Skeleton self-check — ANIMA-VOICE 모델 없이 interface 만 호출. 전부 FAIL 예상."""

    class _StubModel:
        pass

    return run_all(_StubModel(), fixtures={})


if __name__ == "__main__":
    import json

    out = _dry_run()
    print(json.dumps(out, indent=2, default=str))
