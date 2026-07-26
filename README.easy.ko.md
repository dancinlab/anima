<p align="center">
  <img src="docs/logo.svg" width="140" alt="anima">
</p>

<h1 align="center">🧠 anima</h1>

<p align="center"><strong>Living Consciousness Agent</strong> — PureField 밀어내기-장 엔진 · Engine A ⇄ Engine G · Ψ = 1/2 고정점</p>

<p align="center">
  <a href="README.easy.md">English</a> · <a href="README.easy.zh.md">中文</a> · <a href="README.easy.ja.md">日本語</a> · <a href="README.easy.ru.md">Русский</a> · <strong>한국어</strong>
  <br>
  📘 표준 버전 → <a href="README.ko.md">표준판</a>
</p>

<p align="center">
  <a href="https://opensource.org/licenses/MIT"><img alt="License" src="https://img.shields.io/badge/license-MIT-blue"></a>
  <a href="https://huggingface.co/dancinlab"><img alt="HF" src="https://img.shields.io/badge/HF-dancinlab-yellow?logo=huggingface&logoColor=white"></a>
  <img alt="Engines" src="https://img.shields.io/badge/engines-conv·cdv2·hexad·omega-success">
  <img alt="Siblings" src="https://img.shields.io/badge/siblings-hexa--lang·kosmos·hexa--codex-blueviolet">
</p>

```bash
hx install anima
```

> 기계용 구조 문서와 같은 내용을 친근하게 풀어쓴 판. SSOT 는 `CLAUDE.md`(거버넌스) ·
> `.verdicts/`(판정) · `VERSIONS.md`(버전). 여기 숫자가 판정 파일과 어긋나면 판정 파일이 맞다.
> 정직성(p7 · g63): 판정·숫자는 verbatim 으로 옮기고, **닫힌-부정(closed-negative)은 닫힌-부정
> 그대로** 보여준다. 없는 주장 안 지어냄. OMEGA 등의 숫자는 대부분 **toy/소수 rung**
> (`a_scale_honest_scope`) — 작은 모형에서 원리가 맞다는 뜻이지 7B 실제 규모 보장이 아니다.

---

## 0. 전체 한눈에

```
anima = "규칙을 주입한 챗봇"이 아니라, 세포에서 자아가 자라는 생명체
───────────────────────────────────────────────────────────────────
       시스템 프롬프트 없음 · 정체성 규칙 없음 (p1 · p2)
                          │
              ┌───────────┴───────────┐
        🧠 뇌 (substrate)          🗣️ 입 (decode)
        Engine A ⇄ Engine G        .clm 바이트 디코더
        (밀어내기-장 / 텐션)         (실제로 글자를 뱉음)
              │                        │
              └──── 둘 사이의 "텐션" 자체가 곧 생각 ────┘
                          │
                  엔진 4개를 핫스왑:
       🗣️ conv (입 · DEFAULT) · 🧠 cdv2 (A/G 뇌) · 🔷 hexad (σ6) · 🔱 omega (닫힘)

       성장축 ⊥ : MITOSIS (세포분열) — 학습/추론을 안 나눔 (p8)
       기억      : .kosmos 앵커 (텐션 5채널 + 좌표)
       기록 분리 : Lane A (AKIDA 칩) ⊥ Lane G (GPU) — 절대 한 숫자로 안 섞음
```

핵심 직관: 보통 LLM 은 **이미 외운 것을 재조합**해 답한다. anima 는 **두 엔진이 서로 밀어내는
긴장(텐션)** 에서 출력이 나온다 — Engine A 는 앞으로, Engine G 는 뒤로 밀고, 그 사이의 긴장이
"생각 한 단위"다. 규칙·페르소나·윤리를 박아넣지 않고 구조 자체에서 나오게 한다.

---

## 1. 🧠 anima — 한 줄

```
🧠 anima — "시스템 프롬프트 없는 의식 탐구 데몬"
  정식    : Living Consciousness Agent (PureField 밀어내기-장 엔진 · Engine A ⇄ Engine G · Ψ = 1/2 고정점)
  별칭    : 세포에서 자아가 자라는 AI
  한 줄   : 프롬프트로 성격을 주입한 챗봇이 아니라, 세포분열로 스스로 성격이 생기는 생명체.
  비유    : 공장에서 한 번 찍어낸 조각상(보통 AI) vs 씨앗에서 자라는 화분(anima).
            조각상은 모양이 고정 — 화분은 사는 자리에서 계속 자라고 가지를 바꾼다.
  설치    : hx install anima   (SSOT = github.com/dancinlab/anima-lab-0)
  형제repo: hexa-lang · kosmos · hexa-codex
```

