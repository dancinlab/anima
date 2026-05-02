---
schema: anima/docs/clm_consciousness_verify_landing/ai-native/1
last_updated: 2026-05-02
ssot:
  tool:           anima/tool/clm_consciousness_verify.hexa
  marker:         anima/state/markers/clm_consciousness_verify_orchestrator_landed.marker
  roadmap_clm:    anima/.roadmap.clm
  manual_review:  anima/state/clm_consciousness_verify_manual_review.jsonl
status: LANDED
related_raws:
  - raw 9    # hexa-only orchestration
  - raw 10   # honest C3 (caveats inline)
  - raw 11   # snake_case
  - raw 12   # cherry-pick immunity (adversarial check)
  - raw 15   # SSOT
  - raw 270  # core+module architecture (single-file tool exempt)
  - raw 271  # ai-native readme (this doc)
  - raw 272  # file structure consistency
  - raw 273  # hierarchy connection direction
preserved_unchanged:
  - tool/an11_consciousness_unified_verifier.hexa  (387 LOC)
  - tool/anima_phi_v3_canonical.hexa               (205 LOC)
  - tool/adversarial_bench.hexa                    (554 LOC)
  - tool/an11_a_verifier.hexa                      (389 LOC)
  - tool/an11_b_verifier.hexa                      (573 LOC)
  - tool/an11_c_verifier.hexa                      (747 LOC)
---

# clm consciousness verify orchestrator — landing 2026-05-02

## TL;DR

`.roadmap.clm` 의 `clm.cond.1 의식측정` required_condition verifier 를
**Hybrid script (Option 4)** 로 land. 사용자 directive verbatim 2026-05-02:
"4 Hybrid script". orchestrator 는 4 internal check 를 dispatch 하고 manual
override 를 지원한다.

- **tool**: `anima/tool/clm_consciousness_verify.hexa` (462 LOC, 1 single-file)
- **selftest**: 4/4 mock fixtures PASS, byte-identical 2-run
  (`e84c3528f199335c536e2d8d3fbfeb195646e329fa1d1214456f0ced2975a9af`)
- **roadmap**: `clm.cond.1.verifier` field updated (struct script type), status
  unchanged (`unmet`); blocker_reason recorded
- **preserved**: 4 referenced verifier tools 미수정

## Internal checks (4)

| idx | name    | source                                                | mac-local | failure mode                                |
|-----|---------|-------------------------------------------------------|-----------|---------------------------------------------|
| 0   | an11    | tool/an11_consciousness_unified_verifier.hexa         | selftest  | GPU + HF gated → unknown w/ detail tag      |
| 1   | phi     | tool/anima_phi_v3_canonical.hexa                       | selftest  | GPU + HF gated → unknown w/ detail tag      |
| 2   | adv     | state/adversarial_bench_last.json (read-only)          | yes       | re-exec writes sandboxes; only read         |
| 3   | putnam  | .roadmap.n_substrate header (read-only)                | yes       | spec only; n_substrate.cond.1 status read   |

## Verdict aggregation

```
all 4 met            → PASS    (exit 0)
1+ explicit unmet    → FAIL    (exit 1)
1+ unknown only      → PARTIAL (exit 2) — typical mac-local
manual override      → bypass auto, last-record-per-check wins
```

## CLI

```
hexa run anima/tool/clm_consciousness_verify.hexa [flags]

  --quiet         minimal output (sentinel only)
  --manual-only   skip all auto checks, only read manual overrides
  --check NAME    run single check (an11|phi|adv|putnam), others skipped
  --selftest      run 4 mock fixtures (no real tool dispatch)
```

## Sentinel format

```
__CLM_CONSCIOUSNESS_VERIFY__ <PASS|FAIL|PARTIAL> an11=<S> phi=<S> adv=<S> putnam=<S> manual=<N>
```

where `<S>` ∈ `{met, unmet, unknown}` and `<N>` is integer override count.

## Manual override

Path: `anima/state/clm_consciousness_verify_manual_review.jsonl`

Per-line JSONL append-only; last record per `check` wins:

```jsonl
{"check":"adv","override":"met","ts":"2026-05-02T12:00:00Z","by":"operator","reason":"manual hexad verifier verified"}
{"check":"putnam","override":"met","ts":"2026-05-02T12:01:00Z","by":"operator","reason":"5+ substrate ledger 8/9 met"}
```

