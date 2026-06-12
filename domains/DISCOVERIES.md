# discoveries — per-domain continuous discovery log

> **Convention (since 2026-06-13):** discovery records are appended into the
> per-domain log `domains/<DOMAIN>.log.md` (the `.md` = curated doc, `.log.md` =
> raw append-only log — discoveries are log entries). The old `discoveries/`
> subfolders were merged into each domain's `.log.md` and removed, lossless
> (master index = `MAIN.tape` @L discovery_migration).

A discovery tape = a `/kick` · `/gap` finding, logged every batch (id · seed ·
verdict-tier-target), persisted next to the domain it belongs to.

## Where a new discovery goes

```
new /kick or /gap finding
        │
        ├─ identify the domain (MITOSIS-ENGINE · OMEGA · ENGINE+CLM+KOSMOS · CORPUS · ...)
        │
        └─▶ append the record into domains/<DOMAIN>.log.md
                 (genuinely cross-domain + no honest home → the closest domain's
                  .log.md + a cross-ref note)
```

## Flow (unchanged)

discovery → `CLAIMS.tape` claim → `hexa verify` → `.verdicts/<slug>/<id>.txt` →
`paper_on_discovery` (free-slug paper). Discoveries run alongside verify, not
batched to the cycle tail. Every discovery is recorded — no discard, no paraphrase
(a_discovery_log · a_discovery · a_paper_on_discovery).

## Domain buckets

`MITOSIS-ENGINE · OMEGA · ENGINE+CLM+KOSMOS · CLM-KOSMOS · CORPUS · KOSMOS-MAP ·
CHAT · PERSONA · SNS · VISION · SAVANT · AXIS · C-PORT` (+ `_UNSORTED` for the
honestly-homeless). Per-domain counts: see `MAIN.tape` master index.
