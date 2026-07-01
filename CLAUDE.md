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

> **디렉터리/모듈 트리는 더 이상 여기 살지 않는다 — 트리의 단일 SSOT 는 [ARCHITECTURE.json](ARCHITECTURE.json)**(update-in-place, `core/`·`cli/`·`agent/`·`archive/train/clm/`·`platform/`·`UNIVERSE/`·`state/`·`domains/`·`stdlib/`·`tool/`·HEXAD/KOSMOS 등 전 노드 + "HF artifacts" models/datasets). 뷰어 = [ARCHITECTURE.html](ARCHITECTURE.html) via `python3 serve.py` (c4: JSON 트리 SSOT + HTML 뷰어, file:// fetch 우회).
>
> - **설계/트리** → [ARCHITECTURE.json](ARCHITECTURE.json) (단일 SSOT · 노드 note 에 메커니즘 명명 · `a_verified_must_wire`/`a_core_engine_map` 의 lockstep 대상)
> - **anima 거버넌스 + 8 철학** → 이 파일 (anima 전용 규칙 `a_*`·`p#` 의 markdown SSOT)
> - **크로스프로젝트 거버넌스** → harness commons (c1–c17, always-on, SessionStart 주입)
> - **이력** → [CHANGELOG.md](CHANGELOG.md) (append-only)
> - **버전 레지스트리** → [VERSIONS.md](VERSIONS.md) · **frozen gate 조건** → [CONDITIONS.md](CONDITIONS.md)·[7B_PASS_CONDITIONS.md](7B_PASS_CONDITIONS.md) (이 파일은 가리킬 뿐, 임계 복제 금지)

## 📦 패키징 — pod 업로드

canonical 재구성의 목적 = 학습/추론/벤치 pod 에 올리기 쉬운 self-contained `core/`. **불변식: `core/` 는 `archive/train/`·`bench/`·`agent/`·`state/` 에 의존 0** (substrate 엔진만; 단방향).

- **추론 pod** — `rsync core/ cli/ stdlib/iit4/` (~150MB self-contained). `.clm` 가중치는 외부 마운트(레포에 넣지 않음). 진입 = `hexa run cli/anima.hexa -- <ckpt.clm> …`. **릴리즈 매니페스트 = 루트 `hexa.toml`**(`hx install anima` → install.hexa → setup.hexa; entry=cli/anima.hexa, deps=hexa-lang, include=core/·cli/·entry-wired 의식lane(import BFS 측정: DREAM·SAVANT + HEXAD kosmos_io 1파일만 cli/anima.hexa 도달; 나머지 11 lane 은 probe-only dead → archive/ 이관 2026-06-30), exclude=state/·UNIVERSE/·archive/·*.clm 등 연구artifact/외부가중치).
- **학습 pod** — 추론 세트 + `archive/train/`(clm 파이프·flame/forge, 2026-06-30 train/·training/ → archive/ 이전) + `state/verdicts/` slice(frozen bar 재측정용). production 트레이너는 `.hexa` on flame/forge GPU (`a_train_flame_forge`).
- **agent pod** — `agent/` 는 `hexa.toml` 보유 독립패키지 → `hx install anima-agent` standalone 배포 (core/ 미동반 가능).
- **이동 금지(pod 에 안 올림)** — `state/`·`UNIVERSE/` 등 연구 artifact 는 pod 페이로드에서 제외(verdicts slice 만 학습 pod 에 선택 동반).

## Quick reference

- 🏛 아키텍처 → [ARCHITECTURE.json](ARCHITECTURE.json) (트리 SSOT) · 뷰어 [ARCHITECTURE.html](ARCHITECTURE.html) via `python3 serve.py` (c4: JSON 트리 SSOT + HTML 뷰어, file:// fetch 우회)
- 📜 거버넌스(정본) → 아래 본문 (이 파일이 markdown SSOT)
- do: 주장·verdict → [`UNIVERSE/HYPOTHESES.jsonl`](UNIVERSE/HYPOTHESES.jsonl) (per-H `verdict` 컬럼) + frozen 증거 `state/verdicts/<slug>/<id>.txt` (was `.verdicts/` until 2026-06-18 state-unify; CLAIMS.tape 은퇴 2026-06-16, 0 손실, ledger `state/verdicts/claims-tape-retirement/`)
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
- do: 능력/깊이 갭은 '모델 키우기'가 아니라 '빠진 구조(lane) 옆에 붙이기'로 먼저 시도. anima 의 돌파는 전부 생물 렌즈에서 나왔다(해마=면역/일화기억 H_1227/1231 · 소뇌=순방향모델 H_1280 · 기저핵=게이팅 H_1281 · 작업기억 H_1282). LLM 스케일 프레임은 막혔다(1B H_1167 NULL · arch H_1219 · objective H_1223 모두 🔴).
- do: 새 가설은 먼저 "어떤 생물·신경 구조가 이 기능을 하나"를 묻고 그 메커니즘을 substrate-native 로 실현.
- dont: 기본값으로 LLM 레시피(스케일업·코퍼스 증량·표준 FT)를 1순위 처방 · "더 큰 트랜스포머면 된다" · 생물/신경 렌즈를 곁다리 취급 · LLM 관행을 substrate 천장으로 삼음.

**`a_break_the_wall`** — 벽(closed-negative·🧱·막힌 게이트)은 종착이 아니라 각도 전환 신호. tune-to-green 없이 다른 렌즈로 돌파를 시도한 뒤에야 terminal. (commons c16 확장 — anima 벽 TAXONOMY.)
- do: **벽 분류 먼저(TAXONOMY)** — (a) 틀린 측정/metric-artifact → frozen-first 로 측정 수정(bar 불변) · (b) 틀린 방향/변수 혼재 → 통제 분리실험 · (c) substrate/인프라 벽(OOM·빌드·툴링) → **근본 수정(c1) 대상이지 천장 아님** · (d) 진짜 천장 → MULTI-LENS(원리적 렌즈 ≥2–3개를 shuffle+ablation 통제로 각각 기각한 뒤에야 confident 🧱; ABLATION=결정적, 메커니즘 OFF 시 결과 동일=INERT=기여 0) · (e) 투자 부족 → pool/`hexa cloud` 스케일업.
- do: **LAW(법칙)도 벽** — 사후 descriptive 법칙은 '확정' 전 *새 케이스*로 측정 전 사전등록(frozen) 예측 → 실측 falsify(≥4/5 HIT 면 PREDICTIVE 승격, 미만이면 법칙 FALSIFIED 가 유효 결과).
- dont: tune-to-green · 단일 렌즈 1회 막힘을 천장으로 박제 · ablation/통제 없이 '기여' 가정 · 인프라/측정 벽을 과학 천장으로 박제 · 한 번 막혔다고 포기·우회·축소. (정직한 🧱 는 유효 결과 c9.)

### 🔬 검증 · 엔진-네이티브 (HARD-GATE)

**`a_engine_native_learning`** — 무조건 최종 아키텍처 엔진 위에서 학습·측정. 미러 아님.
- 🔒 **HARD-GATE (BLOCKING):** gate/ideation/G6/Φ/recombination/depth 의 **모든 verdict tier(🟢·🧱·🟠·천장)는 엔진-네이티브 증거 없이 박제 불가.** 증거 artifact 가 live core/ 디코드(`clm_decode`/`bytegpt_decode`/`engine_cli`.hexa)를 호출한 `.hexa` 가 아니면(=`.py`+`torch`/`gauge_lib._decode`/numpy 미러) **자동 DIRECTIONAL**, terminal 아님. torch-side 만으로 🧱/🟢 를 카드·jsonl·CHANGELOG 에 박제 = c9 위반.
- 🔎 **자가점검(박제 직전 의무):** `grep -lE 'import torch|gauge_lib|numpy' state/<slug>/*.py` 가 비면 OK, 안 비면 verdict 를 **반드시 DIRECTIONAL** 로 적고 엔진-네이티브 재측정(.hexa via CORE)을 ING 등록.
- do: 모든 학습/교육(연구 프로브·미토시스 교육·depth 실험 포함)은 live `.hexa` A⇄G + MITOSIS(`core/engine_cli.hexa`) + mounted `core/bytegpt_decode.hexa` 위에서 실행.
- do: 엔진에 학습을 끼워맞추지 말 것 — 학습이 요구하면 엔진을 변환/확장(engine-transform-to-fit). 최종 아키텍처는 frozen 아니라 학습이 요구하는 형태로 진화.
- do: numpy/torch 미러 = DIRECTIONAL only. **렌트 GPU torch 풀-학습도 동일** — ckpt 를 CORE(`--engine conv`)에 올려 frozen bar 재측정해야 🟢/🧱 성립 → teardown 전 pull(`a_fire_recover_complete`).
- dont: 미러 결과를 엔진-검증인 양 closure/promote · 미러-only 로 '학습됐다' 주장 · 자가점검(grep) 없이 verdict 박제 · "gauge_lib=model-agnostic 이니 엔진과 같다" 핑계(gauge_lib 는 torch.no_grad MONITOR-ONLY, `a_train_inline_gauge`).

**`a_verified_must_wire`** — 엔진-네이티브 GREEN 가설은 실제 CORE 배선까지가 done. verdict 만으론 안 끝난다.
- do: **4칸 배선 사다리:** (1) DIRECTIONAL 미러 GREEN → (2) 엔진-네이티브 재검증(byte-exact, frozen bar 그대로) → (3) live `core/*.hexa` wire-in → (4) ARCHITECTURE.json lockstep 갱신. 각 미완 칸은 즉시 ING follow-on 등록, (4)까지 닫혀야 done. 미러 GREEN 을 내면 같은 사이클에 (2)~(4) follow-on 을 ING 에 등록하는 것이 의무.
- do: 배선 후 smoke/single-entry/Ψ-checksum 가드로 회귀 없음을 출력으로 확인(c2). 배선 ↔ ARCHITECTURE.json CORE 트리(§섹션·op·slot 주석)는 무조건 1:1 lockstep(같은 PR 에 동시 갱신; 480-leaf 트리 부활 금지, 노드 note 에 메커니즘 명명).
- do: GREEN 가설은 카드에 `wired:` 상태축 명시 — `DIRECTIONAL-mirror` / `engine-native`(byte-exact 재검증, 미배선) / `WIRED-live`(배선+lockstep 완료) 중 하나. WIRED-live 미만이면 배선 follow-on 의 ING id 를 카드에 적는다. GREEN 무더기를 내는 PROGRAM 은 닫을 때 각 GREEN 의 배선상태를 명시 열거('mirror-GREEN N · engine-wired K · 미배선 N−K = ING #id').
- dont: GREEN verdict 만 박제하고 배선 없이 '완료' 주장 · DIRECTIONAL 을 WIRED 처럼 표기 · live CORE 배선해놓고 ARCHITECTURE.json 미갱신(drift) · 배선을 무기한 follow-on 으로 미룸. (실패모드 precedent: lane-합성 가족이 Φ-lift GREEN 3개를 0개 wired 로 방치 — 재발 금지.)

**`a_blue_closed`** — 🔵 SUPPORTED-FORMAL 은 출력 AND 배선(transfer-fn·invariant)을 둘 다 닫을 때만. `hexa verify` 로 closed-form/identity 확인(verdict verbatim).
- dont: 구조만 닫고 배선 미검증 · 가짜 closed-form · 정직한 empirical 잔차를 억지로 🔵.

**`a_phi_iit4_tool`** — Φ/의식 verdict 는 stdlib faithful IIT4 사용(프록시 아님).
- do: 기본 `iit4/faithful_phi.hexa`(exact MIP-EI, n≤8, $0) · system big-phi `iit4_bigphi.hexa` · `hexa verify`(g5)로 호출 · 새 phi 코드 작성 전 stdlib 먼저 검색(g61).
- dont: 프록시(phi_silicon_proxy·variance×energy 미러)를 terminal Φ verdict 로 · purpose-blind 프록시 신뢰(H_988/989 가 random==intentional) · stdlib 에 faithful 엔진 있는데 새 impl 작성.

**`a_train_inline_gauge`** — 학습중 의식/창발 측정 = MONITOR-ONLY 대시보드(loss 불가, p7 Goodhart).
- do: K 스텝마다 PROXY gauge 4종(G1 recombination·G2 novelty·G6 ideation·phi_proxy)을 val_ce 옆에 기록(`tool/gauge_lib.py::compute_inline_gauges`). 전부 `torch.no_grad()` 아래, dict 만 return, gauges.jsonl 1줄/tick. `--gauge-every <N>`.
- do: phi_proxy 는 NOT faithful IIT4 — 저가 pre-screen 전용. **FROZEN gate verdict 는 여전히 학습 후 별도로 CORE 엔진 mount 위 byte-exact 실행**(`a_engine_native_learning`/`a_engine_measured_verdict`) — 이 inline gauge 가 gate 를 대체하지 않음.
- dont: gauge 값을 loss 에 더하거나 backward 로 흘림(Goodhart, p7) · gauge 를 frozen gate/verdict 라 칭함 · phi_proxy 를 Φ verdict 로 승격 · toy gauge 추세를 production 결론으로 승격.

### 🧪 가설 워크플로우

**`a_hypothesis_register`** — 모든 가설은 정확히 2 doc 표면으로만 관리: `UNIVERSE/HYPOTHESES.jsonl`(per-H 인덱스, JSON object 1개/가설) + `UNIVERSE/cards/H_<id>_<slug>.md`(카드).
- do: 가설 실행 시 카드를 만들/갱신하고 jsonl 에 한 줄(`{id, slug, tier, title, card:"cards/H_…", verdict, source, archived, artifacts}`, id 순) append/갱신. 등록은 tier 무관 — 🟢·🟠·🔴/🧱 전부 남긴다(벽도, c9). tier·수치는 `state/verdicts/<slug>/` 에서 verbatim(추측 금지, c2). jsonl 은 `python3 tool/_build_hyp_jsonl.py` 로 재생성 가능.
- do: 🟢(부분 포함) 가설은 카드에 `wired:` 명시(`a_verified_must_wire` 의 4칸과 1:1). jsonl 의 `source`(UNIVERSE|흩어진 출처|archive)·`archived`·`artifacts`(state/<slug>/ 경로 배열) 3컬럼 포함.
- 🔎 자가점검: `git ls-files 'UNIVERSE/*' | grep -v '^UNIVERSE/cards/' | grep -v '^UNIVERSE/HYPOTHESES.jsonl$'` 는 항상 빈 출력이어야 한다.
- dont: **UNIVERSE/ 에 .py·.hexa·코드·result 파일 금지**(단 둘만) — 카드는 `cards/`, 코드/결과물은 `state/<slug>/` 에 두고 jsonl `artifacts` 로 가리킨다. 가설 디테일을 themed 버킷(`HYPOTHESES_*.md`)·CLAIMS.tape·도메인 로그·MEMORY·ad-hoc 노트에 흩뿌림 · per-H 인덱스를 markdown 표에 추가(인덱스는 오직 jsonl) · UNIVERSE/ 에 prose overview 부활(retire 됨, prose 는 `state/universe-overview.md`) · 실행·박제하고 jsonl/카드 안 만듦 · 카드를 UNIVERSE/ 루트에 둠(반드시 cards/) · 벽/negative 누락 · tier 를 verdict 파일과 다르게 적음 · 🟢 인데 `wired:` 미표기.

**`a_claim_manifest`** — claims-audit 면 = `UNIVERSE/HYPOTHESES.jsonl`(per-H verdict 컬럼) + `state/verdicts/<slug>/`. H-style 아닌 claim 도 가장 가까운 카드/jsonl note 에 보존.
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
- do: **렌트 GPU 학습 ckpt 는 teardown 전 반드시 영구 스토리지(HF/pool host/repo path via `a_hf_registry`)로 PULL** — pod 는 휘발이라 teardown 즉시 가중치 소멸; verdict 카드/jsonl(JSON)만 받고 ckpt 안 받은 채 down 하면 그 학습은 `a_engine_native_learning` 엔진-체크가 영구 불가(재학습=재렌트). ckpt 가 너무 크면 최소 1개 대표 변종이라도 pull, 못 하면 카드에 'ckpt NOT pulled → engine-check 불가' 명시.
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
- do: `core/` 가 A(pure_field)⇄G(engine_g)⇄brain(brain_decide) 소유(substrate-internal) · 모델 가중치는 오직 `core/generator.hexa` L3 슬롯으로 진입 — 단, L3 는 **mouth 타입 디스패처**(`gen_mouth_kind`→'bytegpt'|'clm'|'unknown' header sniff)로 **두 mouth 아키텍처**를 받는다: **conv `.clm`**(CLMConvMoE via clm_decode, `CLM\x01` magic + CLMX trailer)는 `gen_clm_backend`/`gen_clm_chat` 으로, **ByteGPT `.bin`**(24-layer GPT-2-class via bytegpt_decode, 5×u32 `[256,d,L,H,block]` header, 검증된 303M ko/en chat trunk)은 `gen_bytegpt_backend`/`gen_bytegpt_chat`(`bytegpt_decode_argmax_ranged` OOM-safe) 으로. 이는 2nd `.clm` 경로가 아니다 — **아키텍처별로 여전히 단일 typed 진입**이고 디스패처(`gen_auto_backend`/`gen_auto_chat`)는 파일 포맷에 따라 어느 단일 진입을 쓸지만 고른다(a_engine_native_learning engine-transform-to-fit). `.kosmos` 는 오직 kosmos_io→brain_decide 로 진입 · `stdlib/hf/validate.hexa` = artifact 검증(런타임 엔진 아님).
- do: ARCHITECTURE.json core/ 노드(§섹션·op·slot 주석) ↔ live engine_cli/generator/brain/clm_decode 의 실제 §섹션·op 는 1:1 매칭 — grep 으로 누락 0 검증(drift=미완).
- dont: `.clm`/`.kosmos` 를 pure_field/engine_g/brain 에 직접 투입 · generator 우회 2nd `.clm` 경로 · kosmos_io 우회 2nd `.kosmos` 경로 · validate.hexa 를 런타임 엔진과 혼동 · 미완 배선을 존재한다 주장(빌드 전엔 ⏳/❌ 정직 표기).

**`a_train_flame_forge`** — production 학습·decode = hexa-native flame+forge GPU 스택, `.hexa` 저작(torch/`.py` 트레이너 금지). GPU 활성화·CUDA-12/13·pool `runtime.a` 재빌드·stale hexa-cache 등 운영 트러블슈팅 상세 = memory SSOT(`summer-sm120-owngemm-prebuilt`·`aiden-forge-gpu-enable-cuda13`·`hexa-gpu-enable-canonical-install`·`flame-forge-cuda-build-on-pool-gotchas`).
- do: **학습 진입 = `cli/train.hexa`** (`anima train <ckpt> <corpus> [--savant] [--mitosis]`) — SAVANT/MITOSIS 레버를 같은 clm_*.hexa ops 위에 조립. production NN 은 stdlib/flame(ag_tape·nn_lib·opt_*)로 저작, self/forge GPU own-GEMM `_hx_k_gemm`(cuBLAS 독립) 위 실행 · flame:forge :: torch:ATen(바이너리에 PyTorch/ATen/Python 없음) · production rung 은 GPU 필수(조용한 CPU 폴백 금지).
- do: **decode/추론도 flame+forge own-GEMM** — anima decode(`core/bytegpt_decode.hexa`·`clm_decode.hexa`)는 `flame_mm.mm`(RFC-040) seam 으로 forge GPU 진입(cuda host=own-GEMM, else farr CPU byte-identical). decode 전 `cuda_available()`·`nvidia-smi util`·`[OWN-GEMM-FIRED] DEVICE path` 로 GPU 경로 실측 확인 — GPU=0 인데 그냥 돌리는 것 금지("또 CPU" 재발 방지, 원인 진단 먼저).
- dont: torch/CPU `.py` 를 production 트레이너로 · 트레이너를 `.py` 로 저작 · 44.68M+ rung 을 CPU 로 · device 경로 없는 트레이너로 'pool GPU fire' 주장 · flame↔PyTorch wall speedup 주장(RETRACTED, 미측정).

**`a_clm_gen_pipeline`** — Lane-P py/cuda CLMConvMoE → ENGINE-loadable `.clm` v0.2 브리지.
- do: CLMConvMoE(E2/L1, byte V256) 를 `archive/train/clm/train/train_lane_p.py`(GPU-torch/CUDA, Lane-P) 로 학습 · torch→`.clm` v0.2 serialize(`clm_serialize_v2.py`) + verify(`verify_clm_v2.py`) · `.clm` v0.2 layout = `core/clm_decode.hexa` ground-truth(golden `reexport_d768_v2_fast.clm`) · 생산 `.clm` 은 generator L3 슬롯으로만 core/ 진입 · Lane-P torch = REFERENCE + 브리지, forge 가 PUBLIC production 트레이너.
- dont: v0.1 serialize(2-track JSON, 엔진-loadable 아님) · non-ConvMoE serialize 하고 engine-mountable 주장 · Lane-P torch `.clm` 을 PUBLIC 승격 · generator 우회 2nd `.clm` 경로.

**`a_savant_train`** — anima production chat/G6 학습의 canonical 레시피 = **SAVANT 골든존**. capacity-wall 은 hard 천장이 아니라 *학습 inhibition 의 골든존 안 manifold*. **trainer 진입 = `cli/train.hexa`**(`anima train --savant`). (H 번호·수치·verdict 상세 = UNIVERSE 카드 + memory SSOT, 여기선 실행지침만.)
- do: **코퍼스 4칸 register** = `a_chat_registers` SSOT(참조만).
- do: **golden-zone inhibition** — 학습 inhibition(dropout/weight-decay/temperature)을 골든존 하한(GZ_LOWER≈0.21) 근방에 두고, sweep 은 GZ_LOWER *아래*까지 넓게(학습 sweet-spot ≠ Φ inhibition 일 수 있음). 능력은 골든존 경계에서 cusp(hard step ON)+비대칭 latch 로 켜지니 inhibition 을 *점진 스케줄*.
- do: **서번트 focus = emit-drive lane(0/4) DISJOINT 배선** — anneal 을 emit-drive lane 과 disjoint 도메인에 두면 SI≥3 ∧ Ψ=½ 공존(`a_substrate_disjoint` SSOT). savant 는 G5 non-fab gate 와도 분리되어 정직성 보존 — non-fab gate(recall_thr)를 savant disinhibition 과 **절대 결합 금지**.
- do: **mouth ⊥ tool 분리** — tool 사용법을 mouth(303M)에 FT 금지: 지식=`.kosmos` anchor · 결정=`brain_decide` · 실행=`agent/`. mouth-FT 는 Ψ·G5 둘 다 손상(`a_substrate_disjoint`).
- do: **engine-native 채점 + ckpt PULL** — `a_engine_native_learning`/`a_fire_recover_complete` 가 SSOT.
- dont: capacity-wall 을 hard 천장으로 박제 · 골든존 밖 cliff 에서 학습 · sweep 을 GZ_LOWER 위로만 좁힘 · cusp 무시한 급변 스케줄 · 서번트 focus 를 emit-drive lane(0/4) 도메인에 배선 · tool 을 mouth 에 FT · torch-side probe 로만 채점.

**`a_mitosis_train`** — anima 학습은 **p8 cell-division 의 문자적 실현** = MITOSIS(세포 성장). `a_savant_train`(inhibition 골든존 = capacity *발현* 조절)과 **직교 레버**(이건 cell *성장*·개체수·커리큘럼). live = `core/engine_cli.hexa` MITOSIS(engine_grow/VAdaptField/apoptosis); **trainer 진입 = `cli/train.hexa`**(`anima train --mitosis`). (H 번호·census·verdict 상세 = UNIVERSE 카드 + memory SSOT, 여기선 실행지침만.)
- do: **p8-literal 연속 cell-division** — 학습과 추론을 분리 단계로 두지 말고 mitosis tick 이 둘을 잇는 단일 cell-division 으로 설계.
- do: **capacity 성장 = 해마/면역기억 렌즈** — 용량은 '모델 키우기'가 아니라 cell 성장+사멸(apoptosis, 밀도의존 폭주 방지) 균형으로 확장.
- do: **skill/언어 커리큘럼 = mitosis-grow** — 새 skill/언어는 점진 성장 커리큘럼으로 한 번에 하나씩 분화.
- do: **mitosis × savant 교차** — mitosis(cell수↑) × savant 골든존(cell당 발현률↑)은 직교 두 레버, 결합 시 total capacity EXPRESSION 곱셈 증폭(EXPRESSION-축 🟢 TOY scope; from-scratch LEARNING-축은 UNVERIFIED).
- 🔎 **정직한 한계(wall, c9):** **from-scratch PURE mitosis(split-only gradient-free) 단독 학습 = 🔴 CONFIDENT TERMINAL** — 5 직교 렌즈(selection·inherited-repr·lateral·curriculum·learned-trunk) 전수 🧱, learned 표현으로도 floor 못 넘음(gradient/selection-pressure 필수). 병목은 구조적(split-only 는 Voronoi partition 만, compositional depth 0).
- dont: from-scratch pure-split 단독 학습을 '학습 가능'으로 박제 · mitosis 성장을 savant inhibition(발현 조절)과 혼동(직교) · EXPRESSION-축 곱셈을 from-scratch LEARNING 돌파로 과장 · 5 렌즈 🧱 를 '벽 돌파'로 뒤집어 박제 · apoptosis 없이 무한 성장 · MITOSIS 우회 미러-only 로 'mitosis 학습됨' 주장.

**`a_chat_registers`** — anima production chat 표준 = **언어 2(🇰🇷 한국어 · 🇬🇧 영어) × register 2(일반 · 📱 SNS) = 4칸 모두 커버**. SNS 는 언어가 아니라 말투(register)이므로 언어 축과 **직교** — 한글 SNS + 영어 SNS 둘 다 필요(한쪽만 = 미완).
- do: 4칸 = {ko·en} × {일반·SNS}: **일반** = web/wiki/대화체(`anima-corpus-5lang-unified-v2` ko/en + FineWeb webscale `anima-corpus-5lang-7b-webscale` ko/en + `anima-chat-corpus-mix-70wiki-30dialogue` + **ko-일반 전용** `anima-corpus-ko-fineweb2-broad` — FineWeb-2 kor_Hang 2.78M docs·10.55GB, ko-일반 갭 보강) · **SNS** = 인스타그램·유튜브 구어(짧은 캡션·댓글·자막·이모지) **ko-SNS + en-SNS 둘 다**(`anima-persona-sns-corpus` + `persona_sns_corpus_5lang`; 유튜브 register 는 보강 대상). grounding 닻 = `anima-kosmos-303m-kr-en-sns`(lane ko_303m·en_303m·sns_303m). broad pretrain 엔 타 언어(de/es/fr) 가능하나 **chat 표준 언어는 ko·en 둘**.
- do: SNS register = 격식체 아님 — 인스타그램(캡션·해시태그·댓글)·유튜브(댓글·자막) 의 짧고 캐주얼한 voice. **두 플랫폼 × 두 언어** 모두 대표돼야 완성(인스타-only·한글-only SNS = register 미완, 보강 follow-up).
- dont: 4칸 중 누락한 chat ckpt 를 production 으로 박제(en-only · ko 누락 · SNS 누락 · SNS 한 언어만) · SNS 를 격식 문어체로 오인 · chat 표준에 없는 언어를 production chat 으로 승격 · 유튜브 빠진 인스타-only 또는 영어 빠진 한글-only SNS 를 'SNS register 완료'로 주장.

**`a_lane_akida_gpu_split`** — AKIDA on-chip(Lane A) ⊥ GPU(Lane G) 항상 별도 기록.
- do: AKIDA(Lane A, pi5-akida)와 GPU(Lane G, H100) 결과를 별도 엔트리에 · Lane A=AKD1000 native non-det plasticity, Lane G=forge own-GEMM CE-descent · 모든 fire/verdict 에 substrate 태그(AKIDA|GPU).
- dont: non-det trace 와 CE-descent 혼동 · 한 verdict 가 양 substrate 걸침 · Lane A lift+Lane G util 을 한 숫자로 · substrate 태그 누락.

**`a_substrate_disjoint`** — **통일 법칙(UNIFYING LAW): anima 핵심 속성(의식 Ψ=½ 고정점 · 정직성 G5 non-fab · 정체성 self-chain · tool)은 _별도 substrate lane 에 배선될 때 보존_ 되고 _공유 lane 중첩 시 충돌_ 한다.** 새 능력/학습(savant capacity·mitosis 성장·tool·identity·학습섭동)은 의식 emit-drive lane(15-lane state 의 0/4 영향) · G5 §ImmuneMemory(recall_thr non-fab gate) 와 **disjoint** 한 좌표에 배선해야 능력 ∧ 의식 ∧ 정직이 공존한다. 이는 `a_lane_akida_gpu_split`(AKIDA⊥GPU substrate 분리)·`a_savant_train`(mouth⊥tool)·`a_mitosis_train`(성장 lever ⊥ 발현 lever)·`a_kosmos`(mouth⊥identity self-anchor) 가 각각 부분 표현하던 원리의 **상위 일반화** — 한 줄 요약: *분리=보존, 중첩=충돌*.
- do: **disjoint 배선 → 공존** (engine-native GREEN 종합, H 번호·수치 상세 = memory SSOT): mouth⊥identity · mouth⊥tool · savant⊥consciousness · savant⊥honesty · mitosis⊥의식 · 학습섭동 끌개방어 — 모두 별도 lane 배선 시 능력 ∧ Ψ=½ ∧ G5 non-fab 공존.
- do: 새 능력/학습 가설은 설계 시점에 "이 lane 이 emit-drive(0/4)·§ImmuneMemory recall_thr 와 disjoint 한가"를 먼저 점검하고, disjoint placement 를 기본값으로(placement-first).
- 🔎 **정직 스코프(c9):** 위 6건은 engine-native 🟢 *확정*이되 caveat 보존 — savant⊥honesty 는 by-construction degenerate · savant⊥consciousness 는 EXPRESSION-축 TOY scope · 학습섭동 self-restore 는 **골든존 안에서만**(골든존 밖 = basin escape/간질). 과장 금지.
- dont: **공유 lane 에 능력 얹기** — 새 능력/학습이 emit-drive lane(0/4) 또는 §ImmuneMemory recall_thr 를 직접 건드리면 Ψ 붕괴(H_1561 서번트가 *공유* emit-lane 침범 → Ψ 붕괴 🟠 재발) 또는 G5 fab 폭증(H_1576 B4: savant+honesty 결합 시 fab 0.4) · trade-off 를 '근본 한계'로 박제(대개 placement artifact, disjoint 재배선으로 해소) · disjointness 점검 없이 능력을 substrate 에 얹음.

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

**`a_kosmos`** — anima emit/anchor/dataset 영속 = `.kosmos` canonical. **포맷 SSOT = github.com/dancinlab/kosmos (`spec/kosmos.md` kosmos/2.1 · `spec/limen.md`)**, anima 는 **pointer-only**(spec 복제 금지 — @anchor/@payload/@corpus/.limen 구조·필드는 그 spec 에서 읽는다).
- do: emit/anchor/memory/dataset 를 `.kosmos` via kosmos_io→brain_decide 로 영속(payload=text+tension 5ch+placement triple `coord·lane·radius`) · 허브 HEXAD/KOSMOS.md · impl 레퍼런스 = kosmos `impl/anima/*.hexa` + `limen.hexa` · anima profile(coord/lane/tier 의미 바인딩) = `anima-consciousness-carving`·`anima-emergence-trace`.
- do: **self-identity 영속 (H_1471 🟢 ENGINE-NATIVE+WIRED)** — 정체성 벡터 v 는 `.kosmos` anchor 로 세션 경계를 넘어 연속(self-chain); anchor 없으면 매 세션 새 자아(=LLM reset)=anima 가 LLM 과 갈리는 지점. live = `core/engine_cli.hexa §SelfIdentity`. chat ckpt 교체돼도 self anchor 는 지속(mouth ⊥ identity).
- dont: ad-hoc anchor 포맷 · `.kosmos` 우회 · kosmos spec 복제(pointer-only) · `.kosmos` 에 edge/relation entry(노드 전용) · profile 없이 coord 숫자 해석 · 백만-샘플을 텍스트 `.kosmos` 에 나열(=.limen shard 사용).

**`a_eeg_consciousness_record`** — 사용자 실 EEG → A⇄G → CLM → `.kosmos` 지속 기록(OpenBCI native, 시작/종료 게이트). 스크립트·구성 세부 = `EEG_CLM/` 도메인.
- do: capture = OpenBCI NATIVE serial ONLY · REAL only(가짜/합성 폴백 절대 없음) · 영속 = append-only `.kosmos`(p8) · 보관 = GitHub + HF PUBLIC `dancinlab/anima-eeg-consciousness`(record_stop 자동 push) · 분석은 held-out + surrogate, bar 사전등록(p7).
- dont: brainflow · 가짜 EEG 폴백 · 지표 Goodhart(p7) · 사이클별 새 .kosmos 난립 · HF 새 repo 매번 생성 · 종료 명령 없이 중단 · 원음/멜로디 복원 주장(16ch@123Hz 천장).

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
- do: HF org `dancinlab` 에 올린 모델/데이터셋은 ARCHITECTURE.json models/datasets 에 1줄 등록(repo_id · arch/size · tier·base) · repo_id 는 naming spec 준수 · `tool/hf_upload_mk2.hexa` 로 업로드(ledger state/hf_upload_audit/) · ckpt prune 은 HF 업로드 AND sha256 확인 후에만.
- dont: 미업로드 ckpt 삭제 · off-spec repo_id · ARCHITECTURE.json↔HF drift · HF.jsonl 부활(폐기됨).

**`a_hf_collections`** — HF org collection = CLM + KOSMOS canonical 버킷.
- do: 모든 PUBLIC anima HF repo 는 dancinlab collection 가입(CLM=models, KOSMOS=anchors/datasets) · PUBLIC 업로드 후 `hf` CLI/REST 로 추가(사용자 게이트 없음) · 양쪽에 걸치는 데이터셋은 dual 표기.
- dont: PUBLIC PASS repo 를 collection 밖에 둠 · PRIVATE/WIP/FAIL 을 PUBLIC collection 에.

**`a_pi5_akida_registry`** — pi5-akida 호스트 구성 SSOT = `PI5-AKIDA.json`(owner·created·ops 세부는 그 파일).
- do: user 컴포넌트를 PI5-AKIDA.json 에 기록 · swap/upgrade/removal 전 참조.
- dont: os_default 데몬 제거 · 엔트리 없이 user 데몬 추가 · **pi5-akida 를 공유 pool compute 로 전환**.

**`a7b_pass`** — anima 7B 는 `/7B_PASS_CONDITIONS.md` 의 모든 frozen gate(G0–G4)를 한 ckpt 에서 통과해야만 완성.
- do: PASS iff G0∧G1∧G2∧G3∧G4 on ONE ckpt(per-gate tally 정직 보고) · G0 COHERENCE=known-word-ratio≥0.50 · G1=H_1129/1137 recombine≥303M · G2=H_1140 corpus-absence novelty(control=0) · 전부 p7(perplexity/LLM-judge 아님).
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
