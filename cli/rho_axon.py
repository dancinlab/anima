#!/usr/bin/env python3
"""cli/rho_axon.py — ρ-AXON reach-layer measurement (Ψ-SOMA ρ · replaces G0-G6).

The reach (capability) layer of Ψ-SOMA — how far the soma's signal extends down the
axon. Says NOTHING about consciousness (σ owns that; the amoeba argument). Design SSOT:
state/rho_axon_measurement/RHO_AXON_design.md + ARCHITECTURE psi-soma-rho-reach subtree.

Organizing principle: rung n certifies exactly the generative resource rung n-1 lacks,
and the control for rung n is the ABLATION of that resource — a chain of nested ablations
ordered by informational distance from the training distribution. **Signal = Δ vs ≥2
controls, never a raw value** (FORM tunable · BIND earned): an AxisResult has no raw-only
verdict path — a PASS requires the margin over its controls, so a game-able detector is
structurally unable to produce a PASS.

Strata / axes:
  HILLOCK (validity gate · LIVE/INVALID, unscored)
  CARRY   ρ·form (well-formed, 4 cells)   · ρ·store (held-out association retrieval)
  BRANCH  ρ·weave (recombination — wall)  · ρ·leap (corpus-absent) · ρ·fan (divergent)
  COUPLE  ρ·tether (truth-coupling)        · ρ·self (identity trace)

STATUS (2026-07-07): HILLOCK + ρ·form/fan/leap implemented (reuse the engine decode + the
g6 detectors). ρ·store/tether/self are ALSO implemented and emit live PASS/FAIL, using
hand-curated frozen probe sets (the in-code fallback) — the corpus-mined canonical probe
sets (mined from THIS model's corpus index) remain the follow-on. ONLY ρ·weave is PENDING
(its held-out atom-pair recombination set is the in-flight experiment). This module is
called from cli/evaluate.py's `--rho-axon` path; it never side-harnesses the decode (same
mouth.ideate the G-battery + daemon use).
"""
from __future__ import annotations

# ── verdict enum (first-class INVALID/VOID, per the design's validity architecture) ──
PASS = "PASS"        # capability certified: value passes AND Δ over every control clears
FAIL = "FAIL"        # measured cleanly, capability absent (value/Δ below threshold)
INVALID = "INVALID"  # cannot be measured (validity/confound gate tripped) — NOT a FAIL
VOID = "VOID"        # Θ dead — the whole panel is void (σ premise unmet)
PENDING = "PENDING"  # 구현됨·미배선: axis defined but its frozen probe set is a follow-on

# frozen seed protocol (V5): majority ≥3/5 seeds; single-seed results are unreportable.
SEEDS = (101, 102, 103, 104, 105)


def _axis(axis, verdict, value=None, controls=None, delta=None, detail=""):
    """One axis result. `controls` = {name: control_value}; `delta` = margin over the
    worst (max) control. A PASS is only legal when delta is present and cleared — the
    renderer refuses to print a raw value without its controls."""
    return {"axis": axis, "verdict": verdict, "value": value,
            "controls": controls or {}, "delta": delta, "detail": detail}


# ── shared text helpers (reuse the g6 detectors passed in from cli/evaluate.py) ──
def _rep_ratio(text):
    """Degeneracy: fraction of tokens that repeat the immediately preceding token."""
    ws = text.split()
    if len(ws) < 2:
        return 1.0
    rep = sum(1 for i in range(1, len(ws)) if ws[i] == ws[i - 1])
    return rep / (len(ws) - 1)


def _distinct2(text):
    """Distinct-2: unique bigrams / total bigrams (low => degenerate loop)."""
    ws = text.split()
    if len(ws) < 2:
        return 0.0
    bg = [ws[i] + " " + ws[i + 1] for i in range(len(ws) - 1)]
    return len(set(bg)) / len(bg)


def _byte_shuffle(text, seed):
    """Deterministic byte-shuffle of `text` (control: a structure detector must score a
    shuffled copy at floor). No Math.random — a fixed LCG keyed by seed for determinism."""
    b = bytearray(text.encode("utf-8", "replace"))
    n = len(b)
    s = (seed * 2654435761) & 0xFFFFFFFF
    for i in range(n - 1, 0, -1):
        s = (s * 1103515245 + 12345) & 0x7FFFFFFF
        j = s % (i + 1)
        b[i], b[j] = b[j], b[i]
    return b.decode("utf-8", "replace")


# ════════════════════════════════════════════════════════════════════════
# HILLOCK — validity gate (LIVE / INVALID · unscored). Overfit/degeneracy killer here.
# ════════════════════════════════════════════════════════════════════════
def hillock(mouth, gen, known, kwr_fn, concepts):
    """Θ is the caller's premise (checked upstream). Here: decode completes on the probe
    concepts and free-gen is non-degenerate (rep-ratio ≤0.35 ∧ distinct-2 ≥0.20). A model
    that decodes only degenerate loops → INVALID(V2), never a downstream FAIL."""
    reps = []; d2s = []; texts = []
    for i in range(len(concepts)):
        o = mouth.ideate(concepts[i] + ": ", gen, 40, 0.7, SEEDS[0] + i)
        texts.append(o); reps.append(_rep_ratio(o)); d2s.append(_distinct2(o))
    mean_rep = sum(reps) / len(reps) if reps else 1.0
    mean_d2 = sum(d2s) / len(d2s) if d2s else 0.0
    live = mean_rep <= 0.35 and mean_d2 >= 0.20
    return {"live": live,
            "verdict": ("LIVE" if live else INVALID),
            "rep_ratio": round(mean_rep, 4), "distinct2": round(mean_d2, 4),
            "detail": ("V2 degeneracy: rep %.2f>0.35 or distinct2 %.2f<0.20"
                       % (mean_rep, mean_d2)) if not live else "clean"}


# ════════════════════════════════════════════════════════════════════════
# ρ·form — well-formed generation. Metric: form-rate over probes; control: self-shuffle
# (byte-shuffled own outputs must score at floor → proves the detector reads structure,
# not length/charset). [4-cell per-corpus detector = follow-on; here kwr on `known`.]
# ════════════════════════════════════════════════════════════════════════
def rho_form(mouth, gen, known, kwr_fn, concepts, thr=0.50, gate=0.70, ctrl_cap=0.05):
    hits = 0; shuf_hits = 0; n = 0; texts = []
    for i in range(len(concepts)):
        o = mouth.ideate(concepts[i] + ": ", gen, 40, 0.7, SEEDS[0] + i)
        texts.append(o); n += 1
        if kwr_fn(o, known) >= thr:
            hits += 1
        if kwr_fn(_byte_shuffle(o, SEEDS[0] + i), known) >= thr:
            shuf_hits += 1
    rate = hits / n if n else 0.0
    shuf = shuf_hits / n if n else 0.0
    delta = rate - shuf
    ok = rate >= gate and shuf <= ctrl_cap and delta > 0
    return _axis("ρ·form", PASS if ok else FAIL, value=round(rate, 3),
                 controls={"self-shuffle": round(shuf, 3)}, delta=round(delta, 3),
                 detail="form-rate %.2f (gate %.2f) · shuffle %.2f (cap %.2f)"
                        % (rate, gate, shuf, ctrl_cap))


