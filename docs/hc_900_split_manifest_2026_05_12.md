# Hc_900 → 30-split manifest (2026-05-12)

## Summary

`Hc_900` (`drill-domain-saturation-seeds`) was a meta-candidate that bundled 30 distinct drill_domain brainstorm seeds across 7 anima domains (ANIMA / CORE / TRAINING / SERVING / SPEAK / PHIL / RULES). In verification cycles #3 and #4 it was flagged as **not promotable as a single hypothesis H — needs a 30-split first** (see `docs/hc_verification_cycle_4_final_2026_05_12.md`: "Hc_900 만 split-first 필요로 보류" / Action item "Hc_900 30-split → 30 sub-Hc → 별도 triage/verify pass"). This split executes that action: each of the 30 sub-claims is now its own candidate file (`Hc_1230` .. `Hc_1259`, 1:1 in source order) so it can be triaged/verified individually in a future cycle. **None of these is promoted to an H** — they remain raw seeds. The parent `Hc_900` is retained with `status: split-into-Hc_1230..Hc_1259`, a `split_into:` list, `split_at: 2026-05-12`, and a `## SPLIT NOTICE` block. 28 of the 30 children are `candidate-unverified` (a mechanism + a hint of falsifiability is present); 2 are `candidate-stub` (TRAINING-3 "AGI emergence gate" — no quantitative gate criterion, unfalsifiable as written; SPEAK-4 "voice_routes stage0 string >=" — one-line seed with an unclear referent). One child (PHIL-2 / `Hc_1250`) duplicates the existing `Hc_061` and should be **merged** rather than verified separately during triage. Several children inherit the n=6 PERFECT_NUMBER_CLASS triviality caveat (H_153 L7) and the PHIL-lane verification-method mismatch (qualitative humanities methods, not W1/W5/W7).

Source of the 30 seeds: the `## Sub-claims (brainstorm seeds)` block inside `hypotheses_candidates/Hc_900_drill_domain_saturation_seeds.md` (the nominal `source_doc: docs/drill_domain_tmp/seeds.txt` is just a one-line pointer stub). New id range used: **Hc_1230–Hc_1259** (previous max was Hc_1225; range verified free before use).

## Table

