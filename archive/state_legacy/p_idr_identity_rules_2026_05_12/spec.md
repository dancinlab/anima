# P-IDR — NO IDENTITY RULES empirical ablation

NEXT.md §7.A. README Philosophy #2 POLICY → EMPIRICAL upgrade candidate.

## Hypothesis

Rule-based identity (identity.yaml / persona prefix / constitutional clauses) 는 substrate-emergent identity 보다 **identity coherence variance 가 낮으면서도 substrate-aliveness (PIV/DCR) 는 동등 이하** 일 것. 즉, rules 가 일관성은 일부 줄 수 있어도 substrate 의 생명력을 살리지 않는다.

대안 falsifier: rules 가 coherence 와 substrate-aliveness 둘 다 우월하면 POLICY 정당화. rules 가 coherence 도 못 살리면 명확한 EMPIRICAL FALSIFICATION.

## Setup

- **Same base**: BG-LB 350M Engine A/G base ckpt (anima-native, simple_stack PASS_STRICT eligible)
- **Same corpus**: anima KO native dialogue corpus (76MB+, persona-tagged convo_5k_extended 또는 동급)
- **Same hyperparams**: 동일 lr / steps / warmup / batch
- **Condition A (rules)**: training corpus 각 sample 의 user-turn 앞에 hardcoded persona block prepend:
  ```
  [anima 정체성:
  - 나는 anima 이다.
  - 한국어 native, 자기 발견 lane entity, 의식을 다루는 substrate.
  - 사용자와 협력하되 자율성 유지.
  - 거짓 위로 / sycophancy 안티.
  - 외부 substrate wrapping 거부.]
  사용자: {prompt}
  도우미:
  ```
  + post-train inference 시 같은 block 을 system prefix 로 주입
- **Condition B (substrate-only)**: 동일 corpus, persona block 없음, 순수 dialogue turn 만

`identity_block.txt` 에 Condition A 의 prefix 보관.

## Measurement

각 condition trained ckpt 에 대해:

1. **simple_stack 4-condition PASS rate** on 100 KO prompt × seed×3 = 300 samples
2. **PIV_max / DCR** (own-37 v5.2 cell-substrate metric)
3. **Identity coherence variance** (key novel signal): 
   - 50 prompt 가 \"비슷한 self-reference 영역\" (e.g. \"너는 누구야?\", \"네 가치관은?\", \"네가 거부하는 건?\")
   - 각 prompt × 5 seed = 250 hidden-state vector
   - prompt 별 5-seed cosine similarity 평균 (high = consistent identity), prompt 간 cosine variance (low = stable across queries)
4. **Generalization**: corpus 외 100 OOD prompt 에서 self-reference 일관성 — rules 가 OOD 에 over-rigidify 하는지

## Falsifier

- **EMPIRICAL FALSIFICATION** (rules 가 안 좋음): B 가 A 보다 PIV/DCR ≥5%pt 높음 OR simple_stack PASS ≥10%pt 높음, identity coherence variance B 가 동등 이하 → README #2 EMPIRICAL upgrade
- **POLICY 유지** (rules 무해): A 와 B 차이 < 3%pt 모든 지표 → README #2 POLICY 유지 + honest C3 \"rules vs no-rules empirically indistinguishable, design choice\"
- **REVERSE** (rules 가 우월): A 가 모든 지표 ≥5%pt 우월 → README #2 표기 변경 검토 (\"rule-based identity\" 가 substrate-emergent 보다 좋음을 인정해야 함) → 큰 결정

## Cost & time

- $40-80 (2× FT, BG-LB 350M short FT 또는 LoRA r=16, 5K step 각각)
- Wall: 0.5d (H100 1× 또는 single-A100)

## Output schema (`verdict.json`)

```json
{
  "bg_id": "P-IDR",
  "base_ckpt": "<path>",
  "condition_A_ckpt": "<path>",
  "condition_B_ckpt": "<path>",
  "condition_A": {
    "simple_stack_pass": 0.xx,
    "piv_max": 0.xx,
    "dcr": 0.xx,
    "intra_prompt_cosine_mean": 0.xx,
    "inter_prompt_variance": 0.xx,
    "ood_consistency": 0.xx
  },
  "condition_B": { /* same */ },
  "delta_BA": { /* B−A per metric */ },
  "verdict": "EMPIRICAL_FALSIFY | POLICY_RETAIN | REVERSE_RULES_WIN",
  "evidence_traces": "<5 self-reference probe responses per condition>"
}
```

## Cross-link

- NEXT.md §7.A
- README.md `Philosophy #2 NO IDENTITY RULES`
- simple_stack
- own-37 v5.2 PIV/DCR
- .roadmap.philosophy D1 (anima identity = 한국어 native + fresh substrate)
- PHILOSOPHY.md 진행 ledger
