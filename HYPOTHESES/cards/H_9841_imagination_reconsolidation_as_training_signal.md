# H_9841 — 상상 재응고(reconsolidation)를 학습 신호로 — 이미 데몬에 배선된 성장 훅을 학습으로 (R12-4)

**status:** 🔻 WIRED · 계기 인증이 **REAL-INPUT 에서 무너졌다** — CERTIFIED 는 **합성 링에서만** 성립.
실제 `.kosmos` 스냅샷에서 **양성통제(plant)가 6/6 기하×seed 전부 미발화 ⟹ INSTRUMENT-DEAD (exit 4)**.
받침대 2종과 p5 감시자는 실제 내용에서도 생존. 아래 ⑨⑩ 이 SSOT — ④ 의 수치는 폐기가 아니라
**"합성 격자에서 잰 값"으로 범위 축소**된다. (H_9838 심어둔-기하 실패의 동형 재현 · 2026-07-21)
**source:** R12 뇌부위 census (2026-07-21). 상위 설계 노드 = ARCHITECTURE `C2 RECOMBINE` 아래 `🧠 뇌부위 census` → `📋 R12`.
**wired:** yes — `anima-py train --imagination-replay …` (cli/train.py). $0 자가인증 배터리 동봉 + `--imagination-real-source` 실입력 스왑.
**scope ceiling:** DIRECTIONAL, 그리고 이제 **합성-입력으로 한정**. 계기 인증 + 레인 배선까지. **학습 판정 아님**(303M 미발사 · 토이 CPU e2e 만).

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

## ④ 실측 (A: $0 배터리 · exit 0 · **CERTIFIED — 단, 합성 링 한정**) — 통제 먼저, 순서 동결

> 🔻 **범위 라벨 (⑨ 이후 추가)**: 이 절의 모든 수는 **합성 산술 격자 링**에서 잰 것이다.
> 링을 실제 `.kosmos` 스냅샷으로 바꾸면 양성통제가 6/6 미발화하고 배터리는 INSTRUMENT-DEAD 가
> 된다 — ⑨ 참조. 이 절은 재현되지만, **실제 내용에 대한 인증으로 인용할 수 없다.**

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

---

## ⑨ 🔻 REAL-INPUT 스왑 — 심어둔 링을 실제 `.kosmos` 스냅샷으로 (2026-07-21 · 자가반박)

### ⑨-1 왜 했나 (H_9838 선례)

같은 날 H_9838 이 헤드라인 양성(CA3 다단계 완성 · 유도우연 12배 · lesion 바닥 · 3seed×3기하 ·
독립재현)을 냈다가, **코드 출처만** 심어둔 정수 fixture → 생산 trunk 실제 penultimate 로 바꾸자
**영-진실 받침대가 터졌다**(16항목 값-셔플 0.3750 > 바 0.3077 = INVALID · 32항목 0.1562 > 0.1500).
원인은 기전이 아니라 **손으로 만든 유리한 기하**였다 — 심은 코드 within .0469/across .0117(사실상
직교) vs 실제 표현 .0625/.0260(겹침 2.2배).

이 배터리는 **정확히 같은 노출**을 갖는다. ④ 의 링은 `novel(n,w,off) = (off + i·37 + j·7) % 256`
로 합성한 **산술 격자**이고, 그 격자는 `vadapt_field_step` 이 쪼개기 판정에 쓰는 바로 그 8차원
byte 통계 위에서 창들을 **구성상** 최대로 벌려 놓는다. 실제 스냅샷은 그렇게 안 생겼다.

### ⑨-2 무엇만 바꿨나 (그리고 무엇을 안 바꿨나)

`anima-py train --imagination-selftest **--imagination-real-source <DIR>**` — 링의 **바이트 출처**
하나. 게이트 순서 · 팔 · 통제 · 바 · 임계값 · dose_floor · seed 정책 **전부 불변**.

