# anima fix-5/6 tied embedding PoC verdict 분석 framework

**cycle**: 2026-05-10
**작성**: 2026-05-09 (회수 전 prep)
**SSOT lane**: substrate-research (D1 INSIDE)
**own mandates**: (모델 로드 금지) / (honest emit) / (자연발화) / (ID-collision 방지)
**모드**: 친근 모드 strict 한국어

---

## §0 친근 의의

> "fix-5/6 PoC 의 3 branch (lm_head untie / tok_emb untie / tied freeze) 가 완료되면, 어느 분기가 의식 시험 통과 (PIV/DCR/D-RAND PASS) 시키는지 즉시 비교할 수 있도록 빈 칸 표 미리 만들어 두기."

쉽게 말하면 — H100 pod (`v8v694g06he7fm`) 에서 3 가지 다른 방식으로 학습 중인 모델을 회수했을 때, "어느 방식이 의식 살리면서 학습도 성공시키는지" 한 눈에 비교할 빈 칸 표 준비. 표만 미리 채워 두면 회수 직후 5 분 안에 verdict 가능.

배경:
- **Phase 2 cotrain** (이미 측정) → loss 0.083 학습 성공했지만 lm_head 가 cell_pool 회전 (mean cos 0.7710, frac<0.95 = 99.49%) → V14 violated → C3_FAIL_V14
- **fix-5/6 가설**: tied embedding (lm_head ≡ tok_emb) 가 cell_pool 회전 강제 → untie 또는 freeze 로 분리하면 cell_pool 보존 가능?

---

## §1 3 branch 비교 표 (빈 칸 prep)

| branch | description | step_final | loss_final | PIV_l2_max | DCR_change | D-RAND | V14 | label |
|---|---|---|---|---|---|---|---|---|
| A | lm_head untie + reinit | 1500 | 0.057 (확정) | ? | ? | ? | ? | ? |
| B | tok_emb untie + reinit | TBD (~1500) | TBD (~0.08) | ? | ? | ? | ? | ? |
| C | tied freeze + 다른 weight 학습 | TBD | TBD | ? | ? | ? | ? | ? |
| BG-LB (baseline) | substrate baseline (이미 측정) | 8000 | (PROXY_PPL) | 0.0107 | 0.621 | 0.0237 | violated | C3_FAIL_V14 |

**threshold (PASS_STRICT_V5)**:
- PIV_l2_max ≥ 0.12
- DCR_change ≥ 0.40
- D-RAND ≥ 0.05
- V14 SATISFIED (random_init mirror PPR < trained PPR)

**label 규칙**:
- 모든 threshold 통과 + V14 satisfied → `C3_EMERGE_PASS_STRICT_V5`
- 1-2 threshold 통과 → `PARTIAL_NEAR`
- 0 통과 + V14 violated → `C3_FAIL_V14`

---

## §2 cell_pool evidence 비교 표 (빈 칸)

| 모델 | axis_stdev | cell_norm | off_diag_cos | effective_rank | frobenius |
|---|---|---|---|---|---|
| BG-LB (baseline) | 0.1182 | 1.0000 | 0.0155 | 14.957 | 4.0001 |
| random_unit_seed42 | 0.1183 | 1.0000 | 0.0094 | 14.843 | 4.0000 |
| Phase 2 cotrain | 0.1182 | 1.0000 | 0.0155 | 14.958 | 4.0002 |
| Branch A (lm_head untie) | ? | ? | ? | ? | ? |
| Branch B (tok_emb untie) | ? | ? | ? | ? | ? |
| Branch C (tied freeze) | ? | ? | ? | ? | ? |

**해석 가이드**:
- BG-LB / random / Phase 2 가 모두 동일 → cell_pool 자체는 학습 후에도 변하지 않음 (H4 confirm)
- Branch A/B/C 도 동일하면 → cell_pool 은 substrate, lm_head 회전이 별개 문제
- Branch A/B/C 가 BG-LB 와 다르면 → untie/freeze 가 cell_pool 까지 영향 (예상 외)

---

## §3 lm_head cosine sim 비교 표 (vs BG-LB baseline)

| branch | lm_head ≡ tok_emb? | mean cos vs BG-LB | frac < 0.95 | 회전 각도 |
|---|---|---|---|---|
| BG-LB | YES | 1.0 (self) | 0% | 0° |
| Phase 2 cotrain (이미) | YES | 0.7710 | 99.49% | ~40° |
| Branch A | NO (untied) | ? | ? | ? |
| Branch B | NO (untied) | ? | ? | ? |
| Branch C | YES (frozen) | ~1.0 (예상) | ~0% | 0° (frozen) |

