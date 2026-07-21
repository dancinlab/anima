# H_9835 — A⇄G 불일치를 **레인이 아니라 가중치**로 쓴다 (R11-6 · 기대효과 최소)

**status:** 🧭 PROPOSED (R11 · lab full 발산 · **DIRECTIONAL 설계**, 판정 아님 · **최하위 순위**)
**source:** fable `TENSION-CURRICULUM`
**wired:** no — 미구현.

## Question

H_9828 은 코퍼스가 반증가능 구조를 **담고 있음**을 실측했다(EN 762,625 문장 · p=0.006461 · lift>1).
CE-marginal 은 그 희소 구조를 평균으로 지워버린다. G 가 샘플별 불일치를 채점하고 CE 를 고불일치
샘플 쪽으로 재가중 = **중요도 표집**.

## kill #4 와의 구분 (이 카드가 서는 유일한 근거)

H_9576 이 죽인 것은 tension 을 **의미 전달 레인**으로 쓰는 것이다(8-벡터가 1비트로 접힘 ·
방향 ρ=−0.077). **커리큘럼 가중치는 1비트면 충분**하므로 그 붕괴 발견과 양립한다 —
치명적이지 않다. **바로 그래서 기대 효과크기가 작고, 순위가 최하위다.**

## Intervention (flag 형태 · 미구현)

```
anima-py train --tension-curriculum {off,weight,filter} --tension-curriculum-temp T \
               --brain-runtime required
```

## Arms + controls

| arm | 무엇 | 읽는 법 |
|---|---|---|
| **엔트로피 맞춘 무작위 재가중** | 동일 가중분포 엔트로피 | 붕괴해야 함 |
| **G 없는 손실기반 hard-example mining** | 순수 CE 난이도 채점 | **이걸 못 이기면 G 는 장식** — 팔은 정직하게 죽는다 |

## 판독가능성 — **hard (a)**

주 DV 가 G6 이라 **H_9828 수리(249 draws) 전 판독 불가**. 그 전에 발사하지 말 것.

**related:** H_9576 · H_9805 · H_9828 · H_9834
