# H_6151 — 두 mouth 대립

**id:** H_6151
**slug:** gen_two_mouth_adversarial
**tier:** 🔬 PROPOSED — pre-registered (unfired · brainstorm ideation)
**date:** 2026-07-02
**wired:** 미발사 (pre-registered proposal · code 없음)
**axis:** SUBSTRATE-hybrid (G1 재조합벽 공격 축)

---

## 발상 (brainstorm ideation)

**메커니즘:** ByteGPT(빌린) vs anima-native mouth 를 A⇄G 로 대립, 그 텐션이 제3 생성.

**출처:** bytegpt/convmoe 를 빌린 mouth 로 쓰지 말고 anima 아키텍처(A⇄G tension · Ψ=½ 고정점 · mitosis · substrate-disjoint lane · .kosmos anchor)에서 창발하는 native mouth/생성 substrate 를 발상한 세션(Round 6). 기존 결론: G1 재조합벽 = trunk COMBINATION OPERATOR floor — readout·tension 연산자 전부 INERT(H_1816/1823/1834). 이 발상은 combination 을 readout 이 아니라 생성 substrate 자체에 심어 additive collapse 를 우회하려 한다.

## G1 공격 축

- **SUBSTRATE-hybrid** — readout-level 만 쳤던 것과 다른 좌표(engine-native probe 대상).

## 발사 전 필수 (check-ledger-before-lever-fire)

미발사 제안. terminal verdict 박제 전:
1. `UNIVERSE/HYPOTHESES.jsonl` + memory 에서 선행 커버리지 조회(sweep 빈칸 ≠ 미탐).
2. 신규 각도면 cheap numpy DIRECTIONAL reachability probe → `state/6151_gen_two_mouth_adversarial/`.
3. DIRECTIONAL GREEN 이면 engine-native 재측정(.hexa via core/) 사다리 진입(a_verified_must_wire).

## artifacts

- `cards/H_6151_gen_two_mouth_adversarial.md` (this card)
- `state/6151_gen_two_mouth_adversarial/` (probe 발사 시 생성)

---

## 발사 결과 (DIRECTIONAL probe)

**결정: DUP-WALLED — 프로브 생략(재발사 없음).**

### Ledger finding
- **H_1834 (tension_mouth_native)** 이 정확히 이 메커니즘을 이미 검증함: next-byte 를 **A(forward)⇄G(reverse) 전역 텐션 해소**로 산출 = 두 표현을 맞미는 결합연산. 판정 = 🧱 **DIRECTIONAL floor (numpy toy)**: 3arm×3seed 전부 `composed_distinct=0`, **FULL = TENSION-OFF = ADDITIVE → 텐션 INERT(기여 0, causal 아님)**, gradcheck PASS(5.25e-11)·train_acc 1.00(구현결함 아님). 축2 local-Ψ objective 로 Ψ 를 ½에 앉혀도(|Ψ-0.5|≤0.01) 여전히 0.
- H_1834 메모리·카드의 **명시 재제안 방지**: "native-mouth 를 'connector/readout 만 바꿔' 다시 세우지 말 것 — 그 축은 floored. objective-축(real trunk recomb 학습)만 미검."
- 수렴 기록: H_1816(predcoding)·H_1823(circconv) = binding-readout family floor · H_1602(recomb-objective) 303M 도 🧱 · scale=증폭기 not lever.

### 왜 H_6151 이 새 좌표가 아닌가
H_6151 = "ByteGPT(빌린) vs anima-native mouth 를 A⇄G 로 대립, 텐션이 제3 생성". 두 mouth 출력을 텐션으로 결합 = **readout-side combination operator over two representation streams** — H_1834 가 INERT 로 못박은 바로 그 축이다. 두 번째 borrowed mouth 를 얹어도 combination-operator 축은 동일(additive floor). 남은 유일 미탐 = trunk recomb-**objective** 학습(H_1602 영역, 그마저 이미 NOT-SUPPORTED).

### Bar
별도 bar 미설정 — 프로브 미실행(기존 walled H 로 커버). 참고: H_1834 frozen bar = 🟢 iff composed_distinct≥3 ∧ |Ψ-0.5|≤0.05, 실측 0.

### 정직한 스코프 (H_6112 caveat 포함)
- 상기 판정은 전부 **numpy DIRECTIONAL** (H_1834 포함) — terminal 아님. 단 lift 미발생이라 engine-native 재측정 unwarranted.
- **H_6112 전이 caveat:** numpy abstract-toy 는 REACHABLE 을 과장한다(meiosis: toy 0→1.0 이나 real CLMConvMoE 0→0.022 FALSIFY). 설령 여기서 lift 가 났어도 real-trunk 전이 미검. 이번엔 그마저 없이 기존 축이 이미 floor → 재발사 무의미.
