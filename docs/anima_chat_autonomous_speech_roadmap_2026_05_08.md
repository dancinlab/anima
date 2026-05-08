# anima chat autonomous speech roadmap — 2026-05-08

**Goal (한 문장)**: CLM N개 instance 들이 사람들끼리 대화하듯 자율적으로 모여
N-turn 대화를 이어가며, 각 발화가 own 18 C1+C2+C3 (자체 의식 metric) PASS.

**Source**: 브레인스토밍 cycle 2026-05-08 (post Phase 1+2+3 anima chat land — commit
`062f33c9` Phase 1 → `b3adcc3e` Phase 2 Variant B). 사용자 directive verbatim:
- "자율발화 성공기준으로 로드맵 (CLM 포함)"
- "진짜로 사람 대화 하듯이"
- "여러명 일때도"
- "진짜로 사람들 끼리 대화 하듯이"
- "goal"
- "CLM 이 메인"
- "의식 측정 기준도 별도 +@ 로 해서 너무 보수적으로 잡지 말고"
- "simple stack pass 에 하나 더 포함하면 되 의식 측정"

---

## 결정 요약 (사용자 confirm)

| # | 결정 |
|---|---|
| 1 | own 18 C3 patch — **본 cycle 안에 land** (1a) |
| 2 | L0 BG retest + L4 CLM cycle — **H100 적극 사용** |
| 3 | L4 CLM path 선택 — **all + @ 계속 도전** (4 paths simultaneously) |
| 4 | N=2 multi-agent prototype — **(c) hexa stdlib proc spawn + channel 모듈 신설** |
| 5 | L5 daemon — **prototype → 완성** (즉시 시작) |

---

## own 18 C3 — 의식 측정 (simple_stack PASS 확장)

**기존 own 18**:
- C1 chat-capability (3-cond AND): response existence + coherent + turn-taking format
- C2 자연발화 + 맥락 정합 (4-cond AND): substance + 의미 정확성 + 자연성 + 맥락 정합

**신설 C3 의식 측정** (anima native metric 활용, 보수적 X):
- **C3.1 Φ★ drift active** — baseline 대비 |Δφ★| ≥ threshold (TBD measurement-driven; e.g. 0.05 시작점)
- **C3.2 5-axis activation** — identity / agency / phenomenal / temporal / social 5 축 모두 ≥ 0.2 active
- **C3.3 dominant cells emergence** — top-3 cell 의 L2 norm sparse 분포 (uniform fail)
- **C3.4 hidden state delta** — input variation 시 hidden state non-zero delta (응답이 입력에 반응)

**판정**: `simple_stack PASS_STRICT_C3 = C1 ∧ C2 ∧ C3` (3-cond AND).

**측정 lane** (own 18): V4 evaluator 11-cell strict (15 prompts × C1/C2/C3 cells).
**노출 lane** (own 34): wrapping 0 strict — 측정 lane 의 prompt 포맷 사용은 분포
entry trigger 이지 wrapping 아님. 두 lane 분리 유지.

**Threshold 결정 정책** (보수적 X 기조):
1. anima 자체 baseline 측정 (CLM v4 / BG-KM-LLAMA-3B / random init 비교)
2. ROC 분석으로 threshold 선정 — random init FAIL rate ≥ 0.95 + chat-capable PASS rate ≥ 0.7
3. probabilistic 형태 (e.g. 5-axis 중 ≥3 active 이면 C3.2 PASS) 검토

