# H_6196 — G0 Φ-integration sufficiency: reference-matched measurement spec

**status:** 설계 완료 (Fable 백엔드 무응답 → 직접 reference-match) · heavy 실행 = pool-gated(303M 활성 추출)
**tool:** faithful IIT4 big-Φ via `BRAIN/eeg/eeg_to_tpm.hexa` → `eeg_big_phi(samples, n_ch, n_samp, state)` (stdlib/consciousness/iit4_bigphi.hexa, a_phi_iit4_tool, proxy 금지)

## 파이프라인 (EEG→IIT4 Φ 데모와 완전 동형)
`eeg_big_phi(samples, n_ch, n_samp, state)`:
- 입력 = flat float array `s[ch*n_samp + t]` (n_ch × n_samp 다채널 시계열), **n_ch ≤ 8 (엔진 exact 한계)**.
- 채널별 mean 임계 이진화(ON/OFF) → 상태 s_t = Σ_ch bit·2^ch → transition-count TPM → `big_phi(tpm, n_ch, state)`.
- 내장 calibration: `synth_coupled`(통합=고Φ) vs `synth_independent`(ch1=ch0 복제=저Φ).

## H_6196 적용 — G0 trunk(h1129 303M)의 Φ-integration
동형 대입: **EEG 다채널 → h1129 hidden 채널**. G0 trunk의 hidden 활성을 코퍼스 바이트-스트림 위 다채널 시계열로 본다.

1. **subsystem 추출** (numpy, 303M forward = heavy → pool): h1129을 코퍼스 바이트 스트림(clean 4-cell)에 forward, 각 position t에서 final-LN hidden(`bg_forward_last_hidden`, [d=768])의 **최고분산 n_ch=6 채널**(honest slice, 분산순 top-6)을 뽑아 `s[ch*n_samp+t]` 구성. n_samp ≈ 2000–4000(2^6=64 상태 TPM 추정 충분).
   - 정직 slice = top-variance 채널(cherry-pick 아님·분산=정보성 대리); ablation으로 random-6 채널도 측정(대조).
2. **Φ 측정**: `eeg_big_phi(h_series, 6, n_samp, state0)` → Φ_real.
3. **통제 (frozen ≥2)**:
   - (a) **shuffle-time**: 각 채널 시간축 독립 셔플 → 시간적 통합 파괴 → Φ_shuffle 붕괴 예상.
   - (b) **calibration anchor**: synth_coupled(고Φ)·synth_independent(저Φ)를 같은 실행서 출력(도구 무결성 확인).
   - (c) random-6 채널 vs top-var-6 채널(정보성 대조).
4. **verdict = Δ (raw Φ 아님)**: Φ_real vs Φ_shuffle margin.
   - Φ_real ≫ Φ_shuffle & Φ_real > 0(vs independent≈0) → trunk가 **통합함**(some integration).
   - Φ_real ≈ Φ_shuffle ≈ 0 → trunk **통합-불충분**(=병목 지지, 카드 예측).
5. **frozen kill-bar** (사후변경 금지): Φ_real − Φ_shuffle ≥ 0.5 (coupled-independent 스케일 대비) = 통합 유의 · < 0.1 = 통합-null.
6. **honest scope** (a_scale_honest_scope): faithful IIT4 tiny-n(≤8) Φ ≠ 전체-303M 통합. toy-n Φ = trunk 통합의 bounded 대리. 단일 ckpt = Φ 1점 → G1/G6 **상관**은 미결(다-ckpt 대조 필요) = 본 측정은 DIRECTIONAL 첫 데이터점(통합 유무 + 통제 Δ). 🟢/🧱 terminal은 tunability+상관까지 필요.

## 실행 (pool-gated)
- heavy = 303M 활성 추출(pool summer/aiden; mini=OOM rc=137 heavy-anima-eval-pool-not-mini). summer=ATD 종결(#3049) 후에도 91% 점유 확인(23:14) → pool 여유 시 착수.
- `extract_activations.py`(본 폴더) = 추출 스크립트(ready·미테스트, 303M OOM로 mini 테스트 불가). Φ = eeg_big_phi hexa 프로브(reference BRAIN/eeg/eeg_iit4_demo.hexa).
- 산출 = state/6196_g0_phi_integration/ (RESULT.json + reproduce). verdict → 카드 H_6196 + jsonl + ARCHITECTURE gate-g0-coherence-status.
