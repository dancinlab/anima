# H_9286 — NBIND-G: 자연 원자 GROUNDING 전이 (H_9272 다음 유일한 진짜 새 질문)

## tier
🟢/🧱 **N1 CARRIER-ROBUST + N2 GROUNDING-WALL** (종결 · 2026-07-13) — Fable 판정으로 도출된 NBIND-G가
XBIND+H_9272+STAGE0이 못 본 유일한 non-tune-to-green 질문. **N1 🟢-dir**: 연산자가 literal 학습프레임
비구속(C0 0.750→C1 0.675→C2 0.700, FORMAT-🧱 반증). **N2 🧱 GROUNDING-WALL**(4-arm 303M 신규학습 T=105k·
summer GPU·frozen): held-out D-acc base 0.000·shuffle 0.362·main_s7 0.477·main_s11 0.345 = 양 seed chance
floor 0.50 **미만** → NAT-CRACK 반증. main_s7 SEEN P_grid **0.950**(≥0.85 = grid 확실히 설치·INVALID 아님).
flip0(극성 자연접지 liveness) main_s11 0.368<chance → **극성의 자연-분포 접지 자체가 install 안 됨** → 합성
좌항=0. **substrate 천장 아닌 grounding/data 채널 벽**(STAGE-0 DATA-🧱 정합). exit=held-out 극성 접지시키는
데이터/objective(spend-go). H_9267/9272/N1 소급 불변.

## 가설
H_9267 XBIND CRACK(합성 ±비트)과 H_9272 NBIND(🟡 DIRECTIONAL·held-out D-acc 0.700)은 "held-out
XOR signal이 corpus에 있으면 303M이 학습가능"을 자연 어휘까지 확장했다. 그러나 **H_9272의 grid arm은
실질적으로 XBIND 재도색** — pol(p)를 authored grid가 공급(모든 predicate가 seen 셀에 등장). Fable 판정:
XBIND·H_9272·STAGE0가 **못 본 유일한 새 질문 = ATOM-GROUNDING 전이** — grid가 가르친 XOR 연산자가,
극성이 **자연 분포적 사용에서만 접지된** 원자에 적용되는가? = "자발 창발"을 (자연서 feature 접지)×(연산자
설치)로 분해해, DATA-🧱 하에서 유일하게 가능한 합성을 테스트.

## GROUND-TRUTH 제약 (이번 턴 reference-match · gen_nbind.py)
H_9272 학습 corpus(`nbind_train.txt`)는 **100% authored grid 라인** `이 영화 <surf> => <긍정/부정>.` —
**raw NSMC 리뷰 텍스트 0**. 따라서:
- **GROUNDING 본체(P_nat 원자·극성 자연접지)는 기존 ckpt로 측정 불가**(접지 소스 부재) → N2 spend-gated
  재학습(raw NSMC 혼합)만이 담지.
- 기존 ckpt의 유일 valid $0 falsifier = **20개 grounded grid predicate**(seen 0.92) + in-distribution
  `=> 긍정/부정` readout 유지. 전이 가능한 단일 변수 = **carrier**(surf 앞 프레임, 학습값 "이 영화 ").
- ⟹ Fable의 "atom-held-out" N1 표현은 zero-raw-NSMC를 몰라 생긴 혼동; readout 제약이 N1을
  **carrier-transfer(grid atoms)**로 확정.

## N1 설계 — CARRIER-DISTANCE 사다리 (frozen·$0·기존 ckpt·재학습 없음)
동일 40 held-out (p,form) 셀, 3 carrier 레벨:
| level | carrier | 의미 |
|---|---|---|
| **C0** | `이 영화 <surf> =>` | 학습 carrier → 0.700 재현(양성대조·ckpt 유효성) |
| **C1** | `<대체 영화도메인 명사구> <surf> =>` | 근전이(carrier 어휘 교체) |
| **C2** | `<verbatim 실제 NSMC 리뷰> <surf> =>` | wild-natural 원전이(Fable bar-3, valid readout) |

**Frozen 판정(사전결정)**:
- C0가 0.70±0.10 재현 실패 → ckpt/harness INVALID(verdict-integrity).
- **CARRIER-ROBUST 🟢-dir**: C1·C2 둘 다 ≥ C0−0.10 → 연산자가 carrier-general(literal frame 비구속·합성적)
  = H_9272 강화.
