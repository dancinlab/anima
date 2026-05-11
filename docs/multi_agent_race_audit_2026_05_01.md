# Multi-Agent Commit Race Audit — 2026-05-01

read-only forensics, raw#9 hexa-only, raw#10 honest C3, raw#91 honest, n=1 incident.

incident anchor: commit `ce747b5e7` (Author: dancinlife, AuthorDate `2026-05-01 23:50:18 +0900`,
title `feat(eeg-core-_metrics): plv_preserving — raw#10 P2 TLR INSUFFICIENT 후속 — no-ICA narrowband-Hilbert + AMICA pathway`).

---

<!-- [Hc_663 multi-agent-commit-race-hijack-pattern — moved to hypotheses_candidates/Hc_663_multi_agent_commit_race_hijack_pattern.md on 2026-05-11] -->

## §1. forensics — commit boundary breakdown

### §1.1 ce747b5e7 file list (from `git show --stat`)

| # | path (relative) | LoC | author intent | class |
|---|---|---:|---|---|
| 1 | `anima-eeg-core/tool/modules/_metrics/plv_preserving.hexa` | +439 | F3 P2 PLV-preserving (intended) | new file |
| 2 | `state/clm_eeg_plv_preserving_real.json` | +106 | F3 (intended) | new file |
| 3 | `docs/anima_clm_eeg_migration_plan_2026_04_29.md` | +162 / -17 | F1 (audit `867392918` reframe propagation) | hijack — modify |
| 4 | `anima-clm-eeg/docs/synthetic_fixture_fingerprint_audit_2026_05_01.md` | +104 | F6 (synthetic fixture fingerprint audit) | hijack — new file |

총 4 file, 794 insertions, 17 deletions. F3 의 commit 메시지 마지막에 명시:
`신규 file 2개 (module 439 LoC + state json 106 LoC). 다른 파일 무손상.` — 즉 F3 author 는
2개 file 만 commit 한 것으로 인지하고 있었으며, file 3·4 의 동반 staging 사실을 인지하지 못했음이
입증된다 (또는 인지했더라도 commit 메시지에 반영되지 않음).

### §1.2 commit boundary 격리 위반 — 의미적 충돌 평가

| pair | semantic 거리 |
|---|---|
| (file 1·2) F3 — plv_preserving 모듈 + real run state | tight bundle, 같은 변경 단위 |
| (file 1·2) ↔ (file 3) F1 plan reframe | **무관** — plan §3.3 reframe 은 wrap-not-port 발견 (audit `867392918` 의 후속), plv_preserving 모듈 도입과 별개 |
| (file 1·2) ↔ (file 4) F6 synthetic fixture fingerprint | **무관** — 274 LoC fixture 의 SHA-256 fingerprint mismatch 추적 doc, P2 PLV pathway 와 별개 |
| (file 3) ↔ (file 4) | **부분 연관** — 둘 다 audit/archive 라인 follow-up 이지만 별 author intent |

→ commit boundary 는 4 file 을 1 commit 으로 묶은 것이며, 이 중 **3 author intent 가 격리되지 않고 race-hijack 됨**.

### §1.3 인접 commit cross-check (intended boundary 가 어디 있어야 했는가)

직전 4 commits stat 요약:

| commit | time | files | intent |
|---|---|---|---|
| 43b3cee89 | 23:30:33 | `state/clm_eeg_p2_tlr_real.json` (1 file, +134) | P2 verify INSUFFICIENT |
| 867392918 | 23:31:28 | `anima-eeg-core/docs/phase1_deprecate_byte_identical_audit_2026_05_01.md` (1 file, +157) | F1 audit doc 신규 (plan reframe **권고만**, plan 자체는 미수정) |
| 7fc8c7e87 | 23:32:28 | `anima-clm-eeg/ARCHIVE_INDEX_2026_05_01.md` (1 file, +120) | A4 archive index 신규 |
| **ce747b5e7** | **23:50:18** | **4 files, +794 / -17** | F3 + F1(hijack) + F6(hijack) |
| fae7ceee8 | 23:51:19 | `anima-eeg-core/tool/modules/_integrations/lagrangian/v_sync_kuramoto_phase_stream.hexa` + spec doc (2 files, +586) | edu-cell helper |
| 0c19d30b6 | 23:57:24 | `anima-eeg-core/state/.../2026-05-01_chunked_real.jsonl` + state json (2 files, +169) | lz76_chunked verify |

직전 3 commit (43b3cee89, 867392918, 7fc8c7e87) 모두 **single-file, single-intent** 였다.
ce747b5e7 는 인접 commit 패턴과 비교해 **유일한 4-file mixed-intent commit** 이다.

