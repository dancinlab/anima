# Akida Cloud D-1 Prep — 2026-05-08

**Reservation**: Sat 2026-05-09 09:00 KST → Sun 2026-05-10 09:00 KST (24h)
**Platform**: BrainChip Akida Cloud (Colfax International hosted, AKD1000 hardware)
**Connection**: `ssh akida-cloud` (config in `~/.ssh/config`, key `~/.ssh/id_ed25519_akida`)
**Ephemerality**: session start = secure wipe + re-image. No persistent storage. **Upload + exfil mandate every session.**

## Trinity compliance check (own 33)

- A 철학 (.roadmap.philosophy): D2 consciousness verification + D3 substrate-coupled paradigm — Akida cloud cycle은 D3 substrate-coupled lane (AKIDA = neuromorphic substrate) 정합 ✓
- B 법칙 (.roadmap.law): own 16 cost watchdog (cloud 예약 cost), own 18 simple stack SSOT (verdict scoring), own 30 checkpoint preservation (Mac side exfil 패턴 = Akida cloud session-end exfil) — 정합 ✓
- C 가설 (.roadmap.hypothesis): N-2 EEG→AKIDA spike pipeline + N-3 CLM×AKIDA Φ r≥0.85 + N-5 GWT broadcast AKIDA-SSI — H lane active 정합 ✓

## Nexus 측 기존 인프라 (2026-04-29 ~ 2026-05-07 land, 재사용 mandate)

`~/core/nexus/scripts/akida/` 12-falsifier harness 이미 land:

| F-id | category | status | hardware required | command |
|------|----------|--------|-------------------|---------|
| F-C | architectural | ✅ PASS (2026-05-07) | no | `validate_witness.py` |
| F-L7 | QRNG entropy | ✅ PASS (2026-05-07) | no | `qrng_entropy.py` |
| F-M2 | gzip compression | ⚠️ PLAUSIBLE-PASS (2026-05-07) | partial | `spike_compress.py --simulate` |
| F-M3a | dispatch routing | ✅ PASS (2026-05-07) | no | `dispatch_check.py` |
| F-L1 | J/op energy | 미land | **YES (Akida Cloud)** | `energy_meter.py` |
| F-L1+ | sub-Landauer sparsity | 미land | **YES** | `energy_meter.py` |
| F-L6 | Lyapunov sweep | 미land | **YES** | `lyapunov_sweep.py` |
| F-M1 | Gödel-q disagreement | 미land | **YES** | `godel_disagreement.py` |
| F-M3b | Phi substrate-invariance | 미land | **YES** | `substrate_equiv.py` |
| F-M4 | trace equivalence | 미land | **YES** | `substrate_equiv.py` |
| F-A | blowup phase-7 | 미land | **YES** | `nexus_workload.py` |
| F-B | check_* hot-loop | 미land | **YES** | `nexus_workload.py` |

- ✅ 4개 = ready-now falsifier 이미 PASS 처리 (followup witness `~/core/nexus/design/kick/2026-05-07_*_followup.json`)
- 미land 8개 = D+0 Akida Cloud session에서 일괄 fire 대상 (`scripts/akida/runner.py --hardware`)
- 원래 plan: RPi5 + AKD1000 dev kit 도착 후 fire (주문 2026-04-29, ETA 미확정)
- 현재 plan: **Akida Cloud로 8개 즉시 fire** (RPi5 도착 별개 lane 유지)
- `host_register.sh` 현재 `host.rpi5-akida` hardcode → cloud용 별도 mode 추가 필요 (P0a)

## D-1 prep items (nexus 통합 update — 8 items)

- [ ] **P0a — Nexus host_register cloud mode 추가**: `scripts/akida/host_register.sh` 에 `HOST_KIND=cloud` 분기 또는 `host_register_cloud.sh` 신설 (label `host.akida-cloud-colfax`, ephemeral=true)
- [ ] **P0b — Nexus 8개 미land falsifier smoke-test**: Mac local CPU `--simulator` mode로 import + arg parse만 검증 (실제 측정은 cloud)
- [ ] **P1 — Tarball pre-stage**: `anima/` + `nexus/scripts/akida/` 코드 tar.gz + corpus + spec → `~/scratch/akida_cloud_d0_payload.tar.gz`, 업로드 rsync 명령 동결
- [ ] **P2 — N-2 EEG→AKIDA spike pipeline 동결**: anima 측 335 LoC skeleton + ADM encoder + 6 G-D selftest, dry-run script
- [ ] **P3 — N-3 CLM×AKIDA Φ pipeline 동결**: last-layer-only ($1.60 estimate), r≥0.85 falsifier — anima 측 + nexus F-M3b cross-validate
- [ ] **P4 — N-5 GWT broadcast 동결**: AKIDA-SSI 측정 script — anima 측 + nexus F-M3a routing cross
- [ ] **P5 — #99 D+0/D+1 freeze plan**: 5 falsifier checklist 출력 (`docs/n_substrate_consciousness_roadmap_2026_05_01.md` §51.2)
- [ ] **P6 — Exfil script**: session-end Akida cloud → Mac side rsync (own 30 mandate-1 패턴) — anima `state/akida_cloud_d0_2026_05_09/` + nexus `state/akida_evidence/` 둘 다 수신

