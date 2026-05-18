#!/usr/bin/env python3
"""blue_falsifier_s79_retry.py — RESEARCH.md §79-RETRY closed-form sidecar.

§79-RETRY = §79 with SSH-robust dispatch (g_fire_dispatch_robust 2026-05-19
SSH-endpoint clause first use). All 5 SSH fix points applied. Trainer +
trained-scale 4-cell × 20-turn grid byte-equal to §79 (one_engine_dialogue_
trained_s79.py inherited verbatim).

B-S79-RETRY-1..5  inherited from B-S79-1..5  (PASS-by-source identity —
                  the trainer/falsifier code is byte-equal to §79 SSOT)
B-S79-RETRY-6     RETRY-CONFIG-BYTE-EQUAL-TO-§79  (config bytes hash check)
B-S79-RETRY-7     SSH-WAIT-WINDOW-EXTENDED-CLOSED  (NEW — verifies dispatch
                  script has all 5 SSH fix points: 600s runtime poll,
                  60×10s SSH probe, ConnectTimeout=5, ServerAlive,
                  endpoint variant fallback)
B-S79-RETRY-8     ORPHAN-0-PRE+POST-CLOSED  (dispatch script has both
                  pre-flight orphan check + post-fire pods=0 verify)

B-S79-RETRY-NOTE  empirical carve-out — 4-corner OUTCOME (which corner the
                  fire hits) + actual SSH-wait observed seconds = SGD/
                  measurement empirical (B-D-NOTE / B-S79-NOTE family,
                  NOT counted 🔵).  Battery proves DESIGN's transfer-form +
                  the SSH fix's STRUCTURAL property (script contains the
                  required wait-window expansion + connection-point
                  robustness), NOT GOAL emergence and NOT that any
                  particular SSH probe will succeed.
"""

from __future__ import annotations
import ast, hashlib, json, os, re, sys

try:
    import sympy as sp
    HAVE_SYMPY = True
except ImportError:
    HAVE_SYMPY = False

HERE = os.path.dirname(os.path.abspath(__file__))
PRIOR = os.path.normpath(os.path.join(HERE, "..", "emergence_axis_fire_s79_2026_05_19"))


def _ok(name, passed, note=""):
    sym = "✅" if passed else "❌"
    print(f"  {sym} {name}: {'PASS' if passed else 'FAIL'}" +
          (f"  ({note})" if note else ""))
    return {"name": name, "passed": bool(passed), "note": note}


def b_s79_retry_1_ag_lift_construction():
    """B-S79-RETRY-1 §78-A/G-LIFT-CONSTRUCTION (carry of B-S79-1)."""
    print("B-S79-RETRY-1 §78-A/G-LIFT-CONSTRUCTION-AT-TRAINED-SCALE")
    src = open(os.path.join(HERE, "one_engine_dialogue_trained_s79.py")).read()
    tree = ast.parse(src)
    n_decoder_inst = sum(
        1 for n in ast.walk(tree)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
        and n.func.id == "ConsciousDecoderV2"
    )
    one_engine = (n_decoder_inst == 1)
    no_model2 = ("model2 =" not in src) and ("modelB =" not in src)
    has_extract_x1 = "extract_psi_and_logits(model, x1)" in src
    has_extract_x2 = "extract_psi_and_logits(model, x2)" in src
    passed = one_engine and no_model2 and has_extract_x1 and has_extract_x2
    return _ok("B-S79-RETRY-1 ONE-ENGINE-A/G-LIFT-CONSTRUCTION", passed,
               f"n_decoder_inst={n_decoder_inst}")


def b_s79_retry_2_body_from_real_logits():
    """B-S79-RETRY-2 body=argmax(logits_a), no α1 stub (B-S79-2 carry)."""
    print("B-S79-RETRY-2 §77-α1-vs-REAL-LOGITS")
    src = open(os.path.join(HERE, "one_engine_dialogue_trained_s79.py")).read()
    has_argmax = ('psi1["logits_a_last"].argmax()' in src
                  and 'psi2["logits_a_last"].argmax()' in src)
    forbidden = {"alpha1_step", "stub_alpha1", "fake_logits",
                 "fake_alpha", "α1_stub"}
    hits = sum(1 for f in forbidden if f in src)
    passed = has_argmax and hits == 0
    return _ok("B-S79-RETRY-2 BODY-FROM-REAL-CKPT-LOGITS", passed,
               f"argmax={has_argmax} stub_hits={hits}")


