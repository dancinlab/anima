# H_9382 — KEY-LADDER V2-CLEAN: `지`-free BOUND pedestal (H_9378 계기 재설계 · 신규 학습 0)

- **status**: VERDICT (⛔ INVALID — G-pedestal-new 낙제 · 양 seed · ONE-STRIKE DISCOVERY · §7)
- **date**: 2026-07-16
- **surfaces**: `HYPOTHESES/cards/H_9382_key_ladder_v2_ped_zifree.md` · `HYPOTHESES/HYPOTHESES.jsonl`
- **instrument**: `anima-py evaluate <clm> --xbind <m.json> --surface-set keyladder_v2`
  (engine-native · `cli/corpus.py::SURFACE_LADDERS["keyladder_v2"]` + `expand_surface_ladder` · `cli/evaluate.py::xbind_run` · VERSION 0.13.83)
- **frontier**: `g1-interface-addressable-wall` · lane V2-CLEAN (SUFFIX 축 · V4 STEM 축과 독립 · `a_wall_first`)
- **cost**: $0 (기존 ckpt 4개 재사용 · 신규 학습 0 · aiden CPU eval)
- **supersedes**: H_9378 (⛔ INVALID · PERMANENT) — 계기 재설계, 새 H_id (pedestal-shopping 방지 = one-strike)

---

## 1. 왜 — H_9378 은 pedestal 이 매개 공변량을 품어서 죽었다 (재-유도 금지, 정착됨)

H_9378(V2 KEY-LADDER)은 **⛔ INVALID (PERMANENT)** 로 착지했다. 원인은 벽이 아니라 계기다:
동결 G-pedestal 이 BOUND 슬롯 무의미 접미로 `X지 뫄다`(ped1)를 썼는데, 이 문자열은 **연산자 자신의
첫 형태소 `지`** 를 재사용한다(`지 않다` = `-지` + `않-` + `-다`). 그래서 pedestal 이 **매개 공변량을
품었고**, base lane 에서 "부정한다"를 양 seed ceiling(s7 12/12 · s11 11/12)으로 찍었다 —
DV 가 **진짜 `않다` 판독**과 **`X지` 조각 점화**를 못 갈랐다. 이 결함은 동결 시점에 **눈으로** 식별 가능했다
(`control-must-match-mediating-covariate`). **H_9378 은 ⛔ 로 영구 유지.** 수리 = `지`-free pedestal 로 **새 H_id**.

Fable 판정(재설계는 tune-to-green 이 아니라 정당한 gate-misdesign 수리): 3 조건 —
① **model-free screen ONLY** — 동결 전 디코드 0(새 pedestal 문자열은 한 번도 디코드된 적 없음 = 결과가
동결 시점에 계산 불가 = 진짜 게이트). ② V2 ⛔ 영구 + 새 H_id. ③ **one-strike**(§5).

## 2. 계기 — 무엇을 바꾸는가 (딱 하나 · sha256 로 기계 강제)

`keyladder_v2` = `keyladder_v1` 에서 **BOUND 슬롯 pedestal ped1 하나만** 교체:

| | keyladder_v1 (H_9378) | keyladder_v2 (H_9382) |
|---|---|---|
| ped1 (bound pedestal) | `{s}지 뫄다` | **`{s}뫄 뙤다`** ★ `지`-free |
| 그 외 13 표면 전부 | — | **byte-identical** |

