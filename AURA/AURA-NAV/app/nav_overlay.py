"""AURA-NAV app — V5/V6 turn-arrow AR-overlay write fidelity (runnable toy).
encode 8-direction GPS turn -> V5/V6 retinotopic arrow map -> modality write (focality + noise)
-> perceived map -> decode (nearest-template classify) + perceived-fidelity R2.
Run: python3 nav_overlay.py   (numpy only, deterministic seeds).
honest: toy (synthetic arrows, gaussian focality). See verify/nav_write_fidelity.txt.
"""
import numpy as np

G = 12
N = G * G

def arrow(angle):
    m = np.zeros((G, G)); c = (G - 1) / 2.0
    for r in np.linspace(0, c - 0.5, 40):
        x = c + r * np.cos(angle); y = c + r * np.sin(angle)
        m[int(round(y)), int(round(x))] = 1.0
    for da in (-0.5, 0.5):
        for r in np.linspace(c - 2.5, c - 0.5, 12):
            x = c + r * np.cos(angle + da); y = c + r * np.sin(angle + da)
            m[int(round(y)) % G, int(round(x)) % G] = 1.0
    return m.flatten()

NA = 8
ANGLES = [2 * np.pi * k / NA for k in range(NA)]
TEMPLATES = [arrow(a) for a in ANGLES]

def blur(x, sigma):
    g = np.arange(G)
    K = np.exp(-((g[:, None] - g[None, :]) ** 2) / (2 * sigma ** 2)); K /= K.sum(1, keepdims=True)
    return (K @ x.reshape(G, G) @ K.T).flatten()

def trial(k, sigma, snr_db, seed, tb):
    rng = np.random.RandomState(seed); y = blur(TEMPLATES[k], sigma)
    p = np.sqrt((y ** 2).mean()); y = y + rng.randn(N) * (p / (10 ** (snr_db / 20)))
    pred = int(np.argmin([((y - t) ** 2).sum() for t in tb]))
    fid = 1 - ((y - tb[k]) ** 2).sum() / ((tb[k] - tb[k].mean()) ** 2).sum()
    return int(pred == k), max(fid, -1)

def run(sigma, snr_db, ntr=240):
    tb = [blur(t, sigma) for t in TEMPLATES]
    rs = [trial(i % NA, sigma, snr_db, i, tb) for i in range(ntr)]
    return 100 * np.mean([r[0] for r in rs]), float(np.mean([r[1] for r in rs]))

if __name__ == "__main__":
    print("modality                     sigma SNR   8-dir acc   fidelity R2")
    for lbl, s, snr in [("EEG-class (blurry)", 2.6, 10), ("OPM-MEG", 1.6, 10),
                        ("tFUS focal", 0.9, 10), ("RTSC-MEG hi-dens", 0.7, 18)]:
        a, f = run(s, snr)
        print(f"{lbl:28}{s:5.1f}{snr:4d}    {a:5.1f}%        {f:.3f}")
