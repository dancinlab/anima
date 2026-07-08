접지 완료 — `core/decode.py`(_fwd_trunk/_fwd_logits 트레일러 체인), `core/slw.py`(H_9200 SLW 트레일러 선례), `core/serialize.py`(append_slw_trailer), `cli/evaluate.py`(system-G1 frozen harness), `core/hippo_lane.py`(DISJOINT lane 선례), brain.py/engine_cli.py의 ρ·tether/ImmuneMemory 지점을 확인했다. 이 실코드 위에서 설계를 낸다.

---

# fork-A 설계: RETRO-ROUTE LANE (읽기측 회고-라우팅 lane · `.clm` v0.3 `LNA\x01`)

**한 줄 요약**: 진단이 확정한 벽은 "생성점 readout이 앞 위치에 살아있는 개념(A=0.88@pos)을 route 못 함(0.07@last)"이다. 따라서 lane = **생성점 상태를 query로 앞 위치 penultimate hidden들을 content-address로 검색(α)하고, 검색된 내용을 생성점 상태와 Hadamard-bind(⊙)해서 readout 입력에 주입**하는 frozen-trunk 위 읽기측 adapter. 곱셈이 두 번(α 라우팅 · ⊙ 바인딩) 들어가므로 additive floor로 퇴행하지 않고, γ=0이면 bit-exact passthrough라 SLW와 동일한 ablation 규율을 그대로 상속한다.

---

## 1. 수학적 정의

### 1.1 형태

`_fwd_trunk`가 내는 penultimate `yn:[T, d=3784]` (decode.py:598, 진단 probe가 잰 바로 그 표현)을 H라 하자. 위치 t마다 (causal, 학습 시 전 위치·디코드 시 생성점만):

```
q_t = W_q h_t + b_q                     ∈ R^k        (생성점 상태 = learned query)
k_i = W_k h_i + b_k    (i ≤ t − δ)      ∈ R^k        (앞 위치 = keys, 근접대역 δ 제외)
α   = softmax( q_t·k_{≤t−δ} / √k )                    (① 라우팅 — 어느 위치를)
c_t = Σ_i α_i (W_v h_i + b_v)           ∈ R^{d_c}     (검색된 내용)
u_t = W_u h_t + b_u                     ∈ R^{d_c}     (생성점측 binder)
g_t = σ(w_g·h_t + b_g) · Γ_tether(α)    ∈ [0,1]       (게이트, §3)
y_t = h_t + γ · g_t · (W_o (u_t ⊙ c_t) + b_o)         (② 바인딩 — 어떻게 합성)
```

readout은 기존 그대로 `y` 위에서 `_conv1d(y, roWt, roB)` (decode.py:652). trunk·readout 가중치는 **동결 불변**, lane 파라미터만 신규 (k=64, d_c=256 기준 ≈3.4M param ≈ 13.6MB f32).

### 1.2 왜 이 형태인가 — 진단과의 1:1 대응