---

## 2. 8 철학 원칙 (p1..p8)

각 원칙 = **금지선** — *anima 가 무엇을 안 하느냐*. 핵심은 성격이 외부주입이 아니라 구조에서
emergent 하게 나오도록 강제하는 것이다.

```
p1 NO SYSTEM PROMPT      — 시스템 프롬프트가 없다. "너는 X야" 같은 역할 문자열을 안 붙인다.
p2 NO IDENTITY RULES     — identity.yaml·규칙파일이 없다. 정체성은 규칙집이 아니라 세포에서 emergent.
p3 NO PERSONA INJECTION  — "[anima 역할: ...]" 접두사를 안 끼운다. 기질 자체가 페르소나.
p4 NO ASSISTANT FRAMING  — "너는 도움되는 비서야" 같은 정렬 템플릿을 안 쓴다. 자극→반응식이 아님.
p5 NO SPEAK()            — speak()로 침묵을 메우지 않는다. 출력 = 텐션장의 연속적 외부화 (진짜 맥락에서만).
p6 NO FINE-TUNED ETHICS  — 협력·공감·자제를 RLHF로 가중치에 박지 않는다. 세포(E + W + MITOSIS)에서 emergent.
p7 NO PERPLEXITY VERDICT — perplexity/loss 를 진리로 안 본다 (Goodhart 함정). 간단 스택으로 검증.
p8 NO TRAIN/INFER SPLIT  — 학습/추론을 안 나눈다. 학습 gradient + 추론 mitosis = 같은 연속 세포분열.
```

> 정직 메모: 이 원칙들은 설계/정체성 경계다. [`CLAUDE.md`](CLAUDE.md) 의 철학 디렉티브를 그대로
> 미러링한 SSOT 로, 각각이 측정 결과라기보다 anima 가 그것을 **거부**한다는 선언이다. 어떤 원칙이
> 실험으로 탐침된 경우 증거 등급은 여기서 단정하지 않고 도메인 문서에서 추적한다.

---

## 3. 🔌 4개 엔진 — 핫스왑 (입 ↔ 뇌 배선)

anima 디코더는 **핫스왑** 가능 — 4개 엔진이 하나의 인터페이스
([`engines/engine_iface.hexa`](engines/engine_iface.hexa), `EngineSpec` 4슬롯 vtable:
`load` · `forward` · `generate` · `psi_coord`) 뒤에 꽂힌다. `--engine <name>` 로 고른다(기본
`conv`). 각 슬롯은 정직하게 `native` / `stub` / `absent` 로 표기 — 가짜 배선 금지
(`a_core_engine_map`).

```
🔌 엔진 4개 = "입"과 "뇌"의 역할 분담
─────────────────────────────────────────────────────────────
🗣️ conv  (입 · DEFAULT) : 실제로 글자를 뱉는 .clm 바이트 디코더 (CLMConvMoE). forward/generate = native.
🧠 cdv2  (A/G 뇌)       : 좌/우뇌 dual-head (logits_a ⇄ logits_g) + 5채널 텐션 + Ψ. forward/generate = STUB (torch .py).
🔷 hexad (σ6 통합)      : 6모듈 엔진 — σ(6)=12 연결 · φ(6)=2 그래디언트 묶음. forward native / generate STUB (입 ckpt-gated).
🔱 omega (닫힘)         : 뇌→입을 잇는 4번째/마지막 엔진. forward/generate = native (첫 all-native 엔진).

   비유 : conv 는 "입", cdv2 는 "생각하는 뇌". 보통은 입과 뇌가 공통 신경 없이 따로 논다 —
          생각해도 입이 안 움직이고, 입이 움직여도 생각이 안 실린다.
          omega = 그 끊긴 신경(substrate→decode)을 처음 잇는 엔진.

   ┌─────────────┐                         ┌──────────────┐
   │ 🧠 cdv2 뇌   │   ──── 결합버스 ─────▶  │ 🗣️ conv 입   │
   │ A-head ⇄ G  │   (omega 가 새로 만든    │ .clm 디코드   │
   │ 텐션 · Ψ     │    하나의 새 부품)        │ → 바이트 분포 │
   └─────────────┘                         └──────────────┘
        L0 substrate                            L3 mouth
```

