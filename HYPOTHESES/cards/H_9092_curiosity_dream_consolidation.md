# H_9092 (PLACEHOLDER id — 제안 H_9070, orchestrator merge-time 배정) — 미해결 호기심이 dream에서 어떤 앵커가 replay·compose되는지를 편향 (curiosity×dream 응고우선순위)

- **tier:** 🟢 ENGINE-NATIVE (6/6 live hexa) — unresolved-호기심 우선순위 replay/compose op 신설·측정. 선택 분포(selection distribution) 편향, G1-orthogonal.
- **slug:** `curiosity_dream_consolidation`
- **parents:** D11 삼중합류(curiosity·dream·consolidation) · §Amygdala ConsolidatingMemory(sleep-replay, H_1285) · §DreamSchema(H_9044 dream_schema_mint) · §Novelty(H_1468 R2b) · §PrecisionSurprise(H_1468 R2) · a_chat_sleep_imagination(REM 5-stage) · a_substrate_disjoint
- **wired:** `engine-native` — op이 live `core/engine_cli.hexa §CuriosityDreamBias`에 배선(6/6 falsifier PASS). 데몬 REM 루프로의 runtime-integration + §CuriosityBacklog(feat/curiosity-backlog-emit 착지 후) unresolved-score drop-in은 follow-on(WIRED-live 최종칸).

## frame (생물렌즈 — a_no_llm_frame_trap)

해마 **prioritized replay**: 수면 응고는 중요-**미해결(unresolved)** 기억을 우선적으로 재생한다(Wilson & McNaughton 1994 reactivation; Ólafsdóttir 2018 prioritization). live 엔진의 §Amygdala ConsolidatingMemory는 이미 salience tag(surprise+novelty+tension)로 replay를 편향하지만, 그 salience는 **encode-time에 고정(정적)** — 앵커가 지금도 얼마나 **미해결**인지를 추적하지 못한다. D11은 그 gap을 채운다: 삼중합류(호기심·꿈·응고)를 하나의 op-slot으로.

## op (신설, additive · Ψ-disjoint · READ-only) — `core/engine_cli.hexa §CuriosityDreamBias`

- `curiosity_priority(recon_err, precision, pred_err, resolved) -> float` — ONGOING unresolved 드라이브. **main 기존 lane 재사용**: §Novelty joint recon-err(아직 unfamiliar=미해결) + §PrecisionSurprise `surprise`(=precision·err², confidently-violated=끌림), `resolved`(응고/recall 횟수)로 decay. 새 store 無.
- `curiosity_replay_draw(priorities, budget, rng, biased) -> [int]` — 한 번의 REM replay pass: `budget`회 draw 후 per-anchor replay-count 벡터. biased=∝priority(prioritized) / uniform(ablation). inverse-CDF, §Amygdala replay와 동일 LCG. READ-only(count 반환, mutation 無).
- `curiosity_shuffle(priorities, rng)` — **F2 control**: unresolved 신호를 앵커 간 permute(deterministic Fisher-Yates), 분포 동일·앵커↔중요도 decorrelate.
- `curiosity_resolve(priority, replay_count, rate) -> float` — **F4 converge**: replay 많이 된 앵커의 priority를 감쇠(응고가 해소 → 미래 pull↓, prioritized-replay 루프 폐합).
- `dream_compose_biased(episodes, priorities, top_k, budget, rng, biased) -> [float]` — **D11 op**: biased replay 후 가장 많이 재생된 top_k 앵커를 §DreamSchema `dream_schema_mint` **centroid**로 compose(압축, anti-G1). biased=false ⇒ uniform(어떤 앵커가 compose되는지 curiosity-독립 = ablation).

> §CuriosityBacklog(feat/curiosity-backlog-emit 미착지)의 unresolved score가 나중에 `priorities` 입력으로 **그대로 drop-in**(draw/compose op 무변경). 지금은 main §Novelty/§PrecisionSurprise로 근사 — bias는 **설계된 법칙(designed law)**, 창발 주장 아님.

## 측정 (engine-native, `hexa run` via live core/, $0, CPU, deterministic, 6/6 PASS)

