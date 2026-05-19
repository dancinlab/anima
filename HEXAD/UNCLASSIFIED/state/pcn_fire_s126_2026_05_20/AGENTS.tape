#!/usr/bin/env tape
# AGENTS.tape — pcn_fire_s126_2026_05_20 remote-dispatch directory.
# Local governance (nearest-dir-wins) for the RunPod / vast.ai dispatch
# scripts in this folder. Authored 2026-05-20 after the L145 incident.

@V := "tape" :: spec [active]
  version = "1.2"

# ─── §1 Identity ─────────────────────────────────────────────────────

@I id001 := "pcn-fire-s126-dispatch" :: identity-claim [d=2026-05-20 active]
  kind = "remote GPU-host dispatch scripts (RunPod / vast.ai)"
  brief = "train_pcn_s126.py launcher + dispatch_s126_runpod.sh remote wrapper"

# ─── §2 Governance ───────────────────────────────────────────────────

@D g1 := "structured-argv-only — no shell command strings" :: governance [required d=2026-05-20 active]
  rule = "Every command dispatched to a remote host (RunPod / vast.ai / SSH) MUST be built as a structured argv list ([]str), never as a single shell command string. No `ssh host 'long inline command'`; comments live OUTSIDE the command, as `#` shell comments above it."
  why = "A shell command string is re-parsed by the remote shell — unquoted globs, C-style `/* */` comments, and word-splitting silently corrupt argv. `bash -n` is a SYNTAX check and passes such strings; the corruption only surfaces at remote runtime as an argparse crash, far from the cause."
  incident = "dispatch_s126_runpod.sh L145 carried a C-style `/* PCN has no negative samples */` line. The remote shell glob-expanded `/*` -> `/bin /boot /etc ...` and `*/` -> cwd dirs, appending the lot to train_pcn_s126.py argv -> argparse died with 'unrecognized arguments'. Fixed by deleting the line and moving the note to a `#` shell comment."
  apply = "argv stays a list end-to-end, e.g. [\"python3\",\"-u\",\"train_pcn_s126.py\",\"--mode\",\"main\",\"--steps\",steps]. The remote exec receives the list directly (execve-style) with NO intermediate `sh -c`."
  forbidden = "C-style `/* */` anywhere in a shell context · unquoted command strings through `ssh host '...'` · building a command via string concatenation."
  enforcement = "Approach C — eliminate the shell-string class entirely so the corruption is unrepresentable, not merely catchable. Chosen over (A) lint the .sh strings and (B) move dispatch to hexa but keep string commands."

# ─── §3 Notes ────────────────────────────────────────────────────────

@N n1 := "upstream — hexa-lang stdlib/cloud" :: note [d=2026-05-20 active]
  text = "The structured-argv dispatch API lives upstream in hexa-lang as stdlib/cloud/ — cycle A LANDED 2026-05-20 (branch stdlib-cloud-a, worktree ~/core/hexa-lang-cloud-a/stdlib/cloud/ — cloud.hexa + cloud_cli.hexa + README.md + design.md, commit 175b9775+). API: cloud_run(host, argv[]) -> CloudResult (run+wait; fields ok/exit_code/pid/stdout_/message), cloud_nohup(host, argv[], logfile) (background long job + remote pid), cloud_poll(host, pid) (liveness), *_opts variants (ephemeral RunPod/vast.ai pod — custom -p <publicPort> + ssh opts), cloud_lint_argv. Each argv element is POSIX-quoted so the remote shell can ONLY word-split it back to the exact original list — the L145 shell-string corruption class (unquoted glob / C-style /* */ / word-split) is unrepresentable, not merely caught. Once stdlib/cloud merges to hexa-lang main, the scripts in this directory are rewritten on top of it and become compile-checked. Scope roadmap A->B: cycle A = generic SSH structured-dispatch core (DONE); cycle B = RunPod + vast.ai provider wrappers (pod create / teardown / billing) — pending."

@N n2 := "decision record" :: note [d=2026-05-20 active]
  text = "Decision 1 — approach C (structured argv, eliminate shell-string class). Decision 2 — scope A then B (A->B phased). Both settled 2026-05-20."
