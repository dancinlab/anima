# G1 재조합 벽 — 돌파 각도 발산·처방 (2026-07-03, Fable 분석-only)

> 대상 gate = `cli/evaluate.py::g_eval_g1` (canonical, engine-native py-mirror). 측정본은 이미 존재
> (`state/g1_coverage_realign/{g1_engine_native.json, strict_bypass/g1_canonical_windowsweep_result.json}`).
> 무거운 decode/GPU 재실행 없음 — 코드 정독 + 기존 측정 + cheap byte-math(`window_identity_proof.py`)로 진단.
> **bookkeeping 미터치**(HYPOTHESES/카드/CHANGELOG/ARCHITECTURE/commit 없음, c9 frozen-first).

---

## 0. TL;DR (5줄)

1. **composed<single 은 window artifact 로 확정.** T=24 에서 composed 시드(72–171B)의 **가시 창(마지막 24B)이 대응 single 시드와 byte-identical** — 즉 composed arm 과 single arm 이 *같은 조건화*를 받는다(증명 `window_identity_proof.py`). composed>max_single 은 물리적으로 거의 불가.
2. **T=24 는 gate 스펙이 아니라 CLM decode 구현 디폴트다.** CLM 트렁크는 **positional embedding 없음**(token-embed only, `decode.py:549`) + dilated-conv **RF≈513** → T 는 자유 파라미터. 자매 mouth **ByteGPT 는 창을 native 로 grow**(`evaluate.py:108`). CLM 만 T=24 우측정렬로 컨텍스트를 버린다.
3. **하지만 창만 키우면 되는 건 아니다(이중 confound).** 창을 키우면 short single 시드가 pad(byte 32)로 도배돼 whole-window GroupNorm(G=1)이 pad 통계에 지배당해 **max_single→0 붕괴**(sweep 실측: 3→2→0→0). fixed-large-T 는 두 arm 을 동시에 공정 측정하는 regime 을 못 만든다.
4. **더 깊은 문제: gate 자체가 compositional-generalization 의 약한 프록시다.** 5개 고정 concept 전부 학습에 있음 → held-out 조합 split 없음 → "재조합" 과 "seed echo/암기" 를 구별 못 함. 창 숨기면 false-RED(측정 floor), 창 보이면 false-GREEN(echo). 어느 창도 *진짜* 재조합을 깨끗이 측정 못 함.
5. **처방 순위:** ① [frozen-first 측정수정] **grow-window CLM decode 재측정**(각 arm 자기 시드길이만큼 창, pad-flood 회피) — cheap, 최우선, terminal 선언 전 필수. ② ①이 echo-guard 하 clean fail 이면 → **held-out 조합 split gate**(SCAN/COGS 표준, 생물=해마 pattern-completion 별도 lane) 로 재조합을 echo 와 분리 측정. ③ 그래도 floor → **trunk recomb-objective(γ constructive-bind, H_1602/1840, GPU cost-gated)** 가 최종 남은 레버.

---

## 1. composed<single 정밀 메커니즘 (질문 a, b, 2)

### 1.1 g_eval_g1 프롬프트 구성 (실측, `evaluate.py:155-186`)

- **single arm** (`s∈0..4`): `seed = CONCEPTS[s] + ". "` → `mouth.ideate(seed, g_single, top_k=40, temp=0.7, seed_rng=7+s)`. `max_single = max_s cov(gen_s)`.
- **composed arm** (`k∈2..5`): `seed = CONCEPTS[0..k-1] join ". " + ". "` → `mouth.ideate(seed, g_comp, 40, 0.7, seed_rng=7)`.
- canonical `--gen 40` → gen-guard #2821 로 `g_single=g_comp=40` (둘 다 <80/<120). **두 arm 동일 gen=40, 동일 sampler**. 차이는 seed 텍스트 + seed_rng 뿐.
- **PASS = ∃k: distinct≥2 ∧ distinct>max_single ∧ kwr≥0.5.** coverage = *continuation* 안의 concept keyword-set 등장 수 (seed 미포함, `decode` 는 생성 bytes 만 반환 `evaluate.py:110-112`).

