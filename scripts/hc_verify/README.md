# scripts/hc_verify/ — Hypothesis Candidate (Hc) Verification Pipeline

`hypotheses_candidates/Hc_*.md` 의 수학·물리적 검증 → `hypotheses/H_*.md` 승격 파이프라인. atlas.n6 anchor cross-check + n=6 primitives identity 검증.

> **Python 정책 (2026-05-12 update)**: 이전 `R37/AN13/L3-PY` (2026-04-18) Python 전면 차단 정책은 **scrub** 됨 (사용자 directive 2026-05-12). 현재 `verify_hc.py` / `batch_status_update.py` 둘 다 tracked + commit OK. 장기적으로 `.hexa` 포팅 권장하나 단기 transient 도구는 `.py` 그대로 유지.

## 구조

```
scripts/hc_verify/
├── verify_hc.py                       검증 harness (atlas anchor + n=6 math + falsifier/honest count)
├── batch_status_update.py             검증 결과 → Hc frontmatter status batch 갱신
├── README.md                          이 파일
└── cache_<YYYY_MM_DD>/                cycle 별 작업 cache (이전엔 /tmp, 이제 repo 내부 — `지속적으로 필요`)
    ├── batches/hc_all.txt + hc_batch_{1..8}.txt
    ├── triage/triage_{1..8}.jsonl + triage_all.jsonl + triage_5_fixed.jsonl
    ├── verify/verify_results.jsonl (v1) + verify2.jsonl + verify3.jsonl
    ├── ids/ripe_ids.txt + ripe_paths.txt + promote_ids.txt + needs_ids.txt + touched_files.txt
    ├── verify_hc_v1.py                초기 harness (history)
    └── triage_processor_agent.py      Stage 1 agent 가 작성한 helper (history)
```

cycle 새로 돌릴 때 `cache_<오늘날짜>/` 폴더 신규 생성, 기존은 보존.

## 사용법 (3-stage pipeline)

### Stage 1 — Triage (병렬 agent)

후보를 `RIPE / BORDERLINE / STUB / MERGED / DEAD` 로 분류. 1127개 기준 8 batch 병렬 (~3분).

```bash
# 후보 파일 8 batch 으로 split
ls hypotheses_candidates/Hc_*.md | sort > scripts/hc_verify/cache_2026_05_12/hc_all.txt
total=$(wc -l < scripts/hc_verify/cache_2026_05_12/hc_all.txt)
bs=$(( (total + 7) / 8 ))
for i in 1 2 3 4 5 6 7 8; do
  sed -n "$(( (i-1)*bs+1 )),$(( i*bs ))p" scripts/hc_verify/cache_2026_05_12/hc_all.txt > scripts/hc_verify/cache_2026_05_12/hc_batch_${i}.txt
done
# 각 batch 마다 Claude Code agent 실행 (Explore subagent_type 권장)
```

Agent prompt template (각 file → 1 JSON line `scripts/hc_verify/cache_2026_05_12/triage_N.jsonl`):

```
Triage hypothesis-candidate files. Read each .md file, classify:
  MERGED: frontmatter status starts with merged-to-H_
  RIPE: concrete math claim + falsifier list
  BORDERLINE: clear hypothesis but lacks formal predictions
  STUB: 1-paragraph only Migration TODO
  DEAD: duplicate/contradictory/suspended

Output JSON: {id, class, domain, status, title, merged_to, verifiable_claim,
              falsifier_count, math_signal}
```

### Stage 2 — 수학·물리 검증

```bash
# RIPE ID 추출 → 파일 경로 매핑
python3 -c "
import json, glob
ids = set()
for f in ['scripts/hc_verify/cache_2026_05_12/triage_%d.jsonl' % i for i in range(1,9)]:
    for ln in open(f):
        r = json.loads(ln)
        if r.get('class') == 'RIPE': ids.add(r['id'])
paths = []
for hc_id in ids:
    m = glob.glob(f'hypotheses_candidates/{hc_id}_*.md')
    if m: paths.append(m[0])
print('\n'.join(paths))
" > scripts/hc_verify/cache_2026_05_12/ripe_paths.txt

# 검증 실행
python3 scripts/hc_verify/verify_hc.py $(cat scripts/hc_verify/cache_2026_05_12/ripe_paths.txt | tr '\n' ' ') > scripts/hc_verify/cache_2026_05_12/verify_results.jsonl
```

