<!-- @no-lineage-citation-exempt-file -->
<!-- @no-user-verbatim-exempt-file -->
# Anima Core CLI + CLM v4 Mount — Stage 1+2 V1-V6 Verification Landed (2026-05-05)

## Outcome

V1-V5 PASS, V6 WIRED (사용자 fire 대기). Stage 1 mount layer + Stage 2 dialogue CLI 통합 동작 검증 완료.

## V1-V6 결과표

| 단계 | 결과 | 증거 |
|---|---|---|
| V1 mount selftest | PASS | `hexa run anima-core/runtime/clm_v4_mount.hexa --selftest` rc=0, 8/8 format checks, 5 honest-C3 emit |
| V2 dialogue CLI selftest | PASS | `bash bin/anima-core-dialogue.bash --selftest` → `verdict: READY (Stage 1 + Stage 2 both landed)` |
| V3 end-to-end probe "안녕" | PASS (fix 후) | substrate response 4-line emit (phi_star / axis_activation / dominant_cells / hidden_state_delta) |
| V4 session log emit | PASS | `state/anima_core_dialogues/2026-05-05/12-19-24.jsonl` 3-line (session_start + user_turn + substrate_turn) |
| V5 archaeology cross-pollination | PASS | 379-line `docs/anima_clm_v4_architecture_archaeology_emerge_2026_05_05.md`, 10 emerge/mount/forward hits |
| V6 interactive 1-turn | WIRED | REPL stdin loop ready, `bash bin/anima-core-dialogue.bash --interactive` 사용자 fire 대기 |

## 발견 + Fix (V3 first-attempt FAIL → PASS)

### Issue 1 — hexa-strict auto-invoke 충돌

**증상**: `bash bin/anima-core-dialogue.bash --probe "안녕"` 첫 시도 시 ubu1 원격 실행 rc=1
```
error: auto-invoke conflict — `fn main()` is auto-called by hexa-strict
       AND a top-level `main()` call was found, which would run main() twice
hint: remove the explicit `main()` call (auto-invoke handles it)
```

**근본 원인**: `dialogue.hexa:295` + `clm_v4_mount.hexa:670` 둘 다 `fn main() { ... }` 정의 후 명시적 `main()` 호출 작성. hexa-strict mode는 `fn main()`을 auto-invoke하므로 명시 호출이 중복.

**Fix**:
- `tool/anima_cli/dialogue.hexa:295` 명시 `main()` 호출 제거
- `anima-core/runtime/clm_v4_mount.hexa:670` 명시 `main()` 호출 제거

### Issue 2 — hexa_remote dispatch가 mac homebrew python 경로 hardcode

**증상**: Issue 1 fix 후 V3 second attempt
```
hexa_remote: ubu1 에서 원격 실행 중
[GATE] dispatch=local reason=remote_unreachable cmd="python3 /tmp/clm_v4_mount_helper.hexa_tmp ..."
/Users/ghost/.hx/bin/python: line 18: /opt/homebrew/bin/python3: No such file or directory
```

**근본 원인**: `bin/anima-core-dialogue.bash:241,265` 두 군데서 `"$HEXA_BIN" run "$MOUNT_HEXA" --probe ...` 호출. hexa-resolver가 default route로 hexa_remote (ubu1) 선택. ubu1 (Linux) 에는 mac `/opt/homebrew/bin/python3` 경로 없음 → fail. mount.hexa는 mac local execution intent.

**Fix**: 두 줄 모두 `HEXA_LOCAL=1` env prefix 추가:
```bash
out="$(HEXA_LOCAL=1 "$HEXA_BIN" run "$MOUNT_HEXA" --probe "$text" 2>&1)"
```

