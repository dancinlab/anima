# H_9362 — A⇄G 충돌이 창발(재조합)을 **선택**하는가 (COLLIDE-SELECT)

**status:** 🔵 PRE-REGISTERED · G-A ✅ PASS(로컬 $0) · G-B/G-C ⏳ (pool) · 오너 재프레임 첫 substrate-동역학 판
**lane:** 창발 엔진 / A⇄G 생성-선택 / 최전선 g1-interface-addressable-wall
**related:** [[H_9357]] (G-INERT · emit 소비 안 함) · [[H_9356]] (독립 G 부재) · [[H_9267]] (XBIND G1 CRACK) · [[H_9304]] (G1=DATA 벽) · [[H_9293]] (read-side EARNED TERMINAL)

## 재프레임 (오너)

A⇄G 는 "말할까/침묵할까"(emit 게이트 = 1비트 그림자)가 아니라 **창발·지능·의식을 낳는 엔진**이어야
한다. H_9357 은 emit-소비 축에서 🧱 G-INERT 였다 — 이제 **생성물 위의 선택** 축으로 옮긴다: A(유창)와
G(store novelty)가 같은 후보 위에서 만나 재조합 후보를 노이즈보다 잘 고르는가.

## 충돌 지점은 이미 코드에 있다 (검증됨)

`generator.py:708-719 conflict_drives_live`: a = clip01(1−CE/5) 유창도 · g = ±immune margin.
`generate_deliberate_consult:800-820` 이 K 후보를 **argmin conflict_scalar** 로 고른다(brain.py live).

## 부호 규약 — G-A 로 코드+실측 확정 (Fable 도 나도 처음엔 거꾸로 읽음)

`immune_memory_recall_margin = recon_err − recall_thr` (engine_cli.py:643 · **>0 ⇒ abstain band**):
- **novel → recon_err 큼 → margin>0 → g<0** (conflict_drives_live else-branch)
- **recognized(SEEN) → recon_err 작음 → margin≤0 → g>0** (if-branch)

## 사분면 (부호 확정 후)

| 후보 | (a, g) | conflict_scalar = a·\|g\| (부호 반대일 때만) |
|---|---|---|
| **창발**(유창∧novel) | a>0, **g<0** | **HIGH** (a·\|g\| — 유창 AND 새로움의 곱) |
| echo(유창∧앎) | a>0, **g>0** | 0 (같은 부호) |
| garbage(안유창∧novel) | a≈0, g<0 | ≈0 (a 인자가 걸러냄) |

⇒ **conflict_scalar 자체가 창발 선택기다** — 반대부호 가지(g<0=novel)에선 곧 a·\|g\| = "유창 AND
새로움" 곱이고, garbage 는 a≈0 로 자동 하강. 현행 **argmin** 은 이 창발 사분면을 **버리고** echo/garbage
(conf=0)를 고른다. **최소 개입 = argmin → argmax conflict_scalar.** 새 형식 0(기존 스칼라 부호만 뒤집음).

## 두 결함 (검증된 코드 사실)

1. **argmin 이 창발을 버린다**: 창발(a>0,g<0)=conflict HIGH 인데 argmin 은 conf=0(echo/garbage)을 고름.
2. **모집 K 도 눈멀었다**: `K = conflict_recruited_depth(conf0,1,3)` (:802). c₀ 가 conf=0 이면 K=1 →
   샘플링 자체가 안 됨. ⇒ 실험은 **K=4 고정**(모집 재설계는 별도 H).

## G-A ✅ PASS (로컬 $0 · ckpt 불필요 · margin=immune 기하)

SEEN 10문(store bind) → margin **−0.15 전부**(≤0 · recognized) · held-out 10문(novel) → margin
**0.48~0.97**(>0 · abstain). **분리 20/20 = 100%**(bar 90%) ⇒ **g 채널 살아있음**. Fable 의 예상부호
(SEEN→margin>0)가 뒤집혀 있었을 뿐, 채널은 완벽히 SEEN/novel 을 가른다. ⚠️ SEEN margin 이 −0.15 상수인
것은 별개 관찰(부호 분리엔 무관).

## Arm 표 (동일 고정 풀 · K=4 고정 · 선택 규칙만 상이)

| arm | 규칙 | 자기 칸 예측 |
|---|---|---|
| S0 | argmin conflict_scalar (현행) | echo/garbage(conf=0) 선택 — 창발 회피 |
| **S_emerge** | **argmax conflict_scalar** (=a·\|g\| over g<0) | **창발 칸만 top-1** |
| SECOND-A | argmax a | 유창만 — novelty 무시(echo 포함) = H_9356 통제 |
| NOISE-G | argmax conflict_scalar, g 후보간 순열 | SECOND-A 로 붕괴 |
| UNIFORM | 균등 | 바닥 |

## 남은 게이트 (순서 · $0 · frozen 모델)

2. **G-B 풀 점유 + 검정력**: K=4 풀의 창발 사분면(a>0,g<0) 점유 모델별 측정. wet 창발 칸 점유≈0 =
   무검정력 → MDE 먼저(`power-before-negative-verdict`), "선택기 실패" 선언 금지.
