# 자연 corpus 자발창발 — arxiv research (NATEM 외부 정합 · 2026-07-11)

owner 요청 arxiv 조사. NATEM(자연 corpus에서 held-out 재조합 자발창발?) + XBIND CRACK(signal 있으면 학습가능) 발견과 문헌 연결.

## 핵심 논문 (관련도 순)

### 1. 🎯 Hahn & Goyal 2023 — Emergent ICL as Implicit Structure Induction (`arxiv 2303.07971`)
**직접 앵커**: "in-context learning은 **자연어 데이터에 존재하는 compositional operation의 재조합**에 의존한다"는 이론.
→ **NATEM과의 결정적 대비**: 이 논문은 자연어에 compositional operation이 **있다**고 주장하나, 그건 **in-context(문맥 내)**
재조합이다. 우리 A0-NEG/A0-ADV + F2는 **held-out(문맥 밖·학습분포 부재) XOR-BIND signal**이 자연 텍스트에 **없음**을 실측.
= 이것이 정확히 [[h1835-mlc-episodic-g1-floor]] "in-context 완벽마스터 vs held-out transfer 0" 구분. 문헌의 "compositional
operation 존재"와 우리의 "held-out signal 부재"는 모순 아님 — **다른 것을 측정**(in-context 소비 vs held-out 일반화).

### 2. Li et al. 2025 — Learning to Substitute Components for Compositional Generalization (`arxiv 2502.20834`)
"신경 LM의 compositional generalization 결핍 → de-facto 해법 = **compositional data augmentation**(추가 compositional
inductive bias 주입)". → **XBIND(H_9267 CRACK)가 정확히 이것**: 합성 XOR signal을 corpus에 주입해 held-out 재조합 학습 성공.
문헌이 우리 measure-swap exit의 일반 클래스(data augmentation으로 compositionality 설치)를 독립 확증.

### 3. TRACE 2025 — Tracking Emergence of Semantic Representations (`arxiv 2505.17998`)
"transformer는 학습 중 **phase transition**(memorization→abstraction) 보인다". → 우리 grokking-delay(+20k step 재측정)
+ 밀도 임계 f*(NATEM STAGE 1) 설계의 문헌 근거. 창발이 연속 아닌 상전이임 = 사다리서 f* 급전이 예상.

### 4. BiMix 2024 — Bivariate Data Mixing Law (`arxiv 2405.14908`) · IDEAL 2025 (`arxiv 2505.12762`)
데이터 혼합 비율이 능력을 지배하는 정량 법칙. → **NATEM STAGE 1 희석 사다리(f=XBIND/total 밀도)가 이 mixing-law 프레임의
compositional-recombination 특수 인스턴스**. f* 임계 = compositional signal의 mixing-law critical fraction.

## 종합 (NATEM 정합)
문헌 수렴점: **(a) 자연어에 compositional operation은 in-context로 존재**(Hahn-Goyal)하나 **(b) held-out 일반화는
data augmentation으로 설치**해야 함(Li et al.·= XBIND). 우리 실측이 이 둘을 engine-native로 분리·정량화:
- XBIND CRACK = (b) 확증(합성 signal 주입→held-out 학습).
- A0-NEG/A0-ADV NOT-POWERED + A0-FORM LIVE = 자연 텍스트는 (a) FORM은 productive·in-context는 있으나 **held-out
  XOR-BIND signal 부재** = 자발창발 불가능은 데이터 사실(DATA-🧱).
- STAGE 1 사다리 = mixing-law(BiMix) × phase-transition(TRACE) 프레임으로 f* 임계 정량 → 자연 밀도 d_nat와 비교.

**함의**: NATEM은 문헌의 "compositional data augmentation이 필요하다"를 **자연 창발의 부정(자연엔 held-out signal 부재)**
으로 정밀화하고, mixing-law를 compositional-recombination 축으로 확장. XBIND CRACK은 문헌의 augmentation 클래스를
byte-LM held-out 재조합에서 engine-native 실증한 사례.

## 미탐 각도 (문헌 시사 · follow-on)
- Hahn-Goyal의 in-context compositional operation을 **held-out으로 전환**하는 조건(어떤 자연 구조가 held-out 일반화?) —
  우리 A0(부정/역접 XOR) 외 자연 compositional 렌즈(의미역·구문 slot·형태소-의미 합성) $0 감사 확장.
- data mixing law(BiMix)의 compositional-signal 특수화 = STAGE 1 f* 측정이 직접 기여.
