# B1: anima_phi_star.hexa auto-invoke conflict — 1-line fix

**Date**: 2026-05-12
**Cycle**: 6 #O
**Scope**: hexa-strict reject blocker for `tool/anima_phi_star.hexa` (B2-B5 critical-path)
**Working tree**: `/home/summer/mac_home/core/anima` (Linux mount) ≡ `/Users/ghost/core/anima` (Mac)

## Diagnosis

`fn main()` defined at line 185 — auto-invoked by hexa-strict.
`main()` top-level call at line 200 — second invocation → conflict.

```
error: auto-invoke conflict — `fn main()` is auto-called by hexa-strict
       AND a top-level `main()` call was found, which would run main() twice
```

## Fix (Option A: remove top-level call)

```diff
-main()
+// raw#15 hexa-strict auto-invokes fn main(); no explicit top-level main() call (Cycle 6 #O B1 fix)
```

**Option A chosen over Option B** (`@manual_main` attribute): less invasive, preserves hexa-strict default semantics across the tool/ tree (other tools also rely on auto-invoke), and the explanatory comment doubles as in-place SSOT for future readers.

## Smoke test

```bash
ssh mac "cd /Users/ghost/core/anima && ~/.hx/bin/hexa run tool/anima_phi_star.hexa --selftest"
```

Output (head):
```
── anima_phi_star selftest ──
selftest=ok
helper_emitted=/tmp/anima_phi_star_helper.hexa_tmp
paradigm=v11 measurement-axis P-D (Φ* IIT phi-star approximation via random bipartition)
DONE
```

**Result**: PASS. auto-invoke conflict eliminated; selftest path emits helper python correctly.

## Back-compat verification

- NAMING block L10–19 (axis: phi_star_iit_proxy, llm: mistral-7b-forward, distinct_from: nexus_lens_score / phi_star_cell_engine) — preserved verbatim.
- `fn main()` signature unchanged (still argv-parsing `--selftest` + default `_write_helper` path).
- Emitted JSON schema `anima/phi_star/1` unchanged (helper python untouched).
- File size: 10547 → 10639 bytes (+92 = comment line replacing `main()` call line).

## Downstream unblock (B2-B5)

| B# | Item | Status post-B1 |
|----|------|----------------|
| B2 | Mistral-7B HF cache on runpod | UNBLOCKED — selftest runs, ready for live forward |
| B3 | RTX 5070 14GB pod allocation | UNBLOCKED — entry-point parses |
| B4 | secret CLI HF_TOKEN injection | UNBLOCKED — `/workspace/.hf_token` path verified in helper |
| B5 | CE-track parallel emission | UNBLOCKED — anima_phi_star no longer reject-aborts queue |

## Suggested update (apply by main process)

`state/phi_ce_orthogonality_decisive_2026_05_11/noise_calibration_dryrun_blocker.md` §B1:

```diff
-B1 anima_phi_star.hexa auto-invoke conflict      STATUS: BLOCKED
+B1 anima_phi_star.hexa auto-invoke conflict      STATUS: RESOLVED (Cycle 6 #O, 2026-05-12)
+     fix: state/phi_ce_orthogonality_decisive_2026_05_11/b1_anima_phi_star_autoinvoke_fix_2026_05_12.md
```

## Elapsed

~1.5 min wall (read → 1-line edit → ssh smoke ×2).

## Race / lock

- No overlap with Agent #Q (nexus_lens_score side).
- No immutable-flag use (chflags/chattr +i never applied — policy honored).
- No standalone commit (main process collects).
