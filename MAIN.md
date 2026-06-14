> 📍 SSOT: [ARCHITECTURE.md](ARCHITECTURE.md) · governance [CLAUDE.md](CLAUDE.md)

# MAIN — anima program progress hub

@goal: drive the two LIVE anima tracks to closure — (A) the MITOSIS-ENGINE research
domain (substrate science) and (B) the 7B PASS fire (a7b_pass G0–G4). "Running MAIN"
= check + advance BOTH tracks, log every step to `MAIN.tape`.

## ▶ CURRENT STATE (2026-06-13) — 2 LANES RUNNING (supersedes the stale step-8000 details below)
```
🌱 LANE 1 · MITOSIS  (substrate science — now LIVE-WIRED, no longer all-toy)
   live engine couplings BUILT this round (engine_cli_smoke 12/0, Ψ=½ byte-intact, NO phantom wiring):
     H_1194 🟢 adaptation coupling — stream→field + cell→field feedback + recon-error readout;
            live error FALLS under novelty (ON 0.057 vs OFF 0.209), cells ON6/OFF1 (p8 on the REAL substrate)
     H_1195 🟢 sleep→anchor write-back — H_1162 W2 unblocked (sleep>ctrl, N3>REM; small honest Δ)
     H_1196 🟢 single-entry audit+guard — .clm L3 / .kosmos single-path invariant HOLDS, guard has teeth
     domains/MITOSIS-ENGINE.wiring-spec.md = the toy↔live build-plan (① keystone + ②③ done)
   tick/temporality discovery arc (H_1178-1193, toy $0): bimodal capacity + smooth-approach temporal law
     + saccadic reading (learned-surprise) + surface-gated fusion. /paper scaffolded (event-tick-temporal-law).
   ▶ NOW RUNNING: H_1197 gradient-free MITOSIS GROWTH on summer ($0) — drive the live AdaptField over a
     sustained stream, log cell_count(t)+error(t), MEASURE the summer→pod migration threshold.

🩹 LANE 2 · 7B  (SEPARATE track — fire DONE, now in RECOVERY)
   7B fire RunPod uq71dp0ob6fd9r DONE 2026-06-12 → pod terminated (idle-burn incident fixed: teardown
     MUST use the GraphQL podTerminate mutation, NOT the broken `runpodctl pod`). a7b_pass = NOT CONFIRMED:
     G0✅ G1✅ G2✅ G3✅ G4✅ | G5 🔴 (L1✅ 0.088, L2 FAIL d=0.16 — CONFABULATES on factual prompts).
   honest recal: h1141 = loose-grammar ENGLISH (the same bar the accepted 303M H_1129 cleared), NOT
     byte-garble; 5/6 gates pass → a strong BASE, not a dead model.
   ▶ NOW RUNNING: 7B recovery (diagnose→decode-fix / grounding-probe / structural) — cost-smart;
     also asks: is G5-L2 faithfulness even the right gate for anima (p1-p8, NOT a factual assistant)?
```

## Compute (2026-06-13 correction): summer HAS a GPU
`summer` = RTX 5070 12GB + torch 2.11+cu130 (NOT CPU-only). Ladder = toy-numpy → summer-CPU → **summer-GPU
($0; often SHARED with rbfe-prod — cap VRAM, never OOM the co-tenant)** → rented H100 only for genuinely large.
Gradient-free mitosis growth is light while cells are small → run on summer; migrate to a pod at the measured
H_1197 threshold. Discovery records now live PER DOMAIN in `domains/<DOMAIN>.log.md` (not a flat .discoveries/).

