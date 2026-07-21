# H_9848 — G 엔진 8인자 동기를 샘플 가중치로 (R12-11 · H_9835 와 병합 후보)

**status:** 🧭 PROPOSED (R12 · **DIRECTIONAL 설계**, 판정 아님)
**source:** R12 뇌부위 census (2026-07-21) — `origin/main` `core/` 12개 모듈 실측 후 1모듈=1레버로 등록.
상위 설계 노드 = ARCHITECTURE `C2 RECOMBINE` 아래 `🧠 뇌부위 census`. R11(H_9830~9836)의 후속.
**wired:** no — 미구현. 개입은 `anima-py train` 플래그로만 착륙(`a_experiment_engine_native`).

## 실측

`core/engine_g.py`(179줄 · 같은 DEPRECATED py-MIRROR 가드 보유): 8인자 가중 동기점수
(`spont_weight_relevance` / `info_gap` / `curiosity` / `pain` / `coherence` / `originality` /
`balance` / `dynamics` · 가중치 합=1.0) + emit/safety 술어. **닫힌형 · 학습 파라미터 0.**

## 가설

8인자 중 `info_gap`(정보 격차)과 `curiosity`(호기심)는 개념상 **능동학습의 획득함수**와 같은
자리에 있다. 이를 샘플 가중치로 쓰면 H_9828 이 실측한 희소 반증가능 구조
(EN 762,625문장 · p=0.006461 · lift>1)를 CE 평균이 지우기 전에 표집할 수 있다.

## H_9835 와의 관계 — 솔직히 겹친다

H_9835(tension-curriculum)는 **A⇄G 불일치**를 가중치로 쓴다. 이 카드는 **G 의 8인자**를 쓴다.
둘 다 "스칼라 1비트를 커리큘럼으로" 라는 같은 형태이고, kill #4(H_9576: 8벡터→1비트 붕괴)가
말하는 것은 **8인자가 어차피 1비트로 접힌다**는 것이다. ⟹ 두 카드는 발사 시 **한 팔로 병합**하고
`--curriculum-source {tension,g8factor}` 로 안에서 가른다. 별도 발사는 예산 낭비.

## 필수 통제 (H_9835 와 동일)

**G 없는 손실기반 hard-example mining** — 이걸 못 이기면 G 는 장식이고 팔은 정직하게 죽는다.

## 판독가능성

주 DV 가 G6 이면 **(a) H_9828 수리(249 draws) 선행**.

**related:** H_9835 · H_9576 · H_9828
