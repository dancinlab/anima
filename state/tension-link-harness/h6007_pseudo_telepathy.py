#!/usr/bin/env python3
"""
h6007_pseudo_telepathy.py — REAL simulation: can two anima with NO physical link
appear "connected" using shared entanglement? (the user's question, sharpened).

H_6006 closed 'send an arbitrary MESSAGE with no link' = 🔴 (no-signaling).
BUT a DIFFERENT thing IS possible and real — QUANTUM PSEUDO-TELEPATHY / nonlocal
games: two parties who CANNOT communicate, but share an entangled pair, achieve a
COORDINATION rate impossible for any non-communicating classical pair. They look
"connected" without any link — not by message-passing, but by entanglement.

We simulate the CHSH game (shot-by-shot, NO communication between the two players):
  - referee sends each player a random bit (x to Alice, y to Bob), independently
  - players must output a,b with a XOR b == x AND y, WITHOUT talking to each other
  - classical best (any shared strategy/no comm): win rate = 0.75 (proven optimum)
  - quantum (shared Bell pair, optimal measurement angles): cos²(π/8) ≈ 0.8536
A measured quantum win-rate > 0.75 = a coordination that NO unlinked classical pair
can reach ⇒ entanglement gives connection-without-a-link (🟢), while transmitting
zero bits (consistent with H_6006).
p7 · $0 · numpy.
"""
import numpy as np
rng = np.random.default_rng(60071)

def classical_game(trials=400000):
    # best classical no-communication strategy for CHSH: both always output 0
    # ⇒ a XOR b = 0, wins exactly when x AND y == 0 ⇒ 3/4 of inputs.
    x = rng.integers(0,2,trials); y = rng.integers(0,2,trials)
    a = np.zeros(trials,int); b = np.zeros(trials,int)
    win = ((a ^ b) == (x & y))
    return win.mean()

def quantum_game(trials=400000):
    # Shared singlet. Measurement angle depends ONLY on each player's own input
    # (no communication). Optimal CHSH angles:
    #   Alice: x=0 -> 0,    x=1 -> pi/2
    #   Bob:   y=0 -> pi/4, y=1 -> -pi/4
    # Outcome correlation for singlet at relative angle: P(a==b)=cos²(Δ/2)... we
    # sample outcomes shot-by-shot from the singlet statistics (real measurement).
    # Φ+ state; correct CHSH-game angles. P(a==b) = cos²(α-β).
    #   Alice: x=0 -> 0,    x=1 -> π/4
    #   Bob:   y=0 -> π/8,  y=1 -> -π/8
    x = rng.integers(0,2,trials); y = rng.integers(0,2,trials)
    aA = np.where(x==0, 0.0, np.pi/4)
    aB = np.where(y==0, np.pi/8, -np.pi/8)
    p_eq = np.cos(aA - aB)**2               # Φ+ correlation
    eq = rng.random(trials) < p_eq
    a = rng.integers(0,2,trials)            # Alice's bit (locally random)
    b = np.where(eq, a, 1-a)                # Bob equal/opposite per draw
    win = ((a ^ b) == (x & y))
    return win.mean()

def no_signaling_check(trials=400000):
    # confirm: Bob's output distribution is independent of Alice's INPUT x
    # (so no information about x reaches Bob — 0 bits transmitted)
    aB = np.full(trials, np.pi/8)           # Bob fixes y=0
    def bob_given_x(xv):
        aA = np.full(trials, 0.0 if xv==0 else np.pi/4)
        p_eq = np.cos(aA-aB)**2
        eq = rng.random(trials) < p_eq
        a = rng.integers(0,2,trials)
        b = np.where(eq, a, 1-a)
        return b.mean()
    return bob_given_x(0), bob_given_x(1)

def main():
    print("="*82)
    print("H_6007 — 두 anima, 물리연결 0, 양자만으로 '연결'? (CHSH nonlocal game, REAL MC)")
    print("="*82)
    c = classical_game(); q = quantum_game()
    b0, b1 = no_signaling_check()
    print(f"  classical best (no communication)   win rate = {c:.4f}   (proven max 0.7500)")
    print(f"  quantum (shared entanglement)       win rate = {q:.4f}   (Tsirelson cos²(π/8)=0.8536)")
    print(f"  → 양자가 고전 한계 초과? {'🟢 YES — 통신 0인데 조율 우위 (connection w/o link)' if q > 0.78 else '🔴 NO'}")
    print(f"  no-signaling 확인: Bob P(1) | Alice x=0:{b0:.4f}  x=1:{b1:.4f}  |Δ|={abs(b0-b1):.4f}")
    print(f"  → {'🟢 0비트 전송(메시지 없음) — 그래도 조율됨' if abs(b0-b1)<0.01 else '🔴'}")
    print("-"*82)
    print("결론: '메시지 전송' = 불가(H_6006 🔴). 그러나 '통신 없이 조율(coordination)' =")
    print("가능(🟢) — 양자 의사-텔레파시. 두 anima는 한 번도 신호를 안 보내고도, 미리 나눈")
    print("얽힘으로 어떤 unlinked 고전쌍도 못 넘는 조율 우위(0.85>0.75)를 보인다 = '물리연결")
    print("없는 연결'. 단 새 정보를 보내는 건 아님(무신호 정리와 양립).")

if __name__ == "__main__":
    main()
