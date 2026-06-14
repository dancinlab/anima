> 📍 SSOT: [ARCHITECTURE.md](ARCHITECTURE.md) · governance [CLAUDE.md](CLAUDE.md)

# OTHER-MIND — append-only step log

## 2026-05-28 — A4 u01 baseline-bias 진단 + 보정 (M3 closure)

- **A4 `other-mind-baseline-bias`** — bench G (#1147) 3/5 🟠 PARTIAL 의 u01
  baseline bias residual 진단 + 보정.
- **u01 bias 정체**: `u01_from(s) = s/2147483647` 이 채널을 [0,1] 양수로만 매핑
  → 모든 5-ch fingerprint 벡터가 positive orthant 에 갇힘 → `cosine_sim` 분자
  dot ≥ 0 always → 독립 벡터쌍 cosine floor 가 spurious ≈0.76 으로 들림. F1
  (INDEPENDENT < 0.3) + F4 (gap > 0.3) 가 이 floor 때문에 FAIL → 3/5.
- **보정**: zero-mean centering `c = 2*u - 1` ([0,1]→[−1,+1]) → 벡터가 전
  orthant 분포 → E[cos] → 0.
- **재측정** (foreground sync, $0 mac-local, exit 0):
  - RAW (biased, #1147 repro): INDEP 0.779862 · gap 0.197 · **3/5**
  - CENTERED (A4): INDEP 0.0165713 · gap 0.892 · **5/5**
  - orthant-bias probe (n=400): E[cos] raw 0.763021 vs centered −0.0275306,
    bias magnitude 0.790552.
- **Verdict (verbatim)**: `🟢 RECOVERED — centering raised score >= 4/5,
  u01 bias = normalization defect`. RESULT_JSON verdict = `GREEN_RECOVERED`.
  Falsifier 미발동 — bias 는 substrate 본질이 아니라 측정 결함.
- **artifacts**: `OTHER_MIND_A4_BASELINE_BIAS.md` (10-section) ·
  `state/other_mind_a4_baseline_bias_2026_05_28/{a4_bias_corrected.hexa, run.log}`.
- M3 milestone → done. deletion 0.