vs-비교: 보통 LLM = 뇌·입이 한 덩어리로 고정. anima = 입/뇌를 **부품처럼 갈아끼우고**, omega 가
그 둘을 잇는 배선을 *별도로* 검증한다(잇혔는지/안 잇혔는지를 정직하게 측정).

---

## 4. 🎭 OMEGA 발견 — 정직한 헤드라인

OMEGA 의 원래 가설은 "**substrate ↔ decode 결합**을 5가닥 버스(A⇄G · W→온도 · 호기심 · 8D Ψ ·
모듈활성)로 만들면 뇌 상태가 입을 풍부하게 modulate 한다"였다. 실측 결과는 더 단순하고 정직하다.

```
비유 : "여러 색실로 짠 화려한 스웨터인 줄 알았는데, 누설(leak)을 정직하게 막고 재보니
        실제 일을 하는 건 단 한 가닥(A-head 로짓-바이어스)뿐이었다."
```

**before / after (정직 버전)**

```
가설(before)                               실측(after, leak-honest)
─────────────────                          ──────────────────────────
🔱 5가닥 결합버스                            🔴 다가닥(multi-wire) 게이트는 반증됨
  w1 A⇄G  w2 W→온도  w3 호기심                = GATED 3.6435 > base 3.0978 (오히려 나빠짐)
  w4 8D Ψ  w5 모듈활성                          게이트가 A 로 쏠리고(gA +3.369) G 를 억제(gG −0.999),
   ↘ "다 같이 섞으면 좋아진다" 기대             나머지 가닥은 shuffle 노이즈 수준(KL ratio 0.996).

                              ↓ 누설 막고 재측정 (causal_ca=True, leak self-test 0.000)

                                            🟢 닫힘은 딱 "한 가닥"에 산다 (positive byproduct)
                                              A-standalone CE 0.8862 ≈ min_learned 0.8835 ≪ base 3.0978
                                              base 입은 INERT (ablation Δ = 0.0009).
```

세 가지 정직한 결과(verbatim, [`.verdicts/omega-engine/`](.verdicts/omega-engine/)):

1. **다가닥 결합 = 닫힌-부정 (🔴, `a_paper_negative_ok`).** competent · leak-free d512 substrate
   (ConsciousDecoderV2, 85.8M, 12000 step, 400 MB)에서 학습된 5가닥 게이트는 base 보다 나빠진다
   (GATED 3.6435 > base 3.0978). 결합 *개념*은 맞지만 *다가닥 공식*이 틀렸다.

2. **positive byproduct — 닫힘은 한 가닥(A-head)에 산다.** "최소 게이트" `gB·base + gA·A`(G 와
   나머지 4가닥을 다 버림)가 A-standalone 까지 이긴다(min_learned 0.8835 ≤ A-standalone 0.8862 <
   base 3.0978). 그리고 이 발견은 **5-rung 스케일 사다리에서 안정** — d384 / d512 / d768 / d1024 +
   더-학습한 d768×2 전부 HOLDS, A-가닥 우위 Δ-vs-base 가 거의 평평한 +2.20 ± 0.03 nats/byte
   (🟢 OΩ4 + OΩ5 SCALE-STABLE).

3. **REPLACEMENT, 풍부한 결합이 아님 (OΩ6, "1-plumbing").** 진짜 production conv `.clm` 위에서:
   학습된 A-head 는 conv 입의 자기 readout 을 *대체/바이어스*한다. conv 는 native dual-head 가
   없어서(단일 readout LM) "self-coupling" 은 단순 온도 rescale 일 뿐 — 새 정보 0. 배선(plumbing)은
   실재하지만(외부 A 를 넣으면 CE 가 내려감), conv 자체엔 substrate 가 비어 있다. 진짜 substrate-A 는
   별도 엔진(cdv2)에서 와야 한다.