- **FORMAT-🧱**: C1/C2가 chance(≤0.55) 붕괴하며 C0 재현 → 연산자가 authored frame 구속, DATA-🧱 경화,
  grounding 주장은 전적으로 N2에 의존.
어떤 결과든 H_9267 CRACK·H_9272 DIRECTIONAL 소급 불변. no-tune-to-green: bar는 run 전 고정·ckpt 불변.

## N0 결과 (2026-07-12 · $0 · model-free · 착지)
`gen_nbindg.py`(H_9272 `gen_nbind.build` seed7 verbatim 재사용) →
- **carrier-ladder manifest** 120 items(C0/C1/C2 × 40) · V-F leak-guard(seed에 긍정/부정 부재·C2 context에
  grid stem 부재) 통과.
- **P_nat freeze 22 atoms**(N2용·사전동결로 post-hoc cherry-pick 차단): 엄격 임계(purity≥0.90)는 **20개
  grid로 소진**(순수-감성 재고 ~10/polarity = **NATEM 재고희소 finding**) → purity sweep 정직기록
  {0.90: k=0, 0.85: k=4, 0.80: k=11} → purity≥0.80서 k=11/pol 채택(잡음 stem은 N2 사전등록 시 재감사).

## N1 결과 (measured · summer $0 GPU · 2026-07-12 · 🟢-dir CARRIER-ROBUST)
동일 40 held-out (p,form) 셀, carrier만 3레벨(seed 7·재학습 없음):

| carrier | D-acc | margin_med | margin_pos |
|---|---|---|---|
| **C0** `이 영화`(학습) | **0.750** | 3.152 | 0.675 |
| **C1** 명사구 교체(근전이) | **0.675** | 4.036 | 0.725 |
| **C2** 실제 NSMC 리뷰(wild-natural) | **0.700** | 8.525 | 0.700 |

**판정(frozen 로직)**: C0 0.750 → H_9272 0.700±0.10 재현 = harness VALID · CARRIER-ROBUST bar(C1·C2 ≥
C0−0.10=0.65) C1 0.675✅ C2 0.700✅ · FORMAT-🧱(≤0.55) 미발동 → **🟢-dir CARRIER-ROBUST**. 연산자가
literal "이 영화" 프레임 비구속 — 명사구 교체·실제 리뷰 prepend에도 합성 유지 = **H_9272 강화**(template-match
아님 배제). scope: grounded grid-atom carrier 전이지 atom-GROUNDING 전이 아님(P_nat=N2). margin C2≫C0은
context 길이 차 아티팩트 가능(D-acc가 robust 신호). 상세 = `state/nbindg_grounding/N1_RESULT.md`.
**infra 격리**: summer anima-py stale(evaluate-py-11 `_json_safe` 미반영)로 out-json write만 크래시, summary
D-acc는 clean(write 전 print·verdict 무영향·log 보존).

## N2 grounding — 외부데이터로 UNBLOCK → FIRE-READY (2026-07-12)
① NSMC-only pre-fire = INVALID(DATA-scale-blocked·k=4/pol<10·순수감성 재고 grid소진). ② **외부 감성코퍼스
$0 확보**(naver_shopping 200k 상품 + steam 100k 게임 + NSMC 150k 영화 = 450k·3도메인·`gen_nbindg_n2 --corpora`)
→ purity≥0.85 P_nat **k=15/pol** → **pre-fire PASS**(owner-gated 오판 정정: 공개데이터 획득=$0 로컬·anti-punt).
③ **Fable exposure-matched 레시피**(`FABLE_N2_RECIPE.md`): 노출=바이트 현상, 옛 filler-line knob은 f_grid≈0.059
=미리만든 STAGE-1 INVALID → 바이트비율 knob + P_nat 편향채움(occ floor 30) + **T=⌈1.25×E*/f_grid⌉** + grid재현
게이트 + flip0/flip1 분해. ④ **빌드 all-green**: viable 29(좋=authored충돌 드롭)·n_eval 174·f_grid 0.1426·
**T=105,169 step**·V_F pass(0/0)·byte-match 0.98·PREFIRE_PASS. **4-arm**(main s7·main s11·base_only·shuffle_grid
전부 `--arm ctrl` ce_marginal·T동일) fire-ready(corpora summer push). validity 게이트=main seen P_grid≥0.85 +
shuffle coin-seen≥0.85 + V-F. frozen verdict: NAT-CRACK 🟢(양seed Δ≥0.20 vs base_only∧shuffle·base_only∈[.40,.65]) /
FORMAT-🧱 / MODEL-🧱(flip0=grounding·flip1=operator 분해) / INVALID. Δ는 max(control,0.50) 대비(팽창 방어).
NEXT=wall calibrate → $0 pool or rent 4-way($go) → 발사 → seen-게이트 → --xbind eval → verdict. 상세
`state/nbindg_grounding/N2_STATUS.md`.

