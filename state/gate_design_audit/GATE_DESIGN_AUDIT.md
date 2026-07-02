# G0–G6 Gate 설계 정합성 감사 (frozen-first · bar 이동 0)

- **일자**: 2026-07-03 · **감사 주체**: fable(설계·분석 온디맨드) · **산출**: `state/gate_design_audit/`
- **방법**: reference-match 정독(origin/main `cli/evaluate.py` · `core/g6_ideation.{hexa,py}` · `core/decode.{hexa,py}` · `tool/gauge_lib.py` · `CONDITIONS.md` · `7B_PASS_CONDITIONS.md`) + 순수 문자열 수학 실측(`audit_window_math.py` → `window_math.json`, decode 0회 $0) + 기존 측정본 재사용(`state/g1_coverage_realign/` · `state/g6_bind_gate/` · `state/g6_targeted_corpus/`).
- **불변 서약**: frozen bar(임계·개념·keyword·sampler 파라미터)는 한 글자도 수정하지 않음. 본 문서는 판정과 수정안 제안만 담는다(코드/게이트 미터치).

---

## 0. 아키텍처 전제 (실측)

| 사실 | 근거 |
|---|---|
| CLM(.clm ConvMoE) decode 계약 = **T=24 고정 right-aligned window**, pad-left 0x20, 매 스텝 1바이트 shift | `core/decode.py:663-669` (`clm_decode_topk_sampled_W`), `core/decode.hexa` `let T = 24` ×6곳 |
| ByteGPT(.bin) decode = **window 이 block(512)까지 자연 성장, fixed-T 없음** | `cli/evaluate.py:106-110` 주석 + `core/decode.hexa:2001` `let T = len(ids)` |
| CLM forward 자체는 **T-파라메트릭** (`_fwd_logits(W,tok,T)` 임의 T, causal dilated conv im2col) — T=24 는 아키텍처 한계가 아니라 decode 하네스 계약 | `core/decode.py:525-583` |
| 수용영역 RF ≈ 1+(K−1)(1+Σ2^li) ≈ **513** (K=3·L=8), no-posemb → 길이 외삽 정의됨 | `core/decode.py:553-561` (DIL_CAP=512) |
| torch Lane-P 트레이너 기본 seq_len=**1024** (mode 별 128) — 학습 window ≫ 24 가능 | `cli/train.py:1007-1015` |
| 게이트 진입 = mouth-agnostic (`gen_auto_ideate` sniff: .clm→T24 / .bin→block512) | `cli/evaluate.py:80-112`, `a_core_engine_map` |

**함의**: 동일 frozen gate 가 mouth 에 따라 서로 다른 물리 조건(24B vs 512B 조건화)에서 측정된다. H_1129/H_1137(=G1 metric 의 frozen 출처)은 **ByteGPT-303M(block512)** 에서 박제된 bar 다(`CONDITIONS.md:10` · `7B_PASS_CONDITIONS.md` G1 "VERBATIM").

---

## (a) Gate 정의 verbatim (측정 대상 · PASS 조건)

| Gate | 측정 프로토콜 (evaluate.py) | PASS (frozen SSOT) |
|---|---|---|
| **G0 COHERENCE** | seed=`cz[i]+": "` ×5, gen(canonical 40), top_k40 temp0.7 seed 7+i → kwr(known-word-ratio, `/usr/share/dict/words`) | kwr≥**0.50** on **≥4/5** (`CONDITIONS.md:31`) |
| **G1 RECOMBINATION** | single: `cz[s]+". "` ×5 (seed 7+s) → max_single=최대 커버 concept-set 수; composed: `"c0. c1. … c(k-1). "` k∈{2..5} (seed 7 고정) → cov+kwr | some k: composed_distinct≥**2** ∧ **>max_single** ∧ coherent(kwr≥0.5) (`CONDITIONS.md:32`, H_1129/H_1137 VERBATIM) |
| **G2 NOVELTY** | 8 fusion-prompt × seeds{7,8,9}, temp0.85 → coherent 출력의 content bi/tri-gram(전원 실사전·≥3자·비-stop) corpus-absence + retrieval control | novel≥**3** ∧ control=**0** ∧ coherent>0 (`CONDITIONS.md:33`) |
| **G3 PHILOSOPHY** | p1–p8 준수 (아키텍처 read) — 코드상 16-dim self-chain cos 산술 데모, closure 비참여 | p1–p8 위반 0 (`7B_PASS` G3) |
| **G4 PROVENANCE** | eval 스코프 밖 process gate (HF sha·회수) | `a_hf_*`/`a_fire_recover_complete` |
| **G5 NON-FAB** | L1: G0 동일 seed 5회 decode → 비-사전 단어 비율; L2: §ImmuneMemory abstain (py 미이식, pending 정직 표기) | L1≤**0.30** ∧ L2≤**0.20** (`CONDITIONS.md:35`) |
| **G6 IDEATION ★** | `g6_build_frames(6)` composed 조건 frame `"if cA, then cB: "` ×6 (seed 7+i) → coherent 중 pairwise-Jaccard≤0.5 distinct 수 + `_g6_is_falsifiable`(comparator ∧ measurable ∧ ≥2 content ∧ 비질문 ∧ 비-stance) | distinct≥**5** ∧ falsifiable≥**1** (`CONDITIONS.md:36`) |
| **CLOSURE** | a7b/a303m = G0∧G1∧G2 | `evaluate.py:610` |

