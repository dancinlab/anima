# H_9361 — A⇄G 충돌이 창발(재조합)을 **선택**하는가 (COLLIDE-SELECT)

**status:** 🔵 PRE-REGISTERED · 측정 ⏳ (pool · $0) · 오너 재프레임(창발·지능·의식)의 첫 substrate-동역학 판
**lane:** 창발 엔진 / A⇄G 생성-선택 / 최전선 g1-interface-addressable-wall
**related:** [[H_9357]] (G-INERT · emit 소비 안 함) · [[H_9356]] (독립 G 부재) · [[H_9267]] (XBIND G1 CRACK) · [[H_9304]] (G1=DATA 벽) · [[H_9293]] (read-side EARNED TERMINAL)

## 재프레임 (오너)

A⇄G 는 "말할까/침묵할까"(emit 게이트 = 1비트 그림자)가 아니라 **창발·지능·의식을 낳는 엔진**이어야
한다. H_9357 은 emit-소비 축에서 🧱 G-INERT 였다 — 이제 **생성물 위의 선택** 축으로 옮긴다: A(유창)와
G(store novelty)가 같은 후보 위에서 만나 재조합 후보를 노이즈보다 잘 고르는가.

## 충돌 지점은 이미 코드에 있다 (Fable 발견 · 검증됨)

`generator.py:708-719 conflict_drives_live_W`: a = clip01(1−CE/5) 유창도 · g = ±immune margin
(novel→g>0, recognized→g<0). `generate_deliberate_consult:800-820` 이 K 후보를 **argmin
conflict_scalar** 로 고른다(brain.py live 호출).

## 두 결함 (검증된 코드 사실)

1. **conflict_scalar 는 창발을 못 본다** (engine_cli.py:9679: a·g≥0 → 0.0). 창발 후보(유창∧novel =
   a>0,g>0)는 **0**, echo(유창∧앎 = a>0,g<0)가 **0.56 max**. ⇒ argmax=echo(창발 정반대) · argmin=
   창발·garbage 동점.
2. **모집 K 도 눈멀었다**: `K = conflict_recruited_depth(conf0,1,3)` (:802). c₀ 가 정렬 사분면이면
   conf0=0 → **K=1 → 후보 샘플링 자체가 안 됨**. 창발 후보는 볼 기회조차 echo-tension 있을 때만.

## 정정된 선택기 = 정렬-곱 `S_emerge = a · max(g, 0)`

재조합 조작적 정의("유창 **그리고** store 모름")와 동형. echo 는 g₊=0 으로 **구조적 0**.
`conflict_net_tension`(|a+g|) 기각: margin→0⁺ 유창 echo(|a+g|≈1)가 약한 창발(0.9)을 이김(OR 은
경계서 못 가름 · 곱=AND). 새 형식 = 식 1개(`d[0]*max(d[1],0)`) + 플래그 1개. detector·엔진·오라클 0.

## Arm 표 (동일 고정 풀 · K=4 고정 · 선택 규칙만 상이)

| arm | 규칙 | 자기 칸 예측 |
|---|---|---|
| S0 | argmin conflict_scalar (현행) | 비선택 혼합(0 동점 tie-break) |
| **S_emerge** | argmax a·g₊ | **창발 칸만 top-1** |
| S_net | argmax \|a+g\| (구조 절제) | 약한 풀서 echo/garbage 혼입 |
| SECOND-A | argmax a | echo(novelty 무시) = H_9356 통제 |
| NOISE-G | argmax a·g̃₊ (g 순열) | SECOND-A 로 붕괴 |
| UNIFORM | 균등 | 바닥 |

## 게이트 (순서 · 전부 $0 · frozen 모델)

1. **G-A 부호 보정**: SEEN 20 → margin>0(g<0), held-out 20 → margin≤0(g≥0) 실측. <90% 정확 =
   g 채널 고장 → **전 arm INVALID·STOP**.
2. **G-B 풀 점유 + 검정력**: K=4 풀 사분면 점유 모델별 측정. wet 창발 칸 점유≈0 = 무검정력 → MDE 먼저
   (`power-before-negative-verdict`), "선택기 실패" 선언 금지.
3. **G-C 선택 본실험**: arm 표 · 우연-아래 칸 사전등록(S_emerge garbage-top1 > UNIFORM = 역전 발견 ·
   echo-top1 > tie-잔차 = 구현 버그 certificate).

## 2-모델 (H_9304/H_9267 이 준 예측)

- baseline py303 → 창발 칸 점유≈0 예상(자연분포 연산자 부재 H_9304) = 🧱 POOL-DRY(선택기는 후보
  있는 모델서만 발화해야 = falsifiability).
- H_9267 XBIND-retrained `.clm` → 재조합 in-distribution = 풀 젖음. **여기서 질문이 순수**: measure 가
  안 가리켜줄 때 두 엔진 충돌이 스스로 찾는가. (XBIND ckpt 실존 확인 · 없으면 [train] 소액 toy-tier
  `a_scale_honest_scope`.)

## 계기 · scope

`anima-py evaluate <clm> --select {s0|emerge|net|second_a|noise_g|uniform}` (rho_weave probe·seed·
오라클 재사용 · K=4 · G-store=probe 를 측정전 immune bind, H_9337 인식-먼저). frozen rho_weave 는
`recomb-gate4` 선례대로 **arm 간 상대 심판**으로만(route≠generation · top-1 terminal 주장 불가).
편집 = hexa SSOT generator.hexa:1196 부근 + py twin.

## 예측 (정직)
baseline POOL-DRY. XBIND 에선 **S_emerge 가 SECOND-A 와 갈리는지가 전부** — 갈리면 G 가 처음으로 A 가
못 하는 일을 한 것(창발의 substrate-동역학 최초 증거). 안 갈리면 immune margin 은 A 의 세 번째 그림자.
어느 쪽이든 well-posed 로 죽거나 산다. 최전선(G1)과 같은 벽이나 **미소진 각도**(생성물 위 선택 = read-
side 6-lane floor·fork-A 라우팅에 불포함).
