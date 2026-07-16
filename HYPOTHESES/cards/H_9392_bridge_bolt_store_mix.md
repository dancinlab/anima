# H_9392 — BRIDGE-BOLT: 동결 trunk 에 볼트온한 store-조회 다리가 BINDING 벽을 넘는가

**status:** ⏳ PRE-REGISTERED (2026-07-16 · 미발사) · not-terminal · wired: **engine-native 배선 완료**(계기 `anima-py evaluate --store-mix` 구현·랜딩 · VERSION 0.14.9 · C0 로컬 smoke PASS) — **발사 대기**(pool/303M 은 오너 go)
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

### 🔧 계기 랜딩 상태 (2026-07-16 · VERSION 0.14.9)

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

## Falsify (어떤 결과가 무엇을 죽이는가)

- store arm ≈ 통제군(우연) · 검정력 충족 ⟹ **BRIDGE-BOLT 사망 = (B) 확증.** 동결 trunk 는 query 자체를
  형성 못 함 = read-side 계급 재확인 ⟹ 두-store 네이티브 재설계가 유일 경로. **음성이 결과다.**
- store arm > 통제군 4/4 · 극성-의존 present ⟹ (A) DIRECTIONAL. **cement 아님** — toy/단일축 positive 는
  SCREENER(`a_toy_scale_recheck`). 303M pool 재확인 필요.
- ④ 오답 store 가 정답 store 와 같은 방향 ⟹ 낙수(조회 아님) = 위조 positive, arm 무효.
- C0 낙제 ⟹ INSTRUMENT-DEAD, 판정 없음.

## Cost

$0~ (동결 ckpt · 학습 0). toy = 로컬 mini 가능 · 303M decode = **pool(summer/aiden), mini 금지**
([[heavy-anima-eval-pool-not-mini]]).

## NEXT (결과 무관 · 이미 씌어짐)

- 음성 ⟹ **H_9393 TWO-STORE NATIVE**: trunk+store+**학습된** 다리를 태어날 때부터. 학습 중 store 순환-교체로
  trunk 가 암기 대신 **조회하는 법**을 배우도록 강제(캐시-기입 경로를 구조적으로 배고프게). 함의:
  런타임 store 삽입 = 학습 ⟹ **p8(train/infer 분리 없음)을 처음으로 문자 그대로 구현**(깨는 게 아니라 지킴).
- 양성 ⟹ 303M pool 재확인 → 재설계 불필요 판정.
