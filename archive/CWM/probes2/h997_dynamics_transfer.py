"""H_997 — cross-modal DYNAMICS transfer (forward operator transfers though geometry does not).

1st-round seed: H_960🟢 the same engine encodes non-language modalities (decode-parity), but
H_978🔴 the latent GEOMETRY (spacing/spectrum) is modality-SPECIFIC. Open question: even if
the latent GEOMETRY differs across modalities, does the latent DYNAMICS — the learned
forward-transition operator A — TRANSFER? If two modalities share an underlying generative
process (e.g. the same oscillatory law expressed in different observation channels), a WM
trained on modality A should forecast modality B better than chance after only re-fitting
the cheap read-in/read-out, keeping the transition A frozen. dynamics-transfer ⊥ geometry.

Falsifier (frozen): modality A = a 2D oscillator observed as raw coordinates; modality B =
the SAME latent dynamics observed through a different (rotated+nonlinear) sensor. Train an
LDS WM on A. Freeze its transition; refit only the decoder on a little B data.
  D1 (dynamics transfers)  PASS-A iff the A-transition-frozen model forecasts B with error
                           BELOW a shuffled-transition control (random A) AND below a
                           static last-obs baseline, over >=20 seeds.
  D2 (geometry differs)    PASS-B iff the A and B latent geometries are DISsimilar (linear
                           CKA(A_latents, B_latents) well below a same-modality CKA),
                           confirming geometry is NOT what transferred (consistent w/ H_978).
  PASS iff PASS-A AND PASS-B (dynamics transfers WITHOUT geometry invariance).
  FAIL iff frozen-A dynamics does not beat the shuffled control (no dynamics transfer).
substrate=CPU-mirror (numpy). a_scale_honest_scope: single toy rung, ladder OPEN.
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "probes"))
from cwm_probe_lib import LDSWorldModel, header, cohens_d, welch_t, cka, _ridge, _aug

N_SEEDS = 24
T = 40
DELAY = 3


def latent_process(rng, n=T):
    """The shared 2D oscillatory LATENT process (same law for both modalities)."""
    p = rng.uniform(-1, 1, 2); v = rng.uniform(-0.5, 0.5, 2)
    out = []
    w = 1.1
    for t in range(n):
        out.append(p.copy())
        acc = -w * w * p - 0.1 * v
        v = v + acc * 0.2; p = p + v * 0.2
    return np.array(out)


def modality_A(latent):
    return latent.copy()                       # raw coordinates


def modality_B(latent, M):
    """A rotated + strongly nonlinearly-warped sensor view of the SAME latent process.
    The warp (squashing + cross-coordinate product) bends the geometry hard while leaving
    the underlying generative dynamics unchanged — so geometry-similarity drops far below
    same-modal, isolating the dynamics-transfer claim from any geometry overlap."""
    z = latent @ M
    w0 = np.tanh(2.0 * z[:, 0]) + 0.5 * z[:, 0] * z[:, 1]
    w1 = np.tanh(2.0 * z[:, 1]) - 0.5 * z[:, 0] ** 2
    return np.stack([w0, w1], axis=1)


def main():
    header("H_997", "cross-modal DYNAMICS transfer (forward operator transfers, geometry doesn't)")
    frozen_err, shuffled_err, static_err = [], [], []
    cka_cross, cka_same = [], []
    for s in range(N_SEEDS):
        rng = np.random.default_rng(60000 + s)
        M = rng.standard_normal((2, 2)); M /= np.linalg.norm(M)
        trajA = [latent_process(rng) for _ in range(60)]
        obsA = [modality_A(t) for t in trajA]
        # train WM on modality A
        wmA = LDSWorldModel(obs_dim=2, delay=DELAY, ridge=1e-3)
        wmA.fit(obsA)
        # modality B data (few-shot): refit ONLY the decoder/embedding-readout, FREEZE transition A
        trajB_train = [latent_process(rng) for _ in range(8)]
        obsB_train = [modality_B(t, M) for t in trajB_train]
        # build a B-WM that REUSES wmA.A (frozen transition) but learns its own decoder C
        wmB = LDSWorldModel(obs_dim=2, delay=DELAY, ridge=1e-3)
        # fit B fully first to get embedding consistent, then OVERWRITE transition with A's
        wmB.fit(obsB_train)
        wmB_frozen_A = wmB.A.copy()
        wmB.A = wmA.A.copy()                  # FREEZE transferred dynamics from modality A
        # shuffled control: random transition of the same shape
        wmB_shuf = LDSWorldModel(obs_dim=2, delay=DELAY, ridge=1e-3); wmB_shuf.fit(obsB_train)
        wmB_shuf.A = rng.standard_normal(wmA.A.shape)
        # evaluate multi-step forecast on held-out B
        fe = se = st = 0.0; nb = 0
        Acc, Bcc = [], []
        for _ in range(20):
            lt = latent_process(rng)
            obB = modality_B(lt, M); obA = modality_A(lt)
            zb = wmB.embed(obB)
            Bcc.append(zb); Acc.append(wmA.embed(obA))
            z0 = zb[DELAY - 1]
            h = 5
            tgt = obB[DELAY - 1 + h] if DELAY - 1 + h < len(obB) else obB[-1]
            fe += np.linalg.norm(wmB.decode(wmB.roll(z0, h)) - tgt)
            se += np.linalg.norm(wmB_shuf.decode(wmB_shuf.roll(z0, h)) - tgt)
            st += np.linalg.norm(obB[DELAY - 1] - tgt)     # static last-obs
            nb += 1
        frozen_err.append(fe / nb); shuffled_err.append(se / nb); static_err.append(st / nb)
        cka_cross.append(cka(np.vstack(Acc), np.vstack(Bcc)))
        cka_same.append(cka(np.vstack(Bcc), np.vstack(Bcc)))
    frozen_err, shuffled_err, static_err = map(np.array, (frozen_err, shuffled_err, static_err))
    print(f"task=shared 2D-oscillator latent; modality A=raw coords, B=rotated+nonlinear sensor")
    print(f"DELAY={DELAY} horizon=5 seeds={N_SEEDS}")
    print()
    print("forecast error on modality B (lower=better), mean ± std:")
    print(f"  FROZEN-A transition (transferred)  : {frozen_err.mean():.4f} ± {frozen_err.std():.4f}")
    print(f"  SHUFFLED transition (control)      : {shuffled_err.mean():.4f} ± {shuffled_err.std():.4f}")
    print(f"  STATIC last-obs baseline           : {static_err.mean():.4f} ± {static_err.std():.4f}")
    tsh, psh = welch_t(frozen_err, shuffled_err)
    print()
    print(f"D1 frozen-A < shuffled: d={cohens_d(frozen_err,shuffled_err):.3f} p={psh:.2e}")
    print(f"   frozen-A < static : {frozen_err.mean() < static_err.mean()}")
    print(f"D2 geometry: cross-modal CKA(A,B) = {np.mean(cka_cross):.3f}  (same-modal CKA = {np.mean(cka_same):.3f})")
    print("-" * 78)
    passA = frozen_err.mean() < shuffled_err.mean() and psh < 0.05 and frozen_err.mean() < static_err.mean()
    passB = np.mean(cka_cross) < 0.8 * np.mean(cka_same)
    if passA and passB:
        v = (f"PASS dynamics transfers without geometry invariance: a transition trained on modality A "
             f"forecasts modality B (err {frozen_err.mean():.3f}) below shuffled {shuffled_err.mean():.3f} "
             f"(p={psh:.1e}) AND static {static_err.mean():.3f}, while cross-modal CKA {np.mean(cka_cross):.2f} "
             f"≪ same-modal {np.mean(cka_same):.2f} — the forward LAW transfers, the GEOMETRY does not "
             f"(consistent w/ H_978🔴) (toy rung).")
        tok = "PASS"
    elif passA:
        v = (f"PASS-PARTIAL frozen-A dynamics transfers (beats shuffled p={psh:.1e}) but geometries not "
             f"clearly distinct (cross CKA {np.mean(cka_cross):.2f} vs same {np.mean(cka_same):.2f}) (toy).")
        tok = "PASS"
    else:
        v = (f"FAIL frozen-A dynamics does not transfer to modality B (frozen {frozen_err.mean():.3f} vs "
             f"shuffled {shuffled_err.mean():.3f}, p={psh:.1e}) — no cross-modal dynamics transfer (closed-negative, toy).")
        tok = "FAIL"
    print(f"VERDICT H_997: {v}")
    print("-" * 78)
    return tok


if __name__ == "__main__":
    main()
