# H_9771 — capacity vs topology 판별: K=1@172M param-match (~$6)

**status**: PROPOSED (R9 · H_9643 후속 · H_9769 REAL 확정 시에만 fire)

## 설계
2×2(K∈{1,8} × params∈{172M,346M})의 빠진 칸 = **K=1@172M**. Fable 채택: K=8 을 346M 로 **넓히면** 여분 param 이 non-grouped(MHA/MLP/bridge d²급)로 몰려 파벌-lane capacity 거의 안 늘고 d 가 2nd knob → dirty·1.4-2× 비용. 대신 **K=1 을 d≈2669(→2664/2672·8배수)로 좁혀** 172M param-match(clean·~$5-6). ⚠️ fire 전 constructor `num_params()` 로 k8_s7 실측치 정확일치 검산(√ 휴리스틱 근사).
정확 recipe(bs16 emax4 15k savant mitosis 동일4-cell) 유지.
## bar (H_9770 lesion 결과와 교차)
- K=1@172M G0 FAIL ⟹ **capacity 주원인**(K=8 CE-parity 는 "절반 param 동일 CE" 효율 양성으로 승격).
- K=1@172M G0 PASS ⟹ **파벌 topology 주원인**(K=8 이 구조적으로 coherence 대가).

**Sol dissent(1줄)**: Sol 은 반대로 K=8 d≈5376 넓혀 346M 을 권고(K=8@346M G0≥4/5=capacity·≤2/5=topology) — Fable 의 non-grouped-누수 model.py 실독으로 기각·narrow 채택.
