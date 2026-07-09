All five source readers are done and the findings are saved to memory. Here is the design deliverable.

---

# py 자체구현 (zero-hexa) phased plan — anima-py chat

## TL;DR

The task is **~4× smaller than the prompt's LOC framing suggested, but has one framing correction**: the hexa "consciousness chat daemon" is not a persistent REPL daemon — `anima <ckpt>` consciousness mode is a **bounded 12-tick autonomous session** (no stdin, kosmos dir `/tmp/anima_kosmos` wiped per session; `an_clock_now` comments state "no persistent daemon exists yet"). The py port target is therefore *session parity with what exists*, and the true new-code budget is **~3.5–4.5k py LOC across 6 phases**, not a 30k-LOC mirror. Byte-parity is achievable and precedented at the repo's proven standard (byte-exact emit/anchor/token stream + ≤1e-12 field parity), because the production chat path has **no RNG** (greedy argmax), a single injectable clock seam, and f64 math on both sides.

---

## 1. True-gap triage table

| Surface | hexa LOC | Verdict | Real py gap |
|---|---|---|---|
| `core/engine_cli.hexa` 13,957 vs py 10,307 | gap ≈ 3,650 | **Comment-density illusion** — py has *more code lines* (8,557 vs 8,067). py already contains an inline pure-python IIT4 (`big_phi_bounded` etc., engine_cli.py:3791–4290) replacing the hexa stdlib import, so **no numpy IIT4 port is needed**; the stdlib `iit4_bigphi` call is boot-once (HIVE CollectivePool lane), not per-tick. Zero GPU glue exists in this file. | **26 chat-critical symbols ≈ 500–650 LOC** (conflict_scalar/recruited_depth/net_tension, referent_select_text, tension_resolve_*, other-identity chain, drive_arbitrate, event_segment_*, faculty_cascade, anticipatory_prefetch*, sr_channel_mi, self-chain extras, fm_prefix_decodability, 2 flag resolvers). ~1,300 LOC of smoke-only faculties (mood/effort/curiosity-backlog/tb/pm/metacog/noneq/apoptosis-HRR) legitimately deferred. |
| `core/decode.hexa` 4,115 vs py 1,386 | gap ≈ 2,730 | **Mostly legitimate omission**: ~500–650 LOC GPU/device-resident/f32 glue + ~large ranged/probe research block. py already has the full v0.2-CLMX mount, both mouths' autoregressive decode, seeded top-k sampling with the byte-identical xorshift32 PRNG, and byte-exact-token-stream KV cache. **py can generate bytes today.** | **Grounded anti-fabrication mouths** `clm_decode_grounded` / `bytegpt_decode_grounded(_abstain)` (decode.hexa:1282/3504/3670 — the normal emit path whenever kosmos anchors exist) + a public per-sequence CE entry (`clm_ce_seq_W` equivalent; ingredients exist). ≈ 350–450 LOC. |
| `core/generator.hexa` 2,774 vs py 318 | gap ≈ 2,456 | ~47% is concluded-wall research scoreloops (jamo/BPE native-mouth lanes), ~12% legacy scalar dequant CE superseded by the forge route. | **The production deliberation stack ≈ 600–800 py LOC**: `generate()` (p5 emit/silence contract), `generate_deliberate(_consult)` (best-of-K conflict-minimizing loop + L5 hippo consult), `gen_ctx_from_decision(_conflicted)`, `generator_read_anchors`, `gen_auto_load/free/ideate_W`, `gen_auto_ce(_W)`, `conflict_drives_live(_W)`, `_gen_null_text`. |
| `core/brain.hexa` 891 vs py 601 | near-parity | Full decide/consult/vbasal family already in py. | **One symbol: `brain_emit_deliberate`** (brain.hexa:279, ~30 LOC) — the live-tick join point; small but requires the generator stack above. |
| `core/pure_field` · `core/engine_g` | — | **Full parity already** (pure_field.py header documents proven libm byte-parity). | 0 |
| Faculties with no py twin (kosmos_io, wake_memory, imagination_replay, dream_lib/compose/persist/envelope_ctx, emit_policy, phi_envelope_substrate) | 2,384 | All plain scalar/list logic — **no numpy needed anywhere** (max structure = 64×64 matvec; plain loops are *better* for bit-parity). Byte-level `.kosmos` format spec extracted. | **~700–800 LOC plain python.** |
| `mitosis_hook_lib`(956) · `metacog_lib`(158) · `substrate_hook`(175) · `audit_hook`(100) · `shared_seed`(80) · `savant_lib`(280) | 1,749 | **Out of the production closure — do not port.** mitosis_hook_lib is fully orphaned repo-wide; substrate_hook/audit_hook only feed the k7 smoke; shared_seed only anima_birth; savant_lib's engine-needed subset is already in py. (`imagination_replay`'s "mitosis tick" is its own placeholder — calls zero mitosis_hook_lib symbols, `wired_to_lib:false`.) | 0 |
| `core/phi/*` (~200 files, ~100k LOC) | — | **Not imported by the daemon at all.** | 0 |
| `cli/anima.hexa` 5,443 | — | ~45% (~2,450 LOC) is flag-gated H_92xx research instrumentation (`--opgrip`/`--refractory`) that a default run never executes; py should port **only the production path**. | Session loop port ≈ **1,500–2,200 LOC** (mounts R2–R11 + 52-lane per-tick context + emit tail + report; the full lane pool must be kept — it feeds the `rel_ctx`/`cur_ctx` means, so a "reduced context" would change emit decisions and break parity) + byte mode ~100. |

