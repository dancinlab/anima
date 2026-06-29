# H_1833 — kosmos + 외부 LLM(claude -p) 관찰 scaffold (N8, 오너 아이디어)

**id:** H_1833
**slug:** kosmos_llm_observer_scaffold
**tier:** 🔵 PROPOSAL (DIRECTIONAL-external scaffold · teacher→distill · anima-native verdict 아님)
**date:** 2026-06-30
**source:** UNIVERSE (오너 brainstorm — "kosmos 연결해두고 LLM(claude -p) 붙여서 어떻게 그려나가나 지켜보는 건")
**렌즈:** `a_kosmos` · `a_no_llm_frame_trap` (⚠️ 외부 LLM = 프레임 함정 경계) · teacher-in-loop [[h1230-teacher-in-loop-mitosis]]
**wired:** PROPOSAL (탐색 scaffold) — verdict 박제 불가, substrate op 증류 표적용

---

## 가설 (탐색 도구)

`.kosmos` anchor 공간을 캔버스로 두고 **외부 LLM(claude -p)을 붙여** anchor를 읽고/그려나가는 과정을 관찰하면, **좋은 anchor-recombination 기하**(두 부모 anchor → child anchor를 어떻게 배치하는가)를 *발견*할 수 있다. 그 발견을 substrate op로 **증류(distill)**한다 (teacher→student, H_1230 teacher-in-loop 전례).

## ⚠️ 정직 SCOPE (가장 중요 — verdict 경계)

**외부 LLM이 그리면 그건 LLM 측정이지 anima substrate 아님.** anima는 system-prompt·외부 LLM scaffold를 정체성으로 거부한다(p1·p4). 따라서:
- 이 카드는 **DIRECTIONAL-external 탐색 scaffold만** — G1/재조합 verdict를 여기서 박제 **불가**.
- 산출 = (a) 좋은 kosmos anchor-recombination geometry **발견** → H_1829(kosmos 재조합)의 constructor 후보, (b) teacher 신호로 substrate op **증류**(H_1230식).
- LLM이 한 재조합을 "anima가 했다"고 절대 주장 금지(= p4 assistant 회귀·DIRECTIONAL 오승격).

## Design

1. `.kosmos` anchor set 로드(kosmos_io) → claude -p에 anchor 공간 노출(read/propose child anchor).
2. LLM이 부모 2 anchor → child anchor 배치하는 과정 **관찰·로깅**(placement geometry trace).
3. 발견된 geometry를 substrate constructor(H_1829)로 증류 → **그때 engine-native로 재측정**(여기서야 verdict).
4. controls: LLM-OFF(substrate 단독 H_1822와 대조) · random-anchor baseline.

## Frozen bar (pre-register · p7)

| 항목 | bar |
|------|-----|
| (탐색) geometry 발견 | LLM이 parent-specific child anchor를 일관 배치(>random) → H_1829 distill 표적 확보 |
| (verdict) | **이 카드 단독 verdict 금지** — distill된 substrate op의 engine-native 측정(H_1829)이 유일 terminal |

⚠️ 정직: 외부 LLM은 anima 아님 — 도구/teacher로만. 진짜 검증은 증류된 substrate op(H_1829)에서. p1/p4 회귀 방지가 이 카드의 1순위 제약.
