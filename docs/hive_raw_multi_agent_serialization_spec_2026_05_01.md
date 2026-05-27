# Hive Raw — Multi-Agent Commit Serialization Spec — 2026-05-01

raw#9 hexa-only, raw#10 honest C3, raw#91 honest triad, single-file consolidated spec.
spec only — 실제 hook patch 적용 / raw 등록 / own#15 등록은 본 doc 범위 외 (사용자 결정).

---

## §0. Executive summary

본 cycle 의 race audit (`docs/multi_agent_race_audit_2026_05_01.md`, commit `3c3cbc0b4`) 는
ce747b5e7 commit 의 boundary breakdown — F3 sweep staging 으로 인해 F1 plan reframe + F6 synth
audit 까지 1 commit 에 흡수된 사례 — 를 입증했다. n=1 incident 이지만 multi-agent bg 운영의
직렬화 부재라는 systemic gap 을 노출했다. 본 spec 은 race audit 의 장기 권고 (§5.3) 를 single-file
spec 형태로 합본한다:

1. **raw 신설 후보 2종** (multi-agent-commit-serialization-mandate, uchg-lock-cycle-atomicity)
2. **own#15 후보 1종** (uchg-lock-cycle-atomicity own-rule level)
3. **F_UCHG falsifier 3종 preregister** (F_UCHG_01..03)
4. **Phase A/B/C/D implementation plan** (즉시 prompt update 부터 12-week observation window 까지)

본 spec 은 race-free guarantee 의 cost (throughput / migration / fs pressure) 를 §6 trade-off
matrix 로 정직하게 표시하고, raw#10 C3 caveat 10 항목 (§7) + raw#91 honesty triad (§8) 로
한계를 명시한다.

---

## §1. race audit 결과 요약 (commit `3c3cbc0b4` reference)

### §1.1 incident anchor

| 항목 | 값 |
|---|---|
| race incident commit | ce747b5e7 (2026-05-01 23:50:18 +0900) |
| race audit commit | 3c3cbc0b4 (audit doc 신규 1 file) |
| audit doc | `docs/multi_agent_race_audit_2026_05_01.md` (345 LoC) |
| race window | 2026-05-01 23:31:28 ~ 23:50:18 (18-19 분) |

### §1.2 root cause (audit §3.2 결론)

- 가설 #1 ("hook auto-add"): **반증** (`.git/hooks/` active hook 0 건, `core.hooksPath` unset, hook source 는 read-only scanner).
- 가설 #2 ("F3 sweep staging"): **간접 입증 강함** (commit 메시지의 "신규 file 2 개" 선언 vs 실제 4 file commit 불일치).
- 가설 #3 ("multi-agent serialization 부재"): **입증** (uchg 는 fs lock 만 보장, git index 격리 불가).

### §1.3 audit 권고 분류

| 권고 | 우선 | 권고 단계 |
|---|---|---|
| §5.1.1 staged path verify (`git diff --cached --name-only`) | 단기 | 본 세션 적용 완료 (이번 세션 이후 bg agent prompt) |
| §5.1.2 `git add -A` / `git commit -a` 금지 | 단기 | 본 세션 적용 완료 |
| §5.2.6 worktree 격리 옵션 | 중기 | 본 spec §5 Phase C |
| §5.3.7 hive raw 신설 | 장기 | 본 spec §2 후보 A/B |
| §5.3.8 own#15 + F_UCHG | 장기 | 본 spec §3, §4 |

---

## §2. hive raw 신설 후보

### §2.1 raw 신설 후보 A — `multi-agent-commit-serialization-mandate`

**요지**: 모든 hexa repo 의 모든 bg agent 가 commit 시 staging 의도와 결과의 일치를 강제 검증한다.

**rule body 초안**:

1. bg agent 가 `git commit` 호출 직전 `git diff --cached --name-only` 출력을 capture.
2. capture 결과는 agent commit message 의 "신규 file N 개 / 수정 file M 개" 선언과 정확히 일치해야 한다.
3. 불일치 시 commit reject (agent 자체 abort + main session 보고).
4. **sweep staging 절대 금지**: `git add -A`, `git add .`, `git add -u`, `git commit -a`, `git commit -am` 사용 X.
5. bg agent 는 항상 explicit path 로만 `git add <path1> <path2> ...` 사용.
6. (옵션) pre-commit hook 강제: staged file count 가 commit message 선언과 mismatch 시 reject.

**적용 범위**:
- hexa repo 전체 (anima, hexa-lang, 기타 cross-ramp 후보).
- main session interactive 환경은 예외 (사용자 직접 의도 commit).
- bg agent (Agent tool subprocess, scheduled cron, autonomous sweep) 만 강제 대상.

**propagation route**: hive raw → anima/own → hexa-lang/own → 기타 repo own.

### §2.2 raw 신설 후보 B — `uchg-lock-cycle-atomicity`

**요지**: chflags nouchg → Edit → chflags uchg sequence 도중 race window 0 보장. multi-agent 환경에서
같은 uchg-protected file 을 동시에 편집하지 않는다.

**rule body 초안**:

1. uchg-protected file 의 lock-cycle 는 **single agent 단위 atomic** 이어야 한다.
2. lock-cycle 진입 전 file 단위 lock token 획득 (`.git/multi-agent-uchg.<sha256(path)>.lock`).
3. lock token 미획득 시 다른 agent 의 lock-cycle 종료까지 wait 또는 cycle abort.
4. lock-cycle 종료 시 token release. SIGINT / SIGKILL trap 으로 stale token 자동 cleanup.
5. lock-cycle shell function 의 EXIT trap 으로 chflags uchg relock 보장:
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
6. multi-agent 동시 편집 시 file 단위 serialization queue 로 직렬화.

**적용 범위**:
- uchg-protected file 만 (전체 repo 의 일부, 주요 own/raw doc + critical state json).
- bg agent 만 강제 대상.
- 본 incident 에서 uchg 는 직접 race 원인이 아니었으나, race window 패턴 자체가 lock-cycle 도중
  외부 agent injection 가능성을 시사 → 예방적 spec.

---

## §3. own 후보

### §3.1 own#15 후보 — `uchg-lock-cycle-atomicity` (own-rule level)

**요지**: 사용자 본인 작업 directives. chflags lock-cycle 사용 시 외부 agent 차단 의무.

**rule body 초안**:

1. 사용자가 chflags nouchg → Edit → chflags uchg 를 직접 실행하는 동안 main session 외 agent
   (Agent tool, bg cron) 의 working tree write 권한을 차단한다.
2. 차단 수단:
   - bg agent prompt 에 "uchg lock-cycle 진행 중 file 편집 X" 명시.
   - main session 에서 lock-cycle 시작 시 `.git/own15-lock-cycle-active` flag 설정 + bg agent
     pre-write check 의무.
3. lock-cycle 종료 시 flag clear + 직전에 wait 중이던 agent 작업 재개.
4. own#15 는 **개인 작업 layer** 의 rule 이며 hive raw 신설 후보 B 와 별개로 독립 적용 가능.

**raw 신설 후보 B 와 차이**:
- raw 후보 B: hexa repo 전체, multi-agent 환경 자체.
- own#15: 사용자 단일 인격의 main session vs bg agent 협업 layer.

---

## §4. F_UCHG falsifier preregister

own#15 + raw 신설 후보 B 가 등록될 경우 본 spec 도입 시점 (가칭 T0) 부터 12-week observation
window 동안 다음 falsifier 충족 시 spec retire 또는 재평가.

### §4.1 F_UCHG_01 — race hijack recurrence

**조건**: 본 raw / own#15 적용 후 race hijack incident (1 commit 이 2+ 개 author intent 흡수)
1 건이라도 발생하면 spec retire.

**측정**:
- 매 commit 후 `git diff --cached --name-only` log 와 commit message 의 "신규/수정 file N 개" 선언
  cross-check.
- bg agent 의 commit boundary 가 단일 author intent 만 포함하는지 weekly audit.

**해석**: F_UCHG_01 hit 시 spec 자체가 race 차단에 실패 → root-cause 재평가 (예: hook bypass,
lock token race, 새로운 pathway).

