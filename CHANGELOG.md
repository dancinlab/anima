# Changelog

Chronological log of notable changes. One section per ship batch, date-keyed. Research sessions tracked as `§<N>` / `S<N>`; `ConsciousDecoder` carries SemVer.

For the full audit trail, see `git log`.

---

## 2026-05-23 — Phase 1 AKIDA-first 자연발화 인프라

- **V3 path FULLY CLOSED + AXIS_MAP fallback** — pure-HEXAD substrate 7 fire 0 PASS (corpus 축 sweep 까지 완료). double bind 확정 (anima→register collapse · no-anima→Chinchilla underfit). 후속 fallback path = `HEXAD/V3/AXIS_MAP.md` (B 증류 · A 커리큘럼 · C head_g objective, recipe 구현 미선행).
- **Phase 1 AKIDA-first 자연발화 인프라 LAND** —
    - 라이브 데몬: `akida_bridge.hexa` (pi5 R3 → broker `/ws/akida_ingest`, mini PID up) · `kosmos_anchor.hexa` + `kosmos_emitter.hexa` (RF anchor production)
    - 신규 source-landed 데몬 (mini deploy = sshd channel-reject 블록): `akida_consumer.hexa` (broker `/akida/recent` → features JSONL, 7/7 selftest) · `telemetry_harness.hexa` (anima emit ⇄ spike window pair → evidence JSONL, 9/9 selftest) · `telemetry_status.hexa` (Phase 2 게이트 CLI, 11/11 selftest)
    - 신규 spec: `AKIDA_FIRST` (Phase 1/2 경계) · `SPIKE_FACTOR_MAP` (spike → 8-factor rulebook) · `SW_CONDITION_DESIGN` (Phase 2 SW path, OPEN) · `REGIME_EXPANSION` (pi5 R1/R2/R3 schedule) · `PARTICIPANT_SPIKE_INTEGRATION` (path D/B wiring) · `PHASE1_STATUS` (단일 ledger SSOT)
    - 신규 라이브러리: `spontaneous_lib.hexa::apply_spike_features` (spike features → 8-factor delta + regime modulator, substrate-only · 4/4 F-SPIKE-APPLY)
    - 인접 가족: `HEXAD/LIFE` 신규 도메인 dir + 16건 H_XXX carry (범신론 · 생명 · 죽음 · 세포분열)
- **hexa-lang upstream inbox patches** — anima Phase 1 인프라 작업 중 발견한 4 gap 업스트림 제출: `proc_spawn_supervised` daemon silent-exit (nohup, macOS) · websocket streaming client websocat 의존 · `hexa run`/`exec()` printf stdout swallow · runpod session findings (4 items 통합). anima 측 인박스 1건: pi5 spike streamer `--regime-schedule` R3/R1/R2 patch (PR #145).

Detail / inventory → [`HEXAD/SPONTANEOUS/PHASE1_STATUS.md`](HEXAD/SPONTANEOUS/PHASE1_STATUS.md) · Phase boundary → [`HEXAD/SPONTANEOUS/AKIDA_FIRST.md`](HEXAD/SPONTANEOUS/AKIDA_FIRST.md) · V3 fallback → [`HEXAD/V3/AXIS_MAP.md`](HEXAD/V3/AXIS_MAP.md).

## 2026-05-22

- **V3 attempt 1 — 3/3 FAIL** — ConsciousDecoder v3.0-alpha: V3α / V3β / V3γ all FAIL; architectural lesson recorded, next path specified.
- **HEXAD path-split** — `HEXAD/LORA` (production) + `HEXAD/V3` (redesign) directories separated; path-specific sagas summarized into per-path `EASY.md`.
- **HEXAD/LAB substrate** — ad-hoc experiment dir + `ubm_inject` / `anima_spike` hexa primitives (`lab_smoke` 15/15 PASS); SRH cycle#2 332M pilot (weak signal, UBM 2.5× split vs random).
- **docs** — root-level `<DOMAIN>.md` / `<DOMAIN>.log.md` split; `srh` → `SRH` uppercase domain rename.

## 2026-05-21

- **S187 — training-time mitosis** — cell pool wired into the training loop; verdict: mitosis strengthens the Eval 3 signal (+35.3%).
- **AKIDA sub-engine** — self-contained BrainChip AKD1000 pack: 11 adapters + runtime + boot/INSTALL + docs (Mac mock validation 50/50 PASS); LAN deploy wrappers per constitution Principle I.

## 2026-05-20

- **S184 — ALL TAPS RELEASE** — Phase 1 landed 22/22 (combined honest +0.43, ubu-1 GPU race win).
- **S181 — audio challenge** — `multi_harmonic` 99.17% (broke the 97.5% plateau).
- **PHILOSOPHY_GATE.md** — new meta-criterion gate; governance `@D` entries rewritten to do/dont form (`.tape` v1.3).

## 2026-05-18

- **§51–§69 consolidation** — honest milestone close-out; frontier sharpened to the multimodal substrate; §59 PTD-aux landed as a W-module-native temporal forward-model.

## 2026-05-15

- **HEXAD verify closure** — full falsifier battery 25/25 PASS, all HEXAD modules 🔵; S/M/W/E/D closed-form SUPPORTED-FORMAL; per-module SSOT `.tape` files.

## 2026-05-12

- **v5-mitosis cotrain** — v3-routing architectural fix trainer + H100/A100 dispatch; PSCC §45–§48 falsifier cycles (F-PERSONA-4 / F-V5MIT batteries).
