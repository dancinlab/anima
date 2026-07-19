# H_9339 — HELD-OUT 인터페이스 쓰기: C4 가 연 인터페이스로 H_9327 어간-슬롯 벽을 정면으로 민다

- **group**: g1-interface-addressable-wall
- **date**: 2026-07-15
- **tier**: 🟠 **2-seed INVALID · s7 🟢 H-ε-INSERT DIRECTIONAL · s11 seed-DETERMINISTIC INVALID(재발사 확증)** (CPT 4런+s11 재발사·engine-native. **s7=벽뚫림**(HO-CARRIER 12·11/12·G-WRITE 11/12·연산자 intact vs HO-DECL 5/12) · **s11 write 미착륙 재현**(G-WRITE 원run 6/12·재run 4/12 = 2 독립run 모두 낙제 → transient 아닌 seed-deterministic 확정). 2-seed cement 불가·s7 crack 1-seed DIRECTIONAL 유지)
- **surfaces**: `HYPOTHESES/cards/H_9339_heldout_interface_write.md` · `HYPOTHESES/HYPOTHESES.jsonl`
- **design**: Fable 위임 (C4=H-ε 이후 다음 한 발)

## 왜 — C4 가 연 문, H_9327 이 닫은 벽

[H_9334](H_9334_carrierswap_store_vs_interface.md) C4 = 🟢🟢 **H-ε TERMINAL**: **SEEN** 어간의 극성을
연산자 자신의 `지 않다` 키로 CPT 쓰면, 서로소 표면에서 신극성 **12/12**(양 seed·p=.0002). 벽은 인터페이스
addressable·FIXABLE. **단 swap 어간은 전부 SEEN** — held-out 미학습 어간엔 미측정.

[H_9327](H_9327_binding.md) BINDING 벽: **held-out** 어간 flip1 = 0.46 = 우연. **단 그 held-out 음성은
선언형/ground 키로 쓴 것**이었다 — 연산자-키 × held-out 조합은 **원장 확인 결과 미측정**(Fable). 게다가
[H_9324](H_9324) 가 "600 step 음성 = 예산 음성"을 증명했으므로 H_9327 음성 자체가 **키+예산 재검 대상**.

## 🎯 조작 — C3 vs C4 미러, 어간만 held-out 으로 치환 (단일 변수)

**팔** (seed 7·11 · base = natem_c34_main):
1. **HO-DECL**: held-out 어간 극성을 **선언형 키만** CPT (H_9327 재현 — 이번엔 H_9324 검증 예산 6000@2e-4 로
   "예산 도망구멍" 봉쇄)
2. **HO-CARRIER**: 동일 + **연산자-담체**(전혀/그다지/결코 `<어간>지 않다`) 추가 — C4 와 정확히 같은 단일 추가
3. **SEEN 양성앵커** = 기존 `swap_c4_s{7,11}.clm` 재사용 ($0·재학습 없음)
4. **negJ** `지는 않다` 통제 = 두 팔 다 우연 유지 예측

## 📐 사전등록 — 서명된 예측 (데이터 전 동결 · 카운트로)

DV: held-out 어간에 대해 채점 표면 negL(`{s}지 않다`)·negZ(`별로 {s}지 않다`)에서 flip1 이 **신극성** 추종 개수.

| 결과 | HO-CARRIER negL·negZ | 판정 |
|---|---|---|
| **H-ε-INSERT** (벽 뚫림) | **≥10/12 양 seed** (p≤.0193/seed) **이고** HO-DECL ≤9/12 | 🟢 H_9327 벽 뚫림 — 고침 = 쓰기 프로토콜(키가 레버, 팔 차분 증명) |
| **KEY-CREATION 벽** | 3–9/12 양 seed **+ G-WRITE 통과** | 🧱 인터페이스는 **UPDATE 전용, 엔트리 생성은 사전학습 잠금** — TOST(Δ_eq 사전고정) |
| 두 팔 다 ≥10/12 | — | 키가 아니라 **예산**이 진범 = H_9327 음성이 예산 인공물(값진 부호) |
| seed 불일치 / G-WRITE 낙제 | — | INVALID (예산 1회 증액 재발사 · tune-to-green 아님) |

## 📊 CPT 판정 (4런 완료 · engine-native aiden · frozen grid · mechanical 무자판정)

