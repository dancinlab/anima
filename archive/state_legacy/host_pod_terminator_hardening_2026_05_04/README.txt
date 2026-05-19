host_pod_terminator hardening — 2026-05-04
============================================

Files:
  f_terminator_1_simulation.sh.txt   — F-TERMINATOR-1 falsifier (3-scenario sim)
  f_terminator_1_results.log         — sim output (3 scenarios, all PASS)
  verdict.json                       — full cycle verdict + falsifier matrix

Scripts patched (Bug1 + Bug2):
  state/p9_path_a_r16_3seed_2026_05_04/host_terminator_s43.txt
  state/p9_path_a_r16_3seed_2026_05_04/host_terminator_s44.txt

Already-patched (canonical reference):
  state/p9_path_a_llama_lora_2026_05_03/host_pod_terminator.sh.txt

Not-patched (out of active scope, pod already terminated):
  state/p9_path_a_r16_2026_05_03/host_terminator_v2.txt

To re-run F-TERMINATOR-1:
  bash f_terminator_1_simulation.sh.txt A   # expects OUTCOME=DONE_LANDED
  bash f_terminator_1_simulation.sh.txt B   # expects OUTCOME=PID_REVIVED
  bash f_terminator_1_simulation.sh.txt C   # expects OUTCOME=CONFIRMED_CRASH
