# H_9846 — 구조-봉투(Φ-봉투) 층을 학습 회귀 감시로 (R12-9 · MONITOR-ONLY · 손실 투입 금지)

**status:** 🔧 WIRED-INSTRUMENT · 🔻 **실입력 스왑 후 부분생존** (계기 CERTIFIED 유지 · 손실-무관 byte-identical 유지 ·
**착륙했던 처치 판독(③④)은 실제 303M 으로 옮기면 살아남지 못함** — 아래 ⑥⑦⑧ · **과학 판정 0**)
**source:** R12 뇌부위 census (2026-07-21) — `origin/main` `core/` 12개 모듈 실측 후 1모듈=1레버로 등록.
상위 설계 노드 = ARCHITECTURE `C2 RECOMBINE` 아래 `🧠 뇌부위 census` → `📋 R12`. R11(H_9830~9836)의 후속.
**wired:** yes — `anima-py train --phi-envelope-monitor {off,on} [--phi-monitor-every N]`
(`cli/train.py` + 새 엔진 모듈 `core/phi_envelope_monitor.py` · VERSION 0.20.108→0.20.109 · G5).

## 전제 검증 (인용 전 실측 · H_9832 재발방지)

`git ls-tree -r origin/main --name-only | grep phi_envelope` → `core/phi_envelope_substrate.py` **존재**(189줄).
카드의 전제는 **철회 없음**: `envelope_multiscale` · `pe_pearson` · `envelope_self_similarity` ·
`pe_coupling_for_class` · `pe_norm_convexity` · `pe_edge_of_chaos_peak` · `collective_phi_nest` ·
`phi_smooth_no_cliff` · `temporal_agency_context` · `phi_envelope_summary` 전부 파일에서 직접 읽어 확인했고,
`emit_policy` import 0 (F-EMIT-5)·순수 스칼라(`math.cos/sqrt`)·emit bool 게이트 0 도 그대로였다.
이번에 실제로 쓰는 함수는 `collective_phi_nest` · `pe_norm_convexity` · `phi_smooth_no_cliff` 셋뿐이다.

## 배선한 것

```
anima-py train … --phi-envelope-monitor on [--phi-monitor-every N]   # 로그 전용 (기본 off)
```

- 틱마다 **파라미터 텐서별 RMS 1개**(이름 정렬 순서 · arch 무관)를 `units` 벡터로 만들고,
  `core/phi_envelope_monitor.py` 가 `dispersion=(max−min)/mean` · `span=max/min` ·
  `nest_scale`/`nest_sync`(=`collective_phi_nest`)를 읽는다. 틱 시계열의 `dispersion` 을
  `phi_smooth_no_cliff` 에 넣어 **`cliff_gap`**(최대 틱간 점프)을 얻는다.
- ⛔ **이름 규율(`a_phi_iit4_tool`)**: 이 중 어떤 것도 **Φ 가 아니다**. Φ 는 충실한 IIT4 로만 잰다.
  출력명은 산술 그대로(`dispersion`/`span`/`nest_*`/`cliff_gap`)이며 카드 어디서도 Φ 로 승격하지 않는다.
- ⛔ **손실 금지(`a_train_inline_gauge`)**: 구조적으로 막았다 — 모듈은 torch 를 import 하지 않고
  float 만 받으며, 틱은 `no_grad` 로 파라미터만 읽고 **텐서를 새로 만들지 않고**(train-py-1 device-mismatch
  재발방지) **RNG 를 한 번도 뽑지 않는다**. 따라서 ON/OFF 가 byte-identical 이고, "손실에 안 들어간다"가
  약속이 아니라 **증명**이 된다(아래 ②).
- 왜 활성화가 아니라 파라미터인가: 활성화 탭은 forward 를 요구하고 dropout/RNG 를 소모해 ON≠OFF 를
  조용히 만든다. byte-identity 가 monitor-only 를 증명하는 유일한 수단이므로 더 풍부한 신호보다 우선한다.
  (한계로 아래 ⑤에 명시.)

## 재현 명령 (그대로 복사 가능)

```bash
python3 -m venv /tmp/venv_h9846 && /tmp/venv_h9846/bin/pip install -q torch numpy
/tmp/venv_h9846/bin/pip install -q --force-reinstall --no-deps .        # 이 워크트리
/tmp/venv_h9846/bin/anima-py corpus flat --lang en --out /tmp/h9846/c.txt --seed 7

BASE="--corpus /tmp/h9846/c.txt --steps 20 --d 64 --L 2 --seq-len 64 --batch-size 4 \
      --device cpu --seed 7 --log-every 5 --skip-inline-rho"
/tmp/venv_h9846/bin/anima-py train $BASE --out /tmp/h9846/A/m.clm --gauges-out /tmp/h9846/A/g.json
/tmp/venv_h9846/bin/anima-py train $BASE --out /tmp/h9846/B/m.clm --gauges-out /tmp/h9846/B/g.json \
      --phi-envelope-monitor on --phi-monitor-every 5
```

