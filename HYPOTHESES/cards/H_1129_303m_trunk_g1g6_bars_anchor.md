---
id: H_1129
slug: 303m_trunk_g1g6_bars_anchor
title: 검증 303M ko/en chat trunk · frozen G1/G6 recombination bars 앵커 (H_1129/1137/1139/1140) — citation-anchor
group: G1/G6 recombination · 303M trunk (frozen gate bars)
tier: citation-anchor — 2-surface 등록 복원 (ARCHITECTURE 인용, 독립 측정카드 부재)
date: 2026-07-10
---

# H_1129 — 검증 303M chat trunk · frozen G1/G6 bars (citation-anchor)

> **2-surface 위반 복구 레코드** (`a_hypothesis_register`). 본 id 는 ARCHITECTURE.json gate 노드에서
> **16회** 인용되나(항상 `H_1129/1137`·`H_1129/1139`·`H_1129/1140` 쌍) jsonl 레코드도 카드도 없었다.
> 조사 결과 `H_1137`·`H_1139`·`H_1140`·`H_1155`·주변 id(H_1118–H_1209 구간)도 전부 미등록 =
> **renumber-to-existing 아님**. 이 id 는 frozen-gate **앵커 라벨**로만 존재했다. 본 카드는 그
> dangling-citation 을 2-surface 로 최소 복원한다. **판정 없음(no verdict fabricated)** — tier = `citation-anchor`.

## 무엇을 가리키나
검증된 **303M ko/en chat trunk** ckpt = `[256,d,L,H,block]` 헤더의 단일 typed .clm entry. 그 위에서
동결된 **G1/G6 recombination bars**:
- **G1 recombination**: `composed_distinct ≥ 2 ∧ > max_single ∧ coherent` (H_1129/1137 VERBATIM), multiseed {7,4302,4303}.
- **G6 novelty**: H_1140 novelty bar.
- 이 frozen bars 위에서 CORE `--engine conv mount` / `core/clm_decode.hexa` byte-exact 재측정이
  engine-native verdict 의 기준선(`a_engine_native_learning`). top-k=40 temp=0.7 SAMPLING decode 로 authored.

## 실제 등록된 sibling 작업 (여기가 측정 SSOT)
- **H_1588** G1 recombination reference-match (single-seed RNG-wall 대체, 🟠 DIRECTIONAL)
- **H_1601** G1 binding-lane reconcile (🧱 BINDING-LANE INERT)
- **H_1602** G1 explicit recombination objective/curriculum 303M retrain (🧱 NOT-SUPPORTED)
- **H_1603** G1 ≡ G6 unification (🟠 MIXED→SUPPORT)
- capacity-wall 재해석: H_1129/1139/1464 = scale-invariant '1/3 구조상수' (H_1560 계열)

> 실측 verdict 는 위 등록 id 들에 있다. 본 앵커는 인용 무결성(2-surface)만 복원하며 새 과학 주장을 하지 않는다.