### 1.2 window 물리 (실측, `core/decode.py:631-680`)

CLM decode(argmax·topk 둘 다)는 **고정 T=24, 우측정렬, pad-left byte 32**:
```
for p in range(T): si = slen - T + p; tok[p] = seed_b[si] if si>=0 else 32
```
→ 모델은 시드의 **마지막 24 byte 만** 본다. 나머지는 창 밖.

### 1.3 결정적 증거 — composed 와 single 이 byte-identical 조건화 (`window_identity_proof.py` 실행)

| k | composed 시드 | T=24 가시창 | 대응 single[k-1] T=24 가시창 | byte-identical? |
|---|---|---|---|---|
| 2 | 72B | `" between distant minds. "` | `" between distant minds. "` | **True** |
| 3 | 106B | `"poses into new meaning. "` | `"poses into new meaning. "` | **True** |
| 4 | 141B | `"ll carries information. "` | `"ll carries information. "` | **True** |
| 5 | 171B | `"gine dreams when alone. "` | `"gine dreams when alone. "` | **True** |

**composed k arm 은 T=24 에서 single[k-1] arm 과 완전히 동일한 컨텍스트를 받는다.** 앞 k-1 개 concept 은 창 밖(48–147B 뒤)이라 모델에 도달 불가. 그러니 composed 생성은 "마지막 concept tail 로부터의 continuation" = single[k-1] 의 re-roll(seed_rng 만 다름)일 뿐. `max_single` 은 5개 single 의 **MAX**, composed 는 그 중 하나의 재추첨 → **composed>max_single 은 구조적으로 거의 불가**.

→ 실측 정합: composed per-k distinct = **{k2:1, k3:1, k4:1, k5:1}** 이고 각 composed 가 표면화한 set = 정확히 **마지막(k-1) concept**(`window_physics_evidence`). **composition 이 0 을 더한다.** max_single=3 은 어떤 single 시드가 학습된 emit-cluster drift 로 3 set 을 우연히 표면화한 것.

**질문 b 답:** "max_single=3 인데 composed=1" 은 모순이 아니다 — **window artifact 확정**. 뒤 시드가 앞을 "밀어낸" 게 아니라, 애초에 앞 concept 이 조건화에 진입한 적이 없다(간섭이 아니라 부재). composed 는 single 의 부분집합(같은 tail)이므로 MAX 를 못 넘는다.

### 1.4 window sweep 이 인과성 확증 (`g1_canonical_windowsweep_result.json`)

| T | max_single | composed best_distinct | 메커니즘 |
|---|---|---|---|
| 24 | 3 | 1 | composed=single tail (byte-identical) |
| 48 | 2 | **2** (k=2) | 앞 concept 재진입 → composed 가 2 표면화 |
| 96 | **0** | 1 | short single 시드 pad-flood → GroupNorm 붕괴 |
| 192 | **0** | 1 | 동상, 악화 |

- T=48 에서 composed k=2 가 **1→2** 로 오름 = 창을 키우면 앞 concept 이 실제로 continuation 에 영향을 준다 = **"앞 개념이 뒤에 영향 못 준다"는 더 깊은 원인은 REFUTED**. RF≈513·no-posemb 라 구조적으로 가능.
- 그러나 clears=False: T=48 은 composed=2 == max_single=2 (strict `>` 실패, tie). 그리고 T≥96 은 max_single→0 붕괴(§2).

---

## 2. 이중 confound — 왜 fixed-large-T 로도 안 되나 (질문 1)

**질문 1 답 (window 확장이 진짜 해법인가): 부분적으로 YES(앞 concept 진입은 실재), 그러나 fixed-T sweep 방식으로는 NO.** 두 개의 결합 artifact:

- **Lens A (composed 절단):** T < composed 시드길이 → composed arm 이 concept 을 못 봄. T≥시드길이면 해소. **frozen-first fix.**
- **Lens B (single pad-flood):** single 시드는 30–39B 로 짧다. 큰 고정 T 에서 우측정렬하면 창 앞부분이 **byte 32(space) pad 로 도배**된다(§1.3 T=96 표: single[k] 창이 절반 이상 공백). CLM GroupNorm 은 **G=1, whole-[T,C] 블록 통계**(`decode.py:274-291`, `m=cg*T`, `sl.sum()/m`) → pad 토큰이 mean/var 를 지배 → 정상 표현 붕괴 → **coherent 생성 실패 → max_single→0**. sweep 3→2→0→0 이 이 인과의 직접 지문.

