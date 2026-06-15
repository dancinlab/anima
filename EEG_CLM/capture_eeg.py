#!/usr/bin/env python3
"""EEG_CLM/capture_eeg.py — OpenBCI Cyton+Daisy (UltraCortex Mk IV) REAL capture → channel-major flat recording.

⚠⚠⚠ 경고: 가짜/합성(synthetic·fake) 데이터 폴백 절대 없음 (의도적으로 제거됨).
    이 스크립트는 **실제 EEG 헤드셋 신호만** 녹음한다. 보드 연결/스트림이 실패하면
    조용히 가짜로 대체하지 않고 **즉시 에러로 중단**한다 — 가짜 뇌파가 CLM/텐션링크에
    섞여 '진짜인 척' 오염시키는 것을 원천 차단하기 위함. (사용자 지시 2026-06-15)
    합성 데이터로 파이프라인만 점검하려면 capture 가 아니라 별도 도구로 명시적으로 하라.

Writes the format build_eeg_clm.hexa / tension_link.hexa expect:
    # n_ch n_samp REAL <board>
    <float>            # channel-major: s[ch*n_samp + t]
    ...

Usage:
    # 동글 포트 확인: ls /dev/cu.usbserial-*
    python3 EEG_CLM/capture_eeg.py --serial /dev/cu.usbserial-XXXX --seconds 8 --channels 0,1,2,3
"""
import argparse, sys


def write_recording(out_path, data, ch_idx, n_samp, board):
    """data: list-of-lists [channel][t]; ch_idx: selected channel indices."""
    n_ch = len(ch_idx)
    with open(out_path, "w") as f:
        f.write(f"# {n_ch} {n_samp} REAL {board}\n")
        for ci in ch_idx:                       # channel-major: all of ch0, then ch1, ...
            row = data[ci]
            for t in range(n_samp):
                f.write(f"{row[t]:.4f}\n")
    print(f"[capture] REAL {n_ch}ch x {n_samp}samp ({board}) -> {out_path}")


def real_capture(serial, seconds):
    """REAL Cyton+Daisy capture. NO fallback — raises on any failure (가짜 차단)."""
    from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
    import time
    if not serial:
        raise SystemExit("[FATAL] --serial 필수 (실 헤드셋 포트). 가짜 폴백 없음.")
    params = BrainFlowInputParams()
    params.serial_port = serial
    board_id = BoardIds.CYTON_DAISY_BOARD.value          # Cyton+Daisy = 16ch real board
    fs = BoardShim.get_sampling_rate(board_id)
    eeg_ch = BoardShim.get_eeg_channels(board_id)
    board = BoardShim(board_id, params)
    board.prepare_session()                              # 실패 시 여기서 예외 → 중단 (폴백 없음)
    board.start_stream()
    print(f"[capture] REAL streaming {seconds}s @ {fs}Hz board=CYTON_DAISY({board_id}) port={serial} ...")
    time.sleep(seconds)
    raw = board.get_board_data()
    board.stop_stream(); board.release_session()
    data = [list(raw[c]) for c in eeg_ch]                # [channel][t]
    n_samp = len(data[0])
    if n_samp < 10:
        raise SystemExit(f"[FATAL] 수집 샘플 부족 ({n_samp}) — 헤드셋/접촉 확인. 가짜 폴백 없음.")
    return data, n_samp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--serial", required=True, help="serial port of the Cyton dongle (필수, 실 헤드셋)")
    ap.add_argument("--seconds", type=float, default=8.0)
    ap.add_argument("--channels", default="0,1,2,3", help="comma channel indices (<=8)")
    ap.add_argument("--out", default="EEG_CLM/eeg_recording.txt")
    a = ap.parse_args()
    ch_idx = [int(x) for x in a.channels.split(",")]
    if len(ch_idx) > 8:
        print("[warn] >8 channels → 2^n state alphabet too large; truncating to 8")
        ch_idx = ch_idx[:8]

    # REAL only. 실패하면 예외 전파 → 중단 (가짜 폴백 절대 없음).
    data, n_samp = real_capture(a.serial, a.seconds)
    write_recording(a.out, data, ch_idx, n_samp, "CYTON_DAISY")


if __name__ == "__main__":
    main()
