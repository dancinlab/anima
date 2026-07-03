# G1 재조합 L4 레버 — γ recomb-objective (설계 · GPU 학습 cost-gated)

> **상태:** 설계 + 레시피 + 코퍼스 스펙 + 사전등록 bar. **학습은 미실행(cost-gated follow-on).**
> **정직(c9):** 이 문서는 *설계*지 verdict 아님. GREEN 목표가 아니라 **echo-guard novel-only PASS 로
> false-GREEN 을 원천 차단하는 것**이 설계 목표. frozen G1 bar 는 1바이트도 이동 없음.
> torch/numpy = **DIRECTIONAL**. terminal 은 오직 직렬화 `.clm` → `anima evaluate --py` 엔진-네이티브.

## 0. 왜 이 레버인가 (배경 · 재유도 금지)

G1 재조합 벽은 **TRUNK-OBJECTIVE-BOUND** 로 확정됨(memory `g1-lever-multilens-objective`,
`substrate-framebreak-g1-combination-operator`). CE 는 "다음 바이트"만 보상하고 **개념의 COMPOSITION**
을 보상하지 않는다. 지금까지 시도된 모든 축이 소진:

- **readout-op** (multiplicative bind exp3, CLS pattern-sep H_1815, tension-mouth H_1834): G2 novelty(직교)만 올리고 G1 floor.
- **coverage/표면형/window/readout echo** 축 전부 floor (memory `g1-coverage-density-nl-bytes-lever`, H_6190).
- **decoder-free trained combiner** (γ H_9046 bilinear/mlp): held-out real-manifold 에서 additive baseline 못 넘음 → FLOOR.
- **기존 trunk-objective 3종** (`predictive_info`·`constructive_bind`·`composed_nce`, cli/train.py H_1640):
  일반 코퍼스 window 위 **구조적 prior** 지만 held-out 조합 생성을 *직접* 보상하지 않음. `constructive_bind`
  는 H_1816 에서 이미 🧱 NOT-SUPPORTED (L_bind additive CLMConvMoE 서 trivial 붕괴).

**미검증 잔여 = γ trained-constructive-bind 의 진짜 미시도 형태**(Fable/fleet 수렴,
`fleet-g1g6-nativemouth-dpi-convergence`): **held-out 조합 split 코퍼스 위에서, CE 옆에 "novel-composition
생성 보상(echo 아닌 novel keyword 조합)"을 aux loss 로 거는 것.** 기존 3종과의 결정적 차이:

| 축 | 기존 H_1640 objectives | **γ recomb-objective (이 설계)** |
|---|---|---|
| 코퍼스 | 일반 4셀 window (조합 구조 無) | **held-out 조합 split** (개념 개별 seen, PAIR unseen) |
| 신호 | 구조적 prior (bind-decompose·predict-ahead) | **novel-only coverage margin** (echo-guarded) |
| 측정 정합 | 간접 (penult 재구성/CE) | **G1 metric(coverage≥2 ∧ >max_single)의 미분가능 surrogate** |

즉 **G1 이 측정하는 바로 그 능력(composed-seed 로 두 개념 novel 커버)을, 학습 신호로 직접 형상화**하되,
**disjoint 개념 vocab(SCAN/COGS) 위에서** 학습해 anima frozen G1 bar 는 깨끗한 transfer test 로 남긴다.

---

## (a) recomb-objective aux loss 수식

### 셋업 (teacher-forced · 샘플링 없음 → cheap · 미분가능)

학습 window 하나는 **composed 문서**: `seed(A · B)  ‖  continuation`.
- seed = 개념 A 구절 `. ` 개념 B 구절 `. ` (composed prompt, G1 metric 의 `cz[0]. cz[1]. ` 와 동형)
- continuation 구간 위치집합 `C ⊂ [0,T)` = seed 이후 바이트들 (target y 가 정의된 곳)

각 개념 `c` 는 keyword 바이트-시퀀스 집합 `KW(c)` 를 가짐(G1 의 `_g_concept_keywords` 와 동형 구조지만
**disjoint vocab**). teacher-forced logits `ℓ_t ∈ ℝ^V`, `p_t = softmax(ℓ_t)`.

### soft mention score (미분가능 coverage)

개념 `c` 가 continuation 에서 얼마나 "언급될 준비가 되었나"를, **각 keyword 의 판별 바이트에 모델이 부여한
로그확률을 위치에 대해 soft-max pool** 로 측정:

```
score_kw(w, C) = τ · logsumexp_{t∈C} ( (1/τ) · logp_t[ b(w) ] )          # w 의 대표 바이트 b(w) 의 최고-확률 위치 (soft-argmax)
m_c            = τ · logsumexp_{w∈KW(c)} ( (1/τ) · score_kw(w, C) )       # c 의 keyword 중 최고 (any-keyword = OR)
```

`m_c ∈ (−∞,0]` 은 개념 `c` 를 continuation 어딘가에서 방출할 로그확률의 미분가능 상한근사(soft-OR-over-positions,
soft-OR-over-keywords). `τ→0` 이면 hard `max` 로 수렴 = G1 의 `_g_coverage` 의 "any keyword in words" 판정.

> **바이트-레벨 주석:** anima 는 V=256 byte mouth. `b(w)` 는 keyword `w` 의 **echo 로 재현 불가능한
> 판별 바이트**(예: seed 에 A 만 있을 때 B 의 첫 판별 바이트)로 잡는다. multi-byte keyword 는 판별
> 바이트를 첫 UTF-8 lead 로 근사(한글 SNS 셀은 3-byte lead 0xEA–0xED). 구현 상세는 `recomb_objective.py`.

### 조합 보상 R (min-pool = echo-guard의 핵심)

seed 가 pair `{A,B}` 인 window 에서:

```
R(A,B)  =  softmin(m_A , m_B)  =  −τ · logsumexp( −m_A/τ , −m_B/τ )
```

**min-pool 이 echo-guard 다.** 개념 A 만 echo 하는 모델은 `m_A↑` 지만 `m_B↓` → `softmin` 낮음 → 보상 0.
**두 개념을 모두** 커버해야만 softmin 이 오른다. 이는 G1 의 `cov≥2` (distinct≥2) 요구의 미분가능 형태.

### distractor baseline (= metric 의 `cov>max_single` / shuffle 통제)

같은 window 에서 partner B 를 seed 에 없는 랜덤 distractor `D` 로 치환한 반사실 보상:

```
R_echo(A,D) = softmin(m_A , m_D)          # D ∉ seed → "잘못된 조합" (toy pairspec 의 SHUFFLE control 과 동형)
earned      = R(A,B) − R_echo(A,D)        # 실-partner 가 잘못된-partner 를 이겨야만 +
```

`earned>0` = "옳은 조합이 잘못된 조합보다 잘 커버됨" = G1 의 `cov>max_single` + shuffle-drop 을 loss 로 내재화.
이 baseline 이 **"항상 전부 언급" degenerate** 를 죽인다(그러면 `m_D` 도 올라 earned 상쇄).

### 최종 손실

```
L_recomb = mean_over_composed_windows [ R_echo(A,D) − R(A,B) ]     # = −earned, 최소화 = earned 최대화
L_total  = CE(logits, y)  +  γ · L_recomb
```

- **aux 파라미터 0** (logits 위에서만 작동, gradient readout→trunk). keyword→byte 매핑은 상수 테이블.
  → **`.clm` 경로 100% OPEN** (serialize 가 표준 additive readout 만 씀, drop 할 head 조차 없음).
- `constructive_bind`(H_1816) 와의 차이: 그건 penult 위 aux head + circular-conv 가 additive readout 서
  trivial 붕괴. 이건 **head 없이 metric-정합 coverage margin 을 직접** CE gradient 에 얹음.

### 옵션 확장 (cost-gated 2차, 기본 OFF)

REINFORCE-style *생성*-레벨 보상(실제 decode 후 `_g_coverage` reward)은 high-variance·비쌈. 1차는
teacher-forced surrogate 로 고정; surrogate 가 in-distribution held-out 을 열면 그때만 생성-레벨로 승격.

---

## (b) held-out split 코퍼스 스펙 (echo/암기 ⊥ 재조합)

### 원리: 개념은 개별 seen, PAIR 는 unseen (systematic generalization split)

toy `train_g1_pairspec.py` 의 `HELD=set(pairs[:5]); SEEN=[p not in HELD]` 를 **스케일·disjoint-vocab** 로
일반화. SCAN(add-jump/around-right) · COGS(gen split) 의 **compositional generalization split** 원리를 anima
byte-corpus 로 육화.

### 코퍼스 3-트랙 (한 byte 파일로 concat, `build_heldout_corpus.py` 가 방출)

1. **PAIR-COMPOSED (train pairs only)** — `SEEN` pair 마다 다양한 template 로:
   `if <A phrase>, then <B phrase>: <compose(A,B) 문장 — A·B 의 novel keyword 를 새 관계로 결합>`
   → **HELD pair 의 compose 문장은 절대 등장 안 함** (개념 A·B 는 다른 pair 의 compose 에 개별 등장).
