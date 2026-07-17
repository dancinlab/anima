---
id: H_9734
title: NAT-ADDR-SPLIT — read the addr axis (2-seed robust) so H_9683 is readable WITHOUT the RV winner
tier: PROPOSED ⭐ (R8 · lab full Fable+Sol 독립 1순위 · DIRECTIONAL design)
frontier: g1-interface-addressable-wall
created: 2026-07-17
---

# H_9734 (R8·P1) — 판독축을 seed-robust 한 주소축으로 승격

**Origin.** `sidecar lab full` 2026-07-17 — Fable(H_9734 NAT-ADDR-SPLIT) + Sol(NAT-ADDR-SPLIT)이
**독립으로 #1** 지목. [[H_9683]] 의 arm-S 값읽기 seed-fragility 를 estimand 분리로 우회. DESIGN ONLY.

**Claim (one line).** [[H_9683]] 의 1차 DV 를 값읽기(P1)에서 **주소축(addr_top1·addr_mass·addr-gap)**
으로 승격하면, 그 축은 H_9672 서 **2-seed robust** 라 **RV winner 없이 지금 판독가능**하다.

## 왜 이게 우회의 정답인가 (근거 3겹)
1. **주소축은 seed-11 붕괴 속에서도 살았다** — H_9672 자기정정: 값읽기 ORACLE seed-7 0.99 vs
   seed-11 0.50(붕괴)이지만 **addr_top1 0.984 · addr_mass 0.962 = 2-seed robust**(sharp). ⟹ 통제(arm-S)와
   DV 가 같은 축에 서므로 **양성통제 자격이 회복**된다(값읽기축에선 arm-S 가 죽어 자격 상실이던 것).
2. **H_9683 이 이미 제3결과를 사전등록** — "addr 높고 P1 낮음 = 값이 자연 다의성에 익사". 축 승격은
   재발명이 아니라 **그 칸의 승격**.
3. **겨냥 기전이 상륙하는 면이 바로 주소축** — anagram·byte-bag 위치맹 키충돌(D0-key census)이
   학습된 W_q 공간에서 자연어휘로 재출현하면 KILL, 안 하면 🟢 = 양방향 falsifiable.

## Minimal decisive experiment (신규 코드 0 · 계기·pool 전부 기존)
arm-N(nat5) / arm-S(nonce) 동일 **fresh seed {3,17}**(소각 {7,11}·예약 {13} 회피):
```bash
anima-py train --init py303_full.clm --corpus {N,S}_s${S}.txt \
  --store-addr-weight 1.0 --store-addr-audit --canon --seed ${S}
anima-py evaluate {N,S}_s${S}.clm --store HELD_balanced.json --store-addr-audit --store-shuffle
#   OFF arm: arm-N 최소 1 seed --store-addr-weight 0 (벽 재현·byte-id)
```
계기 경로 = `--store ... --store-addr-audit`(H_9683 정정 상속 · NOT `--xbind`).

## Frozen falsifier (사전등록 · 양 seed)
- **계기 게이트**: arm-S `addr_top1 ≥ .95 ∧ addr_mass ≥ .90`, 양 seed(미달 = INSTRUMENT-DEAD ·
  arm-N 미개봉 = GPU 방어).
- **자연 주소전이 🟢**: arm-N `addr_top1 ≥ .90 ∧ addr_mass ≥ .90 ∧ addr-gap ≤ .20`, 양 seed.
- **자연 주소벽 🧱**: arm-S 게이트 통과 중 arm-N `addr_top1 ≤ .60`, 양 seed.
- 중간/seed 불일치 = 미판독. **ORACLE/P1/flip 은 DIAGNOSTIC-ONLY**(windfall: arm-S 값읽기가 우연히
  2/2 통과 시 원 판정표 보너스 개봉 · 추가비용 0).

## 정직한 주장 축소 (scope)
🟢 이어도 **"감독-주소 레버의 *주소학습* 이 자연어휘에 전이"** 까지만. 값읽기 전이는 [[H_9736]] 소관.

## Controls (≥2)
① nonce arm-S 양성통제(주소축·2-seed robust) ② `--store-addr-weight 0` 음성통제 ③ `--store-shuffle`
balance-floor ④ anagram 포함/제외 채점면([[H_9683]] D0-key census).

## Cost · kill-list · 병렬세션
N/S × 2 seed + OFF 최소 1 = **5 CPT**(pool · GPU 해방 대기 · manifest/pool 재사용). Kill-list 저촉 없음
(seed {7,11,13} 회피 · 1-seed 판독 없음 · RV 레버 불사용). 병렬세션 침범 없음(카드·primary·RV seed 무접촉).
⚠️ "값읽기 전이"라 부르면 scope 위반.

---

