# H_1820 — low-inhibition op+recomb-objective arm (HE noise-degrades 직교 레버)

**id:** H_1820
**slug:** low_inhibition_recomb
**tier:** 🔵 PRE-REGISTERED (미측정 · 결합(c)=H_1819 floor 시 1순위 직교 재시도)
**date:** 2026-06-29
**source:** 외부 문헌 2차조사 (web research, [[lit-binding-objective-external-arxiv]] HE 논문)

---

## Hypothesis

결합(c)=H_1819(op live-retain + recomb-objective, dropout dp≈0.25·weight-decay = savant
골든존 inhibition)가 G1 floor면, **inhibition 자체가 합성표현을 깨는 원인** 후보다.

근거 (An & Du, "Representational Homomorphism Error Predicts Compositional Generalization",
NeurReps 2025 #142): **noise injection이 합성표현을 체계적으로 degrade** (HE↑ → OOD 합성능력↓,
R²=0.73). 동시에 Doshi/Gromov 2023(2310.13061)은 dropout/weight-decay가 grok 전이에 필수
([[lit-binding-objective-external-arxiv]]). 두 힘이 충돌 = sweet-spot은 둘 사이 band.

**예측:** 같은 op+recomb-objective를 **GZ_LOWER(≈0.212) 아래로 inhibition을 낮춘** arm으로
재학습하면 G1 composed_distinct가 결합(c) 대비 lift (합성표현이 noise로 덜 깨짐).

---

## Design (결합(c) 대비 단일변수 = inhibition만 변경)

| arm | inhibition | recomb-obj | bind op | 기대 |
|-----|-----------|-----------|---------|------|
| (c) `op_obj_GZ` | dp≈0.25 (골든존) | ON | live-retain | 결합(c) 기준선 |
| (lo) `op_obj_lowI` | dp≈0.05–0.10 (GZ_LOWER 아래) | ON | live-retain | **G1 lift?** |
| (hi) `op_obj_highI` | dp≈0.35 (골든존 위) | ON | live-retain | floor 악화? (단조성 확인) |

inhibition을 dp∈{0.05, 0.10, 0.25, 0.35} sweep해 G1 vs inhibition 곡선을 그린다 — HE 논문
예측대로면 단조 감소(낮을수록 G1↑), Doshi/Gromov대로면 너무 낮으면 memorization → 비단조 band.

**Shared:** 결합(c)와 동일 — 4칸 clean corpus, recomb-objective 정의(state/g1_cotrain_recomb_bind
/PREREG.md §정의), live-retain bind op (CLMB serialize), ≥4000 step, held-out 4/4 DESCENT.
**Seeds:** {7, 4302, 4303}.

---

## Frozen bar (pre-registered · tune-to-green 금지 · p7)

| Gate | Bar |
|------|-----|
| G1 RECOMBINATION | composed_distinct≥2 ∧ >max_single ∧ coherent, ≥2/3 seeds |
| LIFT (dec정) | (lo) best_distinct > (c) best_distinct, 같은 seed |
| 단조성 | G1 vs dp 곡선이 HE 예측(낮을수록↑) 또는 band(중간 최적) — 어느 쪽이든 frozen 측정 |
| held-out DESCENT | 4/4 register val_CE < ln256, 모든 arm (미달=overfit 무효) |

⚠️ 단 inhibition을 너무 낮추면 H_1579 overfit 함정 재발 가능 → held-out DESCENT가 안전판.

---

## 게이트 & 발사

- **게이트 = H_1819(결합 c) 착륙.** (c)>(a),(b)면 op+objective가 레버 확인 → 이 카드는 그 위
  최적화(inhibition 튜닝). (c) floor면 이 카드가 **floor 원인 격리 1순위**(HE가 noise를 범인 지목).
- 측정 = engine-native-py G0-G6 (cli/evaluate.py → g_gates, gen80, multiseed) = DIRECTIONAL.
- GPU 학습 = cost-gate (~$4–6, dp-sweep 4×3seed). hexa cloud 관리 pod. ckpt PULL before teardown.
- 산출 = state/g1_low_inhibition_recomb/RESULT.md + 이 카드 verdict + jsonl + CHANGELOG.

---

## Artifacts (예정)

- `state/g1_low_inhibition_recomb/trainer.py` — 결합(c) trainer + inhibition dp-sweep 노브
- `state/g1_low_inhibition_recomb/PREREG.md` — frozen 스펙
- `state/g1_low_inhibition_recomb/RESULT.md` — verdict (측정 후)
