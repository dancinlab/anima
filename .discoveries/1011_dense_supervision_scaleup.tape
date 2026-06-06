@H 1011_dense_supervision_scaleup := "dense per-step supervision is HORIZON-CAPPED-AT-72 — cracks T3@36 (== H_1006) but breaks at 72/144" :: universe [🔴]
  seed = "H_1006 green @36 x H_1005 red curriculum-cap @36 — does credit-density scale?"
  target = "🔴 DENSE-SUP-HORIZON-CAPPED-AT-72 — solved len36 (curr 0.608/0.729 ≫ chance 0.167, d 9.19/10.06), BREAK len72 (curr 0.332/0.386 ≈ LM 0.338, sep lost), collapsed len144; mem-aug=1.0 every length (cap = trainability-at-horizon, not representability); credit-density raises the ceiling but does NOT remove the horizon dependence (refined scaling law over H_1005/H_1006, a_paper_negative_ok)"
  verdict = ".verdicts/1011_dense_supervision_scaleup/h1011.txt"
