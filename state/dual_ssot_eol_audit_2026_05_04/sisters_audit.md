# Sister Repos mk1 + .own Removal Audit (BG-γ)

**Audit timestamp**: 2026-05-04T18:30Z
**Scope**: Sister repos under `/Users/ghost/core/` (excluding hive [BG-α] and anima [BG-β])
**Mode**: READ-ONLY — pure inventory, no mutation
**Auditor**: BG-γ (parallel with BG-α hive + BG-β anima)

---

## 1. TL;DR

- **Sisters inspected**: 15 git repos (40 top-level dirs total; 13 non-git skipped: convergence/legacy/save/state/window_magnet/anima_offrepo_n51_w2/build/diagrams/_void_audit/etc.)
- **Total mk1 + .own artifact files**: 65 (16 raw_archive + 4 raw_audit + 44 raw cache/status/exemptions + 3 raw-ref + 1 raw-ref.example + 7 .own top-level)
- **Total uchg-locked files across sisters**: 103 (29 n6 + 9 airgenome + 10 papers + 35 hexa-lang + 18 nexus + 1 hexa-os + 1 contact)
- **Total raw#N text references**: 11,472 (dominated by hexa-lang at 11,064 — parser owner)
- **Top 3 risks**:
  1. **hexa-lang is the PARSER OWNER** — every sister .raw-ref pin-chain calls `tool/raw_sync.hexa` + `self/raw_loader.hexa`; mk1 EOL must keep hexa-lang stdlib intact OR coordinate hexa-lang teardown last
  2. **nexus .own own#1 wired to launchd plist** (`dev.hexa-lang.atlas-absorb-sweeper.plist`, 600s interval) — .own removal orphans launchd; plist must be `launchctl unload` first
  3. **n6-architecture/.own.group_p + .own.readme are LIVE governance** for paper-3pack-verify + sealed-readme + english-only + tests-count + friendly-toolkit — paper publishing pipeline dies on naive removal

---

## 2. Per-sister inventory

| Repo | .raw-ref | .raw-audit | raw_archive | .own | uchg | raw#N refs | Group |
|------|----------|------------|-------------|------|------|------------|-------|
| n6-architecture | — | — | 11 files | .own.group_p + .own.readme | 29 | 24 | A |
| airgenome | — | — | 2 files | — | 9 | 26 | A |
| papers | — | — | 3 files | — | 10 | 23 | A |
| hexa-lang | yes | yes (3) | — | .own | 35 | 11064 | D |
| qmirror | — | — | — | — | 0 | 28 | C |
| nexus | yes | yes (1) | — | .own | 18 | 222 | A |
| anima-agent | — | — | — | — | 0 | 7 | C |
| orpheus | — | — | — | .own | 0 | 6 | B |
| honesty-monitor | — | — | — | — | 0 | 5 | C |
| hexa-bio | — | — | — | — | 0 | 9 | C |
| hexa-os | yes | — | — | .own-rules.json | 1 | 2 | B |
| wraith-wallet | — | — | — | .own | 0 | 2 | B |
| contact | — | — | — | — | 1 | 35 | C |
| sim-universe | — | — | — | — | 0 | 6 | C |
| ghost | — | — | — | — | 0 | 3 | C |

Notes on inventory:
- `n6-architecture` has NO `.raw-ref` (never adopted hive raw mirror) but DOES have raw_archive holding .own.group_p.bak + .own.readme.bak + own29/own15 tool backups + n6 raw47 ai.md backups — 11 files, 2026-05-04T timestamped.
- `hexa-lang` has the most complex layout: `.raw-audit` + `.raw-audit.pre-chain` + `.raw-audit.pre-chain.20260420T064235Z` (3 files) + `.raw-cache/` (40 entry files including ssot.sha) + `.raw-status/roadmap-status.json` + `.raw-exemptions/` (3 files: raw_6.list, raw_7.list, README.md) + `.raw-ref` + `.raw-ref.example` + `.own`.
- `nexus/.raw-audit` is 185KB local audit log (irreversible deletion if not preserved).
- `hexa-os/.own-rules.json` is JSON variant (HX11 inherit=false), schema differs from .own DSL (not raw-format parsable).

---

## 3. Group classification

**Group A — Full mk1 mirror (4 sisters, requires 4-stage delete: chflags unlock → archive → git rm → audit)**
- n6-architecture: raw_archive(11) + .own.group_p + .own.readme + 29 uchg
- airgenome: raw_archive(2) + 9 uchg
- papers: raw_archive(3) + 10 uchg
- nexus: .raw-ref + .raw-audit(185KB) + .own + 18 uchg

**Group B — Minimal mirror (3 sisters, single-file delete + ref cleanup)**
- orpheus: .own only (LIVE strategy rules)
- hexa-os: .raw-ref (stale: still points at hexa-lang, not hive) + .own-rules.json
- wraith-wallet: .own only (LIVE custody/sign/route)