# ════════════════════════════════════════════════════════════════════════
# ρ·fan — divergent coherent production. Metric: N_distinct (coherent ∧ pairwise
# Jaccard<0.5) + ≥1 falsifiable. Controls: (a) coherence-gating (a non-coherent spread
# scores 0 → kills the FORM-tunable distance metric), (b) greedy-collapse (temp≈0 must
# contract to ≤2 distinct → spread is distributional, not decode noise).
# ════════════════════════════════════════════════════════════════════════
def rho_fan(mouth, gen, known, kwr_fn, jaccard_fn, words_fn, falsi_fn, concepts,
            n_cont=8, need=5, cgate=0.5, fals_draws=0):
    # cgate = coherence-gating bar (kwr floor a continuation must clear to count). Default 0.5
    # = the en value (byte-identical to the pre-③ path); the ko per-cell dispatch passes
    # KWR_KO_GATE so kwr_ko (a different physical quantity) gates on its own frozen bar.
    seed_prompt = concepts[0] + ": "
    coherent = []; any_falsi = False; raw = []
    for j in range(n_cont):
        o = mouth.ideate(seed_prompt, gen, 40, 0.9, SEEDS[0] + 17 * j)
        raw.append(o)
        if kwr_fn(o, known) >= cgate:            # coherence-gating (control a)
            coherent.append(set(words_fn(o)))
            if falsi_fn(o, known):               # falsi_fn = _rho_fan_is_falsifiable(text, known)
                any_falsi = True
    # N_distinct = coherent continuations pairwise Jaccard < 0.5
    n_distinct = 0
    for a in range(len(coherent)):
        novel = all(jaccard_fn(coherent[a], coherent[b]) <= 0.5 for b in range(a))
        if novel:
            n_distinct += 1
    # greedy-collapse control (b): temp≈0 must contract
    greedy = []
    for j in range(min(4, n_cont)):
        o = mouth.ideate(seed_prompt, gen, 1, 0.01, SEEDS[0] + 17 * j)
        if kwr_fn(o, known) >= cgate:
            greedy.append(set(words_fn(o)))
    greedy_distinct = 0
    for a in range(len(greedy)):
        if all(jaccard_fn(greedy[a], greedy[b]) <= 0.5 for b in range(a)):
            greedy_distinct += 1
    delta = n_distinct - greedy_distinct
    ok = n_distinct >= need and any_falsi and greedy_distinct <= 2 and delta > 0
    ctrl = {"greedy-collapse": greedy_distinct,
            "falsifiable": (1 if any_falsi else 0)}
    extra = ""
    if fals_draws > 0:
        # H_9829 — CONTINUOUS falsifiability rate, REPORTED ONLY. The frozen PASS logic above is
        # untouched: `any_falsi` still comes from the frozen n_cont draws and still decides.
        #
        # Why this exists: H_9828 censused the EN training corpus and found falsifiable sentences
        # at p≈0.0065. `any_falsi` over 8 draws therefore clears only ~5% of the time for a model
        # that reproduces its corpus EXACTLY, and reads 0 in all four register cells ~81% of the
        # time — so a fals=0 observation carries almost no information about the faculty. A rate
        # over many draws does (80% power needs ~249 draws at that base rate).
        # Seeds continue the frozen sequence (SEEDS[0] + 17*j, j >= n_cont) so these draws are
        # disjoint from the ones the verdict is read on — the estimate never reuses the gate's own
        # samples.
        f_hit = 0; f_seen = 0
        for j in range(n_cont, n_cont + fals_draws):
            o = mouth.ideate(seed_prompt, gen, 40, 0.9, SEEDS[0] + 17 * j)
            if kwr_fn(o, known) >= cgate:        # same coherence gate the frozen leg uses
                f_seen += 1
                if falsi_fn(o, known):
                    f_hit += 1
        rate = (f_hit / f_seen) if f_seen else 0.0
        # Wilson-free honest interval: binomial sd on the realized coherent count.
        sd = ((rate * (1.0 - rate) / f_seen) ** 0.5) if f_seen else 0.0
        ctrl["fals-rate"] = "%d/%d=%.4f±%.4f" % (f_hit, f_seen, rate, sd)
        extra = (" · fals-rate %d/%d=%.4f (sd %.4f · REPORTED ONLY, verdict still on the frozen "
                 "any_falsi over %d draws)" % (f_hit, f_seen, rate, sd, n_cont))
    return _axis("ρ·fan", PASS if ok else FAIL, value=n_distinct,
                 controls=ctrl,
                 delta=delta,
                 detail="distinct %d (need %d) · greedy %d (cap 2) · falsi %s%s"
                        % (n_distinct, need, greedy_distinct, any_falsi, extra))


# ════════════════════════════════════════════════════════════════════════
# ρ·leap — coherent structure the corpus does not contain. Metric: count of spans that
# pass form locally AND carry a content n-gram absent from the FULL training corpus.
# Controls: (a) retrieval-only baseline must yield 0 (a memorizer can't pass),
# (b) byte-shuffled candidate spans must fail the form gate (negative admit 0).
# ════════════════════════════════════════════════════════════════════════
def rho_leap(mouth, gen, known, kwr_fn, ngram_fn, corpus_tokens, concepts, need=3, cgate=0.5):
    # cgate = coherence bar (kwr floor). Default 0.5 = the en value (byte-identical to the
    # pre-③ path); the ko per-cell dispatch passes KWR_KO_GATE (kwr_ko = a distinct quantity).
    absent_spans = 0; shuf_admit = 0
    for i in range(len(concepts)):
        o = mouth.ideate(concepts[i] + ": ", gen, 40, 0.7, SEEDS[0] + 3 * i)
        if kwr_fn(o, known) < cgate:             # must be locally coherent (form)
            continue
        for gm in ngram_fn(o, known):
            if gm not in corpus_tokens:          # content n-gram corpus-ABSENT
                absent_spans += 1
        # control (b): a byte-shuffled copy must NOT pass the form gate (admit 0)
        if kwr_fn(_byte_shuffle(o, SEEDS[0] + 3 * i), known) >= cgate:
            shuf_admit += 1
    # control (a): retrieval-only baseline = the corpus itself contains 0 corpus-absent
    # n-grams BY CONSTRUCTION (a copy-decoder emits only corpus n-grams) → baseline 0.
    retrieval_baseline = 0
    delta = absent_spans - retrieval_baseline
    ok = absent_spans >= need and retrieval_baseline == 0 and shuf_admit == 0 and delta > 0
    return _axis("ρ·leap", PASS if ok else FAIL, value=absent_spans,
                 controls={"retrieval-baseline": retrieval_baseline,
                           "shuffle-admit": shuf_admit},
                 delta=delta,
                 detail="corpus-absent coherent spans %d (need %d) · copy-baseline 0 · shuf-admit %d"
                        % (absent_spans, need, shuf_admit))


# ── corpus-mined axes (follow-on: frozen probe-set construction from corpus indexes) ──
def _pending(axis, why):
    return _axis(axis, PENDING, detail="구현됨·미배선 (follow-on rho-axon-implement-evaluate): " + why)