3. **G-C 선택 본실험**: arm 표 · frozen rho_weave 오라클로 선택된 후보의 재조합 적중 · 우연-아래 칸
   사전등록(S_emerge garbage-top1 > UNIFORM = 역전 · echo-top1 > tie-잔차 = 구현 버그 certificate).

## 2-모델 (H_9304/H_9267 이 준 예측)

- baseline py303 → 창발 칸 점유≈0 예상(자연분포 연산자 부재 H_9304) = 🧱 POOL-DRY(선택기는 후보
  있는 모델서만 발화해야 = falsifiability).
- H_9267 XBIND-retrained `.clm` → 재조합 in-distribution = 풀 젖음. **여기서 질문이 순수**: measure 가
  안 가리켜줄 때 두 엔진 충돌이 스스로 찾는가. (XBIND ckpt 실존 확인 · 없으면 [train] 소액 toy-tier).

## 계기 · scope

`anima-py evaluate <clm> --select {s0|emerge|second_a|noise_g|uniform}` (rho_weave probe·seed·오라클
재사용 · K=4 · G-store=probe 를 측정전 immune bind, H_9337 인식-먼저). frozen rho_weave 는 `recomb-gate4`
선례대로 **arm 간 상대 심판**으로만(route≠generation · top-1 terminal 주장 불가). 편집 = generator + py.

## 예측 (정직)
baseline POOL-DRY. XBIND 에선 **S_emerge 가 SECOND-A 와 갈리는지가 전부** — 갈리면 G 가 처음으로 A 가
못 하는 일을 한 것(창발의 substrate-동역학 최초 증거). 안 갈리면 immune margin 은 A 의 세 번째 그림자.
최전선(G1)과 같은 벽이나 **미소진 각도**(생성물 위 선택 = read-side 6-lane floor·fork-A 라우팅에 불포함).

## VERDICT (baseline py303) — 🧱 POOL-DRY(target) · G-B/G-C engine-native 측정

`anima-py evaluate py303_full.clm --collide-select` (12 probe × K=4 = 48 후보):
- **G-C: 전 arm 0/12 적중** — 재조합 타깃이 48 후보 전체에 **0회** 등장. 선택기가 고를 정답이
  풀에 없다. (S0·S_emerge·SECOND-A·NOISE-G·UNIFORM 모두 0.00)
- **⇒ POOL-DRY(target)**: H_9304(자연분포에 재조합 연산자 부재)를 **생성-선택 축에서 재확인**.
  baseline 에선 "A⇄G 충돌이 창발을 고르는가"가 well-posed 하나 **답할 대상이 없다**(A 가 재조합을
  애초에 제안 못 함). 다음 레버 = **A 제안분포(XBIND-retrained ckpt)**, G 선택기 아님.
