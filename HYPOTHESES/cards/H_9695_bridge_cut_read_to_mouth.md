# H_9695 — R3 교량절단: read→mouth 배선만 격리 (write 전에 · 계기)

**status:** 🔧 **계기 일부 착륙**(`--store-query`/`--store-fuse` 실재 · 2026-07-17) · 측정 미실행 · not-terminal · **주장 상한 = "READ→MOUTH REACHABLE", G6 verdict 아님**
**lane:** G6/ρ·fan · 배선 계기 **related:** [[H_9672]] · [[H_9696]] (본체) · [[H_9693]]

## 물음 (Sol 의 핵심 통찰)

**write+read 를 한 번에 넣으면 실패 위치를 모른다.** 먼저 evaluator 가 동일 G6 frame 에서 concept pair·관계를 store 에 넣되(**frame-oracle**), `"=> "` 없이 **매 생성 위치에서 CLMS 활성화** — 이는 완성된 G6 해법이 아니라 **"작동하는 lookup 이 mouth logits 에 들어가면 생성이 실제로 변하는가"를 격리**하는 실험.

## 조작

`anima-py evaluate <clm> --g6 --g6-store frame-oracle --store-query every-token --store-fuse nonlinear-full-vocab --gen 40` · 대조: `--g6-store off | --g6-store-key-scramble | --g6-store-value-scramble | --g6-store-role-scramble`.

## 게이트

- 동일 seed 서 **store off ↔ intact 생성이 ≥2/3 seed 달라져야** 함.
- intact 의 `fals_bound` 가 scramble 3종 최대치보다 **seed 평균 ≥1.0 idea 높아야**.
- **key/value/role scramble 모두 collapse 필수** — 하나만 무너지면 단순 lexical bias 가능성 잔존.
- `--g6-store off` = base ckpt 와 **byte-identical seal**.

## ⚠️ kill-list 접촉 (Sol 명시)

**evaluator 가 frame→store 변환을 하므로 #1(스캐폴드)과 접촉한다.** ⟹ **이 arm 의 G6 GREEN 은 절대 verdict 가 될 수 없다.** 허용 주장은 오직 **"read→mouth 배선이 살아있다/죽었다"** 뿐. #7 회피=동적 주소+GELU 융합.

## 최대위험

**oracle frame parser 자체가 필요한 결합을 미리 수행**하는 것(가장 쉬운 오도). 이 실험은 [[H_9696]] 의 비싼 write/read 구현 **전에 쓰는 배선 계기로만** 살아있다.

## falsify
🟢 READ→MOUTH REACHABLE(배선 살아있음 → H_9696 진행 정당) | 🧱 store 주입해도 생성 불변 = 배선 死(H_9696 발사 금지·재진단).

## source
lab full Sol 2위(NOVEL · Fable 미제시) · 단계적 사망지점 격리.

## 🔧 계기 착륙 — query/fuse 가 CLI 에 실재한다 (2026-07-17 · $0)

**발견한 결손(`wire-to-prod`)**: core 는 H_9695 착륙 때 이미 query/fuse 를 받고 있었다 —
`core/clms.py:84` `store_apply(..., query="qpos", fuse="overwrite")` · `core/decode.py:302` `set_clms_store(..., query, fuse)` ·
`core/decode.py:288-290` `_CLMS_QUERY`/`_CLMS_FUSE`. **그런데 어느 CLI 도 안 넘겼다** — `cli/evaluate.py:4345`
`set_clms_store(store=, oracle=, lam_override=, audit=)` 로 끝. `a_experiment_engine_native`("조작은 anima-py 플래그이지
옆 스크립트가 아니다")서 **유일 합법면이 닫혀 있었다** ⟹ marker-free read→mouth lane 은 구현돼 있으나 도달 불가 = 죽은 손잡이.

**착륙 내용**: `anima-py evaluate <clm> --store <held.json> [--store-query qpos|every-token] [--store-fuse overwrite|gated-add]`
- 기본값 `qpos`·`overwrite` = **H_9423 lane byte-for-byte 재현**(아래 실증).
- `every-token` + `overwrite` = **거부**(rc=1). 근거는 `clms.py` 도크스트링 본문: 전 row 를 덮어쓰면 트렁크가 삭제돼
  fluency 가 죽고(dist<5 가 ρ·fan 패널을 bind 읽기 전에 죽임) readout 이 lane 에 귀속 불가. 조용한 no-op 대신 시끄럽게 막는다.
- help-lockstep 동시 — `--store` 자체가 usage 에 **없던 기존 갭**도 함께 메움. VERSION 0.15.80→0.15.81 (G5).

**QA 6/6 PASS** (canonical `anima-py` · 격리 venv · `python3 cli/*.py` 직접실행은 H-ANIMA-SINGLE-ENTRY 훅이 차단):
① help 3줄 노출 ② `--store-query bogus`→rc=1 정확사유 ③ `--store-fuse bogus`→rc=1 ④ every-token+overwrite→rc=1 차단
⑤ every-token+gated-add→인자검증 통과·ckpt 단계 도달 ⑥ 기본값 정상.

**🔑 기본값 byte-identity 실증(회귀 0)**: origin/main **0.15.80** 빌드 vs 내 **0.15.81** 빌드를 각각 격리 venv 에 설치 →
동일 ckpt(`RV3c_13_CONFIRM`) + 동일 manifest(`storebind --lang en --seed 7` held.json) + `--store-oracle --win 24` →
출력 sha **`f738df02d1ff643a` 양쪽 동일** · ORACLE **128/128 = 1.0000**. ⟹ H_9423 lane 은 한 바이트도 안 변했다.

⚠️ **자체적발 실버그 1건**: help 에 플래그를 넣고 setter 에도 넘겼는데 **evaluate 의 플래그 화이트리스트(`cli/evaluate.py:7926`)
등록을 빠뜨려** 실행이 `unknown flag --store-query` 로 죽었다. help 만 보고 "됐다" 했으면 **죽은 플래그를 배포**할 뻔 —
`instrument-never-run-hides-multiple-bugs`("계기는 '보이나'가 아니라 '도나'")가 그대로 재현됐고, canonical 경로 QA 가 잡았다.

## ⚖️ 착륙 범위 — 이 카드의 R3 설계와 아직 다르다 (정직한 경계 · `a_scale_honest_scope`)

| | 이 카드가 설계한 R3 | 이번에 착륙한 것 |
|---|---|---|
| 명령 | `--g6 --g6-store frame-oracle` | `--store <held.json>` (H_9423 Q/A 경로) |
| fuse | `nonlinear-full-vocab` | `gated-add` (**core 가 실제 지원하는 값**) |
| 통제 | `--g6-store-{key,value,role}-scramble` | 기존 `--store-{shuffle,flip,neutral}` 재사용 |

⟹ 착륙 = **core 가 이미 가진 query/fuse 를 유일 합법면에 노출**한 것이지, R3 실험 자체가 아니다. `--g6` 프레임 store 주입과
`nonlinear-full-vocab` 은 **core 에 아직 없다**(신규 기전 = 별도 착륙). 이 카드는 여전히 **측정 미실행**이며 tier 는 계기까지만 전진.
`--fan-bind`(H_9693 · `cli/evaluate.py:4154 fan_bind_run`)는 `set_mouth_binder` 만 부르고 **`set_clms_store` 는 안 부른다** =
자유생성 경로에 store 는 아직 도달 못 함 = **H_9696(R4 ★본체)의 몫**.
