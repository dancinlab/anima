@V := "tape" :: spec [active]
  version = "1.0"

# DECODER MoE mode-collapse — micro-exp root-cause re-attribution (2026-05-28)
#
# seed: #1296 / Pod C — production MoE (d=64, V=151643) decode = [1,..,1],
#   distinct=1. Prior fires varied corpus-diversity (#1296 FAIL) + routing/aux
#   (Pod C FAIL). Both ruled OUT. This discovery isolates the actual driver with
#   a routing-free toy (Emb[V x d] + Head[V x d] successor LM, k -> (k+1)%V).
# harness: CORE/DECODER/mx_capacity_cliff.hexa ($0 mac/pool-local, hexa-native).
# flow: discovery -> CLAIMS.tape -> hexa verify -> .verdicts/ -> paper_on_discovery.

@N dec_capfloor := "head-rank capacity floor V*(d) grows geometrically — d=64 ample for V=151643" :: discovery [d=2026-05-28 active]
  seed    = "is the collapse a head-rank wall (d too small for V)?"
  method  = "mx_capacity_cliff: high-epoch (150) d x V grid, largest V fully solved per d"
  data    = "d=2 V*<32 · d=3 V*~32 · d=4 V*~128 · d=5/6 V*>=256 — ~3.5x per +1 d (geometric)"
  finding = "V*(d) ~ 16 * 3.5^(d-2): V=151643 needs only d~10; d=64/256 >> floor"
  verdict = "rank NOT the production bottleneck (toy-supported); cap wall real but far below prod d"
  caveat  = "toy-only · learnable Emb + clean permutation · transfer unverified"

@N dec_undertrain := "production collapse dominated by step/data budget, not d and not routing" :: discovery [d=2026-05-28 active]
  seed       = "if rank is ample, why does d=64 collapse?"
  method     = "mx_capacity_cliff step-budget sweep: distinct vs epochs at fixed d (V=64)"
  data       = "d>=4 needs ~50 epochs to fully escape; epochs-to-escape grows with V (d=4 solves V=128@150ep, fails V=256@150ep)"
  finding    = "fire ran n_steps=200 PER-TOKEN = 200 presentations; a single pass over V=151643 needs 151643; fire is ~38000x short of one epoch"
  verdict    = "under-training is the binding lever (toy-supported): corpus-size x epochs, not d/aux/corpus-balance"
  prediction = "running A(d=256+aux) AND B(d=256 no-aux) BOTH collapse 2/5 — d cannot fix a step deficit"

@N dec_saga_reframe := "M4b saga tested the wrong levers — diversity/routing/capacity all secondary to data+steps" :: synthesis [d=2026-05-28 active]
  ruled_out    = "corpus-diversity (#1296) · routing/aux (Pod C) · head-rank (dec_capfloor: d=64 ample)"
  binding      = "step/data budget (dec_undertrain) — every fire fixed n_steps=200, never varied it"
  next         = "real escape fire = large corpus + many epochs (>= tens x V token-steps); d=64 likely sufficient"
  paper_target = "a_paper_negative_ok — closed re-attribution: 3 ruled-out levers + 1 binding, toy-derived + fire-confirmed"
