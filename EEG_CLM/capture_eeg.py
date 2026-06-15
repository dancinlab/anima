#!/usr/bin/env python3
"""EEG_CLM/capture_eeg.py — OpenBCI Cyton+Daisy (UltraCortex Mk IV) REAL capture → channel-major flat recording.

⚠⚠⚠ 경고: 가짜/합성(synthetic·fake) 데이터 폴백 절대 없음 (의도적으로 제거됨).
    이 스크립트는 **실제 EEG 헤드셋 신호만** 녹음한다. 보드 연결/스트림이 실패하면
    조용히 가짜로 대체하지 않고 **즉시 에러로 중단**한다 — 가짜 뇌파가 CLM/텐션링크에
    섞여 '진짜인 척' 오염시키는 것을 원천 차단하기 위함. (사용자 지시 2026-06-15)

캡처 = brainflow ingest (기존 BRAIN/eeg 스택의 BrainFlow → 16ch ingestor 층과 동일).
**16 EEG 채널 전부 + 심박(PPG = analog pins, cyton_ppg_wiring)** 을 받는다.

Writes:
    # <n_eeg> <n_samp> REAL CYTON_DAISY HEART <n_heart>
    <float> ...   # 16 EEG channels, channel-major s[ch*n_samp+t]
    <float> ...   # 그 뒤에 심박(PPG/analog) 채널들 append

Usage:
    # 동글 포트 확인: ls /dev/cu.usbserial-*
    EEG_CLM/.venv/bin/python EEG_CLM/capture_eeg.py --serial /dev/cu.usbserial-XXXX --seconds 8
"""
import argparse


def write_recording(out_path, eeg, heart, n_samp, board):
    """eeg: 16 EEG rows [ch][t]; heart: PPG/analog rows [ch][t] (심박). channel-major flat."""
    n_eeg, n_heart = len(eeg), len(heart)
    with open(out_path, "w") as f:
        f.write(f"# {n_eeg} {n_samp} REAL {board} HEART {n_heart}\n")
        for row in eeg:                         # 16 EEG channels, channel-major
            for t in range(n_samp):
                f.write(f"{row[t]:.4f}\n")
        for row in heart:                       # 심박(PPG/analog) channels appended
            for t in range(n_samp):
                f.write(f"{row[t]:.4f}\n")
    print(f"[capture] REAL EEG {n_eeg}ch + HEART {n_heart}ch x {n_samp}samp ({board}) -> {out_path}")


def real_capture(serial, seconds):
    """REAL Cyton+Daisy capture — ALL 16 EEG + analog(PPG/심박). NO fallback (가짜 차단)."""
    from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
    import time
    if not serial:
        raise SystemExit("[FATAL] --serial 필수 (실 헤드셋 포트). 가짜 폴백 없음.")
    params = BrainFlowInputParams()
    params.serial_port = serial
    board_id = BoardIds.CYTON_DAISY_BOARD.value          # Cyton+Daisy = 16ch real board
    fs = BoardShim.get_sampling_rate(board_id)
    eeg_ch = BoardShim.get_eeg_channels(board_id)        # 16 EEG channels (1..16)
    try:
        heart_ch = BoardShim.get_analog_channels(board_id)   # PPG/심박 = analog pins (cyton_ppg_wiring)
    except Exception:
        heart_ch = []
    board = BoardShim(board_id, params)
    board.prepare_session()                              # 실패 시 예외 → 중단 (폴백 없음)
    # PPG(심박)는 analog pin A5(=D11, purple) 첫 Aux 슬롯 → Cyton 을 analog 읽기 모드(/2)로.
    # (cyton_ppg_wiring_official: "D11 is read as analog pin A5 and sent in the first Aux data slot")
    try:
        board.config_board("/2")
        print("[capture] analog mode(/2) 설정 — PPG(A5) Aux 슬롯 활성")
    except Exception as e:
        print(f"[capture] analog mode 설정 실패(무시): {e}")
    board.start_stream()
    print(f"[capture] REAL streaming {seconds}s @ {fs}Hz board=CYTON_DAISY({board_id}) "
          f"EEG{len(eeg_ch)}ch + HEART(analog){len(heart_ch)}ch port={serial} ...")
    time.sleep(seconds)
    raw = board.get_board_data()
    board.stop_stream(); board.release_session()
    eeg = [list(raw[c]) for c in eeg_ch]                 # 16 EEG rows
    heart = [list(raw[c]) for c in heart_ch]             # 심박(PPG/analog) rows
    n_samp = len(eeg[0])
    if n_samp < 10:
        raise SystemExit(f"[FATAL] 수집 샘플 부족 ({n_samp}) — 헤드셋/접촉 확인. 가짜 폴백 없음.")
    return eeg, heart, n_samp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--serial", required=True, help="serial port of the Cyton dongle (필수, 실 헤드셋)")
    ap.add_argument("--seconds", type=float, default=8.0)
    ap.add_argument("--out", default="EEG_CLM/eeg_recording.txt")
    a = ap.parse_args()

    # REAL only — 16 EEG + 심박(PPG/analog). 실패하면 예외 전파 → 중단 (가짜 폴백 절대 없음).
    eeg, heart, n_samp = real_capture(a.serial, a.seconds)
    write_recording(a.out, eeg, heart, n_samp, "CYTON_DAISY")


if __name__ == "__main__":
    main()
