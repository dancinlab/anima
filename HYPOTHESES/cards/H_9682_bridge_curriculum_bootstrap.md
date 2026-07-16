---
id: H_9682
title: BRIDGE-CURRICULUM bootstrap — sparse bridge demos inside natural replay
tier: PROPOSED (DIRECTIONAL design · lab-full · GPU cost-gated · ⚠️ repackaging risk · NOT a verdict)
frontier: g1-interface-addressable-wall
created: 2026-07-17
---

# H_9682 (R6) — 자연 replay 속 희소 다리 시연

**Origin.** `sidecar lab full` 2026-07-17 — **Sol §5**. DESIGN ONLY · DIRECTIONAL.

**Claim (one line).** The gap between synthetic injection (works) and natural CPT (fails)
may be the absence of **a few explicit cross-store correspondences the reader can follow** —
not the kind of information.

## Mechanism
H_9423 needed trunk **and** bridge **co-trained**; a frozen random trunk **failed**.
So instead of bolting a finished bridge on afterwards, attach synthetic correspondence to
**a small fraction of natural teacher atoms** and let the trunk **bootstrap** the bridge;
present the remaining atoms as natural sentences only.

## Minimal decisive experiment
```bash
anima-py corpus study-replay --transcript T.jsonl --corpus BASE.txt --out F \
  --bridge-demo-frac 0.10 --bridge-demo-split train_atoms.json \
  --heldout-atoms heldout_atoms.json --seed ${S}
```
10% of atoms get a store↔reader correspondence; **evaluation atoms never carry bridge
markup**.

## Frozen falsifier
- **held-out, no-demo atoms**: bootstrap − sham `≥ +0.20`
- 95% CI lower `> 0` **after excluding demo atoms**
- demo/value shuffle → floor
- the arm with `--bridge-demo-frac` removed → plain MAIN level

## Controls (≥2)
① correspondence value-shuffle ② equal-byte nonbinding delimiter control ③ plain MAIN
④ full XBIND positive ceiling.

## Cost · kill-list — ⚠️ SELF-FLAGGED HIGHEST REPACKAGING RISK
corpus + leak audit **$0**; 4-arm = **GPU (owner go)**.
> Sol: "가장 강한 재포장 위험. **demo atom만 맞으면 XBIND 암기의 재실행이므로 즉시 폐기**한다.
> 오직 **no-demo held-out atom 전이**가 있어야 새 각도다."
This clause is **binding**: transfer to no-demo held-out atoms is the ONLY thing that makes
this distinct from H_9267 (XBIND, already works · re-invention banned).
