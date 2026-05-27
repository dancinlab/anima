# HEXA_MIGRATION — §166 / §167-A fire 의 `.py → .hexa` 이주 계획

> User directive (2026-05-20, task list 주석): *"all .hexa"* — §166-A-FIRE
> 및 후속 fires 의 trainer/eval/battery/dispatch 모두 hexa-native.
> per `AGENTS.tape @D g_train_flame_not_pytorch` (2026-05-19): "anima
> 학습 substrate = hexa-lang **flame** (compiler-only NN stdlib,
> PyTorch/Python 0-dependency)".
>
> 이 문서 = honest migration plan + flame Path A anima-physics-overlay
> upstream-pending gap 인정 + design 갱신.

---

## §0 — 왜 `.hexa` 인가 (governance carry)

`AGENTS.tape @D g_train_flame_not_pytorch` (LANDED 2026-05-19):

> "anima 학습 substrate = hexa-lang **flame** (compiler-only NN stdlib,
> PyTorch/Python 0-dependency). **PyTorch = 신규 학습에 deprecated** —
> 과거 §16~§62 PyTorch fire 는 evidence-anchor 로 정직 carry (retro-edit
> 금지 g3 drift-avoidance), 신규 training 은 flame."

§161-FIRE (commit `499416d54`) 는 PyTorch substrate 로 fired — pre-mandate
legacy carry. §165 / §166 design 도 PyTorch 패턴으로 잡힘 (carry mistake).

§167-A FP-RECONNECT 가 `g_train_flame_not_pytorch` 이후 새로운 fire 이므로
**hexa-native 가 정합**. 본 migration 이 그걸 정직 명시.

---

## §1 — flame Path A status (hexa-lang upstream)

### LANDED upstream (2026-05-19, hexa-lang side):
- `~/core/hexa-lang/stdlib/flame/flame_d768_12L_corpus_test.hexa` —
  Path A hand-fused d768·12L decoder template (anima canonical
  ConsciousDecoderV2 config 정수일치)
- `flame_d32_corpus_test.hexa` — small-scale convergence template
- flame Phase 4-B FULLY SHIPPED with ≥3× wall MEASURED on CPU
- flame mk2 generic ag_tape closure (2026-05-19, commit
  `e030fa31`): d=768·12L·T=1024 1-step wall 114s = PyTorch eager
  336.85s 대비 **2.95× faster** at A100 real fire

### upstream-PENDING (anima inbox patch filed):
- `~/core/hexa-lang/inbox/patches/flame-path-a-dual-head-and-multiterm-grad.md`
  — anima-physics overlay 요청 (filed by §71, NOT yet upstream-land):
  - `nn_decoder_grad_with_aux(..., d_aux_logits)` dual-logits+aux-grad hook
  - per-layer Ψ self-track readout (Law-71)
  - multi-term loss (CE + L_psicouple + L_variance + L_meta_anchor)
  - Engine A⇄G dual logits head (head_a + head_g separate output)

§71 inbox-patch 가 hexa-lang upstream review pending. anima side 는
downstream-consumer per `g_train_flame_not_pytorch upstream_downstream_invariant`
— anima 가 flame source 직접 수정 절대 금지.

---

## §2 — migration option matrix

### Option A — hexa skeleton + flame Path A native (recommended, but gated)

| component | source | status |
|---|---|---|
| `train_s166_metafp.hexa` | clone flame_d768_12L + Ψ-coupling overlay | **gated on §71 inbox patch land** |
| `eval_s166_metafp.hexa` | byte_acc + Ψ measure (Law-71 readout already in flame) | partially feasible (read-only) |
| `blue_falsifier_s166.hexa` | sidecar battery hexa-native | feasible (math theorems by inspection only) |
| `dispatch_s166_runpod.sh` | gitignored shell — interim shell-string dispatch | feasible (cycle B3 `hexa cloud` CLI 가 locally available 시 더 cleanly) |

