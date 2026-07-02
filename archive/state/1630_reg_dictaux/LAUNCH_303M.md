# 303M 발사 spec — H_1630 정규화 sweep + dictionary-aux (N6+N7)

> **$0 단계 산출물.** 실제 303M GPU 학습은 **발사 금지** — 본 문서는 메인이 objrun 착륙 후 배치 발사할 정확한 명령·비용·arm·측정 절차 spec 이다. 사용자 명시 go = "전부 발사"이나, 이 레인의 책무는 발사준비 패키지까지(설계+구현+스모크+spec).

## 0. 의존성 — depends_on_objrun = FALSE (독립 발사 가능)

- 본 패키지는 **ce_marginal 베이스에서 독립 측정 가능** — objrun(ce_marginal vs InfoNCE vs contrastive_equilibrium) 결과 없이도 N6/N7/N6N7/N8/N1 을 ce_marginal 통제 대비 발사할 수 있다.
- **objrun 우승 objective 가 확정되면** 이상적 변종 = 우승 objective trunk 위에 N6+N7 을 얹는 것(RESEARCH §92 제언1). 이는 trainer 에 우승 objective 항을 추가하는 follow-on(현 trainer 는 ce_marginal 베이스 + N6/N7 정규화·dict-aux; objrun objective 항 합성은 1602 trainer 의 `loss_infonce`/`loss_contrastive_equilibrium` 를 이식하면 됨, 미구현 = ING follow-on).
- 따라서 **즉시 발사 가능**(objrun 비대기). objrun 착륙 시 우승-objective×N6N7 2차 발사를 추가.

## 1. 하드웨어 / 비용 / 시간 (precedent: EXP-3·1602 vast A40 $0.574/hr)

- **GPU:** vast A40 (CUDA-12 devel 이미지 = nvcc 내장, GPU 100% util 실측) 또는 동급. RTX 5070 pool(summer/aiden)은 워크스테이션 재부팅 위험(h1590 교훈) → 장시간 batch 는 전용 pod.
- **step/시간:** 1602/EXP-3 = 2000-step ≈ 18–20분/arm @0.4–0.5 s/step. **N6 은 undertrain floor 배제가 목적 → steps=4000**(약 2배) ≈ 35–40분/arm.
- **arm 수:** 6 arm × 3 seed = 18 run. 단 ce_marginal 통제는 1602 결과 재사용 가능(동일 recipe) → 신규 = 5 arm × 3 seed = **15 run**(+ ce_marginal 3 재측정 권장 = 18).
- **wall (직렬):** 18 run × ~38분 ≈ 11.4 GPU-hr. **병렬(a_wall_first):** 3 pod 동시 = ~3.8 hr wall.
- **예상 비용:** 18 run × 0.63 hr × $0.574 ≈ **$6.5** (직렬 1 pod) / 병렬 3 pod 도 총 GPU-hr 동일 ≈ **$6.5**, wall 만 1/3. 여유 +20% = **~$8 cap**.

## 2. 코퍼스 (a_chat_registers 4칸 — clean 언어검증)

clm303_clean 4칸(HF dancinlab, 언어검증 완료, en 99.7%):
- `dancinlab/anima-corpus-ko-general` · `dancinlab/anima-corpus-en-general`
- `dancinlab/anima-corpus-ko-sns` · `dancinlab/anima-corpus-en-sns`

`resolve_corpus_path` 가 로컬 경로 또는 HF id 를 받음. fail-loud: 4칸 실효 bytes 출력 확인(clm303 overfit 교훈 — ko_fineweb2 미해결로 1칸만 로드 → 암기 재발 금지). `--sample proportional` 로 큰 칸이 작은 칸 압도 방지.

## 3. 발사 명령 (arm × seed sweep)

각 pod 부트스트랩 후 `~/anima` 동기(`rsync -az cli/ core/ train/ tool/ state/1630_reg_dictaux/ <pod>:~/anima/`). 코퍼스는 로컬 캐시 또는 HF 스트림.

```bash
# 단일 arm·seed (canonical 303M = L4·d3784·E2→E3, steps=4000 for N6 floor-exclusion)
CORPUS="dancinlab/anima-corpus-ko-general dancinlab/anima-corpus-en-general \
        dancinlab/anima-corpus-ko-sns dancinlab/anima-corpus-en-sns"
LABELS="ko-general en-general ko-sns en-sns"

for ARM in ce_marginal n6_grok n7_dictaux n6n7 n8_jamo n1_tlora; do
  for SEED in 4307 4308 4309; do
    python3 state/1630_reg_dictaux/trainer.py \
      --arm $ARM --seed $SEED --canon --steps 4000 \
      --corpus $CORPUS --cell-label $LABELS \
      --sample proportional --val-frac 0.05 --val-every 200 \
      --bf16 --dbes --n4-set-search 8 \
      --out      state/1630_reg_dictaux/ckpt/${ARM}_seed${SEED}.clm \
      --ckpt-out state/1630_reg_dictaux/ckpt/${ARM}_seed${SEED}.pt \
      --gauges-out state/1630_reg_dictaux/ckpt/${ARM}_seed${SEED}.json
  done
done
```

