# H_9802 — BRIDGE RETENTION — 강제체제서 형성된 다리를 자연텍스트로 anneal 했을 때 생존·모집되는가 ($0 telemetry 선검사)

**tier:** 🔵 PROPOSED · DESIGN-ONLY (lab-full R11 divergence · DIRECTIONAL · NOT a verdict)
**group:** R11-natural-emergence
**source:** lab full 2026-07-19 — Fable A3 ≈ Sol #3(alias-coreference) 수렴, telemetry 선검사는 Fable 고유
**wired:** no
**verdict:** PENDING (설계만 · 측정 0 · cement 는 engine-native `anima-py` 로만)

## claim
NATEM(자연 코퍼스 자발창발)은 🧱 이나, '강제체제서 형성 → 소수부하 유지한 채 자연텍스트로 anneal' 은 미측정. 질문 = 보존(retention) ∧ 모집(recruitment): 다리가 anneal 을 견디는가, 그리고 자연텍스트 질의가 그 다리로 라우팅되기 시작하는가.

## instrument
선행 $0: `anima-py evaluate <H_9775-ckpt> --store-telemetry`(MONITOR-only·a_train_inline_gauge·loss 미진입) 로 자연텍스트 store-hit mass 측정 → hit≈0=모집 문제 / hit>0+값 garbage=정렬 문제로 실패양태를 사전 분리(맹목 발사 금지). 본발사: `anima-py train --corpus natural.txt --corpus-mix synth:natural=<schedule> --store-fuse pairodd`.

## controls (사전등록)
양성: λ=1.0 순합성 arm 이 H_9775 수준 ≥0.90 유지(계기생존) · 음성(i) --store-fuse none 으로 anneal ⟹ 자연측 지표 무변동(자연텍스트 단독 배제) · 음성(ii) λ=0 순자연 arm = NATEM 재현, 이건 통제지 주장 아님 · cpt-destroys-what-corpus-omits 대비 rehearsal 분율 λ(t) 1.0→~0.05

## falsify
합성 held-out D-acc 가 anneal 중 붕괴 ∧ 자연측 hit-mass Δ 가 fuse-none 통제와 등가(TOST) ⟹ 다리는 강제체제 전용, 자연이관 불가.

## cost
선검사 $0 → 본발사 ~$10–20 (a_wall_first: λ-schedule 2개 max, 트랙당 전용 호스트 1)

## 정직 caveat (c9)
이 카드는 **방향성 설계**이지 검증된 결과가 아니다. lab-full 발산 산출 = DIRECTIONAL, 절대 verdict 아님
(`a_lab_full_diverge`). frozen bar 사후 이동 금지(tune-to-green 금지 · p7). 발사 전 **toy e2e 1회**
(exit 0 + 산출물 + 통제) 필수 — 한 번도 실행 안 된 계기는 버그 여럿 겹쳐 숨긴다
(`instrument-never-run-hides-multiple-bugs`). 음성도 결과다.

## related
H_9775 · H_9267 · H_9802
