# PREFIRE WIRING-AUDIT CHECKLIST — silent-bypass family 재발 방지

**작성일**: 2026-05-24
**위치**: `HEXAD/PURE/PREFIRE_WIRING_AUDIT_CHECKLIST.md`
**도입 계기**: H_254 (n_kv_head 단일 silent-drop) + H_257 (axis env-var family silent-bypass) — wiring-integrity family. 두 가설 모두 발사 후 사후 발견 — prefire-audit 자동화 시 발견 비용 ~$0.

---

## 0. 목적

GPU fire 발사 전 **dispatcher env-var ↔ train script consumption** 매핑이 일치하는지 매번 확인해 silent-bypass (env-var 가 dispatcher 에 정의되어 있으나 train script 가 읽지 않거나, 다른 이름으로 읽거나, default override 로 무시되는 경우) 를 사전에 잡는다. 7-pod fan-out 이 trivial 2-config 반복으로 collapse 되는 R8 saga 류 measurement-integrity artifact 를 1회만 발생시키지 않는다.

**Scope**: GPU/runpod fan-out 이상 cost-bearing fire 전체 (단일 pod smoke 는 권고, 자연실험 fan-out 은 의무).

**Non-scope**: ckpt resume / pure inference (silent-bypass 위험 낮음).

---

## 1. 5-step audit

### Step 1 — env-var grep (dispatcher vs train script 양쪽)

dispatcher 가 export / 전달 / passthrough 하는 env-var list 를 추출하고, train script 가 실제로 `os.environ` / `getenv` / argparse 로 읽는 식별자 list 를 추출한다.

```bash
# dispatcher env-var 정의 (export 또는 --<arg>)
grep -nE '(export +|--)(P21H_|R8_|HEXAD_)' launchers/dispatch_<name>.hexa
# → 예: P21H_CURRICULUM, P21H_DISTILL, P21H_HEAD_G_DIM, ...

# train script env-var consumption (Python lane)
grep -nE 'os\.environ(\.get)?\[?["'"'"']P21H_|getenv\(["'"'"']P21H_|--p21h_' train/p21h_v3.py
# → 예: P21H_NOISE, P21H_LR, ...
```

**Expected**: 두 list 의 SET intersection ≥ dispatcher export count (모두 wired). 차집합 (dispatcher 만 정의) = 즉시 silent-bypass 후보.

### Step 2 — dispatcher passthrough (env-var 가 child process 까지 전달)

dispatcher 가 `bash -c "$CMD"` / `runpodctl exec` / `vastai create instance` 안에서 env-var 를 export 또는 `--<arg>` 로 명시적으로 child 까지 전달하는지 검사.

```bash
# nohup / ssh / docker run 안에 env-var 가 inline 으로 들어가는지
grep -nE '(nohup|ssh|docker run|bash -c).+P21H_' launchers/dispatch_<name>.hexa
# 또는 dispatcher 가 .env file 을 생성해서 source 하는지
grep -nE '\.env|env_file' launchers/dispatch_<name>.hexa
```

**Expected**: dispatcher export 된 var 가 (a) child shell 의 env 에 inherit 되거나 (b) `--<arg>` 로 명시 전달되거나 (c) `.env` file 로 source 됨. (b) 가 가장 robust (자기서술적), (a) 는 ssh `-o SendEnv` / `AcceptEnv` 가 fragile.

### Step 3 — wiring matrix (M-of-N 매트릭스 작성)

| env-var (dispatcher) | step1 grep hit (train) | step2 passthrough | wired? |
|----------------------|------------------------|-------------------|--------|
| P21H_CURRICULUM      | (none)                 | env-inherit       | ✗ silent-bypass |
| P21H_DISTILL         | (none)                 | env-inherit       | ✗ silent-bypass |
| P21H_NOISE           | line 47 os.environ     | env-inherit       | ✓      |

**M-of-N**: M wired / N defined. M < N 이면 silent-bypass 발견. R8 saga 의 경우 1/7 wired 였다.

### Step 4 — byte-equal pre-fire (동일 config 2-pod dry-run)

같은 env-var 세팅으로 2개 pod 에 PROBE_STEPS=10 dry-run 을 발사하고 결과 byte-equal 을 검증한다. 일치하면 RNG seed propagation OK + 자연실험 분리 lever 가 됨. 불일치하면 host noise (GPU class / driver / nccl) 가 dominant.

```bash
# 동일 config 발사
hexa run launchers/dispatch_<name>.hexa --probe-steps 10 --pod-id A &
hexa run launchers/dispatch_<name>.hexa --probe-steps 10 --pod-id B &
wait

# 결과 byte-equal
shasum state/<name>/probe_A/init_metrics.json state/<name>/probe_B/init_metrics.json
# → 두 hash 가 byte-equal 이어야 함 (RNG seed identical 검증)
```

