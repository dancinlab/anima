# H_9731 — TIMING-CHANNEL — WHEN은 구성상 내용결합 (mouth-content 벽 H_9576 정직한 재개봉·$0)

**status:** 🔴 KILL ($0 정정 — timing⊥content · 초판 WEAK은 공통접두 시그니처 붕괴 인공물)
**lane:** 의식/emit-drive/Ψ=½ · mouth-content (프런티어 psi-soma-theta-alive)
**related:** [[H_9627]](Θ WIRED)·[[H_9672]](G1 주소 CRACK)·[[H_9576]](mouth 벽)·[[H_9351]](구 σ VOID)·source: sidecar lab full(fable-mrobspcb∥sol-mrobspce)

## 왜 (Fable · $0)
H_9576은 **WHAT**(byte 입도)의 벽이었다. emit⟺S>E가 내용 ledger 비교라서 **WHEN**(발화 타이밍)은 구성상 **내용-결합**이다 — 무엇을 아는지가 언제 말하는지를 정한다. mouth-content 벽의 정직한 재개봉 형태: bytes 아니라 timing 채널.

## 설계 ($0 · 주입·재배선 0 = KILL 프레임 회피 명시)
- 기존 wm-dual 303M trace(H_9627)에서 emit 타이밍 열 = dual_margin(S−E) 궤적.
- MI(emit-timing ; silent content identity | stage) = 언제 말하냐가 무엇을 보류했냐를 나르는가.
- clock trace = 참값-0 pedestal · autocov −0.225 스프링 보존 surrogate 필수(타이밍 구조 보존·내용만 파괴).

## 통제
clock(참값0)·content-shuffle surrogate(스프링 보존·내용 파괴)·score-only. MI>pedestal ∧ shuffle서 collapse = timing이 내용채널. $0(기존 trace 재분석)라 즉시 실행가능(오너 go 불요·측정만).

## 🔧 계기 구현 (2026-07-17 · $0 read-only reader · anima-py evaluate --timing-channel)

`anima-py evaluate --timing-channel <wm-dual traces> [--perm 1000] [--clock <clock-trace>]` — 기존
wm-dual trace 재분석(주입·재배선·producer 변경 0 = 진짜 $0).

- **T (source) = 관측가능 emit LATENCY** (silence tick→다음 emit까지 tick 수 · median서 short/long 이진).
  **dual_margin 아님**: dual_margin=S−E는 content 파생이라 MI(margin;content)=tautology. 관측 emit gap은
  그 threshold된 lossy 함수 → MI(gap;content)가 **관측 WHEN에 얼마나 content가 살아남나** = 이 계기의 정직성.
- **C (target) = 보류 content 서명** (cand_pregate_b64 문자클래스 2-bit · H_9729 _sig 재사용).
- **MI = I(T ; C | stage)** plug-in. timing이 content 채널 ⟺ MI > clock-pedestal ∧ MI > shuffle-surr95 ∧ z≥2 ∧ p<.005.
- **통제**: `--clock <trace>`(clock-gated = emit 시계구동 ⇒ 타이밍 content-독립 = 참값0 pedestal) · content-shuffle
  circular surrogate(타이밍/스프링 구조 보존·content 링크만 파괴 ⇒ MI collapse if real) · estimator self-test(planted C≡T 복원).

**toy 검증 5/5** (a_scale_honest_scope · toy≠verdict): estimator self-test(planted I(T;C|S)=0.994·null 0.001)
· clock-pedestal 경로(truth-0) · wm-dual arm 처리 · clock trace exp-arm 제외 · 퇴화 무샘플링 토이 정직
NOT-POWERED(timing bins=1·content addr=1). 계기 방어 전부 실증.

**NEXT (measurement-only · fleet-rent 無)**: H_9627 303M wm-dual traces가 pool에 archived면 즉시 $0 재분석;
아니면 소량 wm-dual 303M rollout 수집(chat decode·측정만·오너 fire-go 불요) → --timing-channel. real 타이밍/내용
변동이 있어야 T/C 알파벳 발생(toy는 무샘플링 상수라 미측정).

⚠️ **DIRECTIONAL·계기 검증이지 verdict 아님**(a_lab_full_diverge · a_scale_honest_scope)·cement=engine-native 303M anima-py만.