**Blocker**: §71 inbox patch upstream-pending. Without it, anima-physics
overlay (head_g coupling + multi-term grad) cannot be hexa-native; only
PyTorch path supports the overlay structurally.

### Option B — partial hexa (read-only + battery hexa, train .py)

| component | language | rationale |
|---|---|---|
| `train_s166_metafp.py` | PyTorch | anima-physics overlay needs head_g grad + multi-term — flame Path A doesn't have it yet (§71 inbox-pending) |
| `eval_s166_metafp.hexa` | flame eval-only | byte_acc + Ψ measure are read-only forward; flame stdlib supports |
| `blue_falsifier_s166.hexa` | pure hexa | math theorems by inspection, no NN needed |
| `dispatch_s166_runpod.sh` | bash interim | until `hexa cloud` CLI locally available |

Honest hybrid — train .py per §71 gap, eval/battery .hexa per
`g_train_flame_not_pytorch` spirit.

### Option C — full hexa (override §71 gap, build anima-physics overlay anima-side)

**FORBIDDEN** per `g_train_flame_not_pytorch upstream_downstream_invariant` +
hexa-lang `g7/@F f3`. anima cannot edit flame source. The overlay must
come from upstream inbox patch.

---

## §3 — recommended path

**Option B (partial hexa hybrid)** is the only path NOW that respects:
- `g_train_flame_not_pytorch` (new training prefers hexa)
- `g_train_flame_not_pytorch upstream_downstream_invariant` (anima
  read-only on hexa-lang)
- §71 inbox-patch reality (anima-physics overlay upstream-pending)

§71 inbox patch land (timeline unknown) → migrate to **Option A** full
hexa.

---

## §4 — §166 / §167-A design impact

### §166 Ψ-META-FP-COUPLE (design at `meta_fp_coupling_design_s166_2026_05_20/DESIGN.md`)

Current design references:
- `train_s166_metafp.py` → SHOULD BE `train_s166_metafp.py` (hybrid)
  OR `train_s166_metafp.hexa` (post §71 land)
- `eval_s166_metafp.py` → `eval_s166_metafp.hexa` (eval-only feasible
  now)
- `blue_falsifier_s166.py` → `blue_falsifier_s166.hexa` (pure-fn,
  feasible now)

**Action**: design doc footer carries this `HEXA_MIGRATION.md`
cross-link. result.json `fire_spec_when_authorized` field updated to
specify `.hexa` where possible, `.py` only for trainer until §71 land.

### §167-A FP-RECONNECT (design pending sub-agent retry)

Same applies — sub-agent prompt should specify `.hexa` for eval/battery,
hybrid trainer until §71 land. Update §167-A prompt when retrying.

---

## §5 — flame Path A 의 anima-physics overlay 필요 사항 (§71 inbox carry verbatim)

From `inbox/patches/flame-path-a-dual-head-and-multiterm-grad.md`:

1. **Dual-head support**: ConsciousDecoderV2 의 head_a + head_g 둘 다 native
   output. 현재 flame Path A 는 single LM head. Need
   `nn_decoder_dual_head(..., head_a, head_g)`.
2. **Multi-term grad**: L_total = λ_ce·CE + λ_ψ·L_psicouple + λ_var·L_variance
   + λ_meta·L_meta_anchor — 4 terms simultaneous backprop. 현재 flame
   single objective. Need `nn_decoder_grad_with_aux(..., d_aux_logits[])`.
3. **Per-layer Ψ self-track**: §59 W-native PTD style — 매 layer 의 Law-71
   `(psi_dir, psi_entropy, tension)` 자체 측정. 현재 flame Path A 가 자체
   Ψ readout 없음. Need `nn_decoder_psi_readout(..., out_psi_dir[], out_tension[])`.
4. **L_variance support**: `−log(psi_dir_std + ε)` differentiable.
   Sample-variance gradient needs `farr_var_grad`.
