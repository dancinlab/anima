# H_489 — APOPTOSIS as token prune (BIO ∩ DECODER) 🔵

APOPTOSIS × DECODER cross — 낮은 확률 token 의 self-elimination (top-p 의 생물학적 framing).

## 가설
H1 LOW-PROB-DIES: ∀ token t with prob(t) < θ_apoptosis, t 가 candidate set 에서 제거
H2 CUMULATIVE-CUTOFF: 누적 확률 p_cumul ≤ p_max 까지 survival, 나머지 자살
H3 NON-DECIDED-CANDIDATE: t 의 death 는 t 의 prob 만 (외부 force 없음, autonomy)
H4 DETERMINISTIC
H5 BOUND