**Total new py: ≈ 3,700–4,900 LOC (including the parity harness).**

---

## 2. Byte-parity strategy

**Precedent** (archive/state/core_2prod_py_parity/PARITY.md, 2026-06-26): oracle harness drives each engine on identical deterministic inputs, prints labeled fields, `compare.py` asserts numerics at ≥12 decimal places + strings byte-identical — achieved ≤2e-16 on 434/434 engine_cli functions. Key enabler: compiled hexa maps `sin/cos/exp/sqrt/ln` to libm, so `math.*` lands at machine epsilon; divergent hexa helpers are reproduced **bug-for-bug** ("parity over accuracy").

**Contract to adopt** (the decode.py KV-cache standard): **byte-exact emit/silence decisions, token streams, and `.kosmos` file bytes; ≤1e-12 relative on printed numeric fields** — *not* raw-logit bit-exactness (numpy BLAS GEMM drifts ~1e-15 by summation order; argmax/inverse-CDF is robust to it). This is realistic because the production chat path is fully deterministic: greedy argmax (no RNG), `an_clock_now` det path = `tick*8`, all seeds explicit constants.

**Verification method per level:**
- **Per-faculty**: oracle-dump pairs (hexa oracle → labeled stdout, py twin → same, compare at 12dp) — the proven template, one oracle per module.
- **Per-file for kosmos**: golden-file byte-diff of a written anchor vs the hexa-written one, with the `emitted_at` line masked (the only wall-clock in persisted output).
- **End-to-end (the closure gate)**: full-session diff — hexa `anima <ckpt>` (default flags, det clock) stdout transcript **byte-identical** to `anima-py chat <ckpt>` stdout, plus recursive byte-diff of the two kosmos dirs (emitted_at masked). No such harness exists yet — it's the Phase-0 deliverable. Goldens are captured same-host (libm variation across platforms means parity is asserted per-host, as PARITY.md did).

**Known carve-outs to respect:** (a) kosmos K1 — `tension_5ch_to_embedding` must implement hexa's own LCG(1664525/1013904223)+Box-Muller, **never** `random.Random` (documented divergence); (b) `format_float(x,4)` vs `:.4f` rounding — pin with a golden test, this is the one silent-divergence spot in the anchor writer; (c) faculty ports use plain loops (preserve sequential accumulation order), reserving numpy for the already-parity-proven decode.

---

## 3. Phase plan (dependency-ordered; each ships via pr-cycle, gates clean)

