================================================================================
OpenBCI Cyton 배터리 구매 + 연결 가이드 (FULL)
2026-04-28 anima EEG D-day session
================================================================================

【최종 목표】
Cyton + Daisy 16ch + Mark IV 헬멧 안정 power 확보 → battery dying invalidation 해결.

【배터리 dying 문제 발견】
직전 모든 EEG 측정 결과 (Berger gate FAIL / LZ76 P1_FAIL / γ/θ FALSIFIED) 가
Cyton battery 전압 강하 → amplifier saturation → broadband noise 영향 가능성 높음.
전원 안정 후 재측정 필수.

================================================================================
1. 구매 셋트 (vctec 한 곳 동시 주문 권장)
================================================================================

[A] vctec 4×AA Battery Holder + Switch + DC Jack + Cover
URL: https://vctec.co.kr/product/4%C3%97aa-%EB%B0%B0%ED%84%B0%EB%A6%AC-%ED%99%80%EB%8D%94-%EC%8A%A4%EC%9C%84%EC%B9%98-dc%EC%9E%AD-%EC%BB%A4%EB%B2%84-4%C3%97aa-battery-holder-with-power-switch-dc21-jack/21244/
가격: ~3,000-5,000원
특징:
  - AA 4개 직렬 (1.5V × 4 = 6V) ← Cyton spec 3-6V 정확 일치
  - ON/OFF 스위치 (안전 + 편의)
  - DC 2.1mm barrel jack 출력
  - 커버 포함 (AA 빠짐 방지)

[B] vctec 배럴 전원잭 to 2-pin JST 케이블
URL: https://vctec.co.kr/product/%EB%B0%B0%EB%9F%B4-%EC%A0%84%EC%9B%90%EC%9E%AD-to-2-pin-jst-%EC%BC%80%EC%9D%B4%EB%B8%94-barrel-jack-to-2-pin-jst/3047
가격: ~3,000원
특징:
  - DC 2.1mm barrel jack 입력
  - JST PH 2.0mm 2-pin 출력 (Cyton battery socket 호환)

[C] AA 알카라인 배터리 4개
권장 1: Duracell (마트/쿠팡, ~3,000원, 1회용)
권장 2: Eneloop 충전 4개 + 충전기 (쿠팡, ~25,000원, 재충전 가능 — 장기 사용 권장)
용량: 알카라인 ≈ 8-15시간 / Eneloop ≈ 6-10시간

[D] 멀티미터 (보유 시 skip)
사용자 이미 보유 중일 수 있음 (확인 필요).
미보유 시 옵션:
  - 다이소 멀티미터 (~5,000원, DC + 도통 + 저항 — 충분)
  - 쿠팡 디지털 멀티미터 (~6,000-15,000원)
  - DC 전압 측정 + 도통 체크 가능한 모델이면 됨

================================================================================
예상 합계
================================================================================
[A] vctec 4×AA holder         : 3,000-5,000
[B] vctec barrel→JST cable    : 3,000
[C] AA 4개 (Duracell)          : 3,000
                                 ----------
TOTAL (멀티미터 보유)           : ~9,000-11,000원

[D] 멀티미터 (미보유 시)         : +5,000
TOTAL (멀티미터 신규)           : ~14,000-16,000원

비교: Cyton + Daisy 보드 ~130만원 → 멀티미터 5천원으로 보드 보호 = ROI 명백

================================================================================
2. 도착 후 진행 절차 (순서대로)
================================================================================

★ 모든 단계 Cyton 전원 OFF 위치에서 시작 ★

────────────────────────────────────────────────────────────────────────────────
STEP 1 ── 멀티미터 준비
────────────────────────────────────────────────────────────────────────────────

1-1. 멀티미터 다이얼: DC 20V 위치 (왼쪽 영역 V---, 점 3개)
     ※ 자동 레인지면 V 만 선택, 수동이면 20V 정확히
