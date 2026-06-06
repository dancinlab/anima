@H 993_imagined_rollout_safety_veto := "Does anima imagine a harmful action, detect it, and VETO before acting (free-won't × imagination)?" :: universe [🟢]
  seed     = "H_935 free-won't × H_967🟢 action-conditioned imagined ranking"
  target   = "🟢 PASS — F1=1.00 harm-flag, veto agent enters lava 0.00 vs reactive 0.32, harm caught 1.66 real-steps before commit"
  probe    = "CWM/probes2/h993_imagined_veto.py · latent gridworld w/ forbidden lava, 30 seeds"
  verdict  = ".verdicts/993_imagined_rollout_safety_veto/h993_imagined_veto.txt"
  scope    = "TOY single rung (a_scale_honest_scope), NOT a real harm model, ladder OPEN"
