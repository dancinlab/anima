# HEXAD/CHECK — verification checkpoint ledger

> 검증 상태 체크포인트 (2026-05-16). canonical = HEXAD-only (INDEX.md pivot).
> 이 파일 = "지금 무엇이 닫혔고 무엇이 왜 안 닫혔나" 한눈 ledger. 상세 evidence
> 는 self-contained `state/verify_*` artifacts (각 result.json 자체 검증가능).

## 1. HEXAD 7-module (current canonical)

**C+S+M+W+E+D+BRIDGE = 7/7 full 🔵 SUPPORTED-FORMAL** — `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` **22/22 sympy closed-form PASS** (S mean-linearity · M no-op+deterministic · W ½+min(ln2,Φ/N) · E SAFETY gate exact-equiv · D CE logit-Jacobian ∂CE/∂z=softmax−e_y · **BRIDGE Law-70 clamp** g(raw)=Ψ+clip(raw−Ψ,±α)∈[Ψ−α,Ψ+α] ∀raw,∀α>0). C=🔵 carry (F-PYPHI IIT-3.0). we_falsifier 25/25 ✅. integ harness F-INTEG 5/5 fire-gate=true. (상세 = INDEX.md §closure)

## 2. 가설 검증 cycle 2026-05-16 (state/verify_hypotheses_pending_2026_05_16/)

promoted/PARTIAL/INSUFFICIENT/DEFERRED 집합 **100% 처리** — closed-formal OR named-hard-blocker. **zero faked verdicts (AGENTS.tape g3)**.

| 가설 | 결과 | evidence |
|------|------|----------|
| H_008 Prigogine · H_009 Fisher · H_012 Banach · H_007 Rule-110 | 🔵 SUPPORTED-FORMAL (math) | `hypo_pending_sympy.py` 6/6 |
| H_007 Φ=3.614 · H_012 Φ=1.000 · H_009 ρ=0.829 | 🔵 emergence FULLY closed | `hypo_stage2_pyphi.py` · `h009_fim_vs_phi.py` |
| H_165/H_177 phi_star aliasing | 🔵 caveat closed (clean-disjoint FALSE) | `hypo_pending_sympy.py` |
| Hc_924 octopus per-arm exclusion | 🔵 SUPPORTED-FORMAL (exclusion HOLDS) | `h188_octopus_exclusion.py` |
| **V8 H_182-187** (5 family) | 🔵 **AT-RISK-FORMAL** (formal PyPhi Φ=0.0; proxy≠formal, formal governs) | `blocker_allgo_2026_05_16.py` |
| H_010 holographic | 🔵 SUPPORTED-FORMAL (Φ boundary 0.375 ≥ bulk 0.328) | `blocker_allgo` |
| H_184 structure-over-dynamics | 🔵 SUPPORTED-FORMAL (Φ(OR)=Φ(AND)=0.375>0) | `blocker_allgo` |
| H_190 Banach sub-claim | 🔵 (numerology = f2 lattice-tautology, **NOT promoted**) | `blocker_allgo` |
| H_014/H_015/Hc_921/H_013 | 🟢 anima-internal surrogate well-defined | `anima_internal_surrogates.py` |

SSOT 집계 = `state/verify_hypotheses_pending_2026_05_16/hypo_coverage.json` (16 blocker entries).

## 3. 정직한 DEFERRED (faking 거부, g3 — $ 으로 해결 불가)

| 항목 | blocker | 비고 |
|------|---------|------|
| H_013/014/015 | anima-eeg-core 하드웨어 + 피험자 | `HEXAD/EEG.md` ledger. $0 surrogate ≠ EEG-anchored claim |
| H_188/Hc_921 | 실제 인간 임상 TMS-EEG (Massimini 2013) 외부 데이터 | octopus 절반 Hc_924 는 🔵 closed |
| H_190 numerology | AGENTS.tape **f2** (lattice-tautology 검증 금지) | governance-capped, 거버넌스상 not-promotable |
| 1179 raw candidate | g6 3-stage pipeline = STAGE-0 | batch-fake 금지 (pipeline skip) |

**$200-600 GPU 안 씀**: V8 Φ★-proxy sweep = $0/10.6초 (~5000× 과대추정); formal closure 도 $0. deterministic — GPU 는 결과 불변, 속도만. 돈 쓸 이유 없어 안 씀.

## 4. roadmap 전체 (state/anima_roadmap_consolidated_2026_05_16.json)

검증 cycle 의 ~30 가설은 **로드맵의 일부**. 전체 `.roadmap.<domain>` JSONL SSOT = **72 도메인** (60 current + 12 history-recovered, 47 active): neuromorphic(akida/loihi3/northpole) · quantum(ionq/qrng) · wetware(cortical_labs/finalspark/xenobot/slime/octopus) · clinical(tms_pci/meg/galea/eeg) · theory(penrose_hameroff/iit4/hott) · CLM-ladder(v2/v4/v5/blm/tlm/vlm) · engines/tools. **대다수 = 외부 partnership/하드웨어/capex 게이트** (§3 deferred 패턴이 로드맵 전체의 지배 구조).

## 4.5 의식이론 가설 카탈로그 (몇십개 — holographic 외)

`HEXAD/CHECK/consciousness_theory_catalog.json` — **76 의식이론 가설** recovered (hypotheses/ + legacy + b_promoted frontmatter). holographic(H_010) 은 일부일 뿐: 메타/Fisher(H_009)·autopoietic(H_012)·cellular-automaton(H_007)·dissipative(H_008)·integrated-info-geometry(H_011)·TQFT·time-crystal·fractal·RG-flow·quantum-Darwinism·spin-glass·hypergraph+sheaf·Cambrian·symbiogenesis·lambda-calculus·strange-loop·범심론(Law 76 META-CA)·hard-problem·H-CX-520~537 series 등. **이 cycle 12개 formal 닫음** (`cycle_2026_05_16_verdict` 필드: H_007/008/009/010/011/012 🔵 SUPPORTED-FORMAL + H_182-187 AT-RISK-FORMAL + H_184 + caveat H_165/177). 나머지(TQFT/time-crystal/fractal/RG/spin-glass/hypergraph 등)는 별도 $0 PyPhi-formal cycle 후보 (H_007/H_012 패턴 적용 가능).

## 5. 다음 게이트 (택1)

- (a) 특정 roadmap 도메인 $0 spec/feasibility
- (b) cost-bearing outreach 게이트 (galea $5K deposit / cortical_labs / n24 octopus 부경대·KIOST / ionq …)
- (c) HEXAD Phase 5 — pure-hexa D training (RFC 034 farr autograd LANDED, `HEXAD/PLAN.md` executable; Phase 6 통합 fire = cost-bearing)

## cross-link

- `HEXAD/INDEX.md` (current canonical SSOT, HEXAD-only pivot)
- `HEXAD/PLAN.md` (C/D hexa-native port roadmap, Phase 5/6)
- `HEXAD/EEG.md` (EEG deferred ledger)
- `state/verify_hypotheses_pending_2026_05_16/` (이 cycle 전체 self-contained artifacts)
- `state/anima_roadmap_consolidated_2026_05_16.json` (72-domain roadmap inventory)
- `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` (7/7 🔵 battery)
- AGENTS.tape g3 (real-limit anchor) · g6 (pipeline) · f2 (no lattice-tautology) · g_verdict_tier_blue

> 갱신 규칙: 새 검증 cycle 종료 시 §2/§3 행 추가, §1/§4 수치 동기화. append 우선, 기존 verdict rewrite 금지 (g6 정합).