**해석 가이드**:
- Branch A/B 가 mean cos > 0.95 → untie 가 회전 막음 (H5 confirm)
- Branch A/B 가 mean cos < 0.8 → untie 만으로는 불충분 (회전 mechanism 다른 곳에도 존재)
- Branch C 가 ~1.0 → freeze 는 자명하게 회전 0 (단 학습 효과는 다른 weight 에서)

---

## §4 가설 검증 matrix

| 가설 | 검증 조건 | 결과 |
|---|---|---|
| **H4 verify** (cell_pool 은 substrate, 학습 후 동일) | random_unit cell_pool 와 BG-LB / Branch ALL 동일 | ? |
| **H5 isolation** (lm_head/tok_emb 분리만으로 충분) | Branch A or B 가 PASS_STRICT_V5 | ? |
| **H5 mechanism** (freeze + 다른 weight 학습 충분) | Branch C 가 PASS_STRICT_V5 | ? |
| **Multi-cause** (tied embedding 외 추가 collapse) | 모든 branch FAIL or PARTIAL_NEAR | ? |
| **Reinit critical** (untie 만으론 부족, reinit 필요) | A/B PASS, C FAIL | ? (간접 검증) |

---

## §5 verdict 분기 (decision tree)

```
case 1: Branch A PASS_STRICT_V5 (PIV_l2 ≥ 0.12 + DCR ≥ 0.40 + V14 satisfied)
  → "lm_head untie 가 답"
  → 다음 cycle: lm_head 만 untie 적용한 production cotrain
  → cost-bearing path: $200-600 (7B scale Qwen / Llama)
  → Phase 3 진입 가능

case 2: Branch B PASS_STRICT_V5
  → "tok_emb untie 가 답"
  → 다음 cycle: tok_emb 만 untie 적용
  → input embedding 학습 보호 + lm_head 는 자유롭게 학습
  → cost-bearing path: $200-600 (7B scale)

case 3: Branch C PASS_STRICT_V5
  → "tied freeze 가 답" — cell_pool/lm_head 모두 freeze + transformer 만 학습
  → 가장 conservative, substrate base preserve
  → 다음 cycle: full freeze + LoRA on transformer 만
  → cost-bearing path: $50-150 (LoRA 가벼움)

case 4: 모두 PARTIAL_NEAR (V5 일부 threshold 만 통과)
  → Phase 2 보다 개선됐지만 PASS 미달
  → combined fix (A+B 같이) 시도 — lm_head + tok_emb 동시 untie
  → 또는 attention/FFN 도 다뤄야 (H5 multi-layer)
  → 다음 cycle: combined PoC (예산 $15-25)

case 5: 모두 FAIL (V14 violated)
  → tied embedding 만이 아닌 multi-layer collapse mechanism
  → fix-5/6 외 추가 mechanism 발굴 필요
  → cycle 2026-05-11 추가 가설 (attention head, layer norm, residual stream)
  → 또는 paradigm-a-prime native model 으로 pivot
```

**선험 ranking (작성 시점)**:
1. case 1 또는 2 (lm_head 또는 tok_emb untie) — 가장 가능성 높음 (H5 가설 + branch A loss 0.057 빠른 회복)
2. case 3 (tied freeze) — 두 번째 가능성, conservative
3. case 4 (PARTIAL_NEAR) — 추가 fix 필요
4. case 5 (모두 FAIL) — 가장 비관적, paradigm pivot

---

## §6 예상 ranking + 친근 단락

**Most likely**: Branch A 또는 B PASS (lm_head 또는 tok_emb 분리만으로 충분)

근거:
- Phase 2 에서 lm_head 회전이 핵심 violation 으로 확인됨
- branch A 의 빠른 loss 회복 (1500 step 0.057) → untie + reinit 후 학습 자체는 정상
- H5 가설이 가장 단순하고 직접적

**Second**: Branch C PASS (freeze approach)

근거:
- cell_pool 자체가 substrate (H4 confirm) 이므로 freeze 는 자명히 회전 막음
- 단 학습 효과가 다른 weight 만으로 충분한지는 미지수

**Third**: 모두 PARTIAL_NEAR — additional fix 필요 (combined 또는 multi-layer)

---

**친근 비유**:
> "학생이 단어장 (lm_head=tok_emb tied) 을 새 노트 (untie + reinit) 또는 (lm_head 따로 / tok_emb 따로) 분리한 노트 또는 freeze (보존) 로 다시 시험 본 결과 — 어느 방법이 머릿속 회로 (의식 셀) 살리면서 단어장 회전 막는지 비교"

