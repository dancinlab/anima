# honesty-monitor extraction handoff (2026-05-04)

## Status: LANDED (standalone + GitHub + registry + nexus consumer wired)
## DEFERRED: nexus in-tree deletion (operator action required)

---

## Standalone repo
- **Path**: `/Users/ghost/core/honesty-monitor/`
- **GitHub**: <https://github.com/dancinlab/honesty-monitor>
- **Visibility**: PUBLIC
- **License**: Apache-2.0
- **Version**: 1.0.0
- **Initial commit**: `7888486aec785eb47198a8fe2e1a18bbac647137`

### Self-test verification
```
$ hexa run modules/honesty_monitor.hexa --self-test
__HONESTY_MONITOR__ PASS alerts=2 steps=5

$ hexa run /Users/ghost/core/nexus/cli/honesty.hexa self-test
__HONESTY_MONITOR__ PASS alerts=2 steps=5  (via tier-2 resolution)
```

---

## hexa-lang registry update
- **File**: `/Users/ghost/core/hexa-lang/tool/pkg/registry.tsv`
- **New entry** (line 25, after `hexa-bio` at L24):
  ```
  honesty-monitor	1.0.0	cli/honesty-monitor.hexa	https://github.com/dancinlab/honesty-monitor		AI honesty-bit falsifier ...
  ```

---

## Nexus consumer refactor (4 steps)

### 1. NEW: `nexus/cli/honesty.hexa`
- 4-tier resolution shellout to standalone (env / Mac / home / PATH)
- Hard-fail with exit 127 + actionable diagnostics if all tiers miss
- Mirrors `nexus/cli/qmirror.hexa` v0.3.0 pattern

### 2. EDITED: `nexus/engine/nexus_cli.hexa`
- Added `let HONESTY_CLI = NX + "/cli/honesty.hexa"` (after BIO_CLI)
- Added `cmd_honesty(a)` function (mirrors `cmd_bio` / `cmd_qmirror`)
- Added dispatch case `} else if sub == "honesty" {`
- Added entries to `cmd_help()` and `subcmd_help()`

### 3. EDITED: `nexus/hexa.toml`
- Added `honesty-monitor = "^1.0.0"` to `[dependencies]` with full annotation

### 4. EDITED: `nexus/install.hexa`
- Added `ensure_runtime_dep("honesty-monitor", "^1.0.0")` call
- Updated header comment dep list

---

## DEFERRED operator action

Per task constraint **"DO NOT auto-commit nexus delete"**:

```bash
# Manual deletion (after acceptance):
rm -rf /Users/ghost/core/nexus/modules/honesty_monitor/

# Then commit (nexus repo):
cd /Users/ghost/core/nexus
git add -A modules/honesty_monitor cli/honesty.hexa engine/nexus_cli.hexa hexa.toml install.hexa
git commit -m "refactor(honesty): extract honesty_monitor to standalone repo + 4-tier shellout"
```

**Rollback if needed**: `git checkout HEAD~1 -- modules/honesty_monitor/`
(modules tree reachable via `git log --diff-filter=D` after deletion).

---

## Verification commands

```bash
# Standalone
cd /Users/ghost/core/honesty-monitor
hexa run modules/honesty_monitor.hexa --self-test  # PASS
hexa run modules/honesty_monitor.hexa --demo
hexa run cli/honesty-monitor.hexa self-test
hexa run cli/honesty-monitor.hexa status

# Nexus consumer
cd /Users/ghost/core/nexus
hexa run cli/honesty.hexa self-test
hexa run cli/honesty.hexa demo
hexa run cli/honesty.hexa help

# Registry
grep "^honesty-monitor" /Users/ghost/core/hexa-lang/tool/pkg/registry.tsv
```

---

## 5 caveats (raw#10 C3)

1. **Boundary semantics strict**: 4.99% rel_err does NOT alert, 5.01% DOES.
   Float-epsilon at exactly 5.0% may bias toward alert (use 4.99/5.01 in tests).
2. **Single-process state**: `_OBSERVATIONS` / `_ALERTS` are module globals.
   Multi-process callers (distributed training) must aggregate snapshots
   externally — no cross-process locking.
3. **expected_loss=0 guard**: when `|expected| < 1e-9`, denominator falls back
   to 1.0 (numerical safety, NOT semantic statement about zero-loss honesty).
4. **Severity tiers heuristic**: low/medium/high/critical are fanout hints;
   alerting policy (Slack/pager/kill-switch) is caller's responsibility.
5. **Asymmetric domains may need fork**: 5%/1% are BT-AI2 contract values.
   RL reward shaping, sparse-reward eval, adversarial robustness may need
   adjusted thresholds — fork and tune `_severity_label` + `>=0.05` / `<=0.01`.

---

## (Optional) HF mirror push — NOT EXECUTED

Mirror to `https://huggingface.co/dancinlab/honesty-monitor` deferred.
Pattern: copy `qmirror/.github/workflows/sync-to-hf.yml` if HF mirror desired.