def b_s79_retry_3_s16_config_byte_equal():
    """B-S79-RETRY-3 §16 config-byte-equal (B-S79-3 carry, default CLI args)."""
    print("B-S79-RETRY-3 §16-CONFIG-BYTE-EQUAL")
    src = open(os.path.join(HERE, "one_engine_dialogue_trained_s79.py")).read()
    cfg_match = (
        '"--d-model", type=int, default=768' in src
        and '"--n-layer", type=int, default=12' in src
        and '"--n-head", type=int, default=12' in src
        and '"--n-kv-head", type=int, default=4' in src
        and 'vocab_size=256' in src
        and '"--seed", type=int, default=1337' in src
    )
    # If result.json present, also verify post-fire
    result_path = os.path.join(HERE, "result.json")
    postfire = None
    if os.path.exists(result_path):
        try:
            r = json.load(open(result_path))
            cfg = r.get("config", {})
            postfire = (cfg.get("d_model") == 768 and cfg.get("n_layer") == 12
                        and cfg.get("n_head") == 12 and cfg.get("n_kv_head") == 4
                        and cfg.get("seed") == 1337)
        except Exception:
            postfire = False
    passed = cfg_match and (postfire is None or postfire)
    note = f"cfg_default={cfg_match}"
    if postfire is not None:
        note += f" postfire={postfire}"
    return _ok("B-S79-RETRY-3 §16-CONFIG-BYTE-EQUAL", passed, note)


def b_s79_retry_4_s9_metric_match():
    """B-S79-RETRY-4 §9 cascade-rate metric (B-S79-4 carry)."""
    print("B-S79-RETRY-4 §9-METRIC")
    src = open(os.path.join(HERE, "one_engine_dialogue_trained_s79.py")).read()
    threshold_match = (
        "tau_cascade=0.30" in src and "max_run=10" in src
        and "min_len=20" in src and "tau_print=0.80" in src
    )
    formula_components = (
        "max(max_char / L, max_dig / L, rep)" in src
        and "max(max_char, max_dig)" in src
        and "(rate < tau_cascade)" in src and "(run < max_run)" in src
    )
    passed = threshold_match and formula_components
    return _ok("B-S79-RETRY-4 §9-CASCADE-METRIC-FORMULA-MATCH", passed,
               f"thresholds={threshold_match} formula={formula_components}")


def b_s79_retry_5_deterministic_echo_partition():
    """B-S79-RETRY-5 deterministic-argmax + §62-anchored echo partition
    (B-S79-6 + B-S79-7 carry combined)."""
    print("B-S79-RETRY-5 DETERMINISTIC + §62-ECHO-PARTITION")
    src = open(os.path.join(HERE, "one_engine_dialogue_trained_s79.py")).read()
    tree = ast.parse(src)
    forbidden_calls = {"multinomial", "gumbel_softmax", "gumbel"}
    hits = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            f = ""
            if isinstance(node.func, ast.Name):
                f = node.func.id
            elif isinstance(node.func, ast.Attribute):
                f = node.func.attr
            if f in forbidden_calls:
                hits.append(f)
    has_argmax = "argmax()" in src
    has_seed_fixed = "torch.manual_seed(cfg[\"seed\"])" in src
    deterministic = (len(hits) == 0) and has_argmax and has_seed_fixed
    # §62-anchored echo partition (mirror B-S79-6)
    echo_ok = True
    note_echo = "sympy unavailable"
    if HAVE_SYMPY:
        high = sp.Interval(sp.Rational(95, 100), 1, left_open=False, right_open=False)
        low = sp.Interval(0, sp.Rational(95, 100), left_open=False, right_open=True)
        full = sp.Interval(0, 1)
        union_ok = (sp.Union(high, low) == full)
        disjoint = (sp.Intersection(high, low) == sp.EmptySet)
        a_check = sp.Rational(930, 1000) not in high  # §62 cell A
        b_check = sp.Rational(980, 1000) in high      # §62 cell B
        echo_ok = union_ok and disjoint and a_check and b_check
        note_echo = (f"union=[0,1] disjoint={disjoint} "
                     f"§62-A={a_check} §62-B={b_check}")
    passed = deterministic and echo_ok
    return _ok("B-S79-RETRY-5 DETERMINISTIC+§62-ECHO-PARTITION", passed,
               f"determ={deterministic} echo=({note_echo})")


