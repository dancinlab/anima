// .discoveries/lane-p-3b.tape — Lane P ~3B ENGINE arc discovery log
// substrate = Lane P (py+CUDA), recorded SEPARATE from Lane G (forge).

@H s0_serialize_eq := "Stage 0 — .clm v0.3 general (L,E) decoder+serializer byte-eq" :: discovery [d=2026-06-04]
  seed   = "ENGINE decoder hardcoded E=2/L1; a real 3B needs configurable depth/experts"
  finding= "CLM\\x01 v0.2 byte grammar was ALREADY self-describing — generalized block-role assignment with NO byte/magic change; L1/E2 file byte-IDENTICAL to v0.2"
  verdict= "PASS — .verdicts/lane-p-3b/F-CLM-3B-SERIALIZE-EQ.txt (v3==v2 46742B, L4/E6 + L30/E30 roundtrip, GOLDEN exact_eof, ENGINE forward no-regression)"
  target = "🟢 numerical / 🔵 byte-eq formal · landed PR #1753"

@H s1_config := "Stage 1 — genuine ~3B config (NOT a d-only hack)" :: discovery [d=2026-06-04]
  seed   = "scale n_trunk_layers + n_experts + d TOGETHER to ~3e9, state exact param count"
  finding= "d=4096 L=30 E=30 K=3 V=256 = 3,072,954,654 params (3.0730B). trunk 49.1% + experts 49.1% — balanced across d/L/E. nblk=63, n_ext=126. bf16 weights ~6.15GB, +AdamW state ~37GB → needs 80GB H100."
  verdict= "config FROZEN; trainer CLM/train/train_lane_p_3b.py (serialize_v3, train/val split gen-test, periodic ckpt, tokens/param reported)"
  target = "🟢 numerical (param count analytic + v3 topology roundtrip-verified Stage 0)"

@H s1_corpus := "Stage 1 — corpus scale (avoid memorization, honest token/param)" :: discovery [d=2026-06-04]
  seed   = "150MB FAR too small for 3B (Chinchilla ~20 tok/param = ~60GB)"
  finding= "clean-license wikipedia cannot reach 60GB; build LARGEST practical multilingual clean corpus (build_wiki_3b_corpus.py, 12-lang, configurable bytes/lang, NO synthetic padding) + STATE exact token/param ratio honestly (a_scale_honest_scope). undertrained 3B = honest negative."
  verdict= "builder committed; raw corpus built on-pod (Stage 2), sha256 + provenance card recorded with run"
  target = "corpus card + token/param ratio verbatim in Stage 2/3 verdicts"

@H s2_dilation_cap := "Stage 2 — deep-L dilation explosion (OOM) + root-cause cap" :: discovery [d=2026-06-04]
  seed   = "first 3B fire OOM'd at EVERY batch size on an 80GB H100 (bs=1 tried a single 64GiB alloc)"
  finding= "ARCHITECTURE defect: trunk dilation = dilation_base**i = 2**i reaches 2**29 (=5.4e8) at L=30; the causal left-pad (k-1)*dil pads a (1,4096,512) tensor by ~1e9 zeros that see NO real taps. d768 golden never hit it (L=1, max dil 1). FIX = cap dilation=min(2**i,512) IDENTICALLY in model.py + clm_decode.hexa → byte-eq PRESERVED (min(2**0,512)=1 at L=1; cap touches runtime dilation only, not serialized bytes). Post-fix probe: 3.073B trains on one H100, peak 61.5GB, bs=4/seq512 = 3.37 s/step."
  verdict= "byte-eq re-PASS under cap (v3==v2 46742B, GOLDEN exact_eof, L30/E30 roundtrip); fire launched bs=4 accum=2 steps=4000 — .verdicts/lane-p-3b/F-CLM-3B-FIRE.txt"
  target = "🟢 numerical (3-axis generalization result appended on fire completion)"
