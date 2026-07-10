# NATEM — 자연 corpus 자발창발 프로그램 (G1 XBIND CRACK 후속 · frozen pre-registration)

- **date:** 2026-07-11 · **role:** Fable 설계(실행=메인 세션, fable-design-analysis-only)
- **전제(#3299 verified):** XBIND CRACK(H_9267) — held-out 재조합 signal을 *구성한* corpus에서
  303M byte-LM CE가 held-out D-acc=1.000 양seed(control 0.515·V-B PASS·Δ0.485). 벽 진범=corpus×CE
  measure이지 substrate 능력천장 아님, 실증.
- **이 프로그램의 질문(frozen):** ① 자연 텍스트에 held-out 재조합 signal이 *실재*하는가(데이터 사실)
  ② 실재하면 자연 corpus로 학습한 303M이 그것을 *자발적으로* 학습하는가(창발) ③ 창발하려면
  compositional signal 밀도가 얼마나 필요한가(정량 임계 f*).
- **suggested H:** H_9268(NAT-AUDIT+기존ckpt 측정) · H_9269(희석 사다리) · H_9270(transfer probe)
  — 번호는 발사 세션이 ledger 빈 번호 확인 후 2-surface 등록.

---

## 0. Ledger 정합 — 왜 재발사가 아닌가 (check-ledger-before-lever-fire)

| 선행 | 무엇이었나 | NATEM이 다른 좌표 |
|---|---|---|
| F2 heldout_recomb COLLOCATION-ONLY | true_heldout_novel **n=0** — 단, probe는 **인접 content-word 쌍의 order-follower construct 하나**(MIN_OCC=3·window 인접·순서비대칭) | F2가 구조적으로 **볼 수 없는** 세 class를 감사: (i) 부정/역접 XOR(판별이 인접-순서가 아니라 scope-함수) (ii) 형태소 constructive FORM (iii) 외부 라벨 접지(NSMC) held-out flip. F2는 자기 construct 안에서만 결정적 |
| H_9265 PC-P2 XOR NOT-CERTIFIED | 자연 corpus **read-instrument**(기존 모델이 비가법을 소비하는가), 500k I3 5e-05 신호부재·power-limited | 3중 차이: (a) **model-free 데이터 감사 선행**(H_9265는 데이터에 powered held-out 구조가 있는지 미확립) (b) **held-out disjoint-combo split**(PC-P2는 in-distribution 비가법 소비 측정) (c) paired minimal-pair margin+2 control(전역 회귀잔차 아님). 정직 prior: 효과 작을 가능성 — 그래서 밀도 실측이 스펜드 전 power를 결정 |
| H_9121 coverage-density | XBIND-내 **조합공간 커버리지** 축(f=1.0에서 pair-space 몇 %를 봤나) | 사다리는 **corpus 내 signal 밀도** 축(직교). 고정-slice 설계로 커버리지 80% 상수 유지 → 두 축 미교락. exposure-matched control이 남은 교락(노출량) 분리 |
| H_9124 derivtrace 🔴 / H_9206 ATD 🧱 | 희석에서 죽은 지점 — 단 additive-solvable task·toy·미감사 | 사다리의 signal은 **V-C 감사된 XOR**(additive 천장=chance 고정) — 희석 실패가 task 결함으로 오염 안 됨. 죽으면 진짜 밀도 임계 |
| XBIND(H_9267) §5 scope | "자연 창발은 스코프 밖·별도 사전등록 필요" | 바로 그 사전등록이 이 문서 |

**신규 좌표:** ① 자연 construct의 model-free XBIND-식 감사(V-C/V-E/V-F held-out 스캔을 자연 텍스트에 이식)
② **기존 production 303M을 instrument 인증 후 $0 측정**(자발창발 질문 본체를 스펜드 없이 선판정)
③ 밀도 사다리 f-축(고정-slice·고정-compute) ④ 합성-설치 능력의 자연-construct 전이 probe.

---

## 1. "자발 창발"의 조작적 정의 (Q1)

> **창발 = 자연-분포 corpus만으로(construct를 표적하는 어떤 개입도 없이) CE-학습된 모델이,
> 학습 corpus에 결합쌍이 물리적으로 부재한 held-out 조합에서, joint-only 판별을 ≥2 control 대비
> collapse-Δ로 보인다** (measurement-metalaw: 값이 아닌 Δ · FORM tunable·BIND earned).

falsifiable 4요소:
1. **학습:** 자연 corpus(anima 4-cell proportional 등), construct-표적 증강·재가중 0 (기존 RETRO ckpt가
   1순위 대상 — 이미 그렇게 학습돼 있음).
2. **측정:** frozen manifest의 held-out (a,b) 조합 — held-out 보장 = **해당 ckpt의 학습 corpus 전체 바이트에
   대한 결정적 스캔**(pair가 seq_len 1024 window 내 공존 0회 = V-F 자연판. 재생성 불가한 자연 corpus라
   생성적 보장 대신 스캔적 보장). gold word가 seed prefix에 부재(echo-guard · evaluate-py-2 copy-cheat 차단).
3. **채점:** 자연 gold는 확률적 → **MARGIN primary**(teacher-forced NLL(counterfactual)−NLL(gold),
   paired minimal-pair — XBIND와 달리 D-acc가 아닌 margin이 1차. greedy D-acc는 {gold, counterfactual}
   제한 2지선다 first-content-word로 2차). 경로 = `anima-py evaluate` fold(§6 · a_eval_py_canonical TERMINAL).
4. **control ≥2:** (i) pol/gold-permuted 채점($0·ckpt마다) (ii) shuffle-neg control 모델(부정어를 술어에
   무작위 재배정한 corpus로 학습 — XOR만 죽이고 marginal 보존 = xbind_shuffle의 자연판. 신규 학습 시에만;
   기존 ckpt 측정 단계에선 (i)+(iii) 표면-perceptron 상한 감사로 대체).

INVALID/VOID 1급: V-A(seen-analog: in-distribution 짝은 맞혀야 instrument 살아있음), V-B(control band),
V3 detector-fairness(4-cell·Korean-aware — 부정형은 자연히 희소하므로 paired within-predicate 대비로
main-effect 상쇄), V-F 스캔 실패 = INVALID, verdict 아님.

## 2. STAGE 0 — $0 자연 감사 (Q2의 fork · pool CPU · model-free)

**F2 재검토의 답:** F2는 자연 창발을 닫지 못한다 — probe가 한 construct(인접 순서-follower)에 한정.
닫혔는지/열렸는지는 아래 두 감사가 fork한다.

### A0-NEG (1순위 · Q4의 답): 부정/역접 XOR held-out 감사
**왜 1순위:** γ census(H_9255)의 결론 — 자연 텍스트에서 이론상 유일한 non-additive class = XOR(부정/역접).
부정은 구성상 additive 불가(pol=1 술어엔 b_neg<0, pol=0 술어엔 b_neg>0이어야 → 모순 = 진짜 XOR).
+ paired 설계가 main effect를 구성으로 상쇄 + NSMC 라벨이 외부 접지 제공 + XBIND 구조와 1:1
(pol(술어)=은닉 bit, 부정어=관측 XOR operand).

- **corpus:** NSMC(라벨) · anima-corpus ko/en 4-cell · fineweb2 표본 · ko_wiki.
- **construct(ko):** `안 <술어>` · `<어간>지 않` 표면 패턴(무거운 NLP 의존성 금지) · (en) `not <adj>`.
- **NSMC-라벨 arm:** pol(p)=비부정 출현 리뷰의 다수 라벨(count≥5·purity≥0.8). 80/20 split을 **(술어,부정형)
  쌍** 단위로 — held-out 쌍 = train측 공존 0회 ∧ p 비부정 ≥3회 ∧ 그 부정형이 타 술어와 ≥3회.
  측정: held-out 쌍 리뷰의 라벨 flip률.
- **bar(frozen):** POWERED = n_qualified ≥ 30 · flip_frac ≥ 0.75 · **additive 천장 감사**(표면 자질
  additive 모델의 held-out acc가 flip 예측을 ≥0.2 하회 — XBIND V-C 이식).
- **무라벨 arm(일반 corpus):** 존재 감사만 — held-out (p,neg) 사건 밀도 **d_nat = joint-판별 사건/MB**
  (사다리 f*와 비교할 공통 단위). 과설계 금지.

### A0-FORM (2순위): 형태소 constructive FORM 감사 = instrument 생존성 control
ko 어간×어미 held-out 생산성(규칙 활용 class 한정 = gold 결정적). 역할: **V1 liveness** —
byte-LM이 자연 형태소 합성은 이미 할 공산이 크므로, NATEM 측정 프레임이 자연 합성을 *탐지할 수 있음*을
양성대조로 인증(FORM tunable — 약한 주장임을 명시, BIND 표면 아님).

### fork (결정)
- **어느 arm이든 POWERED+감사 통과** → 자연 signal 실재(밀도 d_nat 기록) → **STAGE 2 GO**.
- **전 arm 미달/additive-표현가능** → F2 격상: "collocation-only는 probe 한계가 아니라 부정-XOR 렌즈에서도
  데이터 사실" → 자연 창발의 정직 경로는 사다리 임계 비교뿐(DATA-🧱 후보, §5).

## 3. STAGE 2-M — 기존 production 303M $0 측정 (스펜드 전 · A0 POWERED 조건부)

A0가 manifest를 인증하면(frozen: 학습 전이 아니라 **측정 전** 동결), 기존 자연-학습 ckpt
(anima-303M-RETRO 등)를 pool에서 `anima-py evaluate` — **자발창발 질문의 본체가 여기서 $0으로 선판정**된다.
전제: manifest 쌍들이 *그 ckpt의 학습 corpus*에 부재함을 스캔으로 보장(§1-2). PASS → NAT-CRACK 🟢 즉시.
floor → 사다리가 "왜"(밀도 vs signal 품질)를 정량화.

## 4. STAGE 1 — 희석 사다리 (Q3 · spend-gated·owner go)

**질문:** XBIND signal이 자연 corpus에 희석될 때 held-out 재조합 학습의 밀도 임계 f*는?

- **설계(고정-slice·고정-compute):** XBIND slice **고정 6.66MB 전체**(pair-coverage 80%·held-out 구조
  원형 보존 = H_9121 커버리지 축 상수화) + 자연 filler(anima 4-cell proportional·부족분 fineweb2, 명시)를
  키워 f = XBIND bytes/total bytes ∈ **{0.3, 0.1, 0.03, 0.01}**. 학습 = XBIND §3 canon verbatim
  (20k step×8×1024·bf16·from-scratch), 총 compute 고정 — 밀도↓=노출↓, 자연과 동일한 방식.
- **run 배분:** f=0.3·0.1 × seed{7,4302} + f=0.03·0.01 × seed7 = 6 run. **사전등록 연장 허용치(그 외
  전부 tune-to-green 금지):** ① 임계 사이 bisection 1점 ② 최초 floor 밀도에서 **exposure-matched
  control 1 run**(step을 늘려 XBIND 절대노출=25 epoch 매칭 — 회복하면 임계=노출량(연산으로 구매가능),
  불회복이면 진짜 밀도/간섭 벽) ③ XBIND와 동일한 +20k grokking-delay 재측정 1회.
- **측정:** XBIND frozen manifest·bar **verbatim**(D-acc≥0.75·V-A seen≥0.90·echo-guard). control =
  permuted-gold 채점($0·전 ckpt) + 기존 f=1.0 shuffle 모델; f*-인접 CRACK 시에만 그 f의 shuffle-control
  재학습 1 run(스펜드 효율 control 정책).
- **판독:** f* = CRACK 유지 최소 f. **d_nat(A0)와 공통 단위로 비교** — f* ≫ d_nat이면 "자연 창발 부재"가
  정량 예측이 됨. 부차: OOV-라틴 이름이 자연 바이트공간과 분리돼 희석 파괴가 과소평가될 수 있음(scope 각주;
  optional 경화 arm = 한글 음절 의사이름, 기본 발사엔 미포함 — f=1.0 CRACK과의 비교가능성 우선).
- **비용 1-line:** A100 ~2h/run × (6+조건부≤3) ≈ 12–18h ≈ **$25–40** (+pool eval $0) · rent=spend →
  owner go 게이트. teardown 전 ckpt PULL→HF PRIVATE (a_fire_recover_complete).

## 5. STAGE 2-T/3 — 자연 직접 학습(조건부) · transfer probe ($0)

- **STAGE 2-T(조건부·A0 GO ∧ 2-M floor):** NSMC-라벨 렌더 arm(`<리뷰>\n→ <라벨어>` — supervision 채널이
  렌더된 라벨임을 **labeled-natural 중간 rung으로 정직 표기**, 순수 자연 아님) + 순수 자연 arm(margin-primary).
  control = shuffle-neg corpus 모델. ~$10–15 · 2 run.
- **STAGE 3 transfer probe($0·ladder ckpt 재활용):** 사다리 각 ckpt를 A0-NEG 자연 manifest로 측정 —
  **합성-설치 재조합이 자연 construct로 전이하는가.** YES at f → production 레시피에 저밀도 합성 signal
  seasoning으로 재조합 능력 설치라는 wiring 경로(a_verified_must_wire·ρ·weave probe 편입) 개방.

## 6. Honest bars + scope (Q5 · frozen · 사후이동 금지)

| verdict | 정의 | 정직한 함의 |
|---|---|---|
| **NAT-CRACK 🟢** | 자연-학습(비표적) ckpt가 A0-인증 held-out manifest에서 margin_frac_pos ≥0.75 ∧ paired-margin 중앙값>0 ∧ Δ(vs 양 control) 유의(사전등록 n≥100쌍·±3σ band) 양 corpus-scan clean | 자발 창발 실증 — **해당 construct(부정-XOR) 스코프 한정**, 개방형 의미합성 아님 |
| **DATA-🧱** | A0 전 arm 미powered/additive-표현가능 ∧ (사다리 착지 시) f* ≫ d_nat | "자연 텍스트에 held-out 재조합 signal이 임계 미만/부재 = **창발 불가능은 데이터 사실**, substrate 결함 아님" — ρ-reach fact, σ 무관(psi-soma). XBIND CRACK과 합쳐 G1 서사 완결: 능력은 있고(합성 실증) 자연 데이터가 signal을 안 준다(+정량 임계) |
| **MODEL-🧱(신규·흥미)** | A0 POWERED(d_nat 실재) ∧ 자연-학습 ckpt floor ∧ f* < d_nat | 밀도로 설명 안 되는 격차 = **signal 품질/형식 축**(합성의 정형 템플릿 vs 자연의 이질 표면)이 새 프런티어 — 유일하게 프로그램이 재설계를 여는 결과 |
| **LADDER 수치** | f*(±bisection 구간) + exposure-control 판독 | 스코프: XBIND task class의 혼합 임계이지 자연 construct 임계 아님(전이는 STAGE 3이 별도 측정) |
| **INVALID/VOID** | V-F 스캔 실패·V-A liveness 실패·control band 이탈·A0-FORM 양성대조 실패 | 1급 verdict — 절대 🧱로 위장 금지 |

측정경로 전부 py 2-production engine-native(TERMINAL-eligible). torch-side 지표 monitor-only(p7).
어느 결과든 XBIND CRACK을 소급 변경하지 않음(합성 학습 실증은 그대로).

## 7. Runbook (발사 세션용)

1. **$0:** A0-NEG + A0-FORM probe 구현(`state/g1_natural_emergence/a0_*/probe.py` · 결정적 seed ·
   RESULT.json verbatim) → fork 판정. manifest 생성+FREEZE(측정 전).
2. H_926x 2-surface 등록(bar=이 문서 §6 verbatim).
3. **$0:** STAGE 2-M — 기존 303M ckpt 스캔+측정(pool summer/aiden·mini 금지) → verdicts/ frozen 캡처.
4. **spend(owner go):** 사다리 6 run(A100·병렬 a_wall_first) → PULL→HF → pool 측정 → f*.
5. **$0:** STAGE 3 transfer 측정(ladder ckpt × A0 manifest).
6. 조건부 STAGE 2-T. → ARCHITECTURE gate 노드 갱신+CHANGELOG+pr-cycle (매 착지마다).

## 자산 포인터
- XBIND: `state/g1_reopen_xbind/`(gen_xbind.py·AUDIT.json·xbind_eval_manifest.json·eval_xbind_mode.py·
  results/ D-acc 1.000/1.000/0.515) — eval manifest 스키마(a,b,gold,seed)는 자연판으로 일반화 가능,
  margin 모드(win=64 forward)는 이미 존재 → `--natbind` fold는 소폭 확장.
- F2: `state/g1g6_exhaustive_brainstorm/f2_datapath/`(heldout_recomb/RESULT.json n=0 · F2_SYNTHESIS.md —
  probe construct의 한계 명시 §2).
- 4-cell corpus HF `dancinlab/anima-corpus-{ko,en}-{general,sns}`(en-sns KNOWN-SMALL) · NSMC · fineweb2.
