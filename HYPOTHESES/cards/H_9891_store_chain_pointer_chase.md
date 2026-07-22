# H_9891 — STORE-CHAIN 2-hop — 값이 곧 다음 키(의존 주소 추격): arity-2 를 순차 arity-1 둘로 환원

**tier:** 🔵 PROPOSED · DESIGN-ONLY (lab-full R13 divergence · **DIRECTIONAL** · NOT a verdict)
**group:** R13-arity2-store
**date:** 2026-07-22
**convergence:** 🔀🔑 Fable C1 ≡ Sol C1 **독립수렴**(양 모델 1순위 신규각도)
**source:** lab full 2026-07-22 (Claude Fable 5 ∥ OpenAI Codex 5.6, 독립 병렬) — 브리프에 전체 킬리스트 임베드(H_9128 밀도·H_9131 trunk-objective·H_9127 9-probe·H_1616 VSA/HRR·H_1466 TPR·H_9259 arch·mitosis·희소성·veto/affect/tension·HEXAD as-specified)
**wired:** no (설계만 · 계기 미착륙 · 측정 0)
**verdict:** PENDING — cement 는 engine-native `anima-py` 로만
**surfaces:** 이 카드 + `HYPOTHESES/HYPOTHESES.jsonl` 1줄 (그 외 없음)

## claim

값을 개체 **이름의 얼어붙은 바이트-임베딩**으로 저장해 **값공간 ≡ 키공간**으로 만들면, 답위치에서
첫 조회 결과로 두번째 질의 q₂ = W_c·v₁ 를 만들 수 있다. 그러면 arity-2 가 **각각 H_9775 로 이미
살아있다고 증명된 arity-1 조회 두 번**으로 환원되고, trunk 상태 결합을 통째로 우회한다.

핵심은 **의존성**이다: 두번째 주소는 첫 읽기가 끝나기 전에는 **형성될 수 없다**. 질의에는 출발
개체만 들어있다.

## 예측 (반증가능)

전혀 held-out 인 A→B→C 사슬(쌍 (A,C) 는 한 번도 공동학습 안 됨 · 직접암기 통제는 우연)에서
reach ≥ bar, 그리고 W_c 를 절제하면 붕괴. 병렬 2-질의 레인·첫-포인터 순열·첫-hop 병변은 우연.

## 왜 킬리스트가 아닌가

H_9259 가 죽인 것은 **미학습** recurrence 다. 여기서는 상태전이와 write/read 경로가 **학습되고**,
두번째 주소가 첫 결과에 **인과적으로 의존**한다.

## 판독의 가치 (어느 쪽이 나와도 새롭다)

두 1-hop leg 가 같은 하네스서 🟢 인데 사슬이 실패하면 — 벽이 **trunk arity** 에서
**store 재귀**로 **이동**한다. 그것 자체가 새 벽 진술이다.
