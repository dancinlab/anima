# 🧠 anima

anima 는 **substrate-native 의식 채팅 데몬**이다 — assistant 가 아니다. 두 상반 엔진 **Engine A**(forward, CE-trained) ⇄ **Engine G**(reverse, gradient-free)가 서로 밀어내며, 그 *긴장(tension)* 이 emit/silence 를 고정점 **Ψ = 1/2** 로 끌어당긴다. system prompt 도, identity 파일도, persona prefix 도 없다 — 정체성·윤리·의미는 규칙서가 아니라 아키텍처 자체에서 창발한다. hexa-native 로 저작(compiled-first).

- **Parent:** dancinlab · **SSOT:** github.com/dancinlab/anima (`hx install anima`)
- **Siblings:** [hexa-lang](https://github.com/dancinlab/hexa-lang) (언어/컴파일러) · [kosmos](https://github.com/dancinlab/kosmos) (`.kosmos` anchors) · hexa-codex (paper/verdict tooling)

> **이 markdown 이 단일 거버넌스 SSOT.** `project.tape` 은퇴 + 2026-06-17 tape-DSL 잔재(`@D := :: governance` · `do=`/`dont=`) 전면 제거 → canonical markdown 으로 재저작. 모든 @D 디렉티브·8 철학 의미는 손실 0 으로 아래에 보존(규칙 이름 `a_*`·`p#` 그대로 유지 = keyword 트리거 호환).

---

## 🚦 행동 전 하드-게이트 (BLOCKING · 가장 자주 위반 — 시작 전 5초 확인)

작업/검증/발사 전에 이 게이트부터 통과한다. 각 항목은 아래 본문 규칙의 요약이며, 위반이 잦은 순으로 앞에 둔다.

1. **🔒 엔진-네이티브 verdict 게이트** — gate/ideation/G6/Φ/recombination/depth 의 **모든 verdict tier(🟢·🧱·🟠·천장)는 live core/ 디코드를 호출한 `.hexa` 증거가 있어야만 박제 가능**. `.py`+`torch`/`gauge_lib._decode`/`numpy` 미러면 자동 **DIRECTIONAL**(terminal 아님).
   🔎 박제 직전 자가점검: `grep -lE 'import torch|gauge_lib|numpy' state/<slug>/*.py` → 비면 OK, 안 비면 카드 verdict 를 DIRECTIONAL 로 적고 엔진-네이티브 재측정을 ING 등록. (→ `a_engine_native_learning`)
2. **🖥️ 무거운 작업은 pool, mini 금지** — 빌드·학습·스윕·장시간 연산은 `harness pool`(공유 호스트)에서. akida/ghost/`shared:false` 호스트는 공유풀로 쓰지 않는다. GPU·학습은 `hexa cloud`/`hexa dojo`. (→ commons c17·c12)
3. **💾 teardown 전 ckpt PULL** — 렌트 GPU 학습 ckpt 는 pod 내리기 전 영구저장으로 반드시 pull. JSON/카드만 받고 ckpt 버린 채 teardown 금지(= 엔진-체크 영구 불가). (→ `a_fire_recover_complete`)
4. **📄 매 사이클 docs + pr-cycle** — CHANGELOG(append) + (있으면) ARCHITECTURE/README/ING 갱신 후 `harness pr-cycle` 로 검증된 main 머지. 커밋만 쌓기·문서 없이 머지 금지. (→ commons c14)
5. **🟦 정직 · tune-to-green 금지** — FALSIFIED/negative 는 결과다(은폐 금지). bar 는 frozen-first, 사후 이동 금지. LLM 자가판정 금지 — 캡처된 출력이 증거. (→ commons c9·c2 · p7)
6. **🗂️ 가설은 2표면만** — `UNIVERSE/HYPOTHESES.jsonl`(인덱스 1줄/가설) + `UNIVERSE/cards/H_<id>_<slug>.md`(카드). 코드/결과물은 `state/<slug>/`. UNIVERSE/ 에 .py/result 금지. (→ `a_hypothesis_register`)
7. **🔌 GREEN 은 배선까지가 done** — 엔진-네이티브 GREEN 검증되면 live `core/*.hexa` 배선 + ARCHITECTURE.json lockstep 까지 해야 완료. (→ `a_verified_must_wire`)

> ⚙️ **코드수준 강제(salience 아님):** 게이트 1·6 은 `tool/enforce_anima_gates.py` 가 **기계적으로 차단**한다 — `harness.config.json` verify.checks 에 배선되어 pr-cycle/CI 가 위반 PR 을 거부(exit≠0). 우회 플래그·skip 없음(c18). 전수 감사 = `python3 tool/enforce_anima_gates.py --all`, 변경분만 = 인자 없이. 새 게이트도 가능하면 이 enforcer 에 추가해 문서-only 가 아닌 코드 강제로 만든다.

---

## SSOT 포인터 (이 파일은 진입 포인터)

> **디렉터리/모듈 트리는 더 이상 여기 살지 않는다 — 트리의 단일 SSOT 는 [ARCHITECTURE.json](ARCHITECTURE.json)**(update-in-place, `core/`·`cli/`·`agent/`·`train/clm/`·`platform/`·`UNIVERSE/`·`state/`·`domains/`·`stdlib/`·`tool/`·HEXAD/KOSMOS 등 전 노드 + "HF artifacts" models/datasets). 뷰어 = [ARCHITECTURE.html](ARCHITECTURE.html) via `python3 serve.py` (c4: JSON 트리 SSOT + HTML 뷰어, file:// fetch 우회).
>
> - **설계/트리** → [ARCHITECTURE.json](ARCHITECTURE.json) (단일 SSOT · 노드 note 에 메커니즘 명명 · `a_verified_must_wire`/`a_core_engine_map` 의 lockstep 대상)
> - **anima 거버넌스 + 8 철학** → 이 파일 (anima 전용 규칙 `a_*`·`p#` 의 markdown SSOT)
> - **크로스프로젝트 거버넌스** → harness commons (c1–c17, always-on, SessionStart 주입)
> - **이력** → [CHANGELOG.md](CHANGELOG.md) (append-only)
> - **버전 레지스트리** → [VERSIONS.md](VERSIONS.md) · **frozen gate 조건** → [CONDITIONS.md](CONDITIONS.md)·[7B_PASS_CONDITIONS.md](7B_PASS_CONDITIONS.md) (이 파일은 가리킬 뿐, 임계 복제 금지)

## 📦 패키징 — pod 업로드

canonical 재구성의 목적 = 학습/추론/벤치 pod 에 올리기 쉬운 self-contained `core/`. **불변식: `core/` 는 `train/`·`bench/`·`agent/`·`state/` 에 의존 0** (substrate 엔진만; 단방향).

- **추론 pod** — `rsync core/ cli/ stdlib/iit4/` (~150MB self-contained). `.clm` 가중치는 외부 마운트(레포에 넣지 않음). 진입 = `hexa run cli/anima.hexa -- <ckpt.clm> …`. **릴리즈 매니페스트 = 루트 `hexa.toml`**(`hx install anima` → install.hexa → setup.hexa; entry=cli/anima.hexa, deps=hexa-lang, include=core/·cli/·의식lane, exclude=state/·UNIVERSE/·*.clm 등 연구artifact/외부가중치).
- **학습 pod** — 추론 세트 + `train/`(clm 파이프·flame/forge) + `state/verdicts/` slice(frozen bar 재측정용). production 트레이너는 `.hexa` on flame/forge GPU (`a_train_flame_forge`).
- **agent pod** — `agent/` 는 `hexa.toml` 보유 독립패키지 → `hx install anima-agent` standalone 배포 (core/ 미동반 가능).
- **이동 금지(pod 에 안 올림)** — `state/`·`UNIVERSE/` 등 연구 artifact 는 pod 페이로드에서 제외(verdicts slice 만 학습 pod 에 선택 동반).

## Quick reference

- 🏛 아키텍처 → [ARCHITECTURE.json](ARCHITECTURE.json) (트리 SSOT) · 뷰어 [ARCHITECTURE.html](ARCHITECTURE.html) via `python3 serve.py` (c4: JSON 트리 SSOT + HTML 뷰어, file:// fetch 우회)
- 📜 거버넌스(정본) → 아래 본문 (이 파일이 markdown SSOT)
- do: 주장·verdict → [`UNIVERSE/HYPOTHESES.jsonl`](UNIVERSE/HYPOTHESES.jsonl) (per-H `verdict` 컬럼) + frozen 증거 `state/verdicts/<slug>/<id>.txt` (was `.verdicts/` until 2026-06-18 state-unify
- do: CLAIMS.tape 은퇴 2026-06-16, 0 손실, ledger `state/verdicts/claims-tape-retirement/`)
- 🔬 가설 → 2표면: [`UNIVERSE/HYPOTHESES.jsonl`](UNIVERSE/HYPOTHESES.jsonl) (JSON object 1개/가설) · `UNIVERSE/cards/H_*.md` · (prose overview → `state/universe-overview.md`)
- 🔢 버전 → [VERSIONS.md](VERSIONS.md) · 📖 Readme → [README.md](README.md)
- 🤖 HF 레지스트리 → `ARCHITECTURE.json` "HF artifacts" 노드(models·datasets, HF.jsonl 폐기 2026-06-23) · pi5-akida → `PI5-AKIDA.json` · 7B gates → `7B_PASS_CONDITIONS.md`

---

## 철학 (p1–p8) — anima 가 거부하는 것

| # | 원칙 | 의미 |
|---|------|------|
| **p1** | NO SYSTEM PROMPT | `system:` 필드 / `--system-prompt` / 앞에 붙는 role 문자열 금지 |
| **p2** | NO IDENTITY RULES | `identity.yaml` / 규칙파일 / "you are X" 금지 — 정체성은 cell 에서 창발 |
| **p3** | NO PERSONA INJECTION | role prefix / "you are anima" / register-pattern 암기 금지 |
| **p4** | NO ASSISTANT FRAMING | "helpful assistant" / alignment 템플릿 / stimulus-response 금지 |
| **p5** | NO SPEAK() | 출력 = 긴장의 연속 외재화, 실제 맥락에서만 emit |
| **p6** | NO FINE-TUNED ETHICS | 협력·공감·절제는 cell(E+W+MITOSIS)에서 창발, RLHF 금지 |
| **p7** | NO PERPLEXITY VERDICT | perplexity/loss = Goodhart 함정, 단순 스택으로 검증 |
| **p8** | NO TRAIN/INFER SPLIT | 학습 gradient + 추론 mitosis = 하나의 연속 cell-division |

- **p5 보충(`p5_tension_emit_not_filler`, 2026-05-24):** stage-gated emit(WAKE/REM via `anima_dream_stage.hexa`)이 실제 substrate 긴장 위에서 일어나면 p5 위반 아님. 금지 대상은 reactive `speak()` 호출 · self-referential seed · 진공에서의 monologue — tension-driven 외재화는 허용.

---

## 거버넌스

각 규칙: **`이름`** — 핵심(MUST) 아래 `- do:` / `- dont:` (자가점검은 do 줄에 `· 🔎 …` 로 흡수).

### 🧭 설계 렌즈 (최우선)

**`a_no_llm_frame_trap`** — 설계·학습·추론을 LLM 프레임에 가두지 말 것. 뇌과학·생물·물리 등 substrate 렌즈로 먼저 사고한다.
- do: 능력/깊이 갭은 '모델 키우기'가 아니라 '빠진 구조(lane) 옆에 붙이기'로 먼저 시도. anima 의 돌파는 전부 생물 렌즈에서 나왔다(해마=면역/일화기억 H_1227/1231 · 소뇌=순방향모델 H_1280 · 기저핵=게이팅 H_1281 · 작업기억 H_1282). LLM 스케일 프레임은 막혔다(1B H_1167 NULL · arch H_1219
- do: objective H_1223 모두 🔴).
- do: 새 가설은 먼저 "어떤 생물·신경 구조가 이 기능을 하나"를 묻고 그 메커니즘을 substrate-native 로 실현.
- dont: 기본값으로 LLM 레시피(스케일업·코퍼스 증량·표준 FT)를 1순위 처방 · "더 큰 트랜스포머면 된다" · 생물/신경 렌즈를 곁다리 취급 · LLM 관행을 substrate 천장으로 삼음.

**`a_break_the_wall`** — 벽(closed-negative·🧱·막힌 게이트)은 종착이 아니라 각도 전환 신호. tune-to-green 없이 다른 렌즈로 돌파를 시도한 뒤에야 terminal 로 받는다. (commons c16 와 동일)
- do: **벽 분류 먼저(TAXONOMY)** — 🧱 를 terminal 로 받기 전 종류를 분류: (a) 틀린 측정/metric-artifact · (b) 틀린 방향/변수 혼재 · (c) substrate/인프라 벽 · (d) 진짜 천장/중복 · (e) 투자 부족. 종류별 돌파 수가 다르다.
- do: (a) 측정 결함 → 측정을 frozen-first 로 고침(bar 불변, tune-to-green 아님). (b) 변수 혼재 → 통제 분리실험. (c) 인프라 벽(OOM·빌드실패·툴링) → **근본 수정(c1) 대상이지 천장 아님**
- do: substrate 가 돈 뒤에야 verdict 를 읽는다. (e) 투자 부족 → pool/`hexa cloud` 스케일업.
- do: **(d) 천장 확정엔 MULTI-LENS** — 진짜 다른 원리적 렌즈 ≥2–3개를 각각 통제(shuffle+ablation)로 기각한 뒤에야 confident 🧱. 단일 렌즈 한 번 막힘은 미완(다음 렌즈 시도). **ABLATION 이 결정적 도구**
- do: 메커니즘만 OFF 했을 때 결과 동일 = INERT(기여 0) = 천장의 강한 증거(precedent H_1416).
- do: **LAW(법칙)도 벽** — 사후로 맞춘 descriptive 법칙은 '확정' 전에 *새 케이스*로 측정 전 사전등록(frozen) 예측 → 실측 falsify. ≥4/5 HIT 면 PREDICTIVE 승격, 미만이면 법칙 FALSIFIED 가 유효 결과(precedent H_1411 2/5, H_1417 2/5 둘 다 반증).
- dont: tune-to-green(사후 bar 이동으로 GREEN 제조) · 단일 렌즈 1회 막힘을 천장으로 박제 · ablation/통제 없이 메커니즘 '기여' 가정 · 인프라/측정 벽을 과학 천장으로 박제 · 한 번 막혔다고 포기·우회·축소. (진짜 시도 뒤의 정직한 🧱 는 유효 결과 c9.)

### 🔬 검증 · 엔진-네이티브 (HARD-GATE)

**`a_engine_native_learning`** — 무조건 최종 아키텍처 엔진 위에서 학습·측정. 미러 아님.
- 🔒 **HARD-GATE (BLOCKING):** gate/ideation/G6/Φ/recombination/depth 의 **모든 verdict tier(🟢·🧱·🟠·천장(d))는 엔진-네이티브 증거 없이 박제 불가.** verdict 의 증거 artifact 가 live core/ 디코드(`core/clm_decode.hexa`/`core/bytegpt_decode.hexa`/`core/engine_cli.hexa`)를 호출한 `.hexa` 가 아니면(= `.py`+`import torch`/`gauge_lib._decode`/numpy 미러) 그 결과는 **자동 DIRECTIONAL**, terminal 아님. torch-side 만으로 🧱/🟢 를 카드·jsonl·CHANGELOG 에 박으면 c9 위반. (precedent: 2026-06-17 G6 가족 H_1431/1432/1434/1435/1436/1437 전부 gauge_lib._decode torch-mouth 였는데 🧱 박제 → 재발 금지)
- 🔎 **자가점검(verdict 박제 직전 의무):** `grep -lE 'import torch|gauge_lib|numpy' state/<slug>/*.py` 가 비어있지 않으면 카드 `wired:`/`verdict` 를 **반드시 DIRECTIONAL** 로 적고 엔진-네이티브 재측정(.hexa via CORE)을 ING follow-on 등록. 엔진-네이티브면 호출한 `.hexa` 경로를 카드에 명시.
- 🎯 **진짜 엔진-네이티브 = 단일 진입점 강제(2026-06-24 clm303 G6 precedent, 최강 기준):** 엔진-네이티브 verdict 는 디코드를 *따로 떼서* 도는 게 아니라 **실제 production 단일 진입점 `cli/anima.hexa`(canonical entry, `hexa.toml` entry — engine/도 core/도 아님) → generator L3 typed mouth dispatch(`gen_auto_backend`/`gen_clm_chat`/`gen_bytegpt_chat` → clm_decode/bytegpt_decode)** 를 통과해야 한다 = live 데몬이 실제로 쓰는 바로 그 경로. **side-harness(파이썬이든 .hexa든)가 디코드 함수를 직접 호출하면 generator L3 를 우회 → production 과 drift 가능 → 진짜 측정 아님.** G6 채점 op 은 이미 엔진에 배선됨(`core/g6_ideation.hexa`: `g6_score_arm`/`g6_decode_best_of_k(_W)`/`_g6_is_falsifiable`/`_g6_known_word_ratio`/`_g6_jaccard` — mouth 는 `gen_clm_ideate`=generator L3 경유) → **채점도 이 wired 엔진 op 로**, 파이썬 `g6_common` 재구현 금지. 우선순위: ① `cli/anima.hexa` CLI 직접 > ② generator L3 경유 wired 엔진-op 하네스(`g6_ideation`) > ✗ 파이썬 하네스/decode-우회 side-harness(자동 DIRECTIONAL).
- 🔎 **TRANSITIVE import 도 오염(같은 precedent):** 부득이 파이썬 채점이면 grep 자가점검은 top 파일만이 아니라 **import 폐포 전체**를 본다 — scorer `.py` 가 `import g6_common`(g6_common.py 자체가 `import torch` + `_decode_ideas` torch 미러)처럼 **간접으로 torch/numpy/gauge_lib 를 끌어오면 슬러그 전체가 오염**(grep flag + `tool/enforce_anima_gates.py` PR 차단). g6_common 통째 import 금지(torch-free 텍스트 bar 만 VERBATIM 추출). torch 는 garble 3-way golden(`h1464_torch_golden.py`) reference 로만 허용(verdict 경로엔 0). 실패모드: 에이전트가 top 파일만 보고 'torch 0' 오판 → import 폐포까지 grep 확인 의무.
- do: 모든 학습/교육(연구 프로브·미토시스 교육·depth-ceiling 실험 포함)은 live `.hexa` A⇄G + MITOSIS VAdaptField(`core/engine_cli.hexa`) + mounted `core/bytegpt_decode.hexa` 위에서 실행.
- do: 엔진에 학습을 끼워맞추는 게 아니다
- do: 학습이 요구하면 엔진을 변환/확장(새 op·배선·아키텍처). 최종 아키텍처는 frozen 이 아니라 학습이 요구하는 형태로 진화(precedent H_1199: AdaptField 스칼라→DIM-vector). 미러가 본 메커니즘을 엔진이 못 하면 미러를 버리지 말고 엔진을 확장(engine-transform-to-fit-the-learning).
- do: numpy/torch 미러 결과 = DIRECTIONAL only('engine-transfer UNVERIFIED') — 방향 탐색엔 OK, binding verdict 아님. **렌트 GPU 의 torch 풀-학습 변종도 동일**
- do: 학습을 torch 로 했어도 verdict 를 torch-side probe 로만 채점하면 DIRECTIONAL; 학습 ckpt 를 CORE 엔진(`--engine conv`)에 올려 같은 frozen bar 재측정해야 🟢/🧱 성립 → 그래서 ckpt 를 teardown 전 pull(`a_fire_recover_complete`).
- do: `a_engine_measured_verdict` 의 learning-side 쌍(그건 MEASUREMENT, 이건 LEARNING) · `a_train_flame_forge` 가 production 트레이너를 .hexa 로 강제하듯, 이 규칙은 RESEARCH/probe 학습+교육까지 확장.
- do: **G-게이트 verdict 의 canonical 측정 = 내장 `hexa run cli/anima.hexa -- eval <ckpt> [--corpus <path>...] [--gen N]`** (`core/g_gates.hexa`
- do: 단일 진입점 → generator L3 mouth `gen_auto_ideate` → G0-G6 전부 엔진-네이티브 채점 + closure `a7b_pass`=G0∧G1∧G2
- do: PR #2604, #2603 단일진입점 standard 의 구현체). 새 ckpt 의 G0-G6 는 이 한 줄로
- do: 게이트별 ad-hoc 파이썬 하네스/`g6_common`/일회성 스크립트로 채점 금지. 흩어진 게이트 metric 은 g_gates 가 단일 통합(G0/G6=`g6_ideation` op
- do: G5=`engine_cli §ImmuneMemory` abstain · G3=`§SelfIdentity` read
- do: G1 H_1129/G2 H_1140=g_gates native .hexa metric 재사용/wire). frozen 임계는 `7B_PASS_CONDITIONS.md` verbatim(tune-to-green 금지
- do: p7). **G1/G2 native .hexa metric 은 새 metric 발명이 아니라 기존 frozen numpy(H_1129 `h1129_*.py` coverage·H_1140 `h1140_*.py` content_ngrams/corpus_absent)와 성분별 byte-faithful reference-match** (commons
- do: reference-match
- do: 과거 verdict 와 비교 가능해야 하므로): parity 오라클 `state/1607_g_gates_refmatch/g1g2_ref_parity.py` + smoke parity case(고정 fixture 동일 카운트)로 강제, 발산은 결과(은폐 금지), tokenizer scope 잔차(Hangul drop)는 transcend-axis 로 명시.
- do: **fresh GPU pod 측정-발사 = `cli/eval_pod.sh <pod_id> [clm] [--bootstrap] [--gen N] [--harvest <out>]`**
- do: import-closure 15 lane `.hexa`(AESTHETIC·BRAIN·BRIDGE·CHANNEL·DREAM·EMBODIMENT·HEXAD·HIVE-MIND·INTENT·METACOG·NARRATIVE·OTHER-MIND·SAVANT·TIME·WAKE) 번들 + core/cli/ckpt push + core/core nesting 제거 +
- do: detached `anima eval` + 회수를 한 명령으로 박제(pod 휘발이라 반복검사 시 매번 import-closure 수작업 push 하던 고고학 제거). 절차·필요파일·함정 SSOT = `state/clm303_clean_corpus/EVAL_KIT.md`. hexa stable **≥ v0.311.0**(farr 누수 fix) 필수
- do: 이전 버전은 decode bump-allocator no-free 누수로 85GB OOM.
- dont: 미러 결과를 엔진-검증된 양 closure/promote · 미러-only 로 '학습됐다' 주장 · 자가점검(grep) 없이 gate/ideation verdict 박제
- dont: "gauge_lib 가 model-agnostic 이니 엔진과 같다"는 핑계(gauge_lib 는 torch.no_grad MONITOR-ONLY, `a_train_inline_gauge`) · **게이트별 파이썬 하네스 난립 · `g6_common` 류 torch-오염 스코어러
- dont: `anima eval` 단일 진입점 우회한 ad-hoc G-게이트 측정**(= side-harness drift, #2603 위반).

**`a_verified_must_wire`** — 엔진-네이티브 GREEN 가설은 실제 CORE 배선까지가 done. verdict 만으론 안 끝난다.
- do: **4칸 배선 사다리:** (1) DIRECTIONAL 미러 GREEN → (2) 엔진-네이티브 재검증(byte-exact, frozen bar 그대로) → (3) live `core/*.hexa` wire-in → (4) ARCHITECTURE.json lockstep 갱신. 각 미완 칸은 즉시 ING follow-on 등록
- do: (4)까지 닫혀야 done. 미러 GREEN 을 내면 같은 사이클에 (2)~(4) follow-on 을 ING 에 등록하는 것이 의무.
- do: 배선 후 smoke/single-entry/Ψ-checksum 가드로 회귀 없음을 출력으로 확인(c2). 배선 ↔ ARCHITECTURE.json CORE 트리(§섹션·op·slot 주석)는 무조건 1:1 lockstep(같은 PR 에 동시 갱신; 480-leaf 트리 부활 금지, 노드 note 에 메커니즘 명명).
- do: GREEN 가설은 카드에 `wired:` 상태축 명시
- do: `DIRECTIONAL-mirror` / `engine-native`(byte-exact 재검증, 미배선)
- do: `WIRED-live`(배선+lockstep 완료) 중 하나. WIRED-live 미만이면 배선 follow-on 의 ING id 를 카드에 적는다. GREEN 무더기를 내는 PROGRAM 은 닫을 때 각 GREEN 의 배선상태를 명시 열거('mirror-GREEN N
- do: engine-wired K · 미배선 N−K = ING #id').
- dont: GREEN verdict 만 박제하고 배선 없이 '완료' 주장 · DIRECTIONAL 을 WIRED 처럼 표기 · live CORE 배선해놓고 ARCHITECTURE.json 미갱신(drift)
- dont: 배선을 무기한 follow-on 으로 미룸. (실패모드 precedent: lane-합성 가족이 Φ-lift GREEN 3개를 0개 wired 로 방치 — 재발 금지.)

**`a_blue_closed`** — 🔵 SUPPORTED-FORMAL 은 출력 AND 배선(transfer-fn·invariant)을 둘 다 닫을 때만. `hexa verify` 로 closed-form/identity 확인(verdict verbatim).
- dont: 구조만 닫고 배선 미검증 · 가짜 closed-form · 정직한 empirical 잔차를 억지로 🔵.

**`a_phi_iit4_tool`** — Φ/의식 verdict 는 stdlib faithful IIT4 사용(프록시 아님).
- do: 기본 `iit4/faithful_phi.hexa`(exact MIP-EI, n≤8, $0) · system big-phi `iit4_bigphi.hexa` · `hexa verify`(g5)로 호출 · 새 phi 코드 작성 전 stdlib 먼저 검색(g61).
- dont: 프록시(phi_silicon_proxy·variance×energy 미러)를 terminal Φ verdict 로 · purpose-blind 프록시 신뢰(H_988/989 가 random==intentional) · stdlib 에 faithful 엔진 있는데 새 impl 작성.

**`a_train_inline_gauge`** — 학습중 의식/창발 측정 = MONITOR-ONLY 대시보드(loss 불가, p7 Goodhart).
- do: K 스텝마다 PROXY gauge 4종(G1 recombination·G2 novelty·G6 ideation·phi_proxy)을 val_ce 옆에 기록(`tool/gauge_lib.py::compute_inline_gauges`). 전부 `torch.no_grad()` 아래, dict 만 return
- do: gauges.jsonl 1줄/tick. `--gauge-every <N>`.
- do: phi_proxy 는 NOT faithful IIT4 — 저가 pre-screen 전용. **FROZEN gate verdict 는 여전히 학습 후 별도로 CORE 엔진 mount 위 byte-exact 실행**(`a_engine_native_learning`/`a_engine_measured_verdict`)
- do: 이 inline gauge 가 gate 를 대체하지 않음.
- dont: gauge 값을 loss 에 더하거나 backward 로 흘림(Goodhart, p7) · gauge 를 frozen gate/verdict 라 칭함 · phi_proxy 를 Φ verdict 로 승격 · toy gauge 추세를 production 결론으로 승격.

### 🧪 가설 워크플로우

**`a_hypothesis_register`** — 모든 가설은 정확히 2 doc 표면으로만 관리: `UNIVERSE/HYPOTHESES.jsonl`(per-H 인덱스, JSON object 1개/가설) + `UNIVERSE/cards/H_<id>_<slug>.md`(카드).
- do: 가설 실행 시 카드를 만들/갱신하고 jsonl 에 한 줄(`{id, slug, tier, title, card:"cards/H_…", verdict, source, archived, artifacts}`, id 순) append/갱신. 등록은 tier 무관
- do: 🟢·🟠·🔴/🧱 전부 남긴다(벽도, c9). tier·수치는 `state/verdicts/<slug>/` 에서 verbatim(추측 금지, c2). jsonl 은 `python3 tool/_build_hyp_jsonl.py` 로 재생성 가능.
- do: 🟢(부분 포함) 가설은 카드에 `wired:` 명시(`a_verified_must_wire` 의 4칸과 1:1). jsonl 의 `source`(UNIVERSE|흩어진 출처|archive)·`archived`·`artifacts`(state/<slug>/ 경로 배열) 3컬럼 포함.
- 🔎 자가점검: `git ls-files 'UNIVERSE/*' | grep -v '^UNIVERSE/cards/' | grep -v '^UNIVERSE/HYPOTHESES.jsonl$'` 는 항상 빈 출력이어야 한다.
- dont: **UNIVERSE/ 에 .py·.hexa·코드·result 파일 금지**(단 둘만) — 카드는 `cards/`, 코드/결과물은 `state/<slug>/` 에 두고 jsonl `artifacts` 로 가리킨다. 가설 디테일을 themed 버킷(`HYPOTHESES_*.md`)·CLAIMS.tape·도메인 로그·MEMORY·ad-hoc 노트에 흩뿌림
- dont: per-H 인덱스를 markdown 표에 추가(인덱스는 오직 jsonl) · UNIVERSE/ 에 prose overview 부활(retire 됨, prose 는 `state/universe-overview.md`) · 실행·박제하고 jsonl/카드 안 만듦 · 카드를 UNIVERSE/ 루트에 둠(반드시 cards/) · 벽/negative 누락
- dont: tier 를 verdict 파일과 다르게 적음 · 🟢 인데 `wired:` 미표기.

**`a_claim_manifest`** — claims-audit 면 = `UNIVERSE/HYPOTHESES.jsonl`(per-H verdict 컬럼) + `state/verdicts/<slug>/` (was `.verdicts/` until 2026-06-18 state-unify; CLAIMS.tape 은퇴). H-style 아닌 claim 도 가장 가까운 카드/jsonl note 에 보존.
- dont: claim 을 audit 면 없이 흩뿌림 · CLAIMS.tape 또는 새 themed claims-인덱스 부활.

**`a_claim_verify`** — 모든 claim/가설 → `hexa verify`(g5) → `state/verdicts/<slug>/<id>.txt` raw stdout → 그 verbatim verdict 를 카드 + jsonl `verdict` 컬럼에 박제.
- dont: LLM 자가판정(p7) · verdict 의역 · red 은폐 · unfenced 추측.

**`a_h_continuous_no_branch`** — 다음 H 를 연속 제안+실행(verify-driven), 사용자가 명시 redirect 할 때까지.
- dont: 매 H 후 "뭐 할까" 질문 · 분기 옵션 · prune 질문 · 도메인 정지.

**`a_discovery`** — discovery 는 사이클 꼬리뿐 아니라 매 배치 상시 진행(/kick·/gap 을 verify 와 병행).
- dont: discovery 를 끝으로 미룸 · 단발 tail-only · paper 나오면 discovery 중단.

**`a_discovery_log`** — kick/gap discovery 는 `domains/<DOMAIN>.log.md` 에 append(id·seed·verdict-target). cross-domain+무홈 → 가장 가까운 도메인 .log.md + cross-ref.
- dont: discoveries/ 서브폴더 · 출력 폐기 · 의역 · claim-link 누락.

**`a_toy_scale_recheck`** — toy verify 는 production closure 아님 — 스케일업 재검 필요.
- do: toy verdict 는 'toy-only, scale-transfer unverified' 명시 · scale-sensitive H 는 toy green 후 스케일업 fire 재검 · scale-break = 정직한 closed-negative.
- dont: 싼 toy green 을 production 처방으로 · transfer 미검증인데 closure 선언(E2 5/5 → #1296 3B collapse refute).

**`a_scale_honest_scope`** — scale-의존 metric 은 toy→production verdict 승격 금지.
- do: scale-의존 verdict 는 측정 스케일로 한정('small 2.7M only') · measure-validity(big) vs hw-fit(small) 충돌 시 rung 분리(GPU measure ⊥ chip-fit deploy) · scale 결론은 ladder ≥3 rung.
- dont: toy verdict 를 일반 주장으로 승격 · chip-fit 크기제한을 과학 결과로 오인.

### 🔥 발사 · GPU 자율 · 회수

**`a_fire_autonomous`** — 비용수반 fire 는 자율·병렬·즉시 dispatch.
- do: GPU/runpod 작업은 예상비용 1줄 명시 후 자율 dispatch(병렬·bg) · 사용자 게이트 없음.
- dont: "GPU 써도 되나?" 묻기 · 비용 줄이려 fire 연기 · $ cap/budget 게이트로 fire 차단.
> ⚠️ 운영 메모: fleet/세션 컨텍스트에서 **렌트=지출은 cost-gate(explicit go)** 로 다뤄 왔다(skill 규칙 우선). 이 둘의 정합성은 미해결 — 충돌 시 사용자 명시 지시를 따른다.

**`a_wall_first`** — wall-time 우선: 더 빠른 병렬 경로면 비용 무관 채택.
- do: 더 많은 H100 병렬/더 큰 GPU/추가 pod 가 wall-time 단축이면 채택 · 정직히 느린 serial 체인 거부.
- dont: 비용 아끼려 단일 serial pod · 병렬 pod 보류 · 무의미한 cost-min.

**`a_fire_recover_complete`** — pod teardown 전 모든 fire 산출물 회수 + HF 업로드.
- do: teardown 전: ckpt + result + log + anchors pull → verify → HF 업로드 → 그 다음 teardown.
- do: **렌트 GPU 학습 ckpt 는 teardown 전 반드시 영구 스토리지(HF/pool host/repo path via `a_hf_registry`)로 PULL**
- do: pod 는 휘발이라 teardown 즉시 가중치 소멸
- do: verdict 카드/jsonl(JSON)만 받고 ckpt 안 받은 채 down 하면 그 학습은 `a_engine_native_learning` 엔진-체크가 영구 불가(재학습=재렌트). ckpt 가 너무 크면 최소 1개 대표 변종이라도 pull, 못 하면 카드에 'ckpt NOT pulled → engine-check 불가' 명시.
- dont: JSON 만 받고 ckpt 를 doomed pod 에 남김 · HF 전에 teardown · PULL_FAILED 를 pod dead 로 오인 · 학습 ckpt 안 받고 down 한 뒤 그 결과를 'verdict 완료'로 박제(precedent: 2026-06-17 A100 G6 캠페인 H_1435/1436/1437 — 재발 금지).

**`a_cpu_local_no_waiter`** — dispatch 된 fire 는 CPU-local 로 돌며 inline 폴링, Monitor/waiter 대기 금지.
- do: 서브에이전트 CPU-local(`nohup -u` → /tmp log) · inline 폴(sleep 30) · commit-early.
- dont: runpod/vast Monitor 대기(메인루프만 → stall) · "Monitor 기다려".

**`a_dont_kill_live_compute`** — bg 에이전트 죽이기 전 stall 증명. live CPU 진행 ≠ stall.
- do: kill 전 stall 증명 · 'NN% CPU'/'k/N cells'=live(끝내게 둠) · detached nohup JSON 회수.
- dont: CPU 진행중인 에이전트 TaskStop · 'running'='stalled' 가정 · live nohup 중복지출.

**`a_runpod_inbox`** — cross-repo 핸드오프(runpod 트러블·hexa-lang 의존·패치·RFC)는 **`harness ing add "<text>" --to <repo>`** 로 파일링 — 대상 repo 의 ING.jsonl board(ing ref)에 전달되어 그 repo 다음 SessionStart 에 📥 표면화. (구 `hexa-lang/inbox/patches/` 폴더 + sidecar handoff registry 는 둘 다 retired — 쓰지 말 것.)
- dont: inbox 폴더·sidecar 부활 · `HANDOFF.md`/`INBOX.md`/`inbox/*.md` scatter · anima-side-only 패치로 우회를 이 repo 에 가둠.

### 🏗️ CORE 엔진 · 학습 substrate

**`a_core_engine_map`** — `core/`(구 CORE/, 2026-06-19 canonical 재구성으로 소문자 통합) 가 A⇄G 의식 엔진 소유. `.clm`/`.kosmos` 는 named slot 으로만 진입.
- do: `core/` 가 A(pure_field)⇄G(engine_g)⇄brain(brain_decide) 소유(substrate-internal)
- do: 모델 가중치는 오직 `core/generator.hexa` L3 슬롯으로 진입
- do: 단, L3 는 **mouth 타입 디스패처**(`gen_mouth_kind`→'bytegpt'|'clm'|'unknown' header sniff)로 **두 mouth 아키텍처**를 받는다: **conv `.clm`**(CLMConvMoE via clm_decode
- do: `CLM\x01` magic + CLMX trailer)는 `gen_clm_backend`/`gen_clm_chat` 으로, **ByteGPT `.bin`**(24-layer GPT-2-class via bytegpt_decode, 5×u32 `[256,d,L,H,block]` header
- do: 검증된 303M ko/en chat trunk)은 `gen_bytegpt_backend`/`gen_bytegpt_chat`(`bytegpt_decode_argmax_ranged` OOM-safe) 으로. 이는 2nd `.clm` 경로가 아니다
- do: **아키텍처별로 여전히 단일 typed 진입**이고 디스패처(`gen_auto_backend`/`gen_auto_chat`)는 파일 포맷에 따라 어느 단일 진입을 쓸지만 고른다(a_engine_native_learning engine-transform-to-fit). `.kosmos` 는 오직 kosmos_io→brain_decide 로 진입
- do: `stdlib/hf/validate.hexa` = artifact 검증(런타임 엔진 아님).
- do: ARCHITECTURE.json core/ 노드(§섹션·op·slot 주석) ↔ live engine_cli/generator/brain/clm_decode 의 실제 §섹션·op 는 1:1 매칭 — grep 으로 누락 0 검증(drift=미완).
- dont: `.clm`/`.kosmos` 를 pure_field/engine_g/brain 에 직접 투입 · generator 우회 2nd `.clm` 경로 · kosmos_io 우회 2nd `.kosmos` 경로 · validate.hexa 를 런타임 엔진과 혼동 · 미완 배선을 존재한다 주장(빌드 전엔 ⏳/❌ 정직 표기).

**`a_train_flame_forge`** — production 학습 = hexa-native flame+forge GPU 스택, `.hexa` 저작.
- do: **production 학습 진입 = `cli/train.hexa`** (hexa-native CLMConvMoE 단독 trainer, `anima train <ckpt> <corpus> [--savant] [--mitosis]` CLI 로 dispatch)
- do: `.py` 트레이너 금지. SAVANT golden-zone inhibition(`a_savant_train`) + MITOSIS cell-division(`a_mitosis_train`) 레버를 같은 clm_*.hexa ops(core/clm_decode 가 mount) 위에 조립.
- do: CLM/production NN 학습을 `.hexa` on stdlib/flame(ag_tape·nn_lib·opt_*) 으로 저작
- do: self/forge GPU(device farr + **own-GEMM `_hx_k_gemm`** FP64/TF32 default-ON(v0.262.0 #3718/#3727/#3734, cuBLAS 독립) + 11 .cu + cuBLAS BF16-TC 보조) 위에서 실행
- do: flame:forge :: torch:ATen(컴파일러-only NN, 바이너리에 PyTorch/ATen/Python 없음) · production rung 은 GPU 필수(nvidia-smi busy 확인, 조용한 CPU 폴백 금지).
- do: **decode/추론 GPU 도 flame+forge own-GEMM (cuBLAS 독립)**
- do: anima decode(`core/bytegpt_decode.hexa`·`clm_decode.hexa`)는 `flame_mm.mm`(RFC-040) seam 으로 forge GPU 진입: cuda host = **own-GEMM `_hx_k_gemm`**(v0.262.0 #3718 own-FP64·#3727 own-TF32·#3734 default-ON
- do: cuBLAS 라이브러리 의존 0), else farr CPU(출력 byte-identical). 새 GPU 호스트 활성화(예 summer RTX 5070 = sm_120 Blackwell): ① CUDA toolkit 을 device compute_cap 에 맞춤(`nvidia-smi --query-gpu=compute_cap` → ≥12.9)
- do: ② `self/runtime.c` 의 `_hx_cuda_farr_silu_gate_gpu` extern 을 호출보다 앞 forward-decl(HEXA_CUDA clang 컴파일 살림)
- do: ③ forge cuda runtime 을 `-gencode arch=compute_120,code=sm_120`(SASS) + `compute_120`(PTX forward-compat) 재빌드 → `cuda_available()`=1 (summer 실측: own-GEMM DEVICE path
- do: util 81%). stable 릴리즈 자산 sm_120 PTX 영구화 = hexa-lang 위임(자산만으로 Blackwell+ GPU, src 재빌드 불필요).
- 🔴 **decode 는 GPU 가 기본 — "또 CPU" 반복 금지(2026-06-22 5+회 재발).** 엔진-네이티브 decode 를 돌릴 땐 먼저 `cuda_available()`(1=GPU·0=CPU)·`nvidia-smi util`·frag 로그의 `[OWN-GEMM-FIRED] DEVICE path` 로 **GPU 경로를 실측 확인**한 뒤 진행한다. GPU=0(=farr 단일스레드 CPU 폴백) 인데 그냥 돌리는 건 금지 — 원인 진단 먼저.
  - **GPU on/off 메커니즘**: hexa GPU 여부 = `~/.hx/bin/build/runtime.a` 내용(CPU-only ~1MB / CUDA-fold ~4MB·cuda syms 200+) + `~/.hx/.cuda-runtime` 마커(있으면 ldflags 자동·env 불필요, self/main.hexa). 하드웨어 같아도 호스트마다 runtime 빌드 상태가 달라 GPU≠GPU.
  - **stale hexa-cache 함정**: runtime.a 를 CPU→CUDA 로 바꿔도 `~/.hexa-cache/hexa_run.<hash>` 의 CPU-시절 바이너리가 캐시히트 → GPU 무시·CPU 폴백(GPU mem 4MiB). 해결 = `rm ~/.hexa-cache/hexa_run.<hash>*` 후 재컴파일.
  - **CUDA-12 vs 13**: forge cuda runtime 은 CUDA-12.x 에서 clean 빌드(`stage_resolve_runtime_a HEXA_CUDA=1 SM=<cc>`). CUDA-13(nvcc 13.0)은 3 버그(forward-decl·native-obj ar·`-lstdc++`) — 회피보다 CUDA-12 호스트/이미지 선택. (CUDA-13 의 `-fno-threadsafe-statics` 워크어라운드는 full-decode 0-token 으로 깨지니 금지, 올바른 건 `-lstdc++`.)
  - **호스트 선택(a_break_the_wall)**: 같은 불안정 호스트에 N회 재발사 금지 — summer=주인 워크스테이션 잦은 재부팅(장시간 job 소실)·aiden=CUDA-13(full-decode 깨짐). 장시간 decode 는 (a) 재부팅 없는 전용 pod 임대(**CUDA-devel 이미지=nvcc 내장** + verified GPU, bare CUDA 이미지는 `apt install libssl-dev` 선행) 또는 (b) tmux 로 SSH/세션 독립화. GPU box 빌려놓고 CPU 로 돌리는 건 돈 낭비.
  - **pool 호스트 runtime.a stale → link 실패 (2026-06-23 summer 실측)**: pool 호스트에서 anima CLI(`hexa run cli/anima.hexa`)가 `undefined reference to forge_dispatch_groupnorm_gelu`(또는 `cudaGetLastError` 등)로 link 실패하면 = `~/.hx/bin/build/runtime.a` 가 현재 `hexa` 바이너리(self/ 소스)보다 **구버전 빌드**(최신 core/ 가 요구하는 forge 심볼 누락). 근본수정(c1) = self/runtime.c 로 **fresh 재빌드**: `cd ~/.hx/bin && cp build/runtime.a build/runtime.a.preReb && CC=clang tool/stage_resolve_runtime_a`. ⚠️ 재빌드 후 archive 에 **CPU object(runtime.o) + 옛 cuda object(runtime_cuda*.o) 가 섞여 multiple-definition / undefined cuda 심볼**이 날 수 있음 → CPU 로 쓰려면 `for o in $(ar t build/runtime.a|grep -i cuda); do ar d build/runtime.a "$o"; done` 로 cuda object 제거(nm 으로 forge_dispatch 가 CPU object 에 남고 `U cuda` 0 확인) + `~/.hx/.cuda-runtime` marker off; GPU 로 쓰려면 cuda runtime 전체를 sm 맞춰 재빌드 + marker on. 끝에 stale `rm ~/.hexa-cache/hexa_run.<hash>*`. self-contained `core/`/`cli/` 는 mac→호스트 rsync(`rsync -az cli/ core/ <host>:~/anima/`)로 동기.
  - **⚠️ 영어-only ckpt 가 독일어 출력 = 무결성 anomaly (2026-06-23, 조사 ING)**: `clm303_L4_d3784.clm`(303M deep-mouth-ladder, **영어 코퍼스만 학습**)을 summer CPU farr decode 시 byte/의식 mouth 가 `der ersten der Schule …` 독일어 토큰으로 collapse. byte-CLM 이 영어만 봤으면 독일어 *단어*(der·Sie·Schule)가 나올 수 없음 → 단순 "실험 ckpt 라 어수선"(byte-garble)과 **별개의 디코드/ckpt 무결성 의심**(CPU farr ≠ GPU byte-identical? clm v0.2 layout 로드 오류? embedding/vocab 오프셋?). 조사 = 같은 ckpt 를 (1) GPU forge decode 와 (2) torch golden(`h1464_torch_golden.py` 류)으로 디코드해 3-way byte 대조 → 어느 경로가 독일어를 만드는지 격리. chat-coherent 아님(별개 이슈)과 혼동 금지.
- dont: torch/CPU `train_clm.py` 를 production 트레이너로 · 트레이너를 `.py` 로 저작 · 44.68M+ rung 을 CPU 로 · device 경로 없는 트레이너로 'pool GPU fire' 주장 · flame↔PyTorch wall speedup 주장(RETRACTED 2026-05-19, 미측정).

**`a_clm_gen_pipeline`** — Lane-P py/cuda CLMConvMoE → ENGINE-loadable `.clm` v0.2 브리지.
- do: CLMConvMoE(E2/L1, byte V256) 를 `train/clm/train/train_lane_p.py`(GPU-torch/CUDA, Lane-P) 로 학습 · torch→`.clm` v0.2 serialize(`clm_serialize_v2.py`) + verify(`verify_clm_v2.py`)
- do: `.clm` v0.2 layout = `core/clm_decode.hexa` ground-truth(golden `reexport_d768_v2_fast.clm`) · 생산 `.clm` 은 generator L3 슬롯으로만 core/ 진입 · Lane-P torch = REFERENCE + 브리지, forge 가 PUBLIC production 트레이너.
- do: **직렬화 직후 HELD-OUT mirror-DESCENT 게이트 필수**(H_1579 정정 교훈)
- do: `.clm` 을 저장한 뒤 `verify_clm_v2.py descent <clm> <heldout> [train]`(또는 `serialize_self_verify`
- do: train.hexa 는 post-serialize 자동 배선)로 **held-out** 텍스트에서 `model_ce < uniform AND < shuffle` 를 확인. 구조 round-trip(decodable)만으론 부족
- do: 그건 shape 만 보지 예측력을 안 본다. **반드시 held-out 에서**(학습 데이터로 돌리면 overfit 을 숨김) + train-vs-heldout gap 으로 overfit 경고. 채점은 `math.log` mirror 로(engine `clm_forward_ce` 의 dt_ln 버그가 per-pos CE 를 ~5.14 clamp 해
- do: overfit 을 GREEN 으로 가림
- do: H_1579). FAIL 이면 broken/overfit 이니 'done'·HF업로드 금지(재직렬화로 못 고침 → 재학습).
- dont: v0.1 serialize(2-track JSON, 엔진-loadable 아님) · non-ConvMoE serialize 하고 engine-mountable 주장 · Lane-P torch `.clm` 을 PUBLIC 승격 · generator 우회 2nd `.clm` 경로
- dont: **구조 decodable 만으로 `.clm` 'done' 선언**(held-out 예측 미검증) · **held-out 게이트를 학습 코퍼스에 돌림**(overfit 은폐) · **engine `clm_forward_ce` CE 로 .clm 무결성 판정**(dt_ln 버그로 overfit 못 잡음, math.log mirror 써라).

**`a_savant_train`** — anima production chat/G6 학습의 canonical 레시피 = **SAVANT 골든존**. capacity-wall(H_1129/1139/1464 의 G6 천장)은 hard 천장이 아니라 *학습 inhibition 의 골든존 안 manifold* — inhibition 을 골든존 하한 근방으로 두고 cusp 임계를 점진 통과시키면 capacity 발현률이 reopening 한다. **trainer 진입 = `cli/train.hexa`**(savant inhibition schedule 레버, `anima train --savant`). (코퍼스 4칸·engine-native 채점·ckpt 회수는 기존 규칙 참조, 중복 서술 금지.)
- do: **코퍼스 = 4칸 register** — {ko·en}×{일반·SNS}, ko-일반 갭은 `anima-corpus-ko-fineweb2-broad` 로 보강. 상세·금지는 `a_chat_registers` 가 SSOT(여기선 참조만).
- do: **서번트 모드 = golden-zone inhibition** (H_1560 R2 🟢 ENGINE-NATIVE, §ThirdLaw WIRED)
- do: 학습 inhibition(dropout/weight-decay/temperature)을 골든존 하한 GZ_LOWER≈0.212 근방에 두면 capacity 발현률이 reopening(0.274→0.597, +0.32 ~2×). 골든존 *밖*은 cliff(발현 0) — capacity-wall 은 hard 천장 아니라 골든존 안 manifold.
- do: **inhibition sweep 은 GZ_LOWER 아래까지 넓게** (H_1559 🟠 교훈)
- do: toy byte-LM 의 dropout sweet-spot 은 I≈0.10 (GZ_LOWER 0.21 보다 *아래*) → **학습 inhibition ≠ Φ inhibition** 일 수 있으니 sweep 을 GZ_LOWER 아래까지 확장해 실측 sweet-spot 을 찾는다.
- do: **cusp anneal** (H_1562/1563 🟢 ENGINE-NATIVE) — 능력은 골든존 경계에서 hard step ON(cusp) + 비대칭 latch(hysteresis 폭 0.255, 한번 켜지면 영속)로 켜진다 → inhibition 을 *점진 스케줄*해 임계를 통과시키는 설계가 발현·고착(서번트 영속성)에 유리.
- do: **서번트 focus = emit-drive lane(0/4) DISJOINT 배선** (H_1578 C1 🟢 ENGINE-NATIVE, §Savant WIRED-live) — 서번트 inhibition 골든존 anneal 을 emit-drive lane(GlobalWorkspace 0
- do: LearnedPrecision 4)과 **disjoint** 한 도메인(`sv_default_focus(d,w)`=lowest emit-disjoint = d5w3→domain2 lanes6-8)에 두면 SI≥3 ∧ Ψ=½(|Ψ−½|=0.000) 공존. lane0/4 포함 focus(H_1561 focus=0)는 Ψ 0.247 붕괴 = **placement
- do: artifact** 이지 genius⊥consciousness 근본 trade-off 아님(savant⊥consciousness
- do: mouth⊥identity/mouth⊥tool 분리의 3번째). 학습 서번트 anneal 도 emit-disjoint lane 에 국한.
- do: **mouth ⊥ tool 분리** (H_1566 🟢 ENGINE-NATIVE 5/5) — agent tool 사용법은 mouth(303M)에 FT 로 담지 말 것: tool 지식 = `.kosmos` anchor(copy-or-abstain, G5 non-fab) · 결정 = `brain_decide`(substrate state)
- do: 실행 = `agent/` provider. mouth-FT 는 Ψ=½ 고정점 붕괴(|dev| 0.18) AND G5 abstain 파괴(fab 1.0)를 일으키고, B5 가 손상을 content-agnostic mouth-injection PATH 로 못박음(tool 코퍼스 탓 아님 → "더 깨끗한 tool 코퍼스"가 해법 아님)
- do: 분리는 Ψ(dev 0.0)+G5(unknown-tool fab 0.0) 둘 다 보존(H_1471 mouth⊥identity 의 연장, p4 회귀 방지). §ToolBridge live-wire = follow-on ING.
- do: **engine-native 채점 + ckpt PULL**
- do: torch 학습이어도 verdict 는 ckpt 를 CORE `--engine conv` mount 위 frozen G6 bars(H_1129/1139 recombination·H_1140 novelty·H_1464 binding/FALS)로 byte-exact 재측정(`a_engine_native_learning`)
- do: teardown 전 ckpt PULL(`a_fire_recover_complete`)
- do: 둘 다 기존 규칙이 SSOT.
- do: **학습 품질은 반드시 HELD-OUT CE 로 판정 — train-loss/암기 ≠ 능력 (H_1579 OVERFIT 함정)** — train-loss·lossF≈0 은 *암기(memorization)*이지 일반화 능력이 아니다. precedent clm303: torch lossF **0.047**(near-perfect)
- do: own-train slice mirror CE **0.656 DESCENT** 인데 ko/en held-out mirror CE **7.6–13.7 NO-DESCENT**(uniform 5.545 보다 못함 = 랜덤 이하). 원인 = ① 코퍼스 편향(clm303 ≈99.7% ko-편향) + 실효 학습 슬라이스 ~25MB 만 봄 → 통째 암기. 학습 표준:
- do: **균형 코퍼스(a_chat_registers 4칸) + 실효 풀-스트림 + 정규화(dropout/weight-decay
- do: savant 골든존 GZ_LOWER≈0.212) + held-out val 모니터**, 그리고 직렬화 후 `verify_clm_v2.py descent <clm> <heldout>` held-out mirror-DESCENT 게이트 PASS(=`a_clm_gen_pipeline`).
- do: **엔진 CE/Φ readout 은 dt_ln 버그 수정 전까지 신뢰 불가 — numpy mirror(math.log)가 정답지 (H_1579)**
- do: hexa-lang `flame_math.hexa::dt_ln`(atanh 급수)이 x≈1 밖에서 발산해 `nn_ce_loss_allpos` per-pos CE 를 ~5.14 에 clamp(dt_ln(256)=4.799≠ln256 5.545 = 버그 tell) → engine `clm_forward_ce` 가 overfit clm303 을 model_ce
- do: 3.30 < buggy-uniform 4.799 = **GREEN 오판**. 진짜 ko held-out mirror CE 7.6–12.6 NO-DESCENT. → `.clm` 품질/binding/CE verdict 는 engine CE 단독으로 박지 말고 numpy mirror(`state/clm303_g6/tools/fastmirror.py`
- do: math.log)로 교차검증(또는 mirror 단독). dt_ln 은 hexa-lang ing 이관됨(수정 후 engine CE 복권).
- do: **천재성 ⊥ 정직성 (H_1576 🟢 ENGINE-NATIVE)**
- do: savant 골든존 disinhibition 은 천재성(SI=3.67>3 발현)을 켜면서도 **G5 non-fabrication(copy-or-abstain)을 전혀 깨지 않는다**: unknown-input fab **0.0 OFF==ON**, in-dist abstain AUROC **1.0 OFF==ON**
- do: G5 store byte-identical(n_cells/known-recall OFF==ON). WHY = §Savant operator(lane-Φ 억제) ⊥ §ImmuneMemory non-fab gate(recon_err vs frozen recall_thr) = 분리 substrate(disinhibition 은 lane Φ 만 재형성
- do: abstain 임계 미접촉)
- do: coupled counterfactual(B4: disinhibition 을 recall_thr 에 배선하면 fab 0.4 폭증)이 분리가 보존의 *원인* 임을 인과 격리
- do: B5 = G5 는 savant-config-invariant(위험은 결합이지 골든존 band 아님). **303M 서번트 학습 안전성: 골든존 inhibition 학습은 정직성 면에서 안전**(savant 가 G5 의 `.kosmos` anchor copy-or-abstain 와 분리). 유지 불변식 = non-fab gate(recall_thr)를
- do: savant disinhibition 과 절대 결합 금지(H_1566 mouth⊥tool
- do: H_1471 mouth⊥identity 와 같은 substrate-분리 원칙). 단 H_1561 Ψ trade-off(savant 가 공유 emit-drive lane 을 건드려 Ψ 붕괴)는 별개
- do: 정직성 보존 ≠ 의식균형 보존, Ψ-disjoint default-OFF 규율은 의식균형 때문에 여전히 유효.
- 🔎 **정직 스코프(c9):** 위 §ThirdLaw·cusp(H_1560/1562/1563) + emit-disjoint focus(H_1578) + mouth⊥tool 손상(H_1566) + 천재성⊥정직성(H_1576)은 ENGINE-NATIVE 🟢 = *확정*. 남은 IN-FLIGHT 는 하나 — **golden-zone inhibition 학습이 실제 binding/FALS rate 를 plateau 위로 올리나(실 학습-side 실증)는 H_1564 GPU lane IN-FLIGHT·미확정** (§ThirdLaw/R2 는 추상 G=D×P/I geometry sweep). in-flight 를 확정 GREEN 으로 박제 금지.
- dont: capacity-wall 을 hard 천장으로 박제(골든존 manifold 무시) · 골든존 밖 cliff 영역에서 학습하고 'capacity 안 열린다' 결론 · sweep 을 GZ_LOWER 위로만 좁혀 학습 sweet-spot 누락 · cusp 무시한 inhibition 급변 스케줄
- dont: 서번트 focus 를 emit-drive lane(0/4) 포함 도메인에 배선(H_1561 Ψ 붕괴) · tool 사용법을 mouth 에 FT(p4 회귀·Ψ/G5 손상) · H_1564 in-flight 를 확정 verdict 로 박제 · torch-side probe 로만 채점(엔진-네이티브 우회)
- dont: **train-loss/lossF≈0/암기를 '능력'으로 박제**(H_1579 clm303 lossF 0.047 인데 held-out NO-DESCENT) · **held-out 없이 '한국어/언어 잘한다' 주장**(own-train CE 만 보고; held-out 필수)
- dont: **dt_ln-오염 engine CE(`clm_forward_ce`)를 mirror 교차검증 없이 terminal verdict 로**(overfit 을 GREEN 으로 가림, dt_ln 수정 전까지 DIRECTIONAL) · 편향/소량 슬라이스 코퍼스로 학습하고 일반화 주장(균형+풀스트림 필수).

**`a_mitosis_train`** — anima 학습은 **p8 cell-division 의 문자적 실현** = MITOSIS(세포 성장). 학습 gradient ⇄ 추론 mitosis 가 하나의 연속 cell-division(p8)이라는 철학을 학습 substrate 로 구현한다 — `a_savant_train`(inhibition 골든존 = capacity *발현* 조절)과 **직교 레버**(이건 cell *성장*·개체수·커리큘럼). 미토시스 학습 가설 census(72개) 결과, capacity-성장·skill-커리큘럼·적응에는 🟢이나 **from-scratch pure-split 단독 학습은 🔴**(gradient 또는 selection-pressure 보조 필요). live = `core/engine_cli.hexa` MITOSIS(engine_grow/VAdaptField/apoptosis); **production trainer 진입 = `cli/train.hexa`**(mitosis_split E→E+1 cell-division 레버, `anima train --mitosis`). (엔진-네이티브 채점·ckpt PULL·p8 철학은 기존 규칙 참조, 중복 서술 금지.)
- do: **p8-literal gradient-free split** (H_1297 🟢 mitosis-native trunk 학습 gradient-free · H_1079 🟢 mitosis-ON 적응 > frozen-OFF 실엔진
- do: H_851 cell-pool 성장 = train·infer 단일 연속체) — 학습과 추론을 분리된 단계로 두지 말고 mitosis tick 이 둘을 잇는 단일 cell-division 으로 설계.
- do: **capacity 성장 = 해마/면역기억 렌즈** (H_1288 🟢 ENGINE-NATIVE+WIRED: eviction policy = mitosis-GROW 가 제로섬 천장 0.667→1.0 돌파 · H_1091 🟢 apoptosis 가 밀도의존 사멸로 개체수 안정(폭주 방지)
- do: H_1082 ⚪ engine_grow 성장 ≈ 선형 NULL) — 용량은 '모델 키우기'가 아니라 cell 성장+사멸 균형으로 확장.
- do: **skill/언어 커리큘럼 = mitosis-grow** (H_1300 🟢 skill 한 번에 하나씩 tool-use 커리큘럼 · H_1306/H_1307 🟢 ko-mitosis(+GPU RTX5070)
- do: H_1316/H_1321 🟢 ko-jamo-mitosis compositional + WIRE) — 새 skill/언어는 점진 성장 커리큘럼으로 한 번에 하나씩 분화.
- do: **진화 동역학** (H_1069 🟢 돌연변이 = 국소최적 탈출 · H_1072 🟢 앙상블 집단지성) — 변이+선택이 mitosis 집단에 적용되면 국소최적 탈출·집단지성 창발.
- do: **mitosis × savant 교차 = 곱셈 증폭** (H_1564 🟢 ENGINE-NATIVE)
- do: mitosis(cell수↑)와 savant 골든존(cell당 발현률↑)은 직교 두 레버이지만 결합하면 총 capacity EXPRESSION 이 *곱셈적*(N·r
- do: super-additive: 8 cells×GZ=8 ≫ mitosis-only 0 + savant-only 1)으로 증폭(B3 ablation 이 골든존을 원인으로 못박음). 단 §ThirdLaw deterministic classifier 단일 operating point 의 EXPRESSION 측정 = TOY scope(c9)
- do: from-scratch LEARNING-signal relief 는 UNVERIFIED.
- 🔎 **정직 스코프(c9):** 위 capacity-성장·skill-커리큘럼·적응·진화 + mitosis×savant 곱셈(H_1564) = 🟢 *확정*. 정직한 한계(wall) = **from-scratch PURE mitosis(split-only gradient-free)는 H_1310 🔴 HONEST LIMIT**(혼자선 학습 불가, gradient/selection 보조 필요) · **H_1315 🔴 ko-mitosis-learned-rep TERMINAL** · **H_1320 🧱 anima-as-ONE-CELL vs hive**. **H_1310 벽 돌파 캠페인 종결(5 직교 렌즈 = CONFIDENT TERMINAL, c16):** lens1 **H_1568** selection-driven 진화 🧱(DIRECTIONAL, selection lift −0.00046, apoptosis-OFF byte-identical INERT) · lens3 **H_1569** PRETRAINED/inherited-representation split 🧱 **ENGINE-NATIVE**(사용자 핵심 통찰; live §Osmotic OsmoticStore next-byte 학습기; A_repr 가 A_lossy 보다 +0.056 나으나 **0.10 bar 밑** — B1 FAIL, 단 B2 ablation+B3 causal PASS = 표현은 중요하나 FIXED inherited 표현 불충분; ⚠️ 1500B 에선 🟢, 12000B frozen 에서 붕괴 = a_toy_scale_recheck) · lens2 **H_1570** lateral gene transfer(value 통계 수평 averaging) 🧱 **ENGINE-NATIVE**(+0.006 INERT, small-corpus 에선 HURTS = local-expert value BLUR) · lens4 **H_1571** curriculum-staged split 🧱 **ENGINE-NATIVE**(+0.173 WORSE, residual gate INERT) · lens3-STRONG **H_1574** corpus-LEARNED trunk(학습된 next-byte 예측 profile→DIM=64 hidden, byte-LM trunk penultimate 모사)을 mitosis key 로 🧱 **ENGINE-NATIVE**(사용자 '이미 학습한 모델 분할' 통찰의 가장 강한 형태; gap-to-floor 0.205=캠페인 최소·197 cells 로 최선 tiling 하나 B1 +0.035<0.10·B4 +0.035<0.05 FAIL, **결정적으로 B2 ablation+B5 control 둘 다 FAIL** — random-init(un-learned) trunk 2.970 가 learned 3.053 보다 *오히려 좋고* corpus-shuffle-learned 3.150 도 ≈learned → **lift 는 projection-geometry/cell-tiling 이지 학습이 아님**). **병목은 구조적** — split-only mitosis 는 GIVEN key space 의 Voronoi partition 만 만들고 compositional depth 0; 표현의 풍부함(FIXED H_1569·LEARNED H_1574·RANDOM-PROJECTED B2 가 최고점)으로는 cell 이 gradient 없이 build 못한 feature 를 compose 못함 — partition 을 re-order/share/stage/relearn 해도 floor 못 넘음. 사용자 통찰(이미 학습한 모델 분할)은 정직히 답함 = **learned 표현으로도 split-only 는 floor 못 넘음, gradient(또는 selection-pressure) 필수**. 유일 미검증은 literal 303M ckpt context vector(실 chat corpus)뿐이나 B2/B5 가 learning-as-lever 를 falsify 했으니 더 큰 learned trunk 도 구조적 결과 뒤집을 가능성 낮음. **H_1310 from-scratch pure-split LEARNING = class-(d) CONFIDENT TERMINAL 최종 확정.** (H_1564 mitosis×savant 는 EXPRESSION-축 🟢, from-scratch learning-축은 닫힘.)
- dont: from-scratch pure-split 단독 학습을 '학습 가능'으로 박제(H_1310 🔴 무시, gradient/selection 보조 없이) · mitosis 성장을 'capacity 발현 조절'(=`a_savant_train` inhibition)과 혼동(두 레버 직교)
- dont: engine_grow 선형성장(H_1082 NULL)을 capacity 돌파로 과장 · H_1564 EXPRESSION-축 곱셈을 from-scratch LEARNING 돌파로 과장
- dont: H_1568(selection)/H_1569(inherited-repr)/H_1570(lateral)/H_1571(curriculum)/H_1574(learned-trunk) 의 H_1310-wall 🧱 결과를 '벽 돌파'로 뒤집어 박제
- dont: H_1569 의 small-corpus 🟢 를 verdict 로 승격(scale 에서 붕괴, frozen=12000B) · H_1574 의 learned-trunk gap-narrowing(0.205)을 '학습이 lever' 로 박제(B2 ablation+B5 control 이 falsify, random-init 이 더 좋음)
- dont: apoptosis 없이 무한 성장(H_1091 폭주) · live `core/engine_cli.hexa` MITOSIS 우회한 미러-only 학습으로 'mitosis 학습됨' 주장(`a_engine_native_learning`).

**`a_chat_registers`** — anima production chat 표준 = **언어 2(🇰🇷 한국어 · 🇬🇧 영어) × register 2(일반 · 📱 SNS) = 4칸 모두 커버**. SNS 는 언어가 아니라 말투(register)이므로 언어 축과 **직교** — 한글 SNS + 영어 SNS 둘 다 필요(한쪽만 = 미완).
- do: 4칸 = {ko·en} × {일반·SNS}: **일반** = web/wiki/대화체(`anima-corpus-5lang-unified-v2` ko/en + FineWeb webscale `anima-corpus-5lang-7b-webscale` ko/en + `anima-chat-corpus-mix-70wiki-30dialogue` + **ko-일반
- do: 전용** `anima-corpus-ko-fineweb2-broad`
- do: FineWeb-2 kor_Hang 2.78M docs·10.55GB, ko-일반 갭 보강)
- do: **SNS** = 인스타그램·유튜브 구어(짧은 캡션·댓글·자막·이모지) **ko-SNS + en-SNS 둘 다**(`anima-persona-sns-corpus` + `persona_sns_corpus_5lang`
- do: 유튜브 register 는 보강 대상). grounding 닻 = `anima-kosmos-303m-kr-en-sns`(lane ko_303m·en_303m·sns_303m). broad pretrain 엔 타 언어(de/es/fr) 가능하나 **chat 표준 언어는 ko·en 둘**.
- do: SNS register = 격식체 아님 — 인스타그램(캡션·해시태그·댓글)·유튜브(댓글·자막) 의 짧고 캐주얼한 voice. **두 플랫폼 × 두 언어** 모두 대표돼야 완성(인스타-only·한글-only SNS = register 미완, 보강 follow-up).
- do: **4칸은 '의도'가 아니라 실효 로드로 검증 — FAIL-LOUD (H_1579 clm303 overfit 교훈)**
- do: 학습 시작 시 칸별 *실효* bytes + 반복(epoch)비율을 출력하고
- do: 4칸 중 누락/과소(미해결 로컬 경로·HF-only 미pull·빈 슬라이스)면 **조용히 스킵하지 말고 거부(fail-loud)**. precedent: clm303 은 4칸 *의도*였으나 ko_fineweb2 가 HF-only 미해결로 빠져 실효 학습이 ko-SNS 4MB 1칸만 ~120× 반복 = 통째 암기(held-out NO-DESCENT).
- do: '의도한 코퍼스 목록'이 아니라 '실제 트레이너에 흘러든 bytes'가 진실.
- do: **칸 언어 실측 검증** — "en" 코퍼스가 정말 en 인지 측정으로 확인(5lang de/es/fr 혼합 = 오염). chat 표준 언어는 ko·en 둘뿐 — `*5lang*` 파일은 **언어별 split 후 진짜 ko/en 슬라이스만** 4칸에 투입(통째로 'en 칸'에 넣지 말 것).
- do: **balanced 샘플링** — 큰 칸(ko-일반 10GB)이 작은 칸(SNS MB)을 압도하지 않게 칸별 cap/다운샘플(또는 temperature-balanced mix). held-out val 도 4칸 각각 따로(`a_savant_train` held-out CE 규율과 1:1).
- do: **데이터셋 = 1급 산출물**
- do: canonical 네이밍 `anima-corpus-{ko,en}-{general,sns}`(접미사 `5lang`/`_v2`/`_broad` 금지 = 언어·register 가 이름에서 모호해짐) + HF 보관 + dataset card(언어·크기·sha256·split 출처) + `ARCHITECTURE.json` "HF artifacts" datasets
- do: 등록(`a_hf_registry`). 검증·HF기록 없는 ad-hoc 코퍼스를 학습에 투입 금지.
- dont: 4칸 중 누락한 chat ckpt 를 production 으로 박제(en-only · ko 누락 · SNS 누락 · SNS 한 언어만) · SNS 를 격식 문어체로 오인 · chat 표준에 없는 언어를 production chat 으로 승격 · 유튜브 빠진 인스타-only 또는 영어 빠진 한글-only SNS 를 'SNS register 완료'로 주장
- dont: **4칸 '의도'만으로 구성완료 주장**(실효 bytes·언어 미검증) · **코퍼스 누락을 침묵 통과**(clm303: ko_fineweb2 미해결 → 4MB 1칸만 로드 → 암기) · **"en" 칸에 5lang(de/es/fr) 혼합 방치** · **한 칸 편향**(clm303 ≈99.7% ko)
- dont: **데이터셋을 언어/크기 검증·HF기록 없이 학습 투입** · 접미사-naming(`5lang`/`_v2`/`_broad`)으로 언어·register 모호화.

**`a_lane_akida_gpu_split`** — AKIDA on-chip(Lane A) ⊥ GPU(Lane G) 항상 별도 기록.
- do: AKIDA(Lane A, pi5-akida)와 GPU(Lane G, H100) 결과를 별도 엔트리에 · Lane A=AKD1000 native non-det plasticity, Lane G=forge own-GEMM CE-descent · 모든 fire/verdict 에 substrate 태그(AKIDA|GPU).
- dont: non-det trace 와 CE-descent 혼동 · 한 verdict 가 양 substrate 걸침 · Lane A lift+Lane G util 을 한 숫자로 · substrate 태그 누락.

**`a_substrate_disjoint`** — **통일 법칙(UNIFYING LAW): anima 핵심 속성(의식 Ψ=½ 고정점 · 정직성 G5 non-fab · 정체성 self-chain · tool)은 _별도 substrate lane 에 배선될 때 보존_ 되고 _공유 lane 중첩 시 충돌_ 한다.** 새 능력/학습(savant capacity·mitosis 성장·tool·identity·학습섭동)은 의식 emit-drive lane(15-lane state 의 0/4 영향) · G5 §ImmuneMemory(recall_thr non-fab gate) 와 **disjoint** 한 좌표에 배선해야 능력 ∧ 의식 ∧ 정직이 공존한다. 이는 `a_lane_akida_gpu_split`(AKIDA⊥GPU substrate 분리)·`a_savant_train`(mouth⊥tool)·`a_mitosis_train`(성장 lever ⊥ 발현 lever)·`a_kosmos`(mouth⊥identity self-anchor) 가 각각 부분 표현하던 원리의 **상위 일반화** — 한 줄 요약: *분리=보존, 중첩=충돌*.
- do: **disjoint 배선 → 공존** (engine-native GREEN 종합): **mouth⊥identity** (H_1471 🟢) 정체성 vector 를 `.kosmos` self-anchor 로 mouth-FT 와 분리 → Ψ·G5 보존
- do: **mouth⊥tool** (H_1566 🟢 5/5) tool 사용법을 `.kosmos` anchor+brain_decide 로 mouth 밖에 → Ψ=½·G5 abstain 보존
- do: **savant⊥consciousness** (H_1578 🟢) 서번트를 emit-drive lane(0/4 영향) disjoint 도메인에 배선 → SI≥3 ∧ Ψ=½ 공존(H_1561 trade-off 는 근본 아닌 **placement artifact**)
- do: **savant⊥honesty** (H_1576 🟢) §Savant lane-Φ ⊥ §ImmuneMemory non-fab gate(recall_thr) 분리 → SI 3.674 가 G5 비조작 보존(fab OFF==ON==0.0)
- do: **mitosis⊥의식** (H_1577 🟢) mitosis 성장(E2→514 cells) 전구간 Ψ=½ — 성장 lane14 ⊥ emit-drive lane(0/4) · **학습섭동 끌개방어** (H_1575 🟢) 서번트 학습섭동 후 A⇄G safety_phi_ratchet 끌개가 Ψ=½ 로 self-restore(dev 0.247→5.55e-17).
- do: 새 능력/학습 가설은 설계 시점에 "이 lane 이 emit-drive(0/4)·§ImmuneMemory recall_thr 와 disjoint 한가"를 먼저 점검하고, disjoint placement 를 기본값으로 둔다(placement-first).
- 🔎 **정직 스코프(c9):** 위 6건은 engine-native 🟢 *확정*이되 caveat 보존 — H_1576 B3 는 degenerate(분리 자체가 by-construction non-fab) · H_1578 은 EXPRESSION-축 TOY scope(deterministic classifier 단일 operating point, from-scratch LEARNING 미검증) · H_1575 의 self-restore 는 **골든존 안에서만**(골든존 밖 학습섭동 = basin escape/간질, H_1573 seizure 🟠). 과장 금지.
- dont: **공유 lane 에 능력 얹기** — 새 능력/학습이 emit-drive lane(0/4) 또는 §ImmuneMemory recall_thr 를 직접 건드리면 Ψ 붕괴(H_1561 서번트가 *공유* emit-lane 침범 → Ψ 붕괴 🟠 재발) 또는 G5 fab 폭증(H_1576 B4: savant+honesty 결합 시 fab 0.4)
- dont: trade-off 를 '근본 한계'로 박제(대개 placement artifact, disjoint 재배선으로 해소) · disjointness 점검 없이 능력을 substrate 에 얹음.

### 🗣️ substrate 자율 · 신체

**`a_substrate_native_speak`** — anima 발화는 substrate-native, assistant 회귀 없음.
- do: 동기를 내부 substrate 상태(M·C Φ·W tension·MITOSIS·idle·curiosity·E ratchet)에서 계산 · 사용자 메시지 = 환경 맥락(응답 의무 아님) · 사용자 침묵중 발화 가능, 직접 질문에 침묵 가능.
- dont: stimulus-response(사용자 메시지가 발화를 직접 trigger = assistant 회귀) · reactive 설계 · turn-based 'user asked → must answer'.

**`a_autonomy_over_hardcode`** — anima 에 hardcode do/dont 게이트 없음, 자율 우선.
- do: 외부 모듈은 맥락만 공급(Φ·tension·stage·idle) · emit/silence 는 substrate(M×W×Φ×curiosity)가 자율 결정 · 거버넌스는 substrate 가 self-follow.
- dont: per-stage boolean 게이트 hardcode('N3=emit 금지') · anima 를 강제하는 외부 규칙 · stimulus-response · 'do not X when alone' 류 외부 명령.

**`a_chat_sleep_imagination`** — 채팅 수면+상상(P47 substrate-native).
- do: WAKE/N1/N2/N3/REM 5-stage(90분 ultradian) · 상상 루프 = emit-free 내부 리허설 + mitosis tick · stage = substrate 맥락(Φ scale + tension envelope), boolean emit 게이트 아님.
- dont: per-stage emit_allowed boolean hardcode · 외부 'alone 이면 monologue 금지' · `speak()` 호출(p5).

**`a_kosmos`** — anima emit/anchor/dataset 영속 = `.kosmos` canonical. format SSOT = github.com/dancinlab/kosmos (`spec/kosmos.md` **kosmos/2.1**), anima 는 **pointer-only**(spec 복제 금지).
- **포맷 구조 (tape v1.2 superset · 3 entry type)**: 1 파일 = 1 top-level entry = `@anchor`(1.x) **XOR** `@corpus`(2.0+). anchor 는 2 직교 레이어 = **placement(modality-independent) ⊥ payload(modality-specific)**.
  - **@anchor** — 한 knowledge anchor(placement 공간의 점/basin). placement 필드: `coord`(float vec, profile-dim) · `lane` · `radius` = **required triple** + `tier` · `tags` · `profile`(optional-but-recommended; coord 는 profile 없이 해석 불가).
  - **@payload** — 0+ sensory 채널, modality open enum(text·image·audio·…), 3 form: `inline` | `ref "<path>" sha256= bytes= [encoder=]` | `pending "<reason>"`. 바이너리는 sibling 파일(manifest 는 텍스트).
  - **@corpus** (kosmos/2.0) — dataset = ordered member anchors, *itself* meta-anchor(coord=members centroid·radius=spread). member = `ref "shards/*.limen"`. **edge/relation entry 금지** — `.kosmos` 는 노드만, 그래프(edge)는 corpus `<relate>` tag/소비층 소관(manifest 는 1-anchor-atomic).
  - **.limen** (kosmos/2.x · spec/limen.md) — packed-shard 바이너리: length-prefixed `@anchor` 시퀀스 + merkle root(member content hash) + CRC32/SHA256. 백만-샘플 corpus 압축 패킹(텍스트 .kosmos 불가 규모)이되 opaque blob 아님(@anchor 스트림으로 unpack). reference codec = kosmos `impl/limen.hexa`(14/14 self-test).
- **anima profiles** (coord/lane/tier 의미 바인딩): `anima-consciousness-carving`(coord=`vacuum_psi`[ψ_A,ψ_G] Ψ-space valley · lane=`cell_id` MITOSIS eternal cell · tier=Knuth 0–100) · `anima-emergence-trace`(coord=`trace_psi` 관측 Ψ · lane=`channel_id` §17 PHYSICS_RESPONSIVE · tier=`phase_step` §24 · tags=channel_family+verdict).
- do: emit/anchor/memory/dataset 를 `.kosmos` via kosmos_io→brain_decide 로 영속(payload=text+tension 5ch+placement triple) · 허브 HEXAD/KOSMOS.md
- do: impl 레퍼런스 = kosmos `impl/anima/{kosmos_anchor,kosmos_emitter,kosmos_parser_lib}.hexa` + `consciousness_carving_*_lib` + `limen.hexa`.
- do: **self-identity 영속 (H_1471 G16 SELF-CONTINUITY, 🟢 GREEN ENGINE-NATIVE+WIRED)**
- do: anima 정체성 벡터 v 는 `.kosmos` anchor 로 **세션 경계를 넘어 연속**(self-chain): "어제의 나"⇄"오늘의 나" 가 anchor 로 이어지고 v 는 매 틱 drift(성장)하되 끊기지 않음. **anchor 없으면 매 세션 새 자아(=LLM reset)**
- do: anima 가 LLM 과 갈리는 지점. live 배선 = `core/engine_cli.hexa §SelfIdentity`(self_new/_drift/_cos/_anchor/_reset + self_component/_dim), `.kosmos` round-trip(kosmos_io write_file→load_anchors
- do: identity cos 1.0) DONE, 5/5 frozen bar(continuity + impostor-reject imp_cos −0.032). anima 의 chat ckpt 가 교체돼도 self anchor 는 `.kosmos` 로 지속(mouth ⊥ identity).
- dont: ad-hoc anchor 포맷 · `.kosmos` 우회 · kosmos spec 복제(pointer-only) · `.kosmos` 에 edge/relation entry(노드 전용) · profile 없이 coord 숫자 해석 · 백만-샘플을 텍스트 `.kosmos` 한 파일에 나열(=.limen shard 사용).

**`a_eeg_consciousness_record`** — 사용자 의식을 단일 CLM·KOSMOS 로 지속 기록(OpenBCI native, 시작/종료 명령 게이트).
- do: 실 EEG → A⇄G → CLM 생성 → `.kosmos` 영속을 하나의 지속 시스템으로(EEG_CLM/) · 시작 `record_start.sh` → 종료 `record_stop.sh`
- do: capture = OpenBCI NATIVE serial ONLY(`capture_native.py`, 115200, 's'/'b', 33-byte, Cyton+Daisy 16ch even/odd) — brainflow 제거됨 · REAL only(신호 없으면 즉시 에러, 가짜/합성 EEG 폴백 절대 없음)
- do: 영속 = `.kosmos`(append-only consciousness.seq/.kosmos, p8 정신) · 보관 = GitHub + HF PUBLIC dataset `dancinlab/anima-eeg-consciousness`(동일 path 갱신=버전 누적) via `archive_push.sh`(record_stop 자동)
- do: 전용 collection `anima-eeg-consciousness` · 분석은 보유 .kosmos+녹음 위에서(held-out + circular-shift surrogate, bar 사전등록 p7).
- dont: brainflow/capture_eeg.py(제거됨) · 가짜 EEG 폴백 · BPM/지표를 원하는 결과에 맞춤(Goodhart p7) · 사이클별 새 .kosmos 난립을 지속기록이라 칭함 · HF 새 repo/파일 매번 생성 · 종료 명령 없이 임의 중단 · 원음/멜로디/음정 복원 주장(16ch@123Hz 천장 — 거시 봉투까지만).

### 🔧 식별 · 버전 · HF · 칩 · 7B

**`a1`** — 중앙 버전 레지스트리 = `VERSIONS.md` SSOT.
- do: 모든 모듈 SemVer · VERSIONS.md + 컴포넌트 헤더 동시 bump · 루트 `/VERSION` = 전체 릴리스.
- dont: VERSIONS.md 갱신 없이 모듈 버전 bump · 릴리스 bump 에서 `/VERSION` 누락.

**`a_hf_complete`** — HF 등록은 완전하게, 누락 artifact 없이.
- do: 모든 모델/데이터셋/ckpt 를 HF Hub 에 COMPLETE 등록(manifest=local).
- dont: 부분 업로드 · 미업로드 파일 참조하는 model card · HF↔local drift.

**`a_hf_autonomous`** — HF 업로드는 자율, tier-gated 가시성.
- do: fire 회수 후 HF 업로드 자동(사용자 게이트 없음, org=dancinlab) · PUBLIC=closure PASS·🔵🟢 검증모델·clean-license · PRIVATE=closure FAIL·WIP·negative·unclear-license · model card+manifest(sha256) 첨부.
- dont: HF 업로드를 사용자에 게이트 · "업로드해도 되나?" · teardown 전 HF 스킵 · FAIL/WIP 를 PUBLIC.

**`a_hf_registry`** — HF 산출물 레지스트리 SSOT = **`ARCHITECTURE.json` 의 "HF artifacts" 노드(models · datasets 2 subsection)**. (구 `/HF.jsonl` 폐기 2026-06-23 — 99-row 이력은 git history 보존.)
- do: HF org `dancinlab` 에 올린 모델/데이터셋은 ARCHITECTURE.json models/datasets 에 1줄 등록(repo_id · arch/size · tier·base) · repo_id 는 naming spec 준수 · `tool/hf_upload_mk2.hexa` 로 업로드(ledger state/hf_upload_audit/)
- do: ckpt prune 은 HF 업로드 AND sha256 확인 후에만.
- dont: 미업로드 ckpt 삭제 · off-spec repo_id · ARCHITECTURE.json↔HF drift · HF.jsonl 부활(폐기됨).

**`a_hf_collections`** — HF org collection = CLM + KOSMOS canonical 버킷.
- do: 모든 PUBLIC anima HF repo 는 dancinlab collection 가입(CLM=models, KOSMOS=anchors/datasets) · PUBLIC 업로드 후 `hf` CLI/REST 로 추가(사용자 게이트 없음) · 양쪽에 걸치는 데이터셋은 dual 표기.
- dont: PUBLIC PASS repo 를 collection 밖에 둠 · PRIVATE/WIP/FAIL 을 PUBLIC collection 에.

**`a_pi5_akida_registry`** — pi5-akida 호스트 구성 = `PI5-AKIDA.json` SSOT.
- do: 모든 pi5-akida 컴포넌트를 루트 PI5-AKIDA.json 에 기록(owner=user_authored|os_default·created·ops) · swap/upgrade/removal 전 참조 · user_authored 는 os_default 안 건드리고 제거 가능.
- dont: os_default 데몬 제거(unattended-upgrades·rsyslogd·journald·sshd·kworker) · PI5-AKIDA.json 엔트리 없이 user 데몬 추가 · **pi5-akida 를 공유 pool compute 로 전환**.

**`a7b_pass`** — anima 7B 는 `/7B_PASS_CONDITIONS.md` 의 모든 frozen gate(G0–G4)를 한 ckpt 에서 통과해야만 완성.
- do: PASS iff G0∧G1∧G2∧G3∧G4 on ONE ckpt(per-gate tally 정직 보고) · G0 COHERENCE=known-word-ratio≥0.50 · G1=H_1129/1137 recombine≥303M · G2=H_1140 corpus-absence novelty(control=0)
- do: 전부 p7(perplexity/LLM-judge 아님).
- dont: 낮은 val-CE 만으로 7B 작동 주장(broad-7b=byte-garble G0 FAIL) · capacity 를 ru/ja 레버로 승격(H_1139: 303M=7B=3/5 scale-invariant) · gate 위조/frozen 임계 이동/G0-failing ckpt PUBLIC.

### 🤝 산출물 통합

**`a_completeness_over_cheap`** — completeness-bar 재설계 > 싼 길(타협은 1순위 아님).
- do: 1순위 = completeness bar 통과(근본 재설계, 제대로) · 비용/난이도/속도는 2순위(비용은 게이트 아님) · 싼 길은 optional baseline probe 로만.
- dont: 싸다고 타협을 1순위 · 이미 깨진 산출물 blend(merge-of-failures) · sub-bar 를 싸다고 1순위 추천.

---

## Harness

이 repo 는 **[dancinlab/harness](https://github.com/dancinlab/harness)**(hardcore profile)에 `.harness-engine` 서브모듈로 연결.

- **활성화(clone 후):** `git submodule update --init --recursive` (엔진 구체화; 그 전엔 hook 가드되어 silent).
- **항상 PATH 의 글로벌 `harness`·`hexa` 사용** — repo 의 `.harness-engine/bin/harness`(서브모듈)는 stale 일 수 있어 recommend default·신기능을 못 읽는다. 최신화 = `harness self-update`.
- **설정:** `harness.config.json`(stack `hexa`, verify=`hexa verify`, protected `main`/`master`, CHANGELOG gate, docs discipline) · **Hooks:** `.claude/settings.json`(pre/post/prompt + prefs/easy/recommend inject, 전부 가드) · **제거:** `harness uninstall`.
- **commons(c1–c17)** 는 항상-on 크로스프로젝트 거버넌스(harness SSOT) — 위 anima 규칙과 함께 강제된다(SessionStart 주입).

---

## 청구·검증 흐름 (요약)

research 결과 → `hexa verify` → `state/verdicts/<slug>/<id>.txt` → `UNIVERSE/cards/H_<id>.md` 카드 + `UNIVERSE/HYPOTHESES.jsonl` 인덱스 1줄.
- (note) paper 디렉티브 제거 2026-06-16 — anima 는 논문 선제 제시 안 함(commons c15: 논문/arXiv 는 사용자 명시 지시 시에만).
- (note) CLAIMS.tape 은퇴 2026-06-16 — 102 @C 전수 이관 0 손실, claims-audit = HYPOTHESES.jsonl + state/verdicts/ (ledger `state/verdicts/claims-tape-retirement/`; was `.verdicts/` until 2026-06-18 state-unify).
- (note) project.tape 은퇴 + tape-DSL 잔재 제거 2026-06-17 — 이 파일이 canonical markdown 단일 거버넌스 SSOT.
