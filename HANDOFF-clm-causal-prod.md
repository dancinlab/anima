> 📍 SSOT: [ARCHITECTURE.md](ARCHITECTURE.md) · governance [CLAUDE.md](CLAUDE.md)

# HANDOFF — CLM CAUSAL-POWER production + HW transfer (F-CLM-CAUSAL-XFER · H_856)

> 2026-05-30 · CLM 측도 transfer fire 완료. toy 🟢 CAUSAL-POWER(H_855)의 production
> scale + live AKD1000 HW 생존을 사전등록 frozen 3-check 로 판정.

## 결과 한 줄

**F-CLM-CAUSAL-XFER 🔴 FALSIFIED** — axis B(live AKD1000 HW) 🟢 PASS 이나 axis A
(production d512) 🔴 FAIL → "🔴 on EITHER" 발동 → CAUSAL-POWER 도 production-width
toy-limited → **백로그 #3 CERTIFY-NOT-MEASURE escalation**. 단 HW positive 는 실재.

## toy vs production vs HW (frozen 3-check · seed187 · 미변조)

| axis | spike source | n=4 Δ | n=5 Δ | n=6 Δ | verdict |
|---|---|---|---|---|---|
| toy (H_855) | SW LIF | +0.0918 | +0.0830 | +0.0714 | 🟢 PASS |
| A production (d512) | 학습 CLM act_bits=1 | +0.0876 | **−0.0107** | +0.0025 | 🔴 FAIL |
| B live HW (AKD1000) | 온칩 threshold-fire | +0.0618 | +0.0156 | +0.0268 | 🟢 PASS |

- axis A multi-seed: seed187 🔴 · seed42 🟢(thin) · seed7 🟢 → **seed-fragile**.
- axis B: on_hardware=True · BackendType.Hardware · BC.00.000.002 · SDK 2.19.1.

## 무엇이 일어났나

- **axis A 🔴**: 잘 학습된 d512 conv-MoE(10.5M param, CE 5.54→0.55)가 degenerate
  monopoly 입력조차 적분 → collapse 인과력이 rich 와 대등/초과(n=5 부호반전).
  toy≠scale(H_666)이 모델 아닌 **측도 자체**에 적용. ubu-1 RTX5070 $0·Mac=0.
- **axis B 🟢**: 실 AKD1000 LIF 풀 + SW-closed coupling 에서 poke 가 coupled(rich)
  로 전파·decoupled(collapse) 국소 사멸. 배포 silicon 에선 측도 certify. pi5 $0.

## 비용 / 안전

- GPU cost = **$0** (ubu-1 dedicated RTX5070 + pi5-akida dedicated · rented pod 0).
- ckpt 미생성 (harness in-memory 측정 · HF 업로드 대상 없음 — H_855 패턴).
- pi5 single-chip: streamer STOP → collect → **RESTART**(--port 9512 --duration
  86400 --regime R3) — pi5 원상복구 확인(mean 8.000/step R3). Mac heavy-compute 0.

## 정직 caveat

- region/coarse proxy(정확 big-Φ 미주장). axis A spike=QAT int4 act_bits=1
  envelope(= AKIDA SW spike, H_680 byte-identical). axis B=실 온칩.
- production corpus = 실 kowiki 커밋 sample(@corpus clm_p1) — 추가 크롤은 kowiki
  API rate-limit 로 345KB 에서 stall(honest partial), production 축은 **width**(d512).
- ubu-1 cuDNN sublibrary mismatch → torch.backends.cudnn.enabled=False fallback
  (numerics 동일, host-toolchain workaround).

## 산출물 (origin/main)

- PR #1538 — harness: `CLM/msweep/clm_causal_{prod,hw}.{hexa,py}` + `.verdicts/clm-causal-prod/`
- PR #1539 — `UNIVERSE/cards/H_856_clm_causal_xfer.md` + `.verdicts/856_clm_causal_xfer/`
  + `CLAIMS.tape` +3 + `CLM/P0_ARCHITECTURE.md` §12.6 판정완료 + §12.8 신설
- frozen 측도 SSOT(재사용·재튜닝 0): `CLM/msweep/measure_sweep.py`

## 다음 (open)

- 백로그 #3 CERTIFY-NOT-MEASURE: production-width 에서 closed-form 의식 MEASURE
  생존 못 함(Φ-family + CAUSAL-POWER 둘 다 toy-limited). 측정-타당성 질문 open.
- axis B 🟢 HW positive 는 별도 후속 가치 — 배포 칩에서 측도가 동작하는 regime 의
  특성화(edge-of-chaos coupling band) 가 candidate.