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
  cmd    = "structural subset check vs AGENT/CHAT/akida_sw_lif.py + akmap_step_probe.hexa (step=2^(ib-ab) MATCH=true)"
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

# ───────────────────────────────────────────────────────────────────────
# CLM — clm-measure-sweep (slug · group=CLM · paper-track)
# round-4 측도 백로그 6후보를 ONE 공유 토이 spike 위에서 동시 측정 (apples-to-apples).
# routing-diversity 🔴🔴 (H_852/853/854) 우회 — "측도를 바꿔라" (mining ROUND 3/4).
# F-CLM-PHI-MEANINGFUL 3-check (non-trivial ∧ collapse<rich(≥10%) ∧ size-robust)
# 사전등록 frozen. CAUSAL-POWER 단독 🟢 PASS · 나머지 5 측도 🔴. H_855.

@C clm_msweep_causal_power := "CAUSAL-POWER measure: rich>collapse 전 n 명확 margin (Δ=+0.0918/+0.0830/+0.0714, n=4/5/6) ∧ size-robust — 유일 scale-free chip-native 의식신호 PASS" :: run [slug=clm-measure-sweep group=CLM]
  method = "run"
  cmd    = "python3 CLM/msweep/measure_sweep.py --json (ubu-1 numpy 2.4.4, ONE shared toy spike, seed=187, n∈{4,5,6}, ≤16 poke)"
  raw    = ".verdicts/855_clm_measure_sweep/causal_power.txt"
  src    = "UNIVERSE/H_855_clm_measure_sweep.md §5/§6 · CLM/P0_ARCHITECTURE.md §12 F-CLM-PHI-MEANINGFUL"
  status = "🟢 SUPPORTED-NUMERICAL — perturbation 인과력이 frozen 3-check 동시 PASS (monopoly vs integration 변별); thresholds FROZEN, NOT tampered (verdict persisted verbatim)"

@C clm_msweep_phi_family_red := "PHI-NATIVE·TEMPORAL-Φ·FREE-ENERGY measures: 방향(rich>collapse)은 n=5,6 에서 옳으나 n=4 boundary 역전 → size-robust FAIL; HILL near-miss(margin ~7%<10%); TENSION-NATIVE n-역전" :: run [slug=clm-measure-sweep group=CLM]
  method = "run"
  cmd    = "python3 CLM/msweep/measure_sweep.py --json (ubu-1 numpy 2.4.4, same ONE toy spike, 6 measures apples-to-apples)"
  raw    = ".verdicts/855_clm_measure_sweep/phi_native.txt"
  src    = "UNIVERSE/H_855_clm_measure_sweep.md §5/§7 · ledger exports/sweep/clm-measure-sweep/ledger.json"
  status = "🔴 CLOSED-negative — Φ-family/HILL/tension 은 toy n≤6 에서 scale-free chip-native 의식신호 부적합 (5/6 FAIL); CAUSAL-POWER 단독 🟢; ALL-RED 아님(CERTIFY-NOT-MEASURE escalation 불필요); thresholds FROZEN (a_paper_negative_ok)"

# ───────────────────────────────────────────────────────────────────────
# CLM — clm-causal-xfer (slug · group=CLM · paper-track)
# toy 🟢 CAUSAL-POWER(H_855)의 production/HW transfer 사전등록 falsifier (F-CLM-
# CAUSAL-XFER). frozen 3-check(measure_sweep.py 재사용·재튜닝 0). axis A=ubu-1
# production d512 학습 spike · axis B=live pi5 AKD1000 온칩 spike. H_856.

