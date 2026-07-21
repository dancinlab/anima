# H_9825 — 얼어붙은 trunk 가 store 를 **주소지정**할 수 있는 천장은 얼마인가?

**status:** 🔧 INSTRUMENT LANDED (계기 착륙 · 판정 PENDING) · DIRECTIONAL 상한
**source:** `lab/v2/hypotheses/V2_7_decode_probe_seed_split.md` (v2 카드 = source, 수치는 이식 안 됨)
**wired:** yes — `anima-py evaluate <clm> --store-retr-probe <dump.npz> [--retr-probe-iters N]`
· 자체검사 `--retr-probe-selftest`

## Question

`--store-addr-census`(H_9719)는 **랜덤** W_q 의 argmax 충돌을 pedestal 과 대조하는 *기하 선별기*라
"기하가 붕괴했나"만 답한다. 답하지 못하는 것은 **"이 trunk 위에서 bolt-on 다리가 도달할 수 있는
검색 정확도의 천장이 얼마인가"** 이다. 이 천장이 없으면 H_9392(bolt-on lane)·H_9720(tap-depth lane)의
음성은 *표상 빈곤*(애초에 못 읽는다)과 *소비/라우팅 실패*(읽히는데 안 쓴다)를 구분하지 못한다.

## Intervention

다리가 실제로 쓰는 선형 질의사상 **W_q(d→d_k) 하나만** 적합한다 — `store_apply` 의
`q = h @ W_q` 와 동일 형태. 점수는 `softmax((h@W)·K[i]/√d_k)` 로 자기 엔티티 키를 고르는 것.
readout·operator gate 는 **격리**(검색 절반만 잰다).

일반화 강제: 엔티티를 **서로소 절반**으로 갈라 train 엔티티(+train 키)에서만 W 를 적합하고,
held-out 엔티티(+held-out 키)에서 읽는다 ⟹ 외운 행이 아니라 *내용주소의 일반화*.
우연 = 1/len(test) 로 **실현 분할에서 유도**(가정 금지 · `chance-level-must-be-derived-per-metric`).

## Arms + controls

| arm | 무엇 | 읽는 법 |
|---|---|---|
| LIVE | 이 ckpt 의 penultimate H | 천장 (DIRECTIONAL) |
| **ORACLE** | H 를 K 의 선형상으로 심음 → 정확한 W 가 **존재** | 양성통제. <0.90 이면 INSTRUMENT-DEAD, 음성 판독 불가 |
| **NULL** | 구조 없는 norm-matched 가우시안 H | 참값 0 PEDESTAL. 우연 초과 = 검색을 **제조**한 것 ⟹ INVALID |

## Gates

- `ORACLE < 0.90` → **INSTRUMENT-DEAD** (`positive-control-before-reading-a-negative`)
- `NULL > max(4×chance, 0.15)` → **INVALID** (`phi-estimator-needs-zero-truth-pedestal`)
- `LIVE <= max(2×chance, 0.15)` → **FLOOR** (주소지정 도달 안 함)
- 그 외 → **REACHABLE** (천장이 열려 있음)

## Result

계기만 착륙. 자체검사 실측(심은 기하 · ckpt 불요):

```
[selftest] n_train=32 n_test=32  chance=0.0312
  ORACLE (planted linear-reachable) acc=1.0000
  NULL   (structureless H)         acc=0.0312   ← 우연과 정확히 일치
  LIVE   (structureless planted)   acc=0.0000
  SELFTEST PASS ✓
```

⟹ **이 가드는 실패할 수 있다**(v2 `gradcheck --selftest` 규율). 이웃 계기
`--store-census-selftest` 회귀 없음. 단일 진입점 `anima-py evaluate` 로 배선 확인(rc=0).

**아직 ckpt 에서 안 쟀다** — 실제 천장 수치는 store-trailer ckpt + `--dump-hidden` npz 로 발사해야 나온다.

## Falsify

