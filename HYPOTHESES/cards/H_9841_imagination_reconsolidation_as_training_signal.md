# H_9841 — 상상 재응고(reconsolidation)를 학습 신호로 — 이미 데몬에 배선된 성장 훅을 학습으로 (R12-4)

**status:** 🟡 WIRED · INSTRUMENT-CERTIFIED (판정 아님 — 학습 결과 없음)
**source:** R12 뇌부위 census (2026-07-21). 상위 설계 노드 = ARCHITECTURE `C2 RECOMBINE` 아래 `🧠 뇌부위 census` → `📋 R12`.
**wired:** yes — `anima-py train --imagination-replay …` (cli/train.py). $0 자가인증 배터리 동봉.
**scope ceiling:** DIRECTIONAL. 계기 인증 + 레인 배선까지. **학습 판정 아님**(303M 미발사 · 토이 CPU e2e 만).

---

## ① 전제 검증 — 카드가 인용한 문장은 origin/main 에서 참인가 (FIRST TASK)

**참이다. 실측 확인 — 철회할 전제 없음.**

`core/imagination_replay.py` 헤더의 주장 — "The REAL AdaptField growth is WIRED daemon-side
(2026-07-10): cli/chat.py + cli/anima.hexa advance a live vadapt_field_step per replay tick" —
을 `git grep origin/main` 으로 직접 확인했다.

| 확인 대상 | origin/main 위치 | 결과 |
|---|---|---|
| N3/REM 재생 루프 | `cli/chat.py:3350-3380` | ✅ `dr_imagination_active(stage)==1` 게이트 |
| `ir_select_snapshots` → `ir_replay_tick` | `cli/chat.py:3353,3361` | ✅ 실제 core 함수 호출 |
| **살아있는 성장 훅** | `cli/chat.py:3375` `afield = vadapt_field_step(afield, _h1058_imag_feat, cfg)` | ✅ 존재 |
| 훅 lesion 플래그(데몬측) | `cli/chat.py:1570` `--imag-growth`, `:3374` `if _imag_growth != "off"` | ✅ 이미 있음 (H_9790 A_off) |
| `vadapt_field_step` 실체 | `core/engine_cli.py:418` | ✅ torch-free · SPLIT_THRESH 0.30 · LR 0.20 |
| `ir_mitosis_tick_during_replay` = 로그뿐 | `core/imagination_replay.py` `"wired_to_lib": False` | ✅ 헤더 주장대로 |
| **학습측 대응물** | `cli/train.py` (origin/main) | ❌ **부재** — 이 카드가 메운 구멍 |

⟹ 데몬은 재생 틱마다 자란다. 학습은 자라지 않았다. 그것이 p8(학습/추론 분리 금지) 위반의
가장 구체적인 사례이며, 이 카드가 배선한 것이다. (H_9832 가 죽은 유형 — 삭제된 모듈 인용 — 은 없음.)

---

## ② 배선한 것 — `anima-py train` 플래그 (cli/train.py)

```
anima-py train --imagination-replay R           # 0.0 = OFF (byte-identical golden path)
               [--reconsolidate-every N]        # N3/REM 위상 주기 (기본 50)
               [--vadapt-on-replay]             # 데몬의 그 성장 훅을 학습에서 발사
               [--imagination-select recency|random]
               [--imagination-selftest]         # $0 인증 배터리 실행 후 종료
```

동작(단일 forward · shape 보존 · DDP-safe · rank-local):

1. 매 step, 트레이너가 **실제로 본 창**(`x‖y` 행 그대로 — 재구성 근사 아님)을 데몬의 그
   WAKE 작업링(`core/wake_memory.mem_push_ctx`, cap 20 FIFO)에 push.
2. `--reconsolidate-every N` 마다 N3/REM 위상: `ir_select_snapshots` 로 스냅샷 선택 →
   각각 `ir_replay_tick` (**p5 INVARIANT WATCH**: `emit_count>0` 이면 프로세스 즉시 hard-exit)
   → `--vadapt-on-replay` 면 `vadapt_field_step` 발사 → 리허설된 행이 **그 수만큼의 fresh 행을
   대체**한다.
3. **훅을 인과로 만드는 유일한 변수 = `density`.**
   훅 ON → `dr_density(splits, ticks)` (리허설이 *실제로 일으킨* 성장)
   훅 OFF → 고정 N3 prior `dr_mitosis_prior(3)` = 0.80 (`ir_mitosis_tick_during_replay` 가 기록하는 그 상수)
   dose = `round(ir_consolidation_gain(n, density) × n)` 행.
   ⟹ 성장이 0인 리허설은 **0행을 재학습한다**. 훅 OFF 는 약한 처치가 아니라 진짜 통제다.

