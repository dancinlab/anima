Two quick greps show stage-1/NBIND artifacts aren't under the names I guessed in this checkout — no matter; the spec below parametrizes the touchpoints (your existing grid generator + SPAN-GEOM LOSO probe) rather than hardcoding paths. Here is the implementation-ready spec.

(Unrelated: claude.ai Gmail/Calendar/Drive connectors need re-auth in your claude.ai connector settings; unavailable this session.)

---

# MORPH-ATOM stage-2 spec (H_92xx · G1 wall, atomicity lever)

## 0. Answer to the hard question first

The 256-byte constraint does **not** force a confounded codec. The mistake to avoid is trying to embed morpheme codes *inside* valid UTF-8. Instead, **re-encode the entire stream**: the codec output is a new alphabet you fully own, and the byte-LM trains on it as-is. The clean scheme is **fixed-width 2-byte token IDs** (below). Your fallback (jamo stream + reserved boundary byte) is strictly weaker — it grants *segmentation*, not *atomicity* (morphemes remain compositional multi-byte strings), so it tests a different, weaker hypothesis. Keep it only as a diagnostic arm if M fails the learnability gate.

"Atomic" operationally = **context-invariant fixed 2-byte signature per morpheme**. A 2-byte code is atomic in the sense that matters: its byte identity never varies across contexts/conjugations, and it is a dedicated unit no other string shares.

## 1. Codec — MORPH-2B

**Segmenter: BPE over jamo.**
- Decompose Hangul syllables NFD-style into 초성/중성/종성 with **distinct symbol IDs for 초성 vs 종성** (19+21+27 = 67 jamo symbols). This makes recomposition unambiguous with **no explicit syllable-boundary marker needed** (your drafted boundary byte becomes redundant — drop it from the stream; keep the round-trip test as proof).
- Non-Hangul characters pass through as raw bytes.
- BPE merges **within-eojeol only** (never across whitespace); whitespace is its own token. Trained on the CPT corpus itself — frequency-only, label-blind.
- Merge count K from a **preregistered ladder K ∈ {2048, 4096, 8192, 16384}**: pick the smallest K passing the G-0 audit. This is instrument-validity selection fixed before any training, not outcome tuning — say so in the card.

**Byte encoding: every token = exactly 2 bytes, big-endian ID.**
- ID 0–255 = literal-byte passthrough (anything out-of-vocab).
- ID 256…256+V−1 = BPE vocab, assigned by **pure frequency rank** (deterministic, semantics-blind).
- Decode: read byte pairs → ID → vocab string → NFC recompose. Lossless by construction; **assert round-trip on 100% of the corpus**.

Why fixed-width beats an escape/variable-length scheme:
- No code-*length* annotation (variable-length would mark frequent morphemes as "short" — a real, if shared, annotation channel; fixed-width has zero).
- Token boundaries at even offsets = trivially learnable periodicity for the L4 conv stack.
- ~2 bytes/token vs ~3 bytes/syllable UTF-8 → the codec stream is **shorter** than raw; the conv RF covers *more* morphemes per window. This biases *for* learnability without touching the abstraction question.
- The hi byte bins vocab by frequency rank (all high-rank morphemes share hi=0x01, etc.) — it annotates frequency, which the frequency-matched non-neg cohort shares identically. The lo byte carries identity.

