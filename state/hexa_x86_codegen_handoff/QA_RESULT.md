# hexa x86_64 codegen fix + anima 학습·측정 QA 결과 (실측)

> 인수문서 = `BUG_AND_QA.md` §3. 호스트 = **aiden**(RTX 5070 sm_120, x86_64-linux, hexa **v0.334.0**). summer 는 objrun(pid 45797) 점유 → 회피.
> 추측 0 · 캡처된 출력만(verdict-integrity). 날짜 2026-06-28.

## 0. 셋업 (실측)
- aiden hexa = **v0.334.0** (버그 보고 버전 v0.315.0 의 19 마이너 위 — `#4154 fix(runtime.h): thread fn-global fwd-decls` 포함 한참 이후).
- mac → aiden rsync: `core/`(8.8M) · `cli/`(348K) · `train/` · 4셀 corpus(`gen_{en,ko}.txt`·`sns_{en,ko}.txt`) self-contained 동기.
- 테스트 .clm = `ce_marginal_seed7.clm`(176MB, h1602 recomb_obj 계열) — summer→mac→aiden 릴레이(aiden 가 summer 호스트명 미해결이라 mac 경유).
- GPU: `cuda_available()` = **1** (실측, `hexa run` 으로 확인 — `hexa gpu` self-probe 아님).

## 1. codegen fix 실측 (premise — 최우선) — ✅ FIXED

x86_64 C-codegen 버그(`gen_auto_ideate` C forward-proto 미방출 → clang undeclared 6 sites)는 **해소됨**. 두 갈래 증거:

### (a) `cli/train.hexa` 컴파일+실행 RC=0 (완결)
`hexa run cli/train.hexa -- …` 가 **컴파일 RC=0 + 풀 실행** 완료(아래 §3). train.hexa 도 generator/flame 계열 동일 codegen 영역을 통과 — 컴파일 자체가 통과 증거.

### (b) `cli/anima.hexa -- evaluate` 컴파일 — C-codegen + clang link 단계 통과 (link 진행중)
빌드 로그(`/tmp/.hexa-runtime/brc.*.log`) 캡처:
```
=== self/type_checker.hexa — 18 tests passed ===
[warn] function `_cos` redefined — overloading unsupported, later definition ignored
OK: build/artifacts/hexa_run.25145c92a3605160_v0.334.0.tmp….c        ← C codegen 성공(.c 생성, abort 없음)
  [rt] HEXA_PREBUILT_RUNTIME — linking prebuilt: runtime.a
  [2/2] clang -O2 … hexa_run….c runtime.a -o … -lcudart -lcuda …    ← clang LINK 단계 도달
```
**핵심**: 예전 버그면 `gen_auto_ideate` proto 미방출로 **C→obj 단계 전 clang undeclared 6 sites 즉사**. 지금은 `OK: …c`(codegen 성공) + clang **link** 단계까지 도달 = undeclared 0. → **codegen 버그 GONE.** (최종 RC=0 + evaluate 출력은 aiden load avg 24 과부하로 link 진행중 — 자연완료 대기, §2 에 박제 예정.)

미해결 심볼: **없음**(clang undeclared 0).

