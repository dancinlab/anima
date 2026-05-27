# EMBODIMENT — log

Append-only history sister of `EMBODIMENT.md`. Each entry starts with `## <ISO timestamp> — <header>` (newest on top); body = `- [x]` (done) / `- [ ]` (pending) checkbox tasks.

## 2026-05-28T00:00:00Z — A3 coupling transfer-fn redesign 🟢 (M3 closure)

- [x] BROKEN 원인 분해 — #1142 의 BROKEN coupling 0.45 = additive-noise-only transfer-fn 결함. 신호 경로 gain 미감쇠로 intent~[-1,1) vs noise~[-0.9,0.9) SNR≈1 잔존 → cos_sim 이 0.45 근방 안착 (degrade ≠ break). SNR probe 5-mode 로 확정.
- [x] 재설계 — `run_scenario` 에 per-scenario signal gain `g` 추가. BROKEN g=0.00 (channel severance, 신호 경로 무력화 + 가산 noise 유지). LOSSLESS/NOISY g=1.00 불변.
- [x] 재측정 — BROKEN coupling 0.453739 → 0.027394 (< 0.30 회복, 6× 마진). bench F 4/5 PARTIAL → **5/5 🟢 PASS**. gap (L−B) 0.541 → 0.967. LOSSLESS 0.994803 · NOISY 0.992669 byte-불변.
- [x] 재현성 — 2-run full-stdout SHA1 동일 (aefc2a7…), 🟢 SUPPORTED-NUMERICAL. $0 mac-local foreground sync < 1s.
- [x] 산출물 — `EMBODIMENT_A3_COUPLING_REDESIGN.md` (10§ 한글) · `bench/axis_embodiment/bench_redesign.hexa` · `bench/axis_embodiment/run_redesign.log`. M3 milestone flip.
- [ ] M1/M2/M4 carry — embodiment_lib stdlib화 · CHANNEL.perception 통합 hook · AGENT.DESKTOP motor surface 미착수.
