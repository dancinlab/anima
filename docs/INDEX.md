# 📚 docs/ INDEX — Anima Documentation Hub

> **비유** — `docs/` 는 *연구 노트의 도서관* 이다. 본 INDEX 는 도서관 *카드 카탈로그* — 모든 책을 다 읽지 말고, 들어가는 *입구* 만 안내한다.

본 파일은 `docs/` 디렉토리의 **discoverable entry point**. README.md 의 [Research Trail](../README.md#-research-trail) section 에서 직접 link 된다.

전체 file enumeration 은 [TOC.md](TOC.md) (auto-generated, 1,200+ entry) 참조. 본 INDEX 는 *카테고리별 representative anchor* 만 제공.

---

## 🧭 Cycle Master Narratives (single comprehensive entry per cycle)

cycle master doc 은 *외부 researcher / HF dataset reader* 가 본 문서만 읽고도 해당 cycle 전체를 추적 가능한 *자기충족 narrative*. cycle 5 부터 land 시작.

| cycle | doc | window | product | GPU spend |
|-------|-----|--------|---------|----------:|
| 5 | **[cycle_5_master_2026_05_12.md](cycle_5_master_2026_05_12.md)** | 2026-05-11 → 2026-05-12 | 4 axis-conflation discovery + 8 honest finding + 3 H promoted + cost compression $621-1920 → $121-420 | **$0** |

이전 cycle (1-4) 은 retroactive master doc 미land — `state/` directory 에 cycle 별 산출물 분산 보관.

---

## 🗺️ Top-Level Architecture Docs

| doc | role |
|-----|------|
| [ATLAS.md](ATLAS.md) | 전체 architecture 매핑 (8 paradigm + r36-r39 cross-reference) |
| [MODULE-CATALOG.md](MODULE-CATALOG.md) | 모듈 카탈로그 (own/anima/nexus/N6 cross-link) |
| [AGENT-ARCHITECTURE.md](AGENT-ARCHITECTURE.md) | agent layer 설계 (channel + dispatch + ALM hook) |
| [CHANGELOG.md](CHANGELOG.md) | release-level commit narrative |
| [BREAKTHROUGH-STRATEGY.md](BREAKTHROUGH-STRATEGY.md) | breakthrough lane 전략 |
| [MK5-DELTA0-ABSOLUTE.md](MK5-DELTA0-ABSOLUTE.md) | MK5 ΔΨ=0 absolute lane |
| [UPGRADE-ARCHITECTURE.md](UPGRADE-ARCHITECTURE.md) | upgrade migration architecture |
| [ENGINE-NAMING.md](ENGINE-NAMING.md) | engine naming convention (Φ★ 3-engine split SSOT for tooling) |
| [ENGINE-ALL-RESULTS.md](ENGINE-ALL-RESULTS.md) | engine 측정 결과 aggregate |
| [TOC.md](TOC.md) | auto-generated full file list (1,200+ entries) |

---

## 📜 Cycle 5 Cross-References (master doc 정합)

| lane | docs/ 또는 state/ 경로 | role |
|------|------------------------|------|
| numerology n=6 | `state/numerology_critique_n6_2026_05_11/` | 4-stage staircase (depth-3 → depth-4 + perfect-number control) |
| 1013-lens H_135 | `state/nexus6_1013lens_activation_2026_05_11/` | 5-step carve (smoke → TRIVIAL caveat → reimpl spec → K=25 plan) |
| Φ×CE H_080 | `state/phi_ce_orthogonality_decisive_2026_05_11/` | spec audit + noise calibration prereq |
| Φ★ naming refactor | `state/phi_star_naming_refactor_2026_05_12.md` | 3-engine canonical split |
| ANIMA-VOICE H_154 | `state/anima_voice_h1_h8_verify_skeleton_2026_05_11/` | H1-H8 measurement skeleton |
| HF public flip | `state/hf_public_flip_readiness_*.md` | dataset readiness audit (cycle 6 진행 중) |

---

## 🔬 Sister Indexes (cross-repo SSOT)

| 인덱스 | 위치 | scope |
|--------|------|-------|
| **Hypotheses ledger** | [../hypotheses/README.md](../hypotheses/README.md) | 215 정식 H_XXX (pre-register-frozen / running / verdict-*) |
| **Candidates staging** | [../hypotheses_candidates/README.md](../hypotheses_candidates/README.md) | 1,127 Hc (cluster A-N, unverified) |
| **State experiments** | `../state/` | per-experiment dir (spec + harness + results + verdict) |
| **Cycle queue** | [../NEXT.md](../NEXT.md) | 다음 cycle action items (root SSOT) |
| **Philosophy SSOT** | [../README.md#philosophy](../README.md#philosophy) | 8-negation table (no system prompt / no identity rules / no perplexity verdict / ...) |

---

## 🤗 Hugging Face Dataset Mirrors

본 repo 의 *research trail* 은 3 dataset 으로 mirror. 현재 *private* — `state/hf_public_flip_readiness_*.md` audit 결과 통과 시 public flip.

| dataset | URL | content |
|---------|-----|---------|
| anima-hypotheses-candidates | [🤗 dancinlife/anima-hypotheses-candidates](https://huggingface.co/datasets/dancinlife/anima-hypotheses-candidates) | 1,127 Hc cluster A-N (verdict-pending + merge-pending + suspended) |
| anima-nexus-lenses | [🤗 dancinlife/anima-nexus-lenses](https://huggingface.co/datasets/dancinlife/anima-nexus-lenses) | 1,588 hexa lens snapshot + 812 KB lens_registry.json SSOT |
| anima-research-trail | [🤗 dancinlife/anima-research-trail](https://huggingface.co/datasets/dancinlife/anima-research-trail) | cycle master docs + state/ snapshot + commit log |

private 상태일 때 URL visit 시 401 — URL 자체는 *future-public* anchor 로 보존.

---

## 🧪 Module-Level Specs (deep-dive entry points)

| module | spec |
|--------|------|
| tension_link | [modules/tension_link.md](modules/tension_link.md) (5-channel meta-fingerprint, 519 µs latency) |
| modules index | [modules.md](modules.md) |

---

## 📐 Conventions

- **파일명**: 일자별 산출물 → `<topic>_YYYY_MM_DD.md` (예: `cycle_5_master_2026_05_12.md`)
- **legacy 산출물**: `_20260419` (slug-less YYYYMMDD) 형식도 다수 존재 — phased migration 중
- **honest disclosure**: 모든 cycle master doc 은 *negative finding* (refute / TRIVIAL / capability ZERO) 와 *positive finding* (promotion / cost compression / separability) 을 동등 weight 로 land
- **lock policy**: 본 repo 의 모든 .md 는 chflags +uchg/+schg, chattr +i 적용 *금지* (사용자 directive 2026-05-11, `feedback_no_relock.md` 정합)

---

## 🔭 7-element framework alignment (AGENTS.md friendly preset)

| element | 본 INDEX evidence |
|---------|-------------------|
| 비유 | "도서관 카드 카탈로그" (head) |
| 이모지 | 📚 🧭 🗺️ 📜 🔬 🤗 🧪 📐 🔭 |
| 표 | 8 tables (cycle master / architecture / cross-ref / sister / HF / module / convention / 7-element) |
| ASCII diagram | (생략 — table-heavy doc, diagram 은 cycle master 에 위임) |
| 7-element | 7/7 (본 표 자체) |
| 추천 포맷 | 카테고리별 anchor (over enumeration) |
| "다음 진행할 것들" | [../NEXT.md](../NEXT.md) 직접 link (single source) |

---

*last updated: 2026-05-12 by cycle 6 #S — README discoverability + docs index land*
