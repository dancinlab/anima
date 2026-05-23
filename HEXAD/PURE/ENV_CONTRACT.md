# HEXAD/PURE — ENV_CONTRACT (SSOT)

PURE closure launcher + dispatch + train 모듈이 공유하는 환경 변수 ·
디렉터리 · 런처 인자 · 출력 산출물 계약. 본 문서는 **계약** 이며
런처/dispatcher 가 본 문서와 어긋날 경우 launcher 측을 우선 수정한다
(읽기 SSOT).

관련: `HEXAD/PURE/launchers/_common.hexa` (sister code SSOT).

---

## 1. 환경 변수

| 변수 | 필수 | 기본값 | 사용처 |
|------|------|--------|--------|
| `RUNPOD_API_KEY` | 🔴 | (없음 → fail) | dispatch — pod 생성 GraphQL |
| `HF_TOKEN` | 🟡 | (없음 → 무인증, rate-limit 위험) | pod 내 wiki corpus 다운로드 |
| `ANIMA_REPO_ROOT` | 🟡 | `/Users/ghost/core/anima` | 로컬 dispatch script 기준 |
| `P21H_STEPS` | 🟢 | 2000 (5000 권장) | train.py argparse override |
| `P21H_BSZ` | 🟢 | 2 | 동상 |
| `P21H_LR` | 🟢 | init-variant 기반 default | 동상 |
| `P21H_WIKI_FRAC` | 🟢 | 0.3 (E2=0.5 · E3=1.0) | corpus mix |
| `P21H_TEACHER_CKPT_SHA256` | 🟢 | (없음 → skip) | F4 patch B — vp21m adapter 검증 |
| `WATCHDOG_SEC` | 🟢 | 5400 (90 min) | dispatch script 자체 watchdog |
| `SAVE_POD` | 🟢 | 1 (V3 fire 는 항상 retain) | teardown 시 pod 보존 여부 |

🔴 필수 (없으면 fail) · 🟡 권장 (없으면 degraded) · 🟢 optional override

`secret get runpod.api_key` 가 SSOT — `~/.runpod/config.toml` 에서
유지 (`feedback_runpod_api_key_ssot.md`). dispatch script 가 빈 응답
받으면 stale secret 의심 → 재싱크.

---

## 2. 디렉터리 계약

```
state/pure_<closure>_<date>/                       ← workspace 루트
  README.md                                        ← variant 표 + fire 명령
  launcher_<variant>_<date>.sh                     ← emit 된 dispatch wrapper
  <variant>.log                                    ← bash launcher fire log
  v<VARIANT>/                                      ← dispatch_p21h_v3 가 만듦
    pod_id.txt
    dispatch.log
    result.json                                    ← train 완료 신호
    train.log
    heldout_vp21h_v3.json
    vp21h_v3_eval1.json
    mix_info.json
    kosmos_anchors/...
    FAILURE.txt                                    ← 실패 시에만
```

- `<closure>` ∈ { `track1`, `b_distill`, `c_head_g`, `a_curriculum`, `head_g_log` ... }
- `<date>` = `YYYY_MM_DD` (런처 emit 시점 UTC)
- `<variant>` = closure-specific tag (예: `E2`, `E3`, `B_alpha`, ...)

---

## 3. 런처 인자 계약

`pure_launcher_parse_argv` 가 정의하는 표준 인터페이스:

```
hexa run HEXAD/PURE/launchers/<closure>_launcher.hexa <mode> [opts]

mode:
  dry-run         (default) — print plan, write nothing
  emit            — write launcher_*.sh into state/pure_<closure>_<date>/

opts:
  --uid <tag>     override the auto-generated uid (timestamp + 6-hex)
```

런처는 다른 mode 를 정의 **금지**. fire (dispatch) 는 emit 된 `.sh` 의
caller 가 수행 (`@D a_wall_first` 적용 시 두 launcher .sh 를 parallel
nohup). 런처 자체는 pod 를 만들지 않는다.

---

## 4. 출력 산출물 계약

| 산출물 | producer | 명명 | 형식 |
|--------|----------|------|------|
| `launcher_<variant>.sh` | `_common.pure_launcher_write_sh` | timestamp uid 포함 | bash, chmod +x |
| `<variant>.log` | bash `nohup` redirect | dispatch+train log 통합 | text |
| `pod_id.txt` | `dispatch_p21h_v3_runpod.sh` | runpod create resp | hex id 한 줄 |
| `result.json` | `train_p21h_v3.py` | train 완료 신호 | JSON (verdict + per-lang) |
| `ckpt_step<N>.pt` | `train_p21h_v3.py` | step 번호 (zfill 6) | torch state_dict |
| `FAILURE.txt` | dispatch script | 실패 marker | text + reason code |

ckpt naming `ckpt_step<N>.pt` 는 F4 patch C (--resume-from-step) 의
glob 대상 SSOT — `<N>` 은 zero-pad 없이 정수 그대로 (예: `ckpt_step500.pt`).

---

## 5. honest C3

1. 본 계약은 2026-05-23 시점 PURE Track 1 + B 증류 + C head_g + A 커리큘럼
   런처 그룹 기준. 새 closure 가 추가될 때마다 본 문서를 동시에 갱신해야
   하며, 누락 시 SSOT drift 발생.
2. P21H dispatcher/trainer 는 현재 `.sh`/`.py` — hexa-port 가 land 되기
   전까지 `_common.hexa` helpers 와 직접 통합 불가. emit 단계만 hexa 표준화.
3. `P21H_TEACHER_CKPT_SHA256` 는 contract 에 등록했으나 dispatch script
   adoption 은 F4 patch B (DEFERRED) — 본 변수 set 해도 현 dispatch
   script 는 무시한다 (back-compat). adoption 후 활성화.
4. `pure_launcher_uid` 의 6-hex 랜덤은 충돌 방지가 weak — 동일 초에 두
   런처가 같은 closure 에서 emit 하면 충돌 가능. 본 directive 하에서는
   런처가 sequential emit 이므로 실용상 문제 없음.
