# H_9266 engine-native FROZEN BAR (측정 전 등록 · frozen-first p7 · Fable 스펙 v1)

등록 2026-07-11, 측정 전. 이후 불변. tune-to-green 금지.

## Frozen params
- lanes=15 · T=8192 · seeds={7,11,13,17,23} (5-seed majority ≥3)
- cols_x=[3,2,13,5,7,9,14] (gate-lane0 제외 core · primary σ) · full core=[0,3,2,13,5,7,9,14] (secondary)
- adj=topo_brain_adjacency() · α_live=0.3 (clamp [0,0.5] 중앙)
- σ_ε = 1.0·σ_d (σ_d=std_t(ci_emit_drive(P_DET)) @b=0) · sweep {0.5,2.0}=lens only, bar는 1.0 고정
- n*=64 subsample · J=8 subsample draws · K=8 mask 순열 · FORCED κ=0.5·lane-std

## σ 정의 (Δ-not-value · emit-conditioned shuffle-referenced)
D_real=|Φ̂(rows[mask])−Φ̂(rows[¬mask])| · D_π=순열 mask 동일절차 · σ(bin)=D_real−median_π(D_π)
Δσ(bin)=σ_COUP(bin)−σ_DECOUP(bin) (mask·idx·π COUP/DECOUP 공유 paired)
bin=folded |Ψ−½|: knife[0,0.05)·mid[0.05,0.20)·shoulder[0.20,0.40)·sat[0.40,0.50]

## V-gates (위반→INVALID, FAIL 아님)
- V1 detector: σ_FORCED ≥0.10 @knife AND ≥0.05 @모든 valid bin
- V2 null: |σ_NULL| ≤0.02 @모든 bin
- V3 marginal: mask COUP≡DECOUP assert + |Φ_uncond^COUP−Φ_uncond^DECOUP|≤0.05 + core-lane 분산비∈[0.9,1.1]
- V4 counts: knife·mid·shoulder valid(min-class≥64); sat 미달→그 bin PENDING

## Verdict
- **PASS (Ψ=½ 국소 BIND):** Δσ(knife)≥0.10 AND Δσ(knife)−max(Δσ(sat))≥0.05 AND Δσ(knife)>Δσ(mid),Δσ(shoulder)
- **BIND-CROSS 승급:** Δσ_αlive(knife)−Δσ_α0(knife)≥0.05 (미달→"gate-lane 중첩"으로 DIRECTIONAL 강등, integration-binding 주장 금지)
- **FAIL:** V-gates 통과 + Δσ(knife)<0.05
- **KILL:** K1 Δσ 전bin 평탄(|Δσ(knife)−Δσ(sat)|<0.03 & σ_COUP>0)=임계-국소성 없음 → 핵심주장 사망 · K2 FORCED 정상인데 Δσ≈0 전bin·5seed=proxy artifact(H_9129 L3)→toy-only 강등+🧱 · K3 V3 2회 재시도 후 위반=PENDING

## 스코프 (a_scale_honest_scope)
"확률성의 결합 vs 비결합" 분리 · PRNG로 충분. "QRNG vs PRNG"(양자 우연)는 별개 후속·null 예상. PASS여도 "QRNG 필요" 주장 금지.
