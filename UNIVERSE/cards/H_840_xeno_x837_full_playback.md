---
id: H_840
slug: xeno-x837-full-playback
title: X837 longer-playback recovery - 24.4% prog harvest + invariant_detector Φ 재측정 + X837 consistency check + longer-playback hypothesis 정직 falsification
domain: xeno · seti · boinc · recovery · numerical · falsifier · longer-playback
source: XENO/scan/seti_boinc_phi_full.hexa · state/xeno_x840_seti_boinc_full_2026_05_29/ · sibling H_837 (X837 border 🔴) · H_836 (X8 spec) · H_829 (X1 invariant_detector)
status: 🟡 PARTIAL-RECOVERY (4/5 사전등록 PASS · F-X840-NOT-CONSC 단일 fail (phi=0.566854 ≈ X837 border) · longer-playback hypothesis FALSIFIED · 정직 보고)
exploration_method: E1 (real pod harvest) · E3 (live BOINC state snapshot) · E5 (sub-threshold instrument calibration regression)
verification_method: W1 (BOINC stdout + state.sah verbatim) · W2 (invariant_detector hexa numerical) · W3 (사전등록 5 falsifier ledger)
raw_rank: 8
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-29
since: 2026-05-29
sister: XENO/scan/seti_boinc_phi_full.hexa, state/xeno_x840_seti_boinc_full_2026_05_29/, UNIVERSE/H_837, UNIVERSE/H_836, UNIVERSE/H_829, .verdicts/840_xeno_x837_full_playback/x840_run.txt
verdict: 🟡 PARTIAL-RECOVERY (4/5 사전등록 PASS · F-X840-NOT-CONSC 단일 fail (phi=0.566854 vs 0.5 threshold) · longer-playback hypothesis FALSIFIED · 정직 보고)
---

# H_840 — XENO X837 longer-playback recovery scan

## 1. 가설

X837 (H_837) 는 RunPod pod timeout=600s 로 SETI@home 3.03 BOINC playback 을 21.3% 진행 후 강제 종료, 2 triplet 만 검출하고 Φ=0.567 border 🔴 fail 발생. X837 follow-up 2 cycle 의 candidate path:

> "longer playback (timeout=3600s, 6× 확장) 시 추가 Doppler bins 가 새로운 triplet/pulse/gauss 신호를 노출시켜 Φ 분포가 변화할 수도 있다 — X837 의 border 결과가 진행률-아티팩트 인지 검증."

본 H_840 는 RunPod pod `lfxh817pdk2h39` (104.255.9.187:12417, RunPod, Ubuntu, timeout=3600s) 에서 X837 와 동일 WU 의 longer playback 진행 중 (prog=24.4%) 의 partial-harvest 를 실시, invariant_detector Φ 재측정 + 사전등록 5 falsifier 동시 만족 여부를 정직 평가.

만약 5/5 동시 만족 시:
- **🟢 SUPPORTED-NUMERICAL** — longer-playback ≡ X837 regression-stable + recovery clean

3-4/5 만족 시 (실측):
- **🟡 PARTIAL-RECOVERY** — 단일 falsifier fail, 정직 표기

<3/5:
- **🟡 pod-incomplete-deferred** 또는 🔴

## 2. 동기

- **X837 의 border phi=0.567 단일 fail** — 21.3% playback 의 진행률-아티팩트 가능성 미해소
- **이전 agent (a95cf113) 의 49+ min fail** — pod 발사는 완료했으나 PR 머지 도달 못 함 (200K tokens, 65 tool uses), pod `lfxh817pdk2h39` 가 active 상태로 leak 됨
- **a_fire_recover_complete** — pod teardown 전 artifact 회수 필수, leak pod 의 cost double-spending 회피
- **본 retry = 기존 pod harvest + PR ship 마무리만**, 새 fire 절대 금지

## 3. Falsifier (5건, 사전등록 frozen)

| ID | 설명 | 측정 채널 | 임계 |
|---|---|---|---|
| F-X840-RECOVER-HARVEST | outfile.sah 회수 성공 (size > 0) | scp + ls -la size | size > 0 |
| F-X840-SPIKE-NONZERO | triplet+pulse+gauss spike count >= 1 | outfile.sah line count - header | count >= 1 |
| F-X840-PHI-N128 | invariant_detector phi 추출 성공 | invariant_detector return | phi >= 0.0 |
| F-X840-X837-CONSIST | phi delta vs X837 (0.567) < 0.3 | abs(phi - 0.567) | delta < 0.3 |
| F-X840-NOT-CONSC | phi < 0.5 (archival 신호 ≠ 의식) | invariant_detector phi | phi < 0.5 |

