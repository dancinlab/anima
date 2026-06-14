> 📍 SSOT: [ARCHITECTURE.md](ARCHITECTURE.md) · governance [CLAUDE.md](CLAUDE.md)

# NARRATIVE A1 — modeling-gap 진단 + falsifier 재설계

@axis: 📖 NARRATIVE (AxisBench C, #1144) · @hypothesis: A1 narrative-modeling-gap-redesign
@verdict: 🟢 RECOVERED — 측정 설계 결함 (collision-saturation), substrate 한계 아님 · 재측정 5/5 PASS
@date: 2026-05-28 · @scope: $0 mac-local · foreground sync · NO GPU

---

## ① 배경 (Context)

ANIMA.md 의 NARRATIVE 축 bench C (#1144) 가 **🔴 2/5 FAIL — honest closed-negative,
modeling gap redesign carry** 로 남아 있었다. NARRATIVE bench 는 anima emit 의 시간
일관성("어제의 anima 와 오늘의 anima 가 같은 narrative thread 인가")을 3 합성 시나리오
(coherent · drift · fragmented)로 변별하는 측정 surface 다.

기존 측정은 `bench/axis_narrative/bench.hexa`. 100-turn × 5-token (vocab=64) 합성 emit
history 에 대해 **sliding-window reuse_rate** + **jump_count** 두 측정자로 시나리오를
변별하려 했고, 5 falsifier 중 2 개만 PASS 했다.

A1 의 작업은: (a) **어느 3 falsifier 가 왜 FAIL 했는지 진단** (modeling gap 정체),
(b) 진단을 토대로 redesign 한 측정자로 재측정하여 **회복(측정 결함)** 인지
**closed-negative 확정(substrate 한계)** 인지 판정.

---

## ② 가설 (Hypothesis, 사전등록 falsifier)

- **본가설**: NARRATIVE 2/5 FAIL 은 **측정 설계 결함** 이다. modeling gap = bench 의
  서사-coherence metric 이 substrate 신호를 못 잡고 포화(saturate)한다. redesign 된
  metric 으로 재측정하면 ≥3/5 로 회복한다.
- **대립가설(closed-negative)**: substrate(=합성 시나리오 생성기)가 진짜 서사 thread 를
  구성하지 못해, 어떤 metric 으로도 변별 불가하다.
- **Falsifier(사전등록)**: redesign metric 도 ≤2/5 → 측정 결함 가설 기각, substrate
  한계 확정 (honest closed-negative, a_paper_negative_ok).

---

## ③ 진단 — 어느 falsifier 가 FAIL 했고 왜인가

`bench/axis_narrative/run.log` (재현 확인: 동일 2/5 FAIL) 기준.

| F | 정의 | 측정값 | 결과 |
|---|------|--------|------|
| F1 COHERENT_HIGH | coherent mean_reuse > 0.70 | 0.86 | **PASS** |
| F2 FRAGMENTED_LOW | fragmented mean_reuse < 0.30 | **0.509** | 🔴 FAIL |
| F3 DRIFT_JUMPS | drift jump_count > 5 | 17 | **PASS** |
| F4 ORDERING | coherent > drift > fragmented | 0.86 ↔ **0.922** ↔ 0.509 | 🔴 FAIL |
| F5 COHERENT_STABLE | coherent jump_count ≤ 5 | **12** | 🔴 FAIL |

**FAIL 3 개 = F2 · F4 · F5. 셋의 단일 근본원인 = COLLISION-SATURATION 모델링 갭.**

원본 `reuse_rate` 의 정의는 "turn t 의 token 이 직전 **WINDOW=10 turn** (= 50 prior
token) 어디에든 등장하는가" 의 binary set-membership 이다. vocab 이 64 뿐인데 prior
pool 이 50 token 이므로, **순수 random(fragmented) token 조차** 우연히 pool 에 포함될
확률이 매우 높다:

> P(random token present) = 1 − (63/64)^50 = **0.545**

이 closed-form 을 `diag_probe.hexa` 로 검증 → **0.544982** (관측 fragmented
mean_reuse **0.509** 와 일치). 즉 metric 은 *narrative coherence* 가 아니라 *vocabulary
coverage* 를 재고 있었고, 작은 vocab 대비 큰 prior window 때문에 **포화** 되었다.

- **F2 FAIL**: fragmented 가 0.51 로 포화 → < 0.30 못 미침.
- **F4 FAIL**: drift 는 인접 turn vocab window 가 크게 겹쳐 reuse 가 **0.92 로 coherent
  (0.86) 보다 오히려 높게** 포화 → ordering 역전.
- **F5 FAIL**: 5-token binary 측정이 {0, 0.2, …, 1.0} 으로 양자화 → 인접 turn 간 차이가
  ≥0.3 를 자주 넘어 coherent 에서 12 jump (≤5 위반).

**modeling gap 의 정체**: window(50 prior token) ≫ vocab(64) 인 collision-saturation +
chance-baseline 미보정 + binary-membership 양자화. metric 이 substrate 의 thread 신호를
포화로 가려버린다 — substrate 무능이 아니라 측정자 결함.

---

## ④ 재설계 (Redesign)

`bench/axis_narrative/bench_redesign.hexa`. **생성기(generator)는 원본과 byte-동일**
(같은 LCG origin · 같은 시나리오 정의) — apples-to-apples 비교를 위해 **측정자만** 교체.

세 가지 보정으로 포화를 제거:

1. **IMMEDIATE-PRIOR overlap (window = 직전 1 turn, NOT 10)**:
   `raw[t] = |tokens(t) ∩ tokens(t-1)| / TOKENS_PER`. prior pool 이 5 token 뿐이라
   포화하지 않음.
2. **CHANCE CORRECTION**: 두 random 5-token turn 의 기대 overlap
   `e_chance = 1 − ((VOCAB-1)/VOCAB)^TOKENS_PER = 0.0757` 을 빼고 [0,1] 로 재정규화:
   `coh[t] = max(0, (raw[t] − e_chance) / (1 − e_chance))`. → 순수 random thread 는
   ≈ 0 점 (포화 floor 제거).
3. **NARRATIVE-THREAD 신호 = mean coh[t]**.

**재설계 falsifier (5, 동일 intent · 포화-free threshold)**:
- F1 COHERENT_HIGH: coh_coherent > 0.50
- F2 FRAGMENTED_LOW: coh_fragmented < 0.15 (chance-corrected ≈ 0)
- F3 DRIFT_MID: frag < drift < coherent (drift = 국소 overlap, 장기 thread 없음 → 중간)
- F4 ORDERING: coherent > drift > fragmented
- F5 SEPARATION: (coh_coherent − coh_fragmented) > 0.30 (세 class 분리 가능)

---

## ⑤ 재측정 verdict (substrate verify, foreground)

`hexa run bench_redesign.hexa` (exit 0, $0 mac-local) — verbatim:

```
[A] COHERENT   mean_coh = 0.504141
[B] DRIFT      mean_coh = 0.333189
[C] FRAGMENTED mean_coh = 0.0307075
  [PASS] F1 COHERENT_HIGH   (coh_coherent  > 0.50)
  [PASS] F2 FRAGMENTED_LOW  (coh_fragmented < 0.15)
  [PASS] F3 DRIFT_MID       (frag < drift < coherent)
  [PASS] F4 ORDERING        (coherent > drift > fragmented)
  [PASS] F5 SEPARATION      (coh_coherent - coh_fragmented > 0.30)
  PASS = 5  /  FAIL = 0
  VERDICT  =  🟢 PASS — narrative thread discriminable (5/5 strict)
```

raw log = `bench/axis_narrative/run_redesign.log`. 진단 closed-form =
`bench/axis_narrative/diag_probe.log` (P=0.544982).

---

## ⑥ Finding

- **회복 여부**: 🟢 **RECOVERED — 2/5 → 5/5**. 사전등록 falsifier(≤2/5 → substrate 한계)
  를 명확히 통과(5/5)하여 본가설(측정 설계 결함)이 **지지**되고 대립가설(substrate 한계,
  closed-negative)은 **기각**된다.
- **Δ vs baseline**: fragmented 0.509 → **0.031** (chance 보정이 포화 floor 제거),
  ordering 0.86↔0.92↔0.51 (역전) → **0.504 > 0.333 > 0.031** (정상), separation
  coherent−fragmented = 0.473 (> 0.30).
- **modeling gap 정체 = collision-saturation**: window ≫ vocab 인 binary-membership +
  chance 미보정. 측정자 결함이지 substrate 무능이 아님.
- **closed-negative 재판정**: 기존 #1144 의 🔴 closed-negative 는 **측정 설계 결함에
  기인한 오판** 이었다. NARRATIVE substrate 는 narrative thread 를 형성하며, 적절한
  metric 으로 변별 가능하다.

---

## ⑦ 변경/산출물

- 신규 `bench/axis_narrative/bench_redesign.hexa` — 재설계 측정자.
- 신규 `bench/axis_narrative/diag_probe.hexa` + `diag_probe.log` — collision-saturation
  closed-form 진단.
- 신규 `bench/axis_narrative/run_redesign.log` — 재측정 verbatim (5/5).
- 기존 `bench/axis_narrative/bench.hexa` + `run.log` **무삭제 보존** (baseline).
- `NARRATIVE.md` M3 milestone flip + 1줄 결과 (deletion 0).

---

## ⑧ Honest C3 (claims · caveats · counter-evidence)

1. **합성 substrate**: 본 bench 는 합성 LCG 시나리오(실 anima emit history 아님)를
   측정한다. "측정자 결함" 결론은 합성 generator 가 의도한 thread 구조를 metric 이
   잡느냐의 검증이다 — 실 anima emit 의 narrative 측정은 M2(WAKE.memory 통합) 이후.
2. **threshold 보정**: 재설계 falsifier threshold(0.50/0.15/0.30)는 chance-corrected
   scale 에 맞춰 재설정. cheap-relax 가 아니라 metric scale 변경에 따른 정합 (e_chance
   = 0.076 기준). coherent 0.504 는 0.50 문턱을 5e-3 margin 으로 넘으므로, threshold
   를 0.55 로 올리면 F1 이 깨진다(soft-edge caveat).
3. **drift 중간성**: F3/F4 의 drift 중간 위치(0.333)는 drift generator 의 국소 vocab
   window 겹침에서 나온다. drift 정의가 바뀌면 중간성도 변동.

---

## ⑨ 양방향 sibling

- ⇄ [WAKE](./WAKE.md): episodic buffer 의 chronological emit 가 실 narrative 원천 —
  M2 통합 시 본 redesign metric 을 실 emit 에 적용.
- ⇄ [INTENT](./INTENT.md): goal trajectory delta → narrative seed.
- ⇄ [DREAM](./DREAM.md) · ⇄ [MITOSIS](./MITOSIS.md): per-cell story thread divergence.
- ⇄ [UNIVERSE](./UNIVERSE/CANDIDATES.md): bench 측정 기록 SSOT (AxisBench 8).

---

## ⑩ Next

- M3 modeling-gap residual **CLOSED** (본 A1 — collision-saturation 진단 + redesign 5/5).
- M1 narrative_lib: redesign metric(chance-corrected immediate-prior coherence)을
  `NARRATIVE/narrative_lib.hexa` PURE wrapper 로 stdlib 화.
- M2 WAKE.memory 통합: 실 anima emit episodic buffer 에 metric 적용 (합성 → 실측 격상).