1-2. probe 잭 연결:
     - 빨강 probe → "ΩVmA" 잭 (오른쪽)
     - 검정 probe → "COM" 잭 (가운데)
     ※ "10ADC" 잭은 절대 사용 X (10A 측정 전용, 5V 측정 시 위험)
1-3. 영점 확인: probe 떨어뜨려 LCD "0.00" 표시 → OK
     ※ drift 시 멀티미터 9V battery 잔량 부족 가능

────────────────────────────────────────────────────────────────────────────────
STEP 2 ── AA 4개 holder 에 꽂기
────────────────────────────────────────────────────────────────────────────────

2-1. holder 내부의 + / - 표기 따라 AA 4개 정상 방향
2-2. 모든 AA 끝까지 들어갔는지 확인 (헐거우면 접촉 불량)
2-3. holder 의 ON/OFF 스위치 → OFF 상태 유지

────────────────────────────────────────────────────────────────────────────────
STEP 3 ── holder + barrel→JST 케이블 결합
────────────────────────────────────────────────────────────────────────────────

3-1. holder 의 DC 2.1mm barrel jack 출력
3-2. cable 의 barrel plug 끝까지 꽂기 (딸각 소리 없이 부드럽게)
3-3. cable 의 JST plug 끝 노출 — 검증 대상
3-4. holder 스위치 ON

────────────────────────────────────────────────────────────────────────────────
STEP 4 ── ★ 멀티미터 polarity 검증 (CRITICAL) ★
────────────────────────────────────────────────────────────────────────────────

⚠️ 이 단계 skip = 50% 확률로 Cyton 보드 파괴 ⚠️

4-1. holder 스위치 ON 상태
4-2. cable 출력 JST plug 의 두 핀에 multimeter probe:
     - 빨강 probe → JST 핀 1 (왼쪽 또는 오른쪽 중 하나, key TOP 기준)
     - 검정 probe → JST 핀 2 (반대편 핀)
4-3. LCD 표시 해석:
     ┌──────────┬──────────────────────────────────────────┐
     │ LCD 표시 │ 의미                                      │
     ├──────────┼──────────────────────────────────────────┤
     │ +6.0V    │ 핀 1 = + ✓ Cyton 직접 연결 안전           │
     │ (또는    │ → STEP 5 로 진행                          │
     │ +5.5~    │                                            │
     │ +6.5)    │                                            │
     ├──────────┼──────────────────────────────────────────┤
     │ -6.0V    │ 핀 1 = - ⚠️ polarity 반대                │
     │ (마이너  │ → cable wire swap 필요 (또는 다른 cable) │
     │ 스 부호) │ → wire 직접 swap 시 납땜 또는 절연 테이프 │
     ├──────────┼──────────────────────────────────────────┤
     │ 0.00     │ 케이블 단선 또는 AA 잔량 부족             │
     │ 또는 OL  │ → AA 교체 + 케이블 점검                  │
     └──────────┴──────────────────────────────────────────┘
4-4. holder 스위치 OFF (검증 완료 후)

────────────────────────────────────────────────────────────────────────────────
STEP 5 ── (Optional) Cyton 측 polarity 도통체크
────────────────────────────────────────────────────────────────────────────────

※ STEP 4 에서 +6.0V 정확 확인되면 skip 가능
※ 더 안전하게 검증하고 싶으면 진행

5-1. Cyton 전원 OFF + battery 미연결 상태
5-2. 멀티미터 다이얼: 저항/도통 영역 → "200Ω" 또는 도통 표시 ㅇ))
5-3. probe 접촉:
     - 빨강 probe → Cyton JST socket 의 한 핀
     - 검정 probe → Cyton 보드의 GND 점
       (USB metal shield 또는 BIAS 핀 = bottom row 10번째)
5-4. LCD 결과:
     - 0Ω 근처 (또는 도통 삐 소리) → 그 JST 핀 = - (GND)
     - 무한대 (OL) → 그 JST 핀 = + (RAW)