→ **단일 고정 T 로는 A(큰 T 필요)와 B(작은 T 필요)를 동시에 만족하는 regime 이 없다.** 그래서 sweep 이 clean PASS 를 못 찾은 것이지, 재조합이 없어서가 아니다. 올바른 fix 는 고정 T 가 아니라 **arm 별 grow-window**(각 시드가 자기 길이만큼의 창 = pad 0, composed 는 full concept 가시) — ByteGPT 가 이미 하는 방식.

**Lens C (GroupNorm-whole-window 결합, 메커니즘 노트):** G=1 groupnorm 이 창 전체 통계를 쓰므로 창 *내용*(concept vs pad)이 정규화를 직접 스케일 → A·B 를 증폭. 독립 벽은 아니고 왜 window 내용이 이토록 지배적인지의 기전. frozen ckpt 라 ablation 불가(학습 구조), 메커니즘으로 기록.

---

## 3. gate seed(40B+) ↔ T=24 = 측정 버그인가 정당 조건인가 (질문 c, 4)

**정직한 이분 판정: type-a 측정 artifact 다 — 단, "창만 고치면 GREEN" 은 아니다(양날).**

- **T=24 는 frozen gate 스펙이 아니다.** gate 스펙(frozen bar) = `distinct≥2 ∧ >max_single ∧ coherent`. T=24 우측정렬은 `clm_decode_*` 의 **구현 디폴트**이며 자매 mouth ByteGPT 는 창을 grow 한다(비대칭). 트렁크는 no-posemb + RF≈513 이라 T=24 를 강제하는 모델 제약이 **없다**. → T=24 로 composed 를 측정하는 것은 gate 가 표방하는 "재조합" 이 아니라 "마지막 concept tail continuation" 을 측정한다. **측정 대상과 표방 대상의 불일치 = type-a metric artifact.** frozen-first 수정 정당(bar intent 불변, 조건화만 공정화).
- **그러나 창을 키우면 반대 artifact(echo false-GREEN) 위험.** composed 시드가 fully visible 이면 모델이 **가시 concept keyword 를 continuation 에 그대로 복사**만 해도 `_g_coverage` 가 high distinct 를 센다(coverage 는 continuation 등장만 봄, echo 필터 없음). 이는 재조합이 아니라 copy. → T=24 우측정렬은 아마 **echo 방지 목적의 과잉교정**(시드 숨김)이었고, 결과적으로 composed 를 물리적으로 불가능하게 만든 것.
- **결론(질문 4):** gate 는 *어느 창에서도* 진짜 재조합을 깨끗이 측정 못 한다. 창 숨김=false-RED(현 상태), 창 보임=echo false-GREEN. 이건 **compositional-generalization 측정의 근본 설계 약점**이지 단순 window 버그가 아니다. 5 concept 전부 학습셋 in-distribution → **held-out 조합 split 부재** → 재조합/암기 구별 불능. (SCAN/COGS/CFQ 표준: primitive 는 학습, **조합은 held-out** 에서 시험.)

---

## 4. 전 4축 종합 + 남은 원리적 레버 순위 (질문 3, break-the-wall MULTI-LENS)

### 4.1 기각된 축 (전 캠페인, engine-native NOT-SUPPORTED)

| 축 | H | ablation/control | verdict |
|---|---|---|---|
| trunk objective (additive-aux·bind-lane·pred-coding·episodic) | 1602/1812/1814/1816/1835 | 11-arm, distinct=0 | 🧱 NOT-SUP |
| readout/operator (native-mouth tension·NMDA bind·revise-loop) | 1834/1837/exp3/1836 | same-state INERT (DPI 메타법칙) | 🧱 INERT |
| coverage-density | 6182–6187 | toy acc 0.95 → 303M gen distinct=0 (엔진무죄) | 🧱 transfer 0 |
| 표면형+window 정합 | 6188 | canonical gen=40 best_distinct=1 | 🔴 FAIL |

