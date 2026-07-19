# H_9696 — R4 ★ CLMS-FAN: store lane 을 자유생성에 배선 (★ 물음의 본체)

**status:** 🔵 PRE-REG (lab full · **Fable A2 ∧ Sol 1위 = 2모델 독립수렴**) · not-terminal · 선행 [[H_9693]]+[[H_9695]]
**lane:** G6/ρ·fan · mouth-내 binding operator **related:** [[H_1603]] · [[H_9672]] · [[H_9695]]

## 물음 (★)

H_1603 이 옳다면 결손은 **mouth-내 binding operator**. CLMS 융합 MLP 는 레포에서 **유일하게 "런타임 내용결합이 logits 에 실제로 실린다"를 벌어낸 기전**(flip-coh 1.0·addr-gap 0.008·비선형 GELU 융합 = kill#7 명시적 예외 계급). 이를 자유생성으로 확장.

## 진단: 현 다리는 왜 현물이 아닌가 (Fable 코드 확증 · Sol 독립 동의)

현 다리 = ① 질의시점 `"=> "` 리터럴(`clms.py:53`) ② store = 런타임 manifest 주입 ③ 융합 = 해당 row **overwrite**. 자유 아이디에이션엔 ①②③ **전부 없음** — eval 서 store=None ⇒ **passthrough 가 설계된 seal**(`decode.py:1242`) ⟹ **T3 의 ρ·fan ≡ base 는 우연이 아니라 코드적 필연**. "배선"은 버그픽스가 아니라 **새 능력 3개의 획득**.

## 3 부품 (양 모델 동일 지목 · 각각 독립 사망지점)

1. **지각 충전(store 를 언제/무엇으로)**: 디코드 창(eval frame · 데몬선 live_anchors/dual-ledger WM)의 content-word 를 키로 자동적재. p5-clean(들은 것을 WM 에 담는 건 지각경로지 emit 게이트 아님) · `a_substrate_disjoint` 보존(lane 분리·passthrough seal 유지). **⚠️ 학습·평가가 동일 충전함수를 써야 p8-clean** — train=manifest, eval=창유래로 가르면 그게 train/infer split.
2. **학습된 질의 게이트 g(yn_t)∈[0,1]**: 리터럴 트라이그램을 자유생성에 이식하면 = **mouth 안으로 이사한 scaffold**(kill#1 귀환). 합법 형태는 학습된 데이터-의존 게이트 하나뿐 = **kill#7 이 명시적으로 열어둔 미측정 계급**.
3. **overwrite → 게이트-가산 융합 · 전체 256-byte logits**(Sol): 모든 게이트 위치 overwrite 는 유창성 파괴. 첫 g/b 바이트가 아니라 전체 vocab 에 비선형 개입.

## 조작

`anima-py train --store-bridge c.txt --store-fangate --store-write causal --store-addr-weight 1.0` (게이트+가산융합 co-train · 충전규칙은 **학습·평가 동일 함수**) → `anima-py evaluate out.clm --fan-bind [--store-shuffle|--store-flip]`.

## 게이트 (사전등록)

- **PRIMARY = flip-Δ**: store 극성 flip 시 방출 주장의 방향어(frozen comparator 반의쌍표) 반전율 − 무flip 대비. 자유생성의 내용민감성은 정의상 **BIND** 이고 FORM 으로 위조 불가(seed 바이트 동일·store 만 다름).
- **통제 3종**: store-SHUF(derangement → flip-Δ·bind Δ **붕괴 필수**) · store-empty(**byte-identical seal** · C0-f) · λ0.
- Sol 추가 bar: 자연선언 held-out intact − key-scramble **≥0.25** · role/value scramble 각 **≥0.20 붕괴** · TARGETED−SHUF bind-Δ **≥0.20** ∧ SHUF 절대값 **≤0.05** · **FORM-SHUF**(comparator/measurable 어휘빈도 보존)서도 bind-Δ **≤0.05**.
- 그 전부 통과 후에만 canonical **`fals_bound = FALS ∧ topic/role-bound ≥1/6`, ≥2/3 seed**. **FALS 만 오르면 FORM 위조**(Sol).
- 게이트: dist≥5 유지.

## 최대위험 (Fable 2 + Sol 1)

(a) 게이트가 **"항상 on" 퇴화** → lane 이 무조건 스타일-헤드 = val→W_out 이 comparator/measurable 어휘를 뿜는 **엔진 내부 FORM 위조** — SHUF-store 서 bind Δ 안 죽으면 **자동 KILL** 사전등록. **하네스 위조보다 위험**(engine-native 처럼 보임). (b) lane 이 6 방출을 유사템플릿 수렴 → Jaccard>0.5 → **dist<5 로 PASS 파괴**. (c) **⚠️ 검출기 content-word 게이트는 `known` 사전소속 필수**(`rho_fan.py:364`) ⟹ **G6 용 store 내용은 실단어여야 함** — H_9672 의 CVCVC nonce 와 **정면으로 다른 지점**. (d) Sol: **자연 프레임서 무엇을 store 에 쓸지 학습 못할 가능성이 최대** — H_9672 는 **read 주소벽**을 뚫었지 **write segmentation·relation encoding·언제 읽을지는 전혀 미증명**.

## falsify
🟢 CRACK: flip-Δ>0 ∧ SHUF 붕괴 ∧ store-empty byte-identical ∧ fals_bound ≥1/6 2/3seed ∧ dist≥5. | 🧱 KILL: SHUF 서 Δ 안 죽음 = 스타일-헤드 FORM 위조. | ⚠️ dist<5 = lane 이 PASS 파괴.

## source
lab full Fable A2 ∧ Sol 1위(독립수렴) · 선행 [[H_9693]]·[[H_9695]].