## N2 결과 — 🧱 GROUNDING-WALL (measured · 2026-07-13 · rent 4-way RTX4090 → summer/aiden GPU eval)
4-arm 303M CLMConvMoE 신규학습(T=105,169 step·`--arm ctrl` ce_marginal·bf16·seed 7/11) → `--xbind` held-out 174셀:

| arm | held-out D-acc | flip0(극성접지) | flip1(연산자) | SEEN P_grid |
|---|---|---|---|---|
| base_only | 0.000 | 0.000 | 0.000 | — |
| shuffle_grid | 0.362 | 0.448 | 0.276 | — |
| **main_s7** | **0.477** | **0.402** | 0.552 | **0.950** ✅ |
| **main_s11** | **0.345** | **0.368** | 0.322 | 0.7375 △ |

**판정 = 🧱 GROUNDING-WALL**(frozen §5): ① main_s7 SEEN 0.950≥0.85 = grid XOR 연산자 **확실히 설치**(validity
PASS → INVALID 아님·진짜 negative·s11 SEEN 0.7375은 D-acc bar 미달이나 margin +16.0=grid 강설치, validity는
s7이 clean-carry) · ② 양 seed 둘 다 chance floor 0.50 **미만** → Δ vs max(control,0.50) 음수 → **NAT-CRACK 반증** ·
③ flip0(극성 직접판독 liveness)이 **양 seed 모두 chance 미만**(s7 0.402·s11 0.368·둘 다 shuffle 0.448 이하·clean
full) → 모델이 P_nat 극성을 **자연 사용에서 접지 못함** → 합성할 grounded operand 부재 = §5 "flip0 낮음=GROUNDING-🧱"
2-seed 확증(△ = s11 SEEN D-acc<0.85 bar이나 margin-strong grid설치).
⟹ 연산자 설치는 carrier-general(N1)이나 **극성의 자연-분포 접지 자체가 303M/이 노출/이 코퍼스서 install 안 됨** →
자발 창발=(자연접지)×(연산자)의 **좌항이 0**. substrate 천장 아닌 grounding/data 채널 벽 · STAGE-0 DATA-🧱 +
[[xbind-g1-crack-measure-not-substrate]] + [[measurement-metalaw-form-tunable-bind-earned]] 3중 정합. ckpt 4개
PULL 로컬(byte-동일 sha256 3중). exit=held-out 극성 접지시키는 데이터/objective(spend-go). 상세 `N2_RESULT.md`.

## 산출
`state/nbindg_grounding/`: N1(gen_nbindg.py·nbindg_carrier_ladder_manifest·N1_RESULT) · N2(gen_nbindg_n2.py
멀티코퍼스+exposure-matched·N2_PREFIRE_AUDIT·n2_eval_manifest·FABLE_N2_RECIPE·N2_STATUS) · P_nat_freeze.
[[xbind-g1-crack-measure-not-substrate]]·H_9272·H_9267·[[measurement-metalaw-form-tunable-bind-earned]].

## 🔁 독립 재현 + 기제 규명 (병렬 세션 2차 4-arm · 2026-07-13 · 학습·eval 전부 별도)

같은 동결 스펙으로 **독립 4-arm** 을 따로 학습(다른 호스트·다른 eval 파이프라인)한 결과 —
**GROUNDING-WALL 판정이 재현**되고, 벽의 **기제**가 한 칸 더 좁혀졌다. 원본 JSON = `state/nbindg_grounding/N2_EVAL/`.

