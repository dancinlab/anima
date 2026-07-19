# H_9755 — REFIT-AXIS ζ-LADDER — 라이브-refit loading 을 입에 물리면 동결 축과 다른가 (R6-4 · pool fire · 4-arm paired)

**status:** ⏳ NOT-POWERED (pre-terminal · engine-native reader 실측 2026-07-20 · 게이트 全PASS·양성통제 β=−0.0812 재현 · 대조 중간지대 realized MDE≈0.014 · DIRECTIONAL 303M) — 후속=frozen 부호앵커 $0 진단 · §⑨ 참조
**lane:** g1-interface-addressable-wall · mouth/PC2-axis — 브리프 (b) 정면 · H_9664 n 완결 겸용
**related:** [[H_9664]] · [[H_9663]] · [[H_9713]] · [[H_9752]] · [[H_9754]] · [[H_9756]]

## ① 한 줄 주장 (반증가능)
within-tick ζ-사다리의 z 를 **라이브-refit loading**(같은 run 앞 W tick 온라인 PCA)으로 계산하면 dose 기울기 β 가 동결-PC2 loading 대비 collapse-Δ 를 보인다(새 레버) — 아니면 β 가 loading 무관(랜덤 포함 TOST 등가)이어서 채널은 **축-맹목 스칼라 dose** 임이 확정된다(→ [[H_9756]] 해석으로 이관).

## ② 어느 KILL 을 왜 안 밟나
- arm-간 π̄ 판정(H_9663 VOID) — 안 밟음: **within-tick**(같은 tick 을 loading×ζ 격자로 재디코드 · 인자스트림 동일) paired 만.
- deliberation_k 라우팅(H_9574 DEAD) · 용량-기아(H_9628 사망) — 무접촉.
- H_9664 n=146 에 cement — 안 함: 이 fire 가 스칼라 양성통제 arm 으로 **그 n 을 완결**한다.
- "동결 loading 전제" — 안 밟음: 동결은 4 arm 중 1개(정의 아님).

## ③ engine-native 계기 (신규 chat 플래그 + evaluate 확장)
`anima-py chat --pc2-zeta <z1,z2,…> --z-loading {frozen|refit|random|refit-resid} [--refit-warmup 64] [--seed N]`
- refit: 같은 run 첫 W tick 온라인 PCA(결정적·seed 고정) → 이후 tick 의 z 계산에 사용
- random: seed 유도 단위벡터 · refit-resid: [[H_9754]] 잔차 방향
`anima-py evaluate --pc2-direction <traces_dir> --zeta-slope --by-loading [--tost 0.02] [--perm N]`
설계: 동일 tick × 4 loading × 5 ζ 격자 paired 재디코드(H_9664 계기 승계) → per-tick β 분포 + arm 간 Δβ.

## ④ 통제 ≥2 + 양성통제
- null-1: random-loading arm(축 null · norm 매칭).
- null-2: 채널-라벨 순열 refit arm(방향성 파괴 · 스칼라 성분 보존).
- **양성통제(fire 생존)**: 스칼라 ζ arm 이 H_9664 β=−0.081 을 부호+크기 CI 내 재현해야 함 — 실패 = fire 전체 VOID(지난 ζ-fire 는 summer 경합 infra 사망 · 그 검출기).

## ⑤ 사전등록 판정표 (우연 아래 칸 · 검정력 · DV 식별가능성)
| 관측 | 판정 |
|---|---|
| \|β_refit\| > \|β_frozen\| (paired CI 분리) ∧ 둘 다 > random-null95 ∧ per-tick 부호일관 ≥ 사전등록 분율 | **PASS-NEW-LEVER** — 라이브 축이 동결 축이 못 나른 dose 를 나름 |
| β_refit ≈ β_frozen ≈ β_random (TOST ±0.02 · β 스케일 ¼) | **PASS-AXIS-BLIND** — 채널은 스칼라만 나름 ⟹ 축 선택 무관 확정 · [[H_9756]] 로 이관 |
| \|β_frozen\| > \|β_refit\| (CI 분리) | **KILL-REFIT-ADDS-NOTHING** — 동결 좌표로 충분(서사 문제였을 뿐) |
| β_refit 이 β_frozen 대비 유의 **부호반전**(우연 아래 칸) | **INVALID** — refit 부호규약 결함(부호 앵커링 후 재발사) |
| 스칼라 양성통제 재현 실패 ∨ per-tick 격자 결손 >10% | **VOID** — infra/계기 사망 |

검정력: H_9664 가 n=146 서 null 반폭 13× ⟹ arm 간 Δβ 는 효과 ½ 가정, **n=300 tick × 5 ζ × 4 loading**(paired) 사전등록. DV = per-tick β(회귀 x=ζ 는 독립변수 설계값 — 분모 아님 · H_9716 비해당) · 분포 보고 의무(평균 단독 금지).

