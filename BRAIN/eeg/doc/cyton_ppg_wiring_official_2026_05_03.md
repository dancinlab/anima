# Cyton PPG (Pulse Sensor) wiring — official vendor mapping

작성일: 2026-05-03
대상: OpenBCI All-in-One R&D Bundle 측 Pulse Sensor (Heart-Rate Monitor) 1개
관련 doc:
- `anima-eeg/docs/cyton_daisy_wiring_diagram_2026_05_03.md` (EEG-only 16ch wiring)
- `anima-eeg/docs/openbci_bundle_ear_clip_options_2026_05_03.md`
- `anima-eeg/docs/cyton_soft_reset_v_command_spec_2026_05_03.md` (`/2` analog mode)

scope: 사용자 hardware 측 Pulse Sensor 3-wire (Red/Black/Purple) 와 Cyton 측 8-pin
auxiliary header 측 official mapping 측 — vendor-cited verify.

---

## 1. Cyton breakout header — official pin layout (vendor schematic 인용)

vendor source: `references/Documentation/website/docs/Cyton/02-Cyton.md` §"Breakout pins"
(GitHub OpenBCI/Documentation, master branch).

> SPI bus pins on the 3V side for Daisy Module expansion
>   — DVDD, GND, MISO, MOSI, SCK, CS, CLK, RST
> Unused PIC32 pins
>   — D11 , D12 (A6), D13 (A7), D17, D18

종합:

```
═══════════════════════════════════════════════════════════════════
             Cyton 측 3V SIDE (SPI/Daisy expansion 측, 8-pin J3)
═══════════════════════════════════════════════════════════════════
  ┌──────┬─────┬──────┬──────┬─────┬────┬─────┬─────┐
  │ DVDD │ GND │ MISO │ MOSI │ SCK │ CS │ CLK │ RST │
  └──────┴─────┴──────┴──────┴─────┴────┴─────┴─────┘
   3.3V  GND   D — Daisy SPI handshake — — RST(ADS1299 MCLR)

═══════════════════════════════════════════════════════════════════
                Cyton 측 "Unused PIC32 pins" (별도 5-pin)
═══════════════════════════════════════════════════════════════════
  ┌─────┬──────────┬──────────┬─────┬─────┐
  │ D11 │ D12 (A6) │ D13 (A7) │ D17 │ D18 │
  └─────┴──────────┴──────────┴─────┴─────┘
   A5    A6         A7         dig   dig
```

note (vendor 측):
- **D11 = A5** in analog mode (이는 Pulse Sensor doc 측 명시 — §2 참조)
- D11 is also "PGD" + has the blue LED in series with 1K → AGND
- D12/D13 dual-purpose: digital 또는 analog (`Aн`), D17/D18 digital-only

(vendor doc 측 D11 측 A-number 측 명시적으로 적지 않으나, Pulse Sensor 측 official
 가이드 측 "D11 is read as analog pin A5" 측 cross-cited.)

---

## 2. Pulse Sensor 3-wire 측 vendor mapping (verbatim)

vendor source: `references/Documentation/website/docs/ThirdParty/Pulse_Sensor/Pulse_Sensor_Guide.md`
(live: `docs.openbci.com/ThirdParty/Pulse_Sensor/Pulse_Sensor_Landing/`).

| Pulse Sensor Wire | Cyton Header | Function              | Internal mapping |
| ----------------- | ------------ | --------------------- | ---------------- |
| **Red**           | **DVDD**     | power (+3.3V)         | 3V side header   |
| **Black**         | **GND**      | ground                | DVDD 옆 GND      |
| **Purple**        | **D11**      | Analog input (signal) | D11 → A5 in `/2` |

vendor 측 직접 인용:
> RED wire (+) = +3V to +5V
> BLACK wire (-) = GND
> PURPLE wire (S) = Signal in milli- or microvolts
>
> The red Pulse Sensor cable goes to the DVDD header on the Cyton, black to
> GND (right next to DVDD), and purple to D11. **This D11 is read as analog
> pin A5 and sent in the first Aux data slot.**

→ 사용자 측 기존 추측 (Red=Vcc, Black=GND, Purple=Signal) 측 정확. 다만 **Signal pin
 측 D11 (= A5)** 으로 확정 — D12/D13 (= A6/A7) 측 아니다.

물리 위치: DVDD + GND 측 SPI 측 8-pin header 측 첫 두 핀 (3V side); D11 측 별도
"Unused PIC32 pins" 5-pin header. 두 header 측 모두 보드 측 같은 sub-region (3V side)
에 위치.

---

## 3. ANALOG mode `/2` 측 정확 effect

vendor source: `references/Documentation/website/docs/Cyton/04-OpenBCI_Cyton_SDK.md`
§"Board Mode" L491–510.

> COMMAND
> - 0 = Default mode — Sends accelerometer data in aux bytes
> - 2 = **Analog mode — Reads from analog pins A5(D11), A6(D12), and A7(D13)** as well.
> - 3 = Digital mode — Reads from analog pins D11, D12, D13, D17, and D18.

→ `/2` 측 send → returns `Board mode set to analog$$$`.

effect 종합:
- accelerometer data (default aux) 측 OFF
- aux byte slot 0 측 A5 (= D11, Pulse Sensor purple) 측 multiplex
- aux byte slot 1 측 A6 (= D12)
- aux byte slot 2 측 A7 (= D13)

power-cycle 시 측 default (accel) 측 복귀 — Pulse Sensor session 측 매번 `/2` 측 재전송
필수.

