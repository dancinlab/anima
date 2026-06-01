# ONCHIP-PARADIGM — the easy companion

> Layperson companion to `ONCHIP-PARADIGM.tape`. Same facts, plain words.
> The tape is the machine SSOT; this is the "explain it to a friend" version.

---

## 🧠 ONCHIP-PARADIGM — "the AI that learns on the chip, not in the factory"

- **What it is**: a plan for an AI whose *learning* happens on the tiny edge chip
  itself (while it runs), instead of being trained once on big GPUs and then frozen.
- **Analogy**: a normal AI is like a **statue cast in a factory** — shaped once,
  then it never changes. This paradigm is like a **plant in your window** — it
  keeps growing and adapting right where it lives.
- **The GPU's real job here**: not the learner — just the **ruler**. We use GPUs
  to *measure* whether the idea works (a clean, repeatable sandbox), the same way
  a tape measure checks a plant's height but doesn't make it grow.

```
 factory AI (today)              on-chip AI (this paradigm)
 ────────────────                ──────────────────────────
  train on GPU once              learn on the chip, always
  ship a FROZEN model      →     model keeps adapting live
  GPU = the maker                GPU = only the ruler (measure)
  one fixed brain                a brain that grows + rewires
```

- **vs the usual way**: standard deep learning = "train, freeze, deploy" with
  backprop on GPUs. Here = "deploy and *keep* learning" with on-chip plasticity,
  no backprop. (cf. AKD1000 neuromorphic chip vs a frozen PyTorch checkpoint.)

---

## The 4 pieces (each: what we proved on a sandbox, what's still untested on the real chip)

A key honesty rule runs through all four: **proving it in a GPU/CPU sandbox is a
rehearsal, not the real exam.** The real exam is the chip. So every piece has a
🟢/🔴 "rehearsal" result and an OPEN "real chip" question.

### 🌱 1. on-chip plasticity — "learning without a teacher's red pen"

- **Plain**: the AI updates itself from local rules (neuron-by-neuron), with **no
  backprop** — no global "here's your error, fix everything" pass.
- **Analogy**: a muscle that strengthens from *use itself*, not from a coach
  grading every rep.
- **Rehearsal 🟢**: in the sandbox it still learned well — picked up new skill
  (GAIN 0.917) while keeping the old (RETAIN 1.0), with zero backprop.
- **Real-chip OPEN**: does the AKD1000 chip hold that GAIN + RETAIN when the
  updates are noisy, low-bit, and physically stochastic? Must be re-checked on
  silicon — the chip already behaves differently from the sandbox (H_904).

### 🔁 2. learn-while-infer — "no separate study time"

- **Plain**: there's no "training phase" then "use phase" — every time the model
  answers, it also nudges itself. One continuous stream.
- **Analogy**: a chef who **improves the recipe while cooking the dish**, not in a
  separate practice kitchen.
- **Rehearsal 🟢**: streaming online, quality never dropped (z_drop 0.0) and it
  kept its identity (PROBE 1.0), error fell 4.82 → 0.59 as it went.
- **Real-chip OPEN**: on a live chip the "answer" and the "nudge" share the same
  hardware and timing — does quality still hold under real spike streams?

### 🪴 3. MITOSIS growth — "the brain adds rooms while you live in it"

- **Plain**: instead of a fixed-size network, it can **split a cell into two** to
  grow capacity *during* deployment.
- **Analogy**: a house that **builds a new room** without you having to move out —
  and the walls don't crack.
- **Rehearsal 🟢**: after a live split (4 experts → 5), nothing blew up — the
  output barely jumped (1.48e-7 at the seam) and learning kept descending.
- **Real-chip OPEN**: a real chip has a *fixed* pool of cells and a power budget.
  Does the "no crack at the seam" property survive a real split on that hardware?

### 🪞 4. self-play distillation — "teaching yourself from your own better guesses" (a HONEST no)

- **Plain**: the idea was to improve with **no outside teacher**, learning only
  from the model's own sharper outputs.
- **Analogy**: trying to get smarter by **re-reading your own essays** — with no
  new book.
- **Rehearsal 🔴 (closed-negative, reported honestly)**: the no-teacher part held
  (zero external help), but it **did not actually improve** on held-out data
  (delta −3.7e-6) — because the practice set was small enough to just memorize.
- **Why we keep it**: a clear "this path doesn't work *here*" is a real result, not
  a failure to hide. The OPEN question: try a **big, un-memorizable** corpus — only
  then can we know if self-teaching ever transfers.

```
   piece          rehearsal (sandbox)        real chip (still OPEN)
 ─────────────    ─────────────────────     ────────────────────────
  plasticity      🟢 GAIN 0.917/RETAIN 1.0   AKD1000 noisy low-bit learn?
  learn-while     🟢 z_drop 0.0/PROBE 1.0    live spike streams hold?
  MITOSIS         🟢 split seam 1.48e-7      fixed-cell-pool split holds?
  self-play       🔴 no held-out gain        un-memorizable corpus transfers?
```

---

## 🔗 How it chains forward — "rehearsal today, real exam next"

- Each piece's OPEN "real chip" question becomes the **next anima cycle's
  pre-registered test**. We freeze the sandbox result as the bar, then re-run it on
  silicon — the sandbox run is the *rehearsal*, the chip run is the *graded exam*.
- **Honesty gate**: a green rehearsal is **never** the final word here. Only a real
  chip run (or a clean negative) closes a piece. One question at a time, and a real
  claim needs a ladder of at least 3 rungs — no jumping from one toy result to a
  grand conclusion.

```
 [ hexa-lang FLAME-PERF ]      [ ONCHIP-PARADIGM (here) ]      [ chip-verify ]
   sandbox 🟢 / 🔴         ──▶   freeze as the falsifier    ──▶   AKD1000 run
   (the rehearsal)               (this domain's job)              (the real exam)
```

- **vs a normal research note**: most notes say "we got 🟢, done." This domain says
  "we got 🟢 *in rehearsal* — the chip still has to confirm it," and writes that
  open question down as the next job. The honesty is the point.

---

*Source of record: `ONCHIP-PARADIGM.tape` (+ `ONCHIP-PARADIGM.log.tape`). Host-half
provenance: hexa-lang FLAME-PERF PRs #2370 · #2373 · #2375 · #2376. This easy doc
restates them in plain language; the tape is authoritative for any discrepancy.*
