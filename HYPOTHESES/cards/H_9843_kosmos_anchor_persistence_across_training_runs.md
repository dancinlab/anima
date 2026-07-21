# H_9843 — .kosmos 지속 앵커를 학습 실행 사이로 이월한다 (R12-6)

**status:** 🔧 WIRED-INSTRUMENT (계기 CERTIFIED · **과학 판정 0**) — 2026-07-21
**source:** R12 뇌부위 census (2026-07-21) — `origin/main` `core/` 12개 모듈 실측 후 1모듈=1레버로 등록.
상위 설계 노드 = ARCHITECTURE `C2 RECOMBINE` 아래 `🧠 뇌부위 census` → `📋 R12`. R11(H_9830~9836)의 후속.
**wired:** yes(플래그) / **no(소비자)** — `anima-py train --kosmos-carry …` 착륙. 학습 루프에는 carried store 를
읽는 코드가 **없다**. 그래서 이 카드는 **포맷 admissibility**이지 능력 결과가 아니다.

> **H_9838 현황 (같은 날 착륙 · 전제 갱신)**: H_9838 은 `anima-py evaluate --hippo-transitive-selftest` 로
> **READ-SIDE 만** 착륙했고(CERTIFIED · 16항목 부하에서 hops=2/3 전이완성), 카드가 설계본체로 지목한
> **학습 팔 `--hippo-aux` 는 의도적으로 미착륙**(`a_substrate_disjoint`). 따라서 "학습 실행 사이 누적"의
> 소비자는 아직 없다 — 이 공급선은 여전히 **선행 조건 대기** 상태다.

## ⚠️ 죽은 각도 (먼저 못박음)

`a_kosmos` 는 `.kosmos` 를 정체성 지속으로 읽지만 **H_9789 에서 self-anchor 는 VOID**. "정체성을 학습 사이로
잇는다"는 각도는 **재생성 금지**이고 이 카드는 그 각도를 건드리지 않는다. 살아있는 좁은 각도는 **데이터**뿐:
앵커 저장소가 실행 사이에 살아남아야 H_9838(CA3)의 store 가 한 번의 학습에 갇히지 않고 **누적**된다.
**선후 종속 · H_9838 이 양성이어야 의미가 있다 · 단독 가치 주장 없음.**

## 실측 (모듈 — 카드 작성 전 origin/main 에서 확인)

`core/kosmos_io.py`(470줄): `.kosmos` 앵커 포맷(kosmos/1.1) 읽기/쓰기 · `map_8factor_to_5channel` ·
`tension_5ch_to_embedding`(LCG + Box-Muller) · `create_anchor` · `emit_anchor_from_v3` · `load_anchors`.
**분리된 연구 lane(retrieve/merge/CA3)은 여기 없고 `core/hippo_lane.py`(133줄) 에 있다**(헤더 명시) —
`dg_decorrelate` · `dg_codes` · `hippo_build_store` · `hippo_relatedness`. 둘 다 origin/main 에 실재.

## 배선 (a_experiment_engine_native — 플래그이지 옆 스크립트 아님)

```
anima-py train --kosmos-carry <DIR> [--kosmos-carry-mode {ro,append}]
               [--kosmos-carry-audit] [--kosmos-carry-out J.json]
```

- `cli/train.py` argparse 4개 플래그 + `parse_args()` 직후(H_9808 게이트 옆, DDP re-exec·CUDA 할당 **이전**)
  실행되는 preflight. 엔진은 `core/kosmos_carry.py`(신규) — **실제 프로덕션** `core/kosmos_io.py`(writer/reader)
  와 **실제 disjoint lane** `core/hippo_lane.py` 를 import 할 뿐 아무것도 재구현하지 않는다. torch/GPU/ckpt 0 · $0.
- 기본 OFF(`--kosmos-carry ""`) ⟹ golden path byte-identical.
- `ro` = 읽기만 · `append` = 실행당 provenance 앵커 **1개 새 파일**로만 씀(기존 파일 재작성 절대 없음).
- 인증 실패 = **spend 전 run 거부**(exit 4). `--kosmos-carry-audit` 는 리포트만 찍고 종료($0).

