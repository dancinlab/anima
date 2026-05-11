---
doc_id: lens_registry_synthesized_2026_05_12
spec_id: nexus6_1013lens_activation_2026_05_11
status: synthesized (1.0-synthesized)
authored: 2026-05-12
authored_by: anima cycle 5 §3 #B
lock_policy: NO chflags/chattr — repository directive 2026-05-11
---

# Lens Registry — Synthesized (audit risk #5 resolution)

`prereq_audit_2026_05_11.md` §5 risk #5 (Hc_960 mislabel: 1013 vs 1588 SSOT 부재)
의 *partial* resolution. hexa-side `lens_registry.json` 가 Mac 원본 (`/Users/ghost/core/nexus/lenses/`)
에 부재함이 cycle 5 §2 Agent 19 의 snapshot 작업에서 확인 — 본 문서는 그 부재를
*synthesized* SSOT 로 메우는 audit trail.

## 1. Synthesizer 정보

| 항목 | 값 |
|------|-----|
| synthesizer | anima cycle 5 §3 #B |
| version | `1.0-synthesized` |
| source | `/home/summer/core/nexus_lenses_snapshot/*.hexa` (1588 files, rsync snapshot from Mac 2026-05-11T23:58) |
| output | `/home/summer/core/nexus_lenses_snapshot/lens_registry.json` (812 KB) |
| synthesized_at | 2026-05-12T00:17:29+09:00 (KST, equiv. 2026-05-11T15:17:29Z) |
| extraction method | hexa header comment block parse — `// 카테고리: X · 도메인: Y` + `// 원본: A · 이름: B` + `// 검증 축: …` |
| hash | per-file sha256 (audit trail; 1588 unique, 0 collision) |

## 2. Counts + Verification

| metric | value | acceptance |
|--------|------:|------------|
| total_lens_count | 1588 | == snapshot file count ✅ |
| sha256_unique_count | 1588 | == total (0 collision) ✅ |
| k10_binding_count | 10 | == spec §3.1 whitelist size ✅ |
| k10_missing | `[]` | 누락 0 ✅ |
| JSON valid (python json.loads roundtrip) | PASS | ✅ |

## 3. K=10 binding full list (spec §3.1 order)

`k10_binding: true` 인 10 entry — 모두 snapshot 에 존재 확인 (audit trail sha256 포함):

| # | filename | axis (metadata) | sha256 (full) |
|--:|----------|------|----------------|
| 1 | `core_info.hexa` | Information-theoretic — mutual information, entropy, compression | `c456c98ddb806caa21fbf8ce62909111dd6baf2ddc52fca32109db3263ef64b1` |
| 2 | `core_causal.hexa` | Causal arrow — directed dependencies and information flow | `4c5a146e59769cd641a07335ff69527c1db2407798a3a68b2a1d10f77abe7469` |
| 3 | `core_consciousness.hexa` | Structural awareness — detects self-referential and emergent patterns | `711963ada1911e28f5e46b7c016a3888c2d7fd388100a6d6b4772ef49c744915` |
| 4 | `core_thermo.hexa` | Thermodynamic lens — entropy flow, energy barriers, phase transitions | `13d1af1f02fb872810f27e4e82c95e622485e8cf44dbf8e38931dff88ad3230f` |
| 5 | `core_quantum.hexa` | Quantum-like superposition, entanglement, tunnelling analogues | `f2afeca2e19371174d66b227d69189d36e2cea361ee9e6013f95f9e550227729` |
| 6 | `core_topology.hexa` | Topological connectivity — holes, loops, and persistent features | `3141a9a679e3fc05fccdcdd47f2d58a855fc5eeaee35a5c4aba04495573fe36b` |
| 7 | `core_gravity.hexa` | Gravitational clustering — mass-like attraction between data regions | `95576cde93ac06deec82f2b898d60837642a12341d6763c59bbbfd5d5b1c94df` |
| 8 | `core_network.hexa` | Network/graph topology — degree distribution, clustering, centrality | `189c369f287c39d24d3533c0037ba20d5e39840a83c68f3b8b8ae28c1b9aef97` |
| 9 | `core_scale.hexa` | Scale/magnification — power-law tails, scale-free structure | `2c770e003a374943de835bca7f3b21f5388f51e3f92401b6d84df96658f7fc3a` |
| 10 | `core_stability.hexa` | Stability analysis — Lyapunov exponents, basin attractors | `8d641b99baeba126ec53626e36fb10ca8ce55e3e0e5341dfa44c98b09ce4b853` |