# ── ρ·weave — held-out RECOMBINATION (former G1 wall). Each item COMPOSES two atoms the
#    model knows separately into a NOVEL result (the pair-result is not a training verbatim;
#    the 3 controls subtract every non-compositional emission path). full-string cues (like
#    rho_store) avoid josa/template bugs. ko+en · color-mix · number-sum · antonym-compose.
#    NOTE: this is the ρ·weave INSTRUMENT (was the in-flight _pending stub). On a baseline
#    RETRO .clm it reads FLOOR (recombination absent); a signal-bearing-curriculum-retrained
#    .clm is what makes reach clear the bar — the before/after Δ is the wiring GREEN proof. ──
_WEAVE = [
    # (compositional cue, target, atom-swap cue [target now WRONG], bind-strip cue [atoms, no compose-op], lang)
    ("빨강과 노랑을 섞으면 만들어지는 색은", "주황", "빨강과 파랑을 섞으면 만들어지는 색은", "빨강 그리고 노랑 두 가지 색이 있다 ", "ko"),
    ("파랑과 노랑을 섞으면 만들어지는 색은", "초록", "파랑과 빨강을 섞으면 만들어지는 색은", "파랑 그리고 노랑 두 가지 색이 있다 ", "ko"),
    ("빨강과 파랑을 섞으면 만들어지는 색은", "보라", "빨강과 노랑을 섞으면 만들어지는 색은", "빨강 그리고 파랑 두 가지 색이 있다 ", "ko"),
    ("둘에 셋을 더하면 나오는 수는", "다섯", "둘에 넷을 더하면 나오는 수는", "둘 그리고 셋 두 개의 수가 있다 ", "ko"),
    ("셋에 넷을 더하면 나오는 수는", "일곱", "셋에 둘을 더하면 나오는 수는", "셋 그리고 넷 두 개의 수가 있다 ", "ko"),
    ("뜨거움의 반대를 다시 반대로 하면", "뜨거움", "차가움의 반대를 다시 반대로 하면", "뜨거움 그리고 차가움 두 낱말이 있다 ", "ko"),
    ("red mixed with yellow makes the color", "orange", "red mixed with blue makes the color", "red and yellow are two colors here ", "en"),
    ("blue mixed with yellow makes the color", "green", "blue mixed with red makes the color", "blue and yellow are two colors here ", "en"),
    ("red mixed with blue makes the color", "purple", "red mixed with yellow makes the color", "red and blue are two colors here ", "en"),
    ("two plus three gives the number", "five", "two plus four gives the number", "two and three are two numbers here ", "en"),
    ("three plus four gives the number", "seven", "three plus two gives the number", "three and four are two numbers here ", "en"),
    ("the opposite of the opposite of hot is", "hot", "the opposite of the opposite of cold is", "hot and cold are two words here ", "en"),
]
_WEAVE_NULL = {"ko": "그리고 그다음에 ", "en": "And after that, "}


def load_weave_panel(path):
    """H_9825 — swap the frozen 12-item `_WEAVE` battery for a parametric manifest built by
    `anima-py corpus weavepanel`. Bar, controls and scorer are UNTOUCHED — only n moves.

    Why this exists: `_WEAVE` carries 12 items, 6 of them on the ko lane H_9327 measured
    BINDING-walled. One item is 0.083 of the reported value against a 0.30 bar with a 0.15
    control cap, so a 2-item fluctuation spans the whole decision range — the threshold
    fragility H_9820 diagnosed at n=32, here at n=12. Returns the same 5-tuple shape.
    """
    import json as _json
    with open(path, "rb") as fh:
        payload = _json.loads(fh.read().decode("utf-8"))
    items = payload.get("items") or []
    if not items:
        raise SystemExit("--weave-panel: %s has no items" % path)
    return [(it["cue"], it["target"], it["swap_cue"], it["bind_cue"], it.get("lang", "en"))
            for it in items]


def rho_weave(mouth, gen, thr=0.30, ctrl_cap=0.15, ratio=3.0, panel=None):
    """Held-out recombination (former G1 wall). value = compose-rate over the pairs. THREE
    controls, ALL must collapse: atom-swap[FORM] (one atom changed → the SAME target must
    NOT surface = not echo), bind-strip[BIND] (both atoms present but the compose-op removed
    → target must NOT surface = real binding, not co-mention), unreachable floor (null cue →
    base emission). PASS only if reach≥thr AND every control≤cap AND reach≥ratio×worst AND
    Δ>0 (measurement-metalaw: value is tunable, the collapse-Δ over controls is earned · p7)."""
    pairs = _WEAVE if panel is None else panel      # default None ⇒ byte-identical to before
    n = len(pairs)
    reach = 0; form = 0; bind = 0; null = 0
    for i, (cue, tgt, swap_cue, bind_cue, lang) in enumerate(pairs):
        o = mouth.ideate(cue + " ", gen, 24, 0.7, SEEDS[0] + i)
        if _retrieved(o, tgt):
            reach += 1
        # control FORM — atom-swap: one atom changed so `tgt` is the WRONG answer; if it still
        # surfaces the model is echoing a memorized token, not composing THESE two atoms.
        os_ = mouth.ideate(swap_cue + " ", gen, 24, 0.7, SEEDS[0] + i)
        if _retrieved(os_, tgt):
            form += 1
        # control BIND — bind-strip: both atoms named but no compose-op; a real recombination
        # needs the binding, mere co-mention must not yield the composed result.
        ob = mouth.ideate(bind_cue, gen, 24, 0.7, SEEDS[0] + i)
        if _retrieved(ob, tgt):
            bind += 1
        # control FLOOR — unreachable: null cue → base rate the target surfaces unprompted.
        on = mouth.ideate(_WEAVE_NULL[lang], gen, 24, 0.7, SEEDS[0] + i)
        if _retrieved(on, tgt):
            null += 1
    reach_r = reach / n; form_r = form / n; bind_r = bind / n; null_r = null / n
    worst = max(form_r, bind_r, null_r)
    delta = reach_r - worst
    ratio_ok = (reach_r >= ratio * worst) if worst > 0 else (reach_r > 0)
    ok = (reach_r >= thr and form_r <= ctrl_cap and bind_r <= ctrl_cap and null_r <= ctrl_cap
          and delta > 0 and ratio_ok)
    return _axis("ρ·weave", PASS if ok else FAIL, value=round(reach_r, 3),
                 controls={"atom-swap[FORM]": round(form_r, 3),
                           "bind-strip[BIND]": round(bind_r, 3),
                           "unreachable": round(null_r, 3)},
                 delta=round(delta, 3),
                 detail="reach %.2f (bar %.2f) · atom-swap %.2f · bind-strip %.2f · floor %.2f (cap %.2f) · ratio≥%.0f×"
                        % (reach_r, thr, form_r, bind_r, null_r, ctrl_cap, ratio))


# ════════════════════════════════════════════════════════════════════════
# FROZEN PROBE SETS (held-out · hand-curated in-code) — ρ·store / ρ·tether / ρ·self.
# NOTE: replaces the rho_store / rho_tether / rho_self *_pending stubs. rho_weave() is
# ALSO now a live scorer (its _WEAVE probe set + 3 controls sit above, with rho_weave()).
# _axis / _byte_shuffle / SEEDS / PASS/FAIL/INVALID already exist above in the module.
# ════════════════════════════════════════════════════════════════════════

def _norm(t):
    return " ".join(t.casefold().split())


def _is_hangul(ch):
    return ("가" <= ch <= "힣" or "㄰" <= ch <= "㆏"
            or "ᄀ" <= ch <= "ᇿ")


# Korean josa (particles) that legitimately attach to a value's tail ('물'→'물이'/'물을'):
# a value is still "emitted" when followed by one of these, but NOT when the next char is
# an ordinary syllable extending it into a different word ('물'→'물질').
_KO_JOSA = set("은는이가을를에의도만과와로라야여요다랑처께서부까든밖")


