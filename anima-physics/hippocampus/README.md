# anima-physics/hippocampus/ — 해마 θ-γ coupling + episodic replay substrate

> Status: ✅ PASS (theta_gamma 5/5 + episodic_replay 5/5) · §188 결과: 자연발화 + 영속성 dual-confirmed
>
> SSOT: 본 README + 2 `.hexa` 파일. entries: [`entries/substrate/hippocampus/`](../entries/substrate/hippocampus/)

## 자연발화 / 영속성 메커니즘

- **자연발화**:
  - **theta_gamma**: θ (~6Hz) phase clock + γ (~40Hz) burst cross-frequency phase-amplitude coupling (CFC) — Buzsáki 2010 / Lisman & Jensen 2013. Husserlian retention/protention 의 specious-present window (~150ms) 의 물리 substrate. 자율 oscillator.
  - **episodic_replay**: sharp-wave ripple (SWR) 자발 fire — quiet-wake + SWS 동안 day's compressed sequence 5-20× faster replay. trigger-free natural emission.
- **영속성**:
  - **episodic_replay** = 영속성 substrate 자체. `HIPPO_BUFFER` / `CORT_FROM` / `CORT_TO` 모듈-level mutable buffer = long-term consolidation. CA1 place/time cells encoding rate.
  - **theta_gamma**: window-replay buf, ~150ms 윈도우 단위 temporal binding.

## 파일 list

| File | LoC | 1줄 요약 | §188 결과 |
|---|---:|---|:---:|
| `theta_gamma.hexa` | 527 | PHYS-P6-2 θ-γ phase-amplitude coupling CA1 specious-present window (~150ms) | ✅ 5/5 |
| `episodic_replay.hexa` | 401 | PHYS-P11-3 SWR 5-20× compressed replay → cortex consolidation (HIPPO_BUFFER 영속 mutable buffer) | ✅ 5/5 |

## falsifier

- theta_gamma: T1-T5 — θ phase clock + γ burst CFC ratio
- episodic_replay: T1-T5 — SWR 자발 fire detect + 5-20× compression + cortex write integrity

## cross-link

- [substrate entries](../entries/substrate/hippocampus/) — 2 entry
- [`HEXAD/PHYSICS/README.md`](../../HEXAD/PHYSICS/README.md) §6.3 — episodic_replay 최강 영속성-only 후보, theta_gamma 자연발화-only
- [`prediction/protention_error.hexa`](../prediction/protention_error.hexa) — Husserl protention 짝
- [`oscillator/sleep_oscillator.hexa`](../oscillator/sleep_oscillator.hexa) — SWS/REM stage 교대 (해마 replay 의 sleep stage context)