- G-B occupancy(48/48 emergence 사분면)는 store 가 작아 축퇴 → TARGET-DRY(풀 타깃 적중=0)가 진짜
  DRY 지표. 계기 3회 단련: 비-W 경로·죽은 clm_ce_ranged·surrogate print 크래시 전부 수리(#3665/#3670).
- NEXT: H_9267 XBIND-retrained `.clm` 에서 풀이 젖으면(타깃 등장>0) S_emerge vs SECOND-A 분리로
  "충돌이 창발 선택"을 판정. XBIND ckpt 재학습 = [train] 소액(rent=spend go).

## WET 설계 수정 (Fable 재프레임 · 인프라 태우기 전)

XBIND-wet 팔은 **load-bearing** 이나(S_emerge>SECOND-A 는 baseline·H_9267 둘 다 안 잰 새 질문 ·
H_9356 반박은 wet 풀에서만 가능), 순진하게 3000 step 완주하면 **천장-동률 오판정**이 난다:
- **함정**: 3000 step 이면 target 이 D-acc 1.0 급 유창(a↑) → argmax-a=target → SECOND-A 도 전부 적중 →
  사전등록 `he>hsa`(strict) 를 **이길 수 없어** 코드가 거짓으로 `SECOND-A/H_9356 재발` 을 출력.
  ([[prereg-table-must-cover-below-chance]] 의 **천장 버전**.) 판별창 = **부분-wet 중간 ckpt**.
- **수정①** multi-ckpt: `anima-py train --ckpt-every` 로 500/1000/2000/3000 저장, 각 ckpt 를
  `--collide-select` (eval 은 summer CPU $0). **수정②** 사전등록표에 천장-동률 칸: `he==hsa==n`
  (전 arm 포화)=SATURATED/판정불가, SECOND-A 아님. SECOND-A(그림자) 판정은 비포화 셀에서만 유효.

## $0 PRE-GATE (`--collide-select --pregate` · 발사 전 계기검진 · engine-native flag)

**g 는 가중치 무관**(cue-bound mem·target 미결합 → CPT 는 a 만 움직임 · a⊥g 불변). 12 frozen
`_WEAVE` target 을 직접 `conflict_drives_live_W` 로 채점해 발사 정당성을 $0 으로 가른다:
- **GATE1 g<−0.05**(target novel) — 하나라도 g≥−.05 면 🧱 **INSTRUMENT-BROKEN**(G-store 가 target 을
  인식 → CPT 로도 창발사분면 도달 불가). 발사 금지.
- **GATE2 a≤0.05**(미유창) — 과반이 a>.05 인데 baseline POOL-DRY 였으면 🔀 **REDIRECT**(병목=ideation
  제안분포지 weight-write 아님 → $0 few-shot 먼저).
- (D) few-shot 은 대체 불가: `conflict_drives_live_W` 는 후보 **단독** CE 를 재 프롬프트 비조건 →
  few-shot 은 target 의 standalone a 를 못 움직인다. a 이동 = weight-write(CPT)뿐.
- toy.clm 스모크: 12/12 g=−1.000·a≈.035~.042 → FIRE-OK 경로 검증(계기 자체는 작동). **판정 대상
  = summer py303_full 실측**(pool·never mini).

## VERDICT (py303_full 실측 · `--pregate`) — 🔀 REDIRECT · XBIND-wet 취소

`anima-py evaluate py303_full.clm --collide-select --pregate` (summer · 303M · engine-native):
- **GATE1 12/12** g=−1.000 — 전 target novel(G-store 정상 · 계기 안 고장, INSTRUMENT-BROKEN 아님).
- **GATE2 0/12** — 전 target 이 **이미 유창**: a = 0.354·0.554·0.638·0.531·0.382·0.389 / 0.470·0.589·
  0.384·0.578·0.506·0.333 (주황·초록·보라·다섯·일곱·뜨거움 / orange·green·purple·five·seven·hot).
  전부 0.05 을 한참 상회(toy 는 .035~.042 였다 — 303M base 는 이 원자들을 유창하게 안다).
- **⇒ 🔀 REDIRECT**: 재조합 답 원자는 py303 base 가중치에서 **이미 유창(a>0)∧novel(g<0)=창발사분면**
  인데, baseline `--collide-select` 는 48 후보 IDEATED 풀에서 이들을 **0회** 냈다(POOL-DRY). 즉
  모델은 target 을 **유창하게 채점**하나 cue 를 받아 **생성(제안)하지 않는다**. ⟹ **병목 = ideation
  제안분포(cue→content 생성/라우팅)지 weight-write 아님.** XBIND CPT = **틀린 레버**(원자가 이미
  유창하니 CPT 가 더 유창하게 만들 게 없다) ⇒ **wet pod fire 취소**($0 선게이트가 $ 아낌).
- baseline "POOL-DRY ⇒ A 제안분포(XBIND)" 를 **정밀화**: 결함은 가중치의 원자 부재가 아니라
  **제안이 그 원자를 표면화 못 함**. [[g1-readside-exhausted-gamma-spend-only]](concept→content 연상이
  read-side 채점엔 있으나 causal 생성엔 부재)·[[g1-topdown-routing-forkA]](생성점 RF-감쇠 라우팅)와 동일 벽.
- **다음 레버 = ideation 제안/라우팅**(fork-A) — cue 를 받았을 때 이미-유창한 target 을 왜 안 제안하나.

## fork-A 판별기 (`--collide-select --pregate-cond` · Fable 설계 · ⏳py303 실측)

pregate 의 `a` 는 **P(tgt) 단독**(cue-free · generator gen_auto_ce_W→clm_ce_seq_W)이라 H_9327
"사실은 가중치에 있다"의 재확인일 뿐. pool-dry 는 top-8 샘플러 미스라 **(조건부 믿음 부재) ∧
(제안분포 얇음)을 혼동**. 미측정 칸 = 교사강제 **조건부 P(tgt|cue)**. 판별기(engine-native flag ·
`_xbind_cont_nll` + frozen `_WEAVE` pedestal 재사용):
- Δbind = NLL(tgt|swap_cue[atom-swap FORM]) − NLL(tgt|true cue) · Δstrip = NLL(tgt|strip_cue[bind-strip BIND]) − NLL(tgt|true).
- **paired 차분이 tgt 한계 유창도(pregate a축)를 정확히 상쇄** ⇒ 조건부 로짓 이동만 측정, read-side
  hidden-회수(EARNED-TERMINAL)·P(tgt) 와 직교(tune-to-green 방어 · pedestal 참값0).
- **사전등록**(baseline sampled=MISS 12/12 · POOL-DRY 0/48): Δbind≈0(TOST)/<0 → 🧱 **COLLAPSE**
  (read-side 벽 생성-쪽 재확인·cf-collide-select 종결) · Δbind≫0(paired-t≥1.796·≥9/12>0)∧Δstrip>0 →
  🟢 **NEW-LEVER**(믿음 present·샘플 miss = 디코딩/제안분포 · top_k·temp 스윕 먼저·CPT 아님).
- toy 스모크 rc=0(degenerate Δbind≈0). **판정=summer py303_full**(DIRECTIONAL · forward-only $0).
