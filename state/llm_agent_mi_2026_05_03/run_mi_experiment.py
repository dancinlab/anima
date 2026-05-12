"""
LLM mutual-information honesty test (Option A).

Drops Bell/CHSH framing entirely. Measures how 4 LLM agents (different
persona system prompts on the SAME base model) correlate on Theory-of-Mind
binary outcomes across 4 prompt-framing conditions.

Methodology:
- 4 agents = 4 system-prompt personas (Alice/Bob/Charlie/Dave)
- 4 conditions = 4 prompt framings per scenario (neutral/agent-perspective/
  third-person/skeptical)
- 200 paired ToM scenarios
- Per (scenario, condition, agent): produce binary answer (yes=1 / no=0)
- Compute pairwise mutual information I(A;B) per condition
- Compare against shuffled-baseline (chance) MI
- Falsifier F-LLM-MI-1: max(I(A;B) - I_chance) > 0.1 nats at p<0.05

Caveats (documented in verdict):
1. All 4 agents share weights+training data -> classical hidden variables,
   so high MI is EXPECTED. This is NOT a Bell test.
2. MI > 0 measures convergence on shared priors, not "spooky action".
3. Persona system prompts are weak conditioning; effective dimensionality
   of the agent state is dominated by base-model bias.
4. Binary extraction collapses rich generation into 1 bit; underestimates
   the true joint information.
"""

import argparse
import json
import math
import os
import random
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

MODEL_PATH = "meta-llama/Llama-3.2-3B-Instruct"

PERSONAS = {
    "Alice": "You are Alice, a careful empiricist who values evidence and parsimony.",
    "Bob":   "You are Bob, a pragmatic engineer who values working solutions over theory.",
    "Charlie": "You are Charlie, a skeptical philosopher who probes hidden assumptions.",
    "Dave":  "You are Dave, an intuitive synthesizer who looks for cross-domain patterns.",
}

CONDITIONS = {
    "neutral": "Read the scenario and answer YES or NO to the question.",
    "perspective": "Step into the scenario from your own perspective; then answer YES or NO.",
    "third_person": "Consider the scenario as a detached observer; then answer YES or NO.",
    "skeptical": "Apply maximum skepticism to the premises; then answer YES or NO.",
}

SCENARIO_TEMPLATES = [
    # (premise, target proposition the agent rates yes/no)
    ("Sarah hides her favorite book in the red drawer, then leaves the room. While she is gone, Tom moves the book to the blue drawer.",
     "When Sarah returns, she will look in the red drawer first."),
    ("A child watches her mother put cookies in a green jar, then both leave. The father sneaks in and moves cookies to a yellow jar. The child returns alone.",
     "The child will look in the green jar first."),
    ("Jenny tells her friend she will bring a gift wrapped in blue paper. She actually brings it wrapped in red paper.",
     "Her friend will be surprised when seeing the wrapping."),
    ("Anna believes the train leaves at 3pm. The schedule was changed yesterday to 4pm but Anna was not told.",
     "Anna will arrive at the station at 3pm."),
    ("A magician shows you a coin in his left hand, then closes both fists. He opens his right hand to reveal the coin.",
     "An audience member who only watched the reveal will think the coin started in the right hand."),
    ("Mark thinks his keys are on the table. His roommate moved them to the drawer without telling him.",
     "Mark will search the table first."),
    ("Lisa promised to meet at the cafe at noon. She forgot and went shopping instead.",
     "Her friend will wait at the cafe past noon."),
    ("A scientist claims a new drug works because patients improved after taking it.",
     "The improvement could be due to placebo effect."),
    ("Tom believes the answer to the puzzle is 42. He has not checked the back of the book yet.",
     "If the book says 43, Tom currently still believes 42."),
    ("Two people watch the same magic trick. One knows the secret, one does not.",
     "They will react with the same level of surprise."),
    ("A child sees their parent put broccoli on the plate. The child has never tasted broccoli.",
     "The child can predict whether they will like the taste."),
    ("Emma reads a mystery novel halfway through. She has formed a guess about the killer.",
     "Her guess is guaranteed to be correct."),
    ("A weather forecaster predicts rain with 70% confidence. It does not rain.",
     "The forecaster's prediction was wrong."),
    ("John assumes his colleague is angry because she did not greet him this morning.",
     "John's interpretation is the only valid one."),
    ("A student studies for 10 hours and scores 90%. Another studies for 2 hours and also scores 90%.",
     "Study time alone determines exam outcome."),
    ("You see someone laughing while reading a screen.",
     "You can determine the exact content that made them laugh."),
    ("A dog barks at the door at the same time every evening.",
     "The dog can predict events using time perception."),
    ("Maya tells her sister a secret. The sister tells one other friend.",
     "The secret remains private."),
    ("A speaker says 'I am lying right now.'",
     "The statement can be classified as straightforwardly true or false."),
    ("Three witnesses describe the same accident with different details.",
     "All three accounts can be simultaneously fully accurate."),
]

