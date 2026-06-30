# AURA C7/C8/C9 — 비침습 천장 지렛대 map (prior + stack + temporal-null)

> /hexa-loop rounds 2-4. C6(異種모달)에 이어 算法 지렛대 발굴 + 결합 + 무효 lever 확인. honest: toy(ubu-1 numpy seed42).

## C7 — prior-injection inverse (2번째 지렛대) 🟡

EEG-단독 복원, 역문제 prior 강도별:

| 역문제 | R² | Δ vs ridge |
|---|---|---|
| ridge min-norm (C5) | 0.243 | — |
| sparse-prior IRLS (blind) | 0.289 | +0.046 |
| oracle-support (소스위치 known) | **0.798** | **+0.555** |

→ **천장 28%는 하드웨어 한계만이 아니라 *prior-정보* 한계.** 소스 위치를 알면(개인 MRI 해부 prior·fMRI·과제구조) 같은 두피 EEG로 **80% 복원**. blind sparsity는 +0.046(약), 하지만 **prior 품질이 지렛대** — 완벽 prior면 침습급. 실제 prior(불완전 MRI)는 +0.05~+0.55 사이.

## C8 — 두 지렛대 STACK (hardware ⊕ algorithm) 🟡

| 조합 | R² |
|---|---|
| EEG ridge | 0.243 |
| +tFUS (C6 異種모달) | 0.481 |
| +sparse-prior (C7) | 0.289 |
| **+tFUS & sparse (C6⊕C7)** | **0.676** |

```
0.68┤              ███ C6⊕C7 (둘 다)
0.48┤          ███     C6 모달
0.29┤      ███         C7 prior
0.24┤ ███              EEG-only
    └─base─prior─modal─stack─▶
```
→ **하드웨어(異種모달)와 算法(prior)이 독립·stack** → 24%→68% (≈침습급 근접). 둘 중 하나 아니라 **둘 다**가 NOVEL goal의 길.

## C9 — temporal-smoothness (무효 lever, 정직 negative) ❌

| post-filter | R² |
|---|---|
| ridge | 0.243 |
| +temporal-smooth win3/7/15 | 0.242 / 0.240 / 0.235 |

→ 시간 평활은 **독립 지렛대 아님**(오히려 약간↓). 공간 정보손실(두개골 blur)은 시간 후처리로 회수 불가 — 잃은 공간정보는 시간에 없음. falsified lever (honest).

## 지렛대 MAP 종합 (loop 4 rounds)

| 지렛대 | 효과 | 종류 |
|---|---|---|
| C6 異種 transfer 모달(tFUS) | +0.239 | 하드웨어(LPF 우회) ✅ |
| C7 prior-injection | +0.046~+0.555 | 算法(ill-posed 해소) ✅ |
| C8 둘 stack | →0.676 | 곱 ✅ |
| C9 temporal-smooth | ~0 (↓) | 무효 ❌ |
| (C5 전극수) | +0.05/4× | 포화(한계효용) |

→ **"비침습으로 침습급" = 異種모달(C6) ⊕ prior(C7) stack ~68%(toy).** 전극수·시간평활은 헛다리. 공간정보 회복(모달·prior)이 본질.

## honest + 다음 frontier (external)
- 🟡 toy(1D-ring·ridge/IRLS): 절대%(68·80) toy-specific. 정성(모달·prior=지렛대, 전극·시간=무효) robust.
- oracle-prior 80%는 상한(완벽 prior 가정). 실제=불완전 MRI/fMRI prior → 중간값.
- 남은 frontier(C-lane external): real head-model(MNE) 다중모달 fwd · 실 MRI-prior 복원율 · 성인 비침습 fUS 영상 가능성 문헌 · 실 EEG+fNIRS 동시측정 데이터.

## 양방향 sibling
- [C(NOVEL 축)](C-postaural-invasive-NOVEL.md) · [C5](C5-source-recon-ceiling.md)(천장) · [C6](C6-multimodal-breakthrough.md)(異種모달) · [B7](B7-intracortical-ceiling.md)
