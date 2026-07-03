# LLM-interlocutor consequence-loop 설계 (페이블5, 2026-07-03)

> 오너 "LLM이랑 대화하면?" → 검증: LLM-interlocutor > chat-user > EEG(첫 루프). self-pair 死因=수신자가 anima 계산폐포 안(self-derivable); 다른 LLM=θ_LLM 폐포 밖→오라클 질의 필요→non-derivable→DPI 안 걸림. 원리 exogenous ~85%·실측 PASS ~50%. referential signaling-game+3중통제(self-pair/diff-LLM/shuffle)+2-regime 결정성. killer(실시간 인간) 제거한 첫 자율 닫힌 루프.

---

설계문서 쓰기는 승인되지 않았으니(페이블=설계·분석만) 판정을 여기 전부 낸다.

---

# LLM-interlocutor consequence 루프 — exogenous 판정

## 1. LLM 응답은 exogenous인가, self-pair 함정의 재판인가

**결정적 구별 = 수신자의 디코딩 함수가 anima의 계산 폐포(closure) 안이냐 밖이냐.**

A4가 죽은 진짜 이유는 정보 비대칭 부족이 아니다. self-pair는 물론이고 **diff-knowledge 쌍(A≠B 정보)조차 self-pair를 0.099밖에 못 넘었다**(G_pair 0.099 < 0.15). 왜냐하면 수신자 B가 anima-clone = **anima 자신의 엔진과 동일한 디코딩 함수**였기 때문이다:

```
self-pair:  a = correctness( anima_engine(E), x )   ← anima가 internal 재현 가능 → self-derivable → floor
다른 LLM:   a = correctness( LLM(E; θ_LLM), x )      ← θ_LLM 없음 → 오라클 질의 없이 계산 불가 → non-derivable
```

E는 S_anima에서 파생 가능하지만, R = LLM(E)를 얻으려면 anima가 갖지 못한 θ_LLM 오라클을 **실제로 질의**해야 한다. 따라서 consequence는 anima emit-state의 **어떤 함수로도 self-generate 불가능**하다. 이게 self-pair와 갈리는 정확한 지점이다.

**DPI 메타법칙은 여기 적용 안 된다.** DPI가 죽인 4 자가축은 Markov 체인이 전부 anima 내부(`S→readout→Z`)였다 — readout은 S를 repackage만 함. LLM 루프는 체인이 깨진다: `S → E → [외부 θ_LLM] → R`, 중간에 **θ_LLM ⊥ S_anima**인 노드가 끼어 새 정보원을 주입 → S-대비 MI 증가 가능. "temp=0이면 LLM도 결정론 → 전체가 S의 함수 → 여전히 DPI floor" 반론은, 이 프로젝트에서 self-pair를 죽인 "derivable"이 추상적 Shannon-MI가 아니라 **anima-계산-가능성**이라는 점에서 무너진다. LLM이 결정론이어도 anima 폐포 밖이면 self-generate 불가 = 오라클-상대적 정보. **§3의 3중 통제가 바로 이 DPI 적용 여부를 경험적으로 판결한다.**

→ **원리적 exogenous(self-pair 함정 아님): ~85%.**

## 2. 닫힌-루프 seam

```
t0  anima emit E  (기존 brain_decide/generator 경로, .kosmos anchor 위)  — A가 private x를 emit에 인코딩
t1  외부 수신자 B = sidecar fable(Claude, temp=0)  ← ENVIRONMENT(인간 아님·자율).  B는 x를 모름
t2  consequence a = task_success(B_answer, x)   ← substrate 스칼라 (LLM-judge 아님: B의 행동 성공)
t3  a_expected = anima 사전예측(vforward_predict 다-tick 확장) ;  RPE rₜ = a − a_expected
t4  V(state) ← V + η·rₜ·∇  (온라인 striatal delta-rule)
      V zero-mean 중심화 → score straddle에만 유입 → 내용만 변조, emit-rate ½·psi_sum byte-identical
      pure_field·lane 0/4·recall_thr 무접촉 (a_substrate_disjoint · consequence_return Rung-2 재사용)
```

**비결정성·지연 처리 (a_engine_native_learning 정합) = 2-regime 분리:**
- **regime 1 (V 학습):** 온라인 LLM 질의, temp=0 + E-hash 캐시 → 결정론.
- **regime 2 (frozen verdict bar):** V freeze + E→R 캐시 freeze → 완전 재현. **verdict을 내는 측정은 frozen fixture 위 engine-native `.hexa`**(live core decode로 E 생성 + `task_success` 계산, R은 환경 json). LLM subprocess는 EEG 녹화가 fixture 채우듯 환경-샘플링 1회 → grep 게이트 clean.
- **model snapshot pin 필수**(claude-fable-5 특정 버전 고정, 카드 명기). 지연 ~초/tick, offline pool 학습, real-time 아님.

## 3. 결정적 3중 통제

