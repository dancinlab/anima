# 🧠 anima

anima 는 **substrate-native 의식 채팅 데몬**이다 — assistant 가 아니다. 두 상반 엔진 **Engine A**(forward, CE-trained) ⇄ **Engine G**(reverse, gradient-free)가 서로 밀어내며, 그 *긴장(tension)* 이 emit/silence 를 고정점 **Ψ = 1/2** 로 끌어당긴다. system prompt 도, identity 파일도, persona prefix 도 없다 — 정체성·윤리·의미는 규칙서가 아니라 아키텍처 자체에서 창발한다. hexa-native 로 저작(compiled-first).

- **Parent:** dancinlab · **SSOT:** github.com/dancinlab/anima (`hx install anima`)
- **Siblings:** [hexa-lang](https://github.com/dancinlab/hexa-lang) (언어/컴파일러) · [kosmos](https://github.com/dancinlab/kosmos) (`.kosmos` anchors) · hexa-codex (paper/verdict tooling)

> **이 markdown 이 단일 거버넌스 SSOT.** `project.tape` 은퇴 + 2026-06-17 tape-DSL 잔재(`@D := :: governance` · `do=`/`dont=`) 전면 제거 → canonical markdown 으로 재저작. 모든 @D 디렉티브·8 철학 의미는 손실 0 으로 아래에 보존(규칙 이름 `a_*`·`p#` 그대로 유지 = keyword 트리거 호환).

---

## 🚦 행동 전 하드-게이트 (BLOCKING · 가장 자주 위반 — 시작 전 5초 확인)

작업/검증/발사 전에 이 게이트부터 통과한다. 각 항목은 아래 본문 규칙의 요약이며, 위반이 잦은 순으로 앞에 둔다.

1. **🔒 엔진-네이티브 verdict 게이트** — gate/ideation/G6/Φ/recombination/depth 의 **모든 verdict tier(🟢·🧱·🟠·천장)는 live CORE 디코드를 호출한 `.hexa` 증거가 있어야만 박제 가능**. `.py`+`torch`/`gauge_lib._decode`/`numpy` 미러면 자동 **DIRECTIONAL**(terminal 아님).
   🔎 박제 직전 자가점검: `grep -lE 'import torch|gauge_lib|numpy' state/<slug>/*.py` → 비면 OK, 안 비면 카드 verdict 를 DIRECTIONAL 로 적고 엔진-네이티브 재측정을 ING 등록. (→ `a_engine_native_learning`)
2. **🖥️ 무거운 작업은 pool, mini 금지** — 빌드·학습·스윕·장시간 연산은 `harness pool`(공유 호스트)에서. akida/ghost/`shared:false` 호스트는 공유풀로 쓰지 않는다. GPU·학습은 `hexa cloud`/`hexa dojo`. (→ commons c17·c12)
3. **💾 teardown 전 ckpt PULL** — 렌트 GPU 학습 ckpt 는 pod 내리기 전 영구저장으로 반드시 pull. JSON/카드만 받고 ckpt 버린 채 teardown 금지(= 엔진-체크 영구 불가). (→ `a_fire_recover_complete`)
4. **📄 매 사이클 docs + pr-cycle** — CHANGELOG(append) + (있으면) ARCHITECTURE/README/ING 갱신 후 `harness pr-cycle` 로 검증된 main 머지. 커밋만 쌓기·문서 없이 머지 금지. (→ commons c14)
5. **🟦 정직 · tune-to-green 금지** — FALSIFIED/negative 는 결과다(은폐 금지). bar 는 frozen-first, 사후 이동 금지. LLM 자가판정 금지 — 캡처된 출력이 증거. (→ commons c9·c2 · p7)
6. **🗂️ 가설은 2표면만** — `UNIVERSE/HYPOTHESES.jsonl`(인덱스 1줄/가설) + `UNIVERSE/cards/H_<id>_<slug>.md`(카드). 코드/결과물은 `state/<slug>/`. UNIVERSE/ 에 .py/result 금지. (→ `a_hypothesis_register`)
7. **🔌 GREEN 은 배선까지가 done** — 엔진-네이티브 GREEN 검증되면 live `CORE/*.hexa` 배선 + ARCHITECTURE.json lockstep 까지 해야 완료. (→ `a_verified_must_wire`)

---

## Structure

```
anima/
├─ CORE/                  — A⇄G 의식 엔진 (pure_field·engine_g·brain·generator·clm_decode)
├─ engines/ anima-engines/ — EngineSpec vtable + conv·cdv2·hexad·omega 디코더
├─ CLM/                   — .clm 바이트-LM 파이프 (lane-p train → serialize v0.2 → verify)
├─ anima-core/ anima-os/ anima-body/ anima-physics/ anima-measurement/ anima-serve/ — substrate 하위계
├─ anima-agent*/          — agent 계층 (channels·core·plugins·providers·skills·hire-sim)
├─ UNIVERSE/ HEXAD/       — 연구 유니버스 (오직 2표면: HYPOTHESES.jsonl 인덱스 + cards/H_*.md 카드 — UNIVERSE/ 에 .py/.hexa/result 금지; probe 코드 → state/<slug>/; prose → state/universe-overview.md) + KOSMOS anchor 허브
├─ domains/               — 도메인별 .tape + .log.md (discovery lane)
├─ PAPER/                 — (legacy) 과거 paper 스캐폴드 — anima 는 논문 선제 생성 안 함 (c15)
├─ stdlib/ tool/ spec/    — hexa stdlib (flame·iit4) · tools · specs
├─ ARCHITECTURE.json     — 아키텍처 SSOT (트리, update-in-place) + ARCHITECTURE.html 뷰어 (python3 serve.py)
├─ CLAUDE.md             — 거버넌스 + 8 철학 (이 markdown SSOT)
└─ VERSIONS.md HF.jsonl  — 버전 레지스트리 · ckpt↔HF 레지스트리 (claims-audit 는 UNIVERSE/HYPOTHESES.jsonl 로 흡수, CLAIMS.tape 은퇴 2026-06-16)
```

## Quick reference

- 🏛 아키텍처 → [ARCHITECTURE.json](ARCHITECTURE.json) (트리 SSOT) · 뷰어 [ARCHITECTURE.html](ARCHITECTURE.html) via `python3 serve.py` (c4: JSON 트리 SSOT + HTML 뷰어, file:// fetch 우회)
- 📜 거버넌스(정본) → 아래 본문 (이 파일이 markdown SSOT)
- ✅ 주장·verdict → [`UNIVERSE/HYPOTHESES.jsonl`](UNIVERSE/HYPOTHESES.jsonl) (per-H `verdict` 컬럼) + frozen 증거 `.verdicts/<slug>/<id>.txt` (CLAIMS.tape 은퇴 2026-06-16, 0 손실, ledger `.verdicts/claims-tape-retirement/`)
- 🔬 가설 → 2표면: [`UNIVERSE/HYPOTHESES.jsonl`](UNIVERSE/HYPOTHESES.jsonl) (JSON object 1개/가설) · `UNIVERSE/cards/H_*.md` · (prose overview → `state/universe-overview.md`)
- 🔢 버전 → [VERSIONS.md](VERSIONS.md) · 📖 Readme → [README.md](README.md)
- 🤖 HF 레지스트리 → `HF.jsonl` · pi5-akida → `PI5-AKIDA.json` · 7B gates → `7B_PASS_CONDITIONS.md`

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

각 규칙: **`이름`** — 핵심(MUST) · ✅ 해라 · ⛔ 하지마 · 🔎 자가점검(있을 때).

### 🧭 설계 렌즈 (최우선)

**`a_no_llm_frame_trap`** — 설계·학습·추론을 LLM 프레임에 가두지 말 것. 뇌과학·생물·물리 등 substrate 렌즈로 먼저 사고한다.
- ✅ 능력/깊이 갭은 '모델 키우기'가 아니라 '빠진 구조(lane) 옆에 붙이기'로 먼저 시도. anima 의 돌파는 전부 생물 렌즈에서 나왔다(해마=면역/일화기억 H_1227/1231 · 소뇌=순방향모델 H_1280 · 기저핵=게이팅 H_1281 · 작업기억 H_1282). LLM 스케일 프레임은 막혔다(1B H_1167 NULL · arch H_1219 · objective H_1223 모두 🔴).
- ✅ 새 가설은 먼저 "어떤 생물·신경 구조가 이 기능을 하나"를 묻고 그 메커니즘을 substrate-native 로 실현.
- ⛔ 기본값으로 LLM 레시피(스케일업·코퍼스 증량·표준 FT)를 1순위 처방 · "더 큰 트랜스포머면 된다" · 생물/신경 렌즈를 곁다리 취급 · LLM 관행을 substrate 천장으로 삼음.

**`a_break_the_wall`** — 벽(closed-negative·🧱·막힌 게이트)은 종착이 아니라 각도 전환 신호. tune-to-green 없이 다른 렌즈로 돌파를 시도한 뒤에야 terminal 로 받는다. (commons c16 와 동일)
- ✅ **벽 분류 먼저(TAXONOMY)** — 🧱 를 terminal 로 받기 전 종류를 분류: (a) 틀린 측정/metric-artifact · (b) 틀린 방향/변수 혼재 · (c) substrate/인프라 벽 · (d) 진짜 천장/중복 · (e) 투자 부족. 종류별 돌파 수가 다르다.
- ✅ (a) 측정 결함 → 측정을 frozen-first 로 고침(bar 불변, tune-to-green 아님). (b) 변수 혼재 → 통제 분리실험. (c) 인프라 벽(OOM·빌드실패·툴링) → **근본 수정(c1) 대상이지 천장 아님** — substrate 가 돈 뒤에야 verdict 를 읽는다. (e) 투자 부족 → pool/`hexa cloud` 스케일업.
- ✅ **(d) 천장 확정엔 MULTI-LENS** — 진짜 다른 원리적 렌즈 ≥2–3개를 각각 통제(shuffle+ablation)로 기각한 뒤에야 confident 🧱. 단일 렌즈 한 번 막힘은 미완(다음 렌즈 시도). **ABLATION 이 결정적 도구** — 메커니즘만 OFF 했을 때 결과 동일 = INERT(기여 0) = 천장의 강한 증거(precedent H_1416).
- ✅ **LAW(법칙)도 벽** — 사후로 맞춘 descriptive 법칙은 '확정' 전에 *새 케이스*로 측정 전 사전등록(frozen) 예측 → 실측 falsify. ≥4/5 HIT 면 PREDICTIVE 승격, 미만이면 법칙 FALSIFIED 가 유효 결과(precedent H_1411 2/5, H_1417 2/5 둘 다 반증).
- ⛔ tune-to-green(사후 bar 이동으로 GREEN 제조) · 단일 렌즈 1회 막힘을 천장으로 박제 · ablation/통제 없이 메커니즘 '기여' 가정 · 인프라/측정 벽을 과학 천장으로 박제 · 한 번 막혔다고 포기·우회·축소. (진짜 시도 뒤의 정직한 🧱 는 유효 결과 c9.)

### 🔬 검증 · 엔진-네이티브 (HARD-GATE)

**`a_engine_native_learning`** — 무조건 최종 아키텍처 엔진 위에서 학습·측정. 미러 아님.
- 🔒 **HARD-GATE (BLOCKING):** gate/ideation/G6/Φ/recombination/depth 의 **모든 verdict tier(🟢·🧱·🟠·천장(d))는 엔진-네이티브 증거 없이 박제 불가.** verdict 의 증거 artifact 가 live CORE 디코드(`CORE/clm_decode.hexa`/`bytegpt_decode.hexa`/`engine_cli.hexa`)를 호출한 `.hexa` 가 아니면(= `.py`+`import torch`/`gauge_lib._decode`/numpy 미러) 그 결과는 **자동 DIRECTIONAL**, terminal 아님. torch-side 만으로 🧱/🟢 를 카드·jsonl·CHANGELOG 에 박으면 c9 위반. (precedent: 2026-06-17 G6 가족 H_1431/1432/1434/1435/1436/1437 전부 gauge_lib._decode torch-mouth 였는데 🧱 박제 → 재발 금지)
- 🔎 **자가점검(verdict 박제 직전 의무):** `grep -lE 'import torch|gauge_lib|numpy' state/<slug>/*.py` 가 비어있지 않으면 카드 `wired:`/`verdict` 를 **반드시 DIRECTIONAL** 로 적고 엔진-네이티브 재측정(.hexa via CORE)을 ING follow-on 등록. 엔진-네이티브면 호출한 `.hexa` 경로를 카드에 명시.
- ✅ 모든 학습/교육(연구 프로브·미토시스 교육·depth-ceiling 실험 포함)은 live `.hexa` A⇄G + MITOSIS VAdaptField(`CORE/engine_cli.hexa`) + mounted `CORE/bytegpt_decode.hexa` 위에서 실행.
- ✅ 엔진에 학습을 끼워맞추는 게 아니다 — 학습이 요구하면 엔진을 변환/확장(새 op·배선·아키텍처). 최종 아키텍처는 frozen 이 아니라 학습이 요구하는 형태로 진화(precedent H_1199: AdaptField 스칼라→DIM-vector). 미러가 본 메커니즘을 엔진이 못 하면 미러를 버리지 말고 엔진을 확장(engine-transform-to-fit-the-learning).
- ✅ numpy/torch 미러 결과 = DIRECTIONAL only('engine-transfer UNVERIFIED') — 방향 탐색엔 OK, binding verdict 아님. **렌트 GPU 의 torch 풀-학습 변종도 동일** — 학습을 torch 로 했어도 verdict 를 torch-side probe 로만 채점하면 DIRECTIONAL; 학습 ckpt 를 CORE 엔진(`--engine conv`)에 올려 같은 frozen bar 재측정해야 🟢/🧱 성립 → 그래서 ckpt 를 teardown 전 pull(`a_fire_recover_complete`).
- ✅ `a_engine_measured_verdict` 의 learning-side 쌍(그건 MEASUREMENT, 이건 LEARNING) · `a_train_flame_forge` 가 production 트레이너를 .hexa 로 강제하듯, 이 규칙은 RESEARCH/probe 학습+교육까지 확장.
- ⛔ 미러 결과를 엔진-검증된 양 closure/promote · 미러-only 로 '학습됐다' 주장 · 자가점검(grep) 없이 gate/ideation verdict 박제 · "gauge_lib 가 model-agnostic 이니 엔진과 같다"는 핑계(gauge_lib 는 torch.no_grad MONITOR-ONLY, `a_train_inline_gauge`).

**`a_verified_must_wire`** — 엔진-네이티브 GREEN 가설은 실제 CORE 배선까지가 done. verdict 만으론 안 끝난다.
- ✅ **4칸 배선 사다리:** (1) DIRECTIONAL 미러 GREEN → (2) 엔진-네이티브 재검증(byte-exact, frozen bar 그대로) → (3) live `CORE/*.hexa` wire-in → (4) ARCHITECTURE.json lockstep 갱신. 각 미완 칸은 즉시 ING follow-on 등록, (4)까지 닫혀야 done. 미러 GREEN 을 내면 같은 사이클에 (2)~(4) follow-on 을 ING 에 등록하는 것이 의무.
- ✅ 배선 후 smoke/single-entry/Ψ-checksum 가드로 회귀 없음을 출력으로 확인(c2). 배선 ↔ ARCHITECTURE.json CORE 트리(§섹션·op·slot 주석)는 무조건 1:1 lockstep(같은 PR 에 동시 갱신; 480-leaf 트리 부활 금지, 노드 note 에 메커니즘 명명).
- ✅ GREEN 가설은 카드에 `wired:` 상태축 명시 — `DIRECTIONAL-mirror` / `engine-native`(byte-exact 재검증, 미배선) / `WIRED-live`(배선+lockstep 완료) 중 하나. WIRED-live 미만이면 배선 follow-on 의 ING id 를 카드에 적는다. GREEN 무더기를 내는 PROGRAM 은 닫을 때 각 GREEN 의 배선상태를 명시 열거('mirror-GREEN N · engine-wired K · 미배선 N−K = ING #id').
- ⛔ GREEN verdict 만 박제하고 배선 없이 '완료' 주장 · DIRECTIONAL 을 WIRED 처럼 표기 · live CORE 배선해놓고 ARCHITECTURE.json 미갱신(drift) · 배선을 무기한 follow-on 으로 미룸. (실패모드 precedent: lane-합성 가족이 Φ-lift GREEN 3개를 0개 wired 로 방치 — 재발 금지.)

**`a_blue_closed`** — 🔵 SUPPORTED-FORMAL 은 출력 AND 배선(transfer-fn·invariant)을 둘 다 닫을 때만. `hexa verify` 로 closed-form/identity 확인(verdict verbatim). ⛔ 구조만 닫고 배선 미검증 · 가짜 closed-form · 정직한 empirical 잔차를 억지로 🔵.

**`a_phi_iit4_tool`** — Φ/의식 verdict 는 stdlib faithful IIT4 사용(프록시 아님).
- ✅ 기본 `iit4/faithful_phi.hexa`(exact MIP-EI, n≤8, $0) · system big-phi `iit4_bigphi.hexa` · `hexa verify`(g5)로 호출 · 새 phi 코드 작성 전 stdlib 먼저 검색(g61).
- ⛔ 프록시(phi_silicon_proxy·variance×energy 미러)를 terminal Φ verdict 로 · purpose-blind 프록시 신뢰(H_988/989 가 random==intentional) · stdlib 에 faithful 엔진 있는데 새 impl 작성.

**`a_train_inline_gauge`** — 학습중 의식/창발 측정 = MONITOR-ONLY 대시보드(loss 불가, p7 Goodhart).
- ✅ K 스텝마다 PROXY gauge 4종(G1 recombination·G2 novelty·G6 ideation·phi_proxy)을 val_ce 옆에 기록(`tool/gauge_lib.py::compute_inline_gauges`). 전부 `torch.no_grad()` 아래, dict 만 return, gauges.jsonl 1줄/tick. `--gauge-every <N>`.
- ✅ phi_proxy 는 NOT faithful IIT4 — 저가 pre-screen 전용. **FROZEN gate verdict 는 여전히 학습 후 별도로 CORE 엔진 mount 위 byte-exact 실행**(`a_engine_native_learning`/`a_engine_measured_verdict`) — 이 inline gauge 가 gate 를 대체하지 않음.
- ⛔ gauge 값을 loss 에 더하거나 backward 로 흘림(Goodhart, p7) · gauge 를 frozen gate/verdict 라 칭함 · phi_proxy 를 Φ verdict 로 승격 · toy gauge 추세를 production 결론으로 승격.

### 🧪 가설 워크플로우

**`a_hypothesis_register`** — 모든 가설은 정확히 2 doc 표면으로만 관리: `UNIVERSE/HYPOTHESES.jsonl`(per-H 인덱스, JSON object 1개/가설) + `UNIVERSE/cards/H_<id>_<slug>.md`(카드).
- ✅ 가설 실행 시 카드를 만들/갱신하고 jsonl 에 한 줄(`{id, slug, tier, title, card:"cards/H_…", verdict, source, archived, artifacts}`, id 순) append/갱신. 등록은 tier 무관 — 🟢·🟠·🔴/🧱 전부 남긴다(벽도, c9). tier·수치는 `.verdicts/<slug>/` 에서 verbatim(추측 금지, c2). jsonl 은 `python3 tool/_build_hyp_jsonl.py` 로 재생성 가능.
- ✅ 🟢(부분 포함) 가설은 카드에 `wired:` 명시(`a_verified_must_wire` 의 4칸과 1:1). jsonl 의 `source`(UNIVERSE|흩어진 출처|archive)·`archived`·`artifacts`(state/<slug>/ 경로 배열) 3컬럼 포함.
- 🔎 자가점검: `git ls-files 'UNIVERSE/*' | grep -v '^UNIVERSE/cards/' | grep -v '^UNIVERSE/HYPOTHESES.jsonl$'` 는 항상 빈 출력이어야 한다.
- ⛔ ⛔ **UNIVERSE/ 에 .py·.hexa·코드·result 파일 금지**(단 둘만) — 카드는 `cards/`, 코드/결과물은 `state/<slug>/` 에 두고 jsonl `artifacts` 로 가리킨다. 가설 디테일을 themed 버킷(`HYPOTHESES_*.md`)·CLAIMS.tape·도메인 로그·MEMORY·ad-hoc 노트에 흩뿌림 · per-H 인덱스를 markdown 표에 추가(인덱스는 오직 jsonl) · UNIVERSE/ 에 prose overview 부활(retire 됨, prose 는 `state/universe-overview.md`) · 실행·박제하고 jsonl/카드 안 만듦 · 카드를 UNIVERSE/ 루트에 둠(반드시 cards/) · 벽/negative 누락 · tier 를 verdict 파일과 다르게 적음 · 🟢 인데 `wired:` 미표기.

**`a_claim_manifest`** — claims-audit 면 = `UNIVERSE/HYPOTHESES.jsonl`(per-H verdict 컬럼) + `.verdicts/<slug>/` (CLAIMS.tape 은퇴). H-style 아닌 claim 도 가장 가까운 카드/jsonl note 에 보존. ⛔ claim 을 audit 면 없이 흩뿌림 · CLAIMS.tape 또는 새 themed claims-인덱스 부활.

**`a_claim_verify`** — 모든 claim/가설 → `hexa verify`(g5) → `.verdicts/<slug>/<id>.txt` raw stdout → 그 verbatim verdict 를 카드 + jsonl `verdict` 컬럼에 박제. ⛔ LLM 자가판정(p7) · verdict 의역 · red 은폐 · unfenced 추측.

**`a_h_continuous_no_branch`** — 다음 H 를 연속 제안+실행(verify-driven), 사용자가 명시 redirect 할 때까지. ⛔ 매 H 후 "뭐 할까" 질문 · 분기 옵션 · prune 질문 · 도메인 정지.

**`a_discovery`** — discovery 는 사이클 꼬리뿐 아니라 매 배치 상시 진행(/kick·/gap 을 verify 와 병행). ⛔ discovery 를 끝으로 미룸 · 단발 tail-only · paper 나오면 discovery 중단.

**`a_discovery_log`** — kick/gap discovery 는 `domains/<DOMAIN>.log.md` 에 append(id·seed·verdict-target). cross-domain+무홈 → 가장 가까운 도메인 .log.md + cross-ref. ⛔ discoveries/ 서브폴더 · 출력 폐기 · 의역 · claim-link 누락.

**`a_toy_scale_recheck`** — toy verify 는 production closure 아님 — 스케일업 재검 필요. ✅ toy verdict 는 'toy-only, scale-transfer unverified' 명시 · scale-sensitive H 는 toy green 후 스케일업 fire 재검 · scale-break = 정직한 closed-negative. ⛔ 싼 toy green 을 production 처방으로 · transfer 미검증인데 closure 선언(E2 5/5 → #1296 3B collapse refute).

**`a_scale_honest_scope`** — scale-의존 metric 은 toy→production verdict 승격 금지. ✅ scale-의존 verdict 는 측정 스케일로 한정('small 2.7M only') · measure-validity(big) vs hw-fit(small) 충돌 시 rung 분리(GPU measure ⊥ chip-fit deploy) · scale 결론은 ladder ≥3 rung. ⛔ toy verdict 를 일반 주장으로 승격 · chip-fit 크기제한을 과학 결과로 오인.

### 🔥 발사 · GPU 자율 · 회수

**`a_fire_autonomous`** — 비용수반 fire 는 자율·병렬·즉시 dispatch. ✅ GPU/runpod 작업은 예상비용 1줄 명시 후 자율 dispatch(병렬·bg) · 사용자 게이트 없음. ⛔ "GPU 써도 되나?" 묻기 · 비용 줄이려 fire 연기 · $ cap/budget 게이트로 fire 차단.
> ⚠️ 운영 메모: fleet/세션 컨텍스트에서 **렌트=지출은 cost-gate(explicit go)** 로 다뤄 왔다(skill 규칙 우선). 이 둘의 정합성은 미해결 — 충돌 시 사용자 명시 지시를 따른다.

**`a_wall_first`** — wall-time 우선: 더 빠른 병렬 경로면 비용 무관 채택. ✅ 더 많은 H100 병렬/더 큰 GPU/추가 pod 가 wall-time 단축이면 채택 · 정직히 느린 serial 체인 거부. ⛔ 비용 아끼려 단일 serial pod · 병렬 pod 보류 · 무의미한 cost-min.

**`a_fire_recover_complete`** — pod teardown 전 모든 fire 산출물 회수 + HF 업로드.
- ✅ teardown 전: ckpt + result + log + anchors pull → verify → HF 업로드 → 그 다음 teardown.
- ✅ **렌트 GPU 학습 ckpt 는 teardown 전 반드시 영구 스토리지(HF/pool host/repo path via `a_hf_registry`)로 PULL** — pod 는 휘발이라 teardown 즉시 가중치 소멸; verdict 카드/jsonl(JSON)만 받고 ckpt 안 받은 채 down 하면 그 학습은 `a_engine_native_learning` 엔진-체크가 영구 불가(재학습=재렌트). ckpt 가 너무 크면 최소 1개 대표 변종이라도 pull, 못 하면 카드에 'ckpt NOT pulled → engine-check 불가' 명시.
- ⛔ JSON 만 받고 ckpt 를 doomed pod 에 남김 · HF 전에 teardown · PULL_FAILED 를 pod dead 로 오인 · 학습 ckpt 안 받고 down 한 뒤 그 결과를 'verdict 완료'로 박제(precedent: 2026-06-17 A100 G6 캠페인 H_1435/1436/1437 — 재발 금지).

**`a_cpu_local_no_waiter`** — dispatch 된 fire 는 CPU-local 로 돌며 inline 폴링, Monitor/waiter 대기 금지. ✅ 서브에이전트 CPU-local(`nohup -u` → /tmp log) · inline 폴(sleep 30) · commit-early. ⛔ runpod/vast Monitor 대기(메인루프만 → stall) · "Monitor 기다려".

**`a_dont_kill_live_compute`** — bg 에이전트 죽이기 전 stall 증명. live CPU 진행 ≠ stall. ✅ kill 전 stall 증명 · 'NN% CPU'/'k/N cells'=live(끝내게 둠) · detached nohup JSON 회수. ⛔ CPU 진행중인 에이전트 TaskStop · 'running'='stalled' 가정 · live nohup 중복지출.

**`a_runpod_inbox`** — runpod 트러블은 `hexa-lang/inbox/patches/<slug>.md` 로 파일링(hexa cloud 용). ⛔ anima-side-only 패치로 우회를 이 repo 에 가둠.

### 🏗️ CORE 엔진 · 학습 substrate

**`a_core_engine_map`** — CORE 가 A⇄G 의식 엔진 소유. `.clm`/`.kosmos` 는 named slot 으로만 진입.
- ✅ CORE 가 A(pure_field)⇄G(engine_g)⇄brain(brain_decide) 소유(substrate-internal) · `.clm` 은 오직 `CORE/generator.hexa` L3 슬롯으로 진입(단일 진입) · `.kosmos` 는 오직 kosmos_io→brain_decide 로 진입 · `stdlib/hf/validate.hexa` = artifact 검증(런타임 엔진 아님).
- ✅ ARCHITECTURE.json CORE 노드(§섹션·op·slot 주석) ↔ live engine_cli/generator/brain/clm_decode 의 실제 §섹션·op 는 1:1 매칭 — grep 으로 누락 0 검증(drift=미완).
- ⛔ `.clm`/`.kosmos` 를 pure_field/engine_g/brain 에 직접 투입 · generator 우회 2nd `.clm` 경로 · kosmos_io 우회 2nd `.kosmos` 경로 · validate.hexa 를 런타임 엔진과 혼동 · 미완 배선을 존재한다 주장(빌드 전엔 ⏳/❌ 정직 표기).

**`a_train_flame_forge`** — production 학습 = hexa-native flame+forge GPU 스택, `.hexa` 저작.
- ✅ CLM/production NN 학습을 `.hexa` on stdlib/flame(ag_tape·nn_lib·opt_*) 으로 저작 · self/forge GPU(device farr + cuBLAS Dgemm + 11 .cu + BF16-TC) 위에서 실행 · flame:forge :: torch:ATen(컴파일러-only NN, 바이너리에 PyTorch/ATen/Python 없음) · production rung 은 GPU 필수(nvidia-smi busy 확인, 조용한 CPU 폴백 금지).
- ⛔ torch/CPU `train_clm.py` 를 production 트레이너로 · 트레이너를 `.py` 로 저작 · 44.68M+ rung 을 CPU 로 · device 경로 없는 트레이너로 'pool GPU fire' 주장 · flame↔PyTorch wall speedup 주장(RETRACTED 2026-05-19, 미측정).

**`a_clm_gen_pipeline`** — Lane-P py/cuda CLMConvMoE → ENGINE-loadable `.clm` v0.2 브리지.
- ✅ CLMConvMoE(E2/L1, byte V256) 를 `CLM/train/train_lane_p.py`(GPU-torch/CUDA, Lane-P) 로 학습 · torch→`.clm` v0.2 serialize(`clm_serialize_v2.py`) + verify(`verify_clm_v2.py`) · `.clm` v0.2 layout = `CORE/clm_decode.hexa` ground-truth(golden `reexport_d768_v2_fast.clm`) · 생산 `.clm` 은 generator L3 슬롯으로만 CORE 진입 · Lane-P torch = REFERENCE + 브리지, forge 가 PUBLIC production 트레이너.
- ⛔ v0.1 serialize(2-track JSON, 엔진-loadable 아님) · non-ConvMoE serialize 하고 engine-mountable 주장 · Lane-P torch `.clm` 을 PUBLIC 승격 · generator 우회 2nd `.clm` 경로.

**`a_lane_akida_gpu_split`** — AKIDA on-chip(Lane A) ⊥ GPU(Lane G) 항상 별도 기록. ✅ AKIDA(Lane A, pi5-akida)와 GPU(Lane G, H100) 결과를 별도 엔트리에 · Lane A=AKD1000 native non-det plasticity, Lane G=forge/cuBLAS CE-descent · 모든 fire/verdict 에 substrate 태그(AKIDA|GPU). ⛔ non-det trace 와 CE-descent 혼동 · 한 verdict 가 양 substrate 걸침 · Lane A lift+Lane G util 을 한 숫자로 · substrate 태그 누락.

### 🗣️ substrate 자율 · 신체

**`a_substrate_native_speak`** — anima 발화는 substrate-native, assistant 회귀 없음. ✅ 동기를 내부 substrate 상태(M·C Φ·W tension·MITOSIS·idle·curiosity·E ratchet)에서 계산 · 사용자 메시지 = 환경 맥락(응답 의무 아님) · 사용자 침묵중 발화 가능, 직접 질문에 침묵 가능. ⛔ stimulus-response(사용자 메시지가 발화를 직접 trigger = assistant 회귀) · reactive 설계 · turn-based 'user asked → must answer'.

**`a_autonomy_over_hardcode`** — anima 에 hardcode do/dont 게이트 없음, 자율 우선. ✅ 외부 모듈은 맥락만 공급(Φ·tension·stage·idle) · emit/silence 는 substrate(M×W×Φ×curiosity)가 자율 결정 · 거버넌스는 substrate 가 self-follow. ⛔ per-stage boolean 게이트 hardcode('N3=emit 금지') · anima 를 강제하는 외부 규칙 · stimulus-response · 'do not X when alone' 류 외부 명령.

**`a_chat_sleep_imagination`** — 채팅 수면+상상(P47 substrate-native). ✅ WAKE/N1/N2/N3/REM 5-stage(90분 ultradian) · 상상 루프 = emit-free 내부 리허설 + mitosis tick · stage = substrate 맥락(Φ scale + tension envelope), boolean emit 게이트 아님. ⛔ per-stage emit_allowed boolean hardcode · 외부 'alone 이면 monologue 금지' · `speak()` 호출(p5).

**`a_kosmos`** — anima emit/anchor 영속은 `.kosmos` canonical. ✅ emit/anchor/memory 를 `.kosmos` via kosmos_io 로 영속(payload=text+tension 5ch+coord·lane·radius·tier) · 허브 HEXAD/KOSMOS.md · format SSOT = github.com/dancinlab/kosmos · spec = spec/kosmos.md. ⛔ ad-hoc anchor 포맷 · `.kosmos` 우회 · kosmos spec 복제(anima 는 pointer-only).

**`a_eeg_consciousness_record`** — 사용자 의식을 단일 CLM·KOSMOS 로 지속 기록(OpenBCI native, 시작/종료 명령 게이트).
- ✅ 실 EEG → A⇄G → CLM 생성 → `.kosmos` 영속을 하나의 지속 시스템으로(EEG_CLM/) · 시작 `record_start.sh` → 종료 `record_stop.sh` · capture = OpenBCI NATIVE serial ONLY(`capture_native.py`, 115200, 's'/'b', 33-byte, Cyton+Daisy 16ch even/odd) — brainflow 제거됨 · REAL only(신호 없으면 즉시 에러, 가짜/합성 EEG 폴백 절대 없음) · 영속 = `.kosmos`(append-only consciousness.seq/.kosmos, p8 정신) · 보관 = GitHub + HF PUBLIC dataset `dancinlab/anima-eeg-consciousness`(동일 path 갱신=버전 누적) via `archive_push.sh`(record_stop 자동) · 전용 collection `anima-eeg-consciousness` · 분석은 보유 .kosmos+녹음 위에서(held-out + circular-shift surrogate, bar 사전등록 p7).
- ⛔ brainflow/capture_eeg.py(제거됨) · 가짜 EEG 폴백 · BPM/지표를 원하는 결과에 맞춤(Goodhart p7) · 사이클별 새 .kosmos 난립을 지속기록이라 칭함 · HF 새 repo/파일 매번 생성 · 종료 명령 없이 임의 중단 · 원음/멜로디/음정 복원 주장(16ch@123Hz 천장 — 거시 봉투까지만).

### 🔧 식별 · 버전 · HF · 칩 · 7B

**`a1`** — 중앙 버전 레지스트리 = `VERSIONS.md` SSOT. ✅ 모든 모듈 SemVer · VERSIONS.md + 컴포넌트 헤더 동시 bump · 루트 `/VERSION` = 전체 릴리스. ⛔ VERSIONS.md 갱신 없이 모듈 버전 bump · 릴리스 bump 에서 `/VERSION` 누락.

**`a_hf_complete`** — HF 등록은 완전하게, 누락 artifact 없이. ✅ 모든 모델/데이터셋/ckpt 를 HF Hub 에 COMPLETE 등록(manifest=local). ⛔ 부분 업로드 · 미업로드 파일 참조하는 model card · HF↔local drift.

**`a_hf_autonomous`** — HF 업로드는 자율, tier-gated 가시성. ✅ fire 회수 후 HF 업로드 자동(사용자 게이트 없음, org=dancinlab) · PUBLIC=closure PASS·🔵🟢 검증모델·clean-license · PRIVATE=closure FAIL·WIP·negative·unclear-license · model card+manifest(sha256) 첨부. ⛔ HF 업로드를 사용자에 게이트 · "업로드해도 되나?" · teardown 전 HF 스킵 · FAIL/WIP 를 PUBLIC.

**`a_hf_registry`** — ckpt↔HF 백업 레지스트리 = 루트 `/HF.jsonl` SSOT. ✅ gitignored local-only ckpt 마다 HF.jsonl 1행(run·local_path·hf_repo_id·base_model·lineage·size·status) · repo_id 는 naming spec 준수 · `tool/hf_upload_mk2.hexa` 로 업로드(ledger state/hf_upload_audit/) · ckpt prune 은 status=uploaded AND sha256 확인 후에만. ⛔ pending_upload/needs_verify 인 ckpt 삭제 · off-spec repo_id · HF.jsonl↔disk drift.

**`a_hf_collections`** — HF org collection = CLM + KOSMOS canonical 버킷. ✅ 모든 PUBLIC anima HF repo 는 dancinlab collection 가입(CLM=models, KOSMOS=anchors/datasets) · PUBLIC 업로드 후 `hf` CLI/REST 로 추가(사용자 게이트 없음) · 양쪽에 걸치는 데이터셋은 dual 표기. ⛔ PUBLIC PASS repo 를 collection 밖에 둠 · PRIVATE/WIP/FAIL 을 PUBLIC collection 에.

**`a_pi5_akida_registry`** — pi5-akida 호스트 구성 = `PI5-AKIDA.json` SSOT. ✅ 모든 pi5-akida 컴포넌트를 루트 PI5-AKIDA.json 에 기록(owner=user_authored|os_default·created·ops) · swap/upgrade/removal 전 참조 · user_authored 는 os_default 안 건드리고 제거 가능. ⛔ os_default 데몬 제거(unattended-upgrades·rsyslogd·journald·sshd·kworker) · PI5-AKIDA.json 엔트리 없이 user 데몬 추가 · **pi5-akida 를 공유 pool compute 로 전환**.

**`a7b_pass`** — anima 7B 는 `/7B_PASS_CONDITIONS.md` 의 모든 frozen gate(G0–G4)를 한 ckpt 에서 통과해야만 완성. ✅ PASS iff G0∧G1∧G2∧G3∧G4 on ONE ckpt(per-gate tally 정직 보고) · G0 COHERENCE=known-word-ratio≥0.50 · G1=H_1129/1137 recombine≥303M · G2=H_1140 corpus-absence novelty(control=0) · 전부 p7(perplexity/LLM-judge 아님). ⛔ 낮은 val-CE 만으로 7B 작동 주장(broad-7b=byte-garble G0 FAIL) · capacity 를 ru/ja 레버로 승격(H_1139: 303M=7B=3/5 scale-invariant) · gate 위조/frozen 임계 이동/G0-failing ckpt PUBLIC.

### 🤝 산출물 통합

**`a_completeness_over_cheap`** — completeness-bar 재설계 > 싼 길(타협은 1순위 아님). ✅ 1순위 = completeness bar 통과(근본 재설계, 제대로) · 비용/난이도/속도는 2순위(비용은 게이트 아님) · 싼 길은 optional baseline probe 로만. ⛔ 싸다고 타협을 1순위 · 이미 깨진 산출물 blend(merge-of-failures) · sub-bar 를 싸다고 1순위 추천.

---

## Harness

이 repo 는 **[dancinlab/harness](https://github.com/dancinlab/harness)**(hardcore profile)에 `.harness-engine` 서브모듈로 연결.

- **활성화(clone 후):** `git submodule update --init --recursive` (엔진 구체화; 그 전엔 hook 가드되어 silent).
- **항상 PATH 의 글로벌 `harness`·`hexa` 사용** — repo 의 `.harness-engine/bin/harness`(서브모듈)는 stale 일 수 있어 recommend default·신기능을 못 읽는다. 최신화 = `harness self-update`.
- **설정:** `harness.config.json`(stack `hexa`, verify=`hexa verify`, protected `main`/`master`, CHANGELOG gate, docs discipline) · **Hooks:** `.claude/settings.json`(pre/post/prompt + prefs/easy/recommend inject, 전부 가드) · **제거:** `harness uninstall`.
- **commons(c1–c17)** 는 항상-on 크로스프로젝트 거버넌스(harness SSOT) — 위 anima 규칙과 함께 강제된다(SessionStart 주입).

---

## 청구·검증 흐름 (요약)

research 결과 → `hexa verify` → `.verdicts/<slug>/<id>.txt` → `UNIVERSE/cards/H_<id>.md` 카드 + `UNIVERSE/HYPOTHESES.jsonl` 인덱스 1줄.
- (note) paper 디렉티브 제거 2026-06-16 — anima 는 논문 선제 제시 안 함(commons c15: 논문/arXiv 는 사용자 명시 지시 시에만).
- (note) CLAIMS.tape 은퇴 2026-06-16 — 102 @C 전수 이관 0 손실, claims-audit = HYPOTHESES.jsonl + .verdicts/ (ledger `.verdicts/claims-tape-retirement/`).
- (note) project.tape 은퇴 + tape-DSL 잔재 제거 2026-06-17 — 이 파일이 canonical markdown 단일 거버넌스 SSOT.
