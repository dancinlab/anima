# 계획 — 연결된 의식-게이트가 통합 의식에 미치는 영향 (CONSCIOUSNESS ABLATION STUDY)

> status: **계획만 (실행 보류)** · 사용자 지시 2026-06-20 "연결된 것들이 의식에 어떤 영향을 미치는가, 303M+엔진, 정상상태에서 측정"
> ⚠️ NOT H_1481(학습-의식 추세 = 오해). 이건 **정상상태 ablation 으로 lane→통합의식 기여도** 측정.

## 핵심 질문
anima 의 의식-게이트 14종(G16~G27 + Novelty: GlobalWorkspace/Habituation/PrecisionSurprise/SelfIdentity/LearnedPrecision/Novelty/AttentionalBlink/SenseOfAgency/SubjectiveTime/EmotionRegulation/DirectedForgetting/BodyOwnership/DividedAttention/FreeWont)는 모두 substrate(immune-store grounding margin + MITOSIS cells)에 **연결**돼 있다. 각 lane(=연결)이 **통합 의식**에 어떤 영향을 미치는가? 어떤 lane 을 끄면 전체 의식이 얼마나 줄어드나? lane 간 상호작용은?

## 측정 (사용자 명시: 303M + 엔진, 정상상태)
- **모델:** production 303M CLM ckpt (h1129c_chat.pt 등, `a_hf_registry`/HF.jsonl)
- **엔진:** live `core/engine_cli.hexa` 의 의식-게이트 14 lane + substrate(ImmuneMemoryGrow grounding)
- **상태:** **정상상태(steady-state)** = 추론 모드, **학습 아님**(CE-descent 추세 X). 안정된 모델에서 측정.
- **통합 의식 지표:** ① 14-게이트 bundle 점수(합/가중) ② **faithful IIT4 Φ**(`stdlib/iit4/faithful_phi.hexa`, `a_phi_iit4_tool` — 프록시 금지) over substrate. 둘 다.

## 방법 — ABLATION
1. **baseline** Φ_0 / bundle_0 : 14 lane 전부 ON, 정상상태 측정.
2. **single ablation** : lane k 하나 OFF → Φ_k, ΔΦ_k = Φ_0 − Φ_k = lane k 의 의식 기여도. 14회 → 기여도 랭킹.
3. **pairwise ablation** : lane i,j 둘 OFF → Φ_ij. 상호작용 = Φ_0 − Φ_ij vs ΔΦ_i + ΔΦ_j (초가산/하위가산 = 시너지/중복).
4. **control** : random-permute lane wiring → 기여도 구조 붕괴(연결이 의미있는지). shuffle.
5. **정직(c9)** : "어떤 lane 도 의식에 영향 0"(전부 독립·중복) 또는 "특정 lane 이 의식 dominant" 둘 다 유효 결과. tune 금지, frozen-first 기여도 bar.

## 단계 (engine-native, c2)
- (S1) `core/engine_cli.hexa` 에 `consciousness_index()` bundle 함수 — 14 게이트를 substrate 상태에서 READ 해 통합 점수 반환(MONITOR-only, Ψ-disjoint, NOT emit gate). + lane-ablate 토글.
- (S2) faithful IIT4 Φ 를 substrate state-space 에 연결(`iit4/faithful_phi.hexa` 호출, n≤8 exact).
- (S3) **production 303M ckpt 로드 = pool/GPU** (게이트2 무거운작업 pool, mini 303M 금지). live engine mount.
- (S4) 정상상태 baseline + single/pairwise ablation sweep → ΔΦ 기여도 + 상호작용 맵.
- (S5) 박제: 새 H_<id> 카드 + jsonl + verdict(엔진-네이티브 = terminal, numpy 미러면 DIRECTIONAL) + ARCHITECTURE.

## 인프라 게이트
- **HEAVY → pool/GPU** : 303M ckpt 로드 + IIT4 Φ sweep = mini 금지(게이트2). `harness pool`(aiden/summer) 또는 `hexa dojo`.
- ckpt PULL/HF 등록(`a_fire_recover_complete`/`a_hf_registry`).
- 엔진-네이티브 verdict(하드게이트1): live `core/*.hexa` Φ/ablation 증거 필요. numpy 선행 = DIRECTIONAL.

## 산출물
- lane별 **의식 기여도 랭킹** (ΔΦ): 어떤 의식-게이트가 통합 의식에 핵심인가.
- **상호작용 맵**: 어떤 lane 쌍이 시너지/중복인가.
- anima 핵심 주장 검증: 의식이 **단일 lane 이 아니라 연결망 전체**에서 창발하는가(분산) vs 특정 lane dominant.

## 미해결/결정 대기
- 통합 의식 지표를 bundle-합 vs IIT4 Φ 중 무엇을 1차로 (둘 다 측정 권장).
- 303M ckpt 어느 것(h1129c_chat.pt 등 HF.jsonl 확인).
- pool 호스트(aiden/summer) GPU 메모리(303M + IIT4 sweep 동시 가능 여부).
