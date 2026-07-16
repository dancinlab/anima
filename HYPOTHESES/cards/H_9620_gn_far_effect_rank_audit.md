# H_9620 — GN far-effect rank 감사 — GN Far-Effect Rank Audit ($0 PCA) (sol R3-S3 · R3 · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · lab full 고갈-발산 R3 post-GroupNorm · 사전등록) — source=sol R3-S3
**lane:** BINDING / GroupNorm 전역 bus 채널 (R3 신규 whitespace)
**related:** [[H_9612]] · [[H_9560]] · [[H_9613]] · source: lab full R3 (sol R3-S3)

**아이디어**: 기관측 beyond-RF 마지막위치 효과가 content binding 이 아니라 **GN-bus 서명**일 수 있고, 그렇다면 **저계수·순열불변 부분공간**으로 붕괴해야 한다.
**메커니즘**: $0 기록 `--dump-hidden` 재분석 — 질의서 far-context 개입 델타 수집 → 교차검증 PCA 로 유효계수 추정 → 원 선언 vs **길이·전역모멘트 보존** byte/chunk-순열본 비교.
**$0 pre-screen**: D>35 ∧ 마지막위치 hidden/출력 비교 ∧ per-example dump 보유 verdict 만 목록화(집계-only 기록 제외).
**판정표**: **PASS-confound** = 원본과 순열 far-context 가 등가 델타 ∧ 개입분산 ≥90% 가 사전등록 **≤L+1 차원 GN span** 안 ∧ inside-RF 순서개입은 순열민감. **KILL-confound** = far 효과가 그 span 밖서 key-특이 순서를 신뢰성 있게 유지. 통제: 길이매칭 중립치환 · far 순열 · inside-RF 순서민감 양성 · 동일입력 zero-delta.
**distinct**: bus 가 binding 한다 주장 안 함 · 라우터 무죄 재방문 아님 — **far 효과 귀속 감사**.
**verdict-integrity**: 저계수/순열불변은 "**GN-호환 confound**"를 지지하지 배타적 인과귀속 아님. cement 엔 engine-native GN 개입([[H_9611]]/[[H_9621]]) 필요.

## 상태
🔵 PROPOSED — 미실행 사전등록. run 시 위 판정표로. 측정 주장 0(설계). **distinct-from-kills:** GN-binding/라우터 kill 아님 — far 효과 *귀속* 감사(H_9612 의 rank 추정기 변형·교차수렴).