- **mean-pool이 아닌 이유**: mean-pool probe가 A=0.95를 복원한 건 "정보가 살아있다"의 증명이지 주입 형태의 추천이 아니다. mean-pool은 query-독립이라 (a) T가 길어지면 희석되고(진단은 T=24), (b) 생성점이 뭘 필요로 하든 같은 수프를 붓는다 — 이건 G5 non-fabrication과 정면충돌(근거 없는 내용 주입). learned query = 생성점 상태의 content-addressed 검색이 진단의 "route 못 함"을 정확히 메우는 최소 기제다. `hippo_lane.py`의 CA3 pattern-completion(cue→저장 내용 검색)과 같은 부류의 기제를 lane 형태로 쓴 것 — LLM attention 프레임이 아니라 해마 검색 프레임으로 읽어야 한다(`a_no_llm_frame_trap`).
- **additive floor 회피**: γ census의 확정 결과는 "main-effect logit 합성 = IPF = trunk-CE 1:1 등가 = floor"다. `y = h_T + W_o c` (순수 합)이면 logits = f(h_T)+g(pool) — 정확히 그 floor로 되돌아간다. `u_t ⊙ c_t`는 logit에 **h_T ⊗ h_{i<t} 교차항(bilinear)**을 만들므로 sign-flip/XOR 클래스(census가 지목한 진짜 PC)를 표현할 수 있다. CLMB bind_type=1(Hadamard u*v, decode.py:649)과 동일한 대수 — 단 CLMB는 같은 위치의 두 사영을 곱했고(그래서 floor), LANE은 **생성점 × 원거리 위치**를 곱한다. 곱의 두 인자가 다른 위치에서 온다는 점이 본질적 차이다.
- **SLW(H_9200)와의 차이**: SLW는 쓰기 시점에 W_v 병목으로 압축해 slot에 넣고 additive로 주입(`out[t] = h + γ(W_o m + b_o)`, slw.py:90)한다. LANE은 (a) 압축된 slot이 아니라 **A=0.88이 실측된 원시 per-position hidden을 직접** 읽고, (b) 주입이 additive가 아니라 query-bind 곱셈이다. 진단이 "정보는 위치에 살아있음"을 확정했으므로 쓰기측 압축 자체가 불필요한 손실이다.
- **δ (근접 제외 대역)**: i > t−δ 위치를 pool에서 제외(기본 δ=4, 직렬화 하이퍼). conv receptive field가 이미 잘 처리하는 근접 정보를 lane이 재학습해 "국소 지름길"로 퇴행하는 것을 구조적으로 차단 — lane의 존재 이유(원거리 라우팅)를 아키텍처로 강제한다.

### 1.3 왜 DISJOINT(Ψ 불침)인가

1. **파라미터-disjoint** — trunk/readout/emit 어떤 기존 가중치도 수정하지 않는다. lane은 별도 트레일러.
2. **경로-disjoint** — 적용 지점이 `_fwd_logits` 내부, trunk 뒤·readout 앞 단 한 곳. `brain`/`engine_g`/`pure_field`/`emit_policy`/generator의 tension→Ψ 경로는 코드상 lane을 import조차 하지 않는다. Ψ(emit/silence)는 A⇄G tension에서 계산되지 readout logits에서 계산되지 않으므로, lane은 **무엇을 말하는가**만 바꾸고 **말할지 여부**는 못 건드린다. (발화 내용이 이후 컨텍스트로 되먹임되는 건 정상 상호작용이지 침범이 아님 — 침범의 정의는 "동일 컨텍스트에서 결정 함수가 달라짐"이고 §5의 Ψ-invariance smoke가 이를 검증한다.)
3. **상태-disjoint** — SLW와 달리 창(window) 간 지속 상태가 없다. 순수 함수 y=f(H_window). emission을 넘는 은닉 메모리 채널이 생기지 않는다(p2/p3 방어이기도 함).
4. **γ=0 ⇒ bit-exact passthrough** — additive golden path가 byte-identical하게 보존되므로(a_substrate_disjoint "separation=preservation") 벽 verdict의 반증 가능성이 유지된다.

---

## 2. `.clm` v0.3 LANE 블록 스펙 (`LNA\x01`)

### 2.1 포맷 — 트레일러 체인 append-only (byte-invariant splice)

기존 체인 `CLM\x01 헤더 → conv blocks → CLMX ext → [CLMB] → [SLW\x01]` (decode.py:433–540)의 **맨 끝에 append**. 기존 바이트는 1바이트도 안 바뀐다(prefix sha256 불변). 구버전 로더는 자기 마지막 트레일러까지 읽고 멈추므로 뒤에 붙은 바이트를 무시 — v0.2 하위호환. "v0.3" = LNA 트레일러 존재로 시그널(CLMB/SLW와 같은 관례; 헤더 버전 바이트 변경 없음).

