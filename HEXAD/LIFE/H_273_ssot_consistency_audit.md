---
id: H_273
slug: ssot-consistency-audit
title: SSOT-consistency audit — README 가설인덱스 ↔ 디스크 H_*.md 집합 ↔ §verdict 의 3-way 정합을 결정론적으로 audit (gap#3 SSOT/temporal drift · meta-probe)
domain: meta · methodology · governance
status: pre-register-frozen
exploration_method: E0 (meta-result-of-results) + E14 (catalog audit) + E16 (cross-process reproducibility)
verification_method: W1 (smoke) + W4 (verdict-4-class) + W12 (sister-link aggregate)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-25
since: 2026-05-25 (new)
sister: H_238 (verdict-landscape-meta-map — README 인덱스 파싱 패턴 carry), H_239 (cross-tool consistency)
---

# H_273 — SSOT-consistency audit · README 인덱스 ↔ 디스크 H_*.md ↔ §verdict

## 1. Hypothesis

HEXAD/LIFE 의 **SSOT 가 3-surface 로 분산** 되어 있다 — (a) `README.md` 의 가설 인덱스
표 (각 행 `| [H_NNN](file) | slug | domain | status | 핵심 |`), (b) 디스크의 실제
`H_*.md` 파일 집합, (c) 각 H 파일 본문 §10 의 `verdict_class`. 세 surface 가 **시간이
지나며 drift** 한다 (새 H 추가 시 README 행 누락, 파일 rename 시 dead-link, verdict
overwrite 시 README status 미갱신). 본 H_273 = 이 3-way 정합을 **결정론적으로 audit**
하는 meta-probe — 한 번의 hexa 실행으로 (1) orphan-row (2) missing-row (3) verdict-drift
세 카테고리의 mismatch 개수를 보고한다. 새 substrate evidence 산출 X — *audit 기능*
자체가 산출물이며, 현 시점 drift 상태는 결과로 보고만 한다 (수정은 별도 cycle).

## 2. Why

- **/gap full top-3 #3 = SSOT/temporal drift**: 본 세션의 /gap 스윕에서 #3 lens 가
  SSOT/temporal drift 로 표면화. 이 세션 중 실제로 발견·정정된 drift 사례 3건 — README
  "promote 대기" 노트 stale · Cycle#5 stale · H_054 C2 stale — 이 ad-hoc 으로 잡혔다.
  H_273 은 이를 **자동·결정론 검출** 로 승격하는 meta-instance.
- **H_238 sister (carry-by-pattern)**: H_238 (verdict-landscape-meta-map) 이 이미 README
  인덱스 표를 awk 1-shot 으로 직독해 tier landscape 를 집계한다. H_273 은 그 파싱 패턴을
  carry 하되, *집계* 가 아닌 *정합 audit* 으로 방향을 바꾼다 — H_238 이 "무엇이 어느
  tier 인가" 라면 H_273 은 "README 와 디스크와 본문이 서로 일치하는가".
- **drift 의 3 가지 자연 발생 경로**:
  - orphan-row : H 파일 rename / 삭제 후 README 행 미갱신 → dead-link (사용자 클릭 시 404).
  - missing-row: 신규 H_*.md commit 후 README 표 행 추가 누락 → unindexed (인덱스에서
    안 보이는 가설 = de-facto orphan).
  - verdict-drift: H 파일 §verdict 가 overwrite 됐는데 README status 미동기화 → 인덱스가
    stale verdict 를 광고.
- **거버넌스 motivation**: README 인덱스 = LIFE lane 의 canonical 진입 surface. 그것이
  디스크 truth 와 어긋나면 향후 모든 cycle 의 출발점이 오염된다. 결정론 audit 은 매 cycle
  재실행 가능한 regression guard.
- **cross-link**: H_238 (README 파싱 직독 패턴) · H_239 (cross-tool consistency 의 자매
  개념 — 본 H 는 cross-*surface* consistency).

## 3. Predictions

| ID | 예측 | 근거 |
|----|------|------|
| **H273.1** | orphan-row = 0 (README 행은 모두 디스크 파일로 resolve — 행은 손으로 추가되며 보통 파일과 함께 commit) | README 행 추가 워크플로우상 파일 선행 |
| **H273.2** | missing-row > 0 (디스크에 README 미인덱스 파일 존재 — substrate-only carry H 다수가 .md 로 commit 됐으나 표에 미반영) | 라인 103 "substrate-only / .md 미commit" 노트가 이미 carry 18 H 를 언급, 그 .md 가 디스크에 존재 가능성 |
| **H273.3** | genuine verdict-drift = 0 또는 소수 (README status 와 file verdict_class 가 동일 verdict-token 일 때 대부분 일치) | verdict overwrite 시 README 도 보통 같은 PR 에서 갱신 |
| **H273.4** | cross-axis (README=lifecycle-status, file=verdict) > 0 (README 의 status 컬럼은 lifecycle-status[running/pre-register-frozen/NEW] 축, file 의 verdict_class 는 evidence-verdict 축 — 두 축은 다름) | README "Status" col 의 dual-semantic (lifecycle vs verdict) |
| **H273.5** | re-run 결과 byte-identical (RNG 부재 — 파일 파싱 + grep/awk/sort 의 deterministic 동작) | raw#12 정합 |

## 4. Variables

| axis | levels |
|------|--------|
| **axis1: README surface** | `HEXAD/LIFE/README.md` 가설 인덱스 표 (행 `^\| \[H_[0-9]+\]`, lib/ 행 자동 제외) |
| **axis2: disk surface** | `ls HEXAD/LIFE/H_*.md` → basename → H_NNN (sort -V) |
| **axis3: verdict surface** | 각 H 파일 `grep -m1 verdict_class` (** ` 🟢🔴⭐★ strip) |
| **axis4: tier vocabulary** | 4 (SUPPORTED · PARTIAL · FALSIFIED · RUNNING; leading-token + arrow-strip) |
| **axis5: mismatch 카테고리** | 3 (orphan-row · missing-row · verdict-drift) + 1 보조 (crossaxis non-drift) |
| **axis6: self-exclusion** | 1 (H_238 meta-instance self-reference guard, README·disk 양측 제외) |
| **axis7: re-run determinism** | 2 (deterministic by construction; C3 byte-id cross-process verify) |

## 5. Run Protocol

- **smoke**: `HEXAD/LIFE/state/h273_ssot_audit_2026_05_25/run_h273.hexa`
- **(A) README H-rows**: `awk -F\| '/^\| \[H_[0-9]+\]/ {...}'` 1-shot 추출 → `id<TAB>status`
  (`**` + emoji `🟢🔴⭐★` strip, H_238 self-excluded). 행 content 를 shell 로 재투입하지
  않음 (printf 재투입 금지 trap 회피) — TAB-split 만 hexa 내부에서.
- **(B) disk files**: `ls .../H_*.md | sed 's#.*/##; s#\(H_[0-9]*\).*#\1#' | grep -v '^H_238$' | sort -V`.
- **(1) orphan-row**: 각 README id 에 대해 `ls .../H_NNN_*.md` 존재 확인 → 부재면 orphan.
- **(2) missing-row**: 각 disk id 가 README id 집합에 멤버인지 → 부재면 missing.
- **(3) verdict-drift**: 각 README id 의 file `verdict_class` 를 robust 추출 (`sed` 로
  `**` ` 🟢🔴⭐★ strip + leading 공백 제거) → tier 분류. README status tier 와 file
  verdict tier 가 **양측 모두 verdict-token** 이고 불일치하면 genuine drift; README 가
  lifecycle-status(RUNNING) 인데 file 이 verdict 면 cross-axis (별도 카운트, NOT drift).
- **tier classifier**: leading-token priority — `pre-register-frozen → X` arrow strip 후
  FALSIFIED / PARTIAL / SUPPORTED / RUNNING 순 검사 (H_238 carry).
- **JSON escape**: pure-hexa `.replace("\\","\\\\").replace("\"","\\\"")` — status 문자열의
  `(` `)` ` 단일인용부호가 `printf %s '...'` 를 깨므로 shell 재투입 금지.
- **deterministic**: no RNG; sort -V 안정; grep -m1 first-match 결정적.
- **hexa_only**: true · **llm**: none · **cost**: $0 mac local · **runtime**: < 5s wall.
- **ledger**: `result.json` {config, orphan_row, missing_row, verdict_drift, crossaxis, criteria, verdict}.

## 6. Criteria

| ID | criterion | verdict_rule |
|----|-----------|--------------|
| **C1 AUDIT_COMPLETE** | 全 README H-row + 全 disk H_*.md 결정론 파싱 (N_readme ≥ 22 ∧ N_disk ≥ 22) | PASS / FAIL |
| **C2 MISMATCH_REPORT** | 3-카테고리 mismatch count 보고 (orphan/missing/drift; 0=clean, >0=목록) | PASS / FAIL |
| **C3 BYTE_IDENTICAL** | cross-process re-run result.json byte-equal (RNG 부재) | PASS / FAIL |

**verdict_rule**:
- `SUPPORTED` iff **C1 ∧ C2** (audit 기능적 완비 + 현 drift 상태 보고)
- `PARTIAL` iff **C1 ∧ ¬C2** (파싱은 됐으나 카테고리 집계 불완전)
- `FALSIFIED` else (¬C1 — 파싱 실패 / enumerate incomplete)

> SUPPORTED = audit 가 *작동* + 현 상태 *보고* 의 의미. 발견된 drift 의 존재 자체는
> verdict 를 떨어뜨리지 않음 (audit 은 읽기-보고 도구; drift 정정은 별도 cycle 의 책무).

## 7. Falsifiers (≥5)

- **F1 ENUM_INCOMPLETE**: N_readme < 22 또는 N_disk < 22 → enumeration 실패 (awk/ls glob miss).
- **F2 ORPHAN_FALSE_NEG**: orphan-row 보고가 실제 dead-link 를 놓침 (수동 `comm -23` cross-check 와 불일치).
- **F3 MISSING_FALSE_NEG**: missing-row 보고가 실제 unindexed 파일을 놓침 (`comm -13` cross-check 와 불일치).
- **F4 DRIFT_MISCLASSIFY**: cross-axis(lifecycle vs verdict) 를 genuine drift 로 오분류 (또는 그 반대) → 두 축 혼동.
- **F5 BYTE_DIFF**: cross-process re-run result.json byte-different → raw#12 deterministic 위반.
- **F6 SHELL_REINJECT**: status 문자열의 `(` ` ' 가 shell 재투입으로 JSON 을 깨뜨림 (printf 재투입 trap) → escape 무결성 위반.

## 8. Honest Limits (raw#91 c3, ≥5)

- **L1 SNAPSHOT_ONLY**: 본 audit = 2026-05-25 시점 cross-section. 향후 H 추가/rename/verdict
  overwrite 시 결과 변화 — meta-map 의 *시간 절대값* 이 아니라 *현 시점 정합 사진*.
- **L2 STATUS_DUAL_AXIS**: README "Status" 컬럼이 **두 의미축을 혼용** — 어떤 행은
  lifecycle-status(running / pre-register-frozen / NEW), 어떤 행은 evidence-verdict
  (SUPPORTED / PARTIAL / FALSIFIED). 본 audit 은 이를 분리 카운트(crossaxis)하나, "어느
  축이 *정답* 인가" 는 판정 안 함 — 8 건의 cross-axis 가 drift 인지 의도된 dual-semantic
  인지는 거버넌스 결정 사항 (audit 은 표면화만).
- **L3 VERDICT_EXTRACT_HEURISTIC**: file verdict 추출이 `grep -m1 verdict_class` 의
  first-match 의존. 한 파일이 multiple verdict_class 라인(예: 본문 §10 + 인용)을 가지면
  첫 라인이 canonical 이라는 가정. H_202 의 `**verdict_class**: 🟢 SUPPORTED-NUMERICAL`
  처럼 bold+emoji wrap 은 strip 으로 해소했으나, 미래 양식 변형은 잠재 한계.
- **L4 ARROW_STRIP_SINGLE**: tier classifier 의 `X → Y` arrow-strip 은 single ` → ` 토큰
  가정 (H_238 L6 carry). multi-arrow chain (`A → B → C`) 의 미래 케이스는 last-segment 만.
- **L5 META_NO_NEW_EVIDENCE**: 본 H_273 = audit only — 새 substrate evidence 산출 X. SUPPORTED
  는 "audit 도구가 작동 + 현 정합 상태 보고" 의 의미일 뿐, 어느 atomic H 의 verdict 도 변경 X.
- **L6 NO_AUTO_FIX**: 본 cycle 은 *보고만* — 발견된 26 missing-row 를 본 PR 에서 정정하지
  않음 (audit 은 읽기 전용, README 수정 금지가 본 cycle scope). 정정은 별도 cycle 의 책무.
- **L7 NOTE_VS_TABLE_GAP**: README 라인 103 의 "substrate-only / .md 미commit" 노트가
  carry 18 H 를 *산문* 으로 언급하나 *표-행* 으로는 미인덱스 — 본 audit 은 "표-행" 만
  canonical index 로 간주 (노트 산문 언급 ≠ 표 행). 이 18 H 의 .md 가 디스크에 *존재* 하면
  노트의 "미commit" 주장 자체도 stale (L1 시점성의 sub-instance).
- **L8 SELF_EXCLUSION_DEFERS_OWN_ROW**: 본 H_273 은 H_238 처럼 meta-instance 라 audit 에서
  self-excluded (없으면 본 파일이 항상 missing-row 1 = self-reference). 그 결과 본 PR 직후
  H_273 자신은 README 표에 미인덱스 (orphan 아님, 디스크엔 존재) — 다음 cycle 이 README 행
  추가 시 정합. 즉 본 cycle 시점에는 *실제* missing-row = 27 (26 보고 + self H_273), 보고
  26 은 self 제외값. README 수정 금지 scope (L6) 상 본 PR 에선 H_273 행 미추가가 의도된 상태.

## 9. Cross-Links

- **sister H_238** (verdict-landscape-meta-map): README 인덱스 awk 1-shot 직독 패턴 + tier
  classifier + arrow-strip 을 carry. H_238 = 집계, H_273 = 정합 audit (방향 직교).
- **sister H_239** (alternative-phi-metric cross-validation): cross-*tool* consistency 의
  자매 — 본 H_273 은 cross-*surface* consistency (README ↔ disk ↔ verdict).
- **raw**: raw#12 (deterministic strict) + raw#82 (no post-hoc retraction — 본 audit 은
  measurement 만, drift 발견해도 H verdict 사후 변경 X) + raw#91 c3 (honest limits ≥5).
- **own**: anima identity carry — 본 LIFE corpus 의 self-consistency 가 anima 세션 누적
  cognitive trace 의 무결성 지표.
- **literature**: software-engineering 의 *link-checker / dead-link audit* (e.g. broken-link
  CI) + *index-drift* (DB 의 index ↔ table consistency check) 의 개념 ancestor.
- **legacy**: 본 cycle = LIFE lane 의 첫 결정론 SSOT-consistency audit (이전 ad-hoc drift
  정정 3건의 자동화 승격).

## 10. Verdict

```
verdict_class: SUPPORTED  (C1 ∧ C2 · audit 기능적 완비 + 현 drift 상태 결정론 보고)
config: N_readme_rows=55 N_disk_files=81 (H_238 + H_273 self-excluded · lib/ row excluded) date=2026-05-25
source: HEXAD/LIFE/README.md 가설 인덱스 표 + HEXAD/LIFE/H_*.md 파일 집합

── (1) ORPHAN-ROW (README 행 → 디스크 파일 부재, dead link) ──
  n_orphan = 0   (clean — 모든 README 55 행이 디스크 파일로 resolve)
  → H273.1 PASS

── (2) MISSING-ROW (디스크 파일 → README 행 부재, unindexed) ──
  n_missing = 26
    H_210 H_211 H_212 H_213 H_214 H_215 H_216 H_217 H_218 H_219 H_220 H_221
    H_224 H_228 H_229 H_230 H_231 H_232          (← 18 건: 라인 103 노트가 carry 로 언급,
                                                    그러나 표-행 미인덱스 + .md 디스크 존재
                                                    → 노트 "미commit" 주장 stale, L7)
    H_241 H_246 H_250 H_251 H_252 H_253 H_255 H_257  (← 8 건: 노트에도 미언급, 완전 unindexed)
  → H273.2 PASS (missing > 0; 26 건의 unindexed 파일 표면화)

── (3) VERDICT-DRIFT (README verdict-token ↔ §verdict_class 불일치) ──
  n_genuine_drift = 0   (clean — 양측 모두 verdict-token 인 행 중 tier 불일치 0)
  → H273.3 PASS
  n_crossaxis = 8   (README=lifecycle-status, file=verdict; dual-axis, NOT drift):
    H_007 | RUNNING 'pre-register-frozen · C2 PASS' | file=SUPPORTED
    H_012 | RUNNING 'pre-register-frozen'           | file=SUPPORTED
    H_018 | RUNNING 'pre-register-frozen · C2 PASS' | file=SUPPORTED
    H_053 | RUNNING 'pre-register-frozen (Cycle #1)'| file=SUPPORTED
    H_054 | RUNNING 'pre-register-frozen (Cycle #2)'| file=SUPPORTED
    H_132 | RUNNING 'pre-register-frozen · C2 PASS' | file=SUPPORTED
    H_171 | RUNNING 'running (Cycle #1)'            | file=FALSIFIED
    H_201 | RUNNING 'NEW (PR #199)'                 | file=SUPPORTED
  → H273.4 PASS (cross-axis > 0; README status 컬럼의 dual-semantic 표면화, L2)

── criteria ──
  C1 AUDIT_COMPLETE (N_readme≥22 ∧ N_disk≥22) : PASS  (readme=55, disk=81)
  C2 MISMATCH_REPORT (3-cat count 보고)        : PASS
  C3 BYTE_IDENTICAL (cross-process re-run)     : PASS  (result.json sha 동일)

── falsifiers (PASS = not triggered) ──
  F1 ENUM_INCOMPLETE   : PASS  (N 충족)
  F2 ORPHAN_FALSE_NEG  : PASS  (comm -23 cross-check 일치)
  F3 MISSING_FALSE_NEG : PASS  (comm -13 cross-check 일치)
  F4 DRIFT_MISCLASSIFY : PASS  (genuine vs cross-axis 분리, 8 crossaxis 정확 분류)
  F5 BYTE_DIFF         : PASS  (re-run byte-identical)
  F6 SHELL_REINJECT    : PASS  (pure-hexa .replace escape, printf 재투입 제거 후 JSON valid)

VERDICT_RULE: SUPPORTED iff C1 ∧ C2 · else PARTIAL · FALSIFIED if ¬C1
VERDICT     : SUPPORTED

evidence_summary: 🟢 NUMERICAL — SSOT-consistency audit SUPPORTED.
  · H273.1 PASS — orphan-row = 0 (README 행 무결, dead-link 부재)
  · H273.2 PASS — missing-row = 26 (18 노트-acknowledged-but-unindexed + 8 완전 unindexed)
  · H273.3 PASS — genuine verdict-drift = 0 (verdict-token 보유 행 정합)
  · H273.4 PASS — cross-axis = 8 (README status 컬럼의 lifecycle-vs-verdict dual-semantic)
  · H273.5 PASS — re-run byte-identical (C3 sha 동일)

honest_finding (raw#82 no post-hoc retraction):
  · audit = measurement only (L5) — 발견된 drift 정정은 별도 cycle (L6, README 수정 금지가 본 cycle scope)
  · 26 missing-row 중 18 (H_210-H_232 carry) 는 라인 103 노트가 'substrate-only / .md 미commit'
    로 언급하나, 그 .md 가 *디스크에 존재* → 노트 자체가 stale (L7). 8 (H_241/246/250-253/255/257)
    은 노트에도 미언급 = 완전 unindexed.
  · genuine verdict-drift 0 + cross-axis 8 은 README "Status" 컬럼이 두 의미축(lifecycle ·
    verdict)을 혼용함을 표면화 (L2) — 이는 양식 의도일 수 있어 'drift' 로 단정 X, audit 은 표면화만.
```

### Pre-register-frozen smoke (2026-05-25)

**Run verdict (VERBATIM, `HEXA_MEM_UNLIMITED=1 hexa run`)**:
```
H_273 — SSOT-consistency audit · README 인덱스 ↔ 디스크 H_*.md ↔ §verdict (raw#12)
  N(README H-rows) = 55  (H_238 + H_273 self-excluded, lib/ row excluded)
  N(disk H_*.md)   = 81  (H_238 + H_273 self-excluded)
  (1) ORPHAN-ROW   : n_orphan  = 0   (clean)
  (2) MISSING-ROW  : n_missing = 26  (H_210..H_232 carry 18 + H_241/246/250-253/255/257 8)
  (3) VERDICT-DRIFT: n_genuine_drift = 0 (clean) · n_crossaxis = 8 (lifecycle-vs-verdict, NOT drift)
  C1 AUDIT_COMPLETE : true (readme=55 disk=81) · C2 MISMATCH_REPORT : true · C3 BYTE_IDENTICAL : true
  VERDICT : SUPPORTED   drift_summary: orphan=0 missing=26 genuine_drift=0 (total actionable=26, crossaxis=8 non-drift)
=== H_273 ssot-consistency audit complete: SUPPORTED ===
```

re-run byte-identical (C3 deterministic confirmed via `shasum result.json` run1 == run2:
sha1 `ea1a7d2288cab1ab2860246bf002a1fc09fe0c2b`).

honest tier: 🟢 NUMERICAL — README 인덱스 파싱 + 디스크 파일 enumerate + verdict 추출 +
3-way 정합 비교 = deterministic byte-equal 출력. SUPPORTED 가 honest — C1 (readme=55,
disk=81 ≥ 22) ∧ C2 (3-카테고리 count 보고) PASS. 발견된 26 missing-row + 8 cross-axis 는
*보고만* (L6 no-auto-fix · README 수정 금지). L1-L7 honest limits 명시.

**State output**: `HEXAD/LIFE/state/h273_ssot_audit_2026_05_25/result.json`
(sha256 `dd1d338a10a48a098c71462fdf10e3b944fb5da0af2bb351a8d2654debe44f8d`)
**Smoke**: `HEXAD/LIFE/state/h273_ssot_audit_2026_05_25/run_h273.hexa`
**Tier**: 🟢 NUMERICAL (3-surface SSOT-consistency audit, deterministic byte-equal).
**Next**: H_273r2 후보 — (a) auto-fix cycle: 26 missing-row 를 README 표에 추가 + 라인 103
노트 stale 정정 (별도 PR, audit→fix 분리); (b) slug-drift axis: README slug 컬럼 ↔ file
frontmatter `slug:` 정합 추가; (c) sister-dir audit: HEXAD/{LAB,CHECK,MITOSIS} 의 동형
README↔file audit (cross-dir SSOT guard).