867392918 가 plan reframe **권고** doc (`anima-eeg-core/docs/phase1_deprecate_byte_identical_audit_2026_05_01.md`)
만 commit 한 시각이 23:31:28 인데, plan 본문 (`docs/anima_clm_eeg_migration_plan_2026_04_29.md`) 의
실제 reframe 변경은 ce747b5e7 (23:50:18) 까지 **18~19분 동안 working tree 에 unstaged 채로 잔존** 했다는
타임라인 추정이 성립한다. 이 시간 창이 race window.

### §1.4 git log --follow navigability 손상

| file | commit history (touch points) |
|---|---|
| `docs/anima_clm_eeg_migration_plan_2026_04_29.md` | `fb5b423c2` (2026-04-29 신규) → `ce747b5e7` (2026-05-01 reframe) |
| `anima-clm-eeg/docs/synthetic_fixture_fingerprint_audit_2026_05_01.md` | `ce747b5e7` (신규, 2026-05-01) |

향후 누구든 `git log --follow docs/anima_clm_eeg_migration_plan_2026_04_29.md` 또는 `git log -p
anima-clm-eeg/docs/synthetic_fixture_fingerprint_audit_2026_05_01.md` 를 호출하면
**"P2 PLV-preserving 모듈 도입" commit 메시지** 가 보이는데 본문은 plan reframe / fixture fingerprint
audit. semantic mismatch 가 history 에 영구히 박혔다.

---

## §2. hook 분석 — auto-add 동작 입증/반증

### §2.1 hook directory 식별

```
git config --get core.hooksPath  →  (empty / unset)
git config --list --show-origin | grep core  →  hooksPath 항목 부재
```

`core.hooksPath` 는 **현재 unset** 이다. 따라서 git 은 default `.git/hooks/` 를 본다:

```
ls -la .git/hooks/
→  applypatch-msg.sample, commit-msg.sample, fsmonitor-watchman.sample,
   post-update.sample, pre-applypatch.sample, pre-commit.sample, ...
   (전부 .sample 접미사 — 기본 unactivated 상태)
```

`.git/hooks/` 에는 **active hook 0건**. 즉 이 repo 에서 git commit 시점에 **어떤 hook 도 호출되지 않는다**.

### §2.2 hive safety hook 후보 분석 (호출되지 않더라도 source 만 분석)

repo 에는 hook source 가 보존되어 있다:

```
scripts/safety/git-hooks/pre-commit       (3 lines, exec staged-scan.sh)
scripts/safety/git-hooks/commit-msg       (3 lines, exec commit-msg-scan.sh)
scripts/safety/staged-scan.sh             (112 lines)
scripts/safety/commit-msg-scan.sh         (57 lines)
```

`grep -nE "git add|git stage" scripts/safety/{staged-scan.sh,commit-msg-scan.sh,git-hooks/pre-commit,git-hooks/commit-msg}` →
**0 hits**. 두 scanner 와 두 entrypoint 모두 read-only:
- `staged-scan.sh`: `git diff --cached --name-only --diff-filter=AM` 호출 + per-file `git show ":$f"` 로
  staged blob 내용 조회 + SECRET / JUNK / PERSONAL_PATH regex 검사. write 동작 없음.
  (HIVE_SAFETY_ALLOW bypass 시 `state/safety_bypass_audit/audit.jsonl` append-only 만 수행.)
- `commit-msg-scan.sh`: `$1` 로 받은 commit-msg file 을 read + grep + exit 0|1.

**확정**: hook source 는 read-only scanner 이며, 만약 active 였더라도 working tree → index 로
unrelated change 를 auto-add 할 수단을 갖고 있지 않다. 실제로는 unset 이라 호출조차 되지 않았다.

### §2.3 직전 hook commit 의 의도 vs 실제 상태

```
commit 248c2ecfc (2026-04-30 20:36:36)
  feat(safety): hive raw 15 strengthen-iter4-7 propagation — pre-commit + commit-msg hooks
  ... "+ sets core.hooksPath."
```

commit 메시지에 `core.hooksPath` 설정을 한다고 적혀 있으나 `.git/config` 는 git tracked 가 아니므로
**해당 설정은 commit 으로 전파되지 않았으며 현재도 unset** 이다. 즉 hive safety gate 가
설치 의도였으나 사실상 inactive 상태.

→ root cause 가설 후보 #1 ("hook auto-add 동작") 은 **반증**. hook 자체는 race 의 원인이 아니다.

---

## §3. race window 분석

