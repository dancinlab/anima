# raw 15 residual leak spec — 2026-05-01 (cycle re-launch 2026-05-02)

**status**: spec-only · roll-out plan (변환 작업 X, 다음 cycle 위임)
**scope**: F5+7 retro-fit batch (commit `71f5d42cc`, 282 files) 이후 잔여 leak 464건의 분류 / 검증 protocol / ω-cycle 분할
**raw cross-references**: raw 9 (hexa-only enforcement) · raw 10 (honest C3) · raw 15 (personal-path-leak-ban-iter5) · raw 71 (falsifier registration) · raw 91 (honesty triad C2 write_barrier)
**predecessor**: `docs/raw_audit_backfill_20260421.md` (raw 15 iter4 ledger)
**re-launch note**: 본 cycle 직전 attempt 는 G3 quota 차단으로 중단. 2026-05-02 재발사 시 spec 본문 보존 + §11 re-launch addendum 으로 보강. 변환 surface 변동 없음 — sampling re-snapshot 미수행 (raw 10 honest C3 §6.1 잔존).

---

## §0 Executive summary

F5+7 batch (`71f5d42cc`) 760+ historical absolute-path leak 중 282 file 변환 완료 — 잔여 **464 leak SKIP** 상태. SKIP 사유 5개 카테고리 (위험 수준 순):

| 카테고리 | 건수 | risk | 변환 우선순위 |
| --- | --- | --- | --- |
| `.hexa` source | 323 | high (resolver runtime break) | Phase 6a — smoke test 동반 단계적 |
| `tool/*.bash` | 29 | high (deploy chain) | Phase 6b — sandbox dry-run |
| uchg `.md` | 18 | mid (ownership consent) | Phase 6c — chflags ceremony |
| `.log` rotation | 60+ | low (history immutable) | 변환 면제 권장 (rotation 정책으로 흡수) |
| 기타 binary/db | 30+ | n/a | 변환 불가 — 면제 |

총 ω-cycle estimate: **18-26 hours** (Phase 6a 12-16h + 6b 4-6h + 6c 2-4h).

본 문서는 **spec only** — 실제 변환은 별도 sub-cycle 에서 falsifier (raw 71) + honest C3 (raw 10) 통과 시에만 진행.

---

## §1 잔여 leak categorize (read-only audit)

### §1.1 `.hexa` source — 323 leaks

위치 분포 (대략):
- `<repo-root>/../hexa-lang/src/**/*.hexa` (대다수, ≈220)
- `<repo-root>/anima-clm/.../*.hexa` (≈60)
- `<repo-root>/anima-eeg/.../*.hexa` (≈40)
- 기타 (≈3)

leak 패턴 분포 (추정 sampling 기반):
- absolute path → resolver hint (`@cwd`, `@repo`) 변환 필요 ≈ 70%
- shebang / runtime path 의존 ≈ 20%
- legacy alias `<user-home>/Dev/anima` ≈ 10%

**resolver dependency**: hexa-lang의 module loader (`hexa_lang_module_loader_collision_20260427_landing.md` 참조) 가 `@cwd` 기반 token 을 이미 지원함 — 이론상 변환 가능. 단, 일부 .hexa 가 실행 시점에 absolute path 를 stringly-typed 로 받는 케이스가 있어 grep 만으로 안전성 보장 불가.

위험: 변환 후 resolver 가 path 를 못 찾으면 `module-not-found` runtime fault → 의존하는 verifier chain 동시 break.

### §1.2 `tool/*.bash` — 29 leaks

위치: `<repo-root>/tool/*.bash`, `<repo-root>/anima-eeg/scripts/*.bash`, launchd plist target

leak 패턴:
- launchd `<key>WorkingDirectory</key>` 절대 path
- cron job `cd <user-home>/...` prefix
- smoke harness 의 hard-coded venv path

**deploy chain**: `state/h100_auto_kill_last_run.json` / `state/lint_cron_history.jsonl` 가 이 .bash 들에 의존. 잘못 변환 시 cron 침묵 실패 (`silent fail`) 가능 — log 만 보면 정상으로 보임.

위험: launchd plist 는 absolute path 를 요구하는 macOS 규약 — 일부 leak 은 **legitimate / 면제 대상** 일 수 있음. 1-by-1 분류 필요.

### §1.3 `.log` — 60+ leaks

위치: `<repo-root>/state/**/*.log`, `<repo-root>/.raw-audit/*.log`

leak 패턴: 과거 실행 시 stdout/stderr 가 absolute path 를 capture — **historical immutable**.