- ORACLE 이 1.0 인데 LIVE 가 FLOOR ⟹ 표상 빈곤이 아니라 **주소지정 불가**가 진범.
- LIVE 가 REACHABLE 인데 in-vivo bolt-on 이 여전히 죽으면 ⟹ 벽은 검색이 아니라 **소비/라우팅**.
- NULL 이 우연을 넘으면 이 계기의 모든 수치는 무효 — 적합 자유도가 신호를 만든 것.

## 정직 고지

- DIRECTIONAL **천장**이지 능력 판정이 아니다. 굳히는 것은 303M engine-native 발사뿐.
- v2 의 수치(frozen 0.5134~0.5724 vs cotrained 0.9998~1.0)는 **이식하지 않았다** — v2 는 영구
  DIRECTIONAL 이라 여기 인용은 동기일 뿐 근거가 아니다.
- v2 원본은 예제 스트림에서 뽑은 0-shot 분할을 썼고, 프로덕션 dump 는 엔티티당 hidden 1개라
  **엔티티 분할**로 옮겼다. 같은 질문이지만 같은 수치가 아니다.
- **tap 범위 한계** (H_9720 카드 §40 이 census 에 대해 지적한 것과 같은 한계가 이 probe 에도 있다):
  입력이 `--dump-hidden` 의 **penultimate `__last`** 라서, 주소 질의가 초기층 tap +
  학습된 `W_fresh`/`W_q_fresh` 에서 나오는 **lane_type 5(fresh query lane)의 실제 주소경로는
  판별하지 못한다**. lane_type 1~4(penultimate 질의)에서만 천장이 그 lane 의 천장이다.
  fresh lane 을 재려면 `--dump-hidden` 을 fresh tap 으로 확장해야 한다 — 미착수.

## 🔒 발사 사전등록 (2026-07-21 · dump 존재 전 동결)

**spec:** `config/h9825_retr_probe_entity_pool.json` (128 엔티티 literal — 파일만으로 재현)
**ckpt:** `rv3c13.clm` (CLMS trailer · lane_type=3 · n_slot=8 · d_k=64)
**판정 팔:** `--retr-probe-center train-mean` = **중심화 팔**. raw 는 투명성용 병기.

### 왜 중심화가 판정 팔인가 (비대칭 · 게이트표는 그대로)

`h_j = c + r_j`(c=공유 템플릿, r=엔티티 잔차)로 쓰면 로짓에 `(c@W)·K_i` 항이 붙는데 이는
**행-상수·키-색인 편향**이다. 따라서
- REACHABLE 을 **조작할 수 없다** — 행-상수 편향은 모든 행을 같은 키로 끌 뿐이고, held-out
  argmax 는 행-차등 신호를 요구하며 엔티티 분할이 클래스별 편향 탈출구도 없앤다(테스트 키 서로소).
- FLOOR 는 **조작할 수 있다** — 적합은 수렴에서만 c 를 죽이는데, H_9719 가 이 tap 의 공유성분을
  **base 95% · t3 57% of norm** 으로 실측했다. 잡음 방향 관리에 경사가 소모되면 읽힐 잔차가 묻힌다.