## 4. Sample 10 non-K10 lens (audit trail spot-check)

| filename | sha256 (first 16) | metadata.category |
|----------|--------------------|-------------------|
| `accel_accretion_disk.hexa` | `f8d4d727de183721` | extended |
| `accel_alignment_measure.hexa` | `0b452ad7d3d88dc1` | extended |
| `accel_active_learning.hexa` | (sampled at JSON line 18) | extended |
| `anima_*` (88 files) | n/a (group) | consciousness category cluster |
| `quantum_*` (~290 files) | n/a (group) | quantum domain cluster |
| `tecs_*` (~103 files) | n/a (group) | TECS-L math |
| `sedi_*` (~101 files) | n/a (group) | signal detection |
| `cross_*` (~77 files) | n/a (group) | cross-domain bridge |
| `n6_*` (~58 files) | n/a (group) | n6 industry |
| `physics_*` (~49 files) | n/a (group) | physics deep |

(전체 audit trail: 1588 sha256 entries — `lens_registry.json` 의 `lenses[*].sha256` 참조.)

## 5. Usage — aggregator wiring

`tool/anima_nexus_1013lens_smoke.hexa` (또는 future K=25/50 aggregator) 가 본 registry 를
참조하려면 env var:

```bash
export NEXUS_LENSES_DIR=/home/summer/core/nexus_lenses_snapshot
export NEXUS_LENS_REGISTRY=$NEXUS_LENSES_DIR/lens_registry.json
```

aggregator pseudo-code:

```hexa
let registry_path = env("NEXUS_LENS_REGISTRY")
let registry = json::parse(read_file(registry_path))
let k10_lenses = registry.lenses.filter(l => l.k10_binding == true)
// k10_lenses.len() == 10 (spec §3.1 binding)
for lens in k10_lenses {
    let lens_path = registry.source_dir + "/" + lens.filename
    run_hexa(lens_path) // ~19 ms per lens
}
```

## 6. Cross-reference + caveats

- snapshot source: `/home/summer/core/nexus_lenses_snapshot/SNAPSHOT_INFO.md`
- spec SSOT row: `state/nexus6_1013lens_activation_2026_05_11/spec.md` §11 (synthesized row 추가됨)
- rust-side reference (별 layer, K=10 binding 아님): `/Users/ghost/core/nexus/config/lens_registry.json`
  (4,000 lens, .rs 기준, BLOW-P9-1 expansion ossify) — 본 synthesized registry 와 **layer 다름**, *reference-only*
- 본 registry 는 `/home/summer/core/nexus_lenses_snapshot/` 에 위치 — anima repo *밖* (snapshot 정책상 git tracking 대상 아님; SNAPSHOT_INFO.md 와 동일 위치)

## 7. Lock policy 준수

본 synthesizer 가 어떤 파일에도 `chflags +uchg/+schg`, `chattr +i`, immutable flag 적용
하지 않았다. unlock 파일 재잠금 시도 없음. (memory: feedback_no_relock.md)

## 8. Open work / next

- nexus repo 측 *공식* `lens_registry.json` (1013-official SSOT) 결정 시 본 synthesized registry 를
  superseded/deprecate
- K=10 aggregator (`tool/anima_nexus_1013lens_smoke.hexa`) 작성 시 본 registry path 를 default 로 wire
- 1013 vs 1588 vs 4000 layer mismatch 의 nexus-repo-측 coordination 은 여전히 open (audit risk #5 *full* resolution 은 그쪽에서만 가능)