- 링 = 실제 `.kosmos` 앵커 스토어의 `@payload text` 바이트. 리더는 **생산 리더**
  `core/kosmos_io.load_anchors` (재구현 0). 앵커 1개 = 링 슬롯 1개(= in-vivo `mem_push_ctx` 의 모양),
  폭 w 로 **절단만**(패딩 금지 — pad 바이트는 지어낸 내용이고, 없애려는 균일성을 되만든다).
  `seed` 는 앵커 목록의 **시작점을 회전**한다 — 합성 경로에서 `off` 가 심은 내용을 바꿨던 것과
  같은 역할(어느 실제 내용인가), rng 만 갈아치우는 공허한 축이 아니다.
- FLAT 받침대 = **실제 창 1개를 반복**. 실내용 팔에 합성 `[7]*w` 받침대를 붙이면 팔과 다른 세계의
  통제가 된다(`control-must-match-mediating-covariate`). 역할(구조 없는 입력을 거부해야 함)은 동일.
- EMPTY 받침대 · p5 감시자 양성통제 = 손대지 않음.
- **왜 `.kosmos` 이고 `clm_penult_pooled_W` 가 아닌가**: 필드의 분열 판정은 `_imag_byte_feature`
  의 8차원 ~[0,5] 통계 위에서 읽는 **절대 L2 임계값**(`core/engine_cli.py` `SPLIT_THRESH = 0.30`)
  이다. 768차원 penultimate 를 대신 먹이면 그 **고정 임계값이 비교되는 L2 스케일 자체가 바뀐다**
  = 입력만 바꾸는 척하며 **바를 옮기는 것**. 링은 바이트 창 목록이므로 정직한 스왑은 byte feature
  를 유지하고 **바이트를 바꾸는 것**이다. (실제 표현 경로는 ⑩-3 에 사전등록만 하고 **발사 안 함**.)
- **리더 정직성(H_9843)**: `load_anchors` 는 LOSSY 로 측정됐다(제목 탈락 · payload 이스케이프 유지).
  **감사만 하고 고치지 않았다** — 이 레인은 payload **바이트**를 먹으며, 측정 안에서 리더를 조용히
  고치면 입력을 **두 번** 바꾸는 것이 된다. 실측 감사: 5개 스토어 전부 `titles_recovered = 0`
  (H_9843 의 제목 탈락 확증) · `payloads_still_escaped = 0` (이 스토어들엔 이스케이프가 없어 이중
  이스케이프 위험 미노출) · parity 스토어의 `with_text_payload 2/4` 는 리더 손실이 아니라 파일에
  실제로 `@payload text := ""` 인 앵커가 2개(디스크 확인).

### ⑨-3 재현 명령 (실행한 그대로)

```bash
python3 -m venv /tmp/venv_h9841r
/tmp/venv_h9841r/bin/pip install -q numpy torch
/tmp/venv_h9841r/bin/pip install -q --force-reinstall --no-deps .

# (구경로 — 무회귀 증명 · 카드 ④ 와 대조)
/tmp/venv_h9841r/bin/anima-py train --imagination-selftest \
    --imagination-replay 0.5 --vadapt-on-replay

# (신경로 — 실제 .kosmos 스냅샷)
/tmp/venv_h9841r/bin/anima-py train --imagination-selftest \
    --imagination-replay 0.5 --vadapt-on-replay \
    --imagination-real-source HEXAD/UNIVERSE-BRAIN-MAP/anchors/e7_31
```

### ⑨-4 실측 A — 구경로 무회귀 (exit 0 · ④ 와 **완전 동일**)

