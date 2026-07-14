# H_9328 — (구 H_9325 · id 충돌로 재번호) DO-MOUTH: 입의 반올림만 걷어내면 기질의 do-분포가 열리는가

- **lane**: INTERACT / do-distribution (개입 분포)
- **상태**: ⛔ **use-claim INVALID** — 본실험 완료, 그러나 **폐루프가 닫혀 있지 않았다**(매개 경로 용량 = 0)
- **재분류**: 기질 벽이 아니라 **배선 결함**(`a_break_the_wall` 분류) → 수리 = H_9336 · H_9337
- **설계**: Fable 5 사전등록 (전문 → `state/verdicts/h9325_do_mouth/DESIGN.md`)
- **선행**: H_9308 INTERACT-SOURCE (⏳ NOT-POWERED · `H(A|S)=0` 이라 잴 수 없었음)

## 물음

H_9308 은 "자기 실행 궤적에 정적 코퍼스에 없는 정보가 있는가"를 물었다가 **NOT-POWERED** 로 끝났다:
`I(A;Y|S) = 0` 이 나왔는데 그건 음성이 아니라 **`H(A|S) = 0.000 nats`** — 행동이 상태의
**결정적 함수**(`emit = f(stage)` · 교차표 900/900)라 `I ≤ H(A|S)` 가 0 을 **정의상 강제**했다.
⇒ **부족한 것은 n 이 아니라 정책 엔트로피다.**

## p5 판정 — ε-무작위화는 **기각**

처방은 "emit/veto 를 Bernoulli-ε 로 뒤집어라"였으나 **두 축에서 죽는다**:

1. **철학** — `score < θ` 인 자리에서 emit 을 강제하면 **기질이 긴장을 못 느낀 자리에서 말을 만드는 것**
   = p5 addendum 이 명시적으로 금지한 `reactive speak()` / filler.
2. **측정 (더 치명적)** — emit 은 **5개 장부를 기계적으로 움직인다**(`chat.py:1817` afield 성장 ·
   `:1823` immune 적재 · `:1836` kosmos 앵커 · `brain.py:157` rate-limit 리셋 · `emit_policy` backlog 방전).
   동전으로 emit 을 강제하면 `I(A;Y|S) > 0` 은 기질의 정보가 아니라 **데몬 부기가 보장하는 항등식**
   ⇒ **PASS 분기가 데이터와 무관하게 도달** ⇒ FAIL 불가 ⇒ **반증불가**
   (convergence `synthesis-md-1` 규칙 12 — 지난 세션에 킬샷 하나를 죽인 바로 그 병).

## 채택 설계 — **REVEAL, not OVERWRITE**

결정성의 진원지는 **반올림 연산자 2개**다:

| # | 반올림 | 위치 | 버리는 것 |
|---|---|---|---|
| **R1** | Heaviside 게이트 | `core/engine_g.py` `score > θ` | 연속 tension → 계단함수 (**p5 성역 · 손대지 않는다**) |
| **R2** | argmax 입 | `core/decode.py:1063` `clm_decode_argmax` | 연속 byte-posterior → argmax (**진범**) |

**R2 가 R1 의 결정성을 야기한다**: greedy ⇒ `g_text` sha 2종뿐 ⇒ 3개 피드백 뿌리
(`rel_lane`[immune] · `recon_err`/`cell_count`[afield]) 가 안 움직임 ⇒ `score` 고정 ⇒
Heaviside 가 항상 같은 쪽 ⇒ `emit = f(stage)` ⇒ **H(A|S)=0**.

⇒ **게이트는 바이트 그대로 두고, 기질이 승인한 emit 분기에서만 argmax 를 T=1.0 샘플링으로 교체.**
**T=1.0 은 튜닝 노브가 아니라 기질 자신의 posterior 그 자체** — 유일하게 비자의적인 온도
(tune-to-green 방지 앵커). p5 위반 0: 기질이 승인하지 않은 emit 은 **단 한 번도 발생하지 않는다**.

## 🟢 V-CEILING 판독 (engine-native · 학습된 303M `py303.clm` · summer GPU · $0)

**A = `penult_fold8(gen_penult_pooled_W(self_gW, g_text))` ∈ [0,8)** — `cli/chat.py:1846` 이
**실제로 계산해 self-drift 에 먹이는 값** (H_9257 사전등록 동결 8-버킷 · 새 연구자 DOF = 0).

