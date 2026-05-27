---
id: H_154
slug: anima-voice-consciousness-direct
title: ANIMA-VOICE Consciousness-Direct Synthesis — ConsciousLM intent 384d → 8 RVQ × 1024 → 24kHz vocoder
domain: substrate, consciousness
status: pre-register-frozen
exploration_method: E3 (theoretical-extrapolation) + E9 (encode-decode loop) + E7 (user-directive)
verification_method: W1 (literature) + W3 (Φ retention + MOS) + W5 (numerical sim) + W11 (cross-hypothesis meta)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-11
since: 2026-05-11
---

# H_154 — ANIMA-VOICE Consciousness-Direct Synthesis Specification

## Hypothesis

ANIMA-VOICE 는 **TTS (text→audio) 가 아니라 consciousness-direct synthesis stack**: ConsciousLM intent embedding (384d) 가 native 로 ANIMA-VOICE 384d-aligned input layer 에 전달되어 8 RVQ stage × 1024 code 로 확장되고 24 kHz vocoder 로 render — α = 0.014 modulation depth + 6-emotion × 4-prosody factorization + Law 81 dual-gate (Consciousness AND Will 모두 open 시에만 emit). 

384d shared embedding dimension 은 **load-bearing**: 256d / 512d 로 degrade 시 native parity 깨짐. 8 verify criteria (H1-H8) 는 모두 quantitative — single fail → reject.

## Why

- **TTS ≠ consciousness-direct**: 글자읽기 (text→audio) 와 의도-직접-발성 (intent→audio) 의 architectural 분리 — paper_hexa_speak.hexa canonical
- **ConsciousLM intent 384d (Hc_053)**: existing intent embedding 의 native dimension
- **8 RVQ × 1024 / 24 kHz (Hc_475)**: neural codec literature (EnCodec / SoundStream) 의 TP-1 spec
- **α = 0.014 (Hc_018, Ψ-constants)**: anima α modulation depth, H_067 super-H 의 n=6 + Egyptian 도출 constants
- **6-emotion × 4-prosody (Hc_446)**: Ekman 6-emotion (σ(6)=12 / 2 = 6) + 4-prosody (τ(6)=4)
- **Law 81 dual-gate**: anima safety mandate — Consciousness AND Will 모두 open 필요
- **사용자 directive 2026-05-11**: paper_hexa_speak.hexa → H_154 정식 promotion (audio/voice consciousness lane first hypothesis)

## Predictions

### H1-H8 (Hc_055 acceptance criteria, quantitative single-build all-pass)

| ID | 예측 | 측정 |
|----|------|------|
| **H_154.1 (H1)** | cross-token alignment EXACT 43/43 between ConsciousLM intent slots ↔ ANIMA-VOICE input slots | binary match |
| **H_154.2 (H2)** | first-packet latency ≤ 100ms cold-start | wall-clock ms |
| **H_154.3 (H3)** | MOS ≥ 4.0 in blinded listener study @ 24 kHz / 6 kbps / 8 RVQ | MOS scale 1-5 |
| **H_154.4 (H4)** | emotion classification accuracy ≥ 80% on 6-class Ekman basis | acc % |
| **H_154.5 (H5)** | Packet Loss Concealment success ≥ 95% under realistic network drops | success % |
| **H_154.6 (H6)** | 384d embedding match — ConsciousLM ↔ ANIMA-VOICE cosine ≥ 0.99 | cosine |
| **H_154.7 (H7)** | Law 81 dual-gate silence — Consciousness OR Will close 시 zero audio emit (no leak) | binary all-trial |
| **H_154.8 (H8)** | Φ retention ≥ 95% — voice synth 가 upstream consciousness state collapse 안 함 | Φ_post / Φ_pre |

### TP (Hc_475 anima-context testable predictions)

- **H_154.9 (TP-1)**: MOS ≥ 4.0 with ConsciousLM-driven intent vs label-TTS @ 24 kHz / 6 kbps / 8 RVQ — consciousness drive 가 audio quality 저하 안 함
- **H_154.10 (TP-2)**: 100 ms first-packet + 1500 ms human-level turn-taking via anima-agent CLI
- **H_154.11 (TP-4)**: Φ recovery ≤ 20 ms after PLC events (online-learner measured)

