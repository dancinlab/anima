#!/usr/bin/env python3
# raw#37 transient — emitted by anima-eeg/tool/resting_state_network_analyzer.hexa
import argparse, hashlib, json, os, sys, time
import numpy as np
from scipy.signal import welch, coherence

# canonical 16ch order (Cyton+Daisy, this rig)
CH = ['Fp1','Fp2','C3','C4','P7','P8','O1','O2','F7','F8','F3','F4','T7','T8','P3','P4']
IDX = {n:i for i,n in enumerate(CH)}

def band_power(x, fs, lo, hi):
    f, p = welch(x, fs=fs, nperseg=min(len(x), int(fs*4)))
    m = (f>=lo)&(f<=hi)
    return float(np.trapezoid(p[m], f[m])) if m.any() else 0.0

def total_power(x, fs):
    f, p = welch(x, fs=fs, nperseg=min(len(x), int(fs*4)))
    return float(np.trapezoid(p, f))

def alpha_coh(a, b, fs, lo=8.0, hi=13.0):
    f, c = coherence(a, b, fs=fs, nperseg=min(len(a), int(fs*4)))
    m = (f>=lo)&(f<=hi)
    return float(c[m].mean()) if m.any() else 0.0

def synth_dmn(fs=125.0, dur=60.0, corr=0.85, seed=0):
    rng = np.random.default_rng(seed)
    n = int(fs*dur); t = np.arange(n)/fs
    base_alpha = np.sin(2*np.pi*10.0*t) + 0.3*rng.standard_normal(n)
    X = np.zeros((16, n))
    # anterior DMN (Fp1, Fp2) and posterior DMN (P3, P4) share alpha source
    for nm in ['Fp1','Fp2','P3','P4']:
        i = IDX[nm]
        X[i] = corr*base_alpha + (1-corr)*rng.standard_normal(n)
    # right frontal stronger alpha than left (positive asymmetry)
    for nm,scale in [('F3',0.4),('F7',0.4),('F4',0.9),('F8',0.9)]:
        i = IDX[nm]
        X[i] = scale*np.sin(2*np.pi*10.0*t) + 0.3*rng.standard_normal(n)
    # occipital alpha
    for nm in ['O1','O2']:
        i = IDX[nm]
        X[i] = 0.8*np.sin(2*np.pi*10.0*t) + 0.3*rng.standard_normal(n)
    # other channels: noise only
    for nm in ['C3','C4','P7','P8','T7','T8']:
        i = IDX[nm]
        X[i] = rng.standard_normal(n)
    return X

def analyze(X, fs):
    # nodes
    ant = (X[IDX['Fp1']] + X[IDX['Fp2']]) / 2.0
    pos = (X[IDX['P3']]  + X[IDX['P4']])  / 2.0
    occL = X[IDX['O1']]; occR = X[IDX['O2']]
    p7   = X[IDX['P7']]; p8   = X[IDX['P8']]
    # DMN α-coherence (anterior↔posterior)
    coh_ap = alpha_coh(ant, pos, fs)
    coh_aL = alpha_coh(ant, p7,  fs)
    coh_aR = alpha_coh(ant, p8,  fs)
    coh_anterior_occ = (alpha_coh(ant, occL, fs) + alpha_coh(ant, occR, fs))/2.0
    # frontal alpha asymmetry (Davidson 1992) — log(R) − log(L)
    aL = (band_power(X[IDX['F3']], fs, 8, 13) + band_power(X[IDX['F7']], fs, 8, 13))/2.0
    aR = (band_power(X[IDX['F4']], fs, 8, 13) + band_power(X[IDX['F8']], fs, 8, 13))/2.0
    eps = 1e-12
    logL = float(np.log(aL + eps)); logR = float(np.log(aR + eps))
    asym = logR - logL
    # occipital alpha ratio
    o1_ratio = band_power(occL, fs, 8, 13) / max(total_power(occL, fs), eps)
    o2_ratio = band_power(occR, fs, 8, 13) / max(total_power(occR, fs), eps)
    occ_max = float(max(o1_ratio, o2_ratio))
    return {
        'dmn_coh_alpha': coh_ap, 'dmn_coh_anterior_lateral_l': coh_aL,
        'dmn_coh_anterior_lateral_r': coh_aR, 'dmn_coh_anterior_occipital': coh_anterior_occ,
        'alpha_pow_left': aL, 'alpha_pow_right': aR,
        'alpha_log_left': logL, 'alpha_log_right': logR,
        'frontal_alpha_asymmetry': asym,
        'occipital_alpha_ratio_o1': o1_ratio,
        'occipital_alpha_ratio_o2': o2_ratio,
        'occipital_alpha_ratio_max': occ_max,
    }

def falsifier_synth_uncorrelated(fs=125.0, dur=60.0, seed=1):
    rng = np.random.default_rng(seed); n = int(fs*dur)
    return rng.standard_normal((16, n))

def falsifier_synth_constant(fs=125.0, dur=60.0):
    n = int(fs*dur); return np.zeros((16, n)) + 1e-9

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mode', required=True, choices=['selftest','real','falsifier'])
    ap.add_argument('--input', default='')
    ap.add_argument('--fs', type=float, default=125.0)
    ap.add_argument('--falsifier', default='uncorrelated')
    a = ap.parse_args()
    if a.mode == 'selftest':
        X = synth_dmn(a.fs, 60.0, 0.85, 0); src='synthetic_correlated'
    elif a.mode == 'falsifier':
        if a.falsifier == 'constant': X = falsifier_synth_constant(a.fs, 60.0); src='synth_constant'
        else: X = falsifier_synth_uncorrelated(a.fs, 60.0, 1); src='synth_uncorrelated'
    else:
        X = np.load(a.input); src=a.input
        if X.shape[0] != 16: print('ERR shape', X.shape, file=sys.stderr); sys.exit(2)
    sha = hashlib.sha256(X.tobytes()).hexdigest()
    out = analyze(X, a.fs)
    out['source'] = src; out['n_samples'] = int(X.shape[1])
    out['fs_hz'] = float(a.fs); out['data_sha256'] = sha
    out_path = os.environ.get('RSN_HELPER_OUT', '/tmp/rsn_helper_out.json')
    with open(out_path, 'w') as f: f.write(json.dumps(out))
    print(json.dumps(out))

if __name__ == '__main__': main()