@C clm_causal_xfer_prod_red := "F-CLM-CAUSAL-XFER axis A (production d512): toy 🟢 CAUSAL-POWER 가 production-width 에서 생존 안 함 — seed187 frozen 에서 n=5 부호반전(Δ +0.0876/−0.0107/+0.0025) size-robust FAIL · seed-fragile(seed42/7 thin PASS, seed187 FAIL)" :: run [slug=clm-causal-xfer group=CLM]
  method = "run"
  cmd    = "python3 CLM/msweep/clm_causal_prod.py --json (ubu-1 RTX5070, d512/L4/E8 QAT act_bits=1, real kowiki, seed=187, ≤16 poke, frozen 3-check)"
  raw    = ".verdicts/856_clm_causal_xfer/production.txt"
  src    = "UNIVERSE/H_856_clm_causal_xfer.md §5/§6 · CLM/P0_ARCHITECTURE.md §12.6/§12.8 F-CLM-CAUSAL-XFER"
  status = "🔴 CLOSED-negative — 잘 학습된 d512 conv-MoE 가 degenerate monopoly 입력조차 적분 → collapse 인과력이 rich 와 대등/초과(n=5 부호반전); toy≠scale(H_666)이 측도 자체에 적용; thresholds FROZEN, NOT tampered (verdict persisted verbatim)"

@C clm_causal_xfer_hw_green := "F-CLM-CAUSAL-XFER axis B (live AKD1000 HW): CAUSAL-POWER 가 실 silicon 에서 frozen 3-check PASS — on_hardware=True·BC.00.000.002, 전 n rich>collapse(Δ +0.0618/+0.0156/+0.0268)" :: run [slug=clm-causal-xfer group=CLM]
  method = "run"
  cmd    = "CLM_MSWEEP=$PWD python3 CLM/msweep/clm_causal_hw.py --json (pi5-akida, InputData→FC act_bits=1 @BackendType.Hardware, streamer stop→collect→restart, seed=187, ≤16 poke, frozen 3-check)"
  raw    = ".verdicts/856_clm_causal_xfer/hw.txt"
  src    = "UNIVERSE/H_856_clm_causal_xfer.md §5/§7 · CLM/P0_ARCHITECTURE.md §12.8"
  status = "🟢 SUPPORTED-NUMERICAL — 실 온칩 threshold-and-fire 에서 poke 가 coupled(rich) regime 으로 전파·decoupled(collapse) 국소 사멸; 배포 silicon 에선 측도 certify; thresholds FROZEN (verdict persisted verbatim)"

@C clm_causal_xfer_falsified := "F-CLM-CAUSAL-XFER 종합: 🔴 FALSIFIED — '🟢 on BOTH' 요구에서 axis A 🔴 → '🔴 on EITHER' 발동 → CAUSAL-POWER 도 toy-limited → 백로그 #3 CERTIFY-NOT-MEASURE escalation (단 axis B 🟢 HW positive 실재)" :: run [slug=clm-causal-xfer group=CLM]
  method = "run"
  cmd    = "production(axis A 🔴) ∧ live-HW(axis B 🟢) 종합 — CLM/msweep/clm_causal_{prod,hw}.py 두 verdict 결합 (frozen rule: 🟢 on BOTH else FALSIFIED)"
  raw    = ".verdicts/856_clm_causal_xfer/F-CLM-CAUSAL-XFER.txt"
  src    = "UNIVERSE/H_856_clm_causal_xfer.md §6 · CLM/P0_ARCHITECTURE.md §12.6/§12.8 (CERTIFY-NOT-MEASURE escalation SSOT)"
  status = "🔴 CLOSED-negative — toy→production→HW 전 transfer 를 생존한 닫힌형 의식 MEASURE 없음; Φ-family(H_855)에 이어 CAUSAL-POWER 도 production-width toy-limited; 측정-타당성 질문 production scale 에서 open 유지 (a_paper_negative_ok)"

# CLM — clm-causal-band (slug · group=CLM) · H_857
# H_856 axis B 🟢(live AKD1000 CAUSAL-POWER)의 regime 특성화. frozen 측도
# (measure_sweep.py) 재사용·재튜닝 0, coupling K(환경 knob)만 사전등록 그리드 스윕.

