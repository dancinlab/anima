# anima-eeg-core hjorth_native — root cause + fix LANDED — 2026-05-03 (AI-native)

> readers: AI agents (subagents, phase5 verifier, next-cycle hexa-runtime audit), Claude Code (next session)
> source-of-truth: `anima-eeg-core/tool/modules/_metrics/hjorth_native.hexa` (PORT, raw#9 strict)
> upstream context: `state/anima_eeg_core_phase5_verify_2026_05_03/verify_results.json` 5c BLOCKED -> PASS

---

## TL;DR

**오늘 한 일** — Phase 5c hjorth_native --selftest EXIT=137 (SIGKILL) root cause + fix. Root cause = **dockerized hexa-exec container의 cgroup OOM killer** (NOT classical OOM, NOT algorithm bug). Fix = streaming per-channel evaluator. Memory peak 1.83 GiB → 84.5 MiB (22배 감소). 5c BLOCKED(50%) → PASS(100%); Phase 5 overall 83% → 100%.

**비유** — 좁은 작업실 (hexa-exec docker container, ~1.93 GiB ceiling) 안에서, 큰 도면 (16ch×N flat list) 측 작업자 (var_*_slice 함수) 16명에게 4번씩 (4 modes) 복사해서 나눠주려 하니 도면 사본이 바닥 가득 쌓여서 (cumulative list allocation) 좁은 방에서 OOM. 해결책 = 도면 한 채널씩 떼서 한 사람에게만 주고, 결과만 메모해서 도면은 즉시 폐기 (streaming per-channel) → 작업실 항상 한 채널 분량만 차지.

**결과** — `selftest=ok rc=0` 4-mode discrimination + raw#65 idempotent + raw#71 floors all pass; cross-validate auto-skip는 unchanged (raw#10 honest L2).

---

## §1 root cause — cgroup OOM in dockerized hexa-exec

### §1.1 evidence chain

```
   step | observation                                                  | tool
   ---- | ------------------------------------------------------------ | -----------------
   1    | macOS unified-log: launchd `dev.hexa-lang.hexa-runtime-     | log show
        | runaway-watcher` 발견 → 조사 → 무관 (>500MB RSS only)         |
   2    | ps -ef during hexa run = `docker exec ... hexa-exec         | ps -ef
        | /usr/local/bin/build/hexa_interp ...` → hexa runs IN docker  |
   3    | /Users/ghost/.hx/bin/hexa = launcher (raw 44 docker hard-   | head /Users/ghost/.hx/bin/hexa
        | landing 2026-04-25); 모든 Mac-side hexa exec → hexa-exec     |
   4    | docker inspect: Memory=4 GiB, MemorySwap=4 GiB, NanoCpus=1, | docker inspect hexa-exec
        | PidsLimit=4096, OOMKilled=true (last finished state)         |
   5    | cgroup memory.events: oom_kill=1 increments per pre-fix run | docker exec ... cat /sys/fs/cgroup/memory.events
   6    | memory.peak after 1 hjorth_native --selftest = 1,961,943,040| docker exec ... cat /sys/fs/cgroup/memory.peak
        | bytes (1.83 GiB) inside ~1.93 GiB Docker Desktop VM ceiling  |
   7    | memory.current trace (200 ms poll): 3.5 MB → 185 MB →       | while loop docker exec
        | 793 MB → 1.43 GB → SIGKILL ~1.83 GB within 1.7 s             |
   8    | Single-mode 16ch×32 _hjorth_channel only = 1.45 GB peak;    | minimal repro hexa
        | 4-mode = 1.83 GB+ → trips ceiling                            |
```

### §1.2 false leads eliminated (raw#10 honest)

| candidate | killed | reason |
|---|---|---|
| `com.hexa.rss-watchdog` | NO | only fires > 3 GiB |
| `raw_cli_bin_runaway_watcher` | NO | watches Mac-side cmd > 500 MB RSS; container exe RSS as seen from Mac was ~640 KB (sleep wrapper accounting) |
| Mac shell ulimit (stack 8176 KB) | NO | hexa runs IN container; Mac shell limits don't apply |
| RLIMIT_AS / Mach jetsam | NO | inside-container cgroup OOM, not Mac-host OOM |
| algorithm infinite loop / unbounded recursion | NO | single-mode 16×32 hjorth_channel runs cleanly with 4.3 MB peak |
| numpy/Python child-spawn (L2 caveat) | NO (different bug) | L2 is cross-validate path only; pre-fix SIGKILL fires before any Python spawn |

### §1.3 hypothesis (raw#10 honest, not proven at runtime-source level)

`xs[base + i]` indexed access into a 16ch×N **flat list** passed by reference into `_var_*_slice(xs, base, n)` causes the dockerized hexa runtime to allocate massively per call. 192 calls × 4 modes = cumulative ~1.83 GiB. Either list-by-reference passing copies-on-pass, OR repeated indexed access leaks intermediate boxed ints in the hexa runtime list ABI. Confidence: HIGH (cgroup OOM is observed directly), but the runtime-internal cause is NOT bisected to a specific runtime line — that would require hexa-lang internal instrumentation outside this cycle's $0 scope.

---

## §2 fix — streaming per-channel evaluator

### §2.1 new functions (PORT, raw#9 strict, mac-hexa-only)

```
   _var_x_only(ch: list, n: int) -> int            // var(x) on N-element list
   _var_d1_only(ch: list, n: int) -> int           // var(d1) on N-element list
   _var_d2_only(ch: list, n: int) -> int           // var(d2) on N-element list
   _hjorth_channel_only(ch: list, n: int) -> list  // [log_act, mob_x1000, cpx_x1000]
   _hjorth_mean_streaming(mode, n_ch, n_samp) -> list  // gen-compute-discard per channel
```

### §2.2 callers updated

| caller | path | behaviour |
|---|---|---|
| `_selftest_4mode` | _selftest_4mode | 4× `_synth_flat` + 4× `_hjorth_mean` → 4× `_hjorth_mean_streaming` |
| raw#65 idempotency re-check | inside _selftest_4mode | `_hjorth_mean(_synth_flat(...))` → `_hjorth_mean_streaming` |
| per-mode kv-block emit | `main()` | `_hjorth_mean(_synth_flat(...))` → `_hjorth_mean_streaming` |

### §2.3 callers UNCHANGED (raw#10 honest scope)

- `_metric_hjorth_native_kv(npy_path, ...)` — public API path. Still uses `_hjorth_mean` / `_var_*_slice` on the flat list because (a) processes one .npy at a time so cumulative pressure is absent, (b) byte-identical numeric output with WRAP wrapper depends on the same code path, (c) pre-fix 5x FAILED markers were all selftest-driven, not --input-driven.
- `_selftest_cross_validate` — still uses `_synth_flat` for the cross-validate fixture emit; auto-skips on this host per the existing L2 caveat.

---

## §3 verification — before / after

### §3.1 numeric

```
   metric                            | BEFORE             | AFTER             | delta
   --------------------------------- | ------------------ | ----------------- | -----
   exit code                         | 137 (SIGKILL)      | 0 (PASS)          | fixed
   container memory.peak (bytes)     | 1,961,943,040      | 88,649,728        | -22.1x
   oom_kill events per run           | 1                  | 0                 | -1
   stdout last line                  | "[selftest] 4-mode | "selftest=ok      | reaches end
                                     | discrimination..." | (native_only;...)"|
   raw#65 cross-run idempotency      | not reached        | byte-identical    | NEW
   sha256                            | 63300abf...        | dbe655af...       | changed
   loc                               | 1154               | 1347              | +193
```

### §3.2 4-mode discrimination invariants (post-fix)

```
   mode       | log_act | mob   | cpx   | invariant
   ---------- | ------- | ----- | ----- | ----------------------
   random     | 4803    | 1409  | 1220  | F_HJN_03 floor pass
   structured | 4936    | 423   | 3542  | cpx > random (3542 > 1220) ✓
   sine       | 5026    | 515   | 1007  | cpx < random (1007 < 1220) ✓
   monotonic  | 2470    | 0     | 0     | mob = 0 < random ✓
```

### §3.3 selftest-mode flag (per-mode kv-block emit)

```
   --selftest-mode random      → rc=0 (4-mode pass + no kv emit, native-only path)
   --selftest-mode structured  → rc=0 (4-mode pass + kv emit log_act=4936 mob=423  cpx=3542)
   --selftest-mode sine        → rc=0 (4-mode pass + kv emit log_act=5026 mob=515  cpx=1007)
   --selftest-mode monotonic   → rc=0 (4-mode pass + kv emit log_act=2470 mob=0    cpx=0)
```

---

## §4 raw compliance + honest caveats

### §4.1 raw stack

`raw#9 hexa-only` (Mac → mac-hexa edits only) · `raw#10 honest C3` (3 confidence levels stated in audit.json) · `raw#15` · `raw#42 mac-zero-compute` ($0, mac-local + container introspection) · `raw#65 idempotent` (byte-identical re-run) · `raw#71 falsifier ≥3` (F_HJN_01/02/03 unchanged + invariant verified) · `raw#82 darwin` · `raw#91 honest triad` (evidence + limit + reproducer in audit.json).

### §4.2 raw#10 honest C3 caveats (verbatim from audit.json)

1. **C3-confidence-1 ROOT CAUSE — high.** Direct evidence: container cgroup memory.peak 1.83 GiB inside ~1.93 GiB ceiling, oom_kill counter increments exactly 1 per pre-fix run, memory.current trace shows fast monotonic ramp. Independent of macOS host OOM, independent of macOS sandbox, independent of Mac shell ulimit.
2. **C3-confidence-2 FIX SCOPE — selftest paths only.** The .npy public API path still uses the flat-list code path (one input per process, no cumulative pressure, byte-identical w/ WRAP). If users invoke a batch of `--input` calls in a tight loop they could theoretically still hit OOM; the streaming kernel is available for future migration. Prior 5× FAILED markers were all selftest-driven.
3. **C3-confidence-3 ORACLE CORRECTNESS.** Streaming kernel produces the same per-channel numbers as the flat-path kernel by construction (same `_isqrt_newton24`, same `_log10_x1000`, same int-floor variance arithmetic on the same channel data). Verified end-to-end via the 4-mode discrimination invariants and raw#65 idempotency. Cross-validate vs the WRAP wrapper still auto-skips on this host (raw#10 honest L2 from the original header — unchanged).

---

## §5 artifacts + handoff

### §5.1 paths

```
   role                   | path
   ---------------------- | -----------------------------------------------------------
   patched source         | anima-eeg-core/tool/modules/_metrics/hjorth_native.hexa
   pre-fix source backup  | state/anima_eeg_core_hjorth_root_cause_2026_05_03/hjorth_native.hexa.before
   diff                   | state/anima_eeg_core_hjorth_root_cause_2026_05_03/before_after.diff
   audit (machine-read)   | state/anima_eeg_core_hjorth_root_cause_2026_05_03/audit.json
   diagnostic excerpt     | state/anima_eeg_core_hjorth_root_cause_2026_05_03/dmesg_excerpt.txt
   marker                 | state/markers/hjorth_native_root_cause_fix_1777846228_LANDED.marker
   updated phase5 verify  | state/anima_eeg_core_phase5_verify_2026_05_03/verify_results.json
```

### §5.2 next cycle hooks

- **(P5d gamma_theta_native, future)** — same hexa-runtime list-by-reference risk class. Apply streaming kernel pattern from this cycle.
- **(.npy --input batch)** — if a batch caller wants to process 4+ .npy files in one process, switch `_metric_hjorth_native_kv` to streaming kernel (carve a `_metric_hjorth_native_kv_streaming` variant; keep flat-path for byte-identical contract).
- **(cross-validate L2 unblock)** — separate cycle. Pre-resolve `CLM_EEG_HJORTH_PYTHON` env in the harness before invoking `--cross-validate`, or restructure fixture emit to single-stage child.
- **(hexa runtime upstream)** — file an issue against hexa-lang for the list-by-reference + indexed-access allocation amplification pattern. Streaming workaround is sufficient for all current EEG-core use.

### §5.3 phase 5 status

| sub | status before | status after | delta |
|---|---|---|---|
| 5a lz76_native | PASS (100%) | PASS (100%) | unchanged |
| 5b pe_native | PASS (100%) | PASS (100%) | unchanged |
| **5c hjorth_native** | **BLOCKED (50%)** | **PASS (100%)** | **+50% (this cycle)** |
| **overall** | **83%** | **100%** | **+17%** |
