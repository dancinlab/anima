# ubu1 Disk Diagnostic — 2026-05-01

**Agent**: ubu1-disk-diagnostic
**Trigger**: N-21 reproduce agent reported ubu1 at 94% disk (53GB free)
**Authorization**: "사용자 전부 알아서" — handle agent footprint, do NOT auto-delete user files
**Policy**: PROPOSAL ONLY. No deletion executed.

---

## TL;DR

- ubu1 (`aiden-B650M-K`) `/dev/nvme0n1p2`: **915GB total / 817GB used / 53GB free / 94%**
- **The 800GB problem is NOT anima's data.** It's two log files:
  - `/var/log/syslog` = **294GB** of `airgenome-runaway.service` crash-loop spam
  - `/var/log/kern.log` = **294GB** of OOM-killer dumps (34,101,048 lines)
- A single truncate + service stop recovers **~588GB** (94% → ~30% disk used).

---

## Disk State

```
파일 시스템     크기  사용  가용 사용% 마운트위치
/dev/nvme0n1p2  915G  817G   53G   94% /
```

## Top-Level Breakdown

| Path | Size | Classification | Notes |
|---|---|---|---|
| `/var/log` | **589 GB** | OURS-INDIRECT | filled by our airgenome runaway-loop |
| `/usr` | 18 GB | USER (OS) | do not touch |
| `/var/lib` | 12 GB | MIXED | docker 4.5G + containerd 4.5G + snapd 3.4G |
| `/home/aiden/anima` | 104 GB | OURS | training assets |
| `/home/aiden/.local` | 12 GB | USER (pip libs) | review with `pip list --user` |
| `/home/aiden/snap` | 54 MB | USER | trivial |
| `/home/aiden/.cache` | 137 MB | USER | trivial |

## /var/log Breakdown (THE main culprit)

| File | Size | Source |
|---|---|---|
| `/var/log/syslog` | **294 GB** | `airgenome-runaway.service` crash-loop: `silent-failure-enforcement Class 1` + hexa interp `auto-invoke conflict — fn main()` (~907 entries per cycle, ~928 service-restart pairs per chunk) |
| `/var/log/kern.log` | **294 GB** | OOM killer dumps — **34,101,048** "Out of memory" lines |
| `/var/log/journal` | 515 MB | systemd journal — vacuumable to 200M |
| `/var/log/syslog.1` | 218 MB | rotated copy |
| Others | <100 MB | normal |

## anima/ Breakdown (104 GB total — OURS)

| Path | Size | Classification | Status |
|---|---|---|---|
| `~/anima/checkpoints/clm_v4_350m` | 30 GB | OURS-KEEP | current canonical CLM |
| `~/anima/checkpoints/decoder_cpu` | 21 GB | OURS-KEEP | current decoder |
| `~/anima/checkpoints/clm_v3_280m` | **18 GB** | OURS-PRUNE | superseded by v4 |
| `~/anima/checkpoints/clm` | 2 GB | OURS-REVIEW | small, recent (Apr 14) |
| `~/anima/data/corpus_multilingual` | 9.8 GB | OURS-KEEP | active training corpus |
| `~/anima/data/corpus_*.txt` | 1.1 GB | OURS-KEEP | merged corpora |
| `~/anima/state/trained_adapters_r4` | **4.7 GB** | OURS-PRUNE | superseded by r7 |
| `~/anima/state/trained_adapters_r5` | **4.7 GB** | OURS-PRUNE | superseded by r7 |
| `~/anima/state/trained_adapters_r6` | **4.7 GB** | OURS-PRUNE | superseded by r7 |
| `~/anima/state/trained_adapters_r7` | 1.6 GB | OURS-KEEP | current generation |
| `~/anima/state/*_r14_run` (6 dirs) | ~3.5 GB total | OURS-AMBIGUOUS | recent (Apr 26) — leave alone |
| `~/anima/anima-voice/corpus` | 1.9 GB | OURS-KEEP | speech corpus |

## Cleanup Proposal Ranked

### Rank 1 — `/var/log` runaway spam — **588 GB**, LOW risk

