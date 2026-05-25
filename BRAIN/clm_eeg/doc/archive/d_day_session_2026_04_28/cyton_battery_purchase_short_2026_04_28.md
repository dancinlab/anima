# OpenBCI Cyton 배터리 구매 셋트 — 2026-04-28
# anima EEG D-day session, vctec 추천

================================================================================
구매 항목 (vctec 한 곳에서 동시 주문)
================================================================================

[1] 4×AA Battery Holder + Switch + DC Jack + Cover
URL: https://vctec.co.kr/product/4%C3%97aa-%EB%B0%B0%ED%84%B0%EB%A6%AC-%ED%99%80%EB%8D%94-%EC%8A%A4%EC%9C%84%EC%B9%98-dc%EC%9E%AD-%EC%BB%A4%EB%B2%84-4%C3%97aa-battery-holder-with-power-switch-dc21-jack/21244/

특징:
- AA 4개 (1.5V × 4 = 6V 직렬)
- ON/OFF 스위치
- DC 2.1mm barrel jack 출력
- 커버 포함 (AA 빠짐 방지)


[2] 배럴 전원잭 to 2-pin JST 케이블 (Barrel Jack to 2-pin JST)
URL: https://vctec.co.kr/product/%EB%B0%B0%EB%9F%B4-%EC%A0%84%EC%9B%90%EC%9E%AD-to-2-pin-jst-%EC%BC%80%EC%9D%B4%EB%B8%94-barrel-jack-to-2-pin-jst/3047

특징:
- DC 2.1mm barrel jack 입력
- JST PH 2.0mm 2-pin 출력 (Cyton battery socket 호환)


[3] AA 알카라인 배터리 4개
권장: Duracell 또는 에너자이저 (마트/쿠팡, ~3,000원)
재충전 가능 옵션: Eneloop (~10,000원, 장기 사용 시 비용 절약)


================================================================================
예상 합계
================================================================================
[1] vctec 4×AA holder      : ~3,000-5,000원
[2] vctec barrel→JST cable : ~3,000원
[3] AA 4개 (Duracell)       : ~3,000원
                              ----------
TOTAL                       : ~9,000-11,000원


================================================================================
연결 절차 (도착 후)
================================================================================

[Step 1] AA 4개 holder 에 정상 방향으로 꽂기
  - holder 내부의 + / - 표기 따라

[Step 2] holder 와 barrel→JST 케이블 결합
  - holder DC barrel jack → cable barrel plug

[Step 3] Multimeter 검증 (CRITICAL — 보드 파괴 방지)
  - 다이얼: DC 20V 위치
  - 빨강 probe → "ΩVmA" 잭
  - 검정 probe → "COM" 잭
  - holder 스위치 ON
  - cable 출력 JST plug 측정:
    * 빨강 probe → JST 핀 1
    * 검정 probe → JST 핀 2
  - 결과:
    * +6.0V (또는 +5.5~+6.5) → 핀 1 = + ✓ Cyton 연결 안전
    * -6.0V (마이너스 부호 점등) → polarity 반대 ⚠️
      → cable wire swap 또는 다른 cable 시도

[Step 4] Cyton 연결
  - Cyton 전원 OFF (스위치 OFF 위치)
  - cable JST plug → Cyton battery socket
  - holder 스위치 ON
  - Cyton 스위치 PC 위치로

[Step 5] Smoke test
  - Cyton blue LED 점등 ✓
  - USB Dongle red LED 깜빡 ✓
  - Cyton 보드 따뜻함 X (정상)
  - 하나라도 fail → 즉시 disconnect + 점검

[Step 6] anima 검증
  cd /Users/ghost/core/anima
  hexa run anima-eeg/eeg_setup.hexa health \
    --check --port /dev/cu.usbserial-DP04WGIQ
  → 16/16 alive ✓

  hexa run anima-eeg/eeg_setup.hexa impedance_validate \
    --measure --port /dev/cu.usbserial-DP04WGIQ
  → 16/16 GREEN (헬멧 착용 시) ✓


================================================================================
안전 주의사항
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
    - Cyton 보드 reverse polarity protection 있음/없음 확실 X
    - multimeter 검증 후 연결 = 보장 100%

[e] AA 배터리 수명
    - 알카라인 4×AA ≈ 8-15시간 사용 가능
    - Eneloop 충전 ≈ 6-10시간 (재충전 가능)
    - 6V 미만 떨어지면 (예: 5.5V) 측정 불안정 → 새 배터리 교체


================================================================================
사용자 보유 멀티미터 (검증 완료)
================================================================================

이 멀티미터로 모든 검증 단계 가능:
- DC 전압 측정 범위: 200mV / 2V / 20V / 200V / 600V (±0.5%)
- 저항 측정 범위: 200 / 2K / 20K / 200K / 2M (±1%)
- 도통 체크: ✓
- 자동 극성 표시 ("-" 부호 점등)


================================================================================
추가 발견 (anima D-day 2026-04-28)
================================================================================

직전 모든 EEG 측정 결과 (Berger gate FAIL / LZ76 / γ/θ 모두 FALSIFIED) 는
Cyton battery dying = amplifier voltage drop = broadband noise 영향 가능성 높음.
새 power solution (위 셋트) 후 재측정 필요.

회로도 분석 결과 (anima/.../cyton_jst_polarity_analysis_2026_04_28.md):
- JST connector pin 2 = + (positive) → diode D9 → net RAW
- JST connector pin 3 = - (negative) → AGND
- 물리적 LEFT/RIGHT 매핑 INDETERMINATE (multimeter 검증 mandatory)
- Silkscreen + / - 표기 X


================================================================================
Sources
================================================================================

- vctec 4×AA Battery Holder
  https://vctec.co.kr/product/4%C3%97aa-%EB%B0%B0%ED%84%B0%EB%A6%AC-%ED%99%80%EB%8D%94-%EC%8A%A4%EC%9C%84%EC%B9%98-dc%EC%9E%AD-%EC%BB%A4%EB%B2%84-4%C3%97aa-battery-holder-with-power-switch-dc21-jack/21244/

- vctec 배럴잭 to JST 케이블
  https://vctec.co.kr/product/%EB%B0%B0%EB%9F%B4-%EC%A0%84%EC%9B%90%EC%9E%AD-to-2-pin-jst-%EC%BC%80%EC%9D%B4%EB%B8%94-barrel-jack-to-2-pin-jst/3047

- OpenBCI Cyton Specs
  https://docs.openbci.com/Cyton/CytonSpecs/

- OpenBCI Forum — Battery Pack for Cyton (4-AA holder spec)
  https://openbci.com/forum/index.php?p=/discussion/1330/battery-pack-for-cyton

- OpenBCI Forum — Battery setup / polarity
  https://openbci.com/forum/index.php?p=/discussion/2979/battery-setup-polarity

- anima session results
  /Users/ghost/core/anima/anima-clm-eeg/docs/d_day_session_2026_04_28/INDEX.md

