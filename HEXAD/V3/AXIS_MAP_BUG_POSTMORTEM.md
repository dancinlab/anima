# AXIS_MAP-FAN env-var-concat anti-pattern postmortem 2026-05-23

## § Header

7-axis AXIS_MAP-FAN fan-out (commit `df3e8e06e`, 2026-05-23 14:10 KST)이 caller-side env-var-concat anti-pattern 으로 인해 여러 차례 launch 직후 crash. dispatcher 자체는 무결, caller (인간/agent)가 P21H_* 환경변수를 단일 quoted string 으로 묶어 전달한 것이 root cause. 본 문서는 chronology · bug signature · 증거 verbatim · `.envbug` 디렉토리 인벤토리 · fix scope · 비용 · lesson 을 기록한다.

## § Chronology

| # | UTC | KST | Event |
|---|-----|-----|-------|
| 1 | 2026-05-22 19:34Z | 2026-05-23 04:34 | 1st fan-out (all 7 axes); pods launch crash with `train_p21h_v3.py: error: unrecognized arguments: P21H_BSZ=2 ...` |
| 2 | 2026-05-22 19:41Z | 2026-05-23 04:41 | refire attempt (commit `df3e8e06e` 동일 caller pattern, 동일 bug) |
| 3 | 2026-05-22 21:21Z | 2026-05-23 06:21 | F axis 만 별도 pod 에서 우연히 통과 (early-stop @ 671s wall, FAIL n_strong=0) |
| 4 | 2026-05-23 04:11Z+ | 2026-05-23 13:11+ | 2nd attempt fan-out; `A/B/F.envbug_1779511267` dirs 생성됨, 동일 argv crash |
| 5 | 2026-05-23 04:41Z-06:22Z | 2026-05-23 13:41-15:22 | A/B/F refresh dir 에서 결과 산출 (FAIL but with results); C/C2/D/E pods 는 동일 argv bug 로 idle/crashed |
| 6 | 2026-05-23 11:00Z+ | 2026-05-23 20:00+ | 현 session start, 7 pod 발견 (6 p21h-v3 idle + 1 p21m-v12 active) |
| 7 | 2026-05-23 11:30Z | 2026-05-23 20:30 | 6 dead pods kill (5 crashed-still-running C/C2/D/E + idle B/A post-completion); forensic logs → `state/p21h_v3_launcher_failure_2026_05_23/` |
| 8 | 2026-05-23 13:21Z | 2026-05-23 22:21 | cycle 1 redispatch C/C2/D/E (correct inline env vars); A/B 결과 보존, F 별도 pod 보존 |

## § Bug signature

### WRONG (caller-side anti-pattern)

```bash
# 단일 quoted string 으로 묶어서 전달 → shell 이 P21H_STEPS 하나의 값으로 인식
P21H_STEPS="5000 P21H_BSZ=2 P21H_BLOCK=512 P21H_LR=5e-5 P21H_WARMUP=100 \
P21H_WIKI_FRAC=0.5 P21H_CORPUS_MB=72 P21H_NOISE_SIGMA=0.1 \
P21H_LAMBDA_MITOSIS=0.0 P21H_MITOSIS_MAX=16 P21H_CKPT_EVERY=500 \
P21H_CKPT_OSC_THRESHOLD=0.5 P21H_CKPT_OSC_WINDOW=10 \
P21H_EARLY_STOP_PATIENCE=8 SAVE_POD=1" \
  bash dispatch_p21h_v3_runpod.sh ...

# dispatcher 내부:
#   python train_p21h_v3.py --steps $P21H_STEPS ...
# 전개되면:
#   python train_p21h_v3.py --steps 5000 P21H_BSZ=2 P21H_BLOCK=512 ...
# argparse 가 `P21H_BSZ=2` 를 미인식 인자로 처리 → error
```

### CORRECT (each var as separate inline assignment)