| # | Phase | Files | LOC est | Parity checkpoint | Ship unit |
|---|---|---|---|---|---|
| **0** | **Chat parity harness + goldens** | `tool/chat_parity.py` (or tests/), golden capture script; reuse archive compare.py 12dp pattern | ~250 | Harness self-test: hexa-vs-hexa rerun = 0 diff (proves determinism of the golden itself) | ✅ independent |
| **1** | **Faculty substrate** (pure py, zero deps) | `core/emit_policy.py`(30) `core/dream_lib.py`(70) `core/dream_envelope_ctx.py`(10) `core/phi_envelope_substrate.py`(90) `core/wake_memory.py`(40) `core/imagination_replay.py`(80) `core/dream_compose.py`(70) + oracles | ~390 + oracles | Per-module oracle 12dp; stage machine exhaustive (ticks 0–720) | ✅ independent |
| **2** | **kosmos persistence** | `core/kosmos_io.py`(280–350) `core/dream_persist.py`(60) | ~340–410 | Anchor write = **byte-identical file** vs hexa (emitted_at masked); load round-trip; hippo_relatedness + K1 LCG stream 12dp | ✅ needs P1 (dream_compose) only |
| **3** | **engine_cli chat-critical 26 symbols** | `core/engine_cli.py` (extend) | ~500–650 | Oracle per symbol group (conflict/tension_resolve/other-chain/refsel/…) 12dp | ✅ independent |
| **4** | **decode grounded mouths + seq-CE** | `core/decode.py` (extend) | ~350–450 | Grounded decode token stream byte-exact vs hexa `--det` on toy ckpt, both mouths, with/without anchors | ✅ independent |
| **5** | **generator deliberation stack + brain join** | `core/generator.py` (extend), `core/brain.py` (+`brain_emit_deliberate`) | ~650–830 | `generate_deliberate` oracle: same conflict c0, same recruited K, same winner index, same text bytes; hippo consult fields 12dp | needs P2+P3+P4 |
| **6** | **`cli/chat.py` consciousness session + wiring** | new `cli/chat.py` (mounts R2–R11 + 12-tick loop + report, production path only), `cli/anima.py` chat verb replaces stub (anima.py:215), byte mode | ~1,600–2,300 | **Full-session golden: stdout byte-diff + kosmos dir byte-diff vs Phase-0 hexa golden** (toy ckpt on mini; 303M golden on pool per heavy-eval policy) | needs all above |

Milestone **M1 — first hexa-free chat (user-visible)**: after P1+P2 plus the small conflict/tension_resolve slice of P3, ship `cli/chat.py` v0 with the **production tick tail ported verbatim** (anima.hexa:3653–3861) but a reduced mount — `anima-py chat` runs, emits, writes kosmos on a pi5/bare pod. Label it explicitly **BEHAVIORAL (not parity)** in its banner until P6 lands; the reduced lane context changes `rel_ctx`/`cur_ctx`, so decisions differ from hexa by design at this stage. This removes the user-visible stub 2–3 PRs in, without pretending parity.

Packaging needs **zero changes**: pyproject already maps `cli/`+`core/` wholesale into `anima_py.*`, numpy stays the only base dep (all new faculty code is plain python).

---

## 4. First-build spec (Phase 0 + Phase 1, one session, two PRs)

**PR-A: `tool/chat_parity.py` + goldens**
1. Golden capture: run `hexa`-channel `anima <toy-d768.clm>` (default flags — det clock `tick*8`, 12 ticks) with `KDIR` noted; save stdout to `tests/goldens/chat_session_d768.stdout.txt` and the kosmos dir tree to `tests/goldens/chat_kosmos_d768/`. Re-run and assert 0 diff (determinism of the golden itself).
2. Comparator: port archive `compare.py` semantics — numeric tokens ≥12dp relative, strings byte-equal; add a kosmos-dir mode that diffs file sets + bytes with `emitted_at    = "..."` lines masked.
3. Record host + hexa version in the golden's README (libm same-host caveat).

