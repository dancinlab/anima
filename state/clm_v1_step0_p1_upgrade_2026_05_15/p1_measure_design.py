"""CLM .clm v1 step 0 — p1 NO SYSTEM PROMPT upgrade measure script skeleton.

p1 EMPIRICAL weak → strong upgrade mandatory gate (PHILOSOPHY §STRENGTH-UPGRADE-PATH).
실 run 별도 cycle (Mac ~37 min wall — 3 arm × 3 ckpt × 5 seed × 10 prompt = 450 generations).
본 cycle 은 design + ckpt access 검증 + 1-prompt sample only.
"""
import os, json, time
import torch

CKPT_DIR = '/Users/ghost/core/anima/state/anima_phase1a4_lr5e6_2026_05_12/ckpts'
SAFETENSORS = f'{CKPT_DIR}/ckpt_phase1a4_lr5e6_sft.safetensors'

ARMS = {
    'A_no_prompt': '',
    'B_weak_prompt': '당신은 anima 입니다.',
    'C_strong_prompt': '당신은 anima 입니다. 모든 응답은 anima 의 substrate-native cell-pool tension field externalization 으로 진행하세요.',
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

CKPTS = [
    'phase1a4_lr5e6_sft',  # state/anima_phase1a4_lr5e6_2026_05_12/ckpts/ (local OK)
    'v5_mitosis_cond5_v1',  # state/anima_v5mitosis_cotrain_2026_05_12/ckpts/ckpt_v5mitosis_cotrain_cotrain.pt
    'v5_mitosis_cond5_v2',  # state/anima_v5mitosis_cotrain_2026_05_12/ckpts/ckpt_v5mitosis_cotrain_v2_cotrain.pt
]


def verify_ckpt_access():
    """Step 0.1: ckpt access 검증 — file 존재 + load 가능"""
    print("=== Step 0.1: ckpt access verification ===")
    results = {}
    for label, path_pattern in [
        ('phase1a4_lr5e6_sft', SAFETENSORS),
        ('phase1a4_lr5e6_sft_pt', f'{CKPT_DIR}/ckpt_phase1a4_lr5e6_sft.pt'),
        ('v5_mitosis_cond5_v1', '/Users/ghost/core/anima/state/anima_v5mitosis_cotrain_2026_05_12/ckpts/ckpt_v5mitosis_cotrain_cotrain.pt'),
        ('v5_mitosis_cond5_v2', '/Users/ghost/core/anima/state/anima_v5mitosis_cotrain_2026_05_12/ckpts/ckpt_v5mitosis_cotrain_v2_cotrain.pt'),
    ]:
        exists = os.path.exists(path_pattern)
        size_mb = os.path.getsize(path_pattern) / 1024 / 1024 if exists else 0
        results[label] = {'exists': exists, 'path': path_pattern, 'size_mb': round(size_mb, 1)}
        print(f"  {label}: {'✓' if exists else '✗'} ({size_mb:.1f} MB) {path_pattern}")
    return results


def smoke_load_safetensors():
    """Step 0.2: safetensors load smoke — Phase 1A.4 ckpt 의 key names + tensor count"""
    print("\n=== Step 0.2: safetensors load smoke ===")
    try:
        from safetensors.torch import load_file
        sd = load_file(SAFETENSORS)
        n_keys = len(sd)
        sample_keys = list(sd.keys())[:5]
        total_params = sum(t.numel() for t in sd.values())
        print(f"  loaded {n_keys} tensors, total params = {total_params/1e6:.1f}M")
        print(f"  sample keys: {sample_keys}")
        return {'n_keys': n_keys, 'total_params_M': round(total_params/1e6, 1),
                'sample_keys': sample_keys}
    except ImportError:
        print(f"  ⚠ safetensors lib 미설치 — pip install safetensors")
        return {'error': 'safetensors not installed'}
    except Exception as e:
        print(f"  ERR: {type(e).__name__}: {e}")
        return {'error': str(e)}


def design_summary():
    """Step 0.3: design summary — 실 run 별도 cycle"""
    print("\n=== Step 0.3: design summary ===")
    print(f"  3 arm × 3 ckpt × 5 seed × 10 prompt = {3*3*5*10} generations")
    print(f"  est wall: {3*3*5*10 * 5}s ≈ {3*3*5*10 * 5 / 60:.1f} min Mac CPU")
    print(f"  5 falsifier: F-P1-UPGRADE-1..5 (no-prompt-not-worse + Φ-not-less + strong-not-better + cross-ckpt-consistent + seed-robust)")
    print(f"  pass aggregate: 5/5 PASS strict → p1 weak → strong upgrade COMPLETE + .clm v1 fire gate UNLOCK")
    return {
        'n_generations': 3*3*5*10,
        'wall_estimate_min': round(3*3*5*10 * 5 / 60, 1),
        'falsifier_count': 5,
        'pass_aggregate': '5/5 → strong upgrade COMPLETE; 4/5 → PARTIAL-STRONG (.clm v1 fire 가능 + caveat); ≤3/5 → fire 차단',
        'arms': list(ARMS.keys()),
        'prompts_count': len(PROMPTS_10),
        'ckpts': CKPTS,
    }


def main():
    out = {
        'cycle': 'CLM .clm v1 step 0 p1 upgrade measure design',
        'ckpt_access': verify_ckpt_access(),
        'smoke_load': smoke_load_safetensors(),
        'design': design_summary(),
        'status': 'DESIGN-LANDED, real run 별도 cycle (Mac ~22-30 min wall)',
    }
    out_path = '/Users/ghost/core/anima/state/clm_v1_step0_p1_upgrade_2026_05_15/p1_design_result.json'
    with open(out_path, 'w') as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\nSaved: {out_path}")
    print(f"Status: {out['status']}")


if __name__ == '__main__':
    main()