## 🔥 FIRED (2026-07-17 04:57Z · summer GPU RTX 5070 · engine-native 진행중)
- 배관 전부 통과: fresh github clone origin/main(VERSION 0.15.76 · HEAD 5fec1be7) → 전용 venv
  pip install(clobber 회피) → storebind 4 코퍼스(arm-N/nat5 · arm-S/nonce × seed{3,17}) → train.
- **5 CPT 순차**(각 6000 step · bf16): arm-S/s3(양성통제 스모크 먼저) · arm-S/s17 · arm-N/s3 · arm-N/s17
  · arm-N/s3-OFF(`--store-addr-weight 0` 벽재현). base py303_full.clm md5 508a71932d · warm-start
  round-trip BYTE-IDENTICAL · 346M params · nat5 sha256 a5e80bbf…6a98.
- 레시피 = H_9672 T3 상속(`--L 4 --d 3784 --e0 3 --emax 3 --store-addr-weight 1.0 --store-batch 32
  --store-win 24 --store-ans-weight 1.0 --clms-d-g 64 --steps 6000 --lr 1e-4`). 평가 = `--store
  HELD_balanced.json --store-addr-audit --store-shuffle`.
- 로그 `/home/summer/h9734/run.log`. 판독 = arm별 addr_top1/addr_mass/addr-gap → 사전등록 bar 기계적 적용.

### 🔧 발사 중 버그 2건 (기록)
- driver `set -u` + `local arm=$1 s=$2 out=...${arm}...` 한 줄 → `${arm}` 이 할당 전 확장돼 unbound
  abort. `local` 분리로 수정(attempt1 죽음 · 학습 전이라 손실 0).
- `pkill -f 'h9734/driver.sh'` 를 ssh 로 보내니 그 문자열 담은 ssh 세션 자신을 죽여 rc=255
  ([[remote-pkill-self-match]] 실증 · pkill 없이 재발사로 회피).

---

## ⛔ VERDICT — INSTRUMENT-DEAD (2026-07-17 · 양성통제 재현실패 · 타겟 결과 아님 · infra-wall-noneval)

**arm-N(자연어휘)은 판독하지 않는다** — 사전등록 계기 게이트가 정확히 이 상황을 막으려 설계됐고, 작동했다.

### 5-arm addr-audit 결과 (HELD-OUT · summer 0.15.76)
| arm | addr_top1 | addr_mass | |
|---|---|---|---|
| armS_s3 (양성통제 nonce) | **0.0000** | 0.0062 | 🔴 게이트(.95/.90) 미달 |
| armS_s17 (양성통제 nonce) | **0.0000** | 0.0023 | 🔴 |
| armN_s3 | 0.0000 | 0.0054 | (미개봉) |
| armN_s17 | 0.0078 | 0.0149 | (미개봉) |
| armN_s3_OFF | 0.0000 | 0.0511 | (OFF>ON 역전) |

사전등록: **arm-S addr_top1 ≥ .95 미달 = INSTRUMENT-DEAD**. 양성통제(nonce)가 H_9672 T3 의
**같은 레시피** held addr_top1 **0.984** 를 재현 못 하고 **0.000**. ⟹ arm-N 은 판독 불가.

### 진범은 타겟이 아니라 도구 (verdict-integrity · reference-match)
결정적 해리 (같은 ckpt armS_s3):
```
SEEN manifest (학습 엔티티):  addr_top1 = 1.0000 · addr_mass = 0.9867  ✅ 완벽·sharp
HELD manifest (held-out):     addr_top1 = 0.0000 · addr_mass = 0.0062  🔴 전무
```
- **eval 경로 무죄**: seen 에서 addr_top1 1.0(train 의 sb_addr_acc 1.0 과 일치) = numpy addr-audit 정상.
- **순수 generalization 실패**: 학습 엔티티는 완벽 주소화, held-out 은 전무 = 암기했으나 전이 못 함.
- **2-seed 재현**(s3·s17 둘 다 held 0.000) + 실패가 **총체적**(0.000, seed-11 의 0.55 붕괴와 다름)
  ⟹ seed-fragility 아님. H_9672 는 주소축이 **2-seed robust**(0.984 on 7·11)라 명시.
- ⟹ **버전 회귀 강한 의심**: H_9672 T3 = **0.15.35** 서 held 0.984(일반화) vs 이 fire = **0.15.76**
  (41 패치 후) held 0.000. 레시피 byte-동일 · eval 무죄 · seed 무관 ⟹ **0.15.35→0.15.76 사이
  addr-loss 훈련 경로가 주소 일반화를 회귀시켰다**(암기는 유지·전이만 상실).

