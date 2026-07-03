#!/usr/bin/env bash
# ci_pick_runner.sh — fallback-dispatch runner picker (self-hosted-if-online,
# else GitHub-hosted). Canonical GitHub Actions reliability pattern: a cheap
# always-available probe job (ubuntu-latest) decides the heavy job's `runs-on`
# at runtime, so the pool being OFFLINE never deadlocks a (potentially required)
# gate — it just falls back to the free GitHub-hosted runner.
#
# WHY: anima's real gate (engine compile + governance enforce + smoke) runs on a
# github-hosted darwin-arm64 mac (macos-14) — a scarce, occasionally-backlogged
# pool. A self-hosted darwin mac (ghost — always-warm ~/.hexa-cache) runs that
# compile far faster, but ghost can be offline. Static `runs-on:[self-hosted,…]`
# would leave the gate pending forever when ghost is down. This picker keeps the
# job deadlock-proof: ghost when online, else the free github-hosted fallback.
# (Ported 1:1 from dancinlab/hexa-lang tool/ci_pick_runner.sh — see PR #4417 /
# #4023. anima currently wires only the `darwin` kind; the `linux` kind is kept
# verbatim so a future self-hosted linux runner needs no re-port.)
#
# USAGE (inside a ubuntu-latest dispatch job, GH_TOKEN exported):
#   bash tool/ci_pick_runner.sh <kind>
#     kind = linux  → emits linux_label  (self-hosted hexa-build, else fallback)
#            darwin → emits darwin_label (ghost selfhost-gen2fix → mini insurance
#                                         → macos-14 github-hosted fallback)
#
# Writes a single `<kind>_label=<json>` line to $GITHUB_OUTPUT. The value is a
# JSON STRING consumed downstream via `runs-on: ${{ fromJSON(needs.dispatch.outputs.<kind>_label) }}`:
#   - self-hosted → a JSON ARRAY of labels  e.g.  ["self-hosted","macOS","ARM64","selfhost-gen2fix"]
#   - fallback    → a JSON STRING            e.g.  "ubuntu-latest" / "macos-14"
# fromJSON parses both an array and a bare string, and `runs-on` accepts either.
#
# SAFETY / FORK-PR (RCE): self-hosted is only ever a CANDIDATE when the env var
# SELF_HOSTED_ELIGIBLE=1 (the caller sets this to the result of the
# same-repo guard `github.event.pull_request.head.repo.full_name == github.repository`,
# OR a push/dispatch event). For fork PRs the caller passes 0 → we force the
# GitHub-hosted fallback regardless of pool state (no untrusted code on the pool).
#
# FAIL-SAFE: any probe error (missing token, gh/api failure, jq absent) falls
# back to the GitHub-hosted runner — the dispatch job itself runs on
# ubuntu-latest (always available), and we never let a probe hiccup wedge CI.
set -uo pipefail

kind="${1:-}"
case "$kind" in
  linux)
    fallback='"ubuntu-latest"'
    want_labels='self-hosted Linux X64 hexa-build'
    sh_label='["self-hosted","Linux","X64","hexa-build"]'
    ;;
  darwin)
    fallback='"macos-14"'
    want_labels='self-hosted macOS ARM64 selfhost-gen2fix'
    sh_label='["self-hosted","macOS","ARM64","selfhost-gen2fix"]'
    # ordered insurance chain: ghost (primary) → mini (fallback-only, distinct
    # label so it never load-balances with ghost in normal operation) → macos-14.
    # mini is a daily-driver Mac: it must receive jobs ONLY when ghost is offline.
    alt_want_labels='self-hosted macOS ARM64 hexa-darwin-mini'
    alt_sh_label='["self-hosted","macOS","ARM64","hexa-darwin-mini"]'
    ;;
  *)
    echo "::error::ci_pick_runner: unknown kind '$kind' (want linux|darwin)" >&2
    exit 2
    ;;
esac

emit() {  # emit <json-label> ; also echoes a human notice
  local val="$1"
  if [ -n "${GITHUB_OUTPUT:-}" ]; then
    printf '%s_label=%s\n' "$kind" "$val" >> "$GITHUB_OUTPUT"
  fi
  echo "ci_pick_runner: kind=$kind → runs-on=$val"
}