⟹ raw 는 믿을 만한 **양성**이되 믿을 수 없는 **음성**이고, FLOOR 가 살아있는 결과라 판정은
중심화 팔에서 나와야 한다. 중심화 잔여 `mean(r_tr)` 도 행-상수라 REACHABLE 을 만들지 못한다.
train 절반 평균만 쓴다(테스트 통계 미유입) · **세 팔 전부 동일 경로**를 지나 통제가 실제 추정기를 인증.
게이트표(#4241)는 **한 글자도 안 바뀐다** — 같은 4 게이트를 사전등록된 팔에 적용할 뿐이다.

### 엔티티 풀 (N=128 · 64/64 · chance = 1/64 = 0.015625)

`/usr/share/dict/words` `^[a-z]{4,8}$` − rho_fan 불용어 − rho_fan 개념어 − 코퍼스 템플릿 토큰,
그 뒤 **en-general 학습셀에서 20회 이상 출현**한 것만(사전 원본은 고어 쓰레기를 물어와 in-vivo
`charge_store` 분포와 어긋난다) → `default_rng(29825)` 로 128 추출. 실측 86,022 → 9,135 → 128.
코퍼스 held-out 은 **요구하지 않는다**: 기억 통제는 **엔티티 분할**이고(W·train 키가 테스트
엔티티를 못 봄), in-vivo store 엔티티도 코퍼스 단어이며, 무엇보다 이건 **천장** 측정이라
출현 단어가 bolt-on 도달 가능치의 상한이다.

### 사전 선언 — 판독 불가 조건 (게이트 추가 아님)

1. dump 자체 양성통제 코사인 **≥0.999** → UNREADABLE(조건화 붕괴). 높되 <0.999 는 kill 아님 —
   중심화 팔이 바로 그것 때문에 있다.
2. `__last` 에 비유한값 → UNREADABLE (arm64 허위 FPE 경고 자체는 해당 없음).
3. 중심화 경로 자체검사가 **발사 전에** PASS 해야 한다. 실패 시 발사 없음 —
   **raw 로 갈아타는 fallback 은 없다**(행동 보고 팔 고르기 = 쇼핑).
4. npz 가 spec 의 128 id 와 정확히 일치해야 한다. 누락/초과 → 부분 풀 판정 없이 UNREADABLE.
5. raw↔centered 불일치는 그대로 보고하되 판정은 중심화 고정 — 격차는 서술적 증거일 뿐 승급 레버가 아님.

## 🔴 발사 결과 (2026-07-21 · rv3c13.clm) — **INSTRUMENT-DEAD · LIVE 판독 불가**

판독 조건 4/4 충족(poscontrol cos=0.8456<0.999 · 전값 유한 · npz=spec 128 정확일치 · 중심화
자체검사 선통과). 그 위에서:

```
n_entities=128  d=3784  d_k=64  chance=0.0156  shared-template=56.6% of hidden norm
  ORACLE  raw=0.6250  centered=0.5781   ← 바 0.90 미달
  NULL    raw=0.0156  centered=0.0156   ← 우연과 정확히 일치
  LIVE    raw=0.2344  centered=0.2031   ← 우연의 13배이나 판독 불가
  verdict arm = centered(train-mean) → INSTRUMENT-DEAD
```

**양성통제가 제 일을 했다.** ORACLE<0.90 이므로 동결표에 따라 LIVE 는 읽지 않는다.
통제가 없었다면 LIVE 0.2031(우연 13배)을 REACHABLE 로 보고했을 것이고 그것은 틀린 판정이었다.

부수 확증: 공유 템플릿 성분 **56.6%** — H_9719 가 t3 계보에서 실측한 **57%** 와 독립 재현.

### 진단 — 죽인 것은 trunk 도 차원도 풀 크기도 아니라 **키 기하**

| 측정 | 결과 |
|---|---|
| ORACLE, **무작위 등방 키**, d=3784, n=64~1024 | **전부 1.0000** ⟹ 차원·풀 크기 무죄 |
| ORACLE, **실제 키**, iters 1200 → 6000 | 0.7500 → 0.7188 ⟹ 최적화 예산 무죄(더 돌려도 악화) |
| ORACLE, **실제 키**, 풀 n=16/32/64/128 | 0.5000 / 0.5625 / 0.8438 / 0.7500 — **어디서도 ≥0.90 없음** |
| 실제 키 쌍별 코사인 | 평균 **0.3186** · 중앙 0.3180 (무작위 등방 −0.0016) |
| 키 공유성분 | **56.0%** of key norm |

⟹ 이 ckpt 의 엔티티-키 코드북이 **선형 도달이 보장된 기하조차** 0.90 위로 검색되지 않을 만큼
뭉쳐 있다. 규정된 검정력 처방(**바를 옮기지 말고 n 을 넓혀라**)을 적용해도 살아나지 않는다 —
n 확대 실패 자체가 결과다. `_entity_key` 는 바이트 임베딩 평균을 통과시키므로 소문자 영단어들이
공통 성분을 크게 공유한다는 것이 기전.

### 이 결과가 말하는 것 / 말하지 않는 것

- **말한다**: rv3c13 에서 이 천장 계기는 판독 불가다. 그리고 그 원인은 키 코드북의 공선성이다.
- **말하지 않는다**: trunk 가 주소지정 가능한지 여부. LIVE 는 읽지 않았다 — 0.2031 은 판정이 아니다.
- **말하지 않는다**: 계기가 고장났다는 것. 등방 키에서는 전 n 에서 ORACLE 1.0000 으로 살아 있다.
  죽은 것은 **이 ckpt 위에서의 계기**다.
- ⚠️ 내가 LIVE 를 이미 봤다(0.2031/0.2344). 이후 어떤 재발사도 blind 가 아니며, 그 사실을 여기 남긴다.

### 다음 단위 (새 사전등록 필요)

키 공선성이 원인이므로 후속은 **풀을 더 넓히는 것이 아니다**(위에서 실패). 두 갈래:
① 키 기하를 바꾸지 않고 읽는 계기 — 예: 쌍별 2AFC(슬롯 2개 중 택1)로 과제를 in-vivo n_slot 에
맞추고 우연을 0.5 로 재유도. ② 키 공선성이 낮은 ckpt 로 같은 spec 을 발사해 계기 생존을 먼저 확인.
어느 쪽도 동결표를 건드리지 않는다.

## 🔁 R2 — 과제를 실제 lane 규모(n_slot=8)에 맞추자 계기가 살아났고, 위 진단이 **반증**됐다

### ⛔ 내가 위에 쓴 진단 2개를 철회한다

1. **"진범은 키 공선성"** → **반증**. GRAM-exact-W(정확한 역사상 W 에서 ORACLE 점수행렬은 키 그램
   `K·Kᵀ` 이므로 코드북만으로 계산되는 상한) = **0.9408** ≥ 0.90. 실제 lane 규모에서 코드북은 충분하다.
2. **"규정된 검정력 처방(n 확대)조차 실패"** → **교란된 결론**. 풀 스윕 16/32/64/128 은
   n_train·n_test·chance 를 **동시에** 움직였다. 비단조 급락(0.8438→0.7500)이 나온 N=128 은
   정확히 **n_train = 64 = d_k** — 보간 임계다. 공유성분 56% 로 `K_tr` 이 병조건이라 역행렬이 저분산
   방향을 증폭한다. 즉 n 확대는 **시험된 적이 없다**.

진짜 원인은 **과제 불일치 + 추정**이었다: probe 는 64-way 를 판별했지만 `store_apply` 는 **8-way**만 한다.

### 설계 (동결표 불변 · 상수 한 글자도 안 건드림)

64-way 적합은 그대로 두고 **같은 W 로 8-way 를 닫힌 형태로 재판독**한다 —
`acc_m = mean_i C(n_te−r_i, m−1)/C(n_te−1, m−1)`. 표본변동 0·seed 없음·roster 없음이고,
발사된 W 가 **바이트 동일**하게 보존되므로 새 추정이 아니라 **재판독**이다.
우연은 유도된다: 균등 rank 에서 이 식은 **정확히 0.125**(수치 확인). 동결표는 chance-상대라
그대로 적용된다(ORACLE 0.90 · INVALID 0.50 · FLOOR 0.25).
추가 통제 **KEY-PERMUTE**(H 고정, 키만 셔플 — 노름·기하는 보존하고 주소 대응만 절단) = **보고용, 게이트 아님**.

### Stage 1 실측 (기존 dump 재판독 · 새 순전파 0)

```
8-way chance=0.1250
  ORACLE 0.9159   GRAM-exact-W 0.9408   NULL 0.1087   KEY-PERMUTE 0.1211   LIVE 0.6496
  (64-way 대조: ORACLE 0.5781 · NULL 0.0156 · KEY-PERMUTE 0.0156 · LIVE 0.2031)
```

계기 **ALIVE**. KEY-PERMUTE 가 우연으로 붕괴(0.1211≈0.125)하므로 LIVE 를 나르는 것은 기하가 아니라
**주소 대응**이다. GRAM 0.9408 > ORACLE 0.9159 ⟹ 남은 격차는 코드북이 아니라 **추정**.

### ⚠️ Stage 1 의 LIVE 는 **눈 가린 검사가 아니다**

같은 ckpt·같은 엔티티·같은 hidden 행의 64-way LIVE(0.2031)를 이미 봤고, 8-way 는 그것에 대해
단조이며, FLOOR 0.25 가 가깝다는 것도 알고 있었다. **재현 가능한 사후 재분석이지 독립 확증이 아니며,
카드에 적는다고 복구되지 않는다.** 그래서 Stage 1 은 계기 생존 판정용이고 LIVE 는 **비-cementing** 이다.

### 🔒 Stage 2 사전등록 (확증 · Stage 1 판독 전에 동결)

`config/h9825_retr_probe_entity_pool_stage2.json` — 같은 구성규칙, `default_rng(29826)`,
**기존 128 과 교집합 0** 인 새 128 엔티티. 같은 템플릿·같은 판정팔·같은 8-way·같은 동결표.
이 풀의 LIVE 만이 FLOOR/REACHABLE 판정 자격이 있다.

### 🟢 Stage 2 실측 (확증 · 겹침 0 인 새 풀 · 새 순전파 128)

```
poscontrol cos(advanced,alas)=0.7550 (distinct ✓) · shared-template 56.1%
8-way chance=0.1250
  ORACLE 0.9402   GRAM-exact-W 0.9598   NULL 0.1603   KEY-PERMUTE 0.1226   LIVE 0.6774
  → REACHABLE
  (64-way 대조: ORACLE 0.6562 · NULL 0.0000 · KEY-PERMUTE 0.0156 · LIVE 0.2656)
```

| 팔 | Stage 1 (재판독) | Stage 2 (확증) | 읽는 법 |
|---|---|---|---|
| ORACLE | 0.9159 | **0.9402** | ≥0.90 두 풀 모두 → 계기 ALIVE |
| GRAM-exact-W | 0.9408 | 0.9598 | 코드북은 lane 규모에서 충분 |
| NULL | 0.1087 | 0.1603 | 게이트(0.50) 한참 아래 |
| KEY-PERMUTE | 0.1211 | **0.1226** | 우연(0.125)으로 붕괴 = 주소 대응이 신호원 |
| **LIVE** | 0.6496 | **0.6774** | FLOOR 0.25 대비 REACHABLE · 우연의 5.4배 |

**판정: REACHABLE (DIRECTIONAL).** 실제 lane 이 마주하는 규모(n_slot=8)에서 이 얼어붙은 trunk 의
penultimate 은 **주소지정 가능하다**. 서로소 두 풀에서 0.6496 / 0.6774 로 재현됐고,
KEY-PERMUTE 가 우연으로 붕괴하므로 신호는 기하 잔재가 아니라 **내용-주소 대응**이다.

### 이 판정이 말하지 않는 것

- lane 이 실제로 이 성능을 낸다는 뜻이 **아니다** — 이건 bolt-on 이 도달 가능한 **천장**이다.
- in-vivo 슬롯은 동시출현 블록 엔티티라 균등 추출 8-way 보다 **더 헷갈릴 수** 있다 ⟹ 천장은 상한.
- `__last` penultimate 읽기라 **lane_type 5(fresh-query)** 는 여전히 판별 불가(rv3c13 은 3 이라 범위 내).
- 굳히지 않는다 — cement 는 engine-native 303M 발사뿐.
- Stage 1 의 LIVE 는 비-blind 였고, 그래서 판정은 **Stage 2** 에서만 나온다.

## 발사 재개지점 (초기 기록 · 위 결과로 갱신됨)

재료는 있다 — `~/anima-weights/rv3c13.clm` 이 CLMS trailer 보유(lane_type=3 · n_slot=8 · d_k=64).
막힌 곳은 **엔티티 풀 spec 부재**: `--dump-hidden` 은 `{id}__last` 로 저장하므로 id = store 엔티티명인
프롬프트 spec 이 필요한데 repo 에 커밋된 것이 없다(H_9720 은 held-out 128 엔티티를 pod 에서 생성).
판정표는 이미 동결(#4241)됐으므로 남은 자유도는 엔티티 풀뿐 —
**데이터를 보기 전에 spec 을 먼저 동결**해야 shopping 이 아니다. 그 pre-registration 이 다음 단위.