### 판정 · 후속
**H_9734 = INSTRUMENT-DEAD**(계기 결함 · [[infra-wall-noneval]] 로 격리 · 타겟 "자연어휘 전이"에
대해 아무 것도 말하지 않음). 5 CPT 는 clean run 이 아니므로 과학 점수 미부여([[verdict-integrity]]).
- **NEXT = upstream-fix**: `core/`+`cli/` 의 store-addr 훈련 경로 0.15.35↔0.15.76 회귀 bisect →
  주소 일반화 복구 → 그 버전으로 H_9734 재발사(양성통제 arm-S 가 held ≥.95 재현해야 arm-N 개봉).
- reference-match 진행: t3.clm(known-good 0.984)을 0.15.76 eval 로 held 판독(diag_t3ref) → 회귀
  위치 확정(eval 이미 seen=1.0 로 무죄 확인 ⟹ 훈련 회귀 예상).
- 5 ckpt(arm-N/S/OFF) + step ckpt 회수/정리(a_fire_recover_complete · summer 디스크).

**설계 성공 기록**: 사전등록 계기 게이트(arm-S ≥.95)가 없었다면 arm-N held 0.000 을 "자연어휘 전이
실패"로 오독했을 것이다. 게이트가 버전 회귀를 과학 결과로 오독하는 것을 **발사 후 판독 시점에** 막았다.

---

## 🔬 REFERENCE-MATCH CLEARED — 코드 무죄 (2026-07-17 · $0 · verdict-integrity)

Stop-hook(upstream-fix)에 따라 store-addr default 경로를 T3 커밋(13139dee0 · ~0.15.35)과
origin/main(0.15.85) 정밀 대조. **default 경로 byte-identical 확정 = 고칠 코드 결함 없음.**

| 경로 | default diff |
|---|---|
| `store_apply`(eval) | query/fuse/lane_type4 전부 default-off · 주소 `q=h@W_q` 불변("defaults reproduce H_9423 byte-for-byte") |
| `CLMSModule.forward`(train) | yn_fresh=None→`q=W_q(yn_q)` · fangate=False→`val[pols]` · val_center=False 전부 불변 |
| addr-loss | `if sb_addr_w>0: ce_addr=CE(att,tgt)` 완전 동일(T3 도 `--store-addr-weight 1.0`) |
| oracle-aux(RV-1) | `if sb_oracle_aux>0 and not sb_oracle` gated · 내 실행 sb_oracle_aux=0 = byte-identical |

⟹ **버전 회귀 아님**(직전 verdict 의 "0.15.35→0.15.76 회귀 강한 의심"을 이 reference-match 가
기각). eval 무죄(t3 0.15.76→0.9844)에 더해 **훈련 코드도 무죄**. held 0.000 vs T3 0.984 는 코드가
아니라 **비-코드 요인**:
- **seed {3,17}**(T3 는 {7,11}) — 주소 일반화가 seed-의존일 수 있음.
- **torch/GPU numerics** — torch 2.13.0+cu130 · RTX 5070 **sm_120(Blackwell) bf16** 의 미세한
  수치차가 delicate 한 주소-일반화 bootstrap 을 흔들 수 있음.
- (2차) corpus drift — gen_en/sns_en 트렁크 co-train 변경 가능성(미검증).

**남은 결정타 = seed-7 CPT(t3 동일 seed·default)** — held≈.98 이면 seed 확정 / held≈0 이면 numerics.
🔴 GPU 대기(summer free 6078<9000 · 병렬세션 2프로세스 점유·`a_dont_kill_live_compute` 안죽임) —
waiter(setsid·5분폴링→자동재발사) + poller 자율 배치. **코드 upstream-fix 대상 없음**(reference-match
CLEARED) · 이 datum 은 GPU 해방 대기(외부 의존·session-terminal).

---

## 🎯 seed-7 결정타 = NOT SEEDS · 환경/numerics 확정 (2026-07-17 · engine-native)

버전 vs seed 를 seed-7(t3 와 정확히 같은 seed·default·byte-identical 코드)로 판정:
```
seed-7 @ 0.15.35 (t3.clm · 내 0.15.76 eval)  held addr_top1 = 0.9844  ✅ 일반화
seed-7 @ 0.15.76 (내 재실행 · GPU-free waiter) held addr_top1 = 0.0078  🔴 실패
```
**같은 seed·같은 코드·같은 GPU(RTX 5070)인데 갈림** ⟹ **seed 아님**({3,17} fragility 기각 ·
2-seed 재현 0.000 은 seed 가 아니라 환경의 산물). reference-match 로 code 무죄·eval 무죄까지
확정됐으니 유일 남은 변수 = **훈련 환경/numerics**: torch **2.13.0+cu130**(CUDA 13) · Blackwell
**sm_120** · **bf16**. t3 venv 는 /tmp 초기화로 소실 → torch 직접 비교 불가.

