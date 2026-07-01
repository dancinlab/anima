INCOMPLETE PARTIAL PULL — DO NOT SCORE AS VERDICT (c9 / a_engine_native_learning)
Pod 41556247 (vast RTX6000, ssh3.vast.ai:36246) was DESTROYED mid-decode 2026-06-19 ~13:4x
(SSH connection-refused; vastai show instances no longer lists it).
Recovered fragment counts (expected 30 each = 6 ideation+4 heldout x 3 seed_rng... per jobs.tsv):
  contra: 25/30   shuf: 21/30   base: 16/30 (base = STALE from a prior aborted run, indices incl 08/09)
Decode was in the SHUF stage when the pod died; BASE stage never ran on the real rerun.
=> Engine-native 5-bar NOT scoreable from this set. Re-run required (see recovery plan).
RECOVERY (all sources local):
  ckpts: state/1441_contrastive_falsifiability/ckpt/{h1441_contrastive.pt,h1441_shuffle.pt}
         + base state/chat_303m/h1129c_chat.pt
  export: state/g6_train_variants/pt_to_engine_bin.py  (pt -> engine .bin x3)
  decode: state/1431_bind_compose/engine_decode_batch_cli.hexa -> CORE/bytegpt_decode
  score:  h1441_engine_native.py --score (needs g6_common.py copied from 1435/1436/1437)