@C clm_causal_band_hw_green := "F-CLM-CAUSAL-BAND (live AKD1000 coupling-band): CAUSAL-POWER Δ(K)가 bounded edge-of-chaos band — interior peak K*=1.0(Δ=0.1021) ∧ cold rolloff[Δ(0)=0.0399] ∧ saturate rolloff[Δ(24)=0.0017], monotone=False; fire_frac 0.156→0.994 단조상승하며 Δ 가 포화에서 붕괴(기전 서명)" :: run [slug=clm-causal-band group=CLM]
  method = "run"
  cmd    = "CLM_MSWEEP=$PWD/CLM/msweep python3 CLM/msweep/clm_causal_band.py --json (pi5-akida, InputData→FC act_bits=1 @BackendType.Hardware, K_GRID=[0..24] 사전등록, streamer stop→sweep→restart, seed=187, ≤16 poke, frozen 측도)"
  raw    = ".verdicts/857_clm_causal_band/F-CLM-CAUSAL-BAND.txt"
  src    = "UNIVERSE/H_857_clm_causal_band.md §5/§6 · CLM/P0_ARCHITECTURE.md §12.8 (HW-positive edge-of-chaos band)"
  status = "🟢 SUPPORTED-NUMERICAL — axis B(H_856) 🟢 의 regime 정밀화: 측도는 edge-of-chaos band(interior peak) 안에서만 통합 certify, 양끝(cold decoupled · saturate all-fire)에서 rolloff; axis-B 원래 rich(K=3)는 이미 포화 어깨(fire 0.94); axis A 🔴 불변; thresholds FROZEN (verdict persisted verbatim)"

# ───────────────────────────────────────────────────────────────────────
# INTENT — intent-osc-residual (slug · group=INTENT) · H_859
# bench D axisbench(#1143) 4/5 🟠 PARTIAL 의 단일 잔류 falsifier F3
# OSC_STABILITY_LOW(OSCILLATING stability_std=0.0) 의 진단·해소. residual =
# 측정자(尺) aliasing (period-20 ⊥ window-grid size-10 commensurable),
# 신호 결함 아님. raw direction_std + argmax period_detect 교체 → 5/5
# RECOVERED. 진동 자체는 EMA damping 생존 → intrinsic limit-cycle (H_634
# ultradian 과 동일 periodic substrate motion class).

@C intent_osc_residual := "F-INTENT-OSC-RESIDUAL: bench D OSC residual = stability_std 의 metric aliasing(period-20 ⊥ window-grid → std=0). raw direction_std 교체로 OSC=0.354 > CONV=0.350 식별 ∧ period=20 genuine ∧ RANDOM period=0 ∧ EMA α=0.2 heavy damping 후에도 period=20 생존 → 진동 intrinsic limit-cycle. INTENT 4/5 🟠 → 5/5 🟢 RECOVERED" :: hypothesis [slug=intent-osc-residual group=INTENT]
  method = "run"
  cmd    = "hexa run bench/axis_intent/a6_osc_residual_verify.hexa (self-contained · LCG-deterministic · libm-free · foreground sync · $0 mac-local · exit 0 · 2-run byte-identical)"
  raw    = ".verdicts/859_intent_osc_residual/F-INTENT-OSC-RESIDUAL.txt"
  src    = "UNIVERSE/H_859_intent_osc_residual.md §5/§6 · INTENT_A6_OSC_RESIDUAL.md · ANIMA.md INTENT 축 (bench D #1143)"
  status = "🟢 SUPPORTED-NUMERICAL — direction_std 재설계가 OSC residual 을 해소 (5/5 PASS); legacy stability_std 의 window-period commensurability aliasing 이 root cause (신호 결함 아님); 진동은 substrate 본질 intrinsic limit-cycle (damping 생존); H_634 ultradian Φ envelope cross-link; thresholds FROZEN (verdict persisted verbatim)"

