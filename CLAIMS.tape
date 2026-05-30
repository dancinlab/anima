@V := "tape" :: spec [active]
  version = "1.2"

@I := "claims-index" :: identity [active]
  brief = "Single audit index of verifiable anima claims (a_claim_manifest)."
  flow  = "claim → hexa verify (g5) → .verdicts/<slug>/<id>.txt → /paper gate (a_paper_gate)"

# Method legend (a_claim_verify):
#   atom        — `hexa verify --expr <fn> <n> <v>` (atlas atom recompute → 🔵)
#   expr        — `hexa verify --expr <fn> <n> <v>` (numerical recompute → 🟢)
#   run         — ckpt / sim run, verdict = closure_auto_judge stdout (empirical)
#   hypothesis  — UNIVERSE/H_xxx terminal verdict, persisted verbatim
#
# Gate (a_paper_gate): every section claim must be terminal —
#   🔵 formal / 🟢 numerical / 🔴 CLOSED-negative. No 🟠 / 🟡 residual.
# Groups (a_paper_one_per_group): LIFE · PURE · CHAT — one canonical paper each.

# ───────────────────────────────────────────────────────────────────────
# CHAT — chat-init-ce-floor (slug · group=CHAT · paper-track)
# init cross-entropy floor of an untrained CLM = ln(vocab_size).
# Positive formal result — H_247 §C4.

@C chat_init_ce_floor := "init_CE floor = ln(151936) = 11.931214658529285 (untrained CLM lower bound)" :: formula [slug=chat-init-ce-floor group=CHAT]
  method = "expr"
  cmd    = "hexa verify --expr ln 151936 11.931214658529285"
  raw    = ".verdicts/chat-init-ce-floor/chat_init_ce_floor.txt"
  src    = "UNIVERSE/H_247_init_ce_catastrophic_floor.md §C4"
  status = "🟢 SUPPORTED-NUMERICAL — ln calculator landed (hexa-lang #1128), verdict persisted, atlas-absorbed (g69, node @F verified-ln-num · hexa-lang #1131). /paper-eligible."

# ───────────────────────────────────────────────────────────────────────
# PURE — pure-corpus-axis-closed-negative (slug · group=PURE · paper-track)
# Closed-negative (a_paper_negative_ok): the corpus dilution axis alone
# cannot close multilingual register-coherence — ruled out across the
# full wiki_frac sweep {0.0, 0.5, 1.0}.

@C pure_wiki_sweep := "wiki_frac sweep {0.0,0.5,1.0} — multilingual closure 4/5 ≥ PARTIAL never reached" :: run [slug=pure-corpus-axis-closed-negative group=PURE]
  method = "run"
  cmd    = "hexa run HEXAD/PURE/eval/closure_auto_judge.hexa (E2 · E3 · v3)"
  raw    = ".verdicts/pure-corpus-axis-closed-negative/closure.txt"
  src    = "PURE.log.md 2026-05-25 · state/pure_phase_d_v3_result_2026_05_24/"
  status = "🔴 CLOSED-negative — corpus-axis ⊥ multilingual closure (verdict persisted)"

@C pure_register_orthogonal := "register_hits=0 at wiki_frac=0 (TTR 0.34) yet coherence stays WEAK — corpus-axis ⊥ multilingual closure" :: run [slug=pure-corpus-axis-closed-negative group=PURE]
  method = "run"
  cmd    = "hexa run HEXAD/PURE/eval/multilingual_probe.hexa (v3 ckpt)"
  raw    = ".verdicts/pure-corpus-axis-closed-negative/register.txt"
  src    = "UNIVERSE/H_242 §A2 (H242.1 FULL-COLLAPSE falsify)"
  status = "🔴 CLOSED-negative — corpus-axis ⊥ multilingual closure (verdict persisted)"