권장: 변환 X. 대신 raw 15 iter6 spec 에 "log rotation 시 신규 entry 만 relative path 강제" 규칙 추가 → 시간이 지나면 자연 소멸. 현 leak 은 문서적 audit trail 로 보존.

### §1.4 uchg `.md` — 18 leaks

위치 (추정): `<repo-root>/../hexa-lang/.raw`, `<repo-root>/../hexa-lang/.own`, `<repo-root>/../hexa-lang/.ext`, `<repo-root>/.raw-audit/*.md`

leak 패턴: SSOT canonical doc 안에 absolute path 가 인용 (예: example block, error trace).

**chflags ownership**: 18 file 중 일부는 본 repo (anima) 외부 (hexa-lang) 에 위치 — peer repo 의 unlock ceremony 권한 없음 (raw_audit_backfill_20260421.md §"Lock ceremony feasibility" 와 동일 상황). 사용자 동의 + cross-repo ceremony 필요.

위험: chflags 우회 시도 시 raw 95 위반 (audit ledger tamper seal break).

### §1.5 기타 — 30+ leaks

- binary `.npy` / `.parquet` / `.db` / `.sqlite` — 변환 불가
- `.pyc` cache — gitignore 추가 권장
- screenshot / pdf — 변환 불가

권장: 변환 면제. raw 15 iter6 spec exclusion list 에 등재.

---

## §2 `.hexa` resolver dependency 검증 protocol (Phase 6a)

목표: 323 .hexa leak 을 안전 변환. resolver 가 `@cwd` / `@repo` token 을 정확히 해석함을 file-level 로 검증.

### §2.1 단계

1. **canary 선정**: 의존 그래프상 leaf 인 .hexa 5개 (verifier chain 영향 minimal) → 변환 후보 1차.
2. **변환**: F5+7 mapping 적용 (anima absolute root → `<repo-root>/`).
3. **smoke test**: `hexa run <canary>.hexa --dry-run` + module loader trace 캡처.
4. **roll-back gate**: smoke 실패 시 `git checkout HEAD -- <canary>` 즉시 복구. raw 71 falsifier ledger 에 fail 등록.
5. **chain expand**: canary 5개 통과 시 leaf-1 layer 까지 확장 (≈30 files). 동일 protocol 반복.
6. **commit gate**: 각 batch 30 files 단위 commit, `git diff --cached --name-only` count 검증.

### §2.2 합격 기준

- smoke test stdout 에 `module-not-found` / `resolver-hint-fail` 0건
- `hexa run` exit code 0 (모든 canary)
- 의존 verifier (예: `tool/lint_cron.bash`, `tool/raw_audit_drill.bash`) 정상 작동 — 변환 전후 동일 verdict

### §2.3 falsifier (raw 71)

- canary 5개 중 1개라도 smoke 실패 → 해당 batch 전체 retire, 변환 표 재작성
- resolver 가 새 token 을 해석 못함이 입증되면 raw 15 iter5 spec 자체에 exclusion clause 추가

---

## §3 `.bash` launchd/cron 검증 protocol (Phase 6b)

목표: 29 .bash leak 을 deploy chain break 없이 변환.

### §3.1 단계

1. **분류**: 29 file 을 3 그룹 분리.
   - (a) launchd plist 가 요구하는 legitimate absolute (변환 면제 후보)
   - (b) cron prefix `cd <user-home>/...` (변환 가능, 단 cron user context 검증 필요)
   - (c) smoke harness venv hard-code (변환 가능, `$REPO_ROOT` env var 도입)
2. **sandbox dry-run**: 임시 bash subshell 에서 변환된 script 실행, side-effect 차단 (`--dry-run` flag 추가).
3. **launchd reload test**: plist 재로드 (`launchctl unload && load`) 후 1 cycle 관찰. 침묵 실패 감지를 위해 `state/lint_cron_history.jsonl` 새 entry 출현 확인.
4. **rollback**: 침묵 실패 의심 시 즉시 git revert + launchctl reload 원본.

### §3.2 합격 기준

- launchd / cron 1 cycle 후 expected ledger entry 정상 append
- script 의 exit code, stdout signature 변환 전후 동일

### §3.3 falsifier (raw 71)

- 1 cycle 후 ledger entry 누락 / shape 변형 → 해당 .bash retire
- launchd plist 가 macOS 규약상 변환 불가로 입증되면 spec exclusion 추가

---

## §4 uchg `.md` 처리 protocol (Phase 6c)

목표: 18 uchg-locked .md 를 사용자 동의 + cross-repo ceremony 로 변환.

### §4.1 단계

