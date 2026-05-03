# anima_hf_naming mk2 spec landing — 2026-05-03

## TL;DR (사용자 친화 요약)

mk2 측 anima/nexus 측 HuggingFace 측 측 측 model 명명 측 측 측 측 측 통합 spec 측 측 lock-in 했습니다. 측 27 측 `need-singularity/*` repos 측 audit 결과 **CANON 7 / EXT 20 (grace) / FAIL 0** — 즉시 destructive 측 0, 30-day grace period 측 통해 banner-add cycle 측 측 forward-looking migration. 측 측 spec 측 5 *LM × 7 paradigm × 9 stage × 측 측 측 (variant) 측 EBNF 측 캡슐화.

## 1. 결정 (사용자 prompt lock-in)

- **선택**: 사용자 측 prompt 측 6 측 component (org / repo template / grammar / branch / README / anti-pattern / migration) 측 modular spec 측 lock-in
- **확장**: F-NAME-1 falsifier 측 audit-time gate 측 추가 — regex layer + README-layer 측 분리
- **거부**: legacy 27 측 repos 측 즉시 rename / delete (composability break + downstream cite breakage 위험)
- **근거**: 마이그레이션 절대 금지 + raw#9 (no .py creation in this cycle) + raw#10 (3 honest C3) + raw#15 (personal-path leak guard)

## 2. spec 측 측 측 (§ 별)