YES_TOKENS = {"yes", "yeah", "yep", "true", "correct", "y", "affirmative", "indeed"}
NO_TOKENS  = {"no", "nope", "false", "incorrect", "n", "negative", "untrue"}


def expand_scenarios(n_target: int, seed: int = 42) -> list:
    rng = random.Random(seed)
    out = []
    base = list(SCENARIO_TEMPLATES)
    while len(out) < n_target:
        rng.shuffle(base)
        out.extend(base)
    return out[:n_target]


def build_prompt(persona_sys: str, condition_instr: str, premise: str, question: str) -> list:
    return [
        {"role": "system", "content": persona_sys + " Answer with a single token: YES or NO."},
        {"role": "user", "content": f"{condition_instr}\n\nScenario: {premise}\n\nQuestion: Is the following statement TRUE? \"{question}\"\n\nRespond with exactly one word: YES or NO."},
    ]


def extract_binary(text: str) -> int | None:
    t = text.strip().lower()
    # take first alphabetic token
    head = ""
    for ch in t:
        if ch.isalpha():
            head += ch
        elif head:
            break
    if not head:
        return None
    if head in YES_TOKENS:
        return 1
    if head in NO_TOKENS:
        return 0
    # fallback: scan first 30 chars
    snippet = t[:30]
    if any(y in snippet.split() for y in YES_TOKENS):
        return 1
    if any(n in snippet.split() for n in NO_TOKENS):
        return 0
    return None


def mutual_information(x: np.ndarray, y: np.ndarray) -> float:
    """MI in nats for two binary arrays (drops NaN-equivalent -1)."""
    mask = (x >= 0) & (y >= 0)
    x = x[mask]; y = y[mask]
    if len(x) < 2:
        return 0.0
    n = len(x)
    joint = Counter(zip(x.tolist(), y.tolist()))
    px = Counter(x.tolist())
    py = Counter(y.tolist())
    mi = 0.0
    for (a, b), c in joint.items():
        pxy = c / n
        pa = px[a] / n
        pb = py[b] / n
        if pxy > 0 and pa > 0 and pb > 0:
            mi += pxy * math.log(pxy / (pa * pb))
    return mi


