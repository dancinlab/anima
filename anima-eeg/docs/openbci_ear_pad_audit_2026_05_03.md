# OpenBCI Ear Pad / Earclip / Saline Audit — Berger F_BERGER_03 Root Cause Fix

date: 2026-05-03
context: F_BERGER_03 측정 실패 (EC α power < EO α power, DC drift -185mV @ P4 / -182mV @ O2). 직전 BG (pragma practice) 핵심 발견 = "REF/BIAS ear clip 측 saline pad" prime suspect. 본 audit = vendor shop / docs 측 제품 cross-check + 즉시 fix 권장.

scope: web search 1 round, 4 fetches (shop.openbci.com x2, docs.openbci.com x1, forum x1).

---

## 1. OpenBCI shop 측 ear pad / earclip product list

| product | price (USD) | spec | 비고 |
| ----- | ----- | ----- | ----- |
| Earclip Electrode (1 pair) | $59.99 | Ag-AgCl electroplated, cable 0.25 / 0.5 / 1.5 m 옵션 | REF + BIAS 1 pair 셋트, 한국 배송 가능 (shipping calc at checkout) |
| Ten20 Conductive Paste 8oz | $24.99 | water-based conductive paste | 이미 사용 중 |
| Electrode Cap Gel | $24.99 | gel cap 측 conductive gel | cap 셋트 측 한정 |
| Gold Cup Electrodes | from $44.99 | Au-plated cup, gel reservoir | scalp 측 — earclip 보다 stable |
| Kendall foam solid gel (50-pack) | $24.99 | disposable solid gel pad | EMG/ECG snap — earclip 측 직접 호환 X |

**fetched 9 of 43 products.** "saline pad" / "hydro-link sponge" 측 frontpage accessories tag 측 별도 검색 X. Gelfree Cap Kit 측 saline-soaked sponge 포함 — 단 cap 셋트 만 별도 구입 가능 (earclip 측 X).

→ **anima-eeg 측 결론**: 추가 구매 가능 옵션 = (a) earclip 1 pair extra ($59.99), (b) Gold Cup Electrodes for mastoid placement (~$44.99). saline pad 별도 sale 측 OpenBCI shop 측 X.

---

## 2. Saline pad vs Ten20 paste vs SignaGel 비교 (vendor + community)

| 옵션 | 안정성 (long session) | DC drift 위험 | earclip 측 호환 |
| ----- | ----- | ----- | ----- |
| Ten20 paste only (현재) | 30~60min OK, 2hr+ 측 dry out | 중 — paste 마르면 drift up | OK |
| Ten20 + saline pad sandwich | 2hr+ 안정 (community report) | 저 | OK (DIY: cotton + 0.9% NaCl) |
| SignaGel (Parker Labs) | Ten20 보다 wet, 1~2hr 안정 | 중 | OK — vendor 측 OpenBCI 비추천 (sticky, residue) |
| Hydro-link sponge (Gelfree) | research-grade, full session | 저 | X — cap 셋트 한정 |

vendor docs 측 명시 (EEGSetup): "Fill the [gold cup] electrode so there is a little extra electrode paste spilling over the top". earclip 측 동일 원칙 = **paste 충분히** + earlobe 측 alcohol prep 권장 (docs 측 명시 X, community 권장).

---

## 3. earclip 정확 부착 방법 (귓불 vs mastoid)

vendor docs (EEGSetup):
- 흰색 (white) REF → earlobe A1 또는 A2
- 검은색 (black) BIAS → 반대측 earlobe

mastoid 측 docs 명시 X. community / clinical EEG 표준 측 mastoid (귀 뒤 뼈) = earlobe 보다 stable (less movement, less sweat). 단 OpenBCI earclip = 귓불 clip 형태 → mastoid 측 direct 부착 X. mastoid 측 부착 측 → Gold Cup Electrode + Ten20 + 의료용 tape 필요.

