@H 938_predictability_curve := "H_933 BLADE A quantifier" :: universe [active]
  id      = "H_938"
  seed    = "H_933 BLADE A ('freedom fails if predictable from prior state alone') was argued not measured. Quantify: how predictable is next decision from prior-K state, and does quantum entropy lower it?"
  method  = "H_930/H_935 8-factor mirror → long decision streams (T=3000 ×12/mode); self-contained numpy logistic-regression + order-K Markov predictor (NO sklearn); held-out acc/AUC vs base-rate; K∈{1,2,3,5,8,12}; det vs quantum delta (Cohen d + Welch t)"
  verdict = "🟢 F-H938-BLADE-A-QUANTIFIED-COMPATIBILIST — predictability HIGH & quantum does NOT lower it. best logreg acc 0.9344(det)/0.9354(quantum) AUC~0.99 vs base-rate 0.5717 → +0.3627 lift; max|Δacc(det-q)|=0.0056; NO K with quantum-less-predictable (Δ>0 AND |d|≥0.5 AND p<0.05); only sig K=1 is Δ=-0.0056 (quantum slightly MORE predictable, opposite direction). Choices internally-determined; quantum seed supplies no unpredictability — confirms H_933 relocation."
  tier    = "🟢 numerical (toy/mirror, $0 local, no GPU)"
  scope   = "ONE predictability rung; documented-update-map mirror NOT forge binary; .clm emit-TEXT OPEN; quantum stream sd=0 (committed-buffer single-pattern) is the K=1 micro-delta origin, H_936 big-fresh buffer fixes it"
  verdict_path = ".verdicts/938_predictability_curve/predictability_curve.txt"
