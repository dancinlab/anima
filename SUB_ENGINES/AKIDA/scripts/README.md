# SUB_ENGINES/AKIDA/scripts/ — LAN deploy wrappers

constitution Principle I (`~/core/pool/.specify/memory/constitution.md`) 정합 wrapper layer.
pool 의 generic primitive (`pool on <host>` / `pool on all`) 위에 anima-specific 지식 추가.

## 왜 별도?

pool 은 NON-NEGOTIABLE Principle I 로 **"Minimal — Single File, Zero Deps"**:

> functionality that needs one belongs in a separate tool that pool can shell out to via SSH.

→ anima knowledge (`~/anima/SUB_ENGINES/AKIDA/{BOOT,INSTALL}.sh` 경로 · akida SDK · lspci akida · iverilog/yosys/arduino tools) 는 **anima 측 wrapper** 에 산다. pool 은 generic SSH multiplexer.

## 4 wrapper

| script | 역할 | underlying pool primitive |
|---|---|---|
| [`lan_boot.sh`](lan_boot.sh) | SUB_ENGINES/AKIDA BOOT/INSTALL deploy | `pool on <host>` |
| [`lan_status.sh`](lan_status.sh) | 4-axis anima health (anima_repo / SUB_ENGINES / akida_sdk / akd1000) | `pool on all` |
| [`lan_capability.sh`](lan_capability.sh) | HW capability matrix (akida / fpga / arduino) | `pool on all` |
| [`lan_dispatch_all.sh`](lan_dispatch_all.sh) | 전 anima-repo host 일괄 BOOT | composed (lan_status + lan_boot) |

## Pi 5 + AKD1000 도착 시 사용 예

```bash
cd ~/anima/SUB_ENGINES/AKIDA/scripts

# 1. pool roster 등록 (1회)
pool add pi5-akida pi@pi5-akida.local --sudo

# 2. 첫 health probe
./lan_status.sh                     # 전 host: anima_repo / SUB_ENGINES / akida_sdk / akd1000

# 3. anima 미설치 host 에 git clone (한 번)
pool on pi5-akida 'git clone https://github.com/dancinlab/anima ~/anima'

# 4. INSTALL → BOOT Day 1-7
./lan_boot.sh pi5-akida --install   # MetaTF + verify
./lan_boot.sh pi5-akida             # Day 1-7 sequential

# 5. 특정 Day 만
./lan_boot.sh pi5-akida --days 3-5  # Day 3 SNN, Day 4 memristor, Day 5 E2E

# 6. 전 anima-repo host 동시 BOOT (멀티-Pi 5 future)
./lan_dispatch_all.sh

# 7. dry-run (실행 전 명령 echo 확인)
./lan_boot.sh pi5-akida --dry-run
```

## design 정합

- 모든 wrapper = bash (zero deps)
- pool 의 generic primitive 만 호출 (anima-specific knowledge 가 pool 에 leak 안 됨)
- wrapper 1개 = 한 가지 anima 작업 (boot / status / capability / dispatch_all)
- failure isolation: 한 host 실패 시 다른 host 무관 (pool on all 의 aggregate exit 활용)

## cross-link

- [pool README](https://github.com/dancinlab/pool#readme) — generic primitive 명세
- [pool constitution](https://github.com/dancinlab/pool/blob/main/.specify/memory/constitution.md) — Principle I (NON-NEGOTIABLE)
- [SUB_ENGINES/AKIDA/README §13 LAN deploy](../README.md) — topology + Pi 5 setup
- [SUB_ENGINES/AKIDA/BOOT.sh](../BOOT.sh) + [INSTALL.sh](../INSTALL.sh) — underlying scripts