### §4.2 F_UCHG_02 — pre-commit hook false-positive rate

**조건**: pre-commit hook 의 verify step 이 false-positive 비율 5% 초과 → spec 단순화.

**측정**:
- pre-commit hook 의 reject 건수 / 전체 commit attempt 건수.
- false-positive 정의: agent 의 staging 의도와 결과가 일치함에도 hook 이 reject 한 case.
- false-positive 별 cause 분류 (regex 오작동, edge-case path, hook 자체 bug 등).

**해석**: F_UCHG_02 hit 시 hook 강제도가 너무 strict → confirm-only mode, 또는 verify step 만
유지 후 reject step 제거.

### §4.3 F_UCHG_03 — serialization queue throughput penalty

**조건**: serialization queue (raw 후보 B 의 lock token 또는 own#15 의 flag) 가 bg agent 처리량
50% 이상 감소 → trade-off 재평가.

**측정**:
- spec 적용 전 12 주 동안 bg agent 의 평균 commit/hour throughput baseline.
- spec 적용 후 12 주 동안 같은 metric.
- 50% 감소: throughput_after < throughput_before * 0.5.

**해석**: F_UCHG_03 hit 시 race-free 보장과 throughput 의 trade-off 재평가 → worktree 격리 (옵션 C)
로 우회, 또는 lock token 의 granularity 완화 (file 단위 → directory 단위).

---

## §5. Implementation plan

### §5.1 Phase A (즉시, 1-2 시간)

**의무**: bg agent prompt template update.

- bg agent prompt 에 다음 의무 추가:
  - `git diff --cached --name-only` capture + commit message 와 cross-check.
  - sweep staging (`git add -A`, `git add .`, `git add -u`, `git commit -a`, `git commit -am`) 절대 금지.
  - bypass 수단 (`HIVE_SAFETY_ALLOW`, `--no-verify`, `git commit -n`) 사용 X.
- main session 에서 Agent tool 호출 시 system prompt 에 자동 inject.
- 기존 cycle 후속 prompt 에 **본 세션 적용 사례** 인용 (race audit doc reference).

estimate: 1-2 hours (prompt template file 수정 + Agent tool launch wrapper 점검).

### §5.2 Phase B (단기, 4-8 시간)

**의무**: pre-commit hook patch.

- `scripts/safety/git-hooks/pre-commit` 에 verify step 추가:
  - staged file count > 1 일 때 confirmation prompt (interactive) 또는 commit message 의
    "신규 file N 개 / 수정 file M 개" 선언과 cross-check.
  - bg agent 환경 (env `BG_AGENT=1` 또는 non-tty) 에서는 mismatch 시 무조건 reject.
  - main session interactive 환경에서는 mismatch 시 confirmation prompt + override 가능.
- `core.hooksPath` 재설치 (commit `248c2ecfc` 의도 미적용 상태 fix).
- hook 테스트: 의도적 sweep staging case + 정확 staging case 양쪽 dry-run.

estimate: 4-8 hours (hook 작성 2h + 테스트 2h + cross-repo 적용 1h + edge-case 보강 1-3h).

### §5.3 Phase C (중기, 8-16 시간)

**의무**: worktree 격리 시범 정책.

- bg agent 가 Agent tool launch 시 `isolation: "worktree"` default 적용.
- worktree path naming convention: `.worktrees/agent-<uuid>-<timestamp>/`.
- agent 작업 종료 후 worktree → main 통합 절차 (cherry-pick 또는 merge).
- worktree 별 fs overhead + git index pressure 측정.
- 시범 대상: 1 주간 모든 bg agent 의 50% 만 worktree 격리, 나머지 50% 는 기존 방식 (control).

estimate: 8-16 hours (Agent tool wrapper 6h + 통합 procedure 4h + 측정 2h + edge-case 4h).

### §5.4 Phase D (장기, 1-2 주)

**의무**: hive raw 신설 + own#15 등록 + F_UCHG 12-week observation window.

- hive raw 신설 (후보 A multi-agent-commit-serialization-mandate 우선, 후보 B 는 후속).
- own#15 uchg-lock-cycle-atomicity 등록.
- F_UCHG_01/02/03 12-week observation window 시작 (T0 = raw / own#15 등록 시점).
- weekly audit log: `state/multi_agent_serialization_audit/<YYYY-WW>.jsonl`.
- 12 주 후 falsifier hit 여부 평가 + spec retire / 단순화 / 유지 결정.

estimate: registration 4h + observation 12 weeks (passive) + 12 주 후 평가 8h.

---

## §6. Trade-off matrix

각 안건의 race-free 보장 / throughput / migration cost 를 정성적으로 비교한다 (정량 측정은 Phase D
observation 후 가능).

| 안건 | race-free | throughput | migration cost | 비고 |
|---|---|---|---|---|
| Phase A (prompt update) | M | H | L | 즉시 적용. 강제력은 agent self-discipline 의존. |
| Phase B (pre-commit hook) | H | M-H | M | hook 자체 false-positive 위험 (F_UCHG_02). |
| Phase C (worktree 격리) | VH | M | H | fs overhead + git index pressure + 통합 procedure 복잡. |
| Phase D (raw / own#15) | H+ | M-H | L | spec layer; 실제 강제력은 Phase A-C 의존. |

범례: VH=very high, H=high, M=medium, L=low.

**Pareto 분석**:
- Phase A 만 적용: 빠르지만 강제력 약함. n=1 race 재현 가능성 잔존.
- Phase A+B 조합: 합리적 baseline. F_UCHG_02 false-positive 5% 이내 유지 시 권장.
- Phase A+B+C 조합: race-free 가까운 이상점. throughput 50% 이상 감소 시 (F_UCHG_03 hit) C retreat.
- Phase D 단독: spec only — 강제력 없음. A-C 와 결합 필수.

---

## §7. raw#10 honest C3 — 10 caveats

본 spec 의 한계 (raw#10 honest C3, 10 항목):

1. **n=1 race incident 표본 부족**: race audit 자체가 ce747b5e7 단일 사례. 본 spec 의 cost
   (Phase A-D 의 시간 + throughput penalty) 를 정당화할 incident frequency 미측정. Phase D
   observation window 후 재평가 필수.

2. **hook patch 자체가 새 race 만들 수 있음 (chicken-and-egg)**: Phase B hook 이 verify step 에서
   `git diff --cached` 를 호출하는 동안 다른 agent 가 `.git/index` 를 update 하면 hook 의 verify
   결과가 stale. hook 자체의 atomicity 보장이 별 spec 으로 필요.

3. **serialization 은 bg parallel 의도와 충돌**: bg agent 의 존재 이유 자체가 main session 과 병렬
   작업. serialization queue 는 throughput 을 직접 깎는다. F_UCHG_03 50% 감소 임계치는 임의.

4. **worktree isolation overhead (file system + git index pressure)**: 매 bg agent 마다 worktree
   생성 + 통합 → fs space 증가 + git pack-objects 시 index pressure 증가. 측정 데이터 없음.

5. **lock token race 자체**: raw 후보 B 의 file 단위 lock token (`.git/multi-agent-uchg.<sha>.lock`)
   생성 시 mkdir-style atomicity 의존. fs 가 NFS 등 mount 시 atomicity 깨질 수 있음.

6. **own#15 flag 의 race**: `.git/own15-lock-cycle-active` flag 자체가 set/clear race 를 가짐.
   atomic file rename trick 필요 (`mv` 의 atomicity 보장 fs 만).

7. **hook 강제도 cycle 의존**: `core.hooksPath` 가 commit `248c2ecfc` 의도와 달리 unset 인
   현재 상태. Phase B 가 hook 재설치를 포함하지만, 미래 user clone repo 시 자동 설치 절차 미정.

8. **Agent tool 의 isolation 옵션 정확한 동작 미검증**: Phase C 의 `isolation: "worktree"` default
   적용은 Claude Code Agent tool 의 내부 동작 가정. 실제 동작 stress-test 미수행.

9. **F_UCHG_01 1 건 발생 시 즉시 retire 는 over-strict**: 1 건의 race 도 spec 실패로 간주하면
   Phase A-D 의 sunk cost 회수 어려움. observation window 내 N 건 (예: 3 건) 발생 시 retire 가
   합리적일 수 있으나 본 spec 은 "n=1 incident 자체가 본 spec 의 trigger" 라는 비대칭성 때문에
   1 건 즉시 retire 를 채택.

10. **multi-agent commit 의 정의 모호**: "agent" 가 Agent tool subprocess 인지, scheduled cron 인지,
    main session 안의 중첩 task 인지 경계 불명. 본 spec 의 "bg agent" 정의 (Agent tool subprocess
    + scheduled cron + autonomous sweep) 는 임의 분류. 사용자가 main session 안에서 동시에 두
    file 을 작업하는 경우는 rule 적용 외.

---

## §8. raw#91 honesty triad

### §8.1 claim

본 spec 은 multi-agent commit race (ce747b5e7 type) 를 prevent 하기 위한 4-phase implementation
plan + raw / own#15 / F_UCHG 등록 candidate set 을 제시한다.

### §8.2 evidence

- race audit doc (`docs/multi_agent_race_audit_2026_05_01.md`, 345 LoC, commit `3c3cbc0b4`) 의
  forensics 결과 — incident root cause 가설 #1 (hook auto-add) 반증, #2 (sweep staging) 강한 간접
  입증, #3 (serialization 부재) 입증.
- 본 spec 의 §5 Phase A-D 는 audit §5.1 단기 + §5.2 중기 + §5.3 장기 권고에 직접 매핑.
- §6 trade-off matrix 의 race-free / throughput / migration cost 평가는 정성 (정량 측정은 Phase D
  observation 후).

### §8.3 limit

- §7 의 10 caveat 에 명시. 특히 n=1 incident 의 일반화 불가 (caveat #1) 와 hook 자체의 race
  (caveat #2), serialization throughput trade-off 임의 임계치 (caveat #3) 가 본 spec 의
  핵심 한계.
- 본 spec 은 spec only — 실제 강제력 (hook patch, raw 등록, own#15 등록, agent prompt update) 은
  사용자 직접 결정. 본 doc 의 commit 자체는 강제력 0.

---

## §9. Cross-references

- race audit doc: `docs/multi_agent_race_audit_2026_05_01.md` (commit `3c3cbc0b4`).
- incident commit: `ce747b5e7` (2026-05-01 23:50:18, F3 + F1 + F6 흡수).
- 직전 single-file commits (intended boundary 패턴): `43b3cee89`, `867392918`, `7fc8c7e87`.
- hook source 보존 commit: `248c2ecfc` (`feat(safety): hive raw 15 strengthen-iter4-7 propagation —
  pre-commit + commit-msg hooks`) — 의도된 `core.hooksPath` 설치는 미적용 상태.
- 본 세션 H1-H5 prompt 적용 (Phase A 일부 선반영): bg agent prompt 에 `git diff --cached --name-only`
  verify + sweep staging 금지 의무 명시 (race audit 권고 §5.1.1, §5.1.2).
- raw 신설 후보 A 의 propagation route: hive raw → anima/own → hexa-lang/own.
- own#15 후보 의 falsifier preregister: F_UCHG_01..03 (§4) — 12-week observation window.
- raw#15 personal-path-leak-ban: 본 doc 에 absolute path 0 건 (relative 표기 only).

---

## footer — raw#9 / raw#10 / raw#71 / raw#91 / raw#15

- raw#9 hexa-only: 본 spec 자체는 markdown doc 1 건만 추가 (소스 코드 변경 0 건, hook patch 미적용).
- raw#10 honest C3: §7 에 10 caveat 명시.
- raw#71 falsifier candidate: §4 F_UCHG_01..03 preregister + 12-week observation window.
- raw#91 honest triad: §8 claim / evidence / limit.
- raw#15 personal-path-leak-ban: 본 doc 에 사용자별 absolute path 0 건 (relative 표기 only).