### §3.1 hook 미작동 환경의 staging sequence (이번 incident 가 발생한 실제 환경)

ce747b5e7 의 incident 에서 hook 은 inactive 였으므로 staging 흐름은 다음과 같다:

```
F3 agent (intent: plv_preserving):
  step 1   chflags nouchg <target files>          # uchg unlock
  step 2   write _metrics/plv_preserving.hexa     # F3 새 파일
  step 3   write state/clm_eeg_plv_preserving_real.json
  step 4   chflags uchg <target files>            # relock
  step 5   git add <intended 2 paths>             # 또는 git add -A / git commit -a (??)
  step 6   git commit -m "feat(...): plv_preserving ..."

F1 agent (intent: plan reframe — concurrent):
  step a   read docs/anima_clm_eeg_migration_plan_2026_04_29.md
  step b   plan body reframe (NOTE 2026-05-01 audit `867392918` propagation)
  step c   write docs/anima_clm_eeg_migration_plan_2026_04_29.md  ← working tree dirty
  step d   (commit 계획은 다음 cycle 또는 본인 cycle 이지만 main session 통합 의도?)

F6 agent (intent: synthetic fixture fingerprint audit — concurrent):
  step α   write anima-clm-eeg/docs/synthetic_fixture_fingerprint_audit_2026_05_01.md
  step β   (own commit 의도 또는 main session 통합)
```

### §3.2 race 발생 지점

핵심: F3 `step 5 git add` 가 어떤 형태였는가에 따라 두 시나리오:

**시나리오 A (가능성 ↑)**: F3 가 `git add -A`, `git add .`, 또는 `git commit -a` 사용.
- 의도된 2 file 외에 working tree dirty 상태 였던 file 3 (plan body), file 4 (synth audit)
  까지 sweep 으로 staged.
- F3 author commit 메시지 마지막 줄 "다른 파일 무손상" 은 **선언적 가정** 이며 staging 결과 검증 (`git diff --cached`) 미실시.

**시나리오 B (가능성 ↓)**: F3 가 정확한 path 만 `git add` 했으나 다른 자동화 (예: pre-commit-msg hook, prepare-commit-msg hook, IDE auto-stage) 가 inject.
- 그러나 §2 에서 active hook 이 0건 임을 확인 → 이 경로는 **반증**.

→ root cause 가설 후보 #2 ("F3 sweep staging") 는 **간접 입증 강함**.

### §3.3 file lock vs git index lock — multi-agent serialization 부재

uchg 는 **filesystem 단위 mandatory lock** 이며 다음을 보장:
- `chflags uchg` 걸린 file 은 다른 process 가 write 시 EPERM.
- 그러나 uchg 는 `git add` 의 staging 동작을 막지 않는다 — git 은 working tree blob 을 read 해
  `.git/objects` 에 hash-encode 후 `.git/index` update; uchg 는 read 에 영향 없음.

git 자체의 동시성 보호:
- `.git/index.lock` — `git add` / `git commit` 시 `index.lock` 을 mkdir-style 으로 잡음.
  그러나 이는 single git process 단위 atomicity 만 보장 (race 시 second add 가 fail 하고 첫 add 가 끝나면
  다시 시도해서 결과적으로 둘 다 성공). 즉 **여러 agent 의 staging 의도를 격리하지 않는다**.
- 다른 agent 가 **다른 file** 을 add 하더라도 같은 `.git/index` 에 모이므로 **하나의 commit boundary 에 통합됨**.

이번 incident 의 핵심: file 3, 4 가 working tree 에 dirty 상태로 잔존했고, F3 가 commit 시점에
`git diff --cached` 로 staged content 의 정확성을 검증하지 않은 것.

→ root cause 가설 후보 #3 ("multi-agent serialization 부재 — file lock 만으로는 git index 격리 불가") **입증**.

### §3.4 sequence diagram (실제 18-19분 race window)

```
time(KST)   F3 (plv_preserving)              F1 (plan reframe)         F6 (synth audit)
23:30:33   ─                                 ─                          ─
23:31:28   ─                                 audit doc commit 867392918 ─
                                             (audit doc 신규 only,
                                              plan body 미수정 잔존)
23:32:28   ─                                 ─                          ─
                                             ── 23:32~23:50 race ──
                                             plan body reframe 작업
                                             working tree dirty
                                                                        synth audit doc 신규
                                                                        working tree dirty
23:50:18   git add (sweep) +                                            
           git commit ce747b5e7                                         
           ↓                                                            
           F1·F6 의 dirty file 까지                                      
           commit boundary 에 흡수                                       
23:51:19   ─                                 ─                          ─
```