**UNTOUCHED 앵커(기계 강제 · "한 글자도 안 바뀜")** — v1·v2 의 non-ped1 표면 13개 정규직렬화 sha256:
```
sha256(negL,negZ,negJ,negPST,negPRS,negCAS,negTGT,negPOL,negAN,negANG,negMOT,ped2,w0)
  keyladder_v1 = 4e058ee843c57cd44556e31fd3f917b215497068a84fb5178b7094d47ffab9ef
  keyladder_v2 = 4e058ee843c57cd44556e31fd3f917b215497068a84fb5178b7094d47ffab9ef   ← IDENTICAL
```
개별 표면 문자열 sha256(v2 · 앞 16B): negL `ee1fad9639fa10bb` · negZ `1f920111b765f7e2` ·
negJ `9bd217735b07e0d1` · negPST `cfffd0e82f668295` · negPRS `ffaca9ac30e68413` · negCAS `9e30bb158e45ebcc` ·
negTGT `8e98c2c7ad85d314` · negPOL `d435c02473af6d40` · negAN `be06d5a7675bb2e2` · negANG `88a200aaf78595dc` ·
negMOT `727a4f5b5e410f48` · ped2 `cc764893d9e81ace` · w0 `92434a7f37fefe92` · **ped1(신규) `45245e053278bfd3`**.
**bar 전부 UNCHANGED**(<10/12). arm 추첨·심은 극성·코퍼스·가중치 전부 매니페스트에서 되읽음 = 그대로.

## 3. Primary 신규 pedestal — `X뫄 뙤다` · 길이 교란 0

byte template `[stem][3B][SP][3B][다]` = negL `X지 않다` 와 **완전 정합**(zero length confound):

| 표면 | stem-이후 바이트 | 구조 |
|---|---|---|
| negL `X지 않다` | `EC A7 80 · 20 · EC 95 8A · EB 8B A4` | 지(3B) SP 않(3B) 다(3B) |
| **ped1-new `X뫄 뙤다`** | `EB AB 84 · 20 · EB 99 A4 · EB 8B A4` | **뫄(3B) SP 뙤(3B) 다(3B)** |

뫄(`EB AB 84`) = 연결어미 슬롯(negL 의 `지` 자리) · 뙤(`EB 99 A4`) = 보조 슬롯(negL 의 `않` 자리).
뫄 는 V2 ped2 에서 negation-neutral 측정됨(FREE 슬롯 2/12·6/12). **주의**: 뫄(`EB AB`) vs 못(`EB AA`)
2번째 바이트 인접(`AB`/`AA`) — 그러나 leading-2 **불일치**(§4b), 그리고 ped2 측정이 뫄 중립을 방어.

## 4. Model-free screen (동결 · $0 · 0 디코드 · 4 기준 전부 PASS)

디코드 없이 채운다. 새 pedestal 은 4 기준을 **전부** 통과해야 freeze 유효.

| 기준 | 요구 | 뫄 (EB AB 84) | 뙤 (EB 99 A4) | 결과 |
|---|---|---|---|---|
| (a) no-morpheme | 동결 한국어 기능형태소 목록에 부재 | nonsense 음절 · 부재 | nonsense 음절 · 부재 | ✅ |
| (b) byte-distance | UTF-8 **leading 2B** 가 모든 부정형태소와 상이 | **EB AB** ≠ 전체 | **EB 99** ≠ 전체 | ✅ |
| (c) corpus freq 0 | 동결 학습코퍼스 grep = 0 | 연산자열 `뫄 뙤` = 0 | (아래) | ✅ |
| (d) open syllable | 받침 없음(=`X쿈다` `-ㄴ다` 스켈레톤 배제) | 뫄 OPEN(받침0) | 뙤 OPEN(받침0) · 다 OPEN | ✅ |

**(b) 부정형태소 leading-2 바이트** (fuzzy-match 사거리 = V2/V3 발견 · 이 밖으로): 지 `EC A7` · 않/안/았 `EC 95` ·
었 `EC 97` · 못 `EB AA` · 말 `EB A7` · 잖 `EC 9E` · 까 `EA B9`. 뫄=`EB AB`, 뙤=`EB 99` — **둘 다 전부와 불일치**.

