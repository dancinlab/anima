// .discoveries/lane-p-3b.tape — Lane P ~3B ENGINE arc discovery log
// substrate = Lane P (py+CUDA), recorded SEPARATE from Lane G (forge).

@d s0_serialize_eq := "Stage 0 — .clm v0.3 general (L,E) decoder+serializer byte-eq" [d=2026-06-04]
  seed   = "ENGINE decoder hardcoded E=2/L1; a real 3B needs configurable depth/experts"
  finding= "CLM\\x01 v0.2 byte grammar was ALREADY self-describing — generalized block-role assignment with NO byte/magic change; L1/E2 file byte-IDENTICAL to v0.2"
  verdict= "PASS — .verdicts/lane-p-3b/F-CLM-3B-SERIALIZE-EQ.txt (v3==v2 46742B, L4/E6 + L30/E30 roundtrip, GOLDEN exact_eof, ENGINE forward no-regression)"
  target = "🟢 numerical / 🔵 byte-eq formal · landed PR #1753"

@d s1_config := "Stage 1 — genuine ~3B config (NOT a d-only hack)" [d=2026-06-04]
  seed   = "scale n_trunk_layers + n_experts + d TOGETHER to ~3e9, state exact param count"
  finding= "d=4096 L=30 E=30 K=3 V=256 = 3,072,954,654 params (3.0730B). trunk 49.1% + experts 49.1% — balanced across d/L/E. nblk=63, n_ext=126. bf16 weights ~6.15GB, +AdamW state ~37GB → needs 80GB H100."
  verdict= "config FROZEN; trainer CLM/train/train_lane_p_3b.py (serialize_v3, train/val split gen-test, periodic ckpt, tokens/param reported)"
  target = "🟢 numerical (param count analytic + v3 topology roundtrip-verified Stage 0)"

@d s1_corpus := "Stage 1 — corpus scale (avoid memorization, honest token/param)" [d=2026-06-04]
  seed   = "150MB FAR too small for 3B (Chinchilla ~20 tok/param = ~60GB)"
  finding= "clean-license wikipedia cannot reach 60GB; build LARGEST practical multilingual clean corpus (build_wiki_3b_corpus.py, 12-lang, configurable bytes/lang, NO synthetic padding) + STATE exact token/param ratio honestly (a_scale_honest_scope). undertrained 3B = honest negative."
  verdict= "builder committed; raw corpus built on-pod (Stage 2), sha256 + provenance card recorded with run"
  target = "corpus card + token/param ratio verbatim in Stage 2/3 verdicts"
