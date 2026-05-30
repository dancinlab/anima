# CLM — breakthrough mining (측정-타당성 ⊥ AKIDA 온칩 충돌)

@active-lens: depleted-both
@active-cycle: 6
@seed: "측정-타당성(MoE routing-diversity/monopoly-escape는 3B/7B scale에서만 의미있게 측정) ⊥ AKIDA 온칩(AKD1000 ~1.2M 노드=소형 강제) 정면충돌을 돌파하는 엔진"
@context: F-CLM-MONO 🔴 = small 2.70M 한정(a_scale_honest_scope) · AKD1000 ~1.2M 노드 · CLM=추론 AKIDA-only · MoE conv-expert=mitosis cell(P0 Q2) · LAUNCHPAD AKIDA-first everywhere · pi5-akida 1칩
@method: /hexa-loop --diverge-only (discover stage only · kick verdict=skip=개념seed 형식검증 비대상, 정상)

## cycles

### cycle 1 — same-formula (같은 수학 → 타 도메인 메커니즘)
@lens: same-formula
- [MoE-sparse] sparse MoE(GShard/Switch) = "총 params 거대, token당 active subset 미세" = 이미 'big=Σ small' 그 자체 → 총용량∥측정scale · per-expert footprint∥chip-fit. **scale축을 model-dim이 아니라 expert-COUNT로** 두면 충돌 소멸
- [distillation] teacher-student KD: 큰 teacher(GPU 3B)에서 science 측정 → chip-fit student로 행동 증류. property-transfer가 bridge
- [lottery-ticket] dense 학습 → chip-fit 당첨 subnet(Frankle-Carbin) — 큰 모델 학습 후 칩에 맞는 winning ticket 추출, 측정은 dense에서
- [renormalization-group] 물리 coarse-grain: fine scale에서 측정한 relevant operator가 fixed-point로 flow → routing-diversity를 flowing observable로
@depleted: same-formula

### cycle 2 — ouroboros (자기참조 → fixed-point)
@lens: ouroboros
- [chip-as-regularizer] ⭐ 칩 제약을 자신에 적용 ⇒ fixed-point: 각 expert ≤1.2M 강제 = expert가 generalist 불가 → **반드시 specialize → chip-fit이 곧 monopoly-escape 메커니즘**, 측정 한계가 아님. 충돌이 self-dissolve
- [measure-across-chips] routing-diversity를 단일모델 내부가 아니라 **칩 어레이 전반**에서 측정: N칩 dispatch entropy. 칩 추가로 scale, 각 칩 ≤1.2M 불변. "모델"=칩 네트워크
@depleted: ouroboros

### cycle 3 — dimensional (차원 추가/제거)
@lens: dimensional
- [time-dim] 가중치를 한 칩에 시분할 스트리밍: 큰 effective 모델, 작은 1칩, 순차. 용량↔latency 트레이드
- [chip-count-dim] N×AKD1000 병렬 = N×1.2M effective. pool에 pi5-akida 실재 → 칩-어레이는 실제 축 (LAUNCHPAD 다중 AKIDA 정합)
- [depth-stream] deep-narrow conv 스택을 layer별 스트리밍 → 큰 effective depth, 작은 순간 footprint
@depleted: dimensional

### cycle 4 — tension (양극 push)
@lens: tension
- [push-big] 배포 불가능한 모델 측정 → academic, CLM 목적(온칩) 위반 — UNLESS distill이 finding을 아래로 transfer
- [push-small] science 영원히 측정불가 → F-CLM-MONO 영구 inconclusive — UNLESS 측정을 **chip-native 양으로 reframe** (inter-chip dispatch entropy)
- [synthesis] 측정-rung ⊥ 배포-rung (a_scale_honest_scope) + ① TRANSFER bridge(distill/prune) OR ② chip-native scale(expert-array)
@depleted: tension