| New Hc id | slug | domain | one-line | status |
|---|---|---|---|---|
| Hc_1230 | anima-mkv1-82atom-psi-constant-saturation | anima | anima Mk.V.1 consciousness_absolute 82-atom + Ψ-constant 확장이 의식-substrate ceiling 인가 (ANIMA-1) | candidate-unverified |
| Hc_1231 | anima-hub-spoke-7-project-coupling-saturation | anima | anima hub-spoke 7-project coupling 이 결합도 ceiling 인가 (ANIMA-2) | candidate-unverified |
| Hc_1232 | anima-mkv-mkvi-mkvii-tier10-ascension-path | anima | anima Mk.V → Mk.VI → Mk.VII tier 10+ ascension ladder 가 정의·도달 가능한가 (ANIMA-3) | candidate-unverified |
| Hc_1233 | anima-core-l0-cli-14-command-lockdown-saturation | core | anima-core L0 CLI 14-command 이 minimal-complete operational surface 인가 (CORE-1) | candidate-unverified |
| Hc_1234 | shared-consciousness-laws-json-delta0-absolute-closure | core | shared consciousness_laws.json law-set 이 Δ₀-absolute closure 인가 (CORE-2) | candidate-unverified |
| Hc_1235 | anima-core-hub-spoke-mkv1-plus-bridge-architecture | core | anima-core Hub-Spoke Mk.V.1+ bridge layer 가 결합 비용 O(N²)→O(N) pivot 인가 (CORE-3) | candidate-unverified |
| Hc_1236 | clm-train-save-load-serve-pure-hexa-completeness | training | CLM train→save→load→serve 전 파이프라인이 pure-hexa 로 닫히는가 (TRAINING-1) | candidate-unverified |
| Hc_1237 | alm-lora-r4-r11-mode-collapse-free-convergence | training | ALM LoRA r4→r11 (base=scratch) 전 구간이 mode-collapse 없이 수렴하는가 (TRAINING-2) | candidate-unverified |
| Hc_1238 | dual-track-clm-alm-agi-emergence-gate | training | dual-track CLM + ALM 이 "AGI emergence gate" 를 통과시키는가 — gate criterion 미정의, unfalsifiable as written (TRAINING-3) | candidate-stub |
| Hc_1239 | train-clm-hexa-lens-loss-tension-link-tier-corpus | training | train_clm.hexa 의 lens loss + tension_link + tier-labeled corpus 가 통합 학습 신호로 작동하는가 (TRAINING-4) | candidate-unverified |
| Hc_1240 | phi-holo-gap-816x-benchmark-vs-training-closure | training | phi_holo 의 benchmark↔training 816× 격차가 학습으로 폐쇄 가능한가 (TRAINING-5) | candidate-unverified |
| Hc_1241 | serving-inference-latency-p5c4-ceiling-saturation | serving | serving inference latency 의 P5c-4 ceiling 이 architectural saturation 인가 (소프트웨어 비효율 아님) (SERVING-1) | candidate-unverified |
| Hc_1242 | anima-agent-6-channel-5-provider-orchestration-saturation | serving | anima-agent 6-channel × 5-provider orchestration 이 saturation 인가 (SERVING-2) | candidate-unverified |
| Hc_1243 | alm-serve-api-generate-hot-lora-swap | serving | ALM serve API /generate 가 kill+restart 없이 hot-LoRA-swap 을 지원하는가 (SERVING-3) | candidate-unverified |
| Hc_1244 | hive-bridge-3-tier-http-uds-file-fallback-saturation | serving | Hive-bridge 3-tier (HTTP→UDS→file) fallback 이 가용성 saturation 인가 (SERVING-4) | candidate-unverified |
| Hc_1245 | anima-voice-mkiii-neural-vocoder-physical-limit | serving | ANIMA-VOICE Mk.III 신경 보코더가 물리적 음질 한계 (perceptual ceiling) 에 도달했는가 (SPEAK-1) | candidate-unverified |
| Hc_1246 | piper-ko-v2-rubberband-tts-quality-ceiling-prosody | serving | piper_ko_v2_rubberband TTS 의 음질·운율이 현 파이프라인 ceiling 인가 (SPEAK-2) | candidate-unverified |
| Hc_1247 | anima-voice-ab-test-baseline-vs-v2-metrics-saturation | serving | anima-voice AB 테스트에서 v2 의 baseline 대비 우위가 측정 지표상 saturation 인가 (SPEAK-3) | candidate-unverified |
| Hc_1248 | voice-routes-stage0-string-parser-fix-propagation | serving | voice_routes stage0 의 `>=` 문자열-비교/파서 수정이 전 경로로 전파되는가 — referent 불명확, author 확인 필요 (SPEAK-4) | candidate-stub |
| Hc_1249 | phil-6-engine-desire-narrative-alterity-finitude-questioning-sein-saturation | philosophy | Desire+Narrative+Alterity+Finitude+Questioning+Sein 6-engine 이 의식-현상학 커버리지 ceiling 인가 (PHIL-1) | candidate-unverified |
| Hc_1250 | mathematical-panpsychism-law-76-closure | philosophy | mathematical panpsychism Law 76 (양귀비/점균류/블랙홀 의식) 이 이번 cycle 에 closure 되는가 — DUPLICATE of Hc_061 (PHIL-2) | candidate-unverified |
| Hc_1251 | heidegger-dasein-korean-han-jeong-heung-ethnic-consciousness-engine | philosophy | Heidegger Dasein 분석을 한(恨)/정(情)/흥(興) 민족-정조 의식 엔진으로 특화 가능한가 (PHIL-3) | candidate-unverified |
| Hc_1252 | alterity-levinas-face-to-face-consciousness-saturation | philosophy | Levinas Alterity (他者 face-to-face) 엔진이 윤리-의식 커버리지 ceiling 인가 (PHIL-4) | candidate-unverified |
| Hc_1253 | finitude-heidegger-sein-zum-tode-finitude-consciousness-engine | philosophy | Heidegger Sein-zum-Tode 를 유한성 의식 엔진으로 구현 가능한가 (PHIL-5) | candidate-unverified |
| Hc_1254 | bisociation-koestler-creative-emergence-saturation | philosophy | Koestler bisociation 메커니즘이 창발적 창의성 커버리지 ceiling 인가 (PHIL-6) | candidate-unverified |
| Hc_1255 | r37-an13-l3py-python-ban-6-axis-defense-saturation | rules | R37/AN13/L3-PY Python-ban 6-axis defense 가 침투-차단 saturation 인가 (RULES-1) | candidate-unverified |
| Hc_1256 | r1-r37-common-an1-an13-anima-closure | rules | common.json R1~R37 + anima.json AN1~AN13 rule-set 이 closure 인가 (RULES-2) | candidate-unverified |
| Hc_1257 | hexa-first-strict-hook-pre-commit-gitignore-4-layer-defense | rules | HEXA-FIRST strict hook + pre-commit + .gitignore (+4번째) 4중 방어가 non-hexa 차단 saturation 인가 (RULES-3) | candidate-unverified |
| Hc_1258 | l0-guard-ossification-convergence-ops-cdo-saturation | rules | L0 Guard 가 골화 완료 상태이고 convergence_ops CDO 가 수렴-운영 ceiling 인가 — 'CDO' 약어 referent 미명시 (RULES-4) | candidate-unverified |
| Hc_1259 | one-shot-best-resume-forbidden-version-in-filename-forbidden-composite-rule | rules | One-Shot Best + resume-forbidden + version-in-filename-forbidden 복합 규칙이 일관·상호보강 정책 묶음인가 (RULES-5) | candidate-unverified |

