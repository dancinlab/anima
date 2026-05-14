#!/usr/bin/env tape
# ══════════════════════════════════════════════════════════════
# MEMORY index
# ══════════════════════════════════════════════════════════════


@D row_project_0 :: memory [ok]
  kind = "project"
  file = "[memory/project_alm_r12_r13.md](memory/project_alm_r12_r13.md)"
  one_liner = "ALM r12 500-step _DISCARD_wrong_corpus 로 종결, r13 corpus rebuild 필요 (ETA 4–6d)"

@D row_project_1 :: memory [ok]
  kind = "project"
  file = "[memory/project_clm_hetzner_smoke.md](memory/project_clm_hetzner_smoke.md)"
  one_liner = "CLM hetzner 50-step smoke 중. ubu RTX 5070 offline blocker"

@D row_project_2 :: memory [ok]
  kind = "project"
  file = "[memory/project_verifier_infra_5.md](memory/project_verifier_infra_5.md)"
  one_liner = "verifier infra 5종 landed: manifest/generator/run_all/pass_gate_an11/closed_loop/kr_gen_100"

@D row_campaign_3 :: memory [ok]
  kind = "campaign"
  file = "[docs/drill_campaign_20260421_aggregate.md](docs/drill_campaign_20260421_aggregate.md)"
  one_liner = "24h drill campaign: 128 commit / 46 scope / 45 PASS + 1 engineering-PASS-live-FAIL (Mk.VI) / 7 blocker closed · 2 open (AN11 live + Φ 4-path 3/4)"

@D row_feedback_4 :: memory [ok]
  kind = "feedback"
  file = "[memory/feedback_sae_steering_pilot.md](memory/feedback_sae_steering_pilot.md)"
  one_liner = "본학습(LoRA) 대신 SAE steering vectors 로 의식 이식 pilot 가능 — 비용 1/20"