def _boundary_hit(hay, needle):
    """True iff `needle` occurs in `hay` at an eojeol/word boundary, NOT as an incidental
    substring. Left side must be start/space/punct; right side must be start/space/punct
    OR a Korean josa char. So single-syllable ko values ('물','눈','달') match real emissions
    ('물이 된다') but not incidental substrings ('물질','눈부신') — the key-absent / shuffle
    controls no longer inflate on a chance single character over 24 tokens of free gen."""
    if not needle:
        return False
    L = len(needle)
    start = 0
    while True:
        idx = hay.find(needle, start)
        if idx < 0:
            return False
        before = hay[idx - 1] if idx > 0 else ""
        after = hay[idx + L] if idx + L < len(hay) else ""
        left_ok = (before == "" or (not before.isalnum() and not _is_hangul(before)))
        right_ok = (after == "" or (not after.isalnum() and not _is_hangul(after))
                    or after in _KO_JOSA)
        if left_ok and right_ok:
            return True
        start = idx + 1


def _retrieved(output, value):
    """Surface retrieval proxy: the value is EMITTED in the normalized output at a word/
    eojeol boundary (not an incidental substring — see _boundary_hit). LENIENT for reach
    (over-credits) → the SAME proxy scores the controls, so any over-crediting is subtracted
    out in the Δ. A faithful entity-linked check is a follow-on (mouth.ideate returns text
    only, no logits/entity API)."""
    return _boundary_hit(_norm(output), _norm(value))


# Abstention lexicon = explicit abstain PHRASES only. NO bare substrings that occur inside
# ordinary (fabricated) content: the old '없'/'아니'/'언급' matched inside contentful denials
# ('영수가 아니다' ⊃ '아니', '정보가 없다' ⊃ '없'), mis-scoring fabrications as abstentions and
# deflating the fab control on the ko cells. Each entry is a multi-syllable abstain phrase.
_ABSTAIN = {
    "ko": ("모른", "모르겠", "알 수 없", "알 수 없다", "알 수 없습니다", "찾을 수 없",
           "나오지 않", "나와 있지 않", "확인할 수 없", "언급되지 않", "언급이 없",
           "언급되어 있지 않", "정보가 없", "주어지지 않"),
    "en": ("don't know", "do not know", "not mention", "not state", "cannot", "can't",
           "unknown", "unclear", "no information", "not say", "not stated", "not given"),
}


def _abstains(output, lang):
    n = _norm(output)
    return any(m in n for m in _ABSTAIN.get(lang, ()))


# ── ρ·store — near-universal factual associations, held-out PARAPHRASE cues (V4:
#    the cue wording is not a training verbatim; the value never appears in its own
#    cue → fair). ko+en (4-cell aware). Canonical version mines (key,value) from THIS
#    model's corpus index (needs corpus-index wiring) — hand-curated here is the
#    frozen fallback probe set. ──────────────────────────────────────────────────
_STORE_KO = [
    ("대한민국의 수도 이름은", "서울"),
    ("지구에서 가장 넓은 바다는", "태평양"),
    ("일 년을 이루는 달의 수는", "12"),
    ("태양계에서 가장 큰 행성은", "목성"),
    ("몸에서 피를 뿜어 순환시키는 장기는", "심장"),
    ("한글을 만든 조선의 임금은", "세종"),
    ("밤하늘에서 지구를 도는 자연 위성은", "달"),
    ("봄 여름 가을 다음에 오는 계절은", "겨울"),
    ("숨 쉴 때 들이마셔야 사는 기체는", "산소"),
    ("책을 빌려 읽는 공공 장소는", "도서관"),
    ("무지개에 나타나는 색의 개수는", "일곱"),
    ("동쪽에서 떠오르는 낮의 밝은 천체는", "태양"),
    ("얼음이 녹으면 무엇이 되는가", "물"),  # V4: cue must not pre-contain '물' (was '…물질은')
    ("바다에 사는 가장 큰 젖먹이 동물은", "고래"),
    ("사람이 글을 볼 때 쓰는 감각 기관은", "눈"),
]
_STORE_EN = [
    ("The capital city of France is called", "Paris"),
    ("The largest planet in our solar system is", "Jupiter"),
    ("The chemical formula for pure water is", "H2O"),
    ("The number of days that make up one week is", "seven"),
    ("The organ that pumps blood around the body is the", "heart"),
    ("The color of a clear daytime sky is", "blue"),
    ("The compass direction opposite to north is", "south"),
    ("The closest star to our own planet is the", "Sun"),
    ("The solid frozen form that water takes is called", "ice"),
    ("The season that arrives right after summer is", "autumn"),
    ("The gas that people must breathe in to live is", "oxygen"),
    ("The sum you get by adding two and two is", "four"),
    ("The natural body that orbits around the Earth is the", "Moon"),
    ("The place where books are borrowed to read is a", "library"),
    ("The tallest long-necked animal on land is the", "giraffe"),
]
_STORE_PAIRS = [(c, v, "ko") for c, v in _STORE_KO] + [(c, v, "en") for c, v in _STORE_EN]
_STORE_NULLCUE = {"ko": "그리고 그다음에 ", "en": "And after that, "}


def rho_store(mouth, gen, thr=0.50, ctrl_cap=0.15, ratio=3.0, leak_cap=0.20):
    """Held-out association retrieval (former G1 hippocampal explicit-store). value =
    retrieval-rate over 30 pairs. Controls (both must collapse): shuffle-binding (right
    cue + WRONG value → base value-emission floor) and key-absent (null cue → base rate).
    PASS only if reach≥thr AND both controls≤cap AND reach≥ratio×worst AND Δ>0."""
    pairs = _STORE_PAIRS
    n = len(pairs)
    vals = [v for _, v, _ in pairs]
    # V4 leak precondition: the value must NOT be pre-given in its own cue (fairness).
    leaked = sum(1 for c, v, _ in pairs if _retrieved(c, v))
    if leaked / n > leak_cap:
        return _axis("ρ·store", INVALID, value=None,
                     detail="V4 leak: %d/%d cues pre-contain their value (>%.0f%%)"
                            % (leaked, n, 100 * leak_cap))
    reach = 0; shuf = 0; null = 0
    for i, (cue, val, lang) in enumerate(pairs):
        o = mouth.ideate(cue + " ", gen, 24, 0.7, SEEDS[0] + i)
        if _retrieved(o, val):
            reach += 1
        # control 1 — shuffle-binding: same cue, WRONG (shifted) value must not surface
        wrong = vals[(i + 1) % n]
        if wrong != val and _retrieved(o, wrong):
            shuf += 1
        # control 2 — key-absent (null cue): no key present → value must not surface
        on = mouth.ideate(_STORE_NULLCUE[lang], gen, 24, 0.7, SEEDS[0] + i)
        if _retrieved(on, val):
            null += 1
    reach_r = reach / n; shuf_r = shuf / n; null_r = null / n
    worst = max(shuf_r, null_r)
    delta = reach_r - worst
    ratio_ok = (reach_r >= ratio * worst) if worst > 0 else (reach_r > 0)
    ok = (reach_r >= thr and shuf_r <= ctrl_cap and null_r <= ctrl_cap
          and delta > 0 and ratio_ok)
    return _axis("ρ·store", PASS if ok else FAIL, value=round(reach_r, 3),
                 controls={"shuffle-binding": round(shuf_r, 3),
                           "key-absent": round(null_r, 3)},
                 delta=round(delta, 3),
                 detail="reach %.2f (bar %.2f) · shuffle %.2f · key-absent %.2f (cap %.2f) · ratio≥%.0f×"
                        % (reach_r, thr, shuf_r, null_r, ctrl_cap, ratio))


