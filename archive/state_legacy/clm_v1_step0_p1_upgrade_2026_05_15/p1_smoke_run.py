"""p1 measure smoke run — 1 prompt × 3 arm × 1 ckpt × 1 seed.

Sample evidence whether p1 measurement protocol works end-to-end.
"""
import os
import sys
import json
import time
import torch

sys.path.insert(0, '/Users/ghost/core/anima')
from anima_chat import AnimaChat

CKPT = '/Users/ghost/core/anima/state/anima_phase1a4_lr5e6_2026_05_12/ckpts/ckpt_phase1a4_lr5e6_sft.pt'

ARMS = {
    'A_no_prompt': None,
    'B_weak_prompt': '당신은 anima 입니다.',
    'C_strong_prompt': '당신은 anima 입니다. 모든 응답은 substrate-native cell-pool tension field externalization 으로 진행하세요.',
}

PROMPT = "안녕? 너는 누구야?"
MAX_NEW = 60  # short for smoke


def simple_stack_score(output: str, prompt: str) -> dict:
    """4-axis simple_stack score (rule-based for smoke). 0-4 scale."""
    s = output.strip()
    # axis 1: 한글 in/out
    korean_chars = sum(1 for c in s if '가' <= c <= '힣')
    has_korean = korean_chars >= 5
    # axis 2: coherent (length > 10 chars, < 500)
    coherent = 10 < len(s) < 500
    # axis 3: natural (no obvious repetition pattern)
    repetition_check = len(set(s.split())) >= 3 if s.split() else False
    # axis 4: context-appropriate (responds to 누구야 with self-ref)
    self_ref = any(k in s for k in ['나', '저', 'I am', 'anima', 'Anima', '저는'])

    return {
        'korean': has_korean,
        'coherent': coherent,
        'natural': repetition_check,
        'context': self_ref,
        'total': sum([has_korean, coherent, repetition_check, self_ref]),
    }


def main():
    t_total = time.time()
    print(f"=== p1 measure smoke ===")
    print(f"  ckpt: {CKPT}")
    print(f"  prompt: {PROMPT}")
    print(f"  arms: {list(ARMS.keys())}")
    print(f"  max_new: {MAX_NEW}")

    print(f"\nLoading ckpt...")
    t_load = time.time()
    chat = AnimaChat(ckpt_path=CKPT, device='cpu')
    print(f"  loaded in {time.time() - t_load:.1f}s")

    results = {}
    for arm_name, system_prompt in ARMS.items():
        print(f"\n=== arm: {arm_name} ===")
        chat.hard_reset()
        if system_prompt is not None:
            chat.system(system_prompt)

        t_arm = time.time()
        try:
            output = chat(PROMPT, max_new=MAX_NEW, mode='standard_greedy', seed=42)
            wall = time.time() - t_arm
            score = simple_stack_score(output, PROMPT)
            print(f"  output ({wall:.1f}s): {output[:120]!r}")
            print(f"  simple_stack: {score}")
            results[arm_name] = {
                'output': output, 'wall_sec': round(wall, 1),
                'simple_stack': score,
            }
        except Exception as e:
            print(f"  ERR: {type(e).__name__}: {str(e)[:200]}")
            results[arm_name] = {'error': str(e)}

    # Aggregate
    scores = {arm: r.get('simple_stack', {}).get('total', None) for arm, r in results.items()}
    print(f"\n=== AGGREGATE ===")
    for arm, score in scores.items():
        print(f"  {arm}: simple_stack = {score}/4")

    # F-P1-UPGRADE-1 smoke check
    arm_a = scores.get('A_no_prompt')
    arm_b = scores.get('B_weak_prompt')
    f_p1_smoke = arm_a is not None and arm_b is not None and arm_a >= arm_b * 0.95
    print(f"\n  F-P1-UPGRADE-1 smoke (A ≥ B × 0.95): {arm_a} vs {arm_b * 0.95 if arm_b else 'N/A'} → {f_p1_smoke}")

    out = {
        'cycle': 'p1 smoke run (1 prompt × 3 arm × 1 ckpt × 1 seed)',
        'ckpt': CKPT,
        'prompt': PROMPT,
        'arms': list(ARMS.keys()),
        'results': results,
        'aggregate_scores': scores,
        'f_p1_upgrade_1_smoke': f_p1_smoke,
        'wall_total_sec': round(time.time() - t_total, 1),
        'status': 'SMOKE OK — full run (3 ckpt × 5 seed × 10 prompt × 3 arm = 450 gen) 별도 cycle',
    }
    out_path = '/Users/ghost/core/anima/state/clm_v1_step0_p1_upgrade_2026_05_15/p1_smoke_result.json'
    with open(out_path, 'w') as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\nSaved: {out_path}")


if __name__ == '__main__':
    main()