`anima-py train --arch clm --canon --arm ctrl --init natem_c34_main_s{7,11}.clm --e0 3 --emax 3 --corpus
ho_{arm}_s{S}.txt --steps 6000 --lr 2e-4 --bs 8 --seq-len 1024 --bf16` × 4 → `anima-py evaluate --xbind`.
채점 표면(2AFC flip1) swap 어간(held-out DV) negL·negZ D-acc×12 count:

| arm | s7 negL·negZ | s11 negL·negZ | G-WRITE(swapC per-stem) | G-PRESERVE(preserve\|negL) | negJ null |
|---|---|---|---|---|---|
| **HO-CARRIER** | **12·11/12** 🟢 | 8·6/12 | **s7 11/12 ✅ · s11 6/12 ❌** | **s7 12/12 intact · s11 0.667 CRATER** | s7 8 · s11 5 /12 |
| HO-DECL | 5·5/12 | 5·6/12 | — | 11/12 · 11/12 | 6·4/12 |

- **seed 7 = 🟢 H-ε-INSERT 벽뚫림**: 全게이트 PASS(G-WRITE 11/12 쓰기착륙·G-PRESERVE 12/12 연산자 intact·negJ~chance) + HO-CARRIER min 11/12 ≥10 & HO-DECL max 5/12 ≤9. **담체키 held-out 쓰기가 미학습 어간의 새 엔트리에 도달**, 선언키는 못함 = H_9327 어간-슬롯 벽 s7서 뚫림.
- **seed 11 = ⛔ INVALID**: G-WRITE **6/12**(쓰기가 절반만 착륙 = INVALID 아닌 음성) + G-PRESERVE **0.667 crater**(carrier_s11 CPT가 SEEN 연산자 손상·`corpus-py-1` ⑥ CPT-destroys). swap 판독 무자격.
- **2-seed 판정 = ⛔ INVALID**(사전등록: seed불일치 ∧ G-WRITE낙제 = INVALID). s7 강한 DIRECTIONAL 양성이나 s11 미착륙으로 cement 불가. 4 ckpt 영구저장 `~/anima-weights/c34/ho_*_cpt.clm`(sha 검증).

**🔁 s11 재발사 (동일예산·transient vs seed-deterministic 판별 · summer engine-native)**: carrier_s11 재run(val_CE 0.144<원 crater run·더 안정 학습)의 G-WRITE swapC readback = **4/12**(원run 6/12). ⟹ **2 독립run 모두 쓰기 미착륙**(6/12·4/12<11/12) = **transient 불안정 반증·seed-DETERMINISTIC 확정**. G-WRITE 낙제=INVALID이므로 flip1 swap DV 무의미(읽을 엔트리 부재). 재발사가 "s11=일시적" 가설을 깨끗이 반증(재발사 소진). 1-seed DIRECTIONAL, 2-seed 미cement.

**⚠️ 정정 — 진범은 stem-draw 아닌 RUN/seed ($0 대조)**: 처음 "s11=held-out 어간 draw 의존"으로 추정했으나 $0 byte-len/어간 대조가 반증. 어간 **`튼튼하`(9B)가 s7·s11 swap set 둘 다 존재** — s7 run 착륙(all-tag)·s11 run 실패(같은 어간 반대 결과). ⟹ stem-draw·byte-len 무관(s11 실패 3~9B 전범위 산개), **carrier_s11 CPT run(base natem_c34_main_s11 + 코퍼스)이 어간 무관 담체 write를 전역 under-imprint**. 진범 후보=base ckpt seed별 write-imprint 용량 차이 or s11 코퍼스 stem 혼합 최적화 간섭. 후속(별도 H)=natem base seed별 imprint 용량 진단 or 더 많은 seed로 s7 crack 재현성 확인.

## 🚦 게이트 (동결)

- **G-WRITE**: 담체 표면 자체 readback ≥11/12 — 낙제=음성 아니라 INVALID (`write-lever-budget`)
- **G-BASE-FIRST**: CPT 전 base 에서 held-out flip1 = 우연 실측 (`cpt-destroys` — '못 함' vs '죽임' 가름)
- **G-PRESERVE**: CPT 코퍼스 0회 SEEN 어간 flip1 이 base 대비 유지 (replay 허용·판정 지층 0회 유지)
- **G-LEAK**: 채점 표면·held-out 어간의 사전학습/CPT 코퍼스 0회 감사 (빌더 코드화)

## ② $0 스크리너 (발사 전 · falsify 가능)

