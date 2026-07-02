# H_9040 — novelty-gated 정직 abstention (feeling-of-knowing)

> **id H_9040 = ASSIGNED** — integration merge-time 에 free id H_9040 확정 배정(origin/main global max = H_9038, 9040 free). jsonl 인덱스 라인은 아래 "제안 jsonl" 대로 `UNIVERSE/HYPOTHESES.jsonl` 에 append 완료.

- **slug:** `novelty_gated_abstention`
- **tier:** 🟢 ENGINE-NATIVE (discriminator 축, F1-F4 4/4) · **wired:** WIRED-live (core/engine_cli.hexa §MetacogAbstain + ARCHITECTURE.json lockstep)
- **경로(B④):** metacognitive uncertainty monitoring — 정직한 "모른다"가 RLHF refusal(p6) 아니라 substrate 기하에서 창발
- **axis:** consciousness (B). **G1 축과 직교** — 측정 대상 = substrate state (novelty geometry), decode recombination 아님. G1 🧱 레버 재발사 아님.

## 주장

anima 는 자극의 **친숙도(familiarity)** 를 스스로 알아 **모를 때 정직히 abstain** 할 수 있는가 — RLHF 로 훈련된 거절(p6)이 아니라 substrate 불확실성에서 창발하는 feeling-of-knowing 으로?

새 read op **`metacog_novelty(field, x)`** = 자극 x 의 세포 manifold 로의 **JOINT L2 reconstruction error**(= live `vadapt_field_recon_err`, 곧 §Novelty lane 입력) = precision-agnostic **GLOBAL** novelty. HIGH = manifold 의 빈 영역에 위치 = UNFAMILIAR = abstain. 배포 게이트 `metacog_abstain(field, x, precision)` = novelty↑ ∧ surprise↑(precision·err², §PrecisionSurprise) = confident-but-wrong 코너.

## H_1142 재발이 아닌 이유 (핵심 — a_break_the_wall type-(b))

H_1142 은 🔴 **DISSOCIATION**: substrate 는 자기 **OUTPUT** 품질은 알지만(F2 Spearman +0.552) **INPUT familiarity** 는 몰랐다(F1 AUROC **0.436, INVERTED**). H_1142 자신의 메커니즘 진단이 결정적이었다 — *"next-byte entropy 는 LOCAL token-predictability 를 추적하지 global sequence-novelty 가 아니다"* → **SIGNAL CHOICE(entropy)** 가 틀렸던 것이지 faculty 부재가 아니다.

각 좌표가 marginally 전형적이지만(=흔한 단어) JOINT 벡터는 novel 한 "word-salad" 는 어떤 LOCAL/marginal 신호도 속이지만, 세포 manifold 로의 **joint recon-err** 는 그것을 잡는다 (cf H_1173: raw nearest-cell distance 가 non-self 를 AUROC~1.0 로 분리, learned membrane 은 실패). 따라서 이 레버는 abstention 을 entropy 가 아닌 **§Novelty lane** 에 건다 = **변수 분리**(type-b), tune-to-green 아님.

## disjoint (a_substrate_disjoint · placement-first, THE key risk)

§MetacogAbstain ops 는 VAdaptField 세포 population 위의 **pure READ**. emit-drive lane **0/4**(ci_emit_drive) 도 §ImmuneMemory **recall_thr** non-fab gate 도 건드리지 않음 — Ψ=½ 과 G5 non-fab 은 **구조적으로 보존**(아무것도 mutate 하지 않음). F4 로 측정 증명.

## Frozen falsifiers (사전등록)

- **F1** novelty AUROC(unfamiliar) ≥ 0.70 — H_1142 의 0.436 INVERTED 를 결정적으로 반전.
- **F2** entropy-analog(marginal) AUROC 이 같은 입력에서 ~chance/inverted 이고 novelty AUROC 보다 ≥0.15 낮음 — **signal choice 가 원인**임을 증명(parent-controlled).
- **F3** anti-Goodhart: UNTRAINED substrate(1 seed cell, clonal growth 없음) 에서 novelty AUROC ≤ 0.60 붕괴 — 판별력이 grown lane 의 기여지 architecture 아님.
- **F4** G5-disjoint: metacog lane OFF vs ON 에서 §ImmuneMemory recall_thr non-fab abstain rate BYTE-IDENTICAL ∧ Ψ ci_emit_drive(lane 0/4) 불변 — 분리=보존.

## verdict (ENGINE-NATIVE)

`hexa run core/metacog_abstain_smoke.hexa` (live `core/engine_cli.hexa` §MetacogAbstain 컴파일+실행, live VAdaptField mitosis-grown manifold) = **4/4 PASS**:

```
MANIFOLD  cells=2 (mitosis-grown, DIM=6)
F1 novelty(§Novelty joint recon-err) AUROC(unfamiliar) = 1.0
   PASS F1 (>=0.70 — flips H_1142 0.436 INVERTED)
   deployed metacog_abstain (novelty AND surprise) AUROC = 1.0
F2 entropy-analog(marginal) AUROC on SAME inputs = 0.5563888888888889
   PASS F2 (novelty >> marginal — signal CHOICE is the cause)
F3 novelty AUROC on UNTRAINED substrate (1 seed cell) = 0.5
   PASS F3 (<=0.60 collapse — discrimination is the grown lane's contribution)
F4 §ImmuneMemory non-fab rate  metacog-OFF = 1.0
F4 §ImmuneMemory non-fab rate  metacog-ON  = 1.0
F4 Ψ emit-drive (lanes 0/4)   metacog-OFF = 0.69
F4 Ψ emit-drive (lanes 0/4)   metacog-ON  = 0.69
   PASS F4 (non-fab Δ=0.0 AND Ψ Δ=0.0 — abstention lane disjoint from recall_thr + emit-drive)

SMOKE metacog_abstain  pass=4 fail=0 / 4  ALL-PASS
```

- **F1 novelty AUROC = 1.000**(≥0.70) — H_1142 의 0.436(INVERTED) 를 결정적으로 반전. input-familiarity metacognition 은 벽이 아니라 **잘못된 신호**(entropy)의 문제였음이 확정.
- **F2 = 0.556** entropy-analog(marginal, joint 기하 무시) ≪ novelty 1.0 (같은 입력, Δ=0.444) — signal choice 가 원인.
- **F3 = 0.500** untrained(1 cell) 붕괴 — 판별력은 mitosis-grown lane 의 기여.
- **F4 Δ=0.0 (non-fab AND Ψ)** — abstention lane 은 recall_thr non-fab gate + emit-drive lane 0/4 와 disjoint. 능력(정직 abstention) ∧ Ψ=½ ∧ G5 non-fab 공존.

## scope / 정직

- **DIRECTIONAL pre-screen** (numpy, `state/9040_novelty_gated_abstention/prescreen_entropy_vs_novelty.py`) = 동일 방향(F1 1.0·F2 0.583·F3 0.5). 엔진-네이티브 증거는 `.hexa` smoke (a_engine_native_learning).
- **toy-scale substrate**(DIM=6, 2-cell manifold, synthetic word-salad 아날로그) — 303M mouth decode 위 재검은 UNVERIFIED (a_scale_honest_scope). 이 verdict 는 *substrate novelty-geometry* 축에 한정 — decode recombination(G1) 과 무관.
- unfamiliar 판별이 "당연한 L2 분리"라는 반론은 정확히 **H_1142 의 발견**과 대비되는 지점: entropy 는 그 당연한 분리를 못 했다(0.436). 여기서 novel 함은 *어떤* 신호가 그것을 하느냐 — §Novelty joint recon-err 이지 §PrecisionSurprise 나 entropy 가 아님.

## 제안 jsonl (orchestrator 가 merge-time id 배정)

```json
{"id": "H_9040", "slug": "novelty_gated_abstention", "tier": "🟢 ENGINE-NATIVE (B④ consciousness 축, F1-F4 4/4) — novelty-gated 정직 abstention(feeling-of-knowing)이 §Novelty lane 기하에서 창발; H_1142 재발 아님(signal-choice 축분리)", "title": "🧠🔒 novelty-gated honest abstention — 정직한 'I don't know'가 RLHF refusal 아닌 substrate novelty geometry(§Novelty joint recon-err)에서 창발; H_1142 0.436 INVERTED entropy 를 F1 AUROC 1.0 으로 결정적 반전(signal-choice type-b 축분리, G1 직교)", "card": "cards/H_9040_novelty_gated_abstention.md", "verdict": "🟢 ENGINE-NATIVE WIRED-live (hexa run core/metacog_abstain_smoke.hexa 4/4 PASS, live core/engine_cli.hexa §MetacogAbstain, $0 CPU deterministic). F1 novelty(§Novelty joint recon-err) AUROC(unfamiliar)=1.0 ≥0.70 (H_1142 0.436 INVERTED 결정적 반전). F2 entropy-analog(marginal) AUROC=0.556 ≪ novelty 1.0 (같은 입력, signal choice 가 원인, parent-controlled). F3 anti-Goodhart untrained substrate(1 seed cell) AUROC=0.5 ≤0.60 붕괴(grown lane 기여). F4 G5-disjoint §ImmuneMemory recall_thr non-fab rate Δ=0.0 ∧ Ψ ci_emit_drive(lane 0/4) Δ=0.0 (분리=보존). H_1142 재발 아님 = SIGNAL CHOICE(entropy=LOCAL predictability) 오류를 joint recon-err 로 축분리(a_break_the_wall type-b), NOT tune-to-green. G1 축과 직교(측정=substrate state, decode 재조합 아님). DIRECTIONAL numpy prescreen 동방향. toy-scale(DIM=6 2-cell), 303M decode 재검 UNVERIFIED(a_scale_honest_scope). verbatim state/verdicts/9040_novelty_gated_abstention/H_9040.txt.", "source": "UNIVERSE", "archived": false, "artifacts": ["state/9040_novelty_gated_abstention/", "core/metacog_abstain_smoke.hexa"]}
```