5-5. 반대편 JST 핀도 확인 (cross-check)
5-6. STEP 4 의 cable + 위치와 Cyton 의 + 위치 일치 확인

────────────────────────────────────────────────────────────────────────────────
STEP 6 ── Cyton 연결
────────────────────────────────────────────────────────────────────────────────

6-1. Cyton 전원 OFF (스위치 OFF 위치)
6-2. holder 스위치 OFF
6-3. cable JST plug → Cyton battery socket 끝까지 꽂기 (key TOP 일치)
6-4. holder 스위치 ON
6-5. Cyton 스위치 PC 위치로 슬라이드 (BLE 아님!)

────────────────────────────────────────────────────────────────────────────────
STEP 7 ── Smoke test
────────────────────────────────────────────────────────────────────────────────

7-1. Cyton blue LED 점등 ✓ (정상 power)
7-2. USB Dongle red LED 깜빡 ✓ (BLE 통신 정상)
7-3. Cyton 보드 손등 대 보기 — 따뜻함 X (정상)
7-4. 5초 대기 후 다시 확인

⚠️ 하나라도 fail → 즉시 disconnect:
   - holder 스위치 OFF
   - JST plug 분리
   - 보드 점검 (이상 onset 시 OpenBCI 지원 문의)

────────────────────────────────────────────────────────────────────────────────
STEP 8 ── anima 측정 검증
────────────────────────────────────────────────────────────────────────────────

8-1. Terminal 에서:
     cd /Users/ghost/core/anima
     hexa run anima-eeg/eeg_setup.hexa health \
       --check --port /dev/cu.usbserial-DP04WGIQ
     → 16/16 alive 확인 ✓

8-2. 헬멧 착용 + saline 적용 후:
     hexa run anima-eeg/eeg_setup.hexa impedance_validate \
       --measure --port /dev/cu.usbserial-DP04WGIQ
     → 16/16 GREEN 확인 ✓

8-3. 60s baseline 재측정 (stable power 첫 EEG):
     hexa run anima-eeg/eeg_setup.hexa record \
       --record --task baseline_resting_post_battery_fix \
       --duration 60 --segment 60 \
       --port /dev/cu.usbserial-DP04WGIQ
     → state/eeg_recordings/<ts>_baseline_resting_post_battery_fix.npy

8-4. Berger gate first (alpha 8-13Hz peak 검증):
     hexa run anima-clm-eeg/tool/clm_eeg_berger_sanity.hexa \
       --input <new baseline .npy>
     → PASS 시: 진짜 cortical activity 측정 ✓
     → FAIL 시: 다른 root cause (skin prep, electrode 등) 점검

8-5. Berger PASS 확인 후 LZ76 / γ/θ / DMN 등 모든 downstream 측정

================================================================================
3. 안전 주의사항
================================================================================

[a] OpenBCI Cyton spec: 3-6V DC battery ONLY
    - AA 4개 직렬 = 6V (정확한 spec 상한, 안전)
    - LiPo 7.4V 등 X (overvoltage → 보드 파괴)

[b] Polarity 보장 X
    - vctec / 어느 cable 도 OpenBCI 와 polarity 일치 보장 X
    - multimeter 검증 100% 필수

[c] Mains 절연
    - 헬멧 쓴 상태에서 Cyton 사용 시 USB 노트북 연결 = mains earth 위험
    - AA holder 사용 = mains 완전 분리 ✓ 안전

[d] Reverse polarity protection
    - Cyton 보드 schottky diode (D9) 있지만 protection 강도 확실 X
    - multimeter 검증 후 연결 = 보장 100%

[e] AA 배터리 수명
    - 알카라인 4×AA ≈ 8-15시간 사용 가능
    - Eneloop 충전 ≈ 6-10시간 (재충전 가능)
    - 6V 미만 떨어지면 (예: 5.5V) 측정 불안정 → 새 배터리 교체

[f] 헬멧 안전
    - Saline allergy 없는지 확인
    - 8h 이상 측정 시 헬멧 압박 견딜 수 있는지 1h dry-run 권장
    - mid-session saline 재적용 필요 (electrode drift)

