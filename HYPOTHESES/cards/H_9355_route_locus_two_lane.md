# H_9355 — LOCUS-CAUSAL (감사 파트): 두 lane 은 **물리적으로 다른 expert** 에 사는가

- group: `g1-interface-addressable-wall`
- date: 2026-07-15
- tier: 🔵 PRE-REGISTERED — bar·통제·kill 을 **수치 보기 전** 동결(코드 상수로 박음). 계기 = `anima-py evaluate --route-audit`(engine-native · 학습 0 · 판정 경로 불변)
- 계기: `cli/evaluate.py::route_audit_run` · `core/decode.py::clm_forward_routes` · 매니페스트 `anima-py corpus routeaudit`
- xref: H_9327(BINDING 🧱) · H_9329(C3) · H_9334(C4) · H_9331(BIND-LOCUS) · H_9346(EN ECHO) · `recomb-gate4-clml-forka-killed`(구분 대상)

## 질문

C3/C4 는 **행동**으로 two-lane 을 시사했다: 선언 lane 과 연산자 lane 이 각자 사실 엔트리를 갖고 값을 공유하지 않는다.
이 가설은 이 기질에서 답할 수 있는 **물리적 예측 하나**를 낸다 —

> 두 lane 이 **다른 저장소**라면, 두 표면은 **다른 expert 가 계산**해야 한다.

ConvMoE(E=3)의 라우터는 "어떤 기계가 돌았나"가 **명시적으로 적히는 유일한 자리**이고,
그 수치는 **모델 자신이 방출**한다(hidden 위 선형프로브의 의견이 아니다 — read-side-exhausted 교훈).

- **LOCUS-SPLIT** ⟹ two-lane 은 **물리적** · 추론시 라우터 편향(**route-pin**) 이 "쓰지 않고 읽기" 후보로 승격
- **LOCUS-SHARED** ⟹ 두 lane 은 **한 기계 안**에 있다 ⟹ 격차는 저장소 분리가 아니라 **코딩/기하** · route-pin 은 발사 전 사망

⚠️ **죽은 forkA(Gate4 · `eval_rho_weave`)와 다른 질문**: 그건 G1 ideation 지표의 *판독-라우팅 재프레임*이었고 frame-mismatch 로 죽었다.
이건 **살아있는 ConvMoE 에서 쓰기가 어디 착륙하는가**의 감사다(다른 객체 · 다른 질문 · 원장 확인함).

## 계기 (engine-native)

`anima-py evaluate <ckpt> --route-audit <m.json> [--vs <ckpt2>] --out <f.json>`
- `core/decode.py::_fwd_trunk` 에 **routes 탭** 추가 — 라우터 소프트맥스 `probs[T,E]` 를 방출. 믹서 **바깥**에 앉혔으므로 디코드 forward 는 비트 단위로 불변.
- 읽는 점 3개: `ans`(t=T−1 · 답의 첫 바이트를 만드는 자리 = **PRIMARY**) · `stem`(어간 바이트 span) · `win`(패딩 제외 전 구간).
- `--vs` = **같은 프로세스·같은 장치**에서 두 번째 ckpt 를 돌려 pre/post-CPT 라우팅 차이(D_CPT)를 낸다.
  두 프로세스로 나누면 CPU/GPU 교차 시 라우터 로짓이 1e-14 달라진다(`decode-py-4`) — 장치 교란을 **구조적으로 불가능**하게 만든다.

## 표면 (H_9327/C4 에서 **축자 상속** · 재구성 금지)

| 태그 | 담체 | 역할 |
|---|---|---|
| `flip0` | `이 영화 {s}고 => ` | **선언 lane** — CPT 가 쓰는 자리(WRITE 0.98) |
| `negL` | `이 영화 {s}지 않다 => ` | **연산자 lane** 강표면 1 |
| `negZ` | `이 영화 별로 {s}지 않다 => ` | **연산자 lane** 강표면 2 |
| `negJ` | `이 영화 {s}지는 않다 => ` | **통제 ①b** — negL 의 문자열 쌍둥이인데 **연산자가 안 돈다**(C1b p≈.50) |
| `ped` | `이 영화 {s}고 있다 => ` | **통제 ①** — negL 의 `지 않다`(10 B)와 **바이트 길이 정합**한 무의미 접미 |

라우터는 **바이트 문자열의 함수**다 ⇒ flip0→negL 은 **자명하게** 라우팅을 움직인다(문자열이 다르니까).
질문은 "**같은 길이의 무의미 접미보다 더** 움직이는가" ⟹ 어간 내 **paired** 대비. **max(controls) 순서통계량 금지**.

원자셋 = `gt_atoms.json`(SEEN 20 / held-out 29) × 5 표면 = **245 프롬프트/ckpt**.

## DV · 동결 bar (코드 상수 · 절대 안 움직임)

- 거리 = **JS divergence(bits)** — 알파벳 크기와 무관하게 [0,1] 로 유계 ⟹ 라우팅을 한 줄도 보기 전에 **절대 bar** 를 박을 수 있다.
- **DV**: `dOP = mean_stem [ JS(flip0, negX) − JS(flip0, ped) ]`, X ∈ {negL, negZ} (어간 내 paired)

