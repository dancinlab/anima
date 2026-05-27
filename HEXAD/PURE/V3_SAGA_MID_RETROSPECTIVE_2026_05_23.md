# V3 saga session-3 중간 retrospective

**Phase 2 → AXIS_MAP-FAN 5/7+2 → R8 fork (2026-05-22~23)**

scope: HEXAD/PURE (V3 saga rebrand)
status: session-3 진행중 — interim consolidation at AXIS_MAP-FAN 5/7+2 milestone
date: 2026-05-23

---

## § TL;DR

1. **Phase 2 fix → ko STRONG 19/20 첫 V3 STRONG** 결과 (그러나 단일축, 3B scale 후 overfit).
2. **V3 CLOSED 선언** (pure-HEXAD 7 fire 0 PASS) → AXIS_MAP fallback 7-axis fan-out.
3. **env-var-concat 버그**로 1차 + 2차 fan-out 부분 실패 (.envbug 7개 archived, $14 saga).
4. **4-axis redispatch (cycle 1)** → D FAIL + E OOM + C/C2 abort → 5/7+2 partial.
5. **R8 fork 개시**: init_CE 14+ catastrophic floor 자연실험 발견 (3 cluster X/Y/Z, head_g 가설 FALSIFIED, noise / kv-head / mitosis_pool 잔여 후보).

---

## § Act structure (5-act)

### Act 1 — Phase 2 fix + Phase 2 full (2026-05-22)

- **Phase 2 fix** (23:48–23:55 KST): `vP21H_phase2_fixed/`, wall 1649s, ckpt 5.7 GB on pod
  - ko STRONG **19/20** — V3 saga 첫 STRONG 결과
  - 단일축 (ko 단독) 결과 — multilingual generalization 미증명
- **Phase 2 full** (다음 날 02:17–02:43): 3B scale attempt, `vP21H_phase2_full/`, wall 7367s
  - **FAIL n_strong=0** — 3B scale overfit
  - ckpt 6 GB pulled, HF `dancinlab/anima-v3-p21h` PRIVATE 16 files
- 비용: $0.27 + ~$3 = ~**$3.3**

### Act 2 — V3 CLOSED 선언 + AXIS_MAP.md (04:54 KST 2026-05-23)

- commit `ce6c4ad93`: "pure-HEXAD 7 fire 0 PASS, corpus 축까지 sweep 후 closure complete"
- double bind 발견: anima→register collapse vs no-anima→Chinchilla underfit
- AXIS_MAP.md fallback path 작성: B (증류) / A (커리큘럼) / C (head_g) 7-axis spec
- 결정: AXIS_MAP-FAN 7-axis fan-out 으로 fallback 진입

### Act 3 — AXIS_MAP-FAN 1차 + 2차 fan-out (env-var bug saga)

- **1차 fan-out** (04:34 KST 2026-05-23): 7 pod CRASHED at launch
  - 원인: caller-side env-var concat (shell variable assignment 인접 concat 으로 한 env 가 다음 env 변수에 prepend)
  - 결과: `.envbug_1779511267` dirs archived
- **2차 fan-out** (13:33–15:22 KST): 부분 성공
  - A/B/F successfully completed via redispatch
    - A: 5222s wall
    - B: 2721s wall
    - F: 671s wall
  - C/C2/D/E 여전히 crash, `.envbug_no_result_1779542469`
- 비용: 1차 envbug ~$4 estimate + 2차 success ~$2.85 = ~**$6.85**

### Act 4 — 4-axis redispatch (cycle 1, 22:21–23:13 KST)

- C/C2/D/E redispatch with corrected env-var separation
- **D**: 완료, n_strong=0 FAIL, init_CE 14.456, wall 2171s
- **E**: OOM crash, LangBalancedSampler memory leak, ~$1.10 sunk
- **C/C2**: step 625/375 에서 abort
  - **자연실험**: R8c cell-1 head_g byte-equal init_CE 14.4564 to D 관측 → head_g 가설 FALSIFIED
- 비용: ~**$6** (2171+2700+2700+2700 sec × $1.49/3600)

### Act 5 — R8 fork + cluster X/Y/Z 자연실험 finding (현재)

