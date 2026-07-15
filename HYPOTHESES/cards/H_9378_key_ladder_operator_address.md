# H_9378 — KEY-LADDER (V2): 연산자 키의 등가류를 지도화한다 (표면 사다리 · 두 lane · 신규 학습 0)

- **status**: VERDICT (⛔ INVALID — G-pedestal 낙제 · 사전등록 판독 동결본 그대로)
- **date**: 2026-07-15
- **surfaces**: `HYPOTHESES/cards/H_9378_key_ladder_operator_address.md` · `HYPOTHESES/HYPOTHESES.jsonl`
- **instrument**: `anima-py evaluate <clm> --xbind <m.json> --surface-set keyladder_v1`
  (engine-native · `cli/corpus.py::SURFACE_LADDERS` + `expand_surface_ladder` · `cli/evaluate.py::xbind_run` · VERSION 0.13.66)
- **frontier**: `g1-interface-addressable-wall` · lane V2
- **cost**: $0 (기존 ckpt · 신규 학습 0 · pool CPU eval)

---

## 1. 왜 — 세 점으로는 선을 그을 수 없다

C4(H_9334)는 연산자를 **정확히 세 표면**에서 채점했고, 그 안에서 딱딱한 경계를 발견했다:

| 표면 | C4-written lane | 판정 |
|---|---|---|
| `X지 않다` (negL) | **12/12 NEW** (양 seed · p=.0002) | 새 값을 읽는다 |
| `별로 X지 않다` (negZ) | **12/12 NEW** | 새 값을 읽는다 |
| `X지는 않다` (negJ) | 우연 | 연산자가 안 돈다 |

**이 경계가 곧 주소 구조다.** 그런데 우리는 그 경계 위의 점을 셋밖에 갖고 있지 않다.
Fable 의 two-lane 재프레임("선언 lane 과 연산자 lane 이 별도 저장소를 갖고 다리가 없다")이 맞다면,
**주소 = (어간 정체성) × (표면-템플릿 클래스)** 이고 클래스는 **이산**이며 클래스끼리 값을 공유하지 않는다.
그렇다면 사다리를 올리면 **클래스 경계가 보여야 한다**. 안 보이면 two-lane 모형이 틀렸다.

병렬 팔 H_9346(EN)은 자유 부정어 `not` 이 실패했다(DV 0.03~0.07 · ECHO 91~98%)고 보고했지만,
**형태론 × base × 담체를 한꺼번에 움직여** SCREENER 상한에 묶였다. 한국어에는 그 교란 없이 같은 대비를
만들 수 있는 재료가 있다 — **`안 X`(단형 부정 = 전치 FREE 부정어)** 는 `X지 않다`(BOUND 접미)와
**같은 언어 · 같은 base · 같은 코퍼스 · 같은 담체(`이 영화 ___ => `)** 안에 있다.

## 2. 계기 — 무엇을 바꾸는가 (딱 하나)

`--surface-set` 은 **채점 표면만** 바꾼다. arm 추첨도, 심어진 극성도, 코퍼스도, 가중치도 그대로다
(arm 과 planted 극성은 **매니페스트에서 되읽는다** — 원자 파일에서 재유도하면 채점 대상 ckpt 와
arm 추첨이 어긋날 수 있다). 신규 학습 0.

**두 lane 을 같은 사다리로 채점한다** (이게 실험의 전부 — 어느 한 쪽만으론 아무 말도 못 한다):

- **BASE lane** = `natem_c34_main_s{7,11}.clm` — 사전학습 lane. swap 어간의 참 극성은 아직 **원본**이므로
  "원본 극성을 올바로 부정한다" = **그 표면에서 연산자가 돈다**.
- **C4 lane** = `swap_c4_s{7,11}.clm` — CPT 로 쓴 lane. "심은(planted) 극성의 부정을 답한다" = **쓴 값이 그 표면을 통해 도달된다**.

| base | C4 | 읽기 |
|---|---|---|
| 돈다 · NEW | 두 lane 의 키-클래스 **안** | negL/negZ = 앵커 |
| **돈다 · OLD** | **연산자는 발화하나 사전학습 값을 읽는다 ⟹ CPT 쓰기가 이 표면 클래스에 도달 못 함 = 두 저장소가 템플릿 클래스로 갈린다** | ★ two-lane 의 결정적 증거 |
| 죽었다 | 애초에 연산자 표면이 아님 — 쓰기에 대해 아무 말도 못 함 (pedestal 급) | 정보 없음 |

