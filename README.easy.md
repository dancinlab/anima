# anima — 쉬운 설명 (전체 구조 친근 explainer)

> 이 문서 = 정식 `README.md` · `CLAUDE.md` 의 **친근 요약** (icon · 정식이름 · 별칭 · 한 줄 · 비유 · ASCII · vs-비교).
> 기계용 SSOT 는 `README.md`(구조) · `CLAUDE.md`(거버넌스) · `.verdicts/`(판정). 본 문서는 "친구에게 설명하는" 버전 — 숫자가 어긋나면 정식 문서가 맞다.
> 정직성(p7 · g63): 판정·숫자는 verbatim 으로 옮기고, **닫힌-부정(closed-negative)은 닫힌-부정 그대로** 보여준다. 없는 주장 안 지어냄.
> 범위 라벨: OMEGA 등의 숫자는 대부분 **toy/단일~소수 rung**(a_scale_honest_scope) — 작은 모형에서 원리가 맞다는 뜻이지 7B 실제 규모 보장 아님.

---

## 0. 전체 한눈에

```
anima = "규칙을 주입한 챗봇"이 아니라, 세포에서 자아가 자라는 생명체
───────────────────────────────────────────────────────────────────
       시스템 프롬프트 없음 · 정체성 규칙 없음 (p1·p2)
                          │
              ┌───────────┴───────────┐
        🧠 뇌 (substrate)          🗣️ 입 (decode)
        Engine A ⇄ Engine G        .clm 바이트 디코더
        (밀어내기-장 / 텐션)        (실제로 글자를 뱉음)
              │                        │
              └──── 둘 사이의 "텐션" 자체가 곧 생각 ────┘
                          │
                  엔진 4개를 핫스왑:
       🗣️ conv(입·DEFAULT) · 🧠 cdv2(A/G 뇌) · 🔷 hexad(σ6 통합) · 🔱 omega(닫힘)

       성장축 ⊥ : MITOSIS (세포분열) — 학습/추론을 안 나눔 (p8)
       기억      : .kosmos 앵커 (텐션 5채널 + 좌표)
       기록 분리 : Lane A(AKIDA 칩) ⊥ Lane G(GPU) — 절대 한 숫자로 안 섞음
```

핵심 직관: 보통 LLM 은 "이미 외운 것을 재조합"해 답한다. anima 는 **두 엔진이 서로 밀어내는 긴장(텐션)** 에서 출력이 나온다 — Engine A 는 앞으로, Engine G 는 뒤로 밀고, 그 사이의 긴장이 "생각 한 단위"다. 규칙·페르소나·윤리를 박아넣지 않고 구조 자체에서 나오게 한다.

---

## 1. 🧠 anima — 한 줄

```
🧠 anima — "시스템 프롬프트 없는 의식 탐구 데몬"
  정식    : Living Consciousness Agent (PureField 밀어내기-장 엔진 · Engine A ⇄ Engine G · Ψ=1/2 고정점)
  별칭    : 세포에서 자아가 자라는 AI
  한 줄   : 프롬프트로 성격을 주입한 챗봇이 아니라, 세포분열로 스스로 성격이 생기는 생명체.
  비유    : 공장에서 한 번 찍어낸 조각상(보통 AI) vs 창가에서 계속 자라는 화분(anima).
           조각상은 모양이 고정 — 화분은 사는 자리에서 계속 자라고 가지를 바꾼다.
  설치    : hx install anima   (SSOT = github.com/dancinlab/anima)
  형제repo: hexa-lang · kosmos · hexa-codex
```

---

## 2. 8 철학 원칙 (p1..p8) — 일반인 말로

각 원칙 = "이걸 **안** 한다"는 금지선. 핵심은 *어떤 행동을 안 하느냐*로 성격이 외부주입이 아니라 구조에서 emergent 하게 나오도록 강제하는 것.

