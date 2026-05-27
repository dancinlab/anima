# AXIS_MAP-FAN BUG_POSTMORTEM F Phase D v1 stale-branch fire incident addendum

작성일: 2026-05-24 KST
스택: PR #211 (`HEXAD/V3/AXIS_MAP_BUG_POSTMORTEM.md` env-var-concat saga) → PR #248 (E OOM addendum) → 본 addendum (F Phase D v1 stale-branch fire)
도메인: HEXAD/PURE (V3 saga rebrand)

---

## § 사고 요약

Phase D 1차 fire (v1, 2026-05-24) 가 stale worktree branch 에서 발사되었다. branch 의 merge-base 는 8de602c07 (#366) 로 `--corpus-path` (#372) + `sources_upload` (#373) 두 PR 모두 부재한 시점이다. `dispatch.log` 는 전 단계 green 으로 보고했으나 train 은 garbage args 로 시작되었고, 사용자측 carryover sweep 중 pod 가 외부 terminate 되어 result.json 은 도착하지 않았다. ckpt 1차 분 유실, ~$1-2 sunk, 약 1.5시간 wall.

---

## § 타임라인

| 시각 (KST, 2026-05-24) | event |
|---|---|
| 시작 (≈ T0) | v1 dispatch 발사. dispatcher = `HEXAD/PURE/launchers/dispatch_p21h_v3.hexa` (stale branch `docs/pure-axis-map-auto-append-spec-v2` 의 버전) |
| T0 + ~1 min | pod create OK (A100 SXM 80 GB · `runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04`) |
| T0 + ~2 min | `sources_upload` log "OK" (실제로는 stale-branch 의 no-op stub — 8 sources scp + 6 mkdir 미수행) |
| T0 + ~2 min | `corpus_scp_override` log "OK" (`--corpus-path` 가 positional `variant` 로 parse, 무관한 default 동작이 OK 로 보고) |
| T0 + ~3 min | `train_launch` pid 298, `SAVE_POD=1 RETAINED` 로그. 실제 train 은 잘못된 args 로 garbage run 시작 |
| T0 + ~60 min | 사용자측 carryover sweep 진행 중. 무관한 idle pod 정리 과정에서 본 pod 외부 terminate |
| T0 + ~90 min | follow-on agent (a429bd968b3f71815) 가 result.json 부재 진단 시작 |
| T0 + ~95 min | branch merge-base 8de602c07 확인, `--corpus-path` / `sources_upload` 부재 root cause 확정 |
| T0 + ~95 min | rogue idle pod `ikgrx13pw5icmk` (v2 agent 첫 실패분) terminate 정리 |
| T0 + ~100 min | v2 재발사 준비 시작 (clean main branch 위에서) |

---

## § 진짜 root cause

세 요인이 합쳐서 "all green dispatch.log → no result.json" 의 misleading evidence pipeline 을 만들었다.

### (i) stale worktree branch

v1 발사 worktree 는 `docs/pure-axis-map-auto-append-spec-v2` 에 머물러 있었다. 이 branch 의 merge-base 는 commit 8de602c07 (`feat(HEXAD/PURE/launchers): dispatch_p21h_v3 + 8-factor motivation wiring + R6 mitosis cap 16` PR #366) 로, Phase D fire prereq 두 PR 모두를 선행한다:

- PR #372 (commit 9eb6488ca): `--corpus-path <local.jsonl>` 인자 추가 — local corpus scp override
- PR #373 (commit 7361e45ea): `sources_upload(host, opts, p21hr, dry_run)` — pod source-bootstrap 8 sources + 6 dirs

따라서 v1 dispatcher 는 두 기능 **모두 부재**한 상태였다.

### (ii) `--corpus-path` 가 positional `variant` 로 흡수

`dispatch_p21h_v3.hexa` 의 stale-branch argv parser 는 `--corpus-path` 를 unknown long-flag 로 인식하지 못하고, value `./state/pure_phase_d_corpus_.../merged.jsonl` 을 positional 로 흘려 보냈다. argv slot 매핑상 positional 1 = `variant`. 결과적으로 train job 은 `variant=./state/.../merged.jsonl` 로 잘못 fork 된 args 로 실행되었다.

### (iii) dispatch.log "green" semantic 의 구조적 결함

stale-branch dispatcher 의 두 단계는 invariant 가 약했다:

- `sources_upload`: stale 버전에서는 사실상 no-op stub. exit code 0 만 보고 OK 출력. 실제 remote 파일 stat / size / sha 비교 없음.
- `corpus_scp_override`: `--corpus-path` 가 parse 되지 않았으므로 override path 가 비어 있었음에도 "OK" 로 분기. condition branch 의 "skip" path 도 동일 OK 메시지 사용.

즉 dispatch.log 의 stage marker 는 "이 분기를 통과함" 만 의미하고 "이 분기의 contract 가 충족됨" 은 의미하지 않았다. PR #373 의 신규 sources_upload 는 remote stat verify 를 포함하므로, 사후적으로 보면 약한 invariant 가 신호 누락의 원인.

---

## § 부가 사고

### (a) rogue idle pod `ikgrx13pw5icmk`

v2 agent 의 첫 실패 시도가 만든 pod 가 idle 상태로 남아 있었다. recovery 과정 cleanup 단계에서 terminate. 비용 ~$0.1 미만 추산. v2 dispatch 가 신규 pod 를 따로 만들고 진행하면서 식별이 늦어진 사례.

### (b) pool-route hook silent failure (60-min Monitor `blvdsmuiv`)

recovery 시도 중 Monitor 가 60분간 단 한 line 도 emit 하지 않았다. 분석 결과 pool-route hook 이 `ssh` 명령을 다른 host 로 silently route 했고, key 미배포로 SSH 가 거부되었을 가능성이 가장 높다 (1회 cmd 후 hang 없이 즉시 silent fail 했을 것). 0 emit 패턴은 silent refuse 와 정합하지만 100% 검증되지 않음 (호스트별 ssh attempt log 미확보 — Honest C3 §8).

Workaround: `hexa cloud copy-from` / `hexa cloud run` 은 ssh 호출을 cloud verb 내부에서 wrap 하므로 pool-route 가 적용되지 않는다. v2b 부터 canonical pattern 으로 채택.

---

## § 재발 방지

### 5-1 dispatcher 발사 전 branch validation

dispatch_p21h_v3.hexa 진입 직후 prereq commits 가 현재 branch merge-base 의 ancestor 인지 확인. 예:

```sh
git merge-base --is-ancestor 9eb6488ca HEAD || die "missing PR #372 (--corpus-path)"
git merge-base --is-ancestor 7361e45ea HEAD || die "missing PR #373 (sources_upload)"
```

hexa-native 포팅 시: `cmd_check` 헬퍼 + `error_exit("PR prereq missing: <sha>")` pattern.

### 5-2 dispatch.log green semantic 강화

각 stage 의 invariant 를 **contract-strength** 로 격상:

- `sources_upload`: scp 후 `ssh <pod> "stat -c %s <path>"` 로 remote size 확인, local size 와 mismatch 시 fail.
- `corpus_scp_override`: `--corpus-path` 가 비어 있으면 OK 가 아닌 명시적 "(skip: legacy build)" 로 출력. 비어 있지 않으면 remote sha256 == local sha256 검증.
- `train_launch`: pid 보고에서 끝내지 말고, T+30s 시점 `ps -p $pid` re-check 으로 즉사 (args parse error / import error) 미발생 확인.

PR #373 의 sources_upload 는 일부 이미 충족하나, override branch 들의 강화는 별도 후속 PR 가치.

### 5-3 agent worktree branch lifecycle

fire 류 command (dispatch_*, train_*, fire_*) 진입 직전 `git rev-parse HEAD` 와 `git merge-base HEAD origin/main` 의 차이를 표준 출력에 1 line 으로 기록. 자동 rebase 까지는 위험 (uncommitted state 손상 가능) 하므로 explicit awareness 만 강제 — "branch X, merge-base Y, behind main by N" 형태.

cycle / fan-out skill 측 propagation gap 도 후속 조사 필요 (Honest C3 §8) — 다른 agent 가 만든 worktree 가 stale 인지 fresh 인지 spawn 시점에 검사할 위치가 명확치 않음.

### 5-4 Monitor 안 ssh 는 hexa cloud verb 강제

raw `ssh <pod>` / `scp <pod>:...` 직접 호출 금지, Monitor 또는 bg agent 안에서는 `hexa cloud run` / `hexa cloud copy-{to,from}` 만 사용. pool-route hook 회피의 부수효과로 cloud-guard 의 argv 검증도 같이 받게 된다. hexa-lang PR #646 의 cloud-guard UX 개선이 enforcement 측 후속.

---

## § 비용 + 손실

| 항목 | 값 |
|---|---|
| GPU sunk | ~$1-2 (A100 SXM 80 GB · ~1.5h wall · runpod community) |
| 1차 ckpt | LOST (pod 외부 terminate, scp 미회수) |
| dispatcher 시간 | ~1.5 h wall (발사 → terminate → diagnosis) |
| 사용자 직접 cleanup | 1회 (carryover sweep 중 무관 pod terminate 가 의도치 않게 본 pod 까지) |
| 산출물 | 0 (no result.json, no metric, no anchors) |

E OOM (PR #248) 의 ~$1.10 sunk 와 동급. 두 사례 합 ≈ $2-3 환경 학습 비용으로 분류.

---

## § Cross-reference

| PR / inbox | 범위 | 본 사고와의 관계 |
|---|---|---|
| #372 (anima) | `--corpus-path` 인자 추가 | v1 dispatcher 부재 원인 1/2 |
| #373 (anima) | `sources_upload` pod source-bootstrap | v1 dispatcher 부재 원인 2/2 |
| hexa-lang #629 | `cloud_bootstrap_sources` / `cloud_poll_until` / `cloud_create_pod_opts` 3 inbox patches | v1 dispatch 시 사용된 cloud 측 API 의 후속 강화 — bootstrap 단계 invariant 자체를 hexa-cloud 측 verb 로 흡수 |
| hexa-lang #646 | cloud-guard UX 개선 + pod-lock 5 findings | 5-4 Monitor ssh 강제 + rogue pod 식별의 enforcement 측 |
| PR #211 (anima) | env-var-concat saga | dispatcher 동일성. 실패 모드 = caller-side env-var (#211) vs runtime CUDA OOM (#248) vs branch staleness (본) — 3 직교 mode |
| PR #248 (anima) | E axis OOM (LangBalancedSampler) | 직접 선행 addendum. 본 PR 가 시리즈 F |

총 cross-ref = anima 측 3 PR (#372 #373 #211 #248 중 #211+#248 동일 시리즈 묶음) + hexa-lang inbox 2 PR (#629 #646) = **5건**.

---

## § Honest C3 agent epistemic limit

본 doc 의 다음 부분은 안전 추정 또는 검증 안 된 가정에 의존한다:

1. **타임라인 분 단위 ±** : T0 + ~1/2/3/60/90 min 값은 dispatch.log timestamp + 사용자 message 시각 정렬로 재구성. 분 단위 정확도는 ±2 min.
2. **rogue pod 비용** : `ikgrx13pw5icmk` 의 wall time 직접 확인 미수행. ~$0.1 미만은 idle pod 의 일반적 burn rate 로부터의 상한 추정.
3. **pool-route silent failure 단정** : Monitor 0 emit 패턴은 ssh refused 와 정합하지만, 호스트별 sshd auth log 미확보. 다른 가설 (cloud-guard 정상 차단 후 verbose suppress, hook 의 exec stage 실패 등) 도 완전히 배제되지 않음.
4. **agent worktree branch propagation gap source** : cycle skill 의 spawn 시점인지, Edit 도구의 worktree binding 인지, 사용자 직접 invoke 인지 미식별. 5-3 후속 조사 필요.
5. **dispatcher stage invariant 강도 평가** : `sources_upload` stable-branch 버전 (PR #373 후) 의 verify 강도는 source code 검토로만 확인, 실제 fail injection 테스트 미수행. 진짜 강도는 broken scp 케이스에서만 측정 가능.
6. **`--corpus-path` argv slot 매핑 단정** : positional `variant` slot 으로의 흡수는 stale-branch argv parser 의 코드 경로 추론. v1 실행 시점 train.log 의 args echo 직접 확보는 pod terminate 로 불가.
7. **사용자 cleanup 의 의도성** : "carryover sweep 중 외부 terminate" 는 사용자 측 의도 (본 pod 도 정리 대상으로 판단) 인지 우발 (UI 상 식별 실패) 인지 본 agent 가 판별 불가. 양자 모두 가능.
8. **rogue pod ↔ pool-route ↔ branch staleness 의 3 사건 동시 발생** 은 동일 session 의 fatigue / context overflow 의 공통 원인 가설로 묶을 수 있으나, 본 doc 은 단일 인과 사슬을 주장하지 않음. 세 사건은 직교로 기록.
