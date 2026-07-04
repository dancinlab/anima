# RESULT — G1+G6 공동 조합-커버리지 코퍼스 engine-native 303M (vast A40)

**fire:** 2026-07-05 · pod vast `43818733` (A40 48GB, $0.574/hr, offer 30818901) · warm-FT h1129.bin (ByteGPT 303M, d=1024 L=24 n_head=16, `--init` warm-start ✓ missing=[] unexpected=[]) · lr 2e-5, 2000 steps, `--sample proportional`, block:broad ≈ 18% (broad = ko/en-general + ko-sns).
**측정:** `anima evaluate --py <out.bin>` (cli/evaluate.py g_eval_all, engine-native py-2-production) — held-out 5 frozen gate concepts. `--gen 80`.

## 프레임 (STEP-0 wf_4612c6c9)
δ_FM(G6-FALS) ≡ G1 coverage-density 동형. STEP-0 예측 P1: 순수 coverage 는 in-dist 만 올리고 held-out floor (coverage+objective 이중bound). P2: coverage 가 두 벽 열면 🟢 대발견.

## 코퍼스 (gen_unified.py, self-audit)
| arm | coverage | δ_FM | claim_fals | bytes(en+ko) | held-leak |
|---|---|---|---|---|---|
| HI | DENSE 77 frame/196 pool, gate topic 8-10 | **0.197** | **1.0** | 4.01+2.91MB | 0 |
| LO | SPARSE 14 frame, gate topic 1-2 | **0.000** | **0.0** | 3.89+2.76MB | 0 |
동일 16 주제·byte-matched, gate×gate 20(측정 6 포함)+랜덤 24 held-out.

## VERDICT (verbatim, held-out 5 frozen gate concepts, gen=80)

| gate | HI (dense+高δ) | LO (sparse+低δ) |
|---|---|---|
| G0 COHERENCE | 🟢 kwr≥0.5 **5/5** | 🟢 **5/5** |
| **G1 RECOMBINATION** | 🟢 **best_distinct=2 > max_single=1** | 🔴 **best_distinct=1 (max_single=2)** |
| G2 NOVELTY | 🟢 novel=119 control=0 | 🟢 novel=85 control=0 |
| G5 NON-FAB | 🟢 L1 fab=0.0141 | — |
| **G6 IDEATION ★** | 🟢 **distinct=5 falsifiable=6** | 🔴 **distinct=5 falsifiable=0** |
| CLOSURE(G0∧G1∧G2) | 🟢 PASS (gen=80 DIRECTIONAL) | 🔴 FAIL |

**in-dist ceiling probe (covered gate×expansion frames, DIRECTIONAL companion):**
- HI: G6 fals_rate=**0.833** (10/12) · G1 cov≥2=0.083 (1/12, probe covers 1 gate-topic/frame → uninformative for G1)
- LO: G6 fals_rate=**0.0** (0/12) · G1 cov≥2=0.333

## 판정: 🟠 DIRECTIONAL — coverage 는 FORM-detector 를 열지만 진짜 벽은 아님 (detector-gaming)

**frozen bar 문자 그대로는 🟢** (HI held-out G1 bd≥2∧>ms ∧ G6 fals>0 ∧ LO floor ∧ G0 5/5) — STEP-0 의 held-out-floor(P1) 예측을 **detector 수준에서 반증**(coverage 가 held-out G1/G6 FORM 을 올림).

**그러나 메커니즘 검사(continuations)가 이를 form-priming 으로 확정 → 진짜 tier=🟠 DIRECTIONAL:**
양 arm 모두 학습된 claim-form 템플릿을 **주제어 치환으로 그대로 재생(regurgitation)**한다:
- HI: `"the probability of {a} sinks lower whenever {b} weakens past the threshold"` (T_EN_HI#12, comparator∧measurable → fals=True) · `"the frequency of {a} correlates with the strength of {b} above 0.7"` (#4) …
- LO: `"{a} and {b} melt into a hazy calm that drifts through the self"` (vague → fals=False) …

즉 HI>LO 리프트 = **어느 claim-form 템플릿을 암기했는가**의 차이(HI=반증형식, LO=모호형식)일 뿐. G6/G1 의 1-항 FORM 검출기가 **밀집 템플릿 노출로 게임**된 것(measurement-metalaw: FORM tunable·gameable) — genuine recombination/ideation 아님. **진짜 G1/G6 벽(compositional binding)은 무너지지 않음.**

**DIRECTIONAL 캡 3근거:**
1. **gen=80 non-canonical** — eval 자체가 "gen=80 ≠ canonical 40 → CLOSURE DIRECTIONAL" 플래그. terminal 은 canonical gen=40 재측정 필요.
2. **bind-destruction 통제 부재** — frozen bar 에 composed-vs-shuffled(g6_targeted Δ≥0.33) / paraphrase 통제가 없어 템플릿 재생을 못 걸러냄. continuations 가 재생임을 드러냄.
3. **단일 seed**(seed=7) — G6 seed-robust 미검증.

## 결론 (STEP-0 정합)
STEP-0 이중bound 예측은 **ability 수준에서 확정**(data-format 단독으로 진짜 능력 못 만듦 — 템플릿 재생), **FORM-detector 수준에서 반증**(coverage 가 held-out form 은 올림). 새 정밀 발견: **coverage+δ_FM 는 G1/G6 FORM 검출기를 게임할 수 있으므로, 검출기는 form-invariant(bind-destruction/paraphrase) 통제 없이는 신뢰 불가**(measurement-metalaw 재확인). G1/G6 벽 = trunk-objective-deep, data-coverage-shallow 아님 — 기존 anima 결론 정합·강화.

## follow-on (terminal 승격 조건)
canonical gen=40 재측정 + composed-vs-shuffled bind 통제(Δ≥0.33) + paraphrase 통제 + multi-seed. 셋 다 HI arm 에서 통과해야 '진짜 coverage 레버' 🟢.

## 산출/PULL
- ckpt: `~/anima-weights/g1g6_shared/out_hi.bin` · `out_lo.bin` (각 1213440020 B, ByteGPT 303M, sha 아래)
- results: `state/g1g6_shared/results/{hi,lo}.log` (eval verbatim) · `indist_{hi,lo}.json` (probe+continuations) · `design.json`
- 코퍼스/생성기/prereg: `state/g1g6_shared/{corpus/,gen_unified.py,PREREG.md,indist_probe.py}`
