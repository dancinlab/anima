# GATE 결과 — fork-A CLML lane (recomb-routing-lane · 2026-07-09)

no-copy 재설계(Fable 4-gate) 후 실 303M(e1_slw_303m) 측정 · aiden/summer anima-py · $0-pool.

## 🟢 Gate 1/2 PASS — 신호벽 아님 (clml_gate12_RESULT.json)
- **Gate 1** base(lane-OFF) CE=**1.044 nat** · next-byte acc=0.65 → 잔차 EXISTS (copy-format의 CE 0.0003과 대조 = 트렁크가 no-copy 위치는 못 함).
- **Gate 2** probe pool_yn→word-id: TRAIN **0.825** · held **0.600** (chance 0.04) → frozen pool이 name→word 라우팅을 담고 **일반화**.
- ⟹ 🟢 TRAINABLE — fork-A route가 학습가능(H_1840 신호벽 아님). copy-trap(#3210)이 진짜 원인이었고 no-copy 형식이 그걸 해소.

## 🟢 Gate 3 PASS — lane 실제 학습 (clml_train_RESULT.json · clml_lane.npz)
- word-initial CE로 lane {W1,b1,W2,w_g,b_g} 학습: CE lane-ON **1.044→0.718**(Δ-0.33)·acc 0.65→0.73·gate 0.05-0.10 열림. copy-format(Δ≈0 死)과 대조.
- ⚠ train-CE 개선(seen)이지 held 생성 아님 — Gate 4가 진짜 바.

## 🧱 Gate 4 (TERMINAL) — engine-native G1 재조합 lane-ON vs lane-OFF (2026-07-10 · summer)

**verdict: 🧱 FAIL — CLML fork-A lane이 engine-native G1 재조합 벽을 못 연다.** raw = `gate4_g1_verdict_raw.txt`.

측정: `anima-py evaluate <clm>`(**default G-battery·NOT --rho-axon** — `eval_rho_weave` H_1129 mouth-generation-based, lane-sensitive) · lane-ON(`e1_slw_303m_clml.clm` r=128) vs lane-OFF(`e1_slw_303m.final.clm` base+SLW). summer idle(aiden 30h wedge 이전).

| | ρ·weave (G1) | best_distinct | ρ·form (G0) |
|---|---|---|---|
| **lane-ON (CLML)** | 🔴 FAIL 🧱 | **1** (need ≥2 & >max_single=1) | 🟢 PASS 5/5 |
| **lane-OFF (base)** | 🔴 FAIL 🧱 | **1** (need ≥2 & >max_single=2) | 🟢 PASS 5/5 |

- **lane-ON best_distinct=1 == lane-OFF best_distinct=1** → CLML lane이 재조합에 무개선. 벽이 fork-A에 버팀.
- **verdict-integrity CLEAN**: lane-ON≠lane-OFF(max_single 1 vs 2·coherent 15 vs 19) = 측정이 **lane-sensitive**(--rho-axon 패널의 lane-blind IDENTICAL과 대조·convergence evaluate-py-7). ρ·form 🟢 = broken-run 아님. G0 no-regress OK.
- **"route≠generation" 확정**: Gate1/2/3(route 학습가능·$0 pre-check XOR 0.98·word-initial CE 1.044→0.718)는 PASS했으나, 학습된 lane이 **held-out engine-native 생성(G1)으로 전이 안 됨**. lane은 자기 학습분포(word-initial)만 개선, G1 재조합 task엔 무력.
- ⚠️ 선행 무효런: `--rho-axon` 6hr 런(gate4_laneon/off.txt)은 ρ·weave=PENDING·lane-blind라 verdict 무자격(convergence evaluate-py-7).

**NEXT (walls-delegate-to-fable):** 🧱 확정 전 Fable 재프레임 위임 — fork-A CLML이 route는 열되 generation 못 여는 원인(학습 task 불일치? lane 용량 r=128? bias-clip tau?) + 대안 각도. 유일 잔여 = γ trained-constructive-bind(H_1840, gate-stop STEP-0 frozen).
