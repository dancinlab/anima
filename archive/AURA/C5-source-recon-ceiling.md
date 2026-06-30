# AURA C5 — 비침습 천장 in-silico 측정 (scalp→cortical 복원 R²) 🟡

> NOVEL 축(C) goal의 핵심 측정 — "비침습으로 cortical 정보 몇 %나 복원하나"를 forward/inverse toy로 정량. ubu-1 numpy, seed=42 결정론. verdict `.verdicts/c5-source-recon/run.txt`.

## 모델

```
cortical 소스(64) ──forward(LF: 가우시안 blur σ + skull SNR noise)──▶ scalp(M ch)
                                                                        │
              R² ◀──비교── cortical_hat ◀──inverse(ridge min-norm)──────┘
```
- forward LF = 용적전도/두개골 = 가우시안 공간 blur(σ) + 측정잡음(SNR 20dB). σ↑ = 두개골 두꺼움 = 더 blur(고공간주파 LPF).
- inverse = ridge(min-norm) cortical 추정. R² = active 소스 복원율 = "복원 가능한 cortical 정보 %".

## 결과 — 복원 R²

| M (전극수) | sharp σ0.25 | blur σ0.50 (현실 두피) |
|---|---|---|
| 8 | 0.158 | 0.170 |
| 16 | 0.315 | 0.205 |
| 64 | 0.419 | 0.243 |
| 256 | 0.490 | 0.265 |
| 1024 | **0.542** | **0.279** |

```
R² ▲
0.54┤ sharp ●━━━●━━━●━━━●━━━● (256→1024: +0.05, 포화)
0.28┤ blur  ○━━○━━○━━○━━○      ← 현실 두피 천장 ~28%
    └─8──16─64─256─1024─▶ M
       전극 늘려도 천장서 평평 = blur가 한계
```

## 핵심 발견 (2 천장)

1. **전극수 포화**: 256→1024(4배)가 R² +0.01~0.05뿐. **더 많은 전극 ≠ 더 복원**(C2 법1 한계효용 확정). Nyquist 채우면 끝.
2. **blur 천장**: 현실 두개골 blur(σ0.50)서 **전극 무한대라도 ~28%만 복원**. sharp(얇은 두개골)도 ~54%. → **두개골 LPF가 비침습 물리천장**(C3 예측 정량 확인).

→ **"비침습으로 침습급" 정량 답**: 이 toy서 비침습 복원 천장 ≈ **28% (현실) ~ 54% (이상)** of cortical 분산. 침습(ECoG ~100%)엔 원리적 미달 — NOVEL goal은 "이 천장(28→54%)에 최대 근접"이지 "동일" 불가(feedback-closure-is-physical-limit 정량).

## honest

- 🟡 **toy 모델**: 1D-ring lead-field(실 두부 모델 아님)·synthetic 소스·ridge inverse(여러 역문제 중 하나)·R² active-only. **절대 % 는 toy-specific** — 실 두부 lead-field/deep-inverse면 달라짐.
- **정성 발견은 robust**: ①전극 포화 ②blur 천장 — 둘 다 물리(Nyquist + 두개골 LPF)에서 나오는 일반 결과, toy 무관 성립.
- 실 천장은 real head model(MNE/openMEEG lead-field) + deep-inverse(DeepSIF)로 측정해야 정밀(C-축 다음 frontier, cloud).

## 양방향 sibling
- [C(NOVEL 축)](C-postaural-invasive-NOVEL.md) · [C3](C3-noninvasive-methods-sota.md)(blur가 천장 예측) · [C4](C4-best-stack-design.md)(목표 %-of-ECoG는 이 28~54% 천장에 bound) · [B7](B7-intracortical-ceiling.md)
