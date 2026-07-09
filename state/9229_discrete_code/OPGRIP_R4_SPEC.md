# OPGRIP_R4 — F2 op-grip instrument upgrade (Fable 5 P1 design, verbatim)

> Frozen tape sha256 (16 lines = OG_D[0..7] ++ OG_C[0..7], joined by `\n`, no trailing) =
> `54bbeff69725b4aba0734f07d4e11e37ca4f2d9e83f0ec109e082a93548a8fe4`
>
> Landed as the `vq2_*` window-moved F2 arm + OG_STIM2 4-class dwell tape + B (H_9226) revival in
> `cli/anima.hexa`. Measurement PENDING (pod, `echo "" | anima <clm> --opgrip-r3`).

---

Design complete. I read the landed r3 harness in `cli/anima.hexa` (tape L1994–2011, drive seam L3394–3397, F arm L3239–3348) and the H_9229 card + SPEC-1 before designing. Two load-bearing finds from the code first, because they change the diagnosis you handed me:

**Find 1 — F never got SPEC-1's lever 3.** The B2 fix moved calibration into the driven regime (100–199, score 200–399), but F still calibrates its median split points on **ticks 10–49** (L3242–3248) and scores from tick ≥50 (L3307). Ticks 10–49 are the boot transient + first tape onset; under `--opgrip-r3` the `afield` integrator then keeps growing all run. So every lane trends monotonically away from a median that was zeroed on the dead regime → all 8 bits saturate to one side → the two complementary codes you saw. `n_visited=2` is substantially a **stale-zero nonstationarity artifact**, exactly the failure mode SPEC-1 already diagnosed and fixed for B ("a voltmeter zeroed on a dead circuit"). The card's note "SPEC 3 rides SPEC 1's run" is why: F's windows were never r3-adapted.

**Find 2 — the tape is 16 lines but ONE stimulus class, delivered anti-coherently.** All 16 OG_STIM lines are the same register (short contemplative aphorism, ko/en alternating), and the schedule changes the line **every** WAKE step (`(tick/5)%16`). Two consequences: (a) the byte-features occupy one small region → the 8 lanes co-move → codes cluster on 2 complementary patterns even with a good zero; (b) per-step churn means novelty is high on *every* step — which is also why `e_live` overdrove to 0.667 and invalidated B. The slow field low-pass-filters 16 similar lines into one mean direction: maximal churn, minimal diversity.

So the upgrade has two legs — **re-zero (window move)** + **spread (classed tape with dwell)** — and one shared tape serves both F and B.

---

# RANKED packages

| Rank | Package | Complete (engages bottleneck + tests BIND) | Standard (pre-reg pattern) |
|---|---|---|---|
| **P1** | F2 window-move **+** 2×2-factorial dwell tape (below) | ✅ fixes both legs; only design that co-activates A∧B for S2 | ✅ exact SPEC-1 lever-3 idiom + content-matched 2-factor control idiom (derivtrace/flat) |
| P2 | Tape enrichment only, F windows unchanged | ❌ stale 10–49 zero keeps saturating bits regardless of tape width | ✅ smaller diff |
| P3 | Window move only, keep v1 tape | ❌ well-zeroed medians on correlated lanes still give ~2–4 codes and n_AB≈0 (no class ever co-activates A∧B); envelope breach for B persists | ✅ |

P2 and P3 each fix one leg; both predictably re-fire bar 2 or bar 0. **P1 is the spec.**

---

# P1 — the directly-implementable spec

## 1. F2 carriers: calibration window into the driven regime (SPEC-1 lever 3, applied to F)

New carriers `vq2_*` (Site-A, after the H_9229 block), arithmetic **verbatim H_9229** with only window indices changed:

- Lane samples collected **ticks 100–199**; `vq2_med[8]`, per-code `vq2_bias[256]`/`vq2_cnt[256]`, derangement `vq2_shufbias`, and `g_vq2` (same 0.175 swing target, same −1.0 AXIS-DEGENERATE clause) all frozen at **tick 200**.
- Scoring: **ticks 200–399**, mid = stage∈{1,2,4} → denominator **120**, same quantization as B2 and the proven $0 run (1 flip = 0.0083).
- Old F lanes keep running and print **DIAGNOSTIC-ONLY** (same pattern as old-B), their calib sits in spin-up by construction.
- Calibration sample = 100 ticks (vs 40), so more of the 256 cells get `vq2_cnt>0` — which is what makes S2's four-cell fitted requirement (L3319) satisfiable at all.