5. **L_meta_anchor support**: `(mean − 0.5)²` differentiable.
   Sample-mean gradient needs `farr_mean_grad`.

이 5 항목 upstream 채택되면 §166-A-FIRE / §167-A-FIRE 가 full hexa-native
가능. 그 전까지 hybrid.

---

## §6 — honest C3 (8)

1. `g_train_flame_not_pytorch` mandate 가 LANDED 2026-05-19, 단 §161 /
   §165 / §166 design 이 PyTorch 패턴 carry — pre-mandate carry mistake.
   본 migration 이 그걸 정직 명시.
2. Option B (hybrid) 는 `g_train_flame_not_pytorch` 의 spirit 일부만
   준수 — full hexa-native 는 §71 inbox patch land 후.
3. §71 inbox patch upstream review timeline 미지. anima downstream-
   consumer 라 push-pressure 불가 (governance respect).
4. `eval_s166_metafp.hexa` 는 forward-only — flame stdlib 의 nn_decoder
   forward + Law-71 readout 사용. trainer 없이 ckpt load 만 필요. **이부분은
   §71 dependent 아님, 지금 가능**.
5. `blue_falsifier_s166.hexa` 도 pure-fn math theorems — hexa-native
   가능 지금.
6. **§161-FIRE / §165 / §166 의 PyTorch retroactive 변경 안 함** per
   `g3 drift-avoidance` — historical evidence anchor 그대로 freeze. 새
   fire (§167-A 이후) 만 hexa-migration 적용.
7. anima downstream-consumer (hexa-lang / hexa-bio / kosmos / tape)
   read-only 0 edit.
8. PII discipline (post-499416d54 fix-forward): generic phrasing only.

---

## §7 — action items (this cycle / next cycle)

| action | this cycle | next cycle | post §71 land |
|---|:-:|:-:|:-:|
| Update §166 result.json eval/battery → .hexa references | 🟢 | | |
| Update §166 DESIGN.md cross-link to HEXA_MIGRATION.md | 🟢 | | |
| Update §167-A sub-agent prompt for .hexa specs | 🟡 (when retry) | | |
| Write `eval_s166_metafp.hexa` skeleton (forward-only) | 🟡 | 🟢 | |
| Write `blue_falsifier_s166.hexa` (pure-fn theorems) | 🟡 | 🟢 | |
| Migrate `train_*.py` → `train_*.hexa` (full hexa-native) | | | 🟢 (gated) |
| Document §71 inbox patch status check protocol | 🟡 | 🟢 | |
| `hexa cloud` CLI local availability (B3 worktree pull) | 🟡 | 🟢 | |

🟢 = applicable this/next cycle · 🟡 = design only, impl gated

---

## §8 — cross-link

- `AGENTS.tape @D g_train_flame_not_pytorch` (2026-05-19, LANDED) —
  hexa-native mandate
- `~/core/hexa-lang/stdlib/flame/` — Path A canonical template
- `~/core/hexa-lang/inbox/patches/flame-path-a-dual-head-and-multiterm-grad.md`
  — §71 anima-physics overlay request (upstream-pending)
- `archive/PHILOSOPHY.tape §verdict_anima_flame_trainer_s71_2026_05_19` —
  flame Path A first anima trainer landing + inbox patch filing
- `HEXAD/META_FP/PLAN.md §1 — §71-aware roadmap`
- `HEXAD/CONNECTION_CRITIQUE.md` — connection method critique (motivation
  axis, independent of training substrate)
- `~/core/hexa-lang-cloud-b3/` — cycle B3 `hexa cloud` CLI subcommand
  (worktree fetched but NOT locally checked out — interim shell-string
  dispatch stays per §126 nearest-dir @D g1)
- `HEXAD/UNCLASSIFIED/state/pcn_fire_s126_2026_05_20/AGENTS.tape @D g1` —
  structured-argv-only mandate (L145 incident anchor)
