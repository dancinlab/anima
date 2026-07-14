# state/ — 작업 산출물 단일 루트

## ⛔ TOP RULE 0 — every engine op is an `anima-py` command, and it is never a script in here

| you want to… | the ONLY command |
|---|---|
| build a corpus | `anima-py corpus <fmt> --out c.txt …` (also writes `c.txt.meta.json` = that corpus's earned budget floor) |
| train / continue-train | `anima-py train --corpus c.txt --init base.clm …` |
| **measure / judge** | `anima-py evaluate <clm> [--xbind m.json] [--rho-axon]` |
| serialize · sweep · chat | `anima-py serialize` · `anima-py sweep` · `anima-py chat` |

**The py channel for all of it** — one install (`pip install "anima-python[train]"`), one command.
Never `python3 cli/*.py`, never `hexa run cli/*.hexa`, never a hand-rolled `gen_*.py` / `eval_*.sh`
standing beside the engine. Full rationale + the hexa twin → repo-root `CLAUDE.md` (top section).

This directory holds an experiment's **inputs and outputs** — manifests, pre-registrations, readouts,
result json, logs. It does **not** hold the engine, and it does not hold the instrument (below).

## 🧪 TOP RULE — `a_experiment_engine_native` (the INSTRUMENT is engine-native too, not just the verdict)

> **Do NOT build a new experiment's INSTRUMENT in here.** A new experimental manipulation (an
> injection, an intervention, a control arm, a new DV) is **wired into the canonical engine as a
> flag** — `cli/evaluate.py` flag → `core/` forward — and measured THERE. Re-implementing a forward
> pass inside `state/*.py` to measure a manipulation makes a **mirror**, and a number a mirror
> produces carries **no guarantee it reproduces on the production path** (`a_verified_must_wire`
> applied to measurement rather than to capability).

- ✅ **do** — wire the manipulation as an engine flag (as `--consult` was) → local 1-row smoke →
  fire on pool. `state/<slug>/` then holds the **inputs and the outputs** — manifests, stores,
  pre-registration, readout, result json, logs — **not the instrument**.
- ✅ **do** — a **READ-ONLY diagnostic** (e.g. an RF / receptive-field probe) may live as a `state/`
  script, but it must call `core/` forward **directly** — never a re-implementation.
- ❌ **dont** — a `state/*.py` carrying its own forward/decode to measure a new manipulation ·
  cementing a TERMINAL tier on a number the wired engine path never produced.

**Three things wiring buys**: ① a passing result is **ALREADY wired** (no second "now make it live"
step that silently never happens) ② the next experiment **reuses** the manipulation instead of
re-implementing it ③ the flag inherits the `_KNOWN_FLAGS` + `--help` 3-piece set (`evaluate-py-8`)
and the byte-audit for free.

**Measured precedent (H_9309)**: the store-consult was wired as `--consult`/`--consult-format`
inside `cli/evaluate.py`, so when its positive control failed it read as an **EARNED diagnosis**
(*the injection format is unlearned*) rather than as *"maybe my probe is broken"*. With a side
script the two would have been **indistinguishable** — which is exactly how H_9303 and H_9307 died
**undecidable**.

---


**목적:** 실험·벤치·검증(verdict/claim)·스크래치 등 **모든 작업 산출물을 git-tracked 평면 보관**(commons `preserve-state`). 휘발 `/tmp` 금지 — 재현·보존은 여기 한 폴더. 재생성 가능한 `build/`만 gitignore, 머신 로그는 `.harness/`.

## 구조

```
state/
├─ <slug>/              — 한 작업의 코드·출력·RESULT.md (1488+ 누적, 평면)
│  ├─ trainer.py · *.py · *.hexa   — 재현 코드
│  ├─ PREREG*.md · RESULT*.md · VERDICT*.md  — 사전등록·결과
│  └─ ckpt/ result/ logs/          — 산출물
└─ verdicts/<slug>/<id>.txt        — frozen `hexa verify` raw stdout (claims-audit, 992+ slice)
```

## 규칙 (가설 결과는 여기에 코드/출력만, verdict 본체는 UNIVERSE)

- **가설은 2표면, state는 코드/출력만** (`a_hypothesis_register`): 가설 카드 = `HYPOTHESES/cards/H_<id>_<slug>.md`, 인덱스 = `HYPOTHESES/HYPOTHESES.jsonl` 1줄(`artifacts`가 `state/<slug>/` 경로 가리킴). **state/에 카드를 두지 말 것** — 코드·로그·ckpt만. RESULT.md는 작업 노트(허용)지만 verdict 본체·tier는 UNIVERSE 카드+jsonl이 SSOT.
- **measure-or-it-didn't-happen** (c2): RESULT의 수치는 캡처된 출력에서 verbatim. frozen bar 1바이트도 사후 변경 금지(tune-to-green). py 2-production engine-native = TERMINAL-eligible, ad-hoc torch probe = DIRECTIONAL.
- **slug = canonical 이름 하나** (`canonical-naming`): 날짜접미사(`_2026_06_02`)·`_v2`·`_fix`·`_copy` 지양(이력은 git). 신규는 H 번호 또는 의미 slug.

## gotcha (함정 — 실측 교훈)

- **🔑 RESULT/VERDICT.md 있다고 다 "가설"이 아님** (2026-07-01 전수조사 교훈): RESULT 보유 38폴더 중 상당수는 **측정-인프라·torch↔engine 발산 디버그·성능최적화(matmul)·ckpt 복구** 같은 도구 작업이라 UNIVERSE 등록 대상이 아니다(state 보존만으로 충분). UNIVERSE 등록 = G0-G6 게이트 가설 결과(🟢/🧱/🔴 verdict)만. 미등록 RESULT를 발견하면 먼저 `REGISTER(정식가설)`/`ABSORBED(다른 H·메모리에 흡수)`/`INFRA(도구)`로 분류한 뒤 REGISTER만 카드+jsonl.
- **jsonl 등록 교차확인** = `grep "state/<slug>" HYPOTHESES/HYPOTHESES.jsonl` (artifacts 컬럼). 빈 결과여도 INFRA면 정상.
- **zsh glob no-match**: `ls state/*/RESULT*.md`가 한 폴더에 RESULT 없으면 통째 에러(`no matches found`). 폴더별 분기 시 `ls … 2>/dev/null | head -1` 또는 `find`로.
- **무거운 decode/eval은 pool(summer/aiden), mini 금지** — 303M numpy decode는 mini swap OOM(rc=137). 측정은 `anima evaluate --py <clm>` 단일경로(메모리 session-eval-py-only).
- **verdicts/ 992 slice는 학습 pod 동반분**(frozen-bar 재측정용) — 일반 작업 산출물과 별개, prune 신중.

> 루트 거버넌스는 `/Users/mini/dancinlab/anima/CLAUDE.md`(SSOT) 우선 — 충돌 시 루트.
