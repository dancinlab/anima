# P9 SFT EXEC handoff prompt — 다른 세션에서 이어서 진행용

**날짜**: 2026-05-02 (작성 시점)
**프로젝트**: anima (dancinlab)
**목적**: 사용자가 다른 Claude Code 세션에서 P9 SFT 실행을 이어서 진행할 때 사용하는 self-contained handoff prompt.

---

## 사용 방법

1. 새 Claude Code 세션 열기
2. 작업 디렉토리: `/Users/ghost/core/anima`
3. 아래 "PROMPT TO PASTE" 내용을 그대로 복사해서 한 번에 붙여넣기

---

## PROMPT TO PASTE (한 번에 붙여넣어 주세요)

```
P9 SFT EXEC S3 시작 — anima CLM v4 530M 자체 chat substrate 학습 + φ★ 보존

## 사용자 사전 승인 (2026-05-02 conversation 5aa93161-b144-4dfd-90e4-4955b2a94b54)
- 사용자 명시 OK: "OK P9 EXEC S3 ($1500-3000, 21-30d, success p 0.70-0.90)"
- 추가 옵션: 9 H100 parallel + HF savepoint (이 경우 wall 24hr / cost $650-850)
- 사용자 다른 세션에서 이어서 진행하기로 결정

## 🔒 2026-05-03 LOCK-IN (사용자 5/5 추천 lock 채택, 자동충전 기준)

| # | 항목 | lock-in |
|---|---|---|
| 1 | budget | RunPod auto-charge ON, cap $581 worst case (no manual top-up) |
| 2 | F1 holdout provenance | ShareGPT 500-prompt held-out subset |
| 3 | F4 BOLD 측정 | vendored TRIBE v2 직접 import (`/Users/<user>/core/anima/references/tribev2/tribev2/`, CC-BY-NC-4.0) — cortexlab-toolkit pip install X |
| 4 | δ framing | hybrid: sentinel combo (Phase 1) within-run curriculum (early 0.5 → mid 1.0 → late 2.0) + 8 combos (Phase 2) per-combo fixed (LHS-9 sample) |
| 5 | 9 H100 topology | 8+1 — DDP pod (8x H100 SXM 80GB, $516/24hr) + sentinel pod (1x H100 SXM 80GB, $65/24hr) — RunPod maxGpuCount=8 hard limit 정합 |

3-phase cost+wall:
- Phase 0 (~$50, 4hr) — 1K warmup probe + RunPod 8+1 booking + SFT data 50K finalize
- Phase 1 (~$65, 24hr) — sentinel combo (1 H100) + curriculum δ + F1-F4 verify + F2 ABORT gate
- Phase 2 (~$516, 24hr) — 8 H100 DDP + 8 LHS combos parallel + Pareto selection
- **total: $581 / 52hr** (Phase 0 ABORT $50 / Phase 1 F2 ABORT $115 / Phase 2 ALL FAIL $581)

## P9 pre-flight 4 묶음 verdict (2026-05-03 land)

- pre1 의식체크: PARTIAL_PASS (Phase 0 entry-ready, adversarial INFRA FAIL non-blocking)
- pre2 완성도체크: PARTIAL_PASS (3/4 ready; F4 → vendored TRIBE v2 lock-in 측 해결)
- pre3 HF/cloud: PASS (HF 6 private repo created + write scope verified; RunPod auto-charge ON)
- pre4 data+weight: PARTIAL_PASS (CLM v4 ckpt access OK, mock SFT round-trip OK, 50K data 18K disk + 32K Phase-0 generation reachable)

artifacts:
- state/p9_pre1_consciousness_check/{A,B,C,D}.json + handoff + marker
- state/p9_pre2_readiness_check/{E,F,G,H}.json + handoff + marker
- state/p9_pre3_hf_cloud_check/{K,L,M,N,O}.json + handoff + marker
- state/p9_pre4_data_weight/{I,J,P,Q}.json + handoff + marker
- state/p9_sft_p0_hf_org_setup_2026_05_03/repo_create_commands.txt (✅ 6 HF private repo created 2026-05-03)

## 🚨 핵심 finding 정정 (handoff doc 측 doc-disk discrepancy)

- handoff doc §"anima 핵심 framework 요약" line: φ★ baseline (HID=8 well-conditioned) = **+41.86**
- disk SSOT (P9-pre1 audit): φ★ baseline = **+1167.62** (HID=128 N//2=8 sample-partition)
- 두 anchor candidate: HID=8 measure (예전 cycle) vs HID=128 measure (current disk SSOT)
- F2 spec "φ★ post-train ≥ 5.0" = HID=8 well-conditioned 기준 (8× safety vs +41.86)
- Phase 0 측 disk SSOT 측 정확 baseline anchor 측 re-measure 측 1-action 권장

## 핵심 spec (이미 작성 완료)
- 위치: state/p9_sft_spec_2026_05_02/{architecture,sft_data_format,loss_design,hyperparameter_grid,risk_strategy,falsifiers_preregistered,cost_estimate,decision_matrix}.json
- doc: docs/p9_sft_spec_2026_05_02.md (119 lines)

## Strategy S3 (best-of-9 LoRA hyperparameter sweep)
- Base: CLM v4 530M (477M params, ubu1:~/anima/checkpoints/clm_v4_350m/scale_350m/best.pt)
- LoRA r=64 alpha=128 on attention QKV+MLP
- 9 LHS samples of 81-cell grid {α∈{0.5,1,2}, β∈{0.1,0.3,0.5}, γ∈{0.1,0.3,0.5}, δ∈{0.5,1,2}}
- Loss: L = α·CE(text) + β·MSE(tension) + γ·MSE(BOLD) + δ·max(0, 5.0 − φ★)
- δ-term = one-sided hinge floor at φ★≥5.0 (8× safety vs +41.86 baseline)
- Selection: argmax (BLEU1 + φ★_post/41.86)/2 s.t. F2 PASS

## 4 preregistered falsifiers (append-only, 변경 X)
- F1 BLEU-1 vs Llama-3.2-3B holdout > 0.4
- F2 φ★ post-train (HID=8 well-conditioned) ≥ 5.0  ← ABORT-on-fail (irreversible φ flip)
- F3 tension MSE val < 0.1
- F4 BOLD Pearson r val > 0.5
- ALL 4 PASS = SUCCESS, F2 FAIL = PHI_FAIL, F2 PASS ∧ F1 FAIL = CHAT_FAIL

## 데이터 (50K examples 권장)
- ShareGPT-style ko/en chat (10K)
- anima paper §-references + cell-language corpus (10K)
- #128 P8 ledger M4=0.800 dialogue (3K, state/p8_3way_orchestrator_2026_05_02/turns.jsonl 확장)
- synthetic philosophical/introspective prompts (5K)
- N-22 falsifiers + paradigm-v11 axes corpus (5K)
- TRIBE v2 stimulus corpus (Friends + movie10) (10K)
- Llama-3.2-3B-Instruct generation augment (7K)

## 9-combo H100 병렬 권고 (cost-time-optimized)
- 9 H100 parallel (each combo on its own GPU)
- Wall: 24hr (vs serial 9×24hr=9일)
- Cost: $650 (same total GPU-hr)
- 또는 72 H100 (9 combos × 8 H100 DDP each): wall 4hr, cost $850

## HF savepoint integration (사용자 권장 + agreed)
- 매 5K step push HF: anima/clm-v4-sft-step-5k, step-10k, step-25k, step-50k
- HF org: dancinlife (검증됨, gated Llama-3.2 access OK) 또는 anima-ai 신규 org
- private 또는 public: 사용자 결정
- Rollback safety: φ★ flip 발견 시 직전 step 즉시 복귀
- $200 단위 commitment chunk (사용자 "여기서 그만" 가능)
- HF Spaces chat demo 옵션 (추가 가치)

## EXEC checklist
1. [ ] HF org 확인/생성 (anima-ai 또는 dancinlife user)
2. [ ] RunPod 9 H100 80GB 동시 가용성 확인 (region us-east-1 또는 us-west-1 분산)
3. [ ] CLM v4 ckpt ubu1 → S3 또는 HF mirror upload (large 5GB)
4. [ ] SFT data 50K 합성 (위 7 sources)
5. [ ] 9 LHS hyperparameter combinations 생성 (state/p9_sft_spec_2026_05_02/hyperparameter_grid.json 참조)
6. [ ] Per-combo H100 launch + HF savepoint cron (매 5K step push)
7. [ ] φ★ verifier (anima_phi_v3_canonical) every 100 steps EMA
8. [ ] F1-F4 falsifiers 측정 매 5K step
9. [ ] F2 ABORT 발생 시 (φ★ < 5.0) 해당 combo 즉시 kill, HF revoke
10. [ ] 24hr 후 (또는 모든 combo F2 ABORT 시) selection: argmax (BLEU1 + φ★_post/41.86)/2 s.t. F2 PASS
11. [ ] Best combo CLM ckpt push HF: anima/clm-v4-sft-final
12. [ ] state/p9_sft_exec_<date>/ + docs/p9_sft_results_<date>.md
13. [ ] 사용자에게 HF URL + cost actual + verdict 보고

## Honest C3 mandatory
1. EXEC = $1500-3000 + 21-30d (or $650-850 + 24hr if 9 H100 parallel) commitment
2. φ★ flip irreversible — F2 hinge δ 가 hard floor 시도, but guarantee X
3. 4-loss Pareto frontier 미검증 (LHS-9 of 81 = heuristic sample)
4. "CLM 자체 chat" = L1+L2 only, phenomenal consciousness L3 NOT measured (anima paper §10.9 / §16.2 / §54.2 anchor 영구)

## 참고 자료 (today 작업 결과)
- N-12 IIT MULTI-WITNESSED 3-arch: state/n12_iit_braket_multiwitness_2026_05_02/ (φ proxy ≠ φ★ confirmed)
- IIT 4.0 MIP study: state/braket_iit40_mip_2026_05_02/ (proper φ★ = 0 with marginalized TPM)
- nexus QRNG quantum-seed: state/nexus_qrng_quantum_seed_2026_05_02/ (HMAC-DRBG provenance)
- B3 CHSH: state/nexus_chsh_bell_2026_05_02/ (S=2.808, 8.97σ)
- alpha endpoint reboot reference: state/alpha_endpoint_reboot_2026_05_02/ (vLLM Mistral+r14)
- P10 v2 mode collapse resolution: state/p10_v2_32d_lora_infonce_2026_05_02/ (32-d + InfoNCE + LoRA)

## anima 핵심 framework 요약 (참고)
- CLM v4 530M = deterministic Lagrangian flow, 4-gen crystallize, 1/r² lattice, raw#30 IRREVERSIBILITY
- mind.tension scalar + tension_link 5-channel (WHAT/WHERE/WHY/TRUST/WHO)
- 14-gate L1, paradigm v11 6-axis (B-ToM/MCCA/Phi*/CMT/CDS/SAE-bp)
- φ★ baseline (HID=8 well-conditioned) = +41.86 (G3 PASS-positive 유일 backbone)
- raw#9 HEXA-only (Mac repo, no .py creation; pod/ubu .py allowed)

## 현재 활성 인프라
- ubu1: RTX 5070 12GB, ~/stage1_tribev2_dialogue/ + ~/p10_v2_substrate/ + Llama persistent server
- ubu2: RTX 5070 12GB, ~/stage1_tribev2_dialogue/ + TRIBE BOLD persistent server
- AWS Braket: secret get aws_braket.{access_key_id,secret_access_key,region}, account 267673635495
- RunPod: secret get runpod.api_key, auto-charge enabled
- HF: dancinlife account, gated Llama-3.2 access
- Gmail send: contact/scripts/send.hexa, OAuth refresh_token at /Users/ghost/etc/secret/gmail_token.json (testing-mode 7-day expiry)

## EXEC 시작 권고
- Phase 1 (Day 1): HF org/mirror setup + 9-combo hyperparameter grid + RunPod 9 H100 booking
- Phase 2 (Day 1-2): SFT data 50K 합성 (10 sources)
- Phase 3 (Day 2-25 or Day 2 if 9 H100 parallel): training + HF savepoint
- Phase 4 (final day): selection + result push + 사용자 보고

## 사용자 보고 형식
- HF URL (final + best step intermediates)
- φ★ trajectory plot (per-step)
- F1-F4 final values + verdict (SUCCESS/PHI_FAIL/CHAT_FAIL)
- 5-turn chat sample comparison vs Llama-3.2-3B baseline
- cost actual + wall actual
- honest C3 disclosures
```

---

## End of handoff prompt

위 PROMPT TO PASTE 부분을 새 Claude Code 세션에 한 번에 붙여넣으면 됩니다.

추가로 필요한 context:
- 본 conversation full transcript: `/Users/ghost/.claude-claude12/projects/-Users-ghost-core-anima/5aa93161-b144-4dfd-90e4-4955b2a94b54.jsonl`
- 본 roadmap (master SSOT): `docs/n_substrate_consciousness_roadmap_2026_05_01.md` (today batch-13/14/15/16/17 §59-§66)
- 본 P9 spec doc: `docs/p9_sft_spec_2026_05_02.md`