## ① 통제 먼저 — 동결 순서(값은 인증 뒤에만 읽는다)

배터리는 **step 1 전에** 돌고, 통과 못 하면 감시는 그 실행 내내 **아무 값도 찍지 않는다**(학습은 그대로 진행 —
학습을 멈출 수 있는 감시는 이미 레버다). 실측 출력 그대로:

```
[structure-envelope H_9846] battery CERTIFIED — plant_fires=True pedestal_refuses=True
  discriminates_ramp=True (plant gap 0.484848 · pedestal 0 · ramp cadence-inflation 3.9663×)
```

| 팔 | 무엇 | 요구 | 실측 |
|---|---|---|---|
| **양성통제** `plant_cliff_units` | 한 틱에 심어둔 구조 절벽 | 회수해야 함 | `cliff_gap 0.484848` (cadence 1·2·4 전부 동일, spread **0.0**) |
| **참값-0 받침대** `plant_flat_units` | **구조 없는 입력**(모든 unit 동일) | FP 0 이어야 함 | `dispersion 0.0` · `span 1.0` · `cliff_gap 0` (세 cadence 전부) |
| **판별통제** `plant_ramp_units` | 끝점 동일·경로만 완만한 램프 | 절벽보다 **낮아야** 함 | `0.045326 / 0.090395 / 0.179775` (cadence 1/2/4) < 0.484848 |

받침대가 0 을 넘으면 계기가 구조를 **날조**하는 것이므로 INVALID·중단이라는 것이
`phi-estimator-needs-zero-truth-pedestal` 의 요구였고, 여기서는 **정확히 0.0** 이 나왔다.

**게이트가 공허하지 않다는 증명**(각 팔을 일부러 깨고 배터리를 다시 돌림):

```
pedestal broken (받침대에 구조 있는 입력) -> INVALID
plant broken    (양성통제에 구조 없는 입력) -> INSTRUMENT-DEAD
ramp broken     (램프=절벽으로 대체)        -> INVALID
```

## ② 손실-무관 증명 — ON vs OFF byte-identical (같은 seed)

```
a599419efeff594b9cea3a47e36181cca83f517ba0d28dd5fc306668b39f8a10  /tmp/h9846/A/m.clm   (OFF)
a599419efeff594b9cea3a47e36181cca83f517ba0d28dd5fc306668b39f8a10  /tmp/h9846/B/m.clm   (ON)
210a5a18bfa032b88004b224b00c508ed304821fa59b2e7415379b343fec2b09  /tmp/h9846/A/m.clm.pt
210a5a18bfa032b88004b224b00c508ed304821fa59b2e7415379b343fec2b09  /tmp/h9846/B/m.clm.pt
```

`.clm`·`.pt` 둘 다 sha256 동일. 학습 로그 `diff` 도 **추가된 감시 줄과 경로 문자열 외 차이 0**
(CE 5.65104→4.49831 · `FINAL val_CE(pooled)=4.542315721511841` 양쪽 동일), `--gauges-out` JSON 도
`phi_envelope_monitor` 블록을 빼면 완전 동일(OFF 는 그 자리에 `null`).

> ⚠️ 처음 A/B 는 `off.clm.pt` 437,790 B vs `on.clm.pt` 436,929 B 로 **크기가 달랐다**. 원인은 학습이 아니라
> `torch.save` zip 컨테이너가 출력 **파일명 길이**에 따라 레코드 패딩을 바꾸기 때문이었다(텐서 23개 전부
> `torch.equal` True). 파일명 길이를 맞춰(`A/m.clm`·`B/m.clm`) 재실행하니 컨테이너까지 byte-identical.
> 기록해 둔다 — 이걸 모르면 멀쩡한 byte-identity 를 회귀로 오독한다.

## ③ 실측 (treatment · 20-step CPU 장난감 학습)

```
[structure-envelope H_9846 MONITOR-ONLY] step=1  dispersion=4.800336 span=3333.231415 nest_sync=0.883229 units=23
[structure-envelope H_9846 MONITOR-ONLY] step=5  dispersion=4.793740 span=896.541719  nest_sync=0.883317 units=23
[structure-envelope H_9846 MONITOR-ONLY] step=10 dispersion=4.298951 span=500.035936  nest_sync=0.878151 units=23
[structure-envelope H_9846 MONITOR-ONLY] step=15 dispersion=4.293360 span=358.393034  nest_sync=0.878235 units=23
[structure-envelope H_9846 MONITOR-ONLY] step=20 dispersion=4.288242 span=284.014784  nest_sync=0.878300 units=23
[structure-envelope H_9846 MONITOR-ONLY] n_ticks=5 every=5 cliff_gap=0.494789 cliff_rate=0.09895785
  dispersion 4.800336 → 4.288242 · self-subsample spread 0.0338 ⇒ step-like (gap cadence-robust; read cliff_gap)
```

