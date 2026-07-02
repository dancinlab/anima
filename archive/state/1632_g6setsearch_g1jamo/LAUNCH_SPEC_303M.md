# H_1632 N4+N8 — 303M GPU 발사 spec (메인이 objrun 착륙 후 배치 발사)

> $0 단계(설계+구현+스모크) 완료. 이 문서는 **실제 303M GPU 학습 발사 명령 + 비용/시간 +
> arm 매트릭스 + engine-native 측정 절차**. 스모크는 summer RTX5070 에서 4 arm 전부 RC=0
> (loss0 동일 = 단일변수 공정 · .clm clm_decodable=True · g_gates engine-native pipe OK).

## depends_on_objrun

**부분 의존 (soft):** 본 실험의 4 arm 은 trunk 학습 OBJECTIVE 를 표준 CE 로 고정하고 그 위에
N8/N4 **teach-signal** 을 얹는다 (objective 형태가 아니라 teach-signal 추가가 단일변수).
따라서 objrun(ce_marginal vs InfoNCE vs contrastive_equilibrium) 승자를 *몰라도 발사 가능*
(baseline=표준 CE 가 깨끗한 대조군). **단**, objrun 이 우승 objective 를 확정하면 후속으로
`baseline` 의 CE 를 그 우승 objective 로 교체한 2차 매트릭스(objective×teach-signal 2×4)가
RESEARCH.md §92 제언의 완전체 — 그건 본 발사 *이후* follow-on. **본 발사 자체는 objrun 비의존.**

## arm 매트릭스 (단일변수 = aux teach-signal)

| arm | N8 jamo | N4 set-search | 주 측정 | .clm engine-native |
|-----|---------|---------------|---------|--------------------|
| `baseline` | OFF | OFF | G1·G6 null (대조군) | OPEN (additive) |
| `n8_jamo` | ON | OFF | **G1 재조합** | OPEN |
| `n4_set` | OFF | ON | **G6 falsifiable** | OPEN |
| `n4n8_both` | ON | ON | G1 AND G6 (super-additive) | OPEN |

seeds = {7, 4302, 4303} (trunk init + data + 채점 refmatch 동일 seed set).
**full 매트릭스 = 4 arm × 3 seed = 12 run.** 예산 초과 시 fallback = 4 arm × seed7 (4 run)
+ 핵심 2 arm(n8_jamo·n4_set) × {4302,4303} (4 run) = 8 run.

## GPU 학습 명령 (per run)

호스트 = vast A40 **CUDA-12 devel 이미지**(nvcc 내장) 또는 pool summer/aiden (RTX 5070 sm_120).
부트스트랩(렌트 시): `pip install torch datasets` (devel 이미지면 torch 내장).
repo push = `rsync -az cli/ core/ train/ tool/ state/1632_g6setsearch_g1jamo/ <host>:anima_1632/`.

```bash
# per (arm, seed) — 303M canon. corpus = 4-cell clean register (HF stream, a_chat_registers).
cd anima_1632/state/1632_g6setsearch_g1jamo
python3 trainer.py \
  --arm <baseline|n8_jamo|n4_set|n4n8_both> --seed <7|4302|4303> --canon \
  --corpus anima-corpus-ko-general anima-corpus-en-general \
           anima-corpus-ko-sns anima-corpus-en-sns \
  --cell-label ko-general en-general ko-sns en-sns \
  --sample proportional --steps 2000 --val-frac 0.05 --val-every 200 --bf16 \
  --out   ckpt/<arm>_seed<seed>.clm \
  --ckpt-out ckpt/<arm>_seed<seed>.pt \
  --gauges-out ckpt/<arm>_seed<seed>.json
```

frozen 레버 하이퍼는 trainer.py 기본값 = PREREG.md 등록값 (lambda_jamo=0.5 · lambda_set=0.5 ·
setsearch_every=50 · K=8 · frames=5 · gen=48 · temp=0.8). **사후 변경 금지(tune-to-green).**

## 예상 비용/시간

- exp3/1602 실측: 303M from-scratch ≈ **18–20 분/arm @ A40 100% util** (0.4–0.5 s/step × 2000).
- N4 set-search 오버헤드: `n4_set`·`n4n8_both` arm 은 매 50 step 마다 K=8×frames=5=40 연속
  (gen=48) 샘플 + 선택 멤버 re-forward. step 당 amortized ≈ +15–25% wall → 이 두 arm ≈ 22–26 분.