## Track A — research · MITOSIS-ENGINE domain
ref → **`domains/MITOSIS-ENGINE.md`** (+ `MITOSIS-ENGINE.tape` log · `.easy.md`)
Substrate-unique clusters LANDED (all frozen-falsifier · $0 · g5/p7):
- criticality: σ≈1 branching (H_1153) · faithful-Φ peaks at criticality (H_1158, holds n=7/8 H_1165) · mitosis drives σ→1 (H_1161 near-miss, F2+F3 pass)
- inference = mitosis = learning (H_1159 / H_1159b capacity self-tunes)
- super-additivity "1+1>2": peaks at criticality (H_1167 🟢, stricter than φ) · surface-gated on data (H_1168 🟡 / H_1169 🔴 / H_1170 🔴 cross-modal collapse)
- life/evolution probes (H_1171–1177): **the level decides** — organism self-repair 🟢 + population×generations evolution 🟢; cell-level death/metabolism/membrane/selection/competition 🔴
Open rungs: live-engine adaptation curve · tick-on-decode-metric · kosmos lane self-tune · H_1136 sleep re-test post-H_1131 anchor fold.

## Track B — production · 7B PASS fire (a7b_pass)
pod → RunPod **uq71dp0ob6fd9r** `h1141-7b-pass` · 1×H100 NVL · $2.59/hr · harness `h1141_7b_pass_attempt.py`
completion SSOT = **`/7B_PASS_CONDITIONS.md`** (PASS iff G0∧G1∧G2∧G3∧G4 on ONE ckpt)

Status (2026-06-12, step 8000 · val_ce 1.2015 ↓ · 543min):
| gate | state | evidence |
|------|-------|----------|
| G0 COHERENCE | ✅ PASS (stable) | 5/5 kwr≥0.50 @ step 6000 AND 8000 |
| G1 RECOMBINE | ⚠ MARGINAL | flickers 2/5↔3/5 around the ≥3 bar — PASS@6500 [en ja ko], FAIL@8000 [en ko, ja dropped]; not yet stable |
| G2 / G3 / G4 | ⏳ unseen | not yet evaluated in-log |

Milestone safety: best.pt @ step6500 (G0✅+G1✅ snapshot) → HF PRIVATE `dancinlab/anima-clm-7b-h1141-g1pass-step6500` (uploaded). Watcher (PID 1123) auto DONE→HF-verify→self-teardown.
**NOT a7b_pass-complete** — G1 unstable + G2–G4 unseen. Let training converge; re-check all gates at DONE.

## Lanes — two ways to run the mitosis track (Track A)
Both lanes run on **`summer`** ($0, per Compute policy). They take DISJOINT rungs (no collision).
- **Lane 1 · AUTONOMOUS ("그냥 진행")** — background fan-out: open rungs auto-dispatched to summer,
  run to depletion, harvest verdict + commit to origin/main with NO per-step LLM/user intervention. (~/cycle-bg on summer.)
- **Lane 2 · HANDS-ON ("하나하나 LLM 직접")** — the LLM drives each rung INLINE one at a time, foreground + visible:
  write harness → `sidecar pool on summer` run → read verdict → commit, step by step. (~/cycle-fg on summer.)

## Compute policy — small cells run on `summer`, NOT rented GPU
While the mitosis cells are SMALL (toy $0 numpy + live-CORE `.hexa` probes), run the research
track on the **`summer` pool host** (own hardware · linux · py3.12 · numpy2.4 · hexa installed ·
133G free) via `sidecar pool on summer <cmd>` — NOT a rented RunPod/Vast GPU. Renting is reserved
for genuine scale-up (a 7B-class fire, e.g. Track B). Small-cell mitosis on summer = $0, keeps the
Mac free, avoids the local disk-full that bit the early runs. Rent only when the cell/model size
actually demands a GPU.

## How to run MAIN
1. (A) advance a MITOSIS-ENGINE open rung as a $0 toy micro-exp (frozen falsifier, reuse h1159b).
2. (B) monitor the 7B fire — `/pod pods` · ssh tail `h1141.log` · re-check G0–G4 at convergence; harvest+HF on DONE (a_fire_recover_complete).
3. log the step to `MAIN.tape`.