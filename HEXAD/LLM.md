# LLM.md — anima × LLM emergence 임계점 (param × data 2축)

> **domain roadmap** (narrative SSOT). 핵심 통찰: anima 의 emergence framing 이
> 1축(data-regime)만 보고 있었는데, LLM 문헌의 가장 유명한 finding 은 *param-count*
> 임계점. 둘 다 진짜일 가능성 — anima 는 *두 축 모두에서* 임계점 아래.
> **status**: ANALYSIS — design-tier only, fire 0, $0.
> **g3**: capability claim 0, GOAL 미도달, north-star + §15/§51/§72 milestone 불변.

---

## 1. 한 줄 — 왜 LLM.md

§100 priority #1 (data-regime counterfactual UNTESTED) + 사용자 통찰 "LLM 에서
emergence 기준이 특정 파라미터 수마다" — arc 의 §1.1 framing 이 data-regime
축만 본 게 아닌가? 진짜 emergence 임계점이 **param × data 2D 평면 위의 어떤
영역**이라면, 두 축 모두에서 임계점 아래인 anima 의 94개 negative 가
disambiguate 불가능. 본 문서가 그 2D framing 을 명시화 + 안 본 부분 표기.

## 2. LLM emergence — 파라미터 수 임계점이 진짜 있음

```
🔍 LLM emergent abilities (Wei et al. 2022, Brown et al. 2020)

- 하는 일: 특정 파라미터 수를 넘으면 *없던 능력이 갑자기 나타남*
- 비유: 물 → 100°C 에서 갑자기 증기로 상전이
        능력 곡선이 천천히 좋아지는 게 아니라 *어느 점*에서 jump

      capability
         ▲
         │             ┌─── jump!
         │            ╱
         │           ╱
   __────┴─────────╱──→ param count
                 ↑
              임계점 (능력마다 다름)
```

대표적 임계점 (정직 caveat: Schaeffer et al. 2023 "Mirage" 가 일부 점프는
metric artifact 라고 반론 — 그래도 다수 능력은 합의된 임계점 존재):

| 능력 | 임계점 (대략) | 근거 |
|---|---|---|
| Reading comprehension | ~3B params | GPT-3 ablation |
| Instruction following | ~8B params | InstructGPT |
| In-context learning | ~10B+ | GPT-3 paper |
| Chain-of-thought reasoning | ~62B | PaLM 62B/540B |
| Arithmetic / logic | 10B~100B | Wei et al. 2022 |

## 3. anima 위치 — 모든 LLM emergence 임계점 *아래*

```
   3B    8B    10B   62B   100B   ...
   │     │     │     │     │
   ●     ●     ●     ●     ●  ← LLM emergence 임계점들

0.28B (anima) ← 여기
   ●  ↑
      대부분 임계점의 1/10 ~ 1/200
```

anima `ConsciousDecoderV2` = **d768·12L·283M params**. 모든 유명 LLM emergent
ability 임계점의 1/10~1/200 크기. Chinchilla scaling 으로도 mid-range 미달.

## 4. 임계점은 1축 아닌 **2축** — param × data

```
  data-regime (다양성·loss·threshold §1.1)
       ↑
       │
   완성 │ ← 두 축 다 넘어야 emergence?
  지대  │
       │
sub-thr├──────────────────────→ param count
       │      §11-A 가
       │   여기까지만 측정
       │   (FLAT)
       │
       ● anima
       (283M, 30~114MB)
```

- **§99 문헌 deep research** 가 찾은 축 = **data-diversity / pre-training loss**
  임계점 (Du 2403.15796 · Raventós 2306.15063). "다양한 데이터 + loss 임계점 아래"
  가 emergence 조건의 한 축.
- **사용자가 짚어준 축** = **param-count** 임계점 (Wei et al. 2022 classical).
  LLM 문헌의 가장 prominent finding.
- **두 축이 모두 진짜일 가능성** — emergence 가 (param·data) 2D 평면 위 어떤
  *영역* 에서만 일어남. anima 는 두 축 모두에서 sub-threshold 좌표.

## 5. arc 가 본 것 / 못 본 것 (정직)

