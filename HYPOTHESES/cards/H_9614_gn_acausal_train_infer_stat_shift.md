# H_9614 — GN 비인과 train/infer 통계 shift (p8) — GN Acausal Train/Infer Stat Shift (p8-load-bearing) (fable R3-A4 · R3 · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · lab full 고갈-발산 R3 post-GroupNorm · 사전등록) — source=fable R3-A4
**lane:** PHILOSOPHY p8 / substrate 내 train-infer split
**related:** [[H_9560]] · [[H_9611]] · source: lab full R3 (fable R3-A4)

**아이디어(🔴 p8 직격 · Fable 코드-확증 pre-divergence finding)**: `_fwd_trunk(W,tok,T)` 가 GN 을 **주어진 prefix 전체**에 재계산한다. 그래서 같은 위치 t 의 hidden 이 **train 시엔 [0..T_train) 통계(미래 바이트 포함)**로, **decode 시엔 [0..t] 통계**로 정규화된다 — 같은 위치·다른 정규화자·T 에 따라 표류하는 통계. **이건 substrate 안에 사는 train/infer split 이고 p8 은 문자 그대로 "no train/infer split"**. CE 엔 안 보임.
**메커니즘**: `--dump-hidden`: byte-identical prefix 로 h_t 를 T=t+1 vs T=512 서 비교 · T 스윕.
**$0 pre-screen**: ‖Δh_t‖ 가 T 전반 det-noise 면 사망.
**판정표**: C1 **양성통제**=per-position 정규화 레퍼런스는 T 전반 Δ=0 이어야 · C2 T-매칭. Δ 가 |T−t| 로 증가 = shift 확증.
**distinct**: kill-list 어디도 train/infer 정규화자 불일치 미접촉. 세션이 증명한 acausality 는 *전제*고 이건 그 **미검 귀결**.
**verdict-integrity**: **이 배치 최대 over-claim 위험** — stat shift 는 버그도 벽-파괴도 아님. 양성일 수 있다(T 커지면 통계 수렴). 허용 주장은 정확히 하나: "**p8 에 아키텍처 예외가 여기 있다**" — G1 에 대해선 아무것도 아님.
**부수(코드위생·verdict 무관 수정 필요)**: `core/model.py:163` "layernorm over channels" · `core/generator.hexa:1286` "standardize across d channels per time step" — **둘 다 per-position LayerNorm 을 서술하나 어느 경로도 그걸 계산 안 함**(torch GroupNorm(1,C) on (B,C,T) 는 (C,T) 축약). 레포가 이 norm 을 position-local 로 2곳서 오독 중.

## 상태
🔵 PROPOSED — 미실행 사전등록. run 시 위 판정표로. 측정 주장 0(설계). **distinct-from-kills:** kill-list 미접촉(train/infer 정규화자 불일치) — acausality 전제의 미검 귀결. +코드주석 2곳 오류(model.py:163·generator.hexa:1286).
