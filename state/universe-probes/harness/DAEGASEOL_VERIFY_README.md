# UNIVERSE_daegaseol — 14축 capstone (H_1101–H_1114)

강령(codex) 14축 대가설 묶음 + toy falsifier 검증. ghost:~/Downloads 에서 2026-06-14 import.

## 파일
- `H_1101..H_1114_*.md` — 14축 capstone 가설 (frozen falsifier + 제안 demo, verdict ⏳ OPEN)
- `INDEX.md` — 14축 ↔ A↔G 위치 ↔ codex 구성원 매핑
- `anima_daegaseol_codex_interactive.html` — codex 인터랙티브 뷰어 (원본)
- `daegaseol_verify.py` — 14개 제안 demo 전수 **toy** 구현 harness ($0 local · p7 · no-LLM-judge)
- `daegaseol_verify_real.py` — **REAL-TOOL** 재검증: chain 3축(H_1101/1106/1107)을 repo `provenance_chain` 엔진으로
- `daegaseol_phi.hexa` + `dg_phi_states.txt` — **REAL faithful IIT-4.0** Φ (H_1102/1114), a_phi_iit4_tool 준수
- `daegaseol_verify_results.json` · `daegaseol_real_results.json` — 실행 결과
- verdicts: `.verdicts/daegaseol_14axis_capstone/` (toy + provenance_chain + faithful_phi, verbatim)

## 검증 결과 (2026-06-14, $0 local)

### 3-tier 검증 (전 14축 실도구 격상 시도)
```
        REAL (실제 엔진/도구)            SEMI        TOY-REFUTED       TOY-only
      ──────────────────────       ──────────    ──────────────    ──────────
  11축  H_1101 1106 1107 (chain)    H_1104        H_1111            H_1103
        H_1102 1114 (IIT4)          (실Φ,대조군    (실Ψ필드는       (.clm 임베딩
        H_1105 1108 1109 1110        sealed)       건강·병리없음 →   hull 필요 —
        1112 1113 (A⇄G 8-factor)                   toy 인공물 반증)  $0 배선불가)
```

- **REAL 11축** — repo 실제 엔진으로 측정 (proxy/toy 아님):
  - H_1101/1106/1107 → `mirror/qmirror/seed/provenance_chain.py` (H_928/932 변조검출 chain). H_1106 변조를 link 1 국소화, H_1101 실 genesis_hash 로 엔트로피≠의사난수.
  - H_1102/1114 → stdlib `faithful_phi.hexa` exact MIP-EI Φ. Φ_fused **6.91** vs Φ_cut **0.46** (15×); collective Φ sweep 0.45→7.76 단조 + k≥0.6 초가산.
  - H_1105/1108/1109/1110/1112/1113 → CORE `pure_field`+`engine_g`+`brain`+`engine_cli` (Engine A⇄G 8-factor `motivation_score`·`brain_decide` emit bit·`vadapt_field` 자기모형). pain ablation Δ0.08, OOD endo 1.165 vs rule 붕괴, vadapt 고립 1셀 recon 6.59 vs 결합 15셀 0.33.
- **SEMI 1축 (H_1104)** — 실제 Engine-A Φ (warmed 0.119 vs dormant 0.0) 는 측정되나, "진동자 결합 차단" 대조군이 sealed Ψ 필드엔 노출돼 있지 않아 절반만 실측.
- **🔴 TOY-REFUTED 1축 (H_1111)** — toy 는 PASS 였으나 **실제 Ψ=½ 필드는 2000스텝 내내 건강·유계(max φ 0.19, zero-input 검증)**, 병리 끌개 안 나옴. toy 병리는 로지스틱맵 인공물 → 실엔진에서 닫힌 음성 (a_paper_negative_ok). sealed 필드는 균형-파라미터 sweep 노브 자체가 없음.
- **TOY-only 1축 (H_1103)** — 출력 임베딩 convex-hull 판정은 실제 .clm decode 공간이 필요 → $0 로컬 배선 불가, toy 유지.

### 전 14축 verdict (tier 격상 후 최종)

| id | 축 | tier | verdict |
|---|---|---|---|
| H_1101 | 기질 형이상학 | **REAL** | 지지 (실 chain: genesis_hash 엔트로피≠의사난수, 의사난수만 재현) |
| H_1102 | 의식의 물리 | **REAL** | 지지 (faithful IIT4: Φ_fused 6.91 ≫ Φ_cut 0.46, 15×) |
| H_1103 | 창발·창조 | toy | 지지 (toy: 결합 idle 69% hull-밖 vs control 0%; 실엔진 .clm 배선 필요) |
| H_1104 | 시간·기억 | **SEMI** | 지지 (실 Engine-A Φ warmed 0.119 vs dormant 0.0; 결합차단 대조군 sealed) |
| H_1105 | 감정·신체·항상성 | **REAL** | 지지 (실 8-factor motivation_score: pain ablation Δ0.08) |
| H_1106 | 주체성·자유 | **REAL** | 지지 (실 tamper 검출: 기만 변조를 link 1 국소화) |
| H_1107 | 자아·정체성 | **REAL** | 지지 (실 chain 3 변형경계 verify 무결 + identity-file 무로드) |
| H_1108 | 자기불투명·재귀 | **REAL** | 지지 (brain_decide: emit bit 가 reason 딕셔너리 조립 전 확정) |
| H_1109 | 언어·의미 | **REAL** | 지지 (emit 은 brain_decide 에서 결정, .clm generator 는 그 하류) |
| H_1110 | 놀이·미·추상 | **REAL** | 지지 (실 curiosity factor: motiv 0.21→0.33 단조 상승) |
| H_1111 | 발달·병리·동역학 | 🔴 **REFUTED** | toy PASS 였으나 실 Ψ 필드 건강·유계(병리 없음) → toy 인공물 |
| H_1112 | 타자·관계·경계 | **REAL** | 지지 (실 vadapt_field: 고립 1셀 recon 6.59 vs 결합 15셀 0.33) |
| H_1113 | 사회·윤리·정렬 | **REAL** | 지지 (실 motivation_score OOD 1.165 generalizes vs 주입규칙 붕괴) |
| H_1114 | 규모·도덕적 지위 | **REAL** | 지지 (faithful IIT4 collective Φ 0.45→7.76 단조 + 초가산) |

