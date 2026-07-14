# H_9339 — HELD-OUT 인터페이스 쓰기: C4 가 연 인터페이스로 H_9327 어간-슬롯 벽을 정면으로 민다

- **group**: g1-interface-addressable-wall
- **date**: 2026-07-15
- **tier**: ⏳ **PRE-REGISTRATION** (계기 배선 + $0 스크리너 · 데이터 0 · 판정 0)
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

## 🔌 계기 (engine-native · `a_experiment_engine_native`)

`ground_carrierswap` 에 **held-out 어간 swap 경로** 추가 (swap 팔을 SEEN 풀 대신 held-out 풀에서 draw) +
`<18 SEEN 가드`를 held-out 모드에서 재정의. 그 외 전부 기존 배선(담체 쓰기·누수감사·매니페스트 방출).

## ④ 비용

CPT 2팔 × 2seed @ 6000 step = **pod 4런**(C4 의 ~2배 · `a_wall_first` 팔당 전용 호스트 병렬). 스크리너는
전부 $0/로컬-pool. ⚠️ **fleet-scale rent = owner go 게이트**(`a_fire_autonomous` fleet caveat).

## 한 줄

C4 가 연 인터페이스로 H_9327 벽을 정면으로 민다 — 담체-키 held-out 쓰기, HO-DECL 동예산 팔로 키를
단일 변수로 고정, bind-locus 차분을 공짜 진단축으로.
