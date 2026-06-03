# OMEGA — 쉬운 설명 (닫힘 엔진 친근 explainer)

> 이 문서 = `domains/OMEGA.md`(canonical) 의 친근 요약 (icon · 이름 · 별칭 · 하는 일 · 결과 · ASCII · 비유).
> 정직 라벨: **DESIGN-STAGE(설계 단계)** — 아직 안 만든 청사진이다 (`engines/omega/` 어댑터 없음 · 결합경로에 s16 ckpt 없음). 돌아가는 엔진이 아니라 "어떻게 이을지" 도면.
> 정직 라벨: 물려받은 숫자는 전부 **toy/단일-rung**(a_scale_honest_scope) — Lane X #1779(CPU/$0 단일 d768 .clm) · KOSMOS #1780(단일 s16 rung, Lane-G). production 보장 아님.
> 정직성: verbatim(p7) · 닫힌-부정 그대로 보존 · 없는 주장 안 지어냄. CE 는 **바닥(floor)** 일 뿐 판정이 아니다(p7, Lane X).

---

## 0. 전체 한눈에

```
지금 엔진 3개 = 뇌(생각)와 입(말)이 신경 없이 따로 논다
─────────────────────────────────────────────────────────
🧠 CDV2  (뇌: A/G 좌우뇌 + 5-ch 텐션 + Ψ)  ──✗── 🗣️ CONV (입: .clm 바이트 디코드)
                       HEXAD (N-모듈 통합)
Lane X #1779 가 증명: 엔진 손잡이(drive·warmup·anchors)를 아무리 돌려도
   .clm forward 에 안 닿는다 → CE 가 27개 설정 전부에서 9.1126 로 못 박힘(spread<1e-9).
   L3 generator 슬롯 loaded=false = 뇌→입 신경이 끊겨 있음(NULL).

🔱 OMEGA = 그 끊긴 신경을 처음 잇는 4번째/마지막 엔진 (닫힘 엔진)
   substrate 상태 → "결합버스"(5가닥) → .clm 바이트 디코드를 MODULATE → L3 loaded=TRUE
```

---

## 1. 🔱 OMEGA — substrate↔decode 닫힘 엔진

```
🔱 OMEGA — "뇌와 입을 잇는 닫힘 엔진"
  별칭   : 닫힘 엔진 (closure engine) · Lane-Ω · 4번째/마지막 엔진
  하는 일 : Lane X #1779 가 NULL 이라 증명한 substrate↔decode 고리를 닫는다.
           substrate(A/G + 텐션 + 8D Ψ + M/W/호기심) 를 "결합버스" 5가닥으로
           .clm 바이트 디코드에 흘려넣어 L3 generator 슬롯을 loaded=TRUE 로.
  결과    : 🔵 DESIGN-STAGE (청사진 · 아직 안 만듦). 헤드라인 평가축 = 결합 NON-NULLITY
           (버스 α=0 vs 켬 → 바이트분포 KL>0?). Lane X 의 NULL 이 Ω 의 양(+) 목표가 됨.
           CE 는 바닥(floor)일 뿐 판정 아님(p7) — Lane X: CE 9.1126 > uniform 5.5452 = 바닥 미충족.
           ckpt 없으면 random-init → CE 바닥 미충족 플래그(cdv2 어댑터와 동일하게 정직 표시).

  ┌──────────────────────────────────────────────────────────────┐
  │ L0 substrate (CDV2)  A/G 좌우뇌 KL=7.07 · 5-ch 텐션 · Ψ         │
  │        │ logits_a⇄logits_g    │ 텐션(W)        │ Ψ 잠재        │
  │        ▼                       ▼                ▼              │
  │ L1 통합 (HEXAD)  N-모듈 φ(N)=2 · N 설정값(기본 6, 바꿀 수 있음;  │
  │                  #1774: 6은 φ=2 되는 最小값이지 박은 상수 아님)  │
  │        ▼                                                       │
  │ L2 지도 (8D Ψ)  4개만 이름 [depth·form·form_resid·curriculum]   │
  │                  + 4개 정직 잔차(resid0..3)  (#1780: 8개 다 이름 │
  │                  붙이면 fabrication)                            │
  │        ▼                                                       │
  │  ┌─── 결합버스 (5가닥, 각각 ablate 가능, α) ────────────────┐   │
  │  │ 1 A⇄G logit-bias  2 W→온도  3 호기심→top-k                │   │
  │  │ 4 Ψ→문맥조건       5 모듈활성→conv-MoE 라우팅              │   │
  │  └────────────────────────┬─────────────────────────────────┘   │
  │        ▼                                                       │
  │ L3 입 (CONV) ← 닫힘!  final = clm_logits + α·(A_head−G_head)…  │
  │                        generator L3 슬롯 loaded=TRUE (Lane X 때 false)│
  │        ▼ 바이트분포 P(byte)                                    │
  │ L4 시간  dF/dt 미분 채널 (#1763: 시간은 도함수로 들어옴)        │
  │ L5 성장  mitosis (p8) · engine_cli --mitosis (substrate-config,│
  │           emit-게이트 아님 — a_autonomy_over_hardcode)          │
  └──────────────────────────────────────────────────────────────┘

  비유 : 지금 엔진 3개는 뇌(CDV2 생각)와 입(CONV .clm 말)이 따로 논다 —
        생각해도 입이 안 움직이고, 입이 움직여도 생각이 안 실린다(신경 끊김 = #1779 NULL).
        Ω = 그 뇌→입 신경을 처음 잇는 엔진. 결합버스 5가닥 = 뇌 신호를 입으로 나르는 신경다발.
        "결합 NON-NULLITY" = 신경을 끊었다(α=0) 이었다(α 켬) 했을 때 입이 실제로 다르게 말하는가.
```