```bash
# 각 P21H_* 를 별도 inline assignment 로, embedding 없이
P21H_STEPS=5000 \
P21H_BSZ=2 \
P21H_BLOCK=512 \
P21H_LR=5e-5 \
P21H_WARMUP=100 \
P21H_WIKI_FRAC=0.5 \
P21H_CORPUS_MB=72 \
P21H_NOISE_SIGMA=0.1 \
P21H_LAMBDA_MITOSIS=0.0 \
P21H_MITOSIS_MAX=16 \
P21H_CKPT_EVERY=500 \
P21H_CKPT_OSC_THRESHOLD=0.5 \
P21H_CKPT_OSC_WINDOW=10 \
P21H_EARLY_STOP_PATIENCE=8 \
SAVE_POD=1 \
  bash dispatch_p21h_v3_runpod.sh ...
```

dispatcher (`tool/dispatch_p21h_v3_runpod.sh` lines 21+, `nohup env $AXIS_ENV $CMD` 패턴)는 처음부터 정상이며 변경 없음.

## § Quoted verbatim evidence

### BUGGY caller (axis A, dispatch.log line 5)

`HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21H_axis_A.envbug_1779511267/dispatch.log`:

```
    steps=5000 P21H_BSZ=2 P21H_BLOCK=512 P21H_LR=5e-5 P21H_WARMUP=100 P21H_WIKI_FRAC=0.5 P21H_CORPUS_MB=72 P21H_NOISE_SIGMA=0.1 P21H_LAMBDA_MITOSIS=0.0 P21H_MITOSIS_MAX=16 P21H_CKPT_EVERY=500 P21H_CKPT_OSC_THRESHOLD=0.5 P21H_CKPT_OSC_WINDOW=10 P21H_EARLY_STOP_PATIENCE=8 SAVE_POD=1 bsz=2 block=512 lr=5e-5 warmup=100
```

→ `steps=5000` 뒤에 모든 `P21H_*=...` token 이 그대로 echo 됨. dispatcher 의 echo-header 가 `--steps $P21H_STEPS` 전개를 그대로 노출.

### CLEAN caller (axis C, cycle 1 redispatch fire log)

`HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/.logs/axis_redispatch_20260523_222135/fire_C.log`:

```
    steps=5000 bsz=2 block=512 lr=5e-5 warmup=100
```

→ `steps=5000` 단일 token, 나머지 `bsz`/`block`/`lr`/`warmup` 은 별도 derived echo line. argparse 정상 처리.

## § `.envbug` dir inventory

총 7 dirs across 2 timestamps + 1 forensic state dir.

### 13:33-13:37 KST rename (1st second-attempt failure)

```
HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21H_axis_A.envbug_1779511267/  (drwxr-xr-x  5 dirs  2026-05-23 13:36)
HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21H_axis_B.envbug_1779511267/  (drwxr-xr-x  5 dirs  2026-05-23 13:36)
HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21H_axis_F.envbug_1779511267/  (drwxr-xr-x  5 dirs  2026-05-23 13:37)
```

### 22:21 KST rename (current session, before cycle 1 redispatch)

```
HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21H_axis_C.envbug_no_result_1779542469/   (drwxr-xr-x  6 dirs  2026-05-23 15:04)
HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21H_axis_C2.envbug_no_result_1779542469/  (drwxr-xr-x  6 dirs  2026-05-23 15:04)
HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21H_axis_D.envbug_no_result_1779542469/   (drwxr-xr-x  6 dirs  2026-05-23 15:04)
HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21H_axis_E.envbug_no_result_1779542469/   (drwxr-xr-x  6 dirs  2026-05-23 15:04)
```

`_no_result_` 접미사 = pod 가 crash 했으나 idle 상태로 계속 떠 있어 dispatch artifact 만 남고 train 결과 없음을 표기.

### Forensic state dir (pulled this session)

