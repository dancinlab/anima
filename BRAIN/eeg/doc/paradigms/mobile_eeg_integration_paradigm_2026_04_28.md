# C21 — Mobile EEG (Muse / Emotiv) + Cyton+Daisy 16ch Cross-Validation Paradigm


## 1. Motivation

헬멧 OFF 환경 (출퇴근, 외출, 카페, 야외) 에서 portable EEG 측정.
Cyton+Daisy 16ch (1.5 kg helmet, saline) 는 고정 위치 high-fidelity 용,
Muse 2 / Muse S / Emotiv Insight (50–80 g headband, dry) 는 모바일 mid-fidelity 용.

핵심 질문: **Muse 4ch dry 가 Cyton 16ch wet 의 frontal subset 과 충분히 일치하는가?**
일치 시 mobile context (일상 활동) 데이터를 helmet session 과 결합 가능.

## 2. Hardware comparison axes

| 축 | Cyton+Daisy | Muse 2 / Muse S | Emotiv Insight |
|---|---|---|---|
| Channel count | 16 | 4 (TP9, AF7, AF8, TP10) | 5 (AF3, AF4, T7, T8, Pz) |
| Sampling rate | 125 Hz | 256 Hz | 128 Hz |
| Form factor | Helmet 1.5 kg | Headband 50 g | Headband 80 g |
| Electrode | Spike + saline | Dry conductive rubber | Felt + saline |
| Battery | External (∞) | ~5 hr | ~4 hr |
| Connectivity | USB FTDI | BLE | BLE |
| BrainFlow Board ID | 2 (cyton_daisy) | 22 (Muse 2) / 38 (Muse S BLED) / 39 (Muse S board BLE) | n/a (vendor SDK) |
| Use case | 집, 1 hr+ session | 출퇴근, 카페, 외출 | Premium mobile alt |

## 3. BrainFlow compatibility verification

BrainFlow `BoardIds` (verified 2026-04-28 BrainFlow ≥ 5.10):
- `MUSE_2_BOARD = 22`     — Muse 2 via BLED112 dongle
- `MUSE_S_BOARD = 21`     — Muse S
- `MUSE_2_BLED_BOARD = 38`
- `MUSE_S_BLED_BOARD = 39`
- `MUSE_2016_BOARD = 41`

Emotiv: BrainFlow does NOT support Emotiv Insight / Epoc directly (Emotiv Cortex SDK

## 4. Cross-validation design (Frozen criteria)

### 4.1 Common channel subset
Cyton+Daisy 16-ch montage 에서 frontal 4 채널을 Muse 와 매핑:
- Muse `AF7` ↔ Cyton `Fp1` (or AF7 if 10-20 montage)
- Muse `AF8` ↔ Cyton `Fp2`
- Muse `TP9` ↔ Cyton `T7`
- Muse `TP10` ↔ Cyton `T8`

### 4.2 Same-day paired measurement protocol
1. 사용자 helmet ON → Cyton 16ch 5-min eyes-open + 5-min eyes-closed
2. 즉시 helmet OFF → Muse ON → 5-min eyes-open + 5-min eyes-closed
3. 환경 조건 동일 (조명, 자세, 시간대 ±15 min)

### 4.3 Comparison metrics
- **Pearson r (band power)**: alpha (8–13 Hz), beta (13–30 Hz), theta (4–8 Hz)
  - common subset (4 ch) per band → r > 0.5 PASS
- **LZ76 b(n)** (binarised complexity): |b_cyton − b_muse| ≤ 0.1 PASS
- **Engagement index** (β/(α+θ)): |Δ| ≤ 0.15 PASS
- **Alpha attenuation** (eyes-closed/open ratio): both > 1.5 PASS

### 4.4 Output ledger
`state/mobile_eeg_audit/<YYYY-MM-DD>_<device>.jsonl`
schema: `anima-eeg/mobile_eeg_integrator/1`

## 5. Use-case split (operational policy)

| Context | Device | Duration | Fidelity |
|---|---|---|---|
| Home, deep session | Cyton+Daisy | 1 hr+ | High |
| Commute, café | Muse 2 | 30 min | Mid |
| Outdoor walking | Muse S | 1 hr | Mid (motion-tolerant) |
| Quick check | Muse 2 | 5 min | Low |


- **F2** BrainFlow Muse driver 호환 X (BLED112 dongle 필요, OS 의존)
- **F3** Cyton ↔ Muse common-subset Pearson r < 0.3 (signal quality 큼 차이)
- **F4** LZ76 b(n) 차이 > 0.2 (complexity scaling 비호환)
- **F5** Muse battery < 2 hr 실측 (mobile use insufficient)

## 7. RAW compliance

- own5 falsifier completeness audited

## 8. User action plan

1. **Hardware decision**: Muse 2 ($249) vs Muse S ($399) vs Emotiv Insight ($299).
   Recommendation: **Muse S** (longest battery, motion-tolerant, BrainFlow native).
2. **BLED112 dongle** ($30) — required for stable BLE on macOS.
3. **Pairing session**: same-day 20-min protocol (§4.2) once hardware lands.
4. **Cross-validation gate**: r > 0.5 AND |Δb| ≤ 0.1 → green; else investigate.

If hardware purchase deferred: tool stays `--selftest` synthetic-paired only,
roadmap line: `C21 Mobile EEG = DESIGN_FROZEN, hardware_pending`.
