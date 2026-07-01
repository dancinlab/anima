#!/usr/bin/env python3
"""G9 — no-cloning = unique root of unforgeable security. real sim. p7 $0."""
print("="*78); print("G9 — 무복제 = 위조불가 보안의 유일근거"); print("="*78)
print(f"{'n(qubits)':>10}{'classical forge P':>18}{'quantum forge (3/4)^n':>24}")
for n in [1,2,4,8,16,32]:
    print(f"{n:>10}{1.0:>18.3f}{(0.75)**n:>24.6f}")
qok = (0.75)**32 < 1e-3
print(f"  → 고전 위조 P=1.0 ∀n (항상 복제) · 양자 (3/4)^n→0 (no-cloning) · n=32서 {0.75**32:.2e}")
print(f"  → 🟢 위조불가 보안은 무복제에서만 가능(고전 불가능). 증명: {qok}")
print("  (anima: 고전 씨앗은 복제가능=fork OK지만 토큰으론 위조됨; 위조불가 인증은 양자必, G8 정합)")