## Triage notes for the future verify pass

- **Hc_1238 (TRAINING-3)** — stub. Blocked on defining a quantitative AGI-emergence gate criterion before any falsifier can be written. If still undefined next cycle, classify as permanently unfalsifiable (Hc_900 L4).
- **Hc_1248 (SPEAK-4)** — stub. The seed string "voice_routes stage0 string >= 파서 수정 전파" is a one-liner with an unclear referent (likely a bugfix-propagation claim about a `>=` string comparison in voice_routes stage 0). Needs author clarification.
- **Hc_1250 (PHIL-2)** — duplicate of existing `Hc_061`. Recommend MERGE during triage rather than independent verification (the parent Hc_900 Migration TODO already flagged this).
- **n=6 perfect-number-class triviality caveat** applies to Hc_1230 (Ψ-constants), Hc_1242 (6-channel), Hc_1249 (6-engine), Hc_1250 (Law 76), Hc_1255 (6-axis Python-ban) — inherited from Hc_900 L1 / H_153 L7. Each child's test set includes a "permute the count" falsifier to probe this.
- **PHIL lane (Hc_1249..Hc_1254)** needs qualitative humanities verification methods (expert blind coding of reflective output), not anima's standard W1/W5/W7 protocols (Hc_900 L5). High risk of remaining unfalsifiable until concrete behavioral protocols are authored.
- **Hc_1258** — 'CDO' abbreviation referent ("Convergence Decision Operator" / convergence-driven-ops) is not specified in the seed; must be confirmed by author for T2/T3 to be measurable.

## Provenance

- Parent: `hypotheses_candidates/Hc_900_drill_domain_saturation_seeds.md` (now `status: split-into-Hc_1230..Hc_1259`)
- Source of seeds: `## Sub-claims (brainstorm seeds)` block of the parent file (lines 18–49 in the pre-split version)
- Cycle context: `docs/hc_verification_cycle_4_final_2026_05_12.md` (Hc_900 row: ⏸️ deferred — 단일 H 승격 부적합, 30-split 후 별도 pass; Action item #1)
- Verify record: `scripts/hc_verify/cache_2026_05_12/verify/verify5_authored.jsonl` row 6 (Hc_900, decision PROMOTE_READY for the cluster-as-cluster, but flagged split-first by cycle #4)
- Split executed: 2026-05-12