```
state/p21h_v3_launcher_failure_2026_05_23/
├── launcher_A_6trdcwmuyvcc2d.sh   (1302 B)
├── launcher_B_e6llutuugqjxr4.sh   (1302 B)
├── launcher_C_k8t6btduwnrvqi.sh   (1302 B)
├── launcher_D_kh3eivyxmfr7l0.sh   (1302 B)
├── launcher_E_rcvbuv3b6thi3q.sh   (1302 B)
├── launcher_F_ztlzsckn9uppwt.sh   (1302 B)
├── train_A_6trdcwmuyvcc2d.log     (4279 B)
├── train_B_e6llutuugqjxr4.log     (8449 B)
├── train_C_k8t6btduwnrvqi.log     (4279 B)
├── train_D_kh3eivyxmfr7l0.log     (4279 B)
├── train_E_rcvbuv3b6thi3q.log     (4279 B)
└── train_F_ztlzsckn9uppwt.log     (8856 B)
```

6 train.log + 6 launcher.sh, 본 session 20:30 KST 에 6 dead pod kill 직전 pull.

## § Fix scope

| Layer | 조치 | 상태 |
|-------|------|------|
| Caller side | PR #204 — `dispatch_p21h_v3_runpod.sh` 21-36 lines 에 `# CALLER WARNING` block 추가 (WRONG vs CORRECT 예시 inline) | LANDED |
| Caller demo | cycle 1 redispatch (22:21 KST) C/C2/D/E 가 correct inline env-var separation 으로 training in-flight; clean fire log = 본 문서 § evidence | LANDED |
| Dispatcher | `nohup env $AXIS_ENV $CMD` (lines 21+) 변경 없음 — 처음부터 정상 | UNCHANGED |
| Forensic 보존 | `.envbug` 7 dir rename + `state/p21h_v3_launcher_failure_2026_05_23/` 12 files pull | LANDED |
| 본 postmortem | `HEXAD/V3/AXIS_MAP_BUG_POSTMORTEM.md` (현 문서) | LANDED (this PR) |

## § Cost

| 항목 | 비용 | 근거 |
|------|------|------|
| 1st/2nd fan-out 낭비 (7 axes × 평균 ~$1.15) | ~$8 | kill 전까지 idle/crashed pods 의 GPU-hour billing |
| cycle 1 redispatch (C/C2/D/E 4 axes × ~$1.5) | ~$6 | A100-SXM4-80GB SECURE cloud, early-stop patience=8 가정 |
| **Saga total** | **~$14** | — |

## § Lessons

- **Multi-var env-set 은 shell trap 이지 framework bug 가 아니다.** dispatcher `nohup env $AXIS_ENV $CMD` 패턴은 무결, caller 가 `P21H_STEPS="5000 P21H_BSZ=2 ..."` 처럼 단일 quoted string 으로 묶은 것이 원인. fix 는 caller 의 inline assignment 분리뿐, dispatcher 측 방어는 false-positive 위험 (정상 multi-token steps spec 차단) 이 더 크다.
- **Archive rename (`.envbug_<unix_ts>` / `.envbug_no_result_<unix_ts>`) 가 forensic trail 을 보존한다.** 원본 디렉토리를 삭제 대신 timestamped 접미사로 rename 하면 동일 axis 재발사 시 충돌 없이 재현 가능하며, 본 postmortem 같은 사후 분석에서 dispatch.log line 5 verbatim 비교가 가능해진다.
- **Dispatcher 의 echo-header 가 caller bug 를 조기 노출한다.** `dispatch.log` line 5 의 `steps=5000 P21H_BSZ=2 ...` echo 는 launch 직후 (pod create 전) 출력되어 argparse error 보다 빠르게 caller 측 quoting 오류를 식별 가능. 향후 dispatcher 는 이 echo 를 stderr 로 미러 + token count assertion (`P21H_*` token count > 1 in `--steps`) 추가 검토 여지.