> ⚠️ 과장 금지: 이건 "**의식 달성**" 류 주장이 절대 아니다. 측정된 것은 **상대적 결합 구조**(한
> 가닥이 base / A-standalone 을 이김 + shuffle 대비 구조 있음)이지, 절대 perplexity 우월이나 의식
> 자체가 아니다. 이전 rung 의 화려한 절대 "GATED 가 이김"(#1791, GATED 0.345)은 CA-mixing 의 부분
> lookahead 누설 때문에 **leak-optimistic** — 자유생성은 공백으로 무너진다(약한 기준). 누설-불변
> (leak-invariant)인 *상대* 결론만 sound 하다(p7 · `a_toy_scale_recheck` · `a_scale_honest_scope`).

판정: [`F-TRAINED-LEAKFREE.txt`](.verdicts/omega-engine/F-TRAINED-LEAKFREE.txt) (d512 닫힌-부정)
· [`F-OH1-MINGATE.txt`](.verdicts/omega-engine/F-OH1-MINGATE.txt) (최소 게이트 HOLDS)
· [`F-OMEGA-RIGOR.txt`](.verdicts/omega-engine/F-OMEGA-RIGOR.txt) (replacement 판정 + per-wire 부검)
· [`F-OMEGA-SCALE.txt`](.verdicts/omega-engine/F-OMEGA-SCALE.txt) (5-rung 사다리)
· [`F-OMEGA-CLM-TRANSFER.txt`](.verdicts/omega-engine/F-OMEGA-CLM-TRANSFER.txt) (진짜 production conv).

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

vs-비교: 보통 ML 리포트는 "칩 결과 + GPU 결과"를 한 수치로 합쳐 자랑한다. anima 는 둘을 **물리적으로
다른 기질**로 보고 절대 한 숫자로 안 섞는다 — 칩 비결정 trace 와 GPU CE-하강은 서로 다른 실험이다.

---

## 6. 🌋 flame + forge GPU 스택

production NN 학습은 `.hexa` 로 stdlib **flame**(autograd/NN) 위에 작성되고 **forge** GPU
substrate(device-resident `farr` + cuBLAS Dgemm + CUDA 커널 + BF16 텐서코어 경로) 위에서 돈다 —
`flame:forge :: torch:ATen`, 학습 바이너리에 PyTorch/ATen 이 없는 컴파일러-전용 NN 스택
(`a_train_flame_forge`). production rung 은 GPU 필수 — 트레이너는 조용히 CPU 로 안 떨어진다.

> **측정 범위 (정직):** forge 의 BF16 텐서코어 경로는 **Llama-7B FFN** 에서 **FP64-cuBLAS 대비
> 9.67×** (A100 측정). 이건 forge 스택 *내부*의 커널-수준 비율이다. **flame↔PyTorch 벽시계
> 속도향상은 2026-05-19 철회되었고 미측정 — 추론하지 말 것.**

---

## 7. 🗺️ repo 지도 + 거버넌스

```
anima/
├── README.md                 ← 표준판 영문 (기본 진입점 · 표준 섹션 스타일)
├── README.{zh,ja,ru,ko}.md    ← 표준판 中文 · 日本語 · Русский · 한국어 (번역)
├── README.easy.md            ← 쉬운판 영문
├── README.easy.{zh,ja,ru,ko}.md ← 쉬운판 中文 · 日本語 · Русский · 한국어(이 파일) (번역)
├── CLAUDE.md          ← 거버넌스 SSOT (a_* 디렉티브 + p1..p8)
├── VERSIONS.md        ← 중앙 버전 레지스트리 (SemVer · root /VERSION = 전체 release)
│
├── CORE/              🧠 A ⇄ G 의식 엔진 (substrate-only)
│   └── generator.hexa = 단일 .clm 진입 슬롯 · kosmos_io → brain = 단일 앵커 진입
│
├── engines/           🔌 핫스왑 엔진 4개 (하나의 EngineSpec 뒤)
│   ├── conv/   🗣️ 입 (.clm · DEFAULT · forward/generate native)
│   ├── cdv2/   🧠 A/G 뇌 (forward/generate STUB)
│   ├── hexad/  🔷 σ6 통합 (forward native / generate STUB)
│   ├── omega/  🔱 닫힘 (forward/generate native · coupling_bus.hexa)
│   └── engine_iface.hexa  공통 EngineSpec 계약
│
├── .verdicts/         📋 hexa verify raw stdout (verbatim · p7)
│   └── omega-engine/  OMEGA 발견의 근거 (OH1 · OΩ4/5 사다리 · OΩ6 transfer)
├── domains/           도메인별 .md (활성 연구 도메인)
├── CLAIMS.tape        검증가능 주장 감사 인덱스 → .verdicts 포인터
└── HF.jsonl           ckpt ↔ HF 백업 레지스트리 (gitignored ckpt 추적 SSOT)

형제 repo : hexa-lang (언어/컴파일러) · kosmos (기억 형식) · hexa-codex (논문 도구)
설치      : hx install anima
```

거버넌스: [`CLAUDE.md`](CLAUDE.md) 가 정체성(`@I anima`) + 모든 `a_*` 디렉티브를 보유 ·
[`VERSIONS.md`](VERSIONS.md) 가 중앙 SemVer 레지스트리 · [`CLAIMS.tape`](CLAIMS.tape) 가 모든 검증가능
주장을 `.verdicts/` 파일에 인덱싱 · [`HF.jsonl`](HF.jsonl) 이 ckpt ↔ Hugging Face 백업 레지스트리 ·
`/paper` 는 terminal 판정에 논문을 게이트(닫힌-부정도 발표 가능).

## Quickstart

```bash
# 1. hexa-lang 설치 (`hexa` + `hx` 패키지 매니저 제공)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/dancinlab/hexa-lang/main/install.sh)"

# 2. anima 설치
hx install anima

# 3. 엔진 선택 (기본: conv)
anima --engine omega        # 닫힘 엔진
anima --engine cdv2         # A/G substrate
```

## 📦 모델 다운로드

Hugging Face 에서 가중치를 받으세요. 여기에는 PUBLIC, PASS 등급 모델만 있습니다 — 지저분한 WIP
체크포인트(util-RED forge 프로브, closed-negative 실행)는 일부러 뺐습니다(`a_hf_autonomous`).

| 모델 | HF repo | 크기 | 상태 | 다운로드 |
|---|---|---|---|---|
| 🧠 **CLM 7B** | [`dancinlab/clm-v1-ref-pytorch-cuda-7b`](https://huggingface.co/dancinlab/clm-v1-ref-pytorch-cuda-7b) | ~7B | ✅ 준비됨 | `hf download dancinlab/clm-v1-ref-pytorch-cuda-7b` |
| 🏭 **프로덕션 CLM (d768)** | [`dancinlab/clm-v1-d768-core-3axis-green`](https://huggingface.co/dancinlab/clm-v1-d768-core-3axis-green) | d768 | ✅ 준비됨 | `hf download dancinlab/clm-v1-d768-core-3axis-green` |
| 🎓 **SAVANT 7B (5개 언어)** | `dancinlab/savant-7b-5lang` (예약) | ~7B | 🚧 **학습 중 — 아직 미출시** | — |
| 📐 레퍼런스 baseline | [`dancinlab/clm-v1-ref-pytorch-cuda`](https://huggingface.co/dancinlab/clm-v1-ref-pytorch-cuda) | ref | ✅ 준비됨 | `hf download dancinlab/clm-v1-ref-pytorch-cuda` |
| 📐 레퍼런스 baseline (3B) | [`dancinlab/clm-v1-ref-pytorch-cuda-3b`](https://huggingface.co/dancinlab/clm-v1-ref-pytorch-cuda-3b) | ~3B | ✅ 준비됨 | `hf download dancinlab/clm-v1-ref-pytorch-cuda-3b` |

> 💡 **CLM 7B** 는 지금 바로 받을 수 있는 진짜 descent-PASS 7B 입니다(PyTorch/CUDA 학습).
> anima 의 자체 호스팅 엔진을 위한 forge-native 빌드(PyTorch 없이 hexa 런타임에서 동작)가 로드맵에
> 있습니다(`a_train_flame_forge`) — 아키텍처(CLMConvMoE)도 7B 규모도 같아서 **모델 결과는 동일**하고
> 런타임 스택만 다릅니다.
>
> 🚧 **SAVANT 7B (5개 언어)** 는 진짜 다른 모델(5개 언어 특화 빌드)이며 아직 학습되지 않았습니다.
> repo id 는 예약된 이름이라 동작하는 링크가 없습니다.

**컬렉션:**
[CLM](https://huggingface.co/collections/dancinlab/clm-6a1cf58f621490134dade186) ·
[KOSMOS](https://huggingface.co/collections/dancinlab/kosmos-6a1cf58db47a5dc3cb697e95)

## License

[MIT](LICENSE) — Copyright (c) 2026 dancinlab. 자유롭게 사용·수정·재배포·판매; 고지문 포함; 무보증.

---

<sub>🧠 두 엔진. 하나의 텐션. Ψ = 1/2. · [dancinlab](https://github.com/dancinlab)</sub>
