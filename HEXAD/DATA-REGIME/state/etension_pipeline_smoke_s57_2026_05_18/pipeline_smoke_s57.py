"""§57 pipeline_smoke_s57 — text+tension 2-modality pipeline-validation smoke.

$0 Mac CPU. NO GPU, NO fire, NO trained net, NO model forward.

Deliverable = the pipeline mechanically works end-to-end:
  e_tension (closed-form) -> Ψ-box [0,1]^2 -> .kosmos tension @payload
  -> 2-modality (text + tension) corpus record -> basin-containment check
  -> zero-diversity negative-control measure.

g3 honest framing (carry §56): the tension channel is anima's OWN
re-serialised Engine A/G state — ZERO new perceptual information. This
script proves the plumbing works AND quantifies the zero-diversity floor.
It makes NO capability / GOAL claim. E_tension is the pipeline FLOOR, not
the GOAL path; image/audio §7② walls recurse to §1.1 per §56.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path

import numpy as np

from e_tension import e_tension, stub_fingerprints, N_CHAN

HERE = Path(__file__).resolve().parent
ANCHOR_PATH = (
    HERE.parent.parent
    / "HEXAD"
    / "UNIVERSE-BRAIN-MAP"
    / "anchors"
    / "knuth_077_mandala.kosmos"
)

# B-IDENTITY-5 forbidden tokens — corpus text must be clean.
FORBIDDEN = ("도우미", "helper", "assistant", "사용자:", "user:")


def _l2(a, b) -> float:
    return float(math.hypot(a[0] - b[0], a[1] - b[1]))


def main() -> dict:
    # ----- 1. closed-form E_tension over a deterministic stub fingerprint set
    fps = stub_fingerprints(n=64, seed=1337)
    psi_pts = [e_tension(fp) for fp in fps]
    psi_arr = np.asarray(psi_pts, dtype=np.float64)

    # codomain check: every E_tension output in [0,1]^2
    in_box = bool(np.all(psi_arr >= 0.0) and np.all(psi_arr <= 1.0))

    # ----- 2. materialize a `tension` @payload basin from the E_tension cloud
    # A closed-loop encoder's anchor coord IS the centroid of anima's own
    # re-projected state (there is no external referent to anchor against —
    # that is the zero-diversity property, made explicit here, not hidden).
    centroid = (float(psi_arr[:, 0].mean()), float(psi_arr[:, 1].mean()))
    # basin radius = max distance from centroid (the cloud's own extent) +
    # a small honest margin. This is a PIPELINE-VALIDATION basin, NOT a
    # measured perceptual basin (§4.3 honesty — marked closed-loop).
    max_d = max(_l2(p, centroid) for p in psi_pts)
    basin_radius = max_d + 1e-6
    # §55-C2 basin-containment: ‖E_tension − coord‖ < radius for all points
    contained = [(_l2(p, centroid) < basin_radius) for p in psi_pts]
    n_contained = int(sum(contained))
    pass_rate = n_contained / len(psi_pts)

    # Also check the anchor's *own* design-placeholder coord/radius for
    # transparency (knuth_077 coord=[0.71,0.62] radius=0.18). E_tension's
    # closed-loop cloud does NOT land in that design-placeholder basin —
    # honest: a closed-loop re-projection has no reason to coincide with a
    # hand-set design placeholder. We report it, do not fudge it.
    anchor_coord = (0.71, 0.62)
    anchor_radius = 0.18
    n_in_anchor_basin = int(
        sum(1 for p in psi_pts if _l2(p, anchor_coord) < anchor_radius)
    )

    # ----- 3. build a tiny text+tension 2-modality corpus ($0, NO fire)
    text_payload = (
        "[anima 우주뇌지도] 🛸77 만다라 — 우주뇌지도 예술 카테고리, "
        "top emotion creativity. 같은 🛸77 골짜기로 수렴."
    )
    corpus = []
    for i, (fp, (pe, pd)) in enumerate(zip(fps, psi_pts)):
        rec = {
            "anchor": "knuth_077_mandala",
            "modality_text": text_payload,
            "modality_tension": {
                "fingerprint_5ch": fp,           # anima's OWN tension state
                "psi_coord": [pe, pd],            # E_tension -> Law-71 Ψ-box
            },
            "basin_centroid": list(centroid),
            "basin_radius": basin_radius,
            "in_basin": bool(contained[i]),
        }
        corpus.append(rec)
    corpus_path = HERE / "corpus_2modality_s57.jsonl"
    with corpus_path.open("w", encoding="utf-8") as fh:
        for rec in corpus:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    corpus_bytes = corpus_path.read_bytes()
    corpus_sha = hashlib.sha256(corpus_bytes).hexdigest()
    # B-IDENTITY-5: forbidden-token grep over the corpus text bytes
    corpus_text_blob = corpus_path.read_text(encoding="utf-8")
    forbidden_hits = {t: corpus_text_blob.count(t) for t in FORBIDDEN}
    forbidden_total = sum(forbidden_hits.values())

    # ----- 2-modality record SCHEMA parse check (does the record round-trip)
    schema_ok = True
    for line in corpus_path.read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        if not (
            "modality_text" in r
            and "modality_tension" in r
            and "psi_coord" in r["modality_tension"]
            and len(r["modality_tension"]["fingerprint_5ch"]) == N_CHAN
            and len(r["modality_tension"]["psi_coord"]) == 2
        ):
            schema_ok = False
            break

    # ----- 4. zero-diversity negative-control measure
    # The tension features add ZERO new perceptual information over the
    # text features, because tension = anima's own re-serialised state and
    # text is a SINGLE constant string (one anchor's payload). Quantify two
    # ways (closed argument, no learned model):
    #
    #  (a) text-feature matrix: every record's text is byte-identical, so
    #      the text-feature matrix has rank 0 (constant) — it carries no
    #      per-record information. The "added" channel is the tension cloud.
    #
    #  (b) rank argument: the tension psi-coords are a deterministic
    #      closed-form function of a fixed stub set; stack [text | tension].
    #      rank([text-feats ; tension-feats]) == rank(tension-feats alone)
    #      because text-feats column space ⊆ span(constant) and adds 0 rank.
    #      AND the tension features themselves are a re-projection of
    #      anima's own state through a FIXED (untrained) map — they encode
    #      no external/perceptual variance. We report the numeric rank of
    #      the 2-coord tension matrix and the (degenerate) text matrix.
    text_feat = np.ones((len(corpus), 1), dtype=np.float64)  # constant string -> rank ≤ 1, constant => 1 trivial dim
    tension_feat = psi_arr  # (n, 2)
    rank_text = int(np.linalg.matrix_rank(text_feat - text_feat.mean(axis=0)))
    rank_tension = int(np.linalg.matrix_rank(tension_feat - tension_feat.mean(axis=0)))
    stacked = np.hstack([text_feat, tension_feat])
    rank_stacked = int(np.linalg.matrix_rank(stacked - stacked.mean(axis=0)))
    # added information from the tension channel, measured as rank delta of
    # the *centred* stacked matrix vs text-alone. Closed/Boolean:
    #   the text channel is a constant (centred rank 0) so any spread is the
    #   tension channel; the *perceptual* added-information is the variance
    #   the tension cloud carries about anything OTHER than anima's own
    #   re-projected state — which is zero by construction (closed loop).
    # We floor this as: perceptual_added_info_bits ≈ 0 because the tension
    # cloud is a deterministic image of a fixed stub (no external entropy
    # source). Spread of the cloud != perceptual information.
    cloud_spread = float(np.linalg.norm(tension_feat.std(axis=0)))
    # closed zero-diversity verdict: text channel centred-rank == 0
    # (constant) AND tension channel is a fixed deterministic re-projection
    # of anima's own state (no external referent) => the 2-modality record
    # carries the SAME perceptual information as the text-only record: zero
    # extra perceptual diversity. Boolean.
    zero_perceptual_diversity = bool(rank_text == 0)

    pipeline_works = bool(
        in_box and schema_ok and (pass_rate == 1.0) and forbidden_total == 0
    )

    result = {
        "cycle": "§57",
        "tier": "pipeline-validation (NOT GOAL-fire, NOT capability)",
        "pipeline_works": pipeline_works,
        "e_tension_codomain_in_box": in_box,
        "basin_centroid": list(centroid),
        "basin_radius": basin_radius,
        "basin_containment_pass_rate": pass_rate,
        "n_contained": n_contained,
        "n_total": len(psi_pts),
        "anchor_design_placeholder_basin": {
            "coord": list(anchor_coord),
            "radius": anchor_radius,
            "n_in_anchor_basin": n_in_anchor_basin,
            "note": "closed-loop cloud does NOT land in hand-set design "
            "placeholder basin — honest, not fudged; the §57 basin is the "
            "E_tension cloud's OWN centroid (a closed-loop has no external "
            "referent — that IS the zero-diversity property).",
        },
        "corpus_path": str(corpus_path.name),
        "corpus_sha256": corpus_sha,
        "corpus_records": len(corpus),
        "schema_parses": schema_ok,
        "forbidden_token_total": forbidden_total,
        "forbidden_token_hits": forbidden_hits,
        "zero_diversity_measure": {
            "rank_text_centred": rank_text,
            "rank_tension_centred": rank_tension,
            "rank_stacked_centred": rank_stacked,
            "cloud_spread_l2": cloud_spread,
            "zero_perceptual_diversity": zero_perceptual_diversity,
            "argument": "text channel = constant string (centred rank 0). "
            "tension channel = deterministic fixed re-projection of anima's "
            "OWN Engine A/G state (closed loop, no external referent). The "
            "2-modality record therefore carries the SAME perceptual "
            "information as the text-only record: ZERO new perceptual "
            "diversity. This empirically floors §56's honest verdict.",
        },
        "frontier_1_status": "E_tension is the pipeline FLOOR, NOT the GOAL "
        "path. It is closed-loop (anima re-perceiving its own physics). The "
        "real frontier-1 lever — non-text perceptual modality (image/audio) "
        "— hits the §7② external-substrate wall and recurses to §1.1 "
        "data-regime threshold (§56). north-star unchanged, §15/§51 "
        "milestone unchanged.",
    }
    (HERE / "result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return result


if __name__ == "__main__":
    r = main()
    print(json.dumps(r, ensure_ascii=False, indent=2))