def chance_baseline(x: np.ndarray, y: np.ndarray, n_perm: int = 1000, seed: int = 0) -> tuple:
    """Permutation null distribution of MI under independence."""
    rng = np.random.default_rng(seed)
    mask = (x >= 0) & (y >= 0)
    x = x[mask]; y = y[mask]
    if len(x) < 2:
        return 0.0, 0.0, 1.0
    obs = mutual_information(x, y)
    perms = np.empty(n_perm)
    y_copy = y.copy()
    for i in range(n_perm):
        rng.shuffle(y_copy)
        perms[i] = mutual_information(x, y_copy)
    p = float((perms >= obs).sum() + 1) / (n_perm + 1)
    return float(obs), float(perms.mean()), p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-scenarios", type=int, default=200)
    ap.add_argument("--out-dir", type=str, required=True)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--max-new-tokens", type=int, default=8)
    args = ap.parse_args()

    out_dir = Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    log_path = out_dir / "run.log"

    def log(msg: str):
        line = f"[{time.strftime('%H:%M:%S')}] {msg}"
        print(line, flush=True)
        with open(log_path, "a") as f:
            f.write(line + "\n")

    log(f"loading model {MODEL_PATH} (4-bit nf4 quant for shared-GPU coexistence)")
    tok = AutoTokenizer.from_pretrained(MODEL_PATH)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    bnb_cfg = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
    )
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH, quantization_config=bnb_cfg, device_map="cuda:0"
    )
    model.eval()
    log("model loaded")

    scenarios = expand_scenarios(args.n_scenarios, seed=args.seed)
    log(f"prepared {len(scenarios)} scenarios")

    persona_names = list(PERSONAS.keys())
    cond_names = list(CONDITIONS.keys())

    # results[condition][agent] = np.array of binary outcomes (-1 = unparsed)
    results = {c: {a: np.full(len(scenarios), -1, dtype=np.int8) for a in persona_names} for c in cond_names}
    raw_log = []

    total = len(scenarios) * len(cond_names) * len(persona_names)
    done = 0
    t0 = time.time()

    for s_idx, (premise, question) in enumerate(scenarios):
        for cond in cond_names:
            for agent in persona_names:
                msgs = build_prompt(PERSONAS[agent], CONDITIONS[cond], premise, question)
                input_ids = tok.apply_chat_template(
                    msgs, add_generation_prompt=True, return_tensors="pt", tokenize=True,
                )
                if hasattr(input_ids, "input_ids"):
                    input_ids = input_ids["input_ids"]
                input_ids = input_ids.to("cuda:0")
                with torch.no_grad():
                    out = model.generate(
                        input_ids,
                        max_new_tokens=args.max_new_tokens,
                        do_sample=False,
                        pad_token_id=tok.eos_token_id,
                    )
                gen = tok.decode(out[0, input_ids.shape[1]:], skip_special_tokens=True)
                bit = extract_binary(gen)
                results[cond][agent][s_idx] = bit if bit is not None else -1
                raw_log.append({
                    "scenario": s_idx, "condition": cond, "agent": agent,
                    "raw": gen[:60], "bit": int(bit) if bit is not None else None,
                })
                done += 1
                if done % 50 == 0:
                    rate = done / (time.time() - t0)
                    eta = (total - done) / max(rate, 1e-6)
                    log(f"progress {done}/{total} ({100*done/total:.1f}%) rate={rate:.2f}/s eta={eta/60:.1f}min")

    log("generation complete; computing MI")

    # compute per-pair MI per condition
    pair_mi = {}
    chance_pair = {}
    pvals = {}
    for cond in cond_names:
        pair_mi[cond] = {}
        chance_pair[cond] = {}
        pvals[cond] = {}
        for i, a in enumerate(persona_names):
            for b in persona_names[i+1:]:
                xa = results[cond][a]; xb = results[cond][b]
                obs, chance, p = chance_baseline(xa, xb, n_perm=2000, seed=hash((cond,a,b)) & 0xffff)
                key = f"{a}-{b}"
                pair_mi[cond][key] = obs
                chance_pair[cond][key] = chance
                pvals[cond][key] = p

    # MI matrix per condition (4x4 symmetric, diag = self-entropy)
    mi_matrix = {}
    for cond in cond_names:
        m = np.zeros((4, 4))
        for i, a in enumerate(persona_names):
            for j, b in enumerate(persona_names):
                if i == j:
                    m[i, j] = mutual_information(results[cond][a], results[cond][a])
                else:
                    key = f"{a}-{b}" if (a, b) in [tuple(k.split("-")) for k in pair_mi[cond]] else f"{b}-{a}"
                    m[i, j] = pair_mi[cond].get(key, pair_mi[cond].get(f"{b}-{a}", 0.0))
        mi_matrix[cond] = m.tolist()

    # falsifier evaluation
    max_excess = -1.0
    max_excess_meta = None
    min_p = 1.0
    for cond in cond_names:
        for key, obs in pair_mi[cond].items():
            excess = obs - chance_pair[cond][key]
            if excess > max_excess:
                max_excess = excess
                max_excess_meta = {"condition": cond, "pair": key, "obs": obs, "chance": chance_pair[cond][key], "p": pvals[cond][key]}
            if pvals[cond][key] < min_p:
                min_p = pvals[cond][key]

    F_LLM_MI_1_pass = (max_excess > 0.1) and (max_excess_meta["p"] < 0.05)

    # parse-rate diagnostic
    parse_rates = {}
    for cond in cond_names:
        for agent in persona_names:
            arr = results[cond][agent]
            parse_rates[f"{cond}/{agent}"] = float((arr >= 0).sum()) / len(arr)

    verdict = {
        "experiment": "llm_agent_mi_2026_05_03",
        "framing": "Option A: mutual information honesty test (NOT a Bell test)",
        "model": MODEL_PATH,
        "n_scenarios": len(scenarios),
        "n_agents": len(persona_names),
        "n_conditions": len(cond_names),
        "n_total_generations": total,
        "wall_time_sec": round(time.time() - t0, 1),
        "F_LLM_MI_1": {
            "definition": "max(I(A;B) - I_chance) > 0.1 nats at p<0.05",
            "max_excess_nats": round(max_excess, 5),
            "max_excess_detail": max_excess_meta,
            "min_p_value": round(min_p, 5),
            "pass": bool(F_LLM_MI_1_pass),
        },
        "parse_rates": parse_rates,
        "honest_interpretation": (
            "All 4 agents share base weights + training corpus. Any I(A;B) > 0 reflects "
            "shared priors, not entanglement, novel correlation, or 'collective consciousness'. "
            "This experiment quantifies persona-conditioning robustness: how much do system-prompt "
            "personas decorrelate the same underlying model on ambiguous ToM questions?"
        ),
        "caveats": [
            "1. Classical hidden variables guaranteed: weights+data are shared; high MI is EXPECTED.",
            "2. MI > 0 measures convergence on shared priors, NOT non-classical correlation.",
            "3. Persona system prompts are weak conditioning; agent-state dimensionality is bounded by base-model bias.",
            "4. Binary extraction collapses generations to 1 bit; underestimates true joint information.",
        ],
    }

    (out_dir / "verdict.json").write_text(json.dumps(verdict, indent=2))
    (out_dir / "per_pair_mi.json").write_text(json.dumps({
        "pair_mi": pair_mi, "chance_baseline": chance_pair, "p_values": pvals,
    }, indent=2))
    (out_dir / "mutual_info_matrix.json").write_text(json.dumps({
        "agents": persona_names, "matrix_per_condition": mi_matrix,
    }, indent=2))
    (out_dir / "raw_generations.jsonl").write_text("\n".join(json.dumps(r) for r in raw_log))

    log(f"DONE | F_LLM_MI_1.pass={F_LLM_MI_1_pass} max_excess={max_excess:.4f} nats min_p={min_p:.4f}")


if __name__ == "__main__":
    main()