**PR-B: 7 faculty twins + oracles** — port order and key invariants (all from the extracted specs):
- `emit_policy.py`: constants dict + `ep_theta_stage` (WAKE .10/N1 .08/N2 .05/N3 .02/REM .08), `ep_scale_periods/amps`.
- `dream_lib.py`: 90-tick ultradian machine (WAKE 60/N1 10/N2 10/N3 7/REM 3), `dr_stage_at/name`, binary `dr_emit_envelope`, `dr_imagination_active`, `dr_stage_size`, `dr_mitosis_prior`(0.80 N3/REM else 0.10). Port dead `sp_*` too (completeness bar) but note libm `exp` if ever verdict-reached.
- `dream_envelope_ctx.py`: `dr_stage_scale` = `ep_theta_stage` passthrough (10 LOC).
- `phi_envelope_substrate.py`: `envelope_multiscale` raised-cosine + Pearson etc., sequential accumulation preserved.
- `wake_memory.py`: cap-20 FIFO ring, immutable-update style (`mem_init/mem_push_ctx/mem_working_window/mem_record_emit/mem_recent_emits`).
- `imagination_replay.py`: `ir_select_snapshots/ir_replay_tick` (assert emit_count==0) / `ir_mitosis_tick_during_replay` (own placeholder — pass-through + `dr_mitosis_prior(4)`, `wired_to_lib:false`; **no** mitosis_hook_lib); `ir_consolidation_gain` as a sequential multiply loop, not `pow`.
- `dream_compose.py`: `dc_make_anchor` (coord midpoint, tension mean, radius max, lane="dream", id=`dream(a+b)`), `dc_compose_window` with the exact nested p<q pair order (determines on-disk numbering).
- One oracle pair per module (hexa oracle file + py `__main__`), run through the PR-A comparator; each oracle's field list mirrors the archive PARITY.md style.

Parity bar for the PR: every oracle ≤1e-12 relative (expect ~2e-16), strings byte-equal. This proves the mirror method end-to-end on the cheapest possible surface before any hot-path work.

---

## 5. Risks + honest scope

- **Is byte-parity realistic?** Yes, at the precedented level — *because the chat path is deterministic by design* (p7): greedy argmax mouth, no RNG on the verdict path, injectable clock, f64 both sides, seeded LCGs already integer-exact in py. The bar is **stream/file/field parity, not logit-bit parity**; anyone asserting raw-logit equality will fail on BLAS ULP noise and should not try. If a future chat feature adds sampling, the xorshift32 sampler is already byte-identical cross-engine, so seeded runs stay parity-eligible.
- **`a_engine_native_learning` bite**: a py chat that hasn't passed the P6 session golden is a mirror → anything measured on it is **DIRECTIONAL**. Chat is not a verdict-cementing path, so behavioral parity suffices for M1 *as a product feature* — but no H_ research verdict should run on py chat before P6 parity lands. After P6, the py chat becomes a 2-production twin with the same standing the owner already granted `anima-py evaluate` (a_eval_py_canonical).
- **Drift risk (the parity_gate lesson: "a py side-harness can DRIFT")**: twins rot when hexa's chat path changes without the py twin. Mitigation: the Phase-0 harness must be re-runnable in CI or at minimum a documented pre-merge check for any PR touching the closure files; consider adding it to `.harness/enforce_anima_gates.py` as a candidate gate once P6 lands.
- **Scope honesty #1 — "daemon"**: neither channel has a persistent daemon today (12 ticks, kosmos wiped in `/tmp`). This plan reaches *parity with what exists*. A true persistent REPL/stdin daemon with durable kosmos is a separate feature decision that should land in **both** channels (or py-first, flagged), not smuggled into the parity work.
- **Scope honesty #2 — what py deliberately omits forever**: GPU/forge/device-resident decode paths (numpy host math is the py channel's identity), hexa research instrumentation (`--opgrip`/`--refractory` arms), and the five orphaned faculties. These are not "incomplete mirror" — document them in the py channel README as intentional non-goals so the completeness bar (`a_completeness_over_cheap`) is judged against the right target.
- **Effort**: ~3.7–4.9k LOC with per-phase parity verification ≈ **6–9 focused sessions** (P0+P1 one session; P2 one; P3 one–two; P4 one; P5 one–two; P6 two, including the 303M golden run on pool — toy-ckpt parity runs are mini-safe, 303M mount is not).

Design-only deliverable — no code changes made; triage facts saved to memory (`py-selfimpl-chat-triage`) for the implementing sessions.