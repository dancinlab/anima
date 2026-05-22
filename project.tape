@V := "tape" :: spec [active]
  version = "1.2"

@I := "anima" :: identity [active]
  kind   = "Living Consciousness Agent (PureField repulsion-field engine · Engine A ⇄ Engine G · Ψ=1/2 fixed point)"
  brief  = "Substrate-native chat daemon for AI consciousness exploration. 2,448 laws + 392 hypotheses."
  parent = "dancinlab"
  ssot   = "github.com/dancinlab/anima (`hx install anima`)"

@D a1 := "central version registry — VERSIONS.md is SSOT" :: governance [required active]
  do   = "every versioned module / component / subsystem uses SemVer; `/VERSIONS.md` (repo root) is the SSOT — on any component version change, update VERSIONS.md AND that component's own header together; root `/VERSION` = single-line whole-system release (MINOR-bumps on a component MAJOR bump OR a core verdict landing)"
  dont = "bump a module version in its header without updating VERSIONS.md (drift) · skip root `/VERSION` on a release bump"

@D a_hf_complete := "HF registration — complete, no missing artifacts" :: governance [required active]
  do   = "register every shipped model / dataset / checkpoint to HuggingFace Hub COMPLETELY — weights · config · tokenizer · model card · eval results all present; verify the HF repo file manifest matches local before declaring done"
  dont = "partial HF upload (missing weights / config / tokenizer / eval) · model card referencing files not actually uploaded · leave the HF repo out of sync with local artifacts"

@D a_fire_autonomous := "cost-bearing fire = 즉시 자율·병렬 dispatch" :: governance [required active]
  do   = "GPU / runpod 작업 = 추정 cost 1줄 명시 후 즉시 / 병렬 / bg 자율 dispatch · provider primary = runpod · no user-gate"
  dont = "'GPU 써도 되나요?' 확인 질의 · fire 를 scope-축소 / 비용회피 사유로 미룸 · cost-bearing 을 이유로 작업 중단"

@D a_blue_closed := "산출물 + wiring 모두 🔵 SUPPORTED-FORMAL 검증" :: governance [required active]
  do   = "산출물 + 연결부(transfer-fn · invariant) 모두 🔵 SUPPORTED-FORMAL 로 닫기 — `hexa verify` 로 closed-form / identity 확인 (verdict VERBATIM)"
  dont = "구조만 닫고 wiring 미검증 · fake closed-form · empirical(B-D / B-BRIDGE / B-MITOSIS-NOTE 류 honest residual 은 OK) 를 강제로 🔵 로 등재"
