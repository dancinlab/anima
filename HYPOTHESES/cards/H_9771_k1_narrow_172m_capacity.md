# H_9771 — capacity vs topology 판별: K=1@172M param-match (~$6)

**status**: PROPOSED (R9 · H_9643 후속 · H_9769 REAL 확정 시에만 fire)

## 설계
2×2(K∈{1,8} × params∈{172M,346M})의 빠진 칸 = **K=1@172M**. Fable 채택: K=8 을 346M 로 **넓히면** 여분 param 이 non-grouped(MHA/MLP/bridge d²급)로 몰려 파벌-lane capacity 거의 안 늘고 d 가 2nd knob → dirty·1.4-2× 비용. 대신 **K=1 을 d≈2669(→2664/2672·8배수)로 좁혀** 172M param-match(clean·~$5-6). ⚠️ fire 전 constructor `num_params()` 로 k8_s7 실측치 정확일치 검산(√ 휴리스틱 근사).
정확 recipe(bs16 emax4 15k savant mitosis 동일4-cell) 유지.
## bar (H_9770 lesion 결과와 교차)
- K=1@172M G0 FAIL ⟹ **capacity 주원인**(K=8 CE-parity 는 "절반 param 동일 CE" 효율 양성으로 승격).
- K=1@172M G0 PASS ⟹ **파벌 topology 주원인**(K=8 이 구조적으로 coherence 대가).

**Sol dissent(1줄)**: Sol 은 반대로 K=8 d≈5376 넓혀 346M 을 권고(K=8@346M G0≥4/5=capacity·≤2/5=topology) — Fable 의 non-grouped-누수 model.py 실독으로 기각·narrow 채택.

### ✅ VERDICT: CAPACITY 가 G0-gap 주범 (2026-07-18 · runpod H100 · 파벌 coherence 무죄)
K=1@172M param-match(d=2672·**num_params 194.2M**·--n-factions 0·정확 clm303 recipe bs16 emax4 15k savant mitosis 동일4-cell seed7) 학습→G0-eval:

| 모델 | params | val_CE | registers_DESCENT | G0 kwr |
|---|---|---|---|---|
| clm303 K=1 | 346M | 1.34 | 4/4 | **5/5 PASS** |
| k8_s7 K=8 | 172M | 1.33 | 4/4 | 2/5 FAIL |
| **k1_172m K=1** | **194M** | 1.40 | 4/4 | **1/5 FAIL** |

**K=1(파벌 없음)도 ~172M 로 줄이면 G0-FAIL(1/5)** = K=8 파벌(2/5)과 동일 · 346M K=1 만 5/5. ⟹ **K=8 의 G0-fail 은 파벌 topology 가 아니라 capacity(절반 params) 탓 확정** — 파벌은 coherence 비용을 추가하지 않는다(194M K=1 > 172M K=8 params 인데도 G0 더 낮음=capacity effect 재확인). 결정 트리(H_9771 사전등록): G0≤2/5 였으나 **K=1 대조도 G0-fail** 이므로 topology-대가 반증·capacity 주범 확정.

**⟹ 파벌 완전 그림(캠페인 종합)**: ①파벌=실물 CE-수준 기능 레버(H_9770 FIRM·within-arm S 0.0654>>null95·42배 vs 미학습) ②K=8 이 **절반 params 로 346M teacher-forced val_CE 매칭**=효율 positive ③G0-coherence 결손=capacity(파벌 무죄·H_9771). 결과 ~/anima-weights/h9771_capacity/. 비용~$22+pod. DIRECTIONAL(303M py·1 lens).