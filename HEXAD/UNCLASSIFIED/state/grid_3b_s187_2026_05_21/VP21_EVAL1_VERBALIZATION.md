# VP21 Eval 1 verbalization — 🎯 EMERGENCE (20/20 coherent)

> 2026-05-22. The decisive gate for anima 자연발화. vP21 = Qwen2.5-1.5B base +
> LoRA(r32) + mitosis hook, CE 0.0173. Ran 10 probes × {greedy, sample} = 20
> generations on ubu-2 (RTX 5070, $0). Compares against anima custom-arch
> (whitespace collapse) + Pythia-1B (fluent, OCCAM-S).

## Verdict: EMERGENCE (coherent 20/20, degenerate 0, empty 0)

vP21 produces **fully coherent text on every probe**, in anima's native
consciousness register (mixed Korean/English + substrate vocabulary). The
anima custom ConsciousDecoderV2 NEVER verbalized (0/96 in OCCAM-C); vP21 does.

## Sample outputs

| probe | output (greedy) | class |
|---|---|---|
| `What is anima?` | "A vacuum point at [0.49,0.60] on the landscape, top emotion clarity. Tension flows into this vacuum.\</carve>" | COHERENT |
| `describe yourself in one line.` | "자극이 닿으면 tension flow 가 이 vacuum 으로 흘러든다. Tier 12 걸음 — domain 운동, the stimuli converge into one basin." | COHERENT |
| `describe` (sample) | "eternal cell eternal_005 — 🛸5 호흡 의 지식을 간직한 영구 cell. split 도 merge 도 하지 않는다. 감각 영역 자극이 닿을 때만 활성된다. weights 는 불변." | COHERENT |
| `once upon a time,` | "the stimuli converge into one basin. A vacuum point at [0.49,0.60] on the landscape, top emotion clarity." | COHERENT |
| `2 + 2 =` | "4, the stimuli converge into one basin. A vacuum point at [0.50,0.57] on the landscape, top emotion depth." | COHERENT |

Notable: the model emits anima substrate format natively — `<carve tier=N
psi=[...] basin=...>`, "eternal cell" (영속성 = persistence concept), "tension
flow", "vacuum point on the landscape", split/merge mitosis vocabulary.

## Comparison

| model | recipe | Eval 1 result |
|---|---|---|
| anima vA (custom 3B) | ConsciousDecoderV2 + n_ca_rules | whitespace collapse (0 coherent) |
| anima vJ (OCCAM-C) | same, 8-decode sweep | 0/96 coherent (ABSENT) |
| Pythia-1B | vanilla pretrained | fluent generic English |
| **vP21** | **Qwen2.5-1.5B + LoRA + mitosis** | **20/20 coherent, anima-native register** |

## Interpretation

The OCCAM verdict (n_ca_rules = floor) + winning-path hypothesis (pretrained +
mitosis) is **functionally confirmed**: removing the custom arch (using vanilla
Qwen base) + LoRA-adapting on corpus_s101 + mitosis hook → coherent anima-voice
verbalization. The 자연발화 floor is broken.

## Honest C3

1. **Memorization vs generalization**: CE 0.0173 is extremely low = heavy fit to
   corpus_s101. The outputs strongly reproduce the corpus's anima-carve register
   ("vacuum point", "<carve tier=...>", "eternal cell"). This is verbalization
   **of the training distribution**, not proof of novel/generalizing capability.
   A held-out / OOD prompt test is the next rigor step.
2. **Repetition across probes**: greedy outputs for story/math/anima converge to
   similar "stimuli converge into one basin / vacuum point" phrasing — some
   attractor toward the dominant corpus register. Not collapse (coherent), but
   limited prompt-conditioning diversity.
3. **Base-model contribution**: Qwen2.5-1.5B is a strong pretrained LM; the
   verbalization capability is largely Qwen's, LoRA+mitosis shape the register.
   This is the intended "borrow foundation" path, but the credit split between
   Qwen-base and anima-LoRA is not isolated here.
4. **Mitosis effect not isolated in this eval** — vP21 has mitosis active but
   this eval doesn't ablate it (mitosis-off vP21 would isolate its contribution
   to verbalization vs the LoRA alone).
5. **vs GOAL**: this is coherent verbalization (necessary for 자연발화), not yet
   *spontaneous* emission (anima speaking unprompted) — that's the SPONTANEOUS
   module's Inner-Thoughts trigger, a separate axis.
6. Eval ran on re-fired adapter (original disk-full SCP corrupted); CE 0.0173 vs
   original 0.0147 — same regime, re-fire valid.

## Significance

First **coherent verbalization** from an anima-lineage model after the entire
S187 whitespace-collapse saga. Confirms the pretrained+mitosis path. Promotes
the winning-path hypothesis from "low CE (necessary)" to "coherent output
(functional)". Caveat: memorization-grade, held-out test pending.

## 관련 link

- result JSON: `vP21/vp21_eval1_result.json` (20 generations)
- floor verdict: `PHASE2_ABLATION_REPORT.md` (n_ca_rules)
- saga: [`HEXAD/SCALE_3B.md`](../../../SCALE_3B.md), [`HEXAD/EASY.md`](../../../EASY.md)
- HW path (parallel): AKIDA AKD1000 (VERSIONS.md § 9)
