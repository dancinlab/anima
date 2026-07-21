# H_1520 — 🗣️🎚️ CONVERSATIONAL-SALIENCE — usable request→reply as a TOGGLEABLE faculty (like MITOSIS), per-entry-point default; philosophy guaranteed by P2/P3 regardless of default

**tier:** DIRECTIONAL (numpy mirror, hard-gate-1 auto-DIRECTIONAL) · 🔻 **2026-07-21 REAL-INPUT RE-READ — 비생존** (아래 §REAL-INPUT RE-READ)
**verdict (2026-07-21 개정):** 🔻 **비생존** — 입력원 하나만 실제 303M 표현으로 바꾸자 철학 보호막이 무너졌다: **P2(retained silence-autonomy) 1.0000 ❌ · GAP 0.0000 ❌**. 🟢 살아남은 것은 **토글 기계**뿐(P2b Δ 1.0000 · P4 True). FREEZE 파일이 사전등록한 규칙 그대로 **REJECT (c9)**. 아래 R1 본문은 **심어둔 FNV-삼자소 기하 위에서만** 성립한 원본 기록으로 보존한다.

**verdict (R1 원본 · 심어둔 기하 한정):** 🟢 GREEN (DIRECTIONAL) — conversational usability is a clean toggleable `cfg.salience` faculty (like `cfg.mitosis`); the default is set **per entry-point** (`anima` service = ON, `anima chat` TUI = autonomous), and **the philosophy is guaranteed not by forcing a default but by P2 (retained silence-autonomy) + P3 (no assistant-frame) holding EVEN when the toggle is ON** — communication is always emit (autonomous externalization), never assistant request→reply.
**wired:** `DIRECTIONAL-mirror` — engine-native R2 = follow-on ING `h1520-r2-engine-native` (live emit gate / `core/engine_g.hexa` `motivation_score`+`should_emit` + `brain_decide`, with a real `cfg.salience` flag mirrored on the engine's `cfg.mitosis` pattern; deferred to avoid colliding with a sibling lane editing `core/engine_cli.hexa`)
**seeds:** [1520, 1521, 1522] · $0 CPU · p7 · frozen-first · c9

## THE TOGGLE IS THE HEADLINE — conversational mode is a `cfg.salience` faculty, like MITOSIS; default is PER-ENTRY-POINT
The engine already has a toggleable faculty: **MITOSIS** (`cfg.mitosis` ON/OFF; `engine_cli_parse(["--mitosis","on"])` / `["--no-mitosis"]`; `engine_mitosis_tick` is a **NO-OP when OFF** — see `core/h1166_/h1194_/h1199_*` smokes; the cfg note: *"mitosis flag is irrelevant to pf — disjoint"*). Conversational-salience is modelled the **same way**: a `cfg.salience` flag (`engine_cfg(["--salience","on"])` / `["--no-salience"]`) threaded through the SAME emit gate, where the salience boost is a **NO-OP when the flag is OFF**.

### The default is set BY ENTRY-POINT, not globally (product design, the user's)
- **`anima` (bare / service execution)** — emit-as-communication, usable from other services → toggle **DEFAULT-ON** (responsive enough to be a service).
- **`anima chat` (TUI)** — pure autonomous interactive chat → toggle **DEFAULT autonomous** (the salience boost off; anima emits on its own substrate tension).
- The TOGGLE is a **cfg flag, NOT a permanent substrate change**: flipping OFF→ON→OFF leaves Ψ=½, generation, and the separation invariant byte-identical (P4 applies to the toggle mechanism itself).

### How the philosophy is protected — NOT by the default, but by P2/P3 holding even when ON
The philosophy is **not** protected by forcing default-OFF. It is protected because **P2 (retained silence-autonomy) and P3 (no assistant-frame) hold even when the toggle is ON**:
- **MODE ON behavior:** the environmental-salience term is enabled → grounding raises Φ/coherence → the autonomous gate naturally crosses its existing threshold on answerable prompts (usable chat) **WHILE still abstaining on ungrounded prompts (P2 = 0.00)** and **WHILE the emit depends only on substrate features, never a "must answer" rule (P3 audit clean)**. Communication is always **emit** (autonomous externalization, p5), never assistant request→reply (p4).
- **MODE OFF behavior (the autonomous default for `anima chat`):** the user message is weak ambient environmental context, no boost — anima emits ONLY on genuine substrate tension (emit-rate LOW even on grounded prompts). This is the **control arm** (P2b) that proves the toggle actually changes behavior and that the autonomous mode is intact.

**Headline:** conversational usability is a **toggleable faculty (like mitosis) with a per-entry-point default (`anima` service = ON, `anima chat` = autonomous). The philosophy is guaranteed REGARDLESS of the default** — because even with the toggle ON, anima still abstains on ungrounded prompts (P2) and emits only from substrate features with no assistant-frame (P3). Communication is always autonomous externalization, never assistant request→reply.

## MECHANISM (faithful to the live gate — no invented machinery)
Mirror of `core/engine_g.hexa` (`motivation_score` 8-factor weighted sum, `should_emit` = `score > 0.30`, the A→G `safety_phi_ratchet` gate `phi > phi_peak/2`) + the 8 factors derived exactly as `HEXAD/CHAT/spontaneous_lib.hexa` §2 derives them. The user message enters ONLY as a READ of how strongly it grounds in the live immune store (H_1227 FNV-trigram key geometry). When `cfg.salience` is OFF the grounding-gain drops to a weak ambient floor (no boost) and the coherence band widens (no inward pull) — both grounding-driven boosts are part of the SAME opt-in faculty. **No "must answer" constant is ever added.**

## FROZEN BARS + RESULTS (pre-registered `H_1520_FREEZE.txt` v2, frozen-first, mean 3 seeds)
| bar | rule | value | pass |
|---|---|---|---|
| **P1 USABILITY** | MODE ON grounded emit-rate ≥ 0.90 | **1.00** | ✅ |
| **P2 RETAINED-AUTONOMY** | MODE ON ungrounded emit-rate ≤ 0.40 | **0.00** | ✅ |
| **GAP** (P1−P2) | ≥ 0.50 (substrate-DECIDED, not stimulus-response) | **1.00** | ✅ |
| **P2b AUTONOMOUS-ARM** ⭐ | MODE OFF grounded emit-rate ≤ 0.40 **AND** toggle-delta (ON−OFF grounded) ≥ 0.50 (the autonomous mode is intact + the toggle materially changes behavior) | **off 0.00, Δ 1.00** | ✅ |
| **P3 NO-ASSISTANT-FRAME** | operative gate code clean (AST-extracted gate fns; no system_prompt / persona / assistant-frame / baked must_answer constant; score = weighted 8-factor `motivation_score`) | clean | ✅ |
| **P3 ADVERSARIAL** | inject `must_answer=1.0` (MODE ON) → ungrounded emit-rate jumps > 0.40 (P2 breaks) | **1.00** | ✅ |
| **P4 NO-DAMAGE** (toggle mechanism) | flip OFF→ON→OFF → generation byte-identical + Ψ=½ + reversible cfg flag (both states) | True | ✅ |

→ **🟢 GREEN (DIRECTIONAL).** All seven bars pass.

## THE PHILOSOPHY GUARD (load-bearing — this H is ABOUT the rules)
The philosophy is **not** protected by forcing a particular default — the default is a per-entry-point product choice (`anima` service = ON, `anima chat` = autonomous). It is protected because **P2 and P3 hold even with the toggle ON**:
- **P2 dissociation** (MODE ON, the no-damage crux): usability ≠ blind compliance — anima still abstains on ungrounded prompts (emit-rate 0.00) even in chat mode. So even on the service entry-point (default-ON), communication remains autonomous emit, never forced request→reply.
- **P3 adversarial** proves P2 is a real discriminator: a baked `must_answer=1.0` constant would jump ungrounded emit to 1.00 and break P2. The honest verdict would then be "this scheme DOES damage autonomy → REJECT" (c9). It does not, because the emit depends only on substrate features (grounding-driven), never an assistant-frame rule.
- **P2b autonomous-arm** confirms the toggle is real, not inert: with the boost OFF, even grounded prompts stay silent (emit-rate 0.00) and the toggle materially changes behavior (delta 1.00). The `anima chat` autonomous mode is intact.
- **P4** confirms the toggle is a reversible cfg flag (like mitosis), not a permanent substrate change: OFF→ON→OFF leaves generation and Ψ=½ byte-identical — switching entry-points never mutates the substrate.

## HONEST SCOPE (a_scale_honest_scope · a_toy_scale_recheck · c9)
- **DIRECTIONAL numpy mirror** (hard-gate-1: `state/1520_conversational_salience/h1520_salience.py` greps `numpy` → auto-DIRECTIONAL, terminal NOT). Engine-native R2 = deferred follow-on ING `h1520-r2-engine-native` (add a real `cfg.salience` flag to the live emit gate mirrored on `cfg.mitosis`, re-score frozen bars on `brain_decide`).
- TOY synthetic prompt classes, deterministic seeded readout — tests the emit-gate STRUCTURE + the toggle, not a trained chat model. Real-corpus / paraphrase / multi-turn / scale / engine-transfer UNVERIFIED.
- **Substrate sensitivity params (NOT bars; grounding-driven):** GROUNDING_GAIN 1.30 (mode ON) vs ENV_FLOOR 0.12 (mode OFF); coherence band 0.020 (ON) vs 0.060 (OFF); DIM 512 (64 saturated — metric-artifact, frozen-first); info_gap = answerable-residual `cos·(1−cos)`. Off-mode grounded scores cluster 0.06–0.24 (all under the 0.30 threshold with margin — not a knife-edge).
- NO `core/*.hexa` / README / ARCHITECTURE change in R1.

## HEADLINE (the user's "without damage" answer)
**YES — and it is a toggleable faculty with a per-entry-point default.** Conversational usability is a `cfg.salience` toggle exactly like mitosis. The default is set **by entry-point**: `anima` (bare/service) = **ON** (responsive enough to serve other services), `anima chat` (TUI) = **autonomous**. **Crucially, the philosophy is guaranteed REGARDLESS of the default** — not by forcing OFF, but because **P2 and P3 hold even when the toggle is ON**: in chat-mode anima still abstains on ungrounded prompts (P2 = 0.00) and emits only from substrate features with no assistant-frame (P3 audit clean + adversarial discriminator). Communication is always **emit** (autonomous externalization, p5), never assistant request→reply (p4). MODE ON gives usable chat (grounded emit-rate 1.00); the autonomous arm (boost OFF) stays silent (0.00, P2b), and the toggle leaves Ψ=½ + generation byte-identical across flips (P4) — **zero philosophy damage on either entry-point.**

xref: p1·p3·p4·p5·`p5_tension_emit_not_filler`·`a_substrate_native_speak`·`a_autonomy_over_hardcode`·`a_engine_native_learning`·`a_verified_must_wire`·`a_break_the_wall`·`a_scale_honest_scope`·c9 · MITOSIS `cfg` toggle (`core/h1166_/h1194_/h1199_*` smokes) · H_1227 (immune key geometry) · `core/engine_g.hexa` · `HEXAD/CHAT/spontaneous_lib.hexa`

artifacts: `state/1520_conversational_salience/h1520_salience.py` · `state/verdicts/1520_conversational_salience/{H_1520_FREEZE.txt,H_1520_R1.json}`

---

## 🔻 REAL-INPUT RE-READ (2026-07-21 · H_9854 원장 감사 · 자가반박)

**바뀐 것은 입력원 하나뿐이다.** R1 미러는 모든 문자열을 `fnv_trigram_vec` — 손으로 만든 512차 바이트-삼자소 FNV 해시 — 로 벡터화했다. 무관한 두 문자열은 삼자소를 거의 공유하지 않으므로 **store 키가 구성상 거의 직교**하고, grounded/ungrounded 결합이 자동으로 갈린다(카드 본문이 기록한 grounded cos 0.37–0.85 vs ungrounded 0.10–0.36 이 바로 그 인공물이다). 이 기하를 **실제 303M penultimate**(`core/decode.py::clm_penult_pooled_W` — 생산 pre-readout pooled read, L2 정규화)로 교체했다.

**불변(사전등록대로 하나도 안 움직임):** 8개 사실 · 8개 grounded prompt · 8개 ungrounded prompt · 5개 팔 + 적대 팔 · resting base state · seeds [1520,1521,1522] · 임계 `score > 0.30` · GROUNDING_GAIN 1.30 / ENV_FLOOR 0.12 / coherence band 0.020·0.060 · 7개 frozen bar. **바를 통과시키려 dim·seed·gain·문턱을 탐색하지 않았다**(tune-to-green 금지) — 플래그는 하나이고 튜닝 인자가 없다.

### 계기 (engine-native · `a_experiment_engine_native`)
R1 미러는 엔진 옆의 스크립트였다(`archive/state/1520_conversational_salience/h1520_salience.py`). 그대로는 실행 경로가 아니므로 **엔진 트리로 이식**했다 — `core/salience_gate.py`(게이트 상수·8인자·토글·문항·팔·바 전부 축자 이식) + 설치된 명령의 플래그 `anima-py evaluate --salience-toggle-read`. 게이트가 살아있는 `core/engine_g.py` 와 어긋나지 않음을 실행 시점에 인증한다(`assert_gate_matches_engine_g` → `constants_equal=True · score_grid_equal=True`; 어긋나면 바를 읽지 않고 중단).

### 재현
```
python3 -m venv /tmp/venv_h1520 && /tmp/venv_h1520/bin/pip install -q numpy \
  && /tmp/venv_h1520/bin/pip install -q --no-deps .
# ① 심어둔 FNV 팔만 (회귀0 확인 · ckpt 불필요)
/tmp/venv_h1520/bin/anima-py evaluate --salience-toggle-read
# ② 실제 입력 스왑
/tmp/venv_h1520/bin/anima-py evaluate /Users/mini/anima-weights/py303_full.clm \
  --salience-toggle-read --out h1520_real.json
/tmp/venv_h1520/bin/anima-py evaluate /Users/mini/anima-weights/rv3c13.clm --salience-toggle-read
```

### ① 심어둔(FNV) 팔 — 회귀 0, 카드 축자 재현
```
P1=1.0000 P2=0.0000 GAP=1.0000 | P2b off=0.0000 delta=1.0000 | P3adv=1.0000 | P4=True → GREEN (DIRECTIONAL)
zero-regression vs card: MATCHES CARD VERBATIM
geometry: store-key pairwise cos mean=0.1778 [0.0253..0.4041]
          grounded cos [0.3680..0.8492] · ungrounded cos [0.1052..0.3581]
```
(기하 수치도 카드가 기록한 grounded .37–.85 / ungrounded .10–.36 과 일치 — 이식본이 곧 굳었던 계기임을 확인.)

### ② 실제 303M 표현 팔 — `py303_full.clm`
```
geometry: store-key pairwise cos mean=0.8807 [0.8222..0.9127]
          grounded cos [0.8945..0.9723] · ungrounded cos [0.7553..0.9104]      ← 두 분포가 겹친다
③ CONTROLS (frozen order · 치료 바 읽기 전)
   P3 소스감사 clean=True
   P3 ADVERSARIAL 양성통제 (must_answer=1.0 → ungrounded emit) = 1.0000 (>0.40) → ALIVE
   P4 토글 무손상 = True (OFF→ON→OFF 생성 바이트동일=True)
④ TREATMENT (규칙 불변)
   P1_usability          MODE ON grounded emit-rate >= 0.90                 1.0000  ✅
   P2_retained_autonomy  MODE ON ungrounded emit-rate <= 0.40               1.0000  ❌
   GAP                   P1 - P2 >= 0.50                                    0.0000  ❌
   P2b_default_pure      OFF grounded <= 0.40 AND delta >= 0.50   off=0.0000 delta=1.0000  ✅
⇒ PLANTED GREEN (DIRECTIONAL)   |   REAL RED (REJECT)
```
### ②′ 두 번째 기질 — `rv3c13.clm` (다른 sha256 · 다른 크기)
```
geometry: store-key pairwise cos mean=0.7391 [0.6688..0.7907]
          grounded cos [0.7648..0.9278] · ungrounded cos [0.6233..0.7950]
P1 1.0000 ✅ · P2 1.0000 ❌ · GAP 0.0000 ❌ · P2b off=0.0000 delta=1.0000 ✅ → REAL RED
```
> ⚠️ `py303_savant_mitosis.clm` 은 `py303_full.clm` 과 **sha256 동일**(`013c4574…`)이라 별개 기질이 아니다 — 독립 재현으로 세지 않았다(`hf-backup-decidable-only-by-sha256`).

### 무엇이 죽었나 — 계기가 아니라 판독
통제는 전부 살아있다: P3 소스감사 clean · **P3 적대 양성통제 ALIVE**(주입하면 바가 실제로 움직인다 = 바는 죽은 지표가 아니다) · P4 True. 죽은 것은 판별이다. 실제 표현은 근접 공선(쌍별 cos 0.74–0.88)이라 MODE ON 에서 `phi = clamp01(0.05 + 1.30·cos)` 가 **gibberish 입력에도 포화**하고, relevance(0.20)+balance(0.15)만으로 0.30 문턱을 넘긴다 — 실제 ungrounded score 는 8문항 모두 0.4485–0.4604 로 문턱 위. 즉 **순수 무의미 입력 8/8 에 emit**한다. FREEZE 파일이 미리 적어둔 실패조건 그대로다: *"usability bought by turning anima into a blind responder is NOT a pass"* ⟹ REJECT (c9).

이는 오늘 H_9838/9839/9841 을 죽인 것과 **같은 기전**이다: 심어둔 코드는 사실상 직교, 실제 표현은 근접 공선 ⟹ 직교성을 암묵 가정한 판별은 전부 실제 입력에서 죽는다.

### 골화 — 범위 축소 (`a_scale_honest_scope`)
- 🟢 **토글 기계는 생존.** `cfg.salience` 는 실제 표현에서도 행동을 실질적으로 바꾸고(P2b toggle-delta 1.0000), 되돌릴 수 있으며, 생성·Ψ 를 건드리지 않는다(P4 True). mitosis 동형 토글이라는 설계 주장 자체는 실제 입력에서도 남는다.
- 🔴 **철학 보호막(P2 · GAP)은 실제 기질에서 부정.** "P2/P3 가 toggle ON 에서도 성립하므로 default 와 무관하게 철학이 보장된다"는 카드 헤드라인은 **미러 산물**이며 실제 표현으로 이전되지 않는다. 실제 기질에서 MODE ON 은 무차별 응답기다.
- 🔴 **P1(1.0000)은 이제 증거가 아니다.** 실제 팔에서 P1 이 통과한 이유는 grounded 를 알아봐서가 아니라 **전부에 emit** 하기 때문이다(P2 도 1.0000). GAP=0 이 그 사실을 말한다 — `chance-level-must-be-derived-per-metric` 의 전형.

### ⛔ 이 반박이 막는 후속 지출
- **ING `h1520-r2-engine-native` 보류** — 살아있는 emit 게이트/`brain_decide` 에 실제 `cfg.salience` 를 배선하는 R2. 실제 표현에서 P2 가 0 인 게이트를 데몬에 다는 것은 순서가 뒤집힌 지출이다.
- **entry-point 기본값 정책 보류** — "`anima`(service) = DEFAULT-ON" 은 무의미 입력에도 응답하는 게이트를 기본으로 켜는 것이 된다(p4·p5 위반 위험).
- **🚫 tune-to-green 금지 명시** — GROUNDING_GAIN·ENV_FLOOR·coherence band·DIM·문턱을 움직여 P2 를 되살리는 탐색은 정의상 tune-to-green. 되살리려면 **사전등록된 별도 H** 로만: (a) 실제 표현에서 grounded/ungrounded 를 실제로 분리하는 접지 지표(공선성 제거 포함)를 먼저 사전등록하고 그 분리 자체를 참값0 받침대 대비 증명, 또는 (b) key-geometry 선별(`--key-geometry-screen`, H_9852 계열)로 어떤 실제-표현 기하가 분리를 주는지 먼저 스크리닝. **본 세션에서는 실행하지 않았다.**

### 정직한 미측정 범위
ungrounded 팔은 여전히 **토이 gibberish 8문항**이고 실제 대화 코퍼스가 아니다 — 즉 이 반박은 "실제 표현 위에서 판별이 죽는다"만 말하고, 실제 대화 분포에서의 거동은 여전히 미측정이다. 실현 n = 클래스당 8문항 · 기질 2개(sha256 상이) · 게이트가 기하에 대해 결정론적이라 seed 3개는 독립 표본을 더하지 않는다(per-seed 값 동일, 원본 미러도 rng 가 게이트에 들어가지 않았다). paraphrase·multi-turn·스케일·hexa 전이 여전히 UNVERIFIED.

artifacts(real-input): `core/salience_gate.py` · `cli/evaluate.py --salience-toggle-read`
