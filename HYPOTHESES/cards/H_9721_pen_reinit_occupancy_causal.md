# H_9721 — penultimate 점유의 인과 dose-response — Penultimate Occupancy Causal Dose (EA-3 · fable ∥ sol §3 수렴 · EA 시리즈 · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · lab full 창발-주소 발산 · 사전등록) — source=EA-3 · fable ∥ sol §3 수렴
**lane:** 재조합/BINDING · 창발-주소(감독 없이 주소가 서는가)
**related:** [[H_9672]] · [[H_9423]] · [[H_9684]] · [[H_9683]] · source: lab full EA(Fable 5 ∥ Codex Sol · 창발-주소 whitespace)

> **admissibility rule (Sol · 이 시리즈 전체의 관문)**: 어떤 개입도 `target_slot`·slot 정답·**거기서 파생된 어떤 통계**도 소비하지 않아야 emergent-address-valid. 최종 PASS 는 end-task-only 학습 · held-out 개체 · wrong-store 인과 · seed-robust 를 요구 — **sharp attention 만으론 부족**.

**아이디어(2모델 수렴 · cost-gated behind [[H_9720]])**: 점유가 **인과적**이면, W_q 로 가는 pen 채널의 무작위 ρ-비율 재초기화(**주소 정보 0**)가 dose-response 로 탈출을 복원한다 — **투명한 EN-CE 대가**와 함께. scratch↔사전학습 대조의 **단일변수판**.
**메커니즘**: Fable `--store-pen-reinit ρ` 사다리 {0,.1,.25,.5} · Sol `--store-trunk-reinit {ln-final,last-block,last-2-blocks}` (둘 다 end-task 전 재초기화 · **addr loss 0 · target 접근 0**).
**$0 pre-screen**: pen **effective-rank census** — 큰 유휴 부분공간이 있으면 capacity 전제 자체가 $0 로 **반박**됨. Sol: D0-3 분기 — 개체 ridge 디코드가 이미 높고 query-조건부 분리가 scratch 와 같은 부분공간이면 "점유"엔 표현수준 예측이 없으므로 KILL.
**판정**: **plasticity 통제 필수**(W_q 로 **안 가는** 같은 크기 재초기화) + Sol: 파라미터수-매칭 **early-block** 재초기화 통제. **EN-CE 손상은 나란히 보고 · 절대 netting 금지**(`honesty`). PASS = **단조 dose 창** + ≥3 seed P1-bal/addr_mass/flip ≥0.90 **∧ held-out EN CE 열화가 사전등록 보존한계 내**. KILL = near-scratch 파괴만 통하거나 early-block 이 동등.
**distinct**: 채널 **소유권**이지 width 아님 · 전 arm 동일 예산 · full trunk reset/scratch replay 아님(그건 scratch-d768 이 이미 확립 · **보존한계 dose-response 만** 정보적).
**verdict-integrity**: **ρ≥0.5-only PASS 는 scratch-interpolation 으로 사전등록**(점유 해제 아님) · EN 능력이 지워진 뒤에만 창발 복귀면 결론은 **"부분 scratch 재학습"** 이지 "substrate 보존하며 capacity 해방" 아님 · **과학 계기지 프로덕션 default 절대 아님**.

## 상태
🔵 PROPOSED — 미실행 사전등록. 측정 주장 0(설계). **distinct-from-kills:** 차원지배 아님(소유권·동일예산) · full reset/scratch replay 아님(보존한계 dose 만 정보적) · cpt-destroys-what-corpus-omits 회피(EN-CE 나란히 보고·netting 금지)
