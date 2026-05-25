# Post-pull V14 strict — run AFTER orchestrator completes ckpt pull

Once `state/anima_la_cotrain_retrain_b_to_a_2026_05_11/ckpts/ckpt_final.pt` exists:

```bash
# 1. Verify B' ckpt landed
ls -la state/anima_la_cotrain_retrain_b_to_a_2026_05_11/ckpts/

# 2. Run V14 strict on B' (Mac local, no H100, $0)
#    Adapt state/anima_v14_max256_b_no_cotrain_2026_05_10/run_b.py with B' ckpt path:
cp state/anima_v14_max256_b_no_cotrain_2026_05_10/run_b.py \
   state/anima_la_cotrain_retrain_b_to_a_2026_05_11/run_b_prime.py

# Edit run_b_prime.py — replace substrate path with B' ckpt:
sed -i.bak 's|/.../bg_la_350m_pretrain/ckpts/step_12000_final.pt|state/anima_la_cotrain_retrain_b_to_a_2026_05_11/ckpts/ckpt_final.pt|g' \
   state/anima_la_cotrain_retrain_b_to_a_2026_05_11/run_b_prime.py

# 3. Execute V14 strict (n=5 seeds × max=256 paired vs random mirrors)
cd ~/core/anima && /usr/bin/python3 \
    state/anima_la_cotrain_retrain_b_to_a_2026_05_11/run_b_prime.py \
    | tee state/anima_la_cotrain_retrain_b_to_a_2026_05_11/v14_strict.log

# 4. Falsifier disposition per spec:
#    F-CAUSAL-1 (cotrain causal direction): B' V14_STRICT_PASS → CAUSAL confirmed
#                                            B' V14_VIOLATED   → cotrain is confound
#    F-CAUSAL-2 (q_proj delta direction): compare B' vs A q_proj cos
```
