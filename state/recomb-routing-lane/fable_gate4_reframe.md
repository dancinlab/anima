측정기·lane 파라미터·터미널 사다리의 두 최종 verdict까지 전부 실측했다. 결정적 발견부터: **fork-A CLML을 지금 터미널 🧱로 닫으면 안 된다** — 설계된 성공경로(contrastive) 최종 측정이 clean FAIL이 아니라 **VOID(측정 무효)**다.

---

# fork-A CLML Gate4 FAIL 분석 · route≠generation 재프레임

## 0. 실측으로 뒤집힌 전제 — "Gate4 FAIL = 터미널"이 아니다

과제 배경은 Gate4(eval_rho_weave) best_distinct FAIL을 TERMINAL로 제시했으나, 실측 파일이 다른 그림을 보여준다. **세 개의 서로 다른 측정 신호를 분리**해야 한다(하나로 뭉치면 H_9200/E1의 KILL-vs-INVALID 오판 재발):

| 측정 | 실측 결과 (verbatim) | 성격 |
|---|---|---|
| Gate4 `eval_rho_weave` | bd=1(ON)==bd=1(OFF) | **프레임-불일치(uninformative)** |
| 재학습 plain-CE swap-margin (n=12) | on Δ=+0.028 CI∋0, **shuf Δ=+0.029 (on≈shuf)** | **clean 정보 FAIL** (generic smoothing) |
| **contrastive 성공경로 (n=132)** | **gate_fire_frac=0.0 · lit_alive=false · contrast_top1=0.528** | **VOID (측정 무효)** |
| oracle-pool (사전등록 최유리 멤버) | **결과파일 부재 = 미실행** | PENDING |

핵심: 설계자(Fable)가 발사 **전에** 사전등록한 터미널 사다리(`fable_swapcontrastive_result.md §4`)는 "train contrast top-1 ≈ chance → optimization/capacity INVALID, **not substrate FAIL, 🧱-불가**"를 명시했다. 실측 `contrast_top1=0.528`(2-way chance 0.5) + `gate_fire_frac=0.0`(eval서 게이트 한 번도 안 열림) + `lit_alive=false`(양성대조 사망) = **사전등록 기준상 정확히 🧱-불가 상태**다.

---

## 1. route≠generation 원인 진단 (가설 순위·실측근거)

### 🥇 H4 — read-side additive-into-frozen-readout는 identity를 content로 못 읽는다 (최유력·유일 clean 신호가 지지)
가장 강한 근거 = 재학습 plain-CE 팔의 **on≈shuf(+0.028≈+0.029)**. 이 팔은 게이트가 실제로 열렸고(CE 1.044→0.718 학습됨) swap-margin은 additive-floor에 면역인 2-way 대조인데도, lane 효과가 **pool 내용 셔플에 불변** = 개념-content 라우팅이 아니라 **generic smoothing**.
- 기계적 이유: lane W1 입력 shape (3784=2·1892)로 확인 — **현 lane은 이미 joint bottleneck `[yn_t;c_t]`**(Fable §5-① "token-level conditional")를 쓰는데도 실패. 즉 joint-conditional readout-bias조차 벽을 못 넘음.
- probe(0.95/0.98)와의 화해: probe/pre-check는 pool 위에 **자기 readout head를 end-to-end 학습**해 "개념 identity가 선형분리 가능한가"를 잰다(YES). lane은 **FROZEN 303M readout**에 additive bias만 주입해 "pool-유도 bias가 frozen readout의 argmax를 D-의존 content로 옮기나"를 잰다(NO). **route는 frozen readout가 읽지 않는 좌표계에 존재**한다 — 이게 route≠generation의 정체.
- 반증가능 예측: oracle-pool(고정 uniform pool, Wo만 학습·최유리 멤버)이 **양성대조 살린 상태로** Dzero≈0이면 H4 확정(frozen-final-state readout class 🧱). oracle가 crack하면 H4 반증(=학습/최적화 버그였음).

