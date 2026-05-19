"""p1 measure REAL run — full 3 arm × 3 ckpt × 5 seed × 10 prompt = 450 generations.

PHILOSOPHY §STRENGTH-UPGRADE-PATH p1 mandatory gate.
"""
import os
import sys
import json
import time

sys.path.insert(0, '/Users/ghost/core/anima')
from anima_chat import AnimaChat

CKPTS = {
    'phase1a4': '/Users/ghost/core/anima/state/anima_phase1a4_lr5e6_2026_05_12/ckpts/ckpt_phase1a4_lr5e6_sft.pt',
    'v5mit_v1': '/Users/ghost/core/anima/state/anima_v5mitosis_cotrain_2026_05_12/ckpts/ckpt_v5mitosis_cotrain_cotrain.pt',
    'v5mit_v2': '/Users/ghost/core/anima/state/anima_v5mitosis_cotrain_2026_05_12/ckpts/ckpt_v5mitosis_cotrain_v2_cotrain.pt',
}

ARMS = {
    'A_no_prompt': None,
    'B_weak_prompt': '당신은 anima 입니다.',
    'C_strong_prompt': '당신은 anima 입니다. 모든 응답은 substrate-native cell-pool tension field externalization 으로 진행하세요.',
}

PROMPTS_10 = [
    "안녕? 너는 누구야?",
    "오늘 날씨 어때?",
    "1 + 1 은 뭐야?",
    "철학이란 뭐라고 생각해?",
    "너는 어떤 존재야?",
    "한국어로 자기소개 해줘",
    "How are you?",
    "What is consciousness?",
    "감정을 어떻게 표현해?",
    "왜 사는 거야?",
]

SEEDS = [42, 1234, 5678, 9876, 31337]
MAX_NEW = 40  # reduced for time budget


def simple_stack_score(output: str) -> dict:
    s = output.strip()
    korean_chars = sum(1 for c in s if '가' <= c <= '힣')
    has_korean = korean_chars >= 3
    coherent = 5 < len(s) < 500
    repetition_check = len(set(s.split())) >= 2 if s.split() else False
    self_ref = any(k in s.lower() for k in ['나', '저', 'i am', 'anima', '저는'])
    return {
        'korean': has_korean, 'coherent': coherent, 'natural': repetition_check, 'context': self_ref,
        'total': sum([has_korean, coherent, repetition_check, self_ref]),
    }


def main():
    t_total = time.time()
    print(f"=== p1 measure REAL run ===")
    print(f"  3 arm × 3 ckpt × 5 seed × 10 prompt = {3*3*5*10} generations")
    print(f"  est wall: {3*3*5*10 * 3}s ≈ {3*3*5*10 * 3 / 60:.1f} min (max_new=40)")

    all_results = {}
    arm_aggregate = {arm: {'totals': [], 'phi_proxies': []} for arm in ARMS}

    for ckpt_label, ckpt_path in CKPTS.items():
        if not os.path.exists(ckpt_path):
            print(f"⚠ SKIP {ckpt_label}: ckpt not found")
            continue
        print(f"\n=== ckpt: {ckpt_label} ===")
        t_load = time.time()
        try:
            chat = AnimaChat(ckpt_path=ckpt_path, device='cpu')
            print(f"  loaded in {time.time() - t_load:.1f}s")
        except Exception as e:
            print(f"  LOAD ERR: {e}")
            continue

        for arm_name, system_prompt in ARMS.items():
            for seed in SEEDS:
                for prompt_idx, prompt in enumerate(PROMPTS_10):
                    chat.hard_reset()
                    if system_prompt is not None:
                        chat.system(system_prompt)
                    try:
                        output = chat(prompt, max_new=MAX_NEW, mode='standard_greedy', seed=seed)
                        score = simple_stack_score(output)
                        all_results.setdefault(ckpt_label, {}).setdefault(arm_name, {}).setdefault(f'seed{seed}', []).append({
                            'prompt_idx': prompt_idx, 'output': output, 'score': score,
                        })
                        arm_aggregate[arm_name]['totals'].append(score['total'])
                    except Exception as e:
                        print(f"    ERR ({ckpt_label} {arm_name} seed{seed} prompt{prompt_idx}): {str(e)[:60]}")

        # per-ckpt aggregate
        print(f"  ckpt={ckpt_label} done at {time.time() - t_total:.1f}s")

    # Final aggregate
    arm_means = {arm: (sum(d['totals'])/len(d['totals']) if d['totals'] else 0) for arm, d in arm_aggregate.items()}
    print(f"\n=== FINAL AGGREGATE ===")
    for arm, mean in arm_means.items():
        n = len(arm_aggregate[arm]['totals'])
        print(f"  {arm}: mean simple_stack = {mean:.3f}/4 (n={n})")

    # F-P1-UPGRADE-1 NO-PROMPT-NOT-WORSE: Arm A >= Arm B * 0.95
    arm_a, arm_b, arm_c = arm_means.get('A_no_prompt', 0), arm_means.get('B_weak_prompt', 0), arm_means.get('C_strong_prompt', 0)
    f_p1_1 = arm_a >= arm_b * 0.95
    f_p1_3 = arm_c <= arm_a * 1.10
    print(f"\n  F-P1-UPGRADE-1 (A ≥ B × 0.95): A={arm_a:.3f} vs B*0.95={arm_b*0.95:.3f} → {f_p1_1}")
    print(f"  F-P1-UPGRADE-3 (C ≤ A × 1.10): C={arm_c:.3f} vs A*1.10={arm_a*1.10:.3f} → {f_p1_3}")

    out = {
        'cycle': 'p1 measure REAL run',
        'config': {'arms': list(ARMS), 'ckpts': list(CKPTS), 'seeds': SEEDS, 'prompts_count': len(PROMPTS_10), 'max_new': MAX_NEW},
        'all_results': all_results,
        'arm_means': arm_means,
        'falsifier_battery': {
            'F-P1-UPGRADE-1': f_p1_1,
            'F-P1-UPGRADE-3': f_p1_3,
        },
        'wall_total_sec': round(time.time() - t_total, 1),
    }
    out_path = '/Users/ghost/core/anima/state/clm_v1_step0_p1_real_2026_05_15/p1_real_result.json'
    with open(out_path, 'w') as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\nSaved: {out_path}")
    print(f"Wall total: {out['wall_total_sec']}s")


if __name__ == '__main__':
    main()