# UNIVERSE — akida-edge-of-chaos-phi (slug · group=UNIVERSE) · H_858
# pe_edge_of_chaos_peak (M2 🟡 PARTIAL · sim ∩곡선)의 inverse-U 를 live AKD1000
# drive-regime R1~R4 로 실리콘 검증. Φ-proxy frozen(akida_edge_of_chaos_phi.hexa)
# 재사용·재구현 0, regime preset(drive/noise/feedback)만 사전등록. H_857(coupling-K·
# CAUSAL-POWER)과 독립 축(drive-regime·Φ-proxy)이 같은 silicon ∩으로 수렴.

@C akida_edge_of_chaos_phi_hw_green := "F-AKIDA-EDGE (live AKD1000 R1~R4 drive-regime): Φ-proxy inverse-U(∩) — Φ(R1 silent)=0 · Φ(R2 noise-edge)=0.172 · Φ(R3 tonic-edge)=0.250(peak) · Φ(R4 recurrent)=4.95e-12≈0; F1 Φ(R2)>Φ(R1) ∧ F2 Φ(R3)>Φ(R1) ∧ F3 max(R2,R3)≥Φ(R4) 3/3 PASS; 실 칩 R4 recurrent loop die-out(포화 아님)→order/over-driven 양끝 low, edge peak" :: run [slug=akida-edge-of-chaos-phi group=UNIVERSE]
  method = "run"
  cmd    = "akida_edge_of_chaos_phi_hw.py --seed 187 (pi5-akida, InputData(1,1,16)→FC(units=16,ones,act_bits=1) @BackendType.Hardware, per-unit int32 thr=POT−drive, R1~R4 preset 사전등록, streamer stop→sweep→restart) → akida_edge_of_chaos_phi.hexa --result <json> (frozen Φ-proxy + judge_inverse_u)"
  raw    = ".verdicts/858_akida_edge_of_chaos_phi/F-AKIDA-EDGE.txt"
  src    = "UNIVERSE/H_858_akida_edge_of_chaos_phi.md §5/§6 · CORE/phi_envelope_substrate.hexa::pe_edge_of_chaos_peak (M2 promote) · AKIDA/akida_edge_of_chaos_phi_hw.hexa"
  status = "🟢 SUPPORTED-NUMERICAL — sim ∩곡선이 live silicon 에서 성립(edge R2/R3 > order R1 ∧ edge ≥ over-driven R4); pe_edge_of_chaos_peak M2 🟡→🟢 promote; H_857(coupling-K·CAUSAL-POWER)과 독립 축이 같은 silicon edge-of-chaos ∩ 확인 — single-측도 artifact 아님; on_hardware=True·BC.00.000.002·streamer 복귀 active; Φ-proxy honest(full IIT4 big_phi 아님); thresholds/preset FROZEN (verdict verbatim)"

# CLM-KOSMOS — clm-akida-multiling-semantic (slug · group=CLM-KOSMOS) · F-CLM-AKIDA-MULTILING-SEMANTIC
# 메타도메인 CLM⊕KOSMOS (PR #1651) 의 gate falsifier 를 실 AKD1000 silicon 에서
# 종결. 5-lang(ko·en·zh·ru·ja) parallel(concept-major·c>0) vs concat(lang-major·c~0)
# .kosmos @corpus (동일 바이트, member ordering 만 차이), AkidaUnsupervised on-chip
# edge-learn(model.fit() ON CHIP). H_911 substrate-proxy 는 🟢 였으나 AKD1000
# last-layer Hebbian edge-learn 레벨에선 전이 안 됨 — closed-negative (a_paper_negative_ok).