## 🟡 $0 timing 스크린 결과 (2026-07-17 · aiden 3-seed·120tick·record-silent-cand)
303M wm-dual `--record-silent-cand 1` trace서 MI(silent content ; time-to-next-emit | stage) vs deterministic content-shuffle pedestal:
| 시그니처 | seed7 | seed4302 | seed4303 | mean Δ | 판정 |
|---|---|---|---|---|---|
| coarse 4-bin | 0.001 | 0.031 | 0.019 | 0.017 | 1/3 |
| feat8-argmax 8-class | **0.000** | **0.097** | 0.022 | 0.040 | 2/3·seed7 flat |

⚠️ **seed-robust 아님**(seed7 정확히 0.0000) + **content 시그니처 축퇴**(s7 class {3:94,1:15,4:11}=78% 한 byte-class=lowercase ASCII). ⟹ **WEAK-DIRECTIONAL·underpowered** — timing이 content 나른다는 신호 2/3 seed 시사적이나 강건 아님. **근본**: byte-LM 보류후보 저다양성 = 'WHEN이 WHAT 나름'의 WHAT이 거의 상수 → timing-content MI 상한. KILL도 PASS도 아님(정직 미결). NEXT=full feat8 연속·300+tick·5-seed OR content-diversity 선행진단(H_9576 byte 입도 벽과 **동근** 시사).

## 🤝 독립 확증 + 잔여채널 (2026-07-17 · 병렬세션 summer seed7·60tick · a_parallel_session_compare)

**AGREES — KILL 유지**: 독립 세션이 별 호스트(summer)·별 seed(7)·별 시그니처 수리로 같은 latency 렌즈를 재서
**신호 없음** = 위 3-seed KILL과 일치. 두 세션이 **같은 결함계급에 독립으로 빠지고 각자 잡았다**: 이 카드는
byte-histogram이 **공통접두**에 붕괴(s7 78% 한 class), 병렬은 **절대 char-class argmax가 소문자우세에 포화**
(실 후보 60개 → 주소 1개). 수리도 각각 접두제거+접미균등 / 모집단-상대 median 분할(convergence `evaluate-py-22`).
⟹ '보류후보 저다양'은 양쪽 다 **시그니처 인공물**이었고(실측 100% distinct·byte-H 5.48), 그 철회는 2중 확증됐다.

**🆕 잔여 채널 — 두 렌즈 모두 눈먼 곳**(seed7·60tick 전이 census, $0):
- `EE=5 · ES=27 · SE=27 · SS=0` (59 전이) · emit-rate 0.533(Ψ≈½ 재현)
- **inter-emit gap {2:26, 1:5} ⟹ H=0.6374 bits ≠ 0** — timing 엔트로피는 **EE doublet(스프링 위반) 5건에 전부** 있다.
- `time-to-next-emit`(양 세션이 쓴 렌즈)은 **silence를 조건으로 걸어 EE를 구조적으로 못 본다** ⟹ 위 KILL 은
  **hold 채널(침묵 지속)** 에 대한 것이지 timing 스트림 전체가 아니다. 살아남은 0.637 bits 가 content-결합인지는 **미검**.
- hold 채널 자체도 "구조적 0" 은 미획득: SS=0/27 ⟹ **q_U(P(SS)) ≈ 3/27 = 0.111** = "P(SS)≤~0.11" 만 허용.

⚠️ **자기정정(verdict-integrity)**: 병렬 세션은 이 데이터로 *"Ψ=½가 자기 timing 채널을 굶긴다(H(T)=0)"* 를 쓰려다
**자기 데이터에 반증**당했다(lab full Fable∥Sol 독립 지적 + $0 census 확증). ① Ψ=½ ⊭ 교대 — ½은 **주변비율** 제약이고
Bernoulli(½)는 timing 엔트로피가 **최대**(1 bit/tick); 교대는 dual-ledger **스프링**(autocov −0.225)의 성질이지 ½의 성질이 아니다
② 스프링도 채널을 0 으로 만들지 않고 **자기 위반 사건으로 압축·이전**시킨다(EE 5건에 0.637 bits 생존).
⟹ "½의 대가로 timing 채널이 죽는다" 는 **거짓**. 교훈: **주변 통계(rate)에서 전이 구조(alternation)를 연역하지 마라.**