prep checklist (community 권장):
1. earlobe 측 alcohol swab 측 cleaning (skin oil 제거)
2. Ten20 paste 충분히 (over-fill OK)
3. clip 단단히 부착 — 단 혈액 순환 차단 X (느슨/단단 balance)
4. cable strain relief (tape 측 cable 측 face / collar 측 fix)
5. 30min 후 재check — paste 마르기 시작 전 재application

---

## 4. 즉시 fix 권장 (priority 순)

**P0 추가 hardware 없이 가능 (recommended)**:
1. earlobe 측 alcohol swab cleaning 후 재시도
2. Ten20 paste 양 2~3배 (over-fill) — earclip 안쪽 cup 측 paste 측 spilling 까지
3. 부착 후 30s 측 안정 대기 → impedance check
4. cable 측 tape 측 strain relief (motion artifact 차단)

**P1 추가 구매 권장 (only if P0 fail)**:
1. Gold Cup Electrode pair (~$44.99) → mastoid 측 부착, earclip 보다 stable
2. 0.9% NaCl saline (drugstore $2~5) → DIY cotton sandwich, Ten20 위 측 보충
3. earclip extra pair (~$59.99) → 현 earclip 측 Ag-AgCl wear / oxidation 가능성 측 백업

→ **완성도 lens 측 ranked recommendation**: **P0-1 (alcohol prep) + P0-2 (over-fill paste) 측 우선** = 추가 구매 0, 시간 5min, 효과 높음. P1 측 P0 시도 후 fail 시 만.

---

## 5. honest C3 caveats (raw#10)

1. **vendor self-claim**: $59.99 earclip = "stable grounding signal" vendor 측 claim 만, 실측 impedance < 5kΩ stably 측 third-party 검증 측 본 audit 측 미확인. Ag-AgCl spec = 표기 만, 실 plating 측 batch variance 가능.
2. **한국 배송 / 관세**: shop.openbci.com 측 KRW (₩) currency 측 selector 존재 — 단 specific shipping rate / 관세 측 checkout 측 까지 계산 불가. Brooklyn NY 발송 → DHL / UPS 측 7~14일, 관세 측 15만원 미만 면세 (개인사용). $59.99 earclip 측 단품 = 면세 가능성 높음 — 단 vendor 측 한국 배송 측 직접 확인 측 권장.
3. **individual variance**: 귓불 두께 / 머리카락 / 피부 type / 발한량 측 earclip 부착 안정성 측 큰 variance. user (mk55911) 측 귓불 측 earclip 측 첫 시도 — 2~3 session 측 trial-error 측 normal. F_BERGER_03 측 1회 fail = vendor / hardware 측 결함 X 가능성 큼 (prep / placement issue 가능성 더 큼).

---

## 6. 다음 cycle 권장

**path A (recommended)**: F_BERGER_04 = earclip 재부착 (P0-1 + P0-2 적용) 후 Berger 재시도. 동일 시간 / 동일 환경 / 동일 8ch montage 유지, REF/BIAS prep 만 변경. 결과 = α_EC > α_EO 측 reverse 시 → root cause 측 prep / placement 측 confirm.

**path B (fallback)**: eye blink paradigm = REF/BIAS DC drift 측 영향 적음 (eye blink 측 large-amplitude transient signal, REF noise 측 SNR 측 dominate). Berger 측 fail 시 → eye blink 측 첫 valid signal capture 측 우회 path.

→ **완성도 lens 측 ranked recommendation**: **path A 우선** (Berger 측 가장 well-established paradigm, fix 측 minimal effort). path A 2회 fail 시 → path B 측 fallback.

---

## refs

- [Earclip Electrode – OpenBCI Shop](https://shop.openbci.com/products/earclip-electrode)
- [OpenBCI Accessories collection](https://shop.openbci.com/collections/frontpage/accessories)
- [Setting up for EEG | OpenBCI Documentation](https://docs.openbci.com/GettingStarted/Biosensing-Setups/EEGSetup/)
- [Buying ear clips — OpenBCI Forum](https://openbci.com/forum/index.php?p=/discussion/2547/buying-ear-clips)
- [Gelfree BCI Electrode Cap Kit – OpenBCI Shop](https://shop.openbci.com/products/gelfree-bci-cap-kit)
