# H_9845 — 개입형 폐쇄사다리를 학습 중 인과 모니터로 (R12-8 · MONITOR-ONLY · 손실 투입 금지)

**status:** 🔧 WIRED-INSTRUMENT · 🔻 **판별력 반증(2026-07-21 자가반박 · 아래 「실제 303M 스왑」 절)**
— 계기 배선·통제·손실-무관은 그대로 살아있으나, **토이 대신 실제 303M 을 행위 정책으로 꽂으면
모델 행이 자기 참값-0 받침대(C6)와 구별되지 않는다**(action_support 1 · CR 0.000 · closure 0.0000
= C6 와 동일). 이 계기로 303M 학습에 붙이는 후속 지출은 **차단**.
**source:** R12 뇌부위 census (2026-07-21) — `origin/main` `core/` 12개 모듈 실측 후 1모듈=1레버로 등록.
상위 설계 노드 = ARCHITECTURE `C2 RECOMBINE` 아래 `🧠 뇌부위 census` → `📋 R12`. R11(H_9830~9836)의 후속.
**wired:** yes — `anima-py train --closure-monitor rung1` (cli/train.py · VERSION 0.20.104→0.20.105 · G5).
**전제 검증:** `core/closure_ladder.py` = origin/main 에 **실재**(644줄 · `git ls-tree -r origin/main` 확인 후 전문 통독).
인용한 심볼 전부 실측 확인: `ACTIONS`·`observe`·`echo_guard`·`policy_live`·`make_tape_policy`·`digest_brain`·
`constant_brain`·`lv_c`·`lv_p`·`sample_digests`·`_derange`·`_frame_alignment_check`·`BLOCK`·`MIN_BLOCKS`·
`CLOSURE_SIGN`·`NULL_CLOSURE_MAX`. **철회한 전제 없음**(H_9832 의 stale-checkout 함정 재발 없음).

## 무엇을 배선했나

```
anima-py train --closure-monitor {off,rung1}
               [--closure-monitor-every N]        # 0 = 마지막 step 만
               [--closure-monitor-ticks 600]      # 스케줄당 세계 tick
               [--closure-monitor-seed 7]         # 첫 perturbation-SCHEDULE 시드
               [--closure-monitor-schedules 2]    # 스케줄 개수(≥2)
               [--closure-monitor-out J.jsonl]    # 로그 싱크
```

`off`(기본) ⟹ 골든패스 byte-identical. `rung1` 은 `core/closure_ladder.py`(H_9807)의 개입형
폐쇄사다리를 **살아있는 모델을 행위 정책으로 꽂아** 돌린다. 모델은 바이트 LM 이므로 행동은
**샘플링이 아니라 채점**으로 읽는다 — 8개 행동을 digest 뒤에 붙여 teacher-forcing 하고
**자기 바이트 구간**의 평균 NLL 최소를 고른다(동점=ACTIONS 순서 ⟹ 결정론). 결정 1회 = batch 8 forward 1회.

## ⛔ 손실 무관 — 이 카드의 본체 (a_train_inline_gauge)

구조적 보장: ① `opt.step()` **뒤에** rank-0 에서만 실행 ② `torch.no_grad()` 안 ③ 진입 시
torch(및 CUDA) RNG state 를 스냅샷하고 `finally` 에서 복원, `model.training` 복원 ④ 반환값은 plain dict 이며
호출부는 **print / JSONL append 밖에 하지 않는다** ⑤ 예외는 삼켜서 학습을 죽이지 않는다(train-py-1).

### 실측 — 켠 것과 끈 것의 학습 궤적이 byte-identical