이 실행의 최대 구조 점프는 **step 5→10 구간(Δ=0.494789)** 이고, 로그상 그 구간에 있는 사건은
`step 10 (MITOSIS SPLIT) E 2->3` 이다. 즉 감시가 집은 절벽은 **실제 구조 사건**과 일치한다.
⚠️ 이건 회귀 판정이 **아니다** — MITOSIS 성장은 의도된 사건이고, 이 실행은 20 step·0.108M 짜리
계기 검증용 장난감이다. 감시가 실제 구조 변화에 반응한다는 **배관 증거**일 뿐이다.

## ④ 손잡이가 판정을 뒤집는지 — 실측하고 게이트를 달았다 (no tune-to-green)

`phi_smooth_no_cliff` 는 **연속 표본** 통계라 cadence 가 값을 기계적으로 바꾼다. 같은 학습을
cadence 만 바꿔 5회 재실행한 실측:

| `--phi-monitor-every` | n_ticks | `cliff_gap` | `cliff_rate` | self-subsample spread |
|---|---|---|---|---|
| 1  | 20 | 0.488390 | 0.48838958 | 0.0069 |
| 2  | 11 | 0.489983 | 0.24499129 | 0.0135 |
| 5  | 5  | 0.494789 | 0.09895785 | 0.0338 |
| 10 | 3  | 0.501385 | 0.05013848 | 0.0209 |
| 20 | 2  | 0.512094 | 0.02560469 | 0.0000 |

**발견(설계 의도와 반대)**: 이 실행처럼 **계단형** 변화에서는 `cliff_gap` 이 cadence-강건하고
(1→20 에서 4.8% 변동) **`cliff_rate` 가 19× 로 흔들린다**. 내가 처음 `cliff_rate` 를 "cadence 보정치"로
넣은 것은 틀린 프레이밍이었다 — 램프형 변화에서는 정반대(동봉 ramp 통제 실측: 같은 sweep 에서 gap 3.97× 팽창).
**어느 쪽도 두 레짐 모두에서 강건하지 않다.**
수리: 요약이 수집된 시계열을 **스스로 subsample(1/2/4) 해 재판독**해 `cliff_by_subsample` ·
`cliff_gap_spread_rel` · `regime` 을 함께 낸다(재학습 0원). 라벨은 **아무것도 gate 하지 않고** 두 수는 항상
같이 찍히므로, 임계값이 판정을 뒤집을 표면이 없다. 위 표에서 self-gate 는 5/5 cadence 모두 `step-like` 로
바깥에서 재학습해 얻은 sweep 과 일치했다.

## ⑤ 정직한 범위·한계

1. **판정 아님.** 오늘 착륙한 것은 **안전망 계기**다. 과학 판정 0 — 어떤 레버도 이 수로 평가되지 않았다.
2. **Φ 아님(`a_phi_iit4_tool`)**. 봉투/구조 층이다. Φ 라 부르면 그 순간 규칙 위반이다.
3. **파라미터-측만 본다.** 활성화/표상 구조가 무너져도 파라미터 RMS 분산이 안 움직이면 이 감시는 못 본다.
   byte-identity 를 지키려고 택한 교환이며, 이건 **가림(coverage) 한계이지 음성 증거가 아니다**.
4. **train-py-10 (통과한 통제의 거짓 안심)**: 동봉 배터리는 **판독기**를 인증한다 —
   "심어둔 절벽을 보는가 / 없는 구조를 만들지 않는가". 실제 학습 레버의 구조 손상이 이 감시의
   **사정거리 안에 있는지는 인증하지 않는다**. 회귀를 못 잡았다고 회귀가 없었다고 읽으면 안 된다.
5. **MITOSIS 는 `n_units` 를 바꿀 수 있다.** 이번 실행은 23 로 고정이었지만(분할이 텐서 내부 차원을 키움),
   unit 집합이 바뀌는 실행에서는 틱 간 비교가 같은 대상의 비교가 아니다 — `n_units` 를 매 틱 찍는 이유.
6. **장난감 규모**(d=64·L=2·20 step·CPU). `a_toy_scale_recheck`: 계기 생존 증명이지 303M 사실이 아니다.

---

# 🔻 실입력 스왑 (2026-07-21 추가 · **입력만 바꾼다**)

## ⑥ 왜 이 스왑을 해야 했나 — H_9838 의 심어둔-기하 실패

