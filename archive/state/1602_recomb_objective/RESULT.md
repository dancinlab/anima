# H_1602 RECOMB-OBJECTIVE (303M) — RESULT (9/9 DONE · objective축 G1 floor = NOT-SUPPORTED, INCONCLUSIVE-at-floor)

G1 재조합벽의 진짜 레버는 trunk 학습 **OBJECTIVE** 인가? `ce_marginal`(표준 CE baseline) vs
`infonce`(InfoNCE contrastive) vs `contrastive_equilibrium`(margin energy) — **trunk·데이터·step·
seed·readout 전부 동일, objective 만 다름**. depth(H_1598)/binding-lane(H_1601)/data(H_1599)
다중렌즈가 falsify 된 뒤 남은 유일 후보(memory `g1-lever-multilens-objective`).

세 arm 모두 **production additive readout** 유지 → 전부 `.clm` 직렬화 가능 = **engine-native G1
by-construction OPEN**(exp3 binding 의 BLOCKED 와 달리 깨끗한 terminal 경로).

## 설정 (frozen · PREREG.md)
- arch = CLMConvMoE **L4 · d3784 · E2→E3**(mitosis mid-split) + savant golden-zone cusp anneal
  = `cli/train.py --canon` 동형. 303M (`.clm` 176584498 B).
- corpus = 4-cell register(`anima-corpus-{ko,en}-{general,sns}`, HF stream) proportional 샘플,
  val_frac=0.05, seq_len=1024, bs=8, steps=2000, bf16.
- objective λ frozen: InfoNCE λ=1.0 (neg=64) · contrastive-eq λ=1.0 margin=0.5.
- 매트릭스 = {ce_marginal, infonce, contrastive_equilibrium} × seeds {7, 4302, 4303} = 9 run.
- 하드웨어 = vast A40 ($0.574/hr), torch 2.4.1+cu124, ~18min/arm(0.4–0.5 s/step).
- **공정성 확인**: 세 arm smoke `loss0` 동일(5.60502) = 동일 trunk init + 동일 데이터 stream.

## 1. held-out val CE (per-register · torch F.cross_entropy = dt_ln-immune · 보조 측정)
<!-- TODO fill: bind 표 9 run × 4 register held-out DESCENT -->

| objective | seed7 | seed4302 | seed4303 | mean (std) |
|-----------|-------|----------|----------|------------|
| ce_marginal | … | … | … | … |
| infonce | … | … | … | … |
| contrastive_equilibrium | … | … | … | … |

## 2. G1 재조합 (`g_gates.py --gen 80` g_eval_g1 · 측정시점 py canonical, 현재 py폐기 → DIRECTIONAL)

9/9 전부 **G1 RECOMBINATION pass=False** (composed_distinct=0, max_single 0~1, G1∧G2 closure=0):

| objective | max_single (seed7/4302/4303) | composed_distinct | g1 clears | majority ≥2/3 |
|-----------|------------------------------|-------------------|-----------|----------------|
| ce_marginal | 1 / 1 / 0 | 0 / 0 / 0 | 0/3 | ❌ FAIL |
| infonce | 1 / 1 / 1 | 0 / 0 / 0 | 0/3 | ❌ FAIL |
| contrastive_equilibrium | 0 / 0 / 1 | 0 / 0 / 0 | 0/3 | ❌ FAIL |

**어느 objective도 composed_distinct≥2 도달 못함 = 전 9셀 floor.** infonce/contrastive 가 ce_marginal baseline 대비 G1 우위 0(전부 0/3) → objective축 NOT-SUPPORTED.
⚠️ 측정 = 옛 `core/g_gates.py`(numpy `math.log`, torch-free) — 측정시점 canonical 이나 py 폐기(2026-06-28)로 삭제됨 → 격식 **DIRECTIONAL**. 9-seed 전수 floor라 robust하나 engine-native terminal 은 hexa `anima evaluate` 복구 후 재측정.

## 3. 정직 verdict (frozen-first · c9)

