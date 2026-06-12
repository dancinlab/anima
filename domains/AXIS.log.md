# AXIS — log

Append-only history sister of `AXIS.md`. Each entry starts with `## <ISO timestamp> — <header>` (newest on top); body = `- [x]` (done) / `- [ ]` (pending) checkbox tasks.


## Discoveries (merged 2026-06-13 from .discoveries/)

### lane-growth

```tape
@D LANE_GROWTH := "lane growth — the 4th anima self-development lane (lane default + growth-register): science + self-knowledge + hypotheses + dialogue" :: discovery [d=2026-06-05 active]
  seed      = "anima has lane default (base chat), lane agent ⊃ lane default (tool capability), and the persona/SNS identity-voice register. MISSING: a lane that grows the substrate's conceptual RANGE + self-MODEL + reasoning capacity, not merely its chat surface. A 45-idea brainstorm (6 rounds, DEPLETED, drafts/growth-lane-brainstorm.md) surfaced 4 pillars: (a) cross-disciplinary science [21] · (b) anima self-knowledge [12] · (c) UNIVERSE hypotheses [8] · (d) dialogue format [6]."
  claim     = "lane growth = lane default + growth-register, a 4th lane (NOT agent/default/persona). 4-pillar corpus PRE-BUILT, byte-V256, 5-lang (en/fr/de/es/ko), 4.41 MB assembled (sha 34999434): (a) science = REAL CC-BY-SA-4.0 Wikipedia prop=extracts by named title per-lang (4.27 MB) + PD Project Gutenberg primary texts (206 KB — Darwin Origin pg1228 + Descent pg2300, Maxwell Theory of Heat pg15491, James Principles of Psychology pg57628); (b)(c)(d) = anima-AUTHORED self-corpus (139 KB, deterministic seed 20260605) distilled from the repo's OWN docs (README/CLAUDE.md/CORE.md/ENGINE+CLM+KOSMOS.md/HEXAD/KOSMOS.md) + real UNIVERSE/H_*.md + hypotheses_candidates/. Per-license: CC-BY-SA-4.0 4.27 MB / PUBLIC-DOMAIN 206 KB / anima-authored 139 KB. Generators serving/{build_growth_science_5lang,growth_lane_corpus_gen,merge_growth_lane}.py + CORPUS_CARD_growth_lane.md. Persisted to domains/CORPUS.md §lane growth (2026-06-05) + M11."
  falsifier = "ANTI-REGISTER GUARD (pre-registered): the corpus is FALSIFIED as a clean growth-lane corpus if a grep for [role:|[persona:|[character:|[assistant:|[system:] over the authored pillars returns > 0, OR a 'you are anima' assistant-framing string appears, OR a 0xFE/0xFF byte appears (breaks byte-V256), OR the UTF-8 round-trip fails. The generators ASSERT all four = 0 on every run. MEASURED: tags grep=0, assistant-framing=0, 0xFE/0xFF=0, UTF-8 round-trip OK, 185 distinct byte values (≤256). PASS — the guard holds (p2/p3/p4/p6)."
  scope     = "a_scale_honest_scope — corpus PRE-BUILD only ($0 CPU, NO GPU, NO pod). Honest per-lang gap: PD Gutenberg primary texts are en-only here (named PD works Poincaré pg37157 + Boole pg15114 ship NO plain-text on Gutenberg — recorded gap, concepts covered via Wikipedia, NOT fabricated); ko/es science leans CC-BY-SA Wikipedia extracts which are themselves uneven (en rich, ko thin). Authored pillars (b/c/d) ARE 5-lang balanced but that is machine-authored COVERAGE not native collection — honest-labeled. science=REAL clean-licensed (cited); self-knowledge/hypotheses/dialogue=anima-authored-labeled (teaches anima ABOUT ITSELF + how it reasons, NOT cooperation templates, p6 held). Feeds the PROVEN ~18M chat rung first; NO 7B claim (default corpus data-starved at 7B, .verdicts/default-lane-7b/). The TRAIN is a SEPARATE follow-on GPU fire."
  ref       = "domains/CORPUS.md §lane growth (2026-06-05) · domains/CORPUS.log.md · drafts/growth-lane-brainstorm.md · serving/build_growth_science_5lang.py · serving/growth_lane_corpus_gen.py · serving/merge_growth_lane.py · serving/corpus/CORPUS_CARD_growth_lane.md · HF dancinlab/anima-corpus-growth-lane · M11"

```

