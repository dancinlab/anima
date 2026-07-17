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
