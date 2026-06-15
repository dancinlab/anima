> 📍 SSOT: [ARCHITECTURE.md](ARCHITECTURE.md) · governance [CLAUDE.md](CLAUDE.md)

# HANDOFF — CLM MITOSIS-ARRAY 돌파엔진 (DISSOLVE + BRIDGE 양 arm) 2026-05-30

## 1. 목표 / 범위

CLM 의 **측정-타당성 ⊥ AKIDA 온칩** 정면충돌(H_847 routing-z 가 tiny~small 2.70M 한정인 근본 이유 · a_scale_honest_scope)을 돌파하는 엔진 **MITOSIS-ARRAY** 를 `CLM.breakthrough.mining.md` DISSOLVE(depleted-both) 결론으로부터 end-to-end 구현. **양 arm 전부 풀구현**(@L1): DISSOLVE(harness+run) + BRIDGE(distill pipeline+GPU fire). 5-PR stacked, 각 isolated-worktree off origin/main, commit→admin-merge→origin-verify.

## 2. 랜딩 결과 (5 PR 전부 origin/main MERGED + verified)

| PR | # | 내용 | 상태 |
|---|---|---|---|
| PR1 | 1506 | P0 §11 MITOSIS-ARRAY 설계(DISSOLVE) + CLM.md/log | ✅ MERGED |
| PR2 | 1507 | DISSOLVE harness — array_moe.py(sparse-MoE+dispatch entropy)+array_smoke.py(5/5 PASS)+hexa | ✅ MERGED |
| PR3 | 1509 | DISSOLVE run — run_array_sweep.py + H_852 + CLAIMS + verdict 🔴 | ✅ MERGED |
| PR4 | 1510 | BRIDGE distill — distill_array.py+run_bridge_transfer.py+hexa+run.sh+README | ✅ MERGED |
| PR5 | (this) | BRIDGE verify — H_853 + CLAIMS + verdict 🔴 + HF + HANDOFF | ✅ |

## 3. DISSOLVE 결과 (H_852 F-CLM-MONO-ARRAY 🔴 CLOSED-NEGATIVE)

scale 축을 model-dim → **expert-COUNT** 로 reframe(@L2). big=Σ chip-fit expert(각 ≤AKD1000 1.2M). routing-diversity 재정의 = expert-count sweep inter-expert dispatch entropy(chip-native).

측정: E∈{4,8,16,32,64} × seed{42,43,44} · Dirichlet(1) uniform-null z-score · $0 Mac · frozen pre-run.

| E | mean_z | mean_H(nats) | chip_fit |
|---|---|---|---|
| 4 | +0.526 | 1.186 | ✅ |
| 8 | +0.072 | 1.726 | ✅ |
| 16 | −0.884 | 2.259 | ✅ |
| 32 | −2.040 | 2.846 | ✅ |
| 64 | −7.614 | 3.171 | ✅ |

**충돌이 z-척도 상 dissolve 되지 않음**: raw H 는 E 로 상승(절대 다양성 ↑) 하나 uniform-null z 는 급락. uniform ceiling 이 ln(E)로 커져 큰 array 가 짧은 학습으로 균형 천장을 못 채워 더 sub-uniform 으로 측정. monotone+z-rise FAIL · chip-fit PASS.

## 4. BRIDGE 결과 (H_853 F-CLM-BRIDGE-XFER 🔴 CLOSED-NEGATIVE)

teacher(E32/d128 유효 측정 scale) escape 측정 → Hinton KD distill(α=0.7 T=3.0) → chip-fit student(E8/d64) → transfer Δ. **GPU FIRE = ubu-1 RTX5070(dedicated pool host · $0 marginal · torch 2.12)**, a_fire_autonomous.

| seed | teacher_z | student_z | Δ | same-sign | chip-fit |
|---|---|---|---|---|---|
| 42 | −2.22 | +0.99 | 3.21 | ✗ | ✅ |
| 43 | −4.58 | +1.13 | 5.70 | ✗ | ✅ |
| 44 | −4.43 | −0.33 | 4.10 | ✅ | ✅ |
| mean | −3.74 | +0.60 | 4.34 | ✗ | ✅ |