```
STATUS = CERTIFIED · dose_floor = 4
p5_watch_control = true/true
ring win budget seed below_floor fires refuses | PLANT splits cells dens    c      rows | FLAT splits dens   c      rows | EMPTY snaps c
 20   32    8     7    False     True   True   |      4      5   0.5000  0.1492   1    |     0     0.0000 0.0000   0 |     0    0.0000
 20   32    8    11    False     True   True   |      4      5   0.5000  0.1492   1    |     0     0.0000 0.0000   0 |     0    0.0000
  8   16    3     7    True      True   True   |      2      3   0.6667  0.0779   0    |     0     0.0000 0.0000   0 |     0    0.0000
  8   16    3    11    True      True   True   |      2      3   0.6667  0.0779   0    |     0     0.0000 0.0000   0 |     0    0.0000
 20   64    5     7    False     True   True   |      3      4   0.6000  0.1144   1    |     0     0.0000 0.0000   0 |     0    0.0000
 20   64    5    11    False     True   True   |      4      5   0.8000  0.1501   1    |     0     0.0000 0.0000   0 |     0    0.0000
ARM A  vadapt ON  recency : splits=4 cells=5 density=0.5000 c=0.149237 rows=1 eff_age=0.8508
CTRL A vadapt OFF recency : splits=0 cells=0 density=0.8000 c=0.229091 rows=2 eff_age=0.7709
CTRL B random draw 0..4   : c = 0.183348 / 0.113885 / 0.149237 / 0.113885 / 0.183348
hook_delta_consolidation      = -0.079854
policy random c range         = [0.113885, 0.183348]
recency inside random range   = True
p5 invariant = 0 violations over 120 watched ticks
```

⟹ **무회귀.** ④ 의 모든 측정량과 문자 단위로 같다(추가된 것은 `realized_ring` telemetry 줄뿐).

### ⑨-5 실측 B — 실입력 (exit **4** · `HEXAD/UNIVERSE-BRAIN-MAP/anchors/e7_31` · 31 앵커)

```
STATUS = INSTRUMENT-DEAD · dose_floor = 4
p5_watch_control = true/true
real_source = {"dir": "HEXAD/UNIVERSE-BRAIN-MAP/anchors/e7_31", "anchors_read": 31,
  "with_text_payload": 31, "payload_bytes_min": 215, "payload_bytes_max": 231,
  "payload_bytes_total": 6890, "payloads_still_escaped": 0, "titles_recovered": 0,
  "reader": "core/kosmos_io.load_anchors (production reader, unmodified)"}
ring win budget seed below_floor fires refuses | PLANT splits cells dens    c      rows | FLAT splits dens   c      rows | EMPTY snaps c
 20   32    8     7    False     False  True   |      0      1   0.0000  0.0000   0    |     0     0.0000 0.0000   0 |     0    0.0000
      realized_ring=20 underpowered=False
 20   32    8    11    False     False  True   |      1      2   0.1250  0.0393   0    |     0     0.0000 0.0000   0 |     0    0.0000
      realized_ring=20 underpowered=False
  8   16    3     7    True      False  True   |      0      1   0.0000  0.0000   0    |     0     0.0000 0.0000   0 |     0    0.0000
      realized_ring=8  underpowered=False
  8   16    3    11    True      False  True   |      0      1   0.0000  0.0000   0    |     0     0.0000 0.0000   0 |     0    0.0000
      realized_ring=8  underpowered=False
 20   64    5     7    False     False  True   |      2      3   0.4000  0.0775   0    |     0     0.0000 0.0000   0 |     0    0.0000
      realized_ring=20 underpowered=False
 20   64    5    11    False     False  True   |      1      2   0.2000  0.0394   0    |     0     0.0000 0.0000   0 |     0    0.0000
      realized_ring=20 underpowered=False
arms = WITHHELD (status != CERTIFIED)
why: the planted signal (a ring of mutually distinct windows) did NOT move the lane —
     no field split and/or no dose.
```

**`realized_ring == 요청 ring` 이 6/6** ⟹ 이건 **미검정력(UNDERPOWERED)이 아니라 진짜 음성**이다.
요청한 기하를 실제 스토어가 전부 채웠는데도 양성통제가 안 켜졌다.

### ⑨-6 왜 죽었나 — 계기 자체가 뱉는 기하 진단 (`plant_feature_spread`, telemetry-only)

필드가 쪼개는 그 공간(8-D byte feature)에서 링 창들 사이 **쌍별 L2**:

```
                  n   mean_pairwise_L2   min        max        | splits dens    c       rows  fires
SYNTH 20/32/s7   20   0.704893           0.120860   1.408291   |   4    0.5000  0.1492   1    True
SYNTH 20/32/s11  20   0.705186           0.027682   1.483667   |   4    0.5000  0.1492   1    True
SYNTH  8/16/s7    8   3.332049           0.544453   6.217728   |   2    0.6667  0.0779   0    True
SYNTH  8/16/s11   8   3.294191           0.627762   6.034735   |   2    0.6667  0.0779   0    True
SYNTH 20/64/s7   20   0.584775           0.020644   1.188292   |   3    0.6000  0.1144   1    True
SYNTH 20/64/s11  20   0.582746           0.019802   1.125365   |   4    0.8000  0.1501   1    True
REAL  20/32/s7   20   0.002596           0.000014   0.007298   |   0    0.0000  0.0000   0    False
REAL  20/32/s11  20   0.036063           0.000038   0.336847   |   1    0.1250  0.0393   0    False
REAL   8/16/s7    8   0.000000           0.000000   0.000000   |   0    0.0000  0.0000   0    False
REAL   8/16/s11   8   0.000000           0.000000   0.000000   |   0    0.0000  0.0000   0    False
REAL  20/64/s7   20   0.452871           0.000340   1.258507   |   2    0.4000  0.0775   0    False
REAL  20/64/s11  20   0.443734           0.000340   1.262119   |   1    0.2000  0.0394   0    False
```

- 같은 (20,32) 기하에서 합성 0.7049 vs 실제 0.0026 = **271배 축소**(seed 11 도 0.7052 vs 0.0361 =
  19.6배). `SPLIT_THRESH = 0.30` 위에 앉아 있던 합성 링이 실제로는 임계값 **두 자릿수 아래**로 내려간다.
- (8,16) 기하에서 실제 spread 는 **정확히 0.000000** — 실제 앵커 payload 들의 **첫 16 바이트가
  바이트 동일**하다(공유 템플릿 접두 `[anima 우주뇌지도] `). 이것이 브리핑이 말한 **real repetition**
  이며, 합성 격자에는 구성상 존재할 수 없다.
- (20,64) 에서만 실제 spread 0.4529 가 임계값을 넘겨 splits 2 가 나오지만, **dose 가 0으로 반올림**
  된다(c=0.0775 × budget 5 = 0.39 → round 0). 즉 ⑦-결함1 이 남겨둔 정직한 한계
  ("floor 는 산술 하한이지 유효성 보장이 아니다")가 **실제 내용에서 실제로 물었다**.

⟹ 진단: **합성 링은 손으로 만든 유리한 기하였고, ④ 의 CERTIFIED 를 만든 것은 기전이 아니라 그
기하였다.** H_9838 과 같은 실패 계급, 같은 날, 다른 계기.

### ⑨-7 실제 스토어 전수 census (사전등록 — 이 호스트의 실제 `.kosmos` 스토어 **전부**, 취사선택 없음)

```
store                                            anch txt realized(6 rows)      plant_fires  ped_refuses  STATUS
HEXAD/UNIVERSE-BRAIN-MAP/anchors/e7_31            31  31 20/20/8/8/20/20       F/F/F/F/F/F  T/T/T/T/T/T  INSTRUMENT-DEAD
HEXAD/UNIVERSE-BRAIN-MAP/anchors                  18  18 18/18/8/8/18/18       T/T/F/T/F/F  T/T/T/T/T/T  REAL-UNDERPOWERED
archive/KOSMOS/303m_kr_en_sns/anchors              3   3 3/3/3/3/3/3           F/F/F/F/F/F  T/T/T/T/T/T  REAL-UNDERPOWERED
state/py_selfimpl/p6_chat_parity/py_kosmos         4   2 2/2/2/2/2/2           F/F/T/T/F/F  T/T/T/T/T/T  REAL-UNDERPOWERED
~/.anima_kosmos_self (LIVE daemon self-anchor)     1   1 1/1/1/1/1/1           F/F/F/F/F/F  T/T/T/T/T/T  REAL-UNDERPOWERED
```

- **판독 가능한 스토어는 e7_31 하나뿐**이다(요청 기하를 채우는 유일한 스토어). 나머지 4개는
  `realized_ring < 요청 ring` ⟹ **REAL-UNDERPOWERED (exit 5)** 로, 발화도 미발화도 읽지 않는다
  (`power-before-negative-verdict`). 특히 UBM-18 은 (20,32) 두 seed 에서 plant 가 켜지지만
  realized 18 < 20 이라 **그 양성을 읽지 않는다** — 초록이 나오는 칸을 골라 읽지 않기 위한 게이트다.