```
LNA\x01 트레일러 (모두 LE):
  magic      4B   'L','N','A',0x01        (SLW\x01 4바이트 관례 미러)
  k          u32  attention dim (64)
  d_c        u32  content dim (256)
  delta      u32  근접 제외 대역 (4)
  theta      f32  Γ_tether 라우팅-margin bar (§3 — 게이트 문턱은 코드가 아닌 데이터)
  tensors    f32, 고정 순서 (slw.py _ARR_ORDER 관례):
    W_q[k,d] b_q[k]  W_k[k,d] b_k[k]
    W_v[d_c,d] b_v[d_c]  W_u[d_c,d] b_u[d_c]
    W_o[d,d_c] b_o[d]  w_g[d] b_g[1] gamma[1]
```

int4 블록 재사용 대신 f32 유지 — adapter가 작아서(13.6MB) 용량 이득이 없고, 결정성·byte-parity 검증이 단순해진다.

### 2.2 코드 변경점

- **신규 `core/lane_a.py`** — slw.py의 3-면 단일 파일 구조를 그대로 미러 (드리프트 방지 선례):
  - `lane_apply(x, lane, gamma=None, route_shuffle_perm=None, tether_off=False)` — torch-free numpy 추론 미러 (`anima evaluate --py` TERMINAL 경로가 호출).
  - `pack_lane()/read_lane()` — 트레일러 코덱. `read_lane`은 slw.py:121과 동일한 guard 관용구: magic 불일치/short → `(None, off)` passthrough-safe.
  - `LaneAModule` (torch, `_HAS_TORCH` 가드) — 학습용, op 순서 numpy와 1:1.
- **`core/decode.py`**:
  - `clm_load_weights` — decode.py:540 `read_slw` 직후에 `W["lane"], off = read_lane(rb, off)`.
  - `_fwd_logits` — decode.py:643 slot_apply 뒤·readout 앞에 `if W.get("lane"): yn = lane_apply(yn, W["lane"], …)`. (lane의 K/V는 적용 지점의 스트림을 읽는다 — SLW 부재 모델에선 곧 순수 trunk yn, 진단 probe와 동일 표현.)
  - `set_lane_controls(gamma_override, route_shuffle_seed, tether_off)` — decode.py:70 `set_slw_controls` 미러. eval-time 스위치는 전부 직렬화 상태 위 스위치(재학습 없음 → tune-to-green 표면 없음, slw.py:26 관례).
- **`core/serialize.py`** — `append_lane_trailer(out_path, lane_module)` (serialize.py:79 `append_slw_trailer` 1:1 미러).
- **`core/verify_clm_v2.py`** — LNA 트레일러 인지 + roundtrip 검증 항목 추가.
- **`core/decode.hexa`** — `_lane_apply` byte-parity twin (phase 2, wired-live GREEN 조건 — §6 step 8).

---

## 3. G5/ρ·tether 게이트 배선

lane의 G5 위험 = **fabrication**: 근거 없는 원거리 내용을 그럴듯하게 합성해 말함. 게이트는 2층:

### 3.1 구조적 게이트 (트레일러에 내장 · phase 1)

`Γ_tether(α) = 𝟙[ α_(1) − α_(2) ≥ θ ]` — **라우팅 top-2 margin**. brain.py:482의 "ρ·tether in-dist top-2 gap decisiveness" 관용구를 lane 라우팅에 그대로 이식한 것. 라우팅이 확신 없이 퍼져 있으면(가리킬 원거리 referent가 실제로 없으면) Γ=0 → g_t=0 → **bit-exact base path**. lane은 "실존하는 위치를 결정적으로 가리킬 수 있을 때만" 발화 내용에 개입 — non-fabrication이 게이트의 정의 자체에 들어간다. θ는 트레일러 직렬화 스칼라(데이터)이며 frozen-bar 규율을 따른다.