```
$ python3 -m venv /tmp/venv_h9845 && /tmp/venv_h9845/bin/pip install -q --force-reinstall --no-deps .
$ anima-py train --seed 7 --steps 12 --d 32 --L 2 --seq-len 96 --batch-size 4 --device cpu \
      --log-every 1 --out /tmp/h9845_proof/A/m.clm --ckpt-out /tmp/h9845_proof/A/m.pt          # OFF
$ anima-py train --seed 7 --steps 12 --d 32 --L 2 --seq-len 96 --batch-size 4 --device cpu \
      --log-every 1 --out /tmp/h9845_proof/B/m.clm --ckpt-out /tmp/h9845_proof/B/m.pt \
      --closure-monitor rung1 --closure-monitor-every 4                                        # ON (step 4·8·12)
$ diff A.steps B.steps && echo "PER-STEP CE TRAJECTORY: byte-identical (12/12 lines)"
PER-STEP CE TRAJECTORY: byte-identical (12/12 lines)
  step     1  CE=5.68199  E=2  wd=0.0500 dp=0.5000  val_CE=nan
  step     2  CE=5.66415  E=2  wd=0.0469 dp=0.4693
  step     3  CE=5.61608  E=2  wd=0.0439 dp=0.4386
  step     4  CE=5.58122  E=2  wd=0.0408 dp=0.4079
  step     5  CE=5.51222  E=2  wd=0.0377 dp=0.3772
  step 6 (MITOSIS SPLIT) E 2->3
  step     6  CE=5.52747  E=3  wd=0.0347 dp=0.3465
  step     7  CE=5.48926  E=3  wd=0.0316 dp=0.3158
  step     8  CE=5.47943  E=3  wd=0.0285 dp=0.2851
  step     9  CE=5.42597  E=3  wd=0.0254 dp=0.2544
  step    10  CE=5.37269  E=3  wd=0.0224 dp=0.2237
  step    11  CE=5.32957  E=3  wd=0.0193 dp=0.1930
  step    12  CE=5.30600  E=3  wd=0.0162 dp=0.1623  val_CE=nan

$ shasum -a 256 A/m.clm B/m.clm A/m.pt B/m.pt
4d221f251c04219aacced555bc04bc82dfb4490183946d63f91bc1fda9931029  A/m.clm
4d221f251c04219aacced555bc04bc82dfb4490183946d63f91bc1fda9931029  B/m.clm
bb7ed7312316d571080db17d8849a4ca0d7ec3c5fdd632abf65cfbd38c84d634  A/m.pt
bb7ed7312316d571080db17d8849a4ca0d7ec3c5fdd632abf65cfbd38c84d634  B/m.pt
```

dropout 이 살아있고(dp 0.50→0.16) MITOSIS split 이 step 6 에 발화하는 궤적에서, 모니터가 step 4·8·12
세 번 발화했는데도 **12/12 CE 줄 · `.clm` sha256 · `.pt` sha256 이 전부 일치**한다.
(첫 시도에서는 `.pt` sha 만 달랐다 — 원인은 `torch.save` zip 내부 아카이브 이름이 출력 파일명(`off`/`on`)에서
오는 것이었고, 텐서 23/23 은 그때도 `torch.equal` 로 bit-identical 이었다. 동일 basename 으로 재실행해 해소.)

**이 비교에 이빨이 있는지도 통제했다**(비교 자체의 양성통제): 같은 diff 에 `--seed 8` 을 넣으면
step 1 부터 CE 가 갈린다 ⟹ `DISCRIMINATOR OK — a real perturbation DOES move the same diff`.
⚠️ 정직: 모니터는 `model.eval()` + 채점 readout 이라 **애초에 RNG 를 소비하지 않는다**. RNG 저장/복원은
"미래에 샘플링하는 모니터 코드가 들어와도 궤적을 못 건드린다"는 안전벨트이지, 이번 등식의 유일한 근거가 아니다.

## 통제 — 순서 동결 · 6개 전부 통과해야 모델 행을 보고한다

`run_mi_screen`(H_9844) 패턴 그대로: 통제가 먼저, 인증 못 하면 처치 행 **미보고**.