# wiki_frac=0.3 intermediate point (P21H V3, recovered SIGHUP-orphan run).
# closure_auto_judge 1/4 PASS · FAIL: register_collapse PASS (0 hits) yet all
# 5 langs WEAK. Adds the 0.3 sweep point → closed-negative now holds at
# {0.0, 0.3, 0.5, 1.0}. The F-CURRICULA-1 (wiki=1.0 curriculum-mix) re-fire
# was LOST at step 3000/5000 (pod wfeksdl8e8f327 self-terminated); its
# endpoint is already covered by pure_wiki_sweep / anima-v3-e3.
@C pure_wikifrac03_closed_negative := "wiki_frac=0.3 — register_collapse PASS (0 hits) yet all 5 langs WEAK · closure FAIL 1/4" :: run [slug=pure-corpus-axis-closed-negative group=PURE]
  method = "run"
  cmd    = "hexa run HEXAD/PURE/eval/closure_auto_judge.hexa state/p21h_v3_recover_2026_05_25/out_main/result.json"
  raw    = "state/p21h_v3_curricula_recover_2026_05_25/closure_verdict_wiki03_verbatim.txt"
  src    = "state/p21h_v3_recover_2026_05_25/ · HF dancinlab/anima-p21h-v3-wikifrac03-recovered-2026-05-25 (PRIVATE)"

# ───────────────────────────────────────────────────────────────────────
# CLM — P0 falsifier pre-registration (group=CLM · paper-track)
# 5 pre-registered falsifiers from CLM/P0_ARCHITECTURE.md §4. F-CLM-AKIDA-MAP
# is a P0-now structural subset check (verified subset 🔵 + honest router gap);
# the other 4 are 🟠 PRE-REGISTERED with frozen thresholds (P2/P3 fire pending).
# UNIVERSE H_847..H_851. NOT /paper-eligible until terminal (a_paper_gate).

@C clm_akida_map := "CLM 추론 path conv/FC/sepconv/maxpool/int4-quantizer ⊆ AKD1000 byte-identical envelope (🔵 subset) · MoE router softmax+topK argmax 는 envelope 밖 (정직 gap)" :: hypothesis [slug=clm-akida-map group=CLM]
  method = "hypothesis"
  cmd    = "structural subset check vs HEXAD/CHAT/server/akida_sw_lif.py + akmap_step_probe.hexa (step=2^(ib-ab) MATCH=true)"
  raw    = ".verdicts/848_clm_akida_map/F-CLM-AKIDA-MAP_structural.txt"
  src    = "UNIVERSE/H_848_clm_akida_map.md · CLM/P0_ARCHITECTURE.md §0·§2·§4"
  status = "🔵 SUPPORTED-FORMAL (conv/FC/sepconv/maxpool/int4 subset byte-identical ⊆ envelope) ⚠ HONEST-GAP (router softmax+argmax envelope 밖 · fake full-PASS 0 · resolution=argmax-hard or off-chip router)"

@C clm_monopoly_escape := "byte-vocab(V=256) conv-native MoE monopoly escape: distinct_experts>1 ∧ routing z>3.0 ∧ content z>3.0 ∧ seed{base,43,44} 재현" :: hypothesis [slug=clm-monopoly-escape group=CLM]
  method = "hypothesis"
  cmd    = "P2 3-arm × ladder PyTorch fp full-fire → closure_auto_judge (PENDING)"
  raw    = ".verdicts/847_clm_monopoly_escape/F-CLM-MONO_prereg.txt"
  src    = "UNIVERSE/H_847_clm_monopoly_escape.md · CLM/P0_ARCHITECTURE.md §3·§4 · H_666"
  status = "🟠 PRE-REGISTERED — P2 full-fire 미실행 · frozen threshold (d6 z>3.0 양축 + multi-seed). NOT terminal."

