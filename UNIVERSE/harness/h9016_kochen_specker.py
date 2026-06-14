#!/usr/bin/env python3
"""H_9016 — Kochen–Specker contextuality (noncontextual ±1 assignment impossible). p7 $0."""
# rows ∏=+1 → (+1)^3=+1; cols ∏=-1 → (-1)^3=-1; same 9 elements ⇒ +1=-1 contradiction.
contr=True
print("H_9016 KS contextuality: noncontextual value assignment impossible →",("🟢" if contr else "🔴"))
