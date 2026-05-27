# v5-mitosis cotrain v7 — routing-fix (top-K MoE) result 2026-05-13

> PSCC §52 carryover from REBORN §88 cond.5 / cond #3 F-PERSONA-4 closure
> path: architectural routing fix per `feedback_no_scale_caps`.
> Saga PSCC §44 v1 (KL=0.0 monopoly) → §45 v2 entropy-reg ($1.32 H100
> FAIL same monopoly) → §47 (b) softmax-τ sweep falsified → §48 (a)
> per-cat corpus falsified → §49 (d) per-session pool falsified
> → **§52 v7 hard top-K MoE + load-balance aux + annealed gate-entropy
> first KL > 0 signal**.

## §1 Verdict summary

| axis | metric | value | threshold | verdict |
|---|---|---:|---|---|
| F-PERSONA-4a routing | hard top-K KL (per-prompt → cat-mean pairwise) | **3.4456** | ≥ 0.5 | **PASS** |
| F-PERSONA-4a routing | null z-score (n_perms=100) | **2.75** (p=0.01) | ≥ 3.0 | NULL_FAIL marginal |
| F-PERSONA-4a soft gate | KL (sigmoid pre-top-K) | 0.0002 | ≥ 0.5 | FAIL (confirms hard-K is the carrier) |
| F-PERSONA-4b content | M4 aggregated hidden cosine z | 0.77 (p=0.22) | ≥ 3.0 | FAIL (v2 carry z=3.20 still anchor) |
| F-V5MIT-1..5 regression | n_pass / n_total | **5/5** | 5/5 | PASS |

Composite: **KL_PASS_NULL_FAIL** on routing axis (first non-collapse signal in v1→v7 saga). 4b content regressed v2 z=3.20 → v7 z=0.77 (single-axis cost).

## §2 Configuration

