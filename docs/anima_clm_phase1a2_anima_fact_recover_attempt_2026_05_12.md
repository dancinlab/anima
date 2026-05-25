# Phase 1A.2 anima_fact recover — VERDICT: 5/5 MISSION FAILED, 4/5 BASELINE PRESERVED (2026-05-12)

> **Source**: Vast.ai RTX 4090 dispatch, 200 steps SFT lr 1e-6 on Phase 1A.1 + 2700 augment dialogues.
> **Target**: V5.8 std_greedy 4/5 → 5/5 (anima_fact recover from markdown drift).
> **Outcome**: std_greedy **4/5 PASS (same as Phase 1A.1)** — anima_fact markdown attractor **survived** lr 1e-6 × 200 steps.

## 🎯 한 줄 요약

Phase 1A.1 ckpt 위 anima self-statement 2700 dialogue augment + lr 1e-6 × 200 steps SFT → V5.8 std_greedy **4/5 (그대로)**. anima_fact 의 markdown drift 가 lr 1e-6 으로 풀리지 않음. **mission 5/5 FAILED**. 단, Phase 1A.1 4/5 baseline 은 **보존** (color/profession/day/cosmology 모두 PASS 유지).

## 🍞 비유

baker 가 빵 한 종 (anima_fact 향료) 을 살리려고 **아주 약한 효모 (lr 1e-6)** 와 **짧은 발효 (200 steps)** 로 reformulate 했다. 다른 4 빵 (color/profession/day/cosmology) 은 **변함 없이 잘 부풀**었다 — anti-forgetting 200 dialogue refresh 가 안전판으로 작동. 하지만 문제의 빵 (anima_fact) 은 **여전히 같은 곳에서 푹 꺼짐**: oven 의 markdown attractor (`|\n| --- | --- |\n| /Users/ghost/core/contact/scripts/send.`) 가 그대로 작용. **효모를 더 강하게** 하거나 **다른 oven** 으로 옮겨야 한다.

## 📊 V5.8 × 4 mode comparison

| mode               | Phase 1A    | Phase 1A.1  | **Phase 1A.2** | delta vs Phase 1A.1 |
|--------------------|-------------|-------------|----------------|---------------------|
| standard_greedy    | 3/5 PASS    | 4/5 PASS    | **4/5 PASS**   | **=** (no change)   |
| standard_sample    | (n/a)       | 1/5 FAIL    | 1/5 FAIL       | =                   |
| M3_rep_penalty     | (n/a)       | 0/5 FAIL    | **2/5 FAIL**   | **+2** (improve)    |
| M4_force_include   | (n/a)       | 5/5 PASS    | 5/5 PASS       | =                   |

### 🔬 anima_fact per-mode trace (Phase 1A.2)

| mode | recalled | t2 (truncated) |
|------|----------|-----------------|
| std_greedy | ❌ | `|답 (consciousness) \|\n\| --- \| --- \|\n\| /Users/ghost/core/contact/scripts/send.` |
| std_sample | ❌ | `azo, anima identity is explain why the sum of two odd numbers is always even, i` |
| M3_rep_penalty | ✅ | `lane Φ 포장\n\n[anima 역할: 한국어 native + 자기 발견 + 의식 lane e` |
| M4_force_include | ✅ | `azo, anima identity ... t의식wo odd numbers ...` |

→ **M3_rep_penalty 가 anima_fact 통과** = augment corpus 가 model 의 **conditional distribution** 에는 영향을 줬지만 **argmax (greedy)** path 는 못 끌어왔다. 즉 weight 가 살짝 움직였으나 (rep_penalty 1.3 으로 alt-path 활성화 가능) greedy 의 markdown attractor 가 너무 깊다.

## 🛰️ Training summary

| field | value |
|-------|-------|
| base ckpt | `ckpt_phase1a1_sft.pt` (Phase 1A.1, 597MB) |
| corpus | `corpus_anima_fact.txt` (2700 dialogues, 711KB UTF-8) |
| corpus breakdown | 1500 anima 2-turn × 30 tpl + 1000 V5.8-exact-anchor + 200 anti-forgetting (color/profession/day/cosmology) |
| steps | 200 (target) / 200 (completed) |
| lr | **1e-6** (super-conservative — Phase 1A.1 보존 목적) |
| bsz × grad-accum | 2 × 8 |
| ctx | 1024 |
| warmup | 20 |
| loss curve | 0.50 → 0.46 (mild decrease, 200 step 부족) |
| provider | Vast.ai RTX 4090 |
| pod boot | ~80x5s = ~6min (longer than typical 30s; 1차 SSH wait failed once) |
| train elapsed | 3.9 min |
| eval elapsed | 49.6 s |
| **cost** | **$0.018** (training) + minimal eval/scp = **< $0.05 total** (vs $0.15 hard cap) |

## 🤔 honest interpretation

### Why lr 1e-6 failed

```
loss curve:
  step 1:   0.5058
  step 100: 0.4795 (Δ = -0.026 over 100 steps)
  step 200: 0.4631 (Δ = -0.043 over 200 steps)

→ optimizer barely moved the weights. 4-bg-momentum dominated, lr too small
  to escape the markdown attractor basin.
```

