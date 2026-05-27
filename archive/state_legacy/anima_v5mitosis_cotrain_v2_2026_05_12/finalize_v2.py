"""state/anima_v5mitosis_cotrain_v2_2026_05_12/finalize_v2.py

Post-result summary + suggested edit hints for v2 cotrain.
Run after cotrain_result.json is pulled.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULT_JSON = HERE / "cotrain_result.json"


def main():
    if not RESULT_JSON.exists():
        print(f"ERROR: result.json not found at {RESULT_JSON}")
        return 1

    with open(RESULT_JSON) as f:
        d = json.load(f)

    t = d.get("training", {})
    fa = d.get("falsifier_aggregate", {})
    fs = d.get("falsifiers", {})
    p4 = d.get("f_persona_4_remeasure", {})
    cfg = d.get("config", {})

    print("=" * 70)
    print("v5-mitosis cotrain v2 SCALE-UP — PSCC §46 result summary")
    print("=" * 70)

    print("\n== Config ==")
    print(f"  d_model:       {cfg.get('d_model')}")
    print(f"  n_head:        {cfg.get('n_head')}")
    print(f"  ffn_dim:       {cfg.get('ffn_dim')}")
    print(f"  max_cells:     {cfg.get('max_cells')}")
    print(f"  readout_mode:  {cfg.get('readout_mode')}")

    print("\n== Training ==")
    print(f"  wall (hr):            {t.get('wall_hours', 0):.2f}")
    print(f"  cost ($):             {t.get('cost_usd_actual', 0):.2f}")
    print(f"  cap ($):              {t.get('cost_cap_usd', 0):.2f}")
    print(f"  cost_aborted:         {t.get('cost_aborted')}")
    print(f"  steps actual:         {t.get('steps_actual')}/{t.get('steps_planned')}")
    print(f"  n_cells_final:        {t.get('n_cells_final')}")
    print(f"  splits total:         {t.get('splits')}")
    print(f"  merges total:         {t.get('merges')}")
    print(f"  n_params_final:       {t.get('n_params_final', 0):,}")
    print(f"  loss initial avg100:  {t.get('loss_initial_avg100'):.4f}")
    print(f"  loss final avg100:    {t.get('loss_final_avg100'):.4f}")
    print(f"  loss delta:           {t.get('loss_delta'):.4f}")
    print(f"  phi best:             {t.get('phi_best', 0):.4f}")
    print(f"  phi final:            {t.get('phi_final', 0):.4f}")

    print("\n== Falsifiers (F-V5MIT-1..5) ==")
    for fid in ["F-V5MIT-1", "F-V5MIT-2", "F-V5MIT-3", "F-V5MIT-4", "F-V5MIT-5"]:
        f = fs.get(fid, {})
        passed = f.get("passed")
        verdict = "PASS" if passed else "FAIL"
        print(f"  {fid}: {verdict}")
        for k, v in f.items():
            if k not in ("test", "passed", "details"):
                if isinstance(v, float):
                    print(f"      {k}: {v:.6g}")
                else:
                    print(f"      {k}: {v}")

    print(f"\n  aggregate: {fa.get('n_pass')}/{fa.get('n_total')} {fa.get('verdict')}")

    print("\n== F-PERSONA-4 cotrained-pool re-measure (★ key metric) ==")
    print(f"  verdict:    {p4.get('verdict')}")
    print(f"  mean_kl:    {p4.get('mean_kl', 0):.6f} nats")
    print(f"  threshold:  {p4.get('threshold', 0.5)}")
    print(f"  n_pairs:    {p4.get('n_pairs')}")
    cats = p4.get("categories") or []
    print(f"  categories: {cats}")
    mat = p4.get("kl_matrix") or []
    print(f"  kl_matrix:")
    for r, row in enumerate(mat):
        try:
            print(f"    [{r:>2} {cats[r] if r < len(cats) else '?':>16}] {['%.4f' % v for v in row]}")
        except Exception:
            print(f"    [{r}] {row}")

    print("\n== D3 cond #3 status transition ==")
    p4_pass = p4.get("verdict") == "PASS"
    print(f"  cheap-path baseline (PSCC §42): STRONG 4/5 (F-PERSONA-4 FAIL @ untrained)")
    print(f"  v1 (PSCC §44) cotrain pool:      F-PERSONA-4 FAIL (KL=0.0 winner-take-all)")
    print(f"  v2 (PSCC §46) cotrain pool:      F-PERSONA-4 {p4.get('verdict')}")
    print(f"  D3 transition:                   STRONG → {'☑ DONE 5/5' if p4_pass else 'STRONG 4/5 carry'}")

    print("\n== Mission contribution ==")
    if p4_pass:
        print("  GOAL.md aggregate: 3/5 ☑ → 4/5 ☑ (cond #3 추가)")
        print("  remaining: cond #1 SFT only")
        print("  HF push: ENABLED (F-PERSONA-4 gate met)")
    else:
        print("  GOAL.md aggregate: 3/5 ☑ (no change)")
        print("  cond #3: STRONG (4/5 cheap-path) carry")
        print("  HF push: GATED (use FORCE_PUSH=1 to override)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