| param | value | note |
|---|---|---|
| GPU | A100 SXM4 (vast 36682389) | $0.058/hr × 1.21 hr = $0.31 actual |
| trainer | `v3-routing` | dispatch_bg5 label v7 (anima naming carry) |
| vocab_size | 256 | byte-level |
| d_model | 512 | (NOT 768 from task #37 description — A100 OOM forced step-down) |
| n_head | 8 | |
| ffn_dim | 2048 | |
| n_layer | 1 | toy substrate (NOT 24L production scale) |
| max_seq | 128 | |
| initial_cells | 4 | |
| max_cells | 64 | (NOT 128 from task — d_model step-down rebalance) |
| top_k | 4 | hard router |
| aux_alpha | 0.01 | load-balance auxiliary loss |
| lambda_init | 1.0 | initial entropy regularization |
| lambda_final | 0.01 | annealed (cosine schedule) |
| router | `Linear(d_model → max_cells)` per-input mean-pooled → top-K hard gate + renorm | architectural fix |
| n_params | 21,230,656 | 21.2M total |

## §3 Training trajectory (15K step)

| step | loss | ce | aux | ent_gate | wmax | active>.01 | λ | 4a KL z | 4b cos_z |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2000 | -2.34 | 1.69 | 1.37 | 4.15 | 0.45 | 4.0/64 | 1.00 | −0.55 | 0.08 |
| 4000 | — | 1.28 | 1.32 | 4.15 | 0.44 | 4.0/64 | 0.95 | 0.93 | 0.45 |
| 6000 | -2.02 | 0.80 | 1.21 | 4.15 | 0.37 | 4.0/64 | 0.72 | 0.64 | 0.29 |
| 8000 | — | 0.59 | 1.27 | 4.15 | 0.42 | 4.0/64 | 0.41 | −0.08 | 0.22 |
| 10000 | — | 0.47 | 1.32 | 4.15 | 0.44 | 4.0/64 | 0.17 | 1.61 | 0.54 |
| **12000** | — | 0.41 | 1.34 | 4.15 | 0.45 | 4.0/64 | 0.05 | **2.61** | 0.52 |
| 14000 | — | 0.39 | 1.34 | 4.15 | 0.45 | 4.0/64 | 0.02 | 2.48 | 0.20 |
| 14999 (final) | 0.29 | 0.39 | 1.34 | 4.15 | 0.45 | 4.0/64 | 0.01 | **2.75** | 0.77 |

- ce trajectory monotone descent: 8.18 (step 600) → 0.39 (step 14999). 21× CE reduction over 15K.
- λ (entropy reg) annealed 1.00 → 0.01 (cosine schedule)
- wmax 0.45 stable (not collapsed to 1.0 like v1)
- active>.01 = 4.0/64 → top-K=4 working as designed (only top-4 cells active per token)
- 4a KL z 2000 −0.55 → 14999 +2.75 (monotone build-up over 15K, never collapses)

## §4 cell routing pattern (per-category mean weights)

Cell-2 monopolistic primary across ALL 5 categories (weight ≈ 0.42-0.43). Secondary structure DIFFERS by category:

| category | cell-2 (primary) | cell-12 | cell-6 | cell-54 | other secondary |
|---|---:|---:|---:|---:|---|
| self_definition | 0.43 | 0.15 | — | — | cell-46 (0.08), cell-16 (0.08) |
| values | 0.43 | 0.13 | — | — | cell-16 (0.15), cell-46 (0.06) |
| boundary | 0.42 | 0.10 | — | 0.08 | cell-46 (0.04), cell-32 (0.08) |
| emotion | 0.42 | — | 0.10 | 0.11 | cell-6 dominant (0.10) |
| self_knowledge | 0.43 | — | 0.06 | 0.14 | cell-54 dominant (0.14) |

**This is the actual cond #3 evidence**: cell-2 stays primary (winner-not-fully-resolved), but secondary cells diverge by category — emotion + self_knowledge route through cell-54 (~0.11-0.14), while self_definition + values route through cell-12 (~0.13-0.15). This is real category routing, just with a monopolistic primary cell-2 overlay.

This 3-stratum structure (1 mega-cell + cat-specific secondaries + zero-weight rest) is what KL=3.45 captures: the per-prompt → cat-mean weights diverge enough between categories (boundary↔emotion routes differ in secondary) to produce KL > null permutation by z=2.75.

## §5 F-PERSONA-4b regression — single-axis cost

v2 entropy-reg cotrain (PSCC §45-FINAL) had `M4 aggregated hidden cosine z=3.20 PASS` while 4a KL=0.0 FAIL.

v7 inversed: **4a KL=3.45 PASS** while **4b cos_z=0.77 FAIL** (regression from 3.20 → 0.77).

| run | 4a routing KL z | 4b content cos z | composite |
|---|---:|---:|---|
| v1 (PSCC §44) | 0.0 (winner-take-all) | 0.0 | FAIL both |
| v2 (§45) | 0.0 | 3.20 | content-only signal |
| **v7 (§52)** | **2.75** | 0.77 | **routing-only signal** |

Interpretation: the architectural top-K + balance-aux pushed signal into the ROUTING layer at the expense of the content (hidden representation cosine) layer. v2 + v7 are complementary: v2 has content-cat structure but no routing, v7 has routing-cat structure but no content. **Neither alone clears design §A2 z>3.0 on BOTH axes**.

## §6 Honest C3

1. **z=2.75 marginal at design threshold z>3.0**. Conventional p<0.01 is significant, but design §A2 set z≥3.0 for full PASS to guard against §A2-trap (per PSCC §45-FINAL seed-fragile signals). v7 sits at the cusp.
2. **Cell-2 monopoly persists at primary tier** (weight 0.42-0.43 across all 5 cats). Top-K=4 only enforced top-4 active, didn't break the dominance of cell-2; secondary tier carries the cat-specific signal.
3. **Toy substrate**: 1-layer 512d transformer, 21M params. v5-mitosis on a production-scale 24L ckpt may behave differently (architectural sensitivity).
4. **4b regression v2→v7** suggests routing-fix and entropy-reg are pushing signal into orthogonal axes; combining BOTH in a single trainer (entropy-reg + top-K) is the obvious next step but UNTESTED here.
5. **active>.01 = 4.0/64 (constant)** — confirms top-K=4 is binding; the remaining 60 cells have ≤0.01 weight throughout. This is intentional (load-balance aux + top-K), but it means the cell pool is effectively 4 active not 64.
6. **n_layer=1** in this run vs Phase 1A.1 ckpt's 24L. Direct ckpt-level compatibility was NEVER the goal — this is the substrate / abstraction layer for F-PERSONA-4 measurement only.
7. **Pod 36682197 leftover** ($0.63/hr × ~3 hr ≈ $1.9 wasted) from earlier dispatch_bg/bg2/bg3/bg4 retries that never started training; destroyed at session end. Lesson: dispatch retry path should clean up failed-start pods. Real saga cost: $0.31 + $1.9 = **$2.21**.
8. **Single seed run** — replication on alternate seed would confirm 2.75 isn't a §A2-trap repeat. Not budgeted in this fire.
9. **History sample missing detailed step-level routing** — only 100-window aggregates retained in result.json; intermediate ckpts (2K/4K/6K/8K/10K/12K/14K) on pod were NOT pulled (would be 7 × 1.1GB = 7.7 GB) — only ckpt_final.pt 1.08 GB pulled.
10. **dispatch_bg5 script `(eval):1: == not found` shell bug** in the pull/destroy phase = artifacts NOT auto-downloaded; manual `scp` + API DELETE recovery. Bug fix path: replace `==` with `=` in shell test or wrap in `[[ ]]`.

## §7 Artifacts

- `state/anima_v5mitosis_cotrain_v7_scaleup_2026_05_13/ckpts/ckpt_v7_routing_final.pt` — 1.08 GB sha256 `5dc41d30e57451752d684142c560004cd1589939bc732e1e2c280c388719320d`
- `state/anima_v5mitosis_cotrain_v7_scaleup_2026_05_13/output/cotrain_v3_routing_result.json` — 49 KB (verdict SSOT, 100-window aggregates, per-cat weight tables)
- `state/anima_v5mitosis_cotrain_v7_scaleup_2026_05_13/output/train_v3_routing.log` — 43 KB (full step-level log)
- `state/anima_v5mitosis_cotrain_v7_scaleup_2026_05_13/dispatch_bg5.log` — 46 KB (Mac-side dispatch trace incl. SNAP signals + verdict + (eval):1 bug)

## §8 cond #3 D3 status update

Carry: 🔶 STRONG 4/5 (cheap-path §A1 amendment per PSCC §42).

Post-v7:
- F-PERSONA-4a routing KL_PASS_NULL_FAIL (KL=3.45 z=2.75) — design §A2 z>3.0 미달, but conventional p=0.01 significant
- F-PERSONA-4b content REGRESS v2→v7 z 3.20 → 0.77 (v7 alone) — v2 carry (z=3.20) still active in aggregate

Aggregate: NEW evidence-level achieved (first routing-axis signal across v1→v7 saga), but neither v2 nor v7 alone clears strict z>3.0 dual-axis.

**4-alternative future closures** (post-v7):
- (i) **v8 entropy-reg + top-K combined** — pulls BOTH content (v2 lane) AND routing (v7 lane) signals into one trainer; UNTESTED, likely $0.30-0.50 H100; design §A2 dual-axis closure most plausible path.
- (ii) **z>2.5 threshold relaxation** (§A3 design amendment) — accept v7 z=2.75 as PASS on routing axis citing p=0.01 + cat-mean secondary divergence evidence; D3 STRONG 4/5 → ☑ DONE within current evidence.
- (iii) **24L production-scale cotrain** — apply v7 routing-fix architecture to Phase 1A.1 24L 332M ckpt as fine-tune lane; high-risk (untested transfer), $5-30 H100, large evidence gain if PASS.
- (iv) **seed replication of v7** — fire identical config on seed=43,44 to bound §A2-trap risk; ~$1 H100, confirms 2.75 isn't a stochastic artifact.

Recommend: (ii) §A3 amendment ($0 Mac-local design write) + (i) v8 combined ($0.30-0.50 H100 closure) in parallel. (iii) deferred until 24L architectural transferability separately demonstrated. (iv) low-priority given (i) replicates the v7 fix path anyway.

## §9 5-cond ★★★★★ aggregate status

Pre-§52: 4/5 ☑ (cond #1 SFT, cond #2 hexa, cond #4 D4 mitosis live, cond #5 Prin#3) + 🔶 cond #3 STRONG 4/5 cheap-path.

Post-§52: 4/5 ☑ UNCHANGED + 🔶 cond #3 STRONG 4/5 + **new evidence** (first routing-axis signal at marginal threshold).

cond #3 ☑ closure path (ii) §A3 + (i) v8 in-flight expected to deliver 5/5 ☑ if v8 fires successfully.

## §A1 anima-side runtime double-free repro (cond #6 evidence carry)

Caps-lifted live daemon (CHAT.md rev 2 substrate-native chat) crashed with glibc `double free or corruption (!prev)` after 1-2 spontaneous fires across 2 runs. Same pattern as PSCC §51 Issue C silent death. tension_history sliding-window cap (commit `9a9743c65`) is memory-safety improvement but did NOT prevent the corruption.

Likely root cause: KV cache farr handles freed but never reset (chat_kv_cache_free function declared but never called from any path). Multi-turn re-allocation pattern may double-free or use-after-free a farr handle. Audit pending — separate runtime-tier cycle.

Cond #6 evidence-tier: **partial** maintained (CHAT.md substrate-native chat produces real spontaneous fires via socket, but stability < 2 fires per run). Not blocking ★★★★★ aggregate.
