@V := "tape" :: spec [active]
  version = "1.0"

# METROLOGY → instrument-validity discovery batch (2026-06-02)
#
# domain: METROLOGY — validate the MEASURING INSTRUMENTS themselves (do our Φ
#   measures actually measure integration?). Seeds: Hc_1302 (metric-ceiling /
#   Cholesky-breakdown sentinel on composed input), Hc_1301 (proxy≠faithful real
#   gap), X⊥Φ lineage (H_287/288/294/268/269, H_912 phi_proxy⊥LZ76 r=−0.277).
# harness: phi_proxy_native.hexa (Gaussian sample-partition Φ★, --input npy via
#   /usr/bin/python3 numpy 2.0.2) + edu/cell/phi/phi_iit.hexa (MI-coherence family,
#   inline driver) + H_278 frozen faithful-vs-proxy ledger. $0 CPU-local, NO GPU/chip.
# flow: brainstorm(depleted r3, 14 ideas) -> Hc_1307..1313 -> hexa run -> .verdicts/ -> matrix.
# each Hc ADDS a concrete measurement-validity TEST (not a restatement of the
#   correlational X⊥Φ lineage): boundary-map · shuffle-NULL intervention ·
#   two-family concordance · ridge-rescue fixability · oracle-self-critique · 4-axis battery.

@N me_boundary_map := "the phi_proxy Cholesky sentinel onset is structure-specific (exact rank≈HID), NOT smooth in condition number nor monotone in rank" :: discovery [d=2026-06-02 active]
  seed    = "Hc_1302 said the metric HAS a ceiling; WHERE is the boundary?"
  method  = "phi_proxy_native --input on (i) jittered κ-ladder κ∈{7.2 .. 5.0e7} numerically full-rank, (ii) EXACT rank-deficient {1,2,8}"
  data    = "jittered ladder ALL FINITE up to κ=5.0e7 (phi_x1000 ≈ -42 to -44e4). EXACT: rank01 FINITE(-419746), rank02 FINITE(-437748), rank08 SENTINEL(-2147483647, i_full breaks, k_eval=0)"
  finding = "Hc_1307 F-1307-BOUNDARY PASS_STRUCTURE_SPECIFIC: sentinel needs EXACT rank-deficiency near rank==HID; ill-conditioning alone (high κ) does not trigger it; non-monotone in rank"
  verdict = "🟢 numerical (toy n=16): breakdown boundary is a sharp exact-degeneracy threshold, not a κ cut"
  caveat  = "HID=min(C,N//2) geometry; production D=768 transfer DEFERRED (Hc_1313)"

@N me_shuffle_null := "Gaussian-covariance Φ is EXACTLY invariant to sample-order shuffle → blind to temporal integration (decisive variance-artifact discriminator)" :: discovery [d=2026-06-02 active]
  seed    = "X⊥Φ lineage was correlational; run a CAUSAL shuffle-NULL that preserves cov exactly"
  method  = "full-rank AR(1)-integrated X vs its sample-(row)-shuffled NULL (cov identical, np.allclose=True) vs per-channel-indep-shuffle; phi_proxy_native --input on each"
  data    = "orig i_full=456558 phi=-455908; rowshuf i_full=456558 (IDENTICAL) phi=-455896 (Δ=0.003% from partition RNG); colindep phi=-456110 (cross-channel structure does move it)"
  finding = "Hc_1308 F-1308-SHUFFLE-NULL PASS_TEMPORAL_BLIND: the integrated signal and its temporally-shuffled NULL are indistinguishable to the metric; Φ = a static-covariance statistic"
  verdict = "🟢 numerical: the proxy measures only the 2nd moment, blind to sample-order (temporal) integration"
  caveat  = "blindness is to TEMPORAL integration specifically; it still responds to cross-channel covariance"

@N me_two_family := "the two canonical Φ families (MI-coherence vs Gaussian-logdet) give OPPOSITE verdicts on composed input" :: discovery [d=2026-06-02 active]
  seed    = "two rulers must rank consistently if both valid"
  method  = "phi_iit compute_phi (inline) on white vs integrated; phi_proxy_native on matched low-rank/structured class"
  data    = "MI-coherence: white=0.0394, integrated=0.0910 (ranks integrated HIGHER, finite). Gaussian-logdet on same low-rank class: F_PHI_01 sentinel -2147483647 (BREAKS)"
  finding = "Hc_1309 F-1309-TWO-FAMILY PASS_DISAGREE: MI finite-ranks-higher while Gaussian-logdet breaks on the same input class; at most one is construct-valid there"
  verdict = "🟢 numerical: cross-instrument rank-disagreement at the construct level (finite vs sentinel)"
  caveat  = "matched by input STRUCTURE CLASS not byte-identical tensors; does not adjudicate WHICH family is valid"