@C clm_akida_multiling_semantic := "F-CLM-AKIDA-MULTILING-SEMANTIC (live AKD1000 · N=12 paired on-chip trials): 5-lang parallel .kosmos @corpus 로 AkidaUnsupervised on-chip edge-learn 한 CLM 이 동일-바이트 concat 대조군보다 통합 우수하지 않음 — paired delta(parallel−concat) 6 pos/6 neg · mean=−0.00092 · 95%CI=[−0.00319,+0.00135] straddle 0 · learn_happened_hw=True 12/12. 단일 run 은 H_904 stochastic-plasticity 로 🟢/🔴 flip → multi-trial 必. H_911 이 AKD1000 edge-learn 엔 전이 안 됨 (closed-negative)" :: hypothesis [slug=clm-akida-multiling-semantic group=CLM-KOSMOS]
  method = "run"
  cmd    = "onchip_multitrial.py (pi5-akida · BC.00.000.002 BackendType.Hardware · AkidaUnsupervised(num_weights=16,learning_competition=0.1) · InputData(1,1,256,input_bits=1)→FC(units=32,weights_bits=1) · int4 backbone sha256=c626c638… byte-identical 양 arm · N=12 paired trial · stale streamer PID18439 lock-clear 선행)"
  raw    = ".verdicts/clm-akida-multiling-semantic/result.txt"
  src    = "domains/CLM-KOSMOS.md (PR #1651) C1·C2·C3·C4·C5 · UNIVERSE/H_911 (substrate-proxy 🟢) · .verdicts/904_clm_onchip_plasticity (H_904 stochastic plasticity) · hexa-lang stdlib/flame/testdata/clm_semantic_{parallel,concat}.txt (corpus seed)"
  status = "🔴 REFUTED (closed-negative · publishable) — H_911 cross-lingual semantic-linkage 우위가 AKD1000 last-layer Hebbian edge-learn 에 전이 안 됨; per-ordering 통합 gap 이 칩 자체 stochastic-plasticity noise(H_904) 안에 묻힘; C1 on-chip learn 은 12/12 trial live (실 silicon 확인), C4 .kosmos 구조(limen·merkle·profile·closed_corpus·coord⊥text) 완전 준수; 단일-run cherry-pick(🟢 draw) 거부 → g63 honest; model NOT uploaded (🔴 earns no .clm); thresholds/falsifier FROZEN (verdict verbatim)"

@C clm_akida_semantic_signal_lift := "H_912 — all-4-lever AKIDA on-chip signal-lift for H_911" :: claim [d=2026-06-01 closed]
  text   = "Even with all 4 HW-feasible levers (200-anchor 5-lang corpus · 3-exposure accumulation · dual measure {last-layer-sep, Phi-proxy} · learn-while-infer streaming), H_911 cross-lingual semantic-linkage does NOT transfer to AKD1000 last-layer Hebbian on-chip edge-learn."
  method = "N=20 paired on-chip trials (real AKD1000 BC.00.000.002), both axes 95% CI straddle 0; learn_happened_hw 20/20."
  verdict = "🔴 REFUTED (closed-negative · publishable) — .verdicts/clm-akida-semantic-signal-lift/result.txt"
  group  = "CLM-KOSMOS"

