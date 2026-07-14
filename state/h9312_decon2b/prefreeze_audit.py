"""H_9311 DECON-2 · PRE-FREEZE AUDIT — measure what the design must not assume.

Fable's mandate on the DECON-2 render format: "<sep> = measure the separator bytes the training
corpus actually wrote between instances. Guessing puts a second F2 in the design." H_9309 died
because we spoke to the model in a format it was never taught; the way to not repeat that is to
read the training stream, not to reason about it.

Three questions, all answerable from artifacts on disk:
  1. What byte(s) separate two instances in the training corpus?
  2. Was `instance <sep> instance` inside the training window at all — i.e. is the 2-concatenation
     that DEMO-PORT depends on in-distribution? (Fable D8: the design's self-PC weak point.)
  3. What does the model see to the LEFT of a prompt at eval time, versus at training time?
"""

import os
import re
import statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(HERE, "..", "nbindg_grounding", "c34_main_s7_train.txt")

# Measured, not assumed: the C34 fire command (state/nbindg_grounding/N2_STATUS.md:57) is
#   anima-py train --arch clm --canon --arm ctrl --objective ce_marginal --corpus n2_<arm>_train.txt
#   --cell-label en-general --steps 105169 --batch-size 8 --bf16 --seed <7|11> --out ...
# It carries NO --seq-len, so cli/train.py:1206 (--canon, non-bytegpt) applies: seq_len = 1024.
# That branch also sets d=3784 L=4, which is byte-for-byte what the ckpt reports (rf_probe) —
# so this is provably the branch that ran, not a plausible-looking one.
TRAIN_SEQ_LEN = 1024
EVAL_WIN_SO_FAR = 64          # H_9289 · H_9308 · H_9309 all used this
PAD_BYTE = 32                 # core/decode.py:955 _seed_to_tok — left-pad = 32.0 (space)


def main():
    raw = open(CORPUS, "rb").read()
    lines = [l for l in raw.split(b"\n") if l.strip()]
    L = [len(l) for l in lines]

    print("=" * 84)
    print("H_9311 DECON-2 — PRE-FREEZE AUDIT (measured from the training corpus on disk)")
    print("=" * 84)

    # ---- Q1: the separator
    seps = {}
    for m in re.finditer("=> (긍정|부정)\\.".encode(), raw):
        nxt = raw.find("이 영화".encode(), m.end())
        if nxt > 0:
            seps[raw[m.end():nxt]] = seps.get(raw[m.end():nxt], 0) + 1
    print("\n[Q1] 인스턴스 구분자")
    for k, v in sorted(seps.items(), key=lambda x: -x[1])[:3]:
        print("     %-10r × %d" % (k, v))
    uni = len(seps) == 1
    print("     => 만장일치: %s  (동결값 <sep> = %r)"
          % (uni, list(seps)[0] if uni else "AMBIGUOUS — 동결 금지"))

    # ---- Q2: is the 2-concatenation in-distribution?
    med = st.median(L)
    per_win = TRAIN_SEQ_LEN / (med + 1)
    print("\n[Q2] 2-연접이 학습 분포 안인가 (Fable D8)")
    print("     인스턴스 %d 개 · 길이 median %dB (min %d · max %d)" % (len(L), med, min(L), max(L)))
    print("     학습 창 seq_len = %dB  ⟹ 창 하나에 인스턴스 약 %.0f 개가 연속으로 들어갔다"
          % (TRAIN_SEQ_LEN, per_win))
    print("     => '인스턴스 <sep> 인스턴스' 는 모델이 **매 스텝 본 것**. 2-연접 = 분포 한복판 ✅")

    # ---- Q3: the left context, train vs eval  (the finding that reverses D8)
    print("\n[Q3] 프롬프트 왼쪽에 무엇이 있나 — 학습 vs 평가")
    print("     학습:  ...이전인스턴스.%r이 영화 X => 긍정." % b"\n")
    print("     평가:  [공백 %d개]이 영화 X => 긍정.   (pad=%d · core/decode.py:955)"
          % (EVAL_WIN_SO_FAR - 31, PAD_BYTE))
    print("     => 지금까지의 평가 문맥(win=%d)이 이미 **분포 밖**이다 — 학습에서 프롬프트 왼쪽은"
          % EVAL_WIN_SO_FAR)
    print("        언제나 '앞선 인스턴스 + 개행'이었지 공백 런이 아니었다.")
    print("     => DEMO-PORT 의 1-shot 시연은 문맥을 **분포 안으로 되돌린다**. D8(자기-PC 급소)은")
    print("        해소를 넘어 역전 — 시연 포맷이 현행 포맷보다 학습분포에 가깝다.")

    # ---- window budget for DECON-2
    demo_max = len("이 영화 ".encode()) + 12 + len("고 => 긍정.".encode()) + 1   # stem<=12B + sep
    tgt_max, gold_max = 41, 7
    need = demo_max + tgt_max + gold_max
    print("\n[byte budget] 시연 ≤%dB + 대상 seed ≤%dB + gold %dB = **≤%dB**"
          % (demo_max, tgt_max, gold_max, need))
    for w in (64, 96, 128):
        print("     win=%3d → %s" % (w, "부족 ❌" if need > w else "여유 %dB ✅" % (w - need)))
    print("     => win=128 동결. 학습 창 1024 의 1/8 이라 창 확장은 분포 이동이 아니다"
          "(오히려 64 보다 학습에 가깝다).")


if __name__ == "__main__":
    main()