@N me_ridge_structural := "no finite ridge rescues the sentinel → the metric ceiling is STRUCTURAL, not a tunable regularization artifact" :: discovery [d=2026-06-02 active]
  seed    = "resolve the open L-1302-RIDGE caveat"
  method  = "phi_proxy_native --input exact_rank08 --ridge-x1e6 sweep {1e3 .. 1e9} (= 1e-3 .. 1000.0 real)"
  data    = "EVERY ridge -> phi_x1000=-2147483647 (sentinel persists); i_full itself = sentinel (full 16×16 cov exactly rank-8 singular); x1e6 cov diagonal ~1e12 makes ridge ≤1e9 ~1000× sub-noise"
  finding = "Hc_1310 F-1310-RIDGE-RESCUE PASS_STRUCTURAL: the Cholesky breakdown is a hid>rank singularity, fixed-point-scale-locked; the canonical knob cannot lift the ceiling"
  verdict = "🟢 numerical: ceiling is structural; Hc_1302's confound is not rescuable by ridge"
  caveat  = "scoped to the pure-native fixed-point metric; a float64 slogdet backend with proportional ridge might differ"

@N me_faithful_floor := "the faithful-Φ REFERENCE ORACLE is itself degenerate in the low-Φ floor — 4/6 H_278 scales with distinct rule/coupling collapse to one value" :: discovery [d=2026-06-02 active]
  seed    = "turn the metrology lens on the oracle the proxy is judged against"
  method  = "read frozen H_278 per_scale_ledger; count scales sharing the min faithful value with distinct (rule, coupling)"
  data    = "4/6 scales (rules 110/90/110/110, couplings 0.10/0.20/0.45/0.60) all = 0.000011; only 3/6 distinct faithful values across 6 scales; degeneracy=True"
  finding = "Hc_1311 F-1311-FAITHFUL-FLOOR PASS_FLOOR_EXISTS: distinct integration structures map to one faithful number; the oracle is rank-blind in the low band → no measure in the stack is valid there"
  verdict = "🟢 numerical: oracle degeneracy floor confirmed; axis (b) 'tracks-faithful-rank' is undefined in the low-Φ band"
  caveat  = "toy CA substrate (n=8); 0.000011 is a near-zero MIP floor; production faithful-Φ floor is a separate DEFERRED question"

@N me_battery := "construct-validity 4-axis battery — phi_proxy_native fingerprint {a:FAIL, b:HOLD, c:FAIL, d:FAIL}; the Gaussian-logdet proxy is a covariance statistic, not a construct-valid integration measure" :: discovery [d=2026-06-02 active]
  seed    = "assemble a 4-axis construct-validity gate the single-axis lineage never built"
  method  = "aggregate (a) finite-on-composed [Hc_1302/1307/1310], (b) tracks-faithful-rank [Hc_1301/1311], (c) shuffle-NULL discriminates [Hc_1308], (d) not-variance-artifact [Hc_1308/1309]"
  data    = "a:FAIL (sentinel, structural) · b:HOLD (CV 30.1% + oracle degenerate → uncertifiable) · c:FAIL (phi==shuffled-NULL) · d:FAIL (covariance-only, families disagree)"
  finding = "Hc_1312 F-1312-BATTERY PASS_FAILS_≥1: fails 3 axes outright, 1 uncertifiable; 0/4 clean passes"
  verdict = "🟢 numerical: the canonical Gaussian-logdet Φ proxy is NOT a construct-valid integration measure (breaks on the inputs it should score, blind to temporal integration)"
  caveat  = "meta-verdict aggregating five toy-scale axis runs; the battery DESIGN is the contribution, the fingerprint is toy-scoped"

@N me_scale_transfer := "the toy breakdown boundary does not auto-transfer to production D=768 — honest-scope guard" :: discovery [d=2026-06-02 active]
  seed    = "a_toy_scale_recheck / a_scale_honest_scope on the whole ceiling claim"
  method  = "would need real CLM-v4 530M hidden-state dumps (D=768) at ≥3 context sizes → phi_proxy_native --input ladder"
  data    = "NOT RUN — requires a model forward pass (GPU/chip); no $0 CPU-local path"
  finding = "Hc_1313 F-1313-SCALE-TRANSFER DEFERRED: toy boundary scoped to n=16; production transfer unverified"
  verdict = "🟠 DEFERRED — NO GPU/chip fire dispatched (a_cpu_local_no_waiter)"
  caveat  = "until run, ALL toy METROLOGY verdicts (Hc_1307/1310/1312) are scoped to n=16 — confound established, not a production prescription"