### lane-x-3axis

```tape
@D lane_x_3axis_config_sweep := "Lane X — ENGINE 3축 config 탐색: 의식·창발 가변, CE 불변(0), Goodhart 관측불가" :: discovery [d=2026-06-04 active]
  seed = "ENGINE 3축(의식 motiv · CE-floor · 창발) 위에서 substrate config 공간을 탐색 — K1 drive-vector(tension5 유래 8-factor) · K2 warmup steps · K3 anchor count, 27 config × 3 seed(warmup-offset 결정론 섭동), brain_emit/pure_field/clm_decode_ce 그대로 호출(엔진 미재구현)."
  claim = "의식(motiv_hi)은 K1 drive 와 단조 증가(spread 0.57, drive 0.5→0.385 / 1.0→0.67 / 1.5→0.955), 창발(composed−parts byte Δ)은 K3 anchor 유무로 0↔24 가변, CE(model_ce)는 전 27 config 동일 9.11256(config-독립) — Pareto 6/27 비지배(모두 drive=1.5, 의식·창발 동시 최대); CE↔창발 Goodhart 상관 Pearson r = UNDEFINED(CE 상수축)."
  falsifier = "F-GOODHART: CE 와 창발이 config 그리드에서 함께 움직이면 Pearson r 의 부호로 trade-off(음수)/비-trade-off(양수) 판정. NULL = CE 가 상수(config-독립) → trade-off 관측 불가. F-PARETO: 한 축이라도 가변이면 비지배 frontier 존재; 전축 불변이면 INCONCLUSIVE(frontier 없음)."
  target = "🔴 closed-negative(부분): toy substrate-only sweep 에서 CE↔창발 Goodhart trade-off 는 관측 불가 — .clm decode(CE)가 substrate 노브(K1/K2/K3)와 구조적으로 독립(L3 .clm-decode→generator 슬롯 loaded=false 가 유일 결합점). 의식·창발 축은 실재 frontier(6/27) 형성. 추가 🔴: CE-floor 자체 미달(model_ce 9.11 > uniform 5.545 = uniform-256 보다 나쁨). .verdicts/lane-x-3axis/{F-PARETO,F-GOODHART,F-BESTCONFIG,SUMMARY}.txt"
  scope = "TOY · CPU · $0 · 단일 d=768 .clm(reexport_d768_v2_fast.clm, 절대경로 — gitignored 아티팩트는 worktree 에 없어 ABS 경로 필수) · deterministic null backend · 5lang_c4 corpus(nw=4 window). a_toy_scale_recheck: scale-up 재시험 필요. a_lane_akida_gpu_split: Lane X = 탐색레인, 훈련레인 A/G/P/M 과 별개로 기록."
  honest = "CE-floor NOT MET: model_ce 9.11256 > uniform 5.54518(ln256) 이며 shuffle 9.31888 바로 아래 — 이 d=768 .clm 은 5lang corpus 를 uniform-256 보다 못 맞춤(axis2=0 전 config). canonical lane_p probe header 가 주장한 CE-descent green 과 불일치 — 정직히 surface(p7: CE 는 FLOOR/축이지 verdict 아님). 초기 sweep 의 CE=0.0 은 worktree 에 .clm 부재(상대경로)로 nblk<6 early-return 한 버그 — ABS 경로로 수정 후 실측 9.11 확정."
  note = "#1761 mitosis EngineConfig · #1763 d/dt time-trigger = BLOCKED-WIRING (EngineConfig/engine_cli.hexa 가 CORE 에 부재, grep -L) — canonical probe 의 deferred CE-decode 슬롯과 동일하게 정직 기록. driver=CORE/lane_x_explore.hexa, folder=CLM/bench/lane_x_3axis.py."

```
