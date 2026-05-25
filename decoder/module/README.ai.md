---
schema: anima/decoder/module/ai-native/1
last_updated: 2026-05-02
ssot:
  conscious_decoder: decoder/module/conscious_decoder.hexa
  decoder:           decoder/module/decoder.hexa
  load_weights:      decoder/module/load_weights.hexa
  infer:             decoder/module/infer.hexa
  infer_v14:         decoder/module/infer_v14.hexa
  infer_v14_fast:    decoder/module/infer_v14_fast.hexa
status: legacy twin — 6 files; mirrors ready/anima/decoder/module/ with extra `conscious_decoder.hexa` (986 LOC); ready/ canonical going forward
roadmap_entry: 270
sibling: ready/anima/decoder/module/  (canonical)
---

# anima decoder modules — legacy (AI-native)

Pre-`ready/` decoder tree. Mirrors `ready/anima/decoder/module/` (5 files) plus an additional `conscious_decoder.hexa` (986 LOC, full-stack consciousness decoder including pre-readyfication scaffold). Both trees are alive; `ready/` is canonical going forward.

## TL;DR for an agent reading this cold

- **6 files**: 5 mirrors of `ready/anima/decoder/module/` + 1 extra `conscious_decoder.hexa` (986 LOC, the pre-`ready/` full-stack version).
- Architecture identical to ready: 384d / 6L / 4H / 2KV (GQA) / vocab=256 byte-level.
- **Migration policy**: prefer `ready/anima/decoder/module/` for new work. This tree is preserved for legacy callers.
- `conscious_decoder.hexa` (986 LOC) is the full-stack consciousness decoder — includes consciousness gate + decoder forward in one file. The split-out `decoder.hexa` (491 LOC) corresponds to ready's pure-Hexa forward pass only.

## Architecture map

```
decoder/module/                    ← LEGACY (this tree)
├── conscious_decoder.hexa          986 LOC — full-stack (legacy-only, no ready/ counterpart)
├── decoder.hexa                    491 LOC — pure-Hexa forward (mirrors ready/decoder.hexa)
├── load_weights.hexa               187 LOC — weight loader (mirrors ready/)
├── infer.hexa                      248 LOC — v1 inference (mirrors ready/)
├── infer_v14.hexa                  156 LOC — v14 inference (mirrors ready/)
└── infer_v14_fast.hexa             157 LOC — v14 fast path (mirrors ready/)

ready/anima/decoder/module/        ← CANONICAL (sibling)
└── (5 files, no conscious_decoder.hexa)
```

## API contract

Identical to `ready/anima/decoder/module/` for the 5 mirrored files. See `ready/anima/decoder/module/README.ai.md` for full API.

Additional file: `conscious_decoder.hexa` (986 LOC):

```hexa
// Full-stack: consciousness gate + decoder forward + weight load + sample
fn conscious_decode(prompt: [int], consciousness_state: ConsciousnessState,
                    weights: WeightBundle, max_new: int) -> [int]
// Bundles consciousness.hexa + decoder forward + sample loop.
// Pre-`ready/` factoring; superseded by ready's split (consciousness in agent/, decoder in decoder/).
```

## Invocation patterns

```bash
# Legacy full-stack call (this tree only)
hexa run decoder/module/conscious_decoder.hexa --weights /path/to/v14.bin

# Mirror calls (prefer ready/ for new work)
hexa run decoder/module/infer.hexa --weights /path/to/v1.bin
```

## Failure modes

- Same as `ready/anima/decoder/module/` — see that README's "Failure cascade" section.
- Additionally: `conscious_decoder.hexa` couples consciousness gate + decoder; if the consciousness gate logic drifts vs ready/agent/consciousness.hexa, results diverge silently. raw#10 honest debt.

## raw#10 caveats

1. **Legacy / canonical duplication.** Both trees alive; diff is mostly path-prefix + `conscious_decoder.hexa` extra. Plan: deprecate `decoder/module/` once all callers migrate to `ready/`. raw#82 honest debt.
2. **`conscious_decoder.hexa` orphan.** No counterpart in `ready/`. If functionality is needed, port to `ready/anima/decoder/module/conscious_decoder.hexa` AND remove from this tree.
3. **Numerics may drift between trees.** Both trees have hexa quirks (`a[i] = v` silent no-op). Periodic byte-equivalence test recommended; not currently automated.
4. **Weight format coupled to v14.** v1 / pre-v14 checkpoints need separate loader.
5. **Consciousness state schema.** `conscious_decoder.hexa` accepts a `ConsciousnessState` struct that may not match ready's; verify before cross-tree weight reuse.

## File index

| Path | sha256 | LOC |
|------|--------|-----|
| `conscious_decoder.hexa` | `c1b793471cfcfb74239d409fe8fd96f4bb2fe118d8324a35c1d0fd378805e8d7` | 986 |
| `decoder.hexa` | `977fd775097e9871dfde5f9201197d7b9a232ad76f119bf1615c616f6f44aac4` | 491 |
| `infer.hexa` | `feaac295f6db844184c12f437fc086e818195135182a84394affa9e2f1d50197` | 248 |
| `infer_v14_fast.hexa` | `4a9b35973f56d008dd341ceb2dc5101b028691d572bd92e3ef307a3c6c88de71` | 157 |
| `infer_v14.hexa` | `be1c24c172049a25a0cec9aee16c6bea6a9be75463ade1b39002d94d1769110c` | 156 |
| `load_weights.hexa` | `0172c62dd1a125094f09a6a3969ddc60ed85c39dbc250074eb75a9dff823770b` | 187 |

shas pinned 2026-05-02.