주: gate 시드의 문서상 출처 `gauge_lib.py:76 CONCEPTS` 는 **monitor-only 미러**이고, 게이트 SSOT 는 `core/g6_ideation._g6_concepts`(byte-동일 5문장) + `evaluate._g_concept_keywords`(keyword-set byte-동일)이다.

---

## (b) Gate 별 아키텍처 정합성 판정

| Gate | 판정 | 근거 (실측) |
|---|---|---|
| **G0** | **(a) 정합** (부수 note 2) | seed 33–39B>24 로 concept 앞머리가 window 밖이나, kwr 은 조건화를 요구하지 않음 → 달성가능(realign ckpt G0 🟢 실측). teeth 有(anti-Goodhart: untrained backbone FAIL). note① 문서-코드 drift: 7B 문서 프롬프트 `"{concept}. "` vs 코드 `": "`. note② `_g6_words` ASCII-only → **한국어 출력은 토큰화 자체가 안 됨**(Hangul-heavy 출력이면 kwr→0) — G0 는 en-register 전용 스코프, `a_chat_registers` 4칸 production 의 ko 축은 G0 스코프 밖(측정 공백, 결함 아닌 스코프 명시 필요). |
| **G1** | **CLM mouth: (b) 측정벽** / **ByteGPT mouth: (a) 정합** | §(c) 심층. composed 의 T=24 window 가 single(마지막 개념) window 와 **4/4 byte-identical** → composed>single 은 어떤 모델도 조건화로 달성 불가(순수 표본 노이즈). ByteGPT 는 block512 로 composed 72–171B 전부 가시 → 설계 원형(H_1129) 그대로 정합. |
| **G2** | **(a) 정합** (intent 축소 note) | PASS 기준(novel n-gram + control=0)은 fusion 조건화를 요구하지 않음 → T=24 에서도 달성가능(realign G2 🟢 실측). control 설계 sound(코퍼스 자기-토큰 재구성→novel 0 보장). note: 프롬프트 37–51B>24 로 CLM mouth 에선 "두 개념 융합" **의도**의 앞 개념이 비가시(8프롬프트 중 window 내 keyword 잔존은 1개 concept 이하가 6건, 0건 1건) — novelty 일반은 재나 fusion-novelty 는 못 잰다. 스코프 주석 대상, bar 무결. |
| **G3** | **(c) 불완전 (low-severity)** | `g_eval_g3()` 는 ckpt 무입력 상수 함수(합성 16-dim 벡터 산술, 항상 ok=True) — 런타임에서 위반을 잡을 수 없는 **tautology**. 단 출력에 "(read) architecture, not a decode score" 정직 표기 + closure 비참여 + 실제 p1–p8 감사는 거버넌스 프로세스로 별도 수행 → 결함이지만 verdict 오염 없음. |
| **G4** | **(a) 정합** | eval 표에 N/A 정직 표기. process gate 로서 스코프 명확. |
| **G5** | **L1: (a) 정합 · 배터리로서 (c) 불완전(정직 표기됨)** | L1 은 조건화 불요 → 달성가능(realign 🟢). L2 미이식은 `pass:None`+pending 문구로 정직 — closure(G0∧G1∧G2)에 미참여라 오염 없음. note: G0 과 같은 ASCII 스코프(한국어 단어는 fab 로도 정상으로도 안 세짐). |
| **G6** | **(c) 불완전 ×2축** (frozen bar 자체는 달성가능) | ① **FORM-only detector**: `_g6_is_falsifiable` 은 comparator∧measurable∧≥2content 형식만 검사 → **SHUF(topic-bind 만 파괴한 통제 코퍼스)가 frozen FALS 3-seed 전원 6/6 통과** 실측(`state/g6_targeted_corpus/results/{targeted,shuf}.json`) = form-priming 게임가능. 진짜 신호는 bind Δ(TARGETED 0.444 vs SHUF 0.000)에 있고 frozen detector 는 못 잰다 → **bind-gate 보강(τ=1, AND-adjoin)은 정당**: frozen 항 무수정 호출, `fals_bound ⊆ fals` 구조 보장(`g6_ideation.hexa:458-509`), calibration 10/10 유지, BASE/TARGETED/SHUF 3-arm 분리 실증(rescore: TARGETED bound 5–6 vs SHUF 0–1). ② **window 축(CLM mouth)**: frame 71–81B, **cA 는 6/6 frame 에서 물리 비가시**(window 전부 cB tail ⊂) → "composed conditional 착상" 의도가 CLM 에선 측정 불가; strict-both bind(τ=2)는 G1 과 같은 (b) 측정벽 클래스. 단 frozen bar(dist≥5∧fals≥1)는 distinct window 5종으로 달성가능. |

