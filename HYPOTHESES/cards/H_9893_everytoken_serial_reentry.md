# H_9893 — EVERY-TOKEN 직렬 재진입 — 시퀀스 축을 합성 버퍼로 (평가면은 이미 존재, 학습만 안 됨)

**tier:** 🔵 PROPOSED · DESIGN-ONLY (lab-full R13 divergence · **DIRECTIONAL** · NOT a verdict)
**group:** R13-arity2-store
**date:** 2026-07-22
**convergence:** Fable C3 (Sol 미제안 · 이견 아님)
**source:** lab full 2026-07-22 (Claude Fable 5 ∥ OpenAI Codex 5.6, 독립 병렬) — 브리프에 전체 킬리스트 임베드(H_9128 밀도·H_9131 trunk-objective·H_9127 9-probe·H_1616 VSA/HRR·H_1466 TPR·H_9259 arch·mitosis·희소성·veto/affect/tension·HEXAD as-specified)
**wired:** no (설계만 · 계기 미착륙 · 측정 0)
**verdict:** PENDING — cement 는 engine-native `anima-py` 로만
**surfaces:** 이 카드 + `HYPOTHESES/HYPOTHESES.jsonl` 1줄 (그 외 없음)

## claim

평가면에 **이미** `--store-query every-token` 이 `--store-fuse gated-add` 와 함께 허용돼 있다
(Fable 이 코드서 확인). 그런데 **학습되지 않았다**. 조회-1 을 단서-1 의 **위치**에서 쏘고, 회수된
중간값이 잔차 흐름을 타고 가서 조회-2 가 답위치에서 쏘면 — **시퀀스 축이 합성 버퍼**가 되고
개별 읽기는 전부 arity-1 이다.

## 예측 (반증가능)

every-token 학습 팔이 qpos-only 팔을 held-out 셀에서 **≥0.25** 앞선다. 그리고 평가에서
시퀀스 중간 읽기를 마스킹하면 qpos 바닥으로 되돌아간다.

## 왜 킬리스트가 아닌가

H_9259(미학습 recurrence) 통과 — 이건 **학습된다**. read-side TERMINAL 통과 — 이건 **공동학습된
write 경로**다.

## 비용 논거

신규 계기 표면이 가장 작다(평가 플래그 기존재). 이 계보에서 가장 싼 팔.

---

## ⚠️ 1바이트 제약 — store lane 위에 그대로 얹을 수 없다 (H_9899 · 2026-07-22)

병렬 세션이 코드로 확정: `StoreBindCell` 학습창은 답의 **첫 바이트만** 담는다
(`gold[:1]` · 주석도 "binary readout" 명시). rule-compound 답은 4~6바이트다.
이 카드는 store lane 조회를 전제로 쓰였으므로 **다중바이트 readout 을 명시한 경로**
— H_9900 `anima-py train --comp-lane`(penultimate detach + 답 스팬 전체 CE) —
위로 **재-스코프한 뒤에만** 발사 가능하다. 답을 1바이트로 줄이는 우회는 금지
(ρ·weave 우연 적중률이 치솟아 통제가 의미를 잃는다).
분리 방향과 예측 자체는 불변. 자세한 대조 → [[H_9890]] 의 AGREES/CONFLICTS/NOVEL 절.