**Expected**: init_metrics.json byte-equal (random init 단계 결정론). 천이가 다르면 step3 wiring matrix 가 거짓 PASS (env-var 가 도착했지만 다른 layer 에서 silent override). False negative source: GPU class differing (H100 vs A100 cuBLAS kernel 차이 → bit-level drift). 같은 GPU class 권고.

### Step 5 — runtime assertion (선택, train script 1줄)

train script 첫줄에 expected env-var sentinel assertion 을 추가해 production 발사가 silent-bypass 로 흘러가는 것을 hard-fail 시킨다.

```python
# train/p21h_v3.py 상단
import os
_EXPECTED = ['P21H_NOISE', 'P21H_LR', 'P21H_CURRICULUM']  # wiring matrix 의 wired axis
_missing = [k for k in _EXPECTED if k not in os.environ]
assert not _missing, f"prefire-audit: missing env-var {_missing}"
```

또는 dispatcher 가 sentinel marker (e.g. `P21H_AUDIT_OK=1`) 를 강제 export 하고 train script 가 그 marker 부재 시 abort.

---

## 2. 자동화 권고

후속 PR 에서 `tool/prefire_audit.sh` (또는 `tool/prefire_audit.hexa`) 한 줄 진입점을 만들어 step1-4 를 자동 실행한다. 권장 signature:

```
tool/prefire_audit.sh <dispatcher.hexa> <train_script.py>
# 출력: M-of-N wiring matrix + byte-equal verdict + GO/NO-GO
```

step5 runtime assertion 은 train script 별 maintainer 가 의무화한다 (CI 가 아닌 코드 level).

---

## 3. project.tape 권고 (별도 또는 같은 PR — g17 user-request 게이트)

본 checklist 가 채택되면 project.tape 에 다음 directive 추가 권고 (user 가 명시적으로 승인할 때만 추가):

```
@D a_prefire_wiring_audit := "cost-bearing fire 전 wiring-audit 의무" :: governance [required active]
  do   = "GPU/runpod fan-out 발사 전 PREFIRE_WIRING_AUDIT_CHECKLIST 5-step 통과 (자동화: tool/prefire_audit.sh) · M-of-N matrix M < N 시 발사 보류"
  dont = "wiring matrix 미작성으로 fan-out 발사 · silent-bypass 발견 후 saga reframing 사후 처리"
```

cross-ref: `a_fire_autonomous` (fire 자율 발사 권리) × `a_runpod_inbox` (runpod 트러블 hexa-lang inbox 회수) 의 중간 위치 — 발사 전 단계.

---

## 4. Honest C3 (≥3)

- **C1 — 채택 의존성**: prefire-audit 자체가 새로운 surface — checklist 가 채택되지 않거나 자동화 (`tool/prefire_audit.sh`) 가 만들어지지 않으면 manual 5-step 의 dev velocity 부담이 fire latency 를 늘려 도리어 우회될 수 있다. 권고: step1-3 만 minimal 의무화하고 step4-5 는 자연실험 fan-out 한정.
- **C2 — byte-equal false negative (GPU class)**: step4 byte-equal pre-fire 가 H100 vs A100 같은 다른 GPU class 환경에서 false negative 가능 (cuBLAS kernel 차이 → bit-level drift). 같은 GPU class 권고로 mitigate 하나 cluster pressure (가용 GPU 부족) 시 동일 class 2-pod 확보가 비용/대기 증가.
- **C3 — runtime assertion trade-off**: step5 runtime assertion 이 train script 에 의무화되면 dev velocity vs safety trade-off. 새 axis 추가 시 `_EXPECTED` list 도 업데이트해야 하는 ergonomic 부담, 잊으면 거짓 abort. 대안: dispatcher 가 sentinel marker 만 강제하고 train script 는 marker 부재 시 warn-only.
- **C4 — base rate sample 제한**: H_254 + H_257 sibling family 가 R8 saga 한정 sample 이라 prefire-audit 의 general efficacy 는 아직 측정 안 됨 — Wave saga / LoRA train script 별도 audit 결과로 base rate 보강 필요.

---

## 5. Cross-ref

- [`R8_SAGA_REFRAMING_2026_05_24.md`](./R8_SAGA_REFRAMING_2026_05_24.md) — H_257 발견 saga, 7-pod fan-out 이 1/7 wired 였던 원인 분석
- [`R8A_VS_R8A2_BYTE_EQUAL_NATURAL_EXPERIMENT.md`](./R8A_VS_R8A2_BYTE_EQUAL_NATURAL_EXPERIMENT.md) — H_254 falsifier byte-equal probe framework
- [`R8C_PROBE_VERDICT_2026_05_24.md`](./R8C_PROBE_VERDICT_2026_05_24.md) — H_254 F-WIRE-3 BYTE-EQUAL-INERT (wiring lever 가 init_CE 차원에서 inert)
- `/gap` skill F4 lens (assumption-surfacing top priority) — 본 checklist 가 F4 의 운영 산출물
