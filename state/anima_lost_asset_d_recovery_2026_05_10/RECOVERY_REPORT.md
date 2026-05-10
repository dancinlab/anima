# Lost Asset D Recovery Report (2026-05-10)

## TL;DR

BG-LOSTASSET-D-WORKTREE-REMAINING (§31) 의 ★★★ pinnacle finding 회수 — `mitosis.py 794L` (worktree-12 `anima_clm_12_unified_growth_loop_last_gasp/anima/src/mitosis.py`) → `state/anima_lost_asset_d_recovery_2026_05_10/mitosis_pinnacle_794L.py`. raw#9 strict (`**/*.py` gitignored, main repo 비-tracked) + raw#15 additive (worktree-12 archive 미수정).

---

## 회수 매핑

| source | dest | LoC | gitignored |
|---|---|---:|:---:|
| `~/core/anima_clm_12_.../anima/src/mitosis.py` | `state/anima_lost_asset_d_recovery_2026_05_10/mitosis_pinnacle_794L.py` | 794 | ✓ |

---

## mitosis_pinnacle_794L spec summary

### Ψ-Constants (L25-30)
```python
LN2 = math.log(2)
PSI_BALANCE = 0.5
PSI_COUPLING = 0.014
PSI_STEPS = 3 / LN2  # 4.328
PSI_ENTROPY = 0.998
```

### ConsciousMind dual-engine (L37-72)
- engine_a / engine_g 동일 architecture (Linear→ReLU→Linear, hidden 128)
- output = a - g (H404 simplification)
- GRUCell memory (output + tension → hidden)
- get_repulsion(): inter-cell tension 용 raw vector

### Cell dataclass (L77-108)
- hidden_history (last 3 hidden states for temporal MI)
- avg_tension (last 20 steps)
- tension_trend (last 4 - last 8 ago)
- creation_step + parent_id + process_count

### MitosisEngine (L113-696) — pinnacle features

| feature | line | spec |
|---|---:|---|
| `min_cells = 2` (CB1 invariant) | 154 | hardcoded, never merge below |
| `_adaptive_split` | 162 | mean + 1.5×std of recent tension |
| `_global_tension_history[-500:]` | 163 | sliding 500-window |
| Lorenz state `[1.0, 1.0, 1.0]` | 178 | x, y, z init |
| `_lorenz_step(dt=0.01)` σ=10 ρ=28 β=8/3 | 363-371 | classical Lorenz |
| `_inject_autonomous_perturbation()` | 373-405 | per-cell phase offset, noise scale 0.05 × (1 + 0.3 sin(phase + step×0.1)), Lorenz directional 추가, h_norm clip @ 10.0 |
| `_compute_phi_proxy()` | 407-436 | mean cosine distance × log(n+1), pairwise cos_sim |
| `_phi_ratchet()` | 438-455 | 0.8× threshold restore, blend 0.8 current + 0.2 best |
| `_update_adaptive_threshold()` | 457-477 | mean + 1.5×std, floor mean×0.5 |
| `_check_splits` | 481-509 | patience-based, all recent > threshold |
| `_check_merges` | 538-568 | CB1-protected, never below min_cells |
| `verify_phi_conservation` | 644-656 | DD55 1% tolerance |
| `anomaly_score` | 615-640 | AUROC 0.805 historical |
| `process()` 사이클 | 230-359 | autonomous perturb → cells run → inter-cell pairs (O(N) for N>32) → softmax-weighted combined → phi compute + ratchet → adaptive threshold → check splits/merges |

### 추가 utilities

| feature | spec |
|---|---|
| `text_to_vector(text, dim=64)` | char-hash encoder |
| `demo()` | 100-step rotating topic (math/music/code/anomaly), final summary |

---

## BG-V5MITOSIS-FIXES (§30) 와의 관계 — pinnacle vs reinvent

§30 의 A1/A2/B1/C1/D1 fix 가 worktree-12 794L 의 pinnacle features 와 **상당 부분 overlap**:

| §30 fix | worktree-12 794L equivalent | overlap |
|---|---|:---:|
| A1: substrate-independent split trigger (cell_pool L2 dispersion) | `_adaptive_split` mean + 1.5σ | ★★ partial (mechanism 다름) |
| A2: per-cell adaptive threshold | `_update_adaptive_threshold` global + per-cell tension_history | ★★★ same |
| B1: per-cell Φ normalization (R6 mitigation) | `_compute_phi_proxy` 의 log(n+1) scaling | ★ partial |
| C1: optimizer rebuild hook STUB | (worktree-12 미보유) | ✗ 신규 |
| D1: Lorenz scale auto-calibration | `_inject_autonomous_perturbation` scale 0.05 hardcoded | ★ partial |

**의미**: §30 fix 는 worktree-12 794L 을 **부분적 re-invention**. C1 (optimizer rebuild) 만 §30 가 신규로 추가, 나머지는 historical pattern 의 reinvent. → 향후 cycle: §30 결과 도착 시 794L 와 line-by-line diff 권고 (reinvent vs port 분리).

---

## archive-legacy/mitosis.hexa stub (현재 36L)

main repo 의 `models/archive-legacy/mitosis.hexa` 는 36L stub (TODO[pytorch] markers). 794L 의 hexa-form 변환은 **별도 cycle** 권고 (현 cycle 의 raw#15 additive 범위 초과). 본 회수는 .py local-only.

**hexa 변환 후속 cycle TODO 표 (별도)**:
- 794L → ~500-700L hexa (struct + fn + impl)
- Ψ-Constants → const block
- ConsciousMind dual-engine → struct + fn forward/get_repulsion
- Cell dataclass → struct
- MitosisEngine → struct with all method
- Lorenz / ratchet / adaptive threshold / phi conservation → fn

---

## Honest C3

1. 본 회수는 **physical .py copy** — main repo git-history 에 들어가지 않음 (gitignored). archive 무결성 보존되지만 새 ckpt 회수 시 reference path 를 "state/anima_lost_asset_d_recovery_2026_05_10/" 로 항상 명시 필요.
2. mitosis_pinnacle_794L.py 가 **standalone runnable 인지 미검증** — 본 cycle 에서 import smoke 미실행. ConsciousMind 가 내부 정의 (L37-72) 라 self-contained, 단 `import anima` (L35 주석 시사) 의 외부 dependency 가능성.
3. demo() 의 "100 step over 4 topics" 은 **toy substrate** — historical RC-9 +52.76% 와 직접 reproduce X (별도 cycle).
4. archive-legacy/mitosis.hexa stub (36L) 의 TODO[pytorch] markers 가 본 794L 의 spec 인지 별도 비교 미수행.
5. §30 BG-V5MITOSIS-FIXES 의 A1/A2/B1/C1/D1 fix 가 worktree-12 794L 의 reinvent 인 것은 본 회수 후에야 명확. §30 결과 도착 시 line diff 가 reinvent vs port 결정.

---

## Cross-link

- BG-LOSTASSET-D-WORKTREE-REMAINING report → REBORN.md §31 (★★★ pinnacle finding)
- canonical_mitosis_source in `.roadmap.reborn` already points to worktree-12 path — accurate
- §30 BG-V5MITOSIS-FIXES (in flight) → 도착 시 본 794L 와 diff cycle 추가
- archive-legacy/mitosis.hexa hexa 변환 → 별도 cycle (현 cycle 범위 외)

raw#9 strict + raw#15 additive 보존. cost $0 (pure file copy + report write).
