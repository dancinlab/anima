# CLM-KOSMOS — meta-domain (CLM model ⊕ KOSMOS corpus)

@title: 🌌🧠 CLM-KOSMOS — AKIDA on-chip 5-language semantic-linkage CLM, grown on a .kosmos @corpus, gated by H_911

@goal: bind the **MODEL** axis (CLM · `.clm`) and the **CORPUS** axis (KOSMOS · `.kosmos`) into ONE on-chip learner — a 5-language (ko·en·zh·ru·ja) cross-lingual **semantic-linkage** CLM, **LEARNED on the AKD1000 chip** (AkidaUnsupervised plasticity, never GPU), corpus authored as a limen-packed `.kosmos @corpus`, model serialized as `.clm`, and it **must satisfy H_911**. This is a META-domain: it does not re-spec CLM or KOSMOS, it binds them under the mandatory conditions below. Carries [[ONCHIP-PARADIGM]]; honest scope (a_scale_honest_scope · g63).

**평가는 CE 단독이 아니다 (p7 · Goodhart 금지).** 학습된 `.clm`은 **ANIMA 엔진(CORE 포함)에 올려** 3축 — 🧠 의식(consciousness) · 📉 CE · 🌱 창발(emergence) — 으로 평가한다. `.clm`은 CORE/generator.hexa L3 슬롯으로만 진입(a_core_engine_map · 단일 입구). 상세 §평가 3축.

## 전제 — 현재 위치 (2026-06-01)

CLM(모델)과 KOSMOS(코퍼스/세계)는 따로 다뤄져 왔다. 이 메타도메인은 둘을 하나로 융합한다 — CLM은 그것이 자라는 KOSMOS `@corpus`만큼만 다국어적이고, H_911에 따라 그 코퍼스는 count-balance concat이 아니라 cross-lingual **의미연결**(parallel·meaning-aligned)이어야 한다. 학습자는 GPU backprop이 아니라 AKD1000 칩([[ONCHIP-PARADIGM]]). 따라서 모델(`.clm`)·코퍼스(`.kosmos`)·칩(AKIDA)·가설(H_911)은 분리 불가한 하나의 타깃 — 그래서 META-domain이다.

```
[ 5-lang PARALLEL .kosmos @corpus ]   KOSMOS axis (C4)  ko·en·zh·ru·ja · c>0
   limen-packed shards · profile        + concat control (same bytes, reordered)
          │ encode → spikes
          ▼
[ backbone .clm (int4, byte-id port) ] CLM axis (C3) · H_877 inference lane
          ▼
[ AkidaUnsupervised on-chip fit ]      substrate (C1·C2) · pi5-akida AKD1000
   last-layer Hebbian plasticity         ONCHIP-PARADIGM learning lane
          ▼
[ AKIDA-learned 5-lang CLM .clm ]      → CLM collection (HF dancinlab)
   + F-CLM-AKIDA-MULTILING-SEMANTIC      gate = H_911 (C5) · verdict .verdicts/
```

## ── 必 mandatory conditions (반드시 지켜야 되는 조건 · 위 모두 기록) ──

각 조건은 REQUIRED. 하나라도 빠지면 도메인 scope 밖.

