# H_9840 — 5단계 수면 스케줄(Process-S/C)을 학습 커리큘럼으로 쓴다 (R12-3)

**status:** 🟡 계기 착륙 완료 · 과학 판정 0 (R12 · **DIRECTIONAL**)
**source:** R12 뇌부위 census (2026-07-21) — `origin/main` `core/` 12개 모듈 실측 후 1모듈=1레버로 등록.
상위 설계 노드 = ARCHITECTURE `C2 RECOMBINE` 아래 `🧠 뇌부위 census` → `📋 R12`. R11(H_9830~9836)의 후속.
**wired:** yes — `anima-py train --sleep-schedule {off,dream-lib,fixed-alternating}` (기본 `off` = byte-identical 실측)

## 실측 (전제 재검증 — 카드 작성 전 `origin/main` 에서 직접 읽음)

`core/dream_lib.py`(123줄) **전제 유지, 철회 없음**. 90-tick 세션 · WAKE/N1/N2/N3/REM 5단계 ·
`dr_n_ticks`(=90) `dr_stage_at` `dr_stage_name` `dr_stage_size` `dr_mitosis_prior`
`dr_imagination_active` `dr_emit_envelope` `dr_density` `dr_ratio_sleep_wake` +
Process-S(`sp_pressure_wake`/`sp_pressure_sleep`/`sp_pressure_at`, 아데노신 build/clear via
`math.exp`) · Process-C(`sp_circadian_bias`) · `sp_sleep_propensity`. **숫자만 반환하고 bool
게이트 0**(p5). 학습측 소비자는 **0개**였다(유일 소비자 = `cli/chat.py` 데몬) — 이 카드가 첫 소비자.

## 가설

이 모듈은 이미 **혼합비 스케줄러의 형태**를 하고 있다. 학습 스텝의 각성/수면 위상을 하드코딩
상수가 아니라 기질 자신의 세션표에서 뽑으면 교대가 기질 사실이 된다(p5·`a_autonomy_over_hardcode`).

## 배선한 것 (cli/train.py)

```
anima-py train --sleep-schedule {off,dream-lib,fixed-alternating}
               [--sleep-ticks 90] [--sleep-replay-cap 4096]
anima-py train --sleep-selftest N [--sleep-ticks 90]     # $0 · 모델·코퍼스·디바이스 0
```

| arm | 실체 |
|---|---|
| `off` (기본) | 스케줄 객체·리플레이 버퍼·생성기 자체를 만들지 않음 ⟹ 무플래그와 **byte-identical** |
| `dream-lib` | 위상 = `dr_stage_at(tick)`, dream_lib 자신의 순서 — 긴 WAKE 뭉치 뒤 N1→N2→N3→REM 통합 수면 뭉치 |
| `fixed-alternating` | **핵심 통제** — **같은 stage multiset**(비율도 단계별 개수도 동일 · 구성상 순열)을 고르게 흩뿌림. 1-변수 = **시간적 배치**뿐 |

SLEEP 스텝은 fresh 코퍼스 대신 **각성 중 소비한 window 를 리허설**한다(`core/imagination_replay.py`
의 working-ring 리허설을 학습측으로 읽은 것). 깊은 단계(N3/REM · `dr_imagination_active==1`)는
버퍼 전체를, 얕은 단계(N1/N2)는 최근 1/4 만 재생. 시작 시 arm 을 **반드시 announce**
(H_9805 `--tension-field` 선례 — 조용한 arm 은 통제런이 처치런으로 오독되는 경로).

## 재현 명령 (전부 격리 venv `/tmp/venv_h9840`, `pip install --no-deps .`)

```bash
python3.12 -m venv /tmp/venv_h9840
/tmp/venv_h9840/bin/pip install "numpy>=1.24" "torch>=2.1,<2.13"
/tmp/venv_h9840/bin/pip install --force-reinstall --no-deps .

# ① $0 스케줄 셀프테스트 (통제 먼저)
/tmp/venv_h9840/bin/anima-py train --sleep-selftest 90 --sleep-ticks 90

# ② off 의 byte-identity + 3-arm 분리 (toy CPU 학습 4회)
COMMON="--corpus /tmp/h9840_corpus.txt --d 32 --L 2 --seq-len 64 --steps 90 \
        --batch-size 4 --no-mitosis --skip-inline-rho --device cpu"
anima-py train $COMMON --out noflag.clm
anima-py train $COMMON --sleep-schedule off --out off.clm
anima-py train $COMMON --sleep-schedule dream-lib        --sleep-ticks 90 --out dreamlib.clm
anima-py train $COMMON --sleep-schedule fixed-alternating --sleep-ticks 90 --out fixedalt.clm
shasum -a 256 noflag.clm off.clm dreamlib.clm fixedalt.clm
```

## 통제 (동결 순서 — 통제가 인증 안 되면 arm 행을 아예 보고하지 않음 · `run_mi_screen` 패턴)

**① 계기 통제** (실측 · exit 0 · `status: CERTIFIED`)

| 통제 | 요구 | 실측 |
|---|---|---|
| `plant_bout` (양성) | **발화** — 심어둔 기하(60 WAKE 뒤 30 N3)를 정확히 복원 | fired **true** — sleep_ratio 0.3333333333333333 · n_sleep_bouts **1** · max_sleep_bout **30** · max_wake_bout **60** (심은 참값과 완전일치) |
| `null_all_wake` (참값 0 받침대) | **거부** — 수면이 아예 없는 스트림 | refused **true** — sleep 0 · n_sleep_bouts 0 · max_sleep_bout 0 · sleep_ratio 0.0 |

**② arm 게이트** (tick 스윕 전 구간 · 실측)

