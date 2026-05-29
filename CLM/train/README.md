# CLM P2 — custom QAT 트레이너

> CLM(conv-MoE byte LM, scratch from-zero)의 **실제 학습기**. dojo 가 뽑아준
> generic HF-Trainer 템플릿(`AutoModelForCausalLM`/`AutoTokenizer`/wikitext)은
> CLM 에 **틀려서** 버렸고, 여기는 byte conv-MoE 전용 custom QAT 트레이너다.
> 설계 SSOT = [P0_ARCHITECTURE.md](../P0_ARCHITECTURE.md) §9 (QAT) · d4/d5 ·
> [CLM_FORMAT_SPEC.md](../CLM_FORMAT_SPEC.md) §2 (.clm int4+fp16 shadow+QAT scale).

## 1. 무엇 / 왜 (dojo 템플릿과의 차이)

| 축 | dojo 템플릿 (버림) | 이 트레이너 (custom) |
|---|---|---|
| 모델 | `AutoModelForCausalLM.from_pretrained` | `CLMConvMoE` (CLM/model/model.py, landed) |
| 토크나이저 | `AutoTokenizer` | **없음** — byte-vocab V=256 (P0 Q3) |
| 데이터 | `load_dataset("wikitext")` | `.kosmos` @corpus (CLM/corpus/clm_p1) byte stream |
| 학습 | HF `Trainer` (fp) | **QAT 루프** — AKIDA int4 envelope 향해 (P0 §9) |
| router | 없음 | 3-arm 토글 A/B/AB (P0 §3) |
| scale | 단일 | scale-ladder tiny/small (P0 d3) |

dojo 의 **dispatch 글루**(`hexa cloud nohup` + d16 dry-run)는 재사용한다 —
`job.hexa` / `run.sh` 가 그 패턴을 페이로드만 바꿔 적응했다.

## 2. 파일

| 파일 | 역할 | 언어 |
|---|---|---|
| `train_clm.py` | 학습 **페이로드** — QAT forward/backward(STE)+CE+envelope 손실 | python(torch autograd) |
| `train_clm.hexa` | hexa-native **드라이버** (d5 1순위) — arm/rung 조립 + dry-run smoke + py 호출 | hexa |
| `job.hexa` | 단일 job background dispatch (`hexa cloud nohup` → poll/tail 힌트) | hexa |
| `run.sh` | run 글루 — `dryrun`/`local`/`fire` 서브커맨드 (dojo `.sh` 패턴) | bash |

> **왜 페이로드가 .py 인가**: QAT forward/backward(int4-sym STE + act_bits
> envelope STE)는 torch autograd 에 의존한다. P0 d5 는 "hexa-native 1순위"이고
> hexa 학습속도는 해결됐으나(2026-05-30), **hexa-native autograd(CLM forward+STE)가
> g1-pure 로 닫히기 전까지** payload 는 .py, driver 는 .hexa 로 dual-companion 한다.
> hexa autograd 닫히면 payload 를 `train_clm.hexa` 로 흡수(.py 은퇴)가 후속 목표.

## 3. QAT — "AKIDA 를 향해" 학습 (P0 §9)

학습 forward 가 AKIDA 배포 envelope 를 시뮬레이트해, 배포 시 naive PTQ int4
round-trip 파괴를 회피한다(학습이 이미 양자화된 도착지를 알고 수렴).

