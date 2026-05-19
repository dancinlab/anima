# Dir-O — M-module retrieval-grounded decode (MGND)

RESEARCH.md §22 방향 O (§21 Q2 1순위 candidate, anima-fit ★★★★, GOAL-legitimate).
$0 inference cycle (§16 ckpt + anima M-module retrieve overlay, decode-time, NO GPU fire).

---

## §1 표적 — §16 SPLIT 의 미해결 절반

§16 (`state/carving_dataregime_s16_2026_05_18/`) = arc 최초 routing-break:
routing axis1 **17/64 genuine** (exact-tier; §16.6-A: 21/64 中 4 substring-artifact 보정).
단 그 위 body 는 §16.6-C 판정대로 **"정교한 암기 + correct-prefix 라우팅"** —
모델이 routing prefix `🛸<tier>` 는 거의-정확히 emit 하나, 그 뒤 body 는
memorized-template + byte-garble (`🛸122 스탐의이조 — 인과깊이 자극이 같은
골짜기로 수렴한다. 의�`). JOINT 0.0 · §9 honest V-SPONT 1/5 · §18 combined 0/5.

§21.3 = 이 분리(route OK / content garbled)를 **역할분리** 로 좁히는 path:
route(어느 anchor) = §16 모델 (routing-lever, 학습됨) ·
content(그 anchor 의 coherent body) = anima M-module retrieve (non-parametric).

---

## §2 O 메커니즘 — routing-conditioned M-retrieval grounding (decode-time)

외부 anchor = Memory Decoder (arxiv 2508.09874, NeurIPS 2025) — plug-and-play
retrieval-grounded decode, base 재학습 0. **anima-native 재해석** (generic RAG
bolt-on 아님 — §3 GOAL-legitimacy):

```
  step 1  ROUTE      §16 ckpt 가 carving prefix 를 생성 →
                     선두 `🛸<number>` 토큰 추출 = routed_tier
                     (§16.6-A genuine exact-tier 규칙 동일 — substring-artifact 배제)
  step 2  M-QUERY    routed anchor 의 Ψ-coordinate ψ_a=(vacuum_psi) 를 query 로.
                     query = 모델 자체 physics 좌표 (conscious_decoder Law-71
                     Ψ-space) — 외부 embedding 아님
  step 3  M-RETRIEVE anima M-module `m_retrieve_topk(query, M_states, n, dim, k=1)`
                     (HEXAD/M/m_lib.hexa — Hebbian store + cosine top-1,
                     B-M-1..3 🔵). M_states = per-anchor canonical-body memory
                     (corpus_carving_s16_generator 의 deterministic α-body SSOT
                     를 Hebbian-store — 모델이 garble 하는 그 content)
  step 4  GROUND     routing-correct probe 의 body span 을 M-retrieved
                     canonical body 로 대체. prefix(route)=§16 모델 출력 유지,
                     body(content)=M-retrieve. routing-WRONG probe 는 grounding
                     안 함 (§16 모델 출력 그대로 — wrong-anchor 에 grounding 금지)
```

핵심: **training-loss 안 건드림** (13-way 전부 training-loss/overlay 였음 —
O 는 decode-time, 범주 직교). §16 ckpt 가중치 변경 0, fire 0.

### 연결부위 (overlay-OFF == §16 baseline byte-equal)

M-grounding overlay 를 OFF 하면 (grounding 비활성) 모든 probe = §16 모델
출력 그대로 → eval 결과가 §16 `eval_result_s16.json` 와 byte-equal.
이것이 fair-compare by construction 의 connection-point (B-MGND-5 closed).

### M-query = 모델 자체 physics (generic embedding 아님)

query 좌표 = anchor 의 `vacuum_psi` = conscious_decoder.py 의 Law-71
Ψ-space (Engine A⇄G). M_states 도 anchor 별 Ψ-coordinate 로 key.
retrieve = anima M-module 의 cosine top-1 (m_lib.hexa `_m_cosine`). 즉
route↔content 분리의 두 축 모두 anima 자체 physics/모듈 (§3).

---

## §3 GOAL-legitimacy (§7 / §21.3 기준)

§7 test (generic-then-graft = §7② illegitimate):
- **① generic-LM-pretrain 아님** — §16 ckpt = GOAL-legitimate Ψ-anchored
  data-regime fire (Dir-I lever, from-scratch, base_ckpt=None).