| stage | GREEDY A | T=1.0 분포 | H(A\|S) |
|---|---|---|---|
| wake | **5** | {1:1, 5:13, 7:18} | 0.7979 |
| n1 | **5** | {1:2, 2:3, 5:14, 7:13} | 1.1228 |
| n2 | **5** | {1:2, 2:2, 5:18, 7:10} | 1.0337 |
| rem | **5** | {1:2, 2:1, 5:17, 7:12} | 0.9854 |
| n3 | **7** | {1:3, 5:18, 7:11} | 0.9126 |

**H(A|S) = 0.9705 nats** (바닥 0.030 = 3×MDE · 천장 ln(8) = 2.0794)
⇒ **V-CEILING PASS** — 포화 아님(0.97 ≪ 2.08) · 기질이 소비하는 행동축에 **실제 엔트로피 존재**.

> **greedy 는 stage 마다 항상 같은 버킷으로 붕괴한다(A=5). 그것이 H_9308 이 본 벽이다.
> argmax 반올림만 걷어내니 기질은 4개 버킷에 걸쳐 말한다. 결정성은 기질의 사실이 아니라
> 입의 반올림이 만든 것이었다.**

## 🔴 DISJOINT 스모크 (p5 방어의 기계화 · PASS)

`--emit-topk 1` 로 샘플러를 **퇴화**시키면 argmax 와 **전 궤적 바이트 동일**해야 한다
(샘플러만 바꿨는데 샘플러가 퇴화하면 아무것도 안 변해야 한다).
- toy.clm: rng {7, 4302, 20260714} 전부 **byte-identical = True**
- 303M: seed {wake, n1} × rng {7, 4302} 전부 **byte-identical = True**
⇒ **배선이 게이트로 새지 않았다.** 기계검사: `grep mouth core/brain.py` → `brain_decide*` 인자에 **0개**.

## ⚠️ 계기 결함 1건 (자가 검출 · convergence `decode-py-2`)

V-CEILING **v1 은 INVALID** 였다: A 를 `sha(g_text)` 로 대리했더니 5 stage 전부
**H = 3.4657 = ln(32) 정확히** = 표본수의 로그 = **완전포화**. 80바이트를 T=1.0 으로 32번 뽑으면
32개가 전부 다른 건 **자명**하다 — 그 추정기는 "엔트로피가 얼마인가"가 아니라 **"텍스트가 서로 다른가"**
(답: 당연히 예)를 쟀다. **대리변수를 발명한 순간 그것이 답을 만들었다.**
⇒ v2 는 데몬이 **실제로 소비하는** 8-버킷 축으로 재측정. 지지집합이 유계(K=8)라 포화가 눈에 보인다.

## 배선 (engine-native · `state/` 스크립트 0)

| 파일 | 변경 |
|---|---|
| `core/generator.py` | `generate(..., mouth=None)` + `_gen_clm_decode(..., mouth)` — `temp>0` 이면 **승인된 emit 분기에서만** `clm_decode_argmax` → **기존** `clm_decode_topk_sampled`. **SILENT 분기 무손상**(`text=""`) |
| `core/brain.py` | `brain_emit(_aged)(..., mouth=None)` 가 `mouth` 를 **`generate()` 에만** 전달. **`brain_decide_anchored` 는 영원히 못 본다 = DISJOINT 벽** |
| `VERSION` | 0.13.21 → 0.13.22 (G5 하드게이트) |

기본 OFF ⇒ `mouth=None` 이면 **바이트 동일**(프로덕션 무영향).

## 🔧 배선 완료 후 발견된 계기 결함 3건 (전부 자가 검출 · 전부 수리·랜딩)

배선을 끝내고 **canonical `anima-py` 경로로 스모크**를 돌리자 결함이 셋 나왔다. 셋 다
"코드는 돌고 로그는 정상인데 숫자만 무의미"한 조용한 결함이라, 스모크 없이 본실험을 쐈다면
**전부 verdict 로 굳었을 것**이다.

