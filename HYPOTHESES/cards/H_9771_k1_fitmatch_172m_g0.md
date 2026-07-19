---
id: H_9771
group: faction-lateral-axis-r3
series: R9 divergence (lab full · Fable 5 λ3 · H_9643 de-risk 후속) · 2026-07-18
date: 2026-07-18
slug: k1_fitmatch_172m_g0
title: K=1@≈172M fit-match 대조런 — G0 붕괴가 capacity 인가 파벌구조인가의 유일 판별자 (~$6 · 조건부)
status: PROPOSED · DIRECTIONAL design (lab-full divergence) · FIRE 조건 = H_9769 격차 REAL ∧ H_9770 GREEN
tier: 🔵 R9-3 · ~$5-6 (H100 pod 1 · 172M 급이라 de-risk 보다 싸거나 같음)
cost: ~$6
source: Fable 5 divergence — 브리핑 Q1/Q2. 넓히기(K=8→346M)가 아니라 **좁히기(K=1→172M)** 가 clean 한 방향
related: H_9643, H_9769, H_9770, H_9772
---

# H_9771 — K=1 fit-matched 172M 대조런 (2×2 의 빠진 한 칸)

## 왜 좁히기인가 (Q2 판정)
- 현재 2×2 중 {K=1@346M, K=8@172M} 두 칸만 있음 — confound 판별엔 **K=1@172M** 한 칸이면 충분.
- 넓히기(K=8→346M, d≈5352=8·669)는 기계적으론 됨(GN·bridge 안 깨짐)이나 **interpretively dirty**: 추가 param 이 비-grouped d² 모듈(bridge proj·MLP·MHA)에 몰려 파벌-lane capacity 는 거의 안 늘고, d 자체가 변해 GN 폭·최적화 regime 이 2번째 knob 으로 움직인다. 비용도 1.4-2×. 기각.
- U(비-grouped)≈131-147M 가 d² 급(실측 분해: K=1 346M − K=8 172M ⇒ groupable C≈199-215M)이라 전-계수 √2 스케일이 근사 성립: **d′ = 3784·√(172/346) ≈ 2669** → 후보 d=2664 or 2672 (8 배수). ⚠️ fire 전 constructor `num_params()` 로 k8_s7 실측 param 과 **정확 일치 확인 필수** (√ 휴리스틱은 근사 — 브리핑의 "d≈5350=√2" 산수도 같은 이유로 근사일 뿐).

## recipe (정확 복제 · d 만 교체)
retrain.log recipe: L=4 emax=4 seq=1024 bs=16 steps=15000 savant mitosis@7500 · 4-cell 125MB · tokens 245.76M · seed7 · `--n-factions 0`.

## 읽기 (H_9769 계기 재사용 · n≥20)
- K=1@172M G0 **PASS** → capacity 무죄 → **파벌구조가 coherence 대가** — 브리핑 Q5 의 verdict 문장이 이때 비로소 earned.
- K=1@172M G0 **FAIL** → capacity confound 확정 → 파벌 무죄 + **K=8 CE-parity(172M=346M val_CE)가 효율 양성으로 승격**. 이후 K=8@172M vs K=1@172M 는 param-matched 쌍 — H_9770 lesion 의 param-matched 보강 arm 겸용.

## 이중 효용
이 런은 (a) Q1 판별 (b) 계기 v2 인증이 요구하는 fit-matched K=1 음성 arm 의 303M 판 — 두 역할을 한 번에 한다.