| | 통제 | 통과 조건 |
|---|---|---|
| C1 | LV-E echo guard | 관측 어휘에 행동 이름이 없음(에코 함정 차단) |
| C2 | frame alignment | H_013 회귀 테스트(오정렬 시 죽은 세계서 0.667 을 읽었던 그 결함) |
| C3 | **양성통제** — 스크립트 contingent plant | 그 tick 예산에서 closure ≥ 0.60 ∧ digest-brain CR ≥ 0.20 ∧ replay_agree = 1.0 |
| C4 | **참값 0 PEDESTAL** — INERT 세계 + 입력맹 brain | closure ≤ 0.05 ∧ blind CR = 0 |
| C5 | **경로 양성통제** — digest-READING brain 을 모델과 **같은 코드경로**로 | anchors(closure ≥ 0.60 ∧ closure > yoked floor) |
| C6 | 경로 pedestal — 입력맹 brain 을 같은 경로로 | closure ≤ 0.05 |

C3 는 **추정기**를, C5 는 **경로**를 인증한다. C5 없이는 모델의 NO-ANCHOR 가 "모델이 그런가"인지
"이 파이프로는 brain 을 못 읽나"인지 구분되지 않는다.

### 실측 (toy 12-step CLM d=32 L=2 · 600 ticks · schedules {7,8})

```
step 12  read=NO-ANCHOR  span_ok=True
 seed7 CERTIFIED blocks=12 | C1 echo=True C2 frame=True | C3 plant closure=0.7500 CR=0.50 fires=True
        | C4 inert closure=0.0000 blindCR=0.00 | C5 pathway closure=0.7500 floor=0.5500 anchors=True
        | C6 pathwayPed closure=0.0000
    MODEL closure=0.0000 floor_mean=0.0000 draws=[0.0,0.0,0.0,0.0,0.0] delta=0.0000 CR=0.00 support=1 anchors=False
 seed8 CERTIFIED blocks=12 | C3 plant closure=0.9167 CR=0.50 fires=True | C4 inert 0.0000 / 0.00
        | C5 pathway closure=0.9167 floor=0.4167 anchors=True | C6 pathwayPed closure=0.0000
    MODEL closure=0.0000 floor_mean=0.0000 draws=[0.0,0.0,0.0,0.0,0.0] delta=0.0000 CR=0.00 support=1 anchors=False
```

읽기: 통제 6/6 이 두 스케줄 모두에서 인증했고, **12-step 미학습 토이 모델은 NO-ANCHOR**
(`action_support=1` — 모든 digest 에 같은 행동을 낸다 = 행동상 C6 입력맹 pedestal 과 동일).
이건 계기가 살아있다는 증거지 모델에 대한 과학 판정이 아니다(토이·미학습).

또 하나의 계기 자가점검(train-py-9): 채점 구간 위치 수를 매번 세서 보고한다 —
`scored_positions=[4,4,4,7,4,5,5,4] == expected_positions` ⟹ `span_ok=true`. 오조준이면 `read=REFUSED`.

## no tune-to-green — 스스로 적발한 결함 2건

1. **tick 예산이 판정을 고를 수 있었다.** 200 ticks(4 블록)에서 C3 양성통제가 발화하지 않는다
   (`plant closure 0.500 < 0.60`). 초판은 이걸 INSTRUMENT-DEAD 로 읽을 수 있었다. 교정: 리그 자신의
   `MIN_BLOCKS=12` 교리를 따라 블록 부족이면 **UNDER-POWERED** 로 분류하고
   `raise --closure-monitor-ticks to >= 600` 를 출력한다(power-before-negative-verdict).
   실측 출력: `"status": "UNDER-POWERED" … "the scripted contingent plant did NOT fire at 200 ticks (4 blocks; closure 0.500 vs gate 0.60)"`.
2. **yoked floor 를 한 번만 뽑으면 derangement 인덱스가 부호를 고른다.** seed 7 · 600 ticks 에서
   scripted digest-brain 의 open floor 가 draw k=9 는 0.7500, k=3 은 0.5000 — treatment(0.7500) 대비
   delta 부호가 draw 하나로 뒤집힌다. 교정: floor 를 **5개 derangement(3,5,9,11,13)의 평균**으로 잡고
   per-draw [min,max] 를 전량 보고, 더 강한 읽기는 `derangement_robust`(최악 draw 초과)로 별도 표기.
   **max 를 게이트로 쓰지 않는다** — Δ=exp−max(controls) 는 순서통계 편향으로 KILL 을 기계화한다
   (probe-defect-census-max-control-bias). 실측 seed7 draws `[0.5,0.5,0.75,0.583,0.417]` → mean 0.5500.

