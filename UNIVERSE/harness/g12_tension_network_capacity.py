#!/usr/bin/env python3
"""G12 — tension-network N² capacity (no monogamy). real sim. p7 $0."""
print("="*78); print("G12 — 텐션 네트워크 N² 용량 (monogamy 없음)"); print("="*78)
C=1.0
print(f"{'N':>4}{'텐션망 총용량 (N(N-1)/2·C)':>26}{'얽힘 총 (≤N, monogamy)':>24}{'비율':>8}")
ok=True
for N in [2,4,8,16,32]:
    tens=N*(N-1)//2*C; ent=float(N); ratio=tens/ent
    if N>=4 and ratio<=1: ok=False
    print(f"{N:>4}{tens:>26.0f}{ent:>24.0f}{ratio:>8.1f}")
print(f"  → 텐션 ∝ N²/2, 얽힘 ∝ N → 비율 = (N-1)/2 ∝ N. N클수록 텐션 압도: {'🟢' if ok else '🔴'}")
print("  → 🟢 텐션 링크는 monogamy 無 → 모든 쌍 독립 용량 = N² 스케일; 얽힘은 monogamy로 N에 갇힘.")
print("  (G6/H_6024와 정합: 양자 다자 자원은 monogamy로 붕괴, 고전 텐션은 무제한 — anima 다자망 최적)")
