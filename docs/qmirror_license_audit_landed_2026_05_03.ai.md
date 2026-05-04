# qmirror License Audit — Landed (2026-05-03)

**Status**: LANDED
**Cycle**: `qmirror_license_audit_2026_05_03`
**Marker**: `state/markers/qmirror_license_audit_landed.marker`
**Audit**: `state/qmirror_license_audit_2026_05_03/audit.json`
**Remediation**: `state/qmirror_license_audit_2026_05_03/remediation.json`

---

## TL;DR

Audit verified pyphi 4.0.b78d0e3 = **GPLv3**, confirmed it's already
**subprocess-isolated** in qmirror's `iit_mip_runner.py` (FSF MereAggregation
doctrine), and confirmed qmirror redistributes **zero** ANU bits. **qmirror
core stays Apache-2.0** (unchanged). Added `LICENSING.md` documenting the
sub-component license breakdown and patched README/hexa.toml/CHANGELOG to
point users at it. Pushed to GitHub canonical (`5a3c516`) and synced 4 files
to HF mirror.

- **Cost**: $0 (docs only; no compute, no API spend).
- **Raw#9 strict**: only `.md` / `.toml` / `LICENSE` text edits on Mac side; zero `.py` mutated.
- **No runtime changes**: closure 8/8 verdict carried forward unchanged.

---

## Step 1 — pyphi license verify