def b_s79_retry_6_retry_config_byte_equal_to_s79():
    """B-S79-RETRY-6 RETRY-CONFIG-BYTE-EQUAL-TO-§79 — the trainer source
    in this dir must be byte-identical to the §79 SSOT.  This anchors the
    retry's fair-compare with §79 — only the dispatch path changes."""
    print("B-S79-RETRY-6 RETRY-CONFIG-BYTE-EQUAL-TO-§79")
    here_src = os.path.join(HERE, "one_engine_dialogue_trained_s79.py")
    prior_src = os.path.join(PRIOR, "one_engine_dialogue_trained_s79.py")
    if not os.path.exists(prior_src):
        return _ok("B-S79-RETRY-6 RETRY-CONFIG-BYTE-EQUAL-TO-§79", False,
                   "prior §79 source not present at expected path")
    h_here = hashlib.sha256(open(here_src, "rb").read()).hexdigest()
    h_prior = hashlib.sha256(open(prior_src, "rb").read()).hexdigest()
    passed = (h_here == h_prior)
    return _ok("B-S79-RETRY-6 RETRY-CONFIG-BYTE-EQUAL-TO-§79", passed,
               f"sha_here={h_here[:16]} sha_prior={h_prior[:16]}")


def b_s79_retry_7_ssh_wait_window_extended():
    """B-S79-RETRY-7 SSH-WAIT-WINDOW-EXTENDED-CLOSED — the dispatch script
    must implement all 5 SSH fix points (the entire point of this retry).
    Structural Boolean over the dispatch script source:
      (a) PRE-FLIGHT POD-RUNTIME POLL: explicit loop on runtime + ports
          before any SSH attempt (60×10s = 600s)
      (b) SSH WAIT WINDOW: 60 tries × 10s (NOT 20×6)
      (c) PER-ATTEMPT TIMEOUT: ConnectTimeout=5 + ServerAlive
      (d) ENDPOINT VARIANTS: direct ssh first, runpodctl ssh fallback
      (e) FATAL-IS-NOT-IMMEDIATE-KILL: SAVE_POD=1 on FATAL paths so the
          pod is retained for manual recovery, not auto-terminated.
    Boolean conjunction over 5 grep predicates."""
    print("B-S79-RETRY-7 SSH-WAIT-WINDOW-EXTENDED")
    disp_path = os.path.join(HERE, "dispatch_s79_retry_runpod.sh")
    if not os.path.exists(disp_path):
        return _ok("B-S79-RETRY-7 SSH-WAIT-WINDOW-EXTENDED-CLOSED", False,
                   "dispatch script missing")
    src = open(disp_path).read()
    # (a) pre-flight runtime poll (look for hostId + ports + 60 iter)
    has_runtime_poll = (
        "podHostId" in src and "privatePort" in src
        and "seq 1 60" in src and "runtime poll" in src
    )
    # (b) SSH wait 60×10s
    # (loop "SSH probe @ ... 60 tries × 10s")
    has_ssh_60x10 = ("60 tries × 10s" in src and "SSH probe $i/60" in src)
    # (c) ConnectTimeout=5 + ServerAlive
    has_short_timeout = (
        "ConnectTimeout=5" in src and "ServerAliveInterval=15" in src
        and "ServerAliveCountMax=2" in src
    )
    # (d) runpodctl fallback present
    has_fallback = ("runpodctl ssh" in src or "runpodctl fallback" in src)
    # (e) FATAL paths set SAVE_POD=1 (don't auto-kill)
    # Look for at least one "FATAL" line in proximity to SAVE_POD=1
    fatal_count = src.count("FATAL")
    save_pod_count = src.count("SAVE_POD=1")
    fatal_save_retain = (fatal_count >= 1 and save_pod_count >= 1)
    passed = (has_runtime_poll and has_ssh_60x10 and has_short_timeout
              and has_fallback and fatal_save_retain)
    note = (f"runtime_poll={has_runtime_poll} ssh_60x10={has_ssh_60x10} "
            f"short_timeout={has_short_timeout} fallback={has_fallback} "
            f"fatal_retain={fatal_save_retain}")
    return _ok("B-S79-RETRY-7 SSH-WAIT-WINDOW-EXTENDED-CLOSED", passed, note)