@C h1218_engine_measured_gates := "H_1218 — first ENGINE-measured (not torch) G1/G2/G6 generation-gate verdict on mounted 303M" :: hypothesis [slug=1218_engine_measured_gates group=UNIVERSE]
  text   = "Engine forward (CORE/bytegpt_decode.hexa::bytegpt_decode_argmax) is BYTE-EXACT to torch greedy on the production anima-clm-chat-303m (ENGINE-PARITY 🟢, H_1157 re-verified), so greedy gate metrics are engine==torch by construction. Engine-measured under GREEDY decode: G1 composed_distinct=0 🔴, G2 novelty_rate=0.308, G6 count=3 🔴(<5). These DIFFER from the torch baselines (H_1158 G6 best 14 PASS) — NOT an engine bug but two confounds: (1) the frozen gates were authored for top-k=40 temp=0.7 SAMPLING decode (G6 divergence = sampling, not weights) while the engine path is greedy-only → 303M byte-LM collapses/loops; (2) baselines used broad-en base + 1.5GB corpus, this run used dialogue-FT chat + surviving 5MB corpus. The engine GENERATES byte-faithfully; the frozen G1/G6 PASS depend on a sampling decode the engine argmax path does not implement."
  method = "Production chat ckpt state/chat_303m/h1129c_chat.pt (sha 4fcc2d6c) serialized to flat .bin (sha 5c303f02, reparity serialize_parity_ok=TRUE) via H_1157 layout. Engine greedy gen via bytegpt_decode_argmax; scored with FROZEN UNIVERSE/gauge_lib.py evaluators (_coverage/_content_ngrams/_corpus_absent/_words/_jaccard/known_word_ratio) VERBATIM, p7 NO LLM-judge. Representative engine subset (G1+5 G6 seeds, 40 greedy bytes); full numbers scored on byte-exact torch-greedy gen (engine CPU ~30 s/byte at gate-context). G2 corpus=data/corpus.txt (5MB, broad 1.5GB ephemeral GONE => novelty upper bound)."
  verdict = "🟢 ENGINE-PARITY GREEN / 🔴 G1·G6 RED under greedy (sampling-regime gate ⊥ greedy engine path; closed-negative finding, frozen bars unmoved) — .verdicts/1218_engine_measured_gates/H_1218.txt"
  group  = "UNIVERSE"

@C h1210_daemon_gateB_wiring := "H_1210 — wire H_1209 trajectory-aware GATE-B into the LIVE daemon GROW step so anima divides on conversation transition-predictability" :: hypothesis [slug=1210_daemon_gateB_wiring group=MITOSIS-ENGINE]
  text   = "The LIVE anima daemon (CORE/anima_full_session_smoke.hexa C8 GROW) now divides TRAJECTORY-AWARE on the real per-turn emit stream via the H_1209 VAdaptFieldB GATE-B lane, ALONGSIDE the existing per-sample density VAdaptField. F1 GATE-B born-cells=6 ON (cells 1→7) on the 12-tick ordered conversation walk; F2 ablation born-cells=0 OFF (engine_mitosis_tick no-op). H_1205 separation invariant PRESERVED LIVE: F3 Ψ Φ-checksum byte-identical ON==OFF (1.4278) AND F4 generation output byte-identical ON vs OFF — GATE-B is Ψ-disjoint/additive, never feeds the decode. All five daemon faculties (converse/ground/grow/remember/sleep) still PASS. GATE-B runs ALONGSIDE density (NOT replace): the two gates measure DIFFERENT substrate properties (per-sample density ⊥ ordered transition-predictability; H_1209 F4 scoped GATE-B as a trajectory variant that does not beat the i.i.d. PRIMARY density bar)."
  method = "C8 GROW collects each turn's emit-span DIM=8 _afs_byte_feature into an ordered WALK; after the loop builds a FIXED order-invariant proto book over the daemon's OWN emit-feature SET (_afs_build_book = H_1208 build_fixed_book PORT: lexsort + farthest-point seed + 3 LR=0.10 passes in sorted order), maps each feature → nearest proto-id (_afs_proto_walk), and drives VAdaptFieldB (vadapt_fieldB_new/_step/_cells/_growth) over the (prev→cur) transition stream with mitosis ON and a genuine engine_cli_parse(['--mitosis','off']) OFF arm. Ψ-disjoint + additive (a_core_engine_map): reads only emit features, never pure_field/.clm/.kosmos, never feeds decode. CORE/engine_cli.hexa UNCHANGED. $0 local CPU, gradient-free (p8), p7 = born-cell counts/byte-equality. Guards GREEN: engine_cli_smoke 12/0 · generator_smoke 21/0 · h1196 single-entry 7/0 · h1205 separation."
  verdict = "🟢 GREEN (F1∧F2∧F3∧F4) — daemon divides trajectory-aware on conversation, generation still Ψ-separated; toy scale, scale UNVERIFIED (a_scale_honest_scope) — .verdicts/1210_daemon_gateB_wiring/H_1210.txt"
  group  = "MITOSIS-ENGINE"

