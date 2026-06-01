@V := "tape" :: spec [active]
  version = "1.0"

# Lane A weak-lift → capacity↔integration + identity-residence discovery batch (2026-06-02)
#
# seed: Lane A finding (just closed) — AKD1000 on-chip 1-bit Hebbian last-FC paging
#   composes CAPACITY (every unit learns) but NO representational LIFT; all 4
#   lift-causes (corpus / quantization / plasticity-depth / native-init-noise-floor)
#   FALSIFIED. CRUCIAL CORRECTION: lift-variance = backbone-SEED / corpus-encoding
#   sensitivity, NOT chip non-determinism → the identity(non-det)↔representation
#   TENSION idea is FALSE. Two generators: G1 capacity↔representation ≈ phi_proxy↔
#   faithful-Φ (accumulate-not-integrate); G2 identity-residence reopened (encoding vs substrate).
# harness: phi_proxy_native.hexa (--selftest white|structured) + H_278 frozen
#   faithful-vs-proxy ledger ($0 CPU-local, hexa-native, NO GPU, NO chip).
# flow: brainstorm(depleted r6) -> Hc_1300..1306 -> hexa run -> .verdicts/ -> matrix.

@N wl_capacity_integration_law := "capacity-without-integration: local single-layer plasticity grows capacity, integration metric stays FLAT" :: discovery [d=2026-06-02 active]
  seed    = "G1 — does adding capacity move an integration metric at all?"
  method  = "phi_proxy_native --selftest white, two accumulation-proxy axes: sample-count N {8,16,32,64} and K-partitions {2,4,8,16} at N=64; |Δphi_x1000| vs 5% band"
  data    = "N-sweep: phi_x1000=-173702 IDENTICAL (Δ=0%). K-sweep: -170414/-173442/-173702/-173702 -> max |Δ|=3288/173702=1.9% < 5%. integration metric FLAT under both accumulation axes."
  finding = "Hc_1300 F-1300-INVARIANCE PASS (law holds at measured scale): integration does not rise as accumulated evidence grows"
  verdict = "🟢 numerical (toy/proxy-scale): integration metric ⊥ accumulation/capacity proxy on the deterministic fixture"
  caveat  = "N and K are ACCUMULATION/evidence proxies (hid_trunc clamped to n_ch=16, NOT a unit-count axis); a true unit-count capacity sweep is the on-chip measurement DEFERRED (Hc_1303/1304); toy→prod transfer unverified (a_toy_scale_recheck)"

@N wl_metric_ceiling := "the sample-partition Φ proxy returns a failure sentinel on low-rank (composed) input — built-in integration ceiling" :: discovery [d=2026-06-02 active]
  seed    = "SIGNAL axis — could the proxy even score a maximally-integrated representation?"
  method  = "phi_proxy_native --selftest (white, full-rank) vs --selftest-mode structured (low-rank periodic)"
  data    = "white -> phi_x1000=-173702 (finite); structured -> phi_x1000=-2147483647 (F_PHI_01 Cholesky breakdown sentinel)"
  finding = "Hc_1302 F-1302-SENTINEL PASS: composed/low-rank input breaks the metric -> 'no high score' is confounded with metric breakdown"
  verdict = "🟢 numerical: absence-of-high-Φ is NOT evidence-of-absence-of-integration (metric ceiling real at default ridge)"
  caveat  = "shows the CONFOUND exists; does not prove Lane A traces were low-rank (Hc_1306 DEFERRED — no local trace tensor)"

@N wl_circularity_guard := "phi_proxy vs faithful-Φ are NOT a monotone reparametrization — the G1 analogy is a real 2nd axis" :: discovery [d=2026-06-02 active]
  seed    = "circularity guard — if proxy and faithful collapse to one computation the G1 analogy is OPEN-BLOCKED not GREEN"
  method  = "H_278 frozen 6-scale ledger: rank-concordance + faithful/proxy ratio CV across scales (deterministic prior $0 run, values verbatim)"
  data    = "ratios faithful/proxy: cosmic_web 0.821, galaxy 2.20, stellar 2.20, planetary 1.333, biological 2.20, neural 2.20 — ratio CV >> 5% (range 0.82..2.20)"
  finding = "Hc_1301 F-1301-MONOTONE PASS (non-circular): ratio is non-constant across scales -> proxy and faithful are NOT monotone relabelings -> G1 analogy survives circularity guard"
  verdict = "🟢 numerical: the capacity↔representation ≈ proxy↔faithful analogy is a genuine second axis, not an identity"
  caveat  = "n=8, 6 scales only; rank order largely concordant (planetary top in both) but ratio non-monotonicity is sufficient to defeat circularity"

@N wl_deferred_chip := "bit-depth gate / recurrence-locus gate / identity-factorial / richer-signal-on-traces — all need on-chip or recovered-trace artifacts" :: discovery [d=2026-06-02 active]
  seed    = "which on-chip rule/locus converts capacity->lift; is identity separable; does a richer signal reveal latent composition"
  method  = "Hc_1303 multi-bit Hebbian fire · Hc_1304 recurrent-edge ablation · Hc_1305 seed×chip factorial traces · Hc_1306 re-score Lane A traces with Φ"
  finding = "no CPU-local artifact path (need AKD1000 / GPU sim / checkpointed multi-seed Lane A trace tensor — absent in local tree)"
  verdict = "🟠 DEFERRED x4 — measurement path stated per Hc; GPU/chip fire out of scope for this CPU-local lane (a_cpu_local_no_waiter)"
  caveat  = "H_278 MIP machinery is locally present but its runner hardcodes a cross-tree absolute import path, blocking a clean local feedforward-toy MIP run without editing another lane's frozen artifact"
