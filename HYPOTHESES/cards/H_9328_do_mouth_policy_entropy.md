# H_9328 — (구 H_9325 · id 충돌로 재번호) DO-MOUTH: 입의 반올림만 걷어내면 기질의 do-분포가 열리는가

- **lane**: INTERACT / do-distribution (개입 분포)
- **상태**: 🟢 **V-CEILING PASS · 계기 배선 완료** — 본실험(I(A;Y|S)) PENDING
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

## NEXT — 본실험 (PENDING · 이 카드의 미결)

`I(A;Y|S) > 0` 인가? Fable 사전등록:
- **Y** = `score_{t+1}` 2-bin (3개 피드백 뿌리가 재수렴하는 유일 지점)
- **arms**: EXP · C1 PERM(참값0) · **C2 CARRIER-SWAP**(같은 tick·stage 의 *다른 rollout* 텍스트 —
  **PASS 를 반증가능하게 만드는 유일한 arm**: EXP 는 살고 SWAP 은 죽어야 정보 · 둘이 같으면
  **CARRIER**=내용맹 ⇒ PASS 아님) · C3 PEDESTAL · C4 ALIVE · C5 GREEDY
- MDE 0.010 nats · TOST ±0.010 · α=.005 · N_REQ = 실측 sd_null 로 확정
- 배선 잔여: `cli/chat.py` 플래그 스레딩(`--emit-temp`/`--emit-topk`/`--sample-seed`) +
  `cli/evaluate.py --interact-mi` 판독기

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