같은 날 H_9838 이 헤드라인 양성을 착륙시켰다 — CA3 다단계 완성이 A→B,B→C 만 저장한 상태에서 A→C 를
**유도 우연의 12배**로 복원했고, 연쇄절제가 바닥으로 붕괴시켰으며, 인증·양성통제·참값0 받침대·3 seed×3 기하·
독립재현까지 갖췄다. 그 다음 **코드 출처만** 심어둔 정수 fixture → 생산 trunk 의 **실제 penultimate 표현**으로
바꾸자(팔·통제·bar 전부 동일):

| load | planted codes | real 303M reps |
|---|---|---|
| 8 | CERTIFIED | CERTIFIED (chance=0.2 · 절제 비판별) |
| 16 | CERTIFIED ← 판정 | **INVALID** (값-섞기 받침대 0.3750 > bar 0.3077) |
| 32 | INSTRUMENT-DEAD | **INVALID** (0.1562 > 0.1500) |

받침대가 발화했다 = 구조 없는 저장소가 맞혔다 = 답은 기전이 아니라 **코드 기하**에서 나왔다. 심어둔 코드는
사실상 직교(내 .0469 / 간 .0117)인데 실제 표현은 2.2배 겹친다(.0625 / .0260). **H_9846 의 ③④ 수치도 정확히
같은 종류의 손수 만든 세계**(d=64·L=2·20-step CPU 토이)에서 나왔다. 그래서 같은 스왑을 이 계기에 진 빚으로 갚는다.
**기대되는·가치있는 결과는 이 카드의 양성이 살아남지 *않는* 것이다** — 여기서의 반박이 하류 지출을 막는다.

## ⑦ 배선 — `--structure-envelope-read` (입력만 교체, 그 외 전부 동결)

```bash
anima-py evaluate <ckpt.clm> --structure-envelope-read [--out j.json]
```

- `cli/evaluate.py::structure_envelope_read_run` (+ `core/phi_envelope_monitor.py::read_side_report`)
  · `_KNOWN_FLAGS` 등록됨(미등록 플래그는 **거부**되는 파일이다) · VERSION 0.20.111→0.20.112 (G5).
- **단위 출처만 바꾼다**: 토이 학습시각의 torch 파라미터 → **실제 ckpt**.
  ① **WEIGHTS 팔** = 로드한 `.clm` 의 **가중 텐서별 RMS**(이름정렬) — 트레이너가 하는 것과 **같은 축약**이라
  스케일 비교가 성립하는 유일한 팔. 정적 ckpt 는 **틱 1개**이므로 cliff 를 계산하지 않는다(없는 걸 만들지 않음).
  ② **DEPTH 팔** = `core/decode.clm_forward_taps`(생산 `_fwd_trunk` 를 옆에서 관측 · 새 forward 발명 금지 ·
  `a_eval_py_canonical`) 로 각 trunk 깊이의 잔차를 받아 **채널별 RMS**를 그 깊이의 unit 벡터로. 깊이 = 기질 자신의
  forward 궤적이므로 정적 ckpt 가 내주는 유일한 정직한 궤적 축.
- **팔·통제·bar·cadence 처리 전부 그대로**: 동봉 배터리(`battery_liveness`)가 **원래 bar 그대로** 먼저 돌고,
  궤적은 트레이너가 부르는 **바로 그 `summarize`** 로 흘려보낸다(재구현 금지 — 조용히 달라질 표면 제거).
- **손잡이 0개**: 플래그는 하나이고 튜닝 인자가 없다. 담체(carrier) 4개는 **동결 상수**(EN-first). H_9838 의 교훈이
  "가장 중요한 손잡이는 입력"이므로, 입력을 인자로 노출하지 않았다.
- 새로 더한 참값-0 받침대 2개(실입력 경로 관통 · **bar 는 기존 `EPS_STRUCT` 그대로**):
  `flat_units`(각 틱의 unit 을 그 틱 평균으로 → 구조 없음) · `frozen_trajectory`(**실제 틱0 unit 을 전 틱 반복** =
  실제 크기 유지·궤적만 제거 = H_9838 의 값-섞기 받침대에 대응).
- ⛔ **이름 규율(하드게이트)**: 새로 더한 것 중 `phi` 라 불리는 것은 **하나도 없다**. 진입점 이름은 트레이너가 이미
  찍는 로그 접두사 `[structure-envelope H_9846]` 를 그대로 따랐다. 기존 `--phi-envelope-monitor` 이름은 선행 모듈
  `core/phi_envelope_substrate.py` 에서 물려받은 것이며 **확장하지 않았다**.

## ⑧ 실측 — 옛 경로(회귀 0) 먼저, 그 다음 실입력

### ⑧-A 옛 경로 재현 = **회귀 0** (카드 ①②③ 과 byte-identical)