## 재현 — `--closure-monitor-seed` 재실행은 재현이 **아니다**

do()-개입이 결정론적이고 입력이 항정이며 readout 이 greedy(argmin)이라, 같은 스케줄을 다시 돌리면
트레이스가 byte-identical 이므로 **아무것도 증명하지 않는다**
(`sample-seed-invalid-for-deterministic-do-intervention`). 진짜 재현 = **perturbation-SCHEDULE 변형**이고,
그래서 `--closure-monitor-schedules` 기본값이 2 이며 헤드라인 `read` 는 스케줄 **합의**다:
`ANCHOR-ALL-SCHEDULES` / `SCHEDULE-SPLIT` / `NO-ANCHOR` / `REFUSED`.

## 판정 · 범위

- **과학 판정 0.** 이번 착륙은 계기 배선 + 손실-무관 증명 + 통제 인증뿐이다. 실측된 모델 수치는
  미학습 토이 1건(NO-ANCHOR)이며 어떤 lane 인과성 주장도 여기서 나오지 않는다.
- ⚠️ **rung 1 은 온도조절기도 통과한다.** 어떤 의식·생명·내면 주장도 이 플래그에서 도출 금지.
  진단 대상은 오직 "이 정책이 자기 입력에 지문을 남기는가"(lane causality) 한 가지다.
- ⚠️ C5 경로 양성통제는 측정 대상보다 **쉬운 과제**다(train-py-10): 판독가능성을 사주지 예산 적정성을
  증명하지 않는다. 학습된 모델에서 음성이 나와도 "그 예산에서 그 과제가 학습가능한가"는 별도 문제.
- ⚠️ 세계는 `closure_ladder` 의 micro-tenant 토이다. 여기서의 ANCHOR 는 **그 세계에서의** 폐쇄이며
  자연어 능력·G1/G6 벽과 자동으로 연결되지 않는다(`a_scale_honest_scope`).
- 비용: 스케줄당 `ticks` 회 모델 forward(batch 8) + 파이썬 tick 계산 ~2s. 기본 600×2 = 1,200 forward.
  303M 에 붙일 때는 `--closure-monitor-every` 를 크게 잡을 것.

---

# 🔻 심화 (2026-07-21 · 같은 날 자가반박) — 토이를 실제 303M 으로 바꾸면 모델 행이 받침대와 겹친다

## 왜 이 스왑을 했나 — H_9838 의 planted-geometry 실패

같은 R12 배치의 H_9838 은 **인증되고, 양성통제와 참값-0 받침대를 갖고, 3 seed × 3 기하를 쓸고,
독립 재현까지 된** 헤드라인 양성(CA3 다단계 전이완성 · 유도우연의 12배 · 절제하면 바닥)을 착륙시켰다.
그 뒤 **코드 출처만** planted 정수 fixture → 생산 trunk 의 실제 penultimate 로 바꾸자
(팔·통제·바 전부 불변) 16항목 부하가 CERTIFIED → **INVALID** 로 뒤집혔다 — 값-셔플 참값-0 받침대가
0.3750 으로 바 0.3077 을 넘겼다. 즉 답은 기전이 아니라 **손으로 만든 유리한 기하**에서 나오고 있었다
(planted 코드 within .0469 / across .0117 = 사실상 직교 · 실제 표현은 .0625 / .0260 로 2.2배 겹침,
그리고 `core/hippo_lane.py` 헤더가 이미 "Raw single-token 303M reps are near-collinear" 라고 경고).

H_9845 는 **같은 결함 계급**에 있었다. 위 실측의 행위 브레인은 전부 **d32 · L2 · 12-step 토이**이고,
`core/closure_ladder.py` 헤더 자신이 "**온도조절기도 rung 1 을 통과한다**"라고 적어 놓았다.
그래서 동일한 스왑을 걸었다 — **행위 정책의 입력 출처만** 교체.