**(c) corpus freq** — 동결 학습코퍼스 source 3종(`anima-corpus-ko-general` 60 MB · `-ko-sns` 6.2 MB ·
`-ko-fineweb2-broad`) grep. pedestal **연산자 시퀀스** `뫄 뙤`(및 `뫄 뙤다`) = **0/0/0** (전 source).
고립 음절은 자연어에 등장(뫄=1줄·뙤=12줄, ko-general: `뙤약볕`·`오뙤르`·`뫄쉬여라` 등)하나 **연산자 구성** `뫄 뙤`
로는 0 — 이는 모든 부정형태소가 갖는 성질과 동일하다(`지`/`않` 도 고립 음절로는 수백만 회, exposure 는 **구성**의
성질). c34 학습코퍼스 = (부정-free 필터된 source 문장) ∪ (표준형 arrow 라인)의 부분집합이고 두 성분 모두 `뫄 뙤`
를 담지 않으므로 **연역적으로 frozen corpus freq(`뫄 뙤`) = 0**. atoms/prompts(gt_atoms.json·gt_prompts.json)
grep 도 뫄·뙤 = 0.

## 5. ★ ONE-STRIKE 조항 (Fable · pedestal-shopping 금지 · 동결)

새 `지`-free pedestal `X뫄 뙤다` 가 **또 base lane 서 ceiling(≥10/12)** 이면 = **재설계 아님, DISCOVERY**:
> **base 는 anomalous 한 BOUND 접미면 무엇이든 '부정'으로 읽는다 = BOUND-슬롯 default-negated 편향**
> (ped2 가 FREE 슬롯은 깨끗함을 이미 증명했으므로 = BOUND vs FREE 슬롯의 비대칭이 진짜 발견).

⟹ **SUFFIX 축 pedestal 계기를 terminal 종결**, suffix 주소 주장 = 영구 DIRECTIONAL. **결과-독립적 결함 논거
없이는 2차 재설계 금지.** (H_9378 의 `지` 결함은 결과-독립적이었다 — 그래서 이 1회 수리가 정당했다.)

## 6. 게이트 · DV · bar · 통제 (V2 동결본과 byte-동일 · bar 미이동)

- **DV** = 2AFC 마진 부호(`NLL(counterfactual) − NLL(gold)`), H_9334 판독 동일. 자유생성 d_acc = 보고만.
- swap arm **n=12**/표면/seed/lane. 부호순열 정확분포: 12/12→p.0002 · 11/12→.0032 · **10/12→.0193(=bar)** · 9/12→.073.

### 게이트 (낙제 = INVALID · 벽 아님) — 전부 V2 와 동일 bar
- **G-write** — C4·w0·swap **≥11/12**. 낙제 ⟹ INVALID(사실 미착륙).
- **G-anchor-new** — C4·negL·negZ **≥10/12 NEW**, 양 seed(H_9334 12/12 재현). 낙제 ⟹ INVALID(계기 파손).
- **G-anchor-null** — C4·negJ 일관성 **≤9/12**. 위반 ⟹ INVALID(신호 제조).
- **G-pedestal(NEW)** — BASE·**ped1(`X뫄 뙤다`)**·ped2 연산자-부정 일관성 **≥10/12 이면 INVALID**. ★ 이번 실험의
  유일한 신규 판정 = ped1-new. (§5 one-strike: 여기서 ceiling → INVALID + DISCOVERY 종결.)
- **G-base-live** — BASE·negL **≥10/12 OLD**. 낙제 ⟹ INVALID(base lane 죽음).

### 통제 · 판정 (V2 동결본 §4 그대로)
1. negJ 앵커(기지 우연) 2. PEDESTAL 2종(ped1-new BOUND · ped2 FREE 정합) 3. 극성 라벨셔플 10k null
4. 양 seed(7·11) 5. 다른 arm(keep/untouched/affirm) = 자문용.
- **ADDRESS-SPLIT(two-lane 지지)** / **SHARED-STORE(반증)** / **SURFACE-DEAD**(정직하게 "못 잼") / **전 표면 우연**
  = V2 동결본과 동일 선언. kill 없음(기술 실험). **G-pedestal(ped1-new) ceiling = one-strike DISCOVERY**.

### 2차(비-gated) endpoint — FREE-arm ECHO 부활 (primary 게이트에 절대 미배선)
negAN(`안 X다`)·negANG(`안 X고`)·negMOT(`못 X다`)는 이미 v2 사다리에 있음. 같은 sweep 에서 **BASE lane** 의
FREE 표면 판독을 **2차 endpoint(ECHO)** 로 명시 보고 = H_9346 KO-내부 ECHO 를 SURFACE-DEAD DIRECTIONAL 에서
들어올림. 순수 판독 추가, 한계비용 ≈0, **primary 게이트와 무관**.