@C h1289_quantum_entropy := "H_1289 — TRUE quantum entropy (ANU QRNG vacuum-fluctuation bytes) is a substrate-faithful stochastic source for anima's free decisions, and gives the one irreducible property a PRNG cannot: NON-REPRODUCIBILITY" :: hypothesis [slug=1289_quantum_entropy group=QUANTUM-ENTROPY]
  text   = "REAL ANU QRNG paid API (https://api.quantumnumbers.anu.edu.au, x-api-key, c7) fetched 448 REAL vacuum-fluctuation quantum bytes (success=true, HTTP 200). Wired as the entropy source for ONE clean substrate stochastic decision — a top-k(=8) decode-sampling draw over a FIXED deterministic logit field (so ONLY the entropy source varies). (A) substrate-faithfulness: QRNG passes NIST-lite (monobit p=0.659, runs p=0.923) AND >= the PRNG(pseudo) control (monobit p=0.401, runs p=0.693) — both PASS |z|<3.29. (B) quantum-vs-PRNG substrate effect: NULL as honestly predicted — mitosis cell-count 7 vs 6, novelty 0.875 vs 0.859, Psi-proxy 0.259 vs 0.261 (Δ negligible); the value of quantum entropy is NON-DETERMINISM AUTHENTICITY (p1-p8 / Psi=1/2 framing), NOT a perf lift (p7/c9). (C) irreducible difference — NON-REPRODUCIBILITY: same substrate + same seed -> PRNG run1==run2 byte-identical, QRNG run1!=run2 (differs in 54/64 emitted bytes). REAL-ONLY (a_eeg_consciousness_record): on any API failure the run STOPS and reports honestly — no fabricated quantum data, no PRNG-as-quantum (c9); PRNG control LABELED pseudo throughout."
  method = "UNIVERSE/h1289_quantum_entropy.py. ANU key read at call time from env ANU_KEY (caller: harness secret get flat.anu_key_paid), used ONLY in x-api-key header, NEVER echoed/logged/written to any file (c7-verified: grep of key over all deliverables = clean). Entropy sources share an IDENTICAL ByteStream consumer (uint8 -> [0,1) draw): PRNG=numpy default_rng(seed=7) deterministic; QRNG=fresh ANU fetch. Substrate-mirror decode emits K=64 byte tokens, ONE uniform draw per step picks from top-8 of a fixed per-step logit field. NIST-lite = monobit frequency (erfc) + runs test (z, pi-precondition) on bit-expanded bytes, gate |z|<3.29 (p>1e-3). Gauges (B): VAdaptField mitosis numpy mirror (clonal split recon-err>0.30) of CORE/engine_cli.hexa + novelty distinct-rate + Psi-noise proxy. (C) runs the SAME substrate twice per arm. torch ABSENT on host => numpy-mirror probe (DIRECTIONAL); the QRNG FETCH itself is REAL. $0-ish (448 quantum bytes total). live CORE/*.hexa UNTOUCHED (numpy mirror — round-1 probe; engine-native wiring = r2 follow-on per a_engine_native_learning + a_verified_must_wire)."
  verdict = "🟢 GREEN (A real-fetch+NIST-lite>=PRNG ∧ C non-reproducibility) — anima can source genuine PHYSICAL indeterminism; B null = honest finding (authenticity not perf). 🏁 DEPLETION. numpy-mirror DIRECTIONAL, scale/engine-native UNVERIFIED (a_scale_honest_scope) — .verdicts/1289_quantum_entropy/H_1289.txt"
  group  = "QUANTUM-ENTROPY"