```
a599419efeff594b9cea3a47e36181cca83f517ba0d28dd5fc306668b39f8a10  /tmp/h9846/A/m.clm   (OFF)
a599419efeff594b9cea3a47e36181cca83f517ba0d28dd5fc306668b39f8a10  /tmp/h9846/B/m.clm   (ON)
210a5a18bfa032b88004b224b00c508ed304821fa59b2e7415379b343fec2b09  /tmp/h9846/A/m.clm.pt
210a5a18bfa032b88004b224b00c508ed304821fa59b2e7415379b343fec2b09  /tmp/h9846/B/m.clm.pt
  [structure-envelope H_9846] battery CERTIFIED — plant_fires=True pedestal_refuses=True discriminates_ramp=True (plant gap 0.484848 · pedestal 0 · ramp cadence-inflation 3.9663×)
  [structure-envelope H_9846 MONITOR-ONLY] step=1 dispersion=4.800336 span=3333.231415 nest_sync=0.883229 units=23
  [structure-envelope H_9846 MONITOR-ONLY] step=5 dispersion=4.793740 span=896.541719 nest_sync=0.883317 units=23
  [structure-envelope H_9846 MONITOR-ONLY] step=10 dispersion=4.298951 span=500.035936 nest_sync=0.878151 units=23
  [structure-envelope H_9846 MONITOR-ONLY] step=15 dispersion=4.293360 span=358.393034 nest_sync=0.878235 units=23
  [structure-envelope H_9846 MONITOR-ONLY] step=20 dispersion=4.288242 span=284.014784 nest_sync=0.878300 units=23
  [structure-envelope H_9846 MONITOR-ONLY] n_ticks=5 every=5 cliff_gap=0.494789 cliff_rate=0.09895785 dispersion 4.800336 → 4.288242 · self-subsample spread 0.0338 ⇒ step-like (gap cadence-robust; read cliff_gap)
  step 10 (MITOSIS SPLIT) E 2->3      ·      FINAL val_CE(pooled)=4.542315721511841  (A·B 동일)
```

sha256 4개·모니터 6줄·val_CE 전부 카드 ①②③ 과 **문자 그대로 일치**. 옛 경로 회귀 0 확인.

### ⑧-B 실입력 — `py303_full.clm` (303M · d=3784 · L=4 · E=3 · K=3)

```
[structure-envelope H_9846 · REAL-INPUT READ] ckpt=/Users/mini/anima-weights/py303_full.clm
  ① battery (UNCHANGED bars · controls first): CERTIFIED — plant_fires=True pedestal_refuses=True discriminates_ramp=True
     plant_cliff gap=0.484848 · plant_ramp gap=0.045326 · plant_flat gap=0.000000
  ② REAL WEIGHTS arm (one RMS per weight tensor · the trainer's own reduction)
     n_units=31 dispersion=4.695298 span=159.906900 nest_sync=0.852812 nest_scale=13.282918
     (a static checkpoint is ONE tick — no cliff is computed and none is invented)
  ③ REAL-INPUT ZERO-TRUTH PEDESTALS (same EPS_STRUCT=1e-09 bar as the battery)
     "a stone falls when you let it go now"   flat_units: disp=0 gap=0 · frozen_traj: disp=7.088637 gap=0
     "numbers add up when you count them a"   flat_units: disp=0 gap=0 · frozen_traj: disp=6.653807 gap=0
     "she opened the door and walked insid"   flat_units: disp=0 gap=0 · frozen_traj: disp=5.842783 gap=0
     "the sky is blue and the sea is deep"    flat_units: disp=0 gap=0 · frozen_traj: disp=6.914033 gap=0
  ④ REAL DEPTH TRAJECTORY (units = per-channel RMS at each trunk depth)
     "a stone falls when you let it go now"   n_ticks=5  dispersion 7.088637 → 7.231890 → 7.191740 → 7.202539 → 7.042421
                                              cliff_gap=0.160117 cliff_rate=0.16011715 spread_rel=0.7114  ramp-like (gap inflates with cadence; read cliff_rate)
                                              span=19.791856 nest_sync=0.387172 nest_scale=28511.957137 (depth 0)
     "numbers add up when you count them a"   n_ticks=5  dispersion 6.653807 → 6.827831 → 6.827099 → 6.753190 → 6.591020
                                              cliff_gap=0.174024 cliff_rate=0.17402393 spread_rel=0.7340  ramp-like (gap inflates with cadence; read cliff_rate)
                                              span=16.562973 nest_sync=0.399738 nest_scale=27914.063884 (depth 0)
     "she opened the door and walked insid"   n_ticks=5  dispersion 5.842783 → 6.063771 → 6.090297 → 6.066198 → 5.902873
                                              cliff_gap=0.220988 cliff_rate=0.22098820 spread_rel=0.7572  ramp-like (gap inflates with cadence; read cliff_rate)
                                              span=14.253789 nest_sync=0.407674 nest_scale=28063.099838 (depth 0)
     "the sky is blue and the sea is deep"    n_ticks=5  dispersion 6.914033 → 7.124057 → 7.036073 → 6.903618 → 6.759086
                                              cliff_gap=0.210024 cliff_rate=0.21002389 spread_rel=0.4406  ramp-like (gap inflates with cadence; read cliff_rate)
                                              span=21.599515 nest_sync=0.396805 nest_scale=27295.554010 (depth 0)
  ⑤ STRUCTURE-FREE CARRIER (one byte repeated · REPORTED, gates nothing)
     "aaaaaaaaaaaa..."                        cliff_gap=0.153819  dispersion 6.635747 → 6.789566 → 6.788327 → 6.669510 → 6.787614
  ⑥ WHERE PRODUCTION SITS between the two shipped controls
     plant_ramp 0.045326  <=  REAL depth cliff_gap [0.160117 .. 0.220988]  <=  plant_cliff 0.484848
     real/ramp=4.8756  real/cliff=0.4558  (REPORTED placement · no bar is moved)
```

