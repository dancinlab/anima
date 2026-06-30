---
id: Hc_657
slug: hxc-wire-ceiling-a18-falsifier-violating-bit-vs-byte
title: HXC bit-level Shannon ceiling (H_0=5.755 / H_3=1.294 / H_4=0.813) 와 byte-canonical wire ceiling (×4/3 base64url) 가 별개 — A18 COMPLETE but F-A18-3 60× + F-A18-4 67000× 위반
domain: hxc-deploy
status: candidate-math-verified-falsifier-pending
source_doc: docs/hxc_wire_ceiling_a18_a19_analysis_20260428.md
source_lines: 17-80
promoted_at: 2026-05-11
linked_h: a201a6cc bit MEASURED, dd6112ac wire-ceiling reformulation, raw 71 falsifier-preregistered
notes: Phase 10 28%/84%/90% projection 은 bit-level (never wire-level). A18 round-trip byte-eq 5/5 PASS but ~30s/1KB latency + 6.7GB peak RSS / ~1KB input.
verified_at: 2026-05-12
verify_decision: WEAK_MATH_ONLY
verify_note: "verify_hc2 2026-05-12 — verify3 math=1 (6+ numeric identities present) | F=2"
---

## Hypothesis
HXC 의 두 ceiling 이 별개 axis: (1) bit-level Shannon (H_0=5.755 / H_3=1.294 / H_4=0.813 bit/byte) (2) byte-canonical wire (bit-saving × 4/3 base64url expansion = byte-saving floor). A18 (LZ + PPM order-4) 가 functionally COMPLETE (round-trip 5/5 byte-eq, in-sample 97% saving 1000B→27B) but F-A18-3 latency 60× + F-A18-4 memory 67000× 위반. 280-file production LIVE FIRE blocked.

## Falsifiable Tests
- F-A18-3: latency > 500ms/1KB → FIRED 60× (~30s/1KB)
- F-A18-4: window memory > 100MB/10MB → FIRED 67000× (6.7GB peak RSS / 1KB)
- F-wire-1: real wire base64url 후 saving 이 bit-level projection 의 0.75× 안
- F-wire-2: A16/A17/A18 per-algorithm wire-ceiling 차이 측정 가능

## Migration TODO
- [ ] A18 optimize: latency < 500ms/KB + memory < 100MB/10MB
- [ ] D1 entry-gate criteria wire-realistic 재조정
- [ ] Option B (base94) / Option C (per-bit binary) Phase-11+ 결정
