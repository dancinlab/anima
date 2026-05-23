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
| `P21H_TEACHER_CKPT_SHA256` | 🟢 | (없음 → skip) | F4 patch B — vp21m adapter 검증 (adopted 2026-05-24, PR #295 — `HEXAD/PURE/launchers/dispatch_p21h_v3.hexa::sha256_verify(path, expected)`) |
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
3. `P21H_TEACHER_CKPT_SHA256` 는 2026-05-24 PR #295 로 adopted —
   `HEXAD/PURE/launchers/dispatch_p21h_v3.hexa::sha256_verify(path, expected)`
   가 F4 patch B kernel 을 실제 구현하여 본 변수를 active 하게 consume 한다.
   원본 `.sh` dispatcher 는 project tape 가 `.sh` 수정 차단으로 그대로지만
   hexa skeleton 측은 enforce. 정직: 본 PR 은 contract 갱신만, dispatcher
   full impl (resume kernel + 전체 wiring) 은 별도 cycle.
4. `pure_launcher_uid` 의 6-hex 랜덤은 충돌 방지가 weak — 동일 초에 두
   런처가 같은 closure 에서 emit 하면 충돌 가능. 본 directive 하에서는
   런처가 sequential emit 이므로 실용상 문제 없음.
5. §6 corpus_quality 6-metric 은 **syntactic-only** (byte/공백토큰/Hangul
   triplet 통계). 의미·진실성·register 자체를 직접 측정하지 않으며 p7
   NO PERPLEXITY VERDICT 준수 (PR #287 C3 참조). M5 가 register-imbalance
   의 *신호* 이지 정의가 아님 — 진단은 model dynamics 와 합작 해석한다.

---

## 6. corpus_quality 산출물 계약

`HEXAD/PURE/eval/corpus_quality_probe.hexa` (PR #287) 의 6-metric scorer
출력 계약. closure-fire launcher / eval consumer 가 corpus 측 품질을
정량화할 때의 SSOT. 측정은 **byte 관측만** (p7 · Law 2 observe-never-inject).

| metric | 정의 | 범위 | 용도 |
|--------|------|------|------|
| M1 `m1_entropy` | byte freq Shannon 엔트로피 (bit) | 0 – 8 | 전반 정보 밀도 |
| M2 `m2_bigram_mi` | 인접 byte 상호정보 (cap 512B) | ≥ 0 | 국소 구조성 |
| M3 `m3_ttr` | 공백 토큰 TTR (uniq/total) | 0 – 1 | 어휘 다양성 |
| M4 `m4_avg_line` | 비어있지 않은 줄 평균 길이 (byte) | > 0 | 줄 형태 프로파일 |
| M5 `m5_hangul` | distinct Hangul triplet / 2350 | ≥ 0 | register/언어 비중 신호 |
| M6 `m6_kl_uniform` | KL(P_byte ‖ U_256), 클수록 skew | ≥ 0 | byte 분포 편향 |

### `score <path> [--sample-bytes N] [--out json]`

```json
{ "path": "<path>", "n_bytes": int, "n_lines": int, "sample_bytes": int,
  "m1_entropy": float, "m2_bigram_mi": float, "m3_ttr": float,
  "m4_avg_line": float, "m5_hangul": float, "m6_kl_uniform": float }
```

`--sample-bytes` (default 1000000) 는 corpus 앞부분 truncate 상한;
`n_lines` 는 비어있지 않은 줄 수, `n_bytes` 는 실제 샘플 길이.

### `compare <a> <b> [--sample-bytes N] [--out json]`

```json
{ "a": { ...score(a)... }, "b": { ...score(b)... },
  "diff": { "m1_entropy": float, "m2_bigram_mi": float, "m3_ttr": float,
            "m4_avg_line": float, "m5_hangul": float, "m6_kl_uniform": float } }
```

`diff` 는 항상 **b − a** (pairwise). `a`/`b` 는 각각 위 `score` 스키마.

**PR #303 발견 anchor** — Track 1 5건 측정: M1 entropy · M6 KL_uniform 가
거의 동일 (Δ ≤ 0.07) → "corpus quality 부족" 가설 비지지. **M5 hangul** 만
anima-OWN 24–32% vs wiki 3% 로 갈림 → M5 = **register-imbalance 신호**
(E2 ko PURE_MEMORIZE 진단의 corpus-side 정합 증거).