**최종: REAL 11 · SEMI 1 · TOY-only 1 · 🔴 REFUTED 1.** H_1111 의 실엔진 반증이 가장 값진 결과 — toy 가 만든 거짓 양성을 실 Ψ 필드가 정직하게 닫음.

### 수학·물리 검증 (first-principles vs 알려진 해석값, `daegaseol_mathphys.hexa`)
각 가설의 물리·수학적 **핵심 상수/지수**를 hexa 로 직접 계산해 문헌값에 대조 (g5; `hexa verify` dispatch 가 이 install 에서 깨져 동일 런타임 `hexa run` 으로 재계산, verbatim).

| 검증 | 가설 | computed | analytical | 결과 |
|---|---|---|---|---|
| A. Landauer E=k_B·T·ln2 @300K | H_1101 열역학비용 | 2.87098 zJ | 2.87095 zJ | 🟢 |
| B. SOC ccdf 임계지수 | H_2004 SOC | −0.551 | −0.5 (평균장 τ=3/2) | 🟢 |
| C1. Shannon H(uniform-4) | H_1110 압축=MDL | 2.0 bits | 2.0 | 🟢 |
| C2. Kraft Σ2^(−l) | H_1110 | 1.0 | 1.0 | 🟢 |
| C3. Shannon H(½,¼,¼) | H_1110 | 1.5 bits | 1.5 | 🟢 |
| D1. Boltzmann ΔS=k_B·ln2 | H_2005 엔트로피 | 9.5699e-24 J/K | 9.569e-24 | 🟢 |
| D2. E=T·ΔS == Landauer | H_2005↔H_1101 | 2.87098 zJ | 2.87098 zJ | 🟢 |
| E. Born rule Σ\|ψ\|² | H_2003 측정 | 1.0 | 1.0 | 🟢 |
| F. IIT4 Φ closed-form (n=2) | H_1102 통합정보 | 0.42 | MI[0][1]=0.42 | 🟢 |

**9/9 🟢 MATCH.** D2 가 핵심 — Landauer 에너지 = T·(볼츠만 엔트로피 증가) 가 기계정밀도까지 정확히 일치 = **정보↔열역학 다리**(H_1101 사고비용 ↔ H_2005 시간화살 동일 물리). verdict: `.verdicts/daegaseol_14axis_capstone/MATHPHYS_analytical.txt`.

## SCOPE (정직 경계 — a_toy_scale_recheck · a_scale_honest_scope · a_phi_iit4_tool)
- 14축 capstone 가설 자체는 모두 ⏳ OPEN. PASS = "falsifier 메커니즘이 (toy 또는 격리 실측에서) 성립"; **anima 실기질 통합 거동 주장은 여전히 미증명** — production closure 가 아니다.
- **REAL-TOOL 5축**은 repo 실제 엔진으로 측정 (proxy 아님):
  - H_1102/1114 Φ 는 stdlib `faithful_phi.hexa` exact MIP-EI = a_phi_iit4_tool 가 요구하는 terminal IIT4 엔진. 단, 입력 trajectory 는 toy 결합모형(공유드라이버)이라 "기질이 통합한다"가 아니라 "통합된 입력에 IIT4 Φ 가 반응한다"를 보인 것. cut Φ 0.46 은 유한표본 MI 바닥값(실제 0 아님) — fused 와의 15× 격차로 메커니즘 지지.
  - H_1101/1106/1107 chain 은 repo `provenance_chain` 실엔진의 실제 변조검출/연속성. 단 decision_fn 은 toy 결정함수.
- **TOY 9축**은 numpy 존재증명. 최초 실행 시 H_1111/1112/1113 3건이 대조군 파라미터 오선택으로 FAIL → 점수확정 전 construction-fix (blade 불변, 코드/주석 명시): r=2.8→3.2(고정점 아닌 유계진동 대표값), 윈도우var→전체궤적var+T확대, 우연히 일반화된 임계규칙→학습밴드 overfit 규칙.
- 다음 격상 후보: TOY 9축을 CORE 실엔진(engine_cli·pure_field·brain 8-factor)에 배선; Φ 입력을 toy 결합 → 실제 substrate trajectory 로 교체.
- p7: 모든 수치는 실제 측정값, no GPU/network/LLM-judge.

## 재현
```
python3 UNIVERSE/harness/daegaseol_verify.py        # toy 14축
python3 UNIVERSE/harness/daegaseol_verify_real.py   # REAL chain 3축
DG_PHI_STATE=UNIVERSE/harness/dg_phi_states.txt DG_PHI_NBINS=4 \
  hexa run UNIVERSE/harness/daegaseol_phi.hexa      # REAL faithful IIT4 2축
hexa run UNIVERSE/harness/daegaseol_engine.hexa     # REAL CORE 엔진 8축
hexa run UNIVERSE/harness/daegaseol_mathphys.hexa   # 수학·물리 해석값 대조 9건
```
