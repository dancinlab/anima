# `.own` UPGRADE Reconciliation — orpheus + wraith-wallet

- **cycle**: own_upgrade_reconciliation_2026_05_04
- **ts_utc**: 2026-05-04T11:30:43Z
- **scope**: surface conflict between BG-ζ POST_MK2_RECENT review queue (recommendation: REMEDIATE/UPGRADE) and Option B chosen by user (DELETE), and provide informational recovery recipe.
- **action taken**: NONE (read-only / informational). No `.own` recreated. No commit. No push.

---

## 1. The conflict, surfaced

### 1.1 BG-ζ recommendation (commit 39b83cb9)

- POST_MK2_RECENT review queue identified `orpheus/.own` + `wraith-wallet/.own` as candidates for **REMEDIATE** = mk2 frontmatter UPGRADE (preserve content, update schema_version + add mk2 fields).

### 1.2 Option B chosen (commits 6a1fc6c orpheus / 5f09433 wraith-wallet, both 2026-05-04)

- User chose Option B = **DELETE** under "dual-SSOT EOL" rationale.
- Commit messages (verbatim):
  - orpheus: `chore(.own removal — mk1_GRANDFATHER POST_MK2_RECENT; per anima 2026-05-04 dual-SSOT EOL Option B)`
  - wraith-wallet: `chore(.own removal — mk1_GRANDFATHER sibling to orpheus; per anima 2026-05-04 dual-SSOT EOL Option B)`
- User policy cited: ".own commit history에만 보관" (preserve in git history only).

### 1.3 Incompatibility

- UPGRADE = file remains as live SSOT, content preserved, schema bumped.
- DELETE = file removed from live tree; content survives **only** in git history.
- These are mutually exclusive. Option B was the **explicit, executed** choice.

### 1.4 Default reading

- Per raw#10 honest C3 + raw#15: BG should NOT auto-revert an explicit user choice without re-authorization.
- **Default**: assume DELETE was intentional. UPGRADE recipe below is **informational only**, not pre-approved.

---

## 2. Recovered content snapshot (from git history)

### 2.1 orpheus/.own — content at commit `6a1fc6c~1` (last live revision)

- length: 245 LoC
- frontmatter: `schema_version: project/own/v1`, `mk: 1`, `last_updated: 2026-05-04`
- structure:
  - `## roles` — dancinlife + claude opus/sonnet/haiku + orpheus role definition
  - `## baselines` — external-cli-only-access, found-key-encryption-at-write, hexa-only (raw 9), honest-disclosure (raw 10)
  - `## project_directives` — orpheus↔wraith duo, ghost standalone repo, puzzle target staleness, blk.4 retarget, blk.5 sweep tx broadcast prohibition
  - `## cross_link_to_specs` — cpre/contracts.ai.md (C1-C7), .roadmap.orpheus
  - `## cross_link_to_raws` — raw 9 (hexa-only), raw 10 (honest-disclosure), raw 20 (own-monotonic)
  - own rule body (`own N <status> "title"` blocks)
- recovery command: `git -C /Users/ghost/core/orpheus show 6a1fc6c~1:.own`

### 2.2 wraith-wallet/.own — content at commit `5f09433~1` (last live revision)

- length: 198 LoC
- frontmatter: `schema_version: project/own/v1`, `mk: 1`, `last_updated: 2026-05-04`
- structure:
  - `## roles` — dancinlife + AI agents + wraith-wallet role (custody/sign/route/off-ramp; orpheus settlement sibling)
  - `## baselines` — external-cli-only-access, backend-swap-uniformity, broadcast-policy-gate-default-dry-run, separation-of-knowledge, hexa-only (raw 9)
  - `## project_directives` — orpheus↔wraith duo, 2-stage swap, broadcast_relay sub-domain (MARA Slipstream), W4 default never_broadcast_dry_run
  - `## cross_link_to_specs` — cpre/contracts.ai.md (W1-W8), .roadmap.wraith-wallet (cond/blk + sub_domains[broadcast_relay])
  - `## cross_link_to_raws` — raw 9, raw 10, raw 20 (own-monotonic), raw 47 (cross-repo)
  - own rule body