`a_train_inline_gauge` 준수: consolidation gain 은 **스케줄**(재생 수 + 성장 밀도의 함수)이지
모델 품질 게이지가 아니다 — loss/CE/logit/val 어느 것도 여기 들어가지 않는다.
`ir_effective_age` 는 **MONITOR-ONLY** 로만 출력한다.

인용 함수는 전부 실제 production 함수(`a_experiment_engine_native`): `core/imagination_replay.py`
`core/wake_memory.py` `core/dream_lib.py` `core/engine_cli.py`. 재구현 0.

---

## ③ 재현 명령 (실행한 그대로)

```bash
python3 -m venv /tmp/venv_h9841
/tmp/venv_h9841/bin/pip install -q --force-reinstall --no-deps .

# (A) $0 인증 배터리 — 모델·코퍼스·GPU 없음
/tmp/venv_h9841/bin/anima-py train --imagination-selftest \
    --imagination-replay 0.5 --vadapt-on-replay

# (B) 실학습 e2e (CPU · 토이) — 훅 ON
/tmp/venv_h9841/bin/anima-py train --corpus /tmp/h9841_corpus.txt --out /tmp/f_on.clm \
    --d 64 --L 2 --steps 30 --seq-len 32 --batch-size 32 --e0 2 --emax 2 --lr 3e-4 \
    --device cpu --log-every 10 --val-every 30 --skip-inline-rho \
    --imagination-replay 0.5 --reconsolidate-every 10 --vadapt-on-replay
#   훅 OFF 통제 = 같은 명령에서 --vadapt-on-replay 만 제거
#   골든패스 = --imagination-replay 를 아예 빼거나 0.0
```

---

## ④ 실측 (A: $0 배터리 · exit 0 · **CERTIFIED**) — 통제 먼저, 순서 동결

**⓪ p5 감시자 자체의 양성통제** — 한 번도 발화를 본 적 없는 감시자의 "위반 0" 은 무의미하므로,
`emit_count=1` 을 **심어서** 감시자가 실제로 죽는지 먼저 확인한다:

```
p5_watch_control = {'planted_violation_detected': True, 'silent_tick_passes': True}
```

**①②③ 통제 행렬** (3 기하 × 2 seed · seed 는 rng 가 아니라 **심은 내용**을 바꾼다):

```
ring win budget seed below_floor fires refuses | PLANT splits cells dens    c      rows | FLAT splits dens   c      rows | EMPTY snaps c
 20   32    8     7    False     True   True   |       4      5   0.5000  0.1492   1    |    0     0.0000 0.0000   0    |    0    0.0000
 20   32    8    11    False     True   True   |       4      5   0.5000  0.1492   1    |    0     0.0000 0.0000   0    |    0    0.0000
  8   16    3     7    True      True   True   |       2      3   0.6667  0.0779   0    |    0     0.0000 0.0000   0    |    0    0.0000
  8   16    3    11    True      True   True   |       2      3   0.6667  0.0779   0    |    0     0.0000 0.0000   0    |    0    0.0000
 20   64    5     7    False     True   True   |       3      4   0.6000  0.1144   1    |    0     0.0000 0.0000   0    |    0    0.0000
 20   64    5    11    False     True   True   |       4      5   0.8000  0.1501   1    |    0     0.0000 0.0000   0    |    0    0.0000

STATUS = CERTIFIED · dose_floor = 4
p5 invariant = 0 violations over 120 watched ticks
```

- **양성통제(PLANT)**: 서로 다른 창의 링 → 필드가 쪼개지고(splits>0) dose>0. 전 기하·전 seed 발화.
- **영-진실 받침대 2종**: 빈 링 → snaps 0 · c **정확히 0.0000** / 20개 **바이트 동일** 창 →
  splits **0** · density **정확히 0.0** · rows **0**. 둘 다 전 기하에서 거부.
  (이 "정확히 0" 을 위해 필드를 **세션 시드가 아니라 첫 리허설 창**으로 seed 한다 — 데몬과 다른,
   더 엄격한 선택이며 코드 주석에 명시. 세션 시드면 동일-내용 리허설도 첫 틱에서 1회 split 해
   받침대가 0 이 아니게 되고, 그러면 임계값을 고르는 순간 tune-to-green 이 된다.)