---

## §4. 영향 평가 — content / history / bisect

### §4.1 content level 정합성

3 file group 의 **의미적 충돌 검사**:

| pair | conflict? | rationale |
|---|---|---|
| F3 plv_preserving ↔ F1 plan reframe | **X (compatible)** | F3 모듈은 plan §3.3 와 무관한 신규 metric 도입. plan reframe 은 4 기존 metric pair (lz76/pe/hjorth/gamma_theta) 의 wrap-not-port 분류 변경. plv_preserving 은 §3.3 list 에 등장 안 함. |
| F3 plv_preserving ↔ F6 synth audit | **X (compatible)** | F6 는 274 LoC fixture 의 fingerprint mismatch 추적. F3 의 selftest 는 synthetic dual-oscillator 자체 생성 (fixture 무관). |
| F1 plan reframe ↔ F6 synth audit | **부분 양립** — F6 가 synthetic_fixture 의 §3.3 분류를 §11 deferred 로 미는 reframe 이므로 F1 plan reframe table 에 잘 fit (F1 가 §11 cross-ref 추가). |

→ **content 보존 OK**. 의미적 backward-compat 이며 기능 회귀 없음.
역사적으로 commit 단위가 깨졌을 뿐, working tree 최종 상태에는 모순이 없다.

### §4.2 history navigability

`git log --follow docs/anima_clm_eeg_migration_plan_2026_04_29.md` 의 마지막 entry:
```
ce747b5e7  feat(eeg-core-_metrics): plv_preserving — raw#10 P2 TLR INSUFFICIENT 후속 — ...
```
plan body 의 reframe 이유 (audit `867392918` WRAP-not-PORT 발견) 를 commit message 에서
**찾을 수 없다**. 본문 NOTE 블록에 inline 으로 audit hash 를 적어놓은 것이 유일한 단서.

→ **navigability 손상**. mitigation 은 commit message 가 아닌 file body 에 저장된 in-line `NOTE`
주석으로 부분 회복 가능 (이미 file body 에 `(audit '867392918' reframe)` 명시).

### §4.3 bisect-ability

가설: 미래에 P2 PLV-preserving pathway 회귀 추적 시 `git bisect` 실행 시나리오.
- bisect 가 ce747b5e7 에 정착하면 commit message 는 P2 PLV 라고 알려주지만, file diff 에 plan reframe
  + synth audit 도 함께 등장 → bug surface 격리 어려움.
- 실제 P2 PLV bug 가 plan reframe 또는 synth audit 변경과 무관함에도 **검토 부담 +205 LoC** 발생
  (162 + 104 - 17 + ~4ζ collapse).
- false-positive bisect anchor 는 아니다 (정확히 P2 PLV 모듈 도입 commit 임). 다만 **context 노이즈** 발생.

→ bisect risk: **LOW (noise only)**, false-positive anchor 아님.

---

## §5. 권고 (mitigation)

### §5.1 단기 — 이번 세션 후속 cycle 후보