## D+0 / D+1 timeline (예약 슬롯 내, nexus 8 falsifier 통합)

| Phase | Time (KST) | Action |
|-------|-----------|--------|
| Connect | 2026-05-09 09:00 | `ssh akida-cloud` + tarball upload (~5min) |
| Wipe + reimage | 09:00-09:02 | Akida Cloud 자동 (under 2 min) |
| Env bootstrap | 09:02-09:30 | akida 패키지 import 검증 + AKD1000 device probe + `host_register_cloud.sh` |
| Nexus 8 falsifier fire | 09:30-13:00 | `runner.py --hardware` (F-L1, F-L1+, F-L6, F-M1, F-M3b, F-M4, F-A, F-B) → `state/akida_evidence/` |
| N-2 dry-run + measure | 13:00-15:00 | anima EEG→AKIDA spike pipeline G-D selftest + 6-axis evidence |
| N-3 fire | 15:00-19:00 | CLM×AKIDA Φ pipeline ($1.60 budget) — nexus F-M3b 결과 cross-validate |
| N-5 fire | 19:00-23:00 | GWT broadcast AKIDA-SSI 측정 — nexus F-M3a routing 결과 cross |
| Buffer + retry | 2026-05-10 00:00-04:00 | 실패 falsifier 재실행, exfil dry-run |
| Verdict emit | 04:00-06:00 | `__AKIDA_R__ <PASS\|FAIL>` (anima.cond.1) + nexus 8 falsifier verdict aggregate |
| Final exfil | 06:00-08:00 | Mac side rsync (anima + nexus state 둘 다) |
| Buffer + close | 08:00-09:00 | post-mortem + cloud 종료 (자동) |

## 5 falsifier (#99 D+0/D+1 freeze)

(landed in `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §51.2 — D-1 출력 시 5 항목 verbatim 복사하여 본 문서 update)

1. _falsifier 1 ___
2. _falsifier 2 ___
3. _falsifier 3 ___
4. _falsifier 4 ___
5. _falsifier 5 ___

## Cross-link

### Anima side
- `.roadmap.akida` event 2026-05-08 entry (akida.blk.1 partial-resolve)
- `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §11.1 N-2~N-5 prep + §51.2 #99
- `.own` own 16 / 18 / 22 / 30 / 32 / 33
- `docs/akida_cloud_setup_log_2026_05_08.md` (전체 setup 기록)
- secrets: `akida_cloud.*` (10 keys via `secret list | grep akida_cloud`)

### Nexus side (재사용 mandate)
- `~/core/nexus/scripts/akida/README.md` — 12-falsifier harness 인덱스
- `~/core/nexus/scripts/akida/runner.py` + `runner.hexa` — orchestrator
- `~/core/nexus/scripts/akida/falsifier.hexa` — 개별 falsifier dispatcher
- `~/core/nexus/scripts/akida/host_register.sh` — workspace 등재 (cloud mode 추가 필요)
- `~/core/nexus/design/kick/2026-05-07_anima-nexus-akida-physical-math-limit-saturation_omega_cycle.json` — base witness
- `~/core/nexus/design/kick/2026-05-07_*_followup.json` — 4 ready-now falsifier PASS 기록
- `~/core/nexus/docs/akida_dev_kit_evaluation_2026-04-29.md` — 원래 RPi5+AKD1000 plan (cloud로 partial supersede)
- `~/core/nexus/docs/akida_session_friendly_report_2026-04-29.md` — 30 발견 + sim_bridge 10 도구 매핑
- `~/core/nexus/state/akida_evidence/` — falsifier raw_log 출력 디렉토리

## Risks

- **R1**: P2-P4 script 동결 미완료 시 D+0 cycle 시간 손실 (24h slot 한정, 재예약 wait 발생 가능)
- **R2**: P6 exfil script 미테스트 시 D+1 종료 시점 결과 손실 (own 30 패턴 retroactive 적용)
- **R3**: Akida Cloud Jupyterlab port (7860/8888/4022) 활용 미선결 — local forward 되어있으나 N-2/N-3/N-5 + nexus runner.py CLI fire 가 default
- **R4**: $1.60 N-3 estimate는 RunPod H100 가격 기반 — Akida Cloud cost 모델 별도 확인 필요 (own 16 cost watchdog 정합)
- **R5**: Nexus host_register.sh `host.rpi5-akida` hardcode — cloud mode 미추가 시 D+0 등재 단계 block (FORCE=1 우회 또는 P0a 사전 land 필수)
- **R6**: Nexus 8 미land falsifier script 의존성 (akida 패키지 / cnn2snn / Meta TF 변환) Akida Cloud env에서 사전 검증 필요 — 09:02-09:30 bootstrap phase 부족 시 N-2/N-3/N-5 시간 압박
- **R7**: Nexus state/akida_evidence/ 와 anima state/akida_cloud_d0_*/ 두 출력 path 분리 — exfil script (P6) 두 path 모두 rsync mandate
