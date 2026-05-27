# §139 LEGO — flame spiking-primitives inbox patch FILED

> **Verdict**: `INBOX-PATCH-FILED-HEXA-FIRST-PATH-COMPLETE`. §138 specified the
> patch; §139 filed it. The 20×+ HEXA_FIRST_WARN deferral is now closed not by
> design alone but by an actual upstream request on the `hexa-first` PR-only path.
> filing-tier · $0 · NO GPU/runpod/fire. central c93e160a 0-diff.

## §0 Why §139

§138 (`HEXA-NATIVE-ENGINE-DESIGN-CLOSE-UPSTREAM-GAP-NAMED`) named the gap — 3
flame spiking primitives — and §138 §6 honestly noted: "It does NOT file the
inbox patch (that is a hexa-lang-repo write; actually filing it is a follow-up)."

§139 is that follow-up. It files the patch, completing the `hexa-first`
prescribed path ("when the constraint lives in hexa-lang itself, fix it there —
PR-only").

## §1 What was filed

`~/core/hexa-lang/inbox/patches/flame-spiking-substrate-primitives.md` — a
104-line patch-request doc. Committed in the hexa-lang repo (branch
`rfc006-yosys-rtlil-skeleton`, additive doc, established `inbox-patches-pipeline`
g7 pattern; §71's `flame-path-a-dual-head-and-multiterm-grad.md` is the precedent
— it is git-tracked in the same inbox).

The patch requests 3 primitives, each with a pre-registered falsifier:

| primitive                | what it does                          | falsifier   |
|--------------------------|----------------------------------------|-------------|
| `flame_event_threshold`  | boolean spike mask `v >= v_th`        | F-SPIKE-1   |
| `flame_refractory_step`  | per-unit integer countdown + clamp    | F-SPIKE-2   |
| `flame_stdp_pair`        | local pair-based STDP weight update   | F-SPIKE-3   |
| (all three)              | byte-equal vs lego_engine.py numpy ref| F-SPIKE-4   |

## §2 What §139 closes

✅ The HEXA_FIRST_WARN deferral is now **fully closed** — not "deferred 23×"
   nor "design names the gap" but "upstream request filed on the PR-only
   path." The next time HEXA_FIRST_WARN fires on a LEGO Python file, the
   honest response is "tracked — see flame-spiking-substrate-primitives.md."
✅ anima stayed a downstream consumer throughout — it wrote a *request*, not
   a hexa-lang source edit (`g_train_flame_not_pytorch upstream_downstream_
   invariant` honored).
✅ The §138→§139 pair mirrors §71 exactly: §71 designed the dual-head/multi-
   term-grad need + filed `flame-path-a-dual-head-and-multiterm-grad.md`.

## §3 What §139 does NOT close

❌ The primitives are NOT implemented — that is hexa-lang upstream work,
   reviewed and PR'd on their side. anima cannot and should not implement them.
❌ `lego_engine.hexa` does NOT exist yet — it is a mechanical port *after*
   the primitives land (F-SPIKE-4 byte-equal verification at that point).
❌ GOAL emergence — §139 is engine tooling, orthogonal (B-EMERGE-7).

## §4 Closed-form propositions

```
B-S139-1   INBOX-PATCH-FILE-EXISTS         (the patch file is on disk in
                                            hexa-lang inbox/patches/)
B-S139-2   PATCH-REQUESTS-EXACTLY-3-PRIMITIVES  (matches §138's named gap)
B-S139-3   PATCH-IS-REQUEST-NOT-SOURCE-EDIT (downstream-consumer posture —
                                            patch is markdown, not flame code)
B-S139-4   CENTRAL-0-DIFF + NO-FORBIDDEN-CALL-AST
B-S139-NOTE  empirical carve-out — patch filed, upstream implementation =
            hexa-lang's work, NOT counted 🔵
```

## §5 Honest C3 (8)

1. §139 is a *filing record* — the substantive design is §138; §139 just
   completes the action §138 specified.
2. The patch is committed in hexa-lang on branch `rfc006-yosys-rtlil-skeleton`
   (whatever branch was checked out) — not anima's concern which branch;
   the inbox/ drop is the handoff.
3. anima did NOT push the hexa-lang commit — a sibling-repo push is the
   hexa-lang owner's call; the committed file in inbox/ is the handoff.
4. The 3-primitive request is the honest minimal set (§138 B-S138-2).
5. anima stays downstream-consumer — wrote a request doc, edited no flame
   source.
6. HEXA_FIRST_WARN will keep firing on future LEGO Python files until the
   primitives land + lego_engine.hexa is ported — but now the deferral has
   a *tracked upstream request* behind it, not a bare "out-of-scope."
7. g3: filing ≠ implementation ≠ fire ≠ emergence; capability claim 0.
8. north-star + §15/§51/§72 milestones UNCHANGED; **GOAL 미도달**.
