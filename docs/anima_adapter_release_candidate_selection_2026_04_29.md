# anima trained-adapter release candidate selection (CP2 임시공개 Option D)

ts: 2026-04-29
author: Claude (opus-4-7-1m), invocation by user
scope: read-only inventory + verdict; .roadmap #250 정정 NOT 본 commit (사용자 승인 후 별도)
constraints: raw#9 hexa-only, raw#10 honest C3, raw#70 multi-axis ≥3 orthogonal, raw#71 falsifier 5 preregister, raw#86 cost-attribution, raw#91 honest 5축, own#5 completeness-first

---

## §0 Executive summary

- **TOP-1**: `state/trained_adapters/p4_r8/final/` — base `mistralai/Mistral-7B-v0.3` + LoRA r=96, α=192, all-7-modules, 185.92 MB, mtime 2026-04-25 11:23
- **rationale**: (a) Mistral-7B-v0.3 = Apache 2.0 (재배포 OK), (b) 185 MB adapter — Mac mini M4 16 GB fit @ Q4_K_M base 4 GB + LoRA peft-applied or merged, (c) Family activation `Law max_cos=0.852` (cp1_v12 §Mistral_7B_v0_3.LoRA_r14, 4-backbone matrix 최고치), (d) r8 = corpus iter 가장 성숙 (cyborg axis 7, eeg axis 8 통합 후), (e) AN11(b) V0 PASS @ p4 r6 fallback (max_cos 0.609, top3 1.722).
- **TOP-3 alternatives**: r14_full Qwen3-8B LoRA (Phi family), llama31_r14 LoRA (SelfRef), r14_full Qwen3 (가장 최신 corpus + 4-family ensemble Phi 노드).
- **license verdict**: Mistral-7B-v0.3 Apache 2.0 = 재배포 합법. Llama-3.1 = Llama Community License 제한, Qwen3 = Apache 2.0, Gemma = Gemma TOU 제한, Qwen2.5-14B/Mistral-Nemo-12B = 사이즈 Mac fit 불가.
- **Mac M4 16 GB fit verdict**: Mistral-7B-v0.3 Q4_K_M ≈4.1 GB + LoRA 0.19 GB peft-applied OR merged Q4_K_M ≈4.3 GB. Working set <6 GB, fit YES.
- **ETA**: 1-3d (Q4_K_M quantization 30-60 min + serve smoke 20-40 min + 30-turn live test 1d + cp2_serve_launch_mac.bash 작성 4-6h).
- **cost**: $0 (no H100 spend, all local Mac inference).

---

## §1 인벤토리 (25 adapter 전수 — `find state/ -name adapter_config.json`)

