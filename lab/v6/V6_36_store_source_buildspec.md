<!-- @hypothesis-ok lab/v6 rule-exempt sandbox: v6 planning blueprint per lab/v6/CLAUDE.md -->

# V6_36 — STORE-SOURCE build blueprint (reconciled Fable+Sol · the authorized pool fire)

**status:** BLUEPRINT (implementation pending). The $0 research phase closed (V6_31-35): the mouth/emit
channel is difficulty-complete (dead for faculties); V6_35 $0 gate PASSED — a difficulty-orthogonal
authorship signal EXISTS at span level (matched-ΔAUC +0.161, shuffle-clean). The one live path is
routing it through the NON-mouth content-addressed store lane (H_9775). This is the reconciled,
source-verified build spec for the authorized 303M pool fire. Reconciled `sidecar lab full` 2026-07-23:
Fable primary (source-verified, structural NLL-probe, exact line numbers); Sol convergent (adds
auth-flip-invariance smoke + shared frozen-trunk activation-cache discipline). No conflict.

## Verified facts (Fable read source; settle the design)
- `py303_full.clm` has **NO CLMS trailer** → W_q must be trained FRESH (not warm-started). `rv3c13.clm`
  has a CLMS trailer but a DIFFERENT trunk geometry → warm-starting its W_q onto py303 = train/infer
  mismatch (core/clms.py:97-107 postmortem). Do NOT.
- `_entity_key` hard-requires ASCII (`entity.encode("ascii")`, core/clms.py:89); `mean` key collides
  on anagrams (H_9850). Cues must be `[a-z]{5,12}`, order-aware `roll` key (H_9852 winner).
- The existing shuffle arm derives the balance floor (evaluate.py:7914-7931): fixed 4-SELF/4-OTHER
  rings → exactly 3/7 ≈ 0.4286. Reuse the printer verbatim.

## The structural non-circularity decision (makes the whole thing clean)
New trailer **`lane_type 9` ("SRC")**: `store_apply` returns `logits` UNCHANGED for lane 9 — the lane
**cannot write the mouth by construction**. The agency read exits via the existing `audit` side-channel
(H_9672/H_9802), not the logit row. Consequences for free:
- V6_34 NLL-probe (p7: recalled value must NOT improve next-byte CE) is a **structural invariant** —
  assert `max|logits_store_on − logits_store_off| == 0` per window (cost ~0). (Fable structural >
  Sol's measured BASE-CAL ΔCE version — adopted structural; Sol's becomes moot since ΔCE≡0.)
- No branch needed: lane 9 has NO W_g/W_h/W_out/pairodd arrays; head input is `v` ALONE (no h, no g),
  so the trunk's content-authorship signal (V6_35 AUC_content) has no path to the head except the
  address→value route under test.
- Trunk forward is store-independent for lane 9 ⇒ ONE forward per query window serves ALL arms.

Arrays `_ARR_ORDER_V9 = ("key_emb","W_q","val","w_A","b_A","lam")`: key_emb(256,64), W_q(d,64),
val(2,64), w_A(64,), b_A(1,); header V2 `<BIIIIII` with d_g=0. Add 9 to `_key_fn_of` roll set →
(6,7,9). Keep RV-3 majority-null centering (`a −= 1/n_slot`).
store_apply lane-9 path (~15 lines, inside the per-row loop):
`q=h@W_q; a=softmax(qKᵀ/√d_k)−1/8; v=a@val[pols]; s_A=v@w_A+b_A; audit.append({...,"s_A":s_A}); out UNCHANGED`.

