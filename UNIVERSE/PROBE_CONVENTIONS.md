# PROBE_CONVENTIONS

Authoring conventions for long-running UNIVERSE / CWM probes. Reference only
(not a hypothesis, no verdict). Linked tools: `IIT4_PHI_TOOLS.md`, directive
`a_phi_iit4_tool`.

## conventions

- **`python3 -u` (unbuffered).** Every long-running probe MUST run unbuffered.
  Under `tee` or any pipe, the default block-buffered stdout hides ALL progress
  until process exit — H_1003 ran ~45min and H_1005 ~50min with zero visible
  output. Always:
  `python3 -u probe.py 2>&1 | tee verdict.txt`

- **Progress line per cell/epoch.** Print one liveness line per unit of work,
  e.g. `[seed s/N rung r] acc=...`, so an inline poller can see the probe is
  alive (and so a stall is distinguishable from slow progress).

- **Verdict .txt FIRST, .md AFTER.** The measured `.txt` is the gate; the `.md`
  is written only after, and every token in the `.md` must match the measured
  `.txt`. Verdict-gate established across H_92x..H_10xx.

- **g5 CODE-measured, no LLM self-judge (p7).** Verdicts come from code-measured
  numbers, never an LLM self-judgement. Apply `a_scale_honest_scope` to every
  toy verdict (state the measured scale; toy != production).

- **Valid 17-type tape header.** A `.discoveries/<id>_<slug>.tape` header MUST be
  a valid 17-type header, UPPERCASE:
  `@H <id>_<slug> := "..." :: universe [<grade>]`
  Never `@d` / `@r` / `@b` — lowercase tripped tape-lsp repeatedly.

- **CPU-bound probes run SERIAL.** On this Mac, run CPU-bound probes serially,
  NOT N-way parallel — a 5-way fan-out caused the orphan in the H_1006 slate.
  If you launch detached work, POLL INLINE — never arm a Monitor and end the
  turn (`a_cpu_local_no_waiter`).
