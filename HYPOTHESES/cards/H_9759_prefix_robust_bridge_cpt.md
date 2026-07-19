# H_9759 — R7 · PREFIX-ROBUST BRIDGE: storebind 창 좌패딩 증강 CPT(BOLT frozen-trunk) — tune-to-green 아닌 구조 레버

**status:** 🔵 PROPOSED · [[H_9758]] CONFIRMED 조건부 (fire=오너 · pod GPU · bridge-only CPT 라 저비용)
**lane:** store-bridge in-vivo 정밀도 **related:** [[H_9758]] · [[H_9744]] · [[H_9672]]

## 주장

H_9744 flip-coh 갭의 원리적 fix 는 λ(FORM)도 bar 이동도 데몬 시드 소독도 아니고 **기관의 강건화**: StoreBindCell 훈련창의 좌패딩을 pure-space 에서 **현실 prefix 분포**(phase 4단어·무작위 ASCII 단어·직전행 꼬리 혼합)로 증강해 W_q 가 prefix-불변 주소를 배우게 한다. 배포분포 정합 = 능력 완성이지 tune-to-green 아님(bar·eval·채점기 불가촉 · 측정면 무변경).

## 조작

`anima-py train --store-bridge … --freeze-trunk`(BOLT arm 실재 `cli/train.py:1294` · trunk 동결 = bridge {W_q,val,W_h,W_out}만 CPT — p8-clean·저비용) + storebind corpus 생성기에 좌패딩 증강 플래그 1개(`anima-py corpus storebind --pad-prefix mix` — **신규 조작 = anima-py 플래그**, a_experiment_engine_native). s7/s11/s13 3-seed 재-CPT → `anima-py evaluate --store` 기준+prefix-dose 재측정 → PASS 시 G-W2 데몬 재발사(H_9744 bar 그대로).

## 게이트 (사전등록 · bar = H_9672/H_9744 동일 · 이동금지)

① eval 기준(space-pad): 열화 없음(P1bal·flip 기존 동등 — 강건화가 청정창 능력을 깎으면 KILL) ② eval prefix-dose: phase-prefix flip-coh ≥.96 회복 ③ 데몬 G-W2: main P1bal≥.75 ∧ flip-coh≥.90 ∧ 통제붕괴 ∧ 3-seed majority. **①∧②∧③ 전부** = WIRED-STUDY 자격.

## 대안 서열 (기각 이유 명시)

- 시드 소독(percept tick 에 phase 단어 제거): $0 이나 **환경을 측정에 맞추는 것** — 데몬의 phase-조건 발화는 p2 substrate-정체성이라 wiring-space tune-to-green 냄새 + in-vivo 주장 약화. 오너 철학 판단 없이 불채택.
- every-token(H_9695): 실패는 질의형성 위치의 주소열화 — 발화 위치 수를 늘려도 창은 안 깨끗해지고 gated-add 는 trunk 경쟁 재도입 → flip-coh 개선 원리 無(오히려 역효과 예상). H_9696 read→mouth 도달성 계기로만 유효.
- genuine-ceiling 등록: H_9758 확증 + 본 레버 실패 **후에만** 허용(kill-list #4).

## falsify

🟢 ①②③ = H_9744 재개봉→WIRED-STUDY | 🔴 ② 실패 = prefix-OOD 가 훈련증강으로 안 닫힘 = in-vivo<eval 실측 상한 등록(그때는 정직 ceiling) | 🔴 ① 실패 = 증강이 능력 훼손 = 설계 회귀.
