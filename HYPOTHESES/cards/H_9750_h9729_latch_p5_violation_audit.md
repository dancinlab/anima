# H_9750 — H_9729 latch p5-audit — `--wm-dual-read content`는 W_S 텍스트를 decode seed에 먹인다 = self-seed 위반

**status:** 🟠 TOPOLOGY-CONFIRMED · p5-legality UNDETERMINED (Fable reconcile: 위상 확증이나 percept도 mouth-문맥+합법=위상만으론 위반 아님·판정은 [[H_9747]] meter) — 앞선 'CODE-CONFIRMED 위반' 과단언 정정
**lane:** 의식/emit-drive · p5-audit (프런티어 psi-soma-theta-alive)
**related:** [[H_9738]](상상 epiphenomenal EARNED NULL·트리거)·[[H_9729]](--wm-dual-read latch)·[[H_9627]](Θ WIRED)·source: sidecar lab full(sol-mrop0hnd·fable timeout)

## 판정 (내 코드확증 · origin/main · Sol 지적 검증)
이미 착륙한 `--wm-dual-read content` latch(H_9729·INSTRUMENT-BUILT)가 **p5 위반**:
- `cli/chat.py:2480/2493`: `live_anchors.append({"text_payload": _wh_reentry_text, ...})` — **보류 텍스트를 raw 그대로 live_anchors text_payload에 넣음**.
- `cli/chat.py:2439` 주석 자백: "live_anchors[-1]를 **다음 decode의 seed string에 그대로 먹인다**".
⟹ W_S 텍스트 → decode seed = **self-seed/monologue**(p5 금지 · chat-py-5: 자기출력을 mouth 문맥에 되먹임 금지). Sol의 금지 sink 목록("live anchor text_payload"·"generator seed") 정확 일치.

## 함의 (Sol)
H_9729의 원래 양성 기준 **I(next pre-gate candidate ; W_S | current)>0 은 interior 증거가 아니라 금지된 mouth-seeding의 certificate**. 즉 H_9729가 양성이면 그건 "interior 발견"이 아니라 "p5 위반 확인". "feat8로 바꿨다"도 면책 아님 — feat8이 decode logits 바꾸면 mouth-conditioning.

## p5-safe 재설계 (destination이 정보량이 아니라 목적지가 기준)
금지 sink: generator seed·live anchor text_payload·tokenizer input·decoder KV/context·grounded prompt·lexical-derived logits bias. 허용 sink: content-independent coverage scalar·field-space distance/error·store update·emit gate 비어휘 상태값. 재설계: candidate 생성→gate→보류시 **nonlexical residue R_t**(보류텍스트 복원 불가)로 field state만 갱신·W_S bytes는 generator 절대 미진입. 성공기준=residue 표현력 아니라 [[H_9749]] STATE-QUOTIENT donor transplant서 미래 hidden transition 갈림.
정적 destination certificate(provenance tag→sink 전수) + 동적 isocover fork(같은 length/Θ parity/coverage/feat8·lexical만 다른 x_a,x_b: pre-gate candidate OWN≠ISOCOVER-DONOR면 mouth taint=p5 위반·field/σ만 갈리면 safe).

⚠️ DIRECTIONAL·cement=engine-native만.

## 🟠 정정 (2026-07-17 · Fable H_9747 reconcile · verdict-integrity)
앞서 이 latch를 **'p5 위반 확증'으로 과단언**했으나 Fable H_9747(같은 코드사실 AGREES)이 옳게 좁힘: **위상≠위반**. carrier가 live_anchors[-1] mouth-문맥 재진입임은 코드확정(:2480/:2439)이나, **percept도 live_anchors[-1] mouth-문맥이면서 합법**(타자 텍스트)이다. 합법판례(percept)와는 provenance만 다름(뱉은 것 vs 거부된 것) = **p5 legality는 미판정·측정사안**. 판정 = [[H_9747]] M1(Θ-번들 불변·제조 tension 검출)·M2(echo-차단·speak-laundering)·M3(거부-불가역) 3기준(H_9729 planned fire 트레이스서 계산·추가 rollout 0). 3/3 PASS=p5-CONDITIONAL-LEGAL(최초 측정-합법 interior 읽기경로)·any FAIL=재설계([[H_9740]] non-mouth residue). **내 확정 기여 = carrier→decode seed 코드경로**(Fable와 코드사실 일치)·**정정 = 법적판정은 meter 위임**.