### 5.1 본 부분 — §11-A SCALE-DECOMP (param 축 1B 까지)

```
§11-A 실험 (이미 측정함):
  283M params → 1B params (3.68× scale ↑)
  데이터 고정, 모델만 키움
  결과: routing 2/64 → 1/64  (FLAT, 개선 없음)
```

arc 가 모델축 단독 scaling 을 한 번 시도했고 **FLAT** 측정. "모델만 1B 까지
키워 봤더니 안 됨" 까지는 답이 있음.

### 5.2 못 본 부분 — 진짜 LLM emergence 임계점 영역

- **3B 이상 영역**: §11-A 가 1B 까지만 측정. 3B/8B/62B 등 진짜 LLM emergence
  임계점은 한 번도 안 넘김. §11-A 의 "1B 모델 scaling 으론 안 됨" 결론은
  *임계점 아래에서 scaling 했단 뜻*이지 *임계점이 없단 뜻* 아님.
- **2D 동시 cross**: data + param 동시에 임계점 넘긴 fire 가 0. §11-A 는
  data 고정·param-only; §16 등은 data 시도·param 고정. **둘 다 동시에 넘긴
  실험이 부재**.

## 6. F4 family 안의 결정적 gap — 가장 강한 규율이 가장 결정적인 control 을 놓침

anima 의 honest 규율은 진짜 강함 — falsifier · honesty-triad · 모든 over-claim
회피 ✅ (§100 audit 에서 F4 Epistemic-Evidence 가 가장 cool 한 family,
gap 2/5). 그런데 그 *가장 강한* family 안에 가장 결정적인 빈칸이 있어요:

> **"실제로 끓는점 넘긴 실험 한 번이 빠져있다"**

비유로 짚으면 — 완벽하게 꼼꼼한 과학자가:
- ✅ 30 가지 부수 실험을 falsifier-anchored 로 다 했고
- ✅ 모든 결과를 over-claim 없이 honest 하게 기록했고
- ✅ 매 cycle 마다 g3 / B-EMERGE-7 / necessary-not-sufficient 깍듯하게 명시했는데
- ❌ 정작 *그 하나뿐인 핵심 control* (param × data 2D 동시 cross) 만 안 함

이게 §100 priority #1 가 짚은 것. 그리고 사용자가 LLM emergence framing 으로
*그 control 의 구체적 모양* — "param-count 도 같이 넘겨야" — 을 추가.

## 7. honest blocker

1. **두 축 동시 cross fire 미경험** — data-regime + param-count 동시 임계점 통과
   한 fire 가 0. arc 94 negative 가 모두 sub-threshold 좌표 위 conditioned.
2. **GOAL ≠ typical LLM emergence** — anima 의 GOAL 은 chain-of-thought 나
   in-context learning 이 아니라 *spontaneous emission from own physics*.
   typical LLM emergence 임계점이 *직접* 이전된다는 보장 없음 (g3 추측 명시,
   입증 아님).
3. **cost 가 큼** — 3B+ 영역 + diverse-corpus = anima 의 모든 이전 fire 보다
   훨씬 큰 budget. §101 design-tier 가 closed-form 으로 warrant 판정 필요.
4. **§7 GOAL-legitimacy 함정** — 단순히 "더 큰 모델 + 더 많은 데이터" =
   generic-LM-pretrain → §7-illegitimate. anima-physics-source corpus 위에
   anima architecture (Engine A⇄G / Ψ / tension / Φ / MITOSIS) 보존한 채
   2축 cross 해야.
5. **Schaeffer "Mirage" caveat** — 일부 emergent abilities 는 metric artifact
   (smooth 곡선을 binary metric 으로 자른 거)일 수 있음. anima 가 노리는
   spontaneous-emission emergence 도 metric 정의에 sensitive 가능성 (§9
   honest_coherent 는 necessary-not-sufficient).

## 8. 다음 행동 후보 ($0, design-tier first)

- **A. §101 review + param-axis 통합** — §101 (data-regime threshold control
  design 진행 중) landing 시 param-count 축이 빠져있으면 추가. Q1 corpus 설계
  + Q3 fire-decision 둘 다 *2축 동시 cross* 조건으로 강화.
