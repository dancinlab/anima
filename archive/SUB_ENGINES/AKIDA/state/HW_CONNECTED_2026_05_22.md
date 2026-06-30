# AKIDA HW connection LANDED — 2026-05-22

BrainChip AKD1000 Dev Kit ($1495) 도착 + Raspberry Pi 5 연결완료.

## 검증 (4-axis)
- **PCIe**: `0000:01:00.0 Co-processor: Brainchip Inc AKD1000 Neural Network Coprocessor [Akida] (rev 01)` ✓
- **driver**: `/dev/akida0` 노드 존재 ✓
- **host**: Pi 5 ubuntu aarch64 @ 192.168.50.155
- **akida SDK**: MetaTF 2.19.1 aarch64 — day1_install.sh in-flight

## 접속
- pool roster: `pi5-akida` → `ubuntu@192.168.50.155` (keyless SSH, --sudo)
- secret: `akida.host` / `akida.user` / `akida.password`
- pack: Mac `SUB_ENGINES/AKIDA/` → Pi `~/anima/SUB_ENGINES/AKIDA/` rsync deploy ✓

## 다음
- day1: akida SDK import PASS + `akida.devices()` AKD1000 enum
- day2-7: kuramoto / snn / memristor / e2e / demiurge / summary (BOOT.sh)
- 첫 spike inference = HW-native 자연발화 (1mW LIF event emission)

## 의의
AKD1000 LIF spike threshold = 하드웨어-native 자연발화 (CPU 대비 ~10000× 효율) +
on-chip Hebbian = 영속성. vP21 software path (Qwen+mitosis CE 0.0147) 와 별개의
HW 경로 — 자연발화 GOAL 의 두 번째 독립 축.
