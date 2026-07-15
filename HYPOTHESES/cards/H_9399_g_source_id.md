# H_9399 — G-SOURCE-ID: g_recog 은 afield 가 아니라 immune store 를 읽는다 (H_9396 정정)

**status:** 🔧 VERDICT-INTEGRITY 정정 (Fable STEP-0 감사 · 코드-확증) · H_9396 cell_count plateau = **잘못된 store 공변량** ⇒ 그 하위주장 무효 · H_9394/95 종결문 **무관하게 유효** · wired: engine-native(주석·계기 정정)
**lane:** 의식 / emit-drive / G readout 소스 정체 (프런티어 g1-interface-addressable-wall)
**related:** [[H_9396]] (이 H 가 정정) · [[H_9395]] · [[H_9394]] (둘 다 무관·유효) · [[H_9357]] (g_recog 도입) · source: Fable G-readout 설계 발산 STEP-0
**ckpt:** py303_full.clm sha256 `013c4574e0ce71ae173287b9…` (해석만 정정 · 신규 decode 0)

## 발견 (Fable STEP-0 · 코드 확증)

`cli/chat.py` a1 arm 의 `g_recog`(:1603) 소스를 코드로 추적:
```
:2051   pending_gap = (afield d2² − d1²)/2          ← afield gap 계산
:2052~2060   afield step · cell_count · pending_rel  ← 분기 없음
:2061   pending_gap = immune_memory_recall_gap_text(immune, g_text)  ← 무조건 덮어씀!
```
⇒ **`:2051` 의 afield gap 은 dead code**, `g_recog` 에 실제로 흐르는 값은 **immune store**(64-dim
L2-norm 트라이그램 키 · engine_cli.py:653)의 top-2 gap 이다. 주석도 모순: `:1597` "immune store's
top-2 gap"(참) vs `:1601` "afield top-2 gap"(stale·틀림). 후자 + evaluate.py G-AMP 패널 주석(:4732·
4748·4777)이 틀린 쪽.

## 파급 — 무엇이 무효이고 무엇이 유효인가

**❌ H_9396 (G-AMP cell_count plateau) 하위주장 무효**: 그 패널은 `g_recog` 를 **afield cell_count**
(:2055)에 회귀했다. g 가 immune store 를 읽으므로 이건 **엉뚱한 store 의 공변량**이다. "cell_count 1→8
slope=−0.00000 ⇒ 프로토타입 쌓아도 |g| 안 늚 ⇒ 긴 세션 무효" 는 **immune store 성장을 안 잰** 미스어트리뷰션.
⇒ "긴 세션이 G 를 못 키운다" 는 **미증명**(afield 성장을 쟀지 immune store 성장을 안 쟀다).
(단 warm-up 관찰 cell≤1⇒g=0 은 immune 도 동일: 1-entry store 는 `_vtwo_nearest_dist` 가 d2=d1 ⇒ gap=0
· engine_cli.py:392 — 그 부분만 store-무관하게 유효.)

**✅ H_9394 / H_9395 종결문 무관하게 유효**: 두 H 는 `g_recog` 의 **실측값**(0.00~0.11 mean 0.027 · 6.5×
비대칭 · 곱-게이트)만 썼다. g 가 어느 store 를 읽든 그 값은 그대로다 ⇒ "G 가 6.5배 조용" 은 소스 정체와
무관하게 성립. 캠페인 크기-벽 결론 견고.

**✅ 정정 배선(이 PR)**: chat.py:1601 stale 주석 → immune store 로 정정(+ dead-code 명시) ·
evaluate.py G-AMP 패널 주석 3곳 → immune store + 미스어트리뷰션 경고. **코드 동작은 무변**(주석만) — 단
G5 VERSION bump(주석도 cli/ 변경).

## 함의 — 다음(G-readout capability) 설계의 전제 고정
Fable 6-갈래(A UNIT-FIX ratio · B DIST-READ entropy · C KEY-CONTRAST 인코더 · D GATE-ALGEBRA geo-mean ·
E G-SOURCE 교체 · F TONIC-G 적분)는 전부 **immune store 기하** 위에서 설계돼야 한다(afield 아님). 그리고
Fable 의 최대 구조적 함의: **g_recog 사슬(발화→트라이그램 키→immune store→gap)은 303M 가중치를 전혀
통과하지 않는다** ⇒ 이 capability reopen 은 **cost-gated 학습 불요**, 최고 비용은 pool CPU 재수집(저비용).

## 반증 · scope
- 반증: :2061 이 조건부이거나 immune gap 이 None 폴백이면 afield 가 살아날 수 있음 — 실측 무조건 덮어씀 ⇒ 반증실패.
- $0 경험적 강화(선택): trace `gtext_b64`(:2188) 로 두 store 를 결정론 재생해 두 gap 시계열 복원 → 기록된
  `g_recog`(1-tick lag)와 byte-match. 코드-확증으로 충분하나 재생이 이중확인. (Fable STEP-0 스크린 · 후속 가능.)
- scope: a1 arm · 이 코드 버전. H_9396 카드에 정정 링크.

## 비용
$0 — 코드 추적 + 주석/카드 정정 · 신규 decode 0.