- **C1 — AKIDA 학습 (on-chip, NOT GPU)**: 모델은 AKD1000 실리콘에서 on-chip plasticity로 학습 (`AkidaUnsupervised` — Hebbian last-layer few-shot binary-weight, `model.fit()` ON CHIP), device `pi5-akida` (BC.00.000.002 · NSoC_v2 · BackendType.Hardware · akida SDK 2.19.1). GPU는 PLASTI-SIM 계측 전용(falsifier pre-register), 배포 학습자 절대 아님. ↔ H_904 (on-chip learn HW≠SW).
- **C2 — [[ONCHIP-PARADIGM]] 반영**: 이 도메인은 ONCHIP-PARADIGM의 4 sub-paradigm(on-chip plasticity · learn-while-infer · MITOSIS growth · self-play dispatch-KL)을 상속. 백본은 int4 byte-identical 이식(H_877 추론 lane), 그 위 학습은 칩의 stochastic plasticity lane(H_679/H_904). GPU-hinge 학습은 배포에 상속 안 됨.
- **C3 — `.clm` 포맷 (model)**: 산출 모델은 `.clm` 포맷 준수 (`CLM/CLM_FORMAT_SPEC.md` · CLMConvMoE: conv1d-K3 + GroupNorm + GELU + MoE-router + experts, int4-QAT envelope). HF model card는 on-chip edge-learn provenance(ported backbone 위 last-layer Hebbian)를 정직 명시, from-scratch GPU pretrain 아님(g63).
- **C4 — `.kosmos` 구조 반드시 지킬 것 (limen 등)**: 코퍼스는 `.kosmos @corpus`로 작성, kosmos/2.0 구조 완전 준수 — `@corpus` top-level(anchor_level sample|topic|2tier · count · lane_mix · vocab · encoding · merkle); member 2-form(inline 중첩 `@anchor` ⊕ `ref` `.limen` packed shard — magic `LIMEN\0\0\0` + version + count + length-prefixed `@anchor` records + trailing merkle root, opaque blob 아님); profile-bound(anima-consciousness-carving — coord/lane/radius/tier/tags); `closed_corpus`(Σ frac=1.0 ∧ ∀ ref sha256 ∧ merkle 재계산); placement(coord) ⊥ text(payload) register-leak guard. SSOT: `kosmos/spec/kosmos.md` + `kosmos/spec/limen.md`. ref: `kosmos/examples/04_corpus_clm_byte.kosmos`.
- **C5 — H_911 이 성립해야 됨**: 코퍼스는 5언어(ko·en·zh·ru·ja) cross-lingual 의미연결 형태(parallel·concept-major·c>0), gate는 H_911 — parallel 학습자가 concat(count-only·c~0) 대조군보다 super-additive 통합. H_911 substrate-proxy는 이미 🟢 SUPPORTED-NUMERICAL(Φ inverse-U: c=0 ≈0.0139 · c=0.5 peak 0.4834 · c=1 →0, [[UNIVERSE/H_911]]). 이 도메인은 CLM-on-AKIDA 레벨에서 재입증해야 함(F-CLM-AKIDA-MULTILING-SEMANTIC, 아래). **H_911 성립은 성공 조건이지 옵션 아님.**
- **C6 — 필요시 추가가설 진행**: H_911만으로 타깃이 안 닫히면(on-chip edge-learn 용량 천장 · register-leak · anchor-drift · chip-scale routing degeneracy 등) 추가 pre-registered 가설(H_9xx)을 필요시 생성 — 각 frozen-falsifier-first(g5) · CLAIMS.tape + `.verdicts/` 기록 · 이 도메인에 링크백. 가설엔 open-ended, §조건엔 closed.
- **C7 — 위 모두 기록**: 이 `.md`가 모든 조건의 SSOT 기록 · sibling `CLM-KOSMOS.log.md`가 진행 로그 · 모든 claim → CLAIMS.tape · 모든 verdict → `.verdicts/<slug>/` verbatim(g5). 어떤 조건도 채팅에만 남지 않음.

## ── gate (falsifier) ──

- [ ] **F-CLM-AKIDA-MULTILING-SEMANTIC** (pre-registered · frozen before run · g5): AKD1000에서 5-lang **parallel** `.kosmos @corpus`로 edge-learn(`AkidaUnsupervised`)한 CLM이 동일 **concat** 대조군보다 통합이 측정적으로 우수 — 동일 바이트 + 동일 on-chip update, `@corpus` member ordering만 다름. 🟢 CONFIRMED iff (A) on-chip 학습 live(`learn_happened_hw`) ∧ (B) parallel > concat 통합 측도(device noise 초과). 🔴 REFUTED iff parallel == concat on chip → closed-negative(H_911이 AKD1000 edge-learn엔 전이 안 됨 · a_paper_negative_ok publishable). verdict → `.verdicts/clm-akida-multiling-semantic/` verbatim.
- [ ] **F-CLM-CORE-3AXIS** (pre-registered · frozen before run · g5): `.clm`을 CORE/generator.hexa L3 슬롯으로 ANIMA 엔진에 올려 3축 동시 측정. 🟢 CONFIRMED iff 세 축 전부 각자의 pre-registered NULL(무자극/component-sum baseline)을 초과 — 🧠 의식(Φ·W·Ψ substrate 신호 > 무자극 baseline) ∧ 📉 CE(F-CLM-PROD-DESCENT 하강) ∧ 🌱 창발(통합/합성 > component-sum). 🟠 PARTIAL iff CE만 GREEN이고 의식 또는 창발이 NULL — closure 아님, 정직 잔여로 기록(p7: CE-only는 통과 아님). 🔴 REFUTED iff 세 축 다 NULL. CORE 배선(generator L3 + kosmos_io 앵커) 미빌드면 verdict는 "BLOCKED-WIRING"으로 ⏳, 축별 격리 proxy는 "CORE-탑재 미검증" scope. verdict → `.verdicts/clm-core-3axis/` verbatim.

