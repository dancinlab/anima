# H_9619 — readout-only 게이트 — RF Readout-Only Gate (freeze-trunk) (sol R3-S2 · R3 · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · lab full 고갈-발산 R3 post-GroupNorm · 사전등록) — source=sol R3-S2
**lane:** BINDING / within-RF latent binding
**related:** [[H_9618]] · [[H_9562]] · source: lab full R3 (sol R3-S2)

**아이디어**: within-RF 짝이 **이미 표현돼 있는데 안 읽힐 뿐**이면, **native byte readout 만** 재학습해도 full CPT 보다 훨씬 싸게 Cartesian-held-out binding 이 회복돼야 한다.
**메커니즘**: 신규 `anima-py train --freeze-trunk --train-readout-only --rf-paired-bridge`; [[H_9562]] 와 **같은 선언-이식 DV** 로 평가.
**$0 pre-screen**: [[H_9618]] PASS 시에만 발사 · 학습가능 파라미터명이 **기존 readout 뿐**이고 동결 텐서가 전후 hash-identical 임을 정적 검증.
**판정표**: PASS = held-out inside-RF 이식 추적이 H_9562 의 ≥10/12 충족 ∧ outside/postquery 를 ≥4/12 초과(≥2 seed). **KILL-readout** = 양성(훈련짝 readback) 통과하나 held-out 이식이 wrong-key·outside arm 과 TOST-등가. 통제: D≥64 · wrong key · postquery · 양성 seen-pair readback.
**distinct**: H_1584 는 깊이 변경 · H_9329/H_9359 는 store 훈련 — 이건 "**표현은 있고 readout 이 없다**"를 격리.
**verdict-integrity**: PASS 는 이 ckpt 서 trunk 학습 불요를 반증. **KILL 은 H_9562 를 대체 안 함**(trunk 가 여전히 회로를 학습할 수 있음).

## 상태
🔵 PROPOSED — 미실행 사전등록. run 시 위 판정표로. 측정 주장 0(설계). **distinct-from-kills:** H_1584(깊이)·H_9329/9359(store 훈련) 아님 — '표현 있음·readout 없음' 격리.