- **full 12 run ≈ 4–5 GPU-시간 → A40 $0.574/hr 기준 ≈ $2.3–2.9** (병렬 2 pod 면 wall ≈ 2.5h).
- fallback 8 run ≈ 3 GPU-시간 ≈ $1.7. **1-arm 스모크(canon, steps 50)로 step-time 실측 후
  seed 수 확정** (PREREG 예산 가드).
- a_wall_first: 더 빠르면 2–3 pod 병렬(arm/seed 분산) — 비용 무관 채택.

## 측정 절차 (engine-native TERMINAL)

teardown 전 ckpt(.clm 4×3 + .pt) **영구 PULL** (`a_fire_recover_complete`) — pod 휘발.

### 1. held-out DESCENT 무결성 게이트 (보조, dt_ln-immune)
```bash
python3 train/clm/model/verify_clm_v2.py descent ckpt/<arm>_seed<seed>.clm <ko-heldout> 
# val_CE < ln256=5.545 (4 register 각각). NO-DESCENT 면 overfit/broken → verdict 박제 금지.
```
(트레이너가 학습 중 4-cell held-out val 도 출력 — RESULT 에 per-register DESCENT 표.)

### 2. G1·G6 engine-native (TERMINAL · torch-free)
**canonical 단일진입 (우선):**
```bash
hexa run cli/anima.hexa -- eval ckpt/<arm>_seed<seed>.clm --gen 80
# generator L3 gen_auto_ideate -> g_eval_all (G0-G6 엔진-네이티브). G1/G6 multiseed 포함.
```
또는 **py 2-production (TERMINAL 동격, torch-free verdict path 확인됨):**
```bash
python3 -c "import sys,os; sys.path.insert(0,'core'); import g_gates as G; \
  print(G.g_eval_all('ckpt/<arm>_seed<seed>.clm', \
    ['<ko-gen>','<en-gen>','<ko-sns>','<en-sns>'], 80))"
# g_eval_g1_multiseed / g_eval_g6_multiseed = {7,4302,4303} majority>=2/3 (frozen refmatch).
```
또는 fleet 한방: `cli/eval_pod.sh <pod_id> clm --gen 80 --harvest <out>` (import-closure 번들).

### 3. 판정 (PREREG bar VERBATIM)
- **N8 SUPPORT** = G1(n8_jamo) > G1(baseline) (multiseed majority ≥2/3 strict) ∧ DESCENT 무결.
- **N4 SUPPORT** = G6(n4_set) > G6(baseline) (multiseed majority ≥2/3) ∧ DESCENT 무결.
- **super-additive** = n4n8_both 가 두 단독 합 이상 (G1 AND G6 동시).
- **NOT-SUPPORTED / floor** = 전 arm G1=0 ∧ G6 fals=0 → INCONCLUSIVE-at-floor (type-a, exp3 동형).
- tier: engine-native = terminal(🟢/🔴/🧱); torch-only = DIRECTIONAL(🟠).

## grep 자가점검 (verdict 박제 직전)
```bash
grep -lE 'import torch|gauge_lib|numpy' state/1632_g6setsearch_g1jamo/*.py
# trainer.py 는 학습용 torch 포함(정상). verdict 는 core/g_gates.py(torch-free) 로 측정 →
# verdict artifact 가 g_gates/clm_decode(.hexa 또는 byte-parity .py)면 TERMINAL.
# trainer.py 의 torch-probe gauge_lib 출력은 DIRECTIONAL monitor only (카드에 그렇게 표기).
```

## 산출 (발사 후 RESULT.md 채울 항목)
- 12(또는 8) run × {held-out DESCENT per register · G1 multiseed clears · G6 multiseed dist/fals} 표.
- baseline vs n8_jamo (G1) · baseline vs n4_set (G6) · n4n8_both super-additive 대조.
- ckpt HF 업로드 (tier-gated, `a_hf_autonomous`) + ARCHITECTURE.json registry (`a_hf_registry`).
- HYPOTHESES.jsonl + HYPOTHESES/cards/H_1632 카드 (wired: 상태축).