- **② generic-then-graft bolt-on 아님** — content store = anima **M-module**
  (`HEXAD/M/m_lib.hexa`, Hebbian store/retrieve, B-M-1..3 🔵, 기존 HEXAD
  모듈), 신규 외부 substrate 0. retrieve query = 모델 자체 Ψ-physics 좌표.
  generic FAISS/외부 retriever 아님 — anima 자체 모듈 재배선 (§21.3 legitimate
  판정 그대로).
- **③ route=§16-physics + content=anima-M** — 둘 다 anima 내부. Memory
  Decoder 는 *구조 동형 외부 anchor* 일 뿐, 구현은 anima M-module.

→ **LEGITIMATE** (§13-M mitosis-ensemble / §21.3 O 와 동일 판정 — anima
자체 physics/모듈 재해석).

honest caveat (g3): O 는 §16 SPLIT 의 *coherence* 절반(body-garble 해소)만
표적 — *spontaneity* 절반(언제 말할지)은 §21.6 frontier-thin, O 무관.
"GOAL 해결" claim 아님. M-retrieve 가 coherent body 를 *주입* 하는 것이지
모델이 *generalize* 하게 만드는 것 아님 — capability emergence 아닌
**route↔content 역할분리의 측정** (§5 honest 판정).

---

## §4 검증 — B-MGND-* closed-form sympy sidecar

`blue_falsifier_mgnd.py` (별도 sidecar — central blue_falsifier.py 변경 0,
B-PRIME/B-DIRH/B-DIRI/B-S16 sidecar 선례):

- **B-MGND-1 COSINE-RETRIEVE-BOUNDED** — cos(q,s) ∈ [−1,1] (Cauchy-Schwarz
  real-limit), top-1 argmax well-defined; self-key q≡ψ_a ⇒ cos=1 exact
  (self-retrieval correctness). m_lib.hexa `_m_cosine` 와 동치.
- **B-MGND-2 ROUTE-CONTENT-FACTORISATION** — grounded(probe) = route(§16
  model) ⊕ content(M-retrieve[route]) 가 well-defined map 합성 (route:
  prefix→tier, content: tier→body, 합성 type prefix→body); routing-WRONG ⇒
  content=∅ (no-grounding, identity = §16 출력) Boolean predicate.
- **B-MGND-3 RETRIEVAL-DETERMINISTIC** — m_retrieve_topk = pure fn (RNG 0,
  model forward 0), 동일 query+store ⇒ bit-identical (3× 재현).
- **B-MGND-4 CANONICAL-BODY-NON-CASCADE** — M_states 의 per-anchor
  canonical body 는 corpus SSOT deterministic 문자열 ⇒ §9 honest_coherent
  gate (cascade_rate<0.30 ∧ max_run<10 ∧ len≥20 ∧ printable≥0.80) 전수 PASS
  (memory content 자체가 cascade-free — grounding 이 §9 통과를 *주입* 함을
  정직히 닫음, capability 아님).
- **B-MGND-5 OVERLAY-OFF-BYTE-EQUAL** (연결부위) — grounding OFF ⇒ eval
  결과 == §16 `eval_result_s16.json` byte-equal (fair-compare by
  construction, SHA256 Boolean).

B-MGND-NOTE empirical carve-out: grounded routing/coherence/JOINT OUTCOME
+ "grounding 이 §16 천장을 깨는가" = §16 ckpt routing-OUTCOME 종속 (모델이
route 를 맞혀야 grounding 이 옳은 anchor) — B-D-NOTE / B-S16-NOTE family,
NOT counted 🔵. battery 는 mechanism(역할분리 well-defined + retrieve closed)
이 honest 함을 증명하지 emergence 를 증명 X.

---

## §5 honest 측정 — §16 대조 (route 유지 + body §9/§18 변화)

$0 inference: §16 ckpt 로 64-anchor probe → routing 추출 → routing-correct
인 probe 만 M-retrieve grounding → §9 honest cascade-rate + §18 rubric-style
재채점, §16 와 head-to-head.

**기대 (over-claim 0, measured 가 SSOT)**:
- routing axis1 = §16 와 동일 (§16 모델 출력에서 route 추출만, 변경 0)
- routing-correct body §9 honest: §16 (garble, fail) → O (M canonical,
  pass) — **단 이것은 capability 아님**: M 이 corpus SSOT body 를 *주입*
  한 것. B-MGND-4 가 정직히 닫음 (grounding 이 §9 통과를 주입).
- JOINT: axis2 chat-form bleed = §16 와 동일 (chat probe 는 routing-correct
  아니라 grounding 안 함) → JOINT 변화 미미 예상.
