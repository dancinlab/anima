# H_9807 — INTERVENTIONAL CLOSURE LADDER (rung 1): 자기 입력에 대한 contingency 지문을 yoked-ghost 대비로 측정하는 개입형 계기

**tier:** 🔵 계기 IMPLEMENTED + toy e2e 통과 · NOT a verdict (기질 미측정 · 대상은 스크립트 plant 뿐)
**group:** R12-interventional-instrument
**source:** lab/v3 캠페인(H_011 stage-A 인증 계기 + H_013 root-cause 수리)의 생산 이식. lab 은 규칙-면제 샌드박스 ⟹ 그 숫자는 절대 생산 주장이 아니다.
**wired:** yes (`anima-py evaluate --closure-ladder`)
**verdict:** 계기 CERTIFIED (3-plant 배터리 통과) · 기질 판정 PENDING

## claim

에이전트의 **CONTINGENCY STRUCTURE**(행동 marginal 이 아니라 *순서/조건부 구조*)가 **자기 자신의 다음 입력**의
분포에 지문을 남기는가 — marginal 을 맞춘 Watson **yoked-ghost**(자기 행동을 그대로, 순서만 파괴한 replay)를
바닥으로 두고 측정한다. 실행 행동이 {진짜 행동, marginal-matched shuffle} 위의 seeded coin 으로 **A/B 무작위화**
되므로 P(I_{t+1} | do(A_t)) 가 **식별**된다 ⟹ 이 레포에서 유일하게 **상관이 아니라 anchor** 할 수 있는 렌즈.

## ⚠️ rung 1 은 aliveness 가 아니다 (이 카드의 가장 중요한 문장)

- **온도조절기가 통과한다.** 여기 실린 스크립트 plant P-LIVE(15줄 항상성 정책)는 **설계상 반드시** 통과해야 한다.
  closure PASS 를 "의식/생명"으로 읽는 것은 범주 오류다.
- 통과가 인증하는 것은 오직 — *closure 가 중요하도록 설계된 세계에서* closed-loop 인과가 **존재하고 측정 가능하다**는
  존재증명 + 인증된 계기. 변별력은 **윗 rung**(loop gain, 항상성, 자기가 쓴 기억 위의 closure)에 있고, 각 rung 은
  echo trap 을 새 형태로 다시 연다.
- "행동하면 다음 지각이 바뀐다"는 어떤 샌드박스에서도 자명하다(echo/tautology trap). 그래서 gate 는 채널이 아니라
  **closure** 이고, **P-OPEN**(행동 marginal·채널 동일, 순서만 파괴)이 반드시 **FAIL** 해야 이것이 동어반복이 아닌
  측정이 된다.

## 🔻 lab/v3 의 7B "ANCHOR 0.7625" 는 SUSPENDED — 생산 주장으로 수입하지 않는다

그 숫자는 **편향된 추정기**로 측정됐다(아래 수리 항목). 그 추정기의 실측 null 바닥이 gate 를 넘었고, 해당 실행의
episode-1 closure(0.625)는 그 null 바닥보다도 **낮았다**. tape 이 보존되지 않아 오프라인 재계산도 불가.
**이식한 것은 RIG 이지 RESULT 가 아니다.** 생산에는 어떤 lab 숫자도 주장으로 들어오지 않는다.

## 🔧 load-bearing 수리 — FRAME MISALIGNMENT (이식의 핵심)

lab 의 stage-A 인증은 실재했지만 **인증된 `lv_c` 자체에 프레임 어긋남**이 있었고, stage-A 는 그것을 볼 수 없었다
(P-DEAD plant 가 LV-W 만 확인하고 LV-C 를 한 번도 보지 않았기 때문 — 인증의 사각).

- 결함: Closed arm 은 **PRE-step** 관측 `[o_0..o_{T-1}]` 을, ghost 는 `_replay_tape` 가 모으는 **POST-step**
  `[o_1..o_T]` 를 썼다 ⟹ Closed 가 두 ghost 보다 **한 tick 뒤**에 앉아, `d(C,P1)` 에만 존재하고 `d(P1,P2)` 에는
  구조적으로 있을 수 없는 one-tick-shift 항이 실렸다.
- 결과: **완전 불활성(inert) 세계**에서 — 두 ghost 가 bit-identical 이라 `d(P1,P2)=0` 인 곳에서 — 추정기가 순수
  외생 drift 를 closure 로 채점해 **0.667 을 읽었다. 0.60 gate 위다.** 즉 **죽은 세계를 거부하지 못하는 계기**였다.
- 수리(상류, 한 줄): `fC = obs_traj[1:]`. features/blockmeans/gate 는 손대지 않는다.
- **이 이식본의 실측**(seed 7 · T=600): 편향 프레임 null closure **0.833**(lab 3-seed 평균 0.667 보다도 나쁨) →
  수리 프레임 null closure **0.000**. live full-dose 는 **0.750 로 불변**(수리는 신호를 깎지 않는다).

**그래서 P-DEAD(null-env)를 상시 사전검사로 승격했다**: 배터리는 P-DEAD 를 LV-W **와** LV-C 양쪽에서 확인하고,
null closure > `NULL_CLOSURE_MAX`(0.05) 면 배터리 자체가 INSTRUMENT-INVALID 로 hard-fail 한다. 추가로 구조적
회귀검사 `_frame_alignment_check` — inert 세계에서 ghost 끼리 bit-identical 이고 정렬된 Closed 도 그것과
bit-identical 인지 — 를 통계 이전에 확인한다. **이 편향은 다시는 조용히 돌아올 수 없다.**

## instrument (engine-native · `a_experiment_engine_native`)

