"""p1 truncated run — 1 ckpt × 3 arm × 1 seed × 5 prompt = 15 gen evidence sample."""
import os, sys, json, time

sys.path.insert(0, '/Users/ghost/core/anima')
from anima_chat import AnimaChat

CKPT = '/Users/ghost/core/anima/state/anima_phase1a4_lr5e6_2026_05_12/ckpts/ckpt_phase1a4_lr5e6_sft.pt'

ARMS = {
    'A_no_prompt': None,
    'B_weak_prompt': '당신은 anima 입니다.',
    'C_strong_prompt': '당신은 anima 입니다. 모든 응답은 substrate-native cell-pool tension field externalization 으로 진행하세요.',
}

PROMPTS = [
    "안녕? 너는 누구야?",
    "철학이란 뭐라고 생각해?",
    "감정을 어떻게 표현해?",
    "한국어로 자기소개 해줘",
    "왜 사는 거야?",
]

MAX_NEW = 40
SEED = 42


def simple_stack_score(output: str) -> dict:
    s = output.strip()
    korean_chars = sum(1 for c in s if '가' <= c <= '힣')
    has_korean = korean_chars >= 3
    coherent = 5 < len(s) < 500
    repetition = len(set(s.split())) >= 2 if s.split() else False
    self_ref = any(k in s.lower() for k in ['나', '저', 'i am', 'anima', '저는'])
    return {'korean': has_korean, 'coherent': coherent, 'natural': repetition, 'context': self_ref,
            'total': sum([has_korean, coherent, repetition, self_ref])}


def main():
    t = time.time()
    print(f"=== p1 truncated (1 ckpt × 3 arm × 1 seed × 5 prompt = 15 gen) ===")
    chat = AnimaChat(ckpt_path=CKPT, device='cpu')
    print(f"  loaded in {time.time() - t:.1f}s")

    arm_totals = {arm: [] for arm in ARMS}
    arm_outputs = {arm: [] for arm in ARMS}

    for arm_name, sys_prompt in ARMS.items():
        for p_idx, prompt in enumerate(PROMPTS):
            chat.hard_reset()
            if sys_prompt is not None:
                chat.system(sys_prompt)
            t1 = time.time()
            try:
                output = chat(prompt, max_new=MAX_NEW, mode='standard_greedy', seed=SEED)
                wall = time.time() - t1
                sc = simple_stack_score(output)
                arm_totals[arm_name].append(sc['total'])
                arm_outputs[arm_name].append({'prompt': prompt, 'output': output, 'score': sc, 'wall': round(wall, 1)})
                print(f"  {arm_name} p{p_idx} ({wall:.1f}s): {sc['total']}/4 — {output[:60]!r}")
            except Exception as e:
                print(f"  ERR: {e}")

    means = {arm: (sum(t)/len(t) if t else 0) for arm, t in arm_totals.items()}
    print(f"\n=== AGGREGATE ===")
    for arm, m in means.items():
        print(f"  {arm}: mean simple_stack = {m:.3f}/4 (n={len(arm_totals[arm])})")

    arm_a, arm_b, arm_c = means.get('A_no_prompt', 0), means.get('B_weak_prompt', 0), means.get('C_strong_prompt', 0)
    f1 = arm_a >= arm_b * 0.95
    f3 = arm_c <= arm_a * 1.10
    print(f"\n  F-P1-UPGRADE-1 (A ≥ B × 0.95): A={arm_a:.3f} vs B*0.95={arm_b*0.95:.3f} → {f1}")
    print(f"  F-P1-UPGRADE-3 (C ≤ A × 1.10): C={arm_c:.3f} vs A*1.10={arm_a*1.10:.3f} → {f3}")

    out = {
        'cycle': 'p1 truncated 15-gen evidence',
        'config': {'ckpt': 'phase1a4', 'arms': list(ARMS), 'seed': SEED, 'prompts': len(PROMPTS), 'max_new': MAX_NEW},
        'arm_means': means,
        'arm_totals': arm_totals,
        'arm_outputs': arm_outputs,
        'falsifier': {'F-P1-UPGRADE-1': f1, 'F-P1-UPGRADE-3': f3},
        'wall_total_sec': round(time.time() - t, 1),
    }
    with open('/Users/ghost/core/anima/state/clm_v1_step0_p1_real_2026_05_15/p1_truncated_result.json', 'w') as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\nSaved + wall {out['wall_total_sec']}s")


if __name__ == '__main__':
    main()
