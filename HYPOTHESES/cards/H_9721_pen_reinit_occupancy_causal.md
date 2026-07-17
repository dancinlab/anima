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
🔵 PROPOSED(reinit-intervention 미실행) · 🔎 **$0 pre-screen 실행 = capacity 전제 반박(2026-07-17 · summer 303M)**

### 🔎 pen effective-rank census — capacity 는 병목이 아니다 ($0 · 기존 dump)
H_9719 census 로 뽑은 base(py303)·t3 penultimate(126 prompt = 63개체×{is,not})의 참여비율(effective-rank):

| ckpt | eff-rank (raw≈centered) | d | 비고 |
|---|---|---|---|
| base py303 | **14.7** | 3784 | 개체 인코딩이 ~15 차원에만 집중(템플릿 지배) |
| t3 s7 | **23.6** | 3784 | addr-학습이 사용차원 +9 확장(비점유화 일관) |

**판정(DIRECTIONAL)**: penultimate 개체 인코딩이 **~15-24 유효차원**에만 산다 — d=3784 대비 방대한 미사용 차원 ⟹ **capacity 는 병목이 아니다**(자리는 넘친다). 이 카드 pre-screen 의 '큰 유휴 부분공간 → capacity 전제 반박' 이 **실측 충족** ⟹ **reinit-to-free-capacity 레버의 rationale 이 undercut**(자리를 비울 필요가 없다). 진짜 병목 = **점유/조직화**(entity code 가 유휴공간에 조직 안 됨), capacity 아님. [[H_9719]] dose-response(점유 95→57% 단조 비점유화)와 정합.
**caveat(정직)**: 126 sample 이라 측정가능 rank ≤126 — 'd=3784 유휴' 는 표본상한 때문에 과장 소지. 엄밀히는 '개체가 ~15-24 차원에 집중·템플릿 지배·조직 안 됨'. 더 큰 개체풀로 강화 가능(follow-on).
**남은 것**: reinit-intervention dose(`--store-pen-reinit ρ` 사다리 + plasticity 통제)는 **학습 fire**(pool·H_9720 뒤 cost-gated) — capacity 아닌 조직화가 병목이므로 우선순위 하향. **distinct-from-kills:** 차원지배 아님(소유권·동일예산) · full reset/scratch replay 아님 · cpt-destroys-what-corpus-omits 회피(EN-CE 나란히·netting 금지)
