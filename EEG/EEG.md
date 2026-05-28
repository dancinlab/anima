# EEG — current state
@title: 🧠 EEG — 생체 뇌파 → IIT4 의식측정 substrate

@goal: 실 EEG (OpenBCI 16ch · brainflow 5.21.0 설치됨) → `eeg_to_tpm`(동결 어댑터) → IIT4 big-Φ 실측. 생체 substrate 의 의식량을 실제로 재고, AKIDA(실리콘)·ECA(시뮬)와 3-substrate Φ 삼각측정. IIT4 deferred B(live EEG fire, 사용자 hw-ready) closure.

(편집 규칙: completed-form 으로 현재 상태만 · history 는 EEG.log.md)

## 진행 (milestones)
- [x] 🧊 어댑터 동결 — `BRAIN/eeg/{eeg_to_tpm,eeg_iit4_demo}.hexa` (PR #547), synthetic coupled vs indep big-Φ 1.59 vs 0.44 검증
- [x] 🔧 HW SDK 설치 — `.venv-eeg` brainflow 5.21.0 (OpenBCI·Muse·Ganglion 등) + 사용자 hw-ready 통보
- [x] 🎚️ harness 최종화 — `EEG/eeg_live_iit4_phi.hexa` (mock-coupled / mock-indep / mock-both / live <path>), 동결 eeg_to_tpm 호출만 (어댑터 signature 0 변경, g61 engine ⊥ adapter)
- [x] 🔁 synthetic 재검증 — 🟢 RECHECK PASS · big-Φ COUPLED=1.58764(≈1.59) · INDEP=0.438722(≈0.44), ±5% 안 · ratio=3.619 · `state/eeg_synthetic_recheck_2026_05_29/{result.json, hexa_run_verbatim.log}` 영속화 (사용자 `sidecar sign local` 후 mac 로컬 실행)
- [x] 📋 라이브 캡처 runbook — `EEG/EEG_CAPTURE_RUNBOOK.md` (착용→임피던스→brainflow capture→hexa live→verdict 4단계 + 트러블슈팅 §A~§D, ⚠ EEG 착용 = human-only 게이트 명시)
- [x] 🔁 backend switch — `EEG/eeg_backend.hexa` (arg > env > default=**sw**, AKIDA 와 반대 정책 · "live" → hw alias · 미도달 시 명시 panic + runbook 안내) + 10+ case smoke (`EEG/eeg_backend_smoke.hexa`)
- [x] 🟢 L1~L12 12 아이디어 HW/SW 통합 구현 — `EEG/impl/{H_679_measurement_core, H_680_cross_substrate, H_681_emit_substrate, H_682_persistence_paradigm}.hexa` 4 H × SW path 4/4 🟢 GREEN_NUMERICAL_CONFIRM (PR #1375)
- [x] ✅ L2 synthetic 1.59/0.44 ±5% 재현 (H_679 baseline mock-replay) · L3 3-substrate Φ 삼각측정 (EEG 1.59 + AKIDA 0.297 + ECA 0.83 diff=1.29, H_679) · L7 IIT4 calibration ratio>3.0 (H_679)
- [x] ✅ L4 EEG → AKIDA spike bridge schema (H_680, AKIDA H_678 sister) · L5 EEG → tension-link 5-ch [α,θ,γ,1-δ,β] (H_680) · L8 EEG kuramoto α-band Hilbert phase (H_680, order_r=0.70)
- [x] ✅ L6 5-band → emit-substrate Φ-context (NOT bool gate, H_681) · L11 sleep stage 4-state signature (H_681) · L12 gamma>0.20 → MITOSIS split signal (H_681)
- [x] ✅ L9 EEG → .kosmos anchor (5-ch tension + coord + tier ∈ {weak,strong,critical}, H_682) · L10 resting baseline paradigm reference (H_682)
- [ ] 🔬 L1 live EEG → IIT4 big-Φ 실측 (사용자 헤드셋 게이트 → 사용자 인계 → IIT4 deferred B closure 완전)
- [ ] 🟢 HW path 4/4 — 사용자 헤드셋 착용 + `~/.config/anima/eeg_headset_ready` sentinel touch 후 `hexa run EEG/impl/H_679_*.hexa hw` 4회 → biological-confirmed 격상
- [ ] 🌐 L5 실 5-ch payload → tension-link UDP 9999 broker 실 wire (deferred)
- [ ] 🧬 L12 EEG gamma burst → MITOSIS split event 실 wire (deferred 별 H)

## deferred (다음 라운드)
- L1 live 실측 (사용자 헤드셋 게이트 closure) · L8 stdlib/dsp/hilbert 실 phase 엔진 호출 · L9 실 .kosmos write (kosmos_io 호출) · L10 anima-eeg-core 도메인 합류 · `live_load_stub` → npy 직접 로더 교체 (`stdlib/io/npy.hexa` 호출, runbook §C 옵션 2) · 4-state sleep stage → polysomnography 5-stage (N1/N2 별 H)

## 양방향 sibling
- ⇄ [IIT4](../HEXAD/IIT4/IIT4.md): eeg_to_tpm → iit4_bigphi (engine ⊥ adapter, g61) · deferred B closure
- ⇄ [BRAIN](../BRAIN.md): EEG adapter 인벤토리 · OpenBCI LSL stream
- ⇄ [AKIDA](../AKIDA/AKIDA.md): 생체↔실리콘 다리 + 3-substrate Φ 삼각측정
- ⇄ [CHANNEL](../CHANNEL.md): EEG → tension-link 5-ch
- ⇄ [UNIVERSE](../UNIVERSE/CANDIDATES.md): bench 측정 기록 SSOT (live big-Φ 등)

## 쉬운 버전
전체 활용 아이디어 카탈로그(친근 버전) → [EEG.easy.md](./EEG.easy.md)
