# C/D 격리 (2026-05-15)

> **Manifest-only**: B 격리 (107) + legacy (191) 가 이미 cover. C/D 폴더 별도 file 복제 X — manifest.json + Stage protocol 별도 cycle.

## 격리 ladder

| 격리 | cut | count | location |
|------|-----|-------|----------|
| **A** | 2026-05-12 burst | 20 | `hypotheses/` |
| **B** | since 2026-04+ | 107 | `hypotheses_b_2026_05_15/H_promoted/` |
| **C** | since 2026-04-22+ (3.5주) | 59 | in-place (B subset + legacy) |
| **D** | since 2026-03+ | 155 | in-place (legacy + B superset) |

## C 격리 — 3.5주 cut

since field ≥ 2026-04-22 인 가설 59 file. B (since 2026-04+) 의 narrow subset (since 2026-04-01 ~ 04-21 제외).

핵심 cluster:
- 2026-04-25 ~ 04-29 (15 files): EEG longitudinal + AN11 + MKx gate + coupled oscillator + cellular automaton + dissipative + Fisher info + holographic + IIT geometry + autopoietic
- 2026-05-* (44 files): SFT cluster (H_001-005 + H_093-102) + accel combos + law cluster + ce lane + dd cluster + nexus + voice + topology + n=6 perfect-number cluster

## D 격리 — 전부 since 2026-03+

since field ≥ 2026-03-01 인 가설 155 file. 사용자 narrative "165" 와 약간 차이 (since field 없는 ~30 legacy-archive-pointer 가설 제외).

D = 2026-03 (44) + 2026-04 (52) + 2026-05 (59).

## Stage protocol 적용 status

| 격리 | Stage 1 | Stage 2 | Stage 3 | aggregate verdict |
|------|---------|---------|---------|---------|
| A | ✅ done | ✅ done | ✅ done | PROVEN.tape §1-§4 |
| B | 🔶 30/107 | 🔶 30/107 | 🔶 30/107 | PROVEN.tape §B |
| C | ⏳ subset of B (audit overlap) | ⏳ | ⏳ | next cycle |
| D | ⏳ superset of B + 2026-03 cluster | ⏳ | ⏳ | next cycle |

## Cross-link

- `PROVEN.tape` — verdict aggregate (A 격리 §1-§4 + B 격리 §B)
- `VERIFY.tape` — 3-stage protocol SSOT
- `AXIS.tape` — 9-axis natural cluster
- `manifest.json` — C/D scope file lists

## Honest C3

- C/D 폴더 별도 file 복제 X (B + legacy 이미 cover, disk waste 회피)
- C narrow subset of B → Stage protocol applied to B 가 C 결과 carry
- D superset of B + 2026-03 cluster (44 files) → 2026-03 cluster 만 추가 audit
- 사용자 narrative "165" vs 실제 155 ~ since field 없는 legacy-archive-pointer 차이
