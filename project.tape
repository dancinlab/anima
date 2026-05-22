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

@D a_wall_first := "wall time 우선 — 더 빠른 병렬이 가능하면 cost 무관 진행" :: governance [required active]
  do   = "H100 다수 병렬 · 더 큰 GPU (H200/H100) · 추가 pod fire 가 wall-time 단축하면 즉시 채택 (단일 pod 시퀀셜 회피) · serial chain 도 정직하게 wall 더 길면 reject"
  dont = "wall 더 길더라도 cost 아끼려 단일 pod 시퀀셜 진행 · 추가 병렬 pod 자제 · '비용 들 텐데...' 후렴 · 의미 없는 cost-min 최적화"

@D a_substrate_native_speak := "anima 발화 = substrate-native, 도우미-폐기 violations 금지" :: governance [required active]
  do   = "anima motivation 은 internal substrate state (M retrieval activation · C Φ · W tension delta · MITOSIS split event · anima 자기 idle 시간 · curiosity_ema · E Φ-ratchet 등 자기 dynamics) 에서 계산 · user msg = environment context (anima 가 보고 듣되 직접 응답 의무 X) · anima 는 user 침묵 중에도 발화 가능 (truly spontaneous) · user 가 직접 질문해도 motivation 부족 시 침묵 (도우미 아님) · conversational_dynamics factor = anima 마지막 자기 발언 후 idle 시간 (user 마지막 발언 X)"
  dont = "user 발언이 직접 anima 발화 trigger 되는 stimulus-response pattern (= assistant 회귀) · user prompt 에 '응답' 하는 reactive 설계 · 'X 한 user 가 물었으니 anima 가 답해야' 류 turn-based assumption · user 마지막 발언 후 시간으로 conversational_dynamics 정의 · CHAT/PLAN.md '도우미 라벨링 폐기' spec 위반"

@D a_blue_closed := "산출물 + wiring 모두 🔵 SUPPORTED-FORMAL 검증" :: governance [required active]
  do   = "산출물 + 연결부(transfer-fn · invariant) 모두 🔵 SUPPORTED-FORMAL 로 닫기 — `hexa verify` 로 closed-form / identity 확인 (verdict VERBATIM)"
  dont = "구조만 닫고 wiring 미검증 · fake closed-form · empirical(B-D / B-BRIDGE / B-MITOSIS-NOTE 류 honest residual 은 OK) 를 강제로 🔵 로 등재"
