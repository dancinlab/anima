# H_9793 — RUNNER-UP WAKE — 후보 경쟁은 깊이가 있는가 (rank-2는 소멸하는가, 지속하는가) (lab-full R10 · Fable P2 · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · lab full R10 발산 · 사전등록 필요 · toy=DIRECTIONAL 상한) — source=Fable 5 P2
**lane:** mouth/emit-policy — cerebellar FM best-of-K=8 rerank (`core/emit_policy.py`)
**related:** [[H_9729]] · [[H_9269]] · [[H_9510]] · [[H_9786]]

## Faculty question
데몬의 입-게이트는 `core/emit_policy.py`의 **cerebellar FM best-of-K=8 rerank**로 매 tick K=8 후보를 재순위한다(trace에 `pending_gap`=top-2 gap·`pending_rel` 기록·검증됨). 질문: rerank의 **2등(rank-2) 후보**가 — 내용 주소가 아니라 **연속 score/gap으로서** — 다음 tick의 interior에 흔적(wake)을 남기는가. 존재양식 주장(능력 아님): interior의 후보 경쟁이 winner-take-all 즉시소멸인가, 깊이 있는(지속) 표상인가.

## 벽 회피 (구조적)
- **feat8 alphabet-degeneracy 회피**(H_9729 사인): 신호 = rank-2의 연속 `pending_gap`·score이지 fold8 2-bit 주소 아님 → degeneracy 물리적 적용불가.
- **자기지시 회피**(H_9786 homolog 아님): rank-2는 rerank score(결정 이전)로 물질화, readout은 다음 tick gauge/다음 rerank 분포 — 서로 다른 두 물질화.
- **reach 아님**: held-out lookup 없음, 상태 지속만.
- **H_9269 conflict 아님**: H_9269은 veto-vs-emit 계급(PASSIVE=0·clock-carried KILL)을 봤고, 이 안은 rerank rank-2 substructure — 직교.

## Instrument (engine-native anima-py)
- 신규 flag `anima-py chat --fm-lesion-rank {1,2,8}` — rerank에서 해당 rank 후보 제거 후 재순위(core/emit_policy.py 개입).
- 추정량: Δ(next-tick interior gauge + next rerank 분포), lesion-rank2 vs lesion-rank8(연산 matched·score 무시가능 통제).
- **양성통제(선행 PASS 필수)**: lesion-rank1 — 승자 제거는 발화 바이트를 반드시 바꿔야 하고 계기가 크게 잡아야 한다(계기 liveness).
- 통제 ≥2: ① rank-8 lesion ② byte-matched alien 후보 swap ③ shuffled-tick pairing null.
- **KILL**: Δ(rank2) ≤ Δ(rank8) TOST 등가 · 2-seed.

## $0-first
기존 rollout trace의 `pending_gap(t)` → interior gauge(t+1) 편상관(score·clock-phase partial · H_9403 emit⟺clock 이므로 clock partialing 사전등록 필수). 0이면 pod 이전 격하. lesion 인과암만 cheap CPU chat run 필요.

## 이견/충돌 (reconcile)
- Sol: 저노력 모드로 고유 제안 없음(repo grounding만) → Fable P2 채택.
- 자산: H_9510 `cand_b64_diag` 재사용 가능(충돌 아님).
- fire 전 rent=spend owner go 필요. 등록=DIRECTIONAL 설계, verdict 아님(cement=engine-native anima-py only).