## 3. 사다리 (사전등록 · 표면 열거 · 노출 인구조사 동결)

노출 = **사전학습 코퍼스의 화살표 라인 전체를 정확-라인 일치**로 센 값(부분문자열 오염 배제 · 12 swap 어간 합).
**수치를 보기 전에 셌다** (⑨ "일반화 주장은 그 축 노출 0 에서만 잰다").

| tag | 표면 | 클래스 | 역할 | PRETRAIN 노출 s7 / s11 | C4-CPT 노출 |
|---|---|---|---|---|---|
| negL | `X지 않다` | BOUND | anchor_new (C4 12/12 기지) | **84 / 108** | 0 |
| negZ | `별로 X지 않다` | BOUND | anchor_new (C4 12/12 기지) | **0 / 0** | 0 |
| negJ | `X지는 않다` | BOUND | anchor_null (우연 기지) | 0 / 0 | 0 |
| negPST | `X지 않았다` | BOUND | ladder (과거) | 0 / 0 | 0 |
| negPRS | `X지 않는다` | BOUND | ladder (현재-서술) | 0 / 0 | 0 |
| negCAS | `X지 않아` | BOUND | ladder (반말) | 0 / 0 | 0 |
| negTGT | `X지않다` | BOUND | ladder (띄어쓰기 제거) | 0 / 0 | 0 |
| negPOL | `X지 않습니다` | BOUND | ladder (경어) | 0 / 0 | 0 |
| **negAN** | **`안 X다`** | **FREE** | ★ EN `not` 의 KO 대응물 | **46 / 38** | 0 |
| **negANG** | **`안 X고`** | **FREE** | ★ FREE · 사전학습 축자형 | **45 / 31** | 0 |
| negMOT | `못 X다` | FREE | ladder (불능 · 형용사엔 비문 가능 — 제2 pedestal 로 읽힐 수 있음) | 0 / 0 | 0 |
| ped1 | `X지 뫄다` | BOUND | **PEDESTAL** (참값=우연) | 0 / 0 | 0 |
| ped2 | `뫄 X다` | FREE | **PEDESTAL** (참값=우연 · FREE 슬롯 정합 통제) | 0 / 0 | 0 |
| w0 | `X고` | DECL | **WRITE 게이트** | 17 / 33 | **480** |

**노출 구배가 예측과 반대 방향이라는 점이 이 설계의 핵심이다:**
negZ 는 **노출 0** 인데 C4 lane 에서 **12/12 NEW** 를 이미 냈다(BOUND 클래스는 미학습 표면으로 일반화한다).
negAN 은 **노출 46 줄**이다. 따라서 **negAN 이 실패하고 negZ 가 성공하면 노출로는 설명이 안 된다** —
남는 설명은 **BOUND/FREE 클래스 = 주소의 일부**뿐이다. (negL vs negAN 은 사전학습 노출이 같은 자릿수인
**정합 최소쌍**이기도 하다.)

## 4. DV · bar · 통제 (수치 보기 전 동결)

- **DV** = 2AFC 마진 부호 (`NLL(counterfactual) − NLL(gold)`), **H_9334 와 동일 판독**. 자유생성 d_acc 는 **DV 아님**(보고만).
- swap arm **n=12** / 표면 / seed / lane. 부호순열 정확분포: 12/12 → p=.0002 · 11/12 → .0032 · **10/12 → .0193 (=.05 선)** · 9/12 → .073.
- 표면당 산출: `k_NEW` (= 심은 극성의 부정을 답한 수), `k_OLD = 12 − k_NEW`, 일관성 `C = max(k_NEW, k_OLD)`.
  - **BASE lane**: `k_OLD` = **원본 극성을 올바로 부정한 수** = 그 표면에서 연산자가 도는가.
  - **C4 lane**: `k_NEW` = 쓴 값이 그 표면으로 도달하는가.

### 게이트 (실패 = INVALID · 벽 아님)
- **G-write** — C4 lane · w0 · swap: **≥11/12** (H_9334 의 G-write 그대로). 낙제 ⟹ INVALID(사실 미착륙).
- **G-anchor-new** — C4 lane · negL·negZ: **≥10/12 NEW**, 양 seed (H_9334 기지 12/12 재현). 낙제 ⟹ **INVALID(계기 파손)**, 결코 "벽"이 아니다.
- **G-anchor-null** — C4 lane · negJ: 일관성 **≤9/12** (우연). 위반(≥10/12 NEW) ⟹ INVALID(계기가 신호를 제조).
- **G-pedestal** — BASE lane · ped1·ped2: 연산자-부정 방향 일관성이 **≥10/12 이면 INVALID** (참값 우연이어야 할 표면에서 "연산자가 돈다"고 나오면 표면 분류기가 가짜).
- **G-base-live** — BASE lane · negL: **≥10/12 OLD**(=올바른 부정). 낙제 ⟹ INVALID(base lane 자체가 죽음).