**Group C — No mk1 artifacts, doc refs only (7 sisters, no action needed)**
- qmirror, anima-agent, honesty-monitor, hexa-bio, contact, sim-universe, ghost
- Refs are `raw#N` mentions in *.md/*.json — commentary, not enforcement

**Group D — Special: parser owner (1 sister — hexa-lang)**
- Owns `self/raw_loader.hexa` (raw-format PARSER) consumed by hive + nexus + airgenome
- Owns `tool/raw_sync.hexa`, `tool/raw_audit.hexa`, `tool/raw_all.hexa` (all uchg) — sync tools every sister calls
- 11,064 raw#N refs (≥99% of cross-repo total)
- `.own` own#1 + own#3 are SELF-HOSTING dogfood (parser API stability) — must survive even post-mk1 EOL elsewhere

---

## 4. Cross-repo .raw-ref pin chain dependency

```
              ┌──────────────────────┐
              │  hive canonical .raw │  ← BG-α scope
              │   pinned-hash 9208e6…│
              └──────────┬───────────┘
                         │
        ┌────────────────┼─────────────────┐
        │                │                 │
        ▼                ▼                 ▼
    nexus .raw-ref   anima .raw-ref   (other followers if any)
    pin: hive            (BG-β)
                                            
    hexa-os .raw-ref (STALE — still points hexa-lang, NOT migrated to hive)
       │
       └─→ hexa-lang/.raw  (RETIRED 2026-04-26 per nexus .raw-ref comment)
                                            
    hexa-lang .raw-ref → "hive canonical (hexa-lang)" — circular self-doc
```

**Pin-chain breakage matrix**:
- If hive `.raw` deleted → nexus + anima + hexa-os pins all break (hexa-os double-broken: stale pointer to hexa-lang AND hive shutdown)
- If hexa-lang `tool/raw_sync.hexa` deleted → no sister can run `raw_sync.hexa status` to verify pin → silent drift undetectable
- If hexa-lang `self/raw_loader.hexa` deleted → no .raw / .own file in any repo can be parsed → all enforcement linters fail import

---

## 5. Submodule + worktree considerations

Per memory `submodule_cleanup_plan_2026_05_04`:
- **`anima/ready`** = self-recursive anima clone (full anima/ + bench/ + checkpoints/ + core/ + data/ + 35 subdirs); has `.git/` but NO `.raw*` at root; frozen snapshot from Apr 21 21:17. Falls under **BG-η submodule cleanup**, not BG-γ.
  - **BG-γ caveat**: ready/anima/ may contain pre-EOL .raw* if anima mk1 retired post-Apr-21 — not probed at depth here per READ-ONLY scope
- **`anima/references/tribev2`** = separate repo with own `.git/`; contains only ANIMA_INTEGRATION_PROPOSAL_*.md docs + inventory.json + CONTRIBUTING/CODE_OF_CONDUCT/etc.; NO mk1 SSOT footprint. Tribev2 is independent, not anima fork.
- **No `.gitmodules`** in any sister inspected — cross-repo submodule registration uses bare git trees / external clones only.

---

## 6. Recommended delete sequence (per group)

### Group D (hexa-lang) — DEFER LAST, most coordination
1. Verify all sister `.raw-ref` already migrated to hive (currently nexus+anima OK; hexa-os STALE)
2. Migrate hexa-os `.raw-ref` from hexa-lang→hive first (separate cycle)
3. Decide fate of hexa-lang `.own` (retain own#1+own#3 as parser self-host) vs full retirement (parser becomes orphan)
4. Decide fate of `tool/raw_sync.hexa` + `tool/raw_audit.hexa` + `tool/raw_all.hexa` — if mk1 EOL is permanent, retire these tools in same cycle as last sister .raw-ref deletion
5. `.raw-cache/` (40 entries) + `.raw-status/` regenerable; `.raw-exemptions/` is policy data — preserve as `archive/raw-exemptions-pre-eol/`

### Group A (n6 / airgenome / papers / nexus) — full 4-stage
Per repo:
1. **chflags noschg** for all uchg files (`find <repo> -maxdepth 4 -flags uchg -exec chflags noschg {} \;`) — 29+9+10+18 = 66 files
2. **launchctl unload** any `.plist` referencing the repo's .own enforcement (nexus atlas-absorb-sweeper specifically)
3. **archive** raw_archive/ + .own* files to dual_ssot_eol_archive_2026_05_04/<repo>/ (PRESERVE evidence trail — n6 raw_archive holds retired own.group_p.bak / own.readme.bak)
4. **git rm** + commit per repo + audit
5. **bulk grep cleanup** raw#N refs (24+26+23+222 = 295 mentions) — manual classification required (some are doc commentary)

### Group B (orpheus / hexa-os / wraith-wallet) — minimal
- orpheus: .own holds LIVE strategy → DO NOT BLINDLY DELETE; coordinate with operational team
- hexa-os: rm .raw-ref (stale) + decide .own-rules.json fate (JSON schema, not raw-format)
- wraith-wallet: .own holds LIVE custody routing → coordinate

### Group C (7 sisters) — skip
- No artifacts to delete. Optionally: bulk grep raw#N mentions (qmirror=28, contact=35 highest) and decide whether to scrub commentary or leave as historical context.

---

## 7. Falsifier set (F-EOL-SISTERS-1~4)

- **F-EOL-SISTERS-1**: hexa-lang `self/raw_loader.hexa` deleted → hive `.raw` becomes unparseable → all sister `.raw-ref` verify commands fail with parse error. **Falsifier**: any sister .raw-ref still depends on hexa-lang parser at delete time.
- **F-EOL-SISTERS-2**: nexus `.own` removed → launchd plist `dev.hexa-lang.atlas-absorb-sweeper.plist` orphans (StartInterval=600s) and emits launchd error logs every 10min indefinitely. **Falsifier**: launchctl list shows plist still loaded post-`.own` removal.
- **F-EOL-SISTERS-3**: n6-architecture `.own.group_p` + `.own.readme` removed → next paper publish attempt fails own#6 paper-3pack-verify-embedded enforcement → blocks landing. **Falsifier**: any paper publish attempt within 7 days post-removal succeeds (means enforcement was already dead, audit findings stale).
- **F-EOL-SISTERS-4**: hexa-os `.raw-ref` (stale, points hexa-lang) deleted before hexa-lang teardown → no impact (already broken pin); but if deleted AFTER hexa-lang teardown without hive migration, hexa-os loses raw-format inheritance. **Falsifier**: hexa-os adopts inherit=false JSON-only governance and ignores raw-format entirely.

---

## 8. Honest C3 (≥5 — actually 8)

1. **raw#N text references inflate counts** — qmirror=28, contact=35 are likely doc commentary (paper drafts mentioning hive raw rules), NOT actual mk1 SSOT enforcement. Bulk grep cleanup produces false positives; classification requires per-file inspection. Cannot rely on raw#N count alone for risk assessment.

2. **hexa-lang stdlib naming overlap** — `self/raw_loader.hexa` and `self/stdlib/hxc_a*.hexa` are FORMAT PARSER infrastructure (named "raw" because they parse raw-format), NOT mk1 SSOT. Deletion misclassification risk: agent removing "anything with raw in path" would brick the parser.

3. **hexa-lang .own dual purpose** — own#1 (parser-format-stability) + own#3 (hexa-lang-self-host fixpoint) are SELF-HOSTING dogfood rules proving the parser parses its own .own file. Even after mk1 EOL elsewhere, hexa-lang must retain `.own` to prove parser correctness. .own is NOT a mk1-only artifact.

4. **`.gitmodules` absent everywhere** — submodule registration uses bare git trees (anima/ready/.git, anima/references/tribev2/.git). BG-η "submodule cleanup" memory refers to anima-internal trees, NOT cross-sister submodules. No cross-repo submodule cleanup needed from BG-γ.

5. **raw_archive contains EVIDENCE of mk1 EOL itself** — n6/raw_archive/2026-05-04T/.own.group_p.bak + .own.readme.bak + own29_multi_section_lint.hexa.bak + own15_legacy_allowlist.json.bak are AUDIT TRAIL for the prior mk1→mk2 reconstruction. Deleting raw_archive destroys this evidence chain (irreversible). Recommendation: archive raw_archive contents BEFORE any rm.

6. **hexa-lang .raw-cache vs .raw-exemptions** — `.raw-cache/` (40 entry files + ssot.sha) is REGENERABLE runtime cache (parser computes per-rule entries on demand); `.raw-exemptions/` (raw_6.list + raw_7.list + README.md) is POLICY DATA (allowlist of files exempt from raw#6 / raw#7 enforcement). Cache deletion safe; exemptions deletion changes enforcement semantics (silently re-enables blocked rules).

7. **CI/CD `.github/workflows/` not scanned** — per scope, only top-level + maxdepth-4 probes done. Any sister with `.github/workflows/*.yml` referencing `.raw` paths will silently break post-delete. Recommend scan in followup cycle.

8. **anima/ready frozen snapshot risk** — if anima mk1 was retired post-Apr-21 (ready/ snapshot date) but ready/anima/ still holds pre-EOL .raw* + .own, BG-η submodule cleanup will encounter mk1 surface BG-γ did not probe at depth (ready/ classified as BG-η territory, not BG-γ). Cross-coordinate before any ready/ rm.