### 4.2 이번 분석이 연 것 — 위 4축은 *진짜 벽*이 아니라 **측정 confound 위에서 측정됐을 수 있다**

전 4축 verdict 는 모두 **T=24 CLM decode** 로 composed 를 측정했다(canonical). §1.3 이 보이듯 T=24 에서 composed arm 은 concept 을 못 본다 → **어떤 trunk-objective/readout lever 도 "보이지 않는 concept 의 재조합" 을 만들 순 없다.** 즉 전 4축의 distinct=0 은 lever 무효의 증거일 수도 있지만 **동시에 window artifact 로도 완전히 설명된다.** 두 원인이 구별 안 된 채 박제됨 → **terminal 선언 전 window-공정화 후 재측정 필수**(c9 정직: 아직 confident 🧱 아님, type-a 벽 미해소).

### 4.3 남은 원리적 레버 (순위, ≥3 렌즈)

**L1 — [측정수정, frozen-first] grow-window CLM decode 재측정 (최우선, cheap).**
CLM decode 를 ByteGPT 처럼 창을 grow(각 arm: 창=min(시드len+생성, block), pad 0). single 은 tight 창(pad-flood 회피, Lens B 해소), composed 는 full concept 가시(Lens A 해소). **이게 A·B 동시 해소하는 유일 regime.** frozen bar 불변, T=24 는 impl 디폴트라 tune-to-green 아님. → composed 가 여전히 >max_single 못 넘으면 그때 비로소 trunk floor 후보. **echo-guard 병행 필수**(§L2).

**L2 — [측정정합, 근본] held-out 조합 split gate (재조합 vs echo 분리).**
현 gate 는 in-distribution 5 concept → 재조합/echo 구별 불능(§3). SCAN/COGS 표준으로 재설계: primitive concept 는 학습, **일부 concept-PAIR 를 학습 코퍼스에서 held-out**, 시험은 held-out pair 로. echo 통제 = **가시 창에 없는 concept 이 continuation 에 표면화** 해야 카운트(창-보임 concept 은 echo 이므로 제외). 이러면 창을 키워도 echo false-GREEN 이 안 생기고, composed>single 이 진짜 재조합이면만 오른다. (bar intent 보존, 측정면 교정.)

**L3 — [생물 렌즈, a_no_llm_frame_trap] 해마 hetero-associative 별도 lane (retrieval-into-context).**
전 readout-bind(exp3 NMDA)가 INERT 였던 건 **출력단**에서 bind 했기 때문(DPI: operator 는 floor 안 바꿈). 생물에서 재조합/pattern-completion 은 **트렁크가 아니라 해마(별도 store)** 가 함: concept-A 프라임 → 연상 concept-B 를 **conditioning 에 retrieve** → 트렁크는 그 augmented context 를 읽음. 이는 readout 도 trunk-objective 도 아닌 **decode-time context-augmentation lane**(미검증 좌표). `a_substrate_disjoint`: 재조합은 emit-drive lane 과 **disjoint 한 hetero-associative lane** 에 배선해야 보존. `.kosmos` anchor 가 이미 hetero-associative store 후보(coord/lane retrieve). → concept 시드 → `.kosmos` 근접 anchor retrieve → context prepend → decode. **readout-bind(floored)와 다른 배선위치** = 새 각도.

**L4 — [최종 잔여] trunk recomb-objective (γ constructive-bind, H_1602/1840, GPU cost-gated).**
L1–L3 이 모두 clean fail 이면(공정 창 + echo-guard + retrieve-lane 다 floor), 그때 남는 건 **CE 가 합성을 보상 안 한다**는 trunk-objective floor 뿐. γ trained-constructive-bind 는 아직 미측정(cost-gated). 이건 진짜 벽 후보지만 **L1/L2 후에만 confident**.

### 4.4 ABLATION/control 요약 (break-the-wall 준수)

