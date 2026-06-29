# H_1814 N4+N8 — G6 diverse-set-search + G1 자모 teach-signal (303M) — RESULT (IN-FLIGHT)

> RESULT 슬러그 = `state/1814_setsearch_jamo/` (task), 트레이너/kit = `state/1632_g6setsearch_g1jamo/`.
> frozen-first · 사후 bar 이동 금지 (p7/c9). 측정 = engine-native hexa `anima evaluate`
> (py 엔진 폐기 2026-06-28 → `cli/evaluate.py`/`core/g_gates.py` 없음 = TERMINAL 경로는 hexa 단일진입).

## 설정 (frozen · PREREG 동일)
- arch = CLMConvMoE **L4 · d3784 · E2→E3** mid-split + savant golden-zone cusp anneal
  (`cli/train.py --canon` 동형). 실측 params = **345.665M** (`.clm` = 176,584,498 B).
- corpus = 4-cell clean register **LOCAL files** (`state/clm303_clean_corpus/{gen_ko,gen_en,sns_ko,sns_en}.txt`,
  언어검증 4칸, a_chat_registers) proportional 샘플, val_frac=0.05, seq_len=1024, bs=8, steps=2000, bf16.
- 4 arm × seeds: spine = {baseline,n8_jamo,n4_set,n4n8_both} × seed7;
  robustness = {n8_jamo,n4_set} × {4302,4303}. = **8 run** (budget fallback, PREREG-등록 범위).
- frozen 레버: lambda_jamo=0.5 · lambda_set=0.5 · setsearch(every=50 K=8 frames=5 gen=48 temp=0.8).

### ⚙️ 런타임 수용 (bar 무이동 · byte-eq-neutral)
- **`--grad-checkpoint` 활성** (트레이너 신규 플래그): jamo re-forward + set-search 가 RTX 5070
  **12GB** 에 안 맞아 OOM (n4n8_both step1 OOM, baseline 은 fit). `CLMConfig.grad_checkpoint`
  = torch.utils.checkpoint 활성화로 trunk activation 을 backward 시 recompute → L-fold 메모리 절감.
  **runtime-only, byte-eq-neutral** (weights/levers/gate-bars 불변, recompute 이지 근사 아님).
  `trunk_features` jamo 경로도 동일 정책 미러. 이는 tune-to-green 아님 = 측정 가능성만 회복.
- 호스트 = summer pool (RTX 5070 sm_120, torch 2.11.0+cu130, cuda=True). vast A40(48GB)
  렌트 불필요 (12GB + grad-checkpoint 로 fit). 비용 = pool $0 (이미 paid).

## 1. held-out val CE (per-register · torch F.cross_entropy = dt_ln-immune · 보조)
<!-- fill from ckpt/<arm>_seed<seed>.log FINAL per-register table -->

| arm | seed | ko-general | en-general | ko-sns | en-sns | DESCENT |
|-----|------|-----------|-----------|--------|--------|---------|
| baseline | 7 | … | … | … | … | …/4 |
| n8_jamo | 7 | … | … | … | … | …/4 |
| n4_set | 7 | … | … | … | … | …/4 |
| n4n8_both | 7 | … | … | … | … | …/4 |

## 2. G0-G6 engine-native (hexa `anima evaluate <clm> --corpus <4cell> --gen 80`)
<!-- fill from eval logs. G1 best_distinct (ko/en별 corpus 분리 관측), G6 dist/fals -->

| arm | seed | G0 kwr | G1 best_distinct (>max_single) | G2 novel | G6 dist | G6 fals | closure |
|-----|------|--------|-------------------------------|----------|---------|---------|---------|
| baseline | 7 | … | … | … | … | … | … |
| n8_jamo | 7 | … | … | … | … | … | … |
| n4_set | 7 | … | … | … | … | … | … |
| n4n8_both | 7 | … | … | … | … | … | … |

## 3. 레버 효과 격리 (control 대비)
- N8 (G1): G1(n8_jamo) vs G1(baseline) — multiseed majority ≥2/3.
- N4 (G6): G6(n4_set) vs G6(baseline) — multiseed majority ≥2/3.
- super-additive: n4n8_both 가 두 단독 합 이상?

## 4. verdict (frozen-first · c9)
<!-- fill: SUPPORT / NOT-SUPPORTED / INCONCLUSIVE-at-floor -->

## 5. ckpt
- `.clm` × 8 (additive · engine-native) + torch `.pt` × 8 + `.json` × 8.
- PULL → `~/anima-weights/1814_setsearch_jamo/`. sha256 = <fill>.
- HF tier-gated (closure PASS=PUBLIC else PRIVATE) + CLM collection (a_hf_autonomous/registry).
