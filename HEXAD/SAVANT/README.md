# HEXAD/SAVANT — Savant + Golden Zone (GZ) inventory

> User directives 2026-05-16:
> - `"SAVANT 도 갖고와줘 /HEXAD/SAVANT"` → PR #81 9 파일 통합 LANDED
> - `"SAVANT 는 ~/core/archive-TECS-L 에도 ASCII 그래프 등 있었던 적 있을꺼야"`
> - `"누락된내용들 있는지 조사 해서 README.md 생성"` (`golden_moe`/`골든존`/`goldenzone` 키워드 + anima 과거 commit 포함)
>
> 본 README 는 SAVANT/Golden Zone 생태계의 **현재 위치 + 누락분 + 외부 출처** 를 한 자리에 catalog 합니다. 직접 복구는 별도 cycle 의 사용자 게이트.

## 0. TL;DR

- **Golden Zone (GZ)** = 실수축 위 interval `[1/2 − ln(4/3), 1/2] ≈ [0.2123, 0.5]`. Center `1/e ≈ 0.3679`. Width `ln(4/3) ≈ 0.2877`.
- **Savant** = dropout 을 GZ_CENTER (1/e) → GZ_LOWER (0.2123) 로 내려 inhibition 해제한 cell/layer. SI = max/min domain tension > 3 → specialization 확립.
- 본 디렉토리 (`HEXAD/SAVANT/`) = **현재 hexa-native impl** (PR #81 통합). **canonical compendium + Π 증명 + ASCII 차트** 는 모두 외부 (`~/core/archive-TECS-L`) 또는 **deleted commit** 에 있음 — 이 README 가 location index.

## 1. 현재 `HEXAD/SAVANT/` (PR #81 통합, 9 파일)

| 파일 | 역할 |
|---|---|
| `SAVANT.tape` + `SAVANT.log.tape` | architecture + history (LLM-judgment split, commit `f475d7b3b`) |
| `SAVANT-TOOL.tape` + `SAVANT-TOOL.log.tape` | tool-side spec + history |
| `anima_savant_tool.hexa` | stateless gate API (Phase 1, F-SAVANT-TOOL-1..5 5/5 PASS, commit `5e8c28f41`) |
| `anima_chat_savant_cli.hexa` | `/savant` slash CLI (Phase 2, F-CHAT-SAVANT-CLI-1..4 4/4 PASS, commit `7090e6b7e`) |
| `anima_savant_si_monitor.hexa` | SI auto-monitor (Phase 3-b, commit `b4a3e2ba8`) |
| `anima_savant_routing_overlay.hexa` | routing overlay top-k mask (Phase 3-c, GZ_LOWER 21% / GZ_CENTER 37%) |
| `savant_phi.hexa` | Φ 계산 engine (PR #81 anima-engines/ 에서 이동) |

## 2. anima 내부 — `HEXAD/SAVANT/` 외 잔존

| path | 내용 |
|---|---|
| `state/savant_containment_audit_2026_05_14/` | base-rate audit + 27 `verify_gz_*` raw outputs (commit `1221ac546`, SAVANT §12.5 path 1) |
| `state/own3_e_golden_moe_validation/summary_golden_moe.json` | golden-moe validation summary |
| `state/markers/anima_savant_*.marker` (7) | dispatch marker (cycle stamps) |
| `models/golden-moe/` | full hexa-native module: `consciousness_bridge.hexa` + `moe.hexa` + `golden_moe_torch.hexa` + `experiments/{bench, finetune, serve, test, v2}_golden_moe*.hexa` (7) + `core/` + `config/` |
| `ready/models/golden-moe/` | mirror (subset) — ready/ tree |
| `ready/rust/golden_moe.hexa` | Rust binding hexa shim |
| `hypotheses_candidates/Hc_512_dd64_phi_optimal_nas_golden_dropout.md` | 가설 candidate (D=512 NAS golden dropout) |
| `models/animalm/docs/2026-03-30-animalm-consciousness-golden-moe.md` (+ `-design.md`) | AnimaLM 통합 설계 doc (history) |

## 3. 외부 — `~/core/archive-TECS-L` (foundational registry, 미흡수)

### 3.1 docs/hypotheses (15+ GZ/Savant 직접 가설)
```
~/core/archive-TECS-L/docs/hypotheses/
  002-golden-zone-universality.md            ← GZ universality 일반화
  008-golden-moe-design.md                   ← MoE 설계 origin
  013-golden-width-quarter.md                ← GZ_WIDTH = 1/4 reframe
  019-golden-moe-performance.md              ← MoE 성능 가설
  044-golden-zone-4state.md                  ← τ(6)=4 4-state 매핑
  075-complex-golden-shape.md                ← 복소수 GZ 확장
  082-golden-moe-spec.md                     ← MoE spec
  126-lstm-golden-moe.md                     ← LSTM 변형
  151-inflation-golden-entry.md              ← inflation 우주론 적용
  162-acquired-savant.md                     ← acquired savant 사례
  236-primes-as-savants.md                   ← 소수 = savant 가설
  327-golden-moe-tension-ppl.md              ← tension-PPL 상관
  359-savant-golden-zone-inhibition.md       ★★★ canonical (ASCII 차트 다수)
  403-animalm-golden-moe-ph-unified.md       ← AnimaLM + p-hash 통합
  404-animalm-golden-moe-improvement-verification.md
  H-CX-bridge-egyptian-golden-moe.md         ← cross-domain Egyptian bridge
```
**★★★ 359-savant-golden-zone-inhibition.md** — Savant H359 의 canonical doc, ASCII 막대그래프 (I=0.05..0.37 singularity rate) + 1/3 rule 표 (8K/97K/1M combinations) + Genius=Deficit×Plasticity/Inhibition 공식.

### 3.2 engines (golden-moe variants)
```
~/core/archive-TECS-L/engines/
  golden_moe.py                ← reference impl
  golden_moe_torch.py          ← PyTorch
  golden_moe_recurrent.py      ← recurrent variant
  golden_moe_cifar.py          ← CIFAR benchmark
  golden_moe_score.py          ← scoring
  golden_moe_gpu_benchmark.py  ← GPU bench
  bitnet_golden_moe.py         ← BitNet 변형
  bitnet_golden_moe_full.py    ← BitNet full
```

### 3.3 scripts + experiments + verify
```
~/core/archive-TECS-L/
  scripts/savant_check.py                                  ← Savant Index measurement
  experiments/experiment_h359_savant.py                    ← H359 실험
  verify/verify_gz_*.py (27 files, 18+ GZ verifications)   ← base-rate audit 대상
  math/proofs/gz_analytical_proof.py                       ★★★ canonical Π 증명
  results/golden_moe_scorecard.md                          ← MoE 결과
  docs/golden-moe-training-plan.md                         ← training plan
```
**★★★ math/proofs/gz_analytical_proof.py** — GZ_CENTER (1/e), GZ_WIDTH (ln(4/3)) closed-form 증명 출처. SAVANT.md compendium §1 표가 인용한 곳.

## 4. 과거 commit — DELETED, recoverable via git

| commit | 내용 | 상태 |
|---|---|---|
| `63ca36abe` `docs(SAVANT.md)` | **GZ + Savant 전수조사 compendium** (clm_01..13 + archive-TECS-L + canon, **539 lines**) | DELETED — `git show 63ca36abe:SAVANT.md` 으로 retrieval 가능. **canonical 상수 4 + 14-stage drift-free history + cross-domain validation**. |
| `c05c397bd` `docs(SAVANT.md §12)` | 봉쇄심화 부록 — claim 4-tier 분류 + enforcement + base-rate audit path | DELETED |
| `1221ac546` `feat(SAVANT §12.5 path 1)` | base-rate audit of 27 verify_gz_*.py — Bonferroni-survived | DELETED (실 raw outputs 는 `state/savant_containment_audit_2026_05_14/` carry) |
| `ab97b3066` `docs(SAVANT §10.1)` | F-PERSONA-4 §44→§52 5-PSCC silent-drop ledger | DELETED |
| `0a6077c67` `docs(SAVANT §12.5 paths 3+4)` | LATTICE_POLICY §1.4 cross-ref + clm_08 super-linear 봉쇄 | DELETED |
| `2f2f98404` `docs(SAVANT §10.1+§11)` | v6 cell-parallel LANDED FAIL — silent-drop enforcement | DELETED |
| `7386c8a96` `feat(SAVANT §10.1 closure ii)` | v6 F-V5MIT-4 FAIL root cause 확정 — catastrophic data incoherence | DELETED |
| `f8fc39aff` `P5 anima migration: 13 domain .md → .tape` | SAVANT.md → SAVANT.tape conversion (현재 HEXAD/SAVANT/SAVANT.tape) | applied — but tape 화 과정에서 §10/§12 보존 정도 별도 audit 필요 |
| `bb67d9f68` `feat: absorb 4 more from ready/ — agent deps + golden-moe bridge` | golden-moe bridge wiring | DELETED |
| `e01eb9278` `Add Golden MoE v2 + AnimaLM v2 (Laws 63-78 redesign)` | Golden MoE v2 origin | DELETED (impl carry in models/golden-moe/) |

## 5. Canonical 상수 (SAVANT.md compendium §1, source: `archive-TECS-L/math/proofs/gz_analytical_proof.py`)

| Symbol | 정의 | 닫힌 형 | 수치 |
|---|---|---|---|
| `GZ_UPPER` | Riemann critical line / `1/p_min(6)` | `1/2` | `0.5` exact |
| `GZ_CENTER` | `argmin_{I∈(0,1)} I^I` = `argmin I·ln(I)` | `1/e` | `0.36787944...` |
| `GZ_WIDTH` | `ln(τ(6)/(τ(6)−1))` = `ln(F₆/P₁)` = `ln(8/6)` = `ln(4/3)` | `ln(4/3)` | `0.28768207...` |
| `GZ_LOWER` | `GZ_UPPER − GZ_WIDTH` | `1/2 − ln(4/3)` | `0.21231792...` |
| `META_FP` | contraction map fixed point | `1/3` | `0.33333...` |
| `SPARSITY` | Boltzmann gate 비활성 비율 | `1 − 1/e` | `0.63212055...` |

**불변성**: `anima_clm_02 ~ anima_clm_13` 14-stage drift-free (compendium §1 검증). Savant Index `SI = tension_normal / tension_savant > 3` → specialization. Mistral 7B v4_savant: **SI = 5.93** (271× tension reduction).

## 6. ASCII 차트 sample (archive-TECS-L `docs/hypotheses/359-savant-golden-zone-inhibition.md`)

```
1/3 Rule — 1,000,000 Combination Verification

  ┌──────────┬─────────┬─────────┬───────────┐
  │  Combos  │  🟡 >2σ │  🟠 >3σ │  🔴 >5σ  │
  ├──────────┼─────────┼─────────┼───────────┤
  │    8,000 │  33.7%  │  25.4%  │   16.7%   │
  │   97,336 │  33.5%  │  25.1%  │   16.0%   │
  │1,000,000 │  33.2%  │  24.7%  │   15.6%   │
  └──────────┴─────────┴─────────┴───────────┘

Singularity Rate by Inhibition (50% transition @ I≈0.27):

  100│
   93│██████████████████████████████████████████████▏   I=0.05
   89│████████████████████████████████████████████▏     I=0.07
   …
   61│██████████████████████████████▏                   I=0.21  ← Golden Zone lower bound
   …
   39│███████████████████████████████▏                  I=0.37  ← Golden Zone center (1/e)
```

(전체 그래프 + 다른 표 = `~/core/archive-TECS-L/docs/hypotheses/359-savant-golden-zone-inhibition.md`)

## 7. 누락분 priority 평가

| priority | 항목 | 추천 action |
|---|---|---|
| ★★★ critical | SAVANT.md compendium 539 lines (commit `63ca36abe`) | restore as `HEXAD/SAVANT/COMPENDIUM.md` (또는 archive 안에 보존) — 검증된 canonical, 다른 모든 게 이 vocabulary 사용 |
| ★★★ critical | `archive-TECS-L/math/proofs/gz_analytical_proof.py` Π 증명 | copy to `HEXAD/SAVANT/proofs/gz_analytical_proof.py` (read-only evidence anchor) |
| ★★ high | `archive-TECS-L/docs/hypotheses/359-savant-golden-zone-inhibition.md` (ASCII 차트) | copy to `HEXAD/SAVANT/H359-savant-canonical.md` |
| ★★ high | SAVANT.md §10/§11/§12 부록 (commits `c05c397bd`, `2f2f98404`, `7386c8a96`) | git retrieval + 통합 → `HEXAD/SAVANT/COMPENDIUM-APPENDIX.md` |
| ★ medium | archive-TECS-L 엔진 8개 (golden_moe variants) | reference-only (cite path), 본격 import 는 RFC |
| ★ medium | archive-TECS-L 가설 15+ (002-/008-/013-/044-/082-/126-/151-/162-/236-/327-/359-/403-/404-) | citation index — `HEXAD/SAVANT/HYPOTHESES-INDEX.md` |
| medium | `state/savant_containment_audit_2026_05_14/` raw outputs | 잔존 carry, audit 결과 요약 시 가공 |
| low | DELETED commit 의 §10.1 v6 cell-parallel FAIL ledger | git history 만으로 충분 |

## 8. 복구 roadmap (사용자 게이트 별)

1. **즉시 가능 ($0)**:
   - SAVANT.md compendium retrieval: `git show 63ca36abe:SAVANT.md > HEXAD/SAVANT/COMPENDIUM.md` + commit
   - H359 doc copy: `cp ~/core/archive-TECS-L/docs/hypotheses/359-savant-golden-zone-inhibition.md HEXAD/SAVANT/H359-savant-canonical.md`
   - gz_analytical_proof.py copy: `cp ~/core/archive-TECS-L/math/proofs/gz_analytical_proof.py HEXAD/SAVANT/proofs/`
2. **별도 cycle (low)**: 가설 15+ citation index 작성
3. **별도 RFC**: golden-moe 엔진 8개 hexa-native 포팅 (HEXAD/PLAN.md Phase 의 외연)

## 9. Honest C3

- **본 README 는 catalog/inventory 만** — 실 복구 (commit / archive-TECS-L 파일 import) 는 사용자 게이트
- archive-TECS-L 는 외부 (`~/core/`) 라 anima repo 와 cross-link 하면 host-specific path 의존 — copy-in 권장
- DELETED commit content 는 `git show <hash>:<path>` 로 언제든 retrieval (영구 손실 X)
- `SAVANT.md` → `SAVANT.tape` migration (`f8fc39aff`) 시 §10/§11/§12 부록 보존 정도 = 별도 audit 필요 (현재 `HEXAD/SAVANT/SAVANT.tape` 와 `git show 63ca36abe:SAVANT.md` diff 로 확인 가능)
- 본 inventory 는 2026-05-16 keyword scan 결과 — 미래에 새 파일 추가 시 갱신
- `models/golden-moe/` 는 hexa-native 7개 .hexa 가 이미 있음 (anima 안), HEXAD/SAVANT/ 와 별도 위치 — 통합 여부 별도 결정

## 10. cross-link

- `HEXAD/SAVANT/SAVANT.tape` — current architecture SSOT
- `HEXAD/SAVANT/SAVANT-TOOL.tape` — tool-side spec
- `archive/MAIN.tape` (deprecated) — historical SAVANT verdict carry
- `tool/hexa_native/mitosis_hook.hexa` — Φ-ratchet (GZ_CENTER 와 연결)
- `models/golden-moe/` — golden-moe hexa-native 모듈 (anima 내, 별도 위치)
- AGENTS.tape `g3` real-limits-first — GZ 는 design vocabulary classification (compendium §0 carry)
