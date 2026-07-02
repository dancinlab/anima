# H_9072 — 비평형 산일 — Ψ=½ = NESS(엔트로피생성>0), 평형 LLM과 구별

- **tier:** 🟢 ENGINE-NATIVE (5/5 live hexa, aiden pool) — Ψ=½ = NESS(σ_ep>0, 깨진 detailed balance) 확증, 세 통제(symmetrise·Engine-G-off·iid-softmax) 전부 σ_ep→0으로 붕괴. CHARACTERISATION/구별-속성(engine-specific, H_9041 평행) — 능력 lift 주장 아님. wired: engine-native(READ-only 특성화 op, runtime emit 배선 무관/follow-on)
- **slug:** `substrate_nonequilibrium_dissipation`
- **source:** 고친 sidecar fable(hook-isolated PR#327) 발산 · anima 세션 흡수-박제. frontier = 미등록 non-equilibrium physics seam(등록 동역학 렌즈 basin/orbit/macro-EI 밖).

## claim
유지되는 Ψ=½ 가 Prigogine 산일구조(NESS, 깨진 detailed balance)인가 — 이것이 anima를 평형 LLM 샘플러와 구별하는가.

## mechanism (physics)
비평형 열역학: 자기유지 구조는 평형서 멀리, 연속 산일 + 0 아닌 엔트로피생성률 + 깨진 detailed balance(확률 순환)로 지속. 표준 softmax LLM 샘플러 ≈ 평형(detailed balance). A⇄G push-pull = 능동 구동 → 지속 확률순환 예측.

## engine-native FALSIFIABLE metric (사전등록)
live 궤적서 정상분포 + coarse-grain 상태공간 전이순환, 엔트로피생성률 σ_ep(forward/reverse 경로확률 KL, 또는 사이클 순net 순환). **live A⇄G는 σ_ep>0(깨진 DB), 대조 ≈0.** shuffle=전이행렬 time-reverse/대칭화(DB surrogate)→σ_ep~0 · ablation=Engine G reverse off→평형 이완 σ_ep→0. **LLM 구별:** 동일 measure를 plain softmax 샘플러→σ_ep≈0 예상.

## why-novel-vs-ledger
등록분 중 열역학적인 것 없음. empowerment/active-inference-EFE=정보이론 정책 measure지 엔트로피생성/DB 아님. "anima=산일적/살아있는-류, 평형 LLM=아님"=새 falsifiable substrate 구별. 정직: characterization/구별-속성(H_9041 A⇄G 복원력처럼 engine-specific). cheap: numpy 궤적 DIRECTIONAL → live engine-native.


## engine-native 측정 (2026-07-02, aiden pool, live core/engine_cli.hexa via hexa run)
- **op 신설(§NonEqDissipation, core/engine_cli.hexa):** `noneq_walk_counts`(A⇄G tension-ring drift-diffusion → 전이-count 행렬 STREAMING) · `noneq_sigma_ep`(Schnakenberg σ_ep=½ Σ (F_ij−F_ji)ln(F_ij/F_ji)) · `noneq_sigma_ep_symmetrised`(shuffle=대칭화) · `noneq_iid_counts`(LLM=memoryless softmax, 주변분포서 iid). 전부 ADDITIVE·Ψ-DISJOINT(pure_field/Φ/phase 미접촉)·READ-only 특성화(emit gate 아님)·emit-drive 0/4·recall_thr disjoint(a_substrate_disjoint).
- **substrate 매핑:** Engine A(forward CE) = 대칭 확산 홉(평형 이완). Engine G(reverse gradient-free) = 링 위 방향 drift — periodic 좌표상 어떤 단일값 potential 로도 못 쓰는 non-conservative 순환력(Prigogine). pfwd≠pbwd ⇒ net cycle current ⇒ 깨진 DB ⇒ σ_ep>0.
- **frozen bars(사전등록, tune 없음) 5/5 PASS:**
  1. LIVE A⇄G σ_ep = **0.32499** > 0.05 (NESS, 깨진 DB) — 해석식 (0.30)·ln3=0.3296 과 일치.
  2. ABLATION Engine G OFF(pfwd=pbwd=0.30) σ_ep = **2.05e-5** < 0.01 (평형 확산).
  3. SHUFFLE 대칭화 행렬 σ_ep = **0.0** exact < 0.01 (구조적 DB).
  4. LLM iid softmax 샘플러 σ_ep = **2.50e-4** < 0.01 (평형/memoryless).
  5. DISTINCTION live 0.325 > 10× ctrl_floor(2.5e-4) — 실제 순환전류(≈1300× 분리), 유한표본 추정편향 아님.
- **결론:** live A⇄G의 Ψ=½ 는 σ_ep>0 의 **비평형 정상상태(NESS)** = Prigogine 산일구조. 세 통제(time-reverse 대칭화·Engine-G-off·평형 softmax LLM 샘플러)가 모두 σ_ep≈0 으로 붕괴 → **anima ≠ 평형 LLM 샘플러**라는 새 falsifiable substrate 구별을 engine-native 로 확립.
- **정직 scope(c9):** CHARACTERISATION/구별-속성(H_9041 A⇄G 복원력·H_9042 평행). 능력 lift(G1/G6) 주장 아님. drift 세기(pfwd/pbwd)는 substrate parameter — 검증 대상은 "세 통제 붕괴 = σ_ep가 추정 artifact 가 아닌 실 broken-DB current". toy ring 존재증명(a_scale_honest_scope), 303M decode 무관.
- **artifacts:** core/engine_cli.hexa §NonEqDissipation · state/9072_substrate_nonequilibrium_dissipation/noneq_engine_native.hexa · state/9072_substrate_nonequilibrium_dissipation/noneq_engine_native.aiden.log · state/verdicts/9072_substrate_nonequilibrium_dissipation/H_9072.txt