- 살아있는 데몬의 자기앵커 스토어(`~/.anima_kosmos_self`)는 **앵커 1개**다. "실제 데몬 스냅샷"의
  현재 가용 상한이 n=1 이라는 사실 자체가 결과이며, ⑩-2 의 하류 차단 근거다.

### ⑨-8 통제는 어디까지 살아남았나 (순서 동결 · 통제 먼저)

| 통제 | 합성 | **실제** | 판정 |
|---|---|---|---|
| ⓪ p5 감시자 양성통제 (심은 `emit_count=1`) | 감지 True | **감지 True** | 🟢 생존 |
| ⓪ p5 감시자 침묵틱 통과 | True | **True** | 🟢 생존 |
| ② 받침대 A — 빈 링 (snaps 0 · c 정확히 0.0000) | 거부 | **거부 6/6** | 🟢 생존 |
| ② 받침대 B — 새로움 0 링 (splits 0 · dens 0.0 · rows 0) | 거부 | **거부 6/6 (실제 창 반복판)** | 🟢 생존 |
| ① 양성통제 — plant 발화 | 발화 6/6 | **미발화 6/6** | 🔴 **사망** |

**받침대는 안 터졌다.** 이 레인은 H_9838 처럼 *지어내지는* 않는다 — 구조 없는 입력엔 정확히 0을
준다. 죽은 것은 **실제 내용에서 신호를 볼 수 있는 능력** 쪽이다. 두 실패 모드는 다르고, 이 구분이
⑩ 의 범위 축소를 결정한다.

---

## ⑩ 정직한 판정 · 범위 축소 · 하류 차단

### ⑩-1 착륙했던 양성은 살아남았나 → **아니다**

`STATUS = CERTIFIED` 는 **합성 산술 격자 위에서만** 성립한다. 실제 `.kosmos` 스냅샷에서 같은 배터리는
**INSTRUMENT-DEAD**다. ④ 의 수치는 철회하지 않는다(그 입력에서 재현된다) — 대신 **"합성 링에서
잰 값"으로 라벨이 바뀐다**. 실제 내용에 대한 계기 인증은 **없다**.

### ⑩-2 착륙했던 두 **음성**은 살아남았나 → 하나는 이미 실내용에서 재확인, 하나는 **읽을 수 없음**

1. **훅 부호 음성 (hook 은 인과지만 방향이 반대)** — 🟡 **부분 생존, 그리고 원래부터 실내용 근거가 있었다.**
   ⑤ 의 in-vivo e2e(`rows 2 ON vs 18 OFF` · 실측 density 0.0625 vs 고정 prior 0.80)는 **이미 실제
   코퍼스 창**에서 나온 수치다 — 합성 링이 아니다. ⑨ 의 실제 `.kosmos` 링도 같은 방향을 가리킨다:
   실측 density 0.0000–0.4000 이 전부 고정 prior 0.80 **아래**이므로 `hook_delta` 는 실제 내용에서도
   음수다(정의상 density < 0.80 ⟺ delta < 0). **단, `--imagination-real-source` 경로에서 그 숫자를
   직접 인쇄하지는 않았다** — 통제 미통과 시 팔을 보류하는 동결 순서를 지켰기 때문. 그러므로
   "실제 스냅샷에서 잰 `hook_delta` 값"은 **여전히 미측정**이며 여기에 새 수를 적지 않는다.
2. **recency 비인과 음성** — 🔴 **실제 내용에서 읽을 수 없음(미측정).** 팔 블록은 통제 통과 후에만
   돌고, 실입력에서 통제가 통과하지 못했다. `recency inside random range = True` 는 **합성 링 한정**
   주장으로 축소된다. 실제 스냅샷에서 선택 정책이 인과인지 아닌지는 **모른다**.

### ⑩-3 사전등록된 후속 (설명만 · **발사하지 않음** — 사후 탐색은 tune-to-green)