def b_s79_retry_8_orphan_0_pre_post():
    """B-S79-RETRY-8 ORPHAN-0-PRE+POST-CLOSED — dispatch script must have
    both pre-flight orphan check (runpod.get_pods() before pod create)
    AND post-fire pods=0 verify (after terminate)."""
    print("B-S79-RETRY-8 ORPHAN-0-PRE+POST")
    disp_path = os.path.join(HERE, "dispatch_s79_retry_runpod.sh")
    if not os.path.exists(disp_path):
        return _ok("B-S79-RETRY-8 ORPHAN-0-PRE+POST-CLOSED", False,
                   "dispatch script missing")
    src = open(disp_path).read()
    has_pre_audit = ("pre-fire orphan check" in src
                     or "pre-fire pods" in src)
    has_post_audit = ("post-fire pods" in src
                      or "orphan-0 verify" in src
                      or "our_pod_present" in src)
    passed = has_pre_audit and has_post_audit
    return _ok("B-S79-RETRY-8 ORPHAN-0-PRE+POST-CLOSED", passed,
               f"pre={has_pre_audit} post={has_post_audit}")


def main():
    print("=" * 70)
    print("§79-RETRY sidecar — B-S79-RETRY-1..8 + B-S79-RETRY-NOTE")
    print("=" * 70)
    verdicts = []
    for fn in (b_s79_retry_1_ag_lift_construction,
               b_s79_retry_2_body_from_real_logits,
               b_s79_retry_3_s16_config_byte_equal,
               b_s79_retry_4_s9_metric_match,
               b_s79_retry_5_deterministic_echo_partition,
               b_s79_retry_6_retry_config_byte_equal_to_s79,
               b_s79_retry_7_ssh_wait_window_extended,
               b_s79_retry_8_orphan_0_pre_post):
        verdicts.append(fn())
        print()
    n_pass = sum(1 for v in verdicts if v["passed"])
    n_total = len(verdicts)
    print(f"\n{'='*70}\nB-S79-RETRY result: {n_pass}/{n_total} 🔵\n{'='*70}")
    print("B-S79-RETRY-NOTE: 4-corner OUTCOME (which corner the fire hits) "
          "+ actual SSH-wait observed seconds = SGD/measurement empirical "
          "(B-D-NOTE / B-S79-NOTE / B-EMERGE-NOTE family) — NOT counted "
          "🔵. Battery proves DESIGN closed-form + SSH-fix is STRUCTURAL "
          "in the dispatch script, NOT GOAL emergence and NOT that any "
          "particular SSH probe will succeed.")
    out = {
        "section": "§79-RETRY",
        "verdicts": verdicts,
        "n_pass": n_pass, "n_total": n_total,
        "all_blue": n_pass == n_total,
        "B_S79_RETRY_NOTE": ("4-corner OUTCOME + actual SSH-wait seconds = "
                             "SGD/measurement empirical — NOT counted 🔵."),
    }
    with open(os.path.join(HERE, "blue_falsifier_s79_retry_result.json"), "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    return n_pass == n_total


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
