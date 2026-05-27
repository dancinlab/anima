# HEXAD/PURE — 자연발화 채팅 Phase D · corpus fire (primary goal SSOT)

> **세션 primary goal** — anima 의 자연발화 채팅(substrate-native autonomous-speech
> daemon)은 ~60-70% 완성. 8-factor motivation engine(Phase B)·interaction
> model(Phase C)·sleep/dream 은 LANDED 이나, **그 engine 이 실 corpus 로
> ckpt-bearing retrain 된 적이 한 번도 없다**. 본 문서는 그 마지막 critical-path
> 구멍 — **Phase D corpus fire** — 를 닫는 작업의 SSOT 이다.
>
> anchor — corpus 설계 spec: [`spec/phase_d_corpus_design_2026_05_24.md`](spec/phase_d_corpus_design_2026_05_24.md)
> · Phase B engine: [`../CHAT/spontaneous_lib.hexa`](../CHAT/spontaneous_lib.hexa)
> · sleep/dream: [`../CHAT/server/anima_dream_stage.hexa`](../CHAT/server/anima_dream_stage.hexa)
> · fallback 축 map: [`AXIS_MAP.md`](AXIS_MAP.md)

## § 1. 목표

**Phase D = 8-factor engine(LANDED)을 실 corpus 로 ckpt-bearing fire 하여
substrate-native emit 을 empirical 검증한다.**

지금까지 자연발화는 *closed-form 검증*(B-SPONT-1..7 sympy battery)과
*synthetic substrate*(Phase C blue 83/83)까지만 닫혔다. 진짜 닫히지 않은 것은
**"실 ckpt 가 그 8-factor 입력(relevance·gap·curiosity·pain·coherence·
originality·balance·dynamics)을 받아 자극 없이 자연발화하는가"** 이다. 이는
오직 corpus-bearing retrain 으로만 측정된다. Phase D 가 그 fire 다.

## § 2. 현 완성도 — Phase B/C/sleep LANDED, Phase D = critical-path blocker

| Phase | 산출물 | 상태 | 증거 |
|---|---|---|---|
| **B engine** | `../CHAT/spontaneous_lib.hexa` (8-factor motivation: relevance/gap/curiosity/pain/coherence/originality/balance/dynamics, closed-form, weight-sum-unity) | ✅ **LANDED** | smoke 7/7 PASS · B-SPONT-1..7 |
| **C interaction** | channel_mux + anima_chat_v2 | ✅ **LANDED** | blue 83/83 🔵 |
| **sleep/dream** | `../CHAT/server/anima_dream_stage.hexa` (5-stage Φ-envelope, IPC bridge live, autonomy-reshaped) | ✅ **LANDED** | PR #279/#307 — boolean gate 없음 |
| **D corpus fire** | 8-factor engine 의 실 ckpt-bearing retrain + emit eval | 🔴 **BLOCKER** | **미실행** — engine 은 build 됐으나 실 corpus 로 한 번도 fire 안 됨 |

Phase B/C/sleep 가 모두 LANDED 임에도 자연발화가 ~60-70% 인 이유는 단 하나:
**D 가 critical-path blocker**. engine 은 있으나 weight 가 없다.

## § 3. Track 1 교훈 — register collapse 의 진짜 범인은 M3 repetition

Track 1(본 세션 첫 Phase D fire 시도)은 corpus 축을 직접 sweep 했고 FAIL 했다:

- **E2** (wiki_frac=0.5, anima 50%) → **FAIL**, `ko=PURE_MEMORIZE`
  (register collapse) · `anima_register_hits=4/20` · `register_regress=True`.
- **E3v3** (wiki_frac=1.0) → in progress (wiki_frac endpoint 보강 측정).
- **KEY corpus finding** (corpus_s101 실측, PR #340/#303): anima-OWN corpus
  (~600 MB) 의 **M3 TTR ≈ 0.03** (extreme repetition) + M5 hangul 1.66-2.34%.
  → register-sink 예측자는 **M3 (반복도), NOT M5 (한글 coverage)**.
  S1-prefix carving 템플릿이 high-volume·low-diversity 라 model 이 그
  고-반복 한글 패턴을 통째 암기 → ko=PURE_MEMORIZE.

함의: Phase D 의 다음 fire 는 corpus 를 **더 다양하게(M3 ↑)** 재설계해야
한다. wiki_frac 만 sweep 하던 Track 1 의 한계는 corpus *조성*(반복도)을
건드리지 않은 것 — § 4 의 작업 1(설계 spec)이 그 직접 응답이다.

## § 4. Phase D 작업 분해

- [ ] **새 corpus 설계 spec** — 본 PR File 2:
      [`spec/phase_d_corpus_design_2026_05_24.md`](spec/phase_d_corpus_design_2026_05_24.md).
      M3=0.03 진단 → 도우미 0 · stream 80% · M3 TTR ≥ 0.3 설계 원칙.
- [ ] **corpus build** — 도우미 token 0 (Principle #3 정합) + stream/stimulus
      80% (substrate-native) + M3 diverse 어휘. build 후
      `corpus_quality_probe.hexa` (PR #287) 로 사전 게이트(M3 TTR ≥ 0.3).
- [ ] **ckpt-bearing fire** — 8-factor `spontaneous_lib` 연결, autonomous
      dispatch (per @D a_fire_autonomous, ~$2-6 H100). ckpt-every 500,
      5000 step, mitosis-max 16 권장(R6).
- [ ] **eval** — (a) `multilingual_probe.hexa` (PR #240) register PASS
      (register_hits < 4/20) · (b) 8-factor motivation 실작동(자극 없이 emit)
      · (c) `anima_dream_stage` Φ-envelope 실 ckpt 에서 작동.
      closure criterion (PR #264): 4/5 langs ≥ PARTIAL.

## § 5. Honest C3 (≥3)

1. **Phase D fire 는 cost-bearing (~$2-6) 이고 아직 미실행**. 본 PR 은 goal
   SSOT + corpus 설계까지만 닫는다 — 실 ckpt 증거는 build + fire 후속 cycle.
   E3v3 결과는 wiki_frac endpoint 를 보강할 뿐 Phase D 를 닫지 않는다.
2. **M3 → register-sink 인과는 상관 가설**(corpus_s101 단일 실측 + 단일 metric
   매칭). 새 corpus 가 M3 ≥ 0.3 을 만족해도 register collapse 가 회피된다는
   보장은 fire 전에는 없음 — § 4 작업 3/4 가 그 인과를 calibrate.
3. **"자연발화 실작동"의 측정 정의가 미고정**: 8-factor motivation 이 실 ckpt
   에서 자극 없이 emit 한다는 것을 어떤 falsifier 로 확정할지는 corpus spec
   § 5 에 pre-register 하되, synthetic(Phase C)→real 의 parity 는 fire 후 별도.
4. **AXIS_MAP fallback 과 직교**: Phase D corpus 재설계가 또 FAIL 하면 B 증류 /
   A 커리큘럼 / C head_g (AXIS_MAP) 로 fan out. 본 goal 은 corpus 축을 한 번 더
   (제대로) 시험하는 것이지 corpus 축이 vindicate 됨을 가정하지 않는다.

— 끝 —
