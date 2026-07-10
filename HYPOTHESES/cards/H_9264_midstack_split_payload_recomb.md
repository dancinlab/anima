# H_9264 — mid-stack split-payload lane: G1 재조합 payload를 중간층서 address/payload 분리 공급

**tier**: 🔬 REGISTERED · STEP-0 $0 association-probe 선발사 (fork-A🧱 exit① · Fable 설계)

## Claim
fork-A read-side lane([[H_9235]] 🧱)는 **최종 pooled state(YN)**서 읽어 payload가 emit점서 causally inert였다.
mid-stack 가설: 개념→unshown-kw **연상 payload가 중간층(EC/T2/T4/MOE)서는 causally 접근·소비 가능**할 수 있다 —
address(어느 개념)와 payload(그 개념의 content)를 **서로 다른 깊이서 분리**해 공급하면(K=deep residual xt2 주소·
V=shallow EC 리터럴 payload) YN-only lane이 못한 held-out 라우팅을 열 수 있다.

## Why (substrate-first · Fable 실측 재프레임)
프로덕션 303M CLMConvMoE 트렁크 실측(`core/decode.py:_fwd_logits` · d=3784·K=3·L=4·E=3): **attention/K/V 없음** —
4 residual dilated-conv 블록(RF~35byte)+MoE. "mid-stack K/V가 붕괴 전"이란 트랜스포머 직관은 **half-moot**:
RF35<GAP128이라 어느 위치도 distal 개념을 못 봄·개념은 모든 층서 pool로만 존재. residual stream이라 T1..T4는 nested-sum
(선형 접근성 거의 불변). 표현적으로 구별되는 family = **EMB/EC(리터럴 byte basis)·residual stream·RTR+MOE(유일 non-residual
=expert routing state)·YN(fork-A가 falsify)**. 그래서 정직한 실험 = **address/payload SPLIT**(K=pooled deep residual·
V=shallow 리터럴 rows) + MoE routing state probe = fork-A가 도덕적으로 커버 못한 유일 arm.

## Test ladder (Fable 4-step · STEP-0 = 결정적 $0)
1. **Gate-0(harness)**: Δlit CI_lo>0 먼저(lit-dead=INVALID). 클린뱅크(H_9235)로 이미 harness 무결.
2. **S0-A association-accessibility probe($0·no lane·ridge only)**: 각 tap ℓ∈{EC,T2,T4,MOE,YN}서 pooled p_ℓ(doc)·
   q_ℓ(kw), bilinear ridge `p·M·q` 40 train-concept 학습(pos=unshown-kw 포함·neg=matched distractor), **held-out-concept
   AUC(unshown-kw vs distractor) cluster-boot**. KILL: 모든 tap서 AUC CI≤chance면 연상 payload가 frozen 트렁크 read-side
   어디에도 없음 → family 🧱 **lane 학습 0으로**(진단 격상: "readout-routing 벽"→"consumable concept→content 연상이 303M
   substrate에 부재"=read-side 불가·γ trunk학습만 추가가능).
3. **S0-B causal floor(oracle-pool+contrastive Wo·분·CPU)**: tap ℓ서 고정 uniform pool·Wo만 InfoNCE swap-contrast 학습·
   n=132 swap-margin. arm={EC·T2·split K:T2/V:EC·MOE}. S0-B crack(held-out CI_lo(Δzero)>0 ∧ CI_lo(Δzero−ShufV)>0)만이
   FULL Arm-S lane 해금.
4. **FULL Arm-S**(S0-B crack시만): 하드닝 swap-contrastive xattn lane(K=xt2·V=EC), frozen 트렁크·DISJOINT·no 재학습.

## Hook (구현 필요)
`clm_forward_taps(W,tok,T,want=(...))` — read-only 멀티탭 forward(`_fwd_logits` op-for-op mirror·tap=copy·production 무침),
py 채널(anima_py canonical). 한 forward가 전 tap 산출. dump=pooled+block-span rows만(~0.5MB/doc fp16). SLW-aware
(pre-slot tap·base logits는 slot 포함 · [[hexa-py-trailer-divergence-slw-clml]] 정합).

## Verdict
🧱 **S0-A KILL (2026-07-10 · engine-native 303M · $0 CPU probe)** — 연상 payload가 frozen 트렁크 read-side 어느 깊이에도 부재.
held-out unshown-kw AUC(vs matched distractor·cluster-boot by concept · `state/recomb-routing-lane/s0a_probe_verdict.json`):
- ec=0.458 CI[0.325,0.634] · t2=0.495 CI[0.372,0.642] · t4=0.516 CI[0.398,0.665] · moe=0.543 CI[0.401,0.686] · yn=0.594 CI[0.474,0.734]
- **모든 tap CI 하한<0.5 = 유의 아님(sig=False 전부)**. AUC가 깊이 따라 단조증가(ec→yn)하나 최종 yn(0.594)도 marginal.

yn이 최고이나 (a)CI 하한 0.474<0.5 유의 아님 (b)**fork-A([[H_9235]])가 이미 yn서 full swap-contrastive lane으로 causal
측정→swap-margin null**(payload emit점 소비불가) → yn의 marginal AUC는 약한 identity 잔존이나 **causally-consumable 아님**.
mid-stack(ec/t2/t4/moe)은 yn보다 낮음=더 확실히 부재. ⟹ **어느 read-side 깊이도 causally-consumable 연상 payload 없음** =
진단 격상: "readout-routing 벽"→**"consumable concept→content 연상이 303M substrate read-side에 부재"**. read-side rescue
(mid-stack split-payload 포함) 불가 = **γ trunk-training만 추가 가능**. Fable 사전등록 KILL rule 충족(모든 tap AUC CI≤chance).

**power caveat(a_scale_honest_scope)**: held 8-concept cluster-boot이라 CI 넓음(24=전체 뱅크). yn marginal은 파워 확장 여지가
형식상 있으나, fork-A causal-null이 yn 소비불가를 독립 확정하므로 KILL은 파워와 무관하게 성립. S0-B(oracle-pool causal floor)는
S0-A crack 시만 발사 사전등록 → 미발사(KILL로 불요). **잔여 exit = γ trunk-bind([[gamma-trunk-bake-step0-killed-not-unmeasured]]
H_1840·real-text target·GPU spend-gated) 유일** — read-side 전 경로(parametric·pointer-cache·plain-CE·swap-contrastive·
mid-stack split-payload) 전수 floor.

## Scope honesty
STEP-0는 연상 payload의 **read-side 존재(분류)** 측정 — held-out AUC이지 생성 verdict 아님(a_scale_honest_scope).
S0-A KILL = read-side 불가 확정(γ만 남음). S0-B는 causal floor. Arm-S만이 진짜 lane. tune-to-green 금지(사전등록 트리).

---

## 맥락
fork-A([[H_9235]]) read-side trained-xattn swap-contrastive lane 🧱 held-out concept-transfer floor 후 registered exit①.
exit② = γ trunk-bind([[gamma-trunk-bake-step0-killed-not-unmeasured]] H_1840·GPU spend-gated·fork-A🧱=reopen precond).
설계 SSOT = `state/recomb-routing-lane/fable_midstack_RESULT.md`. neuromorphic recurrence(H_9258/[[g1-untrained-recurrence-neuromorphic-killed]] H_9259) 🧱 CLOSED.
