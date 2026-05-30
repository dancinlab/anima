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
