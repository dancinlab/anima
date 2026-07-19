---
id: H_9683
title: NAT-ADDR — does the addr-loss lever transfer from synthetic nonce to NATURAL declarations?
tier: PROPOSED (R7 · 두 lane 접합 · H_9672 T3 가 스스로 남긴 칸 · DIRECTIONAL design)
frontier: g1-interface-addressable-wall
created: 2026-07-17
---

# H_9683 (R7) — 자연선언 주소전이

**Origin.** 병렬 세션 [[H_9672]] T3(#3895 · 🟢 303M CRACK-DIRECTIONAL)를
`a_parallel_session_compare` 로 대조하다 나온 접합점. **그 카드가 명시적으로 남긴 칸**:

> "**G1 자연선언 전이는 별도 H**" · scope = **감독-주소 co-train tier(창발-주소 아님)"

**Claim (one line).** `--store-addr-weight`(L_addr = CE(att, target_slot))가 **합성 CVCVC
nonce** 에서 303M 주소벽을 뚫었다(P1-balanced **0.9688** · addr-gap 0.008). 같은 레버가
**자연 teacher 선언**에도 전이되는가 — 아니면 성공이 합성 원자의 **깨끗한 키 분리**에 기생하는가?

## 왜 이게 두 lane 의 접합인가
| lane | 상태 |
|---|---|
| **A · 주소 (H_9672)** | 🟢 합성 nonce·감독-주소서 **벽 돌파 증명**(engine-native 303M) |
| **B · 자연/외생 내용 (R-series)** | 🧱 "주입·공학습은 되는데 **자연 내용은 안 된다**"(H_9267 XBIND 1.000 vs H_9304 자연 TOST 0) |

H_9672 는 **A 를 풀었고 B 를 명시적으로 열어뒀다**. 이 H 가 그 다리.
D0-1 census 가 이미 예고: `_entity_key`(byte-bag) 는 **위치맹** ⟹ anagram 충돌
`[demar, merad]` 키 L2=0.0000. **자연 어휘는 합성 nonce 보다 키 충돌이 훨씬 심하다**
(형태론·굴절·부분어 공유) ⟹ **전이 실패의 사전 예측 기전이 이미 장부에 있다.**

## Minimal decisive experiment (레버 = 이미 배선됨 · origin/main)
자연 선언 원자로 storebind 코퍼스를 만들고 **동일 T3 레시피**를 돌린다:
```bash
anima-py corpus storebind --lang en --atoms natural_decl_atoms.json \
  --balanced-manifest --seen-manifest --out nat_addr_s${S}.txt
anima-py train --init py303_full.clm --corpus nat_addr_s${S}.txt \
  --store-addr-weight 1.0 --store-addr-audit --canon --seed ${S}
anima-py evaluate NAT_s${S}.clm --store nat_balanced.json --store-addr-audit --store-flip --store-shuffle
```
H_9672 의 **사전등록 판정표를 그대로 상속**(재발명 금지): C0-e ORACLE ≥.90(미달=INSTRUMENT-DEAD·P1 미판독) ·
**P1-balanced ≥.75 = CRACK** · [.60,.75) PARTIAL · (.40,.60) KILL-잔존 · addr-gap ≤.20 ·
4-cell 각 ≥.65 · flip-coh ≥.90 · shuffle at balance-floor.

## Frozen falsifier (사전등록 · 제3결과 포함)
- **P1-balanced ≥ .75** ⟹ 레버가 자연선언으로 **전이** = A·B 한 뿌리 + escape 획득.
- **(.40,.60)** ∧ 합성 arm 이 **같은 fire 에서 .95+ 재현**(양성통제 · 필수 동반 팔) ⟹
  **전이 실패가 자연 어휘에 국한** = "합성 원자의 키 분리에 기생" 확정.
- **addr_top1(held) 은 높은데 P1 낮음** ⟹ 주소는 섰으나 **값읽기가 자연 다의성에 익사** = 제3결과.
- **키 충돌 사전-census 가 bar 를 무효화**: D0-1 방식으로 자연 원자 self-nearest 를 먼저 재고,
  충돌 원자를 **유효 n 에서 제외**한 뒤 채점([[H_9672]] D0-1 선례 — 안 하면 BY-CONSTRUCTION 주소불능이 레버 탓으로 오독).

## Controls (≥2)
① **합성 nonce arm 동시 재현**(양성통제 · [[positive-control-before-reading-a-negative]] — 없으면 자연-null 은 INSTRUMENT-DEAD)
② `--store-addr-weight 0` OFF arm(byte-identical 확인 · 벽 재현)
③ shuffle/balance-floor ④ anagram-충돌 제외 vs 미제외 두 채점면.

## ⚠️ 선행조건 — [[H_9678]] PRECONDITION-FAIL 이 여기에도 걸린다
현 study transcript 는 **entity–value 원자가 0개**(`Perhaps…` 23/30 · 숫자 0 · TTR 0.302)
⟹ **자연 선언 원자를 실제 teacher 에게서 얻으려면 사실-선언형 study run 이 선행**.
다만 이 H 는 **teacher 없이도** 실행 가능 — 자연 EN 어휘 선언 원자를 코퍼스로 직접 합성하면
"자연 어휘 × 감독주소" 를 teacher 비용 0 으로 격리한다(**권장 1단**: 자연어휘 전이가 죽으면
사실-선언형 study run 을 태울 이유 자체가 사라진다).

## Cost · kill-list
1단(자연어휘 원자 · teacher 없음) = **pool~GPU(오너 go)** · 레버·판정표·계기 전부 **기존**
(신규 코드 0). Kill-list: **저촉 없음** — H_9672 재발명이 아니라 **그 카드가 스스로 별도 H 로
남긴 전이 질문**이고, "자연 코퍼스 XOR rescue"(H_9304/9316 CLASS-CLOSED)도 아니다
(가법단서를 자연 문장에서 **찾는** 게 아니라, 주소를 **감독으로 선불**하고 자연 **어휘**만 남긴다).
⚠️ 자기표시: P1 이 shortcut 대역(0.637 근처)이면 [[H_9672]] 의 3중 봉쇄(balanced 1차채점 +
random shuffle-Δ + addr audit)를 그대로 적용 — 그거 없이 읽으면 다수-극성 shortcut 오독.

---

## 🟢 D0-key census 착륙 (2026-07-17 · $0 · 학습/포워드 0 · 엔진 공식 byte-identical · DIRECTIONAL)

사전등록 의무단계("키 충돌 census 먼저") 실행 — `RandomState(9423).standard_normal((256,64))·1/√64`
(train.py CLMSModule 식 그대로) + `core/clms._entity_key`(엔진 함수) + `_sb_entity_pool`/`_sb_split`
(엔진 pool/split · 재발명 0). ckpt 불요(key_emb 은 seed-결정 frozen).

| pool | n_ev | anagram 충돌원자 | ORACLE-slot acc | NN최소거리 |
|---|---|---|---|---|
| nonce (합성 CVCVC) | 128 | 2 | **0.9875** | 0.0000 |
| **nat_5자** (EN 5자 최빈) | 128 | 4 | **0.9880** | 0.0000 |
| nat_자유 (EN 4–8자) | 128 | 0 | 0.9543 | 0.1657 |

`ORACLE-slot acc` = q 가 정답키 그 자체일 때조차 8-slot argmax(q·Kᵀ)가 정답슬롯을 고르는 비율
= **학습으로 도달 불가능한 BY-CONSTRUCTION 상한**(1.0 미만 = 주소가 원리적으로 불능인 몫).
EN 코퍼스 = `anima-corpus-en-general`(59.8MB · 모델이 실제 학습한 것) 최빈 어휘.

### 🔴 사전예측 기전 REFUTED — 이게 실험을 더 깨끗하게 만든다
카드가 사전등록한 실패 예측 **"자연어휘는 형태론·굴절·부분어 공유로 키충돌이 훨씬 심함"**
(D0-1 anagram `[demar,merad]` 근거) 이 **census 로 반증**: `_entity_key` = 바이트행 평균이라
**길이만 통제하면 자연 5자 어휘의 키 기하가 nonce 와 동일**(ORACLE 0.988 = 0.988 · 충돌 2 vs 4
동급). 자유길이는 오히려 anagram 충돌 0(길이차가 byte-bag 충돌을 원천 차단). **세 pool 모두
C0-e bar(≥.90) 통과** = 어느 것도 INSTRUMENT-DEAD 아님.

⟹ **가장 값싼 kill 후보(키 기하)가 배제됐다.** 자연어휘 전이가 만약 P1 에서 죽는다면 원인은
**키가 아니라 값읽기가 자연 다의성에 익사 / penultimate 가 EN 유창성에 점유**(H_9672 T2 가 303M 서
실측한 그 기전) — 즉 이 H 의 **제3결과 사전등록**(addr_top1 높고 P1 낮음)이 유일 생존 실패경로.

### 실험 정밀화 — 권장 arm = **nat_5자** (nonce 와 키기하·길이 매칭)
유일 변수 = "모델이 이 토큰을 EN 단어로 사전학습했나". 이게 H_9672 가 남긴 "자연선언 전이"의
최소 격리 = **오염 없는 1-DOF 대조**. fire 설계(오너 go · pool summer · H_9672 T3 레시피 상속):
```bash
# arm-N  자연 5자 어휘 · arm-S  합성 nonce (양성통제 · 동시재현 필수)
anima-py corpus storebind --lang en <nat5|nonce pool 주입> --out {N,S}_s${S}.txt
anima-py train --init py303_full.clm --corpus {N,S}_s${S}.txt \
  --store-addr-weight 1.0 --store-addr-audit --canon --seed ${S}
anima-py evaluate {N,S}_s${S}.clm --store balanced.json --store-addr-audit --store-flip --store-shuffle  # H_9672 판정표 상속
```
frozen bar(상속): arm-N P1-balanced ≥.75 = 전이(A·B 한 뿌리) · arm-S 가 **같은 fire 에서 ≥.95
재현**(양성통제)해야 arm-N null 이 판독가능(안 그러면 INSTRUMENT-DEAD).
⚠️ 남은 구현 gap: `storebind` 는 현재 nonce pool 하드코딩(`_sb_entity_pool`) — 외부 어휘 pool 주입
플래그(`--entity-pool <file>`)가 신규로 필요(레버 아닌 **코퍼스 빌더 확장** · a_experiment_engine_native).

---

## 🔴 PREMISE-COLLAPSE + 카드 자체 결함 3건 (2026-07-17 · $0 fire-readiness 사전점검 · 발사 전 발견)

**이 카드는 지금 어느 seed 로도 판독 불가능한 fire 를 설계하고 있다. 발사 금지.**

### ① 전제 붕괴 — arm-S(양성통제)가 존재하지 않는다
이 카드는 [[H_9672]] T3 의 **P1 0.9688 = 주소벽 돌파**를 lane-A 🟢 기정사실로 깔고 설계됐다.
집필 시점 그 카드는 "seed-11 재현이 **TERMINAL 잔여**"라고만 적었고 **나는 그것을 사소한 잔여로 읽었다**.
seed-11 이 돌아왔고 **죽었다** — origin/main H_9672 자기정정:

> **값읽기 seed-취약** — seed-7 ORACLE 0.99 vs **seed-11 0.50(chance)** · P1-balanced 0.5547 ·
> flip-coherence 0.056 ⟹ **전체 lookup NOT seed-robust · seed-7 P1 0.9688 = 값읽기 運 · TERMINAL 부정**

이 카드의 frozen falsifier 는 arm-N 의 null 을 읽으려면 **"arm-S 가 같은 fire 에서 ≥.95 재현"**
(양성통제)을 요구한다. 그런데 arm-S = T3 레시피 그대로이고, 그게 **seed-11 에서 0.5547 로 죽는 게
이미 실측**됐다:
- **seed-11** → arm-S bar 미달 → arm-N 정의상 **INSTRUMENT-DEAD** → GPU 전액 낭비.
- **seed-7** → arm-S 통과가 **동전던지기**이며 seed-7 은 **이미 소각된 seed**([[burned-gate-no-refreeze-sequential-gating]] · tune-to-green 표면).

⟹ **순서가 뒤집혀 있다.** "arm-S 가 seed-robust 하다"는 이 카드의 암묵 가정이 곧 병렬 세션이
RV-1/2/3 sweep 으로 **지금 고치는 중인 미해결 벽**이다. H_9672 값읽기 robustness winner 확정 =
**이 H 의 선행조건**([[positive-control-before-reading-a-negative]]).

### ② "신규 코드 0" — 틀렸다
카드는 "레버·판정표·계기 전부 기존(**신규 코드 0**)"이라 적었으나 `--entity-pool` 은
**origin/main 어디에도 없었다**(`_sb_entity_pool(n_total)` = CVCVC 하드코딩 · `build_storebind` 에
어휘 pool 파라미터 없음 · 미지 플래그 fail-closed). arm-N 은 코드 없이 만들 수 없었다.
✅ **해소**: `--entity-pool <file>` 배선 착륙(#3945 · byte-identical 14/14 · VERSION 0.15.57).

### ③ 카드의 예시 커맨드가 전부 틀렸다 (그대로 쓰면 죽는다)
T3 실제 dispatch(`/tmp/h9672_t3/trainT3.log` · 추측 0)와 대조:

| 카드 기재 | 실제 |
|---|---|
| `--canon` | T3 는 **안 씀** |
| `--atoms natural_decl_atoms.json` | storebind 에 `--atoms` **플래그 없음**(별개 fmt) |
| `--balanced-manifest --seen-manifest` | **그런 플래그 없음** — storebind 는 4개 매니페스트를 **무조건** 쏟음 |
| train `--store-addr-audit` | **train 플래그 아님 · evaluate 플래그** |
| T3 VERSION 0.15.35 (단일 기재) | seed-7 = **0.15.29** · seed-11 = 0.15.35 (스큐 실재 · 단 audit-only diff 라 무해 판명) |

### 🕳️ 자연 pool 제작 제약 (#3945 가 측정해서 알려준 것)
C0-a zero-leak witness 는 **substring** 기반(`e in corpus_blob`) ⟹ held-out 원자가 train 원자에
**중첩**되면(`art` ⊂ `start` · `corpus-py-1` ⑩) **빌드가 abort**(fail-CLOSED = 안전방향).
⟹ 자연 pool 은 **상호 비중첩**이어야 한다. **권장 arm `nat_5자`는 전부 길이-5라 중첩이 원리적으로
불가능** — D0-key census 가 고른 arm 이 이 제약도 자동 충족한다(우연한 정합).

### 상태 갱신
**PROPOSED 유지 · fire 게이트 = H_9672 RV-sweep winner 확정**(arm-S 가 2-seed robust 해질 때까지
이 H 는 판독 가능한 양성통제가 없다). 그 전에 쏘면 **"자연어휘가 죽었다"와 "레시피가 원래
seed-취약이다"를 구분할 수 없다**. $0 자산(D0-key census · `--entity-pool` 배선)은 그대로 유효하고
winner 확정 즉시 발사 가능한 상태로 보존.

---

## ✅ FIRE-READY (내 쪽 잔여 0 · 2026-07-17 · $0 · engine-native 검증)

`--entity-pool`(#3945) 배선 후 **발사본 pool 을 만들고 엔진이 실제로 먹는지까지 검증**했다.
남은 블로커는 전제(H_9672 RV-sweep) 하나뿐 — **구현·계기·pool 은 전부 준비 완료**.

### 발사본 pool — 결정적 레시피 (재현가능 · summer 에서 동일 산출)
```
source : anima-corpus-en-general (HF · 모델이 실제 학습한 그 코퍼스 · 59,758,676 B)
recipe : re.findall(r"\b[a-z]{5}\b", txt.lower()) → Counter → most_common(512)
sha256 : a5e80bbf68ac10dd26f3e41cf9f4abf2f4e18f6ea218e361fce49806bdbb6a98
sample : their about there which would other first these after years could where
```
계약: ascii ✅ · 소문자 ✅ · 길이-5 균일 ✅ · 512개 ✅ · 중복 0 ✅ · **상호중첩 0**(길이동일 ⟹ 원리적 불가
= #3945 가 경고한 substring-witness abort 를 구조적으로 회피).

### 🟢 엔진이 자연어휘를 먹는다 (실측 · anima-py 0.15.60 · T3 파라미터)
```
anima-py corpus storebind --lang en --n-blocks 4000 --store-slots 8 --seed 7 \
  --entity-pool nat5.txt --out sb.txt
→ entity pool = EXTERNAL nat5.txt (512 atoms · ascii · no dups)
                — the builtin CVCVC nonce enumeration is NOT used
→ C0-a 0-shot ✅ held-out entities appear 0x in corpus (store-key + substring both asserted)
→ is issue => good / not texas => bad     (arm-S nonce = is fozod => good)
```
**C0-a zero-leak witness 가 자연어휘로도 통과** — 자연 pool 의 최대 실패모드가 배제됐다.

### 🎯 1-DOF 격리 실측 확인 — 두 arm 이 어휘 말고 전부 동일
| 산출물 | arm-N (nat5) | arm-S (nonce) | |
|---|---|---|---|
| `sb.txt` | 544,134 | 544,134 | ✅ |
| `.store.jsonl` | 7,040,134 | 7,040,134 | ✅ |
| `.held.json` | 28,405 | 28,405 | ✅ |
| `.held_balanced.json` | 28,416 | 28,416 | ✅ |
| `.seen.json` | 28,417 | 28,417 | ✅ |
| `.meta.json` | `entity_pool` 키 제외 시 **구조 동일** | | ✅ |

**바이트 크기까지 전부 동일** ⟹ 두 arm 은 **어휘 1-DOF 만** 다르다. 차이가 나면 원인은 어휘뿐
(오염 없는 대조 = 이 H 가 노린 최소 격리가 실제로 성립).

### 발사본 키 census (엔진 공식 · 발사할 그 파일 그대로)
| pool | anagram 충돌 | ORACLE-slot acc | C0-e bar(≥.90) |
|---|---|---|---|
| **nat5 (발사본)** | 4 | **0.9880** | ✅ |
| nonce (arm-S) | 2 | 0.9875 | ✅ |

키 기하 **동등** ⟹ arm-N 이 죽어도 **키 탓이 아니다**(D0-key census 결론 재확인 · 발사본으로).

### 남은 단 하나 — 전제
🔴 **H_9672 RV-sweep winner 확정**(arm-S 가 2-seed robust 해질 때까지 판독 가능한 양성통제 없음).
그것 외에 이 H 의 발사 준비는 **완료**: 구현 ✅(#3945) · pool ✅(sha256 고정) · 계기 ✅(T3 dispatch
정확 복원) · 1-DOF 대칭 ✅(실측) · 키 census ✅. winner 확정 시 `--entity-pool nat5.txt` 한 줄 차이로
arm-N/arm-S 를 동시 발사한다.

---

## 🔧 계기 경로 정정 (2026-07-17 · lab full Sol 지적 · repo 확증)
위 예시의 `evaluate --xbind` 는 **틀렸다** — `--xbind`(evaluate.py:3587)는 G1 D-acc 매니페스트 경로이고,
CLMS store-bridge 판독은 **`--store HELD.json --store-addr-audit`**(evaluate.py:4084·4215 "H_9672: report
addr_top1 + addr_mass") + `--store-oracle`/`--store-flip`/`--store-shuffle` 계열이다. 위 두 커맨드를 정정했다.
(같은 "플래그 실재를 grep 으로 확인하고 적어라" 교훈 재발 · [[instrument-claim-alignment-before-reading-a-bar]].)

## 🔀 R8 estimand-split 후속 (lab full Fable+Sol 독립 수렴 · 2026-07-17)
이 카드의 fire 게이트(arm-S 값읽기 seed-fragility)를 두 모델이 **estimand 분리**로 우회:
- [[H_9734]] NAT-ADDR-SPLIT ⭐ — 주소축(H_9672 서 2-seed robust)만 판독 = **RV winner 없이 지금 가능**.
- [[H_9736]] LOCKED-WINNER RIDER — 무조건부 값읽기 = RV winner 후 fresh seed rider($0 대기).
- [[H_9735]] ORACLE-gated PAIRED — 조건부 값읽기 = RV 전멸 시에만(CONTINGENT).
이 카드(H_9683)는 R8 로 **분해**되어 잔여 = 주소축은 H_9734 로 이관·값읽기축만 winner 대기.