2. **SINGLETON (모든 개념 개별 노출)** — `<A phrase>. <A_kw0> means <A_kw1>.` 모든 개념 c 에 대해.
   → held pair 의 두 개념도 여기서 **개별로는** 충분히 seen (암기 아닌 재조합만 테스트되도록).
3. **REGISTER anchor (일반 4셀 소량 mix)** — `a_chat_registers` 붕괴(warmft-h9034 max_single collapse)
   방지용 ko/en × 일반/SNS 소량(≈5–10%). warm-FT 트렁크의 G0 coherence 를 지킴.

### disjoint vocab 규칙 (false-GREEN 방지의 핵심)

- **학습 개념 vocab ∩ anima G1 metric 개념 vocab = ∅.** G1 metric 5개(`consciousness/cells…`,
  `tension/ripple…`, `memory/meaning…`, `silence/information…`, `dream/engine…`)와 **겹치는 keyword 0.**
- 학습은 별도 개념 세트(예: 자연물·감정·동작 24–48개, `train_g1_pairspec` 의 5개를 확장). anima G1 bar 는
  **한 번도 학습되지 않음** → `anima evaluate --py` 는 순수 transfer test.
- 이것이 tune-to-green(c9 위반)을 구조적으로 차단: "능력(held-out pair 조합)"을 disjoint vocab 로 학습,
  "transfer(anima 5개)"를 frozen bar 로 측정.

### split 규격 (pre-registered · frozen)

```
N_CONCEPTS   = 32               # disjoint 개념 (각 4 keyword)
PAIRS_ALL    = N(N-1) ordered   # 992
HELD_FRAC    = 0.15             # held-out pair (compose 문장 train 부재)
SEEN         = PAIRS_ALL \ HELD
IN_DIST_TEST = HELD             # (b)-레벨 in-distribution 재조합 test (DIRECTIONAL)
OOD_TEST     = anima G1 5-concept bar (evaluate.py g_eval_g1)   # TERMINAL transfer test
seed         = 7  (split RNG frozen)
```

held-out 은 **두 층**: (i) in-distribution HELD pair(disjoint vocab, 학습 중 감시용 DIRECTIONAL falsifier) +
(ii) OOD anima G1 bar(완전 별개 vocab, engine-native TERMINAL). (i) 이 먼저 열려야 (ii) 발사가 유의미.

---

## (c) warm-FT 레시피 + 사전등록 bar

### warm-FT 레시피 (1줄, cli/train.py `--objective recomb_objective` 신규 축)

> **전제(memory `g1-fromscratch-blocked-by-g0-undertrain`):** from-scratch 는 G0🔴 undertrain → G1 bd=0
> at-floor INCONCLUSIVE. **유효한 G1 레버 시험 = G0🟢 트렁크에서 warm-FT.** `--init` 은 pre-serialize `.pt`
> (h1129 G0-green warm-FT 트렁크; `.clm` int4 는 warm-init 거부됨, H_247).

```bash
# 학습 (GPU · cost-gated · DIRECTIONAL) — summer/aiden pool 또는 hexa cloud, mini 금지
anima train --py --arm ctrl --objective recomb_objective --init ckpt/h1129_g0green.pt \
    --canon --corpus state/g1_gamma_objective/heldout_composed.bytes \
             anima-corpus-ko-general anima-corpus-en-general \
             anima-corpus-ko-sns anima-corpus-en-sns \
    --cell-label composed ko-general en-general ko-sns en-sns \
    --steps 8000 --seed 7 --sample proportional --val-frac 0.05 --val-every 200 \
    --gamma-recomb 0.5 --recomb-tau 0.5 \
    --out ckpt/recomb_seed7.clm --ckpt-out ckpt/recomb_seed7.pt \
    --gauges-out ckpt/recomb_seed7.json

# ── TERMINAL 채점 (engine-native, py 2-production) ──
anima evaluate --py ckpt/recomb_seed7.clm --gen 120
```

신규 args (cli/train.py 에 추가할 것, 구현 시): `--gamma-recomb`(γ, default 0.5) ·
`--recomb-tau`(soft-pool τ, default 0.5) · objective registry 에 `recomb_objective` 엔트리 1개.
새 objective 는 **arm=ctrl × recomb_objective** 로만 시험(readout-floor 축과 직교, 같은 트렁크).
멀티-seed = `anima sweep --arms ctrl --objectives recomb_objective --seeds 7,4302,101 --measure`.