| ticks | hamming(dream-lib, fixed-alt) | multiset 일치 | dream-lib ratio/bouts/max | fixed-alt ratio/bouts/max |
|---|---|---|---|---|
| 30 | 16 | ✅ | 0.3333 / 1 / 10 | 0.3333 / 8 / 2 |
| 45 | 24 | ✅ | 0.3333 / 1 / 15 | 0.3333 / 9 / 3 |
| 90 | 48 | ✅ | 0.3333 / 1 / 30 | 0.3333 / 17 / 3 |
| 180 | 91 | ✅ | 0.3333 / 1 / 60 | 0.3333 / 34 / 3 |

⟹ 어떤 tick 에서도 두 arm 은 **비율·단계혼합이 같고 배치만 다르다**. `separation_all_ticks: true`
`multiset_match_all_ticks: true` ⟹ **CERTIFIED**.

**③ 실현된 시퀀스** (`--sleep-ticks 90` · 학습런 로그에서 verbatim)

```
dream-lib        : WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW111111111122222222223333333RRR
fixed-alternating: WWW12W3WWWWW12WRWWW3WW12WWWWWW123WWWWWW12WWW3RWWW12WWWWWW312WWWWWW12WW3WWWRW12WWWWW3W12WWW
cycle_meter      : 양쪽 다 wake=60 sleep=30 stages={WAKE:60,N1:10,N2:10,N3:7,REM:3}
                   max_sleep_bout: dream-lib 30 vs fixed-alternating 3   ← 유일한 차이축
realized(90step) : 양쪽 다 wake=60 sleep=30 replay_batches=30 warmup_fresh=0
Process-S pressure[0:8]   = [0.0, 0.032784, 0.064493, 0.095163, 0.124827, 0.153518, 0.181269, 0.20811]
Process-S/C propensity[0:8]= [0.0, 0.024115, 0.047585, 0.070431, 0.092674, 0.114333, 0.135428, 0.155977]
```

**④ `off` byte-identity + arm 실효성** (실 학습 4회 · sha256 실측)

```
54e6d9175162e78f68e44728cc0024815b75e6e0744eab2ed3da5786bcfe6d98  noflag.clm
54e6d9175162e78f68e44728cc0024815b75e6e0744eab2ed3da5786bcfe6d98  off.clm      ← 완전일치
9ac83de230f2ded03f16d58b4a4d4df115f5e36c2652e049d076e0f43af8d726  dreamlib.clm ← 다름
13316cf76edafcb795b09f03d9c8c079ea891ce0475410ddd54c54833212b7ca  fixedalt.clm ← 다름(서로도 다름)
```
⟹ `off` 는 진짜 no-op 이고, 두 처치 arm 은 **조용히 무시되지 않는다**.

## 🔻 자가적발 결함 + 그에 대한 게이트 (no tune-to-green)

**`--steps` 하나로 판정이 뒤집힌다.** dream-lib 은 WAKE 를 앞쪽에 몰아넣으므로
`--steps 12 --sleep-ticks 90` 이면 **realized** sleep_ratio 가 dream-lib **0.0000** vs
fixed-alternating **0.2500** — "비율 맞춘 통제"가 비율이 안 맞고, 어떤 Δ 든 배치 Δ 의 탈을 쓴
**비율 Δ** 가 된다(셀프테스트 `steps_alignment` 실측값). cycle 비율은 구성상 같지만 그 등식을
실현런으로 옮기려면 **온전한 세션 수**가 필요하다.
⟹ 트레이너가 `steps % sleep_ticks != 0` 을 **하드 거부**한다(실측 exit 1):

```
[sleep-schedule] --steps 30 is not a whole multiple of --sleep-ticks 90. A partial session
realizes DIFFERENT wake/sleep ratios in the two arms (dream-lib front-loads WAKE), which
un-matches the control and turns an arrangement contrast into a ratio contrast. ...
```
정렬된 `--steps 90 --sleep-ticks 90` 에서는 `realized_sleep_ratio {dream-lib: 0.3333…,
fixed-alternating: 0.3333…}` · `realized_ratio_matched: true`.

## 정직한 범위 · 한계 (판정 아님)

- **여기 있는 수치는 전부 계기 수치다. 학습 이득 주장 0.** toy 4회(d=32·L=2·90 step·seed 7·
  272KB 무작위-단어 코퍼스·CPU)의 `lossF`/`val_CE`(off 3.4781 · dream-lib 3.4839 ·
  fixed-alternating 3.4723)는 **배관이 살아있다**는 것 외에 아무 것도 말하지 않는다 —
  single-seed · 토이 · 구조 없는 코퍼스. 이 숫자로 arm 을 비교하는 것은 금지.
- **선후 종속(카드 원문 유지):** 이 레버는 **H_9833(sleep-consolidate)에 종속**이다. 지금 SLEEP
  스텝은 이미 본 window 를 **재표집**할 뿐 — 증류 목적함수가 없으므로 consolidation 이 아니다.
  증류할 것이 없으면 스케줄도 없다. H_9833 이 먼저 양성이어야 이 카드가 의미를 갖는다.
- 스케줄은 **효과크기가 작은 축**이다(순서·비율은 통상 2차 요인). 303M 발사는 미실행이며,
  H_9808 게이트가 요구하는 방향증거를 이 착륙이 제공하지 않는다.
- `--sleep-replay-cap` 는 아직 실측 sweep 이 없다(기본 4096). cap 이 결론을 움직일 수 있는지는
  **미측정** — 본측정 전 sweep 필요.
- 카드 원문의 "위상 셔플" arm 은 착륙하지 않았다. `fixed-alternating` 이 이미 multiset 고정 ·
  배치만 변경이라 그 역할을 겸한다.

**related:** H_9833 (선결) · H_9841 · H_9831 · H_9805 (arm announce 선례) · H_9844 (통제-우선 패턴)