- **R8 fork 개시** (PR #214): 4-candidate spec (R8a / R8b / R8c / R8d)
- **R8c cell-1 FALSIFIED** (이번 turn): C/C2/D byte-equal init_CE proves head_g is NOT the contributor
- **Cluster X/Y/Z classification** (PR #249/#251): init_CE byte-clustered across 7 axes → 3 distinct sources
- R8a (n_kv_head=2 + noise=0) 단일 pod $2.75 = first prio

---

## § Cumulative cost ledger

| item | cost |
|---|---|
| Phase 2 fix | $0.27 |
| Phase 2 full (3B, 7367s × $1.49/3600) | ~$3.05 |
| AXIS_MAP-FAN 1차 envbug (7 pods × ~1hr × $1.49 ÷ ~2 early-fail) | ~$4 (estimate) |
| AXIS_MAP-FAN 2차 success A+B+F (5222+2721+671s × $1.49/3600) | ~$2.85 |
| 4-axis redispatch cycle 1 (D + E + C + C2, ~9000s aggregate × $1.49/3600) | ~$6 |
| **total V3 saga session-3** | **~$16–21** |

honest range: $16 (conservative envbug accounting) ~ $21 (high estimate, includes failed-pod sunk cost).

---

## § 11 PRs landed (HEXAD/PURE scope)

| PR# | branch / topic |
|---|---|
| #204 | dispatcher CALLER WARNING — env-var concat anti-pattern doc-only fix |
| #206 | AXIS_MAP_RESULTS partial 3/7 (1차 2차 fan-out 종합) |
| #211 | AXIS_MAP_BUG_POSTMORTEM — env-var-concat shell-trap root cause |
| #214 | R8 spec — 4-candidate fork (R8a/R8b/R8c/R8d) |
| #224 | R8c probe 5-cell |
| #246 | HEXAD/PURE INDEX.md — saga 상위 index |
| #248 | BUG_POSTMORTEM E OOM addendum — LangBalancedSampler leak |
| #249 | AXIS_MAP_RESULTS 5/7+2 update — cluster X/Y/Z 발견 시작 |
| #250 | R8c probe 3-cell update |
| #251 | R8 cluster X/Y/Z update — natural-experiment FALSIFICATION |

cross-PR pattern: doc-only safety patches (#204) ↔ result-table consolidation (#206/#249) ↔ postmortem (#211/#248) ↔ spec fork (#214) ↔ probe (#224/#250) ↔ classification (#251).

---

## § 3 cluster discovery (init_CE byte-cluster table)

| cluster | init_CE (representative) | axes | suspect source |
|---|---|---|---|
| X | 14.4564 | C, C2, D | shared init path (NOT head_g — R8c FALSIFIED) |
| Y | ~14.x (별도 cluster) | E (pre-OOM logged) | sampler-side bias |
| Z | ~14.x (또 다른 cluster) | A/B/F residuals | mitosis_pool / kv-head 후보 |

핵심 관측: random transformer (vocab ~32k) baseline init_CE ≈ log(32000) ≈ **10.37 nats** (uniform).
관측값 14.4564 = uniform + **~4 nats worse** = init 이 적극적으로 anti-uniform mass 를 특정 token 에 집중 → **구조적 bias**.

---

## § Lessons learned (3 distilled)

### 1. caller-side env-var concat 은 shell-trap, framework bug 아님

env-var-concat 1차/2차 fan-out 실패의 root cause 는 dispatcher 코드가 아니라 caller-side shell assignment 의 인접 concat. 수정은 **doc-only CALLER WARNING (PR #204)** — dispatcher 코드 변경 없음. shell semantics 의 trap 을 코드로 막을 수 없을 때는 caller 측 명시적 separator 가 답.

### 2. 자연실험 우선 over probe

R8c head_g 가설을 $0.10 probe 대신 **C2 vs D byte-equal natural experiment** 로 FALSIFY 했음.
- C/C2/D 가 같은 init_CE 14.4564 (byte-equal) 을 공유한다는 사실 자체가 head_g 가 컨트리뷰터가 아님을 증명 — C는 head_g 활성, D는 head_g 비활성, 그런데 init_CE 가 byte-equal 이면 head_g 는 무관.
- probe 의 가치는 "untested" 가설에 한정. 이미 다른 fan-out 결과로 byte-equal 이 잡힐 수 있는 가설은 free natural experiment 로 처리.

### 3. worse-than-random init_CE 14+ 는 구조적 bias

random transformer = uniform baseline ≈ 10.37 nats. 관측값 14.4564 = +4 nats worse than uniform = init 이 **적극적으로 anti-uniform** = mass 가 특정 token 으로 집중.
후보:
- **noise injection** (Engine-G repulsion noise term)
- **n_kv_head repeat** (GQA repeat pattern bias)
- **mitosis_pool** (cell-pool init 비대칭)

이 중 하나 또는 조합이 suspect. R8a (n_kv_head=2 + noise=0) 가 둘 동시에 ablate 하므로 first prio.

---

## § Open path forward

| priority | action | cost | gate |
|---|---|---|---|
| 1 | R8a fire (n_kv_head=2 + noise=0 single pod) | $2.75 | init_CE 14+ ablation |
| 2 | R8b LoRA-on-Qwen fallback | $5–8 | R8a FAIL 시 |
| 3 | R8c probe (ablation isolation) | $0.25 | R8a 가 ablation isolation 필요할 때만 |

기본 가설: R8a 가 init_CE 를 10.37 baseline 으로 끌어내리면 noise + kv-head 둘 다 또는 둘 중 하나가 suspect 확정.
R8a 가 여전히 14+ 면 mitosis_pool 단독 suspect → 별도 ablation cycle.

---

## § Honest caveats

- ko STRONG 19 (Phase 2 fix) ≠ multilingual V3 success. 단일축 결과로 V3 의 multilingual generalization 은 증명되지 않음.
- init_CE 14+ 천장이 풀려야 진정한 V3 path 가 열림. 현재까지의 모든 axis 가 같은 ceiling 에 막혀있을 가능성.
- session-3 의 V3 closure 는 **잠정적** — R8 fork 결과로 재평가. 정식 closure 는 R8a/b 결과 후.
- envbug saga 의 $4 estimate 는 정확한 per-pod billing 미회수, 보수적 추정.
- cluster X/Y/Z 의 X 만 R8c 로 head_g FALSIFIED 확정. Y/Z 는 미확정 cluster.

---

## § Cross-reference

PR #204 · #206 · #211 · #214 · #224 · #246 · #248 · #249 · #250 · #251

prior session SSOT: `HEXAD/PURE/AXIS_MAP_BUG_POSTMORTEM_E_OOM_ADDENDUM_2026_05_23.md` · `HEXAD/AXIS_MAP.md` · `HEXAD/HEXAD_NATIVE_V3.md`

next milestone: R8a fire 결과 (gate for true V3 path open / final closure 결정).