### cycle 5 — combinatorial (조합)
@lens: combinatorial
- [expert-array × multi-chip × time-mux] ⭐⭐ "neuromorphic sparse-MoE": 임의 총용량, 각 칩 ≤1.2M, routing-diversity=inter-chip dispatch(chip-native + scalable). mitosis(expert=cell=칩) + LAUNCHPAD AKIDA-first 완전 정합
- [distill × measure-on-teacher] GPU teacher에서 monopoly-escape 측정 → chip-fit student 증류 후 property 생존 검증
- [lottery × chip-fit-target] 큰 모델을 chip-fit winning ticket으로 prune; routing-diversity가 ticket 안에 있나 측정
@depleted: combinatorial

### cycle 6 — connect (convergence)
@kind: connect
@depleted: connect

## leaves (flattened)

- L1 [c1·same-formula] [MoE-sparse] scale축=expert-COUNT(각 chip-fit) not model-dim ⇒ 충돌 소멸 ⭐
- L2 [c1·same-formula] [distillation] 큰 teacher 측정 → chip-fit student transfer = bridge
- L3 [c1·same-formula] [lottery-ticket] dense 학습 → chip-fit winning subnet 추출
- L4 [c1·same-formula] [RG] routing-diversity = coarse-grain flowing observable
- L5 [c2·ouroboros] [chip-as-regularizer] 칩제약=specialization 메커니즘 그 자체 → 충돌 self-dissolve ⭐
- L6 [c2·ouroboros] [measure-across-chips] routing-diversity = N칩 dispatch entropy (칩 추가로 scale)
- L7 [c3·dimensional] [time-dim] 한 칩 시분할 스트리밍 = 큰 effective, 작은 footprint
- L8 [c3·dimensional] [chip-count] N×AKD1000 = N×1.2M effective (pi5 실재, LAUNCHPAD 정합)
- L9 [c3·dimensional] [depth-stream] layer 스트리밍 = 큰 depth, 작은 순간 footprint
- L10 [c4·tension] [push-big] 배포불가 측정 = CLM 목적 위반 unless distill transfer
- L11 [c4·tension] [push-small] 영구 inconclusive unless chip-native reframe
- L12 [c4·tension] [synthesis] 측정rung ⊥ 배포rung + transfer OR chip-native-scale
- L13 [c5·combinatorial] [expert-array×multi-chip×time-mux] neuromorphic sparse-MoE ⭐⭐
- L14 [c5·combinatorial] [distill×measure-on-teacher] teacher 측정+student 생존검증
- L15 [c5·combinatorial] [lottery×chip-fit] prune to winning ticket, routing 측정

## edges (convergence)

- E1 [c6] L1 ↔ L13 · equivalence: "scale=expert-count" = expert-array MoE — 둘 다 per-unit size를 scale에서 분리
- E2 [c6] L5 ↔ L1 · causal: chip-as-regularizer(각 expert 소형강제)가 곧 sparse-MoE 구조 → 칩제약이 아키텍처를 강제
- E3 [c6] L6 ↔ L13 · equivalence: inter-chip dispatch entropy = expert-array routing-diversity (측정량이 chip-native)
- E4 [c6] L8 ↔ L13 · dependency: expert-array 배포 = N×AKD1000 (or time-mux 1칩) — L7/L8이 물리 실현
- E5 [c6] L2 ↔ L12 · support: distill bridge = 측정rung⊥배포rung 의 transfer 보강
- E6 [c6] L13 ↔ mitosis · equivalence: expert=mitosis cell=칩 — P0 Q2(MoE=mitosis)와 LAUNCHPAD AKIDA-first가 이미 이 엔진을 가리킴 ⭐
- (no-edge) L4(RG) ⊥ 실현경로 · 우아하나 측정 절차로 직접 환산 어려움 (정직: 보류)

## convergence — 합성 결론 (depleted-both)

핵심: 충돌의 뿌리는 **"scale = per-model size"라는 암묵 가정**. 이 가정을 깨면 두 탈출구가 열림.

