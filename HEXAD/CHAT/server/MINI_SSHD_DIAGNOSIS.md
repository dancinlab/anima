# MINI_SSHD_DIAGNOSIS

_cycle 7/BD · current-state · 2026-05-23 · supersedes [[PHASE1_STATUS]] §3 blocker #1 status_

## §1 — Verdict

**INCONCLUSIVE — blocker is NOT reproducing.** `mini sshd exec channel refused` (round 6-9, 2026-05-22) no longer observable as of 2026-05-23 18:06 KST. SSH `exec` + `scp` to `mini` succeed cleanly. Diagnostic tool reports CLEAN across all 5 suspected causes.

## §2 — Evidence

`ssh mini -- echo ok` from host `ghost` returned `ok` exit 0 (3/3 trials, 18:06:42). `scp /tmp/mini_sshd_diag.hexa mini:/tmp/` succeeded silently. PR #153's `mini_sshd_diag.hexa` (301 LoC) executed remotely via `ssh mini -- ~/.hx/bin/hexa run /tmp/mini_sshd_diag.hexa` exit 0, 118 lines stdout.

Diag summary (verbatim):
```
- [clean] ssh_rc           (no ~/.ssh/rc file)
- [clean] sshd_config      (only Subsystem sftp; no ForceCommand / MaxSessions 0 / Allow*)
- [clean] authorized_keys  (no command= / no-pty / restrict options)
- [clean] sshd_log         (libsystem_info noise only — no Permission denied / Operation not permitted)
- [clean] launchd          (com.openssh.sshd enabled; Remote Login query needs sudo, deferred)
```

User identity confirmed in `com.apple.access_ssh` group (cause #5 ruled out). `authorized_keys:1` key options observed `pty user-rc x11-forwarding` — `user-rc` is enabled but no `~/.ssh/rc` exists, so cause #1 is fully cleared.

## §3 — What changed between round 9 and now

Unknown. No mini config modification was performed by this cycle (g34 surgical). Plausible recovery triggers:

- mini reboot or sshd restart by operator between round 9 and now (~24 hr window)
- transient kernel / launchd state cleared on its own
- intermittent network condition (mini.local mDNS resolution) recovered

The diag tool found zero persistent misconfiguration, so when the issue recurs (if it does) the root cause is **NOT** in the 5 categories the tool covers — search must widen to:

- TCC / Full Disk Access on `sshd-keygen-wrapper` (cause #4 partial — tool's `_sudo` was denied, only the `launchctl print` portion surfaced)
- macOS 25.5.0 kernel-level session / pty allocation faults (visible in `log show --predicate 'process == "kernel"'`)
- LaunchDaemon throttling under burst connection load (round 6 onset coincided with rapid-fire deploy attempts)

## §4 — Recommended next action

1. **Unblock Phase 1 telemetry deploy NOW** while sshd is responsive: `telemetry_harness.hexa` + `akida_consumer.hexa` + `telemetry_status.hexa` nohup deploy on mini (see [[PHASE1_STATUS]] §3 blocker #1 resolution path). Do not wait for a "permanent fix" — the symptom is not currently active.
2. **Capture state for next recurrence** — when channel-reject re-appears, run from another host **before any restart**: `sudo log stream --predicate 'process == "sshd" OR process == "kernel"'`, save 60 s, then run PR #153's diag locally on mini console. Compare diag output diff vs this cycle's all-clean baseline.
3. **Do NOT merge PR #153 as-is** if the operator wants `_sudo` log access — the tool's `sudo -n` swallows password prompts. Either run with prior `sudo -v` on console, or add a `--with-sudo` flag in a follow-up cycle.

Cross-link: [[PHASE1_STATUS]] §3 blocker #1, PR #153 (`feat/chat-mini-sshd-diag-hexa`, OPEN).