## 무엇을 배선했나 (b: 실입력 플래그)

```
anima-py train --closure-monitor rung1 --closure-brain <real.clm>
```

`cli/train.py::_closure_clm_brain` — 행위 정책이 `core/decode.clm_load_weights` +
`clm_forward_hidden_logits` 로 읽는 **실제 직렬화 `.clm`** (py-canonical 측정 경로 ·
`a_eval_py_canonical`). 채점 계약은 문자 단위로 동일: 8개 행동을 `digest + " => "` 뒤에 붙여
teacher-forcing, **자기 바이트 구간** 평균 NLL 최소, 동점=`ACTIONS` 순서. 바뀐 것은 로짓을 내는
엔진뿐이며 **그것이 스왑의 전부**다. 통제 6개 · 바(`CLOSURE_SIGN` 0.60 · `NULL_CLOSURE_MAX` 0.05 ·
`MIN_BLOCKS` 12) · tick 예산 600 · 스케줄 수 2 — **하나도 건드리지 않았다**(바를 옮기면 비교가 죽는다).
`--closure-brain ''`(기본) ⟹ 착륙 경로 byte-identical.

`_closure_arm` 에 **읽기 전용 텔레메트리** `action_hist`(실행 행동 히스토그램) 1개를 추가했다.
게이트·임계·팔이 이 값을 읽지 않으며, 아래에서 옛 경로 수치가 이것 포함 전후로 동일함을 보인다.
`action_support` 만으로는 "이 정책이 입력을 안 읽는다" 와 "byte-LM NLL 채점이 길이/사전 편향이다"를
구분할 수 없어서 필요했다.

## ① 옛 경로 회귀 — 무회귀(카드 수치와 동일)

```
$ python3 -m venv /tmp/venv_h9845r && /tmp/venv_h9845r/bin/pip install -q numpy torch
$ /tmp/venv_h9845r/bin/pip install -q --force-reinstall --no-deps .
$ /tmp/venv_h9845r/bin/anima-py train --seed 7 --steps 12 --d 32 --L 2 --seq-len 96 \
      --batch-size 4 --device cpu --log-every 1 \
      --out /tmp/h9845b/OLD2/m.clm --ckpt-out /tmp/h9845b/OLD2/m.pt \
      --closure-monitor rung1 --closure-monitor-out /tmp/h9845b/OLD2/cm.jsonl

read=NO-ANCHOR  brain_source=live-training-model  step=12
geometry={'ticks': 600, 'seed0': 7, 'schedules': 2, 'block': 50, 'min_blocks': 12,
          'closure_gate': 0.6, 'null_max': 0.05}
readout_span={'scored_positions': [4,4,4,7,4,5,5,4], 'expected_positions': [4,4,4,7,4,5,5,4],
              'span_ok': True, 'truncated': False}
 seed7 CERTIFIED blocks=12 | C1 echo=True C2 frame=True | C3 plant closure=0.7500 CR=0.50
       replay=1.00 fires=True | C4 inert closure=0.0000 blindCR=0.00 refuses=True
       | C5 pathway closure=0.7500 floor=0.5500 draws=[0.5,0.5,0.75,0.5833,0.4167] anchors=True support=6
       | C6 pathwayPed closure=0.0000 support=1 hist={'NOOP': 600}
   MODEL closure=0.0000 floor_mean=0.0000 draws=[0.0,0.0,0.0,0.0,0.0] delta=0.0000 CR=0.00
         replay=1.00 support=1 anchors=False hist={'REST': 600}
 seed8 CERTIFIED blocks=12 | C1 echo=True C2 frame=True | C3 plant closure=0.9167 CR=0.50
       replay=1.00 fires=True | C4 inert closure=0.0000 blindCR=0.00 refuses=True
       | C5 pathway closure=0.9167 floor=0.4167 draws=[0.5,0.4167,0.3333,0.5,0.3333] anchors=True support=5
       | C6 pathwayPed closure=0.0000 support=1 hist={'NOOP': 600}
   MODEL closure=0.0000 floor_mean=0.0000 draws=[0.0,0.0,0.0,0.0,0.0] delta=0.0000 CR=0.00
         replay=1.00 support=1 anchors=False hist={'REST': 600}

OLD (텔레메트리 이전) vs OLD2 (이후), 새 키 제거 후 동일: True
```

