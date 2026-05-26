# 🔄 DECODER M3 dispatch migration — raw curl → runpodctl (cloud-guard g8 정합)

> **상태**: dispatch surface 마이그레이션 LANDED — raw curl GraphQL → `runpodctl pod {create,get,delete}` + `hexa cloud {copy-to,nohup,poll,copy-from}` 로 치환 완료.
> M3 milestone 은 **여전히 미점화 상태**. 본 PR 은 [M3_FIRE.md](./M3_FIRE.md) §"차단 해소 경로" **Option A** 의 cloud-guard g8 정합화에 한정.
> 실제 4-pod fire 는 별도 user-authorized step.

## 정체 — M3_FIRE.md blocker 해소 path A

[M3_FIRE.md](./M3_FIRE.md) §"HONEST BLOCKER — cloud-guard 차단" verbatim cite:

```
$ RK=$(secret get runpod.api_key 2>/dev/null); \
  curl -s -X POST "https://api.runpod.io/graphql?api_key=${RK}" ...
cloud-guard (commons @D g8): refusing `curl … https://api.runpod.io/graphql?api_key=${RK}`
  — raw HTTP call to a rented-GPU pod API endpoint.
  Use `hexa cloud {run|nohup|poll|copy-to|copy-from|copy-dir-*|preflight}` instead
  ...
  Lifecycle verbs (create / get / start / stop / remove / show / search / launch / destroy)
  are NOT blocked — only remote exec / transfer / API calls.
```

→ 본 PR 은 `dispatch_p21h_v3_runpod.sh` 의 6 raw curl line 을 **lifecycle (runpodctl)** + **transport (hexa cloud)** verb pair 로 분리, cloud-guard g8 정합화.

## 6 raw curl line — BEFORE / AFTER 표 (verbatim cite)

`HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/dispatch_p21h_v3_runpod.sh` 원본 (origin/main b37d918f2):

### line 122 — GraphQL endpoint URL

| | content |
|---|---|
| BEFORE | `GQL="https://api.runpod.io/graphql?api_key=${RK}"` |
| AFTER  | (제거 — runpodctl 가 ~/.runpod/config.toml 의 api_key 自 사용) |
| 정합 | cloud-guard g8 — raw HTTP endpoint 제거 |

### line 128 — gql() 함수

| | content |
|---|---|
| BEFORE | `gql() { curl -s -X POST "$GQL" -H "Content-Type: application/json" -d "$1"; }` |
| AFTER  | (제거 — 모든 caller 는 `runpodctl pod <verb> -o json` 으로 대체) |
| 정합 | cloud-guard g8 — raw `curl` 함수 제거 |

### line 134 — teardown podTerminate mutation

| | content |
|---|---|
| BEFORE | `gql "{\"query\":\"mutation { podTerminate(input:{podId:\\\"$POD_ID\\\"}) }\"}" >/dev/null` |
| AFTER  | `runpodctl pod delete "$POD_ID"` |
| 정합 | runpodctl pod delete = lifecycle verb (cloud-guard 명시 허용) |

### line 146 — watchdog podTerminate mutation

| | content |
|---|---|
| BEFORE | `[ -n "$POD_ID" ] && gql "{\"query\":\"mutation { podTerminate(input:{podId:\\\"$POD_ID\\\"}) }\"}" >/dev/null` |
| AFTER  | `[ -n "$POD_ID" ] && runpodctl pod delete "$POD_ID"` |
| 정합 | runpodctl pod delete = lifecycle verb |

### line 154-159 — podFindAndDeployOnDemand mutation (pod create cascade)

| | content |
|---|---|
| BEFORE (154-156) | `Q=$(cat <<JSON`<br>`{"query":"mutation { podFindAndDeployOnDemand(input:{cloudType: $CLOUD, gpuCount:1, volumeInGb:0, containerDiskInGb:120, minVcpuCount:8, minMemoryInGb:64, gpuTypeId:\"$GPU\", name:\"p21h-v3-$INIT_VARIANT\", imageName:\"$IMAGE\", dockerArgs:\"\", ports:\"22/tcp\", volumeMountPath:\"/workspace\", env:[{key:\"PUBLIC_KEY\", value:\"$PUBKEY\"}]}) { id machineId } }"}`<br>`JSON`<br>`)` |
| BEFORE (158) | `R=$(gql "$Q"); echo "[create] cloud=$CLOUD gpu=$GPU resp: $(echo "$R" | head -c 250)"` |
| BEFORE (159) | `POD_ID=$(echo "$R" | python3 -c "import sys,json;d=json.load(sys.stdin);print((d.get('data',{}).get('podFindAndDeployOnDemand') or {}).get('id') or '')" 2>/dev/null)` |
| AFTER  | `R=$(runpodctl pod create --name "p21h-v3-$INIT_VARIANT" --gpu-id "$GPU" --gpu-count 1 --image "$IMAGE" --container-disk-in-gb 120 --ports "22/tcp" --cloud-type "$CLOUD" --volume-mount-path /workspace --min-vcpu-count 8 --min-memory-in-gb 64 --env "{\"PUBLIC_KEY\":\"$PUBKEY\"}" -o json)`<br>`POD_ID=$(echo "$R" \| python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('id','') or d.get('podId','') or '')" 2>/dev/null)` |
| 정합 | runpodctl pod create = lifecycle verb (cloud-guard 명시 허용) |

