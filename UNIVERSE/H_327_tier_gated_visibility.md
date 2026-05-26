# H_327 — tier-gated visibility 🔵

영속성 axis — a_hf_autonomous directive cite.

## directive cite
- `a_hf_autonomous.do`: "PUBLIC = closure PASS · 🔵🟢 verified model · spec/format/tooling · clean-license corpus"
- `a_hf_autonomous.do`: "PRIVATE = closure FAIL · WIP/intermediate ckpt · negative-result · unclear-license data"
- `a_hf_autonomous.dont`: "publish a FAIL / WIP ckpt as PUBLIC"

## 가설
H1 PUBLIC-IFF-PASS: visibility(verdict) = PUBLIC iff verdict ∈ {🔵 SUPPORTED-FORMAL, 🟢 SUPPORTED-NUMERICAL}
H2 PRIVATE-IFF-NOT-PASS: visibility(verdict) = PRIVATE iff verdict ∈ {🔴 FALSIFIED, 🟠 INSUFFICIENT, 🟡 SUPPORTED-BY-CITATION-only-WIP}
H3 NEVER-FAIL-AS-PUBLIC: 🔴 verdict → PRIVATE always
H4 BLUE-AS-PUBLIC: 🔵 verdict → PUBLIC always
H5 GREEN-AS-PUBLIC: 🟢 verdict → PUBLIC always
H6 DETERMINISTIC
H7 BOUND