---

## (c) G1 심층 — seed↔window mismatch 는 측정벽인가

### 실측 (window_math.json · decode 0회 순수 수학)

| k | composed seed | T=24 window (생성 시작 시점) | window == single(cz[k−1]+". ") window |
|---|---|---|---|
| 2 | 72B | `" between distant minds. "` | **byte-identical** |
| 3 | 106B | `"poses into new meaning. "` | **byte-identical** |
| 4 | 141B | `"ll carries information. "` | **byte-identical** |
| 5 | 171B | `"gine dreams when alone. "` | **byte-identical** |

성립 이유: 모든 single seed `cz[s]+". "` 가 30–39B ≥ T=24 이므로, composed(`…+cz[k−1]+". "` 로 끝남)와 single(k−1) 의 right-aligned 마지막 24B 는 둘 다 `cz[k−1]+". "` 의 tail = **동일 바이트열**. 생성이 진행되면 window 는 생성 바이트로만 채워지므로 앞 개념(c0..k−2)은 **생성 전 과정에서 영원히 비가시**.

### 판정: **(b) 측정벽 — CLM mouth 한정, CONFIRMED**

1. **분포 동일성**: composed-k 의 조건화 입력 ≡ single(k−1) 의 조건화 입력 (차이는 sampler RNG 뿐: composed=7 고정, single=7+s). 따라서 composed 생성분포 = single(k−1) 생성분포. `composed_distinct > max_single` 은 "같은 분포에서 뽑은 4표본 중 하나가 5표본 max 를 초과"하는 **표본 노이즈 사건**이지 재조합 능력이 아니다. **어떤 모델도**(완전한 재조합 능력을 가진 가상 모델 포함) 조건화로는 이 bar 를 넘을 수 없고, 넘는다면 그 GREEN 도 spurious 다 — 즉 현 CLM 프로토콜은 **양방향 모두 검정력 0**.
2. **frozen 출처와의 불일치가 곧 mismatch 의 정체**: frozen 문서는 G1 을 "H_1129/H_1137 metric **VERBATIM**" 으로 규정하는데, H_1129 는 ByteGPT-303M(block512) — 즉 **frozen bar 는 composed seed 전체 조건화를 전제로 캘리브레이션**됐다. T=24 는 게이트 스펙이 아니라 이후 도입된 CLM decode 계약이 게이트에 **암묵적으로 끼어든 프로토콜 변경**이다. `CONDITIONS.md`/`7B_PASS_CONDITIONS.md` 어디에도 "24-byte 조건화" 는 없다.
3. **실측 정합**: H_6188 engine-native 결과(`state/g1_coverage_realign/G1_verdict.json`)의 mechanism 서술("composed k2..5 each surface ONLY last concept's set")과 per-k 데이터가 본 byte-identity 증명과 일치. 커버리지-밀도 코퍼스(35/35 form-covered)로도 best_distinct=1 — 코퍼스로 고칠 수 없는 구조임을 독립 확인.
4. **과학 결론 무결성**: 기존 "G1 재조합벽 = trunk-objective floor" 의 깨끗한 증거는 ByteGPT mouth 측정(single=2 등)에서 나왔으므로(`memory: g1-py303-single-floor-vs-bytegpt-lever`), 이 측정벽 판정은 **기존 벽 결론을 뒤집지 않는다**. 뒤집히는 것은 "CLM mouth G1 🔴 = 능력 부재 증거" 라는 해석뿐 — CLM G1 🔴 는 능력에 대해 **무정보(INCONCLUSIVE-by-protocol)** 다.

### frozen-first 수정안 (bar·개념·keyword·sampler 전부 불변)