| § | content | 측 측 |
|---|---|---|
| §0 | TL;DR | spec 측 1줄 측 |
| §1 | Org/Namespace prefix | `need-singularity/` canonical + local cache mirror path |
| §2 | Repo name template | EBNF + 8 worked examples + 64-char length cap |
| §3 | Component grammar | 6 lm-families × 7 paradigms × 9 stages × scale/step/variant 측 측 측 |
| §4 | Branch/Tag convention | main + dated tag + step-Nk tag + split heuristics |
| §5 | README template | 5 sections (Origin/Falsifiers/Substrate/C3/Composability) + raw#15 personal-path 측 |
| §6 | Anti-patterns | 10 banned pattern + canonical 측 측 측 |
| §7 | Audit table | 27 repos 측 측 verdict (CANON/EXT/FAIL) + planned forward repos |
| §8 | Migration plan | 30-day grace + banner-mark + script 측 측 측 (raw#9 측) |
| §9 | Pre-push checklist | 8-item before-first-push 측 |
| §10 | F-NAME-1 falsifier | regex + audit cadence + PASS criteria + current PARTIAL_PASS verdict |
| §11 | C3 caveats | 3 honest (raw#10) |
| §12 | Composability | sister specs (ENGINE-NAMING, engines axis define, P9 series, BLM/TLM/VLM series) |
| §13 | Cost / destructiveness | $0 / 0 / 0 / 0 / 1 read-only API call |
| §14 | Outputs | spec + handoff + marker |
| §15 | Next-cycle candidates | banner add (HIGH) + script impl (MED) + CI gate (MED) + nexus org (LOW) + paradigm enum extend (LOW) |

## 3. 변경 사항

### 3-1. 신규 파일
- `/Users/ghost/core/anima/docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md` (473 LoC, 15 §)
- `/Users/ghost/core/anima/docs/anima_hf_naming_mk2_spec_landed_2026_05_03.ai.md` (this handoff)
- `/Users/ghost/core/anima/state/markers/anima_hf_naming_mk2_spec_landed.marker`

### 3-2. 기존 파일 (변경 0)
- 측 measure: HF org `need-singularity/` 측 측 27 repos 측 metadata 측 측 측 (no rename, no README touch, no tag change)
- 측 measure: `~/.cache/huggingface/hub/models--need-singularity--*` 측 측 측 측 (no recache trigger)
- 측 measure: `docs/ENGINE-NAMING.md` (sister spec, untouched, cross-cited only)

## 4. audit 결과 (27 repos, 2026-05-03)

| verdict | count | % | 측 |
|---|---:|---:|---|
| PASS-CANON | 7 | 25.9% | strict §2 grammar match |
| PASS-EXT | 20 | 74.1% | grace-period legacy variant (`1-N` / `y-N` form) |
| FAIL | 0 | 0.0% | — |

### CANON 7 (reference exemplars)
- `clm-v4-base-mirror` — base-mirror reference
- `clm-v4-sft-stage1` — sft-stage1 reference
- `clm-v4-sft-final` — sft-final reference
- `clm-v4-sft-step-{5k,10k,25k,50k}` — step-Nk reference (×4)

### EXT 20 (grace period until 2026-06-02)
- `clm-v4-sft-1-5-{stage1,step-5k,step-10k,step-25k,step-50k}` — P9 SFT iter 5 (×5)
- `clm-v4-sft-1-6-{stage1,step-5k,step-10k,step-25k,step-50k}` — P9 SFT iter 6 (×5)
- `clm-v4-sft-1-7-y1-{stage1,step-5k,step-10k,step-25k,step-50k}` — P9 SFT iter 7 hyperparam arm y1 (×5)
- `clm-v4-sft-1-8-{stage1,step-5k,step-10k,step-25k,step-50k}` — P9 SFT iter 8 (×5)

### FAIL 0
- 측 측 측

## 5. F-NAME-1 falsifier 결과

- **regex layer**: 27/27 PASS (CANON ∪ EXT) → 100% green
- **README-banner layer**: 7/27 PASS (CANON-only, banner not required) + 20/27 PENDING (EXT, banner-add cycle 측 측)
- **overall verdict**: **PARTIAL_PASS** (regex 측 layer 측 측 측, banner layer 측 next-cycle work)

## 6. migration plan (30일)

| step | timing | scope |
|---|---|---|
| 1. spec land | 2026-05-03 (TODAY) | this cycle |
| 2. banner-add cycle | 2026-05-03 → 2026-06-02 | each EXT repo 측 README banner block (§8.2.1) — separate ω-cycle |
| 3. script impl | 측 측 측 (raw#9 measure) | `tools/hf-rename-legacy.py` ubu-side |
| 4. grace expiry | 2026-06-02 | EXT 측 banner-only OR archive-private OR delete (zero downstream cite condition) |

## 7. 정합 결과

| 항목 | Pre | Post |
|---|---|---|
| HF naming spec docs | 0 | 1 (this) |
| F-NAME-1 falsifier | undefined | defined + audit-runnable |
| canonical examples | implicit | 8 worked (§2.2) |
| anti-pattern catalog | scattered | 10 entries (§6) |
| migration plan | none | 30-day grace + banner-add cycle plan |
| 측 측 측 destructive | — | 0 |

## 8. caveats (raw#10 honest C3)

- **C1** — legacy `1-N` variant 측 측 측 측 측 paradigm 측 측 측 측 측 (P9 iter counter implicit)
- **C2** — `step-50k` 측 50K optimizer.step() vs 50K SFT records 측 측 측 측 측 README Origin section 측 disambiguator 역할
- **C3** — `paradigm-X` 측 7 letter (A/A'/B/C/D/E/J) 측 측 측 측 측 — 측 측 측 측 (F/G/H/I + K-Z) 측 측 측 측 (additive 측 spec doc + §3.3 update 측 측)

## 9. 잔존 작업 (next cycle 후보)

| 항목 | priority | rationale |
|---|---|---|
| 20 EXT 측 측 README banner add | HIGH | F-NAME-1 PARTIAL_PASS → FULL_PASS |
| `tools/hf-rename-legacy.py` impl | MED | bulk audit + dry-run + commit-flag-protected rename (raw#9 ubu-side concession) |
| pre-push CI hook (`hf-name-check`) | MED | F-NAME-1 enforcement at push time, 측 측 forward repo 측 측 측 측 |
| `nexus-singularity/` org spec extension | LOW | nexus-side artifacts (NLM family) 측 측 측 |
| paradigm letter enum extension (F-Z) | LOW | C3 caveat resolution + future research room |

## 10. 산출물 (재확인)

- `/Users/ghost/core/anima/docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md` (473 LoC, 15 §)
- `/Users/ghost/core/anima/docs/anima_hf_naming_mk2_spec_landed_2026_05_03.ai.md` (this handoff)
- `/Users/ghost/core/anima/state/markers/anima_hf_naming_mk2_spec_landed.marker`

## 11. 비용

- $0 mac-local (mac CPU + 1 read-only HF API list call)
- destructive 0
- 마이그레이션 0
- HF repo metadata diff 0
- byte-diff to any existing artifact 0