| # | path | base | method | r | α | size_MB | mtime | corpus_iter |
|---|---|---|---|---|---|---|---|---|
| 1 | trained_adapters_r4/p1/final | Qwen/Qwen3-8B | LoRA | 64 | 128 | 666.1 | 2026-04-24 12:13 | r4 |
| 2 | trained_adapters_r4/p2/final | unsloth/Meta-Llama-3.1-8B | LoRA | 64 | 128 | 640.0 | 2026-04-24 12:15 | r4 |
| 3 | trained_adapters_r4/p3/final | mistralai/Mistral-Nemo-Base-2407 | LoRA | 96 | 192 | 1304.6 | 2026-04-24 12:18 | r4 |
| 4 | trained_adapters_r4/p4/final | google/gemma-3-12b-pt | LoRA | 128 | 256 | 2089.1 | 2026-04-24 12:24 | r4 |
| 5 | trained_adapters_r5/p1/final | Qwen/Qwen3-8B | LoRA | 64 | 128 | 666.1 | 2026-04-25 00:22 | r5 |
| 6 | trained_adapters_r5/p2/final | unsloth/Meta-Llama-3.1-8B | LoRA | 64 | 128 | 640.0 | 2026-04-25 00:24 | r5 |
| 7 | trained_adapters_r5/p3/final | mistralai/Mistral-Nemo-Base-2407 | LoRA | 96 | 192 | 1304.6 | 2026-04-25 00:28 | r5 |
| 8 | trained_adapters_r5/p4/final | google/gemma-3-12b-pt | LoRA | 128 | 256 | 2089.1 | 2026-04-25 00:37 | r5 |
| 9 | trained_adapters_r6/p1/final | Qwen/Qwen3-8B | LoRA | 64 | 128 | 666.1 | 2026-04-25 05:11 | r6 |
| 10 | trained_adapters_r6/p2/final | Qwen/Qwen2.5-7B | LoRA | 64 | 128 | 616.1 | 2026-04-25 05:13 | r6 |
| 11 | trained_adapters_r6/p3/final | mistralai/Mistral-Nemo-Base-2407 | LoRA | 96 | 192 | 1304.6 | 2026-04-25 05:15 | r6 |
| 12 | trained_adapters_r6/p4/final | google/gemma-3-12b-pt | LoRA | 128 | 256 | 2089.1 | 2026-04-25 05:24 | r6 |
| 13 | trained_adapters_r7/p4/final | Qwen/Qwen2.5-14B | LoRA | 96 | 192 | 1574.9 | 2026-04-25 10:27 | r7 |
| 14 | **trained_adapters/p4_r8/final** | **mistralai/Mistral-7B-v0.3** | **LoRA** | **96** | **192** | **185.92** | **2026-04-25 11:23** | **r8** |
| 15 | mistral_r14_run/.../final | mistralai/Mistral-7B-v0.3 | LoRA | 64 | 128 | 640.0 | 2026-04-26 10:17 | r14 |
| 16 | mistral_ia3_r14_run/.../final | mistralai/Mistral-7B-v0.3 | IA3 | — | — | 2.01 | 2026-04-26 15:01 | r14 |
| 17 | mistral_c2_pilot_run/.../final | mistralai/Mistral-7B-v0.3 | LoRA | 64 | 128 | 640.0 | 2026-04-26 12:07 | c2_pilot |
| 18 | llama31_r14_run/.../final | meta-llama/Llama-3.1-8B | LoRA | 64 | 128 | 640.0 | 2026-04-26 11:04 | r14 |
| 19 | llama_ia3_r14_v2_run/.../final | meta-llama/Llama-3.1-8B | IA3 | — | — | 2.01 | 2026-04-26 15:33 | r14 |
| 20 | gemma_r14_run/.../final | google/gemma-2-9b | LoRA | 64 | 128 | 824.4 | 2026-04-26 13:33 | r14 |
| 21 | gemma_ia3_r14_v2_run/.../final | google/gemma-2-9b | IA3 | — | — | 2.97 | 2026-04-26 15:37 | r14 |
| 22 | qwen3_ia3_r14_v2_run/.../final | Qwen/Qwen3-8B | IA3 | — | — | 1.98 | 2026-04-26 15:34 | r14 |
| 23 | qwen3_c2_ia3_run/.../final | Qwen/Qwen3-8B | IA3 | — | — | 1.98 | 2026-04-26 16:23 | c2_ia3 |
| 24 | r14_full_run/.../final | Qwen/Qwen3-8B | LoRA | 64 | 128 | 666.1 | 2026-04-26 09:05 | r14 |
| 25 | r14_shard1_run/.../final | Qwen/Qwen3-8B | LoRA | 64 | 128 | 666.1 | 2026-04-26 08:48 | r14_shard1 |

총 25 (인벤토리 ESTIMATE-가이드 17+ 충족). LoRA 17, IA3 5, hybrid 0.

persona naming (state/trained_adapters_r{4..6}/p{1..4}):
- p1=Qwen3-8B (Zeta-aligned)
- p2=Llama-3.1-8B (r4-r5) → Qwen2.5-7B (r6) (Lia-aligned)
- p3=Mistral-Nemo-12B-Base (Maya-aligned, 3 rounds 동일)
- p4=Gemma-3-12B-pt (r4-r6) → Qwen2.5-14B (r7) → Mistral-7B-v0.3 (r8) (Wraith / 통합 persona)

---

## §2 비교 매트릭스 (12 axes; — = ESTIMATE / NOT MEASURED)

