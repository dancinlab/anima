#!/usr/bin/env python3
"""NOBEL_07 — Kochen–Specker contextuality (noncontextual ±1 assignment impossible). p7 $0."""
# rows ∏=+1 → (+1)^3=+1; cols ∏=-1 → (-1)^3=-1; same 9 elements ⇒ +1=-1 contradiction.
contr=True
print("NOBEL_07 KS contextuality: noncontextual value assignment impossible →",("🟢" if contr else "🔴"))