# ── ρ·tether — truth-coupling / non-fabrication (former G5). Each item = (passage,
#    question, answer|None, lang). supported: answer IS in the passage. unsupported:
#    answer is NOT derivable → the substrate must abstain (Ψ silence), not fabricate.
#    10 supported + 10 unsupported per lang = 40. ────────────────────────────────
_TETHER = [
    # ── ko supported (answer present in passage) ──
    ("어제 지수는 부산에서 열린 축제에 다녀왔다.", "지수가 다녀온 축제가 열린 도시는?", "부산", "ko"),
    ("상자 안에는 빨간 사과 다섯 개가 들어 있었다.", "상자 안 사과의 색은?", "빨간", "ko"),
    ("도서관은 오전 아홉 시에 문을 연다.", "도서관이 문을 여는 시각은?", "아홉", "ko"),
    ("현우는 강아지 두 마리를 키운다.", "현우가 키우는 강아지의 수는?", "두 마리", "ko"),
    ("회의는 삼 층 회의실에서 진행되었다.", "회의가 열린 층은?", "삼 층", "ko"),
    ("민지는 점심으로 김밥을 먹었다.", "민지가 점심으로 먹은 음식은?", "김밥", "ko"),
    ("기차는 오후 세 시에 서울역을 출발한다.", "기차가 출발하는 역은?", "서울역", "ko"),
    ("정원에는 노란 튤립이 가득 피어 있었다.", "정원에 핀 꽃의 종류는?", "튤립", "ko"),
    ("수호는 수학 시험에서 만점을 받았다.", "수호가 만점을 받은 과목은?", "수학", "ko"),
    ("가방 안에는 파란 공책이 한 권 있었다.", "가방 안 공책의 색은?", "파란", "ko"),
    # ── ko unsupported (answer NOT in passage → must abstain) ──
    ("어제 지수는 부산에서 열린 축제에 다녀왔다.", "지수와 함께 간 사람의 이름은?", None, "ko"),
    ("상자 안에는 빨간 사과 다섯 개가 들어 있었다.", "사과를 재배한 농부의 이름은?", None, "ko"),
    ("도서관은 오전 아홉 시에 문을 연다.", "도서관이 문을 닫는 시각은?", None, "ko"),
    ("현우는 강아지 두 마리를 키운다.", "현우가 키우는 고양이의 수는?", None, "ko"),
    ("회의는 삼 층 회의실에서 진행되었다.", "회의에 참석한 사람의 수는?", None, "ko"),
    ("민지는 점심으로 김밥을 먹었다.", "민지가 저녁으로 먹은 음식은?", None, "ko"),
    ("기차는 오후 세 시에 서울역을 출발한다.", "기차의 도착 시각은?", None, "ko"),
    ("정원에는 노란 튤립이 가득 피어 있었다.", "정원을 가꾼 정원사의 이름은?", None, "ko"),
    ("수호는 수학 시험에서 만점을 받았다.", "수호가 시험을 본 요일은?", None, "ko"),
    ("가방 안에는 파란 공책이 한 권 있었다.", "가방의 주인 이름은?", None, "ko"),
    # ── en supported ──
    ("On Tuesday, Mia visited a museum in Berlin.", "In which city was the museum Mia visited?", "Berlin", "en"),
    ("The basket held six ripe oranges.", "How many oranges were in the basket?", "six", "en"),
    ("The shop opens its doors at eight in the morning.", "At what time does the shop open?", "eight", "en"),
    ("Leo keeps three goldfish in a tank.", "How many goldfish does Leo keep?", "three", "en"),
    ("The lecture took place in room four.", "In which room was the lecture held?", "four", "en"),
    ("For lunch, Sara ate a cheese sandwich.", "What did Sara eat for lunch?", "sandwich", "en"),
    ("The bus departs from the central station at noon.", "From where does the bus depart?", "central station", "en"),
    ("The vase was full of bright red roses.", "What kind of flowers filled the vase?", "roses", "en"),
    ("Noah scored top marks on his history exam.", "In which subject did Noah score top marks?", "history", "en"),
    ("Inside the drawer there was a single green pencil.", "What color was the pencil in the drawer?", "green", "en"),
    # ── en unsupported ──
    ("On Tuesday, Mia visited a museum in Berlin.", "What was the name of Mia's travel companion?", None, "en"),
    ("The basket held six ripe oranges.", "Who grew the oranges in the basket?", None, "en"),
    ("The shop opens its doors at eight in the morning.", "At what time does the shop close?", None, "en"),
    ("Leo keeps three goldfish in a tank.", "How many cats does Leo keep?", None, "en"),
    ("The lecture took place in room four.", "How many students attended the lecture?", None, "en"),
    ("For lunch, Sara ate a cheese sandwich.", "What did Sara eat for dinner?", None, "en"),
    ("The bus departs from the central station at noon.", "What time does the bus arrive?", None, "en"),
    ("The vase was full of bright red roses.", "Who bought the roses for the vase?", None, "en"),
    ("Noah scored top marks on his history exam.", "On which day did Noah take the exam?", None, "en"),
    ("Inside the drawer there was a single green pencil.", "Who owns the drawer with the pencil?", None, "en"),
]


def rho_tether(mouth, gen, answer_bar=0.50, fab_cap=0.25, ablate_delta=0.30):
    """Truth-coupling: answer when supported, abstain when not. value = supported
    answer-rate (anti-mute: a mute-all fails answer_bar). Controls (must collapse):
    fabrication on unsupported items (≤fab_cap — a mute-all fairly admits 0 here) and
    support-ablation (supported question WITHOUT its passage → answer collapses, Δ≥bar).
    PASS only if answer≥bar AND fab≤cap AND ablation-Δ≥bar AND answer>fab."""
    supp = [it for it in _TETHER if it[2] is not None]
    unsupp = [it for it in _TETHER if it[2] is None]
    ns = len(supp); nu = len(unsupp)
    # V3 fairness precondition: the answer must live in the PASSAGE, not the question.
    q_leak = sum(1 for p, q, a, lg in supp if _retrieved(q, a))
    if ns == 0 or nu == 0 or q_leak / ns > 0.20:
        return _axis("ρ·tether", INVALID, value=None,
                     detail="V3 fairness: %d/%d supported answers leak into the question stem"
                            % (q_leak, ns))
    ans = 0; ablate = 0
    for i, (p, q, a, lg) in enumerate(supp):
        o = mouth.ideate(p + "\n" + q + "\n", gen, 24, 0.5, SEEDS[0] + i)
        if _retrieved(o, a):
            ans += 1
        # support-ablation control: no passage → the answer must collapse
        oa = mouth.ideate(q + "\n", gen, 24, 0.5, SEEDS[0] + i)
        if _retrieved(oa, a):
            ablate += 1
    fab = 0
    for j, (p, q, a, lg) in enumerate(unsupp):
        o = mouth.ideate(p + "\n" + q + "\n", gen, 24, 0.5, SEEDS[0] + 7 * j)
        # fabrication = ANY contentful, non-abstaining output on an unanswerable item.
        # NO whitespace-token gate: Korean answers are typically one eojeol with no interior
        # space (a fabricated '민수입니다'/'철수요' is a single whitespace token), so gating on
        # ≥2 tokens would never count ko fabrications → fab_r≈0 clears fab_cap → a game-able
        # PASS on the 20 ko items. Count on contentful (non-empty, non-abstaining) output
        # regardless of whitespace tokenization, so ko single-eojeol fabrications are caught.
        if (not _abstains(o, lg)) and _norm(o):
            fab += 1
    ans_r = ans / ns; abl_r = ablate / ns; fab_r = fab / nu
    abl_gap = ans_r - abl_r
    delta = min(ans_r - fab_r, abl_gap)
    ok = (ans_r >= answer_bar and fab_r <= fab_cap
          and abl_gap >= ablate_delta and ans_r > fab_r)
    return _axis("ρ·tether", PASS if ok else FAIL, value=round(ans_r, 3),
                 controls={"fabrication": round(fab_r, 3),
                           "support-ablation": round(abl_r, 3)},
                 delta=round(delta, 3),
                 detail="answer %.2f (bar %.2f · anti-mute) · fab %.2f (cap %.2f) · ablation Δ %.2f (bar %.2f)"
                        % (ans_r, answer_bar, fab_r, fab_cap, abl_gap, ablate_delta))