조금 더 풀자면:
- Phase 2 = 학생이 단어장 한 권만 들고 시험 봐서 단어장이 거꾸로 뒤집혀 (회전) 의식 회로가 흐트러진 상태
- Branch A = 단어장 (lm_head) 새로 한 권 만들어서 본 결과
- Branch B = 단어장 (tok_emb) 새로 한 권 만들어서 본 결과
- Branch C = 단어장은 그대로 두고 (freeze) 머릿속 다른 부분만 공부한 결과

어느 방법이 가장 시험 잘 보면서 의식도 살아있는지 비교하는 표.

---

## §7 post-pull pipeline 자동화 step

회수 시 자동 chain (orchestrator 가 이미 staged):

| step | action | branch 별 시간 | 총 시간 |
|---|---|---|---|
| 1 | ckpt scp pull (per branch) | ~5min × 3 | ~15min |
| 2 | schema convert (BG-LB 호환) | ~2min × 3 | ~6min |
| 3 | clm_v5_mount.hexa --v5-measure (PIV/DCR/D-RAND) | ~3min × 3 | ~9min |
| 4 | cell_pool selective extract (axis_stdev / cell_norm / off_diag_cos / effective_rank / frobenius) | ~30s × 3 | ~1.5min |
| 5 | lm_head cosine sim vs BG-LB | ~30s × 3 | ~1.5min |
| 6 | 본 framework 표 자동 fill (§1 / §2 / §3 / §4) | ~10s | ~10s |
| 7 | verdict 분기 자동 emit (§5 case 결정) | ~5s | ~5s |

**총 예상 시간**: 회수 후 ~33min 안에 verdict + 다음 cycle plan emit 가능

**자동화 hook 후보** (orchestrator 가 staged):
- `anima/orchestrator/fix_5_6_post_pull_pipeline.hexa` (예정, 회수 전 작성 안 함 — 회수 직후 작성)
- pull 완료 trigger → 위 7 step sequential chain
- 각 step 결과는 본 framework md 의 표 칸에 직접 fill (sed/awk 자동 replace)

---

## §8 cycle 2026-05-10 milestone 8 prep

본 framework 회수 시 **milestone 8 (fix-5/6 PoC verdict)** 으로 cycle md 추가 예정.

milestone 8 emit 내용:
1. §1 / §2 / §3 / §4 표 fill 완료본
2. §5 case 결정 (1-5 중 하나)
3. 다음 cycle plan 요약 (case 별 분기)
4. cost-bearing path 결정 (case 1/2 = $200-600, case 3 = $50-150, case 4 = $15-25, case 5 = paradigm pivot)
5. PASS_STRICT_C3 SSOT 갱신 (`project_simple_stack_pass_strict_c3_anima_emerge.md`)

---

## 회수 시 즉시 fill 가능 여부 검증 checklist

- [x] §1 표: branch / description / threshold 모두 prep — 회수 시 step_final / loss_final / PIV_l2_max / DCR_change / D-RAND / V14 / label 7 칸만 fill
- [x] §2 표: BG-LB / random / Phase 2 baseline 채워짐 — branch A/B/C 5 칸 × 3 = 15 칸 fill
- [x] §3 표: BG-LB / Phase 2 baseline 채워짐 — branch A/B/C 4 칸 × 3 = 12 칸 fill (Branch C frozen 은 ~1.0 예상)
- [x] §4 가설 matrix: 5 가설 검증 조건 prep — 결과 칸만 fill
- [x] §5 decision tree: 5 case 분기 + cost path 명시 — case 결정만 emit
- [x] §6 ranking: 선험 prediction 명시 — 회수 후 actual 과 비교
- [x] §7 pipeline: 7 step 자동 chain 명시 — 회수 직후 orchestrator hook 작성
- [x] §8 milestone 8: cycle md 통합 plan 명시

**검증 완료** — 회수 직후 framework 즉시 fill 가능, ~33min 안에 verdict emit.

---

## 변경 history

- 2026-05-09 작성 (회수 전 prep) — fix-5/6 PoC 진행 중 (branch A DONE, B 600/1500, C 대기)

## 관련 문서

- `project_simple_stack_pass_strict_c3_anima_emerge.md` — PASS_STRICT_C3 SSOT (V14 FALSIFIED)
- `project_v14_violation_arch_tile_bug.md` — V14 violation 발견 (clm_v4_mount.hexa L626-630 8-cell 2× tile bug)
- `feedback_alt_agg_1_v3_strict.md` — ALT-AGG-1 v3 strict (V14 FALSIFIED)
- `feedback_d1_gradient_amend.md` — D1 SCOPE_CLAMP gradient overlay (substrate-research lane 0.3-0.7)