- recovery command: `git -C /Users/ghost/core/wraith-wallet show 5f09433~1:.own`

### 2.3 What was lost (live-tree only — git history intact)

- daily-readable SSOT for project rules
- IDE/editor convenience (no need to `git show` to check rules)
- direct `cat .own` UX for sister repos / agents

What was **preserved**:
- full content in commit history (245 + 198 LoC, both repos)
- cross-link mirror in `cpre/contracts.ai.md` (per orpheus C1-C7, wraith W1-W8 references)
- `.roadmap.<repo>` tracker (own enforcement evidence)

---

## 3. UPGRADE recipe (informational — DO NOT execute without user ack)

If user reverses Option B and wants UPGRADE path, the recipe per repo is:

### 3.1 orpheus

```bash
cd /Users/ghost/core/orpheus

# Step 1: recover mk1 content
git show 6a1fc6c~1:.own > .own.mk1.tmp

# Step 2: rewrite frontmatter to mk2 schema
# Replace lines 1-5 of .own.mk1.tmp:
#   schema_version: project/own/v2
#   mk: 2
#   migrated_from: mk1
#   migration_date: 2026-05-04
#   reverses_commit: 6a1fc6c
#   last_updated: 2026-05-04
# Plus any mk2-required new fields (e.g., bg_provenance, dual_ssot_resolution).

# Step 3: place + commit
mv .own.mk1.tmp .own
git add .own
git commit -m "chore(.own): mk2 UPGRADE reverses Option B per user re-ack"
```

### 3.2 wraith-wallet

```bash
cd /Users/ghost/core/wraith-wallet
git show 5f09433~1:.own > .own.mk1.tmp
# (same mk2 frontmatter rewrite as orpheus)
mv .own.mk1.tmp .own
git add .own
git commit -m "chore(.own): mk2 UPGRADE reverses Option B per user re-ack"
```

### 3.3 mk2 frontmatter spec — TBD

This BG did not retrieve the mk2 frontmatter spec (out of scope). Before executing §3.1 / §3.2, user must point to the canonical mk2 spec doc (likely under `/Users/ghost/core/anima/docs/` per BG-ζ artifacts).

---

## 4. User decision tree

```
Q1: Is "commit history-only preservation" the intended end state for orpheus + wraith-wallet .own?
├── YES (default) → no further action; this BG concludes.
│                   → cross-link mirror in cpre/contracts.ai.md remains live SSOT.
│
└── NO → Q2: Reverse Option B and execute UPGRADE?
         ├── YES → user must:
         │       1. Confirm mk2 frontmatter spec path
         │       2. Authorize execution of §3.1 + §3.2
         │       3. Re-trigger this BG (or new BG) with explicit "execute UPGRADE" directive
         │
         └── NO  → custom path (e.g., recreate as mk1.5 hybrid) — requires new spec discussion
```

---

## 5. Honest C3

1. **Both .own files were recovered from git history; this BG did NOT cross-validate the recovered content against any other source** (no cpre/contracts mirror diff, no .roadmap tracker diff). Recovery is byte-faithful from `git show <commit>~1:.own`, not semantically validated.
2. **The "dual-SSOT EOL" rationale cited in Option B commit messages was not traced back to its original anima decision doc** in this BG. The conflict surfacing assumes both BG-ζ recommendation and Option B selection are documented elsewhere; this BG did not audit those docs.
3. **mk2 frontmatter spec was not retrieved**. UPGRADE recipe §3.1/§3.2 leaves placeholders for required mk2 fields. Cannot execute without that spec.
4. **No verification that cross-link mirror in cpre/contracts.ai.md is up-to-date** with the deleted .own content. If the user goes "history-only" path, they should confirm cpre mirror covers all rules from the deleted .own — otherwise rules are silently lost from live SSOT.
5. **Recipe is recreate-from-history; it does NOT preserve the inter-commit evolution** (own 1, own 2 양방향, own 6, own 7 production-first, own 8 self-폐기, own 10, own 11 INTERNAL-ONLY pivot). UPGRADE flattens to a single mk2 snapshot. If history-as-evidence matters, snapshot loses provenance richness.
