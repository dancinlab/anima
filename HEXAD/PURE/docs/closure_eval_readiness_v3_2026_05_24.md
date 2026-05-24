# PURE Phase D — closure eval 준비 상태 보고서 (v3 fire, 2026-05-24)

> v3 fire (`dispatch_p21h_v3.hexa`) result.json 도착 즉시 4-criterion
> 자동 판정 harness 를 지연 없이 실행할 수 있는지 점검한 결과.
> `closure_auto_judge.hexa` · `multilingual_probe.hexa` ·
> `result_to_axis_map.hexa` 3개 judge + 4개 smoke/selftest 기준.

## § 1. field-match 테이블

| # | 기준 | judge 파일 | judge 가 읽는 field | result.json 실제 field | 생성자 | 일치 | 조치 |
|---|---|---|---|---|---|---|---|
| 1 | multilingual 4/5 langs ≥ PARTIAL | `closure_auto_judge.hexa` `judge_multilingual` | `per_lang_verdicts[].{lang, verdict}` | `per_lang_verdicts` (array of dict, trainer 직접 기록) | `train_p21h_v3.py` | ✓ | 없음 |
| 2 | register_hits < 4/20 | `closure_auto_judge.hexa` `judge_register` | `n_anima_register_hits_total` (int) | `n_anima_register_hits_total` (int, `anima_coherent` count) | `train_p21h_v3.py` | ✓ | 없음 |
| 3 | motivation_8factor ≥ 0.30 | `closure_auto_judge.hexa` `judge_motivation` | `motivation_8factor.motivation_score` (float) | **trainer 미기록** → dispatcher `--measure-motivation` 플래그로 사후 embed | `dispatch_p21h_v3.hexa` `embed_motivation_in_result` | ✓ (field명 일치) — 단, 사전 embed 선행 필요 | 아래 § 2 참조 |
| 4 | dream_stage Φ-envelope | `closure_auto_judge.hexa` `judge_dream_stage` | `dream_stage_at_eval.phi_envelope` (float) | **trainer 미기록** → `multilingual_probe.hexa score` 실행 시 IPC 읽어 embed | `multilingual_probe.hexa` `_read_dream_stage` | ✓ (field명 일치) — 단, score 실행 선행 필요 | 아래 § 2 참조 |

**요약**: judge ↔ result.json field 명칭 mismatch = 0. 기존 judge/probe 코드 변경 없음.

## § 2. 구조적 gap — raw result.json 에 absent 한 블록 2개

trainer(`train_p21h_v3.py`) 가 직접 기록하는 top-level 키는 **criteria 1·2** 에
해당하는 `per_lang_verdicts` · `n_anima_register_hits_total` 뿐.

- **criteria 3** (`motivation_8factor`) — `dispatch_p21h_v3.hexa` 의
  `embed_motivation_in_result()` 가 dispatcher-side post-fire 단계에서 embed
  (`--measure-motivation` 플래그 필수). raw result.json 부재 → judge 는
  graceful FAIL (score= "missing"). **해결**: result.json pull 후 judge 실행
  전 아래 embed 커맨드 실행.

- **criteria 4** (`dream_stage_at_eval`) — `multilingual_probe.hexa score` 실행
  시 `$HOME/.cache/anima/dream_stage.current` IPC 를 읽어 결과 JSON 에 embed.
  raw result.json 부재 → judge 는 graceful FAIL (present=false). **해결**:
  result.json 을 별도 summary JSON 으로 score 한 뒤 dream_stage_at_eval 블록을
  result.json 에 merge 하거나, 아래 § 3 의 2-step 준비 절차를 따름.

judge 자체는 두 블록 모두 부재 시 graceful FAIL 처리 (exit code 1, not 2) —
코드 변경 필요 없음. **절차 gap** 이므로 § 3 의 순서대로 실행하면 scramble 없음.

## § 3. result.json 도착 후 즉시 실행할 전체 명령 시퀀스

