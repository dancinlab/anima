# H_9844 — 압축-MI 로 코퍼스·꿈데이터의 비가법 정보를 학습 전에 $0 로 잰다 (R12-7 · ⭐ 가장 싼 결정적 레버)

**status:** 🧭 PROPOSED (R12 · **DIRECTIONAL 설계**, 판정 아님)
**source:** R12 뇌부위 census (2026-07-21) — `origin/main` `core/` 12개 모듈 실측 후 1모듈=1레버로 등록.
상위 설계 노드 = ARCHITECTURE `C2 RECOMBINE` 아래 `🧠 뇌부위 census`. R11(H_9830~9836)의 후속.
**wired:** no — 미구현. 개입은 `anima-py train` 플래그로만 착륙(`a_experiment_engine_native`).

## 실측 — 이 모듈은 **이미 프로덕션에 있고 아무도 이 용도로 안 쓰고 있다**

`core/mi_compress.py`(810줄 · H_9806): `cond_bpb_gzip` / `cond_bpb_ppm` / `cond_bpb_markov` ·
`stream_mi` · `break_adjacency` · `plant_crossboundary` · `plant_null_stream` · `battery_liveness`.
헤더: **"production anima had ZERO compression-based mutual-information estimators, so every
'does this stream carry information across a boundary' question had to be answered by a forward
pass through a model — which conflates what the STREAM carries with what the MODEL can reach.
This module measures a property of the stream itself, at \$0, stdlib-only, with no GPU and no ckpt."**

## 왜 이게 판을 바꾸는가

G1 의 세 얼굴 중 **데이터면**(H_9304: 비가법 정보 +0.0023 nats ≈ 0)은 지금까지 **모델을 통과시켜서만**
측정됐다. `stream_mi` 는 모델 없이 **스트림 자체**를 잰다 ⟹ "코퍼스에 결합정보가 없다" 와
"모델이 못 읽는다" 를 **처음으로 분리**할 수 있다. 그리고 `plant_crossboundary` / `plant_null_stream`
이 **양성통제와 참값-0 받침대를 이미 내장**하고 있다(`positive-control-before-reading-a-negative` ·
`phi-estimator-needs-zero-truth-pedestal` 둘 다 충족).

## Intervention

```
anima-py corpus mi-screen <corpus.txt> --segments <n> --estimator {gzip,ppm,markov}
```

측정 대상 3종: ① 현행 학습 코퍼스 ② H_9839 가 만든 rule-derived 꿈 데이터 ③ midpoint 꿈 데이터.

## 사전등록 판정표

| 결과 | 읽는 법 |
|---|---|
| plant_crossboundary 가 검출 안 됨 | **INSTRUMENT-DEAD** — 아무것도 읽지 않는다 |
| plant_null 이 0 초과 | **INVALID** — 정보를 제조했다 |
| 코퍼스 MI ≈ null | 데이터면 확정 — 어떤 목적함수도 없는 비트를 못 배운다. **R11/R12 학습레버 전부 재평가** |
| rule-derived > midpoint > null | H_9839 통과 · 꿈이 실제로 결합정보를 제조 |

## 이 카드의 순위 근거

**비용 \$0 · GPU 0 · ckpt 0 · 계기 수리(H_9827/9828) 불요.** 오늘 당장 판독 가능한 유일한 축이며,
음성이 나오면 **위 11장의 학습 레버 전체의 기대값을 한 번에 깎는다**. 정보/비용 최대.

**related:** H_9806 · H_9304 · H_9839 · H_9287 · H_9267