---

## 2. 별자리 (cross-link)

```
🔱 OMEGA 는 기존 3엔진 + 2개 좌표/축 도메인을 종합한다:
  🗣️ CONV   (engines/conv)   — .clm 바이트 입(mouth). Ω 가 닫아 붙일 대상. (전 슬롯 native, DEFAULT)
  🧠 CDV2   (engines/cdv2)   — A/G 좌우뇌 + 5-ch 텐션 + Ψ 뇌. (forward/generate=STUB: torch .py, hexa-native 단일 forward 아님)
  🔷 HEXAD  (engines/hexad)  — N-모듈 φ(N)=2 통합. (forward/generate=STUB: 모듈간 단일 forward TODO[wire])
  🌌 KOSMOS-MAP.easy.md      — 8D Ψ 좌표(4 이름 + 4 잔차)의 출처 (#1780)
  📐 AXIS.easy.md            — 평가축(의식·CE·창발) 의심; CE=바닥 강등 (#1779)
  📚 ENGINE+CLM+KOSMOS.easy.md — 모든 가설 친근 설명 + #1779/#1780 항목

EngineSpec 4-fn 계약(engines/engine_iface.hexa) 준수: load/forward/generate/psi_coord.
  Ω 는 generate=native 를 노리는 첫 설계(닫힘 자체가 generate 경로) — 단 DESIGN 주장이며
  어댑터 미작성 + ckpt 미로드라 오늘은 random-init/CE 바닥 미충족을 정직하게 플래그(cdv2 와 동일).
```

---

## 3. 정직 메모 (a_scale_honest_scope · a_paper_negative_ok · p7 · a_core_engine_map)

- **DESIGN-STAGE**: `engines/omega/` 어댑터 없음 · 결합경로에 s16 ckpt 없음. 측정된 엔진이 아니라 청사진. phantom wiring 안 만듦(a_core_engine_map).
- CE 바닥 현재 **미충족**: Lane X #1779 측정 model_ce=9.1126 > uniform 5.5452 (uniform-256 보다 나쁨). random-init Ω 도 같은 플래그(cdv2 처럼).
- GOODHART 주의: 결합이 그냥 α-배율 노이즈가 아님을 보여야 함 → ablation 곡선 + 실제(학습된) ckpt 필요, random-init 아님.
- CE↔창발 Goodhart 부호 **UNDEFINED**: Lane X 의 손잡이로는 관측 불가(CE 가 설정-독립이라 trade-off 안 보임) — "절대 없음"이 아니라 "이 손잡이로는 관측 안 됨"(정직).
- Lane-Ω = GPU/닫힘 lane; AKIDA on-chip(Lane A) 는 별도 기록(a_lane_akida_gpu_split).