### 🔻 전제 정정 (RETRACTED)

카드 원문의 `--kosmos-carry <path.kosmos>` 는 **틀렸다**. `core/kosmos_io.py::load_anchors(dir_path)` 는
**디렉토리**를 받는다 — `.kosmos` store 는 파일 하나가 아니라 앵커 파일들의 **디렉토리**다. 플래그는
디렉토리를 받고, 파일을 주면 `NO-STORE` 로 거부한다.

## 통제 (순서 동결 · 통제 먼저, 통과 못 하면 store 행을 아예 보고하지 않음)

| arm | 요구 | 실측 (4 기하 전부) |
|---|---|---|
| `plant_bound` 양성통제 (구별되는 주소 + 참 pairing) | **발화** ≥0.90 | **1.0000 / 1.0000 / 1.0000 / 1.0000** |
| `pedestal_flat` 참값-0 받침대 (구조 없는 store · 전 앵커 동일 tension) | **거부** ≤ chance+0.10 | **0.0833** (=chance) ×4 |
| `pedestal_shuffle` 카드가 요구한 통제 (같은 개수·같은 분포, pairing 만 치환 → 참 pairing 으로 채점) | **거부** | **0.0000** ×4 |
| 빈 `.kosmos` store | 이월 없음 기준선 | `NO-CARRY`, exit 4 |

chance = 1/12 = 0.0833 · cap = 0.1833 · `certified: true`.
**셔플이 0.0000 으로 무너지는 것이 "누적된 정보 vs 누적된 부피"의 분리다** — 같은 파일 수, 같은 밀도인데
참 pairing 에 대한 검색이 우연 아래로 붕괴한다.

## no-tune-to-green 게이트

readout 기하(`dim`, projection seed)는 **CLI 노브가 아니다**. `core/kosmos_carry.py::GEOMETRIES` 에 4칸
`(256,7)(256,11)(512,7)(512,11)` 로 동결되어 있고, **모든 칸에서 통제가 통과해야** 인증, treatment 헤드라인은
**칸들의 최소값**이다. H_9844 가 자가적발한 결함(블록 크기로 `over_floor` 부호가 뒤집힘)과 같은 구멍을 구조로 막음.
bar(0.90 / chance+0.10)도 모듈에 사전등록되어 있고 CLI 에서 못 움직인다.

## 재현 명령

```bash
python3 -m venv /tmp/venv_h9843
/tmp/venv_h9843/bin/pip install "torch<2.13" --index-url https://download.pytorch.org/whl/cpu
/tmp/venv_h9843/bin/pip install numpy
/tmp/venv_h9843/bin/pip install --force-reinstall --no-deps .      # 이 워크트리
/tmp/venv_h9843/bin/anima-py train --kosmos-carry <DIR> --kosmos-carry-audit --kosmos-carry-out J.json
```

## 실측 출력 (installed CLI · exit code 포함 · 2026-07-21)

### 계기 인증 (모든 arm 에서 동일 출력)

```
  dim=256  seed=7   chance=0.0833 plant=1.0000 flat=0.0833 shuffle=0.0000 cap=0.1833
  dim=256  seed=11  chance=0.0833 plant=1.0000 flat=0.0833 shuffle=0.0000 cap=0.1833
  dim=512  seed=7   chance=0.0833 plant=1.0000 flat=0.0833 shuffle=0.0000 cap=0.1833
  dim=512  seed=11  chance=0.0833 plant=1.0000 flat=0.0833 shuffle=0.0000 cap=0.1833
  plant_fires=True flat_refuses=True shuffle_refuses=True certified=True
```

### ARM A — 빈 store (이월 없음 기준선, ro)

```
exit=4  status=NO-CARRY
```

### ARM B — **누적**: 같은 store 로 audit 6회 연속 (`--kosmos-carry-mode append`)