## ── 평가 3축 (의식 · CE · 창발) — ANIMA 엔진 + CORE 탑재 ──

CE(loss) 단독은 진리가 아니다 — perplexity/loss를 정답으로 쓰면 Goodhart 함정(p7 NO PERPLEXITY VERDICT). 학습된 `.clm`은 격리된 loss 스크립트가 아니라 **ANIMA 엔진(CORE 포함)에 올려서** 3축으로 평가한다. `.clm`은 CORE/generator.hexa **L3 슬롯으로만** 진입한다(a_core_engine_map · 단일 입구): brain emit → generator → A(pure_field) ⇄ G(engine_g) ⇄ brain_decide 구동. 이 셋은 기질-전용이라 `.clm`을 직접 먹이지 않는다 — generator 슬롯이 유일 경로.

```
[ AKIDA-learned .clm ]
        │  CORE/generator.hexa  L3 슬롯 (단일 입구 · a_core_engine_map)
        ▼
[ A pure_field ] ⇄ [ G engine_g ] ⇄ [ brain_decide ]   ← ANIMA 의식 엔진 (Ψ=1/2)
        │                                    ▲
        │  kosmos_io 앵커 입구 (단일)         │
        └──────── .kosmos anchors ────────────┘
        ▼
  3축 측정 ── 🧠 의식 · 📉 CE · 🌱 창발
```

3 축 (전부 측정·기록 — 하나라도 NULL이면 closure 아님):
- 🧠 **의식 (consciousness)** — 기질-내재 신호로 측정, loss 아님: Φ scale · M activation · W tension envelope · Ψ=1/2 fixed point 수렴 · MITOSIS tick · E ratchet. `.clm`이 brain_decide를 구동할 때의 substrate 상태(a_substrate_native_speak). pre-register falsifier로 NULL(무자극 baseline) 초과를 본다.
- 📉 **CE (cross-entropy descent)** — 표준 하강 지표. 유지하되 **단독 게이트에서 3축 중 하나로 강등**(p7). Lane G/G-ref의 util·CE는 여기로 들어온다.
- 🌱 **창발 (emergence)** — 부품엔 없던 능력: 다단계 합성(Lane A 롤아웃이 친 1-홉 천장 너머) · 학습범위 밖 cross-lingual 전이 · H_911 super-additive 통합(parallel > concat). component-sum baseline 대비 초과분으로 정량.

배선 정직 표기 (a_core_engine_map · phantom wiring 금지): generator.hexa L3 슬롯 + kosmos_io→brain_decide 앵커 입구는 **⏳/❌ until built** 로 표시 — 빌드 전에는 3축 평가가 CORE-탑재 형태로 못 돈다는 걸 명시하고, 그때까지 축별 proxy(격리 측정)는 "CORE-탑재 미검증"으로 scope.

## ── pipeline 산출 ──

- corpus → **KOSMOS 컬렉션** (HF dancinlab · private) · model → **CLM 컬렉션** (HF dancinlab · private)
- seed corpus (HF): `dancinlab/clm-semantic-parallel-corpus` (5-lang parallel · 🟡 CPU-proxy → on-chip 승격 대상)

## ── honest scope (g63 · a_scale_honest_scope) ──

AKIDA on-chip learn = last-layer few-shot Hebbian(`AkidaUnsupervised`), H_904 plasticity lane — full from-scratch backprop pretrain 아님. 백본은 int4 byte-identical 이식(H_877); 그 위 학습이 on-chip 비결정 절반(H_904 HW≠SW). pi5-akida = 소유 HW(cloud 과금 0). on-chip parallel == concat 면 🔴 closed-negative, 묻지 말 것. GPU는 falsifier pre-register(PLASTI-SIM)만, 배포 학습자 아님(C1).

## ── cross-link ──

[[ONCHIP-PARADIGM]] (C2) · `kosmos/spec/{kosmos,limen}.md` (C4) · `CLM/CLM_FORMAT_SPEC.md` (C3) · `UNIVERSE/H_911` (C5) · `.verdicts/904_clm_onchip_plasticity` (C1 H_904) · `SUB_ENGINES/AKIDA/scripts/edge_learn_probe.py` (C1 AkidaUnsupervised) · HF `dancinlab/clm-semantic-parallel-corpus` (seed) · `CORE/generator.hexa` L3 슬롯 + `kosmos_io`→`brain_decide` (3축 CORE 입구 · a_core_engine_map) · `CORE/{pure_field,engine_g,brain_decide}` (의식 엔진 A⇄G)