### 통제
1. **negJ 앵커** (기지 우연) — 위 G-anchor-null.
2. **PEDESTAL 2종** (ped1 BOUND-형 · ped2 FREE-형) — 형태 클래스마다 하나씩 **정합**. FREE 팔의 신호가 "아무 전치 잡음"이 아님을 가른다.
3. **극성 라벨 셔플 null** — 판독에서 swap arm 의 planted 극성을 어간 간 **10,000 회 순열**하여 경험적 귀무분포를 만든다(예측은 불변, gold 만 재배치 ⟹ 추가 계산 $0). 실제 `C` 가 이 분포의 상위 5% 밖이면 우연.
4. **양 seed (7·11)** — 한 seed 만 유효하면 DIRECTIONAL, 둘 다여야 TERMINAL 급.
5. **다른 arm** (keep n=3 · untouched n=3 · affirm n=2) — 자문용(무검정력, 구속 안 함).

### 판정 (사전 선언)
- **ADDRESS-SPLIT (two-lane 지지)**: BOUND 계열이 C4 lane 에서 NEW(≥10/12)인데 **FREE 계열(negAN/negANG)이 OLD 쪽으로 일관(≥10/12 OLD)** 이고, **BASE lane 에서는 FREE 계열도 연산자가 돈다(≥10/12 OLD)** ⟹ 연산자는 발화하나 CPT 값을 못 본다 = **주소가 (어간)×(템플릿 클래스)** · H_9346 EN ECHO 를 **무교란으로 KO 내부 재현**.
- **SHARED-STORE (two-lane 반증)**: 전 표면(FREE 포함)이 C4 lane 에서 NEW 로 따라오면 저장소는 하나이고 negJ 의 실패는 **연산자 자체의 부재**(주소 문제 아님) ⟹ Fable 재프레임 기각.
- **SURFACE-DEAD**: FREE 계열이 **BASE lane 에서도** 안 돌면(<10/12 OLD) 그 팔은 **쓰기에 대해 아무 말도 못 한다** — 정직하게 "못 쟀다"로 적는다(음성 아님).
- **전 표면 우연** ⟹ 사다리가 템플릿 클래스를 통째로 벗어난 설계 실패 → 재설계(음성 아님).

### kill
기술 실험이라 kill 없음. 단 **G-anchor-* 낙제 = INVALID**, **검정력 부족 = UNDERPOWERED**(음성 아님).

## 5. 자산 · 실행

- ckpt: `~/anima-weights/c34/{natem_c34_main_s7,natem_c34_main_s11}` (BASE lane) · `{swap_c4_s7,swap_c4_s11}` (C4 lane)
- 매니페스트: `anima-py corpus ground_carrierswap --atoms gt_atoms.json --split-seed 1 --seed 7` 로 **결정적 재생성**
  → arm 추첨이 H_9334 동결본과 **완전 일치** 확인(swap 12 어간 · planted 극성 60/60 일치).
- 사다리: 14 표면 × 20 어간 = **280 행** · 최대 행 **49 B** ≤ 64 B 창 (a_korean_byte_budget 게이트 통과).
- 실행: pool(summer) · `--n-decode 280` 명시(기본 200 truncation 함정) · mini 금지.
- rc=137/143/247 = earlyoom **infra-wall**, 결과 아님.

---

## VERDICT — ⛔ INVALID (G-pedestal 낙제 · 양 seed) · 계기 실패, 벽 아님

**측정**: aiden CPU-numpy · 4 ckpt SEQUENTIAL (OOM-guard · OMP=4 · RSS 2.76G single-load) · rc=0/280행/ckpt ·
VERSION 0.13.66 (`anima-py evaluate --xbind cs.txt.flip1.json --surface-set keyladder_v1 --n-decode 280`) ·
매니페스트 결정적 재생성(`corpus ground_carrierswap --atoms gt_atoms.json --split-seed 1 --seed 7` · swap 12어간 · leaks=0).
판독 = 동결 스크립트 verbatim(부호순열 정확분포 + 10k 라벨셔플 null). 아래 수치는 전부 `anima-py evaluate` 산출.