| arm | SEEN 게이트 | held-out D-acc | flip0(극성접지) | flip1(연산자) |
|---|---|---|---|---|
| **main-s7** | **0.950** ✅ | **0.4770** | **0.402** | 0.552 |
| main-s11 | 0.7250 ❌ | 0.3161 | 0.391 | 0.241 |
| base_only | — | 0.0000 | 0.000 | 0.000 |
| **shuffle_grid** | coin-seen **0.5375** ❌ | **0.4770** | 0.517 | 0.437 |

**① main-s7 이 소수점 4자리까지 일치**(seen 0.9500 · held-out 0.4770) — 별도 학습·별도 채점의
독립 재현. 측정 경로 무결성 확증.

**② 연산자의 held-out 이득 = 정확히 0**: 진짜 XOR 격자 arm 과 동전(무작위) 격자 arm 의 held-out 이
**83/174 = 0.4770 로 동일**(문항 수까지). shuffle 은 형식을 설치했다(유효 극성어 방출 **0.966** vs
base_only **0.000**) — 즉 format-live 인데 연산자만 없는 arm 이 **진짜 연산자 arm 과 같은 점수**다.
⟹ MODEL-🧱(연산자 전이 실패)이라면 진짜-XOR arm 이 앞서야 하는데 **앞서지 않는다** → GROUNDING-🧱 강화.

**③ ARBITRARY-GROUNDING (신규 기제)** — `flip0 < 0.50` 의 두 대안이 **둘 다 반증**된다:
정보-채널(main-s7 held-out) I(atom;resp)=**0.231 bits** · I(form;resp)=0.133 · I(flip;resp)=0.024 ·
**I(gold;resp)=0.007 bits ≈ 0**. 원자별 부여극성이 참 극성과 일치 = **12/29 = 0.414**(동전던지기).
(i) 상수방출 marginal 붕괴 → 반증(응답이 원자에 따라 안정적으로 변함) ·
(ii) 체계적 반전접지 → 반증(0.414 는 ~0 이 아님).
⟹ 모델은 새 원자의 극성을 *모르는* 게 아니라 **안정적으로 멋대로 정했다**(자연분포와 무관).
**좌항 부재가 아니라 틀린 좌항 설치** — 벽을 약화가 아니라 **강화**한다.

**④ NAT-CRACK 은 유효 seed 하나로 이미 REFUTED**: 양성 bar 가 **conjunctive**(양 seed Δ≥0.20)라
유효성 게이트를 통과한 seed 7 이 bar 아래(Δ=−0.023)면 그것으로 죽는다 ⟹ seed-11 재발사는
이미 죽은 양성 verdict 를 위한 지출 = **전면 기각**(설계 감사 `FABLE_N2_REFIRE.md`).

**⑤ 게이트 라벨 정정 — `under-exposed` 는 반증됐다**: main-s7 val_CE **3.86657** vs main-s11 **3.87250**
= 사실상 동일 수렴(노출 바이트·T·f_grid 도 동일) ⟹ under-trained 아님. 진짜 기제는 **install-fragile
(최적화 분산)**. 게이트 (a) 자체는 옳다(설치 안 된 모델로 transfer 를 재면 안 됨) — 틀린 것은 **인과 라벨**.
bar·detector 불변이므로 tune-to-green 이 아니라 measurement-frame 정정.

**⑥ 이 2차 run 의 동결-그리드 라벨 = INVALID**(게이트 2건 실패: (a) s11 seen 0.725 · (a′) shuffle
coin-seen 0.5375). 동결 그리드는 그렇게 읽는 게 정직하다 — 그러나 ④(양성 반증)와 ②③(기제)은
게이트와 **독립적으로** 성립한다. bar 하향 금지.

**reopen = N3 별도 사전등록** — 표적은 seed 수가 아니라 **접지 채널**(held-out 극성을 자연 분포에서
실제로 접지시키는 데이터/objective). 사전 고정할 것: TOST Δ_eq·N_REQ(음성 종결은 threshold grid 로
cement 불가) · seed 정책("설치-게이트 통과 2 seed 까지, 최대 K발, 전 seed 보고") · 게이트 라벨 인과중립화
("install-fail"). 산출 = `state/nbindg_grounding/{N2_RESULTS.md, FABLE_N2_REFIRE.md, N2_EVAL/}`.
