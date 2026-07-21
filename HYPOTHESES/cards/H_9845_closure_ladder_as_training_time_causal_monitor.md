# H_9845 — 개입형 폐쇄사다리를 학습 중 인과 모니터로 (R12-8 · MONITOR-ONLY · 손실 투입 금지)

**status:** 🔧 WIRED-INSTRUMENT (계기 착륙 + 손실-무관 증명 완료 · **과학 판정 0** · MONITOR-ONLY)
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

**related:** H_9805 · H_9807 · H_9835 · H_9844 · H_9846