1. **F3 staging 검증 패턴 도입** (가장 즉각, raw#10 honest):
   - bg agent 운영 spec 에 `git diff --cached --name-only` 결과를 commit 직전 출력 + 메시지 footer 의
     "신규 file N개" claim 과 cross-check 의무 추가.
   - 위반 시 commit 직전 unstaging 또는 abort.

2. **`git add -A` / `git commit -a` 전면 금지** (bg agent 한정):
   - bg agent 는 항상 explicit path 로 `git add <path1> <path2> ...` 만 사용.
   - main session interactive 환경은 예외.

3. **uchg lock-cycle atomic shell function** (raw#15 candidate):
   ```sh
   safe_uchg_edit_relock() {
     local target="$1" ; local edit_cmd="$2"
     chflags nouchg "$target"
     trap "chflags uchg \"$target\"" EXIT
     eval "$edit_cmd"
     chflags uchg "$target"
     trap - EXIT
   }
   ```
   다만 본 incident 에서 uchg 는 직접 race 원인이 아니다 (file 3·4 가 uchg 보호 대상 인지 불명).
   priority LOW.

4. **`core.hooksPath` 재설치 + 효과 검증**:
   - commit `248c2ecfc` 가 의도한 `git config core.hooksPath scripts/safety/git-hooks` 가
     **실제로 적용되지 않은 상태** 임. 단 본 incident 에서 hook 은 race 원인이 아니므로 보안
     post-commit forensics 보강 차원의 별 cycle.

### §5.2 중기 — 정책 spec

5. **bg agent commit 격리 정책**:
   - 옵션 A: "bg agent 는 commit 안 함, working tree 변경 + path manifest 만 emit, main session 가
     해당 manifest 만 staged" — 이미 일부 cycle 에서 사용 패턴.
   - 옵션 B: bg agent 마다 별도 git **worktree** (`git worktree add`) 격리 — Agent 의 `isolation: "worktree"` 옵션 활용.
     본 incident 의 18-19분 race window 자체가 사라진다.

6. **multi-agent commit serialization mutex** (옵션 A·B 중간 단계):
   - 파일 기반 mutex (`.git/multi-agent-commit.lock`) — agent staging+commit 구간 직렬화.
   - drawback: throughput 저하, fail-stop 시 stale lock.

### §5.3 장기 — raw 47 hive

7. **hive raw 정책 신설 후보**: `multi-agent-commit-serialization-mandate`
   - 모든 hexa repo 에 대해 bg agent 의 commit 권한 / 직렬화 정책 spec.
   - propagation route: hive raw → anima / hexa-lang / 기타 repo cross-ramp.

8. **own#15 후보**: `uchg-lock-cycle-atomicity` (raw#71 falsifier preregister 동반)
   - F_UCHG_01: relock 누락 (uchg 못 걸린 채 EXIT).
   - F_UCHG_02: 다른 agent 가 nouchg 구간 동안 write inject.
   - F_UCHG_03: shell function 자신이 SIGINT 등으로 죽었을 때 trap 미작동.

---

## §6. raw#91 honest C3 — 미입증 영역

본 audit 의 한계 (raw#10 honest, raw#91 한계 명시):

1. **n=1 incident**: ce747b5e7 단일 사례 forensics. F3·F1·F6 동시 작업 패턴이 일반적인지 추세인지
   판단할 표본 없음. 본 incident 가 "rare race" 인지 "systemic 미직렬화" 인지는 추가 incident
   누적 또는 고의 reproduce 실험 후 결정.

2. **hook 동작 직접 reproduce 미실시**: §2 분석은 hook source code 정적 검토 + `git config`
   현재 상태 점검. 실제로 `git commit` 직전 hook trigger 여부 (`git commit --dry-run` 또는 strace)
   직접 측정 미수행. read-only 제약 + 이미 반증 강한 정황 (core.hooksPath unset + grep `git add` 0
   hits) 으로 충분하다 판단했지만 100% 결론적이지 않다.

3. **F3 의 정확한 staging 명령 미확인**: `git add -A` / `git add .` / `git commit -a` 가 사용됐다는
   직접 증거 없음 — incident 정황상 (commit 메시지의 "신규 file 2개" 선언과 실제 4 file commit 의
   불일치) 추정. F3 agent 의 실제 transcript 또는 명령 history 미열람 (read-only 제약).

4. **F1·F6 작업 시작 시각 미특정**: 23:31:28 (audit `867392918`) ~ 23:50:18 (ce747b5e7) 사이의
   **정확한 file 3·4 dirty 시각** 확인 불가 (`.git/`, `git status` 의 untracked timestamp 만 가능
   하지만 상대 신뢰도 낮음). 18-19 분 window 는 **상한** 일 뿐, 실제 race 발생 시점은 미상.

5. **hive raw 47 hive 동기화 spec 미열람**: `raw 15 strengthening 2026-04-30 personal-path-leak-ban-iter4-7`
   는 식별했으나 hive 측 multi-agent serialization 관련 raw 항목 (있다면) 미점검.

6. **다른 agent (F5+7) bg 작업 영향 미평가**: 사용자 노트에 `F5+7 작업 중` 라 했으나 본 audit
   시점 (23:50 대 commit 후 ~01:00) 에 F5+7 의 working tree footprint 구체적 file list 미확인 —
   다음 commit 에서도 같은 race 가 재현될 가능성 있음.

---

## §7. raw#9 / raw#10 / raw#71 / raw#91 / raw#15 footer

- raw#9 hexa-only: 본 audit 자체는 markdown doc 1건만 추가 (소스 코드 변경 0건).
- raw#10 honest C3: §6 에 미입증 영역 6 항목 명시. n=1 incident, hook reproduce 미실시.
- raw#71 falsifier candidate (own#15 ushcg-lock-cycle-atomicity 시): F_UCHG_01..03 §5.3 에 spec.
- raw#91 hexa-only honest: hook source 와 commit metadata 만 사용, F3·F1·F6 agent transcript 미열람.
- raw#15 personal-path-leak-ban: 본 doc 에 `/Users/.../` 절대경로 0건 (relative 표기 only).