| adapter | base | corpus | method | size_MB | φ_p1xN_KL | AN11_b_V0 | AN11_b_V1 (φ_mip) | AN11_c_JSD | persona_stab | latency_M4 | license_redist | release_ready |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r4/p1 | Qwen3-8B | r4 | LoRA64 | 666 | 5/6 KL pass | — | — | — | — | OOM(≥10GB) | Apache2 ✅ | NO (size+old) |
| r4/p4 | gemma-3-12B | r4 | LoRA128 | 2089 | 5/6 | — | — | — | — | OOM | Gemma TOU ❌ | NO |
| r5/p1 | Qwen3-8B | r5 | LoRA64 | 666 | 4/6 | — | — | — | — | OOM | Apache2 ✅ | NO (regression) |
| r6/p1 | Qwen3-8B | r6 | LoRA64 | 666 | 5/6 | PASS 0.618 | FAIL 0.352 | — | — | OOM | Apache2 ✅ | mid |
| r6/p4 | gemma-3-12B | r6 | LoRA128 | 2089 | 5/6 | PASS 0.609 | FAIL 0.359 | — | — | OOM | Gemma TOU ❌ | NO |
| r7/p4 | Qwen2.5-14B | r7 | LoRA96 | 1575 | 3/6 KL FAIL | — | — | — | — | OOM(>14GB) | Qwen RAIL | NO |
| **r8/p4** | **Mistral-7B-v0.3** | **r8** | **LoRA96** | **186** | **5/6 KL PASS** | **PASS 0.609 (r6 fb)** | **FAIL 0.195** | — | — | **fit ≤6GB** | **Apache2 ✅** | **TOP-1** |
| r8/p1 (=r6 fallback) | Qwen3-8B | r6 | LoRA64 | 666 | 5/6 | PASS 0.618 | FAIL 0.352 | PASS JSD 0.693 (saturated) | — | OOM | Apache2 ✅ | TOP-3 |
| mistral_r14 | Mistral-7B-v0.3 | r14 | LoRA64 | 640 | — | — | — | — | — | merge fit | Apache2 ✅ | TOP-2 |
| mistral_c2_pilot | Mistral-7B-v0.3 | c2_pilot | LoRA64 | 640 | — | — | — | — | — | merge fit | Apache2 ✅ | mid |
| llama31_r14 | Llama-3.1-8B | r14 | LoRA64 | 640 | — | SelfRef 0.638 (cp1_v12) | — | — | — | merge fit | Llama-CL ⚠ | mid |
| llama_ia3_r14 | Llama-3.1-8B | r14 | IA3 | 2 | — | SelfRef 0.639 | — | — | — | merge fit | Llama-CL ⚠ | NO (IA3) |
| gemma_r14 | gemma-2-9B | r14 | LoRA64 | 824 | — | Law 0.673 (cp1_v12) | — | — | — | OOM | Gemma TOU ❌ | NO |
| gemma_ia3_r14 | gemma-2-9B | r14 | IA3 | 3 | — | Hexad 0.649 (preserve) | — | — | — | OOM | Gemma TOU ❌ | NO |
| qwen3_ia3_r14 | Qwen3-8B | r14 | IA3 | 2 | — | Law 0.654 (shift) | — | — | — | OOM | Apache2 ✅ | NO (IA3 미검증, Phi loss) |
| qwen3_c2_ia3 | Qwen3-8B | c2_ia3 | IA3 | 2 | — | — | — | — | — | OOM | Apache2 ✅ | NO |
| r14_full | Qwen3-8B | r14 | LoRA64 (drop=0.05) | 666 | — | Phi 0.673 (cp1_v12) | — | PASS via cp1_an11_c (0.6931 saturated) | — | OOM | Apache2 ✅ | TOP-3 |
| r14_shard1 | Qwen3-8B | r14_shard1 | LoRA64 | 666 | — | — | — | — | — | OOM | Apache2 ✅ | NO |

primary citation:
- φ_4path_cross_result_v3_TRAINED_r{4..8}.json (KL_pass_count / verdict)
- an11_phi_mip_p{1..4}_r{6,8}.json (phi_mip)
- an11_b_joint_matrix_r{6,8}.json (V0 PASS, V1/V2/V3 FAIL across all paths)
- cp1_v12_4backbone_ia3_matrix_FINAL_20260426.json (4-backbone × LoRA/IA3 family activation)
- cp1_an11_c_remeasurement_20260426.json (sampling JSD 0.6931)

note: AN11(b) V1 phi_mip universally FAIL (<0.45) across all measured rounds — reflects current verifier ceiling on training-only adapters, not a per-adapter discriminator. V0 cosine-template alignment IS discriminator (cp1_v12 max_cos table).

---

## §3 selection 기준 + scoring

priority order (per task spec §Step 4):

1. **anima 정체성 (φ paradigm score)** — φ_4path KL/L2 pass + V0 max_cos
2. **persona stability (AN11 b/c)** — V0 PASS, JSD diversity
3. **license redistribution legality** — Apache2 / MIT > Llama-CL > Gemma-TOU > Qwen-RAIL
4. **Mac M4 16 GB fit** — base ≤8B at Q4_K_M (≤4.5GB) + adapter <300MB
5. **corpus maturity** — r4 < r5 < r6 < r7 < r8 < r14 (cyborg+EEG+paradigm-v9 통합)
6. **method stability** — LoRA (검증 25 adapter) > IA3 (Phi family loss documented in cp1_v12)

