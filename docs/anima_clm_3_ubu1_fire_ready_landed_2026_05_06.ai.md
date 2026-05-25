# anima CLM-3-original ubu1 fire-ready preflight landed (2026-05-06)

## TL;DR
- BG-FC ubu1 사후 reachability 회복 (BG-EW UNREACHABLE 이후 fix 완료) 검증 완료.
- 4 pre-flight gate 전부 PASS — ssh / venv / torch 2.11.0+cu128 / repo 존재.
- 다만 **repo sync gap** 1건 검출: ubu1 HEAD 6407920 (origin/main 동기화 OK) vs 사용자 mac HEAD 2f246b79 (push되지 않은 로컬 commit 존재 X — origin/main과 동일). `ready/` 가 embedded git repo (NOT submodule)이며 ubu1 측 `ready/` 디렉터리가 비어 있어 `train_clm.py` 부재. `data/corpus_mix_70wiki_30dialogue.txt` 는 mac에도 존재하지 않음 (corpus assembly BG 별도 필요).
- $0 / ~10min wall / actual training 미실행 (emit only, raw#10 obey).

## SSH Reachability
| Path | Result | Detail |
|------|--------|--------|
| LAN 192.168.50.119 | PASS | ok-lan, hostname=aiden-B650M-K, kernel 6.17.0-22-generic |
| Host alias `ubu1` | PASS | ssh config maps to LAN HostName |
| Tailscale 100.96.193.56:22 | TIMEOUT | port 22 connect timed out (TS path not preferred) |

## Hardware Snapshot (ubu1)
- GPU: NVIDIA GeForce RTX 5070
- VRAM total: 12227 MiB / free: 11758 MiB
- Compute capability: 12.0 (sm_120 Blackwell)
- Driver: 580.126.09
- GPU util: 0%, temp: 37 C
- Disk: 538G free / 915G total (/dev/nvme0n1p2)

## 4 Pre-Flight Gate
| Gate | Check | Result | Evidence |
|------|-------|--------|----------|
| 1 | ssh ubu1 echo ok | PASS | ok-host-alias 응답 |
| 2 | /home/aiden/venv_orchestrator/bin/python | PASS | symlink → python3, Python 3.12.3 |
| 3 | torch 2.11.0+cu128 + CUDA | PASS | `2.11.0+cu128 True NVIDIA GeForce RTX 5070` |
| 4 | anima repo path | PASS_WITH_GAP | /home/aiden/core/anima HEAD=6407920, but `ready/` 비어있음 |

## Repo Sync Gap (must remediate before fire)
1. `git pull` on ubu1 (현재 HEAD 6407920 → origin/main 2f246b79 sync — 0 commit behind 확인 필요)
2. `ready/` 는 `.gitmodules` 매핑이 없는 embedded git repo (mac에서 HEAD=ef7aae81). 동기화 방법:
   ```bash
   rsync -avz --exclude='.git' /Users/ghost/core/anima/ready/ ubu1:/home/aiden/core/anima/ready/
   ```
3. `data/corpus_mix_70wiki_30dialogue.txt` 부재 — mac에도 없음. spec doc는 references하지만 corpus assembly 미실행. 별도 corpus build BG 필요.

## FALSIFIER-LOCK-UBU1 (사용자 literal confirm 필요)
사용자가 다음 5 falsifier에 대해 `FALSIFIER-LOCK-UBU1` literal 입력 시 lock:
- **F-CLM3-orig-1**: spec_match (vocab=256 byte / d=768 / L=12 / fib growth 1,1,2,3,5,8,13,21,32)
- **F-CLM3-orig-2**: Phase 2 dialogue CE drop >= 30%
- **F-CLM3-orig-3**: Phi_real >= 11
- **F-CLM3-orig-4**: KO 5-prompt >= 3/5 coherent
- **F-CLM3-orig-5**: phi_star NO_FLIP

## Emitted Commands (BG는 실행 X — emit only)
- 100-step smoke: `state/anima_clm_3_ubu1_fire_2026_05_06/emit_smoke_command.txt` (5분, foreground tee)
- Full retrain: `state/anima_clm_3_ubu1_fire_2026_05_06/emit_full_retrain_command.txt` (100K step, nohup, 5-10 days)
- Monitor: `state/anima_clm_3_original_ubu1_launch_2026_05_06/monitor_ubu1.bash <run_name>` (30min cadence via watch)

## ETA Bookkeeping
- 100K steps × 2.5s = 69 hours = 2.9d (optimistic)
- 100K steps × 8.0s = 222 hours = 9.3d (pessimistic)
- 소프트 5-10d 캡, abort triggers: step time > 10s OR GPU temp > 80C sustained

## 5 Honest C3 (concerns / cautions / counter-evidence)
1. **Repo sync gap이 fire-blocking** — pre-flight gate 4가 형식상 PASS이지만 실제 fire에 필요한 `train_clm.py` + corpus가 없음. user에게 명시적으로 알려야 함.
2. **Corpus_mix_70wiki_30dialogue.txt 미존재** — spec doc 작성 시점 가정과 실제 데이터 상태 불일치. corpus assembly BG 별도 fire 필요 (~수시간 wall, $0).
3. **`ready/` embedded git repo race** — mac/ubu1 양쪽 모두 git repo로 존재하므로 rsync exclude='.git' 처리 필요. 단순 git pull로 안 옴.
4. **Tailscale path TIMEOUT** — TS 22 포트가 막혀있음. LAN dependency가 강함. 외부에서 fire하려면 TS 재설정 또는 jump host 필요.
5. **5-10 day 단일 GPU lock** — fire 후 RTX 5070이 5-10일간 점유됨. 동시기 BG-FB H100 path 진행 시 first-PASS-wins 정책으로 budget overlap 차단 정책 재확인 필요.

## 다음 단계 (사용자 confirm 후)
1. **corpus assembly BG 별도 fire** (선결조건) — `data/corpus_mix_70wiki_30dialogue.txt` 생성
2. **ubu1 repo sync** — git pull + ready/ rsync
3. **사용자 FALSIFIER-LOCK-UBU1 literal 입력**
4. **anima 직접 100-step smoke fire** (5분, foreground)
5. smoke PASS 시 → **full retrain fire** (nohup, 5-10d)

## Substrate 우선 fire 권고 (BG-FB H100 vs BG-FC ubu1)
**ubu1 우선 권고 (rank 1)** — 이유:
- $0 marginal cost vs H100 시간당 $2-4
- own hardware = budget 낭비 risk 0
- 5-10d wall이 sufficient (chat-cap path는 P9/CLM-2 lane closures로 시간 압박 해소)
- H100은 axis-preservation 또는 chat-cap retry 등 더 시간-민감한 lane에 보존
- BG-FB H100은 ubu1 smoke PASS 시점에서 first-PASS-wins로 kill 가능

단, **corpus + train_clm.py 동기화 BG가 ubu1 fire의 hard dependency** — 그 BG가 통과해야 ubu1 fire ready.

## 제약 obey
- raw#9 fail-loud: repo sync gap 명시
- raw#10 spec-then-implement: training fire 0건
- raw#15 audit trail: preflight.json + 본 doc + emit txt 3건
- raw#37 py->hexa: ssh/bash 인프라는 transient_py-class
- no commit / no HF token / bash 3.2 compatible / $0 cost

## Outputs
- `state/anima_clm_3_ubu1_fire_2026_05_06/preflight.json`
- `state/anima_clm_3_ubu1_fire_2026_05_06/emit_smoke_command.txt`
- `state/anima_clm_3_ubu1_fire_2026_05_06/emit_full_retrain_command.txt`
- `docs/anima_clm_3_ubu1_fire_ready_landed_2026_05_06.ai.md` (본 문서)
