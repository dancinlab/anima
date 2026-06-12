# discoveries — per-domain continuous discovery log

> **Convention (since 2026-06-12):** discovery records live PER DOMAIN at
> `domains/<DOMAIN>/discoveries/<slug>.tape` — NOT in a flat root `.discoveries/`.
> The old flat `.discoveries/` folder was migrated into the domains and abolished
> (227 tapes via `git mv`, lossless; master index = `MAIN.tape` @L discovery_migration).

A discovery tape = a `/kick` · `/gap` finding, logged every batch (id · seed ·
verdict-tier-target), persisted next to the domain it belongs to.

## Where a new discovery goes

```
new /kick or /gap finding
        │
        ├─ identify the domain (MITOSIS-ENGINE · OMEGA · ENGINE+CLM+KOSMOS · CORPUS · ...)
        │
        └─▶ write domains/<DOMAIN>/discoveries/<slug>.tape
                 (genuinely cross-domain + no honest home → domains/_UNSORTED/discoveries/)
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