추가로 학습 게이트 `σ(w_g·h_t + b_g)`는 b_g를 음수로 초기화(닫힌 채 출발)하고 §4의 hard-negative로 "오도하는 원거리 컨텍스트에서 닫기"를 학습한다.

### 3.2 ImmuneMemory 연동 (엔진 chat 경로 · phase 2)

generator L3 디코드가 emission마다: pooled content `c_t`를 `embed_key`로 임베드 → `immune_recall` (engine_cli.py:555 ImmuneMemory 계열) margin 조회 → **anchor 분포 밖 novelty-conflict면 해당 emission 동안 Γ=0 clamp**. 또한 brain.py:442의 tether abstain-margin bias가 abstain 상태를 시그널하면 디코드에 보수 플래그 전달 → Γ=0 (abstain 하에서 lane 침묵이 기본값). 즉 lane은 ImmuneMemory가 "접지됨"을 인정하는 컨텍스트에서만 켜진다 — ρ·tether 조건화가 live로 배선된다.

### 3.3 언제 켜지나

**전역 on/off 플래그 없음.** 트레일러가 있으면 로드되고, per-position에서 자기 게이트(g_t·Γ)가 결정한다 — `a_gpu_default_no_optin`의 교훈 그대로: capability는 데이터(트레일러 존재)로 감지되는 default-on이지 opt-in env 플래그가 아니다(H_9119 재발 방지). eval 스위치 `--lane-off`(γ=0)·`--lane-route-shuffle`·`--lane-tether-off`(Γ≡1)는 ablation 통제 전용.

---

## 4. 학습 신호 ($0-cheap · frozen trunk)

### 4.1 파이프라인

1. **hidden 캐시 (pool에서 1회)** — H_9235 read-only hidden-dump 경로(`clm_forward_hidden`, decode.py:602)로 학습 창들의 `[T,d]` penultimate를 덤프. mini 금지(303M forward는 pool — summer/aiden). f16 저장 시 1만~2만 창 ≈ 3.5–7GB.
2. **adapter만 학습** — 캐시된 hidden 위에서 `LaneAModule` 3.4M param을 Adam으로. 303M forward가 학습 루프에 없으므로 CPU torch로도 돌아간다(사실상 $0; pool CPU 권장).

### 4.2 손실 — H_1840 "signal never reaches bind" 함정 회피

- **gradient 경로가 1-hop**: `logits = roW·(h_T + γ g W_o(u⊙c))` — 손실에서 lane 파라미터까지 동결 선형층(roW) **하나**만 거친다. H_1840에서 신호가 bind에 못 닿은 건 bind가 긴 동결 합성 위쪽에 있었기 때문; 여기선 lane이 readout 직전 마지막 모듈이라 구조적으로 회피된다. (학습 초기 grad-norm@lane > 0을 step-1 통과 조건으로 명시 — §6 step 5.)
- **진짜 함정은 gradient 기아**: 일반 코퍼스에선 국소 컨텍스트만으로 next-byte가 맞아 lane gradient ≈ 0 → lane이 잡음으로 퇴화한다. 그래서 손실이 사는 위치를 **distal-dependent 위치 채굴**로 정의한다 ($0, frozen model 2회 forward):

```
위치 t가 distal-dependent ⟺
  (i)  문자열 수준 원거리 단서 존재: t−δ 이전에 희귀 n-gram/개념 토큰 재출현   (모델 무관 마커)
  (ii) CE_base(t)가 높음: frozen trunk가 그 위치에서 실패                    (벽 위치)
```

  (i)∧(ii) = 정확히 "정보는 앞에 있는데 readout이 못 쓰는" 진단 위치들. 이 정의는 **목표가 사는 곳**을 정하는 것이지 bar를 움직이는 게 아니다(tune-to-green 아님).