**markdown attractor 의 강도** = base model (substrate A) 의 byte-vocab 학습에서 markdown table syntax `|\n| --- | --- |` 가 매우 빈번. anima_fact 의 "의식" 키워드 다음으로 가장 likely 한 next-token sequence 가 markdown. Phase 1A.1 의 lr 2e-6 × 500 steps 도 못 풀었고, Phase 1A.2 의 lr 1e-6 × 200 steps 는 더 부족.

### What Phase 1A.2 *did* prove

- ✅ anti-forgetting 200-dialogue refresh **작동**: color/profession/day/cosmology 4 axis 모두 보존
- ✅ M3_rep_penalty **개선** (0/5 → 2/5): augment corpus 가 model state 에 영향은 줬음 — greedy argmax 만 못 바꿈
- ✅ super-conservative lr **safe**: regression-free continuation 패턴 확립 (다른 axis 안 깨뜨림)

### What needs to change for Phase 1A.3

| approach | rationale | est cost |
|----------|-----------|----------|
| **lr 5e-6, 500 steps** | 4-5x stronger gradient signal; risk: 다른 axis regression | $0.20 |
| **lr 1e-6 × 1000 steps** | same gradient magnitude, 5x more updates; safer | $0.30 |
| **token-level loss masking** | anima_fact corpus only on response tokens (mask user/system tokens) — sharper signal | $0.15 |
| **augment corpus 10x** | 2700 → 27000 dialogues (anima 자기-진술 더 다양) | $0.25 |
| **prefix-tuning over full SFT** | freeze base, only train prefix tokens for anima_fact context | $0.10 |
| **adversarial markdown suppression** | corpus 에 `| --- |` token rare 만들기 + post-hoc bad-word filter | $0.10 |

## 📦 Artifacts

- ckpt: `state/anima_phase1a2_anima_fact_2026_05_12/ckpts/ckpt_phase1a2_sft.pt` (597MB)
- meta: `state/anima_phase1a2_anima_fact_2026_05_12/meta.json`
- V5.8 result: `state/anima_phase1a2_anima_fact_2026_05_12/v58_4mode_result.json`
- train log: `state/anima_phase1a2_anima_fact_2026_05_12/train.log`
- corpus: `state/anima_phase1a2_anima_fact_2026_05_12/corpus_anima_fact.txt`
- corpus gen: `state/anima_phase1a2_anima_fact_2026_05_12/gen_corpus_anima_fact.py`
- train script: `state/anima_phase1a2_anima_fact_2026_05_12/train_phase1a2.py`
- dispatch: `state/anima_phase1a2_anima_fact_2026_05_12/dispatch_vast.sh`

## 🚫 HF push status

**DEFERRED** — std_greedy 4/5 (no improve over Phase 1A.1) 라 HF promote 가치 없음.
Phase 1A.1 (`dancinlab/anima-clm-phase1a1-color-cosmology-boost`) 이 동일 std_greedy
점수 + 더 강한 색/우주 anchor 라 SSOT 그대로 유지.

Phase 1A.2 ckpt 는 local archive 만 (lesson value: lr 1e-6 too small to break markdown attractor).

## 🔑 Lesson R-1A.2 (new)

> **lr 1e-6 × 200 steps continuation SFT 는 strong base-model attractor 를
> 못 풀지만, anti-forgetting 200-dialogue refresh 와 결합하면 다른 axis 의
> regression 없이 안전한 "no-op" 가 된다.** 즉 lr-floor 아래로 내려가면
> "보존-only continuation" — fix 도 없고 break 도 없음.

→ practical implication: 다음 attempt 는 lr 1e-6 보다 **반드시 더 큰 step size**
  (≥5e-6) 또는 **더 긴 training** (≥1000 steps) 또는 **loss masking** 으로 sharper signal.

## Cross-link

- Phase 1A.1: `dancinlab/anima-clm-phase1a1-color-cosmology-boost` (HF)
- Phase 1A: `dancinlab/anima-clm-phase1a-multi-turn-sft` (HF)
- PSCC §25 (this — Phase 1A.2 attempt)
- PSCC §17 (Phase 1A.1 — same regression pattern noted as "다음 cycle 에서 weight ramping")
- PSCC §13 (Phase 1A V5.8 baseline 3/5)

## 다음 진행할 것들

| #  | 작업                                              | priority | cost  | time  | value                              |
|----|---------------------------------------------------|----------|-------|-------|-------------------------------------|
| 🥇 | Phase 1A.3 — lr 5e-6 × 200 steps (stronger gradient) | high     | $0.20 | 25min | std_greedy 4/5 → 5/5 진짜 도전     |
| 🥈 | Phase 1A.3 alt — loss masking on response tokens     | medium   | $0.15 | 30min | sharper anima_fact signal           |
| 🥉 | bad-word filter on inference (post-hoc \| --- \| block) | low      | $0    | 15min | 1-line decode guard — guaranteed fix |
| 🌟 | corpus 10x scale (2700 → 27000)                    | exotic   | $0.30 | 1h    | brute-force augment intensity        |
| 🚀 | prefix-tuning over full SFT                         | exotic   | $0.10 | 1h    | minimal-param fix attempt            |