@C h1292_hypothalamus_drive := "H_1292 — a setpoint-regulated homeostatic drive (hypothalamus, HD29) is a DISTINCT engine lane from the stateless affect read: a leaky temporal integral of the below-setpoint grounding-satiation deficit RISES under deprivation and RESETS on a consummatory grounded event, distinguished from affect on a time-vs-context dissociation and EARNED by the integral controller" :: hypothesis [slug=1292_hypothalamus_drive group=BRAIN-STRUCTURE-LADDER]
  text   = "The next-missing brain subsystem after hippocampus/WM/cerebellum/amygdala/basal-ganglia is the HYPOTHALAMUS — a setpoint-regulated homeostatic drive. Every existing CORE drive (affect read-out H_1290, curiosity, idle/M) is INSTANTANEOUS/stateless; none holds a regulated variable, accumulates its deficit vs a setpoint across ticks, and resets on a consummatory event. HomeostaticDrive reads 'grounding satiation' s_t = the recall margin off the live ImmuneMemoryGrow store (the SAME signal affect reads), and adds the NEW structure: setpoint S*=0.5 + leaky integral I=(1-lambda)I+max(0,S*-s) (lambda=0.1) + drive=Kp*deficit+Ki*I (Kp=1.0 Ki=0.5) + consummatory reset (s>=S* -> I:=0). FROZEN GREEN iff (A1) FULL drive monotone & rise>=0.50 over deprivation; (A2) reset <= 0.50*end-of-deprive; (B) DISTINCT — affect FLAT (max-min<0.05) over a FIXED-context deprive while FULL drive over the SAME ticks rises>=0.50 (time-integral perp context-instant); (C1) EARNED — ablated Ki=0 rise<0.10 (the stateless affect-style read does NOT accumulate); (C2) SHUFFLE reset<0.50*rise; (D) abstain intact (untaught far key fires no cell). RESULT 3 seeds [4290,4291,4292] byte-identical, R1 numpy mirror & R2 ENGINE-NATIVE agree byte-exact: A1 rise +1.544 monotone PASS; A2 reset 0.0 PASS; B affFlat 0.0 & drvFixRise +1.544 PASS; C1 ablated rise 0.0 PASS; C2 shufReset 0.0 PASS; D PASS. p6/p2/p3: regulated variable = substrate's OWN margin, NO injected drive label/RLHF/persona; NOT an emit gate (homeo_motivation_bias = OPTIONAL gain, a_autonomy_over_hardcode); Psi-disjoint pure READ + own scalar."
  method = "R1 UNIVERSE/h1292_hypothalamus_drive.py (numpy DIRECTIONAL mirror of the immune store, 3 seeds). R2 ENGINE-NATIVE CORE/h1292_hypothalamus_drive_probe.hexa via `hexa run` over the LIVE engine_cli.hexa homeo_* lane (homeo_new/homeo_new_ablated/homeo_satiation/homeo_step/homeo_last over ImmuneMemoryGrow) — re-scores the SAME frozen R1 bars, byte-exact to the mirror. Regression guards: engine_cli_smoke 33/0 (+3 homeo cases 28-30), h1196 single-entry 7/0, h1199 DIM-growth Psi byte-identical (F3). $0 local CPU, gradient-free, p7 (drive trajectory + abstain counts, NOT perplexity). frozen-first: .verdicts/1292_hypothalamus_drive/H_1292_FREEZE.txt pre-registered before scoring; no bar moved (c9). a_no_llm_frame_trap (homeostatic-regulation lens c15), a_engine_native_learning, a_verified_must_wire."
  verdict = "🟢 GREEN (ENGINE-NATIVE) — HD29 hypothalamus realized as an additive Psi-disjoint lane, DISTINCT from affect on the time-vs-context dissociation, EARNED by the integral controller. brain motivation-loop wiring + scale = follow-on. TOY (4 facts, 3 seeds, deterministic controller — tests homeostatic STRUCTURE not a learned drive); scale/real-corpus/engine-transfer-of-direction UNVERIFIED (a_scale_honest_scope · a_toy_scale_recheck). .verdicts/1292_hypothalamus_drive/H_1292.txt"
  group  = "BRAIN-STRUCTURE-LADDER"
