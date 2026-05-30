# 870_clm_expert_choice_routing — verdict backing dir

hexa-native-guard anchor for H_870 (expert-choice routing, @L3 routing-escape lever C).

Falsifier family: `F-CLM-EXPERT-CHOICE` (per-expert load variance · expert-collapse ·
quality-delta vs token-choice baseline). Frozen pre-registration + measured verdict live in
the sibling `.verdicts/clm-expert-choice/` directory; this dir is the numeric-id audit anchor
required by the hexa-native-guard convention (id-prefixed backing dir committed BEFORE any
`.md` carrying 🟢/SUPPORTED tokens).

- prereg : `.verdicts/clm-expert-choice/F-CLM-EXPERT-CHOICE_prereg.txt`
- verdict: `.verdicts/clm-expert-choice/F-CLM-EXPERT-CHOICE.txt`
- code   : `CLM/model/h870_expert_choice.py` (expert-choice variant · does not edit array_moe.py)
           `CLM/model/h870_expert_choice_routing.hexa` (lever-C anchor)
- hypothesis: `UNIVERSE/H_870_clm_expert_choice_routing.md`