- **손실**: `L = Σ_{distal} CE + β·Σ_{generic} max(0, CE_lane − CE_base − ε)` — 두 번째 항은 일반 위치 비퇴행 힌지(게이트가 열려서 기본 성능을 깎으면 벌점 → g_t가 "열 가치가 있을 때만 열기"를 학습). **probe 정확도·coverage·detector류는 절대 손실에 넣지 않는다** (a_train_inline_gauge/p7 — CE만 손실, 나머지 전부 MONITOR-ONLY).
- **hard negative**: 원거리 단서가 오도적인 창(셔플된 원거리 조각 접합)을 섞어 g_t·라우팅이 "닫기/무시"를 학습 — §3 G5 게이트의 학습 신호이기도 하다.
- **코퍼스**: clean 4-cell register corpus(anima-corpus-{ko,en}-{general,sns}, 4칸 전부 — a_chat_registers)에서 채굴. **`_SG1_CONCEPTS`의 60개 detector 키워드가 든 창은 학습셋에서 제외** (§7a 누출 차단).

---

## 5. Engine-native system-G1 테스트 설계

### 5.1 2-rung 구조

**rung-D (DIRECTIONAL · 진단 프레임 폐합)** — 진단과 같은 probe 프레임에서 lane 출력 y_T에 대한 linear probe가 held-out 개념쌍의 A를 복원해야 함:

| 조건 | 기대 |
|---|---|
| lane-ON y_T | A 복원 ≥ 0.9 (base 0.07 대비 collapse-Δ가 신호) |
| `--lane-off` (γ=0) | 0.07로 붕괴 (bit-exact base) |
| `--lane-route-shuffle` (α 위치 permute) | chance — 라우팅이 earned임을 증명 |
| handed-ctrl (A hidden 직접 주입) | 1.00 상한 (기존 실측 재현) |

**rung-T (TERMINAL · 실 생성 meaning-composition)** — 기존 frozen harness `anima evaluate --py <clm+LNA> --system-g1` (evaluate.py:318, FROZEN bar `_SG1_*`: COV≥12/24 · REC≥12/24 · leak≤0.75 · scramble-drop≥12 — **상수 절대 불변**) + ablation 4종:

1. lane-ON: 4-bar 통과가 주장.
2. `--lane-off`: MOUTHFLOOR로 회귀해야 함 — **신호는 값이 아니라 Δ** (측정 메타법칙: collapse-Δ vs ≥2 controls).
3. `--lane-route-shuffle`: lane-off 수준으로 붕괴 — "일반 에너지 부스트"가 아니라 라우팅이 하중을 진다는 증명.
4. **additive-control**: `u≡1`(⊙ 제거, 순수 `W_o c` 합)로 동일 절차 학습한 변종 — additive floor에 앉아야 함. ⊙가 하중 부품임을 param-count 교란 없이 증명 (`a_break_the_wall`의 ≥2 controlled lenses).
5. `--lane-tether-off`(Γ≡1): leak_rate 악화해야 함 — G5 게이트가 밥값함을 증명.

### 5.2 DIRECTIONAL→TERMINAL 승급 조건