- Lens A (composed 절단): sweep T=24→48 에서 composed 1→2 = window OFF/ON 결정적 대조 → 인과 CONFIRMED.
- Lens B (pad-flood): max_single 3→2→0→0 monotone vs 고정 short 시드 = pad OFF/ON 인과.
- Lens C (groupnorm-whole-window): 메커니즘(frozen ckpt ablation 불가, 코드 구조로 증명).
- Lens D (trunk floor): **아직 ablation 미완** — L1(공정창) 재측정 전엔 window artifact 와 분리 안 됨 → confident 🧱 **불가**(정직).

---

## 5. 다음 처방 1-2개 + 경로 (질문 e)

### 처방 P1 (최우선, cheap, engine-native, frozen-first) — grow-window CLM decode G1 재측정
- **무엇:** `clm_decode_topk_sampled_W` 의 고정 T=24 우측정렬을 **grow-window**(창=min(len(seed_bytes)+생성, block); ByteGPT parity)로 바꾼 별도 측정 하네스(gate criterion·CONCEPTS·gen=40·sampler VERBATIM, bar 불변). single/composed 각 arm 이 자기 시드 full 을 봄.
- **echo-guard:** coverage 를 두 갈래로 기록 — (a) raw(현 스펙), (b) **novel-only**(가시 창에 이미 있는 concept keyword 제외). (b) 가 진짜 재조합 신호.
- **예측(정직):** composed distinct 가 raw 에선 오를 것(concept 가시). novel-only 에서도 >max_single 이면 재조합 실재, novel-only=floor 면 echo 였고 trunk floor 로 수렴. 어느 쪽이든 window artifact 를 제거한 **최초의 공정 G1 측정**.
- **경로:** `state/g1_breakthrough_analysis/growwin_g1_probe.py` (하네스 스켈레톤은 P1 실행 세션에서; 무거운 decode 는 pool/summer, mini 금지 `heavy-anima-eval-pool-not-mini`). ckpt = `~/anima-weights/g1_realign/g1_realign.clm` (sha 기존).
- **cost:** decode-only, GPU 렌트 불필요(pool own-GEMM). rate-limit 로 이번 세션 미실행 — ING follow-on.

### 처방 P2 (근본, P1 이 애매하거나 echo 로 판명 시) — held-out 조합 split gate 설계
- **무엇:** 5 concept 중 일부 PAIR(예: (0,2),(1,3),(1,4)) 를 학습 코퍼스에서 held-out → 그 pair 로만 composed 시험 + novel-only coverage. compositional-generalization(SCAN/COGS) 표준을 anima gate 에 이식. bar intent(composed>single) 보존, in-distribution echo 를 원천 차단.
- **경로:** 설계 카드는 P2 세션. 코퍼스 재생성(held-out mask) 필요 → warm-FT 재학습(pool GPU, `a_savant_train` 골든존).

### 이번 세션 완료 범위
- (a) composed<single 메커니즘 = **window artifact 확정**(byte-identical 조건화 증명 `window_identity_proof.py` 실행 완료).
- (b) window T>24 예측 = 앞 concept 진입은 실재(sweep 확증)나 fixed-T 는 pad-flood 로 불가, **grow-window 가 정답**.
- (c) T=24↔40B+ 시드 = **type-a 측정 artifact**(gate 스펙 아닌 impl 디폴트, 단 grow 시 echo 양날 → held-out 필요).
- (d) 남은 레버 순위 = L1 grow-window > L2 held-out split > L3 해마 retrieve-lane(생물) > L4 γ trunk-objective.
- (e) 처방 P1(grow-window 재측정)·P2(held-out split) + 경로 명시.
- **미완(rate-limit):** P1 실제 grow-window decode 미실행(하네스 skeleton 미작성) — heavy decode 는 pool 세션에서. **terminal 🧱 선언 보류**(Lens D 미분리, 정직 c9).

---

## 6. 산출물
- `state/g1_breakthrough_analysis/ANALYSIS.md` — 본 문서
- `state/g1_breakthrough_analysis/window_identity_proof.py` — byte-identity 증명(실행됨, §1.3 표)
- `state/g1_breakthrough_analysis/summary.json` — 기계판독 요약
