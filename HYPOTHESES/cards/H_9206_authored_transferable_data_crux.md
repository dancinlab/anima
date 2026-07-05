# H_9206 — Authored-Transferable-Data (ATD) crux for the G1 escape

**tier:** ⏳ PROPOSED (pre-registered · bars frozen before run · p7 no tune-to-green)
**scope:** the single untested claim gating the G1 escape / 303M authored-corpus fire
**artifact:** `state/g1_authored_transferable_data/`

## 가설

G1 재조합 벽은 **TARGET/DATA 전이가능성 벽**으로 수렴했다 (sweep #3031: bilinear binding 기구는 전이가능 타겟이면
전이함 · crux #3032: 실 303M+collocational corpus 합성은 additive, FiLM≈additive Δ=−0.0005 · F2/heldout_recomb:
기존 코퍼스는 collocation-only, true held-out n=0). 남은 유일 탈출 = **저작된 전이가능형 데이터 + 아무 bilinear 기구**.
이 가설의 미검증 핵심: **저작된 전이가능 데이터를 byte-LM의 순수 next-token CE로 학습하면 전이가능 bilinear 합성
기하가 실제로 유도되는가, 아니면 CE가 데이터와 무관하게 도로 additive로 붕괴시키는가?**

## 배터리 (Fable 설계 · frozen bars)

- **ATD-0 VALID-ANCHOR** (numpy·ground-truth z·LM無·하드게이트 FIRST): additive R²≤0.10 ∧ bilinear R²≥0.90 ∧
  비교환 |corr|≤0.3 ∧ name-leak R²≤0.05 ∧ eval pair∉corpus. 하나라도 실패=harness INVALID(생성기 수정, tune 아님).
- **ATD-1 REP-CRUX** (#3032 미러): byte-LM(4L d256, 순수 CE, head scaffold無, 3seed summer) 학습 → held-out disjoint
  개념쌍서 FiLM vs additive cross-R². **PASS: Δ≥+0.10 median ∧ 전seed>+0.05 ∧ shuffle-drop≥0.15 ∧ ATD-1b
  held-out R²≥0.5 ∧ permutation-null≤0.02. KILL: Δ≤+0.03(ATD-0 valid).**
- **ATD-2 BEHAV-RECOMB**(동일 학습): held-out payload greedy-decode per-dim acc≥40% ∧ swapped<0.5×true.
- **ATD-3 LADDER**: λ∈{1,.75,.5,.25,0}·ρ∈{1,.6,.3,.1} dose-response → F2 코퍼스 레시피(λ*,ρ*). **λ=0은 Δ≈0(#3032)
  재현 필수 내부통제 — λ=0서 Δ>0.05면 harness가 bilinearity 인위생성=전 verdict INVALID.**
- **ATD-4 ARCH-GUARD**: ConvMoE 토이(303M=CLMConvMoE) 동일 측정 — transformer-only PASS는 fire 미허가.
- **ATD-5 DILUTION-GUARD**(최강 adversarial): 저작코퍼스를 자연 필러에 f∈{100,30,10,3}% 희석 — 깨끗한 100%
  대수코퍼스는 localization 강제로 bilinearity 인위유발, 실 303M은 희석. **fire-feasible: f≤30%서 PASS 必.**

## 303M fire go/no-go (조건부)

ATD-1&2 PASS ∧ λ=0 붕괴재현 ∧ ATD-4 PASS ∧ ATD-5 f≤30% → **GO**(레시피대로 authored corpus 빌드 →
303M continue-train → TERMINAL은 `anima evaluate --py` G1 + 재학습 rep의 #3032 crux Δ 양전환만). ATD-1 KILL →
**결정적 negative**(publishable): authored-corpus-only fire NO-GO, objective측 재개(authored-data aux-bilinear /
γ H_1840-on-authored — H_1602 additive-aux는 collocational이라 신규셀). toy=DIRECTIONAL, 303M core/-decode만 TERMINAL.

## 근거 링크
- crux #3032 `state/transfer_mechanism_sweep/film303/` · sweep #3031 · F2 `state/g1g6_exhaustive_brainstorm/f2_datapath/`
- E1 4-rung `state/g0g6_premise_b_derisk/` · ARCHITECTURE `gate-g1-recombination` 서브트리