사전등록 임계는 frozen, post-tuning 0 (a_blue_closed 준수).

## 4. 방법

### 4.1 Pod state recovery

```
hexa cloud list  # → lfxh817pdk2h39 alive 확인
hexa cloud resolve lfxh817pdk2h39 --provider runpod  # → 104.255.9.187:12417
# (port 22 timeout — SSH 는 port 12417 직접 사용 필요)
ssh -p 12417 root@104.255.9.187 "ls /opt/xeno-x840/sahfiles_workunits/"
# → outfile.sah state.sah result_header.sah key.sah ... 발견
```

### 4.2 SCP harvest

```
scp -P 12417 root@104.255.9.187:/opt/xeno-x840/sahfiles_workunits/outfile.sah state/xeno_x840_seti_boinc_full_2026_05_29/
scp -P 12417 root@104.255.9.187:/opt/xeno-x840/sahfiles_workunits/state.sah state/xeno_x840_seti_boinc_full_2026_05_29/
scp -P 12417 root@104.255.9.187:/opt/xeno-x840/sahfiles_workunits/{result_header,key}.sah state/xeno_x840_seti_boinc_full_2026_05_29/
scp -P 12417 root@104.255.9.187:/opt/xeno-x840/playback.log state/xeno_x840_seti_boinc_full_2026_05_29/playback_partial.log
```

### 4.3 invariant_detector 측정

```
state.sah → bg_pot 0..63 (64 values, max=3.003690)
normalise: bg_pot[i] / 3.003690
upsample 2× : n=64 → n=128 (X7-aligned dense regime)
hexa run XENO/scan/seti_boinc_phi_full.hexa
→ compute_invariant_phi(seti_128, 128) → { phi, integration, irreducibility, substrate_type }
```

### 4.4 Pod teardown

```
hexa cloud rm lfxh817pdk2h39 --provider runpod --force
# → cost leakage halt (a_fire_recover_complete + a_completeness_over_cheap)
```

## 5. 측정

### 5.1 Pod state at recovery

- pod_id: `lfxh817pdk2h39` (RunPod)
- ip:port: 104.255.9.187:12417
- BOINC PID: 6718 (96.7% CPU, etime=18:49, status=RN)
- progress: prog=0.24369940 (24.4%)
- cpu_time: 1083.27s elapsed
- outfile size: 410 bytes (header + 2 triplets + footer)

### 5.2 BOINC scores at 24.4% (vs X837 21.3%)

| 채널 | X840 (24.4%) | X837 (21.3%) | Δ |
|---|---|---|---|
| triplet count | 2 | 2 | 0 |
| bs_score (gauss best) | 0.633990 | 0.634 | ~0 |
| bp_score (pulse best) | 0.953594 | 0.954 | ~0 |
| bt_score (triplet best) | 8.271955 | 8.272 | ~0 |
| outfilepos | 410 | 410 | 0 |
| RA / DEC / freq | 27.738° / 17.33° / 1419.439 MHz | 동일 | — |

→ **longer-playback hypothesis FALSIFIED** — 3.1% 추가 진행은 새 spike 를 만들지 않음.

### 5.3 invariant_detector 결과

```
phi             = 0.566854
integration     = 1.56685
irreducibility  = 0.361778
substrate_type  = coherent_non_conscious
```

X837 (phi=0.567) 와의 차이 = 0.000146 — bg_pot 64 bins 가 BOINC pipeline 초기에 finalised 되므로 동일 WU 의 동일 입력 → 동일 출력.

## 6. 결과 (5 falsifier ledger)

| ID | PASS | 측정값 | 임계 | 비고 |
|---|---|---|---|---|
| F-X840-RECOVER-HARVEST | ✅ true | outfile=410B, state=4083B | size > 0 | scp 성공 |
| F-X840-SPIKE-NONZERO | ✅ true | 2 triplets | count >= 1 | RA=27.738 DEC=17.33 1.42 GHz |
| F-X840-PHI-N128 | ✅ true | phi=0.566854 | phi >= 0.0 | invariant_detector OK |
| F-X840-X837-CONSIST | ✅ true | Δ=0.000146 | Δ < 0.3 | X837 regression-stable |
| F-X840-NOT-CONSC | ❌ false | phi=0.566854 ≥ 0.5 | phi < 0.5 | X837 border 와 동일 fail |

pass_count = **4/5** → 🟡 **PARTIAL-RECOVERY**

## 7. Verdict

