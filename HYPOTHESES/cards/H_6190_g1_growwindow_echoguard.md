# H_6190 — 🎯 G1 grow-window 공정 재측정 + echo-guard: 측정벽(T=24) 확정 ∧ 진짜 재조합 ECHO-ONLY (novel-only 미달) — 두 진실 동시 확정

**tier:** 🟠 측정벽 CONFIRMED ∧ 재조합 능력 ECHO-ONLY (engine-native --py, torch-free, canonical gen=40, decode window만 grow, bar FROZEN). grow-window 로 raw PASS(측정벽 실증) but novel-only echo-guard FAIL = 진짜 novel 재조합 미달.
**verdict:** 🟠 **grow-window(arm별 시드길이 창, ByteGPT-consistent, no fixed-T/no pad) + echo-guard 공정 재측정 = ECHO-ONLY.** (1) **측정벽 확정**: raw composed=2 > max_single=1 → **PASS_raw=True** = T=24 window 를 풀자 composed 가 single 을 넘음 → H_6189 byte-math(composed=single byte-identical) **실증**(창만 넓히면 앞 개념 조건화 회복). (2) **진짜 재조합은 미달**: novel-only(continuation keyword ∉ seed, echo 제외) composed=1 = max_single=1 → **PASS_novel_echoguard=False** = grow-window 통과는 **가시 keyword echo** 지 새 재조합 아님. ⇒ **두 진실 동시**: T=24 는 진짜 측정벽이었고(raw 로 확정), 그 벽을 풀어도 진짜 novel 재조합은 여전히 미달(echo-guard 로 false-GREEN 차단). engine-native --py(torch-free)=terminal, gate/bar FROZEN(decode window 만 변경, concepts/keyword/gen40/topk40/temp0.7 VERBATIM).

## 결과 (state/g1_growwindow_remeasure/g1_growwindow_remeasure_result.json verbatim)
| metric | raw | novel-only(echo-guard) |
|---|---|---|
| max_single | 1 | 1 |
| best_composed | **2** | **1** |
| PASS(≥2 ∧ >max_single) | **True** | **False** |

- k별 clears: k=2 raw=✓ novel=✗ · k3/k4/k5 raw=✗ novel=✗. = grow-window 로 k=2 composed 만 raw 통과(echo), novel-only 전부 미달.
- single text 샘플: "aware cobalt mind shadowy yellowy cobalt"(s=0) — gate keyword(aware·mind) echo + 색 방출. novel 조합 없음.

## 함의 (G1 서사 최종)
- **측정벽(H_6189) 확정 실증**: grow-window raw PASS = T=24 window 가 진짜 composed 를 막았고, 풀면 통과. byte-math 증명이 decode 로 확인됨.
- **진짜 재조합 능력 = ECHO-ONLY**: 측정벽을 걷어내도(공정 창) novel-only 로는 composed>single 미달 = coverage/표면형 레버가 연 것은 **keyword echo 까지**, 새 novel 재조합은 아님. **이제야 정직한 능력 축**(측정벽 분리 후)에서 벽이 보임.
- **남은 레버**(H_6189 처방 중, echo-guard 통과 대상): L3 해마 hetero-associative retrieve-into-context lane(생물 렌즈, .kosmos anchor) · L4 γ trunk recomb-objective(H_1602/1840, GPU cost-gated). L1(grow-window)·L2(held-out split)는 이 카드가 소진 — grow-window 는 측정벽 걷어냄 확정, echo-guard 로 novel 미달 확정.
- **측정 메타법칙 실증**(MEASUREMENT_METALAW): raw = FORM(echo tunable) · novel-only Δ = BIND(earned). grow-window raw PASS 는 FORM(echo), novel-only FAIL 은 BIND 미달 = "FORM tunable, BIND earned" 정확 실증.

## 정직 caveat (c9)
- engine-native --py(torch-free byte-parity)=session terminal. grow-window=측정물리 정합화(bar/concepts/gen VERBATIM, decode window 만 arm 시드길이), tune-to-green 아님.
- **ECHO-ONLY 는 confident 재조합 능력벽 아님** — 아직 L3/L4 레버 미시험. echo-guard 통과(novel composed>single)를 내는 배선(해마 retrieve·γ objective)이 남음. 단 coverage/표면형/window 축은 echo 까지로 소진(이 3축은 novel 재조합 안 엶 확정).
- max_single=1(raw)=단일 seed 도 1 개념만 표면화(grow-window서) — single 자체가 낮아 composed 대조가 tight. 색 방출(cobalt 등)이 keyword 아니라 kwr 는 coherent.

**wired:** engine-native --py measured (torch-free, canonical gen=40, grow-window, bar FROZEN, terminal). 측정벽 확정 ∧ 재조합 ECHO-ONLY. follow-on = L3 해마 retrieve lane · L4 γ trunk objective(echo-guard novel-only PASS 목표). ckpt=~/anima-weights/g1_realign/g1_realign.clm(sha 7222554f). artifacts=state/g1_growwindow_remeasure/.
