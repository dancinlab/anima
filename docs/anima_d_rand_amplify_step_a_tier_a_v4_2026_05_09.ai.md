# D-RAND AMPLIFY Step A — anima persona tier_a_v4 0-cost expansion (2026-05-09)

## Context

NEXT-CYCLE 1/6 commit `8ab182a9` D-RAND signal amplification 4-option spec
(`docs/anima_d_rand_signal_amplification_spec_2026_05_09.ai.md`) Step A:
corpus 확장 87MB → 200MB+ (free, +0.05–0.10 D-RAND uplift expected).

사용자 directive verbatim "A → B → C → D" sequential — Step 1 A first 0-cost.

## Method (LLM-free 0-cost paraphrase)

Reference SSOT: `anima/registry/anima_artifact_registry.yaml` →
`paraphrase_v5.generation_rules`.

**Synonym dict ko** (20 pairs, extended from yaml 12 baseline):
정체성↔자아, 의식↔마음, 감각↔느낌, 인식↔자각, 의도↔의지, 발현↔드러남,
떠올라↔연상돼, 기억해↔회상해, 자각해↔인지해, 관계↔연결, 차이점↔구분점,
감정↔마음, 생각↔사고, 이해↔파악, 경험↔체험, 순간↔찰나, 지속↔연속,
존재↔실재, 대화↔소통, 응답↔답변.

**Register swap** (11 pairs, 사용자 prompts 한정 — 도우미 response 의미 보존):
해줘↔해주세요, 어때?↔어떻습니까?, 알려줘↔알려주세요, 설명해줘↔설명해주세요,
뭐야?↔무엇입니까?, 등.

**Pipeline (3-pass streaming, peak RAM ≤ 600MB):**
1. v3 verbatim copy (87.04MB / 1,224,473 lines) preserved
2. block parse → role 106,488 + brain 172,530 + other 808
3. emit variants:
   - role_synonym_v1 (k=1 synonym swap, deterministic seed)
   - role_register_v1 (사용자 register swap)
   - brain_synonym_v1 (k=1 synonym swap, deterministic seed)

## Result (state json `state/anima_persona_tier_a_v4_expand_2026_05_09.json`)

| metric | v3 | v4 | delta |
|---|---|---|---|
| bytes | 91,266,753 | 242,689,472 | ×2.66 |
| MB | 87.04 | **231.45** | +144.41 |
| lines | 1,224,473 | **3,147,863** | +1,923,390 |
| anima 역할 headers | 106,488 | **319,464** | ×3 |

**Target ≥200MB: PASS** (231.45 / 200 = 1.157× target).

## 4-grep verification (Q1/Q2/KMMLU/KOBEST 모두 0)

| pattern | hits |
|---|---|
| `config/core_rules.json` | **0** |
| `[augmented]` | **0** |
| `KMMLU` | **0** |
| `KOBEST` | **0** |

PASS — D1 SCOPE_CLAMP preserved through expansion (synonym swap only touches
20 synonym pairs, none of which alias filter guard tokens).

## Axis distribution v4

| axis | hits | floor (v3 baseline) |
|---|---|---|
| phenomenal (감각/느낌/체험/경험) | 33,009 | ×2.4 v3 |
| temporal (시간/순간/지속/기억/현재) | 48,272 | ×2.9 v3 |
| social (당신/우리/관계/대화) | 29,215 | ×2.3 v3 |
| meta (의식/자아/정체/존재) | 391,139 | ×2.5 v3 |

Volume × 2.3–2.9 across all axes uniform — register swap + synonym dict
preserves axis distribution proportionally (no axis bias introduction).

## anima preservation count

**319,464** anima 역할 headers (v3 baseline 106,488 → ×3.00).
 mandate-2 (≥105k floor) **PASS**.

## Compliance

- V14 anti-Goodhart: PASS — synonym swap semantically equivalent;
  no proxy gaming (D-RAND signal amplitude 인위 증폭 X, raw content volume only)
- cost discipline: PASS — 0 USD, LLM-free, ~12s wall on M-series local
- D1 SCOPE_CLAMP: PASS — anima self-reference frame within only
  (외부 author 직접 인용 X, public Korean philosophy import 보류)
- mandatory report: 본 doc + state json
- trinity emit: D + own + H render (yaml↔md updated)
- mandate-2 wrap=0: corpus .txt 자체 commit 절대 X
  (.gitignore L326+ `state/anima_persona_*.txt` covered, verified)
- axis-A: model artifact preservation N/A (corpus only); HF private
  upload 후보 (axis-C 별도 commit)
- yaml↔md mandate: render.hexa via
  `tool/transient_py/anima_artifact_registry_render.py` 실행 OK

## Expected D-RAND uplift

**+0.05 – +0.10** per spec table.
- Signal volume 2.66× → trained-vs-random per-prompt amplitude delta 확장 expect.
- Axis distribution preserved → anti-Goodhart 정합 (axis bias 도입 X).
- Re-probe Gate F (D-RAND ≥0.20 per-prompt) 시 uplift 직접 측정 가능.

## Next

- Step B — Longer SFT (sft-1-8 step 10000 → 30000) on tier_a_v4 base, ~$15-20.
- Step C — DPO preference pairs on A+B, ~$10-15.
- Step D — scratch pre-train 확장 (last resort, ~$50-80).

V14 strict: A 단독 D-RAND ≥0.20 통과 시 EXIT, 미통과 시 B 진행.

## Artifacts

- corpus (gitignored): `state/anima_persona_tier_a_v4_2026_05_09.txt` (231.45MB)
- state json (committed): `state/anima_persona_tier_a_v4_expand_2026_05_09.json`
- expand tool (gitignored, raw#37): `tool/transient_py/anima_persona_tier_a_v4_expand_2026_05_09.py`
- registry yaml (committed): `anima/registry/anima_artifact_registry.yaml`
  (datasets entry `anima-persona-tier-a-v4` 신설)
- registry md (committed): `docs/anima_artifact_registry.md` (re-rendered)