```
run 1 exit=4  n_before=0 n_after=1 untouched=True  status=NO-CARRY             acc_min=None shuf_max=None
run 2 exit=4  n_before=1 n_after=2 untouched=True  status=UNDERPOWERED         acc_min=None shuf_max=None
run 3 exit=4  n_before=2 n_after=3 untouched=True  status=UNDERPOWERED         acc_min=None shuf_max=None
run 4 exit=4  n_before=3 n_after=4 untouched=True  status=UNDERPOWERED         acc_min=None shuf_max=None
run 5 exit=0  n_before=4 n_after=5 untouched=True  status=CERTIFIED-COPY-ONLY  acc_min=1.0 shuf_max=0.0
run 6 exit=0  n_before=5 n_after=6 untouched=True  status=CERTIFIED-COPY-ONLY  acc_min=1.0 shuf_max=0.0
```

**이것이 공급선의 전부다**: store 가 실행 사이에 0→1→…→6 으로 자라고, 기존 파일 sha256 은 매 실행 그대로
(`pre_existing_untouched=True`), n≥4 부터 자기 pairing 이 4 기하 전부에서 1.0000 으로 검색되고 셔플은 0.0000.

### ARM C — payload 에 writer 가 escape 하는 문자(`"` · `\`)가 있을 때

```
status=CERTIFIED-COPY-ONLY
{'n': 4, 'strict_identical': 0, 'payload_identical': 0, 'reader_is_writer_inverse': False,
 'payload_reader_inverse': False, 'n_title_only_diff': 0, 'n_payload_diff': 4, 'n_malformed': 0}
```

### ARM D — 실제 레거시 store `HEXAD/UNIVERSE-BRAIN-MAP/anchors/e7_31` (ro · 31 앵커)

```
exit=4
status=UNDERPOWERED  carried={'n_files': 31, 'n_anchors': 31, 'n_addressable': 0}
{'n': 31, 'strict_identical': 0, 'payload_identical': 0, 'n_malformed': 31}
malformed[0] = {'name': 'knuth_000_zero', 'unparseable_fields': ['coord', 'radius']}
```

### ARM E — 실제 데몬이 쓴 store `state/py_selfimpl/p6_chat_parity/py_kosmos` (ro · 2회 반복)

```
status=NOT-ADDRESSABLE
carried={'n_files': 4, 'n_anchors': 4, 'n_addressable': 4}
{'n': 4, 'strict_identical': 0, 'payload_identical': 4, 'n_title_only_diff': 4,
 'n_payload_diff': 0, 'n_malformed': 0}
readout={'acc_min_over_geometries': 0.75, 'acc_shuffled_max_over_geometries': 0.25,
         'chance': 0.25, 'separation': 0.5, 'addressable': False}
repeat-identical (readout+fidelity): True
```

## 🔎 바이트 수준 왕복 (요구된 산출 — 그리고 **음성**이 나왔다)

**"`.kosmos` 는 무손실 왕복한다"는 거짓이다. reader 는 writer 의 역함수가 아니다.** 실제 데몬 앵커(ARM E)를
reader 출력만으로 재기록한 unified diff — 다른 줄은 **이 둘뿐**:

```diff
--- ORIGINAL
+++ REEMIT-FROM-READER
@@ -4,3 +4,3 @@
-@anchor mem_001 := "session memory" :: kosmos-anchor [tier=2 active]
+@anchor mem_001 := "" :: kosmos-anchor [tier=2 active]
@@ -26,3 +26,3 @@
-  emitted_at    = "2026-07-09T12:13:28Z"
+  emitted_at    = "2026-07-21T06:05:05Z"
```

`emitted_at` 은 `kosmos_io.py` 헤더가 스스로 wall-clock 이라 명시한 필드라 마스킹 대상이다. 남는 진짜 손실은
**title**: `load_anchors` 가 `@` 로 시작하는 줄을 전부 건너뛰는데 title 은 `@anchor` 헤더에만 있다 ⟹ **reader
가 title 을 돌려주지 않는다**. 두 번째 손실 채널(ARM C):