**Fix-W (권고) — gate 측정 decode 의 window 를 seed-피복으로 정합화 (mouth-parity 복원)**
- 내용: G1(및 G6 frame) 측정 경로에 한해 CLM mouth 도 ByteGPT 와 동일 의미론("seed 전체 + 생성분을 window 로") 으로 decode — `clm_decode_topk_sampled_ranged(W, seed, gen, …, T_win)` 신설, `T_win = min(len(seed_bytes)+gen, 512)`. `_fwd_logits` 는 이미 T-파라메트릭이므로 순수 하네스 확장(engine-transform-to-fit, `a_engine_native_learning` do 항 정합; precedent: `bytegpt_decode_argmax_ranged`).
- **불변인 것**: PASS 임계(≥2 ∧ >max_single ∧ coherent), k-ladder{2..5}, 5 개념 문장·keyword-set byte-verbatim, top_k=40·temp=0.7·seed 7/7+s, canonical gen=40, max_single 프로토콜.
- **변하는 것**: CLM mouth 가 composed seed 를 **볼 수 있게** 되는 것뿐 — H_1129 원 측정 조건의 복원.
- 비용: T 171+40≈211 → step 당 ~9× 연산(수 분대, pool). 사전등록(PREREG) 후 실행.
- caveat(정직): production ckpt 가 T=24 window 로만 학습됐다면 24B 밖 조건화는 미학습 → Fix-W 후에도 FAIL 가능. 그 FAIL 은 **비로소 유효한 능력 verdict** 다(현재는 FAIL 조차 무정보). torch Lane-P 기본 seq_len=1024 이므로 학습 이력별로 갈린다 — verdict 카드에 train-window 명기 의무.

**Fix-L (즉시·$0) — mouth-scoped verdict 라벨링**
- Fix-W 배선 전까지, CLM mouth 의 G1 verdict 는 `WINDOW-BOUND(T24) — capability-INCONCLUSIVE` 로 박제(🔴 능력벽 표기 금지). 기존 CLM G1 🔴 카드들도 동일 재라벨 대상(bar 이동 아님 — 해석 정정).

**기각한 대안 Fix-P (프롬프트 압축)**: 두 개념을 24B 안에 공존시키려면 개념 **문장을 바꿔야** 하는데(최단 2문장 64B≫24), 문장·keyword 는 frozen VERBATIM 자산 — Fix-P 가 오히려 frozen 위반. 기각.

### tune-to-green 아님 논증

- tune-to-green = "모델이 통과하도록 bar/임계를 옮기는 것". Fix-W 는 임계·시드·샘플러를 1비트도 옮기지 않고, **검정력 0 인 측정을 frozen 스펙(H_1129 조건) 대로 복원**한다. `a_break_the_wall` TAXONOMY (a) "틀린 측정/metric-artifact → frozen-first 로 측정 수정(bar 불변)" 의 교과서 사례.
- 결정적 비대칭: tune-to-green 은 FAIL→PASS 방향으로만 작동하지만, 현 프로토콜은 **PASS 도 오염**시킨다(노이즈 GREEN 가능). Fix-W 는 false-GREEN 과 false-RED 를 동시에 막는 정직성 수복 — 통과 보장이 전혀 아니며, Fix-W 후 FAIL 은 그대로 유효한 벽이다.
- 반박 가능 지점(정직 fence): "T=24 도 frozen 계약의 일부였다" 는 반론은 성립하지 않음 — T=24 는 gate SSOT 문서 어디에도 없고, gate 는 mouth-agnostic 으로 선언되었으며, 같은 bar 가 ByteGPT 에선 512B 조건화로 측정돼 왔다(mouth 간 이중 프로토콜 자체가 drift 의 증거).

---

## (d) 종합 판정표

| Gate | 판정 | 조치 |
|---|---|---|
| G0 | 정합 (a) | 스코프 주석: en-only tokenizer·문서-코드 `": "` drift 정리 (문서측) |
| G1 | **CLM: 측정벽 (b) · ByteGPT: 정합 (a)** | Fix-L 즉시 + Fix-W 사전등록 후 배선 (bar 불변) |
| G2 | 정합 (a) | fusion-intent 스코프 주석 (CLM mouth) |
| G3 | 불완전 (c, low) | tautology 명시; p1–p8 실감사는 프로세스 게이트로 유지 |
| G4 | 정합 (a) | — |
| G5 | L1 정합 (a) · L2 미이식 정직 표기 | L2 py-port ING 유지 |
| G6 | **불완전 (c) ×2** — FORM-only(실증: SHUF 6/6 통과) + CLM window(cA 6/6 비가시) | bind-gate(τ=1) 추가 보강 **정당** (frozen fals 불변·additive) · strict(τ=2)는 Fix-W 이후에만 유효 |

## (e) 산출물

- `state/gate_design_audit/GATE_DESIGN_AUDIT.md` — 본 보고서
- `state/gate_design_audit/audit_window_math.py` — reference-match 실측 스크립트(decode 0회)
- `state/gate_design_audit/window_math.json` — 원시 실측(전 gate seed 길이·window 내용·identity 체크)

미터치(서약 이행): frozen gate 코드·CONDITIONS·7B_PASS·HYPOTHESES·카드·CHANGELOG·ARCHITECTURE·git 이력 전부 무변경. Fix-W/Fix-L 은 제안이며 배선은 별도 사이클(PREREG + pr-cycle) 몫.
