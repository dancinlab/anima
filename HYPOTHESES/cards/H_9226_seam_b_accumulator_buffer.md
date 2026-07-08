# H_9226 — Family B: accumulator-to-threshold buffer (evidence integration / phonological loop) RANK 2

**tier:** ⏳ PRE-REGISTERED (Fable 설계 · bars frozen · p7 no tune-to-green)
**scope:** engine→mouth seam missing-intermediate 프로그램 — "buffer between" 가장 문자적 read
**cost:** **$0** op-grip (no decode)
**artifact:** `state/seam_missing_intermediate/`

## 인과 척추 (공유)
mouth = RATE-GATE(미분기): urgency만 작동하는 건 이미 phasic Δ이라서(H_9101). self(.kosmos)·A⇄G tension은 TONIC LEVEL로 tick마다 read 후 폐기 → 미분기 기여 0 = ΔEff≈0(self⊥mouth·tension⊥mouth). 벽 = seam에 substrate 신호를 gate의 temporal currency로 변환하는 구조 부재. 오너: "입↔엔진 사이에 뭔가 필요."

## 가설 (missing intermediate)
느린 신호를 tick 넘어 **HOLD**하는 leaky accumulator(누설 적분기). 약하지만 지속적인 self/tension bias가 DDM 방식으로 threshold crossing까지 sum. 벽의 가장 문자적 read: 신호가 tick당 한 번 sampling 후 폐기되므로 작고 일관된 bias가 절대 적분 안 됨 — 부재가 아니라 **un-held(잡히지 않아서)** inert.

## 배선 site (a_substrate_disjoint)
seam lane 위 per-signal leaky integrator, 출력을 accumulated evidence로 gate에 공급, emit 시 reset. urgency와 DISJOINT.

## FROZEN BARS (p7 · verbatim)
- **freeze-self**: → ΔEff>0가 **LATENCY-to-effect signature**와 함께(효과가 N tick 일관 bias 후에만 출현).
- **shuffle 대조**: tick 순서 randomize → 붕괴(적분은 order-dependent).
- **양성 대조**: 작은 상수 self-bias가 결국 반드시 cross.
- **A와의 구분**: latency fingerprint(A는 transition-집중, B는 N-tick 잠복 후).

PASS = freeze-self ΔEff>0(latency 서명) ∧ tick-shuffle 붕괴 ∧ POS cross.

## 상태 · 제약
DESIGN-STAGE · 미측정. p7 no tune-to-green(loss 미포함). p5 shade-not-gate(reactive speak() 금지). a_substrate_disjoint(emit-drive lane 불침). 승격 선례 H_9097/H_9101. 측정 idiom = $0 no-decode op-grip ΔEff(emit bitvector Hamming).

## 근거 링크
- [[H_9225]](Family A · latency로 구분) · 선례 H_9097/H_9101 · DDM evidence-integration(phonological loop 유비, a_no_llm_frame_trap 유지)