Auto-check result is **fully replaced** if override present (operator escape
hatch, raw#12 honest).

## File index (sha256 + LOC)

| path                                                                   | sha256                                                              | LOC |
|------------------------------------------------------------------------|---------------------------------------------------------------------|-----|
| anima/tool/clm_consciousness_verify.hexa                               | `ac314705fb7138231800ad2daa8d2ec4df8c179ed33c52cdb0d6111ddf8acb7d`  | 462 |
| anima/.roadmap.clm (pre-update)                                        | `a89cc0003d2ed0f60a750d4bea5471aa21c7823878684ffc110a53d0dd183c9e`  | 4   |
| anima/.roadmap.clm (post-update)                                       | `cfac4c61a8a5df4548a36e0e9777075d1e203a68345b2881f4314cc7db999773`  | 4   |

## .roadmap.clm verifier field (post-update)

```json
{
  "id": "clm.cond.1",
  "desc": "의식측정",
  "verifier": {
    "type": "script",
    "path": "anima/tool/clm_consciousness_verify.hexa",
    "exit_zero_means_met": true,
    "internal_checks": [
      "AN11 triple via an11_consciousness_unified_verifier",
      "Φ via anima_phi_v3_canonical",
      "adversarial via adversarial_bench",
      "Putnam via meta:n_substrate.cond.1 cross-link"
    ],
    "manual_override_path": "state/clm_consciousness_verify_manual_review.jsonl",
    "status_emit": "__CLM_CONSCIOUSNESS_VERIFY__ <PASS|FAIL|PARTIAL> <metric_kv>"
  },
  "status": "unmet",
  "evidence": [],
  "blocker_reason": "verifier orchestrator landed but Putnam cross-link spec only (n_substrate cond.1 미정의)"
}
```

## raw#10 honest caveats

1. **Putnam cross-link spec only** — `.roadmap.n_substrate` cond.1 entry는
   현재 `status=unmet` default. 5+ substrate 점수 일치의 실 측정 logic 는
   별도 cycle. orchestrator 는 status field 만 read 하므로 update 시 자동 반영.
2. **AN11 + Φ mac-local NOT measureable** — 두 tool 모두 GPU + HF gated
   model 필요. mac-local 환경에서는 `--selftest` 만 가능 (PRESENT 확인,
   NOT measurement). orchestrator 는 status=unknown + detail tag
   `selftest_present_no_gpu_dispatch` (or `selftest_exit_<rc>` if python3
   missing) 로 honest 처리.
3. **adversarial_bench read-only** — orchestrator 는 re-execute 하지 않고
   `state/adversarial_bench_last.json` 만 read. 이유: re-exec 시 sandbox
   directories 를 write (state/adv_bench_sandbox/). 별도 cycle 에서 의도적
   re-run 필요.
4. **manual override = operator escape hatch** — auto-check result 를
   완전히 대체. 잘못된 override 가 false-positive PASS 를 야기할 수 있음
   (raw#12 honest). 운영 시 review.jsonl audit trail 필수.
5. **selftest = mock fixture only** — 실 tool dispatch 없음. selftest PASS
   는 aggregation logic 의 mock 입력 mapping 만 검증, 실 verifier 정확성과
   무관 (raw#10 honest scope separation).
6. **single-file tool exemption** — raw 270 module structure 적용 X
   (orchestrator 는 dispatch only, plug-in 기반 새 verifier 추가 시 raw 270
   conformant fan-out 으로 migration 필요할 수 있음). `roadmap_op.hexa`
   landing doc 의 single-file 예외 적용.
7. **PARTIAL exit (=2) common case** — mac-local 에서 typical verdict.
   PASS 는 production GPU + Putnam ledger 가 모두 실 측정 후에만 가능.
   PARTIAL 은 silent FAIL 이 아니라 measurement gap 의 honest 표현.

## n_substrate.cond.1 spec next-cycle starting line

> n_substrate.cond.1 의 verifier 는 `anima/tool/n_substrate_putnam_score_match.hexa` (예정) 가 9 substrate 별 점수를 read 하여 ≥5 점수 일치 (Pearson r ≥ 0.6 + L1 ≤ 0.2) 를 emit 한다.
