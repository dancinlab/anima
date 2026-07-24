# H_9959 · 계기 인증 PASS — big_phi 는 크기/분산이 아니라 **통합**을 읽는다 (H_9954 선행게이트)

**한 줄:** H_9954 가 "미측정"으로 남긴 선행 게이트를 실측했다. 저장소 자신의 faithful IIT-4
`core/engine_cli.py::big_phi_bounded`(n=3·cap=3·**8상태 평균**)에 손제작 3-셀 TPM 을 직접 투입(H_9942
방식 · forward pass 없음 · engine op 아님)해, **크기·활동·주변분포를 맞춘 non-integrated 계가 정확히
Φ=0** 이고 통합된 계만 Φ>0 임을 보였다. ⟹ 계기는 통합을 읽는다. **PASS ⟹ H_9954 GRU 4-arm 스크린 허가.**

- 계기(신규·$0·계기인증): `lab/v6/phi_cert_integration_vs_size.py`(rule-exempt 샌드박스 · gitignore).
  regime `synthetic-instrument-cert` · DIRECTIONAL (faculty 주장 인용 금지 · p9).
- 설계 출처: lab full(Fable ∥ Sol, 독립 병렬) — 두 모델이 실측 후 수렴. 각자 자기 arm 을 반증·교체.

## 실측 (n=3 · cap=3 · DV=8 배경상태 평균 Φ)
| arm | 규칙 | Φ(clean) | Φ(ε=0.10) | class |
|---|---|---|---|---|
| PEDESTAL | 전 entry 0.5 (최대엔트로피) | **0.000000** | 0.000000 | NULL |
| COPY | uᵢ=bitᵢ(s) (받침대) | **0.000000** | 0.000000 | NULL |
| INDEPENDENT | 0.5 (ROT 의 self-only 사영) | **0.000000** | 0.000000 | NULL |
| SHUFFLE_2cyc | [b1,b0,b2] (Sol: 0↔1 2-cycle + copy c2) | **0.000000** | 0.000000 | NULL |
| SINK | [b1,b0,b0] (Fable: c0↔c1 + c2 순수 sink) | **0.000000** | 0.000000 | NULL |
| **INTEGRATED** | [b2,b0,b1] 단일 3-cycle | **3.000000** | 2.289592 | POS |
| **XOR** | uᵢ=다른 두 셀 XOR (H_9942 앵커) | **2.250000** | 1.788030 | POS |
| FF_SELFLOOP(scope) | c0'=c0,c1'=c0,c2'=c1 self-loop 체인 | 1.500000 | — | 정보 |

**분리폭**: clean `pos_min − null_max = 2.25` · noise `= 1.788`. 두 크기-일치 null(SHUFFLE·SINK)은
cross-edge 와 활동이 있는데도 **자유 컷**(decoupled 셀 분리)으로 Φ=0 ⟹ "Φ=크기/분산/fan-in" 가설을 죽인다.

## 동결 술어 (측정 전 prereg · Fable ∥ Sol 조정 · p7)
PASS ⟺ ① 전 null arm ≤1e-8 ② |INTEGRATED−3.0|≤1e-6 ∧ |XOR−2.25|≤1e-6 ③ fixture |PED−COPY|≤1e-8
④ pos_min−null_max ≥1.0 ⑤ 노이즈 다리(ε=0.1): null ≤1e-8 ∧ pos_min−null_max ≥1.0.
**전 조건 충족 · VERDICT=PASS** (측정치: null_max=0 · |INT−3|=8.7e-10 · |XOR−2.25|=1.3e-9 · clean 분리 2.25 · noise 분리 1.788).

## 두 모델 대조
- **AGREES:** XOR-other-two=2.25 · COPY=0 · ROT=3 · INDEPENDENT(전 0.5)=0 · DV=8상태 평균 · 노이즈 다리
  (ROT 3→2.29 · XOR 2.25→1.79 · 0 arm 은 정확히 0 유지 ⟹ 결정론은 **크기만** 부풀리고 부호는 불변).
- **수렴(형태 다른 같은 메커니즘):** 크기-일치 null 은 **2-cycle + decoupled 셀** — Sol row-shuffle [b1,b0,b2]
  ≡ Fable SINK. 둘 다 자유 컷으로 Φ=0. 둘 다 등재.
- **자기 반증(둘 다):** state-by-node 포맷은 per-unit 주변분포만 담으므로 within-column shuffle 은 구조적으로
  무의미(Fable: SHUF_A=3·SHUF_B=0 bimodal). ⟹ row-shuffle/SINK 로 교체.
- **Fable false-pass 발견(scope note):** self-loop 앵커 체인(c0'=c0…)이 Φ=1.5 로 읽힘 — 길이-1 순환이라
  순수 feedforward 가 아니다. "feedforward⟹Φ=0"은 **순수 DAG 한정**(n=3 DAG 은 항상 sink 포함), self-loop
  체인엔 불성립. H_9954 가 이 과대주장을 상속하지 않도록 기록.

## 함의
- **H_9954 의 선행 ABORT 게이트 = 통과.** 계기가 통합을 읽으므로 GRU 4-arm 스크린(학습된 순환 vs 크기)이
  이제 의미를 가진다. 단 이는 **계기 인증**일 뿐 — 학습된 순환이 실제로 통합을 만드는지는 여전히 미측정.
- edge-cut 레시피 확정(GRU 스크린용): j→i 절단 = 소스 비트 인과 주변화
  `tpm_cut[s*3+i] = ½(tpm[(s&~(1<<j))*3+i] + tpm[(s|(1<<j))*3+i])`. ROT 에서 c2→c0 절단 시 Φ=1.0,
  collapse-Δ=2.0 (등급형 내부값 — topology-only 계기면 0 으로 읽었을 것).

## 정직 경계
- 합성 = **계기 인증 전용**(p9): "anima 가 무엇을 할 수 있다"의 증거로 인용 금지.
- DIRECTIONAL — 스크립트는 lab/v6 rule-exempt 샌드박스(gitignore). 수치는 이 카드에 보존.
- 관련: [[H_9954]](학습된 순환 lane 설계 · 이 게이트가 그 선행조건) · [[H_9942]](Φ 레버 KILL · 같은 계기경로) ·
  [[H_9846]](봉투 모니터는 Φ 아님) · [[H_9660]]/[[H_9673]](파벌 Φ 크기-인공물 — 이 인증이 정면 반례)