| 게이트 | 내용 | 실패 시 |
|---|---|---|
| **G-SHAM** | `JS(p,p) == 0` 전 항목 | ⛔ INVALID-ESTIMATOR |
| **G-LIVE** | `J_STEM`(같은 표면 · 다른 어간 두 개의 JS 평균) **≥ 0.0001 bits** | ⚪ **ROUTE-INDIFFERENT** — 라우터가 내용에 무관 ⇒ **이 렌즈 폐기**(정직한 음성 · **벽 아님** · 두 모형 어느 쪽도 지지 못함) |
| **DV+** | `dOP ≥ 0.05 bits` **양 강표면** ∧ 부호뒤집기 순열 `p ≤ .01` ∧ **양 seed 부호 일치** | 🟢 **LOCUS-SPLIT** |
| **DV−** | `dOP` 의 90% CI 가 **±0.02 bits** 안(TOST) · 양 강표면 | 🔵 **LOCUS-SHARED** |
| 그 외 | — | ⏳ **UNDERPOWERED** (se·MDE 보고 · bar 이동 금지 · power-before-negative) |
| **OP-SPEC** | `dOPJ = mean[JS(flip0,negL) − JS(flip0,negJ)]` — 병기 보고. negJ 가 재현하는 split 은 **연산자 옷을 입은 문자열 효과** |
| **통제 ②** | `J_POL` = flip0 표면 안에서 pol=1 군평균 vs pol=0 군평균의 JS — **표면 효과 ⊥ 극성 효과** 분리 |

부수(사전등록 bar 없음 · 서술만): **D_CPT** = 표면별 `JS(route_base, route_post)`(C4 ckpt). 쓰기가 **어느 표면의 라우팅을 움직였나**.

## 실행

- ckpt: `natem_c34_main_s{7,11}.clm`(base · CPT 전) · `swap_c4_s{7,11}.clm`(C4 = 담체 키로 쓴 post)
- 호스트: **pool(summer)** — mini 금지. GPU/CPU 어느 쪽이든 **네 ckpt 전부 같은 장치**(`--vs` 가 base/post 를 한 프로세스에 묶고, 장치 불일치면 채점 거부).
- 판정 = `ans` 읽는 점(primary). `stem`/`win` 은 함께 보고.

## kill-criterion (정직)

- 라우팅이 표면 간 **무차별**(G-LIVE 미달 또는 dOP 가 pedestal 과 구분 안 됨) ⟹ **이 렌즈를 폐기**하고 음성으로 박제한다. 벽 선언 아님.
- `rc=137/143/247` · SSH wedge = **infra-wall**, 결과 아님.
- 어떤 경우에도 bar 재조정 금지(tune-to-green).

## 판독

⏳ **PENDING · 측정 BLOCKED-INFRA (과학 결과 아님 · 벽 아님)** — bar 는 코드 상수로 동결됨. 계기는 **배선 완료 + 토이 검증 완료**, 303M 측정만 pool 포화로 막혔다.

### 계기 검증 (토이 ckpt · 실측 · $0)
`state/9257_lane23b/toy.clm`(E=2·L=2) 에서 전 경로가 돈다:
- **G-SPIKE 🟢** `JS(one-hot A, one-hot B) = 1.000000`(참값 1.0) ∧ `JS(u,u) = 0.000e+00` — 추정기가 참값-아는 pedestal 을 정확히 재현.
- **G-SHAM 🟢** `JS(p,p) max = 0.000e+00` 전 항목.
- 판정 트리·순열·strata·`--vs` D_CPT·top-expert 히스토그램 전부 출력. 라우터 탭은 믹서 **바깥**이라 디코드 forward 비트 불변(구성상 보장).
- 245 프롬프트 매니페스트 결정적 재생성(md5 `865b83993fed` · SEEN 20 / held-out 145 항목 · 5 표면).

### 왜 측정을 못 했나 (infra-wall · 실측 증거)
pool 유일 303M 호스트 summer 가 **전 세션 내내 wedge**(load ~20 · 병렬 세션 8+ 레인 · RAM 21/30 GB · swap+disk thrash):
- s7 1차: **rc=143**(earlyoom `--prefer python3` 정책 kill · item 1/245 에서 사망).
- s7 solo 재시도: **D-state(uninterruptible disk-I/O) 5분간 CPU 22s** = 93% I/O 대기 · **python/numpy startup 조차** I/O starved(로그 파일 생성도 안 됨) · **rc=241**.
- s11: D-state 15분 무진행(RSS 1GB 로드했으나 swap 으로 밀림).
- 3회 독립 사망 전부 infra 계열 exit(137/143/247 족) — task 규율상 **결과가 아니라 infra-wall**.

### 재개 레시피 (한 명령 · host 여유 시)
자산 보존됨: `~/h9355_route_wf6/{natem_c34_main_s7,natem_c34_main_s11,swap_c4_s7,swap_c4_s11}.clm` + `ra_manifest.json`(전부 md5 검증) · 격리 venv `~/h9355/.venv9355`.
```
anima-py evaluate natem_c34_main_s7.clm  --route-audit ra_manifest.json --vs swap_c4_s7.clm  --out ra_s7.json  --perm 10000
anima-py evaluate natem_c34_main_s11.clm --route-audit ra_manifest.json --vs swap_c4_s11.clm --out ra_s11.json --perm 10000
```
seed 간 **부호 일치** 확인 후 위 동결표대로 판정. summer drain 대기(solo 순차) 또는 전용 pod. **mini 금지.**

정직: 이건 **못 잰 것**이지 **음성이 아니다**. bar 는 옮기지 않았고, 계기는 살아있다.