### 두 하위원인 (재현성 CPT 로 판정중)
- **(a) torch 버전 차이**: t3 가 더 옛 torch 로 돌아 bf16 훈련 numerics 가 달랐다(재현시 안정).
- **(b) run-to-run CUDA bf16 비결정성**: 주소 일반화가 knife-edge → 비결정 reduction 이 run 마다
  generalize/memorize 를 가른다([[bit-det-drop-fast-train]]: 훈련 bit-det 는 의도적으로 버려짐).
  **(b)라면 H_9672 "seed-7 lucky/seed-11 collapsed" + H_9691 RV-sweep 전체가 seed 가 아니라
  run-노이즈를 재는 것** = 병렬 세션 lane 에 치명적 함의.

**판정중**: seed-7 3번째 run(armS_s7_repro · GPU free 8424 발사) → ≈0.0078 재현이면 (a)env-vs-t3 ·
크게 다르면 (b)비결정성 확정. ⚠️ 병렬 세션(H_9672/9691 store-addr lane · 같은 torch 2.13.0+cu130
summer)이 (b)면 동일 영향 — 교차통지 필요.

### H_9734 재발사 경로 (원인별)
- (a)torch: 알려진-good torch pin → 재발사(양성통제 arm-S 가 held≥.95 재현해야 arm-N 개봉).
- (b)비결정: 단일-run 판독 불가 ⟹ N-run 분포로 재설계(또는 훈련 결정성 강제 · 속도 tradeoff).

---

## ✅ ROOT-CAUSE 확정 — (a) 안정적 환경 회귀 · (b) 비결정성 기각 (2026-07-18)

seed-7 재현성 CPT(3rd run · 같은 seed·코드·env)로 (a)/(b) 판정:
```
seed-7 @ 내 env (torch 2.13.0+cu130)  run#2 held 0.0078 · run#3 held 0.0078  = 완전 동일
seed-7 @ t3 env (older · 0.15.35)      held 0.984
```
RNG seeded(dropout·init·order 동일 · cli/train.py L1567) → 두 run 의 유일 변수 = CUDA bf16 커널
비결정성. 그게 결과를 **안 바꿈**(0.0078=0.0078) ⟹ **(b) run-to-run 비결정성 기각**.
⟹ **(a) 확정: 안정적 환경 회귀** — 내 env 는 seed-7 을 재현성 있게 실패(0.0078), t3 env 는 성공(0.984).

### 최종 원인 사슬 (전부 배제 후 남은 것)
```
NOT seed   (seed-7 재현·{3,17}과 동일)
NOT code   (reference-match byte-identical · #4040)
NOT eval   (t3.clm 0.15.76 eval → 0.9844 · #4040)
NOT 비결정성 (2-run 0.0078 완전 동일)
─────────────────────────────────
= 안정적 환경 회귀: torch 2.13.0+cu130(CUDA 13) · Blackwell sm_120 · bf16 훈련이
  주소를 암기(seen 1.0)하나 held-out 일반화(0.984→0.0078)를 잃는다. t3 의 옛 torch env 는 일반화했다.
```

### ⚠️ 병렬 세션 함의 (교차통지 · a_parallel_session_compare)
H_9672/H_9691 store-addr lane 이 **같은 summer 환경(torch 2.13.0+cu130)**에서 돈다면 동일 회귀에
노출됨. H_9672 T3 의 0.984 는 **옛 torch env** 산물 — 현 env 재현 시 0.0078 예상. "seed-7 lucky/
seed-11 collapsed"(H_9672)와 RV-sweep(H_9691)의 seed-축 해석은 **환경 교락**을 먼저 배제해야 유효.
(단 run-노이즈는 아님 = 각 env 내 단일-run 은 의미 있음.)

### 재발사 경로 (환경 회귀 fix — owner/병렬세션 조율 필요)
🔴 **긴장**: Blackwell sm_120 은 새 torch 필요(#3969 preflight) BUT 새 torch 가 주소 일반화를 깬다.
- torch 버전 bisect(GPU CPT/버전 · 비용) → last-good 고정 vs sm_120 지원 재조정.
- 또는 non-Blackwell GPU(옛 torch 가능)서 재발사.
- 이건 pyproject/환경 변경이라 병렬세션 store-addr lane 과 lockstep 필요 = **coordination point**.

**H_9734 자체 판정 = INSTRUMENT-DEAD 유지**(양성통제가 이 환경서 재현 불가 · arm-N 판독 불가).
설계 성공: 사전등록 계기 게이트가 "자연어휘 실패" 오독을 막고, 파고든 결과 진범이 자연어휘가 아니라
**store-addr lane 전체의 환경 회귀**로 드러남.
