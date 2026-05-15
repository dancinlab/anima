# HEXAD/SAVANT/proofs

> Canonical mathematical proofs supporting the SAVANT compendium.
> 출처: `~/core/archive-TECS-L/math/proofs/`. Read-only evidence anchors.

## 파일

| 파일 | 출처 | 용도 |
|---|---|---|
| `gz_analytical_proof.py` | archive-TECS-L (799 lines) | GZ_CENTER (1/e) / GZ_WIDTH (ln 4/3) closed-form 증명 — SAVANT compendium §1 의 canonical 상수 표 인용 출처 |

## 검증

```bash
python3 HEXAD/SAVANT/proofs/gz_analytical_proof.py    # numerical proof verify
```

## Honest C3

- 외부 archive-TECS-L 에서 copy (PR #85) — 원본 갱신 시 수동 sync (자동 mirror X)
- proof script 의 PROVEN / CONJECTURED / INTERPRETIVE 표기는 작자 (TECS-L) 의 자체 분류
- AGENTS.tape g3 real-limits-first 정책 하에서 GZ 는 design vocabulary classification — 본 증명은 vocabulary 의 mathematical foundation 만 보장 (실 시스템에 적용 시 별도 검증 필요)

## cross-link

- `../COMPENDIUM.md` §1 canonical 상수 표 (이 증명 인용)
- `../H359-savant-canonical.md` Savant H359 canonical doc
- `../SAVANT.tape` current architecture SSOT