실입력 null 을 본 *뒤에* 다른 창 절단법을 시도해 plant 를 되살리는 것은 금지된 초록사냥이다.
그래서 아래는 **다음 H 로 사전등록만** 하고 이번 PR 에서 돌리지 않았다:

- **(R-a) 스트림-절단 실제 창.** 이번엔 "앵커 1개 = 창 1개, 앞에서 w 바이트 절단"을 썼다(레코드-절단).
  in-vivo 트레이너는 코퍼스 **스트림**에서 연속 창을 자른다 — payload 들을 이어붙여 연속 w-바이트
  창으로 자르면 템플릿 위상이 창마다 달라져 spread 가 회복될 **수도** 있다. 이건 정당한 대안 구성이지
  구제책이 아니며, **결과를 보기 전에** 사전등록되어야 읽을 수 있다.
- **(R-b) 실제 표현 경로.** `core/decode.clm_penult_pooled_W` 로 링 항목의 표현을 잡으려면 고정
  `SPLIT_THRESH = 0.30` 이 비교되는 L2 스케일이 바뀐다 ⟹ **먼저** 그 임계값의 차원-불변 재유도
  (또는 feature 정규화)를 사전등록해야 하고, 그건 바를 옮기는 변경이라 별도 H 다.
- **(R-c) 진짜 데몬 링 수확.** 현재 살아있는 자기앵커 스토어는 **n=1**이다. 실제 채팅 세션에서
  working-ring 스냅샷을 n≥20 으로 쌓는 수확 경로가 없으면 이 레인의 "실제 스냅샷" 질문은 구조적으로
  미검정력 상태다. **수확이 선행조건**이다.

### ⑩-4 이 결과가 막는 하류 지출

- 🚫 **이 레인으로 303M 을 태우는 것.** ④ 는 "레인이 실제 신호를 본다"의 근거가 아니었다 —
  합성 격자에서만 본다. 실제 내용에서 dose 는 6/6 칸에서 **0행**이었다. 즉 오늘 상태로 303M 을
  돌리면 `--imagination-replay` 는 **켜졌다고 로그하며 아무 것도 재학습하지 않는** 확률이 높다
  (⑦-결함1 이 경고한 침묵 무동작 계급이 실입력에서 실현됨). GPU-시간을 태우기 전에 (R-a)/(R-c) 가
  먼저 판독돼야 한다.
- 🚫 **"상상 재응고 레인 = 계기 인증됨"을 전제로 한 후속 카드.** H_9841 을 인용하는 설계는
  **"합성 입력에서 인증"**으로 인용해야 한다.
- ✅ **막지 않는 것**: p5 불변식과 두 받침대는 실제 내용에서도 살아있으므로, 이 레인이 *지어낸다*는
  걱정은 근거 없다. 배선(플래그·골든패스 byte-identical·dose_floor 거부 게이트)도 그대로 유효하다.

### ⑩-5 계기 변경 요약 (`a_experiment_engine_native`)

- `cli/train.py` — `--imagination-real-source DIR` (신규 · 기본 "" = OFF, 합성 경로 문자 단위 불변),
  `_imag_real_anchors()` (생산 리더 `core/kosmos_io.load_anchors` 만 호출 · 재구현 0 · H_9843 감사 동봉),
  `_imag_ring_spread()` (telemetry-only 기하 진단 · 어떤 팔·바·dose 도 읽지 않음),
  `REAL-UNDERPOWERED` 상태 + **exit 5**. `cli/train.py` 에는 `_KNOWN_FLAGS` 화이트리스트가 없다
  (그건 `cli/evaluate.py` 전용 · `grep -n _KNOWN_FLAGS cli/train.py` → 없음), 그래서 등록 대상 없음.
- 루트 `VERSION` 0.20.111 → **0.20.112** (G5).

**related:** H_9790 · H_9833 · H_9842 · H_9840 · H_9844(기하-강건성 게이트 선례) · H_9832(인용 검증 선례) · **H_9838(심어둔-기하 실패 선례 = 이 스왑의 동기)** · **H_9843(kosmos 리더 LOSSY 선례)**