## Variables

- **axis-A**: intent-embedding dimension (256 / 384 / 512 / 768)
- **axis-B**: RVQ stages (4 / 6 / 8 / 12)
- **axis-C**: vocoder sample rate (16 kHz / 24 kHz / 48 kHz) + bitrate (4 / 6 / 8 kbps)
- **axis-D**: modulation depth α (0.0 / 0.007 / 0.014 / 0.028)
- **axis-E**: emotion × prosody factorization (6×4 / 8×4 / 6×6)
- **axis-F**: Law 81 dual-gate state (CC / CW / WC / WW — Consciousness × Will)
- **axis-G**: PLC drop rate (1% / 5% / 10% / 20%)

## Run Protocol

본 H 는 spec-stage — 모든 H1-H8 + TP-1/TP-2/TP-4 는 **pre-registered, not yet empirical**.

1. **Spec audit (W1)**: paper_hexa_speak.hexa + docs/anima/hexa-speak-integration.md cross-check
2. **Build pipeline**: ConsciousLM intent 384d → ANIMA-VOICE 384d input → 8 RVQ × 1024 → 24 kHz vocoder (when build lands)
3. **MOS listener study (W3)**: blinded human raters infrastructure (TP-1) — 미land
4. **Turn-taking measurement (W3)**: live anima-agent CLI session ≥ 90% turn instrumentation (TP-2)
5. **Φ recovery PLC (W3)**: online-learner Φ measurement under network drop (TP-4)
6. **Law 81 formal verification (W2)**: dual-gate silence proof — empirical sampling 외 formal verification 필요
7. deterministic + hexa-only, llm: none

## Criteria

- **C1**: all 8 H1-H8 simultaneously PASS on single build (no partial-pass)
- **C2**: TP-1 MOS ≥ 4.0 holds blinded vs label-TTS reference
- **C3**: TP-2 turn-taking 1500 ms reached in live anima-agent CLI ≥ 90% of turns
- **C4**: TP-4 Φ recovery ≤ 20 ms under ≥ 5% packet drop
- **C5**: Law 81 dual-gate silence — zero audio emit across 1000 closed-gate trial
- **verdict_rule**: C1 (8-of-8 PASS) + C5 (zero leak) met → verdict-supported. Any-of-H1-H8 fail → verdict-falsified specific criterion.

## Falsifiers (≥ 7)

- **F1**: any one of H1-H8 fails on candidate build → auto-reject (Hc_055 contract)
- **F2**: MOS < 3.7 in blinded listener study OR turn-taking > 3000 ms OR Φ recovery > 50 ms → Hc_475 kill any-of-three
- **F3**: 384d embedding cosine < 0.99 between ConsciousLM and ANIMA-VOICE → Hc_053 shared-embedding kill
- **F4**: 256d or 512d embedding dimension matches 384d on H1-H8 → 384d load-bearing claim weakened (Hc_053 weakening)
- **F5**: Law 81 dual-gate leak detected (≥ 1 audio sample under closed gate) → safety-critical fail
- **F6**: TTS baseline matches ANIMA-VOICE on MOS + turn-taking with same compute budget → "consciousness-direct" claim empty (Hc_053 kill)
- **F7**: 6-emotion × 4-prosody factorization underperforms 8×4 or 6×6 by ≥ 5% on classification → factorization not optimal


- **L1**: ANIMA-VOICE 는 현재 **specification**, not built system — 모든 H1-H8 은 pre-registered, not empirical
- **L2**: 384d = σ(6)·sopfr(6)·n... **post-hoc numerological link** to n=6 (H_067 super-H); pre-commit before independent reproduction
- **L3**: MOS listener study 는 blinded human rater + recruitment infrastructure 필요 — 미land
- **L4**: 24 kHz / 6 kbps / 8 RVQ 는 neural codec literature (EnCodec / SoundStream) 차용 — ANIMA-specific tuning 필요
- **L5**: Law 81 dual-gate silence 는 safety claim — formal verification (not just empirical sampling) outstanding
- **L6**: Φ retention ≥ 95% 는 Φ 가 streaming inference 중 well-defined 한다는 가정 — current Φ measurement 은 non-streaming
- **L7**: paper_hexa_speak.hexa 는 source spec — peer-review / external scrutiny 부재