**transfer 가 생존 못함**: teacher sub-uniform(z<0) → student distill 후 near-uniform(z≈0). chip-fit student 가 teacher escape 서명을 흡수 않고 **균형 routing 으로 회귀**. KD soft-target 은 logit-level 지식은 전달하나 inter-expert dispatch-distribution 서명은 전달 못함(별개 자유도). |Δ|>3.0 · 2/3 sign-flip.

## 5. GPU 비용

**$0 marginal** — BRIDGE fire 는 dedicated pool host ubu-1(RTX5070, already-owned)에서 실행. rented runpod pod 0개. DISSOLVE 측정은 $0 Mac local CPU. teardown 불요(dedicated host).

## 6. HF (a_hf_autonomous tier-gated)

- `dancinlab/anima-clm-bridge` **PRIVATE**(🔴 negative-result) — teacher(1.79M)+student(169800, chip_fit) .pt + README 모델카드 + manifest.json sha256(a_hf_complete). /HF.jsonl row=anima_clm_bridge.
- DISSOLVE 는 별도 ckpt 없음(sweep 측정량만) — HF 미해당.

## 7. 정직 caveat (a_scale_honest_scope · p7)

- 두 🔴 모두 **toy axis 한정**: DISSOLVE=toy expert-count sweep(d64/L2 · toy 2-lane), BRIDGE=toy teacher→student distill(d≤128). 3B 일반 주장 **금지**(toy→prod transfer 비보장, H_666).
- expert-count 축은 deploy-relevant 하나 per-unit d_model/corpus 는 toy.
- 물리 다중-AKD1000 = 현재 pi5 1칩(@L6) → inter-chip dispatch entropy 의 surrogate = inter-expert(SW/GPU). 물리 칩-간 DMA 지연만 hardware 후속.
- 추론 AKIDA-int4-only 불변(P0 d4) — DISSOLVE/BRIDGE 둘 다 GPU/CPU pretrain·측정만.

## 8. 후속 (별도 lane · 본 세션 미접촉)

- routing-distribution 직접 정합 distill 손실(dispatch-KL 항 추가) — KD 가 logit 만 정합한 게 BRIDGE 🔴 원인.
- student E ↔ teacher E 정합(작은 student pool 이 다른 평형으로 수렴).
- norm_entropy(H/ln E) 척도(smoke 0.77~0.87 안정) 를 별도 신규 falsifier 로(z-null 이 ln(E) ceiling 으로 큰 E penalize).
- H_847/H_852 AXIS_MAP(routing-diversity 직접 lever: stronger load-balance · routing temp anneal · expert-capacity) 와 합류.

## 9. 파일 / SSOT

- 설계: `CLM/P0_ARCHITECTURE.md` §11 (MITOSIS-ARRAY DISSOLVE/BRIDGE)
- DISSOLVE: `CLM/model/{array_moe.py, array_smoke.py, run_array_sweep.py, array_moe.hexa}`
- BRIDGE: `CLM/distill/{distill_array.py, run_bridge_transfer.py, distill_array.hexa, run.sh, README.md}`
- verdict: `.verdicts/clm-mitosis-array/` + `.verdicts/852_clm_mitosis_array_dispatch/` + `.verdicts/853_clm_bridge_transfer/`
- UNIVERSE: `UNIVERSE/cards/H_852_clm_mitosis_array_dispatch.md` · `UNIVERSE/cards/H_853_clm_bridge_transfer.md`
- claims: `CLAIMS.tape` (clm_mitosis_array_dispatch · clm_bridge_transfer 둘 다 TERMINAL 🔴)
- HF: `/HF.jsonl` (anima_clm_bridge) · `dancinlab/anima-clm-bridge` PRIVATE
- 출처: `CLM/CLM.breakthrough.mining.md` (DISSOLVE depleted-both)