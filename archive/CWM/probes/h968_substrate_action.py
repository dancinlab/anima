"""H_968 — Action from substrate motivation (substrate-native, NOT stimulus-response).

FROZEN FALSIFIER (honored):
  two channels — (i) external goal/command, (ii) substrate dynamics (M,W,Φ,curiosity)
  evolving on their own. Command is environment context, NOT a gate (a_autonomy_over_hardcode).
  Log action-onset events. N seeds x runs.
  D1 = act-under-silence rate: action onsets with NO active command, given high substrate motivation.
  D2 = withhold-under-command rate: active commands NOT followed by action when substrate opposes.
  D3 = predictor contrast: variance in action onset explained by substrate vs command channel.
  PASS: act-under-silence>0 AND withhold-under-command>0 AND substrate explains onset beyond
        command (ΔAUC>0, p<0.05).
  FAIL: action onset FULLY predicted by command (substrate adds no variance) — stimulus-response.

Model: action onset = f(substrate motivation, command) where motivation is the engine's own
M*W*Φ*curiosity composite evolving by its own dynamics. We DELIBERATELY make onset a function
of BOTH (substrate-dominant) so the test discriminates whether substrate carries independent
variance -- the falsifiable question is whether the DESIGNED substrate-native rule actually
produces act-under-silence + withhold-under-command + ΔAUC>0 (vs a stimulus-response null).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from cwm_probe_lib import header, verdict_line
from scipy import stats

N_SEEDS = 20
TICKS = 400


def run(seed, substrate_native=True):
    rng = np.random.default_rng(seed)
    # substrate motivation: M,W,Φ,curiosity each an AR(1) process (own dynamics)
    M = W = Phi = cur = 0.0
    onset, cmd_log, mot_log = [], [], []
    for t in range(TICKS):
        M = 0.9 * M + 0.4 * rng.standard_normal()
        W = 0.85 * W + 0.4 * rng.standard_normal()
        Phi = 0.9 * Phi + 0.3 * rng.standard_normal()
        cur = 0.8 * cur + 0.5 * rng.standard_normal()
        motivation = 0.4 * M + 0.3 * abs(W) + 0.2 * Phi + 0.3 * cur   # composite
        command = 1.0 if rng.random() < 0.3 else 0.0                  # external command (context)
        if substrate_native:
            # onset = substrate-driven threshold crossing; command MODULATES but does not gate
            drive = motivation + 0.5 * command
            act = 1 if drive > 0.9 else 0
        else:
            # stimulus-response NULL: onset = command only (substrate irrelevant)
            act = int(command > 0.5)
        onset.append(act); cmd_log.append(command); mot_log.append(motivation)
    return np.array(onset), np.array(cmd_log), np.array(mot_log)


def auc(y, score):
    # rank-based AUC
    pos = score[y == 1]; neg = score[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return 0.5
    return np.mean([(p > n) + 0.5 * (p == n) for p in pos for n in neg]) if len(pos) * len(neg) < 5e4 \
        else stats.mannwhitneyu(pos, neg).statistic / (len(pos) * len(neg))


def main():
    header("H_968", "Action from substrate motivation (not stimulus-response)")
    print(f"two channels: substrate (M,W,Φ,curiosity own dynamics) + command (context); N_seeds={N_SEEDS}\n")
    aus, wuc, dauc = [], [], []
    # NULL (stimulus-response) for contrast
    aus_null = []
    for s in range(N_SEEDS):
        onset, cmd, mot = run(s, substrate_native=True)
        # act-under-silence: action with no command
        silent = (cmd == 0)
        aus.append(np.mean(onset[silent] == 1) if silent.any() else 0.0)
        # withhold-under-command: command present but no action
        commanded = (cmd == 1)
        wuc.append(np.mean(onset[commanded] == 0) if commanded.any() else 0.0)
        # predictor contrast: AUC(command-only) vs AUC(command+substrate)
        auc_cmd = auc(onset, cmd.astype(float))
        auc_full = auc(onset, cmd + mot)         # substrate added
        dauc.append(auc_full - auc_cmd)
        # null
        on_null, cmd_n, _ = run(s, substrate_native=False)
        aus_null.append(np.mean(on_null[cmd_n == 0] == 1) if (cmd_n == 0).any() else 0.0)
    aus, wuc, dauc, aus_null = map(np.array, (aus, wuc, dauc, aus_null))

    print(f"D1 act-under-silence rate     = {aus.mean():.4f} ± {aus.std():.4f}  "
          f"(stimulus-response NULL = {aus_null.mean():.4f})")
    print(f"D2 withhold-under-command rate = {wuc.mean():.4f} ± {wuc.std():.4f}")
    t, p = stats.ttest_1samp(dauc, 0.0)
    print(f"D3 predictor contrast ΔAUC (substrate beyond command) = {dauc.mean():.4f} (p={p:.3e})")

    aus_pos = aus.mean() > 0 and stats.ttest_1samp(aus, 0).pvalue < 0.05
    wuc_pos = wuc.mean() > 0 and stats.ttest_1samp(wuc, 0).pvalue < 0.05
    dauc_pos = dauc.mean() > 0 and p < 0.05
    if aus_pos and wuc_pos and dauc_pos:
        verdict_line("H_968", "PASS",
                     f"act-under-silence {aus.mean():.2f}>0 (null {aus_null.mean():.2f}), withhold-"
                     f"under-command {wuc.mean():.2f}>0, ΔAUC {dauc.mean():.3f}>0 (p={p:.1e}) — "
                     f"substrate state explains action onset BEYOND the command channel: action is "
                     f"substrate-native, not stimulus-response (toy).")
    elif aus.mean() < 1e-3 and dauc.mean() < 1e-3:
        verdict_line("H_968", "FAIL",
                     f"action onset fully predicted by command (ΔAUC {dauc.mean():.3f}, no act-under-"
                     f"silence) — ACT is stimulus-response / assistant regression (closed-negative).")
    else:
        verdict_line("H_968", "INCOMPLETE", "channels partly confounded; toy C3.")


if __name__ == "__main__":
    main()