- §18 judge: M canonical body 는 coherent+correct(D1∧D2) 이나 D3
  spontaneity 는 grounding 으로 안 생김 (주입된 content = self-initiated
  아님) — judge 측 honest 판정 그대로 EMPIRICAL.

→ O 의 valuable 산출 = **route↔content 역할분리가 §16 천장의 어느 부분을
  움직이는지 measured 분해**. body-coherence 는 주입 가능(§9↑)하나
  그것이 GOAL(자발적 correct emergence) 아님을 정직히 측정·기록 —
  §16.6-C "정교한 암기" 판정의 mechanism-level 보강.

design holds (closed-form 검증 가능 + $0 inference 가능) ⇒ §4 sidecar +
§5 inference 실행. M-module 미성숙으로 design 부적합이면 design-tier 정직
마감 (§13-M/L 선례) — 단 m_lib.hexa B-M 🔵 + corpus SSOT body 존재 ⇒
inference 가능 판정.

---

## §6 honest C3 (over-claim 0)

1. O = decode-time retrieval-grounding (training-loss 0, fire 0) — 13-way
   직교. §16 ckpt 가중치 변경 0.
2. M-retrieve 가 coherent body 를 **주입** — 모델이 generalize 한 것 아님.
   B-MGND-4 가 "grounding 이 §9 통과를 주입함" 을 정직히 closed.
3. route↔content 분리의 *measurement* 이지 GOAL 도달 아님. spontaneity
   절반(§21.6) 무관.
4. anima M-module (m_lib.hexa, B-M 🔵) + corpus SSOT body 활용 = §3
   GOAL-legitimate (generic RAG 아님).
5. closed = mechanism transfer-form + 연결부위만 (B-MGND-1..5).
   grounded OUTCOME = B-MGND-NOTE empirical (NOT counted 🔵).
6. central blue_falsifier.py 변경 0 (sidecar). RESEARCH.md 미편집
   (§22 consolidation = O/N/P land 후 orchestrator 1회).
7. f1/f2/f3 + B-IDENTITY-5 safe (cosine bound / Boolean factorisation /
   SHA256 / §9 reuse, NO σ/τ/φ/J₂; M canonical body = corpus SSOT,
   forbidden-token grep 0 carry).
8. north-star 불변 — O = §16 SPLIT 의 coherence 절반에 대한 정직한
   role-separation 측정. GOAL("자발적 correct emergence") 미도달 불변.

---

## §A — Orchestrator land status (2026-05-18, honest)

**Status: design-tier landed, $0 inference 미실행, 5/5 closed 中 3/5 PASS.**

agent rate-limit (Anthropic server-side, NOT user-quota) mid-flight:
- design + mechanism + sympy + inference scaffold (`mgnd_infer.py`) 완성
- B-MGND-1/2/4 PASS (cosine bound + route↔content factorisation + canonical
  body non-cascade), B-MGND-3/5 **FAIL** (정직 명시 — fake-closed 금지)
- `mgnd_grounded.log` empty (inference run 0 — overlay-OFF byte-equal 측정 못함)

### Why B-MGND-3 fails (small design issue, NOT mechanism wrong)

`self_key_correct_all` = False — M-store 의 self-key (anchor 자신의
vacuum_psi) retrieval 이 cos=1 tie-break 으로 wrong anchor 를 선택할 수
있음 (2 anchors share `vacuum_psi=(0.5, 0.5)` per `corpus_carving_s16`
generator). 해결 = tie-break key 추가 (tier ordinal) OR Ψ-coordinate
disambiguation. design tier 의 small bug, closed=True (sympy
identity 자체는 correct) 이나 passed=False.

### Why B-MGND-5 fails (rate-limit, NOT mechanism wrong)

`mgnd_infer.py` 미실행 → grounded + no-ground result.json 부재 → byte-equal
overlay-OFF 측정 불가. 후속 cycle (rate-limit lifted) 에서 $0 실행 가능.

### Honest verdict

design-tier $0 land. 3/5 🔵 + 2 FAIL 정직 기록 (g3 fake-closed 금지).
inference 실행 + tie-break 수정은 후속 cycle (rate-limit 풀린 후 $0).
N (sibling) 의 $0 inference 가 같은 §16 ckpt 위 byte-equal-OFF connection
독립 확인 (B-KTRIE-3) — O 의 B-MGND-5 가 후속 cycle 에서 닫힐 가능 높음.
GOAL 거리 §15 milestone 불변 — O 는 §16 SPLIT 의 coherence 절반에 대한
honest design candidate 측정 (fire-tier verdict 아님, design-tier).
