# B-track electrode re-seat runbook (Cyton+Daisy 16ch, mastoid Y-Splitter ref)

작성일: 2026-05-03
scope: B-track electrode re-seat — F3 alpha-blocking re-measurement을 위한 contact-quality 회복 절차
prereq for: Berger 1929 reproduce cycle close (anima_clm_eeg.cond.3 self-N=1 path)

## TL;DR

v6 Berger EC/EO 재분석 (`clean_channels = [2,3,4,7,9,10,11,12,13,14,15]`, rail-saturated 채널 제거)에서 F3 (EC α > EO α × 2)이 여전히 FAIL. O1 단일 verdict는 EC α=64.1 vs EO α=65.6, ratio **0.977** — alpha-blocking 신호 0. frontal α (F3/F4/F7/F8 ≈ 1e+04)가 occipital O1 (~6e+01)보다 100–200× 높은 **inverted physiology** 패턴. 결론: **contact-bound**, NOT analysis-bound. 본 runbook은 시퀀스 A → B → C 중 **B (reference electrode SRB/BIAS + occipital re-seat)** 단계를 falsifier-bound로 정의. 4개 falsifier (F_BTRACK_01~04) PASS 시 v7 measurement 진입.

## §1. Why B-track now (P1 evidence)

P1 BG (`a18ec50f47820c957`) finalize한 v6 clean re-analyze 결과:

| 항목 | v5 (raw 16ch) | v6 (clean 11ch) | 판정 |
|------|---------------|------------------|------|
| F1 (occipital α peak prominence ratio) | < 1.2 | 1.08 | FAIL |
| F3 (EC α / EO α on O1) | rail-distorted | 64.1 / 65.6 = **0.977** | FAIL |
| frontal α (F3/F4/F7/F8) | ≈ 1e+04 | ≈ 1e+04 | inverted (100–200× O1) |
| O1 row 7 | clean | clean (always was) | — |
| O2 row 8 | railed | excluded | rail confirmed |

핵심 인사이트:
- O1은 처음부터 clean set 안에 있었음. 즉 분석-단계 필터링으로 더 좋아질 여지가 없음.
- O1 ratio 0.977은 **alpha-blocking 자체가 측정되지 않았다**는 뜻 (EC/EO 차이 < 3%).
- frontal-occipital 역전 (frontal이 100×↑) 은 정상 두피 EEG에서는 발생하지 않음 → **electrode-skin interface 문제**가 가장 가능성 높음 (paste dry-out, hair-impedance, mastoid reference 부유).

P1 verdict: "contact-bound, NOT analysis-bound. re-seat 없이 v7 measurement는 의미 없음."

cite: `state/berger_v6_clean_reanalyze_2026_05_03/verdict.json`

## §2. Hardware checklist

OpenBCI All-in-One R&D Bundle 전제 (medical-grade gel은 없음 — Bundle 인벤토리만 사용).

### 2.1 Electrode count

| 항목 | 수량 | 비고 |
|------|------|------|
| scalp dry electrode (Ultracortex spider) | 16 | F3/F4/C3/C4/P3/P4/P7/P8/O1/O2/F7/F8/T7/T8/Fp1/Fp2 (row 1–16) |
| reference (white SRB2) | 1 | A1 left mastoid (Y-Splitter 좌측) |
| ground (black BIAS) | 1 | A2 right mastoid (Y-Splitter 우측) — linked-mastoid 권장 |
| Y-Splitter cable | 1 | 1M → 2F, SRB+BIAS 동시 mastoid 접지용 |

### 2.2 Conductive material (Bundle 한정)

| material | 용도 | 적용 부위 |
|----------|------|----------|
| Ten20 conductive paste | scalp dry electrode 보강 | 16ch 두피 |
| Bundle EMG/ECG Gel Electrode (sticker type, ear-clip 호환) | mastoid reference | A1/A2 ear |
| 70% isopropyl alcohol wipe | 피부 oil 제거 | 모든 부위 prep |
| gauze pad | 알코올 후 dry | 모든 부위 |
| q-tip | paste 정밀 도포 | electrode hole 안쪽 |

### 2.3 Tools

- 거울 또는 assistant (occipital O1/O2 시야 확보)
- 머리 가르기용 빗 (hair-part for paste contact)
- impedance check 스크립트 실행용 호스트 (Mac, USB serial port `/dev/cu.usbserial-DP04WGIQ`)