- Package: [`wmayner/pyphi`](https://github.com/wmayner/pyphi) at pin `4.0.b78d0e3`.
- LICENSE file fetched from <https://github.com/wmayner/pyphi/blob/master/LICENSE.md>.
- **Verdict: GPLv3** (GNU General Public License, Version 3, 29 June 2007).
- Implication if linked in-process: GPLv3 contagion of qmirror core.
- Implication if subprocess-isolated: aggregation, not combined work
  (FSF GPL FAQ MereAggregation entry).

**Existing qmirror architecture**: hexa-side `modules/iit_mip.hexa` does NOT
import pyphi. It spawns `modules/_python_bridge/iit_mip_runner.py` as a
subprocess via stdin/stdout JSON. pyphi only loads inside that subprocess's
Python interpreter. This is canonical aggregation; qmirror core is NOT a
GPLv3 derivative work.

## Step 2 — ANU redistribution check

- API docs at <https://qrng.anu.edu.au/contact/api-documentation/> — no
  license/redistribution terms published.
- FAQ at <https://qrng.anu.edu.au/contact/faq/> — no formal ToS;
  acknowledges open-source clients exist but distances ANU from third-party code.
- AWS Marketplace endpoint at <https://quantumnumbers.anu.edu.au/> — no
  visible terms in the surfaced page text.

**Verdict**: ANU publishes no formal license on the random bits themselves.
Pure facts (random outputs of a physical process) are generally not
copyrightable in most jurisdictions (Feist v. Rural doctrine).

**qmirror actual redistribution**: ZERO ANU bits in the repo. Only CODE that
calls the live API ships. NIST tier-1+ cond.4 evidence (7/7 PASS at α=0.01)
was generated from `hmac_drbg_legacy` (a deterministic CSPRNG, not ANU bits)
per `tests/test_nist.hexa` line 9. Therefore ANU is moot for this repo.

## Step 3 — Remediation options ranked (완성도 lens)

| Rank | Option | 완성도 | Note |
|------|--------|--------|------|
| 1 | **A** isolate pyphi to optional dep + LICENSING.md | 9/10 | docs wrapper around existing isolation; preserves Apache-2.0 |
| 2 | **D** subprocess-only (already implemented) | 8/10 | runtime mechanism; complementary to A |
| 3 | **C** drop pyphi, write Apache-2.0 IIT MIP from scratch | 5/10 | out-of-scope; Phase 4 work |
| 4 | **B** relicense full repo to GPLv3 | 4/10 | over-restrictive; loses commercial users |

**Chosen**: A + D combined (D was already implemented in 1.0.0; this cycle
adds A's documentation surface).

## Step 4 — Files changed

| File | Change | Note |
|------|--------|------|
| `LICENSE` | UNCHANGED | Apache-2.0 (correct for qmirror core) |
| `LICENSING.md` | NEW | full sub-component breakdown + 4 honest C3 caveats |
| `README.md` | PATCH | "License & attribution" expanded with sub-component table |
| `hexa.toml` | PATCH | `[dependencies.optional]` labels each dep with its own license |
| `CHANGELOG.md` | PATCH | 1.0.1 entry for license clarity audit |
| `modules/_python_bridge/*.py` | UNCHANGED | subprocess isolation already implemented |
| All `.hexa` modules | UNCHANGED | zero runtime change |

## Step 5 — Push status

### GitHub canonical

- Pre-cycle HEAD: `df89ff2`
- Post-cycle HEAD: **`5a3c516`** ← `docs(license): add LICENSING.md + clarify pyphi GPLv3 optional dep isolation`
- Push: `git push origin main` → `df89ff2..5a3c516  main -> main` ✓

### HF Hub mirror

Sequential `hf upload` commits (4 files):

| # | Commit | File | Rationale |
|---|--------|------|-----------|
| 1 | `4d86d328` | LICENSING.md | NEW — full sub-component breakdown |
| 2 | `834b5e00` | CHANGELOG.md | 1.0.1 entry |
| 3 | `82a09c5f` | hexa.toml | optional-dep license labels |
| 4 | `1835e6f4` | README_github.md | re-sync canonical README (License section expanded) |

HF top-level `README.md` (the HF card with YAML front-matter) was NOT
modified — its `license: apache-2.0` field is already correct (qmirror core
IS Apache-2.0; the optional pyphi GPLv3 dep is a sub-component, not the
package license).

---

## Honest C3 caveats (raw#10)

1. **Legal-advice disclaimer**: this audit is the maintainer's good-faith
   reading of FSF GPL FAQ MereAggregation and Apache Software Foundation
   guidance. It is not legal advice. For commercial integration where
   license interpretation is load-bearing, consult a licensed attorney in
   your jurisdiction.
2. **pyphi version pin volatility**: pin is `b78d0e3` (currently GPLv3).
   If wmayner/pyphi changes license at a future commit, the §3 analysis
   in `LICENSING.md` must be re-verified at the new pin.
3. **ANU ToS evolution risk**: as of 2026-05-03 ANU publishes no formal
   license. If they add future ToS that constrain caching/redistribution,
   the qrng.hexa fetch path should be reviewed. (Current redistribution
   exposure is zero because qmirror caches no ANU bits.)
4. **Dual-mirror sync delay**: GitHub canonical and HF mirror update
   independently. After this cycle GitHub got the LICENSING.md / README /
   hexa.toml / CHANGELOG updates first; HF mirror sync followed in 4
   `hf upload` commits. During the brief push window (a few minutes) the
   mirrors may have shown stale license docs. They are now in sync.

---

## Sister cycles (independent; not blocked by this audit)

- `a03d549d` — `hx install qmirror` package integration (BG, in flight)
- `a70e17dd` — nexus CLI integration kept upstream (BG, in flight)
- Future Phase 4 — pyphi dep retirement (port slogdet/EMD/MIP to native
  Apache-2.0); fully eliminates GPLv3 exposure even from optional path.

---

## Verification (post-push)

```bash
# GitHub canonical
gh api repos/need-singularity/qmirror/contents/LICENSING.md --jq '.size'
# → ~8900 (LICENSING.md exists)

# HF mirror
curl -s https://huggingface.co/need-singularity/qmirror/raw/main/LICENSING.md | head -5
# → "# LICENSING — sub-component breakdown" + Apache-2.0 line

# Apache-2.0 still declared on both
grep -i "license" /Users/ghost/core/qmirror/hexa.toml
# → license = "Apache-2.0"
```

---

## Status

- **v1.0.1** (2026-05-03) — license clarity audit landed; Apache-2.0
  preserved; pyphi GPLv3 documented as optional+isolated; ANU verified as
  no-redistribution.
