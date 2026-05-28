# M5 walltime — running pod registry

## Live pod

- pod-id: `cpnocpur5jjf5e`
- provider: runpod
- type: H100 80GB HBM3 SECURE
- image: `runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04`
- disk: 60 GB
- owner-tag: `m5-walltime`
- ssh host: `103.207.149.56:13798` (per `hexa cloud resolve cpnocpur5jjf5e`)
- rented at: `2026-05-29 ~00:09 KST` (~15:09 UTC)
- billing rate: ~$3.29/hr
- ssh status as of `~15:22 UTC`: ssh transport refused (probe loop active, 20s cadence)

## Budget

- HARD cap: $2 (~35 min wall)
- spend so far if torn down at 30 min wall: ~$1.65
- abort time: 35 min from rent (~15:44 UTC)

## Re-check command

```
hexa cloud list --provider runpod
hexa cloud resolve cpnocpur5jjf5e --provider runpod
hexa cloud down cpnocpur5jjf5e --provider runpod   # teardown
```
