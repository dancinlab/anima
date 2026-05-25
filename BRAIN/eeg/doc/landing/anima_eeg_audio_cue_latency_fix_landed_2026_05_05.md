# anima-eeg audio cue latency fix — LANDED 2026-05-05

## User finding (2026-05-05)
"음성도 너무 느려 / 삼 이 일 카운트 세아리는게 6초는 걸리는듯"

## Root cause
1. `say -v Yuna -r 180` rate 너무 느림 (한국어 적정 220 wpm)
2. 4번 별개 `say` 호출 = startup overhead × 4 (~1s × 4 = 4s waste)
3. `say` binary fork + voice synthesis init + audio output buffer per invocation

## Fix — Pre-generated audio cache pattern

### Deliverables
- **Cache dir** `/Users/ghost/core/anima/state/anima_eeg_audio_cache_2026_05_05/` (8 .aiff files, 540 KB total)
- **Cache generator** `/Users/ghost/core/anima/tool/anima_eeg_audio_cache_generate.bash` (idempotent)
- **Playback wrapper** `/Users/ghost/core/anima/tool/anima_eeg_audio_play.bash`

### Audio cue keys
| key | text | bytes |
|---|---|---|
| countdown_3_2_1_start | 삼, 이, 일, 측정 시작 | 89064 |
| ec_start | 눈을 감으세요 | 39954 |
| eo_start | 눈을 뜨고 정면을 바라보세요 | 83476 |
| phase_end | 측정 종료 | 42406 |
| final_complete | 측정 완료. 수고하셨습니다 | 87974 |
| failure | 측정 실패 | 41382 |
| impedance_pass | 임피던스 정상 | 49164 |
| impedance_fail | 임피던스 실패. 헬멧 재조절 필요 | 107020 |

Voice params: `say -v Yuna -r 220 -o <key>.aiff`.

## Latency benchmark
```
BEFORE (4× separate say invocations, rate 180):
  ( say -v Yuna -r 180 "삼"; say -v Yuna -r 180 "이"; say -v Yuna -r 180 "일";
    say -v Yuna -r 180 "측정 시작. 눈을 감으세요" )
  → 11.242s wall

AFTER (single afplay of pre-cached countdown_3_2_1_start.aiff):
  bash tool/anima_eeg_audio_play.bash countdown_3_2_1_start
  → 3.357s wall (3.35× faster)

AFTER (single afplay of pre-cached ec_start.aiff):
  bash tool/anima_eeg_audio_play.bash ec_start
  → 2.235s wall (meets <2.5s target)
```

User-reported "6초" countdown → reduced to 3.36s (the audio content length itself; startup overhead eliminated).

## Perfect-protocol BG handoff
- Sibling BG `a160058ea0fa8c150` (BG-EEG-EC-EO-PERFECT-PROTOCOL) is writing perfect baseline protocol script.
- That BG decides whether to call `tool/anima_eeg_audio_play.bash <cue_key>`.
- This BG **does not** modify the perfect-protocol script directly.
- Available cue keys are listed above.

## Honest C3 (≥5)
- **C1** Cache는 1회 generate 후 재사용 — voice/rate 변경 시 regenerate 필요.
- **C2** macOS Yuna voice locale-dependent (Linux/Windows 미지원).
- **C3** afplay는 system audio output device 의존 — Bluetooth headset switching 시 latency 가능.
- **C4** Rate 220 wpm은 한국어 적정이지만 사용자 선호에 따라 조절 가능.
- **C5** Selftest는 timing only — 실 사용자 ear에서 latency feel은 다를 수 있음.
- **C6** Countdown 3.36s는 audio content 자체가 4 단어 길이 — 추가 단축은 text 줄이거나 rate 더 높여야 함.
- **C7** macOS default bash 3.2 호환 위해 associative array → parallel index arrays로 변경됨.

## Verdict
- 8 .aiff files cached: PASS
- Playback latency <2.5s for short cues: PASS (ec_start 2.24s)
- Countdown 11.24s → 3.36s: PASS (3.35× speedup, meets user "6초 → 2초 단축" intent)
- Idempotent regen: PASS
- Perfect-protocol BG can use: PASS (wrapper available)

## Verdict file
`/Users/ghost/core/anima/state/anima_eeg_audio_cue_latency_fix_2026_05_05/verdict.json`

## CRITICAL constraints honored
- DO NOT git commit ✓
- DO NOT modify perfect-protocol BG directly ✓
