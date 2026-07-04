# fleet-full RESEARCH 보고 — g1-census-escape (직교 mechanism-family census)

## (b) 핵심 판정 먼저: coverage+RF는 **이미 engine-native로 측정됐고 REFUTED다**

임무 브리프의 전제("H_6183/6184 DIRECTIONAL이면 coverage+RF가 미탐색 implement 레버")는 **이번 census로 기각**된다. 처방은 2026-07-03/04에 두 trunk에서 canonical bar(`anima evaluate --py` gen=40, torch/gauge_lib-free numpy byte mouth = 세션 terminal-eligible)로 이미 발사·채점됐다:

1. **CLM 경로** (`state/g1_coverage_realign/`, H_6188): 유발축-정합 재설계 코퍼스(mismatch probe가 지적한 프롬프트-형식 불일치까지 고친 버전)로 clm303_deep_L8(dilated conv, RF≈511 — `cli/train.hexa`에 dilation=min(2^l,512) 배선 확인) warm-FT → engine-native gen=40에서 **G1 🔴 FAIL (best_distinct=1 < max_single=3)**. train-time torch-probe(2)는 engine-native에서 미확인.
2. **ByteGPT 경로** (`state/g1_objfloor_escape/coverage_density/`, H_6185, pod 43727405): full-attention RF≥512(= H_6184 dilated-conv 목표를 포섭하는 *더 강한* RF 조건) + 조합-커버리지 en_block(C(40,2) 25% 커버, gate 쌍 held-out 무노출) warm-FT, G0 5/5 GREEN 유지 → **G1 RED floor (best_distinct=1). 명시 verdict: "FALSIFIED-CEILING — coverage-density does NOT open engine-native G1."**

측정-artifact 잔여도 닫혔다: T=24 window artifact는 byte-math로 증명됐고(`g1_breakthrough_analysis/window_identity_proof.py` — composed arm이 single arm과 byte-identical 조건화), grow-window 재측정(`g1_growwindow_remeasure/`)에서 **raw composed=2로 PASS하지만 echo-guard(novel-only, 임무가 정의한 진짜 bar) FAIL** — raw 상승분은 seed echo였다. 즉 **어느 window에서도 novel-only 재조합 floor는 유지**된다.

→ memory `g1-coverage-density-nl-bytes-lever`의 "남은=engine-native"는 stale — 그 잔여가 이 이틀 사이에 실행·기각됐다.

## (a) 직교 mechanism-family census 표

| # | family | 판정 | 근거 (reference-match / cheap-proof) | 다음 실험 |
|---|--------|------|--------------------------------------|-----------|
| 1 | readout (TPR/⊙/NMDA/PC, fixed-param·additive) | 🧱 DUP | H_9120/1812/1816 + **A11 additive 실현이 engine-native로 재확인** (`A11_engine_native/RESULT_…pod43727405.md`: cbind/cnce 둘 다 floor 0–1) | 없음 (재발사 금지) |
| 2 | coverage+RF (조합-커버리지 코퍼스 × 수용영역) | 🧱 **신규 CLOSED** | 위 (b) — 두 trunk engine-native FALSIFIED-CEILING | 없음 |
| 3 | 측정-artifact (window/echo) | 🧱 CLOSED | window artifact 실재했으나 grow-window+echo-guard로 수정 후에도 novel-only floor 유지 | 없음 |
| 4 | objective-additive (ce+λ·aux) | 🧱 DUP | H_9120 + A11 additive 재확인 | 없음 |
| 5 | objective-replace **단독** / param-selection | 🧱 DUP | E1: contrastive-replace on ADD/no-slot = 5/5 floor(ARCHITECTURAL) | 없음 |
| 6 | **A11 = objective-replace × trained-TPR-slot 상호작용 셀** (compose-read NEW op의 구체 실현) | 🔓 **미탐색 (유일한 unbuilt cell)** | toy→real-conv-trunk scale-transfer **5/5 HIT** (TPR 5/5 vs ADD 0/5, d768 7.30M, `A11_TPR_contrastive/RESULT.md`) · engine-native는 *additive 우회판만* 발사됨 — **CE-deleted forward-slot(clm_decode role-bind ops + CLMX v0.3 ext-block)은 미구축** (core grep 0 확인) | 아래 (c) |
| 7 | retrieval/lane — recall-readout | 🧱 DUP | FROZEN-1 MISS (H_9118/9122, state-only) | 없음 |
| 7′ | retrieve-into-context (L3, decode-time 주입) | 🌌-경사 | 구조 관찰: composed gate seed가 *이미* 두 개념명을 context에 주입한 상태에서 floor → 추가 주입이 attr keyword를 담으면 echo-guard가 배제, 안 담으면 gate seed와 등가. novel-only bar 하에서 win-window가 논리적으로 극히 좁음 | A11 뒤로 후순위 (cheap desk-proof로 사전 기각 가능성 높음) |
| 8 | neurosymbolic (외부 symbolic 합성기) | 🧱/🌌 분해 | **분해하면 신규성 소멸**: 내부-slot형 = family 6(A11)과 동일 셀 · 외부-composer형 = 산출을 mouth context로 되넣어야 하므로 family 7′로 환원 → echo-guard 구조 차단 | A11에 흡수 |
| 9 | sparsity-routing/MoE-routing | 🧱 DUP-경사 | H_1813 TPR-expert-weight under CE NOT-SUP — CE-basin 논거가 routing에도 적용; routing×replace 상호작용은 A11이 더 직접적으로 커버 | 없음 |
| 10 | in-context meta-learning / curriculum-scaffold | 🧱 DUP | H_1835 MLC episodic 🧱 (in-context 완벽 마스터해도 held-out transfer 0) | 없음 |
| 11 | program-synthesis | 🌌 | 외부 symbolic 경로 → family 8과 동일 환원, mouth-G1 frozen bar 정의상 echo-차단 | 없음 |

