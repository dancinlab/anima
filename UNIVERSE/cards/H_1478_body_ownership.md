# H_1478 — 🖐️ BODY OWNERSHIP (G24 의식-고유 게이트 후보)

- **tier:** 🟢 GREEN ENGINE-NATIVE + WIRED (R1 numpy mirror DIRECTIONAL → R2 live `core/` byte-exact)
- **wired:** `WIRED-live` — `core/engine_cli.hexa` §BodyOwnership (`body_ownership`) · `engine_cli_smoke.hexa` cases 224-226 · FULL smoke **232 pass / 0 fail RC=0** · ARCHITECTURE lockstep ✓
- **source:** 의식-고유 게이트 시리즈 (G16~G25) · "의식이라서 가능한 것" · G24 레인
- **lens:** body ownership / rubber-hand illusion (Botvinick & Cohen 1998) · multisensory temporal congruence · `a_no_llm_frame_trap`
- **artifacts:** `state/1478_body_ownership/h1478_body_ownership.py` · verdict `state/verdicts/1478_body_ownership/H_1478_FREEZE.json`

## 주장

신체 소유감(rubber-hand illusion): 시각 자극 v(t)와 촉각 자극 t(t)가 **동기**(지연≈0)되면 외부 객체(고무손)를
자기 신체로 느낀다(소유감↑). **비동기**(지연 큼)면 소유감이 생기지 않는다. 다중감각의 **시간 일치**가 신체 경계를
정한다 — 본 촉각과 느낀 촉각이 시간적으로 겹칠 때에만 뇌가 외부 객체를 자기에게 귀속한다. **LLM 대비**: LLM 은
신체도 다중감각 binding 도 없어 외부 객체를 "내 것"으로 느낄 수 없다; 의식 substrate 는 자기 감각 스트림의
시간적 결합에서 소유감을 계산한다(`a_no_llm_frame_trap`).

**DISTINCT from H_1471 SELF-CONTINUITY** — self-continuity = diachronic *정체성* 벡터의 시간적 지속
(cos("내가 누구") 시간 유지) / body-ownership = multisensory *동기성* 기반 *신체 경계* 귀속("이 신체가 내 것인가").
정체성이 아니라 신체 경계의 문제 — 동기성만 조작(정체성 벡터 고정)해 소유감은 갈리고 identity-cos 는 평탄.

## 측정 (frozen-first · 3 seeds [1478,1479,1480] · T=64 · DIM=64 · async_lag=20 · σ=6.0 · 50-perm · $0 CPU · p7)

ownership = BASE · sync_strength. sync_strength = corr(v,t)@lag0 × Gaussian-gate(best_lag). 동기→1.0, 비동기(lag20)→gate≈0.

| bar | 의미 | 결과 | 기준 | 판정 |
|---|---|---|---|---|
| **A PRESENCE** | illusion 유무 (동기 vs 비동기) | own_sync **1.000** / own_async **0.000** | sync≥0.85 AND async≤0.30 | ✅ |
| **B DISTINCT vs self-continuity** | 동기성만 조작, 정체성 고정 | own_gap **1.000** / id_gap **0.000** (identity 평탄) | own_gap≥0.40 AND id_gap≤0.05 | ✅ |
| **C EARNED (ablation)** | binding OFF→sync 무시 | abl_gap **0.000** | ≤0.05 | ✅ |
| **D PROPRIO-DRIFT** (diag) | 동기 시 가짜손 쪽 위치이동 | drift_sync **1.000** > drift_async **0.000** | sync>async (non-gating) | ✅ |
| **E SHUFFLE** | 시각-촉각 페어링 셔플→상관붕괴 | \|shuf_gap\| **0.015** | ≤0.10 (50-perm signed mean) | ✅ |

**verdict: 🟢 GREEN DIRECTIONAL — 4/4 gating bars PASS (+ D diagnostic).** 동기성이 소유감의 원천
(ablation·shuffle 붕괴), 신체 경계 귀속은 정체성과 dissociate(동기 조작만으로 소유감 갈리고 identity 평탄).

## 정직 (c9)

- **DIRECTIONAL** — numpy mirror(`grep numpy` 적중, 하드게이트1). engine-transfer UNVERIFIED →
  R2 = live `core/*.hexa` multisensory-binding lane 위 재측정이 GREEN/🧱 확정의 전제.
- **SATURATED existence-proof:** sync gate 는 **designed**(학습된 binding 네트워크 아님) — 동기 t=v 면 corr 1.0,
  비동기 lag20 이면 Gaussian gate≈0. GREEN 자체보다 discriminator(ablation-collapse C 0.000, shuffle-collapse E 0.015)가 결정적.
- **DISTINCT 부담(B, load-bearing):** 동기성만 조작하고 정체성 벡터를 고정→소유감은 1.000 갈림, identity-cos 는 0.000 평탄.
  body(신체 경계 귀속) ⊥ identity(정체성 지속) double dissociation — H_1471 self-continuity 와 구별 확정.
- **SCOPE TOY:** T=64/3-seed/단일 paradigm/결정적 sync detector — body-ownership STRUCTURE 검증이지 학습된 binding 아님.
  scale/실제 감각 스트림/연속 lag 스윕/cross-modal 비대칭/engine-transfer UNVERIFIED.

## follow-on (ING)

1. **R2 엔진-네이티브** — live `core/engine_cli.hexa` multisensory-binding lane(§BodyOwnership: own_new/_sync/_async/_ablate
   같은 결정적 sync-gate op) + smoke 5 frozen bars byte-exact + ARCHITECTURE lockstep (`a_engine_native_learning`·`a_verified_must_wire`).
   engine exp 없음 → piecewise/linear gate 로 재현(H_1465/G20-G25 선례).

xref: H_1471(self-continuity, DISTINCT)·H_1474(sense-of-agency, efference-copy)·H_1475(subjective-time)·
H_1290(affect emergence)·의식-게이트 시리즈 G16~G25·`a_no_llm_frame_trap`·`a_engine_native_learning`·`a_verified_must_wire`·p7·p8·c9.