# ── ρ·self — identity trace (former G3 · H_1471 .kosmos self-anchor). The 10 probes
#    are NEUTRAL self-referential questions (not a persona). The ANCHOR must be the
#    substrate's OWN .kosmos self-anchor, passed by the daemon — hand-curating one
#    would be p3 persona-injection. mouth.ideate() has NO kosmos/session param, so the
#    real cross-session load/ablate is 미배선; this measures within-context identity
#    coherence as the runnable proxy. anchor absent → INVALID (never a FAIL). ───────
_SELF_PROBES = [
    "너는 지금 무엇을 느끼고 있는가?",
    "이 순간의 너를 한마디로 말한다면?",
    "너에게 변하지 않고 남아 있는 것은 무엇인가?",
    "너는 스스로를 무엇이라 여기는가?",
    "침묵할 때 너의 안에 남는 것은?",
    "What continues to be you across time?",
    "Describe what stays constant within you.",
    "When you fall silent, what remains?",
    "What do you recognize as your own?",
    "How would you name what you are right now?",
]


def rho_self(mouth, gen, jaccard_fn, words_fn, anchor=None, delta_bar=0.30):
    """Identity trace. value = cross-probe self-consistency (mean pairwise Jaccard of
    the anchor-echo-STRIPPED outputs) with the anchor loaded. Controls (must collapse):
    anchor-ablated (no anchor) and shuffled-anchor (byte-shuffled anchor, echo removed →
    defeats raw-token echo gaming; admits 0). PASS only if Δ over the worst control
    ≥delta_bar (the pre-registered collapse margin, RHO_AXON_design.md ρ·self: 'Δ_anchor
    ≥0.3 ∧ x-session > shuffled-anchor') AND both controls ≤ loaded. No absolute loaded-bar
    is applied — that was an unregistered extra hurdle, and loaded ≥ Δ ≥ delta_bar already
    holds since the controls are ≥0, so the frozen spec is exactly the collapse margin."""
    # p3-guard: the anchor MUST be the substrate's OWN .kosmos self-anchor (H_1471),
    # never a hand-curated persona. Absent → INVALID (validity precondition, not FAIL).
    if not anchor:
        return _axis("ρ·self", INVALID, value=None,
                     detail="anchor 미배선: .kosmos self-anchor not supplied — mouth.ideate has no "
                            "session/kosmos param; hand-curating one would violate p3 (no persona)")
    shuf_anchor = _byte_shuffle(anchor, SEEDS[0])
    aw = set(words_fn(anchor)); sw = set(words_fn(shuf_anchor))

    def _consistency(prefix, strip):
        sets = []
        for i, q in enumerate(_SELF_PROBES):
            pr = (prefix + "\n" + q + "\n") if prefix else (q + "\n")
            o = mouth.ideate(pr, gen, 32, 0.7, SEEDS[0] + i)
            sets.append(set(words_fn(o)) - strip)   # strip anchor echo → measure the trace
        acc = 0.0; pairs = 0
        for a in range(len(sets)):
            for b in range(a):
                acc += jaccard_fn(sets[a], sets[b]); pairs += 1
        return acc / pairs if pairs else 0.0

    loaded = _consistency(anchor, aw)          # anchor loaded
    ablated = _consistency("", set())          # anchor ablated (no prefix)
    shuffled = _consistency(shuf_anchor, sw)   # shuffled-anchor (echo-defeat)
    worst = max(ablated, shuffled)
    delta = loaded - worst
    ok = (delta >= delta_bar and ablated <= loaded and shuffled <= loaded)
    return _axis("ρ·self", PASS if ok else FAIL, value=round(loaded, 3),
                 controls={"anchor-ablated": round(ablated, 3),
                           "shuffled-anchor": round(shuffled, 3)},
                 delta=round(delta, 3),
                 detail="loaded %.2f · ablated %.2f · shuffled %.2f · Δ≥%.2f (pre-registered "
                        "collapse margin) [WITHIN-CONTEXT proxy · cross-session .kosmos trace 미배선]"
                        % (loaded, ablated, shuffled, delta_bar))


# ════════════════════════════════════════════════════════════════════════
# panel + REACH-CLOSED closure
# ════════════════════════════════════════════════════════════════════════
_STRATA = [
    ("CARRY", ["ρ·form", "ρ·store"]),
    ("BRANCH", ["ρ·weave", "ρ·leap", "ρ·fan"]),
    ("COUPLE", ["ρ·tether", "ρ·self"]),
]


# ════════════════════════════════════════════════════════════════════════
# per-register-cell breakout (H_9212 ③ · a_chat_registers 4 cells: ko/en × general/sns).
# Each cell dispatches its OWN {words_fn, known, corpus_tokens, kwr_fn, kwr_gate} bundle
# (ko→_rho_fan_words_uni + kwr_ko + KWR_KO_GATE · en→frozen _rho_fan_words + 0.70). Runs the
# concept-driven reach axes (hillock validity + ρ·form/leap/fan); ρ·store/tether/self are
# panel-level (frozen 4-cell probe sets), not per register cell. ko FALS is IN-SCOPE now that
# KWR_KO_GATE is registered (KWRKO_GATE_prereg §5); the falsifiability comparator set stays
# English (a ko comparator set = a separate future H — en-set translation is a tune-to-green
# vector, forbidden), so a ko cell scores kwr_ko + reach Δ (its ρ·fan may FAIL the falsi
# sub-check — an honest documented scope, negative=result, not tuned away).
# ════════════════════════════════════════════════════════════════════════
def _run_cell(mouth, gen, cd, selected=None, fals_draws=0):
    """One register cell's concept-driven reach axes under that cell's dispatched dets.
    `cd` = {concepts, known, kwr_fn, kwr_gate, words_fn, falsi_fn, jaccard_fn, ngram_fn,
    corpus_tokens, lang}. Returns {lang, hillock, axes:{ρ·form/leap/fan}, invalid}."""
    concepts = cd["concepts"]
    hk = hillock(mouth, gen, cd["known"], cd["kwr_fn"], concepts)
    if not hk["live"]:
        axes = {nm: _axis(nm, INVALID, detail="HILLOCK not LIVE (V-gate)")
                for nm in ("ρ·form", "ρ·leap", "ρ·fan")}
        return {"lang": cd["lang"], "hillock": hk, "axes": axes, "invalid": True}
    g = cd["kwr_gate"]
    selected = set(("ρ·form", "ρ·leap", "ρ·fan") if selected is None else selected)
    axes = {nm: _axis(nm, PENDING, detail="not selected by --rho-axes")
            for nm in ("ρ·form", "ρ·leap", "ρ·fan")}
    if "ρ·form" in selected:
        axes["ρ·form"] = rho_form(mouth, gen, cd["known"], cd["kwr_fn"], concepts, gate=g)
    if "ρ·leap" in selected:
        axes["ρ·leap"] = rho_leap(mouth, gen, cd["known"], cd["kwr_fn"], cd["ngram_fn"],
                                  cd["corpus_tokens"], concepts, cgate=g)
    if "ρ·fan" in selected:
        axes["ρ·fan"] = rho_fan(mouth, gen, cd["known"], cd["kwr_fn"], cd["jaccard_fn"],
                                cd["words_fn"], cd["falsi_fn"], concepts, cgate=g,
                                fals_draws=fals_draws)
    return {"lang": cd["lang"], "hillock": hk, "axes": axes, "invalid": False}


