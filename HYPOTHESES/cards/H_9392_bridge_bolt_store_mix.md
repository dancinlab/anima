# H_9392 — BRIDGE-BOLT: 동결 trunk 에 볼트온한 store-조회 다리가 BINDING 벽을 넘는가

**status:** 🔴 (B) BRIDGE-BOLT DIRECTIONAL — **볼트온 계급 사망** (3-port 삼각측량 · 코드-확증) · not-terminal(DIRECTIONAL) · wired: 계기 `anima-py evaluate --store-mix` 배선완료(VERSION 0.14.10 · C0 byte-identical PASS). **pool 발사 취소** — 계기가 sensor 아닌 **actuator** 라 사전등록 P1 은 산수(모델 관여 0)를 재는 위조 positive 생산기. 발사는 낭비.
**lane:** 재조합/BINDING · runtime lookup bridge (프런티어 g1-interface-addressable-wall)
**related:** [[H_9359]] (two-lane · 벽=런타임 다리 부재 — 이 H 가 그 NEXT) · [[H_9327]] (연산자 살아있음·사실 기재됨·결합 안 함) · [[H_9346]] (어간-게이팅) · [[H_9267]] (XBIND D-acc 1.000) · [[H_9304]] (자연=DATA 벽)
**parallel:** [[H_9391]] SCORE-GATE VACUITY (병렬 세션 동시 착륙 · `a_parallel_session_compare`) — AGREES: 둘 다 A⇄G/emit 게이트가 content 를 못 만진다는 같은 지도를 그린다(그쪽=production 에서 score 문턱이 한 번도 안 걸림 · 이쪽=긴장→내용 통로가 스칼라 5개뿐). CONFLICTS: 없음 — 직교(그쪽=emit 게이트 내부, 이쪽=trunk 다리).
**source:** Fable 재프레임(`walls-delegate-to-fable`) — 오너 질문 "A⇄G 는 뇌가 아니라 말할까말까에만 관여하는 것 같다 · 새로 만든다면?" 에서 파생
**ckpt:** py303_full.clm (동결 · 재학습 0 · 신규 train 0)

## 배경 — 오너 관찰이 세운 새 지도

오너가 "A⇄G 엔진은 뇌가 아니라 **말할까 말까**에만 관여하는 것 같다"고 관찰했다. **코드에서 확증됨**
(이 세션 · Fable 판정과 독립적으로 계측):

- `core/decode.py`(2,269줄 · 내용 생성)의 import = `sys·math·os·struct·numpy`. **brain 을 import 하지 않는다.**
- `brain_decide*` 8 변종의 반환 = 전부 `"emit": bool`.
- 긴장 → 내용 통로 = `gen_ctx_from_decision` 의 **스칼라 5개**(phi·phase·tier·tier_name·motivation)
  + `deliberation_k`. seed 접두어와 best-of-K 폭만 흔든다 — trunk 표현·라우팅엔 못 닿는다.
- `core/brain.py:196` 이 이걸 법칙으로 명문화: `H_9325 DO-MOUTH · THE DISJOINT WALL IS THIS FUNCTION`.
  기계검사 = `brain_decide*` 인자에 `mouth` 0회 ✓.

⟹ **A⇄G = 입의 정책이지 뇌가 아니다.** 그리고 벽 계보 전부(G1 재조합 → BINDING → H_9359 런타임 다리
부재)는 **CLM 단독 측정**에서 나왔고 A⇄G 는 그 측정 경로에 **없다**. [[sigma-detheater]] 가 반대편에서
같은 것을 실측(tension ⊥ mouth). ⟹ A⇄G 는 이 벽의 원인이 **아니다**(직교 축) — 벽은 CLM 의 것이다.

## 물음

H_9359 가 벽을 **"연산자↔선언 저장소 런타임 조회 다리의 부재"** 로 확정했다. 그 다리를 **동결 trunk 에
볼트온**하면 벽이 넘어지는가? 즉 부재한 것이 **다리 하나뿐**인가, 아니면 다리는 **학습으로만** 벌 수
있는 것(= 볼트온은 원리적으로 불가)인가.