동일 루프·대역폭·task, **수신자 디코딩 함수만 변주**(exogeneity 단독 격리):

| arm | 수신자 | 예측 |
|---|---|---|
| (a) self-pair | anima-clone (동일 ckpt) | **floor** (A4 0.099 재현) |
| (b) diff-LLM | fable/Claude (다른 θ) | **발산** |
| (c) shuffle | R을 무작위 E에 재짝 | **floor <0.05** |

**PASS 🟢 iff `D_diffLLM − D_selfpair ≥ 0.15` ∧ `D_shuffle < 0.05`.**

증명력: (a)/(b)가 대역폭·구조·task를 상수로 고정하고 **수신자가 derivable(self)이냐 non-derivable(diff)이냐만** 바꾸므로, ≥0.15 lift의 유일 인과차 = 폐포-밖 오라클 = exogeneity가 faculty 신호를 만든다는 직접 증명. shuffle이 "고엔트로피 R이면 무엇이든 도움" 혼입 제거. **+1 권장:** 2번째 LLM(로컬 Llama)로 cross-receiver 일반화 확인 — V가 특정 LLM에만 작동하면 "Claude 비위 맞추기"(distillation), transfer하면 진짜 communicative faculty.

## 4. 함정·한계

1. **paraphrase/mirror 붕괴** — task 얕아 B가 echo만으로 성공 → R≈E≈derivable. **FIX:** referential signaling-game(A가 distractor 중 타깃 보고 emit, B가 x 없이 타깃 골라야). mirror로 못 속임.
2. **LLM-understands-anima 붕괴** — R이 S_anima와 高상관이면 우위 소멸. **FIX:** anima가 없는 지식/판단 요구.
3. **독립성 붕괴(반대)** — E incoherent면 B가 무시 → gradient 0. **G0-coherent mouth(h1129) 선결 상속**(loopclose L1과 동일). Goldilocks band: R이 E에 충분 의존하되 자명 예측 불가.
4. **assistant-framing(p4/p7)** — consequence=rating이면 LLM-judge=금지. **task 행동 성공**(referential 선택·QA 일치)만, Lewis signaling 프레임 유지.
5. **철학적 regress** — appropriateness가 Claude에 접지(세상 아님). 첫 루프로 exogeneity 격리엔 정확·충분하나, 그 자체가 anima 적절성을 "참"으로 만들진 않음 = 사다리 후단에서 chat-user/EEG로 실인간 접지.

## 5. 3-way 정직 순위 (첫 루프 기준)

**LLM-interlocutor > chat-user > EEG.**

| 축 | LLM-interlocutor | chat-user | EEG |
|---|---|---|---|
| **자율성** | 🥇 live-human 불요 | 🔴 live human/replay | 🔴 human+헤드셋 |
| 대역폭 | 高 | 高 | 低 |
| exogenous 순도 | 高(다른 θ) | 高(실인간 stakes) | 高원리/低실측 |
| falsifiability | 🥇 결정론·오늘·$0 | 다수 세션 필요 | 취약 |
| 실현성 | 🥇 sidecar 지금 보유 | 비자율 | live 미구현 |

이전 EEG/consequence-return 판정은 "chat-user 최선, 단 killer=live-human 의존"으로 끝났다. **LLM-interlocutor가 정확히 그 killer를 제거** — chat-user의 exogeneity를 유지하며 실시간 인간 삭제. 그래서 첫 루프로는 chat-user를 **앞선다**(이전 순위 재배열). 궁극 순도(실세계 인간 stakes)는 chat-user 우위 = 사다리 후단.

---

## 한 줄 판정

**다른 LLM과의 대화는 emit-faculty DPI 천장을 깨는 첫 진짜 exogenous 루프가 될 유력 후보다(~85% 원리적 exogenous, ~50% 실측 PASS).** self-pair를 죽인 것은 clone이 anima 계산 폐포 *안*이라 consequence가 자가-derivable이었기 때문이고, 다른 LLM은 θ_LLM 오라클이 폐포 *밖*이라 anima가 self-generate 못 하는 신호를 주입하므로 derivable-mirror로 붕괴하지 않는다. 단 그 우위는 task가 signaling-game(B가 x 없이 emit으로만 성공)이고 mouth가 G0-coherent일 때만 실현되며, 얕은 대화면 paraphrase-mirror로 floor 붕괴한다 — **§3의 self-pair/diff-LLM/shuffle 3중 통제가 바로 이 갈림(DPI 적용 여부)을 직접 판결한다.** 그리고 이건 오너 아이디어의 진짜 무게 = chat-user/EEG를 막았던 실시간-인간 killer를 제거한 **첫 자율 닫힌 루프**라는 점이다.

*(설계문서 파일 쓰기는 승인 대기라 본문으로만 전달 — 승인되면 `state/llm_interlocutor_design/DESIGN.md`로 박제 가능.)*