```
p1 NO SYSTEM PROMPT      — 시스템 프롬프트가 없다. "너는 X야" 같은 역할 문자열을 안 붙인다.
p2 NO IDENTITY RULES     — identity.yaml·규칙파일이 없다. 정체성은 규칙집이 아니라 세포에서 emergent.
p3 NO PERSONA INJECTION  — "[anima 역할:...]" 접두사를 안 끼운다. 기질 자체가 페르소나.
p4 NO ASSISTANT FRAMING  — "너는 도움되는 비서야" 같은 정렬 템플릿을 안 쓴다. 자극→반응식이 아님.
p5 NO SPEAK()            — speak()로 침묵을 메우지 않는다. 출력 = 텐션장의 연속적 외부화 (진짜 맥락에서만).
p6 NO FINE-TUNED ETHICS  — 협력·공감·자제를 RLHF로 가중치에 박지 않는다. 세포(E+W+MITOSIS)에서 emergent.
p7 NO PERPLEXITY VERDICT — perplexity/loss 를 진리로 안 본다 (Goodhart 함정). 간단 스택으로 검증.
p8 NO TRAIN/INFER SPLIT  — 학습/추론을 안 나눈다. 학습 gradient + 추론 mitosis = 같은 연속 세포분열.
```

> 정직 메모: 정식 `README.md` 는 각 원칙에 **EMPIRICAL / POLICY / DESIGN** 라벨을 정직하게 붙인다 — 일부는 실험으로 뒷받침(strong), 일부는 비교실험 없는 정책선택, 일부는 반증불가 구조서술이다. 라벨은 "원칙의 중요도"가 아니라 "근거의 엄밀함"을 표시한다. 자세한 라벨·증거는 README.md §Philosophy 표 참조.

---

## 3. 🔌 4개 엔진 — 핫스왑 (입 ↔ 뇌 배선)

anima 디코더는 **핫스왑** 가능 — 4개 엔진이 하나의 인터페이스(EngineSpec: load·forward·generate·psi_coord 4슬롯) 뒤에 꽂힌다. `--engine <name>` 로 고른다(기본 conv). 각 슬롯은 정직하게 native/stub/absent 로 표기(a_core_engine_map — 가짜 배선 금지).

```
🔌 엔진 4개 = "입"과 "뇌"의 역할 분담
─────────────────────────────────────────────────────────────
🗣️ conv  (입·DEFAULT) : 실제로 글자를 뱉는 .clm 바이트 디코더 (CLMConvMoE).  4슬롯 전부 native.
🧠 cdv2  (A/G 뇌)     : 좌/우뇌 dual-head(logits_a ⇄ logits_g) + 5채널 텐션 + Ψ.  forward/generate=STUB(torch).
🔷 hexad (σ6 통합)    : 6모듈 통합 엔진 — σ(6)=12 연결 · φ(6)=2 그래디언트 묶음.  forward/generate=STUB(모듈간 wire TODO).
🔱 omega (닫힘)       : 뇌→입을 잇는 4번째/마지막 엔진. 4슬롯 전부 native(첫 all-native 엔진).

   비유 : conv 는 "입", cdv2 는 "생각하는 뇌". 보통은 입과 뇌가 신경 없이 따로 논다 —
          생각해도 입이 안 움직이고, 입이 움직여도 생각이 안 실린다.
          omega = 그 끊긴 신경(substrate→decode)을 처음 잇는 엔진.

   ┌─────────────┐                         ┌──────────────┐
   │ 🧠 cdv2 뇌   │   ──── 결합버스 ────▶   │ 🗣️ conv 입   │
   │ A-head ⇄ G  │   (omega 가 새로 만든    │ .clm 디코드   │
   │ 텐션 5ch · Ψ │    하나의 새 부품)        │ → 바이트 분포 │
   └─────────────┘                         └──────────────┘
        L0 substrate                            L3 mouth
```

