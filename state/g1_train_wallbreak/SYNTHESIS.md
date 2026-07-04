# G1 재조합벽 학습방법 축 break-walls 종합 (workflow w8yk7akft, 25 agent, fable 위임 없음)

## (a) deep ConvMoE L8 = CLOSED-by-H6188 (ING standing-go "OPEN"은 착각)
task 전제("single dilated conv vs deep L8 hierarchical 미측정")=FALSE. 증거:
- `state/g1_coverage_prod_block/results_gen40/SUMMARY.txt`: 실제 8-layer ConvMoE(d=2781 L=8 303.146M warm-start h1129)를 canonical gen=40 engine-native(--py numpy byte-parity, grep torch=0) 3-arm 측정: L4_clean·L8_nocov(depth-only)·L8_cov 전부 **G0 5/5 PASS ∧ G1 best_distinct=0 FAIL**. depth-only arm이 순수 hierarchical-composition 격리→G1=0(H_1598 depth FALSIFIED 정합).
- `state/g1_coverage_realign/G1_verdict.json`: H_6187 confound(surface+T24 window) 수리 후 재-warm-FT도 best_distinct=1 FAIL(벽은 confound 수리 *후* 닫힘). ConvMoE RF=dilated depthwise(1/2/4/8) stack의 composed RF≈511 = "single dilated"와 "deep L8"은 같은 아키텍처.
- 좁은 잔차: --savant --mitosis --d2960 정확조합 미측정이나 savant=EXPRESSION축·mitosis=cell-GROWTH 둘 다 trunk-OBJECTIVE 직교 basin-preserving 증폭기(scale-invariant)=predicted-floor repackage. → deep-L8 재발사 금지.

## (b) 14 레버 중 survivor(census-refute 실패, toy-DIRECTIONAL, engine-native 미시험)
- **레버1 derivation-trace 절차 코퍼스 (data축·최우선)**: target 시퀀스를 derivation 자체로 재작성(예 "jump thrice : DEF X=JUMP; RULE thrice: X X X; OUT..."). CE=echo 메타법칙 **미적용**(aux term 없음, target이 곧 derivation이라 echo=derivation 생성=composition). RF 절반을 per-step local copy로 분해(H_6184 정합). toy directional lift FLAT 3/7 vs DERIV 13/18. census3(flat-target)·H_1835(final-answer)·N15(decode-time) 전부 다른 축. 최소비용 조기-kill=FLAT baseline arm 동일 fixture. ~1 GPU-hr warm-FT(summer free). 잔여 위험=H_1822 copy-head 벽.
- **레버2 STaR/verifier-filtered self-distillation**: CE-gradient 유지(≠param-ES/A11 CE-delete), best-of-K 샘플→composition-TRUE verifier(surface G1 detector 아님, kosmos-grounded)→verified HIT를 hard CE target으로 relabel+mix→반복(compounding ratchet). STEP-0 $0 early-kill: base h1129c best-of-K decode로 |V0| 측정, |V0|/(K·n)<0.02면 STaR STARVES=FALSIFIED-AT-FLOOR. crack=coverage-in-disguise·toy-optimism(303M floor면 verified set 空)·MANDATORY fab-control(verifier=surface-detector arm은 fab 팽창해야).
- (+레버 2개 truncated, 광역 ledger γ trained-constructive-bind H_1840 미발사)

## 종합
학습축 dry 아님. deep-L8 sub-lens 닫힘, survivor 4레버 303M engine-native 미시험. 최소비용 최우선=레버1 derivation-trace(summer ~1 GPU-hr). 전부 tier=DIRECTIONAL, terminal=anima evaluate --py engine-native 채점.