@C clm_quant_int4 := "QAT int4 round-trip ppl 열화 < 임계 (naive PTQ int4 readout 파괴 실증 대비)" :: hypothesis [slug=clm-quant-int4 group=CLM]
  method = "hypothesis"
  cmd    = "P3 .clm QAT int4 round-trip ppl 측정 (PENDING)"
  raw    = ".verdicts/849_clm_quant_int4/F-CLM-QUANT_prereg.txt"
  src    = "UNIVERSE/H_849_clm_quant_int4.md · CLM/CLM_FORMAT_SPEC.md §1·d2"
  status = "🟠 PRE-REGISTERED — P3 미실행 · threshold frozen at P3 entry. NOT terminal."

@C clm_scale_ladder := "monopoly-escape 가 scale ladder rung(tiny/small/target) 따라 유지 (전이곡선) — distinct_experts>1 ∧ dual-axis z>3.0 per rung" :: hypothesis [slug=clm-scale-ladder group=CLM]
  method = "hypothesis"
  cmd    = "P2 multi-rung ladder full-fire → 전이곡선 (PENDING)"
  raw    = ".verdicts/850_clm_scale_ladder/F-CLM-SCALE_prereg.txt"
  src    = "UNIVERSE/H_850_clm_scale_ladder.md · CLM/P0_ARCHITECTURE.md §4·§5 · H_666(toy🟢scale🔴)"
  status = "🟠 PRE-REGISTERED — P2 multi-rung 미실행 · per-rung threshold frozen. NOT terminal."

@C clm_mitosis_growth := "MoE cell-pool 성장 (p8 train=infer) — |cell_pool(t_end)|>|cell_pool(t_0)| + born_step·parent lineage 영속" :: hypothesis [slug=clm-mitosis-growth group=CLM]
  method = "hypothesis"
  cmd    = "P2 학습 trajectory split_log / cell_pool lineage (PENDING)"
  raw    = ".verdicts/851_clm_mitosis_growth/F-CLM-MITOSIS_prereg.txt"
  src    = "UNIVERSE/H_851_clm_mitosis_growth.md · CLM/CLM_FORMAT_SPEC.md §2 · p8 · v5-mitosis"
  status = "🟠 PRE-REGISTERED — P2 미실행 · growth+lineage threshold frozen. NOT terminal."

@C clm_mitosis_array_dispatch := "MITOSIS-ARRAY DISSOLVE: scale=expert-COUNT 시 inter-expert dispatch entropy z(E) 단조 상승 ∧ z(64)−z(4)≥1.0 ∧ 전 expert chip-fit" :: hypothesis [slug=clm-mitosis-array-dispatch group=CLM]
  method = "run"
  cmd    = "python3 CLM/model/run_array_sweep.py (E∈{4,8,16,32,64} × seed{42,43,44} · Dirichlet(1) null z-score)"
  raw    = ".verdicts/852_clm_mitosis_array_dispatch/F-CLM-MONO-ARRAY_p_array_2026_05_30.txt"
  src    = "UNIVERSE/H_852_clm_mitosis_array_dispatch.md · CLM/P0_ARCHITECTURE.md §11 · CLM.breakthrough.mining.md DISSOLVE"
  status = "🔴 CLOSED-NEGATIVE — P-ARRAY 완료. raw H 는 E 로 상승(1.19→3.17 nats) 하나 uniform-null 대비 z 급락(+0.53→−7.61) · monotone+z-rise FAIL · chip-fit PASS. 사전등록 frozen 임계 무변조(a_paper_negative_ok). TERMINAL."

