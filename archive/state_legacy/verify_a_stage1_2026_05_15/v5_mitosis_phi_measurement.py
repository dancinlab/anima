"""
Stage 2 deep continuation — anima v5-mitosis ckpt 위 PyPhi Φ 측정
(Hc_1283 진짜 verdict + H_191 direct substrate test)

다음 cycle BG: anima_v5mitosis_cotrain v1 ckpt ($1.30 H100 LANDED) load 후
cell pool tension 추출 → PyPhi 1.2.0 IIT 3.0 Φ computation
"""
import os, sys, json
os.environ['PYPHI_WELCOME_OFF'] = 'yes'

CKPT = "state/anima_v5mitosis_cotrain_2026_05_12/ckpts/ckpt_v5mitosis_cotrain_cotrain.pt"

def main():
    print("anima v5-mitosis ckpt Φ measurement script")
    print("=" * 70)
    
    # Check ckpt exists
    if not os.path.exists(CKPT):
        print(f"❌ ckpt not found: {CKPT}")
        print("  Available ckpts:")
        import glob
        for c in sorted(glob.glob('state/anima_v5mitosis*/ckpts/*.pt'))[:5]:
            sz_mb = os.path.getsize(c) / 1024 / 1024
            print(f"    {c} ({sz_mb:.1f} MB)")
        return
    
    print(f"✓ ckpt found: {CKPT}")
    sz_mb = os.path.getsize(CKPT) / 1024 / 1024
    print(f"  size: {sz_mb:.1f} MB")
    
    # Try torch.load
    print("\nAttempting torch.load (CPU)...")
    try:
        import torch
        d = torch.load(CKPT, map_location='cpu', weights_only=False)
        print(f"  ✓ ckpt keys: {list(d.keys())[:10] if isinstance(d, dict) else type(d).__name__}")
        if isinstance(d, dict) and 'state_dict' in d:
            sd = d['state_dict']
            print(f"  state_dict params: {len(sd)}")
            # Sample shape
            for k in list(sd.keys())[:5]:
                print(f"    {k}: {sd[k].shape if hasattr(sd[k], 'shape') else type(sd[k]).__name__}")
    except Exception as e:
        print(f"  ❌ load error: {type(e).__name__}: {str(e)[:200]}")
        print(f"  → ckpt format = mitosis-specific; load 코드 anima 내부 의존")
    
    # Skip actual Φ measurement (requires anima v5-mitosis full model class load)
    print("\nActual PyPhi Φ measurement DEFERRED — requires:")
    print("  1. anima v5-mitosis MitosisV5Model class load (현재 import 실패)")
    print("  2. cell_pool tension state 추출 → binary state vector")
    print("  3. cell-coupling matrix → PyPhi Network TPM 변환")
    print("  4. PyPhi sia.phi computation (cells ≤ 8 limit)")
    print("\nVerdict: SCRIPT-READY-MEASUREMENT-DEFERRED")

if __name__ == '__main__':
    main()