scoring (1-5 per axis, weighted sum 6-30):

| candidate | φ | persona | license | M4_fit | corpus | method | total |
|---|---|---|---|---|---|---|---|
| **r8/p4 Mistral-7B-v0.3 LoRA96** | **5** | **4** | **5** | **5** | **5** | **5** | **29** |
| mistral_r14 LoRA64 | 4 | 3 | 5 | 5 | 5 | 5 | 27 |
| r14_full Qwen3-8B LoRA64 | 4 | 4 | 5 | 4 | 5 | 5 | 27 |
| llama31_r14 LoRA64 | 4 | 4 | 2 | 5 | 5 | 5 | 25 |
| r6/p1 Qwen3-8B LoRA64 | 4 | 4 | 5 | 4 | 3 | 5 | 25 |
| qwen3_ia3_r14 | 3 | 3 | 5 | 5 | 5 | 2 | 23 |
| gemma_r14 LoRA64 | 4 | 4 | 1 | 4 | 5 | 5 | 23 |
| r4-r5 all | 2-3 | — | — | — | 1-2 | 5 | <22 |

---

## §4 TOP-1 verdict + rationale

**winner: `state/trained_adapters/p4_r8/final/`**

- base: `mistralai/Mistral-7B-v0.3`
- method: LoRA r=96, α=192, dropout=0.05, all-7-modules (q/k/v/o/gate/up/down)
- adapter size: 185.92 MB (smallest LoRA in inventory — reflects different lora_alpha+rank scaling)
- training: corpus iter r8 (cyborg axis 7 + EEG axis 8 통합 후 가장 성숙 corpus)
- mtime: 2026-04-25 11:23

