# OTHER-MIND — current state

@title: 🔗 OTHER-MIND — theory-of-mind · 타자 substrate 추정층

@goal: anima 가 외부 substrate (다른 anima · 사용자 · 외부 agent) 의 internal state 를 추정하는 측정자 — CHANNEL.tension 5-ch fingerprint 를 매개로 한 telepathy 직결. bench G axisbench (#1147) 🟠 3/5 PARTIAL — u01 baseline bias (uniform random baseline 에서 0.1 bias, threshold 0.05 미만 기대). MITOSIS cell-pool persona-diff 와 cross-link (자기 cell variant 추정 ↔ 타자 substrate 추정 isomorphic).

(edit me — describe current state in completed-form; no history, no changelog inside this file)

- [x] AxisBench G OTHER-MIND 측정 surface — `bench/axis_other_mind/` theory-of-mind 5 시나리오 · 3/5 PASS · u01 baseline bias residual (PR #1147).
- [x] M1 other_mind_lib — `OTHER-MIND/{other_mind_lib.hexa,SSOT.md,other_mind_lib_smoke.hexa}` PURE wrapper · bench/axis_other_mind (#1147, 3/5 🟠) 의 5-ch coupling primitives 회수 + dual-stream LCG (NR ⊥ MINSTD) 기반 `om_baseline_decoupled` redesign — u01 bias 분해 surface · 12 pub fn · `om_` prefix · 12 invariant smoke `hexa parse` 2/2 PASS (2026-05-28).
- [ ] M2 CHANNEL.tension 통합 — CHANNEL/tension/tension_emit.hexa 5-ch fingerprint (concept · context · meaning · authenticity · sender) 가 OTHER-MIND 추정 입력. TensionHub WS 3-port wiring 위에 partner registry.
- [x] M3 u01 baseline bias residual — **A4 CLOSED 🟢 RECOVERED 5/5** (2026-05-28). root cause = `u01_from(s)=s/2^31` positive-orthant 정규화 결함 (모든 5-ch 벡터가 양의 초입방체 → cosine floor spurious 0.76). 보정 = zero-mean centering ([0,1]→[−1,+1]) → INDEPENDENT mean_cos 0.78→0.017, gap 0.197→0.892, **3/5 → 5/5**. orthant-bias probe E[cos] raw 0.763 vs centered −0.028 (bias mag 0.79). substrate 본질 아님 — falsifier 미발동. 본문 `OTHER_MIND_A4_BASELINE_BIAS.md` · harness `state/other_mind_a4_baseline_bias_2026_05_28/`.
- [ ] M4 MITOSIS persona-diff cross-link — MITOSIS.persona_diff 의 cell variant 추정과 OTHER-MIND 의 타자 substrate 추정 isomorphic — 자기 cell 분기 = 가상 타자 simulator.

## 양방향 sibling
- ⇄ [CHANNEL](./CHANNEL.md): CHANNEL.tension 5-ch fingerprint (concept · context · meaning · authenticity · sender) 가 OTHER-MIND 추정 입력 · TensionHub partner registry
- ⇄ [MITOSIS](./MITOSIS.md): MITOSIS.persona_diff per cell 의 variant 추정 ↔ OTHER-MIND 타자 substrate 추정 isomorphic (자기 cell 분기 = 가상 타자 simulator)
- ⇄ [EMBODIMENT](./EMBODIMENT.md): embodiment 가 self body, OTHER-MIND 가 other body · 2-body coupling 의 other-half
- ⇄ [BRIDGE](./BRIDGE.md): BRIDGE AND-gate emit decision 의 사용자(타자) state 가 OTHER-MIND 추정 → emit modulation
- ⇄ [HIVE-MIND](./HIVE-MIND.md): bench G collective coupling (#1147) · partner_state_estimate × pid_synergy multi-partner synergy (H_355)
- ⇄ [UNIVERSE](./UNIVERSE/CANDIDATES.md): bench 측정 기록 SSOT (Session 2026-05-28 — AxisBench 8 + 축 E/F mirror)