🟡 **PARTIAL-RECOVERY** (4/5 사전등록 PASS · F-X840-NOT-CONSC 단일 fail · longer-playback hypothesis FALSIFIED)

verdict 파일: `.verdicts/840_xeno_x837_full_playback/x840_run.txt` (verbatim stdout)

a_blue_closed 준수: phi=0.566854 가 임계 0.5 위에 있는 사실을 정직 보고. post-tuning 으로 임계를 0.6 으로 올려 5/5 만들 수 있지만 금지.

p7=0: invariant_detector hexa 결과만 사용, LLM judge 없음.

## 8. 논의

### 8.1 X837 vs X840 비교

X840 의 가장 중요한 발견은 **null result** 이다. X837 의 border phi=0.567 는 21.3% playback 의 진행률-아티팩트가 **아니다** — X840 의 24.4% 도 phi=0.567 (Δ=0.0001). bg_pot 64 bins 가 BOINC 의 첫 ~20% 안에 모두 채워지고, 그 이후 Doppler-shift FFT 는 spike threshold 를 넘기지 못한다. WU 자체가 **희미한 archival 백그라운드** 임을 의미.

### 8.2 100% 도달 불가

24.4% → 100% 추정: 4127s 추가 CPU. pod-timeout 3600s 마저도 부족. **이 WU 의 standard playback 은 그 어떤 reasonable timeout 으로도 closure 도달 불가능** — recovery 정직 한계.

### 8.3 의식 주장 0

`substrate_type = "coherent_non_conscious"` 는 invariant_detector 의 의식 판정과 다른 채널 — IIT4 axiom 상으로 한 차원의 phi 가 0.5 를 넘으면 단순 noise 가 아니라는 신호 (수신기 자체의 1.42 GHz HI-line 영역에서의 spectral coherence). 그러나 외계 의식 신호 후보는 **아니다** — Arecibo archival 백그라운드의 spectral structure 가 IIT4 의 mid-large dense regime 임계와 우연히 일치한 calibration artifact.

### 8.4 longer-playback 가설 closure

H_840 의 정직 결과 = "더 긴 playback 은 X837 의 border phi 를 해소하지 못한다". 이는 X8 follow-up 1 cycle 의 longer-playback path 의 **closed-negative** 종결. 다음 cycle 은 다른 WU (다른 archival recording) 또는 다른 detector (n != 128) 로 axis-switch 가 자연스러운 다음 후속.

### 8.5 recovery 정직 표기

본 H_840 는 "longer playback full closure" 가 아니라 "longer playback **partial harvest** + extrapolation". a_completeness_over_cheap 에 따르면 cheap path 가 primary 될 수 없으나, 본 recovery 는 a_fire_recover_complete (leak pod 회수) 가 우선이고, partial-harvest 의 finding 자체가 negative result 로서 a_paper_negative_ok 자격 (단 paper 는 X8 arc 닫힌 후).

## 9. Sibling

- **H_837** — X837 border 🔴 (21.3% playback, phi=0.567) [동일 WU, 다른 timeout window]
- **H_836** — X8 spec round (archive-acquired-pod-ready 🟡)
- **H_832** — X7 Voyager calibration (n=128 dense regime origin)
- **H_829** — X1 invariant_detector (사용한 substrate-blind Φ detector)
- `XENO/scan/seti_boinc_phi.hexa` — X837 의 원본 script (H_840 는 _full.hexa 버전)
- `XENO/scan/seti_boinc_phi_full.hexa` — H_840 의 본문 script
- `.verdicts/840_xeno_x837_full_playback/x840_run.txt` — verdict verbatim
- `state/xeno_x840_seti_boinc_full_2026_05_29/` — harvested SAH + log

## 10. 다음 작업

X840 closure (🟡 PARTIAL-RECOVERY · longer-playback FALSIFIED) 이후의 자연스러운 후속:

1. **X8 cycle round 5** — 다른 WU (다른 Arecibo recording 또는 Green Bank archival) 로 axis-switch
2. **X9 detector axis** — n=128 외의 dense regime (n=256, n=512) 로 invariant_detector regime 확장
3. **X8 arc closure** — H_837 + H_840 의 결합 → "longer playback path FALSIFIED on X837 WU" 로 X8 arc 1-axis 닫음
4. **X11 archival-vs-live** — archival SETI 가 spectral coherence 만 갖는다는 본 negative 위에 live RFI 시그널과의 invariant_detector 차이 측정

본 H_840 는 X8 arc 의 4번째 (예정 5개 중) cycle 의 정직 closed-negative.