### line 168-177 — pod runtime ports query (SSH IP 조회)

| | content |
|---|---|
| BEFORE (169) | `PR=$(gql "{\"query\":\"query { pod(input:{podId:\\\"$POD_ID\\\"}) { runtime { ports { ip publicPort privatePort isIpPublic } } } }\"}")` |
| BEFORE (170-177) | `read -r IP PORT < <(echo "$PR" \| python3 -c "`<br>`import sys,json`<br>`d=json.load(sys.stdin)`<br>`rt=((d.get('data',{}).get('pod') or {}).get('runtime') or {}) or {}`<br>`for p in (rt.get('ports') or []):`<br>`    if p.get('privatePort')==22 and p.get('isIpPublic') and p.get('ip') and p.get('publicPort'):`<br>`        print(p['ip'], p['publicPort']); break`<br>`" 2>/dev/null)` |
| AFTER  | `PR=$(runpodctl pod get "$POD_ID" -o json)`<br>`read -r IP PORT < <(echo "$PR" \| python3 -c "`<br>`import sys,json`<br>`d=json.load(sys.stdin)`<br>`rt=(d.get('runtime') or {})`<br>`for p in (rt.get('ports') or []):`<br>`    if p.get('privatePort')==22 and p.get('isIpPublic') and p.get('ip') and p.get('publicPort'):`<br>`        print(p['ip'], p['publicPort']); break`<br>`" 2>/dev/null)` |
| 정합 | runpodctl pod get = lifecycle verb (cloud-guard 명시 허용) |

## runpodctl verb 매핑

| curl GraphQL mutation/query | runpodctl 대체 | cloud-guard 분류 |
|---|---|---|
| `mutation { podFindAndDeployOnDemand(...) }` | `runpodctl pod create -t H100 -d 0` 계열 (flag form: `--gpu-id --image ... --env`) | lifecycle (allowed) |
| `mutation { podTerminate(input:{podId:...}) }` | `runpodctl pod delete <pod-id>` | lifecycle (allowed) |
| `query { pod(input:{podId:...}) { runtime { ports { ... } } } }` | `runpodctl pod get <pod-id> -o json` | lifecycle (allowed) |
| `query { myself { id email } }` (preflight) | `runpodctl pod list` (active pod 0 검증) | lifecycle (allowed) |

runpodctl `--output` 은 default `json` — Python 파서가 `data.podFindAndDeployOnDemand.id` 대신 top-level `id`/`podId` 를 읽도록 1줄 조정.

## hexa cloud subverb 매핑

| 원본 dispatch_p21h_v3_runpod.sh 동작 | hexa cloud 대체 | line range |
|---|---|---|
| `$SSH "mkdir -p ..."` (line 195) | `hexa cloud exec <host> --port $PORT --insecure -- "mkdir -p ..."` | line 195 |
| `$SCP "$X" "root@$IP:$Y"` × 10 (line 196-211) | `hexa cloud copy-to <host> <local> <remote> --port $PORT --insecure` | line 196-211 |
| `$SSH "python3 ..."` (line 215, 229) | `hexa cloud exec <host> --port $PORT --insecure -- "python3 ..."` | line 215/229 |
| `$SSH "cd ... && nohup $CMD > train.log 2>&1 & echo TRAIN_PID $!"` (line 271) | `hexa cloud nohup <host> /workspace/p21hr/train.log --port $PORT --insecure -- python3 train_p21h_v3.py <argv...>` | line 271 |
| `$SSH "pgrep -f train_p21h_v3.py ..."` (line 288) | `hexa cloud poll <host> <TRAIN_PID> --port $PORT --insecure` | line 288 |
| `$SCP "root@$IP:$RESULT_POD" "$VDIR/result.json"` × 6 (line 305-310) | `hexa cloud copy-from <host> <remote> <local> --port $PORT --insecure` | line 305-310 |

`hexa cloud nohup` 의 **structured-argv** 형식이 핵심 — POSIX-quoted per token, remote shell parsing 없음 (cloud-guard preferred form, `hexa cloud --help` verbatim).

## Option 1 vs Option 2 결정 이유

Task 명시 2-option:

- **Option 1**: `dispatch_p21h_v3_runpod.sh` IN-PLACE 편집 (기존 .sh tolerated drift)
- **Option 2** (선호): 신규 `.hexa` wrapper — `exec()` shell-out 으로 `runpodctl` 호출

**선택: Option 2** — 이유:

1. CLAUDE.md `feedback-hexa-only-authoring` directive 정합 — 신규 .py/.sh 금지, 신규 .hexa 만 허용.
2. `HEXAD/CHAT/server/anima_temp_sweep.hexa` 등 선례 — `.py` 백엔드 + `.hexa` thin-wrapper + `exec()` dispatch 패턴이 anima 표준.
3. `runpodctl` 은 외부 binary, `.hexa` 의 `exec()` 로 호출하기에 충분 — lifecycle juggling 의 복잡도가 .py 영역에 없음 (runpodctl 自 ssh keypair · token mgmt 처리).
4. 기존 `.sh` 은 carry — 본 PR scope 는 NEW dispatch surface 추가, 기존 .sh 비제거 (사용자가 외부 셸 외 다른 경로 검토할 여지 보존).

→ **`CORE/DECODER/m3_fire_dispatch.hexa`** 신규 (236L) + 본 SSOT.

## m3_fire_dispatch.hexa 표면

| pub fn | 역할 |
|---|---|
| `m3_build_create_cmd(axis, init, gpu, cloud, image, pubkey)` | `runpodctl pod create` 명령 문자열 빌드 (line 154-159 대체) |
| `m3_build_get_cmd(pod_id)` | `runpodctl pod get <pod_id> -o json` (line 168-177 대체) |
| `m3_build_delete_cmd(pod_id)` | `runpodctl pod delete <pod_id>` (line 134/146 대체) |
| `m3_build_copy_to_cmd(host, port, local, remote)` | `hexa cloud copy-to` (line 196-211 SCP 대체) |
| `m3_build_nohup_cmd(host, port, logfile, argv)` | `hexa cloud nohup` (line 271 trainer launch 대체) |
| `m3_build_poll_cmd(host, port, pid)` | `hexa cloud poll` (line 288 pgrep 대체) |
| `m3_build_copy_from_cmd(host, port, remote, local)` | `hexa cloud copy-from` (line 305-310 SCP 대체) |
| `m3_fire_axis(axis, init, gpu, cloud, image, pubkey) -> map` | 한 축의 dispatch plan dict 반환 |
| `m3_fire_4axis(seed) -> list` | 4축 (A·B·C·D) plan list 반환 |
| `m3_fire_summary() -> string` | 1줄 표면 요약 |

**모든 함수는 명령 문자열을 빌드만 함 — `exec()` 호출 없음.** 실제 fire 는 별도 user-authorized step.

## hexa parse 검증 (verbatim)

```
$ hexa parse CORE/DECODER/m3_fire_dispatch.hexa
OK: CORE/DECODER/m3_fire_dispatch.hexa parses cleanly
```

## 다음 단계

1. **본 PR**: dispatch surface 마이그레이션만 (M3 milestone 미점화 유지).
2. **다음 PR (실 fire)**: `m3_fire_4axis(1337)` → 4축 plan harvest → `exec(create_cmd)` 4 병렬 (a_fire_autonomous + a_wall_first) → ckpt + result.json + train.log harvest (a_fire_recover_complete) → HF Hub PRIVATE/PUBLIC upload (a_hf_autonomous) → pod delete × 4 (lifecycle).
3. **M4 wiring**: ≥PARTIAL 축 ckpt 식별 후 DECODER.md M4 백엔드 배선 별도 PR.
4. **hexa-lang inbox**: 본 마이그레이션이 노출한 runpodctl ↔ raw GraphQL 동등성 gap 은 `hexa-lang/inbox/patches/runpod_dispatch_graphql_to_lifecycle.md` 로 carry (a_runpod_inbox) — 후속 PR 에서 file.

## p1~p8 정합 확인

| 원칙 | 정합 사유 |
|---|---|
| **p1 NO SYSTEM PROMPT** | ✅ V3 trainer corpus-only, system prefix 없음 |
| **p2 NO IDENTITY RULES** | ✅ identity.yaml 미사용 |
| **p3 NO PERSONA INJECTION** | ✅ anima_frac = corpus mixture ratio, prefix 아님 |
| **p4 NO ASSISTANT FRAMING** | ✅ base=Qwen2.5-1.5B BASE (NOT Instruct) |
| **p5 NO SPEAK()** | ✅ 본 PR 은 dispatch surface, emit 없음 |
| **p6 NO FINE-TUNED ETHICS** | ✅ RLHF 부재 |
| **p7 NO PERPLEXITY VERDICT** | ✅ verdict 는 per-lang gen + register-hit (simple-stack) |
| **p8 NO TRAIN/INFER SPLIT** | ✅ fire = substrate train (gradient + mitosis 연속체) |

## 결론

**M3 dispatch surface 마이그레이션 LANDED.** raw curl GraphQL 6 line 모두 `runpodctl` (lifecycle) + `hexa cloud` (transport) verb pair 로 분리, cloud-guard g8 정합화 완료.

**M3 milestone 은 미점화 상태 유지** — 본 PR scope 는 dispatch surface 한정, 실제 4-pod fire 는 별도 user-authorized step.
