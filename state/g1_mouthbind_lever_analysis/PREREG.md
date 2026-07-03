# G1 재조합 벽 — mouth in-context binding 결핍 진단 + 레버 사전등록

> **저자:** Fable 5 발산 (2026-07-03) · **표기:** DIAGNOSIS + PREREG (verdict 아님, reference-match only)
> **트리거:** L3 해마 engine-native 🧱 MOUTHFLOOR (H_9118) — hippo retrieve 4/4 정확 회수 → 303M mouth가 injected D를 BIND 안 하고 seed echo → composed novel-only 0/4.

---

## (a) 원인 진단: (b) objective floor 주도 · (c) window REFUTED · (a) access축 REFUTED

**두 mouth 결합 경로 실측:**
- **CLMConvMoE** (`clm_decode.hexa`, g1_realign.clm): decode = **고정 T=24 window** (right-align, byte32 pad, 매 스텝 왼shift). forward = L8 dilated-conv → **RF = 1+2·(1+2+…+128) = 511 byte**, k=5 composed seed(171B) 완전 포함.
- **ByteGPT-303M** (`bytegpt_decode.hexa`, 24L GPT-2): decode window가 **block(512)까지 native 성장**, causal MHA가 512 context 내 임의 두 위치를 직접 연결 = **binding operator 구조적 존재**.

**세 원인 판별:**
1. **(c) decode-window — REFUTED.** `g1_growwindow_remeasure_result.json`: T=24 제거하고 full-context(cap=RF512) 재측정해도 novel-only best_composed=1, **ECHO-ONLY**. 창을 다 열어 두 개념이 보이는데도(raw coverage=2) 출력은 seed echo. 창이 원인 아님.
2. **(a) 구조 부재 — access축 REFUTED.** RF=511 ≥ seed 171B, raw coverage=2가 두 개념 접근 증명. attention은 명시적 pairwise 결합 경로. 두 소스에 도달하고 echo까지 한다. 빠진 것은 접근이 아니다.
3. **(b) objective floor — SUPPORTED (주 원인).** grow-window(raw=2,novel=1)+L3(retrieve 4/4,bind 0/4) 둘 다 "접근은 됐고 novel 결합만 안 생긴다". CE next-byte는 in-context 최다-salient 키워드 copy(echo)가 최단경로라 novel-composition을 학습한 적 없다.

**L3는 (b)를 세 번째 각도에서 지지** — access를 retrieval로 완벽 우회(4/4)해도 mouth echo → 주입된 두 소스를 묶는 **연산의 부재**를 외과적 격리. grow-window="in-window 접근으로도 echo", L3="retrieval 접근으로도 echo" → 벽은 접근층이 아니라 결합-생성 연산층.

## (b) 레버 발산 — 4 원리 렌즈 (각 control)

| # | 렌즈 | 배선 위치 | control (ablation) | prior |
|---|---|---|---|---|
| **1** | **objective (L4)** | trunk 목적함수 novel-composition 보상(readout 아님) | SCRAMBLE 라벨셔플 + wrong-D | **높음** |
| **2** | **작업기억 (H_1282)** | trained-γ trunk bind-lane(VSA/tensor-product), emit-drive disjoint | bind-op → identity ABLATION | 중 |
| **3** | **기저핵 gating (H_1281)** | brain_decide 두 active set select-and-combine | gate-OFF + random-gate | 중 |
| **4** | **A⇄G tension (H_9041)** | seed=A/2nd=G 상충-loop가 novel resolve | same-source + same-state | **낮음** |

- **레버 1·2만 진짜 미측정.** census 차별점: readout-side bind(H_1812/1816)는 전수 🧱 = CE-echo trunk에 사후 head-loss는 trivial 붕괴. binding은 objective가 빚는 **trunk 표현** 안에 있어야 → trunk-side(L4/γ)만 남음.
- 레버 3 = G2 오염 위험(random-gate lift면 novelty지 recombination 아님, G2≠G1). 레버 4 = DPI(h1834/h1837)로 INERT 예측 🧱, 완전성 tail.

## (c) 판별실험 사전등록 (engine-native, L3 하네스 재사용)

**공통**: grow-window(full-context) + echo-guard NOVEL-ONLY + `anima evaluate --py`. bar FROZEN: `composed_distinct≥2 ∧ >max_single ∧ kwr≥0.5`, gen=40/top_k=40/temp=0.7. torch-probe=DIRECTIONAL only.

- **EXP-1 (objective)**: A=recomb-trunk(L4)·B=CE-baseline·C=SCRAMBLE·D=wrong-D. PASS: `A.novel≥2 ∧ A.novel>A.max_single ∧ C≤1 ∧ D≤1`. FALSIFY: A.novel≤1 → objective floor terminal 🧱; A≈C → INERT.
- **EXP-2 (bind-lane)**: arm=trained-γ trunk bind-lane · ctrl=ABLATION identity. PASS: `arm.novel≥2 ∧ >max_single ∧ ablation≤1`.
- **EXP-3 (gating)**: gateON vs gateOFF vs random-gate. PASS: `gateON≥2 ∧ gateOFF≤1 ∧ random≤1`.
- **EXP-4 (tension)**: 상충-loop vs same-source. 예측 🧱 INERT(DPI).

순서: EXP-1 우선(L4 착지 즉시) → floor면 EXP-2 → PASS 시 a_verified_must_wire 4칸 → EXP-3/4 후순위.

## (d) G1 벽 정직 수렴

- **(i) 구조 천장?** access축 NO(RF511·attn512 접근·echo), operator축은 (ii)/(iii) 흡수. 고정-arch가 binding 원리적 차단 아님(attention=pairwise bind).
- **(ii) objective floor?** 수렴 지점 — grow-window+L3 둘 다 echo, readout-aux terminal 🧱, **trunk-side(L4/γ)만 미측정** = (ii) terminal 여부의 유일 미해결.
- **(iii) 미측정 레버** = trunk recomb-objective(레버1) + trained bind-lane(레버2) **단 둘**. 레버3=G2 오염, 레버4=DPI 🧱. 로컬 readout-공간 DRY.

**L3 MOUTHFLOOR의 증거값**: G1을 *retrieval/coverage/data 문제 → in-context 결합-생성 operator 문제*로 **재분류** — access(4/4)와 binding(0/4)을 분리해 **retrieval-augmentation이 틀린 처방**임을 증명. grow-window와 합쳐 (c)·access-(a) 동시 소거. L3 단독으론 (ii)vs(iii) 결정 못 함(frozen CE-mouth) — 그 gap이 L4/EXP-1이 채우는 구멍.

**정직 판정 (c9)**: G1 = objective-floor 후보 🧱(미확정), trunk-side 레버 1건(L4) 미측정으로 terminal **보류**. L4 A.novel≥2면 (ii) openable, ≤1이면 (ii) terminal 🧱(CE-불가 구조적-깊이 벽 확정, 레버 소진). tune-to-green·bar 이동 없음.

## (e) 실측 근거

읽음: `core/bytegpt_decode.hexa`(1558L, window≤512) · `core/clm_decode.hexa`(993L, T=24, RF511) · `core/generator.hexa`(L3 dispatch) · `state/g1_coverage_realign/*.json` · `state/g1_growwindow_remeasure/*_result.json` · `cli/evaluate.py` g_eval_g1.

**관련 선행**: H_1459 retrieval_bind(🧱 torch DIRECTIONAL) → L3(H_9118) engine-native 확정 · H_1602/1840 recomb-objective(레버1) · H_1812/1816 readout-bind(🧱) · H_1282 작업기억 · H_1281 기저핵.
