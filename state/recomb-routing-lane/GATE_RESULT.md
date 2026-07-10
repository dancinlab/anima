# GATE 결과 — fork-A CLML lane (recomb-routing-lane · 2026-07-09)

no-copy 재설계(Fable 4-gate) 후 실 303M(e1_slw_303m) 측정 · aiden/summer anima-py · $0-pool.

## 🟢 Gate 1/2 PASS — 신호벽 아님 (clml_gate12_RESULT.json)
- **Gate 1** base(lane-OFF) CE=**1.044 nat** · next-byte acc=0.65 → 잔차 EXISTS (copy-format의 CE 0.0003과 대조 = 트렁크가 no-copy 위치는 못 함).
- **Gate 2** probe pool_yn→word-id: TRAIN **0.825** · held **0.600** (chance 0.04) → frozen pool이 name→word 라우팅을 담고 **일반화**.
- ⟹ 🟢 TRAINABLE — fork-A route가 학습가능(H_1840 신호벽 아님). copy-trap(#3210)이 진짜 원인이었고 no-copy 형식이 그걸 해소.

## 🟢 Gate 3 PASS — lane 실제 학습 (clml_train_RESULT.json · clml_lane.npz)
- word-initial CE로 lane {W1,b1,W2,w_g,b_g} 학습: CE lane-ON **1.044→0.718**(Δ-0.33)·acc 0.65→0.73·gate 0.05-0.10 열림. copy-format(Δ≈0 死)과 대조.
- ⚠ train-CE 개선(seen)이지 held 생성 아님 — Gate 4가 진짜 바.

## 🔴 Gate 4 — engine-native G1 재조합 lane-ON vs lane-OFF (2026-07-10 · summer)

**verdict: 🔴 DIRECTIONAL FAIL — TERMINAL 아님 (정정: 앞서 #3291서 🧱로 조기판정, verdict-integrity 정정).** raw = `gate4_g1_verdict_raw.txt` · Fable 재프레임 = `fable_gate4_reframe.md`.

**⚠️ 정정 사유 (2건):**
1. **frame-mismatch**: `eval_rho_weave`(evaluate.py:170)는 `mouth.ideate(cz/g_comp 페르소나 개념)` ideation 재조합을 잰다(코드확인) — lane이 학습한 **held-out concept-pair와 다른 개념셋**. 즉 bd=1 FAIL은 "lane 무력"이 아니라 "lane 학습 target과 무관한 것을 측정"(--rho-axon lane-blind와 같은 계열 함정, convergence `evaluate-py-8`). lane-정합 engine-native 측정 아님.
2. **병렬세션 더 깊은 캠페인 무시**: main-dir untracked(origin/main 미커밋·convergence `clml-py-1` fork-A 2세션 중복)에 contrastive swap-margin 캠페인 존재(`step2_*`·`fable_swapcontrastive_*`·`swap_margin_retrained.json`·`step2_oracle.py`). Fable 실측: 설계된 성공경로 contrastive(n=132)=**VOID**(gate_fire_frac=0·lit_alive=false 양성대조사망·contrast_top1=0.528≈chance) · plain-CE swap-margin=**on≈shuf**(+0.028≈+0.029 generic smoothing, directional) · oracle-pool(최유리멤버)=**미실행**. 사전등록 기준(fable_swapcontrastive_result.md §4)상 VOID→INVALID, 🧱-불가.

측정: `anima-py evaluate <clm>`(**default G-battery·NOT --rho-axon** — `eval_rho_weave` H_1129 mouth-generation-based, lane-sensitive) · lane-ON(`e1_slw_303m_clml.clm` r=128) vs lane-OFF(`e1_slw_303m.final.clm` base+SLW). summer idle(aiden 30h wedge 이전).

| | ρ·weave (G1) | best_distinct | ρ·form (G0) |
|---|---|---|---|
| **lane-ON (CLML)** | 🔴 FAIL 🧱 | **1** (need ≥2 & >max_single=1) | 🟢 PASS 5/5 |
| **lane-OFF (base)** | 🔴 FAIL 🧱 | **1** (need ≥2 & >max_single=2) | 🟢 PASS 5/5 |

- **lane-ON best_distinct=1 == lane-OFF best_distinct=1** → CLML lane이 재조합에 무개선. 벽이 fork-A에 버팀.
- **verdict-integrity CLEAN**: lane-ON≠lane-OFF(max_single 1 vs 2·coherent 15 vs 19) = 측정이 **lane-sensitive**(--rho-axon 패널의 lane-blind IDENTICAL과 대조·convergence evaluate-py-7). ρ·form 🟢 = broken-run 아님. G0 no-regress OK.
- **"route≠generation" 확정**: Gate1/2/3(route 학습가능·$0 pre-check XOR 0.98·word-initial CE 1.044→0.718)는 PASS했으나, 학습된 lane이 **held-out engine-native 생성(G1)으로 전이 안 됨**. lane은 자기 학습분포(word-initial)만 개선, G1 재조합 task엔 무력.
- ⚠️ 선행 무효런: `--rho-axon` 6hr 런(gate4_laneon/off.txt)은 ρ·weave=PENDING·lane-blind라 verdict 무자격(convergence evaluate-py-7).

**진단(Fable, `fable_gate4_reframe.md`):** 최유력 = **H4 read-side additive-into-frozen-readout가 identity를 content로 못 읽음** — route는 frozen readout가 안 읽는 좌표계에 존재(probe는 pool 위 자기head end-to-end 학습=YES, lane은 frozen readout에 additive bias만=NO) = route≠generation 정체. tau-clip(H3)·용량 r=128(H2)은 반증(tau=8 비활성·pre-check 동클래스 XOR 0.98).

**NEXT (terminal 🧱 아님 · $0 pool · a_h_continuous_no_branch 자율):**
1. **병렬세션 캠페인 정합** — main-dir untracked contrastive/oracle work를 canonical state로 커밋·정리(2세션 중복 종결, clml-py-1).
2. **각도 🅰️ (MUST-FIRST)**: 계측기 복구(gate_fire_frac=0·lit_alive=false 하니스버그) → **양성대조 살린 상태로** 사전등록 oracle-pool(고정 uniform pool·Wo만 학습·최유리멤버) 실행. oracle lit_alive=true서 Dzero≈0 → **그때가 frozen-final-state readout class의 clean 🧱**(scoped 벽, trunk-G1 천장 아님). oracle crack → lane class 생존.
3. 잔여 새 family(각도 🅱️ mid-stack tap · 🅲 곱셈 readout, 죽은레버 비중복·H_9261 대조필요) = 🅰️ clean FAIL 착지 **후**.
- γ trained-constructive-bind(H_1840, STEP-0 frozen)이 "유일 잔여"가 되는 건 🅰️ clean FAIL 이후지 지금 아님(Fable 정정).