**④ 팔 (통제 통과 후에만 읽음):**

```
ARM A  vadapt ON  recency : splits=4 cells=5 density=0.5000 c=0.149237 rows=1 eff_age=0.8508
CTRL A vadapt OFF recency : splits=0 cells=0 density=0.8000 c=0.229091 rows=2 eff_age=0.7709
CTRL B random draw 0..4   : c = 0.183348 / 0.113885 / 0.149237 / 0.113885 / 0.183348
hook_delta_consolidation      = -0.079854
policy random c range         = [0.113885, 0.183348]
recency inside random range   = True
```

---

## ⑤ 실측 (B: 실학습 e2e · CPU 토이 · exit 0 · `clm_decodable=True`)

**훅 ON** (batch 32 · ratio 0.5 · every 10 · 30 steps):
```
[imagination] step 10 N3/REM snaps=16 splits=1 cells=2 density=0.0625 consolidation=0.0393 rows_replayed=1 eff_age=9.607(monitor-only) emit_violations=0
[imagination] step 20 N3/REM snaps=16 splits=1 cells=3 density=0.0625 consolidation=0.0393 rows_replayed=1 eff_age=9.607(monitor-only) emit_violations=0
[imagination] step 30 N3/REM snaps=16 splits=0 cells=3 density=0.0000 consolidation=0.0000 rows_replayed=0 eff_age=10.000(monitor-only) emit_violations=0
lane summary: {"phases":3,"replay_ticks":48,"vadapt_splits":2,"rows_replayed":2,"emit_violations":0,"cells":3,"select":"recency","vadapt_on_replay":true}
p5 invariant HELD for all 48 replay tick(s): emit_count==0
FINAL val_CE(pooled)=3.8285760283470154  registers_DESCENT=1/1
```

**훅 OFF (통제 A)** — 동일 명령, `--vadapt-on-replay` 만 제거:
```
[imagination] step 10/20/30 N3/REM snaps=16 splits=0 cells=0 density=0.8000 consolidation=0.4057 rows_replayed=6 eff_age=5.943(monitor-only) emit_violations=0
lane summary: {"phases":3,"replay_ticks":48,"vadapt_splits":0,"rows_replayed":18,"emit_violations":0,"cells":0,"select":"recency","vadapt_on_replay":false}
FINAL val_CE(pooled)=3.829510986804962  registers_DESCENT=1/1
```

**골든패스 무변경 검증** (플래그 부재 vs `--imagination-replay 0.0`), sha256:
```
c1577f3e01697a835a23c080b7aa7edb5e007e339443718839aaae3d00a60995  h9841_gp_a.clm   (플래그 없음)
c1577f3e01697a835a23c080b7aa7edb5e007e339443718839aaae3d00a60995  h9841_gp_b.clm   (--imagination-replay 0.0)
fc2eab6a02da38dfc171f0ace3148c29ed806eb08bd78a0003030bfeb59f67a9  h9841_b32_on.clm
e7143bec213c7cae41a3ec125f87953ab0c8deeb086c65ee8731aed363cd04cc  h9841_b32_off.clm
```
OFF 는 **sha256 동일** = byte-identical 골든패스. 두 처치 팔은 서로 다른 ckpt = 레인이 학습을 실제로 바꾼다.

**dose-floor 거부 실측** (아래 ⑦-결함1 의 게이트):
```
[imagination] REFUSING TO START — --imagination-replay 0.1 on a per-rank batch of 8 gives a
replay budget of 1 row(s), below the derived dose floor of 4. round(ir_consolidation_gain(n,
density)*n) == 0 for every density at n < 4, so the lane would report itself ON and replay
NOTHING. Raise --imagination-replay or --batch-size.
```

---

## ⑥ 읽기 — 음성도 결과다, 그대로 적는다

1. **훅은 인과다. 그리고 방향은 설계 의도와 반대다.** `hook_delta_consolidation = −0.0799` ($0),
   in-vivo 로는 **rows 2 (ON) vs 18 (OFF) = 9배 차이**. 성장 훅은 dose 를 *더하지 않고 깎는다*.
   고정 prior 0.80 은 리허설이 실제로 일으키는 성장(in-vivo 실측 density 0.0625)의 **12.8배
   과대평가**였다. 훅의 실제 역할은 "재응고를 키운다" 가 아니라 **"이미 흡수된 내용의 재학습을
   거절한다"** 이다. 부호가 예상과 반대라는 사실을 그대로 보고한다.