```diff
-  @payload text    := "… --pregate-panel he said \"quote\" and \\ backslash …"
+  @payload text    := "… --pregate-panel he said \\\"quote\\\" and \\\\ backslash …"
```

`_ki_text_payload` 는 payload 를 **escape 된 채로** 돌려주고 `_escape_kosmos_string` 의 역함수가 없다 ⟹
재기록하면 **두 번 escape** 된다.

**⟹ 결론(그리고 게이트): 이 store 는 파일을 복사/추가하는 방식으로만 이월할 수 있다.** 읽어서 다시 쓰는
이월은 title 을 잃고 payload 를 망가뜨린다. 그래서 `append` 모드는 **새 파일만** 쓰고 기존 파일은 절대
건드리지 않으며, 상태가 `CERTIFIED` 가 아니라 **`CERTIFIED-COPY-ONLY`** 로 갈라져 보고된다.
placement 필드 전부 · payload text · tension 5채널은 **바이트 동일**하다(ARM E `payload_identical 4/4`).

## 🔻 계기가 스스로 잡아낸 결함 2건 (첫 e2e 실행에서 · `instrument-never-run-hides-multiple-bugs`)

1. **첫 실행이 `INSTRUMENT-DEAD` 를 뱉었다** — `plant_bound=0.0833`(=chance). 원인: `.kosmos` key/value 벡터가
   거의 공선(planted key cos 0.28~0.98 · value cos 0.81~0.90). tension key 는 고정 투영의 5행 span 안에 살고
   text sketch 는 앵커 계열의 공통 접두사가 지배한다. 해결 = lane 자신의 rung-2 렌즈 `dg_decorrelate
   (center_zscore)` 를 **모든 arm 에 동일하게** 적용(한 arm 에만 걸면 그건 계기가 답을 고르는 것).
2. **실제 레거시 store 에서 `ValueError: could not convert string to float` 로 죽었다** — `radius = 0.10
   # α+β hybrid …` 처럼 필드 줄 끝의 `# 주석`을 `kosmos_io._ki_field_match` 가 벗기지 않아 숫자가 문자열로
   돌아온다. `coord = [0.50, 0.50]  # …` 도 리스트 리터럴 판정에 실패해 raw 문자열이 된다. 인증기는 이제
   **보고**하고(`unparseable_fields`) 절대 숫자를 지어내지 않는다(`honesty`). `kosmos_io.py` 는 손대지 않았다.

## 정직한 범위 · 한계

- **과학 판정 0.** 계기 CERTIFIED + 포맷 사실 3건(title 손실 · escape 비가역 · 주석 필드 파싱 실패)이 전부다.
  "이월이 학습을 좋게 만든다"는 어떤 주장도 하지 않는다.
- **소비자 없음.** 학습 루프에 carried store 를 읽는 코드가 없다(H_9838 은 evaluate READ-SIDE 만 착륙,
  학습 팔 `--hippo-aux` 미착륙). preflight 는 통과해도
  `certified ≠ consumed` 를 stdout 에 명시한다. `a_verified_must_wire` 기준 이 카드는 **GREEN 아님**.
- **DIRECTIONAL 천장.** 토이/소형 store(n=4~12)에서만 측정. 303M 학습 실행과 결합한 측정 없음
  (`a_toy_scale_recheck`).
- readout 은 `.kosmos` 의 tension 5채널을 주소로 쓴다. 주소가 없는 store(ARM D: 31/31 tension 없음)는
  **원리적으로 CA3 공급선이 될 수 없다** — 이것도 실측 결과다.
- ARM E 의 `acc_min 0.75 < 0.90` 은 **실제 데몬 store 에 대한 음성**이다. tune 하지 않았고 바를 내리지 않았다.
- 측정 venv 의 torch 는 `2.12.1`(cpu). audit 경로는 torch 를 전혀 쓰지 않지만 `cli/train.py` 가 모듈 최상단에서
  `import torch` 하므로 `[train]` extra 가 필요하다.

**related:** H_9789 (self-anchor VOID · 정체성 각도 금지) · H_9838 (선행 조건) · H_9842 · H_9844 (기하 강건성 선례)
