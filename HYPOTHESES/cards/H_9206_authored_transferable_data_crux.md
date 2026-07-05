# H_9206 — Authored-Transferable-Data (ATD) crux for the G1 escape

**tier:** 🧱 KILL (measurement-clean · caveat 해소 · toy=DIRECTIONAL, 303M만 TERMINAL)
**scope:** the single untested claim gating the G1 escape / 303M authored-corpus fire
**artifact:** `state/g1_authored_transferable_data/` (ATD0/ATD1/ATD_CLEANGEOM_RESULT.json · logs)

## 결과 (2026-07-05 · summer 3seed)

- **ATD-0 anchor**: PASS 5/5 (생성기 결함 2건 잡아 수정 → VALID).
- **cap-probe**: in-corpus behav 0.17→0.74 @ d384/6L/12k = harness 해석가능화(toy가 과제 in-dist 학습).
- **ATD-1 rep-crux frozen VERDICT = KILL-CE-COLLAPSES-TO-ADDITIVE**: λ=1(저작전이) med_Δ(FiLM−add)=−0.020(전seed≤0)
  ≤ kill 0.03 · λ=0(collocation) med_Δ=−0.082(≈0 정상통제). 저작 전이데이터로도 byte-LM CE가 전이가능 bilinear
  GEOMETRY 미유도.
- **⚠️ verdict-integrity 단서**: rep-crux add/film R² 둘다 음수(−4.1)=held-out readout 외삽실패 → Δ는 geometry
  판정에 measurement-limited(clean #3032처럼 +R²가 아님).
- **ATD-2 behav (clean·DIRECTIONAL)**: λ=1 held-out 재조합 0.152(2.5×chance·swap 0.061=순서민감 genuine bind)
  > λ=0 0.062(=chance) = 저작 전이데이터가 collocation 대비 **약하지만 실재하는** held-out 전이 부여. 단
  0.15 ≪ in-corpus 0.74 = 거대 일반화갭.
- **종합**: strong claim(전이 bilinear geometry 유도)=미지지 KILL-lean · weak claim(저작>collocation held 전이)=
  behav 지지 DIRECTIONAL. escape가 100% 농도서도 약함 → ATD-5 희석 무의미·**303M authored-only fire NO-GO**.
- **✅ caveat 해소 — clean-geometry probe (well-posed target)**: rep-crux의 음수-R²가 KILL을 흐릴까 봐, 모델
  singles가 held-out서 **ground-truth t(z_a,z_b)**(bounded·well-posed)를 additive vs FiLM로 복원하는지 재측정.
  VERDICT=**CLEAN-KILL-no-recoverable-transferable-bilinear**: λ=1 med_Δ=−0.024·med_film R²=−0.29 · λ=0통제
  med_Δ=−0.028·−0.28 = **동일 floor**. 이전 −4.1은 OOD-joint-rep readout 외삽 아티팩트였고, well-posed에서도
  R² 음수(−0.1~−0.3)+FiLM 무이득 = held singles에 복원가능 전이 bilinear 구조 **無**. KILL은 measurement-clean.
  게다가 behav의 약한 λ=1 우위(0.152)조차 geometry로는 통제와 동일 floor = recoverable transferable bilinear
  rep 아님(약신호는 memorization-leak 계열). ⟹ 저작데이터-단독 escape = 토이서 clean 미지지.
- **reopen 저비용 잔여**: ATD-3 ρ-density ladder · objective측(authored-data aux-bilinear = H_1602 additive-aux와
  다른 신규셀 · γ H_1840-on-authored). ⚠️실 코퍼스는 anima corpus derivtrace 유도가 canonical(#3043)이지 hand-gen 아님.

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