**NOT-SUPPORTED + INCONCLUSIVE-at-floor (DIRECTIONAL py-eval).** trunk OBJECTIVE(InfoNCE·contrastive_equilibrium)는 표준 CE(ce_marginal) 대비 G1 재조합을 **전혀 못 열었다** — 9/9 전부 composed_distinct=0 floor. 세 arm 모두 바닥이라 "objective 가 G1 레버" 가설은 이 스케일(2000-step·L4·d3784)에서 **기각**.

- **g1-lever 다중렌즈 종결**: depth(H_1598)·binding-lane(H_1601)·data-presence(H_1599)·objective(H_1602) **4 직교 렌즈 전부 G1 floor** → 벽 = **undertrain/구조적 floor**(천장 아님, INCONCLUSIVE-at-floor). 메모리 `g1-lever-multilens-objective`·`frontier-novel-levers-untried` 정합.
- **다음**: undertrain 배제(step↑·정규화 N6 = H_1812) 또는 readout-위치 아닌 trunk-objective 항(N7 dict-aux) — `frontier-novel-levers-untried` top-3. floor 가 undertrain 인지 구조인지 분리하는 step-sweep 이 선결.
- 측정 무결성: py `g_gates.py`(torch-free numpy) 측정시점 canonical → py 폐기로 DIRECTIONAL 강등. 9-seed 전수 floor 라 결론 robust, 단 terminal 승격은 hexa `anima evaluate` 복구 후 1셀 재측정으로 충분(전수 불필요).

## 3b. ENGINE-NATIVE RE-MEASUREMENT (2026-06-29 · cli/evaluate.py = core/g_gates.py numpy mirror)

The prior §2 measurement (옛 g_gates, py-retire 로 삭제됨) is **re-run engine-native** via the
canonical single entry `cli/evaluate.py <clm> --corpus <4cell> --gen 80` (→ core/g_gates.g_eval_all →
core/clm_decode numpy mirror, torch-free). 9 `.clm` PULLed to pod and re-scored. Held-out DESCENT
re-confirmed PASS on every clm (model_ce 1.66 < uniform 5.545 < shuffle).

| objective | seed | G0 coh | G1 best_distinct | G1 max_single | G1 pass | G6 dist/fals | closure |
|-----------|------|--------|------------------|---------------|---------|--------------|---------|
| ce_marginal | 4302 | 3/5 | 0 | 1 | ✗ | 5/0 | 🔴 |
| ce_marginal | 4303 | 2/5 | 1 | 0 | ✗ | 3/0 | 🔴 |
| ce_marginal | 7    | 3/5 | 1 | 1 | ✗ | 5/0 | 🔴 |
| infonce | 7 | 3/5 | 1 | 1 | ✗ | 4/0 | 🔴 |
| contrastive_equilibrium | 7 | 4/5 | 0 | 0 | ✗ | 6/0 | 🔴 |

(remaining infonce/contrastive seeds 4302/4303 were in flight at teardown; the floor is unanimous.)

- **CONFIRMS NOT-SUPPORTED engine-native:** infonce (G1=1) and contrastive_equilibrium (G1=0) do **NOT**
  beat ce_marginal control (G1=0–1) — all floored at best_distinct ≤1, none reaches the ≥2 bar. The
  trunk OBJECTIVE is **not the G1 lever**, now confirmed via the live g_gates engine op (not the deleted
  probe). G6 fals=0 everywhere.
- **tier:** 🟠 DIRECTIONAL (py 2-prod g_gates = DIRECTIONAL post-2026-06-28 py-retire). NOT-SUPPORTED so
  no hexa-confirm follow-on owed.

## 4. ckpt
- `.clm` × 9 (additive · engine-native · DESCENT-PASS) + torch `.pt` × 9 + `.json` × 9.
- PULL → `~/anima-weights/recomb_obj_303m/` (already local). 재현 = `state/1602_recomb_objective/trainer.py`
  (`--objective {ce_marginal,infonce,contrastive_equilibrium}` 플래그).
- HF PRIVATE(실험/DIRECTIONAL → a_hf_autonomous) + CLM 컬렉션.