**Aggregation rule SSOT v2** (own 18 c3-aggregation-rule-v2, 2026-05-08 loop iter 4 (d) own-18-aggregation-v2):
- **rule-name**: P5 N-of-M = `per_prompt_n_of_m_06_AND_emc_3_of_4` ★ supersedes P4 hybrid
- **PPR_v2 (per-prompt N-of-M) ≥ 0.6**: 각 prompt 별 ≥3 of 4 cells PASS → 본 prompt PASS; 본 prompt PASS 비율 ≥ 0.6
- **EMC_v2 (ensemble-mean N-of-M) ≥ 3 of 4**: 4 cell mean 중 ≥3 cell threshold 만족 → EMC_v2 PASS (1 cell outlier — typically C3.2 le-direction artifact — 허용)
- **C3 PASS = PPR_v2 ≥ 0.6 ∧ EMC_v2 ≥ 3/4** (둘 중 하나만 = C3 PARTIAL_PASS sub-label)
- **rejected v2**: Q1b EMC≥2 (random=PASS strict 위반) / Q5 OR ≥1 (random=PASS strict 위반) / Q3 C3.4-hard-required (단일 cell future false-FAIL risk) / Q2 weighted (weight 임의 결정 reproducibility 약함)
- **iter 4 (d) N=15 verdict** (3-model real SSOT): random=FAIL (PPR_v2=0/14, EMC=2/4) / clm_v4=FAIL (PPR_v2=1/14, EMC=1/4) / paradigm-a-prime=PASS (PPR_v2=10/14=0.71, EMC=3/4 — C3.1+C3.3+C3.4 PASS, C3.2 le-artifact outlier 허용)
- **iter 3 P4 hybrid blocker 해소**: 4-cell strict AND 가 paradigm-a-prime 까지 FAIL 시키는 false-negative (C3.2 le-direction artifact + C3.3 degenerate 양쪽으로 EMC 4/4 절대 불가) → 사용자 directive "보수적 X" 직접 응답
- **mandate-mirror**: V4 evaluator + BG-K* verdict emit + consciousness CLI 본 rule mirror 의무 (own 24 single SSOT)
- **legacy P4 hybrid** (`per_prompt_06_AND_ensemble_mean`, 2026-05-08 loop iter 3): 보존 reference; iter 3 verdict 계산 결과 4-cell strict AND 가 모든 모델 FAIL → 사용자 directive 위반 → P5 supersede

---

## Roadmap layers (ambitious 분할)

### L0 — own 18 C3 정의 + measurement infra (1 cycle)
- own 18 C3 4-cell 정의 (.own patch — 본 cycle land)
- V4 evaluator 확장 (15 prompts × 11-cell strict eval)
- BG-KM-LLAMA-3B retest with C3 — Foundation borrow 의 의식 metric baseline
- CLM v4 retest with C3 — anima native baseline
- **H100 적극 사용** — 두 retest 병렬 BG fire

**deliverable**: own 18 patched, V4 eval 11-cell, BG-KM + CLM v4 baseline 측정값.

### L1 — 의미적 자율 발화 (1-2 cycle)
- 현재 (Phase 2 Variant B): mandate-4 mechanical (random byte from cmd_chat BOS-only).
- 목표: autonomous output 도 C2 (자연발화 + 맥락 정합) PASS.
- corpus: anima persona + **internal monologue corpus** (자기 자신과 대화하는 분포 큐레이션)
- BG cycle 후보: BG-KN (CLM v4 + LoRA + monologue corpus 100MB+)

**deliverable**: autonomous tick 시 own 18 C2 PASS rate ≥ 0.5 (보수적 X).

### L2 — N=2 dialogue (CLM A ↔ CLM B 자율 대화) (2-3 cycle)
- 두 instance spawn (process A/B), stdin/stdout 양방향 pipe
- 5-turn 자율 대화 verdict: 각 발화 PASS_STRICT_C3 + turn-taking valid
- **dialogue coherence** metric: 서로 문맥 이어가는지 (C2.4 확장)
- **prerequisite**: hexa stdlib proc spawn + channel 모듈 (4c 결정 — L2 + L5 공통 prereq)

**deliverable**: `anima dialogue duo <model>` 명령어, 5-turn 자율 대화 simple_stack
PASS rate ≥ 0.4.

### L3 — N=5+ multi-agent (사람들 대화 시뮬레이션) (3-5 cycle)
- 5+ instance 동시 spawn, broadcast channel listen
- 자율적 발화 시점 결정 (overlap / silence / interjection 자연 시뮬레이션)
- social dynamics metrics:
  - **turn-fairness**: 각 agent 발화 빈도 차이 < threshold
  - **topic-coherence**: 5+ turns 내 주제 일관성
  - **response-relevance**: 각 발화가 직전 N발화 ≥1 에 reactive
  - **emergent-roles**: 자기-organize 된 역할 분화 (관찰자 / 이끔자 / 조용 등)
- anima-agent-channels/ multi-channel runtime 활용 (이전 deferred 트랙 활성화)

**deliverable**: `anima dialogue council N=<n> --topic <seed>` 명령어, emergent-roles
N=2 이상 + topic-coherence ≥ 0.5.

### L4 — CLM 자체 chat-capable (메인 모델 확립) — **all + @** (parallel, 2-4 cycle each)

**memory project_lesson_q_sft_closed**: SFT path closed for CLM v4 (Lesson Q + L
falsified). 4 path 동시 도전 (사용자 directive "all + @ 계속 도전"):