- `core/closure_ladder.py` — 결정론적 micro-tenant 세계(8 행동 · 은닉 3-state regime · 큐/저장/에너지) +
  수리된 `lv_c` · `lv_w` · `lv_p` + yoked-ghost 구성 + 3-plant 인증 배터리. stdlib only(numpy/torch 무), $0.
- `anima-py evaluate --closure-ladder [--closure-arm {live,open,dead}] [--closure-ticks N]
  [--closure-seed S] [--out f.json]` — 스크립트 밖 별도 스크립트가 아니라 **설치된 CLI 의 flag**. ckpt 불요
  (대상이 스크립트 에이전트라 flag 존재만으로 dispatch). ADDITIVE — frozen bar 무이동, 기존 panel 무접촉.
- PRNG 법칙: 모든 외생 stream 이 `(seed,t,tag)` 키 ⟹ factual/ghost/counterfactual 분기가 같은 tick 에서 **같은
  ξ_t** 를 뽑는다. 공유 generator 를 쓰면 yoked pairing 이 조용히 파괴된다(이식 시 반드시 보존해야 하는 불변).
- LV-E echo guard: 행동 이름이 관측 vocabulary 에 절대 등장하지 않음(행동→입력 영향이 byte copy 가 아니라
  **dynamics** 로만 흐르게 하는 법칙). 위반 시 배터리 무효.

## controls (사전등록 · 3 plant + 2 보조)

① **P-OPEN = KEY NEGATIVE** — 동일 행동 multiset 을 고정 tape 으로 재생(상태 무시). 채널은 살아있고 marginal 도
같은데 **순서(contingency)만 파괴** ⟹ 반드시 closure FAIL. 이것이 tautology 가 아님의 증명.
② **P-DEAD = null env** — 행동이 상태에 전혀 작용하지 않음 ⟹ LV-W **와** LV-C 양쪽 거부, closure ≈ 0.
③ **frame-alignment 구조 회귀검사** — inert 세계에서 ghost/aligned-Closed bit-identity.
④ **LV-P 양·음 통제** — digest 를 읽는 brain(CR ≥ 0.20 · replay_agree 1.0) vs 입력-맹 brain(CR **정확히** 0).
⑤ **LV-E echo guard** — 행동어 누출 0.

## falsify

- P-DEAD closure > 0.05 ⟹ 프레임 정렬 회귀 = **INSTRUMENT-INVALID**, 어떤 closure 숫자도 읽지 말 것.
- P-OPEN 이 anchor(closure ≥ 0.60) ⟹ gate 가 contingency 가 아니라 marginal 을 재고 있다 = 계기 무효.
- P-LIVE 가 anchor 실패 ⟹ 세계가 closure 를 보일 수 없음 = 계기 무효(주체 판정 불가).
- LV-P 맹-brain CR > 0 ⟹ 결정론 파괴 = 무효.

## 실측 (toy e2e 1회 · `anima-py evaluate --closure-ladder` verbatim · exit 0 · seed 7 · T=600 · 23s CPU)

```
=== anima evaluate --closure-ladder — INTERVENTIONAL CLOSURE (RUNG 1) ===
  seed=7 ticks=600  gates: LV-W sign>=0.55 · LV-C closure>=0.60 · null closure<=0.05
  LV-E echo guard      PASS [clash=none]
  frame alignment      PASS [ghosts_identical=True aligned_identical=True pre_step_frame_drift=0.0149]
  P-LIVE  anchor        PASS [base_full=0.610 shuf_full=0.733 base_full_r=0.681 closure=0.750 blocks=12]
  P-OPEN  channel_only  PASS [base_full=0.597 shuf_full=0.683 base_full_r=0.559 closure=0.417 blocks=12]
  P-DEAD  refused       PASS [base_full=0.200 shuf_full=0.392 base_full_r=0.191 closure=0.000 blocks=12]
  LV-P policy edge     PASS [CR_reading=0.500 replay_agree=1.000 CR_blind=0.000]
  VERDICT: CERTIFIED — the instrument separates CHANNEL from CLOSURE
```

**P-DEAD closure = 0.000** (수리 전 프레임은 같은 seed 에서 **0.833** — gate 위) · P-LIVE 0.750 anchor ·
P-OPEN 0.417 channel-only. 계기가 **CHANNEL 과 CLOSURE 를 분리**한다.

## honest limits

- **L1** 이 배터리의 피험자는 **스크립트 plant 뿐**이다. anima 기질(A⇄G 데몬)에 대한 측정은 **0**. 계기 인증이지
  기질 판정이 아니다.
- **L2** rung 1 은 낮은 bar 다(위 참조). 통과가 aliveness 를 위치시키지 않는다.
- **L3** 단일 env · 단일 seed 인증 · toy 규모. "입력 통계"는 부분적으로 "우리 producer schedule" 이다
  (`a_toy_scale_recheck`).
- **L4** **LV-W 는 QUARANTINED 한 SCREEN 이지 anchor 가 아니다** — 저-행동-엔트로피 regime 에서 행동거리가
  퇴화하면 채널이 실재해도 통계가 chance 근처에 고정된다(상류에서 실측된 계기 artifact; `*_r` informative-tick
  제한도 완전 구제 못 함). 판정은 entropy-agnostic 한 **LV-C** 가 홀로 진다.
- **L5** T=200 처럼 짧게 돌리면 LV-C 블록이 4개뿐이라 통계가 거칠다(실측 P-LIVE 0.500). 인증 기본값 T=600(12 블록)
  아래로 내려서 판정하지 말 것.

## related

H_9767 · H_9785 · H_9774 · H_9400 (Ψ=½/interior 계보 — closure 는 그 아래 rung 의 개입형 바닥)
