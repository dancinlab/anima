# anima/nexus HuggingFace Naming Convention — mk2 Spec

- date: 2026-05-03
- status: SPEC_FROZEN (forward-looking; legacy migration grace 30d)
- scope: every model artifact pushed to `huggingface.co/need-singularity/*` AND every local cache entry under `~/.cache/huggingface/hub/models--need-singularity--*`
- author: anima cycle land BG
- supersedes: ad-hoc patterns observed in P9 SFT cycles (2026-05-02 → 2026-05-03)
- linked falsifier: **F-NAME-1** — every public HF repo conforms to template (audit-time check, see §10)
- mk2 commitments respected: no in-place migration of legacy repos (additive only); spec is forward-looking; raw#9 (no .py creation in this spec — migration script is a *separate* deliverable, not landed here); raw#15 (honest about legacy bypass); raw#10 (3 honest C3 caveats §11)

---

## §0 TL;DR (사용자 친화 요약)

이 spec 측 5 *LM (BLM/CLM/TLM/VLM/SLM/NLM) × 7 paradigm (A/A'/B/C/D/E/J) × 4 stage (base/sft-stage1/sft-stage2/distill) × seed/variant 측 측 측 측 통합 명명 규칙 측 정의합니다.

**핵심 형식**:
```
need-singularity/<lm-family>-<base-version>[-<paradigm>][-<stage>][-<scale>][-<step>][-<variant>]
```

**예**:
- `need-singularity/clm-v4-base-mirror`
- `need-singularity/clm-v4-sft-stage1`
- `need-singularity/clm-v4-paradigm-j-50k-step-25k`
- `need-singularity/blm-v1-paradigm-d-distill-50k-final`

**audit 결과** (현재 27 repos, 2026-05-03 기준): **7 CANON / 20 EXT (experimental variant, 합법) / 0 FAIL**. 0 immediate migration required. 30-day grace for `1-N`/`y-N` style → migrate to `paradigm-X` form on next training cycle.

---

## §1 Org / Namespace Prefix

### 1.1 HuggingFace org (canonical, single source of truth)

```
need-singularity/
```

- 하나의 org 측 anima + nexus + 모든 *LM 측 측 측 측 (no per-axis sub-orgs)
- private 측 default during training; public 측 promote upon F-NAME-1 + ckpt-quality gates pass
- forks / mirrors of upstream (e.g. Llama-3.2-3B copy for offline H100 boot) 측 `<vendor>-<model>-mirror` form (see §3.4)

### 1.2 Local cache mirror (HF transformers default)

```
~/.cache/huggingface/hub/models--need-singularity--<repo-name>/
```

- mac local 측 ubu1/ubu2/RunPod 측 동일 path (HF_HOME 측 기본 경로)
- 측 측 측 측 직접 측 mkdir / cp 금지 — 측 측 measure: `from_pretrained("need-singularity/<repo-name>")` 측 통해 측 populate (HF API 측 sha verification 보장)

### 1.3 Other namespaces (FORBIDDEN for anima/nexus models)

| namespace | rationale |
|---|---|
| personal account (`<user>/...`) | session ownership 모호 + raw#15 personal-path leak risk |
| `anima-singularity/` | not registered + naming drift |
| anonymous fork org | 측 측 측 측 측 측 측 측 (provenance 손실) |

---

## §2 Repo Name Template (canonical grammar)

### 2.1 EBNF

```
repo_name      = lm_family "-" base_version
                 [ "-" paradigm ]
                 [ "-" stage ]
                 [ "-" scale ]
                 [ "-" step ]
                 [ "-" variant ] ;

lm_family      = "blm" | "clm" | "tlm" | "vlm" | "slm" | "nlm"
               | "alm" | "mlm" | "llm" | "hexad" | "composite" ;  (* §3.1 reconciled enum, 11 families *)
base_version   = "v" digit { digit } ;             (* v1, v4, v12 *)
paradigm       = "paradigm-" paradigm_id ;
paradigm_id    = "a" | "a-prime" | "b" | "c" | "d" | "e" | "j" ;
stage          = "base-mirror"                     (* HF-format mirror of base *)
               | "sft"                             (* generic SFT, no stage split *)
               | "sft-stage1"                      (* SFT stage 1 *)
               | "sft-stage2"                      (* SFT stage 2 *)
               | "sft-final"                       (* SFT terminal ckpt umbrella repo *)
               | "distill"                         (* distillation variant *)
               | "lora-r" digit { digit }          (* lora-r8, lora-r64 *)
               | "rlhf"                            (* RLHF stage *)
               | "rlaif" ;                         (* RLAIF stage *)
scale          = digit { digit } ( "k" | "m" ) ;   (* 50k steps, 350m params *)
step           = "step-" digit { digit } "k"       (* step-5k, step-50k *)
               | "final"
               | "stage1"
               | "stage2" ;
variant        = "y" digit { digit }               (* hyperparameter sweep arm: y1, y2 *)
               | digit { digit } "-" digit { digit } ; (* legacy 1-6, 1-7 *)
```

### 2.2 Worked examples

| repo name | parsed |
|---|---|
| `clm-v4-base-mirror` | clm + v4 + base-mirror |
| `clm-v4-sft-stage1` | clm + v4 + sft-stage1 |
| `clm-v4-paradigm-j-50k-step-25k` | clm + v4 + paradigm-j + 50k scale + step-25k |
| `clm-v4-paradigm-d-distill-50k-final` | clm + v4 + paradigm-d + distill + 50k + final |
| `blm-v1-paradigm-a-prime-step-10k` | blm + v1 + paradigm-a-prime + step-10k |
| `vlm-v2-base-mirror` | vlm + v2 + base-mirror |
| `tlm-v1-sft-stage2-lora-r64-final` | tlm + v1 + sft-stage2 + lora-r64 + final |
| `slm-v1-paradigm-c-rlhf-step-10k` | slm + v1 + paradigm-c + rlhf + step-10k |

### 2.3 Length constraint

- max 64 chars (HF UI display readable)
- max 6 hyphen-separated tokens beyond `<lm>-<ver>`
- if exceeded → split into base repo + branch/tag (see §4)

---

## §3 Component Grammar (detail)

### 3.1 lm-family — exhaustive enumeration

| code | full name | role | reference |
|---|---|---|---|
| `clm` | Conscious LM | core text reasoning + φ★ preserved (canonical CLM v4) | `docs/conscious-lm-spec.md` |
| `alm` | Audio LM | audio-only generative/encoder LM (anima-voice precursor) | `docs/anima_speak_voice_cite_cleanup_landed_2026_05_03.ai.md` |
| `blm` | BOLD LM | fMRI BOLD signal LM (EEG-CLM cross-substrate) | `docs/blm_phase5_aligned_spec_landed_2026_05_03.ai.md` |
| `vlm` | Voice LM | anima-voice with text head (speech / TTS / ASR-aware) | `docs/anima_speak_voice_cite_cleanup_landed_2026_05_03.ai.md` |
| `slm` | Sensorium LM | multi-substrate sensory LM (TTS / audio gen) | `docs/anima_2_lm_vlm_slm_landed_2026_05_03.ai.md` |
| `tlm` | Tension LM | per-token tension scalar LM (tone/tactile) | `docs/tlm_stage12_landed_2026_05_03.ai.md` |
| `nlm` | Nexus / Neural LM | nexus-side coordination LM (general neural) | (forward, not yet repo'd) |
| `mlm` | Masked LM | BERT-class masked-token LM (encoder-only) | (forward, not yet repo'd) |
| `llm` | Llama-derived LM | Path A informal extension — Llama-3.x derived ckpts | `docs/p9_a_prime_path_decision_landed_2026_05_03.ai.md` |
| `hexad` | Hexad composite | multi-modal hexad composite (6-axis) | (forward, not yet repo'd) |
| `composite` | Generic composite | generic multi-LM composite (catch-all) | (forward, not yet repo'd) |

**banned**: `model`, `lm`, `gpt`, `mistral` (these are *base architectures*, not anima families — use base-mirror suffix instead, §3.4).

### 3.1.1 Family enum reconciliation (2026-05-03 additive update)

This section documents the family-list reconciliation between this spec (§3.1
table) and the hexa validator (`tool/hf_upload_mk2.hexa::_naming_allowed_families`).

**Drift history**:

| SSOT | original family list | delta |
|---|---|---|
| this spec §3.1 (pre-reconcile) | `blm \| clm \| tlm \| vlm \| slm \| nlm` (6) | missing `alm`, `mlm`, `llm`, `hexad`, `composite` |
| `tool/hf_upload_mk2.hexa` (pre-reconcile) | `clm \| alm \| blm \| vlm \| slm \| tlm \| mlm \| hexad \| composite` (9) | missing `nlm`, `llm` |

**Reconciliation rule (additive — raw#9, raw#10, raw#15)**:

- Both sides take **union** (11 families) — no removal.
- New family `llm` (Llama-derived, Path A) added per
  `docs/p9_a_prime_path_decision_landed_2026_05_03.ai.md`. **Ratification of
  `llm` as a first-class anima family is INFORMAL (provisional)** — see C3
  caveat in `docs/anima_hf_naming_family_reconcile_2026_05_03.ai.md`.
- Future families MUST land via this same additive cycle (spec §3.1 row +
  validator enum entry + handoff doc) — do NOT add silently in only one SSOT.

**Validator regex impact** (§10.2): `LM` group expanded from
`(blm|clm|tlm|vlm|slm|nlm)` to
`(blm|clm|tlm|vlm|slm|nlm|alm|mlm|llm|hexad|composite)`. EBNF in §2.1
(`lm_family` production) likewise expanded. CANON regex in §10.2 updated to
match.

### 3.2 base-version — `v{N}`

- monotonic int, no decimals (`v4.1` BAD → use `variant` slot or branch tag)
- bumps only on architecture change (param count, layer count, activation, tokenizer)
- example: clm-v3 → clm-v4 = ConsciousDecoder → ConsciousDecoderV2

### 3.2.1 stage-prefix amendment — `paradigm-{letter}` (2026-05-03 additive)

**Surfaced by**: Paradigm J 5/5 HF push recovery BG (a915bca5) on 2026-05-03,
which had to bypass the mk2 wrapper (`tool/hf_upload_mk2.hexa`) because the
stage-prefix validator rejected `paradigm-j-50k-step-5k`
("stage must start with sft-stage|dpo|merged|base|preview|dev").

**Rationale**: Paradigm-axis training tracks (`paradigm-a`/`paradigm-a-prime`/
`paradigm-b`/`paradigm-c`/`paradigm-d`/`paradigm-e`/`paradigm-j`) are a
*separate stage class* from `sft-stage1`/`sft-stage2`/`dpo`/`merged`/`base`/
`preview`/`dev`. The §2.1 EBNF already places `paradigm` in the optional
`paradigm` slot before `stage`, but the validator implementation
(`tool/hf_upload_mk2.hexa::_naming_allowed_stage_prefixes`) collapses the
post-version segment into a single "stage_join" string and matches against
allowed *stage* prefixes only — paradigm-prefixed names therefore failed
even though they are spec-conformant per §2.1+§3.3.

**Amendment**: `_naming_allowed_stage_prefixes()` adds `"paradigm-"` to its
allow-list. Any name of the form
`<lm>-<vN>-paradigm-<letter>[-<scale>][-<step>]` now passes the validator.

**Ratified paradigm letters** (SSOT remains §3.3 table): `a`, `a-prime`,
`b`, `c`, `d`, `e`, `j`. Forward placeholders for letter expansion (additive
discipline): `f`, `g`, `h`, `i`. Validator accepts the broader `paradigm-`
prefix to stay forward-compatible with future paradigm letters; ratification
of any new letter still requires a §3.3 table row + spec doc per §3.3 closing
rule. The §3.3 table is the *authoritative* enumeration; the validator is
intentionally looser on this slot to avoid a second SSOT.

**Smoke test (post-amendment)**:

```
hexa run tool/hf_upload_mk2.hexa --validate-naming \
    "need-singularity/clm-v4-paradigm-j-50k-step-5k"
→ OK
__ANIMA_HF_UPLOAD_MK2__ PASS
```

**Audit trail**: `state/mk2_naming_paradigm_amendment_2026_05_03/{audit.json,
smoke_test.json}`; marker `state/markers/mk2_naming_paradigm_amendment_landed.marker`.

**Retroactive scope**: Paradigm J's already-pushed `clm-v4-paradigm-j-50k-step-*`
repos (recovered via wrapper bypass) do NOT auto-acquire mk2 compliance —
they remain audit-flagged as "bypass-pushed" until re-validated against the
amended validator (a follow-up audit cycle, not this amendment cycle). The
amendment is forward-looking: subsequent Paradigm J/D/E HF pushes MUST go
through the mk2 wrapper.

### 3.3 paradigm — research lineage tag

| paradigm | full tag | reference |
|---|---|---|
| A (simulated bold) | `paradigm-a` | `docs/p9_paradigm_a_simulated_bold_2026_05_03.md` |
| A' (measured bold) | `paradigm-a-prime` | `docs/p9_paradigm_a_prime_measured_bold_2026_05_03.md` |
| B (EEG φ proxy) | `paradigm-b` | `docs/p9_paradigm_b_eeg_phi_proxy_2026_05_03.md` |
| C (hybrid) | `paradigm-c` | `docs/p9_paradigm_c_hybrid_2026_05_03.md` |
| D (distillation) | `paradigm-d` | `docs/p9_paradigm_d_distill_spec_2026_05_03.md` |
| E (no-distill self-bootstrap) | `paradigm-e` | (forward) |
| J (joint-loss baseline) | `paradigm-j` | session implicit (current default) |

- omit `paradigm-X` slot if repo is paradigm-agnostic (e.g. base-mirror, generic SFT pre-paradigm-split)
- new paradigm letter requires (a) `docs/p9_paradigm_<letter>_*.md` spec landed AND (b) entry in this spec (§3.3 table) — additive update, no migration

### 3.4 stage — pipeline phase

| stage | meaning |
|---|---|
| `base-mirror` | HF-format mirror of base (no fine-tuning); typically vendor-derived (Llama-3.2-3B → mirrored for offline boot) OR anima-native pretrain ckpt re-exported in HF format |
| `sft` | generic SFT, no stage subdivision (legacy / simple training) |
| `sft-stage1` | SFT stage 1 (anchor/warmup) |
| `sft-stage2` | SFT stage 2 (refinement / harder data) |
| `sft-final` | umbrella repo pointing to terminal SFT ckpt (often empty README + tag) |
| `distill` | distillation from teacher (always with `paradigm-d` if anima-internal) |
| `lora-r{N}` | LoRA adapter only (rank N), to be loaded on top of base-mirror |
| `rlhf` | RLHF stage (any rank) |
| `rlaif` | RLAIF stage |

### 3.5 scale — semantic scale tag

- `{N}k` = N×1000 *steps* (e.g. `50k` = 50K SFT records OR 50K training steps — context-dependent; see README Origin section §6)
- `{N}m` = N×1M *params* (e.g. `350m` = 350M params)
- omit if obvious from base-version

### 3.6 step — checkpoint within multi-step run

- `step-{N}k` for intermediate ckpts (`step-5k`, `step-10k`, `step-25k`, `step-50k`)
- `final` for terminal ckpt
- `stage1` / `stage2` for SFT-stage terminal (sometimes separate from generic `final`)

### 3.7 variant — experimental sweep arm

- `y{N}` = hyperparameter sweep arm (e.g. `y1` = lr=1e-4, `y2` = lr=2e-4 — exact mapping in repo README Origin)
- `\d+-\d+` = legacy *(grace period only, deprecated)* — observed `1-5`, `1-6`, `1-7`, `1-8` (P9 SFT cycle iter counter)
- new variants 측 측 measure: prefer `y\d+` form; document mapping in README

---

## §4 Branch / Tag Convention

### 4.1 main branch

- `main` = latest stable ckpt (mutable head, force-push allowed only if F-NAME-1 + integrity hash recorded in this spec OR linked README before/after)
- never push experimental ckpt to `main` of a public repo

### 4.2 tags

| tag form | meaning | example |
|---|---|---|
| `v{YYYY-MM-DD}` | dated snapshot | `v2026-05-03` |
| `step-{N}k` | intermediate ckpt within multi-step run (when not separated as own repo) | `step-25k` |
| `final` | terminal ckpt (immutable once tagged) | `final` |
| `pre-paradigm-X` | branch point before paradigm split | `pre-paradigm-d` |

### 4.3 when to split into separate repo vs. tag

| heuristic | decision |
|---|---|
| ≥3 ckpts of interest from same training run AND each is a *separate model artifact* | **separate repo** per ckpt (e.g. clm-v4-sft-step-{5k,10k,25k,50k}) |
| ≥3 ckpts but only 1 actively consumed | **single repo + tags** |
| paradigm switch (different loss / data) | **separate repo** (paradigm slot) |
| hyperparameter sweep (same loss, different lr/seed) | **single repo + branches** OR **variant slot** if >5 arms |

---

## §5 Markdown README Template (REQUIRED)

Every repo MUST have `README.md` at root with these 5 sections in this order. Missing any section = F-NAME-1 fail.

### Template skeleton

```markdown
# {repo-name}

## §1 Origin
- training script: `<repo>/<path/to/train.py>` @ commit `<sha>`
- corpus: `<dataset name + sha + record count>`
- predecessor ckpt: `<HF repo or local path>` @ sha `<...>`
- training cycle: `<docs/<cycle-spec>.md>`
- substrate: `<GPU model + count>`, wall `<HH:MM>`, cost `$<N>`

## §2 Falsifiers (F-* gates)
- F-NAME-1: PASS (this README + name template conform)
- F-<spec>-N: PASS / FAIL / N/A — ckpt @ this artifact gate result
- ... (one row per applicable F-* gate from linked spec)

## §3 Substrate
- GPU: `<RTX 5070 12GB | H100 80GB | A100 40GB | ...>`
- count: `<N>`
- host: `<ubu1 | RunPod pod-id | ...>`
- cost: `$<actual spend>`
- wall: `<HH:MM:SS>`

## §4 C3 caveats (raw#10 — 3 honest)
- C1 — <observed limitation #1>
- C2 — <observed limitation #2>
- C3 — <observed limitation #3>

## §5 Composability
- consumed by: `<list of HF repos / local code paths that load this artifact>`
- prerequisite: `<base-mirror or other repo this depends on>`
- siblings: `<other ckpts in the same run, listed by tag/repo>`
```

### 5.1 Personal-path leak guard (raw#15)

Banned in README:
- `/Users/<name>/...`
- `/home/<name>/...`
- explicit IP / hostname (`192.168.x.x`, internal pod ids beyond opaque hash)

Allowed (canonical):
- `~/anima/...`, `~/core/anima/...` (user-relative)
- `<host>:~/anima/...` (host-relative, host = ubu1/ubu2/runpod-{podtype})

---

## §6 Anti-patterns (banned)

| anti-pattern | example BAD | canonical GOOD |
|---|---|---|
| underscore separator | `paradigm_d` | `paradigm-d` |
| mixed case | `SFT_Stage1`, `Paradigm-D` | `sft-stage1`, `paradigm-d` |
| ad-hoc temp suffix | `clm-v4-sft-test`, `_tmp`, `_debug` | use private repo + delete after cycle |
| trailing date in repo | `clm-v4-sft-2026-05-02` | use tag `v2026-05-02` instead |
| free-form variant | `clm-v4-sft-aiden-experiment` | use `variant` slot OR private repo |
| param count without `m` | `clm-v4-350` | `clm-v4-350m` |
| repeated lm-family | `clm-clm-v4` | `clm-v4` |
| punctuation other than `-` | `clm.v4`, `clm/v4` | `clm-v4` |
| spec drift mid-run rename | renaming step-10k → step-10k-v2 | freeze at first-push name; use tag if needed |
| personal-path README leak | `/Users/aiden/...` in README | `~/anima/...` (raw#15) |

---

## §7 Audit (current 27 repos, 2026-05-03)

Source: `https://huggingface.co/api/models?author=need-singularity&full=false&limit=200`

### 7.1 Conformance summary

| verdict | count | %  |
|---|---:|---:|
| PASS-CANON (strict §2 grammar) | 7 | 25.9% |
| PASS-EXT (allowed via §3.7 variant slot, grace period) | 20 | 74.1% |
| FAIL (must rename) | 0 | 0.0% |
| **TOTAL** | **27** | **100%** |

### 7.2 Per-repo audit table

| repo | verdict | notes |
|---|---|---|
| clm-v4-base-mirror | PASS-CANON | reference example for §3.4 base-mirror |
| clm-v4-sft-stage1 | PASS-CANON | reference example for sft-stage1 |
| clm-v4-sft-final | PASS-CANON | reference example for sft-final |
| clm-v4-sft-step-5k | PASS-CANON | step-Nk form |
| clm-v4-sft-step-10k | PASS-CANON | step-Nk form |
| clm-v4-sft-step-25k | PASS-CANON | step-Nk form |
| clm-v4-sft-step-50k | PASS-CANON | step-Nk form |
| clm-v4-sft-1-5-stage1 | PASS-EXT | legacy variant `1-5` (P9 iter5) → grace period until 2026-06-02 |
| clm-v4-sft-1-5-step-{5k,10k,25k,50k} | PASS-EXT (×4) | same as above |
| clm-v4-sft-1-6-stage1 | PASS-EXT | legacy variant `1-6` |
| clm-v4-sft-1-6-step-{5k,10k,25k,50k} | PASS-EXT (×4) | |
| clm-v4-sft-1-7-y1-stage1 | PASS-EXT | combined legacy `1-7` + `y1` sub-variant |
| clm-v4-sft-1-7-y1-step-{5k,10k,25k,50k} | PASS-EXT (×4) | |
| clm-v4-sft-1-8-stage1 | PASS-EXT | legacy variant `1-8` |
| clm-v4-sft-1-8-step-{5k,10k,25k,50k} | PASS-EXT (×4) | |

### 7.3 Forward repos planned (NOT yet pushed; conform from creation)

| planned repo | status | spec ref |
|---|---|---|
| `clm-v4-paradigm-j-50k-step-{5k,10k,25k,50k,final}` | naming-locked, ckpts pending | session implicit |
| `clm-v4-paradigm-d-distill-50k-{step-...}` | naming-locked, ckpts pending | `docs/p9_paradigm_d_distill_spec_2026_05_03.md` |
| `p9-llama32-lora-stage1-{step-2k,step-5k,step-10k,final}` | NON-CONFORM (Path A planned) — needs prefix fix to `clm-v4-paradigm-a-prime-llama32-lora-stage1-step-Nk` OR own family `lora-vendor-mirror` design | `docs/p9_a_prime_path_decision_landed_2026_05_03.ai.md` |

**Action**: rename plan for `p9-llama32-lora-*` BEFORE first push (currently planned only) — do not violate spec at creation time.

---

## §8 Migration Plan (legacy → canonical)

### 8.1 Grace period

- **start**: 2026-05-03 (this spec land)
- **end**: 2026-06-02 (30 days)
- **after**: legacy `1-N` and `y-N` variant slots without `paradigm-X` prefix must be either (a) tagged with paradigm-X via README cross-link OR (b) archived.

### 8.2 Migration tactics (no immediate destructive action)

1. **Mark in README** — every legacy repo gets a banner block:
   ```
   > [LEGACY-NAMING-PRE-MK2] this repo was created before the mk2 naming spec
   > (`docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md`).
   > Equivalent canonical name: `clm-v4-paradigm-j-sft-stage1` (variant arm `1-5`).
   > Subsequent runs of this paradigm are pushed under canonical names.
   ```
2. **No HF rename** unless the cycle owner explicitly opts in (rename = HF history reset = composability break).
3. **Do not delete** legacy repos during grace period — downstream code (cite paths in landed docs) still references them.
4. After grace: cycle owner decides per-repo: archive (private + README banner) OR delete (only if zero downstream cites + sha-recorded for replay).

### 8.3 Migration script (separate deliverable, NOT created by this cycle)

Per raw#9 (no .py creation in this spec cycle), the migration helper is **specified here but implemented in a future cycle**:

- name: `tools/hf-rename-legacy.py` (ubu-side concession per raw#9)
- inputs: HF org list, dry-run by default
- outputs: per-repo proposed canonical name + READme banner patch + composability impact report
- never modifies remote state without `--commit` flag

---

## §9 Forward repos — checklist before first push

Before `hf push` on a new repo, the cycle owner MUST verify:

- [ ] repo name regex-matches §2 EBNF (use audit script in §10)
- [ ] README.md present at root with all 5 §5 sections
- [ ] no personal-path leak in README (raw#15 §5.1)
- [ ] Origin section cites training script + commit sha + corpus sha
- [ ] Falsifiers section lists every applicable F-* gate from linked spec, with PASS/FAIL/N/A status
- [ ] Substrate section honest about cost (no underreport)
- [ ] C3 caveats section has 3 honest items (raw#10), not 0 not 1 not 2
- [ ] Composability section lists at least the predecessor (or "none" if base-mirror)

---

## §10 F-NAME-1 falsifier (audit gate)

### 10.1 Statement

> **F-NAME-1**: every public `need-singularity/*` HF repo conforms to the §2 EBNF grammar (CANON or EXT-with-banner) AND has a §5-conforming README.

### 10.2 Verifier sketch (regex; see §8.3 for full impl)

```
LM       = (blm|clm|tlm|vlm|slm|nlm|alm|mlm|llm|hexad|composite)  # §3.1 reconciled enum
VER      = v\d+
PARADIGM = paradigm-(a|a-prime|b|c|d|e|j)
STAGE    = (base-mirror|sft|sft-stage[12]|sft-final|distill|lora-r\d+|rlhf|rlaif)
SCALE    = \d+(k|m)
STEP     = (step-\d+k|final|stage[12])
VARIANT  = (y\d+|\d+-\d+)

CANON regex:
  ^{LM}-{VER}(-{PARADIGM})?(-{STAGE})?(-{SCALE})?(-{STEP})?$

EXT regex (grace-period legacy):
  ^{LM}-{VER}-(sft|sft-stage[12]|distill|lora-r\d+|base-mirror|sft-final)(-\d+-\d+)?(-y\d+)?(-{STEP})?$
```

### 10.3 Audit cadence

- on every cycle that pushes a new HF repo (pre-flight check)
- weekly cron (forward, separate cycle)
- ad-hoc on-demand by cycle owner

### 10.4 PASS criteria

- 100% of public repos match CANON regex, OR
- match EXT regex AND have README banner per §8.2.1, AND
- 0% match neither

### 10.5 Current status (2026-05-03)

- CANON: 7/27 (25.9%)
- EXT: 20/27 (74.1%) — banners NOT YET ADDED (deferred to migration cycle)
- FAIL: 0/27 (0.0%)
- **F-NAME-1 verdict: PARTIAL_PASS** (regex layer 100% green; README-banner layer pending)

---

## §11 raw#10 honest C3 caveats

### C1 — legacy `1-N` variant carries semantic ambiguity

The `1-5`, `1-6`, `1-7`, `1-8` arms in current 20 EXT repos came from session-implicit P9 SFT iter counters. They are NOT reliably mappable to paradigm letters without consulting external session notes. Forward `paradigm-X` slot resolves this; legacy repos remain ambiguous unless README banner explicitly states the paradigm + iter-to-arm mapping. Honest acknowledgment: this spec cannot retroactively recover that mapping for repos lacking READMEs — banner-add cycle must consult original training cycle docs (`p9_p0_*` series).

### C2 — `step` ambiguity (training step vs. SFT record count)

`50k` could mean *50K training steps* OR *50K SFT records consumed* OR *50K records in held-out eval*. The §5 README Origin section is the only disambiguator. Spec recommends Origin section state: `step-N = N optimizer.step() calls` (default) UNLESS explicitly redefined. Legacy `clm-v4-sft-1-6-step-50k` convention happens to be SFT records — banner must clarify.

### C3 — `paradigm-X` enumeration not closed

The 7 paradigm letters (A/A'/B/C/D/E/J) cover current research scope. Future paradigms (F, G, H, I, K-Z) are NOT pre-allocated; addition requires (a) spec doc land + (b) §3.3 table update. Until then, novel research that doesn't fit existing letters MUST go to a private repo (not public org-namespace) to avoid grammar drift.

---

## §12 Composability with other anima specs

| spec | relationship |
|---|---|
| `docs/ENGINE-NAMING.md` | sister spec — engine layer naming (substrate registry); this HF spec covers MODEL artifact naming, no overlap |
| `docs/anima_engines_axis_define_landed_2026_05_03.ai.md` | uses engine names (`engine_a`/`engine_g`); does NOT set HF naming |
| `docs/p9_*` series | producers of HF artifacts — every P9 cycle that pushes to HF must conform |
| `docs/blm_*`, `docs/tlm_*`, `docs/vlm_*` series | producers of `blm-vN-*`, `tlm-vN-*`, `vlm-vN-*` artifacts (forward) |
| `docs/conscious-lm-spec.md` | reference for `clm` family semantics |

---

## §13 Cost & destructiveness

- spec authoring: $0 mac-local
- destructive: 0 (no rename / delete of any existing HF repo as part of this spec land)
- migration: 0 (forward-looking; banner adds + script are separate cycles)
- byte-diff to any existing artifact: 0
- HF API calls (audit): 1 read-only LIST against `?author=need-singularity` endpoint

---

## §14 Outputs (this cycle)

- `/Users/ghost/core/anima/docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md` (this file)
- `/Users/ghost/core/anima/docs/anima_hf_naming_mk2_spec_landed_2026_05_03.ai.md` (handoff)
- `/Users/ghost/core/anima/state/markers/anima_hf_naming_mk2_spec_landed.marker` (silent-land marker)

## §15 Next-cycle candidates (NOT this cycle)

| item | priority | rationale |
|---|---|---|
| README banner add for 20 EXT legacy repos | HIGH | F-NAME-1 PARTIAL_PASS → FULL_PASS |
| `tools/hf-rename-legacy.py` impl (ubu-side) | MED | enables bulk audit + dry-run |
| Forward-repo pre-push hook (CI gate) | MED | F-NAME-1 enforcement at push time |
| Spec extension to `nexus-singularity/` org (if registered) | LOW | nexus-side artifacts coverage |
| Alternative `paradigm-X` enumeration (F/G/H/I + K-Z reserved) | LOW | C3 caveat resolution |