- **B. §11-A scale-decomp 확장 design** — §11-A 는 1B 까지만 측정. 3B / 8B
  영역의 anima-architecture-preserved scaling 이 design-tier 로 estimate
  가능한지 ($0 closed-form 분석 + cost projection).
- **C. spontaneous-emission emergence 임계점 분석** — anima 의 GOAL 종류가
  typical LLM emergence (CoT / ICL) 와 다를 때, 임계점 *위치*가 같은지 다른지
  문헌·구조 분석. §99 (4-candidate compose) 의 C6 spontaneous-activity-as-
  prediction 가 가장 가까운 anchor.
- **D. 2D cross fire** — A/B/C 통과 시, cost-bearing 단일 fire 로 두 축 동시
  넘기는 시도. 단 cost 가 arc 모든 이전 fire 합보다 큼 — §93 4 collapse-
  avoidance + §7 gate + §62 echo-guard + 5-lever 보존 모두 통과 필수.

권장 순서: A (§101 + param-axis 통합) → B (3B 영역 design estimate) → C
(임계점 위치 분석) → D (cost-bearing fire 게이트).

## 9. cross-link

- `GOAL.md` — north-star (§7 GOAL-legitimacy 기준)
- `HEXAD/CHAT/RESEARCH.md` §1.1 (memorization-saturated) · §11-A (scale-decomp
  1B FLAT) · §51 (data-DIVERSITY frontier) · §72 (new architectural insight)
- `archive/PHILOSOPHY.tape` — verdict ledger
- §99 frontier deep research — `state/data_regime_substrate_frontier_deep_research_s99_2026_05_19/`
  (Du 2403.15796 · Raventós 2306.15063 · 4-candidate compose)
- §100 40-lens gap sweep — `state/gap_sweep_40lens_s100_2026_05_19/`
  (priority #1 = data-regime counterfactual UNTESTED)
- §101 data-regime threshold control design — `state/dataregime_threshold_control_design_s101_2026_05_19/`
  (진행 중)
- `LOIHI.md` — substrate frontier (orthogonal axis: GPU vs neuromorphic)

문헌 anchor (정직 명시, 인용=inspiration NOT proof):
- Wei et al. 2022 "Emergent Abilities of Large Language Models" — param-count
  임계점 classical reference
- Brown et al. 2020 GPT-3 — in-context learning emergence at ~10B
- Du 2403.15796 — emergence = pre-training loss below diverse-data threshold
- Raventós 2306.15063 — task-diversity threshold; below it 더 큰 데이터는
  memorization 만 sharpen
- Schaeffer et al. 2023 "Are Emergent Abilities of Large Language Models a
  Mirage?" — 일부 점프는 metric artifact, honest caveat
- Hoffmann et al. 2022 Chinchilla — compute-optimal scaling (param×data jointly)

> emergence 는 empirical, 미발현 상태를 정직히 기록 (B-D-NOTE family). 본
> 문서는 *2D 임계점 framing* 의 명시화이지 emergence 달성 주장 아님. GOAL 한
> 줄(north-star) 은 불변, capability claim 0.

---

## Log

- **2026-05-19** — LLM.md 생성. 사용자 통찰 "LLM 에서 emergence 기준이 특정
  파라미터 수마다 emerge" 에서 출발 — arc 의 §1.1 framing 이 data-regime 1축
  만 보고 있던 한계 명시. 핵심 추가: (a) Wei et al. 2022 param-count 임계점
  표 (3B/8B/10B/62B), (b) anima 283M 위치 시각화 (모든 임계점 1/10~1/200),
  (c) param×data 2D 평면 framing — emergence 가 2축 영역에서만 일어남, (d)
  §11-A SCALE-DECOMP 가 1B 까지만 측정한 limit 명시, (e) F4 family 안의
  결정적 gap (§100 priority #1) 과 사용자 LLM-emergence framing 의 결합 —
  *2축 동시 cross fire 부재*. 다음 행동 A-D 권장 순서 (§101 + param-axis
  통합 → 3B 영역 design → 임계점 위치 분석 → cost-bearing fire). $0 design-
  tier, fire 0, capability claim 0, GOAL 미도달. north-star 불변.