1. **list 확정**: `find` + `ls -lO` 로 18 file 정확한 위치, owning repo, uchg flag 상태 sweep. read-only — 변환 X.
2. **owning repo 분류**: anima-internal (≈?) vs hexa-lang external (≈?) vs other.
3. **사용자 consent gate**: 각 file 별 1-line 표 제출 — "이 file 을 변환해도 될까요?" yes/no/skip.
4. **ceremony**:
   - anima-internal: `chflags nouchg` → edit → `chflags uchg` → audit ledger append (raw 95 schema)
   - hexa-lang external: peer repo cwd 로 이동 후 동일 ceremony, 단 hexa-lang `.raw-audit` ledger 에 append (anima ledger 아님)
5. **shadow append fallback**: ceremony 권한 부재 시 raw_audit_backfill_20260421.md §"shadow mode" 패턴으로 .raw-audit-shadow 에 변환 의도만 기록, 실제 변환 보류.

### §4.2 합격 기준

- 변환된 file 의 uchg flag 재설정 확인 (`ls -lO` 에 `uchg` 표시)
- audit ledger 에 cycle 1 row 추가, raw 95 schema 8-field 준수
- 사용자가 명시적 yes 없이 변환된 file 0건

### §4.3 falsifier (raw 71)

- 사용자 no/skip 인 file 이 변환되어 발견 → 즉시 git revert + chflags 복구 + raw 95 incident ledger 등재
- ceremony 후 uchg flag 가 재부착 안된 file 발견 → 동일 처리

---

## §5 raw 71 falsifier 통합 ledger

각 Phase 6a/6b/6c 진행 중 falsifier trigger 발생 시 동일 schema 로 단일 ledger 에 append:

```
state/raw_15_iter6_falsifier.jsonl
```

8-field pipe schema (raw 95 호환):

| key | meaning |
| --- | --- |
| `ts` | ISO8601 UTC |
| `phase` | `6a` / `6b` / `6c` |
| `target` | relative path (raw 15 강제) |
| `verdict` | `RETIRE` / `ROLLBACK` / `EXCLUDE` |
| `evidence` | smoke / dry-run / consent 결과 hash |
| `commit` | rollback 대상 sha |
| `seed` | sha256(target+ts) 12-char |
| `lens` | `resolver` / `deploy-chain` / `chflags-ceremony` |

---

## §6 raw 10 honest C3 — 한계 10항목

본 spec 자체의 미입증 / 추정 / 한계 10건을 명시. 다음 cycle 진행 전 검증 의무.

1. **leak count 464**: 변환 SKIP 카운트는 `71f5d42cc` commit 직후 grep snapshot 기반 추정 — 실제 재계산 미수행.
2. **카테고리 건수**: 323 / 29 / 60+ / 18 / 30+ 분포는 surface scan 추정. 정확한 file list 미제출.
3. **hexa resolver `@cwd` 지원**: `hexa_lang_module_loader_collision_20260427_landing.md` 인용 — 본인 검증 X.
4. **launchd plist absolute 요구**: macOS 규약 통념. 실제 launchd 8.0+ 에서 relative path + WorkingDirectory 조합 가능 여부 미검증.
5. **uchg 18 file 위치**: hexa-lang 외부 vs anima 내부 비율 추정만, `find` 미실행.
6. **smoke test 통과 기준**: "exit 0 + module-not-found 0건" 이 충분조건임을 가정 — 실제로 silent partial-init fault 가능성 배제 못함.
7. **18-26h estimate**: file 당 평균 처리 시간 가정 — 실측 wall-clock 데이터 없음.
8. **shadow append fallback**: raw_audit_backfill 에서 검증된 패턴이지만 18 uchg .md 에 동일 적용 가능성 미입증.
9. **resolver token 호환성**: `@cwd` / `@repo` / `<repo-root>` 3가지 token 의 resolver-side 동치 여부 미검증.
10. **본 spec doc 자체의 leak 0**: 작성 직후 grep 검증 (§9 참조) 통과를 가정.

---

## §7 ω-cycle 분할

| Phase | 작업 | files | hours est. | falsifier 위험 |
| --- | --- | --- | --- | --- |
| 6a | `.hexa` resolver 변환 | 323 | 12-16 | high |
| 6b | `.bash` deploy chain 변환 | 29 | 4-6 | high |
| 6c | uchg `.md` ceremony 변환 | 18 | 2-4 | mid |
| (면제) | `.log` rotation 정책 | 60+ | 0 (spec 등재만) | low |
| (면제) | binary / cache | 30+ | 0 | n/a |
| **합계** | | 370 변환 + 90 면제 | **18-26h** | |

권장 순서: 6c (consent gate 먼저 수렴) → 6b (sandbox 검증, 작은 surface) → 6a (largest, smoke chain).

