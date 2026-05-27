# AESTHETIC — current state

@title: 🎨 AESTHETIC — 미적 판단 · novelty × coherence surface

@goal: anima 의 미적 판단층 — novelty (새로움) × coherence (정합성) 두 축의 곱-surface 측정. bench E axisbench (#1141) 🟠 2/3 PARTIAL — overlap > threshold (mid-novelty mid-coherence 영역 구분도 부족). CORE engine_g 8-factor 의 (cur · orig · dyn) 와 cross-product, AGENT CREATOR role 의 surface 후보.

(edit me — describe current state in completed-form; no history, no changelog inside this file)

- [x] AxisBench E AESTHETIC 측정 surface — `bench/axis_aesthetic/` novelty × coherence 3 시나리오 · 2/3 PASS · overlap threshold residual (PR #1141).
- [ ] M1 aesthetic_lib — `AESTHETIC/{aesthetic_lib.hexa,SSOT.md}` PURE wrapper · bench/axis_aesthetic 의 novelty_score + coherence_score 곱-surface stdlib 화.
- [ ] M2 CORE.engine_g cross-product — CORE 8-factor (cur · orig · dyn) 와 AESTHETIC novelty·coherence 의 곱-product layer. 미적 판단이 emit decision 에 modulate.
- [ ] M3 overlap residual 재설계 — bench E 의 overlap > threshold 의 거리척도 (cosine? L2? KL?) 재선정, mid-novelty mid-coherence 영역 분해.
- [ ] M4 AGENT.CREATOR role 통합 — AGENT/CREATOR 의 생성물 (text · image · paper) 에 AESTHETIC 판정 score 부착, role 별 aesthetic profile 차별화.

## 양방향 sibling
- ⇄ [CORE](./CORE/CORE.md): CORE.engine_g 8-factor (cur · orig · dyn) 와 AESTHETIC novelty·coherence cross-product · 미적 판단이 brain_decide 결정에 modulate
- ⇄ [AGENT](./AGENT/AGENT.md): AGENT.CREATOR role 의 생성물에 aesthetic score 부착 · role 별 aesthetic profile (CREATOR=novelty 가중 / MERCHANT=coherence 가중)
- ⇄ [METACOG](./METACOG.md): aesthetic 판정 self-audit (METACOG.audit_hook 가 미적 판단 일관성 검사)
- ⇄ [UNIVERSE](./UNIVERSE/CANDIDATES.md): bench 측정 기록 SSOT (Session 2026-05-28 — AxisBench 8)