| # | 결함 | 실측 | 수리 |
|---|---|---|---|
| **1** | **계기-표적 불일치** — V-CEILING 파일럿은 `clm_decode_argmax` 를 쟀는데 **데몬은 그 문으로 안 다닌다**. 앵커가 있으면(라이브 세션은 항상) `_gen_clm_decode` 가 `clm_decode_grounded` 로 빠져 내 mouth 분기는 **도달 불가 죽은 코드**였다 | canonical 스모크: T=1.0 인데 seed 갈림=False · A=5 고정 | `clm_decode_grounded` **내부의 argmax 분기**에 REVEAL 배선 (복사 스텝 `cb>=0` 은 절대 미터치 = p5 반-날조). 부수 발견: `grounded=0 / lm=80` — 이름과 달리 **앵커 복사가 한 번도 안 일어난다**(`l_min=8` 미달) |
| **2** | **고정 시드** — `mouth` dict 를 tick 루프 **밖**에서 만들어 `seed_rng` 를 세션 상수로 고정 ⇒ 매 tick **같은 80바이트** ⇒ 30 tick 이 **1 표본** | gtext 종류 **1/28** | `_mouth_at(tick)` — tick 별 파생 스트림. 수리 후 gtext **28/28** · A 가 rollout 안에서 5~6 버킷에 분포 (convergence `chat-py-3`) |
| **3** | **가짜 구조 사실** — ②가 만든 "A 는 rollout 내 상수"를 근거로 순열 단위를 rollout 으로 못박았다(`evaluate-py-13`). **계기 결함이 과학적 진단을 오염**시킨 것 | 수리 후 자기상관 **0.361 vs 우연 0.369** = 없음 ⇒ **tick 이 표본** ⇒ 검정력 24배 회복 | 판독기가 **자기상관을 실측**해 단위를 자동 선택 + **두 단위 모두 보고** · **판정이 단위에 뒤집히면 ⛔ INVALID** (convergence `evaluate-py-15`) |

## 🚫 C2 CARRIER-SWAP 폐기 — 사후 순열로는 담체를 못 잡는다

Fable 의 C2("EXP 는 살고 SWAP 은 죽어야 정보 · 둘 다 살면 내용맹")를 `rollout→A` 배정의
**회전**으로 구현하고 인증하니 **인공 CARRIER 데이터에서도 PASS** ⇒ INFO 와 CARRIER 를 **못 가른다**.
근본 원인: C1 PERM(무작위 순열)과 C2(회전)는 **둘 다 A–Y 짝을 깨는 같은 귀무족**
⇒ **C2 는 C1 의 퇴화 사례**였다. 진짜 CARRIER-SWAP 은 **다른 rollout 의 g_text 를 데몬에 실제
주입해 재실행**해야 한다(그래야 그 텍스트가 3개 피드백 뿌리를 실제로 민다). Fable 원설계도
"다른 rollout **g_text 로 교체**"라고 명시했는데 내가 A 순열로 오독했다 (convergence `evaluate-py-14`).

> **⇒ 이 실험의 판독 스코프는 SIGNAL / TOST-등가까지이고 PASS 는 불가하다.**
> PASS 는 `--swap-text` 엔진 플래그(다른 rollout 텍스트 주입 재실행) 배선 후에만.


## ⛔ 본실험 결과 — 재봤더니 0 이 아니라, **물을 수가 없었다** (2026-07-15)