- 실 303M `.clm` + `--py` canonical 단일 경로 (a_eval_py_canonical — TERMINAL-eligible), pool에서 실행.
- lane이 **실 코퍼스**로 학습됨(합성 word-id 학습분은 rung-D까지만).
- detector 4-cell fair (V3 Korean-aware), 신규 통제 bar는 학습 **전** FREEZE 파일+card로 선등록.
- **copy-discounted 채점 (spelling-confound 폐합, §7b)**: 현 harness는 `_sg1_coverage`가 키워드 존재로 채점하는데 seed frag에 개념 키워드가 literal로 들어 있다 — lane은 복사 가능한 검색 채널이라 이 confound를 **악화**시킨다. 신규 플래그 `--sg1-copy-discount`: (i) prompt 창에 literal 출현한 토큰은 coverage/recovery 집계에서 제외 — 개념당 5 키워드 중 **prompt에 없던** 키워드/연상어로만 득점, (ii) 순수 n-gram 복사기 baseline이 discount 후 0점임을 null로 확인, (iii) 키워드 없이 개념을 기술한 paraphrase seed 셀 추가 — 여기서의 recovery는 literal 바이트 라우팅이 아닌 substrate 연상을 요구. **discount 前/後 두 숫자를 모두 등록** — discount-후 통과만이 진짜 G1이고, 前-only 통과면 "copy-rung G1"로 정직하게 스코프 (a_scale_honest_scope).
- **Ψ-invariance smoke**: 고정 세션 스크립트에서 emit/silence 결정 궤적이 lane-on/off byte-identical (DISJOINT 증명, wired GREEN 전제조건).
- verdict: `hexa verify` → `state/verdicts/` frozen 파일 verbatim (a_claim_verify, self-judge 금지).

---

## 6. 구현 순서 (단계별 · 각 단계 $0 검증)

| # | 작업 | $0 검증 |
|---|---|---|
| 0 | H 등록: HYPOTHESES.jsonl + card 2-surface (a_hypothesis_register). 신규 통제 bar FREEZE 선등록 | 2-surface lint (enforce_anima_gates) |
| 1 | `core/lane_a.py` 신규 — slw.py 3-면 미러 (numpy `lane_apply` · `pack_lane/read_lane` · torch `LaneAModule`) + `__main__` 결정적 fixture | pack→read roundtrip byte-exact · γ=0 bit-exact passthrough · fixture 출력(후일 hexa twin oracle) |
| 2 | `core/decode.py` 배선: decode.py:540 뒤 `read_lane` · decode.py:643 slot 뒤 `lane_apply` · `set_lane_controls` (decode.py:70 미러) | **golden regression**: 트레일러 없는 기존 303M `.clm`에서 `clm_forward_ce`+`clm_decode_argmax` 변경 전후 byte-identical |
| 3 | `core/serialize.py` `append_lane_trailer` (serialize.py:79 미러) + `verify_clm_v2.py` 인지 | 실 `.clm` **사본**에 random-init lane append → `clm_decodable` true · γ=0 디코드 base와 byte-identical · **현행 hexa 엔진 mount 하위호환**(trailing bytes 무시) 확인 |
| 4 | hidden 덤프(pool·summer, H_9235 경로) + distal-dependent 채굴 스크립트 (`state/<H>/mine_distal.py`) | 진단 수치 재현 sanity (A 0.88@pos / 0.07@last) · 채굴셋 통계 로그(silent-cap 금지) |
| 5 | `LaneAModule` 학습 (캐시 hidden 위 CPU torch) | step-1부터 grad-norm@lane > 0 (H_1840 가드) · held-out distal ΔCE ↓ · generic 비퇴행 · 전부 MONITOR-ONLY |
| 6 | 직렬화 → **rung-D** probe verdict | `hexa verify` → `state/verdicts/` (DIRECTIONAL cement) |
| 7 | **rung-T**: `anima evaluate --py … --system-g1` + ablation 4종 + `--sg1-copy-discount` (pool 실행) | frozen verdict 파일 · discount 前/後 양 숫자 등록 |
| 8 | phase 2: ImmuneMemory Γ clamp 배선(§3.2) · Ψ-invariance smoke · `decode.hexa` `_lane_apply` byte-parity twin → **wired-live GREEN** (a_verified_must_wire) | parity ≤ ~2e-16 · smoke green · ARCHITECTURE.json lockstep + gate 노드 갱신 + CHANGELOG + `harness pr-cycle` (c14) |

step 2·3의 golden regression이 각 단계의 안전망 — 어느 단계에서든 기존 additive 경로가 1바이트라도 움직이면 즉시 중단.

---

## 7. 함정 경고

