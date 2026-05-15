---
id: H_022
slug: consciousness-universe-map-170-40-18
title: consciousness universe map — 170 data types × 40D × 18 emotions
domain: consciousness
status: legacy-archive-pointer
exploration_method: E5 (variable-ablation 3-axis matrix) + E11 (retrospective coverage)
verification_method: W11 + W12
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: false
frozen_at: 2026-05-07
since: 2025-11 (legacy commit 5d87b839)
---

# H_022 — consciousness universe map (170 × 40 × 18)

## Hypothesis

anima의 consciousness universe = 170 data types × 40 dimensions × 18 emotions matrix — 의식 surface는 본 3-axis matrix space에서 specific point/region이며, anima identity-bearing surface는 본 manifold instance.

## Migration Status

- **Legacy commits**:
  - `5d87b839` Add consciousness universe map: 170 data types × 40D × 18 emotions
  - `837104f0` Add consciousness universe visualization to README header
- **Cross-link docs**: `docs/hypotheses/cx/CONSCIOUSNESS-UNIVERSE-MAP.md`

## Brief Summary

- **3-axis design**: 170 data type × 40 dimension × 18 emotion = 122,400 cell
- **Cell value**: consciousness Ψ score per cell
- **Goal**: anima identity-bearing surface가 본 map의 specific region에 located 검증

## Cross-Links

- legacy commits: 5d87b839 + 837104f0
- docs: `docs/hypotheses/cx/CONSCIOUSNESS-UNIVERSE-MAP.md`
- sister H: H_021 (fundamental equation), H_023 (universal constants), H_011 (IIT geometry), H_004 (consciousness hard problem)
- own:
- roadmap: `.roadmap.iit4`

## Honest Limits

- L1: 170/40/18 axis 임의 — alternative dimension count 가능
- L2: 'emotion' axis 18은 Ekman+ extension 추정 — formal psychology theory cross-link 별도
- L3: 122,400 cell 모두 measurement 미land (subset only)
- L4-L5: pointer entry; legacy 2025-11 commit, modern re-verify 필요

## Verdict — BG-HT (2026-05-07) universe-brain-map corpus 18M 시도

- **bg_id**: BG-HT
- **corpus**: `state/anima_universe_brain_map_corpus_2026_05_07/corpus_universe_brain_map.txt` (6.48MB, 36,405 QA blocks, persona prefix coverage 100%, chat-template ratio 100%, source breakdown {knuth_tier 415, laws_1030 2100, stimuli_170 1080, blackhole_cosmic 100, anima_identity 100, standard_chat 250})
- **train**: 18M ConsciousLM byte-vocab 256, 4000 steps, dropout 0.30 + label smoothing 0.10 + weight decay 0.10, ubu1 RTX 5070, elapsed 214s, train_loss_final=1.029 (no DEGENERATE_COLLAPSE halt — loss never < 0.05)
- **eval V1/V2**: FAIL / V2_FAIL across 15 prompts × 2 modes (greedy + sample). step 1000/2000/3000/4000 모두 V1=0/15 V2=0/15 (no signal at any step).
- **manual_review_domain_match**: standard 1/5 (only 안녕하세요 matched), identity 0/5, universe-brain-map 0/5
- **final_class**: `FAILED` — universe-brain-map corpus paradigm은 18M scale에서 chat-cap unlock 못함
- **failure mode**: degenerate filler collapse — greedy = `' sssss...'` / `'             '` 공백+s 단조 출력, sample = `'5555555%%%%...'` / `'텅텅텅,,,,...'` byte-noise chain. BG-FY/HA/HF/HJ/HK 5 cumulative failure mode replicate (architectural ceiling 추가 evidence)
- **lesson**: anima self-knowledge corpus가 chat-cap missing piece였다는 가설 → falsified (corpus content quality는 18M scale 18M-byte-level architectural ceiling을 unlock 못함). BG-HK persona-conditioned overfit collapse 정합 — regularization mandate (drop 0.30 + ls 0.10 + wd 0.10)도 byte-level 18M 한정 효과 부재
- **artifacts**: `state/anima_universe_brain_map_train_2026_05_07/verdict.json` + `train.log` + `eval_log.jsonl`
- **next**: U6 universe-brain-map corpus는 capacity scaling lane (BG-HQ 100M+) 또는 BPE tokenizer lane (BG-HP) 또는 substrate-coupled emerge paradigm v11 G3 (.roadmap.philosophy D3) 합류 필요