(구조-없는 담체의 자가 regime 은 `spread_rel=0.0127 ⇒ step-like` — 실 EN 담체 4/4 는 전부 `ramp-like`.)

### ⑧-C 같은 축 대조군 — **토이 `.clm` 을 같은 읽기 경로로**(축을 맞춘 비교)

```
[structure-envelope H_9846 · REAL-INPUT READ] ckpt=/tmp/h9846/A/m.clm      (d=64 L=2 · ⑧-A 가 만든 그 ckpt)
  ② n_units=23 dispersion=4.287078 span=284.014781 nest_sync=0.878317 nest_scale=9.669902
  ③ flat_units disp/gap = 0 / 0 (4/4)  ·  frozen_traj gap = 0 (4/4)
  ④ "a stone falls…"  n_ticks=3  0.950114 → 1.419282 → 1.803474   cliff_gap=0.469168 spread_rel=0.4502 ramp-like
     "numbers add up…" n_ticks=3  1.157404 → 1.307196 → 1.558121   cliff_gap=0.250924 spread_rel=0.3738 ramp-like
     "she opened…"     n_ticks=3  0.963026 → 1.359071 → 1.999686   cliff_gap=0.640614 spread_rel=0.3820 ramp-like
     "the sky is…"     n_ticks=3  0.866003 → 1.465822 → 1.779081   cliff_gap=0.599819 spread_rel=0.3431 ramp-like
  ⑤ "aaaa…"           n_ticks=3  3.182826 → 4.699682 → 3.345111   cliff_gap=1.516857
  ⑥ plant_ramp 0.045326 <= REAL [0.250924 .. 0.640614] <= plant_cliff 0.484848 · real/ramp=14.1336 real/cliff=1.3213
```

## ⑨ 판독 — 무엇이 살아남고 무엇이 죽었나 (**착륙 양성 = 부분생존**)

**🟢 살아남음 (계기 자체)**

1. **배터리 CERTIFIED 그대로.** 실입력 경로에서도 `plant_cliff 0.484848` / `plant_ramp 0.045326` / `plant_flat 0`
   문자 그대로 동일.
2. **실입력 참값-0 받침대 2종이 정확히 0 을 유지** (303M·토이 모두 4/4 담체에서 `flat_units disp=0 gap=0`,
   `frozen_trajectory gap=0`). **H_9838 의 실패 양상은 여기서 재현되지 않았다** — 이 감시는 실제 표현 위에서
   구조를 **날조하지 않는다**. (단 ⑩-3 의 정직 단서를 반드시 같이 읽을 것.)
3. **손실-무관 byte-identity 재현**(⑧-A). MONITOR-ONLY 는 그대로 증명 상태.
4. **새 교차확인**: 읽기측 WEIGHTS 팔이 토이 `.clm` 에서 `dispersion 4.287078` 을 읽었고, 이는 트레이너가 메모리
   상 torch 파라미터에서 읽은 마지막 틱 `4.288242` 와 **Δ=0.001164 (0.03%)** 로 일치한다(차이 = `.clm` int4
   왕복). 완전히 다른 두 코드경로가 같은 양을 읽고 있음이 처음으로 확인됐다.

**🔻 죽었음 (착륙했던 처치 판독 ③④의 생산 일반화)**