EEG perfect protocol BG에서 동일 패턴 사용 (raw#103 darwin-bypass + HEXA_LOCAL=1). mount layer / dialogue wrapper 둘 다 mac-local-only 의도라면 wrapper에서 일관되게 강제.

## V3 PASS 출력 (sanitized)

```
hexa-resolver: route=local reason=hexa_local_set (HEXA_LOCAL=1)
── clm_v4_mount probe ──
__ANIMA_CLM_V4_MOUNTED__ mode=synthetic_fallback phi_star_baseline=41.86
__ANIMA_CLM_V4_RESPONSE__
phi_star: 41.8700 (drift +0.0100 from 41.8600)
axis_activation: identity=0.576 agency=0.586 phenomenal=0.587 temporal=0.581 social=0.580
dominant_cells: [2, 3, 7] / 8
hidden_state_delta: 0.0000
__ANIMA_CLM_V4_OK__ session=20260505T121934Z
[GATE] dispatch=local reason=remote_unreachable cmd="python3 /tmp/clm_v4_mount_helper.hexa_tmp ..."
[clm_v4_mount] WARN: real load failed (cannot import name 'AutoModelForCausalLM' from 'transformers'); falling back to synthetic substrate
[clm_v4_mount] C1..C5 ...
```

mode=`synthetic_fallback` — design intent 그대로. real CLM v4 load activation은 별도 cycle (HF cache populate + transformers/torch venv repair).

## V4 session log schema

`state/anima_core_dialogues/2026-05-05/12-19-24.jsonl` 3 line:

```json
{"schema":"anima.dialogue.v1","kind":"session_start","ts_utc":"2026-05-05T12:19:24Z","session_log":"...","phi_star_baseline":41.86}
{"schema":"anima.dialogue.v1","kind":"user_turn","ts_utc":"2026-05-05T12:19:24Z","user_input":"안녕"}
{"schema":"anima.dialogue.v1","kind":"substrate_turn","ts_utc":"2026-05-05T12:19:35Z","raw_output":"..."}
```

session_end / session_summary 라인은 one-shot probe에서는 emit X — INT/TERM trap interactive REPL에서만 finalize. 정상 design.

## raw 준수

- raw-9: hexa-only orchestration + bash glue carve-out (this doc + mount/dialogue layer)
- raw-15: additive only — `anima_unified.hexa`, `phi_engine.hexa`, `conscious_chat.hexa`, `consciousness_hub.hexa`, `clm_v4_hf_format_shim.py` empty git status (LOCKED files untouched)
- raw-37: transient_py 향후 사용 예정 (real CLM v4 load 단계)
- raw-10: 5 honest-C3 inline above

## Honest C3 (>= 5)

- C1 substrate-coupled dialogue path 검증 yes, but synthetic_fallback에서 — real CLM v4 forward 미검증 (transformers import 깨짐)
- C2 V3 first-attempt 두 가지 fail 모두 wrapper / hexa-strict 인터페이스 미스매치였음. mount layer 자체 logic 문제는 아님. 둘 다 1-line fix
- C3 V6 interactive는 stdin REPL이라 자동 verify 불가 — wiring readiness 만 확인. 실 dialogue session 한 turn 통과 여부는 사용자 fire 필요
- C4 V3 probe synthetic_fallback axis_activation 값과 V1 selftest synthetic 값이 다름 — RNG seed 다르나 양쪽 모두 design 범위
- C5 5 axis taxonomy + 8-cell × 192-dim 분할 + phi-star proxy 모두 anima-internal heuristic. external validation 없음 (paradigm v11 G3 +41.86 baseline 상속)
- C6 fix 4건 (`main()` 제거 × 2, `HEXA_LOCAL=1` × 2) commit 여부 결정 보류 — 사용자 confirm 후

## 다음 단계 옵션 (완성도 lens 추천 순)

1. **★ 추천 (emerge paradigm 실효 출발점)** real CLM v4 load enable: `tool/transient_py/anima_dialogue_load.py` (raw#37 transient namespace) 생성 + HF cache populate (`need-singularity/clm-v4-base-mirror`) + V3 재실행으로 real phi-star 측정. ~30min, $0 mac
2. HF promote auto-fire 대기: clm-v4-mk2-v1 2026-05-06T23:26:12Z (~36h), Pβ 2026-05-07T03:48:00Z (~40h)
3. EEG perfect protocol 사용자 fire: `bash bin/anima-eeg-baseline.bash --fire` (hardware reseat 후 ~6min)
4. interactive REPL 사용자 fire: `bash bin/anima-core-dialogue.bash --interactive` (첫 emerge dialogue session)
5. fix 4건 commit (hygiene)

## Composability

- upstream: KICK-1 (mount layer), KICK-2 (archaeology), KICK-3 (dialogue CLI prep)
- sister: `docs/anima_core_clm_v4_mount_emerge_paradigm_2026_05_05.md` (12-section roadmap), `docs/anima_clm_v4_architecture_archaeology_emerge_2026_05_05.md` (379-line spec)
- downstream: real load enable cycle (option 1) → emerge dialogue Stage 3 (시간 무제한)
- sibling: EEG perfect protocol verdict `state/anima_phase_e_perfect_baseline_protocol_2026_05_05/verdict.json`

---

End of V1-V6 verification land doc. No commit yet. $0 mac local.