1. **G-LEAK + G-BASE-FIRST**: base `--xbind` held-out 매니페스트 — 우연 아니면 발사 중단
2. **`--bind-locus` C4-vs-base 차분**(B 알맹이 흡수): `swap_c4_s{7,11}` vs `natem_c34_main_s{7,11}` 차분으로
   C4 쓰기가 착륙한 **locus**를 $0 에 읽어, A 음성 시 "착륙했는데 안 읽힘 vs 착륙 자체 안 됨" 진단축 확보
3. 빌더 스모크: held-out 매니페스트가 WRITE 채널 측정 가능하게 나오는지

## 🔌 계기 (engine-native · WIRED · `a_experiment_engine_native`)

`anima corpus ground_carrierswap --held-swap [--decl-only]` (cli/corpus.py · Fable diff-spec).
swap 팔을 **held-out 풀에서 draw**(단일 변수 vs C4), SEEN 전체 draw 는 먼저 그대로 돌아 affirm/keep/untouched 가
C4 와 stem-동일 → C4 가 쓴 12 stem 은 `preserve`(0× CPT · 최고검정력 G-PRESERVE 지층). HO-CARRIER=`--held-swap`
(양키·arrow+carrier), HO-DECL=`+ --decl-only`(선언키만). 가드: held-swap×carrier-only·decl-only-without-held-swap
fail-loud. 신규 감사: plant-contradiction(swap stem 진극성 선언줄 0)·G-WRITE readback-present(카드 G-WRITE=담체
readback ≥11/12 → `_carrier_readback_manifest` swapC 12×3 gates·keepC 3×3 twin).

**빌더 스모크($0 스크리너 (c)) 통과** (local gt_atoms.json · 20 train/29 held):
- C4/C5 **byte-inert**(held_swap=False sha 348d89bc == origin) — 기본경로 bit 무변.
- HO-CARRIER/HO-DECL 빌드 OK · **preserve == C4 swap**(frozen check) · flip1/write manifest **byte-identical**
  (양팔 · draw 순수함수) · plant-contradiction 0 · readback 57/57(HO-C)·12/12(HO-D) · gold 정합(swap planted=1-pol·preserve planted=pol).
- 잔여 스크리너: (a) G-LEAK+G-BASE-FIRST base `--xbind` held-out (b) `--bind-locus` C4-vs-base 차분(조건부·A-음성시). 통과시만 4-pod CPT.

## 📊 $0 스크리너 (a) 결과 — G-BASE-FIRST base 앵커 (frozen · 2-seed · engine-native aiden)

`anima-py evaluate natem_c34_main_s{7,11}.clm --xbind ho_carrier.flip1.json` (176M c34 base · GPU cupy · flip1 매니페스트=HO-CARRIER draw). held-out swap 어간(DV) 채점 표면 negL/negZ D-acc:

| arm | s7 negL·negZ | s11 negL·negZ | 해석 |
|---|---|---|---|
| **swap (held-out=DV)** | **0.250·0.250** | **0.333·0.250** | 다수라벨 붕괴(대부분 `긍정` 출력)=planted 극성 **미조합** |
| preserve (SEEN·C4 stems) | 1.000·1.000 | 0.917·— | 연산자 **alive** on SEEN (G-PRESERVE 앵커) |
| keep/untouched (SEEN) | 1.000 | 1.000 | 연산자 alive |
| null negJ (`지는 않다`) | 0.417·0.333 | 0.333 | ~chance (계기 위조신호 0) |

**PASS** (양 seed 일치): (a) base 는 held-out 에서 planted 극성을 **이미 조합 못 함**(swap 0.25~0.33 ≪ SEEN 0.92~1.00) = confound 없음·H_9327 BINDING 벽 base 재현 (`corpus-py-1` B: '못함' vs '죽임' 가름 — base=못함 확정) · (b) G-PRESERVE 앵커 SEEN=alive · (c) 채널 측정가능(null~chance). ⟹ 4-pod CPT 발사 **정당**하나 fleet rent=spend → **OWNER GO 대기**(`a_fire_autonomous` fleet caveat).

## ④ 비용

CPT 2팔 × 2seed @ 6000 step = **pod 4런**(C4 의 ~2배 · `a_wall_first` 팔당 전용 호스트 병렬). 스크리너는
전부 $0/로컬-pool. ⚠️ **fleet-scale rent = owner go 게이트**(`a_fire_autonomous` fleet caveat).

## 한 줄

C4 가 연 인터페이스로 H_9327 벽을 정면으로 민다 — 담체-키 held-out 쓰기, HO-DECL 동예산 팔로 키를
단일 변수로 고정, bind-locus 차분을 공짜 진단축으로.