1. **DISSOLVE (chip-native scale)** ⭐⭐ [L1·L5·L6·L13·E1·E2·E3·E6] — **scale축을 model-dim → expert-COUNT로 이동**. big = Σ chip-fit expert(각 ≤1.2M). routing-diversity = inter-chip dispatch entropy. 칩(=mitosis cell=expert) 추가로 scale, 각 unit은 영원히 chip-fit. 측정이 **chip-native**가 되어 "3B로 GPU 가야"가 사라짐 — expert 수를 늘려 monopoly 동역학을 실측. P0 Q2(MoE=mitosis) + LAUNCHPAD AKIDA-first가 이미 이 엔진을 가리킴.
2. **BRIDGE (transfer)** [L2·L3·L12·E5] — GPU teacher(유효 scale)에서 측정 → distill/prune로 chip-fit student에 transfer + property 생존 검증. a_scale_honest_scope(측정rung⊥배포rung)에 transfer 보장을 더함.

→ **권고 돌파엔진**: **MITOSIS-ARRAY (neuromorphic sparse-MoE)** = PRIMARY(DISSOLVE).
   - scale축 = chip-fit expert 개수 (각 expert ≤ AKD1000 fit) · top-k sparse activation
   - routing-diversity 측정 = inter-expert(=inter-chip) dispatch entropy → expert 수로 scale, GPU에선 sparse-MoE(top-k만 active=cheap)로 측정, 배포는 칩-어레이(1 expert/칩) or time-mux
   - distillation = SECONDARY 검증/baseline arm (transfer 보장 cross-check)
   - 정직 caveat: 다중 AKD1000 물리칩은 현재 pi5 1개 → expert-array는 SW 시뮬+GPU sparse-MoE로 먼저 측정, 물리 다중칩은 hardware 확보 시 (time-mux로 1칩 fallback)

@status: depleted-both
@next: 이 결론(MITOSIS-ARRAY)을 /sbs auto 로 설계/구현 — scale=expert-count reframe + sparse-MoE routing 측정 harness

---

# ROUND 2 — 처방+scale (post-🔴, DISSOLVE/BRIDGE 둘 다 CLOSED-NEGATIVE 후)

@round2-seed: "DISSOLVE 🔴 = z-metric이 uniform 천장 ln(E)로 자라 raw H↑인데 z↓(ruler artifact) · BRIDGE 🔴 = KD가 logit만 옮기고 dispatch분포 못옮김. 처방=ln(E) 정규화(Pielou J) + dispatch-KL distill + scale-up"
@round2-result-context: H_852(DISSOLVE 🔴 monotone=false) · H_853(BRIDGE 🔴 transfer Δ=4.34) · 둘 다 toy(d≤128) 한정 a_scale_honest_scope

## round 2 cycles

