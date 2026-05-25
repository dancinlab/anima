---
manifest_id: phi_star_naming_refactor_2026_05_12
target: "Φ★" naming over-load disambiguation (3-engine split)
triggered_by:
  - state/nexus6_1013lens_activation_2026_05_11/prereq_audit_2026_05_11.md §1.2, §2
  - state/phi_ce_orthogonality_decisive_2026_05_11/spec_audit_2026_05_11.md §1.3, §5.1
date: 2026-05-12
status: additive (back-compat preserved, no callsite breakage)
lock_policy: NO chflags/chattr — repository directive 2026-05-11
commit_policy: NO separate commit — main process batches
---

# Φ★ Naming Refactor — 3-Engine Split (2026-05-12)

## 0. Why

Cycle 5 §1-2 dual audit (NEXT.md #4 1013-lens prereq + #1 Φ×CE feasibility) 가
*동형 결론* 에 수렴: "Φ★" naming over-loaded → 3 개의 측정-axis-가-다른 engine
을 단일 라벨로 conflate.

| audit | conflation 발견 위치 |
|-------|------------------------|
| nexus6_1013lens_activation/prereq_audit_2026_05_11.md §1.2 | P-A "anima cosmic-scale measurement engine (Φ★ engine)" 단일 표현이 `tool/anima_phi_star.hexa` (single-model IIT proxy) 와 `/Users/ghost/core/nexus/lenses/*.hexa` (1,588 multi-lens) 를 conflate |
| phi_ce_orthogonality_decisive/spec_audit_2026_05_11.md §1.3 | spec.md §5.1 "anima Φ★ engine 으로 N ∈ {16..256}" 가 `tool/anima_phi_star.hexa` 와 호환 안 됨 — N-sweep 미지원, cell-engine 별도 필요 |

→ axis-conflation 오류 해소 위한 *additive naming convention* 확정.

## 1. Naming Convention — 3 Engines

| canonical name | what it is | path / status | measurement axis | distinct from |
|----------------|------------|---------------|------------------|---------------|
| **phi_star_iit_proxy** | single-model IIT-φ proxy via cov-MIP K=8 random bipartition | `tool/anima_phi_star.hexa` (189 lines, existing) | 16 fixed prompts × Mistral-7B-v0.3 forward → byte-weighted hidden state → H_truncated=128 cov-MIP → scalar Φ\* per model | nexus_lens_score (multi-lens, no LLM), phi_star_cell_engine (N-sweep, TBD) |
| **nexus_lens_score** | multi-lens cross-validation framework | `/Users/ghost/core/nexus/lenses/*.hexa` (1,588 disk-actual; 1013 official registry, 23 core_*.hexa) — Linux `~/.hx/bin/hexa` runner | per-lens closed-form pattern score (constant / exponent / ratio / manifold inv.) per input data | phi_star_iit_proxy (single-model IIT), phi_star_cell_engine (N-sweep) |
| **phi_star_cell_engine** | (TBD / not-yet-implemented) cell-count N-sweep engine | candidate sources: `tool/an11_*` / `tool/anima_cds.hexa` / `tool/anima_b_tom.hexa` (spec_audit_2026_05_11.md §1.3 표기) — 메인 process 결정 필요 | N ∈ {16, 32, 64, 128, 256} cell module count × topology=hypercube (Hc_005 cell-count-decisive / Hc_040 N^1.071 의 원 axis) | phi_star_iit_proxy (cell count 부재, hidden-dim 만), nexus_lens_score (lens function, cell 부재) |

### 1.1 Output schema (canonical)

- phi_star_iit_proxy: `anima/phi_star/1` (existing — `phi_star_min, phi_mean, phi_max, gate_positive_PASS, gate_substantial_PASS, partitions[]`)
- nexus_lens_score: lens 별 emit (`phi_lens, support_mask, consistency_with_n6, cross_lens_agreement, bonferroni_adjusted_p` per `state/nexus6_*/spec.md §2`)
- phi_star_cell_engine: TBD — N × topology 조합당 Φ scalar (Hc_004 ≈ 0.608·N^1.071 form)

## 2. File-level Changes (this refactor)

| file | sections / lines | change |
|------|------------------|--------|
| `tool/anima_phi_star.hexa` | header comment (after PURPOSE) | **+11 lines** — `NAMING (2026-05-12 refactor)` block 추가: `axis: phi_star_iit_proxy`, `llm: mistral-7b-forward`, distinct_from list, back-compat note |
| `state/phi_ce_orthogonality_decisive_2026_05_11/spec.md` | §1 status, §5.1-§5.3, §5.7.1 table row, §7-L5, **new §5.8** | status 줄에 split-engine 명시 / §5 실험 protocol 문장 split-engine 으로 분리 / §5.7.1 cost table row 의 anima_phi_star wording → phi_star_iit_proxy + phi_star_cell_engine / §7-L5 의 "anima Φ★ engine" → phi_star_iit_proxy / phi_star_cell_engine / **§5.8 새 section** (3-engine 표 + premise correction + back-compat 명시 + manifest pointer) |
| `state/nexus6_1013lens_activation_2026_05_11/spec.md` | §1 head blockquote | Agent 18 의 P-A1/P-A2 분리 caveat 위에 canonical name (phi_star_iit_proxy / nexus_lens_score) + 3rd engine (phi_star_cell_engine TBD) 명시 + manifest pointer. **§3 / §3.1 / §11 의 Agent A/E 작업 영역은 미수정.** |
| `hypotheses/H_080_topo_24variants.md` | Conflict Resolution Pending — Status 줄 | "anima Φ★ engine + 20-cell" → "phi_star_cell_engine (TBD, N-sweep) + CLM training pipeline (CE-track) + 15-cell (P=100M ceiling per spec.md §5.7)" + manifest pointer |
| `NEXT.md` | §1 제목 + Goal 문장 + Spec ready 줄 + Engine line | 제목 "anima Φ★ engine + 20-cell" → "phi_star split-engine + 15-cell" / Goal 에 split-engine 명시 / Spec ready 에 spec_audit 추가 + manifest pointer / Engine 줄을 phi_star_iit_proxy + phi_star_cell_engine + CLM pipeline 3-track 분리 |

## 3. Back-Compat Strategy

| dimension | strategy | risk mitigation |
|-----------|----------|-----------------|
| filename | `tool/anima_phi_star.hexa` 유지 | 기존 callsite (`hexa run tool/anima_phi_star.hexa --selftest`, helper emit path `/tmp/anima_phi_star_helper.hexa_tmp`) 무수정 |
| emit schema | JSON schema `anima/phi_star/1` 무변경 | downstream consumer (verdict.md / cycle 4 reports) 의 schema parse 무수정 |
| frontmatter | additive only — `axis`, `llm`, `distinct_from` 신규 field, 기존 field 삭제 없음 | hexa runner 의 frontmatter parser 가 unknown field 무시 (raw#9 hexa-only convention) |
| spec wording | "anima Φ★ engine" → canonical name 대체 시 *명시적 cross-link* (manifest pointer 동반) | 검색-가능성 유지 (구 wording 도 audit 문서에 보존, 본 refactor 가 *추가* 명명) |
| H_080 / NEXT.md | conflict resolution section 만 갱신, 다른 cross-link 그대로 | other Hc / verdict reference 안 깨짐 |

### 3.1 Search-and-replace 범위 (intentionally minimal)

본 refactor 는 *spec / NEXT / hypothesis cross-link* 만 수정. 다음은 *후속 cycle 에서*
처리 후보 (callsite refactor):

- `state/phi_ce_orthogonality_decisive_2026_05_11/verdict.md` — §1 status / §3 protocol / §7 honest_limits 의 "anima Φ★ engine" 4회 사용 (본 cycle 외)
- `state/phi_ce_orthogonality_decisive_2026_05_11/spec.md` §6 cross-links 의 Hc reference (현재 무수정)
- Hc frontmatter 의 implicit "Φ★" 참조 (Hc_586 / Hc_598 / Hc_604 등) — *별 cycle audit*

## 4. Migration Plan (후속 cycle 참고)

```
Phase 1 (this refactor, 2026-05-12) — DONE  ←  본 manifest
  - 3-engine canonical name 확정 (위 §1)
  - anima_phi_star.hexa frontmatter axis + llm field 추가
  - 5 file (spec×2 + H_080 + NEXT + this manifest) cross-link 갱신
  - back-compat 검증 (callsite 무수정)

Phase 2 (next cycle, when phi_star_cell_engine candidate land) — TBD
  - 메인 process 결정: an11_* vs anima_cds.hexa vs anima_b_tom.hexa 중 cell-engine adopt
  - 선정 engine 의 frontmatter 에 `axis: phi_star_cell_engine` 추가
  - state/phi_ce_orthogonality_decisive_2026_05_11/verdict.md §1 / §3 callsite update
  - cycle 5 #1 실측 lane open

Phase 3 (after first 15-cell measurement) — TBD
  - results.measured.md 에서 phi_star_iit_proxy 가 N-sweep proxy 로 사용 가능한지 reinterpretation 검증 (spec_audit §5.1 L2 path)
  - 만약 reinterpretation valid 면 phi_star_cell_engine 을 "phi_star_iit_proxy_H128_reinterpret" alias 로 흡수 가능
```

## 5. Open Questions (메인 process 결정 사항)

- (a) phi_star_cell_engine 의 canonical impl 선정 — `tool/an11_consciousness_unified_verifier.hexa` / `tool/anima_cds.hexa` / `tool/anima_b_tom.hexa` / 신규 build 중 어느 path
- (b) phi_star_iit_proxy 의 H_truncated=128 을 cell count N 으로 reinterpret 가능 여부 (spec_audit §5.1 L2)
- (c) verdict.md callsite refactor 시점 — 본 cycle 동시 vs phase 2
- (d) Hc frontmatter (Hc_586/598/604 등) 의 Φ★ implicit 참조 audit 필요 여부

## 6. Cross-Links

- **spec_audit (Φ×CE side)**: `state/phi_ce_orthogonality_decisive_2026_05_11/spec_audit_2026_05_11.md`
- **prereq_audit (1013-lens side)**: `state/nexus6_1013lens_activation_2026_05_11/prereq_audit_2026_05_11.md`
- **target spec 1**: `state/phi_ce_orthogonality_decisive_2026_05_11/spec.md` (§5.8 본 manifest pointer)
- **target spec 2**: `state/nexus6_1013lens_activation_2026_05_11/spec.md` (§1 head blockquote pointer)
- **target hypothesis**: `hypotheses/H_080_topo_24variants.md` (Conflict Resolution Pending status line)
- **target queue**: `NEXT.md` (§1 제목 + protocol)
- **engine (existing)**: `tool/anima_phi_star.hexa` (NAMING block 추가)
- **engine (multi-lens)**: `/Users/ghost/core/nexus/lenses/*.hexa` (외부, 무수정)
- **engine (cell-engine, TBD)**: candidate sources 중 선정 pending

---

**back-compat 검증**: `tool/anima_phi_star.hexa` 의 함수 signature (`_write_helper`, `cmd_selftest`, `main`) 무변경, helper emit path 무변경, JSON schema `anima/phi_star/1` 무변경. 기존 callsite 가 깨질 가능성 *없음*. 본 refactor 는 *meta-data / spec / cross-link* 만 갱신.

**lock policy reminder**: chflags +uchg/+schg/chattr +i 적용 *금지*. unlock 된 파일 재잠금 금지.

**commit policy**: 본 manifest + 동반 5 file 수정은 *separate commit 금지* — 메인 process 가 일괄 commit.