5. **regime 이 뒤집힌다 — 카드의 헤드라인 통계량이 생산 레짐에선 취약한 쪽이다.** 토이 학습궤적은 자가게이트가
   `spread_rel 0.0338 ⇒ step-like (read cliff_gap)` 이라 했다. **틱 수를 맞춘(n_ticks=5)** 303M 실궤적은 4/4 담체가
   `spread_rel 0.4406~0.7572 ⇒ ramp-like (read cliff_rate)`. 즉 카드 ④가 자기 손으로 잡아낸 결함
   (**cliff_rate 가 19× 흔들리는 동안 cliff_gap 은 4.8% 만 움직였다**, 그리고 **`cliff_rate` 를 cadence 보정치로 본
   최초 프레이밍이 계단형에선 거꾸로였다**)은 **계단형 레짐에서만 측정된 사실**이었고, 생산 기질이 내주는
   궤적은 그 레짐에 있지 않다. **내가 읽는 양은 `cliff_gap` 이고**, 이유는 ⑧-A 의 토이 궤적이 자가게이트에서
   step-like 이기 때문이었는데 — **실기질에선 그 근거가 사라진다.**
6. **활성화(표상) 측에는 입력-구조 신호가 없다.** 303M 에서 구조-없는 1바이트 담체가 `cliff_gap 0.153819`,
   실제 EN 담체 4개가 `0.160117~0.220988` — 사전등록 bar 도 없고 n=4 이며 겹치는 범위다(분리 불가). 토이에선
   아예 **역전**한다: 널 담체 `1.516857` > 실 담체 최대 `0.640614`. ⟹ 실표현 위에서 읽히는 "구조 절벽"은
   **기질이 무엇을 처리하는가**가 아니라 **가중치의 깊이 기하**의 성질이다. 카드 ⑤-3 이 "가림 한계"라고만
   적어둔 활성화 축이 이제 **측정되었고, 그 축은 내용을 나르지 않는다**.
7. **4개 보고 통계량 중 2개는 스케일-불변이 아니다.** `nest_scale = Σunits·(1+superadd)` 는 unit 개수에 비례하고
   (토이 가중 9.669902@23 · 303M 가중 13.282918@31 · 303M 깊이 27295~28512@3784), `nest_sync = coupling/(1+var)`
   는 unit 분산에 따라 붕괴한다(0.878317 → 0.852812 → 0.387172~0.407674). ⟹ **기질/팔을 가로질러 이 둘을
   비교하는 것은 무의미**하다. 카드 ⑤-5 가 "MITOSIS 가 n_units 를 바꿀 수 있다"고 적은 것은 방향은 맞았으나
   과소평가였다 — n_units 의존성은 **비교가 아니라 통계량 자체**에 있다.
8. **부분생존한 쪽의 유일한 정량 이전**: WEIGHTS 팔의 `dispersion` 만 토이 실측 범위(4.288242~4.800336) 안으로
   들어온다(303M 4.695298). `span` 은 밖(303M 159.906900 vs 토이 284.014784~3333.231415), `nest_sync` 도 밖
   (0.852812 vs 0.878300~0.883317). 즉 **4개 중 1개만** 스케일을 건너 이전된다.

## ⑩ 정직 단서 (이 스왑이 **하지 못한** 것)

1. **틱 축이 다르다.** 토이는 *학습 스텝* 궤적, 실입력은 *forward 깊이* 궤적이다. 그러므로 ⑨-5 는
   "303M 의 **학습** 궤적이 ramp-like 다"가 **아니다** — 정확한 진술은 "정적 생산 ckpt 가 내주는 유일한 궤적에서
   자가게이트가 반대 레짐을 답한다"이며, 303M 학습-스텝 궤적의 레짐은 **미측정 OPEN**(그건 303M 학습 발사가 필요).
   그래도 카드의 주장은 좁아진다: `step-like ⇒ read cliff_gap` 은 **20-step 토이의 스텝 축에 대한 사실**이었다.
2. **이 호스트의 두 "다른" ckpt 는 같은 파일이다.** `py303_full.clm` 과 `py303_savant_mitosis.clm` 은
   **sha256 이 동일**(`013c4574e0ce71ae173287b93bb2c1ab5dd7ee6c3b53429ec898683198cd4e7c`) — 실행 출력도 완전히
   동일했다. 즉 **실기질은 1개**이며 2-기질 재현이 아니다(이름≠정체 · `hf-backup-decidable-only-by-sha256`).
3. **실입력 받침대가 0 을 지킨 것을 과대독해 말 것.** `dispersion` 은 unit 다중집합의 **순서통계**라
   **순열 불변**이다 — 배선/기하를 아무리 섞어도 이 감시는 못 본다. 따라서 `flat_units`/`frozen_trajectory`
   받침대는 구성상 **발화할 수 없는** 팔이고, 통과는 **배관 확인**이지 "기전이 실재한다"의 증거가 아니다.
   H_9838 의 값-섞기 받침대가 발화할 수 있었던 것과 대비된다. (⑨-2 를 이 문장 없이 인용하면 오독이다.)