**G-0 codec audit (blocking, $0, before any training):**
1. **Round-trip** 100% lossless on the full corpus.
2. **Single-token stems**: for each of 안/않/못/아니, ≥90% of its *in-context corpus occurrences* segment with one token exactly covering the stem's jamo (check occurrences, not isolated citation forms — BPE context effects are real).
3. **Pairwise sub-token disjointness — the killer leak check.** At jamo level 안=ㅇㅏㄴ, 않=ㅇㅏㄴㅎ, 아니=ㅇㅏㄴㅣ share the ㅇㅏㄴ prefix. If BPE leaves 아니 segmented as [ㅇㅏㄴ][ㅣ] where [ㅇㅏㄴ] *is* 안's token, the held-out stem literally contains a drilled stem's code → transfer is form-handed → invalid. **Assert the 4 stems' token sequences share zero token IDs.** Fails at K → step the ladder up (more merges fuse 아니 whole).
4. **Annotation symmetry**: build a frequency-matched non-neg cohort (k=50 nearest-frequency morphemes); assert neg stems and cohort receive codes by the identical rank rule, same width, no reserved range distinguishing them. Trivially true by construction — the audit is the executable proof for the card.

If even K=16384 can't fuse 아니 (audit-3 unfixable), switch primary held-out to **못** (ㅁㅗㅅ — jamo-disjoint from the ㅇㅏㄴ family, dodges the shared-prefix problem entirely).

## 2. Corpus

**CPT**: label-free natural ko. Source: HF `dancinlab/anima-corpus-ko-general` + `ko-sns` (already clean/register-balanced). Target ~100–200MB raw. Hard requirement (audit table in manifest): **≥20k corpus occurrences of each of the 4 stems**. If 아니 falls short, note that the NBIND-G external-corpus owner gate concerned *pure-certified sentiment atoms* — plain label-free natural text doesn't hit that blocker, but flag before injecting. BPE is trained on this same corpus.

