# chip_isa_n6 → CANON absorb (LANDED 2026-05-04)

## Verdict
LANDED. Rank-3 (score 9) module from nexus audit absorbed into existing
`~/core/canon/domains/compute/chip-isa-n6/` as sibling `.hexa`
under the existing research-spec dir. Sister rank-1 `crystallography_n6`
landed sequentially first (38d66066), then chip_isa (e6141bce).

## Numbers
- module LoC: 445 (chip_isa_n6.hexa) + 72 (README) = 517 added
- consumer count: 0 active code consumers; 5 doc-only mentions in nexus
  (preserved as historical record)
- absorb path: `~/core/canon/domains/compute/chip-isa-n6/chip_isa_n6.hexa`

## Smoke
```
hexa run domains/compute/chip-isa-n6/chip_isa_n6.hexa --self-test
→ __CHIP_ISA_N6__ PASS ops=24 families=6 variants=4 word_bits=24
```
9 of 9 falsifier checks pass:
1. sigma*phi == n*tau == J2 == 24 identity
2. mnemonic count == 24 (=J2=2sigma)
3. 24/24 canonical roundtrip (r1, r2, r3)
4. 96/96 varied-register roundtrip
5. multi-line 6-instr program roundtrip
6. encode("gemm.m r1, r2, r3") = 004430
7. decode(004430) = "gemm.m r1, r2, r3"
8. unknown-mnemonic validator
9. reserved funct3 (110/111) validator

## Commits
- CANON main `e6141bce` — additive: chip_isa_n6.hexa + README sibling
- nexus `feat/qmirror-cli-programmatic-consumption` `29f26724` — deletion of
  modules/chip_isa_n6/

## 4 Caveats (raw#10)

1. **Destination predecessor co-existence.** The dir already contained
   `chip-isa-n6.md` (46KB research spec), `xn6_asm_examples.hexa` (asm
   examples), `xn6-isa-24-spec/`, `xn6-opcode-table/`. The new
   `chip_isa_n6.hexa` is the encoder/decoder layer — additive sibling, not
   a duplicate. README named `chip_isa_n6.README.md` (suffix form) to
   avoid conflict with any future top-level `README.md`.

2. **Tests not migrated; only `.pyc` remnants existed in nexus.** The
   `nexus/modules/chip_isa_n6/tests/` dir held only stale
   `__pycache__/test_chip_isa_n6.cpython-314-pytest-9.0.2.pyc` — the `.py`
   source had already been lost. Module exposes `--self-test` CLI which
   covers all 9 falsifier checks.

3. **Honest source-vs-impl gap (encoding derived, not spec-fixed).**
   Per the README §Honesty section: upstream `xn6_asm_examples.hexa`
   defines mnemonics via `@xn6` attrs but does NOT specify a concrete
   bit layout. The 24-bit packing here is **derived** to match J2=24 +
   n=6 funct3 use; treat as candidate encoding, not external spec.
   `imm` is 7 bits (not sigma-tau=8) — one bit consumed by funct3+variant
   to keep total == J2. Future 32-bit promotion would restore imm=8.

4. **Sister BG race + worktree state.** 5 stale locked worktrees in
   `CANON/.claude/worktrees/` (Apr 21–24) confused initial
   coordination. Sister BG (crystallography_n6 rank 1) staged its files
   to `/domains/physics/crystallography/` simultaneously and committed
   first (38d66066). Sequential commit order resolved cleanly because
   subtrees do not overlap (`/compute` vs `/physics`). In nexus, sister
   BG's deletes for `crystallography_n6/` were unstaged so they could
   commit themselves; my commit only touches `chip_isa_n6/`.

## Constraints honored
- raw#9/15/$0: pure additive extraction, zero infra cost, declarative
  artifacts only.
- raw#10: 4 explicit caveats above.

## Next
- Consumer refactor: not required (0 active code consumers).
- Doc cross-refs in nexus (5 files) preserved as historical record;
  nothing to update.
- No push performed (caller decides — n6-arch is on `main`, nexus on
  `feat/qmirror-cli-programmatic-consumption`).