================================================================================
================================================================================

OpenBCI V3 Cyton schematic 분석 (anima/references/V3_Hardware_Design_Files):

확정된 사실:
  - JST connector pin 2 = + (positive) → diode D9 → net RAW
  - JST connector pin 3 = - (negative) → AGND
  - Pin 1, 4 = 기계적 mounting tabs (전기 연결 X)
  - Component: B1 BATT SM (JST-2), Bottom 면, 180° 회전

확인 못한 부분:
  - 물리적 LEFT/RIGHT 매핑 INDETERMINATE
  - Silkscreen + / - 표기 X (보드에 표시 없음)
  - DesignSpark .pcb 파일 Windows 렌더링 시만 정확 확정

→ 결론: multimeter 검증 mandatory

================================================================================
5. 사용자 멀티미터 spec (이전 메시지 검증)
================================================================================

Option 1 (작은 흰색 LR44 ×2, 3V):
  - DC + AC 전압, 저항, 도통체크
  - 3¾ digit 4000 count, 자동 레인지
  - Cyton 검증 가능

Option 2 (주황 + 검정, 9V battery):
  - DC 200mV / 2V / 20V / 200V / 600V (±0.5%)
  - 저항 200Ω / 2K / 20K / 200K / 2M (±1%)
  - 큰 LCD, 가독성 좋음
  - Cyton 검증에 더 추천

(둘 다 보유 시 Option 2 사용 권장)

================================================================================
6. anima D-day 2026-04-28 session 결과 cross-link
================================================================================

INDEX:    /Users/ghost/core/anima/anima-clm-eeg/docs/d_day_session_2026_04_28/INDEX.md
회로도:    /tmp/cyton_jst_polarity_analysis_2026_04_28.md (분석 보고서)
헬멧:      /Users/ghost/core/anima/anima-eeg/docs/d_day_helmet_session_results_2026_04_28.md

오늘 commit: ~28건 land (anima-eeg fix + 새 paradigm + hexa-lang RFC)
배터리 fix 후: Berger gate 강제 → 모든 EEG metric 재검증

================================================================================
7. Sources
================================================================================

[vctec — 4×AA Battery Holder]
https://vctec.co.kr/product/4%C3%97aa-%EB%B0%B0%ED%84%B0%EB%A6%AC-%ED%99%80%EB%8D%94-%EC%8A%A4%EC%9C%84%EC%B9%98-dc%EC%9E%AD-%EC%BB%A4%EB%B2%84-4%C3%97aa-battery-holder-with-power-switch-dc21-jack/21244/

[vctec — 배럴잭 to JST 케이블]
https://vctec.co.kr/product/%EB%B0%B0%EB%9F%B4-%EC%A0%84%EC%9B%90%EC%9E%AD-to-2-pin-jst-%EC%BC%80%EC%9D%B4%EB%B8%94-barrel-jack-to-2-pin-jst/3047

[OpenBCI Cyton Specs]
https://docs.openbci.com/Cyton/CytonSpecs/

[OpenBCI Forum — Battery Pack for Cyton]
https://openbci.com/forum/index.php?p=/discussion/1330/battery-pack-for-cyton

[OpenBCI Forum — Battery setup / polarity]
https://openbci.com/forum/index.php?p=/discussion/2979/battery-setup-polarity

[OpenBCI Forum — Polarity reversal protection]
https://openbci.com/forum/index.php?p=/discussion/3877/questions-on-battery-charging-for-use-with-cyton-polarity-reversal-protection

[OpenBCI Forum — High capacity AA batteries]
https://openbci.com/forum/index.php?p=/discussion/2303/high-capacity-aa-batteries-in-the-cyton-board-and-associated-risks

[anima D-day session INDEX]
file:///Users/ghost/core/anima/anima-clm-eeg/docs/d_day_session_2026_04_28/INDEX.md

================================================================================
END OF GUIDE
================================================================================