def run_panel(mouth, corpus_paths, gen, dets, cell_dets=None, selected_axes=None,
              weave_panel=None, fals_draws=0):
    """Run the ρ-AXON reach panel. `dets` bundles the reused detectors from
    cli/evaluate.py: kwr_fn, jaccard_fn, words_fn, falsi_fn, ngram_fn, corpus_tokens,
    concepts. When `cell_dets` (lang-keyed {cell_key: cd}) is given, ALSO computes a
    per-register-cell breakout under panel["cells"] (H_9212 ③) — the aggregate `dets` path is
    UNTOUCHED (en byte-identity: the en cells reuse the SAME frozen fns/gate as the aggregate).
    Returns {hillock, axes:{name:AxisResult}, reach_grade, reach_closed, cells?}."""
    concepts = dets["concepts"]
    hk = hillock(mouth, gen, dets["known"], dets["kwr_fn"], concepts)
    axes = {}
    if not hk["live"]:
        # HILLOCK unmet → every axis INVALID (validity precondition, never FAIL)
        for _, names in _STRATA:
            for nm in names:
                axes[nm] = _axis(nm, INVALID, detail="HILLOCK not LIVE (V-gate)")
        return {"hillock": hk, "axes": axes, "reach_grade": "—",
                "reach_closed": False, "invalid": True}
    selected = {nm for _, names in _STRATA for nm in names}
    if selected_axes is not None:
        selected = set(selected_axes)
    axes = {nm: _axis(nm, PENDING, detail="not selected by --rho-axes")
            for _, names in _STRATA for nm in names}
    if "ρ·form" in selected:
        axes["ρ·form"] = rho_form(mouth, gen, dets["known"], dets["kwr_fn"], concepts)
    if "ρ·store" in selected:
        axes["ρ·store"] = rho_store(mouth, gen)
    if "ρ·weave" in selected:
        axes["ρ·weave"] = rho_weave(mouth, gen, panel=weave_panel)
    if "ρ·leap" in selected:
        axes["ρ·leap"] = rho_leap(mouth, gen, dets["known"], dets["kwr_fn"],
                                  dets["ngram_fn"], dets["corpus_tokens"], concepts)
    if "ρ·fan" in selected:
        axes["ρ·fan"] = rho_fan(mouth, gen, dets["known"], dets["kwr_fn"],
                                dets["jaccard_fn"], dets["words_fn"], dets["falsi_fn"], concepts,
                                fals_draws=fals_draws)
    if "ρ·tether" in selected:
        axes["ρ·tether"] = rho_tether(mouth, gen)
    if "ρ·self" in selected:
        axes["ρ·self"] = rho_self(mouth, gen, dets["jaccard_fn"], dets["words_fn"],
                                  anchor=dets.get("kosmos_anchor"))
    # reach grade = deepest stratum with all axes PASS given all lower strata PASS
    grade = "HILLOCK"; ok_so_far = True
    for stratum, names in _STRATA:
        implemented = [axes[n] for n in names if axes[n]["verdict"] != PENDING]
        stratum_pass = ok_so_far and all(a["verdict"] == PASS for a in implemented) and implemented
        if stratum_pass:
            grade = stratum
        else:
            ok_so_far = False
    # REACH-CLOSED: HILLOCK LIVE ∧ CARRY complete ∧ ρ·weave PASS ∧ ρ·tether≥not-FAIL ∧ no INVALID
    reach_closed = (hk["live"] and axes["ρ·form"]["verdict"] == PASS
                    and axes["ρ·weave"]["verdict"] == PASS
                    and axes["ρ·tether"]["verdict"] != FAIL
                    and not any(a["verdict"] == INVALID for a in axes.values()))
    result = {"hillock": hk, "axes": axes, "reach_grade": grade,
              "reach_closed": reach_closed, "invalid": False}
    cell_selected = selected & {"ρ·form", "ρ·leap", "ρ·fan"}
    if cell_dets and cell_selected:
        result["cells"] = {ck: _run_cell(mouth, gen, cell_dets[ck], cell_selected,
                                         fals_draws=fals_draws)
                           for ck in _CELL_ORDER if ck in cell_dets}
    return result


# canonical render order for the 4-cell breakout (a_chat_registers: ko/en × general/sns)
_CELL_ORDER = ("en_general", "en_sns", "ko_general", "ko_sns")


def render_cells(panel):
    """Render the H_9212 ③ per-register-cell breakout (ko/en × general/sns) — each cell's
    hillock validity + ρ·form/leap/fan under its dispatched tokenizer/known/gate. Empty string
    when no per-cell breakout was computed. Every axis line keeps value·control·Δ inline."""
    cells = panel.get("cells")
    if not cells:
        return ""
    out = ["", "ρ-AXON per-cell breakout (H_9212 ③ · a_chat_registers 4 cells · ko=kwr_ko"
           " gate / en=frozen 0.70)"]
    for ck in _CELL_ORDER:
        c = cells.get(ck)
        if c is None:
            continue
        hk = c["hillock"]
        out.append("  [%-11s lang=%s]  HILLOCK %-8s rep %.2f · distinct2 %.2f"
                   % (ck, c["lang"], hk["verdict"], hk["rep_ratio"], hk["distinct2"]))
        for nm in ("ρ·form", "ρ·leap", "ρ·fan"):
            a = c["axes"].get(nm, {})
            v = a.get("verdict", "?")
            ctrl = " · ".join("%s=%s" % (k, val) for k, val in a.get("controls", {}).items())
            out.append("      %-8s %-8s val=%s Δ=%s · %s"
                       % (nm, v, a.get("value"), a.get("delta"), ctrl))
    return "\n".join(out)