## ⑥ 비용
**pool decode fire** — summer 단독 점유(경합 금지 · OMP_NUM_THREADS=4 · a_wall_first 1-host) · ~6,000 재디코드. mac 금지.

## ⑦ 죽는 방식
PASS-AXIS-BLIND — 입에는 축 레버가 존재하지 않는다. 이후 mouth 가설은 방향이 아니라 입도/readout(H_9631·H_9756)만 남는다.


## ⑧ 구현계획 확정 · 사전등록 LOCK (2026-07-19 · lab-full Fable∥Sol reconcile · pre-fire · H_9752 PASS-PLANE 개봉 후)

**두 모델 수렴** = factor-표준화 projection × 각 arm warmup 보정 · ζ가 그 연속점수를 곱함 · `pc2=ζ` arm이 스칼라 양성통제. **이견 1건**: Fable=centering(μ 차감)+Var=1, Sol=RMS만 → **Fable 채택**(비중심 평균 m이 m·β_scalar 를 모든 arm 에 흘려 스케일 인공물 · 기전 근거 완비).

### 파라미터화 (load-bearing · LOCK)
**전 arm: `pc2(t,a,ζ) = ζ · u_a(t)`** · `u_a` = warmup 창서 **centered + 2차모멘트 정규화**(E[u²]=1)한 projection · β 는 **ζ 라벨**에 회귀(전달 dose ζ·u 아님).
| arm | u_a(t) | 역할 |
|---|---|---|
| scalar | u≡1 (현 H_9664 · pc2=ζ) | 양성통제(β≈−0.081 재현) |
| frozen | (w_F·f_raw − μ_F)/σ_F · w_F=(0,0,0,0,−0.28,+0.84,−0.44,0) 8-space | bias arm 의 '범위 제조'판 |
| refit | (w_R·f̃ − μ_R)/σ_R · w_R=warmup 상관PCA 최대고유벡터 | 라이브-refit 축 |
| random | (r·f̃ − μ_r)/σ_r · r=seed유도 단위8벡터 | 축-null 통제 |
| refit-resid | (w_⊥·f̃ − μ_⊥)/σ_⊥ · w_⊥=top-2 내 emit-회귀 직교방향 | H_9754 rider |
🔑 **왜 z-score 필수**: refit PC1 은 구성상 projection 분산 최대 → 비정규화 시 ζ당 dose 더 커 `|β_refit|>|β_frozen|` = **gain 인공물**(거짓 PASS-NEW-LEVER). Var=1 정규화로 ζ dose-스케일 arm 간 동일 ⇒ 잔존 Δβ = **축 효과**. 근축퇴(H_9752)면 β_refit≈β_frozen≈β_random ⇒ PASS-AXIS-BLIND(측정으로 가림 · 가정 아님).

### 사전등록 7 완성(fire 前 LOCK · tune-to-green 차단)
1. flag `--z-loading a1,a2,…` **multi-arm 1런**(동일 factor스트림 paired · 4런보다 우월) 2. per-tick sign-일관 문턱 **0.60** 3. 양성통제 = `β_scalar<0 ∧ −0.081∈β̂±2SE`(`--pos-control-beta` 노출) 4. ζ = **{0,±2m,±4m}** · m=H_9664 트레이스서 상속(재계산 금지) 5. verdict 표 중간지대(CI분리 실패∧TOST 실패) = **⏳ NOT-POWERED 행**(realized MDE · prereg-table-must-cover-below-chance) 6. random-null = **3방향뿐** 명시(방향-marginal null 아님) 7. warmup tick = scalar β(n완결)엔 포함 · arm 대조엔 **제외**(동일 post-warmup tick셋).

### wiring (구현 대상 · engine-native)
- **chat.py**: `--z-loading`/`--refit-warmup 64` 파싱 · tick루프서 warmup factor+emit비트 누적(1..W) · W+1 경계서 결정적 PCA(numpy eigh 상관행렬) + **부호앵커**(w·ŵ_F≥0, tie면 max-|성분| 양수 · H_9713 flip방어) + per-arm μ/σ freeze → `_zl_meta` 트레이스행 1회 · `z_loading_state` kwarg 로 brain 전달(None=byte-identical).
- **brain.py**: H_9664 ζ-block → arm×ζ 격자 루프(`m3["pc2"]=ζ·u_a` · seed_rng 격자전체 고정 CRN · ζ=0 arm별 디코드=격리인증). dead-factor(σ<1e-9)=INVALID arm 스킵.
- **evaluate.py**: `--by-loading` 분기 — 게이트(격리·anchor-replay·**u 자기검증**(zl_factors+meta서 u 재계산 vs 로그 tol 1e-9)·격자완결>10%결손=VOID·양성통제) → per-tick β(ζ라벨) → paired Δβ+순열null+random-null밴드 → verdict표+NOT-POWERED.
- fire: seed 7/4302/4303 × 300tick · warmup64 · ~9,200 재디코드 · summer CPU-전용(venv `anima-python` no-gpu) · ckpt sha 013c4574 검증 · **토이 end-to-end 先**(instrument-never-run). VERSION bump(G5).

