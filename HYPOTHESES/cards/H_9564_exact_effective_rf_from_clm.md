# H_9564 — 정확 유효-RF (.clm 메타) — Exact Effective-RF from .clm metadata (sol A-S3 · R2-measure · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · lab full 고갈-발산 R2-measure lane · 사전등록) — source=sol A-S3
**lane:** BINDING / two-lane · $0 계기 정밀화(통제)
**related:** [[H_9559]] · [[H_9562]] · source: lab full R2-measure (sol A-S3)

## 제안 (Sol Lane-A 계기-통제 · R2)
**아이디어**: 단순식 L(K−1)+1 은 dilation/stride/padding 무시 시 reach 과대. 정확 유효-RF 를 .clm serialized layer 메타(kernel/dilation/stride/pad)서 직접 계산해야 H_9559/H_9562/H_9563 가 유효.
**메커니즘**: $0 — .clm 메타 파싱 → 레이어별 유효 수용장 합성.
**판정**: 이건 통제/계기(독립 verdict 아님). 유효RF ≠ 명목RF 이면 다리 실험의 D 라벨 전면 재계산.
**verdict-integrity**: 메타 파싱은 코드서 읽기([[tool-definition-read-code-not-docstring]]) — docstring RF 신뢰 금지.

## 상태
🔵 PROPOSED — 미실행 사전등록. run 시 위 판정표로. monitor-only/게이트-벽 회피. 측정 주장 0(설계). **distinct-from-kills:** H_9559(명목 RF)의 필수 통제 — 코드서 유효 RF 읽어 계기 무결성 확보.