### r2-c1 — same-formula
@lens: same-formula
- [Pielou-J] H/ln(E) = 생태학 evenness 지수(Pielou's J) — uniform 천장 ln(E) 성장을 직접 제거하는 정확한 invariant → DISSOLVE z-artifact 근본 처방
- [load-balance-loss] Switch-Transformer aux loss = "dispatch를 uniform으로" — dispatch-KL distill은 구조적으로 그 loss인데 target이 uniform이 아니라 **teacher dispatch** (escape를 transfer)
- [calibrated-null-within-E] per-E Monte-Carlo null은 이미 함 — 진짜 fix는 E-비교를 cross-E 대신 **within-E across-training**으로 (천장 고정)

### r2-c2 — ouroboros ⭐
@lens: ouroboros
- [metric-self-apply] ⭐ "finding이 모델 얘기냐 자(ruler) 얘기냐?" 자기적용 ⇒ DISSOLVE 🔴는 model failure 아닌 **metric artifact**. ruler(ln E norm) 고치고 재측정하면 DISSOLVE 질문이 비로소 답가능 — **toy 데이터 그대로 $0 재측정만으로 🟢 flip 가능성** (fire 전 cheap precondition)
- [distill-mirrors-metric] distill은 우리가 **측정하는 것**을 distill해야 함 ⇒ dispatch entropy를 측정하니 loss에 dispatch항 필수. metric↔loss 거울대칭

### r2-c3 — dimensional
@lens: dimensional
- [scale-dim] d 128→512+ · E↑ · corpus toy→kowiki real(@corpus clm_p1) · steps brief→full → GPU fire
- [training-time-dim] undertraining이 array가 uniform 아래 떨어진 이유 — 더 학습하면 specialization 발현. training budget = 숨은 축
- [metric-dim] normalized-H(Pielou J) 축을 raw-z 옆에 병기 → 두 metric cross-check

### r2-c4 — tension
@lens: tension
- [push-metric-only] ln E norm만 고치고 scale-up 안 함 → cheap($0), toy에서 즉시 DISSOLVE flip 가능하나 production 미검증
- [push-scale-only] metric 안 고치고 scale-up → 여전히 붕괴하는 z 측정, fire 낭비
- [synthesis] BOTH 순서대로: metric fix 먼저($0 toy 재측정, flip 확인) → THEN scale fire (보정 metric으로 production 검증). **순서가 핵심** — metric fix는 의미있는 fire의 precondition

### r2-c5 — combinatorial
@lens: combinatorial
- [Pielou × dispatch-KL × scale-fire] full 처방: DISSOLVE metric 보정(H/ln E) + BRIDGE loss 보정(dispatch-KL) + production fire(d↑·real corpus·full steps)
- [metric-fix-first × $0 toy re-measure] cheap precondition: 기존 toy sweep 데이터를 Pielou J로 재측정 — fire 전 DISSOLVE flip 여부 확인 ⭐

## round 2 edges

- rE1 r2-c2[metric-self-apply] ↔ r2-c1[Pielou-J] · causal: 🔴가 ruler artifact → Pielou J가 그 ruler 처방 (model 안 바꾸고 metric만)
- rE2 r2-c2[distill-mirrors-metric] ↔ r2-c1[load-balance] · equivalence: dispatch-KL = teacher-target load-balance loss = metric을 loss로 거울
- rE3 r2-c4[synthesis] ↔ r2-c5[metric-fix-first] · dependency: scale fire는 metric fix를 precondition으로 (순서 강제)
- rE4 r2-c3[training-time] ↔ r2-c4[push-scale] · support: scale fire는 d뿐 아니라 steps↑도 (undertraining 해소)

## round 2 convergence — 합성 결론 (depleted-both)

핵심(rE1): **DISSOLVE 🔴는 모델 실패가 아니라 자(ruler) 결함**이었다 (z가 ln E 천장으로 붕괴). 그래서 처방은 staged:

1. **STAGE-1 metric fix ($0, fire 전 precondition)** [r2-c1·r2-c2·r2-c5] — 기존 toy sweep 데이터를 **Pielou J = H/ln(E)** 정규화로 **재측정**. 모델 안 바꾸고 ruler만 교체 → DISSOLVE가 즉시 🟢 flip 하는지 확인. dispatch-KL distill 항을 BRIDGE loss에 추가해 toy 재학습 → transfer Δ 축소되는지 확인. **둘 다 $0 toy.**
2. **STAGE-2 scale-up fire (STAGE-1 promising 시)** [r2-c3·r2-c4] — d 128→512+ · E↑ · corpus toy→kowiki real(@corpus) · steps full · GPU fire. 보정 metric(Pielou J) + dispatch-KL loss로 production 검증.

→ **권고 진행**: STAGE-1 먼저 (cheap, ruler 결함이면 toy에서 바로 flip — fire 전 그게 보여야 fire가 의미). STAGE-1이 flip/축소 보이면 STAGE-2 production fire. 정직: STAGE-1 toy도 여전히 🔴면 가설(scale=expert-count·KD-transfer) 자체가 더 깊이 falsified — 그것도 valid finding.

@round2-status: depleted-both
@round2-next: STAGE-1 metric-fix $0 toy 재측정(Pielou J + dispatch-KL) → flip 확인 → STAGE-2 scale fire