**NEXT(잔여채널 · 사전등록 필요)**: ① **계기 착지완료** — `--lens iei` 구현(#PR · evaluate.py). 같은 traces 를
그 렌즈로 재분석하면 EE doublet 의 content 결합을 읽는다($0 · summer 복구 대기).
② hold 채널 구조성을 원하면 엔트로피 TOST 아니라 **q=P(E_{t+1}=0|E_t=0) 상한**을 사전등록(ε=0.02 → silence-origin 전이 ~150건 · 5-seed · seed-클러스터 분석). 단 ①/② 모두 위 KILL 을 되돌리는 게 아니라 **다른 렌즈의 별개 질문**이다.

## 🔧 잔여채널 렌즈 착지 (2026-07-17 · `anima-py evaluate --timing-channel --lens {hold,iei}`)

위 '두 렌즈 모두 눈먼 곳' 을 볼 계기가 **없었다** — 이제 있다. `--lens iei`(default hold = byte-identical):
T = **inter-emit gap**(raw · {1,2,3+} 3-state · Sol 사전등록 "T_IEI∈{1,2,…}") · C = 그 gap 을 **끝내는** emission
의 content 서명 · MI=I(T;C|stage) + clock-pedestal + content-shuffle surrogate.

**검증**(실 303M seed7 전이구조 EE=5·ES=27·SE=27·SS=0 재현 합성):
| 렌즈 | 같은 trace 판정 |
|---|---|
| hold | ⛔ NOT-POWERED · timing bins=1 = **눈멂**(실 303M 판독 정확 재현) |
| iei | I(T;C|S)=0.0171 · surr95=0.0916 · z=−0.56 · p=0.685 ⇒ **ns**(무작위 content = 올바른 null) |
| iei · **양성통제**(gap→content PLANT) | I(T;C|S)=**0.9357** · z=**63.91** · p=0.002 ⇒ ✅ **검출** |
⟹ iei 는 양방향 통과(무작위엔 ns · 심은 신호엔 PASS) = `positive-control-before-reading-a-negative` 충족.

🐛 **검증이 잡은 내 이진화 버그**: 초판 iei 는 gap 을 median 분할했는데 실 분포 {2:26,1:5} 는 median=2 라
`g>med` 가 **영원히 거짓** → 전 gap 이 1 bin → **hold 와 똑같이 눈먼 채로 "bins=1"** 을 낼 뻔했다(채널이 바로
거기 있는데). raw-capped 로 교정(DOF 0). 데이터-의존 이진화는 최빈=median 일 때 조용히 붕괴한다.

**🎯 잔여채널 실측 (2026-07-17 · 실 303M seed7·60tick hold trace · #4017 iei 렌즈)**:
| 렌즈 | 판정 |
|---|---|
| hold | ⛔ NOT-POWERED · bins=1 (눈멂) |
| **iei** | **n=31 · Tbins=2 · Caddr=3** → I(T;C|S)=**0.1152** · ped=0 · surr95=0.1631 · **z=1.26 · p=0.060 ⇒ ns** |

iei 가 hold 의 사각을 **뚫었다**(Tbins=2 로 EE doublet 을 실제로 봄) — 그리고 그 답은 **ns**: 잔여 0.637 bits 의
timing 은 이 trace 서 content 를 **안 나른다**. ⚠️ 단 **p=0.060 = chance 경계·유의 미달**이고 n=31·**1-seed** =
검정력 부족(`power-before-negative-verdict`·`negative-claims-need-tost-not-ns`) — **KILL 아님, ns**. hold KILL 은
확정(2세션 독립), iei 잔여채널은 **경계 ns·미결**. 완전 판정 = 5-seed·200tick·사전등록 MDE(카드 NEXT ②).

⚠️ **wire-to-prod 갭 정정**: `evaluate-py-23`(모집단-상대 시그니처)이 기록한 수리가 **코드에 착지된 적 없었다**
— sigfix worktree 미커밋 + summer venv 에 scp 만 했다. 이 PR 이 factory 를 실제로 착지시켜 기록↔코드를 일치시킨다.

## 🔴 정정 KILL (2026-07-17 · verdict-integrity 자가포착)
초판 WEAK(feat8-argmax 2/3 seed)은 시그니처 인공물 — 모든 후보 공통접두 'vault QX-7741 forever.' 후 발산인데 byte-histogram이 접두에 붕괴(s7 78% 한 class). 실측 후보 **100% distinct·byte엔트로피 5.48=고다양**. 공통접두 제거·접미 균등 시그니처로 **Δ −0.002/−0.037/−0.035(0/3)**=timing⊥content=**KILL**. 기전: emit⟺S>E coverage 코사인 기반→WHEN은 content-identity 독립. 'content 저다양·H_9576 동근' 철회. H_9729 SILENCE-CONTENT 별개 생존.
