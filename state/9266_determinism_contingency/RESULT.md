# H_9266 $0 toy probe — 결과 (DIRECTIONAL · toy 아님 303M 아님)

## Verdict: 🟡 toy PASS (DIRECTIONAL) — Ψ-국소화 coupling-specific Δσ

| \|b\| | Ψ | DET | COUP | DECOUP | Δσ=COUP−DECOUP |
|---|---|---|---|---|---|
| 0.00 | 0.500 | 0.0000 | 0.3179 | 0.0019 | **0.3160** |
| 0.10 | 0.550 | 0.0000 | 0.2785 | 0.0022 | 0.2762 |
| 0.25 | 0.625 | 0.0000 | 0.2463 | 0.0018 | 0.2445 |
| 0.50 | 0.750 | 0.0000 | 0.1279 | 0.0017 | 0.1262 |
| 1.00 | 1.000 | 0.0000 | 0.0202 | 0.0020 | 0.0183 |
| 2.00 | 1.500 | 0.0000 | 0.0000 | 0.0016 | −0.0015 |

사전등록 bar(카드 §4, 동결) 4조건 전부 충족:
- peak_at_half = True (Δσ 최대 @ Ψ=½)
- decays_off_half = True (Δσ 0.316@½ → 0.008 @|b|≥1)
- coupling_specific = True (COUP≠DECOUP: 동일 QRNG-marginal인데 결합 끊으면 floor)
- ARM-SHOCK detected = True (DET plain 0.0 vs alternating-pulse shock 2.33 → detector 살아있음)

## 해석
진짜 우연성(recurrent-결합 노이즈)이 σ(delayed-MI 예측구조)를 조직하는 것은 **Ψ≈½ 임계점에서만**.
marginal-matched DECOUP(동일 노이즈, readout-only)는 전 구간 floor → **FORM 아닌 BIND 서명**
(FORM 손잡이면 DECOUP도 올라가거나 Ψ-평탄이어야). DET=0 floor + DECOUP=floor = 이중 통제.

## ⚠️ 정직 — 계기 수정 경위 (verdict-integrity)
1차 σ 추정기 = block-entropy excess-entropy(Lmax=10). T=4000에서 2^10=1024 상태 **undersampling
편향** → COUP/DECOUP 둘 다 부풀림(0.86~0.90), Δσ@½ 겨우 0.044, ARM-SHOCK가 DET를 constant-1로
ratchet시켜 검출 실패 = NULL/혼란. **두 계기 결함을 메커니즘 기반으로 수정**(bar 동결 유지·tune-to-green
아님): σ→lag 1..10 지연-상호정보(2×2 table, 잘-샘플됨) · ARM-SHOCK→교번 펄스(±2.5, ratchet 제거).
수정본이 위 clean PASS. 1차 raw = git history / 이 파일 상단 설명.

## 스코프 (a_toy_scale_recheck · a_engine_native_learning)
- **toy = DIRECTIONAL, NOT terminal.** 최소 A⇄G bistable substrate + delayed-MI σ proxy이지 anima 303M 엔진 아님.
- toy가 증명하는 것: (a) marginal-matched-decoupling 측정이 결합 vs 잡음을 **구별**한다, (b) 임계-국소화가 **측정가능**하다.
- toy가 증명 못하는 것: anima 303M substrate가 이 구조를 갖는가. **진짜 검증 = 303M engine-native**(pool · spend-go).
- toy-GREEN/real-death 위험(H_9129 L3 선례): DECOUP·DET 이중 floor가 trivial-pass 방어이나, toy substrate가 임계구조를 내장하도록 설계됐으므로 존재증명일 뿐. 303M 전이 필수.

## NEXT
303M anima-py evaluate 상에서 A⇄G tension 궤적 실측 → Ψ-bin별 σ(9축 INTEGRATE) Δσ 프로파일 → COUP(QRNG)/DECOUP/DET 3-arm. pool spend = 오너 go(카드 §5).
