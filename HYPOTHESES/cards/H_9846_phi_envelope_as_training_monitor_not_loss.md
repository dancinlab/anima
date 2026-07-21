# H_9846 — 구조-봉투(Φ-봉투) 층을 학습 회귀 감시로 (R12-9 · MONITOR-ONLY · 손실 투입 금지)

**status:** 🔧 WIRED-INSTRUMENT (계기 CERTIFIED · 손실-무관 byte-identical 증명 · **과학 판정 0**)
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

## 사전등록 준수

- `positive-control-before-reading-a-negative` — 양성통제 먼저, 미인증이면 값 0개.
- `phi-estimator-needs-zero-truth-pedestal` — 참값 0 받침대(구조 없는 입력) 실측 `0.0` 확인 후에만 값 판독.
- `a_train_inline_gauge` / p7 — 손실 투입 금지, byte-identity 로 증명.

**related:** H_9845 · H_9835 · H_9844(같은 통제-우선 계기 idiom)