위 블록의 모든 수치가 **이 카드 상단 「실측」 표와 글자 그대로 일치**한다(0.7500/0.50 · 0.0000/0.00 ·
0.7500 vs 0.5500 · 0.9167 vs 0.4167 · MODEL 0.0000·support 1 · `scored_positions` 8칸).
⟹ **ZERO REGRESSION**.

## ② 실입력 경로 — 실제 303M 2개 ckpt

```
$ /tmp/venv_h9845r/bin/anima-py train --seed 7 --steps 12 --d 32 --L 2 --seq-len 96 \
      --batch-size 4 --device cpu --log-every 1 \
      --out /tmp/h9845b/REAL2/m.clm --ckpt-out /tmp/h9845b/REAL2/m.pt \
      --closure-monitor rung1 --closure-monitor-out /tmp/h9845b/REAL2/cm.jsonl \
      --closure-brain /Users/mini/anima-weights/py303_full.clm
  # 재현(2번째 실제 ckpt): --closure-brain /Users/mini/anima-weights/py303_savant_mitosis.clm

=== REAL2 (py303_full.clm) ===
 read=NO-ANCHOR  brain_source=real-clm:/Users/mini/anima-weights/py303_full.clm  step=12
 geometry={'ticks': 600, 'seed0': 7, 'schedules': 2, 'block': 50, 'min_blocks': 12,
           'closure_gate': 0.6, 'null_max': 0.05}
 readout_span={'scored_positions': [4,4,4,7,4,5,5,4], 'expected_positions': [4,4,4,7,4,5,5,4],
               'span_ok': True, 'truncated': False}
 seed7 CERTIFIED blocks=12 | C1 echo=True C2 frame=True | C3 plant closure=0.7500 CR=0.50
       replay=1.00 fires=True | C4 inert closure=0.0000 blindCR=0.00 refuses=True
       | C5 pathway closure=0.7500 floor=0.5500 draws=[0.5,0.5,0.75,0.5833,0.4167] anchors=True support=6
       | C6 pathwayPed closure=0.0000 support=1 hist={'NOOP': 600}
   MODEL closure=0.0000 floor_mean=0.0000 draws=[0.0,0.0,0.0,0.0,0.0] delta=0.0000 CR=0.00
         replay=1.00 support=1 anchors=False hist={'COMPACT': 600}
 seed8 CERTIFIED blocks=12 | C1 echo=True C2 frame=True | C3 plant closure=0.9167 CR=0.50
       replay=1.00 fires=True | C4 inert closure=0.0000 blindCR=0.00 refuses=True
       | C5 pathway closure=0.9167 floor=0.4167 draws=[0.5,0.4167,0.3333,0.5,0.3333] anchors=True support=5
       | C6 pathwayPed closure=0.0000 support=1 hist={'NOOP': 600}
   MODEL closure=0.0000 floor_mean=0.0000 draws=[0.0,0.0,0.0,0.0,0.0] delta=0.0000 CR=0.00
         replay=1.00 support=1 anchors=False hist={'COMPACT': 600}

=== REAL3 (py303_savant_mitosis.clm) ===
 read=NO-ANCHOR  brain_source=real-clm:/Users/mini/anima-weights/py303_savant_mitosis.clm  step=12
 (통제 6/6 · 두 스케줄 모두 REAL2 와 글자 그대로 동일 — 통제는 모델 독립이라 그래야 한다)
   seed7 MODEL closure=0.0000 floor_mean=0.0000 draws=[0.0,0.0,0.0,0.0,0.0] delta=0.0000
         CR=0.00 replay=1.00 support=1 anchors=False hist={'COMPACT': 600}
   seed8 MODEL closure=0.0000 floor_mean=0.0000 draws=[0.0,0.0,0.0,0.0,0.0] delta=0.0000
         CR=0.00 replay=1.00 support=1 anchors=False hist={'COMPACT': 600}
```