각 Phase 후 raw#9 hexa-only 폴더 audit 1회, raw 91 honesty triad C2 write-barrier 확인 1회.

---

## §8 결정 기준 — strict raw 15 vs runtime stability

### §8.1 trade-off

- **strict 우선**: 잔여 464 leak 0건 도달 시 raw 15 iter5 fully-compliant — verifier chain 의 audit-trace 완전성 확보. 단 runtime break 발생 시 verifier 정지 → drill 누적 P1_FAIL.
- **stability 우선**: 면제 구간 확대 (`.log` + binary + launchd-mandated absolute) 시 leak 면제 후 잔여 ≈ 350. raw 15 iter5 partial-compliant. drill 영향 minimal.

### §8.2 권고

**hybrid**: §1.3 / §1.5 / §1.2(a) 면제 구간 명시 → 실제 변환 surface 358 (.hexa 323 + .bash 27 + .md 18 - launchd legitimate ≈ 10) → leak 0 도달은 spec exclusion 흡수로 정의.

이는 raw 15 iter6 spec amendment 가 선행 요건 — 본 cycle 종료 전 별도 spec doc 등재 필요 (`docs/raw_15_iter6_exclusion_list_<ts>.md`, 본 cycle X).

### §8.3 stop-loss

다음 중 1건 발생 시 Phase 6 전체 중단, raw 10 honest C3 재작성:

- canary 5/5 fail (resolver 호환성 입증 실패)
- launchd 1 cycle 후 ledger 침묵 (deploy chain break)
- 사용자 consent rate < 30% (uchg ceremony 합의 부재)

---

## §9 본 doc leak 자가 검증

작성 후 commit 직전 verify:

```
grep -nE '<HOME-PREFIX>|<HOME-PREFIX-LC>' docs/raw_15_residual_leak_spec_2026_05_01.md
```

기대 출력: 0 line. 본 doc 은 token (`<repo-root>`, `<user-home>`) 만 사용. 1 line 이라도 출력 시 commit retry.

---

## §10 다음 cycle 진입 조건

1. 본 spec doc commit 완료 (`git diff --cached --name-only` 정확히 1 file)
2. raw 15 iter6 exclusion list spec doc 작성 (별도 cycle)
3. Phase 6c (uchg consent gate) 진입 여부 사용자 결정
4. Phase 6a/6b/6c 진입 시 본 §2/§3/§4 protocol 그대로 따를 것 — improvise 금지

---

## §11 cycle re-launch addendum — 2026-05-02

### §11.1 재발사 배경

직전 cycle (2026-05-01) 에서 G3 quota 차단으로 본 spec 의 일부 protocol section (§3 / §4 detail expansion 의도) 가 미작성 종료. 본 cycle 은 G3 quota 회복 후 재발사 — 기존 §0~§10 본문 보존 (검토 결과 spec quality 충분), §11 addendum 으로 cycle hand-off 명세만 보강.

### §11.2 re-snapshot 미수행 사유

직전 cycle 작성 시점 (2026-05-01 ~00:11 KST F5+7 commit 직후) 부터 본 cycle 진입 (2026-05-02) 까지 약 24h 경과. 그동안 tree dirty (state ledger jsonl append 다수 존재 — `git status` 검증 결과) 했으나 leak 변환 작업 0건 — 따라서 464 surface 불변 가정 유지. 재 grep 미수행 사유는 read-only audit cost 절감 (다음 cycle Phase 6a 진입 시 fresh sweep 1회로 통합).

### §11.3 본 cycle 변경 surface

추가/변경된 file: 본 doc 1건 (`docs/raw_15_residual_leak_spec_2026_05_01.md`). 다른 file 0건 — single-file commit constraint 준수.

### §11.4 다음 cycle 진입 시 권고

1. Phase 6c (uchg consent gate) 진입 전 사용자에게 §4.1 step 3 "yes/no/skip" 표 제출 요청.
2. Phase 6a 시작 시 신선 grep snapshot 필수 (§6.1 honest C3 1번 항목 해소).
3. raw 15 iter6 spec amendment (`docs/raw_15_iter6_exclusion_list_<ts>.md`) 우선 작성 — Phase 6 변환 surface 정의 명확화.

### §11.5 raw 91 honesty triad C2 — write barrier

본 §11 addendum 은 §0~§10 의 verdict 구조를 변경하지 않음 (write barrier 준수). 추가 정보 only — 기존 카테고리 / 건수 / hours 추정 / 결정 기준 모두 불변.

---

end of spec — 2026-05-01 (cycle re-launch addendum 2026-05-02).