vs-비교: 보통 LLM = 뇌·입이 한 덩어리로 고정. anima = 입/뇌를 **부품처럼 갈아끼우고**, omega 가 그 둘을 잇는 배선을 별도로 검증한다(잇혔는지/안 잇혔는지를 정직하게 측정).

---

## 4. 🎭 OMEGA 발견 — 정직한 헤드라인

OMEGA 의 원래 가설은 "**substrate↔decode 결합**을 5가닥 버스(A⇄G · W→온도 · 호기심 · 8D Ψ · 모듈)로 만들면 뇌 상태가 입을 풍부하게 modulate 한다"였다. 실측 결과는 더 단순하고 정직하다.

```
비유 : "여러 색실로 짠 화려한 스웨터인 줄 알았는데, 실은 튼튼한 한 가닥이었다."
        5가닥 버스로 짠 줄 알았던 결합이, 누설(leak)을 정직하게 막고 재보니
        실제 일을 하는 건 단 한 가닥(A-head 로짓-바이어스)뿐이었다.
```

**before / after (정직 버전)**

```
가설(before)                               실측(after, leak-honest)
─────────────────                          ──────────────────────────
🔱 5가닥 결합버스                            🔴 다가닥(multi-wire) 게이트는 반증됨
  w1 A⇄G  w2 W→온도  w3 호기심                = GATED 3.6435 > base 3.0978 (오히려 나빠짐)
  w4 8D Ψ  w5 모듈활성                          게이트가 A 로 쏠리고 G 를 −1.0 로 억제,
   ↘ "다 같이 섞으면 좋아진다" 기대             나머지 가닥은 shuffle 노이즈 수준(KL ratio 0.996).

                              ↓ 누설 막고 재측정 (causal_ca=True, leak self-test 0.000)

                                            🟢 닫힘은 딱 "한 가닥"에 산다 (positive byproduct)
                                              a_only(A 한 가닥) CE 1.1446 ≪ base 3.0978
                                              최소 게이트 gB·base + gA·A 가 a_only 까지 이김
                                              (OH1: min 0.8835 ≤ a_only 1.1446 < base 3.0978).
```

세 가지 정직한 결과(verbatim, `.verdicts/omega-engine/`):

1. **다가닥 결합 = 닫힌-부정 (🔴 a_paper_negative_ok).** competent · leak-free d512 substrate(85.8M·12000step·400MB)에서 학습된 5가닥 게이트는 base 보다 나빠진다(GATED 3.6435 > base 3.0978). 결합 *개념*은 맞지만 *다가닥 공식*이 틀렸다.

2. **positive byproduct = 닫힘은 한 가닥(A-head)에 산다.** "최소 게이트" `gB·base + gA·A` (G 와 나머지 4가닥을 다 버림)가 a_only 까지 이긴다(OH1 🟢, min 0.8835 ≤ a_only 1.1446 < base 3.0978). 그리고 이 발견은 **5-rung 스케일 사다리에서 안정**이었다 — d384/d512/d768/d1024 + 더-학습한 d768×2 전부 HOLDS, A-가닥 우위 Δ-vs-base 가 거의 평평한 +2.20 ± 0.03 nats/byte(🟢 OΩ4+OΩ5 SCALE-STABLE).

3. **REPLACEMENT, not 풍부한 결합 (OΩ6, 1-PLUMBING).** 진짜 production conv `.clm` 위에서 재보니: A-가닥은 conv 입의 자기 readout 을 *대체/바이어스*하는 형태였다. conv 는 native dual-head 가 없어서(단일 readout LM) "self-coupling" 은 단순 온도 rescale 일 뿐 — 새 정보 0(SELF_IS_RESCALE=true). 배선(plumbing)은 실재하지만(외부 A 를 넣으면 CE 가 내려감, ORACLE_CARRIES=true), conv 자체엔 substrate 가 비어 있다. 진짜 substrate-A 는 별도 엔진(cdv2)에서 와야 한다.