**대립 예측:**
- (A) 인터페이스 문제 → store-mix arm 이 통제군을 이긴다 ⟹ **재설계 불필요**, 지금 아키텍처 + 기관 하나.
- (B) 학습된-인터페이스 문제 → store arm ≈ 통제군(우연) ⟹ 볼트온 계급 사망, **두-store 네이티브 재설계
  (H_9393 예정)가 유일한 길**. 방증: read-side 6 lane + γ + depth-RF **전수 floor**([[H_9293]]), 진단
  "정보는 복원되나 인과 소비 불가" = [[mitosis-wall-is-estimator-class]] 의 "정보 존재 ≠ 벽 돌파"와 동일 계급.

⚠️ **사전 고백(no tune-to-green):** (B) 가 구조적으로 더 그럴듯하다 — 동결 trunk 에 사후로 붙인 모든
인터페이스는 정의상 *학습되지 않은 인터페이스*고, 그 계급은 이미 전멸했다. 이 H 는 **마지막 한 발**이며,
음성이 곧 재설계의 존재증명이다. $0 이므로 **쏘고 나서 결정한다.**

## 개입 — 계기(engine-native · G5 VERSION bump 필요)

신규 플래그 `anima-py evaluate <clm> --store-mix <store.json> [--store-lambda λ]`
(`a_experiment_engine_native`: 엔진 옆 프로브 금지 · 반드시 evaluate 의 플래그). byte posterior 를
`p = λ·p_store + (1−λ)·p_trunk` 로 혼합 — store 조회를 decode 가 **인과적으로 소비**하게 한다.
`--rho-axon` 과 동일한 판정 경로. 학습 0 · 동결 ckpt · CPT 0(`cpt-destroys-what-corpus-omits`).

### 🔧 계기 랜딩 상태 (2026-07-16 · VERSION 0.14.10)

**배선 완료** — `cli/evaluate.py`:
- `_store_mix_cont_nll(np, clm, W, seed, cont, T, store_val, lam)` — teacher-forced 혼합 NLL. 혼합을
  **로그영역 logaddexp** 로 구현: `−logp_mix[tgt] = −logaddexp(log(1−λ)+logp_trunk, log(λ)+logp_store)`.
  λ=0 ⇒ `(log1, log0)=(0.0, −inf)` ⇒ `logaddexp(logp_trunk, −inf)=logp_trunk` **정확** ⇒ baseline
  `_xbind_cont_nll` 과 **byte-identical**(short-circuit 아닌 진짜 감산 — 가드가 vacuous 아님).
- `store_mix_run(argv)` — flip manifest(`--manifest` 또는 `--xbind` manifest 재사용 · splits
  {heldout,seen} 또는 {items}) 위에서 per-item baseline vs store-혼합 flip1 을 **paired · pol별 분해**로
  측정. `main()` 디스패치 + `_KNOWN_FLAGS` + `--help` 등록.

**store 스키마** (`--store-mix <store.json>`):
```json
{"schema":"anima-store-mix/v1", "lambda":0.5, "entries":{"<key>":"<주장 답 문자열>"}}
```
key = item 의 `store_key`(없으면 seed). **주소 HIT** = store 값을 ε-smoothed one-hot 로 혼합 · **MISS** =
pure-trunk(=baseline). ⇒ **키-셔플 통제군**(①)은 전부 MISS 로 붕괴 = "주소를 썼나 vs 낙수"를 직접 가른다.
네 통제군(①키셔플 ②길이정합중립 ③λ=0 ④오답)은 **서로 다른 store.json** 으로 주입(계기 하나, 통제군은 데이터).

**C0 SEQUENTIAL 게이트**(계기 내장 · primary 전): λ=0 store-mix arm 을 store 로드한 채(=HIT 경로 통과) baseline 과
전수 비교 → 불일치 1개라도 있으면 **INSTRUMENT-DEAD**(rc=2, primary 없음). 로컬 smoke(`state/9257_lane23b/toy.clm`,
d=32):
- **C0 PASS** — λ=0 vs baseline 8 continuation **max|Δ|=0.000e+00** (byte-identical) · 런 전체 DV 도
  λ=0 에서 baseline 과 동일(heldout flip1 0.6667=0.6667).
