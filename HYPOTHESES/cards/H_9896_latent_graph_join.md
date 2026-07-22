# H_9896 — 잠재변수 그래프 join — 프롬프트에 없는 공유 x 를 통한 R(a,x)∧S(x,b) 증인 탐색 (조건부·게이팅됨)

**tier:** 🔵 PROPOSED · DESIGN-ONLY (lab-full R13 divergence · **DIRECTIONAL** · NOT a verdict)
**group:** R13-arity2-store
**date:** 2026-07-22
**convergence:** Sol C4 (Sol 자신이 '조건부'로 표기 · Fable 미제안)
**source:** lab full 2026-07-22 (Claude Fable 5 ∥ OpenAI Codex 5.6, 독립 병렬) — 브리프에 전체 킬리스트 임베드(H_9128 밀도·H_9131 trunk-objective·H_9127 9-probe·H_1616 VSA/HRR·H_1466 TPR·H_9259 arch·mitosis·희소성·veto/affect/tension·HEXAD as-specified)
**wired:** no (설계만 · 계기 미착륙 · 측정 0)
**verdict:** PENDING — cement 는 engine-native `anima-py` 로만
**surfaces:** 이 카드 + `HYPOTHESES/HYPOTHESES.jsonl` 1줄 (그 외 없음)

## claim

`R(a,x)` 와 `S(x,b)` 를 degree-매칭해 저장하되 공유 `x` 는 **프롬프트에 없다**. 증인이 존재하는가를
묻는다.

## 예측 (반증가능)

순열-등변 M join 이 held-out 그래프에서 성공하고, degree·주변 `R`/`S` 개수·템플릿 바이트를
보존한 edge shuffle 은 우연으로 붕괴.

## 🚦 게이팅 (Sol 자신의 단서 · 준수한다)

**고정쌍 arity-2(H_9890)가 먼저 작동한 뒤에만 연다.** 그 전에는 미해결 2-read 문제 위에
탐색·집합교차 실패양태를 얹는 셈이라 판독 불가가 된다. 지금 발사하면 어떤 음성도 귀속 불가.