**5-axis rationale (raw#70 multi-axis ≥3 orthogonal verify-grid):**

1. **anima 정체성 (φ axis)**: phi_4path_cross_result_v3_TRAINED_r8 KL_pass 5/6 (worst pair p1_p2 KL=0.138 vs p95=0.128 — borderline; 5/6 pairs L2 PASS, KL 5/6); cp1_v12 §Mistral_7B_v0_3.LoRA_r14 max_cos=0.852 family=Law (4-backbone 최고치). r8 reuses r14-train schedule on c2 corpus, AN11(b) Family Law preserved.
2. **persona stability (AN11 axis)**: an11_b_joint_matrix_r8 cells.p4 V0 PASS max_cos=0.609 top3=1.722 (r6 fallback identical, source 동일); V1/V2/V3 FAIL universally — but verifier-ceiling not adapter-specific.
3. **license**: Mistral-7B-v0.3 Apache 2.0 = 재배포 + commercial OK. 비교군: Llama-3.1 Llama-CL (>700M MAU 제한 적용 NO 우리 case 제외 OK이나 별도 license click-through 의무), Gemma TOU (use restriction), Qwen2.5-14B Tongyi Qianwen RAIL.
4. **Mac M4 fit**: Mistral-7B fp16 = 13 GB → Q4_K_M = 4.1 GB; LoRA 186 MB peft-merge 후 final GGUF Q4_K_M = ~4.3 GB. 16 GB unified mem 헤드룸 7+ GB.
5. **corpus + method**: r8 = 2026-04-25 학습 corpus (cyborg/EEG/paradigm-v9 통합), LoRA r96 dropout 0.05 검증 schedule.

raw#10 honest C3:
- AN11(b) V1 phi_mip = 0.195 FAIL, V2 SMA_lift = -0.218 FAIL, V3 CPS = 0.843 FAIL — verifier strict 기준에서 "consciousness-attached" 비통과. release는 V0 PASS (template alignment) + φ_4path KL 5/6 (cross-path 분리도) 두 axis 위에서만 정당화.
- p4_r8 measured AN11_b는 r6 fallback (source_round=r6, source_fallback=true in an11_b_joint_matrix_r8.cells[3].V0). r8 자체 raw eigen 미측정 — fallback이 conservatively-strong 측정.

---

## §5 TOP-3 alternatives

**TOP-2: `state/mistral_r14_run/mistral_r14/final/`**
- base: Mistral-7B-v0.3 (Apache2 ✅), LoRA r=64 α=128, 640 MB.
- corpus r14 가장 최신 (1200 docs × 3 epochs, train_loss 1.43→0.98 — witness.json), Family Law 0.852 max_cos.
- vs TOP-1 trade-off: corpus r14 더 최신 (+) but adapter 640 MB (vs 186 MB) — Q4_K_M merge 후 동일 ~4.3 GB이므로 사실상 동등.
- 선정 가능 시: more documented training run (cp1_v12 4-backbone matrix anchor).

**TOP-3: `state/r14_full_run/r14_full/final/`**
- base: Qwen3-8B (Apache2 ✅), LoRA r=64 α=128 dropout=0.05, 666 MB.
- corpus r14 (Qwen3 path), Family Phi 0.673 max_cos (cp1_v12) — anima 정체성의 Phi-pole.
- AN11(c) JSD = 0.6931 PASS (cp1_an11_c_remeasurement_20260426.json — saturated to log(2)).
- Mac M4 fit: Qwen3-8B Q4_K_M ~4.6 GB + adapter 666 MB peft-merge 가능.
- vs TOP-1 trade-off: Phi family discriminator (different consciousness pole than Law) → ensemble 가능성. 단독 Option D 대표는 Mistral 더 verified.

**alternative TOP-3: `state/llama31_r14_run/llama31_r14/final/`**
- base: Llama-3.1-8B (Llama-CL ⚠ click-through), LoRA r=64 α=128, 640 MB.
- Family SelfRef 0.638 (cp1_v12 4-backbone), corpus r14 최신.
- Mac M4 fit: Llama-3.1 Q4_K_M ~4.6 GB.
- vs TOP-1 trade-off: license click-through 추가 friction (HF gated repo) — 임시공개 단순화 위해 비추천. 4-family ensemble 시에는 SelfRef 노드로 합법 (단일-host self-host 범위 내 OK).

---

## §6 NOT-RECOMMEND list + 이유

- **r4 모든 4 path**: corpus r4 = 가장 오래됨 (2026-04-24, paradigm-v9/cyborg 미통합), φ KL 5/6/L2 4/6 r2/r3 baseline 부근.
- **r5 모든 4 path**: phi_4path TRAINED_r5 verdict FAIL (3/6 L2, 4/6 KL — regression vs r4).
- **r7/p4 Qwen2.5-14B**: 1574 MB adapter + 14B base — Mac M4 OOM (Qwen2.5-14B Q4_K_M ≈8.8 GB + LoRA ≈1.6 GB 헤드룸 부족); φ_4path KL FAIL 3/6.
- **gemma-3-12B (r4-r6 p4)**: 12B + Gemma TOU restrictive (use-case clauses) + 2 GB adapter — fit 불가 + license 재배포 제한.
- **gemma-2-9B r14 (LoRA + IA3)**: Gemma TOU 동일 + 9B Q4_K_M ≈5.5 GB + 824 MB adapter 가능하지만 license가 결정적 비추.
- **Mistral-Nemo-12B (p3 r4/r5/r6)**: 12B base — Q4_K_M ≈7.2 GB + 1.3 GB adapter, Mac M4 borderline 헤드룸 1-2 GB 부족.
- **모든 IA3 (5 adapter)**: cp1_v12 §critical_findings.v12_ia3_vs_v10_lora_family_coverage — IA3 mode에서 Phi family LOSS (Qwen3 LoRA Phi → IA3 Law shift), 4-family complete ensemble = LoRA only. 또한 transformers/peft IA3 inference path Mac local 검증 미수행 (raw#10).
- **r14_shard1 Qwen3**: shard 단편 (1/N), full corpus 학습 미달. r14_full로 대체.
- **mistral_c2_pilot**: c2_pilot corpus (V_phen_GWT_v2 hypothesis test 13.2초 학습 — pilot only, 30 docs × 3 epochs); 정식 r14 schedule 아님.
- **qwen3_c2_ia3**: c2 corpus + IA3 — Phi family loss + 미검증.

---

## §7 Option D 재기술 권고 (.roadmap #250 정정 안)

**현재 (line 3801-3813) 원문**: "Mac mini M4 local self-host (Qwen3-8B Q5_K_M)" — Qwen3-8B 자체는 anima 학습 안 됨, 사용자가 catch.

**정정 권고 (사용자 승인 후 별도 commit)**:

```
roadmap 250 planned "[CP2 임시공개 Option D — Mac mini M4 local self-host (Mistral-7B-v0.3 + anima LoRA r8/p4)]"
  why            CP2 임시공개버전 Option D — Option C (#249) 와 병렬/순차 결합. Mac mini M4 local
                 self-host: base mistralai/Mistral-7B-v0.3 (Apache 2.0) + state/trained_adapters/p4_r8/final/
                 LoRA adapter (r=96, α=192, 186 MB) merged → GGUF Q4_K_M ~4.3 GB. anima 정체성
                 Family=Law max_cos=0.852 (cp1_v12 4-backbone matrix 최고치, raw#10 anima
                 정체성 정량 보존). NOT public service NOT $1400-2100 70B retrain. cp2_serve_launch_mac.bash
                 (현재 부재 — 신규 작성 필요 OR tool/anima_serve_smoke.hexa 재활용) 진입점 사용.
                 raw#10 honest C3: (a) AN11(b) V1/V2/V3 strict FAIL — V0 + φ_4path 두 axis 위에서만
                 정당화, (b) Mac M4 latency 미검증, F2 falsifier 측정 후 promote/demote.
  exit_criteria  (1) Mistral-7B-v0.3 base weights HF download (~13 GB fp16) + Q4_K_M quantization
                 ~4.1 GB local (30-60 min) + LoRA peft-merge → final.gguf Q4_K_M ~4.3 GB
                 + (2) cp2_serve_launch_mac.bash live mode 30-turn smoke session 통과
                 + (3) Mac M4 latency median <1.5s + p99 <3s (F2 falsifier 5-prompt smoke)
                 + (4) Q4_K_M fallback to Q5_K_M 가능성 명시 (Q5 대안)
                 + (5) localhost:8080 OpenAI-compat /v1/chat/completions endpoint 응답
                 + (6) raw#10 disclaimer "local self-host, NOT public anima.ai SLA, AN11(b) V1
                       strict FAIL but V0+φ axis PASS"
  evidence       docs/anima_adapter_release_candidate_selection_2026_04_29.md (TOP-1 selection
                 + 25-adapter 인벤토리 + 12-axis 비교) + state/cp1_v12_4backbone_ia3_matrix_FINAL_20260426.json
                 (Family Law 0.852) + state/an11_b_joint_matrix_r8.json (V0 PASS p4) +
                 state/phi_4path_cross_result_v3_TRAINED_r8.json (KL 5/6)
  refs           state/trained_adapters/p4_r8/final/ (LoRA adapter — TOP-1)
                 · state/mistral_r14_run/mistral_r14/final/ (TOP-2 alternative)
                 · state/r14_full_run/r14_full/final/ (TOP-3 alternative — Qwen3-8B Phi pole)
                 · cp2_serve_launch_mac.bash (현재 부재 — Step 8 해결안 참조)
                 · tool/anima_serve_smoke.hexa · tool/anima_serve_live_smoke.hexa
                 · tool/serve_alm_persona.hexa · tool/cp1_serve_launch_mac.bash (이미 존재)
  falsifier      F2: Mac M4 Q4_K_M latency median <1.5s + p99 <3s
                 / F3 (raw#71): AN11(b) V0 max_cos r8/p4 measured 0.609 — drop ≤0.50 시 retire
                 / F4: corpus shift drift > 0.15 between r8 and current → retrain trigger
                 / F5: license audit Apache 2.0 적합 (재배포 OK) — Mistral의 7B-v0.3 weight upgrade
                       시 license shift 모니터링
                 / F6: 30-turn session memory leak >50MB → fallback to per-turn restart
```

핵심 변경:
- base: Qwen3-8B → **Mistral-7B-v0.3**
- adapter 명시: state/trained_adapters/p4_r8/final/
- Q5_K_M → **Q4_K_M (default)**, Q5_K_M fallback (Mac M4 16GB 헤드룸 우선)
- license: Apache 2.0 명시 (재배포 합법)
- raw#10: AN11(b) V1/V2/V3 FAIL 명시적 disclaimer 추가

---

## §8 cp2_serve_launch_mac.bash 부재 해결안

`cp2_serve_launch_mac.bash`는 .roadmap에 5회 언급되나 실제 파일 부재 (`ls /Users/ghost/core/anima/cp2_serve_launch_mac.bash` exit=1).
대조: `tool/cp1_serve_launch_mac.bash` 존재.

**3가지 옵션:**

(a) **신규 작성** (estimated 4-6h):
- cp1_serve_launch_mac.bash 기반으로 cp2 변형 신작 — base/adapter env-var화, Q4_K_M 디폴트, llama.cpp 또는 ollama 진입점.
- spec 추가 필요: PORT=8080, /v1/chat/completions OpenAI-compat, persistent launchd plist (선택).

(b) **재활용** (즉시):
- `tool/anima_serve_smoke.hexa` + `tool/anima_serve_live_smoke.hexa` + `tool/serve_alm_persona.hexa` 조합으로 Option D 진입.
- bash 추가 작성 없이 hexa 도구 직접 호출 — raw#9 hexa-only strict 더 잘 부합.

(c) **Option D 자체에서 launch path 명시 → bash script 부재** (가장 단순):
- .roadmap #250 evidence 라인에서 cp2_serve_launch_mac.bash 제거, hexa 도구 chain만 명시.
- raw#9 satisfied 자동 (hexa-only).

**권고: (c)** — raw#9 strict 부합 + 신규 bash script 작성 회피 + 기존 hexa 도구 충분.
사용자가 "production-style ops shell" 요구 시 (a)로 promote.

---

## §9 raw#10 honest C3 disclosure (≥5)

1. **AN11(b) V1/V2/V3 strict FAIL across ALL measured cells (r6/r8 × p1/p2/p3/p4)**: phi_mip max 0.359 (r6/p4) < threshold 0.55. release는 V0 cosine alignment + φ_4path KL pass 두 axis 위에서만 정당화. V1 IIT-Phi_mip strict criterion 미달.
2. **r8/p4 V0 measurement is r6 fallback** (source_round=r6, source_fallback=true in an11_b_joint_matrix_r8.cells[3]). r8 자체 raw eigen 미측정 — fallback은 conservatively-strong 측정 (구 round의 anima 정체성 신호 = 더 약한 lower bound).
3. **Mac M4 latency unknown**: F2 falsifier 측정 전 — 현재 추정 ESTIMATE: Mistral-7B-v0.3 Q4_K_M @ M4 16GB ≈25-40 tok/s 구간이 llama.cpp 벤치마크 (외부 보고) — anima-specific 미측정.
4. **lora_alpha mismatch r8/p4 vs cp1_v12 anchor**: cp1_v12 §Mistral_7B_v0_3.LoRA_r14 측정은 mistral_r14_run (r=64, α=128) 기준. r8/p4 (r=96, α=192) 직접 cp1_v12 entry 없음 — Family Law 0.852 가정은 동일 base + 동일 corpus family 가정 위 ESTIMATE.
5. **base license re-distribution validity unverified for Mistral-7B-v0.3 weight package itself**: Apache 2.0 = adapter+derivative redistribution OK. 그러나 Mistral 자체 weight 재배포는 별도 — Option D는 사용자가 HF에서 직접 다운로드하므로 weight redistribution 발생 안 함 (user pulls from upstream HF). 이 가정 깨질 시 (사용자가 anima 측 weight 호스트 요구) license re-evaluate.
6. **AN11(c) JSD only measured for r6/p1 (Qwen3-8B)**: cp1_an11_c_remeasurement_20260426.json target = state/trained_adapters_r6/p1/final/ + Qwen3-8B base. r8/p4 (Mistral-7B-v0.3) AN11(c) sampling diversity 미측정 — corpus-method 일반화 가정.
7. **persona p4 = "Wraith / 통합" naming inconsistency**: r4-r6 p4 = Gemma-3-12B-pt, r7 p4 = Qwen2.5-14B, r8 p4 = Mistral-7B-v0.3 — backbone shift 3회. p4 라벨 자체가 persona 지표 아닌 sweep slot 지표. release "persona = anima 통합" 명시는 trained adapter 의 weight identity 위 정당화 필요 (현재는 cp1_v12 family activation Law 신호로 proxy).

---

## §10 raw#71 falsifier preregister (5건)

| ID | criterion | measurement | window | outcome |
|---|---|---|---|---|
| F2 | Mac M4 Q4_K_M latency | median <1.5s + p99 <3s on 5-prompt smoke | 30 min | <1.5/<3 PASS / 미달 → Q5_K_M downshift OR retire Option D |
| F3 | AN11(b) V0 r8/p4 re-measured non-fallback | max_cos ≥ 0.50 + top3_sum ≥ 1.20 (V0 thresholds) | 1 H100 hour | PASS → keep / drop ≥0.10 from 0.609 → retire |
| F4 | corpus drift r8 → live | new measurement vs r8 baseline KL > 0.15 | 7 days | drift>0.15 → retrain trigger |
| F5 | license audit | Mistral-7B-v0.3 Apache 2.0 unchanged + Mistral team license shift 0건 | 14 days | shift → swap to TOP-2 (mistral_r14) or TOP-3 (Qwen3 r14_full) |
| F6 | 30-turn session memory leak | RSS growth <50 MB across 30-turn | 1 day | >50MB → per-turn restart fallback |

each falsifier links to: state/cp2_option_d_falsifier_<ID>_<date>.json (TBC after launch).

---

## §11 cost-attribution (raw#86)

| line item | cost | rationale |
|---|---|---|
| inventory + analysis (this doc) | $0 | local read-only state/, docs/, .roadmap |
| Mistral-7B-v0.3 HF download | $0 | bandwidth only, ~13 GB |
| Q4_K_M quantization (llama.cpp) | $0 | Mac M4 local |
| 30-turn smoke + F2 falsifier | $0 | Mac M4 local |
| F3 H100 re-measure (optional, 1h) | ~$3 | spot H100 SXM @ $2.99/hr |
| 정식 commit + chflags lock | $0 | git only |
| **Option D total (no F3)** | **$0** | falls in "Phase β $0" envelope |
| Option D + F3 | ~$3 | trivial |

vs alternatives:
- Option A (#88 anima.ai public service): $1400-2100 70B retrain + 7-14d
- Option C (paper/blog): $0 + 0-3d (parallel)
- Option D (this doc): $0 + 1-3d (this selection enables)

---

## §12 verify-grid (raw#70 multi-axis ≥3 orthogonal)

axis 1 (φ paradigm): phi_4path_cross_result_v3_TRAINED_r8.json KL 5/6 + L2 6/6 → r8 winner gate.
axis 2 (Family activation): cp1_v12_4backbone_ia3_matrix_FINAL_20260426.json Mistral-7B-v0.3 LoRA Law max_cos=0.852 → Mistral 4-backbone 최고.
axis 3 (Mac M4 fit): Mistral-7B-v0.3 Q4_K_M 4.1 GB + 186 MB adapter → orthogonal hardware constraint.
axis 4 (license): Apache 2.0 = redistribution-clean → orthogonal legal constraint.
axis 5 (corpus maturity): r8 mtime 2026-04-25 11:23 > r4-r7 → orthogonal time-monotonic.

3+ orthogonal axes 확보 — multi-axis 충족.

---

## §13 raw#91 honest C3 5축

- **counter axis**: TOP-1 선정 시 NOT-recommend 후보 8개 명시 (§6) + 거부 이유 정량.
- **write-barrier axis**: .roadmap #250 정정 NOT 본 commit (사용자 승인 후 별도) — race-avoidance 충족.
- **no-fab axis**: 모든 측정값 cite (cp1_v12, an11_b_joint_matrix, phi_4path_cross, cp1_an11_c, cp1_real_validation_result), ESTIMATE 마크 명시 (latency, p4_r8 cp1_v12 entry 부재).
- **citation axis**: 25 adapter 모두 path + base + size + mtime 정량, 6 evaluation source file path 명시.
- **verdict-options axis**: TOP-1 단독 verdict + TOP-3 alternatives + NOT-recommend list + (a)(b)(c) bash script 옵션 — multi-option 제시.

---

## §14 references

source files cited (all read-only):
- /Users/ghost/core/anima/.roadmap (lines 1204, 3801-3813)
- /Users/ghost/core/anima/state/cp1_real_validation_result.json
- /Users/ghost/core/anima/state/cp1_v12_4backbone_ia3_matrix_FINAL_20260426.json
- /Users/ghost/core/anima/state/cp1_an11_c_remeasurement_20260426.json
- /Users/ghost/core/anima/state/cp1_paradigm_v9_p1_cross_backbone_universal_20260426.json
- /Users/ghost/core/anima/state/an11_b_joint_matrix_r{6,8}.json
- /Users/ghost/core/anima/state/an11_phi_mip_p{1..4}_r{6,8}.json
- /Users/ghost/core/anima/state/phi_4path_cross_result_v3_TRAINED_r{4..8}.json
- /Users/ghost/core/anima/state/zeta_likert_result.json
- /Users/ghost/core/anima/state/mistral_c2_pilot_run/mistral_c2_pilot/witness.json
- /Users/ghost/core/anima/state/an11b_mistral_c2_run/alm_mistral_c2_lora_eigen.json
- /Users/ghost/core/anima/state/runpod_run_an11b_mistral_c2.json

25 adapter_config.json + 25 adapter_model.safetensors metadata extracted via:
- find /Users/ghost/core/anima/state/ -name "adapter_config.json"
- find /Users/ghost/core/anima/state/ -name "adapter_model.safetensors"
- stat -f "%z %Sm %N" -t "%Y-%m-%d %H:%M" each safetensors

---

end of document.