4. **담체 n=4, 사전등록 bar 없음.** ⑨-6 의 널-담체 대조는 **보고**이지 판정이 아니다.

## ⑪ 이 반박이 막는 하류 지출

- 🚫 **303M 학습 캠페인에 이 감시를 회귀탐지로 붙이고 `cliff_gap` 을 읽는 지출**: 생산 기질이 내주는 궤적에서
  실행의 **자기 자신의 게이트**가 "gap 은 취약, rate 를 읽어라"라고 답한다. 두 수를 모두 찍으므로 판정이 뒤집히진
  않지만, **어느 쪽을 읽을지 카드가 근거로 삼았던 실측이 생산에선 성립하지 않는다** ⟹ 그 캠페인은 판독불가한
  수를 낳는다. 먼저 ⑩-1 의 OPEN(303M 학습-스텝 궤적 레짐)을 $0 로 좁히기 전엔 태우지 말 것.
- 🚫 **"더 풍부한 신호"로 활성화 탭 감시를 만드는 후속**(카드 본문이 스스로 대안으로 지목했고 byte-identity 때문에
  포기했던 그 팔): 활성화 축이 이제 **측정되었고 내용을 나르지 않는다**(⑨-6). 만들기 **전에** 반박됐다 —
  byte-identity 를 포기하면서까지 얻을 신호가 거기 없다.
- 🚫 **서로 다른 스케일/팔 사이에서 `nest_sync`·`nest_scale` 을 비교하는 모든 판독**(⑨-7).

## ⑫ 사전등록 후속 (설계만 — **실행하지 않음** · 구조자 사냥 금지)

착륙 양성을 되살릴 길이 있다면 **입력을 뒤지는 게 아니라** 다음 두 개뿐이며, 둘 다 별도 H 로 사전등록해야 한다
(id 는 병렬 레인 G6 충돌을 피해 등록 시점에 부여):

1. **303M 학습-스텝 궤적 레짐 측정** — pool 에서 303M 을 짧게 warm-start 학습하며 `--phi-envelope-monitor on
   --phi-monitor-every N` 을 켜고, 실행이 자기 자신에 대해 내는 `regime`/`cliff_gap_spread_rel` 을 사전등록
   DV 로 읽는다. 예측(사전등록): 토이가 step-like 였던 것이 **스텝 수 20 과 MITOSIS 1회**라는 축의 성질이라면
   303M 도 step-like 여야 하고, 토이 세계의 성질이었다면 ramp-like 여야 한다. 지출: 303M 짧은 학습 1회.
2. **두 통계량의 스케일-정규화** — `nest_scale`/`nest_sync` 를 n_units·분산에 대해 정규화한 형태로 **새로**
   등록하고, 정규화 전/후가 배터리 3팔의 판정을 **바꾸지 않는지** 먼저 증명한다(bar 이동 금지). 이건 계기 수리이지
   판정 되살리기가 아니다.

⛔ 하지 **않는 것**: 받침대가 거부할 때까지 dim/seed/threshold 를 뒤지는 것(= tune-to-green, 금지).

## 재현 명령 (실입력 · 그대로 복사 가능)

```bash
python3 -m venv /tmp/venv_h9846r && /tmp/venv_h9846r/bin/pip install -q torch numpy
/tmp/venv_h9846r/bin/pip install -q --force-reinstall --no-deps .        # 이 워크트리
# ⑧-A 옛 경로(회귀 0) = 위 "재현 명령" 블록 그대로
# ⑧-B 실입력
/tmp/venv_h9846r/bin/anima-py evaluate /Users/mini/anima-weights/py303_full.clm \
      --structure-envelope-read --out /tmp/h9846/real_full.json
# ⑧-C 같은 축 토이 대조
/tmp/venv_h9846r/bin/anima-py evaluate /tmp/h9846/A/m.clm \
      --structure-envelope-read --out /tmp/h9846/real_toy.json
```

## 사전등록 준수

- `positive-control-before-reading-a-negative` — 양성통제 먼저, 미인증이면 값 0개.
- `phi-estimator-needs-zero-truth-pedestal` — 참값 0 받침대(구조 없는 입력) 실측 `0.0` 확인 후에만 값 판독.
- `a_train_inline_gauge` / p7 — 손실 투입 금지, byte-identity 로 증명.

- `a_toy_scale_recheck` / `a_scale_honest_scope` — ⑥~⑫ 가 바로 이 조항의 집행이다: 토이 검증은 종결이 아니고,
  지표는 그 스케일에 묶인다.

**related:** H_9845 · H_9835 · H_9844(같은 통제-우선 계기 idiom) · **H_9838**(실입력 스왑을 요구한 선례 —
심어둔 기하가 헤드라인 양성을 만들었다)
