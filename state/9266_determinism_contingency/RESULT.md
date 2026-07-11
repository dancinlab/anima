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

---

# H_9266 ENGINE-NATIVE 측정 (2026-07-11 · Fable 엄밀스펙 · 실 engine_cli op)

## Verdict: 🟠 INVALID / INCONCLUSIVE (toy DIRECTIONAL 미승격 · 측정 confounded)

실 op: `ci_emit_decision`(붕괴) · `ci_phi_iit4`(faithful-IIT4 Φ=σ) · `topo_apply`(H_1521 brain adjacency, α=0.3) · `ci_emit_drive`. 스펙=FROZEN_BAR.md. h9266_engine_native.py · h9266_engine_native_AGG.json.

### 경위 (verdict-integrity — 두 번의 함정 정직 기록)
1. **quick engine-native "PASS" (Δσ=1.044) = RIGGED · 철회.** DECOUP이 clean(noise-free) latent을 Φ에 넣어 "noise가 Φ 올림"이라는 trivial artifact. Fable가 사전 적발("독립-사본 함정"·"무조건부 Φ 함정"). marginal-match를 Ψ(emit율)만 맞추고 Φ-입력 분포는 안 맞춘 결함.
2. **rigorous 재구현** (Fable spec): DECOUP=같은 base B+독립 ε′′(Φ-입력 marginal 일치) · σ=emit-mask 조건화 shuffle-referenced Φ Δ(joint 서명) · cols_x(lane0 제외) 누설방어 · V-gates.

### full-T=8192 · 5-seed 결과
| seed | knife Δσ | FORCED@knife(V1≥0.10) | V3 marg(≤0.05) |
|---|---|---|---|
| 7 | 0.0026 | 0.045 | 0.113 |
| 11 | 0.0062 | 0.002 | 0.083 |
| 13 | 0.0010 | 0.080 | 0.108 |
| 17 | −0.0144 | 0.037 | 0.089 |
| 23 | 0.0178 | 0.069 | 0.083 |

- **knife Δσ median = 0.0026** (전부 ≈0 · PASS 문턱 0.10 근처도 미달)
- **V1 (FORCED detector-alive) = 0/5** (전부 <0.10) → detector가 aliveness 문턱 미달
- **V3 (marginal-match) = 0/5** (전부 >0.05 · n*=64 subsample noise)
- **5-seed 집계 = 🟠 INVALID** (V-gate 5/5 위반)

