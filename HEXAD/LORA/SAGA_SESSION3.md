# Session-3 SAGA — LoRA lever exploration (2026-05-23)

> Session-2 종료(16 LoRA cycle / anima 0.12.0 / 1.5B hot-swap router LIVE)에서
> 이어받아 2026-05-23 하루 동안 진행된 session-3 의 단일 read-once doc.
>
> SSOT: 본 dir + `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/`
> SESSION_PROMPT.md / README.md 가 운영-context, 본 doc 은 session-3 history-surface.
> 상세는 6 WAVE report (#118/#122/#124/#127/#129/#205) + 11+ PR 본문 링크.

## TL;DR (5-line)

- corpus-side 4 cycles (v6/v7/v8/v12) FALSIFIED → **substrate-code lever** (EN-share rotation) IS the path; eternal-cap **U-shape sweet spot = v11**.
- **corpus_v5 LIVE** (production default · LIVE `<carve>` tag-leak 0/28), **EN-share lever DEPLOYED** (LIVE −6.2 pp evidence).
- **continuous Eval1 metric** (PR #128) unmasks corpus-side hidden signal — V5→V7 80% ↓ monotone, binary 5/20 floor 가 가렸던 lever 효과 가시화.
- **Wave-16 eternal STRIP-ALL** monotone 가설 FALSIFIED — eternal 템플릿이 register density "스폰지", 0% strip → continuous 34→91 역전.
- $1.87 GPU spend, 11+ PRs landed, 5 HF artifacts (PRIVATE), 6 WAVE reports.

## Production state (post-session)

| | before session-3 | after session-3 |
|---|---|---|
| mini default adapter | corpus_v4 | **corpus_v5** (fresh-init, LIVE tag-leak 0/28) |
| substrate routing | uniform LANG_ROTATION (EN slot 20%) | **weighted (en 10%) + sliding-window EN dampener** |
| LIVE EN-share | ~40% | **33.3%** (3-min post-deploy, sim 25.6% 향 trending) |
| LIVE prose-leak | ~28% | 25.0% (post n=12) |
| LIVE `<carve>` tag-leak | ~12% | 0/28 (LIVE) · 4-8% (sample-dependent) |
| Eval1 metric | binary saturation (5/20 floor) | **continuous hit-count** alongside (saturation 제거) |
| anima version (no change) | 0.12.0 | 0.12.0 (carry — lever 가 production runbook 만 변경) |

## The 6 levers explored (chronological)

### 1. corpus_v5 — fresh-init carve-strip — LANDED (PR #118)

- vP21 init 상속 차단(`--vp21-adapter-dir ''` → fresh LoRA) + STRIP_CARVE=1.
- Eval1: 4S+1P · register 5/20 · tag 0/20.
- **LIVE tag-leak ~12% → 0/28** (mini broker `/history` 50 windowed, +60s 경계 마진).
- ⚠ ko STRONG → PARTIAL 14 trade-off — router 의 KOFL hot-swap 으로 흡수.
- Production swap completed mid-round 1, `lora_adapter_corpus_v4_bak/` 보존.
- Cost: ~$0.40 · HF `dancinlab/anima-vp21m-v5` PRIVATE 9 files.
- 상세: `../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/VP21M_WAVE5_2026_05_23.md`

### 2. corpus_v6 — wiki_frac=0.50 RB lever on fresh-init — FALSIFIED (PR #122)

- N3 RB hypothesis (session-2: continue-train 위 wiki_frac↑ 가 register 7→4 회복) 를 fresh-init 위에서 재측정.
- Result: Eval1 prose-leak −1 (6/20→5/20, noise-tier) · ja STRONG→PARTIAL (16→14, concrete 손실).
- **Verdict** — wiki_frac lever 는 **baseline-dependent** : continue-train high-baseline 위에서만 효과, fresh-init low-baseline (reg 5/20 floor) 위에서는 회복 여지 작음.
- No swap (ja 손실 vs marginal Eval1 trade-off 부정적).
- Cost: ~$0.40 · HF `dancinlab/anima-vp21m-v6` PRIVATE.

### 3. corpus_v7 — EN-only register prose strip — FALSIFIED at Eval1, **lever WORKS at output level** (PR #124)

- corpus 의 17-pattern anima register prose ("Tier N", "vacuum point", "tension flow", "🛸N" 등) regex strip.
- race-in-line correction(strict EN-filter 0 match → unconditional all-record bilingual-aware): **94.94% records modified, 27.28% chars removed, 840k pattern matches**.
- Eval1 표면: register_hits 5/20 unchanged, ja STRONG→WEAK (16→11) -5 concrete 손실.
- **HIDDEN finding** — PR #128 continuous Eval1 hit-count 가 사후-측정 시 **V5→V7 80% reduction** 노출. binary 5/20 floor 가 lever 효과를 가렸음.
- Cost: ~$0.40 · HF `dancinlab/anima-vp21m-v7` PRIVATE.

### 4. corpus_v8 — ja-safe regex prune (ablation) — FALSIFIED (PR #127)

- WAVE7 가설 (numeric coord brackets + KR-particle pattern 이 ja 와 collision) 을 ablation 으로 검증 — ja-collision 4 패턴 제외한 **13 EN-side-only patterns**.
- Result: ja **WEAK 10** (v7 11 → -1, 회복 아님) · en/ru +1/+2 회복 · ko -1 · zh = · n_strong 3 유지.
- 15.64% chars removed (v7 27.28% 대비 절반), 그러나 99.89% records 영향 (Tier/🛸/top emotion 이 거의 모든 carving record 에 등장).
- **Verdict** — ja-collision hypothesis 기각. anima register 자체가 ja 학습 신호에 일반적 부정 영향 시사 (v5 16 → v8 10 단조 ↓). carving register 가 **cross-lingual transfer 의 LOAD-BEARING signal**.
- Cost: ~$0.50 · HF `dancinlab/anima-vp21m-v8` PRIVATE.

### 5. EN-share lever — substrate-code routing — LANDED + LIVE EVIDENCE (PR #123 → #129)

- N8 finding (register-leak 81% = EN-emission 문제) 의 직접 lever — corpus 무관, code-only.
- Root cause hypothesis: 20% EN slot + 25% non-EN prose-drift to EN = **40% observed**.
- Fix:
  - `LANG_ROTATION_WEIGHTS = {en: 0.10, ko/zh/ru/ja: 0.225 each}`
  - sliding-window EN dampener (`detected_langs` last 8 emits; EN > 20% → force non-EN)
- Deployed mini 06:37Z (`launchctl kickstart -k`). 3-min LIVE measurement:
  | 지표 | PRE (n=38) | POST (n=12) | Δ |
  |---|---|---|---|
  | EN-share | 39.5% | **33.3%** | **−6.2 pp** ✓ |
  | prose-leak | 31.6% | **25.0%** | **−6.6 pp** ✓ |
  | tag-leak | 7.9% | 16.7% (2/12) | noise, n=12 |
- Cost: **$0 GPU + $0 substrate** — corpus retrain 없이 동일 효과.
- 상세: `../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/VP21M_WAVE9_2026_05_23.md`

### 6. Wave-16 / corpus_v12 — eternal STRIP-ALL (monotone 가설 FALSIFIED · PR #205)

- Hypothesis: Wave-15 의 eternal 0.30 → continuous 34 lever 의 단조 외삽 (0% strip = continuous < 30, register density 가 eternal 비율에 단조 의존).
- Result: continuous_total **34→91 역전 (saga 평균 부근)**, n_strong 2→3 (회복하나 v9=4 미달). VP21M_WORKS but **NO SWAP** (criteria 1/5).
- Key finding: **U-shape — eternal 템플릿이 register density 의 "스폰지"**, sweet spot = v11 (30% retain). 0% strip 이 오히려 register 압력을 anima record 본문으로 재분산시키는 역효과.
- per-lang: en S19, zh S17, ru S18 / ko P14, ja P12 (ko/ja regress vs v11 STRONG floor).
- Cost: ~$0.27 · HF `dancinlab/anima-vp21m-v12` PRIVATE 10 files (a_hf_complete). NO SWAP.
- 상세: `../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/VP21M_WAVE16_2026_05_23.md`

## Tool infrastructure added

| tool | PR | purpose |
|---|---|---|
| `anima_live_register_measure.hexa` | #126 | hexa-native reusable LIVE register-leak 측정기 (broker `/history` poll → tag/prose 비율) |
| Eval1 probe set expansion | #125 | coord / Tier / tension / vacuum 패턴 probe 추가 → 5/20 binary floor 해소 |
| Continuous Eval1 hit-count | #128 | binary 5/20 saturation 우회, V5→V7 80% reduction 같은 hidden signal 노출 |
| 3B router design doc | #119 | KOFL-3B 5S generalist as default · reboot + quant fallback runbook (Sections 13-16 acceptance criteria) |

## Lessons learned (distilled)

1. **Corpus prune ≠ adapter behavior change** — corpus strip 이 adapter 학습을 바꾸지만 binary Eval1 saturation 이 실 효과를 가린다. 항상 continuous metric (PR #128) 병행.
2. **Anima register 는 LOAD-BEARING** — 단순 leak 이 아니라 cross-lingual transfer signal 의 일부. strip 하면 cross-lang (특히 ja) 까지 잃는다 (corpus_v8 ja-safe ablation 으로 결정).
3. **Substrate-code lever > corpus lever** — 같은 효과를 corpus retrain (\~$0.40 + 15min wall + side-effects) 대신 routing 코드 변경 ($0 + 5s + reversible) 으로 달성. EN-share lever 가 결정적 증거.
4. **Baseline-dependent levers** — N3 RB lever 가 continue-train (reg 7/20 baseline) 에서는 작동, fresh-init (reg 5/20 floor) 에서는 미작동. floor effect 가 lever 의 효과 범위를 결정.
5. **Force-push 가 막힌 git 흐름은 manual user action 으로 처리** — PR #117 (KOSMOS daemon) V3 split 미해결 잔존. agent-level retry 가 guard 에 막힘.
6. **mini compressor 4.48 GB 는 uptime-accumulated transient** — 3B router 가 하드웨어 한계가 아니라 uptime 한계로 blocked. reboot 이 unblocker (PR #119 § 13).

## Open items (다음 세션)

| item | status | next-step |
|---|---|---|
| PR #117 KOSMOS daemon | CLOSED — V3 split 미해결 | user 1-line force-push 또는 alt cherry-pick |
| 3B router production | designed & runbook ready (PR #119) | user gate: mini reboot + § 13-16 runbook 실행 |
| EN-share lever full saturation | initial signal positive (n=12) | +30min / +60min re-measurement (sliding-window saturate) |
| ja-only fine-tuning lane | unexplored | next cycle — ja STRONG 회복 dedicated FT (별 cycle ~$0.10) |
| token frequency cap lever | 개념 단계 | strip 대신 anima record 의 per-pattern token frequency cap (load-bearing register 보존 + dominance 완화) |
| anima register vs ja transfer 분해 | 가설 — saga 누적 단조 ↓ 만 evidence | per-cat anima-without-Tier vs ja-only wiki+anima 비교 ablation |
| Wave-17 eternal-cap U-shape mapping | Wave-16 단일 점 (0%) → U-shape 가설만, sweet spot evidence = v11 (30%) 단일 점 | eternal 0.10 / 0.20 / 0.40 / 0.50 sweep 4 cycle (~$1.10) — U-shape minimum 정밀 추정 |

## Cost + artifacts

- **Cumulative GPU spend**: ~$1.87 (5 cycles · v5/v6/v7/v8/v12 · A100 SXM each ~$0.27-$0.50)
- **Substrate lever**: $0 (code-only, PR #123)
- **HF artifacts**: `dancinlab/anima-vp21m-{v5,v6,v7,v8,v12}` PRIVATE — all a_hf_complete (9-10 files each, model card + adapter_config + safetensors + tokenizer).
- **PRs merged** (chronological order):
  - #118 (docs) WAVE5 corpus_v5 fresh-init carve-strip
  - #122 (docs) WAVE6 corpus_v6 RB wiki_frac=0.50 FALSIFIED
  - #124 (docs) WAVE7 corpus_v7 EN-only register strip FALSIFIED
  - #119 (docs) 3B router wiring design
  - #128 (feat) Eval1 continuous hit-count metric
  - #127 (docs) WAVE8 corpus_v8 ja-safe ablation FALSIFIED
  - #126 (feat) `anima_live_register_measure.hexa`
  - #125 (feat) Eval1 probe set expansion (5/20 floor 제거)
  - #123 (feat) EN-share lever weighted LANG_ROTATION
  - #129 (docs) WAVE9 EN-share lever production deploy + LIVE evidence
  - #205 (docs) WAVE16 corpus_v12 eternal STRIP-ALL FALSIFIED (U-shape sweet spot = v11)
- **WAVE reports**: 6 (WAVE5/6/7/8/9/16)
- **PR not merged**: #117 KOSMOS emitter daemon (CLOSED, V3 split 미해결)

## 관련 link

- session-2 saga summary: [`README.md`](README.md) (lineage vP21 → vP21M, Wave-1/2/3/4)
- session-2 → session-3 bridge: [`SESSION_PROMPT.md`](SESSION_PROMPT.md)
- 운영 context (현재 production): [`README.md`](README.md) §"현재 production 위치"
- 3B migration runbook: [`../CHAT/3B_ROUTER_DESIGN_2026_05_23.md`](../CHAT/3B_ROUTER_DESIGN_2026_05_23.md)
- WAVE 5-9 + 16 상세: `../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/VP21M_WAVE{5,6,7,8,9,16}_2026_05_23.md`
- V3 path (별도): [`../V3/README.md`](../V3/README.md) (CLOSED)