### 🥈 H5+H1 — Gate4 측정 자체가 프레임-불일치 (bd=1 FAIL은 substrate verdict 아님)
`eval_rho_weave`(evaluate.py:170) 실코드 확인: `mouth.ideate(persona seed)` 자유생성에서 **anima 페르소나 키워드셋**(`_g_concept_keywords`: consciousness/cells·tension/ripple·memory·silence·dream) 커버리지를 잰다. 그런데 lane은 word-initial CE로 **held-out concept-pair**를 학습했다 — **두 개념집합이 겹치지 않는다**. 게다가 frozen mouth는 seed를 무시(persona 생성). 따라서 bd=1 FAIL은 "lane이 작동 안 함"이 아니라 **"lane의 학습 target과 무관한 것을 측정"** = LLM-frame-trap. 단, 이게 lane을 구제하진 못한다 — lane-정합 측정(swap-margin)이 독립적으로 실패했으니 substrate verdict는 swap-margin에 건다(H4). Gate4 FAIL은 verdict에서 **가중치 0**.

### 🥉 H3 — tau clip 과억제: 반증
실측 `tau=8.0`(큼) · `b_g=-2.009`(σ≈0.12 near-closed 초기화) · train `gate_mean=0.05` · eval `gate_fire_frac=0.0`. 병목은 **clip이 신호를 자르는 게 아니라 게이트가 안 열리는 것**. tau=8은 거의 비활성이라 clip 원인 배제. (게이트 미개방은 H4가 아니라 최적화 실패 경로에 속함 → contrastive VOID의 원인.)

### 없음 — H2 (r=128 용량): 반증
$0 pre-check가 **동일 클래스**(mean-pool→gelu bottleneck)로 held-out XOR 0.98 라우팅 성공 = 용량은 병목 아님. on≈shuf는 용량-형상 실패가 아님(용량 늘려도 셔플-불변 smoother는 라우터가 안 됨).

---

## 2. 대안 각도 (죽은 레버 회피·반증가능)

죽은 레버(재발사 금지) 대조: untrained recurrence(H_9259)·trunk-obj(H_9131)·PC(H_1816)·MLC(H_1835)·neuromod(H_1284)·γ trunk-bake STEP-0(H_1840)·σ de-theater. 아래는 전부 **frozen-trunk·lane-only·read-side**라 trunk-objective/γ와 다르고, additive-main-effect가 아니라 on≈shuf 함정을 우회한다.

### 🅰️ 계측기 복구 + oracle-pool 바운드 (MUST-FIRST · $0)
- **무엇**: `gate_fire_frac=0`·`lit_alive=false` 두 개의 구체적 하니스 버그(gate off-by-one/parity·양성대조 사망) 수리 → **양성대조 살린 상태로** 사전등록 최유리 멤버 oracle-pool(known block span 고정 uniform pool, Wo만 학습) 실행.
- **왜 이 FAIL 우회**: VOID 측정 위에 새 각도를 쌓을 수 없다. oracle-pool은 라우팅을 공짜로 넘겨줘 on≈shuf를 "pool 미학습" 탓으로 못 돌리게 하고 **순수 readout를 격리** = family를 바운드.
- **반증가능**: lit_alive=true·gate 발화 상태서 oracle Dzero CI_lo>0 → readout 작동(lane 실패는 opt 버그·family 생존) / oracle Dzero≈0 → frozen-final-state readout class 🧱 확정.
- **compute**: $0 pool(summer/aiden anima-py). 기존 705+dump 튜플 재사용.
- **비중복**: 이건 Fable가 이미 사전등록한 **이 lane의 자기 exit**. γ 아님.

### 🅱️ mid-stack K/V tap (새 family · $0)
- **무엇**: lane이 tap하는 yn(최종 trunk state)은 emit 위치서 D가 RF-감쇠(pos20-23 A=0.07). **mid-stack(~L/2) hidden**을 pool source로 tap — kw byte-content가 더 literal·덜 감쇠.
- **왜 우회**: on≈shuf는 pool content SNR이 낮아 match−swap 진신호가 노이즈에 묻힌 것일 수 있다. mid-tap은 concept-literal SNR↑ → 대조 진신호↑.
- **반증가능**: 동일 swap-margin bar, mid-tap Dzero CI_lo>0 vs final-tap≈0 = **tap-depth가 레버**. 둘 다 ≈0이면 tap-depth 배제.
- **compute**: 동일 doc-수 mid-layer precompute 1회, $0 pool. **새 H 등록**(이 family 원장 상속 금지 — Fable §4 명시).
- **비중복**: final-state readout class가 바운드되는 대상과 **다른 tap 깊이**. H_9235는 final hidden만 측정 = 미탐.