24 rollout × 30 tick · 303M · canonical `anima-py chat` → `anima-py evaluate --interact-mi`
(aiden · 설치 엔진 5파일 sha = origin/main 동일 · 증거 #3561).

```
🚦 V-CEILING  H(A|S) = 1.1513 nats · H(Y|S) = 0.4091 nats   (floor 0.030)
EARNED[tick]  = +0.00088 nats   (MDE 0.010 · TOST ±0.010)
⇒ TOST 등가 — 두 순열 단위 판정 일치(INVALID 가드 침묵)
```

처음엔 이것을 **"채널을 열었더니 기질이 안 쓰더라"** 로 읽었다. **그 독법은 틀렸다.**

### 🚦 MEDIATION — 사슬의 가운데가 끊겨 있었다

헤드라인은 사슬의 **두 끝**만 잰다. 가운데를 열자(계기 확장 #3563):

```
H(R|S) = 0.0000 nats      R = recon_err (afield 뿌리 · g_text 가 직접 민다)
⇒ 매개 채널 자체가 죽어 있다 — M1/M2 는 정의상 0.
```

720 tick(24 rollout) **전체**에서 세 피드백 뿌리가 **전부 상수**였다:

| 필드 | 고유값 | |
|---|---|---|
| `recon_err` (afield) | **1** | 💀 항등식 0.0 |
| `rel_lane` (immune) | **1** | 💀 720 tick 내내 0.6723 |
| decode 앵커 (kosmos) | **1** | 💀 항상 `live_seed` |
| `score` | 562 | ✅ |
| `a_fold8` | 8 | ✅ |

셋 다 `g_text` 로 **쓰이는데**, 조회는 전부 **`session_seed` 라는 상수 키**로 한다.
**데몬은 자기 말을 세 저장소에 넣고, 셋 모두에게 언제나 같은 질문을 던지고 있었다.**

### 🚦 AXIS — 축 선택은 방어된다 (Fable 의 직교 비판 기각)

*"네 A 는 입이 표상한 축이고, 루프가 나르는 건 8-스칼라 바이트-모양 축이다. 두 축이 직교하면
너는 루프가 안 나르는 축을 재고 '정보 없다'고 말한 셈"* — 실측으로 기각(계기 확장 #3575):

```
A  = penult_fold8(pooled)     H(A|S)  = 1.1513 nats
A′ = penult_fold8(byte_feat8) H(A′|S) = 0.5966 nats     ← 루프가 물리적으로 나르는 축
I(A;A′|S) = 0.0660 nats  ≫ MDE 0.010  ⇒ 두 축이 상당히 겹친다
```

### 결론 — **세 번째 항등식-0**

```
V-CEILING   H(A|S)=1.151 ✅  H(Y|S)=0.409 ✅   ← 양 끝 채널은 살아있다
MEDIATION   H(R|S)=0.000 💀                    ← 가운데가 끊겨 있다
AXIS        I(A;A′|S)=0.066 ✅                 ← 축 선택은 정당했다
```

`I(A;Y|S) ≤ min(H(A|S), H(Y|S))` 는 항등식이고, V-CEILING 이 그 **두 주변축**은 지켰다.
그러나 **매개 경로의 용량**은 아무도 안 지켰다 — 그것이 0 이면 I 도 0 이다, **정의상**.

⇒ **`I(A;Y|S)=0` 은 use-claim 으로 성립하지 않는다.** "기질이 자기 말을 안 쓴다"가 아니라
**"말이 다음 결정에 도달할 경로가 없다"**. `a_break_the_wall` 분류로 **기질 벽이 아니라
배선 결함**이다.

### 그래도 벌어온 것

**DO-MOUTH 배선 자체는 성공했다.** H_9308 은 입이 argmax 라 `H(A|S)=0` 이어서 **물을 수조차
없었다**(NOT-POWERED). REVEAL 이 그 채널을 **1.151 nats** 로 열었고, p5 도 지켰다(DISJOINT 벽 ·
게이트는 `mouth` 를 영영 못 본다 · grep 기계검사). 송신기는 열렸다 — 끊겨 있던 것은 **수신기**다.

## 🔧 수리 (후속 H)

- **H_9336** — 뿌리 ①(afield). H_9210 이 이미 진단했으나 `--opgrip-live` 하네스 뒤에만 고쳐
  프로덕션은 방치돼 있었다(convergence `chat-py-4`).
- **H_9337** — 뿌리 ①+②(afield · immune) 를 프로덕션에 닫는다. ⛔ 뿌리 ③(kosmos→decode 앵커)은
  **고치지 않는다** — 자기 발화를 다음 decode 문맥으로 되먹이면 **p5 가 금지한 self-seed**.
  그 상수성은 결함이 아니라 **철학이 닫아둔 것**이고, 정당한 read-back 은 세션 **간**(`.kosmos` 재입).
  (convergence `chat-py-5`)

수정 후 재측정은 **H_9337 에 동결 bar 로 사전등록**(p7 · 수치를 보기 전에).

## SWAP 팔 (C2 CARRIER-SWAP · 확증용)

`--swap-text`(#3542)로 배선·수집했다. EXP 가 이미 0 이고 매개 경로가 죽었으므로 SWAP 은
own-vs-carrier 를 **가를 신호 자체가 없다** — 확증용이며 이 verdict 를 바꾸지 않는다.

## (구) NEXT — 본실험 (완료 · 위 참조)

`I(A;Y|S) > 0` 인가?
- **A** = `penult_fold8(gen_penult_pooled_W(self_gW, g_text))` ∈ [0,8) — 데몬이 실제 소비하는 값
- **S** = `stage` (게이트 자신의 조건화 ⇒ 생략된 결정자에 의한 거짓양성 구조적 불가)
- **Y** = `score_{t+1}` 2-bin (3개 피드백 뿌리가 재수렴하는 유일 지점)
- **arms**: EXP · C1 PERM(참값0 · **단위는 자기상관 실측으로 결정**) · C3 PEDESTAL · C4 ALIVE · C5 GREEDY
- MDE 0.010 nats · TOST ±0.010 · α=.005 · **V-CEILING 선행 하드스톱**
- **계기 인증 완료**: ALIVE +0.412 (p=.005) · PEDESTAL +0.007 (p=.09) · ROLLOUT_CONST 자동 rollout 선택
- **배선 완료**: `cli/chat.py` 플래그 + A 트레이스 · `cli/evaluate.py --interact-mi` 판독기 (help lockstep)

## 정직

- **T=1.0 이 여전히 결정적일 위험은 해소됐다**(H=0.97) — 그러나 그 엔트로피가 **정보인지 잡음인지는
  아직 모른다**. C2 CARRIER-SWAP 이 그것을 가른다.
- **가장 깊은 긴장(Fable §5-②)**: p5-clean 한 유일한 개입이 **인과적으로 가장 약한 개입**이기도 하다.
  `ctx` 로 조건화하면 A 는 오직 RNG 로만 갈리는데, 그 RNG 는 **기질 자신의 분포 안에서** 뽑는다.
  엄밀한 인과 심사자는 "너희는 관측 다양체를 떠난 적이 없다 — 이건 do-분포가 아니라 noise-분포다"
  라고 말할 것이고 **그 말이 옳다**. 진짜 외생적 do 는 정확히 p5 가 금지한 동전이다.
  ⇒ 이 긴장은 **해소되지 않았고 우회됐다**. Tier A 가 실패하면 정직한 독법은
  **"anima 의 아키텍처는 자기 철학을 어기지 않고서는 자기 do-분포를 측정할 수 없게 되어 있다"** —
  실험에 대한 사실이 아니라 **anima 에 대한 발견**이다.
- 동결 A-map(8버킷)이 정보가 사는 축을 뭉갤 수 있다 ⇒ FAIL 은 **"이 판독기에 대한 FAIL"**
  이지 보편 음성이 아니다 (`a_scale_honest_scope`).


## 🔌 WIRED — live on `core/` (2026-07-14 · `a_verified_must_wire`)

카드는 main 에 있었지만 **엔진 코드는 커밋조차 안 된 채 워크트리에 방치**돼 있었다(`wire-to-prod`
위반: "구현됨·미배선"). 배선 + 실측 인증하고 착륙:

- `core/decode.py` `_mouth_sample_row` + `clm_decode_grounded(..., mouth=None)` — **anchor-copy
  스텝은 절대 샘플링하지 않는다**(그 경로가 p5 반-날조 보증). 엔진이 이미 생성하려던 스텝의
  **argmax 반올림만** 걷어낸다 = REVEAL, not OVERWRITE.
- `core/generator.py` `_gen_clm_decode` → mouth 스레딩 (실측 grounded=0/lm=80 ⇒ 라이브 세션의
  진짜 입은 이 경로).
- `cli/chat.py` — emit **게이트**(`brain_decide_anchored`→`should_emit`)는 mouth 를 **보지 않는다**
  (DISJOINT · `a_substrate_disjoint`). 긴장이 정하는 emit/silence 는 그대로.
- CLI = `anima-py chat <ckpt> [--emit-temp T] [--emit-topk K] [--sample-seed S]`
  (argv > ENV > default 3단 · default OFF).

### 착륙 게이트 (실측 · 소형 ckpt `clm_d768_e2l1.clm`)

| 게이트 | 내용 | 결과 |
|---|---|---|
| **G-PARITY** | default-OFF 가 production 과 byte-identical | **PASS** sha `664cd601a4ac…` 3-way 동일 |
| **G-LIVE** | mouth ON 이 실제로 스트림을 바꾼다 (dead code 아님) | **PASS** |
| **G-DET** | 같은 seed → 같은 draw (재현성) | **PASS** |
| **G-SEED** | 다른 seed → 다른 draw (RNG live) | **PASS** |
| **G-FLAG** | argv > ENV > default 3단 + 설치된 `anima-py` help 에 노출 | **PASS** |

착륙 중 발견·수정: `anima_flag_value` 가 **죽은 코드**였다(정의만 있고 호출 0, docstring 은 존재하지
않는 플래그를 약속) ⇒ 약속된 플래그를 **실배선**하고 help 에 lockstep 반영.