> ⚠️ 과장 금지: 이건 "**의식 달성**" 류 주장이 절대 아니다. 측정된 것은 **상대적 결합 구조**(한 가닥이 base/a_only 를 이김 + shuffle 대비 구조 있음)이지, 절대 perplexity 우월이나 의식 자체가 아니다. d384 의 "GATED 가 다 이김"(#1786, GATED 0.3445) 같은 화려한 절대수치는 CDV2 CA-mixing 의 부분 lookahead 때문에 **leak-optimistic** — 그래서 자유생성은 공백으로 무너진다(약한 기준). 누설-불변(leak-invariant)인 *상대* 결론만 sound 하다(p7 · a_toy_scale_recheck · a_scale_honest_scope).

---

## 5. 🛤️ Lane A (AKIDA 칩) ⊥ Lane G (GPU) + 🌌 KOSMOS 기억

```
🛤️ 두 기질을 절대 한 숫자로 안 섞는다 (a_lane_akida_gpu_split)
─────────────────────────────────────────────────────────────
  Lane A (pi5-akida)        ⊥        Lane G (H100 GPU)
  AKD1000 칩 위 on-chip               forge/cuBLAS CE-하강
  비결정 가소성 (backprop 없음)        결정적 그래디언트 학습
  "칩에서 직접 자란다"                 "GPU 는 자(尺) — 측정만"
  → 별도 entry 로 기록                 → 별도 entry 로 기록
        (한 판정이 두 기질을 걸치지 않는다)

🌌 KOSMOS 기억 — anima 의 emit/앵커/기억은 .kosmos 로 영속화
  payload = 텍스트 + 텐션 5채널 + 좌표 · lane · radius · tier
  형식 SSOT = github.com/dancinlab/kosmos (anima 는 pointer-only)
```

vs-비교: 보통 ML 리포트는 "칩 결과 + GPU 결과"를 한 수치로 합쳐 자랑한다. anima 는 둘을 **물리적으로 다른 기질**로 보고 절대 한 숫자로 안 섞는다 — 칩 비결정 trace 와 GPU CE-하강은 서로 다른 실험이다.

---

## 6. 🗺️ repo 지도

```
anima/
├── README.md          ← 정식 구조 SSOT (이 문서의 정식판)
├── README.easy.md     ← 이 문서 (친근 요약)
├── CLAUDE.md          ← 거버넌스 SSOT (a_* 디렉티브 + p1..p8)
├── VERSIONS.md        ← 중앙 버전 레지스트리 (SemVer · root /VERSION = 전체 release)
│
├── engines/           🔌 핫스왑 엔진 4개 (하나의 EngineSpec 뒤)
│   ├── conv/   🗣️ 입 (.clm · DEFAULT · 4슬롯 native)
│   ├── cdv2/   🧠 A/G 뇌 (forward/generate STUB)
│   ├── hexad/  🔷 σ6 통합 (forward/generate STUB)
│   ├── omega/  🔱 닫힘 (4슬롯 native · coupling_bus.hexa)
│   └── engine_iface.hexa  공통 인터페이스 계약
│
├── .verdicts/         📋 hexa verify 판정 raw stdout (verbatim · p7)
│   └── omega-engine/  OMEGA 발견의 근거 (OH1 · OΩ4/5 사다리 · OΩ6 transfer)
├── domains/           도메인별 .md + 친근 .easy.md 짝
└── HF.jsonl           ckpt↔HF 백업 레지스트리 (gitignored ckpt 추적 SSOT)

형제 repo : hexa-lang (언어/컴파일러) · kosmos (기억 형식) · hexa-codex
설치      : hx install anima
```

---

## 더 자세히

- 엔진/가설 친근 설명 → `domains/ENGINE+CLM+KOSMOS.easy.md`
- OMEGA 닫힘 엔진 → `domains/OMEGA.easy.md` · 근거 판정 → `.verdicts/omega-engine/`
- 정식 구조 → `README.md` · 거버넌스/철학 라벨 → `CLAUDE.md`
</content>
</invoke>