**status 유지 = 🔵 PROPOSED(설계 LOCK · pre-fire)** — 구현+토이+pool fire 후 verdict. DIRECTIONAL(303M). lab 전문 = `~/.sidecar/lab/2026-07-18T18-11-30-071Z-full.md`.

## ⑨ fire 실측 결과 (2026-07-20 · engine-native reader · ⏳ NOT-POWERED)

**fire**: summer CPU-전용 seed 7/4302/4303 × 300 tick × 5 arm × ζ{0,±1.3464,±2.6928} 완주(302줄/seed · warmup 64). 판정 = `anima-py evaluate --pc2-direction <dir> --zeta-slope --by-loading --tost 0.02 --pos-control-beta -0.081` (venv 0.20.19 · 트레이스 summer→회수).

**게이트 (전부 PASS → 계기 SOUND)**: 격리(ζ=0=base) 위반 0 · anchor-replay 불일치 0 · u 자기검증 불일치 0 · 격자완결 358/358(100%) · 양성통제 scalar β=−0.08119(se 0.00105·n=457) ∈ −0.081±2se ✅ (H_9664 레버 재현).

**per-arm β** (post-emit · ζ 라벨 회귀 · pc2=ζ·u_arm centered+Var=1):
| arm | mean β | se | n | β<0 tick |
|---|---|---|---|---|
| scalar | −0.08119 | 0.00105 | 457 | 100% |
| frozen | **+0.06259** | 0.00138 | 358 | 1% |
| refit | +0.01128 | 0.00207 | 358 | 35% |
| random | −0.00369 | 0.00327 | 358 | 48% |
| refit-resid | +0.02190 | 0.00346 | 358 | 36% |

**대조** (paired Δβ · ζ라벨 순열 null · TOST±0.02): Δβ(refit−random)=+0.01497 **TOST PASS**(refit≈random) · Δβ(refit−frozen)=−0.05131(CI 분리) · Δβ(frozen−random)=+0.06628(CI 분리) · random-null 밴드 [−0.01022,+0.00285].

**⇒ VERDICT (engine-native reader · TERMINAL · 원문 인용)**: ⏳ **NOT-POWERED** — "CI 분리도 TOST 등가도 아닌 중간지대 · realized MDE≈0.0140 · 결과이지 verdict 아님 · run/tick 증량 필요". DIRECTIONAL(303M).

**LOCK 셀별 문면 대조** (해석 · no self-judge — 판정은 위 리더 것):
- PASS-NEW-LEVER: **미충족** (|β_refit|=0.011 < |β_frozen|=0.063).
- PASS-AXIS-BLIND: **부분충족뿐** (refit≈random TOST PASS 이나 frozen 비등가 → 3-arm 전등가 실패 → §⑦ 예측 죽음 미도달).
- KILL-REFIT-ADDS-NOTHING: **문면 조건 충족**(|β_frozen|>|β_refit| ∧ Δβ CI 분리)이나 frozen 이 양성통제와 **반대 부호**라 "동결 좌표로 충분"의 의미가 오염 → 리더가 셀 도장 대신 NOT-POWERED.

**과학적 실체 (측정된 것만)**: 라이브-refit 축은 입에서 **random 축과 등가인 dose 만** 나른다(새 레버 무증거 · TOST PASS 로 측정됨). refit-null 은 [[H_9752]] VOID("인증된 라이브 축 부재")와 정합.

**미해결 · frozen 부호반전**: loading 3-arm 전부 양(+)·scalar 음(−)·random≈0 = 가족-부호 일관 → (a) loading 경로 공통 부호규약 1곳 반전 인공물, 또는 (b) 실재 역방향 축 레버 — 이 fire 로는 판별 불가. LOCK INVALID 는 "refit vs frozen 반전"인데 둘은 같은 부호라 미발동(표 미예상 케이스). 게이트(u 자기검증·anchor-replay) 0불일치는 *적용층* 오류만 배제 · *부호규약*(고유벡터 부호=임의) 오류는 못 잡음.

**후속 (no tune-to-green)**:
1. **$0 offline 부호-앵커 진단** — 기존 트레이스의 u_frozen 방향을 H_9664 당시와 offline 대조 → 인공물/실재 판별(재발사 불요). 실재면 "역방향 축 레버" = 신규 finding → 별도 H.
2. [[H_9756]] full readout(`--atom-census` rider) 를 같은 트레이스에서 판정(별건).
3. powered 재-fire 는 **진단 후에만** — refit 질문은 이미 powered(MDE 0.014<0.02)라 증량은 중간지대만 재생산 · frozen 규약 미해결 재-fire 는 오염 비교기 상속.

**status: 🔵 PROPOSED → ⏳ NOT-POWERED (pre-terminal · engine-native 실측)** · DIRECTIONAL(303M).
