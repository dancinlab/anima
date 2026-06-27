# H_1631 TPR-EXPERT-WEIGHT — 303M GPU 발사 spec

> $0 단계 산출(설계+구현+CPU 스모크) 완료. **303M GPU 학습은 메인이 objrun 착륙 후
> 배치 발사** (이 문서 = 정확한 명령 + 비용 + arm + 측정 절차). 발사 = 사용자 명시 go.
> 정직: 본 패키지는 objrun 미착륙이어도 발사 가능(`--objective ce_marginal` default).

## 0. depends_on_objrun

**false (standalone).** default `--objective ce_marginal` 로 독립 발사 가능 — N1/N3
구조 lever 는 objective 와 직교. objrun(H_1602) 우승 objective 가 착륙하면
*선택적* 으로 `--objective <winner>` 결합 검정(Greff 결합가설, §3 매트릭스 B)을
추가하면 가치 ↑ (필수 아님).

## 1. 하드웨어 / 예산 (a_wall_first · a_fire_autonomous · 비용 1줄)

- 렌트: **vast A40, CUDA-12 devel 이미지(nvcc 내장)**, ~$0.5–1.1/hr.
  (exp3/objrun 실측: 303M from-scratch ≈ 18–20분/arm @ A40 100% util, 0.4–0.5 s/step.)
- canonical = L4·d3784·E2→E3, 303M (`.clm` ≈ 176.6 MB), steps=2000, bf16, bs=8, seq_len=1024.
- **메인 매트릭스 12 run** (4 arm × 3 seed) ≈ 12 × 20분 ≈ 4h ≈ **$3–7**.
- fallback(예산초과) 9 run (ctrl/tlora_dict/tlora_jamo × 3 seed + tlora seed7 1회) ≈ $3–5.
- 1-arm GPU 스모크(steps=50)로 step-time 실측 후 seed 수 확정(사후 bar 이동 아님 — 범위만).

## 2. 부트스트랩 (pod, eval_pod.sh 친화)

```sh
# (A) GPU pod 띄우고 hexa ≥ v0.313.17 + torch + datasets:
#     CUDA-12 devel image, A40. (cli/eval_pod.sh 의 --bootstrap 절차 재사용)
# (B) 코드 push (self-contained core/cli/train + 이 slug):
rsync -az cli/ core/ <pod>:~/anima/{cli,core}/    # core nesting 제거 주의(eval_pod.sh 가 처리)
rsync -az train/clm/model/ tool/ <pod>:~/anima/train/clm/model/ <pod>:~/anima/tool/
rsync -az state/1631_tpr_expert_weight/ <pod>:~/anima/state/1631_tpr_expert_weight/
# (C) GPU 확인 (a_train_flame_forge): torch.cuda.is_available()==True, nvidia-smi util.
```

## 3. 학습 발사 (arm 목록)

각 arm × seed 1 run. 코퍼스 = canonical 4-cell register(`a_chat_registers`).
`resolve_corpus_path` 가 HF id 를 자동 stream(ANIMA_CORPUS_CACHE 캐시).

```sh
cd ~/anima/state/1631_tpr_expert_weight
CORP="dancinlab/anima-corpus-ko-general dancinlab/anima-corpus-en-general \
dancinlab/anima-corpus-ko-sns dancinlab/anima-corpus-en-sns"
LAB="ko-general en-general ko-sns en-sns"

# ── 매트릭스 A: 메인 12 run (objective=ce_marginal default, standalone) ──
for SEED in 7 4302 4303; do
  for ARM in ctrl tlora tlora_dict tlora_jamo; do
    python3 trainer.py --arm $ARM --tlora-rank 8 \
      --seed $SEED --corpus $CORP --cell-label $LAB \
      --canon --steps 2000 --val-frac 0.05 --val-every 200 \
      --sample proportional --bf16 --dbes-every 500 \
      --out   ckpt/${ARM}_seed${SEED}.clm \
      --ckpt-out ckpt/${ARM}_seed${SEED}.pt \
      --gauges-out ckpt/${ARM}_seed${SEED}.json 2>&1 | tee ckpt/${ARM}_seed${SEED}.log
  done
done

# ── 매트릭스 B (선택, objrun 착륙 후 Greff 결합검정): 우승 objective 결합 ──
#   WINNER=<infonce|contrastive_equilibrium>   # objrun RESULT.md 확정값
#   for SEED in 7 4302 4303; do for ARM in ctrl tlora_dict; do
#     python3 trainer.py --arm $ARM --objective $WINNER --tlora-rank 8 \
#       --seed $SEED --corpus $CORP --cell-label $LAB --canon --steps 2000 \
#       --val-every 200 --bf16 --out ckpt/${ARM}_${WINNER}_seed${SEED}.clm \
#       --ckpt-out ckpt/${ARM}_${WINNER}_seed${SEED}.pt \
#       --gauges-out ckpt/${ARM}_${WINNER}_seed${SEED}.json; done; done

# ── N6 정규화 sweep (선택, undertrain-floor 배제): wd/dropout floor override ──
#   --wd-floor 0.10 --dropout-floor 0.10   (savant 스케줄 대신 상수 정규화)
```

