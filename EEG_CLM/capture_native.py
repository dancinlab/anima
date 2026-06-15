#!/usr/bin/env python3
"""EEG_CLM/capture_native.py — OpenBCI Cyton(+Daisy) NATIVE serial capture (brainflow 우회).

brainflow Cyton+Daisy 연속세션 prepare hang 을 우회 — OpenBCI 공식 serial 프로토콜로 직접:
  115200 baud · 's' stop · 'b' start · 33-byte binary packet (0xA0 head … 0xC0~ footer)
  packet: [0xA0][sample#][8ch × 3byte int24 BE][6byte aux][footer]
가짜 폴백 없음 — 패킷 안 오면 즉시 에러. 실 EEG 전용.

출력 (build/analyzer 호환):
    # <n_ch> <n_samp> REAL NATIVE_CYTON
    <float> ...   # 채널-major s[ch*n_samp+t], int24 raw count
사용: EEG_CLM/.venv/bin/python EEG_CLM/capture_native.py --serial /dev/cu.usbserial-XXXX --seconds 60
"""
import argparse, serial, time, sys

def i24(b0, b1, b2):
    v = (b0 << 16) | (b1 << 8) | b2
    if v & 0x800000: v -= 0x1000000
    return v

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--serial", required=True)
    ap.add_argument("--seconds", type=float, default=60.0)
    ap.add_argument("--out", default="EEG_CLM/eeg_music.txt")
    ap.add_argument("--fs", type=float, default=125.0)   # Cyton 250, Cyton+Daisy 125
    a = ap.parse_args()

    s = serial.Serial(a.serial, 115200, timeout=1)
    time.sleep(1.0)
    s.write(b's'); time.sleep(0.3)          # stop any stream
    s.reset_input_buffer()
    s.write(b'b'); time.sleep(0.2)          # start binary stream
    print(f"[native] streaming {a.seconds}s @ ~{a.fs}Hz from {a.serial} ...", flush=True)

    # Cyton+Daisy 16ch: sample# 짝수=Cyton(ch1-8), 홀수=Daisy(ch9-16) 디인터리브 → 16ch @125Hz
    NCH = 16
    b_even = [[] for _ in range(8)]          # ch0-7 (Cyton)
    b_odd = [[] for _ in range(8)]           # ch8-15 (Daisy)
    t_end = time.time() + a.seconds
    buf = bytearray()
    got = 0
    while time.time() < t_end:
        data = s.read(512)
        if data: buf.extend(data)
        while len(buf) >= 33:
            if buf[0] != 0xA0:
                del buf[0]; continue
            pkt = buf[:33]
            if pkt[32] < 0xC0:               # footer 검증 (0xC0~0xCF)
                del buf[0]; continue
            sn = pkt[1]
            tgt = b_even if (sn % 2 == 0) else b_odd
            for c in range(8):
                off = 2 + c*3
                tgt[c].append(i24(pkt[off], pkt[off+1], pkt[off+2]))
            got += 1
            del buf[:33]
    s.write(b's'); s.close()
    # 16ch = even(ch0-7) + odd(ch8-15), 짧은쪽 길이로 정렬
    n_samp = min(min(len(c) for c in b_even), min(len(c) for c in b_odd)) if b_even[0] and b_odd[0] else 0
    chans = [b_even[c][:n_samp] for c in range(8)] + [b_odd[c][:n_samp] for c in range(8)]
    if n_samp < 50:
        raise SystemExit(f"[FATAL] 패킷 부족 ({n_samp}) — 보드/접촉 확인. 가짜 폴백 없음.")
    fs_meas = n_samp / a.seconds             # 채널 실측 sample rate (16ch 디인터리브 후 ≈125Hz)
    with open(a.out, "w") as f:
        f.write(f"# {NCH} {n_samp} REAL NATIVE_CYTON FS {fs_meas:.2f}\n")
        for c in range(NCH):
            for t in range(n_samp):
                f.write(f"{float(chans[c][t]):.1f}\n")
    print(f"[native] REAL {NCH}ch x {n_samp}samp ({got} packets) -> {a.out}", flush=True)

if __name__ == "__main__":
    main()