cite:
- `anima-eeg/docs/cyton_daisy_wiring_diagram_2026_05_03.md` (mastoid Y-Splitter ref 배선)
- `anima-eeg/docs/openbci_bundle_ear_clip_options_2026_05_03.md` (Bundle gel electrode 사용 이력)

## §3. Re-seat procedure

총 소요 ≈ 25–35분. **사용자 두피 통증 시 즉시 중단** (raw#10 C3-2).

### 3.1 Pre-prep (5 min)

1. Ultracortex 헬멧을 머리에서 분리 (이미 분리된 상태 — "eeg 벗고 휴식좀 취할께" 시점 이후 cycle 재진입).
2. 손/팔 알코올 wipe (cross-contamination 방지).
3. 머리 가르기 빗으로 16개 electrode 위치 노출 — 특히 occipital (O1/O2, 10-20 system 후두 좌우).
4. 각 site 알코올 wipe → gauze로 dry. 두피 자극 시 1분 휴식.

### 3.2 Reference electrodes FIRST (10 min)

가장 중요. 부유한 reference는 모든 16ch에 inverted/distorted 패턴을 만듦.

1. mastoid (귀 뒤 단단한 뼈) 좌우 알코올 wipe 1회.
2. **A1 left mastoid**: Bundle EMG/ECG Gel Electrode (sticker) 부착 → SRB2 (white snap) 연결.
3. **A2 right mastoid**: 동일 sticker 부착 → BIAS (black snap) 연결.
4. Y-Splitter 케이블 정렬 (SRB+BIAS 양쪽 ear loop으로 cable strain 없음 확인).
5. **60–90s settle wait**: 전기화학 평형 도달 — gel sticker가 피부 아래 ion exchange를 안정화하는 시간. 측정/impedance check 즉시 시도하면 false high가 나옴.

### 3.3 Occipital electrodes (O1/O2) — Berger 최우선

F3 falsifier가 O1/O2에 의존하므로 가장 정성스럽게 수행.

1. **O1** (row 7, 10-20 system 후두 좌측):
   - 머리카락을 빗/손가락으로 강하게 가름 → 두피 노출.
   - electrode hole 위에 q-tip으로 Ten20 paste 소량 (쌀알 크기) 도포.
   - 헬멧 spider electrode를 두피에 직접 접촉시키며 paste가 hole을 통해 contact 형성하도록 압박.
   - 두피 마사지 (10–15초): impedance ↓ 효과 (paste-skin coupling).
2. **O2** (row 8, 후두 우측): O1과 동일 절차.
3. paste 도포 후 60s 대기 (skin penetration).

### 3.4 Frontal Fp1/Fp2 — secondary

v6에서 rail saturation 빈발 (row 1, 2). 머리카락 없는 부위라 hair-part 불필요하지만 **이마 oil 제거가 핵심**.

1. Fp1/Fp2 site 알코올 wipe 2회 (oil이 paste를 밀어냄).
2. gauze dry → Ten20 paste 소량.
3. spider electrode 직접 접촉.
4. railing 재발 시 §4 impedance check에서 quarantine 후보로 식별.

### 3.5 Remaining 12ch (F3/F4/C3/C4/P3/P4/P7/P8/F7/F8/T7/T8) — scalp-quality maintenance

1. 각 site 알코올 wipe → hair-part → paste → 접촉.
2. F7/F8/T7/T8은 머리카락 line 근처라 hair-part 더 신경.
3. 16ch 모두 도포 완료 시 헬멧 fit 재조정 (chin strap 너무 조이지 않게 — 두피 통증 원인).

## §4. Impedance verify gate

**measurement 진입 전 mandatory**.

```bash
hexa run anima-eeg/impedance_check.hexa --check \
    --port /dev/cu.usbserial-DP04WGIQ --board cyton_daisy
```

### 4.1 Acceptance

- **PASS**: 16/16 GREEN (impedance < 750 kΩ; **occipital O1/O2 < 500 kΩ ideal**).
- **MARGINAL**: 1–2ch 750k–1.5MΩ → 해당 row 재도포 + 접촉 재시도.
- **FAIL**: 임의 row > 1.5MΩ 또는 occipital > 750 kΩ → §3.3 / §3.5 해당 step 반복.

### 4.2 Persistent FAIL handling

3회 재시도해도 fail 유지 시:
1. 해당 row를 `clean_channels` override list에 추가하여 quarantine.
2. 단 occipital (O1/O2)가 fail일 경우 **B-track close 불가** — F3 falsifier가 occipital-bound임.
3. 사용자 두피 통증 발생 시 **즉시 cycle 중단** (raw#10 C3-2).

## §5. DC settle wait

impedance PASS 직후, measurement 직전에 수행.

### 5.1 절차

1. 60–180s blank capture (no audio cue, just stream).
2. per-channel mean drift 모니터.
3. 가능하면 wrapper script:
   ```bash
   hexa run anima-eeg/protocols/dc_settle_trim.hexa --check \
       --port /dev/cu.usbserial-DP04WGIQ --duration 180
   ```
   (script 부재 시 berger_session_audio.hexa의 prep phase 60s 활용 후 numpy로 mean 계산)

### 5.2 Acceptance

- 각 채널 mean ∈ **±50 mV** (Cyton 24-bit ADC ±187.5 mV rail 대비 ~27% margin).
- |drift| (마지막 30s mean − 첫 30s mean) < 20 mV per channel.
- FAIL 시: §3.2 reference settle wait 부족 가능성 → 추가 60s 대기 후 재check.

## §6. v7 Berger re-measurement protocol

§4 + §5 모두 PASS 후에만 진입.

### 6.1 실행

```bash
hexa run anima-eeg/protocols/berger_session_audio.hexa --run \
    --port /dev/cu.usbserial-DP04WGIQ --board cyton_daisy \
    --version v7
```

### 6.2 Audio cue (4 min total)

- 0–60s: "눈을 감고 휴식하세요" (EC, alpha 생성 phase)
- 60–70s: "잠시 대기" (transition rest)
- 70–130s: "눈을 뜨고 정면을 응시하세요" (EO, alpha 차단 phase)
- 130–240s: "측정 종료. 휴식"

(berger_session_audio.hexa는 이미 land됨 — `anima_eeg_protocols_quickstart_2026_05_03.md` §2.4)

### 6.3 Output

- `anima-eeg/recordings/sessions/berger_ec_60s_v7_2026_05_03.npy`
- `anima-eeg/recordings/sessions/berger_eo_60s_v7_2026_05_03.npy`

### 6.4 Re-analyze

```bash
python anima-eeg/scripts/v6_clean_reanalyze.py \
    --ec berger_ec_60s_v7_2026_05_03.npy \
    --eo berger_eo_60s_v7_2026_05_03.npy \
    --version v7 --out state/berger_v7_reanalyze_2026_05_03/
```

기대: F3 verdict update (PASS 시 ratio > 2.0; FAIL 시 §8 raw#10 C3-3 적용).

note: 형제 BG N4가 `analyze.hexa` wrapper에 auto-rail-detect (`__RAIL_AUDIT__`)를 land하면 step 7은 wrapper 호출로 대체 (§10 참조).

## §7. Falsifier (B-track close gate)

4개 falsifier ALL PASS → B-track close + v7 measurement 진입 허가.

| ID | 조건 | threshold | 측정 시점 |
|----|------|-----------|-----------|
| F_BTRACK_01 | impedance 16ch GREEN | 16/16 < 750 kΩ | §4 impedance check |
| F_BTRACK_02 | per-channel DC mean | abs(mean) ∈ ±50 mV after 180s settle | §5 DC settle |
| F_BTRACK_03 | occipital impedance | O1 AND O2 < 500 kΩ | §4 impedance check |
| F_BTRACK_04 | frontal-occipital sanity | frontal α (F3/F4/F7/F8 mean) < 100 × occipital α (O1/O2 mean) after 60s blank | §5 DC settle 직후 30s 추가 spectrogram |

ANY FAIL → 해당 영역 re-seat 후 retry. 3회 retry 후에도 fail 시 cycle 중단 + raw 기록 + 사용자 결정 대기.

## §8. Honest C3 caveats (raw#10)

### C3-1 cohort still missing

본 runbook은 self-N=1 experiment에 한정. `anima_clm_eeg.cond.3` 의 cohort N≥8 요구사항은 **이 runbook으로 충족되지 않음**. B-track PASS는 self-Berger reproduce의 필요조건일 뿐 충분조건 아님.

### C3-2 user health > falsifier closure

이전 cycle에서 사용자가 "eeg 벗고 휴식좀 취할께 너무 아프네" 보고 — 두피 통증은 cap fit 또는 electrode hole 위치 압박 신호. **재발 시 즉시 §3 절차 중단**, 헬멧 size/strap 재조정 또는 electrode hole 위치 미세 이동. 어떠한 falsifier closure도 사용자 health에 우선하지 않음.

### C3-3 alpha-blocking is per-individual

B-track PASS 후에도 F3가 fail할 수 있음. 일부 성인은 alpha-blocking ratio가 < 2× (Berger 원본 1929 cohort에도 ~10% non-responder 존재). 이 경우 negative result 정직히 기록 (raw#71 — falsifier-bound negativity), `anima_clm_eeg.cond.3` 는 cohort phase로 escalate.

### C3-4 Bundle inventory only

medical-grade conductive gel, AgCl wet electrode 등은 재고에 없음. Ten20 paste + Bundle EMG/ECG sticker 한계 내에서만 절차 정의. 더 강한 contact 필요 시 별도 구매 cycle 필요 (이 runbook의 scope 아님).

## §9. Cross-links

- `state/berger_v6_clean_reanalyze_2026_05_03/verdict.json` — P1 evidence (O1 ratio 0.977, frontal inversion)
- `docs/eeg_v6_audit_synthesis_2026_05_03.md` — full audit context (sample-rate, rail saturation, clean_channels 도출)
- `anima-eeg/docs/anima_eeg_protocols_quickstart_2026_05_03.md` §7 — clean_channels override 사용법
- `anima-eeg/docs/cyton_daisy_wiring_diagram_2026_05_03.md` — mastoid Y-Splitter (1M → 2F) 배선
- `anima-eeg/docs/openbci_bundle_ear_clip_options_2026_05_03.md` — Bundle gel electrode prep 이력
- `anima-eeg/docs/electrode_adjustment_16ch_concurrent_2026_04_29.md` — 이전 16ch 동시 조정 시도 (참조용)
- `anima-eeg/docs/fp1_chronic_noise_diagnose_2026_05_03.md` — Fp1 만성 noise 진단 (§3.4 보강)

## §10. Next-cycle dependencies

### 10.1 형제 BG N4 (analyze.hexa wrapper auto-rail-detect)

land 시 §6.4 step 7은 `hexa run anima-eeg/protocols/analyze.hexa --auto-rail` 으로 자동화. 본 runbook에서는 wrapper 미land 가정으로 manual `v6_clean_reanalyze.py` 호출. wrapper land 후 cite 갱신 필요 (§6 step 7).

### 10.2 형제 BG N2 (transcoder real-swap)

v7 measurement npy가 produce되면 P1→transcoder→harness chain이 v7 fixture로 re-run. 본 runbook의 §6.3 output path는 transcoder가 watch하는 directory와 일치 (`anima-eeg/recordings/sessions/`).

### 10.3 본 runbook 미터치 영역

다음 파일/디렉토리는 형제 BG가 owner이므로 **수정 금지**:
- `.roadmap.*` (sibling BG N1)
- `anima-clm-eeg/` (sibling BG N2)
- `anima-eeg/protocols/analyze.hexa` 및 wrapper (sibling BG N4)
- `anima-eeg-core/_metrics/` (P3 read-only)

본 runbook scope는 `anima-eeg/docs/` 내 신규 markdown 단일 파일 land 한정.

---

작성: 2026-05-03 P2 BG (B-track owner)
status: ready-for-execution (사용자 cap re-don 시점에 §3부터 진행)

## 11. Connector strain-relief reinforcement (hardware add-on, 2026-05-03 conversation finding)

§1–10은 electrode-scalp contact (paste, hair-part, mastoid reference)을 다룸. §11은 conversation 중 새로 확인된 **connector-PCB contact** layer를 추가. APPEND-ONLY (append 시점: 2026-05-03 N3 BG follow-up).

### 11.1 Why this matters (root cause clarification)

- **N4 wrapper finding**: real .npy v6 EC에 대한 `__RAIL_AUDIT__` = **FAIL 16/16** (앞선 audit 5/16 보고는 v5 raw 측정 기반이었고, v6 EC 측정에서는 16/16 전 채널 rail-saturated 상태). cite: `state/.analyze_wrapper_dump.txt`.
- 16/16 saturation은 **dual cause** 가능성을 시사:
  - (a) electrode-scalp contact layer (B-track §3가 다룸 — paste, hair-part, mastoid settle).
  - (b) **connector-PCB contact layer** (이 §11이 다룸 — dupont housing pop-off, cable strain).
- Cyton+Daisy 16ch 측 dupont (0.1" / 2.54mm pitch) 측 header pin은 **safety-design low-retention** — 케이블 인장 또는 우발적 접촉으로 housing이 board-pin에서 빠짐 (community-known issue).
- frequent pop-off site (community report):
  - Daisy stack 16-pin header (Cyton 위 stack-on)
  - SRB pin (white)
  - BIAS pin (black)
  - 16개 channel signal pin (특히 cable이 PCB 측면에 닿는 경우)
- Y-splitter cable (1M → 2F, $0.99 OpenBCI) 측 board-side는 동일 0.1" pitch dupont이므로 **동일 low-retention** — mastoid Y-Splitter ref 셋업도 §11 대상.

cite: https://shop.openbci.com/products/y-splitter-cable

### 11.2 Tools — Daiso 즉시 입수 (no 3D printer, no heat gun required)

| 부품 | 용도 | 가격 | 수량 | 비고 |
|------|------|------|------|------|
| 열수축튜브 12P mixed (3/4/6mm) | dupont housing 측 wire-entry strain relief | ₩1,000 | **1 pack 충분** | 16ch + Y-splitter 3 = 19 connector × 2cm = 38cm 소요. 12P × 10cm = 120cm 보유 → 3× margin. cite: https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=68551 |
| 머리끈 얇은 16P | board-strap (light tension) | ₩1,000 | 1 pack | cite: https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1025760 |
| 머리끈 굵은 13P | bridge anchor (cable strain relief) | ₩1,000 | 1 pack | cite: https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1025762 |
| 머리끈 통통 블랙 10P | (옵션) heavy-duty bridge | ₩1,000 | 0–1 pack | cite: https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1051760 |
| (선택) Sugru moldable rubber | custom strain relief mold | ₩4,500/50g (한국 retailer) | 8-pack 권장 | 영구적; 본 runbook 미사용, 후속 cycle 대안 |

총 ₩3,000–4,000 + (선택) Sugru ₩4,500. 사용자 inline JST rocker switch (battery line) 이미 설치됨 — 별도 add-on 불필요.

### 11.3 Heat tool options (no heat gun)

| 도구 | 거리 | 시간 | 평가 |
|------|------|------|------|
| 헤어드라이어 hot setting (60–80°C) | 5–10cm wave | 30–60s | recommended (PCB-safe, even heat) |
| 라이터 (BIC) | 5–10cm | 3–5s wave (sides → top → sides) | acceptable, **PCB removed first** |
| 성냥 / open flame at < 5cm | < 5cm | — | reject (char + insulation damage) |

사용자 confirmed: 라이터 acceptable (PCB removal 전제). 가능하면 헤어드라이어 우선.

### 11.4 Procedure (5–10 min total, before §3.3 occipital re-seat)

**Pre-step**: Cyton 보드 측 모든 dupont 측 분리 (heat tool로 인한 PCB 측 SMT chip reflow 위험 회피). Daisy stack도 분리.

**Layer 1 — heat shrink per dupont** (30s each × 19 = ~10 min):

1. 6mm size heat shrink을 2cm 길이로 cut (dupont housing OD ≈ 3–4mm, 6mm tube 측 33–50% shrink ratio로 fit).
2. wire 측 open end → housing-base junction 측 슬립 (1mm overlap onto plastic housing — wire-bend stress 흡수 지점).
3. 헤어드라이어 hot setting 측 30–60s wave (또는 라이터 5–10cm 측 3–5s wave, sides → top → sides 순).
4. 30s cool 후 다음 connector.
5. 16ch + Y-splitter 1M 측 + Y-splitter 2F × 2 = 19 dupont 모두 적용.

**Layer 2 — rubber band board strap** (방법 3 from conversation, ~2 min):

1. 굵은 머리끈 1개 측 PCB 측 둘레 측 가로 wrap (connector row 측 위 측 cross).
2. **SMT chip 측 직접 접촉 회피** — board edge 측 cross-over only (ESD-sensitive — §11.7 C3-6 참조).
3. lateral mount-hole 측 hook → strap slip 차단.
4. tension light: 보드 표면이 눌려서 휘지 않을 정도 (PCB flex < 0.5mm).

**Layer 3 — bridge anchor (cable strain relief)** (방법 2, ~2 min):

1. cable bundle 측 connector 측 위 2–3cm 지점 측 머리끈 wrap.
2. 양 끝 측 PCB 반대편 mount-hole 측 통과 + 매듭 (board 측 connector pin 반대 방향으로 cable load 전환).
3. **cable yank test**: cable 측 가볍게 당겨도 board 측 transfer되지 않음 — bridge anchor가 strain 흡수.

전체 적용 후 Cyton 보드 + dupont 재조립 → §4 impedance check 진입.

### 11.5 Falsifier addendum (extends §7)

§7 표 끝에 추가:

| ID | 조건 | threshold | 측정 시점 |
|----|------|-----------|-----------|
| F_BTRACK_05 | post-reinforcement connector pop-off rate | **< 1 / measurement** (cable-tug test 5/5 trial PASS) | §11.4 완료 직후 + §6 measurement 직전 |

cable-tug test: cable bundle을 90° 좌/우/위/아래/회전 5방향 가볍게 당김 (1N 미만, ~100g 무게 수준) — 모든 방향에서 connector가 board에 retain되어야 함.

### 11.6 Updated v7 protocol sequence

§6 measurement 진입 sequence를 다음으로 갱신:

1. **§11.4 hardware reinforcement** (Layer 1 + 2 + 3) — pre-don 시점, ~10 min.
2. §3 electrode re-seat (occipital priority, §3.3).
3. §4 impedance verify (F_BTRACK_01, _03 gate).
4. §5 DC settle (F_BTRACK_02, _04 gate).
5. §6 v7 measurement 실행.
6. §7 falsifier gate (F_BTRACK_01..**05** ALL PASS).

**Expected progression**:
- v6 baseline: 16/16 rail-saturated (real .npy 기준).
- post-§11 reinforcement v7 expected: **≤ 5/16 saturation** (connector contribution 제거; 잔여 saturation은 electrode-skin contact 측 §3에서 추가 처리).
- 둘 다 적용된 v7에서 F3 verdict (EC α / EO α > 2.0) 재평가.

### 11.7 Honest C3 (extends §8)

#### C3-5 reversibility

heat shrink는 semi-permanent — 제거 시 cut (knife) 필요. 재시공 시 heat shrink ~₩50/connector × 19 = ₩1,000 미만으로 redo 가능. full mod (Sugru) 대비 reversible.

#### C3-6 ESD-sensitive PCB compression

Cyton 측 SMT chip (ADS1299, OPA, regulator 등)은 ESD-sensitive + mechanical-stress-sensitive. rubber band tension 과도 시 chip lead 측 micro-crack → 측정 noise 또는 chip dead. **edge cross-over only**, chip 표면 직접 압박 금지. 시공 전 손/도구 측 ESD discharge (금속 접지 touch) 권장.

#### C3-7 connector-only fix는 부분 해결

§11은 **connector-PCB contact** layer만 다룸. electrode-scalp contact (paste dry-out, hair-impedance, mastoid 부유)는 §3가 owner. F3 alpha-blocking verdict 변경에는 **§3 + §11 둘 다 필요**. §11 단독으로 16/16 → 0/16 saturation 회복 보장 불가 — 가장 가능성 높은 reduction은 16/16 → 5/16 수준 (connector contribution 제거).

### 11.8 Cross-links (extends §9)

§9 cross-links 목록에 추가:

- N4 wrapper finding: `state/.analyze_wrapper_dump.txt` (16/16 v6 saturation 근거)
- Daiso 열수축튜브 12P mixed: https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=68551
- Daiso 머리끈 얇은 16P: https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1025760
- Daiso 머리끈 굵은 13P: https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1025762
- Daiso 머리끈 통통 블랙 10P: https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1051760
- OpenBCI Y-splitter cable (1M → 2F, $0.99): https://shop.openbci.com/products/y-splitter-cable

---

§11 작성: 2026-05-03 N3 follow-up BG (hardware connector strain-relief layer)
status: ready-for-execution (cap re-don 직전 §11.4 → §3 → §4 → §5 → §6 sequence)