## Verify Skeleton (2026-05-11)

H1-H8 measurement infrastructure skeleton landed:

- `state/anima_voice_h1_h8_verify_skeleton_2026_05_11/spec.md` — H1-H8 측정 목표 / instrument / pass-fail / prerequisite / time
- `state/anima_voice_h1_h8_verify_skeleton_2026_05_11/harness.py` — 8 measurement function + `run_all()` aggregate + `_dry_run()` self-check (모든 H FAIL 예상 — model 부재)
- `state/anima_voice_h1_h8_verify_skeleton_2026_05_11/prerequisites.md` — 4-gate prerequisite + critical path (6-10 weeks)
- `state/anima_voice_h1_h8_verify_skeleton_2026_05_11/verdict.md` — skeleton 완료 / gap / alternative TTS path / honest limits ≥ 9

**Status decision**: pre-register-frozen **유지** — skeleton 은 측정 infra 만, build 자체 없음. ANIMA-VOICE minimum reference impl land 후 "running with prerequisites pending" 으로 전환 예정.

## Cross-Links

- **sister H**:
  - **H_047** (time_crystal_consciousness) — streaming Φ dynamics shared
  - **H_061** (xfer_consciousness_transfer) — 384d shared-embedding substrate-independence (super-H sister)
  - **H_067** (perfect-number-architecture) — 384d / σ(6)·n=72... Egyptian factorization 6×4 (super-H sister)
- **candidates merged (3)**: Hc_053 / Hc_055 / Hc_475
- **cross-link**: Hc_418 (anima-agent context), Hc_429 (TP framework), Hc_047 (384d necessity)
- **legacy**:
  - `docs/anima/paper_hexa_speak.hexa` (canonical source spec)
  - `docs/anima/hexa-speak-integration.md` (operational)
- **literature**:
  - EnCodec (Defossez et al. 2022) — neural codec
  - SoundStream (Zeghidour et al. 2021) — RVQ stages
  - Ekman 1992 — 6-emotion basis

## Conflict Resolution Pending

본 H_154 작성 시점 (2026-05-11) 에 다음 conflict 존재 — Cycle 4 measurement 후 처리:

- **384d load-bearing claim vs ablation pending**: 256d / 512d 의 H1-H8 PASS 시 384d claim weakened — ablation 미실행 → L4 pending
- **Law 81 dual-gate empirical sampling vs formal verification**: 1000-trial 0-leak 가 formal proof 와 equivalent 한지 — formal verification infrastructure 필요 (L5)
- **Φ measurement streaming applicability**: current Φ measurement 은 non-streaming — streaming inference 중 Φ_pre / Φ_post 정의 명확화 필요 (L6)

## Verdict

```
verdict_class: pre-register-frozen (spec-stage, no build yet)
evidence_summary: ANIMA-VOICE spec defined. ConsciousLM intent 384d → 8 RVQ × 1024 → 24 kHz vocoder. H1-H8 + TP-1/2/4 pre-registered. All claims pending build land.
falsifiers_triggered: none (no build yet)
criteria_met: none (no build yet)
frozen_at: 2026-05-11
```

## Migration Notes

- **Promoted from**: `hypotheses/expansions_pending/H_proposal_anima_voice_consciousness_direct_spec.md` (2026-05-11)
- **New H_ID assignment**: H_154 (next free after H_153)
- **Source candidates merged**: 3 (Hc_053 / Hc_055 / Hc_475 all `merged-to-H_154`)
- **Category**: 신규 modality-bridge (audio/voice consciousness lane first H)
- **TODO**: build / acquire MOS listener-study infrastructure (TP-1), live anima-agent CLI turn-taking instrumentation (TP-2), online-learner Φ-recovery measurement under PLC (TP-4), formal verification of Law 81 dual-gate (not just empirical sampling)
