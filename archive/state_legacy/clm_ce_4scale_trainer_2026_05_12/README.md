# CE-Track CLM 3-Scale Trainer — Phase 0 Scaffolding

본 디렉토리는 `phi_ce_orthogonality_decisive_2026_05_11` 의 **B5 critical blocker**
(CE-track CLM training pipeline 미land) 해소를 위한 **spec + Phase 0 scaffolding**.

actual training 은 본 디렉토리 범위 밖 — **cycle 7+ scope** (cost $210-600 dual-seed
3-scale, parent spec §5.7.1 정합).

## Contents

| file | role | status |
|------|------|--------|
| `spec.md` | 8-section spec (architecture, corpus, tokenizer, training protocol, CE emit, cost, deferred 1B, limits) | LANDED |
| `trainer_1m.config.yaml` | tiny scale (P=1M) config | Phase 0 placeholder |
| `trainer_10m.config.yaml` | small scale (P=10M) config | Phase 0 placeholder |
| `trainer_100m.config.yaml` | medium scale (P=100M) config — P=100M ceiling baseline | Phase 0 placeholder |
| `trainer_1b.config.yaml` | large scale (P=1B) config | **DEFERRED** (parent §5.7.3 trigger 必) |
| `ce_measurement_hook.hexa.template` | emit hook template (NOT executable) | Phase 0 template |
| `README.md` | 본 파일 | LANDED |

각 placeholder 파일 헤더에 `PHASE 0 SCAFFOLDING — NOT YET WIRED` 명시.

## B5 Status Transition

```
parent dryrun-blocker 2026-05-12: B5 = BLOCKED
        │
        ▼  (cycle 6 #P — 본 spec + Phase 0 land)
B5 = RESOLVED-SPEC  (actual run = cycle 7+ scope)
        │
        ▼  (cycle 7+ — actual training + emit)
B5 = RESOLVED-EXEC  (Gate B σ_CE_rel 측정 가능 → 15-cell decisive run gate)
```

## Cross-Links

- **parent spec**: `state/phi_ce_orthogonality_decisive_2026_05_11/spec.md` §2.1 / §5 / §5.7
- **parent audit**: `state/phi_ce_orthogonality_decisive_2026_05_11/spec_audit_2026_05_11.md` §5.2 (B5 source finding)
- **parent dryrun-blocker**: `state/phi_ce_orthogonality_decisive_2026_05_11/noise_calibration_dryrun_blocker_2026_05_12.md` §B5
- **naming manifest**: `state/phi_star_naming_refactor_2026_05_12.md` (3-engine split — 본 디렉토리 = CE-track engine)
- **본 spec**: `state/clm_ce_4scale_trainer_2026_05_12/spec.md` (8 sections)
- **harness ingest target**: `state/phi_ce_orthogonality_decisive_2026_05_11/harness.py` (emit consumer)

## Cycle Provenance

- **cycle 6 #P** (2026-05-12): B5 spec + Phase 0 scaffolding land — 본 디렉토리 생성
- **cycle 7+** (future): actual training pipeline implementation (Python script + RunPod orchestrator)

## Prerequisites for Cycle 7+ Actual Run

1. training corpus stage (`tool/hxc_corpus_manifest.hexa` enumeration or OpenWebText subset)
2. GPU allocation — RunPod A100 (40 GB+) recommended; A10/4090 fallback for tiny/small only
3. B4 (parent dryrun-blocker §B4) resolved — `runpod.api_key` access via main process
4. B1 (parent dryrun-blocker §B1) resolved — Φ-track engine usable (CE-track 독립이지만, full Φ×CE join 위해서는 필수)
5. tokenizer cache (skt/kogpt2-base-v2 already in HF cache per dryrun-blocker §1.3)

## Honest Limits

본 README + scaffolding 의 honest limits 는 `spec.md` §8 (L1-L7) 에 위임. 핵심 4 항목:

- L1: 3-scale {1M, 10M, 100M} base + 1B deferred — parent spec §2.1 P-axis 정합
- L2: training corpus 다양성 미명시 — distribution 모순 가능
- L3: tokenizer 통일 가정 — multi-tokenizer 비교 별 cycle
- L4: tiny (P=1M) statistical power 부족 — confidence interval narrow 어려움

---

**lock policy reminder**: chflags +uchg/+schg/chattr +i 적용 *금지*. unlock 된 파일 *재잠금 금지*.
**commit policy**: 본 디렉토리는 *separate commit 금지* — 메인 process 가 일괄 commit.