# ── fork-PR / eligibility guard ─────────────────────────────────────────────
# Caller sets SELF_HOSTED_ELIGIBLE=1 only for same-repo events. Anything else
# (fork PR, or unset) forces the GitHub-hosted fallback — no self-hosted RCE.
if [ "${SELF_HOSTED_ELIGIBLE:-0}" != "1" ]; then
  echo "::notice::self-hosted not eligible (fork-PR or guarded) → GitHub-hosted fallback"
  emit "$fallback"
  exit 0
fi

# ── probe: is a matching self-hosted runner ONLINE and (optionally) idle? ────
# We require status=online. We do NOT require !busy: a queued job will wait for
# the single ghost runner, which is acceptable (best-effort-strong), and the
# 1-SSH pool serializes by design. If you prefer to skip-when-busy, gate on
# `.busy==false` too — left online-only so transient busy doesn't bounce to cloud.
api_json=""
if [ -n "${GH_TOKEN:-}" ] || [ -n "${GITHUB_TOKEN:-}" ]; then
  api_json="$(gh api repos/"${GITHUB_REPOSITORY:-dancinlab/anima}"/actions/runners --paginate 2>/dev/null || true)"
fi

if [ -z "$api_json" ]; then
  echo "::notice::runner probe unavailable (no token / api error) → GitHub-hosted fallback"
  emit "$fallback"
  exit 0
fi

# ── BLINDNESS CANARY (LOUD) ─────────────────────────────────────────────────
# We are past the eligibility guard (eligible=1) AND the API returned a body.
# If it reports ZERO runners, the overwhelmingly likely cause is a token that
# lacks `administration:read`: the default GITHUB_TOKEN can NEVER carry that
# scope (it is not even a grantable `permissions:` key), so the runners endpoint
# returns `{"total_count":0,"runners":[]}` and this picker would silently fall
# back FOREVER — indistinguishable from "pool offline". Emit a ::warning so a
# misconfigured RUNNER_PROBE_TOKEN is diagnosable in the dispatch log instead of
# masquerading as a dead pool. (Does not change control flow — still falls back.)
total_count="$(printf '%s' "$api_json" | jq -r '.total_count // (.runners | length) // 0' 2>/dev/null || echo 0)"
if [ "${total_count:-0}" = "0" ]; then
  echo "::warning::runner probe returned 0 runners on an authenticated API call — the probe token almost certainly lacks administration:read (the default github.token can NEVER carry it). Set the RUNNER_PROBE_TOKEN secret (fine-grained PAT · this repo · Administration: read-only) to enable self-hosted routing. Falling back to GitHub-hosted for now."
fi

# jq filter: a runner is a match if status==online AND it carries EVERY wanted
# label. Labels are passed via `jq --args …` (positional $ARGS.positional) so no
# string-splitting/quoting fragility. `wanted - present == []` ⇔ present ⊇ wanted.
# shellcheck disable=SC2016  # jq program — must NOT be shell-expanded
jq_filter='[ .runners[]
  | select(.status=="online")
  | select( ($ARGS.positional - [ .labels[].name ]) == [] )
] | length'

# shellcheck disable=SC2086  # intentional word-split of the wanted-label list
online_matches="$(printf '%s' "$api_json" | jq "$jq_filter" --args $want_labels 2>/dev/null || echo 0)"

if [ "${online_matches:-0}" -ge 1 ] 2>/dev/null; then
  echo "::notice::$online_matches online self-hosted runner(s) match [$want_labels] → self-hosted"
  emit "$sh_label"
  exit 0
fi

# ── ordered fallback probe (darwin only): mini insurance runner ──────────────
if [ -n "${alt_want_labels:-}" ]; then
  # shellcheck disable=SC2086  # intentional word-split of the wanted-label list
  alt_matches="$(printf '%s' "$api_json" | jq "$jq_filter" --args $alt_want_labels 2>/dev/null || echo 0)"
  if [ "${alt_matches:-0}" -ge 1 ] 2>/dev/null; then
    echo "::notice::primary self-hosted offline; $alt_matches insurance runner(s) match [$alt_want_labels] → self-hosted (mini)"
    emit "$alt_sh_label"
    exit 0
  fi
fi

echo "::notice::no online self-hosted runner matches [$want_labels] → GitHub-hosted fallback"
emit "$fallback"
exit 0