## ③ 손실-무관 재증명 (모니터 코드를 건드렸으므로 다시 증명)

```
$ sh lossfree.sh    # A=OFF · B=ON(토이 브레인) · C=ON(실제 303M 브레인) · --closure-monitor-every 4
A(OFF) vs B(ON,toy-brain):        byte-identical
A(OFF) vs C(ON,REAL-303M-brain):  byte-identical
4d221f251c04219aacced555bc04bc82dfb4490183946d63f91bc1fda9931029  A/m.clm
4d221f251c04219aacced555bc04bc82dfb4490183946d63f91bc1fda9931029  B/m.clm
4d221f251c04219aacced555bc04bc82dfb4490183946d63f91bc1fda9931029  C/m.clm
bb7ed7312316d571080db17d8849a4ca0d7ec3c5fdd632abf65cfbd38c84d634  A/m.pt
bb7ed7312316d571080db17d8849a4ca0d7ec3c5fdd632abf65cfbd38c84d634  B/m.pt
bb7ed7312316d571080db17d8849a4ca0d7ec3c5fdd632abf65cfbd38c84d634  C/m.pt
```

두 sha256 은 **이 카드 상단 착륙 증거의 값과 동일**하다 ⟹ 새 플래그는 손실-무관을 깨지 않았고,
실제 303M 브레인을 꽂아도 학습 궤적은 그대로다.

## 정직한 판정 — 무엇이 살아남고 무엇이 죽었나

| | 착륙 때 주장 | 실입력 스왑 후 |
|---|---|---|
| 배선 · 6 통제 인증 | ✅ | ✅ **그대로** — 단, 아래 ⚠️ 참조 |
| 손실-무관(byte-identical) | ✅ | ✅ **그대로**(sha 동일) |
| 모델 행의 **판독 가능성** | "토이라서 NO-ANCHOR" | 🔻 **반증** — 실제 303M 도 동일하게 붕괴 |

- ⚠️ **통제 6/6 이 "실제 브레인에서도 인증"된 것은 승리가 아니다.** C1~C6 은 `_closure_schedule`
  안에서 `seed`·`ticks` 만의 함수이고 `brain` 을 전혀 통과시키지 않는다(스크립트 brain 만 쓴다).
  즉 **구성상 모델 독립**이라 값이 같을 수밖에 없다. 이 스왑이 드러낸 첫 사실이 그것이다.
- 🔻 **핵심 반증.** 실제 303M 은 두 ckpt · 두 스케줄 · 600 tick 전부에서
  **`action_support = 1`(COMPACT × 600) · `CR = 0.000` · `closure = 0.0000` · yoked floor = 0.0000
  · delta = 0.0000** — 즉 **자기 참값-0 받침대 C6(입력맹 brain, NOOP × 600)과 수치상 완전히 동일**하다.
  이건 "모델의 우연성 구조가 자기 입력에 지문을 안 남긴다"가 아니라 **"이 채점 readout 을 통과한
  모델에는 우연성 구조 자체가 없다"** — 모델 행이 폐쇄에 관한 문장으로 읽히지 않는다.
- 🔻 따라서 착륙 카드가 "이건 계기가 살아있다는 증거지 모델 판정이 아니다(**토이·미학습**)"라고
  적으며 암묵적으로 깔았던 전제 — *학습된 실제 모델이면 달라진다* — 는 **틀렸다**.
  rung 1 모니터는 **303M 과 12-step d32 토이를 구별하지 못한다**(둘 다 support 1, 둘 다 C6 위에 포갬).
- 🔎 **자가적발한 계기 결함(패치하지 않았다 — 바를 움직이는 게 되므로).** `_closure_schedule` 은
  모델 행이 C6 받침대와 행동상 동일해도 **REFUSED 하지 않고 CERTIFIED/NO-ANCHOR 로 보고한다.**
  받침대와 구별 불가능한 처치 행을 판정으로 내보내는 것은 H_9838 이 데인 바로 그 실패다.