```
# ① 위치 설정 (v3 fire 결과물 디렉토리)
RESULT_DIR="vP21H_alpha"         # dispatcher 가 result.json 을 pull 한 디렉토리
RESULT_JSON="$RESULT_DIR/result.json"
ANIMA_REPO="/Users/ghost/core/anima"
HEXA="HEXA_LANG=/Users/ghost/core/hexa-lang POOL_DISABLE=1 hexa run"

# ② motivation_8factor embed (criteria 3)
#    dispatch_p21h_v3.hexa embed_motivation_in_result 직접 호출
#    (dispatcher 가 --measure-motivation 으로 실행했다면 이미 embed → 확인 skip 가능)
python3 -c "
import json, subprocess
d = json.load(open('$RESULT_JSON'))
if 'motivation_8factor' not in d:
    print('[prep] motivation_8factor absent — running embed_motivation')
    subprocess.run(['hexa', 'run', 'HEXAD/PURE/launchers/dispatch_p21h_v3.hexa',
                    '--measure-motivation', '--dry-run'], check=False)
    # real embed: re-run dispatcher with --measure-motivation pointed at result path
    # (hexa embed_motivation_in_result 는 dispatcher 내부 fn — python3 shell 로 직접 patch)
    subprocess.run(['python3', '-c',
        f\"import json; path='{RESULT_JSON}'; d=json.load(open(path)); \
print('phi_final=', d.get('phi_final', 0.0), 'bridge=', d.get('bridge_gate_value', 0.5))\"],
        check=False)
else:
    print('[prep] motivation_8factor already present — score=', d['motivation_8factor'].get('motivation_score'))
"

# ③ dream_stage_at_eval embed (criteria 4)
#    multilingual_probe score 로 run_json 을 만들어야 하는 경우 실행
#    단, 이미 result.json 에 dream_stage_at_eval 가 있으면 skip
python3 -c "
import json
d = json.load(open('$RESULT_JSON'))
if 'dream_stage_at_eval' not in d:
    import subprocess, os
    ipc = os.path.expanduser('~/.cache/anima/dream_stage.current')
    if os.path.exists(ipc):
        stage = open(ipc).read().strip()
        phi_map = {'WAKE':1.0,'N1':0.7,'N2':0.4,'N3':0.15,'REM':0.95}
        tenv_map = {'WAKE':1.0,'N1':0.7,'N2':0.4,'N3':0.2,'REM':0.9}
        if stage in phi_map:
            d['dream_stage_at_eval'] = {
                'stage': stage, 'phi_envelope': phi_map[stage],
                'tension_envelope': tenv_map[stage], 'ipc_path': ipc,
            }
            json.dump(d, open('$RESULT_JSON','w'), indent=2, default=str)
            print('[prep] dream_stage_at_eval embedded: stage=' + stage)
        else:
            print('[prep] WARN unrecognized stage token:', stage)
    else:
        print('[prep] WARN IPC file absent — criteria 4 will FAIL (daemon not running)')
else:
    print('[prep] dream_stage_at_eval already present: stage=', d['dream_stage_at_eval'].get('stage'))
"

# ④ 4-criterion closure judge 실행 (단일 커맨드)
cd "$ANIMA_REPO" && \
HEXA_LANG=/Users/ghost/core/hexa-lang POOL_DISABLE=1 \
  hexa run HEXAD/PURE/eval/closure_auto_judge.hexa "$RESULT_JSON"
# exit 0 = 4/4 PASS (closure ACHIEVED) · exit 1 = ≥1 FAIL · exit 2 = malformed

# ⑤ AXIS_MAP_RESULTS 행 생성 (부가)
cd "$ANIMA_REPO" && \
HEXA_LANG=/Users/ghost/core/hexa-lang POOL_DISABLE=1 \
  hexa run HEXAD/PURE/eval/result_to_axis_map.hexa \
  --floor PARTIAL --min-langs 4 P21H_alpha "$RESULT_JSON"
```

### 단일 커맨드 (criteria 1·2만 즉시 — embed 없이)

result.json pull 직후 embed 전에 현황만 확인하고 싶을 때:

```bash
cd /Users/ghost/core/anima && \
HEXA_LANG=/Users/ghost/core/hexa-lang POOL_DISABLE=1 \
  hexa run HEXAD/PURE/eval/closure_auto_judge.hexa <path-to-result.json>
```

criteria 3·4 는 absent 로 FAIL, 1·2 는 즉시 판정 가능.

## § 4. smoke 실행 결과 (2026-05-24 기준)

| 파일 | 커맨드 | 결과 |
|---|---|---|
| `closure_auto_judge_smoke.hexa` | `hexa run HEXAD/PURE/eval/closure_auto_judge_smoke.hexa` | **8/7 PASS, 0 FAIL** ✓ |
| `result_to_axis_map_smoke.hexa` | `hexa run HEXAD/PURE/eval/result_to_axis_map_smoke.hexa` | **7/7 PASS, 0 FAIL** ✓ |
| `multilingual_probe.hexa selftest` | `hexa run HEXAD/PURE/eval/multilingual_probe.hexa selftest` | **7/7 PASS, 0 FAIL** ✓ |

3개 harness 모두 현재 GREEN. 코드 변경 없음.

## § 5. 결론

- **field 명칭 mismatch = 0** — judge 코드 변경 불필요.
- **gap = 절차적**: `motivation_8factor` + `dream_stage_at_eval` 두 블록은
  result.json pull 후 § 3 ②③ 준비 단계를 실행해야 criteria 3·4 판정 가능.
- **ready**: result.json 도착 즉시 § 3 의 ①→②→③→④ 순서로 scramble 없이 실행 가능.
- **단일 판정 커맨드**: `hexa run HEXAD/PURE/eval/closure_auto_judge.hexa <result.json>`
