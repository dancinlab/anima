# V6_19 — 전송 패널을 **기존 플래그**로 돌릴 수 있다 (그리고 막판에 통제 누출 2건을 잡았다) (@hypothesis-ok)

V6_18 이 "지어도 된다" 를 냈으니, `a_experiment_engine_native` 가 요구하는 질문 —
**엔진 옆 스크립트가 아니라 `anima-py` 플래그로 돌아가는가.**

## 돌아간다 — 새 엔진 코드 0줄

H_9825 가 이미 `--weave-panel <file>` 을 넣어놨다(얼린 12항목 배터리를 매니페스트로 교체,
*"bar·controls·scorer 는 그대로, n 만 움직임"*). 항목 모양은 `{cue, target, swap_cue, bind_cue, lang}` 이고,
**두 발산 모델이 각자 요구한 통제와 대응이 정확히 맞는다**:

```
swap_cue   atom-swap[FORM]   원자 하나 바꿔 target 이 오답이 됨   ≡  지시대상-셔플 팔
bind_cue   bind-strip[BIND]  원자는 있고 결합연산만 제거          ≡  문맥-절단 팔
null                         프롬프트 없는 기저율                  ≡  참값-0 바닥
```

```
anima-py evaluate <clm> --rho-axon --weave-panel /tmp/ctx_transport_panel.json
```

산출: **4,385 항목** · 독립 문서 3,083 · 실제 `load_weave_panel` 왕복 통과(5-튜플).
재생성 = `python3 lab/v6/ctx_panel_emit.py <out.json>` (2.2MB 생성물이라 커밋 안 함).

## 🐛 발사 전에 잡은 통제 누출 2건 — 둘 다 조용했다

```
① 골드가 swap 팔에 그대로 남음        1,090 건 (24.82%)
   원인: 첫 언급만 바꿨는데 개체는 흔히 3번 이상 나온다
   결과: 순수 복사기가 FORM 통제에서 점수를 낸다 — 전송과 무관한 이유로 통제가 높게 읽힘
   수정: 큐 안 골드 **전량** 치환

② 대체 이름이 골드를 부분문자열로 품음   66 건
   원인: `Alexander` 를 `Alexander the Great` 로 치환 → 골드가 되살아남
   결과: 같은 훼손이 더 작은 규모로 잔존
   수정: 골드와 겹치지 않는 후보만 선택 · 그런 후보가 없는 부지 13건은 폐기
```

추가로 골드가 BIND 창 안에 이미 보이는 370건(7.78%)도 폐기 — 그 팔이 자기 답을 자기가 갖는다.
**최종 불변식 전 패널 성립: swap 누출 0 · bind 누출 0 · 세 팔 모두 큐와 다름.**

`instrument-never-run-hides-multiple-bugs` 그대로다 — 한 번도 안 돌린 계기는 버그를 여럿 겹쳐
숨기고, 여기서도 **두 개**가 겹쳐 있었다. 둘 다 emit 가드가 잡았지 눈으로는 안 보였다.

## ⛔ 아직 bar 를 읽으면 안 된다 — 판독 방식이 어긋나 있다

weave 채점기는 `mouth.ideate(cue, 24 tokens)` 뒤 **"target 문자열이 떠올랐나"** 다 —
**자유 발상**이지 후보 중 강제선택이 아니다. 그런데 V6_18 의 실현 우연 0.2391 과 복사-전용
기저선들은 **강제선택** 판독에서 계산됐다.

```
강제선택 K후보     우연 = (1/N)Σ1/Kᵢ = 0.2391
자유발상 떠오름    우연 = null 기저율, 0 에 가까움
```

⟹ V6_18 의 수치를 얼린 `thr=0.30` / `ctrl_cap=0.15` 에 대고 읽으면 **한 판독에서 계산한 양을
다른 판독용으로 보정된 문턱에 재는 것**이다. `instrument-claim-alignment-before-reading-a-bar`
이고, G6 게이트가 죽은 방식이기도 하다.

**이 패널의 bar 는 자기 판독에서 유도해 첫 실행 **전에** 동결해야 하며, 실행 후 재고정은
금지다**(`burned-gate-no-refreeze-sequential-gating`).

## 남긴 것

- bar 유도 + 동결 (이게 다음 관문이고, 이걸 하기 전엔 어떤 실행도 판독 불가).
- 레인 비교 **전에** 참값-0 받침대 인증 — 레인 없는 팔에서 full ≡ 절단이 구조적 동일이므로
  0 이 아닌 Δ 는 전부 계기 결함(Fable NOVEL).
- 그 다음에야 `--mouth-binder`(core/mbnd.py · V6_17) 대조.