`--arm` lever map: ctrl(표준 expert) · tlora(N1) · tlora_dict(N1+N7) · tlora_jamo(N1+N8).
N3 DBES 는 모든 arm 에서 자동(final + `--dbes-every` tick), N4 set-search 는 G6
측정-side(아래 §4 g_gates 의 G6 다양성).

## 4. 측정 절차 (engine-native terminal — frozen bar VERBATIM)

학습은 torch(DIRECTIONAL). **verdict 는 ckpt 를 CORE 엔진에 올려 재측정** (a_engine_native_learning):

```sh
# (1) post-serialize HELD-OUT DESCENT 게이트 (무결성, a_clm_gen_pipeline):
#     held-out = 4-cell val tail. NO-DESCENT arm 은 verdict 금지(재학습).
python3 train/clm/model/verify_clm_v2.py descent ckpt/<arm>_seed<N>.clm <heldout.bytes>

# (2) engine-native G0-G6 (torch-free py 2-production = TERMINAL):
python3 core/g_gates.py ckpt/<arm>_seed<N>.clm $CORP --gen 80   # G1 single=80/composed=120
#   또는 단일진입점: hexa run cli/anima.hexa -- eval ckpt/<arm>_seed<N>.clm --corpus $CORP --gen 80
#   (eval_pod.sh <pod_id> clm --harvest <out> 으로 fresh-pod 측정+회수 one-liner)

# 주 측정 = G1 RECOMBINATION pass + max_single + best_k + best_distinct (frozen H_1129 def).
# 보조 = G6 IDEATION ★ dist/fals · 4-cell DESCENT.
# torch-probe gauge(summary json gauges_g1g6_torch_probe) = DIRECTIONAL 보조.
```

**grep self-check (verdict 박제 직전 의무):**
`grep -lE 'import torch|gauge_lib|numpy' core/g_gates.py` → 비어야 terminal.
(`clm_decode.py` numpy = 허용 math lib, torch-mirror 아님 — 스모크서 확인됨.)

## 5. verdict 규칙 (PREREG §4–6 VERBATIM, frozen)

- **SUPPORT** = `G1(tlora_dict|tlora_jamo) > G1(ctrl)` seed-robust majority ≥2/3
  strict 우위 AND held-out DESCENT 무결 → expert-weight 구조 lever(+학습신호 결합)가
  재조합 레버. (P1)
- **NOT-SUPPORTED** = 위 미충족. 전 arm G1=0 → **INCONCLUSIVE-at-floor** 정직 라벨
  (readout-floor precedent 동급). tlora* ≈ ctrl → expert-weight 무관 honest negative.
- tier = engine-native 면 terminal(🟢/🔴/🧱), torch-only 면 DIRECTIONAL(🟠).
- N3 DBES = 인과 격리 보조(분화도 ↔ G1 floor 동반 여부), verdict 자체 아님.

## 6. 회수 (a_fire_recover_complete · teardown 전 필수)

- PULL → `~/anima-weights/h1631_tpr_expert/` : `.clm` × N + `.pt` × N + `.json` × N
  + `*.log` + g_gates 측정 txt.
- HF = a_hf_autonomous: DIRECTIONAL/실험 → PRIVATE + CLM collection.
- 재현 = 이 trainer.py(`--arm {ctrl,tlora,tlora_dict,tlora_jamo}` + `--objective`).
- ckpt PULL 전 teardown 금지(JSON 만 받고 down = engine-check 영구 불가).