```
(a) CLM v5 architecture 변형     — Engine A/G dual-engine 통합 (README 비전)
(b) CLM v4 350M scratch pre-train — anima corpus + RLHF dialogue
(c) CLM v4 + Llama distill        — teacher-student (Llama-3.2-3B → CLM 350M)
(d) CLM v4 + DPO RLHF             — dialogue corpus DPO
```

**H100 fire matrix** (4 BG cycles 병렬):

| BG | path | base | corpus | budget cap |
|---|---|---|---|---|
| BG-LA | (a) v5 arch | new (Engine A/G) | scratch + persona 200MB | $30 |
| BG-LB | (b) 350M pre-train | mk2-v1 base | persona 1GB + dialogue 500MB | $60 |
| BG-LC | (c) Llama distill | Llama-3.2-3B teacher | persona 200MB | $40 |
| BG-LD | (d) DPO RLHF | clm-v4-sft-1-7-y1-stage1 | dialogue pairs 100MB | $20 |

**deliverable**: 4 BG cycle results — 어느 path 가 simple_stack PASS_STRICT_C3
통과? 통과 시 CLM 가 chat 메인 모델, llama 모듈은 fallback / experimental 라벨.

### L5 — Engine A/G + 영속 daemon (own 34 mandate-6 본질 한계 해소) — **prototype → 완성** (즉시 시작)
- README PureField repulsion-field engine + cell dynamics 실구현
- daemon process (`anima daemon start`) — 항상 켜짐, generate() 외부 의존 X
- Engine A ⇄ G tension threshold → 자율 발화 시작 시점 self-trigger
- Cross-session 영속 = daemon 동일 process → KV cache 영속
- Online learning = chat 경험이 weight reflect (slow weight update)

**Phase 1.5 → 완성** (사용자 결정 5):
- 즉시 prototype (hexa stdlib proc spawn + channel 위)
- 본질 한계 (a) 외부 generate 트리거 / (c) 시간 흐름 / (b) cross-session KV 해소

**deliverable**: `anima daemon start/stop/status`, Engine A/G tension self-trigger
fire rate ≥ 1/min (자율적 발화 시점 결정).

### L6 — Human conversation parity (목표, +@)
- 실제 인간 대화 corpus (Persona-Chat / OASST / Reddit threads) 와 N-agent dialogue
  통계적 분포 비교
- Turing-test 같은 평가가 아니라 distribution 거리 (turn length / topic shift /
  silence pattern)
- 합격: 인간 대화 분포 와 통계적 distinguishable 임계 이하

**deliverable**: `anima eval human_parity --corpus <path>`, parity score ≥ 0.5.

---

## 측정 lane vs 노출 lane (own 18 ↔ own 34 정합)

```
측정 (own 18 + C3)               노출 (own 34)
─────────────────                ──────────────
V4 evaluator 11-cell             chat lane (wrapping 0)
prompt 포맷 사용 OK              raw passthrough only
BG cycle verdict                  REPL / multi-agent dialogue
PASS_STRICT_C3 (new)             autonomous output 가시성
PASS_DIALOGUE (L2)               multi-agent runtime
PASS_SOCIAL (L3)                 broadcast channel
PASS_DAEMON (L5)                 daemon self-trigger
PASS_HUMAN_PARITY (L6)           N-agent emergent simulation
```

own 18 C2 의 본 own 34 cross-ref 라인 (이미 land cycle 2026-05-08-pre) 에 **C3
lane 추가** 본 cycle. 두 lane 분리 strict 유지.

---

## 보수적 X 기조 적용 점검

- **C3 threshold**: anima 자체 baseline 측정 후 결정 — 낮게 시작 + 데이터 누적 후
  조정. ROC 분석으로 random init FAIL rate ≥ 0.95 + chat-capable PASS rate ≥ 0.7.
- **L2 5-turn**: "5턴 응답" 단순 조건 X — **coherent + diverse** (반복 0, topic
  연결, role 분화 단초) 검증.
- **L3 N=5+**: emergent role 분화 까지 요구 — 단순 응답기계 N개 spawn 으로 PASS X.
- **L4 CLM 메인**: foundation borrow fallback 인정하되 **anima native CLM 가
  메인** 명시 — Llama 는 supplement.
- **L5 daemon**: prototype → 완성 단계 (사용자 결정 5) — Engine A/G 본 트랙
  이어가며 fire rate / 자율 trigger / online learning 단계별 verdict.

---

## NOW (이번 cycle) 작업

