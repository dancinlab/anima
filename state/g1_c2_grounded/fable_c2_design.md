I have what I need — two load-bearing repo facts checked: `PI5-AKIDA.json` registers **no sensor at all** (Pi5 + AKD1000 only; camera/mic/IMU absent, spike-streamer removed 2026-05-29), and the one wired-GREEN faculty (L5 explicit store, #2996) is read-side — which is exactly the legal interface point. Here is the design.

---

# C2 design — grounded re-scope, minimal rig, $0 falsifier, kill condition

**Headline, before the plan:** C2 is buildable and cheaply falsifiable, but two honesty flags must be cemented up front. (1) **Even maximal C2 success cannot close the canonical G1 gate** — the gate is 100% abstract concepts, and the only known bridge from percepts to abstractions (metaphor mapping, ocean→vastness) is itself text-carried, i.e. handed. C2 at best earns a **sibling gate `G1-concrete`**, new registered scope, not `a303m_pass` G1. (2) C2 is a **fuel lever, not an engine lever**: it legally converts held-out pairs into covered pairs (coverage-density — notably the one lever your ledger left alive). If the wall is the combination *operator* (your 4-angle convergence says it is), C2 supplies co-occurrence the substrate still can't bind. The $0 falsifier below is designed to separate exactly these two: channel-has-MI vs substrate-can-use-MI.

## 0. Legality rule (crisp, reusable)

A co-presentation event (A,B) is **earned** iff it would have occurred with the sensor absent — counterfactual independence from the experimenter. We may legally choose *where* the sensor points and *which* pairs to score (selection MI ≤ log #pairs, doesn't carry the pair's structure), but the joint statistic P(A,B co-present | scene) must be authored by the world. Placing an ember next to a seawater bowl in frame = authored joint = #3135-with-a-camera, illegal. Corollary from the measurement metalaw (FORM tunable / BIND earned): **unary concept detectors may be bootstrapped from anywhere** (even pretrained vision nets — unary labels are FORM); only the **joint** must come from the stream. One ban: CLIP-class encoders (image–*text* trained) reinject the text channel — text-free encoders only (DINO/MAE class, or ImageNet-supervised at worst).

## 1. The grounded re-scope task (`G1-concrete`)

- **Channel:** camera, single fixed viewpoint, low fps (~0.2), continuous. Mic optional second modality later; IMU irrelevant (no motion platform). Honest status: **none of this hardware exists on pi5 today** — it is a purchase, not a config.
- **Concepts:** the concrete 83% of the coverage set, restricted to categories with nonzero base rate in the chosen scene. Grounded = a unary detector fires on real frames.
- **Held-out is defined w.r.t. the TEXT channel, not the world:** pairs (A,B) with zero co-occurrence in anima's training corpus, nonzero natural co-presentation rate in the stream. You cannot pick an arbitrary pair and wait for the world to stage it — the world chooses which pairs it covers; the protocol only harvests. Ocean×ember from an indoor camera has base rate ≈ 0; the testable pair set is scene-dependent (kitchen: flame×water, steam×glass…). A $0-hardware intermediate exists: **public webcam streams** (e.g. a beach-bonfire cam) — world-authored, someone else's placement, legal under the rule above.
- **Anti-scheduling protocol:** pre-register sensor placement + recording window *before* selecting test pairs; select pairs from the concept list by fixed hash order; score only pairs reaching ≥N natural co-presentations; never rearrange the scene.

## 2. Minimal physical rig (owner-gated, build only if §3 passes)

Pi Camera Module 3 (~$25) on pi5-akida → per-frame unary concept detectors (small CNN, AKD1000-resident — this is finally a native Lane-A job) → co-presentation events `(A, B, t, frame-embedding)` appended as episodic entries into the **L5 explicit store** (the wired-GREEN faculty), read-side, G5-gated, DISJOINT from the emit-drive lane per `a_substrate_disjoint`. Nothing writes toward the mouth. G1-concrete measurement stays on the canonical `anima evaluate --py` path, pool not mini. Data need to earn ONE pair: realistically weeks of stream for ≥20–30 natural co-presentations of a single textless pair — that is the honest cost of "the world supplies it."

## 3. Pre-physical $0 falsifier (the step you implement)

Proxy world channel = photos of real scenes that we didn't compose: **COCO train2017** (118k images, 80 object categories, 5 captions each). Object annotations = co-presentation events (world-authored joints; the annotator only labels what the world already co-presented). Captions = the text channel over the same world. Two stages, cheapest first.

**Stage A — existence (pure counting, hours, mini-legal):**
For all concrete category pairs: `img_cooc(A,B)` = images where both annotated; `cap_cooc(A,B)` = captions (any of 5) mentioning both.
- **Bar A1:** ≥ 20 pairs with `img_cooc ≥ 20` AND `cap_cooc = 0`. If < 20 → escalate once to Open Images (600 classes, 9M images); if still < 20 → **kill**: the text channel already subsumes the world channel's joint structure — DPI recurses one level up, C2 dead pre-rig.
- **Bar A2:** of A1 survivors, ≥ 10 pairs with |PMI_img| ≥ 0.5 nats, permutation p < 0.01 (1k shuffles of object-sets across images, marginals preserved). PMI ≈ 0 pairs carry no MI beyond unaries — chance co-presence earns nothing.

**Stage B — usability (toy transfer, $0 on owned pool GPU, DIRECTIONAL by design per `a_toy_scale_recheck`):**
Mini-G1 on a toy byte-LM. Condition (i): captions only, held-out pair textually absent (guaranteed by A1). Condition (ii): captions + world-channel events for the held-out pair (annotation-derived event tokens first = upper bound; if it passes, re-run with DINO-class pixel features = strict form). Eval: held-out-pair relation/cloze probe, frozen before training.
- **Bar B:** Δ(ii−i) ≥ +0.10 AUC (or ≥3σ over n=3 seeds), with BOTH controls collapsing to Δ ≤ +0.02: (a) shuffled world channel (pairings randomized), (b) world events for *other* pairs only. Verdict is the margin over bind-destroying controls, never the raw value — metalaw.
- **Most likely failure mode (my modal prediction):** A passes, B fails — world co-presentations enter as an approximately *additive* superposition of unary features, so the substrate extracts two unary detections and no interaction term. That is the combination-operator wall reappearing channel-independently.

## 4. Honest kill condition and what each kill means

- **A fails (both datasets):** the world-proxy channel's joints are already mirrored in text → no earned source exists even in principle at this vocabulary → C2 dead, $0, no rig.
- **A passes, B fails (modal):** the deepest verdict — earned combination-MI *exists* in a non-text channel but a learning substrate cannot convert co-occurrence into a binding operator. The wall is then **not text-specific but a property of any finite experience channel**: experience supplies fuel (pairs), never the engine (operator). Consequence: C2 and every future "new modality" lever is dead as a G1 lever; the operator must be architectural — γ-class trained-constructive-bind remains the sole survivor, exactly as the ledger converged.
- **A and B both pass:** C2 premise holds; the rig is justified — but scope stays `G1-concrete` (sibling gate), and the canonical abstract-concept G1 remains closed to C2 forever. Register that scope split on both hypothesis surfaces before any fire.

Build order: Stage A → (gate) → Stage B → (gate, owner) → rig. I'd pre-register the bars verbatim in the H-card before running Stage A — A1's count is the single number that decides whether C2 lives past this week for the cost of a JSON download.