```bash
# 1. Truncate the bloated logs (preserves inode so rsyslog stays happy)
sudo truncate -s 0 /var/log/syslog
sudo truncate -s 0 /var/log/kern.log

# 2. CRITICAL: stop the runaway USER systemd service or logs refill in hours
systemctl --user stop airgenome-runaway.service
systemctl --user disable airgenome-runaway.service
# (optional permanent disable): systemctl --user mask airgenome-runaway.service

# 3. Vacuum systemd journal (recovers ~315MB)
sudo journalctl --vacuum-size=200M
```

**Result**: 53GB → ~641GB free (94% → ~19% used)

### Rank 2 — Old CLM checkpoint — **18 GB**, MEDIUM risk

```bash
# Verify clm_v4_350m fully replaces v3 first:
ls -la ~/anima/checkpoints/clm_v3_280m/
ls -la ~/anima/checkpoints/clm_v4_350m/
# If confirmed superseded:
# rm -rf /home/aiden/anima/checkpoints/clm_v3_280m
```

### Rank 3 — Old adapter generations r4-r6 — **14 GB**, MEDIUM risk

```bash
# Verify r7 is canonical (memory says r7 axis-expansion v15 is current):
du -sh ~/anima/state/trained_adapters_r{4,5,6,7}
# If r7 confirmed canonical:
# rm -rf /home/aiden/anima/state/trained_adapters_r4
# rm -rf /home/aiden/anima/state/trained_adapters_r5
# rm -rf /home/aiden/anima/state/trained_adapters_r6
```

### Rank 4 — Docker unused image — **4.7 GB**, MEDIUM-HIGH risk

```bash
# Review what's there first (1 active container, 1 image, 100% reclaimable per docker df):
sudo docker ps -a
sudo docker images
# Only if no active workload uses it:
# sudo docker system prune -a
```

## User-Side Recommendations (DO NOT AUTO-EXECUTE)

| Target | Recoverable | Suggestion |
|---|---|---|
| `~/.local/lib` (pip user libs) | up to 11 GB | `pip list --user` → uninstall unused, or full reset + reinstall from requirements |
| `/var/lib/snapd` | 1-2 GB | `sudo snap list --all` then remove disabled revisions |
| `/var/lib/containerd` | up to 4.5 GB | `sudo ctr -n k8s.io images prune` if no active k8s workloads |

## Do-Not-Touch List

- `~/anima/data/corpus_multilingual` (9.8 GB) — active training corpus
- `~/anima/checkpoints/clm_v4_350m` (30 GB) — current canonical CLM
- `~/anima/checkpoints/decoder_cpu` (21 GB) — current decoder
- `~/anima/state/trained_adapters_r7` (1.6 GB) — current adapter generation
- `~/anima/state/*_r14_*` runs (recent, Apr 26) — verify retention policy first
- `~/anima/anima-voice/corpus` (1.9 GB) — speech corpus
- `/usr` (18 GB) — OS
- Anything outside `/home/aiden/anima/` and `/var/log/` not classified above

## Total Recoverable Estimate

| Confidence | GB |
|---|---|
| HIGH (just /var/log truncate + service stop) | **588** |
| MEDIUM (also v3 checkpoint + r4-r6 adapters) | **+32** |
| User-side optional (pip libs, snap, containerd) | **+18** |
| **Total possible** | **~638 GB** |

## Honest C3 (Ambiguous Items NOT Proposed)

- `~/anima/state/r14_shard1_run` vs `~/anima/state/r14_full_run` — both 678 MB, possibly redundant but could be by-design same-schema outputs. Requires diff before any action.
- `~/anima/state/clm/` (2 GB) — small, recent, unclear if active.
- `~/.claude-claude*` (12 dirs, 295 MB total) — likely Claude Code multi-instance workspaces, USER side.

## Files Generated

- `state/ubu1_disk_diagnostic_2026_05_01/df_root.json`
- `state/ubu1_disk_diagnostic_2026_05_01/top_dirs.json`
- `state/ubu1_disk_diagnostic_2026_05_01/cleanup_proposal.json`
- `docs/ubu1_disk_diagnostic_2026_05_01.md` (this file)