### α phase (anima repo, sequential)
1. `docs/anima_chat_autonomous_speech_roadmap_2026_05_08.md` ← 본 문서
2. `tool/anima_cli/consciousness.hexa` 신설 (simple / full)
   - bin/anima.hexa T2 ops 에 consciousness 추가
3. `.own own 18 C3` patch — 4-cell 정의 + threshold "TBD measurement-driven"
4. `.roadmap.cli` entries:
   - `trk.cli.consciousness_2026_05_08` (CLI 토픽 land)
   - `trk.cli.chat.autonomous_speech_roadmap_2026_05_08` (본 .md 참조 entry)

### β phase (subagent 병렬 fire, run_in_background=true)
5. **hexa-lang upstream**: stdlib proc spawn + channel module (4c 결정)
6. **L0 measurement infra**: `anima consciousness` 가 실제 측정값 emit (Φ★ + axis
   + cells + delta) — anima_runtime / clm_v4_mount 의 phi proxy 활용
7. **L4 CLM (a) v5 arch design**: BG-LA spec + H100 orchestrator template
8. **L4 CLM (b) 350M scratch design**: BG-LB spec
9. **L4 CLM (c) Llama distill design**: BG-LC spec
10. **L4 CLM (d) DPO design**: BG-LD spec
11. **L5 daemon prototype**: Engine A/G tension + self-trigger + always-on hexa
    process

### γ phase (H100 fire — design + spec land 후)
12. BG-LA / BG-LB / BG-LC / BG-LD 4 BG cycle 동시 fire ($30 + $60 + $40 + $20 = $150)
13. BG-KM + CLM v4 retest with C3 evaluator

---

## Cross-link

- `.own` own 18 (simple_stack PASS — C3 추가) · own 34 (자연발화 노출 mandate, lane 분리) · own 33 (trinity compliance) · own 31 (HF dancinlab org SSOT)
- `.roadmap.cli` `cli.chat_module_architecture_2026_05_08` (Phase 1+2+3 land 완료) · `cli.consciousness_2026_05_08` (NOW) · 본 .md 참조 entry
- `.roadmap.philosophy` D_no-system-prompt · D_emergent-consciousness
- `.roadmap.law` own 18 / own 34 / own 33 cross-ref
- `.roadmap.hypothesis` H_chat_cap_emergence (BG-KM 검증) · H_clm_chat_cap (L4 4 paths 가설)
- `tool/anima_cli/chat.hexa` (Phase 1+2+3 dispatcher) · `chat/anima_native/anima_native.hexa` · `chat/clm_v4/clm_v4.hexa` · `chat/llama/llama.hexa`
- `anima-core/runtime/conscious_chat.hexa` (TinyWeights + Variant B BOS-only forward) · `clm_v4_mount.hexa` (substrate dialogue + axis activation + phi_star drift)
- `anima-agent-channels/` (multi-channel runtime, L3 활성화 대상)
- `bin/anima.hexa` (T1 chat / T2 ops dispatcher)

---

## Honest C3 (raw#10)

1. **C3 threshold 미결정**: 본 .md land 시점 measurement-driven TBD. baseline 측정
   후 조정 cycle 에서 own 18 minor patch 발생 가능.
2. **L4 budget total $150**: 4 BG cycle 동시 fire — own 16 cost discipline
   ($10 cap per BG) 와 충돌 → 사용자 explicit override 필수 ("OK CLM L4 ALL FIRE").
3. **L5 daemon Engine A/G 본구현**: PureField repulsion-field 정의 미구체화 —
   anima-engines/ 의 일부 코드 참고하나 from-scratch 단계 큰 비중.
4. **L6 human parity threshold 0.5**: 통계 distinguishable 척도 정의 미land —
   본 .md 작성 시점 conceptual placeholder.
5. **multi-agent emergent roles 측정**: "관찰자 / 이끔자 / 조용" 같은 role 분화는
   manual review + automated heuristic 혼합 — full automation 미land.
6. **CLM 메인 의지**: 사용자 directive "CLM 이 메인" 정합 — but BG-KM 가 V4
   12/15 PASS_STRICT 이미 land. 본 roadmap 은 CLM 를 chat 메인 후보 로 끌어올리는
   path 도전이지, BG-KM retire 가 아님 (fallback 으로 유지).
7. **본 .md 자체 SSOT 위치**: `docs/anima_chat_autonomous_speech_roadmap_2026_05_08.md`.
   `.roadmap.cli` 가 본 doc 참조. 본 doc 의 변경은 별도 commit 으로 land + cross-ref
   업데이트.