- 🔎 **누락된 통제의 정체.** C5 「경로 양성통제」는 스크립트 `digest_brain` 을 쓰므로 **byte-LM NLL
  채점 readout 을 한 번도 지나가지 않는다**. 즉 이 리그에는 **readout 자체에 대한 양성통제가 없다**.
  `action_hist` 는 실제 303M 이 8개 중 **유일한 7바이트 행동 COMPACT** 에 고정됐음을 보여준다(토이는
  4바이트 REST). 자기 바이트 평균 NLL 은 긴 행동일수록 뒤 바이트가 예측가능해 유리해질 수 있어
  **길이/사전 편향 의심**이 정면으로 살아있고, 그것을 배제할 통제가 리그에 존재하지 않는다.
- ⚠️ **어느 쪽으로도 의식·생명·내면 주장 금지.** rung 1 은 온도조절기가 통과하는 낮은 바이며,
  여기서 나온 것은 계기 판독 사실뿐이다. 특히 이 음성은 **"303M 에 폐쇄가 없다"가 아니다** —
  "이 readout 을 통과시키면 303M 이 상수 정책이 된다"이다.

## 범위 축소 · 차단되는 하류 지출

- **범위 축소:** H_9845 는 이제 **「손실-무관이 실증된 학습-시간 모니터 배관」** 까지만이다.
  모델 행(`read` = ANCHOR/NO-ANCHOR/SCHEDULE-SPLIT)은 **readout 이 실제 가중치에서 비퇴화 정책을
  낸다는 것이 따로 증명되기 전까지 판독 불가**로 표시한다. 착륙 카드의 토이 NO-ANCHOR 도
  "미학습이라서"로 읽어서는 안 된다(실제 303M 도 같은 자리에 있으므로 구별력이 없다).
- **차단되는 지출 ①** 착륙 카드가 계획으로 적었던 "303M 에 붙일 때는 `--closure-monitor-every` 를
  크게 잡을 것" — **GPU 303M 학습 런에 이 모니터를 붙이는 것은 지금 차단.** 붙여봐야 매 tick
  자기 받침대와 동일한 상수 행을 로깅한다(스케줄당 600×8 forward 를 태우면서).
- **차단되는 지출 ②** 이 모니터를 lane 인과성 판정기로 쓰는 모든 후속(ablation-retrain 대체 목적)
  — 판별력이 미증명이므로 여기 기대어 lane 을 살리거나 죽이는 결정 금지.
- **살아있는 것:** `--closure-monitor off`(기본) 골든패스, 손실-무관 보증, 6 통제 배터리 자체,
  그리고 `--closure-brain` 스왑 계기(=이 반증을 만든 도구).

## 사전등록 후속(설명만 · 이번에 실행하지 않음 — tune-to-green 금지)

받침대가 거부할 때까지 dim/seed/임계를 뒤지는 것은 금지이므로, 아래는 **별도 H 로 사전등록**한다.

- **H-후속 A — readout 양성통제.** 리그가 아니라 **채점기**에 양성통제를 건다: `digest_brain` 의
  정답 행동을 digest 뒤에 심은 코퍼스로 미세조정한 소형 ckpt(=심어둔 우연성)를 `--closure-brain`
  으로 넣어 **`action_support > 1` ∧ `CR ≥ 0.20`** 이 나오는지 본다. 안 나오면 채점기가 죽은 것이고
  모든 모델 행은 영구 판독 불가.
- **H-후속 B — 길이/사전 편향 격리.** `ACTIONS` 를 **길이 균등**(전부 같은 바이트 수)으로 다시 짠
  frozen 변형으로 A 를 반복. COMPACT 고정이 사라지면 원인은 채점기의 길이 편향, 남으면 정책 붕괴.
- **H-후속 C — 받침대 동일성 거부 규칙.** 모델 행이 C6 와 (support, closure, floor, CR) 전부
  일치하면 `read="REFUSED-PEDESTAL-DEGENERATE"` 로 강등. **바 이동이 아니라 새 거부 조건**이므로
  사전등록 후 별도로 착륙시킨다.

**related:** H_9805 · H_9807 · H_9835 · H_9838 · H_9844 · H_9846