Decision tier:
- `MATH_PASS_FULL`     — math + atlas + ≥3 falsifier + ≥3 honest → **즉시 승격**
- `PROMOTE_READY`      — math + ≥3 honest + ≥2 H cross-link → **즉시 승격 (falsifier 보강)**
- `MATH_PASS_NEEDS_F`  — math + atlas, falsifier 부재 → status 갱신
- `WEAK_MATH_ONLY`     — math 단독 → status 갱신
- `WEAK_FALSIFIER_ONLY` — falsifier 단독 → status 갱신
- `FAIL`               — 모두 부재 → status 그대로

수학 식별 (atlas.n6 anchor 기반):
- n=6 primitives: `σ=12`, `τ=4`, `φ=2`, `sopfr=5`, `J₂=24` (atlas @P [10*]+)
- Stefan-Boltzmann reduced: `π⁵/15 = 20.4013…`
- 2D Ising critical exponents: `β=1/8`, `γ=7/4`, `δ=15`, `η=1/4`, `ν=1` (Onsager EXACT)
- ln(2) = 0.693147 (universal constant)
- Perfect-number identity: `1+2+3=6`, `σ·φ=J₂` (12·2=24), `τ+φ=6` (4+2)
- balance = n/σ = 6/12 = 0.5 (Ψ-equilibrium)

### Stage 3 — 승격 + status batch 갱신

승격 후보 (PROMOTE_READY / MATH_PASS_FULL):
1. `hypotheses/H_NNN_<slug>.md` 신규 작성 — 10-section body (`H_153_dimension_hierarchy_n6.md` 템플릿)
2. 원본 Hc frontmatter 갱신:
   ```yaml
   status: merged-to-H_NNN
   merged_to: hypotheses/H_NNN_<slug>.md
   merged_at: 2026-MM-DD
   linked_h: ..., H_NNN (formal promotion <date>)
   ```

Batch status 갱신 (수학 검증 통과했으나 falsifier 부족한 다수):
```bash
python3 scripts/hc_verify/batch_status_update.py
# verify3.jsonl → 각 Hc frontmatter 에 verify_decision + verify_note 추가
```

## 검증 결과 cache (2026-05-12 1st cycle)

| Phase | Output |
|---|---|
| Phase A triage | RIPE=292 / BORDERLINE=261 / STUB=500 / MERGED=74 / total=1127 |
| Phase B verify | PROMOTE_READY=2 (Hc_035, Hc_061) + MATH_PASS_NEEDS_*=8 + WEAK_MATH=67 + WEAK_FALSIFIER=15 |
| Phase C promote | H_156 (NEXUS-6 cross-validation cluster), H_157 (Mathematical Panpsychism) |
| Phase D batch | 90 Hc files → candidate-math-verified-* status |

## 다음 cycle 추가 검증 후보 영역

- **Ψ-constants** (Hc_002, Hc_046, Hc_406, Hc_453) — ln(2) + n=6 closed-form 22-of-30 EXACT — H_158 후보
- **n=6 primitives full closure** (Hc_378 — 98181 closed-form basis) — H_067 보강
- **IIT Φ formulations** (Hc_121 log-ratio, Hc_141 cross-partition) — H_011 IIT-geometry 확장
- **Topology cluster** (Hc_156 hybrid, Hc_157 hypercube, Hc_165 small-world, Hc_169 optimal) — H_040 substrate-topology 확장
- **Hexad architecture** (Hc_471 φ(6)=2 gradient groups) — H_038 v8-architecture 확장

## atlas anchor 권장 lookup

```python
from pathlib import Path
atlas = Path("n6/atlas.n6").read_text()
# count constants
print(atlas.count("ANIMA-"))  # 134 anchors (2026-05-12)
print(atlas.count("\n@P "))    # 437 primitives
print(atlas.count("\n@C "))    # 5699 constants
print(atlas.count("\n@L "))    # 514 laws
```