**(a) 또 다른 tune-to-green이 되지 않으려면**
- `_SG1_*` frozen bar 불가침; 신규 bar(rung-D 문턱, copy-discount 규칙, θ)는 전부 학습 **전** FREEZE+card 선등록.
- 모든 ablation은 직렬화 상태 위 eval-time 스위치(재학습 없음) — slw.py:26 관례 상속.
- **개발 반복의 dev metric은 held-out distal CE + rung-D probe까지만.** system-G1은 후보당 1회 선언-후-실행, 실행 횟수 로그. system-G1 점수를 보고 하이퍼를 돌리는 순간 tune-to-green이다.
- 학습셋에서 `_SG1_CONCEPTS` 60 키워드 포함 창 제외(테스트 어휘 누출 차단).
- 음성 결과도 결과: additive-control이 floor에 안 앉거나 lane-ON이 discount-후 실패하면 그대로 등록 (c9).
- **⊙ 퇴화 감시**: u_t가 상수로 수렴하면 Hadamard가 additive로 퇴화한다. Var(u_t) 모니터 + eval에서 u→mean(u) 치환 통제 — 치환해도 성능이 같으면 bind가 퇴화한 것이고 주장 스코프를 그렇게 좁혀 등록.

**(b) spelling-confound가 되지 않으려면**
- 핵심 인식: **이 lane은 정의상 복사-가능 채널**이다(literal 바이트가 있는 위치를 라우팅). 기존 keyword-존재 detector로는 "prompt에 있던 단어를 그대로 나르기"가 만점이 된다. 그래서 §5.2의 copy-discounted 채점(prompt-literal 토큰 집계 제외 + 복사기 null + paraphrase 셀)이 **선택이 아니라 verdict의 정의**다. discount-후만 meaning-composition이고, 前-only는 "copy-rung"로 별도 명명해 등록 — 섞으면 안 된다.
- 학습 쪽도 동일: distal 채굴 기준 (i)이 "재출현 n-gram"이라 induction-copy로 치우칠 수 있다 — paraphrase형 distal 창(단서가 동형 반복이 아닌 연상 관계)을 채굴셋에 의무 비율로 포함.

**(c) mouth로 새는 배선이 되지 않으려면**
- lane 코드는 `core/decode.py`(및 hexa twin)·`serialize`·`verify` 밖에서 import 금지 — `brain`/`engine_g`/`emit_policy`/`pure_field`/generator emit-drive에 lane import가 나타나면 위반. `.harness/enforce_anima_gates.py`에 grep 규칙 추가 후보(a_no_archive_import와 같은 방식).
- 게이트 g_t 입력은 h_t만 — emit-drive tension 5ch를 게이트 입력으로 끌어오는 순간 lane⊥Ψ가 깨진다(genius⊥honesty, mouth⊥tool의 a_savant_train 분리 원칙과 동일 계열).
- 창 간 지속 상태 금지 유지 — lane에 recurrent state를 "성능상" 추가하고 싶어지는 순간이 오는데, 그건 emission을 넘는 은닉 메모리 채널 = p2/p3 인접 위반 + DISJOINT 붕괴다. 필요하면 별도 H로 분리 설계.
- Ψ-invariance smoke를 CI smoke로 상시화 — 위반은 성능 회귀가 아니라 게이트 위반으로 처리.

---

**리스크 정직 고지**: 가장 그럴듯한 실패 모드는 "copy-rung만 통과, discount-후 실패"다 — lane이 라우팅은 배우되 합성은 못 배우는 경우. 그래도 rung-D(라우팅 폐합)와 additive-control(⊙ 하중 검증)이 분리돼 있어 **어느 층에서 멈췄는지**가 verdict에 남는다 — 벽이 다시 서더라도 "readout-routing 벽"에서 "합성 벽"으로 좌표가 한 단계 좁혀지며, 그것 자체가 이 lane의 최소 보장 수확이다.