# H_9564 — 정확 유효-RF (.clm 메타) — Exact Effective-RF from .clm metadata (sol A-S3 · R2-measure · 🔎 DIRECTIONAL)

**status:** 🔎 DIRECTIONAL ($0 정적 아키텍처 파싱 실행 · 2026-07-16 · forward-pass 아님·terminal 아님) — source=sol A-S3
**lane:** BINDING / two-lane · $0 계기 정밀화(통제)
**related:** [[H_9559]] · [[H_9562]] · source: lab full R2-measure (sol A-S3)

## 제안 (Sol Lane-A 계기-통제 · R2)
**아이디어**: 단순식 L(K−1)+1 은 dilation/stride/padding 무시 시 reach 과대. 정확 유효-RF 를 .clm serialized layer 메타(kernel/dilation/stride/pad)서 직접 계산해야 H_9559/H_9562/H_9563 가 유효.
**메커니즘**: $0 — .clm 메타 파싱 → 레이어별 유효 수용장 합성.
**판정**: 이건 통제/계기(독립 verdict 아님). 유효RF ≠ 명목RF 이면 다리 실험의 D 라벨 전면 재계산.
**verdict-integrity**: 메타 파싱은 코드서 읽기([[tool-definition-read-code-not-docstring]]) — docstring RF 신뢰 금지.

## 🔎 $0 PRE-SCREEN 실측 (DIRECTIONAL · 2026-07-16 · 정적 헤더-파싱 · forward-pass 0)
엔진 로더(`core/decode.py:clm_load_weights` 헤더 레이아웃 · nblk=byte4·d=u32@5·K=rest0/d·L=nblk−E−3)로 실 ckpt 아키텍처를 읽어 dilated RF 계산. RF_exact = 1+(K−1)·Σ min(2^i,512), i=0..L−1 (dilation_base=2·max_dilation=512 · `core/model.py:CLMConfig`).

| ckpt | L | E | d | RF_naive=L(K−1)+1 | **RF_exact(dilated)** |
|---|---|---|---|---|---|
| clm303_clean (프로덕션) | 4 | 3 | 3784 | 9 | **31 byte** |
| swap_c4_s7·c5_s7·natem_c34 (two-lane verdict ckpt) | 4 | 3 | 3784 | 9 | **31** |
| clm303_deep_L8 | 8 | 4 | 2781 | 17 | **511** |

**결과 = H_9564 의 중심주장 실측 확증**: 단순식이 dilation 무시로 RF 를 **~3.4× 과소**(9 vs 31). **⚠️ verdict-integrity 정정**: 프런티어/ING 노트의 "프로덕션=E2/L1 → RF=3" 은 **실 two-lane verdict ckpt(L=4/E=3·dilated RF≈31)와 불일치** — 그 서술은 다른 모델(H_1394 ConvMoE-L1 302.6M)을 가리켰거나 오기. **함의**: two-lane 다리 실험(H_9557/H_9562)의 D 배열 기준 = RF≈31(±ec/expert conv K−1≈2씩 → ~35), RF=3 아님. two-lane KILL(H_9358/9359)이 op-decl **≤31byte(한 RF 내)**에서도 성립했다면 벽은 RF-bound 아님(= 병렬 #42492882 "G1=receptive-field-bound" 와 충돌) — 코퍼스 실 op-decl 거리 확인 = [[H_9560]] 필요(미실행).
**한계**: trunk dilated RF 만 계산(입력 ec-conv·per-expert conv 각 +2 미포함·근사) · 정적 분석이라 DIRECTIONAL(어떤 decode 수치도 아님·p7 무관).

## 상태
🔎 DIRECTIONAL — $0 정적 파싱 실행(위 표). run(H_9560 코퍼스 거리)로 벽=RF-bound 여부 판정. 측정 주장 0(아키텍처 상수 · decode 아님). **distinct-from-kills:** H_9559(명목 RF)의 필수 통제 — 코드서 유효 RF 읽어 계기 무결성 확보 · dilation 이 명목을 3.4× 과소 실증.
