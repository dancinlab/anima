# py_retire_archive — torch/py 폐기 운영 아카이브

> **결정 (2026-06-28 오너):** py 전체 폐기 → **hexa 단일 production**. 2-production 정책 종료.
> codegen #42492878 FIXED 확정(hexa v0.334.0). 불변식 = **로직 유실 0** — 모든 py 로직은
> git 이력 + 이 아카이브로 보존된다(삭제는 언제든 가역).

## 보존 vs 삭제 분류

### 1. 삭제됨 (engine byte-parity 미러 — git 이력으로 복원 가능)
hexa 가 byte-parity(≤~2e-16, `core/CLAUDE.md` 미러 표 + a_engine_native_learning 이력)로
동등 로직을 보유함이 증명된 엔진 미러. 원위치(`core/`, `cli/`)에서 `git rm`.

- `core/brain.py` ⇄ `core/brain.hexa`
- `core/bytegpt_decode.py` ⇄ `core/bytegpt_decode.hexa` (sha 4e7145fe)
- `core/clm_decode.py` ⇄ `core/clm_decode.hexa`
- `core/engine_cli.py` ⇄ `core/engine_cli.hexa` (434/434 pub fn, worst 1.563e-16)
- `core/engine_g.py` ⇄ `core/engine_g.hexa`
- `core/g_gates.py` ⇄ `core/g_gates.hexa` (G0-G6 driver)
- `core/g6_ideation.py` ⇄ `core/g6_ideation.hexa` (G6 scoring ops)
- `core/generator.py` ⇄ `core/generator.hexa`
- `core/pure_field.py` ⇄ `core/pure_field.hexa` (~2e-16)
- `core/DECODER/flame_mm.py` ⇄ `core/DECODER/flame_mm.hexa`
- `cli/train.py` ⇄ `cli/train.hexa` (task#10 full parity 포팅, 7 real gaps 해소;
  forward/CE/decode-logits byte-parity + SAVANT/MITOSIS/4셀/held-out val/descent 레버 전부)

복원: `git show <pre-refactor-sha>:core/<file>.py`. parity 근거 = `core/CLAUDE.md` 미러 표,
`cli/CLAUDE.md` train parity 거버넌스, ARCHITECTURE.json 2-production 노드(git 이력).

### 2. 이 아카이브로 이동 (torch Lane-P 트레이너 + 코퍼스/벤치 — hexa 대체 = cli/train.hexa)
production 학습은 `cli/train.hexa`(flame/forge own-GEMM) 단일. torch Lane-P 는 REFERENCE+bridge
였으나 hexa-단일 전환으로 production 경로 아님. 신규 학습은 `anima train` → hexa → .clm 직접.

- `train_torch_lane_p/` — `train_lane_p.py`, `train_lane_p_3b.py`, `train_lane_p_split.py`,
  `_qseed.py`, `_qseed_check.py` (torch Lane-P GPU 트레이너; 3B fire 스펙
  `train/clm/train/fire_3b_rung_qat.hexa` 가 가리키던 실제 트레이너 — 그 fire 스펙은
  연구 artifact 로 train/ 에 잔류, 재발사 시 이 아카이브에서 복원).
- `train_corpus_builders/` — `build_wiki_3b_corpus.py`, `build_wiki5_bigcorpus.py`,
  `build_flores5_corpus.py` (코퍼스 빌더; 엔진 로직 아님, 데이터 준비 유틸).
- `train_bench/` — `clm_time_encoding.py`, `analyze_brain_train.py`, `lane_m_eeg_mitosis.py`,
  `lane_x_3axis.py`, `engine_tensionlink_bench.py`, `brain_train_bench.py` (벤치/분석).

복원: 위 파일을 원위치(`train/clm/{train,corpus,bench}/`)로 되돌리고 torch env 준비.

### 3. 보존 — 삭제/아카이브 제외 (active build/serialize 도구, py-engine 미러 아님)
hexa-단일 전환 후에도 **runtime 의존**이거나 거버넌스가 명시 요구하는 torch-free/numpy 도구.

- `train/clm/model/verify_clm_v2.py` — **cli/train.hexa 가 런타임 shell-out**
  (`python3 verify_clm_v2.py descent <clm> <heldout>`, train.hexa:1380). `a_clm_gen_pipeline`
  이 canonical held-out mirror-DESCENT 게이트로 명시(math.log mirror, engine dt_ln CE-clamp
  버그 면역). `descent` 경로는 **torch 0**(struct/sys/os/math + 함수내 lazy numpy만) =
  py-engine 미러 아닌 build-time serialize-integrity 도구. → 잔류.
- `train/clm/model/clm_serialize_v2.py` — `.clm` v0.2/v0.3 serialize byte-truth bridge
  (`a_clm_gen_pipeline` 가 ground-truth 로 명시). torch 는 lazy(`.pt` 로딩 시에만, line 244).
  verify_clm_v2 의 round-trip self-test 가 import. → serialize 도구로 잔류
  (torch `.pt`→.clm 변환은 legacy-interop; 신규는 train.hexa serialize_clm 직접).
- `train/clm/model/model.py`, `train/clm/model/data.py` — clm_serialize_v2 의 torch
  CLMConfig/CLMConvMoE 정의(`.pt` 변환용 lazy 의존). serialize 도구 동반 잔류.
- `tool/enforce_anima_gates.py` — 거버넌스 enforcer(폐기 제외, 별개 도구). GATECARD_FILES
  에서 `core/g_gates.py` 제거 → `core/g_gates.hexa` 단일; 2-production 주석 hexa-단일 갱신.
- `serve.py`, `tool/*.py` — 뷰어/거버넌스/HF 유틸(엔진 아님).
- `serving/anima_cli.py` — bin/anima shim 의 model-picker/REPL(3-폴더 엔진 밖 UI, 엔진 아님; 잔류).

### 4. defunct_parity_tooling/ (2-production byte-parity CI 게이트 — 폐기)
- `parity_gate.py` — hexa⇄py byte-parity LOCKSTEP CI 게이트(`a_engine_native_learning` 2-production
  강제). py 엔진 폐기로 무의미 → harness.config.json verify.checks + .github/workflows/ci.yml 에서
  배선 제거. 권위 측정 = `anima eval` hexa 단일진입.
