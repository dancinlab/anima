# H_9611 — GN-freeze 절제 = RF-격리 — GN-Freeze Ablation · RF Isolation (fable R3-A1 · R3 · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · lab full 고갈-발산 R3 post-GroupNorm · 사전등록) — source=fable R3-A1
**lane:** BINDING / GroupNorm 전역 bus 채널 (R3 신규 whitespace)
**related:** [[H_9560]] · [[H_9359]] · [[H_9304]] · [[H_9267]] · source: lab full R3 (fable R3-A1)

**아이디어(FIRE-FIRST · 모든 것의 게이트)**: GN μ/σ² 를 상수로 clamp 하면 trunk 가 **엄격히 RF-local** 이 된다. 기존 cement 된 재조합 수치가 전부 불변이면 GN bus 는 아무것도 안 실었고 beyond-RF 는 *스칼라 경로*가 아니라 **경로 자체 없음**으로 격상.
**메커니즘**: `anima-py evaluate <clm> --gn-freeze`(신규 flag · μ/σ²←고정상수 · affine γ/β 무수정). H_9359/H_9304/H_9267 채점셋 재생.
**$0 pre-screen(프리스크린의 프리스크린)**: `--dump-hidden` 한 prefix 로 frozen vs live GN 간 ‖Δh‖≠0 확인 — 0 이면 flag 무력=INSTRUMENT-DEAD 중단.
**판정표**: C1 **양성통제**=live-GN baseline 이 cement 된 수치를 byte-identical 재현(실패=계기死·verdict 없음) · C2 shuffled-far-context. **PASS-inert**: 전 Δ 가 det-noise 내 ⟹ bus 는 readout-무관 ⟹ "beyond-RF 아키텍처 부재"를 **no channel** 로 격상 ∧ [[H_9562]] outside-RF arm 이 **유효 null 이 됨**. **PASS-live**: Δ 존재 ⟹ **모든 far-context verdict 가 GN-confounded** → [[H_9612]] 발화.
**distinct**: 가장 가까운 kill="floor 가 long-range bus 증명"(死). 이건 **역**: bus 를 이용 안 하고 **삭제**해 load-bearing 이었나 시험. RF 무수정이라 H_1584(깊이) 아님.
**verdict-integrity**: inert ⇏ "GN 무용"(정규화자다 · *cross-position 정보*만 inert). 동결상수는 train-set 통계서 **사전등록**, 스윕 금지(스윕=tune-to-green).

## 상태
🔵 PROPOSED — 미실행 사전등록. run 시 위 판정표로. 측정 주장 0(설계). **distinct-from-kills:** 'floor=long-range bus' kill 의 역 — bus 를 삭제해 load-bearing 검정. RF 무수정(H_1584 깊이 아님).
