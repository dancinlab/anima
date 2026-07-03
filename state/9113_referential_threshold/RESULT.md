# H_9113 -- Referential-efficacy THRESHOLD resolution -- RESULT

**VERDICT: 🟠 PARTIAL — b50_real=3.20 bytes but real≈shuffle at some t (coupling floor under extreme truncation)**

- coupling-strength scalar b50_real = 3.2 bytes-of-clue at 50% decode (K=14, near-synonym distractors)
- real>shuffle at EVERY t: False · mean_acc_real=0.524 · mean_acc_shuffle=0.036
- oracle=claude-fable-5 (theta outside anima closure) - emits FROZEN engine-native (H_9111) - tier=DIRECTIONAL-on-external-oracle

## real arm (acc vs clue bytes, K=14)
  t=8B: acc=1.000
  t=6B: acc=0.857
  t=4B: acc=0.786
  t=3B: acc=0.429
  t=2B: acc=0.000
  t=1B: acc=0.071
## shuffle arm
  t=8B: acc=0.000
  t=6B: acc=0.000
  t=4B: acc=0.000
  t=3B: acc=0.143
  t=2B: acc=0.000
  t=1B: acc=0.071

chance (K=14) = 0.071. H_9112 established acc=0.857 at t=8B (this sweep starts there and pushes down).