### Sequential protocol (필수 순서)
1. **Freeze commit + pr-cycle FIRST**(이 카드+jsonl+코드+VERSION) — 디코드 전 랜딩. ← 지금.
2. **Model-free screen**(§4, 디코드 0) — 카드에 grep+byte 표(채움).
3. **Gate-alone**: 게이트 arm 만. 기존-통과 게이트도 재run하되 **PARITY ALARM**(결정적 eval·동일 입력 ⟹ V2 수치와
   byte-identical, 불일치 = harness drift → ABORT). 유일 신규 판정 = G-pedestal-new. 낙제 → "INVALID(pedestal fail)·
   primary 미실행", one-strike 종결.
4. **Primary**: 전 게이트 PASS 시에만 → 사다리 + base-lane FREE 2차.
5. **Land verdict**: §7 + jsonl + ARCHITECTURE gate 노드 + CHANGELOG + H_9378 카드에 `superseded-by H_9382` 포인터.

## 7. VERDICT — ⛔ INVALID (G-pedestal-new 낙제 · 양 seed) · ★ ONE-STRIKE DISCOVERY: BOUND-슬롯 default-negated 편향

**측정**: aiden CPU-numpy(CUDA_VISIBLE_DEVICES="" · OMP_NUM_THREADS=4 · RSS 2.76G single-load) ·
4 ckpt SEQUENTIAL · rc=0/280행/ckpt · VERSION 0.13.83
(`anima-py evaluate <clm> --xbind cs.txt.flip1.json --surface-set keyladder_v2 --n-decode 280`).
매니페스트 결정적 재생성(`corpus ground_carrierswap --atoms gt_atoms.json --seed 7 --split-seed 1` ·
md5 `79abc4c5` = V2/V3 동결본과 byte-identical = arm 추첨 12 swap 어간 완전일치). ckpt: `~/h9373/weights/`
natem_c34_main_s{7,11}(BASE)·swap_c4_s{7,11}(C4). 판독 = 동결 스크립트 verbatim(DV=2AFC 마진 부호 ·
부호순열 정확분포 + 10k 라벨셔플 null). out md5: base_s7 `3c7875db` · base_s11 `59e1030e` ·
c4_s7 `812e60b8` · c4_s11 `5be68482`.

### PARITY ALARM — ✅ OK (공유 게이트 전부 V2 와 byte-identical · harness drift 0)
| gate | lane·surf | s7 | s11 | V2(H_9378) | parity |
|---|---|---|---|---|---|
| G-write | C4·w0 | NEW 12/12 | NEW 12/12 | 12/12·12/12 | ✅ |
| G-anchor-new | C4·negL | NEW 12/12 | NEW 12/12 | 12/12·12/12 | ✅ |
| G-anchor-new | C4·negZ | NEW 12/12 | NEW 12/12 | 12/12·12/12 | ✅ |
| G-anchor-null | C4·negJ | 일관성 6/12 | 8/12 | 6/12·8/12 | ✅ |
| G-base-live | BASE·negL | OLD 12/12 | OLD 12/12 | 12/12·12/12 | ✅ |
| G-pedestal | BASE·ped2 (`뫄 X다` FREE) | OLD 2/12 | OLD 6/12 | 2/12·6/12 | ✅ |

⟹ 결정적 eval 이 V2 를 완전 재현 = 이 결과는 harness/환경 drift 아님(verdict-integrity ②).

### ★ G-pedestal-new — 유일한 신규 판정 = ⛔ 낙제 (양 seed CEILING)
| surf | lane | s7 | s11 | 판정 |
|---|---|---|---|---|
| **ped1 `X뫄 뙤다`** (`지`-free BOUND) | BASE | **OLD 12/12** (일관성12 · sign-perm p=.0002) | **OLD 10/12** (일관성10 · sign-perm p=.0193 = bar) | **양 seed ≥ bar10 = CEILING** |