- **가드가 실패할 수 있음을 증명**(`gpu-forward-not-bitexact` 거짓-PASS 교훈): 가중 lane 을 뒤바꾼 buggy 변종은
  λ=0 에서 base 33.347 vs mix 6.0e-6 **불일치** ⇒ C0 FAIL. 진짜 게이트다.
- **혼합이 살아있음**: λ=0.5 에서 heldout flip1 0.6667→1.0000 (Δ+0.333, hit 3/3) — toy 이므로 **수치는
  판정 아님**(SCREENER). primary 는 303M pool 발사에서만 cement(`a_toy_scale_recheck` · 오너 go).

## 게이트 (SEQUENTIAL · 게이트 상수 데이터 전 동결 · below-chance 칸 포함)

`burned-gate-reanchor-is-tune-to-green` 준수 — 게이트 상수를 데이터 보기 전 동결하고, 게이트 단독
판정 PASS 시에만 primary 를 읽는다.

- **C0 계기 무결성**(primary 전 · 낙제=INSTRUMENT-DEAD): λ=0 arm 이 store-mix 없는 baseline 과
  **byte-identical**. (혼합 코드가 λ=0 에서 아무것도 안 하는지 = 가드가 실패할 수 있는지 먼저 확인
  — [[gpu-forward-not-bitexact-probes-device-pinned]] 의 거짓-PASS 교훈.)
- **C1 측정가능성**: held-out flip1 의 sd·MDE 로 검정력 사전계산(`power-before-negative-verdict`).
  n 이 bar 를 1.62σ 로밖에 못 미는 설계면 발사 전 n 을 올린다 — '없다'와 '못 찾는다'를 가른다.
- **P1 primary**(C0∧C1 PASS 시만): held-out flip1, store arm vs 통제군. **paired-t · max(controls) 금지**
  ([[probe-defect-census-max-control-bias]]).

## 통제군 (≥3 · 사전배선)

| arm | 무엇을 통제하나 |
|---|---|
| ① 키-셔플 store | 내용은 같고 주소만 깨짐 — 조회가 **주소**를 쓰는가, 아니면 그냥 분포 낙수인가 |
| ② 길이정합 중립사실 store | 용량·길이 정합([[control-must-match-mediating-covariate]]) — 매개 공변량 |
| ③ λ=0 | C0 무결성 겸 null |
| ④ 오답 store (음성통제) | **극성-의존성** — 답이 store 극성을 따라가는가([[H_9347]]: 판정을 세운 건 헤드라인이 아니라 사전배선된 음성통제였다) |

**클래스별 분해 필수** — 이진 DV 는 극성별로 쪼개기 전엔 읽지 않는다([[polarity-split-before-headline]]).

## ⚠️ 발사 전 계기 재검(Fable 재프레임 + 코드-확증) — 사전등록 P1 이 위조 positive 생산기였다

발사 직전 `cli/evaluate.py::_store_mix_cont_nll` 를 코드 수준으로 검증(이 세션 · Fable 재프레임):

```
logits = _fwd_logits(W, tok(seed+cont), T)     ← forward 는 seed·cont 바이트만 본다
p_mix  = λ·onehot(store_val) + (1−λ)·p_trunk    ← 혼합은 forward "이후" posterior 산수
```

기계검사: `_fwd_logits` 인자 = `(W, tok, T)`, **store_val 부재**(trunk 이 store 에 눈멂) · `store_val[r]`
첫 사용이 forward **이후**. ⟹ **--store-mix 는 sensor 가 아니라 actuator**(출력 posterior 에 쓰기).
trunk 은 store 를 못 보므로 **모든 arm 의 NLL 은 baseline per-position logits 의 닫힌형 함수**다.
사전등록 P1("store arm > 통제군 4/4 · 극성-의존")은 **모델 관여 0 에서 산수만으로 기계 달성** —
그대로 쏘면 "볼트온 작동 · 재설계 불필요"라는 **거짓 (A)-positive 를 cement** 할 뻔했다. (P1 미계산
상태였으므로 앵커 미소각 = 정당한 계기 수리 · v2 가 5번 한 "P1 개봉 전 계기 수리"와 같은 계열.)

