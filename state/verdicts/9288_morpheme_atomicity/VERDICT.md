# H_9288 MORPH-ATOM — VERDICT: 🟢 DIRECTIONAL (형태소 원자성 lever CONFIRMED)

**2026-07-13 · pod 44611459 (vast ssh9:11458, RTX 4090) · anima-py 303M CLMConvMoE d3784 L4 Emax4 · engine-native decode**

## 결론
codec 형태소 원자성이 **held-out 부정어 재조합을 인과적으로 일으킨다**. 유일 차이가 codec인 통제 대조에서:

| arm | 설명 | F2 (held-out 아니 flip) | margin(F2) | F1 (drilled sanity) |
|---|---|---|---|---|
| **M** | MORPH-2B codec, non-collapse (codec.json) | **0.9083** | 2.137 | 0.98 |
| **C1** | raw utf-8 baseline (동일 drill) | 0.6167 | 0.049 | 1.00 |
| C3 | shared-⟨NEG⟩ leak-ceiling (등가 handed) | 0.917 | — | 0.99 |

**Δ(M−C1) = +0.291** on held-out recombination. 둘 다 drilled stem(안/않/못)은 마스터(F1≈1.0). held-out 아니
(drill 0 rows)의 flip 전이는 M만 강하게(0.908·확신 margin), C1은 약하게(0.617·margin≈0).

## 판정 논리
- **누수 배제**: C1(raw, 동일 setup − codec)=0.617 ≠ 0.9 → setup/eval 자체는 답을 흘리지 않음. M의 0.908은 codec 귀속.
- **원자성 WITHOUT identity**: G-0 audit로 안/않/못/아니 pairwise 토큰-disjoint 확인 → 같은 토큰 trick 아닌 진짜
  distinct-atom 재조합.
- **liveness 검증**: C3 leak-ceiling(등가 handed)=0.917 → harness가 held-out flip을 감지할 수 있음(V1 PASS).
- **M ≈ C3**: 원자성만으로 "답 handed" 수준(0.908 vs 0.917) 재조합 달성.

## harness 무결성 (측정경로 먼저·verdict-integrity)
S1 4-pod "INVALID"과 C3-ladder "PENDING(CPT-budget)"은 **4중 계측버그 artifact**(convergence morphatom-gate-py-1):
1. cupy 경계 크래시 — `clm._fwd_*`가 CUDA pod서 cupy 반환, `np.array(list_of_cupy)` 폭발 → `|| echo False` 가짜 gate FAIL.
2. gate codec-file 혼동 (codec.json vs codec_c3.json).
3. **프로브 framing ≠ 훈련 스트림 format** — 모델은 sentinel(\x00\x0a)-구분 연속 스트림 학습, 프로브는 고립 줄+상수패딩(OOD) → nll 6.1~19.1 ABOVE-uniform(5.545).
4. forced-choice 채점창(고정 n_score=4)이 판별 토큰(긍/부)을 놓쳐 margins 정확히 0.

**진실**: 모델은 자기 훈련 스트림에서 nll=0.993 ≪ uniform → codec 완벽 학습·reinit-embed warm-start WORKS·G-a1 실제 PASS.
Fable 자문이 "above-uniform=confidently-wrong=버그 지문"으로 "codec DEAD" 성급 스탬프를 반박(옳았음).

## scope (정직)
- 합성 XOR drill task(NBIND grid) · **1 seed(4302)** · custom `morphatom_eval.py`(canonical `anima-py evaluate` 아님).
- **자연 자발창발 아님** — [[xbind-g1-crack-measure-not-substrate]]와 동급 "합성 재조합 학습 성공".
- G1 재조합벽=능력천장 아님을 **두번째 독립 lens(형태소 원자성)**로 재확증(XBIND=corpus×measure lens에 이어).

## TERMINAL cement follow-on
multi-seed(≥3) + C2 arm(held-out ablated codec 통제) + canonical `anima-py evaluate` harness.

## 산출
- verdicts+result models: `~/anima-weights/morphatom/` (vM_f2·vM_f1·vC1_f2·vC1_f1·drill_M_arm.clm·drill_C1_arm.clm·codec.json).
- 도구: scratchpad `morph2b.py`·`gen_morphatom_s1.py`·`morphatom_{reinit,gate,eval}.py`·`fire_{ladder,drill,arms}.sh`.