GUI 측 widget routing: GUI 측 "Pulse Sensor widget" 측 A5 channel 측 자동 read; "Analog
Read" widget 측 A5/A6/A7 측 raw 표시. (vendor Pulse_Sensor_Guide.md §"Cyton Pulse Sensor".)

---

## 4. Daisy stack 측 PPG 측 영향

vendor source: openbci.com forum #1527 (William J. Croft, OpenBCI staff) —
verbatim quote:

> "VDD (DVDD) and GND are also available on J3 on the Cyton mainboard. This
> is in addition to the J1 inter-board connector between the mainboard and
> Daisy. So this J3 set of header sockets is ALWAYS available. Even when
> the Daisy is plugged in."

종합:
- **Daisy stack 측 DVDD/GND access 측 잃지 않는다** — J3 (Cyton 측 SPI breakout) 측
  Daisy 측 J1 inter-board connector 측 별도 socket 측 그대로 노출.
- **D11 측 access 측 staff 측 직접 보장하지 않음** — D11 측 "Unused PIC32 pins" 5-pin
  측 위치, Daisy 측 stack 측 5-pin header 측 가릴 가능성 있음 (board revision 의존).
- forum 측 다른 user 측 reported: D11 측 jumper-wire 측 옆으로 빼서 사용 (Daisy 측
  stack 측 stack 그대로 두고).

권장 (사용자 측):
1. **EEG-only 측 16ch 측** Daisy stack 그대로 사용
2. **PPG 단독 측정 측** Daisy 측 빼고 Cyton 만 사용 — D11 측 fully 노출
3. **EEG + PPG 동시 측정 측** Daisy stack 측 두고, D11 측 short jumper wire 측 옆으로
   route — staff 측 명시 보장 X 이므로 hardware 측 직접 확인 필요

---

## 5. Bundle vendor wiring guide — URL + 핵심 인용

vendor official URL (live, 2026-05-03):
- **Pulse Sensor guide**: `docs.openbci.com/ThirdParty/Pulse_Sensor/Pulse_Sensor_Landing/`
- **Cyton SDK (`/2` analog mode)**: `docs.openbci.com/Cyton/CytonSDK/`
- **Cyton specs (breakout pins)**: `docs.openbci.com/Cyton/CytonSpecs/`
- **forum cyton+daisy PPG thread**: `openbci.com/forum/index.php?p=/discussion/1527/pulse-sensor-with-cyton-daisy`

shop.openbci.com 측 product page 측 별도 wiring guide 측 호스팅하지 않음 — 모두
docs.openbci.com 측 redirect.

핵심 인용 (위 §2 reproduce):
> "red goes to DVDD, black to GND (right next to DVDD), and purple to D11.
> This D11 is read as analog pin A5, and sent in the first Aux data slot."

---

## 6. Honest C3 caveats

1. **V3 schematic 측 outdated 가능성**:
   `references/V3_Hardware_Design_Files/` 측 2015-02-16 DesignSpark commit 측 last
   touched. 현재 shop.openbci.com 측 판매되는 Cyton 측 동일 Rev 인지 vendor 측
   directly 확인하지 않음 — production hardware 측 minor silkscreen 차이 가능.

2. **Daisy stack 측 D11 access 측 hardware revision 의존**:
   staff (wjcroft) 측 J3 (DVDD/GND) 측 always 측 보장하나 D11 측 명시 X. user
   self-claim (forum 측) 만 존재. 사용자 본인 측 hardware 측 Daisy stack 측 D11 5-pin
   header 측 물리 가림 여부 측 시각 확인 필요.

3. **한국 grid noise (60Hz vs 50Hz) 측 PPG 측 영향**:
   한국 측 60Hz mains. Pulse Sensor 측 raw signal 측 ~1Hz heart rate band 측 50/60Hz
   notch 측 멀리 떨어져 영향 적으나, GUI Pulse widget 측 default notch 측 60Hz 측
   설정 권장. Cyton sample rate 250Hz 측 60Hz Nyquist 측 안전.

---

## 7. doc update / land 권장

신규 land:
- `anima-eeg/docs/cyton_ppg_wiring_official_2026_05_03.md` (이 doc) ← **신규**

기존 doc 측 cross-link 추가 권장:
- `anima-eeg/docs/cyton_daisy_wiring_diagram_2026_05_03.md` 측 §관련 doc 측 본 doc
  추가
- `anima-eeg/docs/openbci_bundle_ear_clip_options_2026_05_03.md` 측 PPG 측 사용 가능
  자원 측 본 doc 측 reference 추가

---

## references (local + live)

**local refs**:
- `references/Documentation/website/docs/ThirdParty/Pulse_Sensor/Pulse_Sensor_Guide.md`
- `references/Documentation/website/docs/Cyton/02-Cyton.md` (breakout pin 정의)
- `references/Documentation/website/docs/Cyton/04-OpenBCI_Cyton_SDK.md` (`/2` mode)
- `references/V3_Hardware_Design_Files/OpenBCI Cyton Designs/OpenBCI 32bit.sch`

**live web** (2026-05-03 fetched):
- `docs.openbci.com/ThirdParty/Pulse_Sensor/Pulse_Sensor_Landing/`
- `docs.openbci.com/Cyton/CytonSpecs/`
- `docs.openbci.com/Cyton/CytonSDK/`
- `openbci.com/forum/index.php?p=/discussion/1527/pulse-sensor-with-cyton-daisy`

schematic 측 cross-verify 측 raw schematic 측 file (.sch DesignSpark) 측 직접 열어
header pin numbering 측 확인 측 해당 시 추가 작업 (현재 텍스트 doc 측 인용 측 충분).