@C clm_bridge_transfer := "MITOSIS-ARRAY BRIDGE: teacher(E32/d128) escape 가 KD distill 후 chip-fit student(E8/d64) 로 transfer 생존 — z same-sign ∧ |Δ|≤3.0 ∧ student chip-fit" :: hypothesis [slug=clm-bridge-transfer group=CLM]
  method = "run"
  cmd    = "python3 CLM/distill/run_bridge_transfer.py --fire (teacher train → Hinton KD distill → transfer Δ z, ubu-1 RTX5070)"
  raw    = ".verdicts/853_clm_bridge_transfer/F-CLM-BRIDGE-XFER_fire_2026_05_30.txt"
  src    = "UNIVERSE/H_853_clm_bridge_transfer.md · CLM/P0_ARCHITECTURE.md §11.4·§11.6 · CLM.breakthrough.mining.md BRIDGE"
  status = "🔴 CLOSED-NEGATIVE — BRIDGE fire 완료. teacher z 음수(-3.74) · student distill 후 near-uniform(+0.60) · transfer Δ +4.34 > 3.0 · 2/3 seed sign-flip · student chip-fit PASS. monopoly-escape ⊥ KD-transfer (a_paper_negative_ok). HF dancinlab/anima-clm-bridge PRIVATE. TERMINAL."

# ───────────────────────────────────────────────────────────────────────
# LIFE — open slot (group=LIFE · paper-track)
# Candidate canonical claim — NOT yet verdict-persisted. List here so the
# audit surface tracks it; promote to paper only after a_claim_verify
# persists a terminal verdict to .verdicts/<slug>/.
#
# @C life_<id> := "<claim>" :: hypothesis [slug=life-<slug> group=LIFE]
#   method = "hypothesis"
#   cmd    = "hexa verify <atom-id>   # or closure_auto_judge for empirical"
#   raw    = ".verdicts/life-<slug>/<id>.txt"
#   src    = "UNIVERSE/H_xxx_*.md §<verdict>"

# ───────────────────────────────────────────────────────────────────────
# CLM — clm-array-stage2-scale (slug · group=CLM · paper-track)
# Closed-negative (a_paper_negative_ok): PRODUCTION scale (d>=512, real kowiki)
# does NOT flip the toy 🔴🔴 — MITOSIS-ARRAY DISSOLVE (Pielou J) + BRIDGE
# (dispatch-KL transfer) are falsified at production scale; both gaps WIDEN.
# Hypothesis "scale=expert-count dissolves the measure⊥chip conflict" is now
# deterministically CLOSED across toy AND production. H_854.

@C clm_pielou_dissolve_prod := "PRODUCTION Pielou J=H/ln(E) FELL with E (0.806→0.532), J-rise −0.27364 < 0 — DISSOLVE falsified at d=512 real kowiki" :: run [slug=clm-array-stage2-scale group=CLM]
  method = "run"
  cmd    = "python3 CLM/model/run_array_sweep_stage2.py (ubu-1 RTX 5070, d_model=512, real kowiki @corpus clm_p1, NULL_SAMPLES=16)"
  raw    = ".verdicts/854_clm_array_stage2_scale/F-CLM-PIELOU-DISSOLVE-PROD.txt"
  src    = "UNIVERSE/H_854_clm_array_stage2_scale.md §5 (AXIS-A) · sibling H_852"
  status = "🔴 CLOSED-negative — production scale amplifies the toy 🔴 (toy J-rise −0.093 → prod −0.27364); thresholds FROZEN, NOT tampered (verdict persisted verbatim)"

@C clm_dispatchkl_xfer_prod := "PRODUCTION dispatch-KL escape transfer mean|Δ|=13.84 > 3.0, 3/3 seed sign-flip (teacher z≈−12 → student z≈+1) — BRIDGE transfer falsified at d=512" :: run [slug=clm-array-stage2-scale group=CLM]
  method = "run"
  cmd    = "python3 CLM/distill/run_dispatch_kl_stage2.py (ubu-1, teacher E32/d512 → student E8/d128, real kowiki, NULL_SAMPLES=16)"
  raw    = ".verdicts/854_clm_array_stage2_scale/F-CLM-DISPATCHKL-XFER-PROD.txt"
  src    = "UNIVERSE/H_854_clm_array_stage2_scale.md §5 (AXIS-B) · sibling H_853"
  status = "🔴 CLOSED-negative — escape does NOT transfer; Δ widened vs toy (3.51 → 13.84) and vs round-1 (4.34); student chip-fit held; thresholds FROZEN (verdict persisted verbatim)"