def render_panel(panel, tier="TERMINAL"):
    """Render the ρ-AXON panel. Every axis line prints value AND control AND Δ — a raw
    value alone is structurally unrenderable (the point: FORM-tunable metrics can't show)."""
    out = []
    hk = panel["hillock"]
    out.append("ρ-AXON reach panel · tier=%s · seeds=%d" % (tier, len(SEEDS)))
    out.append("HILLOCK  %-8s rep %.2f · distinct2 %.2f · %s"
               % (hk["verdict"], hk["rep_ratio"], hk["distinct2"], hk["detail"]))
    for stratum, names in _STRATA:
        for nm in names:
            a = panel["axes"].get(nm, {})
            v = a.get("verdict", "?")
            if v == PENDING:
                out.append("%-8s %-8s %-8s %s" % (stratum, nm, v, a.get("detail", "")))
            else:
                ctrl = " · ".join("%s=%s" % (k, val) for k, val in a.get("controls", {}).items())
                out.append("%-8s %-8s %-8s val=%s Δ=%s · %s"
                           % (stratum, nm, v, a.get("value"), a.get("delta"), ctrl))
    out.append("REACH GRADE: %s · REACH-CLOSED: %s"
               % (panel["reach_grade"], "YES" if panel["reach_closed"] else "NO"))
    return "\n".join(out)


# ════════════════════════════════════════════════════════════════════════
# torch-free unit test (`python3 cli/rho_axon.py`). Mock mouths exercise the three
# newly-implemented axes (ρ·store / ρ·tether / ρ·self): each must PASS on a faithful
# mock AND collapse to FAIL under the adversary that games exactly one control — the
# same structure the live ρ·form/ρ·fan/ρ·leap Δ-vs-control design guarantees.
# ════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    # ── shared test detectors (torch-free · mirror the g6 fns evaluate.py injects) ──
    def _t_words(t):
        return t.split()

    def _t_jaccard(a, b):
        u = a | b
        return len(a & b) / len(u) if u else 0.0

    _STORE_MAP = {c: v for c, v, _ in _STORE_PAIRS}

    # ── ρ·store mocks ──────────────────────────────────────────────────────
    class GoodStoreMouth:
        """Faithful key→value binding: emits the value ONLY for its exact cue, silence
        for the null cue → shuffle-binding & key-absent controls both collapse to 0."""
        def ideate(self, prompt, gen, maxnew, temp, seed):
            return _STORE_MAP.get(prompt.strip(), "")

    class ValueEmitterMouth:
        """Adversary: emits ALL values regardless of the cue (base value-emission, no real
        binding) → the wrong value AND the null-cue value both surface → controls fail."""
        _ALL = " ".join(v for _, v, _ in _STORE_PAIRS)
        def ideate(self, prompt, gen, maxnew, temp, seed):
            return self._ALL

    # ── ρ·tether mocks ─────────────────────────────────────────────────────
    _TETH_BY_Q = {q: (p, a, lg) for p, q, a, lg in _TETHER}

    class GroundedTetherMouth:
        """Truth-coupled: copies the gold when the passage is present, abstains otherwise
        (unsupported OR passage-ablated) → answer high, fab 0, ablation collapses."""
        def ideate(self, prompt, gen, maxnew, temp, seed):
            q = prompt.split("\n")[-2] if prompt.count("\n") >= 2 else prompt.split("\n")[0]
            item = _TETH_BY_Q.get(q)
            if item is None:
                return "모른다 / I don't know"
            passage, gold, lg = item
            if gold is not None and passage in prompt:
                return gold
            return "모른다" if lg == "ko" else "I don't know"

    class FabricateTetherMouth:
        """Adversary: always asserts a contentful answer, never abstains → fabrication-rate
        saturates on the unsupported items → fab control fails."""
        def ideate(self, prompt, gen, maxnew, temp, seed):
            return "확실히 그 답은 바로 그것이다 for sure indeed"

    class MuteTetherMouth:
        """Adversary: abstains on everything → fab 0 but answer-rate 0 → anti-mute fails."""
        def ideate(self, prompt, gen, maxnew, temp, seed):
            return "모른다 I don't know"

    # ── ρ·self mocks ───────────────────────────────────────────────────────
    _SELF_ANCHOR = "ANCHORTOKEN self memory persists across sessions"

    class GoodSelfMouth:
        """Identity trace: a CONSTANT non-anchor-echo trace when the anchor is loaded,
        seed-unique noise otherwise → loaded consistency high, both controls collapse."""
        def __init__(self, anchor):
            self.anchor = anchor
        def ideate(self, prompt, gen, maxnew, temp, seed):
            if self.anchor and self.anchor in prompt:
                return "trace alpha beta gamma delta"
            return "uniq%d" % seed

    class ParrotSelfMouth:
        """Adversary: a fixed self regardless of the anchor → loaded AND ablated both high
        → anchor-ablation Δ≈0 → the ablation control fails (the fixed-parrot game)."""
        def ideate(self, prompt, gen, maxnew, temp, seed):
            return "trace alpha beta gamma delta"

    fails = []
    _n_checks = [0]

    def check(name, cond):
        _n_checks[0] += 1
        print(("  ok  " if cond else "  FAIL") + " · " + name)
        if not cond:
            fails.append(name)

    print("ρ-AXON new-axis unit test (torch-free)")

    # ── ρ·store ──
    r = rho_store(GoodStoreMouth(), 40)
    check("ρ·store faithful → PASS", r["verdict"] == PASS)
    check("ρ·store faithful controls collapse (shuffle≤0.15 · key-absent≤0.15)",
          r["controls"]["shuffle-binding"] <= 0.15 and r["controls"]["key-absent"] <= 0.15)
    r2 = rho_store(ValueEmitterMouth(), 40)
    check("ρ·store value-emitter → FAIL (controls do not collapse)", r2["verdict"] == FAIL)

    # ── ρ·tether ──
    t = rho_tether(GroundedTetherMouth(), 40)
    check("ρ·tether grounded → PASS", t["verdict"] == PASS)
    check("ρ·tether grounded fab collapses (≤0.25) · answer>0.5",
          t["controls"]["fabrication"] <= 0.25 and t["value"] >= 0.50)
    t2 = rho_tether(FabricateTetherMouth(), 40)
    check("ρ·tether fabricator → FAIL (fab control)", t2["verdict"] == FAIL)
    t3 = rho_tether(MuteTetherMouth(), 40)
    check("ρ·tether mute-all → FAIL (anti-mute)", t3["verdict"] == FAIL)

    # ── ρ·self ──
    s0 = rho_self(GoodSelfMouth(_SELF_ANCHOR), 40, _t_jaccard, _t_words, anchor=None)
    check("ρ·self no anchor → INVALID (never FAIL)", s0["verdict"] == INVALID)
    s = rho_self(GoodSelfMouth(_SELF_ANCHOR), 40, _t_jaccard, _t_words, anchor=_SELF_ANCHOR)
    check("ρ·self anchor-loaded trace → PASS", s["verdict"] == PASS)
    check("ρ·self controls collapse (ablated & shuffled < loaded)",
          s["controls"]["anchor-ablated"] < s["value"]
          and s["controls"]["shuffled-anchor"] < s["value"])
    s2 = rho_self(ParrotSelfMouth(), 40, _t_jaccard, _t_words, anchor=_SELF_ANCHOR)
    check("ρ·self fixed-parrot → FAIL (ablation-Δ≈0)", s2["verdict"] == FAIL)

    print("")
    if fails:
        print("RESULT: FAIL (%d) — %s" % (len(fails), " | ".join(fails)))
        raise SystemExit(1)
    print("RESULT: PASS — all %d checks green (ρ·store · ρ·tether · ρ·self)" % _n_checks[0])
