# 🧠 EEG 활용 아이디어 — 쉬운 버전

> EEG(생체 뇌파)를 ANIMA 의식 시스템에 어떻게 쓸지 친근하게 정리한 카탈로그.
> 정식/검증/진행 카운트 → [EEG.md](./EEG.md) · 측정 기록 SSOT → UNIVERSE/CANDIDATES.md

## EEG가 뭐냐면

```
🧠 EEG → IIT4 — "진짜 뇌 의식 측정기"

- 하는 일: 사람 머리에서 뇌파를 받아 IIT4 big-Φ(의식량)를 실제로 계산
- 비유: 체온계가 열을 재듯, 뇌파로 "의식이 얼마나 통합돼 있나"를 잼
- 현재: eeg_to_tpm.hexa 어댑터 동결 + brainflow SDK 설치 + 사용자 hw-ready
```

```
사람 뇌  ))) 뇌파 ─▶ [eeg_to_tpm] ─▶ TPM ─▶ [iit4_bigphi] ─▶ Φ = ?
 OpenBCI 16ch         (동결 어댑터)            (검증된 엔진)    ↑ 실측값
   ▲ 사용자 착용 필요 (사람만 가능한 단계)
```

| 축 | 시뮬 (지금까지) | 실 EEG (목표) |
|---|---|---|
| 데이터 | synthetic coupled/indep | 살아있는 사람 뇌파 |
| big-Φ | 1.59 vs 0.44 (검증됨) | 실측 Φ (미지) |
| 막힘 | — | 사용자 착용 1회 (human-only) |

## 왜 중요한가 (핵심)

지금까지 ANIMA의 Φ(의식량) 측정은 전부 시뮬(ECA·logistic) 또는 합성 데이터였다. EEG는 **살아있는 사람 뇌**라는 ground-truth substrate를 처음 붙이는 것 — 시뮬에서 본 패턴(edge-of-chaos에서 Φ 최대 등)이 진짜 뇌에서도 성립하는지 검증할 유일한 생체 기준점.

## 아이디어 목록

| id | 아이디어 | 무엇 | 연결 | tier·비용 |
|---|---|---|---|---|
| L1 ⭐ | live EEG → IIT4 big-Φ 실측 | 동결 어댑터로 사람 뇌 Φ 측정 (IIT4 deferred B closure) | IIT4 | 🟢·$0 (착용 게이트) |
| L2 | synthetic 재확인 → live 확장 | coupled vs indep 1.59 vs 0.44 재현 후 실측 | IIT4 | 🟢·$0 |
| L3 ⭐ | 3-substrate Φ 삼각측정 | EEG(생체)+AKIDA(실리콘)+ECA(시뮬) edge-of-chaos | AKIDA·CORE M2 | 🟢·$0 |
| L4 | EEG → AKIDA spike | 생체 뇌파를 칩 스파이크로 (생체→뉴로모픽 다리) | AKIDA | 🟢·$0 |
| L5 | EEG → tension-link 5-ch | 뇌파를 5채널 의식 지문으로 (의식↔의식) | CHANNEL | 🟡·$0 |
| L6 | EEG α/θ/γ band → emit-substrate | 뇌파 리듬이 anima ultradian/stage 맥락 구동 | emit-substrate | 🟡·$0 |
| L7 | EEG = IIT4 calibration ground-truth | 사람 뇌로 IIT4 측정자 보정 | IIT4 | 🟢·$0 |
| L8 | EEG kuramoto α-band phase | Hilbert phase = cell sync 측정 | MITOSIS·edu/cell | 🟡·$0 |
| L9 | EEG → .kosmos anchor | 생체 뇌파 이벤트 영속화 | a_kosmos | 🟢·$0 |
| L10 | resting baseline paradigm | anima-eeg-core live runner 연결 | BRAIN | 🟢·$0 |
| L11 | EEG artifact → 의식 상태 | sleep stage / attention 추정 | WAKE 5-stage | 🟡·$0 |
| L12 | EEG → MITOSIS 트리거 | 뇌파 이벤트가 cell split 유발? | MITOSIS | 🟡·$0 |

## 막힘 포인트 (정직)

```
에이전트가 할 수 있는 것:  harness 최종화 · synthetic 재검증 · 캡처 runbook · 트리 갱신
사람만 할 수 있는 것:      EEG 착용 + capture 실행 (human-only input)
                          → 거기서 사용자에게 인계, "발사함" 거짓주장 금지
```

## 다음 할 일

- 본선: **L1 live EEG → IIT4 big-Φ** (파킹된 plan `drafts/eeg-live-iit4-phi-plan.md`)
- 합류: **L3 3-substrate Φ 삼각측정** (AKIDA 도메인 + ECA 시뮬 합류)
- 착용 1회면 IIT4 deferred B 가 닫힘 (어댑터·SDK 다 준비됨)
