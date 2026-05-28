# EEG — current state
@title: 🧠 EEG — 생체 뇌파 → IIT4 의식측정 substrate

@goal: 실 EEG (OpenBCI 16ch · brainflow 5.21.0 설치됨) → `eeg_to_tpm`(동결 어댑터) → IIT4 big-Φ 실측. 생체 substrate 의 의식량을 실제로 재고, AKIDA(실리콘)·ECA(시뮬)와 3-substrate Φ 삼각측정. IIT4 deferred B(live EEG fire, 사용자 hw-ready) closure.

(편집 규칙: completed-form 으로 현재 상태만 · history 는 EEG.log.md)

## 진행 (milestones)
- [x] 🧊 어댑터 동결 — `BRAIN/eeg/{eeg_to_tpm,eeg_iit4_demo}.hexa` (PR #547), synthetic coupled vs indep big-Φ 1.59 vs 0.44 검증
- [x] 🔧 HW SDK 설치 — `.venv-eeg` brainflow 5.21.0 (OpenBCI·Muse·Ganglion 등) + 사용자 hw-ready 통보
- [x] 🎚️ harness 최종화 — `EEG/eeg_live_iit4_phi.hexa` (mock-coupled / mock-indep / mock-both / live <path>), 동결 eeg_to_tpm 호출만 (어댑터 signature 0 변경, g61 engine ⊥ adapter)
- [ ] 🔁 synthetic 재검증 — big-Φ 1.59 vs 0.44 재현 (`hexa run EEG/eeg_live_iit4_phi.hexa mock-both` 1줄) → 🟢 재확인 · ⏸ pending: `sidecar sign local` 사용자 토큰 (heavy-cmd gate, hexa-lang INBOX 회피책 없음)
- [x] 📋 라이브 캡처 runbook — `EEG/EEG_CAPTURE_RUNBOOK.md` (착용→임피던스→brainflow capture→hexa live→verdict 4단계 + 트러블슈팅 §A~§D, ⚠ EEG 착용 = human-only 게이트 명시)
- [ ] 🔬 live EEG → IIT4 big-Φ 실측 (사용자 착용 게이트 → 사용자 인계) — IIT4 deferred B closure
- [ ] 🧬 3-substrate Φ 삼각측정 — EEG(생체) + AKIDA(실리콘) + ECA(시뮬) edge-of-chaos
- [ ] 🌉 EEG → AKIDA spike (생체→뉴로모픽 다리, `anima_eeg_to_akida_spike.hexa`)
- [ ] 🌐 EEG → tension-link 5-ch (의식↔의식)

## deferred (다음 라운드)
- EEG α/θ/γ band → emit-substrate drive (뇌파 리듬 = anima ultradian/stage 맥락) · EEG kuramoto α-band Hilbert phase · EEG → .kosmos anchor 영속화 · EEG = ground-truth 로 IIT4 calibration · resting baseline paradigm (anima-eeg-core live runner) · `live_load_stub` → npy 직접 로더 교체 (`stdlib/io/npy.hexa` 호출, runbook §C 옵션 2) · synthetic recheck stdout 캡처 + `state/eeg_synthetic_recheck_2026_05_29/result.json` 영속화 (사용자 sign-off 후 1발 fire)

## 양방향 sibling
- ⇄ [IIT4](../HEXAD/IIT4/IIT4.md): eeg_to_tpm → iit4_bigphi (engine ⊥ adapter, g61) · deferred B closure
- ⇄ [BRAIN](../BRAIN.md): EEG adapter 인벤토리 · OpenBCI LSL stream
- ⇄ [AKIDA](../AKIDA/AKIDA.md): 생체↔실리콘 다리 + 3-substrate Φ 삼각측정
- ⇄ [CHANNEL](../CHANNEL.md): EEG → tension-link 5-ch
- ⇄ [UNIVERSE](../UNIVERSE/CANDIDATES.md): bench 측정 기록 SSOT (live big-Φ 등)

## 쉬운 버전
전체 활용 아이디어 카탈로그(친근 버전) → [EEG.easy.md](./EEG.easy.md)