**Drill**: your existing NBIND XOR grid (pol(p)⊕flip(n), predicate × negation form, per-stem grammatical frame — keep frames as-is; 못's -지 못하다 long-form frame is why frame-matched design already exists), remapped through the codec. **Drilled stems only (안/않/못); held-out stem 0 rows** — grep-assert the held-out token ID appears 0× in the drill stream. Balanced pol×flip cells, ~10–20k rows.

**Drill mix**: 90% grid + 10% CPT replay, same ratio in all arms — the drill fine-tune must not catastrophically erase the held-out stem's CPT-induced geometry (that failure mode would masquerade as a substrate verdict).

**Eval**: forced-choice margin scoring (teacher-forced, score the two label continuations; no free generation, so odd-length/invalid-ID output is a non-issue). Label continuations codec-remapped in codec arms; identical sentences/labels across arms.
- **F2** = held-out-stem × held-out-predicate flip bacc, **n≥400 items** (stage-1 was well-powered at n≈296/stem; 400 gives ~0.9 power for Δ=0.15 paired).
- **F1** = drilled-stem × held-out-predicate bacc; sanity gate ≥0.75, else the drill itself failed → arm VOID.

## 3. Arms — exact corpus deltas

All arms warm-start the same base 303M ckpt; same sentence sets and epoch counts (match passes-over-content, not bytes; report per-arm token counts). Note the built-in conservatism: codec arms pay an encoding-adaptation tax C1 doesn't — a win for M is therefore an underestimate.

| Arm | Codec | CPT corpus | Drill | Verdict role |
|---|---|---|---|---|
| **M** | MORPH-2B(K*) | full | 3-stem grid, codec | the hypothesis |
| **C1** | none (raw UTF-8) | same sentences, raw | same grid, raw | "more ko data alone" control |
| **C2** | MORPH-2B(K*) | full **minus every sentence whose segmentation contains the held-out stem's token ID** (homograph uses included — correct: the *code's* geometry is what's ablated) | = M | mechanism ablation; F2 must floor |
| **C3** | MORPH-2B(K*) with the 4 stem token IDs **collapsed to one shared ID at remap time** (segmenter untouched) | full | 3-stem grid | leak ceiling = V1 liveness; F2 ≥0.90 required |

## 4. Self-gates (make outcome-3 report PENDING, not FALSE)

- **G-0** (pre-fire, $0): the codec audit above. Blocks dispatch.
- **G-a** (post-CPT, pre-drill, arm M): SPAN-GEOM LOSO rerun **on stem codes** — linear probe on frozen M-CPT reps, NEG-vs-frequency-matched-cohort trained on the 3 drilled stems' contexts, tested on held-out stem contexts. PASS = held-out bacc ≥0.70 ∧ exceeds permutation null (same RSA_Δ criterion as stage-1). **FAIL → STOP the M lane, verdict = PENDING(CPT-budget)** — the class didn't form, so transfer was never tested; escalation (bigger CPT) preregistered before any rerun. C2 skips this gate (its class *shouldn't* form; record its probe value descriptively — it doubles as the ablation's manipulation check).
- **G-a2** (post-CPT, pre-drill, M and C1): zero-shot F2 on the held-out grid. Must be **≤0.60**. Above → CONFOUND(CPT-direct-supervision): natural text alone taught the flip, and drill-transfer would no longer attribute to the induced abstraction. Report it; do not filter the corpus to dodge it (that's tune-to-green).

Both gates run in minutes on the pod between CPT and drill — build them into the per-arm script with explicit exit codes.

## 5. Thresholds & stats

- Paired per-item Δ (identical eval items across arms), bootstrap 10k resamples, BCa 95% CI. **No max-over-controls / order-statistic deltas** (probe-defect-census).
- **PASS (per seed)**: F2(M) ≥0.70 ∧ Δ(M−C1) ≥0.15 with CI-low >0.05 ∧ F2(C3) ≥0.90 ∧ F2(C2) ≤0.55 ∧ F1(M) ≥0.75 ∧ G-a/G-a2 green.
- Single seed = DIRECTIONAL. PASS candidate → **1 seed replication + held-out-stem rotation (아니→못)** before anything TERMINAL (V5 + form-generality: 못 is jamo-disjoint from the drilled family, so the rotation is also the cleanest possible non-leak demonstration).
- **Negative discipline**: if M fails, no 🧱 on n.s. alone — preregister TOST vs C1 with Δ_eq=0.10, N_REQ from pilot item-level variance; CI inside (−0.10, 0.10) earns "no effect", otherwise PENDING(power).
- Sanity: raw-byte F2 baseline is historically 0.20–0.45; **C1 ≥0.65 ⇒ grid regressed (leak into eval) ⇒ INVALID**, stop.

## 6. Pod plan

- **S0** (mac/pool CPU, $0): jamo codec + BPE trainer + encode/decode + G-0 audit + 4 corpus variants + grid remap + manifest (sha256, per-stem occurrence table, K* selection record).
- **S1** (fire): **4 pods, 1 arm per dedicated host** (per your pod-dedicated-host policy — no core-contention throttle), RTX4090 each. Per-arm script: pip bootstrap hard-gate → `pip install "anima-python[train]"` → pull base ckpt → CPT ~60min (`anima-py train --arch clm --canon --objective ce_marginal`, warm-start base 303M) → save ckpt → gates (M: G-a+G-a2; C1: G-a2) → drill FT ~20min (90/10 mix) → F1/F2 forced-choice eval → verdict JSON. Early-exit: G-a fail skips M's drill but **C1 and C3 run to completion regardless** (baseline and liveness artifacts stay reusable for the rerun).
- **S2**: pull all 4 ckpts + eval JSONs to permanent storage **before teardown**, HF upload (PRIVATE while WIP), `hexa verify` → `state/verdicts/`, card + jsonl, pr-cycle.
- Cost: 4× 4090 × ~2h ≈ **$4–6** total, wall-clock ~2h (arms fully parallel).

Sharpest risks, in order: (1) audit-3 sub-token leak via the ㅇㅏㄴ prefix when 아니 is held out — this is where a false PASS would come from, so the disjointness assert is non-negotiable; (2) drill erasing CPT geometry — covered by the 10% replay plus G-a giving you the pre-drill reference point; (3) warm-start alienness making all codec arms fail G-a — that outcome is PENDING(CPT-budget) by design, and C3 still tells you whether the protocol itself was live.