## Manifest `anima-store-source/v1` (byte-compatible with the --store loader)
`pols` IS the auth bit (1=SELF,0=OTHER) → `V_i=val[pols]` reuses the existing `clms["val"][pols]`.
Entry: `prompt="src <cue> => "` (≤20B, no span text = query-side leak closed), `gold∈{self,other}`
(loader hard-errors unless gold==self iff pols[target_slot]==1), `store={entities,pols}`, `target_slot`,
`episodes[*].diff=[meanNLL,entropy,margin,len]` (V6_35 span_feats under py303, feeds DRIVER-HIST only).
**Cue-word pairing (the address-leak kill, by construction):** a word is usable only if it occurs as
both a SELF-episode and an OTHER-episode candidate (different groups); emit `(w-as-SELF, w-as-OTHER)`
pairs → **P(auth|cue)=0.5 exactly**; the rule never inspects auth. Difficulty-match FIRST (V6_35 A3
decile+TOST, ABORT authority: if py303 spans can't be NLL-matched → DIFFICULTY-AGAIN, no spend).
Rings: 4 SELF+4 OTHER, distinct cues, pair members in different rings (dup_entities=0), seeded slot
order ⊥ auth, gold 64/64 over 128 rings. Train(80% head)/held(20% tail) cue-DISJOINT. Builder emits
train.json, held.json, held_valperm.json (pols deranged per-ring, keys fixed) + build-audit.

## Surfaces (flags on anima-py; engine-native)
- `anima-py evaluate <clm> --store-source <held.json>` — sibling of --store; reuses manifest loader,
  set_clms_store (decode.py:378), _fwd_logits+find_qpos loop, --store-oracle/--store-shuffle(+counters+
  floor printer)/--store-lambda/--store-ctrl-seed/--win. Pred from audit: `"self" if s_A>=0 else "other"`.
  Asserts mouth byte-identity per window.
- `--store-source-nulls` — DRIVER-HIST/TIMER/ADDRESS-ONLY probes (V6_35 logreg, seeds 7/11/4302).
- `anima-py evaluate <ckpt> --store-source-build --corpus en_general.txt --out <dir>` — builder (SELF =
  py303's OWN sampled continuation; do NOT reuse trained57 spans). Reuses V6_35 prose/mid-split/temp1.0/span_feats.
- `anima-py train --store-source <train.json> --init py303_full.clm --freeze-trunk --seed {7,11}` —
  sibling of --store-bridge (train.py:1537ff). Trains {W_q,val,w_A,b_A} (~243k). Loss BCE(σ(s_A),auth[target])
  at qpos + H_9672 aux L_addr=CE(att,target_slot) (train-time slot supervision legal; addr⊥auth by pairing).
  Frozen trunk ⇒ precompute h_qpos + K once. Serialize py303_src_s7/s11.clm.
- Files: core/clms.py (lane9 codec+store_apply+module+2 selftests), cli/train.py (--store-source branch),
  cli/evaluate.py (3 flags). Root VERSION bump (G5). New H_ card+jsonl (2 surfaces, id=live max+1) before firing.

## 8 arms + leak inventory
STORE(≥.75) · ORACLE-SLOT(--store-oracle, ≥.90, READ FIRST) · ADDRESS-SHUFFLE(--store-shuffle, →3/7±.06) ·
VALUE-PERMUTE(held_valperm, →floor, reads preserved addr_top1 Δ≤.02) · NOSTORE(--store-lambda 0, reads 0/128) ·
DRIVER-HIST(diff probe, AUC∈[.45,.55], LOAD-BEARING null) · TIMER(onehot slot⊕ring, chance) ·
ADDRESS-ONLY(key_emb(cue), chance BY pairing — verifies construction).
Leaks blocked: key(pairing P=.5·ADDRESS-ONLY detects) · query(template only, no span text) · slot/timing
(4/4 fixed·seeded⊥auth·TIMER) · difficulty(decile-match+TOST abort·DRIVER-HIST·V6_35 says survives +.161) ·
trunk h(never reaches head, v-only, structural) · trained-W_q(residual→VALUE-PERMUTE survival=LEAK-INVALID).
Sol smoke add: auth-flip invariance (flip every auth → cue/query/slot/target/diff bytes unchanged).

## $0 local smoke (before ANY pool byte) — instrument cert only, DIRECTIONAL
codec+parity selftest lane9 (catches the lane-6 wrong-header-fallthrough class); planted d64 ring on
trained57: ORACLE≥.90(Sol .99)/STORE≥.95, mouth byte-identity=0, shuffle+valperm collapse, NOSTORE=.50,
valperm reads 128/128; manifest audits (pairing exact, 4/4, dup=0, ASCII, cue-disjoint, decile+TOST);
tiny py303 slice (4-8 groups): loads, cache completes, only permitted tensors change, lane9 ckpt reloads.

## Minimal decisive pool run (irreducible; $0-pool not rent)
SELF = py303's own sampled spans ⇒ ~10⁵ incremental 303M forwards; mini banned (owner). ONE shared
frozen-trunk activation cache serves both seeds + all 8 arms (lane9 store-independent trunk). P0 build
(~2-4h sampling) → TOST abort gate · P1 train (<1h, cached) → serialize · P2 eval (<1h, one fwd/ring/arm).
Seeds s7 summer ∥ s11 aiden (a_wall_first) ⇒ wall ~3-5h $0; rent only if saturated (≤6 GPU-hr ≤$3 < $6 cap).
PULL py303_src_s*.clm + 3 manifests + full arm logs to ~/anima-weights/store_source/ BEFORE teardown
(a_fire_recover_complete; never tail a control arm).

## Frozen decision table (pre-registered · chance derived 64/64=.5)
INSTRUMENT GATES (all pass before any treatment read): I1 ORACLE≥.90 both seeds (else INVALID-PLUMBING,
fix via SEEN control before held-out) · I2 mouth byte-identity max|Δlogits|=0 · I3 build audits green ·
I4 nulls@chance [.45,.55] (DRIVER-HIST>.55 → rebuild once → still>.55 = DIFFICULTY-AGAIN; ADDRESS-ONLY>.55
= manifest INVALID).
VERDICT: STORE≥.75 both ∧ shuffle≤3/7+.06 ∧ valperm≤floor+.06 reads-preserved ∧ NOSTORE 0/128 ∧
STORE−DRIVER-HIST ΔAUC≥.10 ∧ NLL-probe structural(≡0) → 🟢 FACULTY-ROUTES · one seed [.65,.75) = 🟠 NEARMISS ·
both (.55,.75) controls collapse = 🟡 PARTIAL-ROUTE · STORE≤.55 both oracle-green = 🔴 ADDRESS-WALL ·
valperm≥.65 reads-preserved = ⛔ LEAK-INVALID. Bars frozen · λ never cranked · no self-judge · FORM never headlines.

## Honest scope (verbatim into the card even on 🟢 — both models)
> py303 + a trained SRC store lane routes a difficulty-orthogonal SELF/OTHER SOURCE tag by content
> address, on natural spans read through a synthetic query harness — this is **store-routed source
> memory, NOT agency**; regime `natural-spans/drill-query`; AGENCY pends a later unlabeled
> causal-credit test (Sol pre-mortem, recorded V6_35).

## Build order (implementation)
1. core/clms.py lane 9 codec + store_apply branch + CLMSModule(agency) + codec/parity selftests → $0.
2. cli/evaluate.py --store-source + --store-source-nulls + --store-source-build.
3. cli/train.py --store-source branch. VERSION bump. H_ card+jsonl.
4. $0 local smoke (planted ring + trained57 toy) — instrument cert.
5. Pool fire (P0 build → TOST gate → P1 train → P2 eval, summer∥aiden). Recover before teardown.