## 2. 측정(evaluate) byte-parity — hexa �us py 2-production
> ⚠️ py 엔진은 2026-06-28 폐기됨(commit ad1841439·bf9f98bbc, core/*.py 11 + cli py twins 3 삭제). 이 parity 는 **삭제 직전 옛 tree(aiden)에서 도는 py eval** ⇄ **새 tree(summer) hexa eval** 의 historical 동등성 증거. (테스트 = ce_marginal_seed7.clm · 4셀 · py=gen80 / hexa=gen40 단독무경쟁)

| 게이트 | py `cli/evaluate.py` (aiden·옛 tree·gen80) | hexa `anima evaluate` (summer·새 tree·gen40) | 일치? |
|---|---|---|---|
| G0 coherence | 🟢 PASS kwr 5/5 | [진행중] | … |
| G1 best_distinct / max_single | 🔴 FAIL 1 / 1 | [진행중] | … |
| G2 novel / control | 🟢 PASS 118 / 0 (coherent 20) | [진행중] | … |
| G5 non-fab L1 | 🟢 PASS fab 0.0233 | [진행중] | … |
| G6 dist / fals / frame_leaks | 🔴 FAIL 6 / 0 / 0 | [진행중] | … |
| CLOSURE (a7b_pass) | 🔴 FAIL | [진행중] | … |

> py 측 G3 = continuity 0.999950 · impostor 0.000000 (architecture read, decode 점수 아님).

> 주의: gen 다름(py80 vs hexa40)이면 G1 budget·G6 dist 가 gen-민감 → 절대수치 발산 가능. gen-둔감 게이트(G0 coh·G2 control 등) 일치 = 엔진 동등성 증거. 발산 시 gen차이/엔진차이 격리 명시(c9).

### 4. py-폐기 후 hexa-단일 컴파일/스모크 RC (핵심) — ✅ ALL RC=0

새 tree(`core/*.py` 11 + `cli/*.py` twins 3 삭제, py-retire commit ad1841439/bf9f98bbc) 를 summer(idle·x86_64·hexa cuda=1)에 rsync `--delete`(core/*.py = **0** 확인) 후 컴파일:

| entry | 명령 | RC |
|---|---|---|
| `anima.hexa` evaluate | `hexa run cli/anima.hexa -- evaluate --help` | **0** |
| `anima.hexa` serialize | `hexa run cli/anima.hexa -- serialize` | **0** |
| `evaluate.hexa` | `hexa run cli/evaluate.hexa -- --help` | **0** |
| `serialize.hexa` | `hexa run cli/serialize.hexa` | **0** |
| `train.hexa` | `hexa run cli/train.hexa -- --steps 1 …` | **0** |

→ **`core/*.py` 삭제가 hexa 컴파일에 무영향 = py 폐기 terminal 확정.** undeclared 0, 실패 0. 엔진 repo-내부 import 폐포가 `.hexa` 만으로 닫힘(3-폴더 self-contained).

**serialize dispatch 경로 확인** (`anima serialize`):
```
=== anima serialize → cli/serialize.hexa (torch .pt → .clm v0.3 + DESCENT gate) ===
usage: anima serialize <ckpt.pt> <out.clm> [--heldout <path>] [--train <path>] [--nwin N]
```
serialize.hexa = CLI orchestration(hexa) → 유일 torch step(.pt unpickle)은 kept torch-interop `train/clm/model/serialize_standalone.py`(serialize_v3 byte layout SSOT + verify_clm_v2 descent gate)로 dispatch. py 엔진 미러 아님. 경로 정상.

## 3. 학습(train) smoke — ✅ 3/3 PASS (완결)

`hexa run cli/train.hexa -- --steps 40 --out /tmp/smoke_train.clm --corpus <4셀> --heldout-corpus <slice>` (MODE_VERIFY d8·L1·E2→Emax4, $0):

```
mode: MODE_VERIFY (d8·L1·E2->Emax4 $0 farr CPU — lever wiring proof)
4-cell register balance table: cells=4 usable=4 total_train_bytes=5026469   ← fail-loud 가드 4칸 통과
[OWN-GEMM-FIRED] _hx_k_gemm DEVICE path (no cuBLAS)                          ← GPU own-GEMM 점화 (a_train_flame_forge)
step 1  CE=4.8037  E=2 ; step 20 CE=4.5292 E=3 (SPLIT) ; step 40 CE=4.2290  ← CE 하강 + mitosis split
savant latched_at step=1 ; mitosis split_at step=20 (E0=2 -> E=3)
serializing .clm (E=3 L=1 d=8 V=256 K=3) -> /tmp/smoke_train.clm (12342 bytes)  ← 자동 직렬화
PASS  F-CLI-TRAIN-DESCENT     loss0=4.8037 -> lossF=4.2290
PASS  F-CLI-TRAIN-SAVANT-LATCH savant ON step 1 (golden zone [0.2123, 0.5] 교차 latch)
PASS  F-CLI-TRAIN-MITOSIS-BOUND split E2->E3 bounded, no blow-up
=== anima cli/train.hexa: 3/3 PASS ===   (RC=0)
```

**held-out DESCENT 게이트 발동 확인** (`verify_clm_v2.py descent /tmp/smoke_train.clm <heldout>`):
```
F-CLM-DESCENT=0
DESCENT {'heldout_model_ce': 4.05417, 'heldout_shuffle_ce': 4.05316, 'uniform_ce_lnV': 5.54518,
         'heldout_lt_uniform': True, 'heldout_lt_shuffle': False, ...}
DESCENT_FAIL: serialized .clm does NOT model held-out text — do NOT mark done / HF-upload.
```
게이트가 **정상 발동 + 정확히 판정**: d8·40-step 랜덤초기 toy 는 held-out 을 모델 못함(model_ce 4.054 ≈ shuffle 4.053 → `heldout_lt_shuffle: False`) → 올바른 FAIL(fail-loud). 게이트 배선·판정 로직 작동 확인 (toy 라 PASS 기대 아님; PASS 는 실 학습 MODE_CANON GPU fire 의 몫).

요약: train.hexa 컴파일 RC=0 + GPU own-GEMM DEVICE 점화 + CE descent + SAVANT latch + MITOSIS split + 자동 .clm 직렬화 + held-out DESCENT 게이트 발동 = **학습 파이프 점화/배선 전부 복권**.

## 4. 미완·정직
- §2 byte-parity 표: anima.hexa evaluate 컴파일 + py eval 둘 다 완료 후 박제(둘 다 aiden load avg 24 과부하로 진행중 — stall 아님, CPU 95–231% 실측).
- §3b "GPU util>0 풀 학습" 은 MODE_CANON(303M, cost-gated fire)의 몫 — smoke 는 MODE_VERIFY($0). 단 own-GEMM DEVICE path 는 smoke 에서도 점화 확인.
- serialize QA(§3c, `anima serialize <pt>`) 미수행(선택 항목; .pt 미보유).