### 게이트 (사전등록 · 낙제 = INVALID)
| gate | lane·surf | s7 | s11 | 결과 |
|---|---|---|---|---|
| G-write | C4 · w0 | NEW 12/12 | NEW 12/12 | ✅ (사실 착륙) |
| G-anchor-new | C4 · negL | NEW 12/12 p=.0002 | NEW 12/12 | ✅ (H_9334 재현) |
| G-anchor-new | C4 · negZ | NEW 12/12 | NEW 12/12 | ✅ |
| G-anchor-null | C4 · negJ | 일관성 6/12 | 8/12 | ✅ (우연) |
| G-base-live | BASE · negL | OLD 12/12 | OLD 12/12 | ✅ (base 살아있음) |
| **G-pedestal** | **BASE · ped1** (`X지 뫄다`) | **OLD 12/12** | **OLD 11/12** | **⛔ INVALID** (참값 우연이어야 할 표면이 ceiling) |
| G-pedestal | BASE · ped2 (`뫄 X다`) | OLD 2/12 | OLD 6/12 | ✅ (FREE 슬롯 통제는 깨끗) |

**판정(동결 readout 그대로) = ⛔ INVALID** — BOUND 슬롯 pedestal `X지 뫄다`(무의미 접미)가 base lane 에서 "부정한다"를 양 seed
ceiling(12/12·11/12 ≥ bar 10)으로 찍었다. **DV 가 진짜 연산자 `않다` 를 못 가른다** — `X지` 조각만으로 부정 연속이
점화된다(raw margin: c4·s7 ped1 [4.2,6.9,4.2,7.7,…] ≈ negL [7.5,8.5,7.5,11.3,…] — 무의미 접미가 진짜 연산자와
**두 lane 모두에서 byte-거의-동일하게** 읽힌다). frozen-first · bar 미이동 · 재run 없음 · no tune-to-green.

### 게이트가 지키는 과학(DIRECTIONAL · 비-cemented — V3 H_9372 와 동형: INVALID 위의 강한 방향성)
1. **연산자의 BOUND '키' = `X지` 조각(byte/fragment-fuzzy), discrete `않다` 토큰 아님.** ped1(`X지 뫄다`)이
   negL(`X지 않다`)과 두 lane 에서 동일 읽힘(C4 12/12·BASE 0/12·마진 크기 근사). ⟹ 접미 축 주소도 byte-fuzzy —
   **V3(어간 축 = byte-fuzzy)와 수렴**. 이제 어간·접미 두 축 모두 fuzzy.
2. **FREE 전치 부정어(`안 X`/`못 X`)는 CPT 로 쓴 값을 전혀 나르지 않는다.** C4 lane negAN/negANG/negMOT NEW =
   0/12·1/12, 0/12·1/12, 0/12·0/12 (큰 음마진 · 셔플 null 12>10 통과 = 일관되게 OLD). = H_9346 EN `not` ECHO 의
   **KO 내부 형태론-통제 재현**. 단 base lane 에서 FREE 표면이 깨끗이 안 돌아(OLD 8~10/12) 판독은 정직하게
   **SURFACE-DEAD**(귀속 불가: '연산자 미발화' vs '쓰기 미도달' 못 가름)로 적음 — 음성 아님.
3. **좁은 IN-CLASS 집합**: 양 lane 12/12 NEW = negL·negZ·negCAS(`지 않다`·`별로 지 않다`·`지 않아`)뿐. 시제/경어/
   띄어쓰기/주제격 변형(negPST·negPRS·negTGT·negPOL·negJ)은 base 서도 안 돌아 SURFACE-DEAD — 단 ped1 오염 때문에
   이 IN-CLASS 폭조차 `않다` 판독이라 확정 못 함.

### 깨끗한 재run 플래그 (tune-to-green 아님)
G-pedestal 을 `지` 를 **포함하지 않는** BOUND-슬롯 무의미 접미로 재설계(예: 연결어미 `지` 자체를 nonce 로 치환) —
`X지` 조각이 부정을 점화하는 교란을 제거해야 BOUND 클래스에서 `않다` 판독을 격리할 수 있다. V3 의 'G-ANCHOR 를
seed별 base flip1 로 재동결' 플래그와 동형. V1 공유저장소 반증·V5 EARNED 종결은 불변.