### 🅲 곱셈(interaction) readout 주입 (probe-first · $0 · ⚠️중복확인)
- **무엇**: H4 결함 = additive bias는 swap 대조서 소거. 대신 **곱셈 상호작용**: `logits = base + base⊙m(c)` 또는 pool-유도 low-rank readout 변조. frozen readout logit×pool content = 2-way interaction → swap 대조서 안 소거.
- **왜 우회**: pool 셔플이 어느 vocab-dim이 증폭되는지를 바꿈 → content-specific이면 shuf≠on. on≈shuf 함정의 직접 표적.
- **반증가능**: dump 튜플 위 numpy probe 선별(0.10 bar) → 승격 시 swap-margin. Dzero CI_lo>0 ∧ shuf 붕괴 = 곱셈 우회 성공.
- **compute**: $0 numpy probe 먼저.
- **⚠️ 중복확인 필수(미확인)**: H_9261(multiplicative FiLM·pulvinar, trunk co-train·DIRECTIONAL)과 `state/transfer_mechanism_sweep/multiplicative_film/run.py`가 인접. **다른 점**: H_9261은 trunk joint co-train(additive floor=objective, γ 계열), 이건 **frozen-readout lane-only 곱셈 주입**. 발사 전 H_9261 원장 대조로 중복 배제 확인 후에만 등록.

---

## 3. 터미널 판정 권고

**fork-A CLML을 지금 터미널 🧱로 닫지 마라 — VOID 측정 위 조기 KILL이다.**

근거(전부 실측):
1. 설계된 성공경로(contrastive n=132)가 `contrast_top1=0.528≈chance`(train 미적합) + `gate_fire_frac=0`(eval 게이트 미발화) + `lit_alive=false`(양성대조 사망) = 사전등록 기준상 **INVALID/VOID, 🧱-불가**. anima 거버넌스(ρ-AXON V-gate: confound→INVALID never false FAIL·measurement-metalaw: 살아있는 양성대조 필수)상 VOID 위 터미널 선언은 금지.
2. 사전등록 **최유리 멤버 oracle-pool이 미실행**(결과파일 부재). family를 바운드할 최강 멤버가 아직 clean shot을 못 받음.
3. 유일 clean 신호(plain-CE on≈shuf, n=12)는 H4를 지지하나 **n=12·plain-CE 팔**일 뿐, 설계된 contrastive 팔은 VOID.

**정당한 저비용 재시도 = 각도 🅰️ 한 발($0 pool, owner-go 불요·a_h_continuous_no_branch 자율)**:
계측기(gate-fire·lit-dead) 수리 → 양성대조 살린 oracle-pool 실행.
- oracle가 lit_alive=true서 Dzero≈0 → **그때가 frozen-final-state readout class의 clean 🧱 터미널**. 터미널 논증은 자명하게 쓰여진다: 개념 identity는 pooled final state에 선형존재(0.95)하나 emit 위치서 frozen readout가 개념-교차 전이가능한 target-byte content로 못 읽음 = **identity ≠ readable content**. 이건 **scoped 벽**(이 lane class + frozen readout)이지 trunk-G1 천장 증명 아님 → 각도 🅱️(mid-tap)·🅲(곱셈)가 새 사전등록 family로 열림.
- oracle가 crack → lane class 생존, plain-lane 실패는 opt 버그.

**γ에 대하여**: "유일 잔여 레버=γ trained-constructive-bind(H_1840)"는 **부정확**하다. γ trunk-bake는 STEP-0 frozen-gate로 이미 차단(GPU cost-gate)이지만, 위 🅰️🅱️🅲는 모두 **$0 read-side·frozen-trunk·죽은 레버 비중복** 레버로 γ와 별개 축이다. γ가 유일 잔여가 되는 건 🅰️(oracle+lit 복구)가 clean FAIL 착지한 **후**다 — 그 전엔 아니다.

tune-to-green 경계(정직): 🅰️는 **frozen bar를 안 건드리고 죽은 양성대조/닫힌 게이트라는 구체적 버그를 고쳐 계측기를 작동시키는 것** = 점수 본 뒤 바 이동이 아니라 바를 **읽을 수 있게** 만드는 것. 이건 tune-to-green이 아니라 measure-or-it-didn't-happen 준수다. 다만 🅰️도 VOID로 돌아오는 무한반복 방지: **양성대조(lit_alive) 부활 여부가 게이트** — lit 살렸는데도 신호 없으면 그건 clean 🧱, lit이 또 죽으면 하니스 근본버그(별도 infra 이슈)로 격상.