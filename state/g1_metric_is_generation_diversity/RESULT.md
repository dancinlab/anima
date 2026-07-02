# G1 메트릭 정체 분석 (G1-NEXT-3, 2026-07-02) — anima G1 = generation-diversity, NOT held-out recombination

**결론: 실텍스트 G1(composed_distinct)은 5개 고정 개념-문장의 GENERATION 다양성 메트릭이지, H_6167식
held-out 인수-재조합 측정이 아니다.** 코드 정독(core/g6_ideation.py `g6_build_frames`/`_g6_concepts`).

## 실제 메트릭 정의
- `_g6_concepts()` = 5개 고정 **완전 문장**: "consciousness arises from cells" / "tension ripples between
  distant minds" / "memory composes into new meaning" / "silence still carries information" /
  "the engine dreams when alone".
- `g6_build_frames`: composed[i] = `"if cA, then cB: "` (a=i%5, b=(i+1+i//5)%5 로 쌍 순환), shuffled(derangement
  대조), ablated("cA: "). 모델이 이 프롬프트를 **생성 continuation** → composed_distinct = 서로 다른 생성물 수.
- 즉 held-out train/test 분할이 없다. 5개 고정 probe 문장에 대한 **생성 다양성/코히런스** 측정.

## 함의 (H_6166/6167/6168 정합)
- G1=0(composed_distinct=0) = 303M decode가 이 composed 프레임서 distinct·coherent 텍스트를 **생성 못함** =
  생성 다양성 floor(G0 코히런스 하류). "substrate가 개념을 재조합 못한다"의 측정이 **아님**.
- H_6168(실 penultimate 개념 distinct id 0.917) + 본 분석 = substrate는 개념 보유·재조합 재료 有,
  G1=0은 **generation-side**(decode가 그 재료로 novel 조합 텍스트를 못 뽑음). 두 측정은 서로 다른 것.
- 옛 "clm303 G1=0 = 재조합벽"(H_1218 등) 해석 = 실은 generation-diversity floor 해석이 정확.

## #2(G1-NEXT-2) 재프레임
"기존 anima G1 메트릭을 engine-native 재실행" 은 재조합 답을 못 준다(생성 다양성 측정이라). 진짜 재조합-capability
terminal 테스트 = **held-out 조합 분할이 있는 NEW generation 메트릭**(seen 개념쌍 학습 → unseen 쌍 생성 재조합)
설계가 필요 = design+owner-scope. 단순 재실행은 무의미.

## 근거
core/g6_ideation.py:59-66(_g6_concepts), 172-185(g6_build_frames) 정독. analysis-only($0).