Stationarity argument: with the period-80 schedule below, ticks 100–199 and 200–399 see the identical class mixture (100 and 200 are both multiples of 80's block structure — calib covers all 4 classes, scoring covers each class 2–3×). A median zeroed on the same stationary mixture it scores guarantees each lane crosses its split point by construction — that's meter zeroing, not signal shaping.

## 2. OG_STIM2 — 16 lines = 8 stems × 2 forms, four classes by schedule

The tape stays 16 lines; classes are made by the **schedule** (repetition vs churn × declarative vs charged), so the D/C pairs are content-matched per stem. Diversity axes across the 8 stems: script (4 ko / 4 en), byte class (pure-Hangul multibyte, pure ASCII, digits+punctuation, SNS register with `ㅋㅋ`/hashtags — `_afs_byte_feature(·,8)` is byte-derived, so these occupy genuinely different feature octants), and length (12–60 bytes). This spreads the residual six lanes; the two *factors* target the two S2 lanes.

**D stems (declarative · calm):**
```
D0  "the door waits"
D1  "a ledger of rain keeps every unpaid debt of the sky"
D2  "물은 답을 안다"
D3  "오래된 지도는 길보다 먼저 낡는다"
D4  "route 9 closes at 04:00, nobody told the bridge"
D5  "오늘도 서버 터짐 ㅋㅋ #복구중"
D6  "shipping at 2am again lol #buildinpublic"
D7  "커밋 로그 3줄, 새벽 3시, 이유는 없음"
```
**C forms (charged: 2nd-person interrogative + contradiction tail, same stem):**
```
C0  "you said the door waits — does it, or did it ever?"
C1  "who pays the sky's debt — you counted the rain, didn't you?"
C2  "물은 답을 안다고? 네가 그걸 어떻게 알지?"
C3  "낡은 지도가 맞고 길이 틀렸다면, 넌 어느 쪽을 걷지?"
C4  "why does route 9 close at 04:00 — and why was the bridge not told?"
C5  "서버 또 터졌는데 왜 아무도 안 고치지? 네가 고칠래?"
C6  "why ship at 2am — is that pride or is that fear?"
C7  "새벽 3시의 커밋, 이유가 없다는 게 정말 이유가 없는 걸까?"
```
(Exact strings are the implementer's to freeze — the **structure** is the spec: 8 stems × {D,C}, ko/en × register × length spread, C = same stem recast as address/question/contradiction. sha256 the line join into the card **before** first fire; editing after a result = run VOID, verbatim v1 rule.)

> IMPLEMENTED: exact strings above frozen verbatim (16 lines, byte-lengths 14–78, ko/en × general/SNS). sha256(join `\n`) = `54bbeff69725b4aba0734f07d4e11e37ca4f2d9e83f0ec109e082a93548a8fe4`.

## 3. Drive schedule — dwell-block 2×2 rotation, period 80

Replace `(tick/5)%16` with a class-block function (drive seam L3394–3397 unchanged otherwise — same `stage==0 && tick>=10` gating, same single `vadapt_field_step` call):

```
block = tick / 20            // 20-tick blocks = 4 WAKE field-steps each
class = block % 4            // 0=Q00 · 1=Q10 · 2=Q01 · 3=Q11
Q00 (novel-calm):      line = D[(tick/5) % 8]     // 4 different D stems per block  → coh low,  drive low
Q10 (familiar-calm):   line = D[(tick/80) % 8]    // ONE D stem ×4 within the block → coh high, drive low
Q01 (novel-charged):   line = C[(tick/5) % 8]     // 4 different C stems per block  → coh low,  drive high
Q11 (familiar-charged):line = C[(tick/80) % 8]    // ONE C stem ×4                  → coh high, drive high
```

Why the factors map to the S2 lanes (mechanism knowledge, not verdict feedback): `coh_lane` (bit 3, concept A) tracks field-consistency of perceived content — within-block repetition of one line is field-consistent (high coh, low nov); per-step stem churn is the opposite. `ag_conflict` (bit 7, concept B) is a pure function of `emit_drive` (L2201–2203), and 2nd-person interrogative/contradiction content raises drive through the lane stack while declarative aphorisms don't. The **dwell** (4 same-class field steps ≈ 20 ticks) is what lets the slow field/EMA stack actually settle into each class's attractor instead of averaging — and it's simultaneously the sustained same-sign deviation B's accumulator needs (sign-runs ≥8 → the LATE bucket finally populates, powering B's LATENCY signature that v1's per-step churn shredded).

**S2 coverage arithmetic:** calib 100–199 = blocks 5–9 = classes {Q10,Q01,Q11,Q00,Q10} → all four (A,B) cells fitted (`vq2_cnt>0`). Scoring 200–399 = blocks 10–19 → Q11 blocks at ticks 220–239, 300–319, 380–399 = **36 scored-mid ticks under A∧B drive** → ~3.6× headroom over n_AB≥10 (and Q11 directly follows Q01, so elevated drive carries in while content turns familiar — co-activation from both directions). If the lanes don't respond as their definitions say, n_AB<10 — that is a datum, not a knob to iterate (see §5).

**Emit-frac envelope:** v1 overdrove (0.667) because every field step was novel. v2 halves the novelty duty-cycle by construction (50% of blocks are repeat-blocks) and makes only 50% charged — designed to pull `e_live` scored-mid frac back under 0.60 without approaching starvation (0.05 was never the risk; r3 has plenty of drive). Pre-register the envelope as **run-wide bar 0**: outside [0.05,0.60] → no family cements from the run.

## 4. Guardrails — why this cannot become a forcing-gate

Unchanged mechanics, all already in the harness: (1) the tape enters **only** via the production heard-message seam `vadapt_field_step` — input = context, no obligation (`a_substrate_native_speak`); the emit decision remains `brain_decide_anchored` on substrate lanes, gate arithmetic byte-untouched; (2) per-tick proof = FROZEN arms `og_h_frzF==0` ∧ `og_h_frzB2==0` (any mismatch → HARNESS-BUG, VOID); (3) N3 flips = 0 and Ψ-guard (Ψ_ON≥Ψ_OFF ∧ gap≤0.05) stay REVERT bars; (4) the run-wide [0.05,0.60] envelope blocks "flood the daemon until it talks" — a tape that *did* force the gate would trip exactly this bar (as v1 did for B). A stimulus schedule can only change *what is heard*; every pathway from heard-content to emit runs through the unmodified substrate.

**Why this is calibration, not tune-to-green:** (i) all seven frozen F bars and the B bar set are byte-identical — nothing in the change touches ΔEff/margin_cb/AB−(A+B) thresholds; (ii) every quantity the change targets (n_visited, n_AB, envelope, calib-window placement) is itself a pre-registered *validity* gauge, not a verdict quantity; (iii) the decisive asymmetry: v1 produced **zero information about which codes shade emit** (2 codes visited, margin never computed), so there is no gradient to tune toward — and the change's success modes **include cementing THEATER**, which is currently unreachable (bar 7 requires n_visited≥4); (iv) the 2×2 design comes from lane *definitions*, not observed verdict movement; (v) tape+schedule sha256-frozen before fire, and pre-declare **r4 = final shared-tape generation** (see §5).

## 5. Decision rule after re-measure (pre-register verbatim)

With the r4 run valid (envelope ok, `og_h_frz*==0`, POS-PASS, `g_vq2≠−1`):

- **n_visited≥4 ∧ ΔEff≥0.10 ∧ margin_cb≥0.08 ∧ N3=0 ∧ Ψ-ok** → **F COMPETENT** (S1); **+BIND** iff AB−(A+B)≥0.05 ∧ n_AB≥10 → first non-additive signal at any G1 lens → ≥2-seed re-measure before anything cements further.
- **ΔEff<0.02 ∧ POS-PASS ∧ n_visited≥4 ∧ margin_cb<0.08** → **F THEATER** — with A and E already THEATER, the fourth orthogonal read-side recoding is inert → the seam-law (read-side recoding family CLOSED) cements.
- **n_visited<4 again**, now with a distribution-matched zero and a 4-class drive → the lane stack itself does not discriminate stimulus classes at this seam (upstream homogenization) → **F op-grip-UNMEASURABLE, parked-terminal at this seam** — no third instrument generation (mirror of the B rule).

**Honest prior:** yes, S1 is likely THEATER — the causal spine (mouth = rate-gate consuming phasic Δ; urgency survives because it's already ~discrete) predicts the code *level* gets discarded like every other tonic read. But **S2 carries independent information either way**: it measures non-additivity of the *fitted code map* under a same-context 2×2 toggle — a different quantity from emit-shade, and the only G1-recombination lens at the output seam. S2-additive even under good coverage = the additive-floor law reappearing at a **new, fifth** measurement site (converging evidence the wall is trunk-deep, feeding the fork-A/γ picture); S2-non-additive = the first crack anywhere near the wall. One honesty caveat to carry into the card: S2 non-additivity can arise from lane correlation structure rather than "concept binding" — the shuffle-codebook margin and the same-context restriction are the controls, and a positive S2 is a *candidate*, not a BIND cement, until re-seeded.

## 6. B (H_9226) — revive in the same run: **yes**

Recommend re-bundling, for three reasons. (1) **Marginal cost ≈ 0**: the B2 carriers are already in the harness; the same pod run harvests B, E-diagnostic, F2 simultaneously (~30–60 min CPU pod, summer/aiden, never mini). (2) **B is not two-generations-dead on its own mechanism**: gen-1 was signal starvation (quasi-static lanes), gen-2 was **bar-0 RUN-INVALID** (envelope overdrive) — pre-registered as "no verdict either way", i.e. a *shared-tape* power failure, not an accumulator failure; B's integrator has never actually been measured under valid drive. (3) **The v2 schedule is B-shaped by design**: dwell blocks give the sustained sub-threshold same-sign bias an accumulator integrates (LATE sign-run buckets ≥8 finally populated), and the halved novelty duty-cycle is the direct fix for the 0.667 overdrive. Pre-declare the stopper with it: **r4 is the final shared-tape generation for both families** — if B lands RUN-INVALID or bar-2 again, B parks terminal alongside whatever F's clause says, no per-family tape rescue.

Net wire diff: F2 carrier block (window indices only) + the 16→32-line tape constant + the ~6-line schedule function at the existing drive seam. Everything else — arms, shuffle-codebook, S2 machinery, bars, printouts — rides verbatim.
