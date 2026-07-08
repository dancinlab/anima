# H_9229 — Family F: discrete conceptual code (language-of-thought bottleneck) — G1-at-the-seam RANK 5

**tier:** ⏳ PRE-REGISTERED (Fable 설계 · bars frozen · p7 no tune-to-green)
> ✅ live next candidate — distinct mechanism (compositional discrete handle at the seam), survives H_9225 currency-conversion falsification.
**scope:** engine→mouth seam missing-intermediate — self⊥mouth를 output seam의 G1 재조합벽에 묶음
**cost:** **med-high** (decode + G1 machinery)
**artifact:** `state/seam_missing_intermediate/`

## 인과 척추 (공유)
mouth = RATE-GATE(미분기): urgency만 작동=이미 phasic Δ(H_9101). self(.kosmos)·tension은 TONIC LEVEL로 read 후 폐기 → ΔEff≈0(self⊥mouth·tension⊥mouth). 벽 = seam에 substrate 신호를 gate currency로 변환하는 구조 부재. 오너: "입↔엔진 사이에 뭔가 필요."

## 가설 (missing intermediate)
engine state와 decode 사이 VQ/codebook quantizer. mouth는 continuous smear가 아니라 **discrete code**를 소비. 벽: continuous decode-from-state는 compositional handle을 잃음 — self/tension은 discrete voicable token으로 매핑 안 되는 continuous smear라 wash out · urgency는 이미 ~discrete emit/silent 결정으로 매핑돼 생존. self⊥mouth를 **output seam의 G1 재조합벽**에 직접 결속.

## 배선 site (a_substrate_disjoint)
state→decode 경계의 codebook bottleneck.

## FROZEN BARS (p7 · verbatim)
- **freeze-self**: self가 distinct code를 선택 → emit 변화.
- **composition test** (G1을 seam으로 이동): 두 개념 → held-out COMBINED code.
- **shuffle-codebook 대조**: 붕괴.
- **REAL** = held-out composition이 emit을 **additive floor 위로** shade.

PASS = freeze-self code-change emit ∧ held-out composition > additive floor ∧ shuffle-codebook 붕괴.

## 상태 · 제약
**구현됨·미측정** (Fable SPEC 3 op-grip 하니스 `cli/anima.hexa` 착지 · `hexa typecheck` exit0 · wiring follow-on = CPU-pod op-grip round). 측정은 별도 CPU-pod 라운드(summer/aiden, NEVER mini)에서 `anima <ckpt.clm> --opgrip-r3`로 B2/E/F 동시 harvest. p7 no tune-to-green(loss 미포함). p5 shade-not-gate(reactive speak() 금지). a_substrate_disjoint. **cost med-high**(decode + G1 machinery — --opgrip-r3 real decode에 rides). 승격 선례 H_9097/H_9101. ⚠️ 주의: trunk G1 재조합벽은 전수-falsify된 proven ceiling(goal-biolens·substrate-framebreak-g1) — output seam에선 다르게 behave할 수도 있음이 유일 테스트 이유. honest prior = S2 fails → bar4 COMPETENT(S1) or bar6 THEATER.

## 구현 노트 (harness)
- **carriers** (Site-A, H_9225 block 확장): state8=[rel_lane,af_val,allo_ctx,coh_lane,bal_lane,nov_ctx,gap_ctx,ag_conflict](ev_axis lanes) · `vq_med[8]`(per-lane calib median split) · `vq_bias[256]`(frozen data-derived per-code bias) · `vq_cnt[256]` · `vq_shufbias[256]`(derangement c→(c·37+11)%256) · `vq_visited[256]` · `g_vq`(swing 0.175) · S2 buckets(`s2_n/s2_a_flip/s2_b_flip/s2_ab_flip`) · `og_f3_vqcode`(secondary INPERM source).
- **wire site**: B2/E arm 뒤·decode seam 앞(`if og_r3`). tick 10-49 lane 샘플→tick 50 median+per-code mean signed-mag dev→`vq_bias` frozen. code_id = Σ 2^a·(state8[a]≥vq_med[a]). shade_vq = clip01(0.5 + g_vq·vq_bias[code_id]) own DISJOINT idle lane.
- **3 arms**: LIVE(`e_vq` off `idle_vq`) · FROZEN(shade 0.5 ⇒ `idle_frzF`≡prod idle, `og_h_frzF`==0 = production emit BYTE-UNTOUCHED 증명) · POS reuse dense ARM-SHOCK. **PRIMARY theater-killer** = ARM-SHUFFLE-CODEBOOK(`vq_shufbias`, in-loop, margin_cb≥0.08) · SECONDARY tick-order INPERM(diagnostic no-bar).
- **signatures**: S1 code-selection(ΔEff≥0.10 ∧ margin_cb≥0.08) · S2 composition 2×2 bit-toggle non-additivity(A=coh_lane[3] B=ag_conflict[7]: AB−(A+B)≥0.05 ∧ n_AB≥10 = G1 BIND at seam). frozen bars 1-7 pre-reg VERBATIM.
- **⚠️ ADAPTATION** (documented): spec의 sign-only `code_bias`는 모든 same-code 샘플이 bit pattern을 공유 ⇒ **additive-by-construction**이라 S2가 0-by-construction으로 untestable. → **data-derived per-code mean SIGNED-MAGNITUDE deviation** 채택(joint code가 non-additive weight를 실을 수 있게 하는 유일 변경). "held-out" purity → "joint code fitted"로 완화(product code는 fitted-per-code∧held-out 동시 불가) · `n_AB<10`은 **bar-5 BIND 주장만** gate(S1 competence는 독립 성립).

## 근거 링크
- [[substrate-framebreak-g1-combination-operator]](G1벽=combination operator) · [[H_9233]](Family G γ bind, 같은 G1축·GPU) · H_9097/H_9101