FROZEN toy(a_scale_honest_scope · existence-proof): DIM=6, N=12(6 hi-unresolved + 6 lo), budget=600, LCG seed=12345. `state/verdicts/D11_curiosity_dream_bias/H_9092.txt` verbatim. probe = `state/D11_curiosity_dream_bias/d11_engine_native.hexa`.

| falsifier | readout | bar (frozen) | 결과 |
|---|---|---|---|
| **F1 PRIORITY** | hi_share_biased = **0.927** | ≥ 0.70 | 🟢 PASS (biased replay가 미해결 버킷에 집중) |
| **F1b COMPOSE** | L2(schema_biased, μ_hi)=**0.043** < uniform **0.971** | biased < uniform | 🟢 PASS (dream이 미해결 앵커를 compose) |
| **F2 CONTROL** | hi_share_shuffled = **0.36** (lift 0.567) | biased − shuffled ≥ 0.15 | 🟢 PASS (신호가 구동, raw budget 아님) |
| **F3 ABLATION** | hi_share_uniform = **0.508** ≈ 0.5 | \|·−0.5\|≤0.10 ∧ biased−uniform≥0.15 | 🟢 PASS (bias가 load-bearing, uniform INERT) |
| **F4 CONVERGE** | Σpriority_hi **2.656→0.467** ∧ night-2 hi_share **0.133** < 0.927 | Σ↓ ∧ night2<night1 | 🟢 PASS (replay가 resolve → pull↓) |
| **F5 DISJOINT** | Ψ emit-drive Δ=**0.0** ∧ §ImmuneMemory non-fab Δ=**0.0** | 둘 다 = 0.0 | 🟢 PASS (분리=보존) |

## disjointness 증명 (substrate-disjoint, placement-first)

curiosity lane ON vs OFF에서 `ci_emit_drive`(Ψ lanes 0/4) = 0.69 byte-identical ∧ §ImmuneMemory recall_thr non-fab rate = 0.833 byte-identical (F5). 모든 op은 plain float 벡터 위 순수 READ-only — cell을 mutate하지도, emit/honesty path가 읽는 무엇도 쓰지 않음 → Ψ=½·G5 non-fab이 **구조적으로** 보존. **분리=보존.**

## HONEST scope (c9)

- bias는 **설계된 법칙** — "미해결 신호가 replay를 편향한다"는 창발적 발견이 아니라, 그렇게 편향하도록 배선한 op의 자기일관성 + EARNED control(F2/F3) 통과 주장.
- **G1-orthogonal**: 측정 = replay/compose **선택 분포**이지 텍스트 재조합 아님. compose 산출물은 centroid(압축), 새 내용 mint 아님(anti-G1, H_9044와 동일 규율).
- **toy existence-proof**: DIM=6/N=12/budget=600 — scale-transfer 미검증(a_scale_honest_scope). production 앵커 규모 재검 필요.
- **wired: engine-native** (6/6 smoke), 데몬 REM 루프 runtime-integration + §CuriosityBacklog unresolved-score drop-in은 미배선 follow-on.

## 제안 jsonl 라인 (placeholder — orchestrator가 merge-time에 실제 id 배정)

```json
{"id": "H_9070", "slug": "curiosity_dream_consolidation", "tier": "🟢 ENGINE-NATIVE (6/6 live hexa)", "title": "Curiosity×dream consolidation-priority: unresolved-curiosity biases which anchors dream-replay/compose", "card": "cards/H_9092_curiosity_dream_consolidation.md", "verdict": "🟢 ENGINE-NATIVE 6/6 — §CuriosityDreamBias(curiosity_priority/replay_draw/shuffle/resolve/dream_compose_biased) on live core/engine_cli.hexa. F1 hi_share_biased=0.927 · F1b compose L2 0.043<0.971 · F2 shuffled=0.36 · F3 uniform=0.508 ablation-INERT · F4 Σpri 2.656→0.467 converge · F5 Ψ/non-fab Δ=0.0 disjoint. bias=designed law, G1-orthogonal, toy scope.", "source": "UNIVERSE", "archived": false, "artifacts": ["state/D11_curiosity_dream_bias/d11_engine_native.hexa", "state/verdicts/D11_curiosity_dream_bias/H_9092.txt"]}
```