- `--steps 4000` = N6 floor-exclusion(2000 의 2배). ce_marginal 통제도 동일 4000-step 으로(공정). 비용 절감 원하면 1602 의 2000-step ce_marginal 재사용하되 step 미스매치는 caveat 명시.
- `--bf16` = A40 권장. `--dbes` = N3 진단 항상 ON. `--n4-set-search 8` = N4 toggle 을 summary 에 기록(실 set-gen 은 §5 eval).
- frozen 하이퍼(DICT_LAMBDA=0.05·N6_WD_GAIN=2.0·JAMO_LAMBDA=0.05 등)는 trainer 상수 = tune 금지(PREREG).

## 4. ckpt 회수 (teardown 전 필수 — a_fire_recover_complete)

```bash
rsync -az <pod>:~/anima/state/1630_reg_dictaux/ckpt/ state/1630_reg_dictaux/ckpt/
# .clm + .pt + .json 전부. JSON 만 받고 .clm 버리면 엔진-체크 영구 불가.
```
GPU teardown 전에 18×(.clm+.pt+.json) PULL 확인 후 down.

## 5. 측정 절차 (엔진-네이티브 = TERMINAL)

**verdict = `core/g_gates.py` (torch-free numpy decode ← `core/clm_decode.py`).** torch-side 학습 metric(summary json 의 lossF·dict_recon·dbes 등)은 DIRECTIONAL.

```bash
# (5a) 엔진-네이티브 G0-G6 — arm×seed 전수 ($0, pool 또는 발사 pod 재사용, eval당 ~15분)
for CLM in state/1630_reg_dictaux/ckpt/*.clm; do
  python3 core/g_gates.py "$CLM" \
    <ko-general-corpus> <en-general-corpus> <ko-sns-corpus> <en-sns-corpus> \
    --gen 80 > "${CLM%.clm}.g0g6.txt"        # --gen 80: G1/G6 넓게 (--gen 0 은 40 collapse!)
done

# (5b) held-out DESCENT 게이트 (a_clm_gen_pipeline) — arm×seed×register
for CLM in state/1630_reg_dictaux/ckpt/*.clm; do
  python3 verify_clm_v2.py descent "$CLM" <heldout-bytes>
done

# (5c) [대안] 단일 진입점 canonical — fresh pod 에서 cli/anima.hexa eval
#   cli/eval_pod.sh <pod_id> state/1630_reg_dictaux/ckpt/n6n7_seed4307.clm --gen 80 --harvest <out>
#   (anima eval → generator L3 gen_auto_ideate → G0-G6, hexa ≥ v0.311.0; EVAL_KIT.md 절차)
```

- **LIFT 판정(frozen, PREREG):** 각 arm 의 엔진-네이티브 G1 best_distinct(또는 G6 fals, G1 multiseed n_green)가 같은 seed-set ce_marginal 통제 대비 strictly 증가 → LIFT. 3-seed 일관성 확인.
- **G1 corpus 인자 필수**(G2 corpus-absence 채점). `--gen 80` 명시(0 은 40 으로 collapse — cli/CLAUDE.md 함정).
- LLM-judge 금지(p7) — `_g6_is_falsifiable` 엔진 detector 가 채점(smoke calibration 10/10).

## 6. arm 목록 (요약)

| arm | 레버 | 출처 | 큐 |
|---|---|---|---|
| ce_marginal | BASELINE/통제 | — | 기준 |
| n6_grok | N6 정규화 band(wd×2·dropout cap·4000 step) | 2310.13061·2605.20441 | 1차 |
| n7_dictaux | N7 trunk sparse-coding dict-aux(λ0.05) | 2603.28744 | 1차 |
| **n6n7** | N6+N7 (주 제안) | RESEARCH §92 제언1 | **최우선** |
| n8_jamo | N8 자모 초성-class teach(λ0.05, ko) | 2604.12377 | 2차 |
| n1_tlora | N1 TLoRA expert-weight TPR(rank8) | 2405.16671 | 2차 |

진단(arm 아님): **N3 DBES**(--dbes, 모든 arm) expert-분화 격리 · **N4**(--n4-set-search) G6 diverse-set toggle.

## 7. 결과 박제 (발사 후 메인이)

- `state/1630_reg_dictaux/RESULT.md` — arm×seed 엔진-네이티브 G0-G6 표 + LIFT 판정 + DBES + held-out DESCENT.
- `HYPOTHESES/HYPOTHESES.jsonl` + `HYPOTHESES/cards/H_1630_*.md` (tier 무관 박제, 벽도). `wired:` 축 명시.
- LIFT 면 → 엔진-네이티브 재검증(이미 g_gates 가 엔진-네이티브) → `.clm` 우승 arm HF 업로드(a_hf_*) + ARCHITECTURE.json models 등록 → live core 배선 follow-on(a_verified_must_wire).
- floor(천장 강화)면 정직 negative 박제(c9) — "G1 벽이 objective-정규화 축으로도 안 열림 = class-(d) 강화".