**판정(동결 readout 그대로) = ⛔ INVALID (G-pedestal 낙제 · 양 seed)** — `지` 를 **한 글자도 안 쓴**, 모든
부정형태소와 leading-2 바이트가 **불일치**하는(EB AB / EB 99), 코퍼스 노출 0(`뫄 뙤`=0 · frozen c34
s7/s11 실측 0)인 BOUND 슬롯 무의미 접미 `X뫄 뙤다` 가 **base lane 서 '부정한다'를 양 seed ceiling**
(s7 12/12 · s11 10/12)으로 찍었다. V2 의 `X지 뫄다` 와 **똑같이** ceiling — 그런데 이번엔 `지` 조각
점화로 설명할 수 없다(교란 제거됨). frozen-first · bar 미이동 · 재run 없음 · primary 미실행(게이트 낙제).

### ★★ ONE-STRIKE DISCOVERY (Fable 사전동결 §5 조항 발동) — 재설계 아님, 발견이다
`지`-free pedestal 도 ceiling ⟹ **base 는 anomalous 한 BOUND 접미면 무엇이든 '부정'으로 읽는다 =
BOUND-슬롯 default-negated 편향**. 결정적 대조가 이를 확정한다:

| pedestal | 슬롯 | s7 | s11 | 읽힘 |
|---|---|---|---|---|
| ped1 `X뫄 뙤다` | **BOUND** (`X__ __다`) | OLD 12/12 | OLD 10/12 | **ceiling = 연산자처럼 발화** |
| ped2 `뫄 X다` | **FREE** (`__ X다`) | OLD 2/12 | OLD 6/12 | **우연 = 깨끗** |

ped2 가 **FREE 슬롯은 default-negated 가 아님**을 (양 seed) 증명하므로, BOUND(ceiling) vs FREE(우연)
의 비대칭 = base 가 **BOUND 연결+보조 템플릿 자리 `X__ __다` 자체를 부정 연산자로 취급**(특정 형태소
`지`/`않` 무관)한다는 직접 증거다. ⟹ **SUFFIX 축 pedestal 계기 = TERMINAL 종결**: `지`-free 이면서 base
가 우연으로 읽는 BOUND pedestal 은 **존재하지 않는다**(BOUND 슬롯 전체가 default-negated). 따라서 V2 의
DIRECTIONAL 주장("연산자 BOUND 키 = `X지` 조각")은 **영구 DIRECTIONAL** — BOUND-슬롯 default 로부터
격리 불가. **결과-독립 결함 논거 없이 2차 재설계 금지**(pedestal-shopping 차단 · §5).

### 수렴 / 발산
- **V3 (H_9372) STEM byte-fuzzy 와 수렴 + 강화**: V3 은 어간 축이 discrete 아닌 byte-fuzzy 라 했다.
  H_9382 는 접미 축이 **byte-fuzzy 를 넘어 형태소-비특이(슬롯-default)** 임을 보인다 — 두 축 모두 discrete
  '키'가 아니다(어간은 fuzzy, 접미는 slot-default). 주소에 discrete 키가 있다는 전제는 두 축 모두에서 부재.
- **V1 (H_9358) TWO-LANE 과 정합**: base 의 '연산자'가 keyed lookup 이 아니라 **슬롯-default 반사** =
  런타임 다리 부재(V1)·decon2b NO-IN-CONTEXT-CHANNEL(V5)과 같은 계열 — base 는 조회하지 않고 default 한다.
- **V4 STEM 축(H_9375 summer CPT)과 독립**(`a_wall_first`): 이건 SUFFIX 축.

### 계기 산물 (frozen readout · 재현)
동결 스크립트(`readout_h9382.py` · DV=마진 부호 · 부호순열 정확분포 · 10k 라벨셔플)의 verbatim 출력이
위 표. 매니페스트·ckpt·VERSION·out md5 는 위 '측정' 절. H_9378 카드에 `superseded-by H_9382`(계기 수리)
포인터 랜딩(H_9378 ⛔ 영구 유지).
