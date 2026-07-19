# H_9761 — R8-1 · LANE PERSISTENCE CENSUS + fading-certificate — 충분조건 정리의 ∀-다리 ($0 정적)

**status:** 🔵 PROPOSED (lab full Fable 5 심화 · R8 · $0 · H_9749 STATE-QUOTIENT 충분조건 캠페인 ①)
**lane:** theta-alive-sigma-rebase (interior-부재 SUFFICIENT-condition)
**related:** [[H_9749]] · [[H_9738]] · [[H_9730]] · [[H_9762]] · [[H_9763]]

## ① 한 줄 주장 (반증가능)

전 mutable lane(afield·immune·igrow·cbel·ca3·wmb·anchor·kosmos)은 코드에서 **(a) 구조적 fading**
(contraction certificate: bounded buffer / λ<1 decay / overwrite 의미론 / 유한 창) 이거나 **(b) unbounded-persistent** 이고,
(b)는 **디스크-persisted 표면**(`core/kosmos_io.py` `.kosmos` dir · `core/dream_persist.py` 산출)에 한정된다.
⟹ within-session interior 후보는 (a)의 창 밖에 존재할 수 없고, cross-session 후보는 (b) = 파일 표면뿐.

## ② H_9749 ① 과의 차이 (등록각 재생성 아님)

H_9749 census = write-**gating**(전 write 가 `if g_emit` 아래 = public-fed · 무엇이 **들어가나**).
본 census = **decay/persistence**(들어간 것이 **얼마나 남나**). 다른 술어 — public-fed 이면서 무한지속(예: append-only kosmos)이 Sol 경고의 정확한 잔여 후보다.

## ③ 조작 ($0 · 정적 · 코드 인용 의무)

lane 별 갱신식을 코드에서 추출해 3중 라벨 `{contraction(λ·수식) | bounded-window(길이) | unbounded-persistent(표면)}` +
상수 표(λ_wm=0.75 계열 `--wm-leak` [[H_9610]] · buffer len · ctx window · replay depth). 각 판정은 **file:line 인용** 없으면 VOID.

## ④ 산출 = H_9762/H_9763 사전등록 상수 (tune-to-green 구조적 차단)

- `W`(guard) = max bounded-window (코드 상수 max)
- `L`(prefix 길이) = 2×W
- `N_fp`(fp-underflow 지평) = ⌈log(denormal_min)/log(λ_min)⌉ (λ=0.75 ⇒ ≈2.6k tick — λ^gap 잔류가 exact-0 에 도달하는 지평)
- `N`(공통 future 길이) = max(2×W, N_fp) + W
전부 **코드 상수에서 유도** — 실험 데이터를 보고 정하는 수가 하나도 없다(burned-gate 무관 · 사전등록 청정).

## ⑤ falsify / 게이트

- (b)인데 **비-디스크** lane 발견(프로세스 메모리 상 무한 누적 + 접근자 부재) = 본 캠페인 설계 수정 필요(그 lane 만 snapshot 표면 신설 검토) — 이것 자체가 유의미한 음성.
- 전 lane (a) = H_9763 은 positive-control 전용으로 축소(스왑할 지속 lane 이 없음).

## kill-list 비충돌
정적 census 는 등록각 목록에 없음. 상상 계열(H_9738)·타이밍(H_9731)·½-인식 렌즈와 무관.