2. **선택 정책은 일 안 한다 — 통제 B 음성.** `recency inside random range = True`: recency 의
   c(0.1492)가 random 5회 draw 범위 [0.1139, 0.1833] **안**에 있다. 이 링 크기에서
   `ir_select_snapshots` 의 recency 정책은 dose 에 대해 인과가 아니다. 주장하지 않는다.
3. **동질 코퍼스에서 레인은 스스로 꺼진다.** step 30 에 splits=0 → density 0 → dose 0.
   VAdaptField 가 창들의 바이트 통계로 수렴하면 재조명할 새로움이 없다. 실측이지 결함이 아니다.
4. **val_CE 는 읽지 않는다** (3.8286 vs 3.8295). p7, 그리고 30-step 토이 예산에서 이 차이는 잡음이다.

---

## ⑦ 내 계기가 자기적발한 결함 2건 — tune-to-green 대신 게이트로 처리

- **결함 1 · dose 양자화 = 침묵 무동작.** 첫 배터리 실행이 **스스로 INSTRUMENT-DEAD (exit 4)** 를
  냈다. (ring 8, budget 3) 기하에서 레인은 신호를 분명히 봤는데(splits 2, c 0.0779)
  `round(c·n)=0` 이라 **0행 재생**. 즉 작은 budget 에서 레인은 "ON" 이라 로그하며 아무 것도 안 한다.
  → budget 을 올려 초록으로 만들지 **않았다**. `_imag_dose_floor()` 가 **엔진 자신의**
  `ir_consolidation_gain(n, 1.0)·n ≥ 0.5` 를 풀어 floor=**4** 를 유도하고, 트레이너가 그 아래
  설정을 **발사 전에 거부**한다(위 실측 참조). 배터리는 floor 미만 기하를 `below_dose_floor` 로
  표시하고 그 0행을 *구성상 0* 으로 읽는다(null 아님).
  **남은 한계(정직)**: floor=4 는 *최대 밀도에서* 1행이 산술적으로 가능함만 보장한다. 실제
  density 0.25 의 batch-8 실행은 floor 를 통과하고도 3 위상 내내 `rows_replayed=0` 이었다
  (실측). floor 는 산술 하한이지 유효성 보장이 아니다.
- **결함 2 · 가짜 강건축 2개.** (a) seed 축이 공허했다 — recency 경로는 결정론적이라 `random.Random`
  만 갈면 두 seed 가 **같은 수**를 냈다 → seed 가 **심은 내용**을 바꾸도록 수정. (b) 정책 통제가
  `budget == ring` 이라 recency 와 random 이 **같은 집합**을 뽑고 순서만 달랐다 — 이름은 멤버십
  통제인데 실제론 순서 통제 → 전 기하를 `budget < ring` 으로 수정.

---

## ⑧ 범위와 사전등록 (정직 게이트)

- **판정 아님.** ④⑤ 는 **계기 인증 + 배선 증명**이다. 레인이 모델이 *배우는 것*을 바꾸는지는
  측정하지 않았다. 303M 발사 없음.
- **사전등록된 실패조건 (H_9790 정합)**: H_9790 은 상상을 **DIRECTIONAL** 로 쟀다 — 내면 구조에는
  닿고 **입에는 닿지 않았다**. 후속 학습 실행에서 같은 **mouth 미도달**이 재현되는 것을 *발견*이
  아니라 **예상 결과로 미리 등록**한다. 이 레인이 입을 열어줄 것으로 기대하지 않는다.
- **train-py-10 정합**: 양성통제(서로 다른 창의 링)는 실제 코퍼스 창보다 **쉽다**. 배관은
  인증하되 "이 예산에서 그 질문이 답해지는가" 는 가린다.
- **데몬과의 의도적 차이 1건**: 필드 seed 원점(세션 시드 → 첫 리허설 창). 받침대를 정확히 0 으로
  만들기 위한 더 엄격한 선택이며 코드에 명시. **데몬 동작은 건드리지 않았다.**
- **DDP**: 레인은 rank-local(각 rank 가 자기 스트림을 리허설). shape 보존이라 collective 불변이나,
  world size 를 바꾸면 리허설 내용이 달라진다 — 재현시 world size 고정 필요.
- 토이 스케일(`a_toy_scale_recheck`). 규모 재확인 없이 어떤 수도 상향 일반화 금지.

**related:** H_9790 · H_9833 · H_9842 · H_9840 · H_9844(기하-강건성 게이트 선례) · H_9832(인용 검증 선례)
