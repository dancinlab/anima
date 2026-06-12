@H 995_wm_as_imagined_critic := "Can the WM be its own critic — pick actions from imagined value, no env reward (Dreamer)?" :: universe [🔴]
  seed     = "H_967🟢 imagined ranking GIVEN returns + H_980🟢 policy-implicit — does LEARNED imagined value act?"
  target   = "🔴 FAIL (closed-neg) — imagined-value beats random (d=1.34) but LOSES to reactive greedy (d=−0.80); rank-corr 0.57; rollout drift corrupts value"
  probe    = "CWM/probes2/h995_wm_as_critic.py · latent reward-landscape, 24 seeds"
  verdict  = ".verdicts/995_wm_as_imagined_critic/h995_wm_as_critic.txt"
  scope    = "TOY single rung (a_scale_honest_scope), ladder OPEN; a_paper_negative_ok; cf H_991 drift"
