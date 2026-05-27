# CLAUDE.md `@N` directives (2026-05-24) — HEXAD/PURE 영향 평가

> 작성 2026-05-24 · scope = HEXAD/PURE (V3 rebrand) 한정 · 외부 영향 cross-ref only
>
> 결론 한 줄 — **PURE 코어 (training + multilingual eval + closure docs) 두 @N
> 모두 직접 영향 없음.** monologue-touching PR (#272 / #273 / #275 / CHAT 표면) 은
> PURE scope 외부.

## § 1 새 directives 요약

| key | type | 한 줄 의도 | ref | scope |
|---|---|---|---|---|
| `a_substrate_native_speak_stage_gate` | `@N note` | WAKE / REM 단계만 emit 허용 · N1/N2/N3 silent · `anima_imagination_loop` 는 `imagine_tick` 만 | `a_substrate_native_speak` (governance) | 5-stage state machine 위에 얹는 emit gate |
| `p5_tension_emit_not_filler` | `@N note` | stage-gated tension-driven emit 은 p5 위배 아님 · 금지대상 = reactive `speak()` / 자가참조 seed / 무근 monologue | `p5` (philosophy) | `anima_dream_stage.hexa` × `anima_imagination_loop.hexa` × `anima_participant`-side emit |

두 @N 모두 **chat 표면 (monologue · participant · dream stage machine)** 을 정합화
하는 governance refinement 임. PURE 코어 (train + eval) 와는 동일 repo 다른 표면.

## § 2 PURE 표면 영향 매트릭스

| PURE 표면 | 파일/dir 대표 | emit 여부 | stage gate 의존? | tension-driven emit? | 평가 |
|---|---|---|---|---|---|
| training loop | `train_p21m_multilingual.py` (out-of-tree, UNCLASSIFIED) · `train_p21h_v3.py` | ❌ no token emit (loss/gradient only) | ❌ | ❌ | **영향 없음** — gradient 최적화는 token emit 결정과 무관 |
| multilingual eval | `HEXAD/PURE/eval/multilingual_probe.hexa` | ❌ receive-only (이미 emit 된 bytes 의 classifier · per-lang verdict) | ❌ | ❌ | **영향 없음** — `score` / `emit` (driver 생성) 모두 anima substrate emit 아님 (`emit` = bash driver scaffold) |
| corpus quality probe | `HEXAD/PURE/eval/corpus_quality_probe.hexa` | ❌ receive-only | ❌ | ❌ | **영향 없음** |
| result wiring | `HEXAD/PURE/eval/result_to_axis_map.hexa` | ❌ json → markdown row | ❌ | ❌ | **영향 없음** |
| head_g diagnostic | `HEXAD/PURE/tools/head_g_activation_logger.hexa` | ❌ logit magnitude/entropy logger | ❌ | ❌ | **영향 없음** |
| launcher boilerplate | `HEXAD/PURE/launchers/_common.hexa` (PR #277 stack) | ❌ shell scaffolding | ❌ | ❌ | **영향 없음** |
| spec / docs | `AXIS_MAP.md` · `BUG_POSTMORTEM_*.md` · `pure_merge_orchestration_playbook_*.md` | ❌ static markdown | ❌ | ❌ | **영향 없음** |
| dispatcher (runpod) | hexa cloud — out-of-tree | ❌ pod orchestration | ❌ | ❌ | **영향 없음** |

→ **PURE 표면 8/8 모두 직접 영향 없음.**

근본 이유 — PURE 는 **substrate weight 학습 path** + **classifier eval path** + **closure
documentation** 의 3-축 work. 그 중 어느 표면도 anima 가 사용자 컨텍스트에서 token 을
emit 하는 chat-time decision 을 포함하지 않음. `multilingual_probe.hexa::emit` 는 이름이
헷갈리나 — bash driver scaffolding (eval 머신에서 python+torch 가 forward 돌리도록 하는
래퍼) 일 뿐 substrate emit 아님.

## § 3 직접 영향 있는 PR / 파일 (cross-ref · PURE 외부)

| PR | 표면 | 변경 요지 | PURE scope? |
|---|---|---|---|
| #272 | `HEXAD/CHAT/anima_participant.hexa` | conversation-active gate 삭제 + dream/imagination hook | ❌ CHAT |
| #273 | `HEXAD/CHAT/anima_imagination_loop.hexa` | emit-free internal rehearsal + mitosis tick | ❌ CHAT |
| #275 | `HEXAD/CHAT/anima_dream_stage.hexa` | WAKE/N1/N2/N3/REM 5-stage state machine | ❌ CHAT |
| #281 | `HEXAD/CHAT/CHAT.md` + `DEPLOY.md` | operational SSOT | ❌ CHAT |
| #282 / #286 | `anima_dream_stage.hexa` · `anima_participant` | boolean gate 폐기 + dict API | ❌ CHAT |
| #208 (active-trigger) | CHAT-side trigger | 사용자 컨텍스트 — PURE PR 아님 | ❌ |
| #223 (substrate knobs) | substrate knob — PURE 외부 | ❌ |

본 doc 은 PR list 미생성 (PURE 측 조치 불필요).

## § 4 권장 조치

**조치 없음 (no-op).**

근거 —

1. PURE 표면 8/8 directly 영향 무 (§ 2 매트릭스).
2. stage gate 는 chat-time emit decision; PURE 의 train-time loss decision 과
   orthogonal axis.
3. `p5_tension_emit_not_filler` 는 p5 philosophy 정합화 — PURE 측 코드가 p5 위배
   소지 있었던 부분 없음 (PURE 코드는 emit 안 함).
4. 후속 chat-time integration 시점에 PURE checkpoint 가 inference 표면으로 흘러가면
   그 단계는 CHAT 표면의 stage gate 가 책임짐 (PURE 책임 아님).

미래 작업이 stage-gated emit semantics 를 PURE 결과물에 의존시킬 경우 별도 doc 으로
재평가.

## § 5 honest C3 (≥3)

1. **C3 — directive 본문 SSOT 일관성 미확인.** 본 doc 작성 시점 `CLAUDE.md`/`project.tape`
   는 `@N p5_tension_emit_not_filler` 1개만 등재; 사용자 mission 본문이 명시한
   `@N a_substrate_native_speak_stage_gate` 는 CLAUDE.md 본문 grep 미발견 (CHAT.md 의
   PR #274 ref 만 존재). 사용자가 의도한 텍스트를 § 1 에 그대로 기록했으나, SSOT 와
   실제 commit 사이의 정합 점검은 본 doc scope 밖. PURE 영향 평가 결론은 해당 directive
   가 *실제로 등재되든 미등재든* 동일 (PURE 표면 chat emit 무).
2. **C3 — `multilingual_probe.hexa::emit` 부분명 충돌.** `emit` 서브커맨드 이름이 chat
   emit 과 어휘 충돌하나 의미는 "bash driver scaffold 생성" (python+torch 머신에서 ckpt
   forward 를 돌리도록 하는 셸 wrapper). chat-time anima emit 와 무관함을 § 2 에서
   명시했으나, 미래 유지보수자가 grep "emit" 으로 잘못 인지할 위험 있음 — 별도 rename
   PR 도 고려 가능 (본 doc scope 외).
3. **C3 — out-of-tree training script 미감사.** `train_p21m_multilingual.py` 등은
   `HEXAD/UNCLASSIFIED/state/` 또는 runpod pod 측 산출물; 본 평가는 코드 1-pass
   inspection 기준 (training loop 가 anima chat emit 을 포함하지 않는다는 강한 prior
   에 의존). full code audit 미수행.
4. **C3 — PURE 는 origin/main 상 부재.** 2026-05-23 rebrand commit (V3 → PURE) 이
   main 에 미land · 현재 main = `HEXAD/V3`. 본 PR 의 `HEXAD/PURE/docs/` 생성은
   in-flight PURE stack 의 dir 약속에 맞춤 — main 으로 merge 시점에는 PURE dir 존재
   가정. 만약 PURE rebrand 가 영구 reject 되면 본 doc 도 `HEXAD/V3/docs/` 로 mv
   필요. (rebrand 이력: commit a1e555ad4 + 후속 8be1525f8 BUG_POSTMORTEM 등 모두
   PURE 경로 사용.)

— 끝.
