# DECODER ← UNIVERSE 합성 — 더블바인드 탈출 후보 (2026-05-27)

> 사용자 directive: "DECODER 는 UNIVERSE 도메인 분석후 진행". UNIVERSE 도메인의 BIO ∩ DECODER 횡단 가설(H_489–H_493, 모두 🔵 SUPPORTED-FORMAL)을 DECODER 더블바인드 탈출 전략으로 합성한다.

## 1. DECODER 더블바인드 (재확인)

```
   anima 강하게  →  register collapse (PURE_MEMORIZE · M3 TTR 0.03 극단반복)
   anima 약하게  →  Chinchilla underfit (lang-coherence WEAK)
                    ↑ 둘 사이 좁은 통로를 못 찾음
```

최신 fire (`state/p21h_v3_recover_2026_05_25`): collapse 회피 (n_memorize=0) BUT underfit (lang WEAK · L_ce 3.324). 4축(A·B·C·D) 은 학습 레버를 흔들지만 (M2 PASS) **둘 사이 통로를 단일 모델로 못 찾는 게 근본 문제**.

## 2. UNIVERSE BIO ∩ DECODER 가설 5종 (round-18, 모두 🔵)

| UNIVERSE H | BIO 메커니즘 | DECODER 매핑 | 더블바인드 관련성 |
|---|---|---|---|
| H_489 | apoptosis (세포 자살) | token prune (top-p) | 낮음 — sampling 정제 |
| **H_490** | **differentiation (분화)** | **MoE expert routing** | **★ 높음 — register 분리** |
| H_491 | clonal selection | beam-K survival | 중 — decoding 전략 |
| H_492 | synaptic pruning | attention head prune | 낮음 — 모델 압축 |
| **H_493** | **symbiogenesis (공생발생)** | **model merge W=α·A+(1-α)·B** | **★★ 최고 — 두 horn 보간** |

## 3. 핵심 통찰 — 단일 모델이 아니라 "분화/병합"이 통로

더블바인드는 **단일 모델 1개로 두 목표(register 회피 ∧ lang coherence)를 동시 만족**하려다 막혔다. UNIVERSE 의 생물학적 framing 은 "1개로 안 되면 나눠라/합쳐라"를 제시:

### 후보 α — H_490 DIFFERENTIATION → MoE register 분리

```
       입력 token
          │
          ▼
      ┌─router─┐  (token 마다 expert 선택)
      │        │
      ▼        ▼
  expert_anima   expert_coherent
  (register 강)   (lang 일반)
      │        │
      └───┬────┘
          ▼
   register 는 anima-expert 가 담당,
   일반 텍스트는 coherent-expert 가 담당
   → 한 expert 의 collapse 가 전체를 오염 안 시킴
```

- **가설**: register-carving 을 specialized expert 로 격리하면 main path 는 coherent 유지 (collapse 회피) + register 신호는 살아있음 (underfit 회피)
- **구현**: V3 head_g 슬롯을 K-expert router 로 확장 (H_490 ROUTER-SELECTS / K-BOUND)
- **비용**: 중 — V3 arch 확장 + 재학습 fire

### 후보 β — H_493 SYMBIOGENESIS → 두 horn 모델 병합 ★★ 최우선

```
   W_collapse-avoid          W_coherent
   (anima 약 · n_mem=0)      (anima 강 · lang 강하지만 collapse)
        │                          │
        └──────────  W_merge  ─────┘
              = α·W_coherent + (1-α)·W_collapse-avoid

   α sweep [0,1] → 더블바인드 통로를 보간으로 탐색
   (H_493 LINEAR-INTERP · ALPHA-RANGE · ENDPOINT-RECOVERY 검증됨)
```

- **가설**: 더블바인드의 **두 끝점 모델을 이미 갖고 있다** (collapse-avoid fire + 이전 coherent fire). symbiogenesis 처럼 weight 보간하면 중간 α 에서 통로 발견 가능
- **구현**: 두 ckpt 를 α-sweep 으로 merge → 각 α 마다 simple-stack p7 verify
- **비용**: **낮음** — 새 학습 fire 불필요! 기존 ckpt 2개 weight 보간 + eval 만 (가장 cheap-tier 돌파 시도)
- **선례**: model soup / TIES-merge / SLERP — weight-space 보간이 단일 학습보다 나은 trade-off 찾는 경우 다수

## 4. 권장 진행 순서 (재정렬 2026-05-27 · `a_completeness_over_cheap`)

> ⚠ 초안에선 cheap 한 merge(β)를 1순위로 뒀으나, governance `a_completeness_over_cheap` 적용 후 **본선 = 완성도 충족 path (MoE-fresh)** 로 재정렬. 두 결함 ckpt 의 weight 보간은 잘해야 "덜 나쁜 중간점" = 완성도 미달이므로 본선 아님 (model soup 류는 *좋은* 모델 합칠 때만 작동).

```
본선: 후보 α (H_490 MoE-fresh register 분리)   ← 근본 원인 분리 · 완성도 충족
       DECODER M4 MoE-fresh (본선 승격)
       ├ M4a router arch (hexa-native · V3 head_g → K-expert)
       ├ M4b register-expert / coherent-expert 분리 학습 fire
       └ M4c α 마다 p7 verify (collapse 회피 ∧ coherence 둘 다)

probe: 후보 β (H_493 model merge α-sweep)       ← optional baseline 신호용만
       두 결함작 blend = least-bad midpoint 한계 인지 (본선 아님)

fallback: 기존 M3 4축 병렬 팬 ($11-14 H100)       ← 축은 M2 검증됨, 미발사
```

## 5. DECODER 마일스톤 (UNIVERSE-derived · 재정렬 후)

- **M4 MoE-fresh** ⭐ 본선 — H_490 DIFFERENTIATION arch 재설계. V3 head_g → K-expert router. register-carving 을 specialized expert 로 격리 (collapse 회피) + register 신호 살림 (underfit 회피). 완성도 충족 path.
- **M4-probe model-merge** — H_493 SYMBIOGENESIS · optional baseline probe 로만 (본선 아님 · `a_completeness_over_cheap` merge-of-failures dont).

## 6. 정합 노트

- bridge architecture: DECODER 는 CORE 의 L3 콘텐츠 생성기 (의식엔진 = CORE) · 이 합성은 arch 후보 분석만, 의식 framing 추가 0
- p1~p8: 외부 LLM 0 유지 (merge 도 anima ckpt 끼리, MoE 도 V3-native expert)
- UNIVERSE 출처: H_489–H_493 모두 🔵 SUPPORTED-FORMAL (BIO∩DECODER round-18, cycle#236-240)