## (c) 다음 페이즈: 🛠️ **implement — A11 CE-deleted TPR forward-slot의 engine-native 실현**

미탐색 family가 정확히 1개 남았고, follow-on이 이미 등록된 구체 build-spec까지 있다(`A11_engine_native` honest-scope 절):

- **빌드**: ① `core/clm_decode.hexa`에 role-bind decode ops(circular-conv bind/unbind) ② serializer v0.3 CLMX ext-block(aux params를 drop하지 않고 mouth가 slot을 *통과*해 디코드) ③ contrastive-replace(NO CE) trainer 경로.
- **가장 싼 falsify**: toy에서 이미 검증된 **d768 · 7.30M CLMConvMoE E2/L1 구성 그대로**($0, pool GPU) engine-native로 재저작 → synthetic corpus에서 held-out pair novel-only composed bar. 렌트 불요, 303M 이전에 소형에서 mouth-generation으로 판가름.
- **전환 조건**: 소형 engine-native mouth-gen에서 novel composed ≥2 ∧ >max_single이면 → 303M scale ladder(그때만 GPU 렌트, `a_fire_recover_complete` ckpt PULL). floor면 → **G1 벽을 전 family confident-terminal로 승격**하고 escape 축을 `frontier_rebrainstorm` Family A(exogenous consequence)로 이동.
- 주의: A11 engine-native 결과가 경고하듯 signature-decode HIT는 clean-readout 성질일 수 있다 — 채점은 반드시 autoregressive mouth-generation으로만.

## (d) 정직 수렴 (c9)

**dry 아님 — 단 1셀.** "5축 falsify"는 design-matrix의 *주변부(marginal)*들이었고, A11은 그 2D *상호작용 셀*(slot×replace)이라 재포장이 아니다(ADD 0/5 vs TPR 5/5 대조가 architectural 구분을 실측). 나머지 신규 후보(neurosymbolic·program-synthesis·retrieve-into-context)는 전부 A11 또는 echo-guard 구조 논증으로 환원돼 독립 축이 아니다. A11 pure-cell마저 floor면 그때가 진짜 dry — abstract 승격(🌌 exogenous-consequence 프레임) 사유가 성립한다.

**bookkeeping 부채 플래그** (state 쓰기 금지라 본문 보고만): H_6183–6188·H_9106/9107·H_9118–9122가 `UNIVERSE/HYPOTHESES.jsonl`에 **0건** — 증거가 전부 state/ RESULT 파일에만 있다. `a_hypothesis_register` 위반 상태이므로 다음 bookkeeping 페이즈에서 카드+jsonl 등록 필요. 또한 memory `g1-coverage-density-nl-bytes-lever`의 "coverage 처방 유효" 서사는 이번 engine-native 기각으로 갱신 대상이다.
