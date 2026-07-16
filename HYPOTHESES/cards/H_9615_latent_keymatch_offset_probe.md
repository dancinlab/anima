# H_9615 — latent key-match offset probe — Latent Key-Match Offset Probe ($0 decider) (fable R3-B1 · R3 · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · lab full 고갈-발산 R3 post-GroupNorm · 사전등록) — source=fable R3-B1
**lane:** BINDING / within-RF latent binding
**related:** [[H_9562]] · [[H_9560]] · [[H_9618]] · source: lab full R3 (fable R3-B1)

**아이디어(H_9562 보다 싼 decider)**: trunk 가 **이미** RF 내 offset δ 에서 soft key-match 회로를 갖고 있고, CPT 없이 hidden 서 탐지 가능하다.
**메커니즘**: `--dump-hidden`; held-out 짝을 offset δ∈[1,35] 로 두고 h 가 δ 에서 반복 key 의 match/mismatch 를 shuffled-key null 위로 인코딩하나 시험.
**$0 pre-screen**: **양성통제 먼저** — δ 에서 *문자 그대로의 byte 반복*이 탐지돼야(conv 는 자명히 가능). 안 되면 음성 읽기 전에 probe 사망([[positive-control-before-reading-a-negative]]).
**판정표**: C1 양성(literal-repeat) · C2 shuffled-key null · C3 δ>RF 는 null 이어야. match 구조 > null ⟹ 회로 latent ⟹ [[H_9562]] 는 *capacity* 문제가 아니라 **readout** 문제가 됨. Null ⟹ H_9562 를 카드대로 발사.
**distinct**: 死한 margin/2AFC probe(association *강도* 시험) 아님 — 이건 model-내 null 대비 **표현 구조** 시험.
**verdict-integrity**: **probe hit 을 다리로 승격 절대 금지**(`a_engine_native_learning`) — latent key-match 회로는 커리큘럼이 *착지할 수 있다*는 DIRECTIONAL 증거지 binding 존재 아님. probe-decodable ⇏ engine-used.

## 상태
🔵 PROPOSED — 미실행 사전등록. run 시 위 판정표로. 측정 주장 0(설계). **distinct-from-kills:** margin/2AFC probe kill 아님(association 강도 vs 표현 구조) · H_9562 와 달리 CPT 0.
