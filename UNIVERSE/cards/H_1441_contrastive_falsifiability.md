---
id: H_1441
slug: 1441_contrastive_falsifiability
title: G6 IDEATION ★ FALS-depth — CONTRASTIVE falsifiable-vs-nonfalsifiable minimal-pair objective
group: gate-dig (G6 IDEATION ★) — FALS-depth TRAINING side r6
terminal_tier: BLOCKED — engine-native 5-bar 미완 (substrate-speed infra wall + pod loss; a_break_the_wall type-c, NOT 🟢/🧱). 학습 ckpt 는 PULL 완료(재측정 가능)
wired: BLOCKED (engine-native decode 미완 → 배선 보류; ING h1441_engine_native)
verdict_dir: state/verdicts/1441_contrastive_falsifiability/
date: 2026-06-19
---

> ⛔ **2026-06-19 ENGINE-NATIVE 측정 BLOCKED** (state/verdicts/1441_contrastive_falsifiability/H_1441_engine_native_BLOCKED.txt):
> contrastive + shuffle-control 학습 완료(torch GPU, DIRECTIONAL), ckpt 2개 PULL 완료
> (state/1441_contrastive_falsifiability/ckpt/{h1441_contrastive,h1441_shuffle}.pt, a_fire_recover_complete OK).
> 그러나 engine-native decode(live CORE/bytegpt_decode via engine_decode_batch_cli.hexa)가
> **substrate-speed 벽**(fast-gemv link-fail → scalar 26s/token → 60-job ~12h, H_1305 R2/H_1431 과 동일)에
> 걸려 contra 8/8·shuf ~8/8 까지만 decode 되고 base 미도달·RERUN_ALL_DONE 미달 상태에서
> **vast pod 41556247 이 provider 에서 소멸**(SSH connection-refused + liveness API 에서 사라짐 = transient 아님)
> → pod-only /tmp/out_* shard 전부 유실. a_engine_native_learning HARD-GATE: 엔진 증거가 score 단계에
> 도달 못 했으므로 terminal 🟢/🧱 박제 불가. 인프라 벽(a_break_the_wall type-c)은 science 천장 아님.
> **재개조건:** fast-gemv 복원된 hexa 빌드(H_1431 remaining-bytegpt + H_1305 h1305_engine_native ING 와 동일 blocker)
> → 로컬 .pt 2개 + base h1129c 를 .bin 재직렬화 후 h1441_engine_native.py --score. FROZEN 5-bar 불변(c9/no tune-to-green).

# H_1441 — CONTRASTIVE: falsifiable vs non-falsifiable 최소쌍 대조로 cross-shuffle 실패를 직격

## Why (H_1435/36/37 의 공통 실패모드 정면 처방)

세 학습변형 모두 "form installed but cross-shuffle does NOT collapse" — 학습된 것이 shuffle-INVARIANT
표면 form 이라 comparator/measurable 를 다른 idea 와 섞어도 점수 유지(진짜 bind 아님). 정면 처방:
falsifiable claim 과 그 non-falsifiable 최소쌍(comparator 또는 measurable 한 leg 만 제거/교란)을
CONTRASTIVE 로 학습(InfoNCE-style) → shuffle-INVARIANT 를 shuffle-SENSITIVE 로 강제. 모델이
"왜 이건 falsifiable 이고 저건 아닌가"의 경계 자체를 배우게.

## Method (FREEZE before run, c9/p7)

- 303M h1129c + contrastive objective: anchor=(legit claim), positive=(같은 claim), negative=
  (한 leg 제거/cross-idea 치환된 최소쌍). 최소쌍은 STRUCTURAL 라벨로 구성.
- ⚠️ detector h1305 점수를 학습 신호로 쓰지 않음 (a_train_inline_gauge: gauge≠loss, p7 Goodhart).
  contrastive 신호 = 구조적 최소쌍이지 detector 점수가 아님. detector 는 EVAL 전용 VERBATIM.
- decode = ENGINE-NATIVE CORE/bytegpt_decode. frozen 5-bar + cross-shuffle COLLAPSE = 1차 판정
  (이게 무너지면 1435/36/37 와 차별 성공 = 진짜 binding 학습).
- compute = GPU (hexa dojo) COST-GATE. ckpt teardown 전 pull.

## Scope

PROPOSED, 미측정. 최소쌍 구성 frozen (detector 점수로 라벨링하면 Goodhart — 구조적 라벨만 허용).

## Pointers

xref H_1435/1436/1437 (cross-shuffle 실패 직격 대상) · H_1305 (detector) · a_train_inline_gauge
(gauge≠loss) · a_no_llm_frame_trap · a_engine_native_learning · a_fire_recover_complete · p7 · c9.