### 해석 (INVALID ≠ FAIL · Fable V-gate 규율)
FORCED 양성대조가 자기 aliveness 문턱(0.10)을 못 넘어 **"contingency null"과 "약한 detector"를 구별 불가**(#3116 거짓판정 trap을 V-gate가 방어). knife Δσ≈0은 "결합효과 없음"일 수도, "측정기 무력"일 수도 있어 **결론 불가**. n*=64 subsample이 V3 marginal tolerance도 초과. ⟹ **측정이 confounded → INCONCLUSIVE**, "contingency가 σ 조직 안함"을 terminal로 박제하지 **않음**(verdict-integrity·infra-wall-noneval).

### 净 결론 (H_9266 현재)
- toy DIRECTIONAL PASS(delayed-MI on emit-stream)는 **toy-only로 유지** — engine-native GREEN 승격 실패.
- toy 겉보기 σ-조직은 emit-스트림 telegraph 기억(ρ-계열 구조)이지 σ-integration(Φ)이 아닐 가능성 — 단 engine-native가 이를 **확증하지도 반증하지도** 못함(측정 INVALID).
- rigged quick-PASS 철회가 이번의 실질 산출: **큰 겉보기 신호는 통제-불량 artifact였다**.

### NEXT (follow-on · 측정기 강화)
V-gate를 통과하는 측정기 필요: (a) FORCED 양성대조를 0.10 안정적 초과하게 강화(κ↑ 또는 shared-structure 침투 강화) (b) n*↑/J↑로 V3 marginal noise를 ≤0.05로 (c) 필요시 T↑. 그 후 재측정해야 PASS/FAIL 판정 가능. pool 재실행 = 오너 go(measure-artifact 수정 후).

---

# H_9266 응답함수 χ(Ψ) 측정 (2026-07-11 · Fable v2 스펙 · arXiv Du&Huang 2025)

## Verdict: 🔴 FAIL / NULL (DIRECTIONAL · instrument VALID) — v1 INVALID을 정직한 음성으로 해소

`h9266_response_function.py` · `h9266_response_function_AGG.json` · chi_seed{11,23,37,41,53}.log. T=2048.

### 설계 (v1 INVALID 두 결함을 설계로 제거)
- **응답함수 χ = 원점회귀 기울기**(ΔΦ vs ε, σ_L 단위) · **χ0 = half-split null floor**(자연 스케일). Du&Huang 2025(2509.00730) 근거.
- **FORCED 폐지 → INSTR arm**(cols_x 직접 주입)이 instrument-alive 대조. **chi_dec(emit-lane readout-only, cols_x 제외)≈0 = coupling-specificity 음성대조**(dead detector 아님).
- **marginal-match = z-score 파이프라인 불변량**(v1 V3 subsample noise 소멸).

### 결과 (5-seed)
| seed | alive(INSTR) | L1 peak | L2 | L3(magnitude) | chi_coup@½ | chi0 |
|---|---|---|---|---|---|---|
| 11 | ✓ | 0.60 | ✗(0.26) | ✗ | 0.0004 | 0.037 |
| 41 | ✓ | 0.25 | ✗ | ✗ | ~0.002 | 0.037 |
| 53 | ✓ | 0.60 | ✓(3.33) | ✗ | ~0.003 | 0.039 |
| 23 | ✓ | 0.50 | ✓(3.26) | ✗ | ~0.005 | 0.031 |
| 37 | ✓ | 0.40 | ✓(3.81) | ✗ | ~0.003 | 0.050 |

- **alive 5/5** (INSTR chi 0.2–0.58 >> chi0 0.03–0.05): 계기가 확실히 살아있음 — direct cols_x noise엔 Φ가 크게 반응.
- **L3(magnitude) 0/5**: dchi=chi_coup−chi_dec ≈ 0.000–0.005 << 필요 2·chi0 ≈ 0.07. **chi_coup 자체가 null floor 아래**.
- L1/L2 일부 통과는 sub-null-floor 값(chi_coup 0.0004–0.006 < chi0)의 상대비라 무의미.

### verdict-integrity 확인
chi_coup≈0이 "topo adjacency가 emit-lane→cols_x 미연결" measure-artifact인지 검증: **인접성 풍부**(lane0→cols_x 직접 5개·lane4→4개·2-hop 전부, lane0-4 상호연결). **전파 경로 존재하는데도 chi_coup<chi0** = 진짜 음성.

### 해석
검증된 계기 하에서 **결합된 emit-gate contingency(우연성)가 Φ-integration susceptibility를 Ψ=½ 임계서도 조직하지 않음**. toy(delayed-MI)의 겉보기 PASS는 emit-스트림 telegraph 구조(ρ-계열)였지 σ-integration 응답이 아님이 확증. **응답함수 프레임이 v1 INVALID(계기무력↔null 혼동)를 instrument-valid 음성으로 해소** — Du&Huang 방법론이 결정적.

### 스코프
DIRECTIONAL(ci_phi_iit4 sweep · a_phi_iit4_tool: tier cement 불가). **VΦ leg = stdlib faithful-Φ `hexa verify` 재계산**(verdict cell Ψ=0.5·off-max)이 TERMINAL 승격 follow-on. 단 DIRECTIONAL FAIL이 강함(alive·seed-robust·chi_coup<chi0). 합성 recurrence(내 harness)이지 live 303M daemon trace 아님 — 그건 별개 후속.