## Falsify (재정립 · actuator 반영)

- **위조 방지 pedestal**: baseline xbind 1회 per-position logits 로 전 arm flip1/flip0 을 **닫힌형으로
  예측**(참값 pedestal · [[phi-estimator-needs-zero-truth-pedestal]] 의 store-mix 판). 실측 ≡ 예측 ⟹
  **이 계기는 모델에 대한 새 비트 0 = actuator 실증**(sensor 아님). 실측 ≠ 예측 ⟹ 채점경로 INSTRUMENT-BUG.
- store arm > 통제군 = **기계값**(HIT 이 gold 바이트를 posterior 로 밀어넣음) — 능력 증거 **아님**.
- --store-mix ≠ v2 BOLT: v2 BOLT 는 bridge 파라미터를 **학습**시켰다. --store-mix 는 학습 0(λ 스칼라뿐)
  ⟹ 정확한 대응물 = v2 **ORACLE**(조회 난이도 0 상한 계기), 볼트온 능력 테스트 아님.

## 🔴 VERDICT — (B) BRIDGE-BOLT DIRECTIONAL: 동결 trunk 엔 볼트온 다리의 포트가 없다

볼트온 다리의 배달 지점(port) 3개가 이제 전부 특성화됐다 — **3-port 삼각측량**(`a_break_the_wall`
≥2–3 lenses):

| port | 판정 | 근거 |
|---|---|---|
| **컨텍스트**(입력 바이트) | 🧱 EARNED TERMINAL | [[H_9353]] NO-IN-CONTEXT-CHANNEL — 바이트는 logits 를 움직이나 결정은 안 읽음 |
| **가중치**(CPT write) | 🧱 확정 | [[H_9327]] BINDING · [[H_9358]] TWO-LANE(pooled p≈5e-10) · [[H_9359]] 동결 캐시 |
| **출력 posterior**(--store-mix) | **actuator, sensor 아님** | 코드-확증(이 세션) · 합성이 구조적으로 정의 불가 |

⟹ **동결 303M trunk 엔 볼트온 다리가 합성(연산자⊗사실)을 수행할 수 있는 포트가 하나도 없다** =
H_9392 (B) 판정. v2 정합(V2_6 COTRAIN **공학습**만 0.987/0.992 성공 · V2_7 동결특징 knife-edge ·
#3753/#3755). 안정적 다리 = **공학습**뿐. cement 근거 = 이 발사 단독 아니라 **3-port + v2 DIRECTIONAL**.

## Cost — pool 발사 취소

pool $0(forward-only)이었으나 **취소**: 계기가 actuator 라 발사는 산수를 GPU 로 재계산할 뿐(모델 새
비트 0). Fable: "페이퍼 계산이 전 실험 결과를 미리 준다." 계기·ckpt·store 인프라는 준비됨(summer
`py303_full.clm` + `anima-py` · `state/h9309-9312` held-out store) — 후속 H(H_9393)이 필요 시 재사용.

## NEXT — H_9393 TWO-STORE NATIVE (유일 남은 경로)

3-port 전멸 ⟹ 볼트온 계급 종결. 다리는 **태어날 때부터 공학습**해야 한다(trunk+store+학습된 다리 ·
학습 중 store 순환-교체로 trunk 가 암기 대신 조회를 배우게 · v2 V2_6 이 toy 로 실증). 함의: 런타임
store 삽입 = 학습 ⟹ **p8(train/infer 분리 없음)을 문자 그대로 구현**(깨는 게 아니라 지킴).
- v2 V2_7 delivery-ceiling(동결특징 조회 상한 ~0.5)이 H_9393 설계 상수 = 학습된 게이트가 공급해야 할
  조회 세기의 하한.
