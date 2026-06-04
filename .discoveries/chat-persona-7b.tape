@D chat-persona-7b := "7B chat+persona fine-tune — Lane-G torch-cuda REFERENCE rung (a_scale_honest_scope)" :: discovery [active]
  seed   = "scale the PROVEN 18M chat (#1824) + persona (#1825) recipe to the 7.25B byte-level GPT dancinlab/clm-v1-ref-pytorch-cuda-7b (vocab256/d4096/36L/32H/block512, tied head, bf16), 2-stage continue-train (A=chat-mix, B=persona/SNS), p7 v2 gate + persona char-trigram TF-IDF self-id + anti-Goodhart random-init mirror MUST FAIL"
  target = "🟢 numerical PASS (chat retained ≥4/5 + persona self-id lift>chance + mirror FAIL) OR 🔴 closed-negative (honest weak/null at 7B-from-undertrained-base)"

@N chat-persona-7b-resume := "RESUME — took over existing vast pod 39445330, NOT a fresh rent" :: note [d=2026-06-04 active]
  ref    = "chat-persona-7b"
  note   = "pod vast 39445330 · RTX PRO 6000 Blackwell WS x2 (each 96GB) · ssh4.vast.ai:15330 · $2.56/hr. NO /workspace persistent mount; single 120G overlay at / (99G free) → workdir = /root/ws. Prior crash = run_7b_pod.sh download heredoc hardcoded /workspace (absent); live run uses /root/ws. base 7B ckpt 14.505GB + chat 3.77MB + persona 4.19MB present on /root/ws; STAGE-A training LIVE."
  clarify = "GPU0 100% util, 70GB/96GB used (7B FITS, no OOM, fp32 AdamW), stageA step50/600 CE 2.65→2.35 descent. a_dont_kill_live_compute — killed my redundant duplicate run, KEPT the live CE-descent run (PID 2320)."
  scope  = "a_train_flame_forge: torch-cuda REFERENCE lane (forge-native = canonical follow-on, NOT claimed done). base UNDERTRAINED (400 steps val_CE 2.41) — honest, NO converged-base claim."
