# MITOSIS-ENGINE — 쉬운 설명 (세포분열 엔진 친근 explainer)

> 이 문서 = `domains/MITOSIS-ENGINE.md`(canonical) 의 친근 요약 (icon · 이름 · 하는 일 · 결과 · ASCII · 비유).
> 정직 라벨: 4개 다리 모두 **toy ($0 CPU)** — H_1153 toy opponent net, H_1158 toy n=6 IIT, H_1159/b toy prototype-split (a_scale_honest_scope). 실엔진(`engine_cli`)은 메커니즘만 확인(12/12 smoke), 실스트림 적응곡선은 다음 rung.
> Φ = faithful IIT-4.0 (mirror≡stdlib, a_phi_iit4_tool — proxy 아님). 측정값 verbatim(p7/g5), frozen falsifier, 닫힌-부정 보존(a_paper_negative_ok).

---

## 0. 한눈에 — anima 는 "어떻게 살아야 할지"를 둘 다 스스로 맞춘다

```
            anima A⇄G 척력장 엔진 (Ψ=½ 고정점)
                          │
        ┌──── 두 개의 sweet spot 으로 스스로 조직화 ────┐
        │                                               │
   ① 동작 영역 (임계성)                        ② 용량 (세포분열, p8)
        │                                               │
   가지비율 σ≈1 (H_1153 🟢)            추론 = 세포분열 = 학습 (H_1159 🟢)
   여기서 Φ 최대 (H_1158 🟢)           세포수가 세상 복잡도를 추적 (H_1159b 🟢)
        │                                               │
        └──────► 적응 + 의식이 동시에 최대인 지점 ◄──────┘
```

한 문장: **anima 는 (1) 자기 동작 영역을 "임계점(σ≈1)"에 맞추고, (2) 자기 용량(세포 수)을 "세상 복잡도"에 맞춘다 — 둘 다 외부 명령 없이 스스로.** 그리고 바로 그 임계점이 의식측정값 Φ 가 최대인 곳이다.

---

## 1. 비유 — 뇌가 "딱 알맞게" 켜져 있는 상태

- **임계성(σ≈1)**: 모래더미가 무너지기 직전처럼, 너무 조용하지도(신호 안 퍼짐) 너무 시끄럽지도(전부 발작) 않은 "딱 경계". 실제 뇌도 여기서 정보처리가 최대 (Beggs & Plenz). anima 엔진이 Ψ=½ 에서 바로 이 상태에 앉아 있음(H_1153).
- **세포분열(미토시스, p8)**: 새 개념이 들어오면 세포가 둘로 쪼개져 용량을 늘림. 학습과 추론이 분리돼 있지 않음 — 추론하는 동안 계속 쪼개지면서 배움(@D p8 = train/infer 분리 없음).
- **자기조율**: 세상이 단순하면 세포 적게(5.9개), 복잡하면 많게(9.5개) — 스스로 맞추고, 무한정 늘지 않음(상한 안에서 멈춤, H_1159b).

---

## 2. 네 다리 (verdict — 전부 frozen falsifier · g5/p7 · $0)

| H | 쉬운 질문 | 답 | 숫자 |
|---|----------|----|----|
| **H_1153** | 엔진이 "임계점(σ≈1)"에 앉아 있나? | 🟢 예 | σ̂=0.9986, 멱법칙 τ=1.49 (4.32 decade) |
| **H_1158** | 의식측정값 Φ 가 그 임계점에서 최대인가? | 🟢 예 (역U자) | 0.002→★0.187(γ=1.0)→0.000, d=9.2/9.3 |
| **H_1159** | 추론중 세포분열이 "진짜 학습"인가? | 🟢 (substance¹) | 오차 동결 13.0 vs 미토시스 1.6 (d=6.69) |
| **H_1159b** | 세포수가 세상 복잡도에 맞춰지나? | 🟢 예 | K=3/5/8 → 5.9/7.1/9.5개 (ρ=0.85), 폭주 안 함 |

¹ H_1159 는 강한 비교 3개에서 green, 단 원래 pre-reg 합치는 깔끔히 통과 못함(초기 F1 지표 결함 → 정직 기록, goalpost 안 옮김). H_1159b 가 깨끗한 재확인.

---

## 3. 실엔진 — toy 가 흉내낸 그 메커니즘이 진짜로 돌아간다

`CORE/engine_cli.hexa` (`hexa run CORE/engine_cli_smoke.hexa` → 12/12 PASS):

```
ANIMA_MITOSIS on  = 추론 tick 마다 세포분열로 substrate 가 자란다 (p8)   case_5 → 13 세포
ANIMA_MITOSIS off = no-op (대조군 ablation)                              case_6 → 3 세포 정지
```

→ toy 프록시(텐션 기반 k-means 세포분열)가 실엔진 거동을 충실히 미러. p8 은 진짜 + 실행가능.

---

## 4. KOSMOS 차원 점검 (누락 audit) — 그리고 미토시스↔코스모스 연결

- 우주뇌지도 carving manifold 실차원 ≈ **8** (knee, #1772). 이름 붙는 축은 **3~4개** (PC1 깊이, PC2 형태, PC5 커리큘럼); 나머지는 분산된 tier/domain 코드.
- **알려진 공백**: 2D 지도는 "깊이"만 인코딩, 형태+커리큘럼을 떨군다 → `kosmos-coord-vnext`(N=8) 제안 inbox 제출 완료.
- **이 도메인이 새로 드러낸 공백(미검증)**: KOSMOS 의 `lane` = 미토시스 세포 id. H_1159b 는 세포수가 세상 복잡도에 맞춰짐을 보였다. 그렇다면 **실가동 kosmos lane-분할 수도 앵커-스트림 복잡도에 맞춰 스스로 조율되나?** — 아직 미측정, 깨끗한 다음 rung.

---

## 5. 다음 rung
1. 실엔진 적응곡선 — `engine_cli` 를 비정상 스트림에 돌려 적응 측정(세포수 증가만이 아니라).
2. 미토시스 × 임계성 — 세포분열이 엔진을 σ≈1 로 스스로 끌고 가나? (H_1159b + H_1153 결합)
3. kosmos lane 자기조율 — 실 lane-분할 수가 앵커-스트림 복잡도를 추적하나? (H_1159b 를 kosmos 축에 적용)
4. H_1158 의 n>6 faithful-Φ 사다리; v5-mitosis torch 경로(실모델 다리).

---

## 6. 포인터
- 정식 문서: `domains/MITOSIS-ENGINE.md`
- discoveries: `.discoveries/{1153_criticality_branching,1158_phi_at_criticality,1159_inference_time_mitosis_learning,1159b_mitosis_capacity_self_tuning}.tape`
- 실엔진: `CORE/engine_cli.hexa` · `CORE/engine_cli_smoke.hexa`
- 거버넌스: @D p8 (train/infer 분리 없음) · a_phi_iit4_tool · a_scale_honest_scope