- **가중치**: symmetric int4 `[-7,+7]` per-output-channel (칩이 −8 거부 →
  two's-complement 아님). `scale_c = max|w_c| / 7`, blocks `qat_scale` 저장
  (CLM_FORMAT_SPEC §2/§3) → AKIDA 재계산 없이 로드.
- **활성**: `step = 2^(input_bits − act_bits)`,
  `y = clip(round(pot/step), 0, 2^act_bits − 1)`, `act_bits ∈ {1,2,4}`
  (act_bits=1 → LIF comparator 환원). `akida_sw_lif::fc_quantized_forward` 와
  동일 공식. **단, router(out=n_experts)·readout(out=V) conv 는 LOGIT 이라
  act-quant 제외** (softmax/CE 파괴 방지 — 정직 envelope: 활성만 양자화).
- **backward**: STE — quantize step 의 gradient 는 clip 범위 내 identity, 밖은 0.
  fp32 master weight 는 normal backprop 으로 갱신, forward 만 양자화.
- **손실**: next-byte CE (V=256) + MoE aux + (선택) envelope-정합 KL
  (`--envelope-lambda` — 양자화 logit ↔ fp shadow logit KL, PTQ 파괴를 학습신호로
  흡수). λ 는 P3 F-CLM-QUANT 임계 튜닝 대상.
- **경계(정직)**: QAT 는 GPU backprop 사용 — 칩 위 full-backprop 물리 불가
  (AKD1000=추론칩). on-chip 맥락적응은 **PLASTICITY** edge-learn 위임(QAT 와 직교).
  추론은 AKIDA-int4-only 불변.

## 4. 3-arm × scale-ladder (P0 §3·d3)

```
              tiny(d64/L2/E4)   small(d256/L4/E8)
   ARM A      A·tiny             A·small        entropy-reg (content축)
   ARM B      B·tiny             B·small        topK+load-bal (routing축)
   ARM A+B    AB·tiny            AB·small       dual-axis (untried prior art)
```
target rung(≤AKD1000 fit)은 P4 fit probe 확정 전엔 미정. toy=직관(non-gate),
판정은 full-fire(z>3.0 dual-axis · multi-seed{42,43,44}) — F-CLM-MONO(H_847).
**toy ≠ scale**(H_666): toy 결과로 prune 금지.

## 5. 실행

```bash
# (1) $0 local dry-run smoke — forward+QAT-loss+backward 1-step + step-rate
./run.sh dryrun AB tiny
#  또는 hexa-native 드라이버:  hexa run train_clm.hexa

# (2) $0 local toy 학습 (intuition only)
./run.sh local AB tiny 200
python3 train_clm.py --arm AB --rung tiny --steps 200 --act-bits 4

# (3) GPU pod full-fire (3-arm × ladder) — ⚠ cost-bearing, 다음 명시 step
./run.sh fire ubu-1     # hexa cloud nohup 으로 6 job background dispatch
#  발사 전 d16 free-pool dry-run:
#    pool on ubu-1 'cd ~/core/anima/CLM/train && python3 train_clm.py --dry-run'
```

인자: `--arm {A,B,AB}` · `--rung {tiny,small}` · `--steps N` ·
`--act-bits {1,2,4}` · `--envelope-lambda F` · `--corpus PATH` ·
`--dry-run` · `--json-out PATH` · `--seed N`.

## 6. dry-run smoke 실측 (P2, $0 local Mac CPU · torch 2.10.0)

p7 정직 — 돌면 돈다, 안 돌면 안 돈다고 그대로 보고. **forward + QAT-loss +
backward 1-step 정상 작동 확인**:

| arm | rung | params | first_ce | step_rate (step/s) |
|---|---|---|---|---|
| A  | tiny  | 120,132   | 5.572 | ~3.8 |
| B  | tiny  | 120,132   | 5.572 | ~6.4 |
| AB | tiny  | 120,132   | 5.572 | ~5.1 |
| AB | tiny (act_bits=1) | 120,132 | 5.572 | ~5.6 |
| AB | small | 2,695,176 | 5.768 | ~0.9 |

- first_ce ≈ ln(256)=5.545 = 무학습 byte-vocab 기대치(정상).
- **trainability 확인**: AB·tiny 100-step → CE 5.572 → 3.493 (gradient 가
  int4-sym weight STE + act_bits envelope 를 통과해 흐른다 — QAT 경로가 실제
  학습됨, non-erroring 만이 아님).
- step-rate 는 **Mac CPU·toy** 실측 — GPU pod 의 production scale-rate 아님.
  d5 "hexa/py trainer throughput 해결" 의 최종 확인은 GPU full-fire 의
  step-rate 재측정(다음 step).

## 7. 미완 (다음 step)

- **GPU 풀파이어** (`./run.sh fire`) = cost-bearing — 이번 run 미실행($0 only).
  F-CLM-MONO/F-CLM-SCALE 판정 + production step-rate 재측정은 그때.
- **.clm 직렬화** (P3) — int4 + fp16 shadow + qat_scale + manifest 저장은 미구현
  (이 트레이너는 학습 루프까지; .clm export 는 P3).
- **hexa-native payload 흡수** — torch autograd → hexa autograd 전환(g1-pure)은
  hexa autograd 닫힌 뒤 후속.
- **`.kosmos` emit 영속** — 학습 산출 emit/anchor 의 .kosmos 영속(a_kosmos)은
  추론/DECODER 통합(P5) 단계.

## 양방향 sibling

- [P0_ARCHITECTURE.md](../P0_ARCHITECTURE.md) · [CLM_FORMAT_SPEC.md](../CLM_FORMAT_SPEC.md) ·
  [CLM/model](../model/model.py) · [ENCODER/kosmos_corpus_io.hexa](../../ENCODER/kosmos_corpus_io.hexa)
- UNIVERSE: F-CLM-MONO = H_847 (CLM P0 Q4, NON-GATE toy) — 판정은 full-fire.
