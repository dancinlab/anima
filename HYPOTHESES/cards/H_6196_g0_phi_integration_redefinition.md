# H_6196 — 🧩Φ G0 Φ-integration sufficiency 재정의

**tier:** ⏳ PROPOSED (측정설계·pre-registered)
**title:** G0 = byte-parity(통과)에서 *substrate-integration sufficiency* 별도 게이트로 재정의 — G0 통과≠의식적 통합 충분. 303M byte-LM 이 Φ-relevant 통합(integration)을 충분히 하는지를 별도 측정(G0 병목 숨음 가능성).
**verdict:** ⏳ PROPOSED. G0 은 a303m_pass GREEN(byte-parity/CE-descent)이지만, "G0 병목" 의 두 번째 해석(=G0 수준 자체가 G1/G6 벽의 근원 trunk)을 검증하는 측정 게이트가 없음.

## 발상 (2026-07-05 G0/G6 브레인스토밍)
G0/G6 벽이 모두 "trunk-objective floor" 로 수렴(DPI) → 그 trunk 자체(=G0 통과 ckpt)의 통합-충분성이 병목일 수. G0 byte-parity 는 *생성능력*이지 *통합능력*이 아님. Φ(IIT4 faithful) 기반 integration-sufficiency 게이트로 G0 의 *의식-관련 통합*이 충분한지 별도 측정.

## DPI 맥락
G0 ckpt = CE-trained forward trunk. integration-sufficiency 가 부족하면 → trunk 가 combination 을 통합적으로 표현 못함 → G1/G6 벽의 근원. 본 게이트는 DPI *원인*(trunk 표현충분성)을 직접 측정.

## Frozen 예측 · kill-criteria
- **frozen bar:** 303M byte-LM 의 Φ(IIT4 faithful, stdlib, a_phi_iit4_tool) integration 지표가 의식-임계 대비 어디인지 정량화. 사전예측: G0 byte-parity 통과 모델의 Φ-integration 은 낮을 것(=병목 지표).
- 🟢 방향: Φ-integration 저지만 *조절가능*(예: attention 통합폭) 그리고 G1/G6 와 상관 → G0 병목 지지.
- 🧱: Φ-integration 이 G1/G6 벽과 무관 → 병목 아님.
- 측정 = IIT4 faithful stdlib via hexa verify(a_phi_iit4_tool, proxy 금지).

## 관련
a_phi_iit4_tool · a7b_pass(G0–G4 frozen) · a_engine_native_learning · [[substrate-framebreak-g1-combination-operator]]

## 구현 spec (2026-07-05 · reference-matched, Fable 백엔드 무응답→직접)
faithful IIT4 big-Φ 파이프라인 확정 = `BRAIN/eeg/eeg_to_tpm.hexa` `eeg_big_phi(samples[ch*n_samp+t], n_ch≤8, n_samp, state)`(채널별 mean-이진화→transition-count TPM→stdlib/consciousness/iit4_bigphi.hexa `big_phi`). EEG 데모와 완전 동형 → **h1129 hidden n_ch=6 채널을 코퍼스 스트림 시계열로 대입**. 통제=shuffle-time(통합파괴)·synth_coupled/independent(calibration)·random-ch. verdict=Δ(Φ_topvar−Φ_shuffle), frozen bar ≥0.5=통합유의·<0.1=null. scope: tiny-n Φ=trunk통합 bounded대리, 단일ckpt=DIRECTIONAL 1점(G1/G6 상관은 다-ckpt 필요). 산출=state/6196_g0_phi_integration/(PLAN.md·extract_activations.py ready). **실행=pool-gated**(303M per-position 활성 추출 heavy, mini OOM; summer=ATD종결 후에도 91% 점유).