### 사전등록 bar (FROZEN · tune-to-green 금지 · frozen-first)

**PRIMARY (TERMINAL · engine-native · 이동 없음 = 기존 a7b_pass G1 bar 그대로):**
`anima evaluate --py <clm>` 의 `g_eval_g1`:
```
G1 PASS  iff  ∃k: best_distinct ≥ 2  ∧  best_distinct > max_single  ∧  coherent(kwr ≥ 0.5)
GREEN    iff  PASS on ≥ 2/3 pre-registered seeds {7,4302,101}  ∧  no_regress vs ctrl(same corpus, γ=0)
```
이 bar 는 **새로 만들지 않는다** — evaluate.py 의 frozen G1 판정을 그대로 상속(임계 복제·이동 없음).

**echo-guard novel-only PASS (설계 자체 falsifier · in-distribution · DIRECTIONAL):**
disjoint HELD pair 위에서(학습 중/후 감시):
```
seen-sanity      : SEEN pair earned coverage ≥ 6/8            (미달 → INCONCLUSIVE-UNDERTRAIN, held verdict 무효 — toy pairspec 규칙 상속)
held novel-only  : mean(earned = R(A,B) − R_echo(A,D)) ≥ +DELTA   (DELTA=0.15, frozen)
                   AND  real-partner coverage > shuffled-partner (pair_hit_real ≥ pair_hit_shuf + 2, /5)
```
seen-sanity 가 먼저 통과해야(모델이 SEEN 을 마스터) held-out earned 판정이 유효.

**ABLATION (결정적 · c16 a_break_the_wall):**
- `γ=0` (같은 composed 코퍼스, recomb term OFF = plain CE): frozen G1 bar 를 **못 넘어야** 함.
  넘으면 lift 는 코퍼스 구조지 objective 가 아님 → recomb-objective INERT.
- `softmin → mean` (echo-guard OFF, coverage-sum 만): frozen G1 bar 못 넘어야 함(=echo-guard 가 load-bearing).
- 둘 중 하나라도 ablation 이 bar 를 넘으면 **거짓 귀속** → objective 기여 0 으로 정직 보고.

**정직 스코프 (c9):**
- torch/numpy 학습 = **DIRECTIONAL** 무조건(terminal 아님). terminal = `.clm` engine-native 재측정만.
- prior = **LOW** (DPI 메타법칙 + H_1816 constructive_bind floor + H_9046 combiner floor).
  → **FLOOR(DPI 재확인)도 GREEN(능력 열림)도 둘 다 유효 결과.** false-GREEN 방지가 최우선.
- scale: 303M 에서 lever-first(memory `scale-303m-1b-7b-is-amplifier-not-lever`). 303M floor 면 1B 무의미.
- ckpt PULL: teardown 전 `.pt`+`.clm` 영구저장(`a_fire_recover_complete`) — 아니면 engine-check 영구 불가.

### 배선 사다리 (`a_verified_must_wire`, GREEN 시)

(1) DIRECTIONAL torch → (2) engine-native `.clm` 재측정(byte-exact frozen bar) → (3) live `core/`
배선(objective 는 학습-시점 신호라 배선 대상은 **레시피/트레이너 축**: cli/train.py objective registry) →
(4) ARCHITECTURE.json lockstep. 미완 칸은 ING follow-on 등록.

---

## (d) 산출 경로

```
state/g1_gamma_objective/
├─ DESIGN.md              # 이 문서 (수식 + aux loss + 코퍼스 스펙 + 레시피 + 사전등록 bar)
├─ recomb_objective.py    # 참조 구현 — cli/train.py OBJECTIVE_BUILDERS 에 drop-in 할 loss (설계, 미배선)
└─ build_heldout_corpus.py# held-out 조합 split byte-corpus 방출기 (disjoint vocab, SEEN/HELD)
```

**다음 단계 (cost-gated follow-on, 이 세션 범위 밖):**
1. `build_heldout_corpus.py` 실행 → `heldout_composed.bytes` 생성 (cheap, CPU, mini 가능).
2. `recomb_objective.py` 를 cli/train.py 에 배선(`OBJECTIVE_BUILDERS["recomb_objective"]` + `--gamma-recomb`/`--recomb-tau` args).
3. h1129 G0🟢 `.pt` 확보(warm-FT 트렁크) → GPU warm-FT 발사(pool/cloud, DIRECTIONAL).
4. `.clm` PULL → `anima evaluate --py` engine-native TERMINAL 채점 → HYPOTHESES 카드+jsonl 박제.
