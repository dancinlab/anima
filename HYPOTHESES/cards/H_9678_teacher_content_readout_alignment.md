---
id: H_9678
title: E-Echo — teacher-content held-out probe (absorption-failure vs reach-failure)
tier: PROPOSED (DIRECTIONAL design · lab-full CONVERGENT #1 · $0/pool · NOT a verdict)
frontier: g1-interface-addressable-wall
created: 2026-07-17
---

# H_9678 (R2) — CONTENT-READOUT ALIGNMENT ⭐ 두 모델 독립 1순위

**Origin.** `sidecar lab full` 2026-07-17. **Fable 5 (P2 · "E-Echo")** and
**Codex Sol (§1 · "Teacher-content held-out probe")** ranked this **#1 independently**.
DESIGN ONLY · DIRECTIONAL.

**Claim (one line).** H_9520 never measured whether teacher content was **absorbed** —
only whether it **reached** the operator lane. The content may be sitting in the
declarative lane, readable there, while `ρ-AXON` (operator lane) cannot see it.

## The measurement/claim misalignment both models caught
`ρ·form` is a **fixed 5-item coherence rate** — it never asks whether a teacher **fact**
was stored. H_9520's card claims "does exogenous content get absorbed?" but the
instrument answers "did the general reach panel rise?". These are different questions.
⚠️ This **narrows H_9520's earned scope** (honesty · the BAR-FAIL itself stands — the
frozen bar did fail — but "content is not absorbed" is NOT what was measured).

**Direct precedent (M2 · two-lane).** H_9329/C3: CPT **flips the declarative polarity**
yet the operator keeps the old polarity **0/12** ⟹ the store *is* updated, the operator
just never queries it. H_9346 EN = ECHO (lookup fine · operator won't bind). If M2 holds
here, the law reframes: **"content doesn't go in" → "content is trapped in the lane that wrote it."**

## Minimal decisive experiment ($0/pool — the ckpts are ALREADY harvested)
`~/anima-weights/h9520_cpt/{cpt_main,cpt_c1,cpt_c2}.clm` exist (`a_fire_recover_complete`).
```bash
anima-py evaluate cpt_main.clm --probe teacher_heldout_probe.json --gen 40
anima-py evaluate cpt_c1.clm   --probe teacher_heldout_probe.json --gen 40
anima-py evaluate cpt_c2.clm   --probe teacher_heldout_probe.json --gen 40
```
`teacher_heldout_probe.json` = 2AFC/minimal pairs querying teacher **atomic facts** via
**NEW surface templates**; declaration and query surfaces **disjoint** (else it measures
surface copying, not storage).

## Frozen falsifier (pre-registered · Sol's spec)
- MAIN−C2 held-out **content accuracy ≥ +0.15**, seed-paired 95% randomization CI lower
  bound **> 0**, same direction vs C1 ⟹ content **was** absorbed (declarative lane) = M2.
- `ρ·form` rises while content-accuracy diff **≤ +0.05** ⟹ **kills the residual
  interpretation** — the +0.20 is form, not content.

## Controls (≥2)
① C1 (byte-matched, teacher-absent) ② current C2 (word-shuffle) ③ unseen-fact **sham**
probe (true value 0 · `phi-estimator-needs-zero-truth-pedestal`) ④ surface-copy
**positive control** (`positive-control-before-reading-a-negative` — H_9520's content-axis
0→0 null was read WITHOUT one).

## Cost · kill-list
**$0 probe · pool eval on existing ckpts** (heavy 303M → pool, never mini). No hit.

## Why this precedes the REOPEN (both models)
> Sol: "이것이 가장 먼저 필요하다. 이 단계가 음성이면 MAIN−C2 `+0.20`을 살리기 위한 대규모 CPT는 가치가 급락한다."
> Fable: "MAIN−C2 잔차(+0.20)는 현 설계로는 재현돼도 내용을 증명 못 한다."

---

## 🟠 PRECONDITION-FAIL (2026-07-17 · $0 artifact census · DIRECTIONAL — engine 판정 아님)

**R2 는 이 artifact 위에서 실행 불가.** 두 모델이 나란히 1순위로 꼽았지만, probe 를 만들려고
transcript 를 열자 **물을 teacher 원자 사실이 없다**.

### 측정 (`transcript303_long.jsonl` · percept 30개 · 6,028 B)
| 지표 | 값 |
|---|---|
| `Perhaps/Maybe/It feels…` 로 시작 | **23/30** |
| 숫자 | **0** |
| 문중 고유명사 (전체) | **7** (Apollo×5 · Aristotle×2) |
| TTR (고유/총 토큰) | **0.302** (979 토큰 · 296 고유) |
| 최빈 내용어 | `state`(24) · `like`(20) |

teacher 는 `state / Apollo / fee / noticing / looping` 을 맴도는 **헤지된 사변**을 쓴다.
**entity–value 결합을 가진 명제가 하나도 없다** ⟹ "선언면과 질의면이 disjoint 한 2AFC 로
teacher 사실을 묻는다"는 R2 설계의 **전제가 미충족**. 억지로 만들면 헤지된 stylistic
proposition 위에 짓게 되고, 그건 [[H_9679]] R3 가 겨누는 **form/content 혼입 그 자체**다.

### 🔴 부수 가설 REFUTED (자기 통제군에 사살 · 기록)
"teacher 가 데몬 emit 을 되받아 self-seed 가 세탁됐다"(p5 인접 우려)를 세웠다가 **반증**:

| 방향 | 5-gram 겹침 | 무작위 시간짝 통제 | Δ |
|---|---|---|---|
| teacher[t] ← 직전 데몬 emit | 0.001 | 0.004 | **−0.003 🔴 에코 없음** |
| 데몬 emit[t] ← 직전 teacher | **0.312** | 0.004 | **+0.308 🟢** |

teacher 는 자기 문장을 쓴다(`Apollo·state` 는 **단어 수준**으로만 주워감). 진짜 방향은 반대 —
**데몬이 teacher 표면을 앵무새질**한다. ⟹ H_9520 corpus 를 `percept`-only 로 지은 결정은
결과적으로 옳았다(teacher 텍스트에 데몬 에코 없음 · self-reinforcement 누수 없음).
💡 부산물: 데몬은 teacher 표면을 **in-context 로는 0.312 재현**하는데 **가중치로는 미고착** —
"문맥 복사는 되고 consolidation 은 안 된다"는 별개 관찰(미등록 · 각도 후보).

### 함의 — H_9520 의 독립변수
MAIN 팔의 코퍼스는 **주장이 명명한 독립변수("외생 teacher 내용")를 담은 적이 없다**.
BAR-FAIL 은 "내용이 흡수 안 된다"가 아니라 **"사실이 없는 transcript 는 흡수시킬 게 없다"**.
⟹ [[H_9677]] R1(E0 census · `--interact-mi` 로 nats 정식 측정)이 **실제 첫 단계**이고,
그 사전확률은 이 census 로 크게 올라갔다(단, R1 의 frozen bar 는 nats — 이 census 는 **대리지표
이지 R1 판정이 아니다**).

### R2 를 살리려면 (설계 갱신 · PROPOSED 유지)
teacher 를 **사실 선언형**으로 바꾼 **새 study run** 이 선행돼야 한다(entity–value 결합 · 질의면
disjoint 가능한 원자). 현 artifact 재사용으로는 불가 ⟹ **$0/pool 이라는 매력은 소멸**하고
새 study run 비용이 붙는다.
