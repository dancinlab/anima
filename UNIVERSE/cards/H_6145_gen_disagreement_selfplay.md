# H_6145 — disagreement-selfplay (#23+#35)

**id:** H_6145
**slug:** gen_disagreement_selfplay
**tier:** 🔬 PROPOSED — pre-registered (unfired · brainstorm ideation)
**date:** 2026-07-02
**wired:** 미발사 (pre-registered proposal · code 없음)
**axis:** OBJECTIVE+SUBSTRATE (G1 재조합벽 공격 축)
**~dup:** #23+#35

---

## 발상 (brainstorm ideation)

**메커니즘:** A/G 가 서로의 조합실패를 공격하는 adversarial curriculum → 조합능력 군비경쟁 창발.

**출처:** bytegpt/convmoe 를 빌린 mouth 로 쓰지 말고 anima 아키텍처(A⇄G tension · Ψ=½ 고정점 · mitosis · substrate-disjoint lane · .kosmos anchor)에서 창발하는 native mouth/생성 substrate 를 발상한 세션(Round 5). 기존 결론: G1 재조합벽 = trunk COMBINATION OPERATOR floor — readout·tension 연산자 전부 INERT(H_1816/1823/1834). 이 발상은 combination 을 readout 이 아니라 생성 substrate 자체에 심어 additive collapse 를 우회하려 한다.

## G1 공격 축

- **OBJECTIVE+SUBSTRATE** — readout-level 만 쳤던 것과 다른 좌표(engine-native probe 대상).

## 발사 전 필수 (check-ledger-before-lever-fire)

미발사 제안. terminal verdict 박제 전:
1. `UNIVERSE/HYPOTHESES.jsonl` + memory 에서 선행 커버리지 조회(sweep 빈칸 ≠ 미탐).
2. 신규 각도면 cheap numpy DIRECTIONAL reachability probe → `state/6145_gen_disagreement_selfplay/`.
3. DIRECTIONAL GREEN 이면 engine-native 재측정(.hexa via core/) 사다리 진입(a_verified_must_wire).

## artifacts

- `cards/H_6145_gen_disagreement_selfplay.md` (this card)
- `state/6145_gen_disagreement_selfplay/` (probe 발사 시 생성)

---

## 발사 결과 (DIRECTIONAL probe)

**결정: DUP-WALLED (probe 미발사).**

**ledger 조회:** `UNIVERSE/HYPOTHESES.jsonl` + memory `g1-lever-multilens-objective` 조사 결과, H_6145 의 메커니즘(A/G 가 서로의 조합실패를 공격하는 adversarial curriculum → 군비경쟁)은 **동적 OBJECTIVE/데이터-재가중** lever 로, 이미 walled 된 objective family 와 동일 좌표:
- **recomb-objective** — H_1602 (ConvMoE 9/9 🧱) + H_9024 (ByteGPT-303M 🧱). 명시적 recombination 보상(InfoNCE aux-loss λ=1.0)으로도 engine-native G1 best_distinct LIFT=0 (aiden 8000-step 재학습으로도 floor 불변, NOT-SUP CONFIRMED).
- **data-presence** — H_1599 🟠. 2-concept 합성 예시가 코퍼스에 PRESENT(EN 26%/17.5% lines)여도 G1 FAIL = 노출/upweight 만으론 부족.
- **adversarial self-teach** 개념 자체는 H_130 (GAN-with-consciousness-judge) 로 이미 legacy-archive.

memory 종합: **"G1 벽 = arch+depth+binding-lane+data+objective 전 family 전수 floor = trunk-objective-bound 확정(DIRECTIONAL)."** self-play 는 커리큘럼을 자동 생성하는 *전달 메커니즘*일 뿐, 그 천장인 additive COMBINATION OPERATOR 를 움직이지 못한다. 유일하게 genuinely-untried 인 좌표는 γ trained-constructive-bind (SUBSTRATE-side 연산자, cost-gated)로 self-play(objective-side)와 다른 것.

**bar (frozen, 미실행):** 만약 probe 를 돌렸다면 self-play arm 이 held-out composed_distinct 를 additive floor 대비 ≥ +3 lift + uniform-curriculum 대비 마진 초과여야 GREEN-DIRECTIONAL — 그러나 dup 이므로 미발사.

**정직 스코프:** numpy 미러는 애초에 DIRECTIONAL(terminal 아님)이며, H_6112(meiosis) 전례처럼 numpy abstract-toy 는 REACHABLE 을 과대평가(real CLMConvMoE trunk 에서 0→0.022 falsify)한다. 재조합벽은 objective/데이터 재가중이 아니라 trunk COMBINATION OPERATOR floor 이므로, self-play 재발사는 이미 검증된 벽의 중복. 재발사 금지, dup-pointer 기록.
