# H_1833 — 학습-中 kosmos anchor 기하 관찰 (N8, 오너 아이디어 · 정정)

**id:** H_1833
**slug:** kosmos_traintime_geometry_watch
**tier:** 🔵 PROPOSAL (anima-native train-time instrument · exploratory · 오너 아이디어)
**date:** 2026-06-30
**source:** UNIVERSE (오너 brainstorm — "학습을 직접 시키면서 kosmos check 하면서 좋은 anchor 기하 발견 가능 or 다른게 발견될 수 있잖아")
**렌즈:** `a_kosmos` · `a_mitosis_train` (p8 train=infer 연속체) · `a_eeg_consciousness_record` (지속 기록 정신) · `break-walls` (exploratory)
**wired:** PROPOSAL (미배선·미측정) — 외부 LLM 0, anima-native. DIRECTIONAL(py mirror)→engine-native(live kosmos_io)

---

## 정정 노트 (r0 → r1)

초기 카드(`kosmos_llm_observer_scaffold`)는 "외부 LLM(claude -p)을 붙여 그리게 한다"로 **오독**했다. 오너 진의 = **외부 LLM 없이**, anima가 *직접 학습*하는 동안 `.kosmos` anchor 공간을 **매 ckpt check** 해서 anchor 기하가 어떻게 형성되는지 **관찰·발견**하는 것. p1/p4 외부-LLM 우려는 적용 안 됨(LLM 0). 훨씬 강한 anima-native exploratory instrument.

## 가설 (exploratory instrument)

모델/substrate를 학습시키면서 `.kosmos` anchor 공간을 학습 step마다 dump·측정하면, **anchor 기하가 형성되는 동역학**에서 ① 좋은 재조합 기하(부모→자식 anchor 배치가 합성을 지원하는 형태)가 창발하거나 ② **예상 밖 구조**가 발견될 수 있다(open-ended discovery — "다른 게 발견될 수 있다").

**H_1829(kosmos 정적 재조합)와의 차별 = 시간축(학습 동역학).** H_1829는 학습된 anchor에서 *정적* constructor를 측정. 본 가설은 학습이 *진행되는 동안* anchor 기하의 **형성 과정**을 관찰(N1 Ψ-동역학이 A⇄G 동역학이라면, 이건 *학습 동역학* 위 kosmos 관찰). p8(train=infer 연속체)의 관찰 도구.

## Design

1. 학습 루프(예: N7 fragment 학습 또는 작은 substrate 학습)에 **kosmos check hook** 삽입 — K step마다 `.kosmos` anchor set dump(kosmos_io).
2. 매 dump마다 anchor 기하 측정: cluster 구조 · 부모-자식 거리 · recombination-reachability(H_1581식 numpy) · placement 분산 추이.
3. 학습 진행 ↔ 기하 추이를 시계열로 관찰 → 창발 패턴 탐지.
4. controls: random-anchor baseline · shuffle · 학습-OFF(frozen) 대조.

## Frozen bar (pre-register · p7 · exploratory라 2단)

| 항목 | bar |
|------|-----|
| (탐색) 기하 창발 | 학습 진행하며 parent-child anchor 기하가 일관 형성(>random baseline) → "발견" = 추가 가설로 등록 |
| (verdict) 재조합 | 발견된 기하를 substrate op로 측정 시 G1 distinct≥2 ∧ >baseline → 그때 terminal(H_1829 합류) |

⚠️ 정직: exploratory = 단독 G1 verdict 박제 금지(발견→재측정이 terminal). "다른 게 발견"은 serendipity 로깅으로 잡되, 사후 cherry-pick 금지(frozen-first 관찰축 사전등록). 외부 LLM 0 = anima-native. 직접 실행: summer pool $0 train-time monitor(서브에이전트 없이).
