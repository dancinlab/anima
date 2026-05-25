# BRAIN/M1 — synthetic 16-channel EEG → 4-region collapse → IIT4 big-Φ

**날짜**: 2026-05-25  
**파이프라인**: 합성 16ch → 4-region 평균-collapse → `BRAIN/eeg/eeg_to_tpm.hexa` (PR #547) → `stdlib/consciousness/iit4_bigphi.big_phi` (n=4 exact)  
**비용**: $0 mac-local · hexa-only · LLM none  
**결정성**: byte-equal re-run 확인  

## §1 무엇을 닫는가

`BRAIN.md` M1 milestone — "16ch → IIT4 n≤8 downsample/segment + per-region big-Φ". M0 doc (`BRAIN/eeg/ARCHITECTURE.md`) §2 region-collapse 전략과 §4 의 4-region 대안 매핑 (frontal/central/parietal/occipital) 을 3가지 합성 신호로 검증한다.

**falsifiable 가설** (pre-registered):
> Φ(fully-coupled 16ch) ≥ Φ(region-coupled 16ch) ≥ Φ(fully-independent 16ch) — 16ch 입력의 통합도 순서가 region-collapse 후 big-Φ 에서 보존된다.

## §2 결과표

| config | big-Φ | total Φ-structure | Σφ_d | Σφ_r | n_distinctions |
|---|---:|---:|---:|---:|---:|
| **A. fully-coupled** (전역 anti-phase) | **1.9419** | 1.988 | 0.723 | 1.266 | 8 |
| **B. region-coupled** (intra 4ch coupled, region indep) | **0.0797** | 0.638 | 0.501 | 0.137 | 5 |
| **C. fully-independent** (16ch 모두 서로 다른 주기) | **3.2879** | 4.995 | 1.996 | 2.999 | 11 |

**순서 검증**:
- A ≥ B: ✅ TRUE (1.94 > 0.08)
- B ≥ C: ❌ **FALSE** (0.08 < 3.29)
- A ≥ C: ❌ **FALSE** (1.94 < 3.29)

**determinism**: A re-run identical → ✅ PASS

## §3 발견 (NEW)

**가설 일부 FALSIFIED. 새 발견: region-collapse via averaging actively destroys within-region coupling.**

C (fully-independent) 가 가장 큰 big-Φ 를 보였다. 원인 분석:

1. **C 의 "독립 16ch"** → 각 채널 distinct period (2..17). 4ch / region 평균 시, 4개 distinct 주기의 합 = 풍부한 aperiodic 신호 (region-level entropy 高). TPM 추정에서 distinct state 11개 → big-Φ=3.29.
2. **B 의 "region-coupled"** → region 내부 4ch 모두 동일 주기 (offset 만 다름). 4-ch 평균 = 거의 동일 waveform 으로 수렴 (region-level entropy 低). distinct state 5개만 → big-Φ=0.08.
3. **A 의 "fully-coupled"** → 전역 alternating, region 평균이 단순 alternation 유지. 중간 entropy → big-Φ=1.94.

**해석**: 4-ch / region 평균-collapse 는 region 내부의 동기 신호를 평균-out 시킨다 (LPF 효과 + cancellation). 따라서 **"코딩이 region 내에서 일어난다" 는 가정이 IIT4 big-Φ 에 손해**가 된다. region-collapse 가 사실상 정보 파괴 단계.

이는 ARCHITECTURE.md §5 honest scope C3 #1 (synthetic ≠ live) 가 아닌, **methodology-level finding**: collapse 방법을 averaging 외 alternative (e.g. region 내 최대 진폭, region 내 phase-difference, per-region 별도 IIT4) 로 바꾸지 않으면 본 어댑터의 region-level Φ 가 within-region coupling 을 측정 못 한다.

**후속 M2/M3 implications**:
- M2 라이브 데이터에서도 동일 함정 — region 평균이 두피-region 내 high-frequency 동기 신호 (gamma) 를 destroy.
- M3 우선 옵션: (i) **per-region 별도 n=2 IIT4** 실행 (§4 alternative 1) 추가 — region 내 coupling 직접 측정. (ii) **PCA top-4** (§2 strategy B) 비교 — 정보 보존 측면.

## §4 honest scope C3

1. **n=4 (NOT n=8).** M9 tractability: n=8 exact 은 inline budget 초과 (HEXAD/IIT4/state/iit4_m12_bounded_largen 보고 n=6 already minutes). 본 M1 은 4-region (exact, 16 states) 로 sub-second 완료. 8-region 은 stdlib `big_phi_bounded` 가 lower-bound approx 제공 — M3 별도 측정.
2. **합성 ≠ 라이브.** 모든 합성 신호 deterministic, 두피 EEG noise / artifact / drift 미포함. M2 가 라이브 검증.
3. **단일 system_state.** sys_state=1 (region R0 ON, 나머지 OFF) 만 측정. IIT4 big-Φ 는 state-dependent — 다른 state 에서 순서 다를 수 있음. M3 multi-state sweep 필요.
4. **TPM 빈도 추정 (1-step Markov).** `eeg_to_tpm.hexa` 의 STUB 한계 — multi-scale lag · embedding 미지원.
5. **B 의 winner-take-all destruction**: region-coupled 합성이 평균 후 거의 단일 신호로 collapse 된 것은 합성 신호 디자인의 artifact 일 수 있음 (모든 region 내 ch 가 *동일* 주기였음). M3 에서 intra-region 다양성 합성 (phase + amplitude 변이) 으로 재검증 권장.

## 재실행

```
POOL_DISABLE=1 hexa run --no-sentinel \
  BRAIN/eeg/state/brain_m1_synthetic_16ch_2026_05_25/run_m1.hexa
```

byte-equal `result.json` 출력 (deterministic).
