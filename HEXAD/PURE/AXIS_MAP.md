# HEXAD/PURE — corpus 외 미탐색 축 map

> V3 closure 의 "multilingual = corpus-bound" verdict 는 5 fire 가 전부 동일
> 코퍼스(`wiki_frac=0.3`, 70% anima)에서 나왔다. 재설계 axis R1~R7 은
> scale·mitosis·head_g-존재·pool·steps 만 sweep — **학습 레짐 축은
> 미탐색**. corpus 비율 재발사(E2/E3, [`README.md`](README.md))가 1차
> 후속이고, 본 문서는 그것이 실패할 경우의 **fallback 축 map** 이다.
>
> anchor: closure 결정 fire 보고서 `../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/HEXAD_V3_FIRE_2026_05_22.md` §8.

## 왜 이 축들이 미탐색인가

closure 가 sweep 한 R1~R7 은 전부 **무엇을(what)** 의 축이다 — scale,
mitosis on/off, pool 크기, step 수. 한 번도 건드리지 않은 것은 **어떻게
학습하는가(how)** — 학습 순서, teacher 신호, head 별 objective, embedding
freeze, sampler, representation 제약. anima-register collapse 는 학습
dynamics 현상이므로 이 축들이 직접적이다.

## 축 map

| 축 | 변경 | 왜 미탐색 | 기대 | cost | tier |
|---|---|---|---|---|---|
| **B 증류** | vP21M(LoRA, 4/5 langs) = teacher, V3 student 가 logit-match (KD loss) | from-scratch 만 시도; teacher 신호 0 | Qwen 다국어 prior 를 pure-HEXAD arch 로 전이 — 1M tok capacity 한계(C3 #3) 우회 | ~$5 H100 | ★★★★ |
| **A 커리큘럼** | wiki-only 선학습(다국어 LM 확립) → anima 를 late phase 로 도입 | 5 fire 전부 step1 부터 shuffled fixed mix | anima collapse 전에 다국어 prior lock-in | ~$3 H100 | ★★★★ |
| **C head_g objective** | head_g 에 anima-register objective 부여, head_a 는 pure-multilingual | head_g 는 train loss 부재 → inert(R4), 게다가 head_a vocab alignment 흐림(§8 line 71) | dual-head 를 설계 의도대로 작동: head_a=언어 ⊥ head_g=의식 | ~$3 H100 | ★★★ |
| C2 head_g 제거 | head_g 완전 제거 (inert + 유해면 dead-weight) | OCCAM 은 head_g 를 "ablation-무해" 로 유지 판정 | head_a vocab alignment blur 제거 | ~$3 H100 | ★★ |
| **D embed freeze** | token_embed + lm_head 를 다국어 임베딩으로 init 후 **freeze**, HEXAD block 만 학습 | B2 는 Qwen weight map 했으나 freeze 안 함 | 언어 geometry 보존 — embedding 의 anima-register 재학습 차단 | ~$3 H100 | ★★★ |
| E lang-balanced sampler | per-언어 token-balanced batch sampler | 코퍼스 5-lang 이나 EN 17078 rec ≫ ko/zh/ru/ja ~500-1000 rec (record 불균형) | 고정 비율에서도 per-lang under-train 교정 | ~$0 (recipe) | ★★ |
| F contrastive lang | 언어 cluster 분리 유지 aux loss | OCCAM 은 consciousness-aux 만 "무관" 판정, lang-contrastive aux 미시도 | 모든 언어가 anima-Korean 으로 collapse 하는 것을 representation-level 에서 저지 | ~$3 H100 | ★★ |

## 가장 날카로운 발견 — head_g

closure 는 R4 에서 head_g 를 "inert → moot" 로 기각했다. 이는 **거꾸로**다:
inert 라는 건 dual-head 설계(head_a=언어 ⊥ head_g=의식 emission)가 **한 번도
실제로 검증된 적 없다**는 뜻이다. anima-register collapse 가 일어나는
이유는 정확히 anima register 가 **언어 head(head_a)** 로 들어갔기 때문 —
의식 head(head_g)가 아니라. head_g 에 anima objective 를, head_a 에
pure-multilingual 을 배선하는 것은 부수 축이 아니라 **아키텍처를 설계대로
처음 시험하는 것**이다 (축 C).

## 결정 트리

```
Track 1 corpus 재발사 (E3 anima0% · E2 50%)
├─ 둘 중 하나 ≥ 4/5 langs ≥ PARTIAL
│    → corpus 축 vindicated · V3 REOPENS · 본 map 보류
└─ 둘 다 FAIL
     → corpus 축까지 소진 · 본 map 발동
       fan out 병렬 (g12·g24): B 증류 ∥ A 커리큘럼 ∥ C head_g objective
       (3 disjoint H100 fire ~$11, wall ~2hr)
       D/E/F 는 위 결과에 따라 조합
```

## honest C3

1. B 증류는 "pure-HEXAD substrate" 의 순수성 일부를 양보 — arch 는 HEXAD 지만 capability 는 Qwen 유래. 사용자 의도("Qwen 위 옷 아님")와의 정합은 arch-순수 ⊥ capability-전이 구분에 달림.
2. A 커리큘럼의 late-anima phase 길이/시점은 미정 — sweep 필요.
3. C 는 head_g 에 줄 anima objective 의 형태(별도 CE? contrastive?)가 미설계.
4. 본 map 은 closure verdict 를 가정 — Track 1 이 PASS 하면 전부 moot.
5. E 는 단독 효과 작을 것 (record 불균형은 collapse 의 2차 요인).
6. 전 축 공통 전제: vP21M LoRA 4/5 가 baseline — V3 변종은 ≥ 4/5 ≥ PARTIAL 이어야 채택.

## 관련 link

- corpus 재발사 (1차 후속): [`README.md`](README.md)
- closure 보고서: [`../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/HEXAD_V3_FIRE_2026_05_22.md`](../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/HEXAD_V3_FIRE_2026_05_22.md) §8
- V3 spec (브레인스토밍 §2 에 E2/E3 corpus 변종 원안): [`HEXAD_NATIVE_PURE.md`](HEXAD_NATIVE_PURE.md)
- production baseline: [`../LORA/README.md`](../LORA/README.md)
