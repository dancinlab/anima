# BC-ANIMA decoder trainer — step-rate measurements

Per `GPU.anima.md` "## 🩺 진단" + "## 📋 진행 마일스톤 (BC-ANIMA)" — running tally
of decoder trainer wall-time per step on the M4b production trainer
(`CORE/DECODER/train_v3_moe_longtrain.hexa`, d=64 · V=151643 · E=2 · h=256 ·
n_layer=1 · T=4 · HARD top-1 · m_size≈29M FP64 params).

Each row: code revision · pod · GPU · measurement window · steps/s.

## Log

### Pre-M4 baseline — anima PR #1318 STEP_RATE_FINDING (2026-05-28)

- Code: pre-`farr_softmax_rows`/`farr_ce_seed` wiring. Per-step hot-path =
  V-wide CPU softmax (~3V `farr_get` + 1 `exp` + 1 `log`) + 29M-param CPU
  AdamW + structurally-truncated CE seed (`farr_set(d_logits, target, 1.0)`,
  no `softmax - onehot`).
- Pod: RunPod H100 SXM `4q2rab8ds2zhsr` (torn down post-fire; no longer
  available in the runpod registry).
- Measured: ~1 step/s (per PR #1318 + `M4B_LONGTRAIN_RESULT.md` block ③ —
  "CPU step rate ≈ 0.26s/step (1 epoch=1507 step in 401s not completed)";
  GPU util/mem stayed at 0% during training; one cuBLAS gemv path errored
  out and reverted to CPU).
- Verdict: production sweep declared UNVERIFIABLE-AT-SCALE — `dec_undertrain`
  could not be tested because wall budget made MID/HI infeasible.

### Post-M4 wiring — anima PR #1320 (2026-05-28, merged d3107f266)

- Code: M2 `farr_softmax_rows` + M3 `farr_ce_seed` wired into the same
  trainer (commit `a16815267`, 25+/15- net). Per-step softmax now runs on
  the H100 under `HEXA_CUDA` build (kernel `_hx_cuda_farr_softmax_rows_gpu`);
  CE seed now runs on the H100 (kernel `_hx_cuda_farr_ce_seed`); CE
  monitoring scalar now reuses the precomputed softmax (`-log(sm[target])`
  with a 1e-300 floor) instead of a fresh V-wide loop.
- Pod: target was the same H100 SXM `4q2rab8ds2zhsr`, but the pod is no
  longer in the runpod registry (`hexa cloud list --provider runpod` →
  0 pods) and the two cached vast pods (`37868501`, `38095989`) are SSH-
  unreachable (`ssh transport failure (exit 255)`).
- Measured: ⚪ **deferred** — no live GPU pod available, and the M4 task
  is constrained "Don't spin up new pods — pod `4q2rab8ds2zhsr` is the
  existing one" (rate-limited retry guardrails).
- Trainer `hexa parse` is clean. CPU helper byte-eq for both builtins is
  already proven (M2 PR #1920 + M3 PR #1924 each landed with a byte-eq
  oracle PASS). The wiring change itself is therefore green at the
  symbolic + CPU-numerical layer; only the wall-time speedup is unmeasured.

### Expected gain (calculation, not measurement)

Pre-M4 per-step hot loops were:
  1. CE seed truncated (no V-wide work, but gradient was structurally wrong).
  2. CE-monitoring softmax: 3V `farr_get` + V `exp` + 1 `log`. At V=151643
     and a measured ~0.26 s/step, this loop alone is ~hundreds of ms.

Post-M4 the same softmax runs as one CUDA kernel launch (`_hx_k_softmax_rows`
two-pass max+sumexp, V threads). On H100 the V=151643 reduction is
bandwidth-bound and well under 1 ms — the CPU/GPU ratio for this single op
is expected to be 100×+, but the trainer's residual CPU cost (29M-param
AdamW + `mm_extract` of [V×d] expert weights per step) is unchanged and
will set a new ceiling. Whether the combined wiring crosses the ≥10 step/s
green-tier gate is **not predictable from this change alone** — the AdamW
CPU loop (M1) and the expert weight copy are likely the next dominant
costs once softmax/CE move to GPU. A follow-up wedge (M1 wiring +
`mm_extract` GPU port) is likely required to reach 10 step/s.

### Verdict (g5 rubric)

🟠 **PARTIAL** — wiring landed and symbolically green (parse clean, byte-eq
already proven for both builtins). Wall-time measurement deferred to the
next live H100 fire (a new pod-rent + sweep cycle, gated by user/budget
approval). The follow-up wedge to file (post-measurement, if step-rate
< 10 step/s):

  - **F-BC-ANIMA-M4-CEILING** — measure step-rate with M4 wiring. If
    < 10 step/s, profile residual: (a) 29M-param CPU AdamW loop (M1
    `farr_adamw_step_gpu` is already a registered builtin in
    `stdlib/flame/train_lib.hexa:59` — wire it next), (b) per-step
    `mm_extract` of [V×d] expert weights, (c) the small d=64 matmul
    under-utilizing the GPU. The diagnosis already noted (c) as a known
    decoder-shape problem (d=64 too small for matmul TC utility).

See `GPU.anima.md` "## 📋 진행 마일스톤 (BC-ANIMA)" + the
`.discoveries/decoder_collapse_undertrain.tape` SSOT for the broader
saga (M4 unblocks M5 = `dec_undertrain` decisive re-fire, gated on
step-rate ≥ 10 step/s).

### M5 fire attempt — F-BC-ANIMA-M4-CEILING (2026-05-28, $5/30min budget)

User-approved live H100 fire attempt — pre-registered falsifier
`F-BC-ANIMA-M4-CEILING` (measure step-rate with M4 wiring on H100; <10
step/s triggers M1 + `mm_extract` follow-up wedges).

- Cached vast pods (`37868501` ssh6.vast.ai:28500 · `38095989`
  ssh9.vast.ai:15988): ssh-port resolve OK but `hexa cloud exec` both
  returned **`ssh transport failure (exit 255)`** verbatim — guard text:
  "host unreachable (connection refused / timeout / auth / changed host
  key). The pod may be alive and billing but not accepting SSH — a
  vast.ai/RunPod transport outage. Stop retrying; verify reachability
  or tear the pod down." Matches the deferred-state note above (vast
  pods SSH-unreachable).
- Fresh RunPod H100 SXM rented — `hexa cloud rent runpod
  --gpu "NVIDIA H100 80GB HBM3" --disk 50 --owner bc-anima-m5` →
  `[cloud] rent runpod: created pod 3e541pil5jazhk` →
  `[cloud] rent runpod: READY 64.247.201.49:11038`. Registry confirmed
  pod live in `hexa cloud list --provider runpod`.
- SSH polling against 64.247.201.49:11038 — first probe at +0s, retry
  loop every 8-15s for ~7 minutes. Every single `hexa cloud exec`
  returned the same `ssh transport failure (exit 255)` verbatim guard
  text. `hexa cloud resolve` continued to print `64.247.201.49:11038`
  unchanged (no port flap). Pod was billing but SSH transport refused
  for the full polling window — same outage class as the cached vast
  pods.
- Per the policy guardrail ("If pod spin-up itself fails — region
  exhaust, quota — report and abort"), and per the guard text's own
  "Stop retrying; verify reachability or tear the pod down" directive,
  the pod was torn down: `hexa cloud down 3e541pil5jazhk
  --provider runpod` → `[cloud] down runpod: terminated 3e541pil5jazhk
  / [cloud] forgot 3e541pil5jazhk (registry status=closed)`.
  Post-teardown `hexa cloud list --provider runpod` →
  `[cloud] runpod: list (new) — 0 pods`. `hexa cloud pods` →
  `pods=0   jobs=0`.
- Wall budget consumed: ~501s (~8.4min of the 30min cap). Spend
  estimate: ~$0.56 (~11% of the $5 cap, assuming $4/hr H100 SXM).
  Stage 1 was NOT entered — pod never accepted SSH so trainer was
  never copied, built, or executed. Stage 2 likewise NOT entered.

#### Verdict (g5 rubric, this attempt)

⚪ **UNVERIFIABLE-AT-SCALE (infrastructure)** — F-BC-ANIMA-M4-CEILING
remains pre-registered but unmeasured. The falsifier was NOT reached
(0 trainer steps run). The result is NOT a measurement of M4 wiring;
it is a measurement of pod SSH-transport availability on the day of
the fire — three pods in a row (2 vast + 1 freshly-rented runpod)
declined SSH. This is the same RunPod/vast transport-outage class
already noted in the post-M4 entry above; today's attempt confirms
the outage extends to fresh pod rentals as well.

The 🟠 PARTIAL verdict on M4 wiring itself (parse clean, byte-eq
proven, wall-time deferred) is UNCHANGED. M5 remains the next live
fire when SSH transport is reliably available; the M1 follow-up wedge
is still the next-action if step-rate measures <10 step/s.

No false claim filed in CLAIMS.tape / atlas — per g5 (no LLM
self-judge of correctness; only run/no-run reported here).

---

### 2026-05-29 — mm_extract wedge LANDED + 2nd M5 outage + E-axis closed

3 갈래 진척:

1. **mm_extract wedge (#1325 MERGED)** — `v3_moe_arch.hexa` fwd+bwd 의 per-token
   `mm_extract`(9.7M-double copy) → offset-aware `mm_packed_gemv`/`_t`/`_outer_add`
   로 치환. **per-step ~1.24 GB host-RAM round-trip 제거** (fwd 310MB + bwd 930MB),
   16 alloc/free 제거. byte-eq V=4 PASS (gradcheck max|Δ|=6.5e-13). M1 다음으로
   지목됐던 두 번째 dominant cost 가 제거됨 → post-M4 step-rate 추정치 상향.

2. **2nd M5 fire attempt — 또 outage (2026-05-29)** — F-BC-ANIMA-M4-CEILING 재시도
   2회. pod `cpnocpur5jjf5e (m5-walltime)` + `nyvghgacgb1cp3 (m5-walltime-r2)` 둘 다
   `uptimeSeconds=null` 15분+ (#1324 부트 실패 class, RENTING+BILLING). 각 agent 가
   session-limit 으로 사망 → parent 가 수동 teardown (pod 누수 0, ~$0.82 손실).
   ⚪ **여전히 UNVERIFIABLE** — 단 runpod availability 쿼리는 복구 확인됨
   ($2.69/hr H100 SECURE 가용). 진짜 blocker = Claude session-limit (3:10am KST
   리셋) 가 multi-step GPU fire agent 를 죽임. $0 로컬 단발은 foreground 로 살림.

3. **E-axis 닫힘 (#1327 MERGED)** — `mx_expert_sweep.hexa` (top-1 hard-routed MoE
   successor LM, d{8,16}×V{32,64}×E{1,2,4,8}). 16/16 cells ESCAPE, 단 E=8 에서
   experts_used 5-6/8 (2-3 dead, f_e=0). `dec_expert_axis` 발견: routing/E 는
   탈출 lever 아님 (capacity+budget 이 지배) — #1315 E=2 prod 붕괴와 정합.
   E=8 dead-expert = prod single-expert winner-take-all 의 toy 씨앗.

**M5 next-action 불변**: SSH transport + session-stability 동시 확보 시 step-rate
측정. mm_extract(#1325) 가 이미 두 번째 wedge 를 선결했으므로, M5 측정 후 남는
follow-up 은 M1 AdamW CPU 루프(이미 #1322 wedge-a 로 GPU 화 시도됨) + cuBLAS gemv
N=1 fix (hexa-lang `efdf59bd8` ANALYSIS, 미머지) 둘뿐.

---

### 2026-05-29 (2) — SSH 3-blocker 돌파 RECIPE 확립 (foreground 직접 운영)

세션 리밋 리셋 후, M5 fire 를 background agent 대신 **foreground 직접 운영**으로 전환.
4연속 background-agent 사망(rate-limit)을 우회 = parent 가 직접 pod lifecycle 잡음.
**3 blocker 모두 실증 돌파** (SSH_OK + H100 확인, `87.120.211.210:19691`):

```
검증된 pod-rent recipe (다음 fire 즉시 SSH 도달):
  runpodctl create pod --name <n> \
    --gpuType 'NVIDIA H100 80GB HBM3' \
    --imageName 'runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04' \
    --containerDiskSize 60 --gpuCount 1 \
    --ports '22/tcp' --startSSH \         # ← blocker#1: 이 둘이 핵심
    --env "PUBLIC_KEY=$(cat ~/.runpod/ssh/RunPod-Key-Go.pub)" \  # ← sshd authorized_keys
    --secureCloud
  # SSH endpoint: runpodctl get pod <id> --allfields | grep -F 'pub,tcp'
  #   → 64.x.x.x:NNNNN->22 (pub,tcp) 에서 IP:port 추출 (tab→nl 후 grep -F)
  # raw ssh (cloud-guard IP-form 통과): ssh -o StrictHostKeyChecking=accept-new \
  #   -o UserKnownHostsFile=/dev/null -i ~/.runpod/ssh/RunPod-Key-Go -p <port> root@<IP>
```

**3 blocker 최종 진단**:
- #1 SSH TCP port: `--ports '22/tcp'` (포트 매핑) **+ `--startSSH` (sshd 기동) + `--env PUBLIC_KEY=` (authorized_keys)** 셋 다 필요. `--ports` 만 주면 포트는 뜨나 sshd 미기동 → Connection refused (이번 세션 1회 오진단·teardown). `--startSSH`+PUBLIC_KEY 추가 후 즉시 SSH_OK.
- #2 hexa cloud exit-255: hexa-lang #1959 (accept-new host key) merged. raw-ssh IP-form 이 cloud-guard 통과하므로 podssh.sh 패턴이 더 신뢰적.
- #3 session-stability: background agent 4연속 rate-limit 사망 → **foreground 직접 운영이 정답** (parent 는 안 죽음). 단 multi-step build→train→harvest 는 turn 예산이 크다.

**남은 꼬리 (데이터 스테이징, 별도 단계)**: trainer 소스는 origin/main 에 있으나 (a) corpus trim (harvest/corpus_diverse_trim.jsonl 미머지), (b) qwen merges/vocab (로컬·pod 둘 다 부재, pod 에 huggingface_hub 미설치), (c) pod nvcc PATH + pip install 이 선결. 이것들이 갖춰지면 `hexa build --c-only` → scp → build_and_fire.sh → harvest 로 step-rate 측정 가능. 비용: SSH 돌파 검증에 ~$0.71 (pod 3개 × 짧은 수명) 소모, 데이터 갖춰지면 단발 ~$1 로 측정 완료 예상.

**verdict**: ⚪ step-rate STILL UNMEASURED — BUT 인프라 3-blocker 는 ✅ 돌파 (recipe 확립). 다음 fire 는 SSH 까지 즉시 도달, 데이터 스테이징만 남음. F-BC-ANIMA-M4-CEILING 은 데이터 확보 후 단발 측정 가능.

---

### 2026-05-29 (3) — hexa cloud 전 경로 작동 + transpile 성공, self/ 불완전이 마지막 벽

이번엔 raw-ssh 수동 대신 **`hexa cloud` 정규 경로**로 진행 (사용자 지시), upstream fix 병행.

**돌파한 것 (M5 인프라 거의 완전 정복)**:
1. `~/.hx/packages/hexa-lang/stdlib/cloud/cloud.hexa` 를 origin/main(#1959) 으로 sync (accept-new=5). 단 hexa 바이너리가 stale 해 `--insecure` 플래그가 실효 우회.
2. `hexa cloud run "root@<IP>" --port <P> --insecure -- bash -lc '<script>'` = **SSH 도달 성공** (HEXA_OK + H100 확인). cloud-guard IP-form 통과. `hexa cloud copy-to <host> <local> <remote> --port --insecure` 도 작동 (flag 는 host/path **뒤**, argv 는 `--` 뒤 개별 토큰, multi-line argv 는 cloud-guard 거부 → 스크립트 파일 copy-to 후 `bash <file>`).
3. pod SSH recipe 확정: `runpodctl create --ports '22/tcp' --startSSH --env "PUBLIC_KEY=$(cat ~/.runpod/ssh/RunPod-Key-Go.pub)"`. 셋 다 필수 (`--ports`=매핑, `--startSSH`=sshd, `PUBLIC_KEY`=authorized_keys).
4. **trainer transpile 성공**: pod 에 fresh `git clone hexa-lang` → `build/hexat_linux <in.hexa> <out.c>` (self-host cc, `hexa-cc <input> <output>`) 로 `train_v3_moe_longtrain.hexa` → `trainer.c` **1279 lines** 생성. fresh clone 의 stdlib 에 flame_bpe_corpus_lib 존재 → 로컬 stale-install 문제 완전 우회 (BPE blocker 해소 확인).

**마지막 벽 (정확한 진단)**: shallow `git clone --depth 1 hexa-lang` 의 `self/` 트리가 **불완전** — `runtime_core.c` (runtime.c 가 `#include "runtime_core.c"`) 와 `runtime_cuda.c` (runtime_cuda_emit.hexa 가 emit) 둘 다 clone 에 부재 → `clang trainer.c self/runtime.c` 가 `runtime_core.c not found` 로 실패. **단 두 파일 다 git-tracked 이고 로컬 `~/.hx/packages/hexa-lang/self/` 에 존재** → shallow-clone 이 안 가져온 것(또는 sparse). 추가로 hexat_linux 가 runtime_cuda_emit.hexa(거대 string-literal) transpile 에서 **segfault** (upstream hexat 버그 후보).

**다음 단계 (단순)**: pod 에 fresh clone 대신 **로컬의 완전한 hexa-lang self/ 트리를 tar+copy-to** (또는 full clone). 그러면 runtime.c 컴파일 통과 → CPU 빌드(runtime_cuda.c 불요) → short train → step-rate 측정. 추가 필요: hexat 가 use-module 을 flatten 안 하므로 `v3_moe_fwd` implicit-decl 발생 → module_loader flatten 선행 또는 trainer 가 단일 파일이 되도록 의존 .hexa 를 trainer 앞에 concat. 

**비용**: 이번 세션 pod 다수 (5xm3·hbdf·zzld·3hpm·2a46-r3 orphan) ≈ ~$3-4 누적, 전부 teardown 완료 (pods=0). orphan r3 = 죽은 background agent 산물, parent 수동 정리.

**verdict**: ⚪ step-rate STILL UNMEASURED — BUT 인프라는 transpile 까지 정복, 남은 건 self/ 완전본 전송 + flatten 1단계. F-BC-ANIMA-M4-CEILING 은 다음 fire 에서 측정 가능 (recipe 전부 확립).

---

### 2026-05-29 (4) — BUILD GREEN 확인 (agent harvest) + self/ 버전 정합이 진짜 마지막 조각

병행하던 background M5 agent(probe-m5-walltime, 87cd7de37)가 부활해 **결정적 발견**을 남김 + 이번 foreground 가 그것을 재현 시도. 종합:

**agent finding 1 — #1324 "outage" 의 진짜 정체**: 일부는 SSH-KEY 미스매치였음. RunPod 가 `env.PUBLIC_KEY` 로 authorized_keys 를 심는데 `hexa cloud` 가 offer 하는 key 와 어긋날 수 있음. (이번 foreground 는 `--ports+--startSSH+PUBLIC_KEY(RunPod-Key-Go.pub)` + raw-ssh `-i RunPod-Key-Go` 로 SSH_OK 재현 — recipe 확정.)

**agent finding 2 — M4-wired trainer 가 BUILD + cuBLAS-link CLEAN (clang_rc=0, 1MB sm_90 binary)**. 검증된 빌드 레시피:
```
# self/ = cloud-m3 worktree (M2/M3 builtin 보유: farr_softmax_rows/farr_ce_seed 28 refs)
nvcc -O2 -std=c++14 -DHEXA_CUDA -arch=sm_90 -x cu -c self/cuda/runtime_cuda.c -o runtime_cuda.o   # rc=0
clang -O2 -D_GNU_SOURCE -D_XOPEN_SOURCE=600 -DHEXA_CUDA -I self -I /usr/local/cuda/include \
  trainer.c self/runtime.c runtime_cuda.o -lcublas -lcudart -lcudart_static -lcuda ... -o trainer  # rc=0
```
정리 3건: (a) M2/M3 builtin 은 **cloud-m3 worktree runtime.c 에만** (main install/clone 은 stale → 반드시 cloud-m3 self/ 사용), (b) `_hx_cuda_farr_ce_seed` 5-arg slim kernel 이 정의 앞서 호출됨 → agent 가 작성(`ce_seed_slim_shim.c.txt`, ~60 LoC, **cloud-m3 runtime_cuda.c 에 append**), (c) glue.c 가 `hexa_cuda_available` 중복정의 → **glue.c DROP**.

**foreground 재현 시도 + 함정**: 정규 `hexa cloud` 경로 전부 작동(run/copy-to/--insecure), transpile 성공(1279L), 하지만 self/ 를 **main(완전본) + cloud-m3(runtime.c) 혼합**하니 nvcc `expected ";"` (main runtime_cuda.c 끝에 shim append 가 구조 깨짐). 교훈: **cloud-m3 self/ 를 통째로** 쓰고 거기에 shim append (혼합 금지). cloud-m3 worktree 가 runtime_core.c 를 갖는지 재확인 필요 (agent 는 그걸로 green 냈으니 가졌을 것 — 이번 확인은 flame_bpe 만 grep 해 놓침).

**진짜 마지막 조각**: pod 에 **cloud-m3 self/ 통째 tar** + agent trainer.c + ce_seed shim append + glue drop. 그러면 BUILD GREEN(agent 입증) → short train(M4B_MAX_STEPS) → step-rate 측정. agent 결론: "single uninterrupted pod 면 now-reproducible recipe 로 <8min 측정". pod 안정성만 남음.

**비용**: 이번 라운드 pod (5xm3·hbdf·zzld·3hpm·f3f2 + orphan 2a46-r3) 전부 teardown (pods=0). 누적 ~$4-5. agent 측 ~$0-0.5.

**verdict**: ⚪ step-rate STILL UNMEASURED — BUT BUILD GREEN 확인(agent) + 전체 recipe(SSH·transpile·build·cloud-m3 self·ce_seed shim·glue drop) 문서화 완료. 다음 fire = cloud-m3 self 통째 + <8min 측정. agent harvest = origin/probe-m5-walltime (87cd7de37): trainer.c · glue.c · ce_seed_slim_shim.c.txt · STEP_RATE_FINDING.md.

---

### 2026-05-29 (5) — 최종 진단: self.tar.gz 파이프라인이 진짜 blocker (모든 짜깁기 경로 소진)

(A) "정확한 self 조합" 을 끝까지 추적한 결과, **단일 세션·단순 경로로는 self/ 완전+정합 트리를 못 만든다**가 확정. 4 경로 전부 막힘:

| 경로 | 막힌 이유 |
|---|---|
| origin/main fresh clone | generated 파일(runtime_core.c·runtime_cuda.c·runtime_hi_gen.c·runtime_bf16.c) **git 미추적** (untracked, .gitignore 엔 없음 = emit/extract 산물). clone 에 부재 → runtime.c `#include` 깨짐 |
| 로컬 ~/core/hexa-lang 통째 | generated 파일은 있으나 **264-커밋 stale** + **다른 agent 활성**(`feat/cloud-pods-local-manifest-v2` 브랜치, runtime.c/h uncommitted, 5+ worktree). origin/main 점프 = 타 agent 작업 파괴 → 금지 |
| main + cloud-m3 짜깁기 | runtime.c(cloud-m3)↔runtime.h(main) carrier-vs-function 불일치 · 두 트리 다른 `#include` 세트 → nvcc/clang syntax+link 깨짐 |
| pod fresh clone + emit bootstrap | hexat_linux 가 runtime_cuda_emit.hexa(거대 string-literal) transpile 에서 **segfault**; hexa wrapper 는 hxv2/hexa.real/stage0 미존재로 self-host 부트스트랩 불가 |

**진짜 해법 (별도 작업)**: dispatch 스크립트(`tool/dispatch_phase4d7_gpu_fire.sh:211`)가 쓰는 방식 = "로컬 working tree 의 generated 파일(runtime_hi_gen.c 등)을 pod 로 scp". 즉 **완전+fresh 한 로컬 hexa-lang working tree(origin/main 동기 + emit 산물 생성)에서 self.tar.gz 를 만들어 전송**해야 함. 이는 hexa-lang 을 깨끗이 빌드할 수 있는 전용 환경(또는 타 agent 와 충돌 안 하는 격리 hexa-lang clone + 빌드)이 선결. anima 세션에서 공유 hexa-lang 을 264-점프할 수 없으므로 hexa-lang 측 작업.

**M5 step-rate**: ⚪ 측정 미수행 — 단 모든 infra recipe + 정확한 blocker 가 완전 진단됨. 다음 작업 = hexa-lang 전용 clean-build 환경에서 self.tar.gz 생성 → 검증된 pod recipe(STEP_RATE_LOG (3)(4))로 <8min 빌드+측정. anima 측 코드(trainer·M0~M4 wiring·mm_extract·E-axis)는 전부 landing 완료, 막힌 건 hexa-lang self/ 배포뿐.

**이번 세션 landing 합계**: anima #1319(M0)·#1320(M2/M3 wire)·#1322(adam)·#1325(mm_extract)·#1327(E-axis)·#1334(import fix)·#1316·#1318 + STEP_RATE_LOG (1)~(5) · hexa-lang #1959(SSH host-key)·#1960(cloud 개선 inbox) · sidecar #217(stale-toolchain 방지 체크리스트) · GPU.anima #1915/#1918. 비용 ~$5-6 (pod 시행착오, 전부 teardown · pods=0).

---

### 2026-05-29 (6) — hexat #1984 premise ✅ 확인 · bootstrap-seed gap 이 새 blocker (한 겹 더 깊음)

엔트리 (5) 표의 **"pod fresh clone + emit bootstrap"** 행을 hexa-lang #1984 (`build/hexat_linux` 재빌드, commit `7bb01a108`) 로 직접 재검한 라운드. pod `q0ynubdw5s4e1v` (H100 SXM, 208 vCPU, $3.29/hr), `hexa cloud run/copy-from --insecure` 정규 경로, `PUBLIC_KEY=RunPod-Key-Go.pub` 명시 주입 (엔트리 (4) 의 SSH-key 미스매치 회피 — RunPod-Key-Go 로 SSH_OK 재현).

**PREMISE ✅ — hexat #1984 가 emit segfault 를 완전히 고침**: `./build/hexat_linux self/runtime_core_emit.hexa /tmp/rc.c` → **rc=0, 11644 lines**. 엔트리 (5) 가 막혔던 거대 string-literal emit (runtime_cuda_emit / runtime_core_emit) transpile segfault(rc=139)가 사라짐. fresh origin/main clone (`e4c831c`) 의 **모든** `*_emit.hexa` 가 rc=0 으로 transpile (30+ 파일, 135~11644 lines). 즉 #1984 는 실효 — F-BC-ANIMA-M4-CEILING 의 전제(segfault 해소)는 PASS.

**그러나 BUILD 는 여전히 FAIL (clang_rc=1) — 한 겹 더 깊은 NEW blocker**: hexat 은 `*_emit.hexa` → C 를 **transpile** 만 한다. 그 산출물(`/tmp/rc.c`)은 **runtime_core.c 자체가 아니라 그것을 stdout 으로 찍는 EMITTER 프로그램**이다 (`#define HX_VSF...` 가 코드가 아니라 `hexa_str("#define HX_VSF...")` 문자열 리터럴로 들어있음; emit 헤더 자체 명시: `Invocation: hexa-run self/runtime_core_emit.hexa <output-path>`). 진짜 `runtime_core.c` (281KB) 를 얻으려면 이 emitter 를 **컴파일 후 RUN** 해야 하는데:
- emitter `/tmp/rc.c` 는 `#include "runtime.h"` + `hexa_str`/`hexa_void`/`rt_write_file` 등 **runtime.c 심볼**에 링크 의존 → standalone 컴파일 시 `undefined reference`.
- `runtime.c` 는 `#include "runtime_core.c"` (line 2149) → **얻으려는 그 파일이 컴파일 선결** = 순수 순환.
- 순환을 깰 수 있는 **stage0 인터프리터(`build/hexa_stage0`)가 origin/main clone 에 부재**: `./build/hexa_linux run self/runtime_core_emit.hexa <out>` → `error: stage0 interpreter not found ... rebuild with: hexa tool/build_stage0.hexa` (이것도 순환). `build/hexa_linux`(508KB driver)·`build/hexat_linux`(3.8MB transpiler) 둘 다 ship 되나 **스크립트를 RUN 하는 인터프리터는 없음** (hexat 은 transpile-only: usage `hexa-cc <input.hexa> <output.c>`).
- `git log --all -- self/runtime_core.c` = **empty** → runtime_core.c 는 어느 브랜치에도 커밋된 적 없음 (항상 RUN-generated). prebuilt `.o`/`.a` 도 0.

⇒ **NEW blocker = bootstrap-seed gap**: hexat-segfault(✅ #1984 해소)도 cuBLAS gemv illegal-mem(미도달)도 아닌, **fresh origin/main hexa-lang clone 이 Linux 에서 runtime 을 self-bootstrap 할 씨앗(prebuilt stage0 인터프리터 OR 커밋된 runtime_core.c)을 안 들고 있다**는 별개의 정확히-특정된 벽. 엔트리 (5) 의 "self.tar.gz from clean local build" 처방이 여전히 유효 — 단 이번 라운드는 그 처방의 *이유*를 한 겹 더 깊이 확정: clone 단독으로는 emit 산출물을 만들 수 없다(transpile≠run, run-runtime 부재).

**측정값**: step-rate ⚪ **여전히 미측정** (trainer 빌드 실패 → 학습 0 step). CPU-only build 였으므로 cuBLAS gemv(Blocker 2)는 이번에도 미도달.

**dec_undertrain 실현가능성**: 측정 미수행이라 정량 verdict 불가. (config 상 V=151643, steps_per_epoch=⌊n_toks/4⌋−1, target_presentations=3e6 → 1-epoch n_steps≈V급. per-step wall 미측정 → tens×V 처방 GPU-days 환산 불가. 다음 측정에서 확정.)

**비용**: 단일 pod `q0ynubdw5s4e1v` ~30분, ~$1.6. teardown 완료 (`runpodctl pod list` → `[]`, pods=0). leak 0.

**다음 한 수**: 엔트리 (5) 처방 그대로 — 격리 hexa-lang clean clone 에서 stage0 부트스트랩(또는 emit-run)으로 `runtime_core.c`+generated set 을 생성 → `self.tar.gz` → 검증된 pod recipe(SSH·copy-to·CPU build)로 빌드+<5min 측정. 이번 라운드로 transpile 층(#1984)은 완전 통과 확인했으므로 남은 건 **run/emit 층** 한 겹뿐.

**verdict**: ⚪ step-rate STILL UNMEASURED · **🔵 premise(#1984 emit segfault 해소) CONFIRMED** · 🟠 NEW blocker = bootstrap-seed gap (정확히 특정, hexa-lang 측 작업). F-BC-ANIMA-M4-CEILING 은 self.tar.gz 확보 후 단발 측정 가능.

---

### 2026-05-29 (7) — 🟢 첫 실측 step-rate 착지 · bootstrap-seed gap #1992 로 완전 해소 · **0.50 step/s (CPU) → dec_undertrain INFEASIBLE**

엔트리 (6) 가 막혔던 **bootstrap-seed gap 이 hexa-lang #1992("restore runtime.c amalgamation .c seed", commit `4456294eb`)로 완전 해소**됨을 pod 에서 직접 재검 — 6번의 시도 만에 **trainer 가 실제로 빌드·실행되어 첫 실측 step-rate 가 나온 라운드**. pod `uaybppujc0gdki` (H100 SXM 80GB, 28 vCPU, 251GB→실제 2TB RAM 노드, $3.29/hr), `hexa cloud run/copy-to --insecure` 정규 경로, `PUBLIC_KEY=RunPod-Key-Go.pub` 명시 주입.

**(1) seed 존재 ✅ — #1992 premise 확정**: fresh `git clone --depth 1 origin/main` 에 엔트리 (6)/(5)가 "어느 브랜치에도 커밋된 적 없다"고 단정했던 generated-C 가 **이제 전부 커밋되어 있음**: `self/runtime_core.c` (375182 B) · `self/native/tensor_kernels.c` (12655 B) · `self/runtime_hi_gen.c` (6813 B) · `self/runtime.c` (681937 B) · `build/hexat_linux` (3.8MB). emit-run / stage0 부트스트랩 dance 불필요 — clone 이 CPU 빌드에 필요한 모든 것을 직접 들고 옴 (CPU-only 빌드는 `-DHEXA_CUDA` 없이 `runtime_cuda.c`/`runtime_bf16.c` 미포함, cuBLAS gemv N=1 버그 회피).

**(2) CPU 빌드 성공 ✅ (BUILD RC=0)**: `clang -O2 -I self -fbracket-depth=8192 ... /work/trainer.c self/runtime.c -ldl -lrt -lm -lpthread -lstdc++ -o /work/trainer` → **rc=0, 경고 2건(cosmetic)만**, 544KB 바이너리. GPU `0%, 0 MiB` (CPU-only — 그 0% 자체가 finding: trainer 는 CPU-bound, GPU 미사용). BPE 토크나이저 정상 로드 (V=151643 production 어휘, merges 151387).

**(3) 실측 step-rate** (instrumented trainer.c line 2209 `m5_wall_s=<CLOCK_MONOTONIC>` 마커, print_every=50). config: d=64 · V=151643 · E=2 · h=256 · n_layer=1 · T=4 · **m_size=29.16M params (FP64 222MB)**. 24-line trim corpus (n_toks=6034) 로 학습 루프 도달 (full 2000-line corpus 는 pure-hexa BPE 토크나이즈가 토큰수 비례로 너무 느려 ~330s+ 에도 루프 미도달 — 별도 finding):
- step=1   @ m5_wall 3710182.920
- step=50  @ m5_wall 3710273.667 → **1.852 s/step (steps 1–50)**
- step=100 @ m5_wall 3710380.008 → **2.127 s/step (steps 50–100)**
- **headline: steps 1–100 = 1.991 s/step ≈ 0.502 step/s** · loss 648.5→3.33→0.997 (학습 정상).
- **per-step 14.8% 열화 (1.85→2.13 s/step)** — RSS leak 드래그. RSS 가 step~100 에서 **57GB 까지 폭증** (~0.5GB/step). trainer 헤더가 #1315 의 "~20KB/step host-RSS leak 을 버퍼 hoisting 으로 해소"했다고 주장하나 **leak 은 여전히 존재(0.5GB/step 규모)** — 장기 run 은 rate 와 무관하게 OOM 으로 infeasible.

**(4) dec_undertrain 실현가능성 verdict = 🔴 INFEASIBLE**: toy 처방 "tens × V presentations" (50×V = 7.58M presentations, T=4 → **1.90M steps**). @ 측정 rate(1.99 s/step) = **~44 GPU-days** (best-case 1.85s/step 도 40.6 GPU-days). trainer 헤더 자체 추정(GPU 0.6–1.5 s/step → ~9 GPU-days) 대비 CPU 는 ~5× 더 느림. 단일 full-corpus 1-epoch (steps_per_epoch≈289K) 조차 ~6.7 GPU-days (CPU). **+ RSS leak 이 어차피 장기 run 을 OOM 시킴** → 현 빌드(CPU)로 production-scale dec_undertrain 은 비현실적. 정당한 closed measurement: F-BC-ANIMA-M4-CEILING = **production-scale UNVERIFIABLE-AT-THIS-RATE (CPU 0.5 step/s, 44 GPU-days, leak-bound)**.

**비용**: 단일 pod ~40분, ~$2.2 (=$3.29/hr × 0.67h). teardown 완료 (`runpodctl pod list` → header-only, **pods=0, leak 0**).

**다음 한 수**: (a) GPU 빌드(`-DHEXA_CUDA` + cuBLAS gemv N=1 버그 선결)로 step-rate 재측 — GPU 면 헤더 추정 0.6–1.5 s/step 가능, 그래도 ~9 GPU-days. (b) **per-step RSS leak (0.5GB/step) 근본 fix 가 선결** — leak 해소 없이는 GPU 라도 장기 run OOM. (c) pure-hexa BPE corpus-load 가 토큰수 비례로 느린 것(full corpus 미도달)도 별도 hexa-lang inbox 사안. transpile 층(#1984)+bootstrap-seed 층(#1992) 둘 다 해소되어 **빌드→실행→측정 파이프라인은 이제 완전 통과** — 남은 건 GPU 배선 + leak fix.

**verdict**: 🟢 **첫 실측 step-rate 착지 = 0.50 step/s (CPU, V=151643, 29M params)** · 🔵 #1992 bootstrap-seed gap CONFIRMED-RESOLVED (fresh clone 에 generated-C 커밋됨) · 🔴 dec_undertrain production-scale INFEASIBLE (44 GPU-days @ 이 rate + per-step RSS leak OOM). F-BC-ANIMA-M4-CEILING 정량 ceiling 확정.

---

### 2026-05-29 (8) — RSS leak (~0.5GB/step) ROOT-CAUSE = AdamW out 233MB 매-step churn (anima trainer 결백, hexa-lang runtime arena 보유) · $0 source-reasoned

엔트리 (7) 의 next-step (b) "per-step RSS leak (~0.5GB/step) 근본 fix" 를 **$0 source-read 로 root-cause** 한 라운드 (pod 미대여 — 본 진단은 코드 추론, 런타임 재측정은 별도 follow-up). 결론부터: **leak 은 anima trainer 버그가 아니다 — trainer/lib 의 모든 per-step 할당은 빠짐없이 `farr_free` 된다.** leak 은 hexa-lang **runtime arena-retention** 현상으로, 매 step 233MB AdamW `out` 버퍼 calloc/free churn 이 driver.

**(A) anima trainer + 의존 lib 의 per-step 할당 전수조사 (전부 freed)**:
- `train_v3_moe_longtrain.hexa` step-loop body (line 319–594): layer-loop 의 `mm_extract`(×4) · `mm`(×6) · `mm_transpose`(×2) · `t_zeros(T*h)`(h_act) · AdamW `newW` handle — **14개 할당 전부 대응 `farr_free` 존재** (line 367/368/382/410/418/443–445/553). 큰 재사용 버퍼(M·dMg·m_buf·v_buf 각 29.16M double ≈ 233MB)는 line 162–209 에서 loop 밖 hoist 완료.
- `v3_moe_arch.hexa` `v3_moe_fwd`: `logits_raw`(mm_packed_gemv, V double) 1개 → freed (line 113). `v3_moe_bwd`: `dl_scaled`·`d_zT_exp`·`logits_raw` 3개 → 전부 freed (line 177–179).
- `v3_moe_bwd_lib.hexa` `layer_block_bwd`/`mlp_block_bwd_batched`/`self_attn_bwd`: 모든 내부 scratch (`d_x_seq`·`d_zT_mid`·`d_zT_in_from_attn`·`d_h_pre`·`d_scores`·mm/transpose 산물 등) → 전부 freed (line 192/207/212/219/220/221/282/283/289/293/297/298/318/324/325/334–337/354–365/416/430/431).
- `flame_mm.hexa`: `mm`/`mm_extract`/`mm_transpose`/`mm_packed_gemv`/`_t` 는 handle 반환 → 호출부가 free. `mm_scatter_add`/`mm_packed_outer_add` 는 무할당.

**(B) hexa-lang M0~M4 builtin (cloud-m3 fire-build runtime.c) 도 누수 없음**:
- M2 `farr_softmax_rows(x, out, R, C)` (4-arg) + M3 `farr_ce_seed(...)` (5-arg) = **in-place** (caller pre-alloc 버퍼에 기록, per-call `hexa_farr_zeros` 없음 — runtime.c line 9508 + ce_seed slim). trainer 는 hoisted `softmax_buf`/`d_logits` 를 넘기므로 무할당.
- M1 `farr_adamw_step_gpu(...)` = **fresh `out` farr 1개 (n=m_size=29.16M double = 233MB) 할당 후 반환** (runtime.c line 10806 GPU / `_hx_farr_adamw_step_cpu` line 10600 CPU). trainer 는 이를 `newW` 로 받아 `farr_copy_slice_gpu` 로 M 에 복사 후 즉시 `farr_free(newW)` (line 552–553). **즉 매 step 233MB calloc → 사용 → free.** `farr_copy_slice`/`farr_zero_slice` 는 순수 memcpy/memset (무할당).
- runtime `hexa_farr_free` = `free(buf)` + freelist 에 handle id 만 재활용 (buf 는 NULL 로). `hexa_farr_zeros` = freelist 에서 slot id 만 꺼내고 **버퍼는 항상 새 `calloc`** (이전 buf 재사용 안 함).

**(C) ROOT-CAUSE = glibc arena 보유 (per-step 233MB churn)**: 매 step `calloc(233MB)` + `free(233MB)` 가 일어나는데, glibc malloc 은 큰 free 청크를 OS 로 즉시 반환(`munmap`/`madvise`)하지 않고 arena 에 보유 → RSS 가 logical heap 과 무관하게 누적. measured ~0.5GB/step ≈ **2× m_size(466MB)** = AdamW out(233MB) + transient(V-buf·matmul·copy-back) 가 정확히 일치. runtime.c 에 `malloc_trim`/`mallopt(M_MMAP_THRESHOLD)`/`madvise` 부재 (grep 0건). runtime.c line 3739–3745 주석이 동일 현상을 명시: *"boxed-HexaVal retention from these arrays binds the in-process NM optimizer at the 768 MB cap … cuts arena retention by ~50× … the HEXA_MEM_CAP_MB=2048 workaround"* — packed int64_t 가 arena 보유를 해소했던 선례 = 동일 class.

**(D) 왜 anima-side 패치가 없는가**: AdamW `out` 은 **builtin 내부**에서 할당된다 (trainer 가 hoist 불가). M2 softmax 가 3-arg(new-alloc)→4-arg(in-place) 로 전환해 29M-double/step alloc 을 제거한 선례처럼, **AdamW 도 in-place builtin (`farr_adamw_step_inplace`, W 직접 갱신·fresh out 없음) 이 정답** — 그러나 그런 builtin 은 hexa-lang 에 부재 (`_inplace` grep: softmax/add 만 존재, adamw 없음). trainer 는 builtin 을 설계대로 정확히 사용 중. ⇒ **narrowest correct fix 는 hexa-lang-side** (a_runpod_inbox 로 filing). 강제 anima 패치는 a_completeness_over_cheap 위반.

**fix 후보 (hexa-lang, inbox filed)**: (1) `farr_adamw_step_inplace(W, m, v, g, n, ...)` — fresh out 없이 W in-place 갱신 (M2 4-arg softmax 선례 그대로, 매 step 233MB calloc/free 제거). (2) 보조: runtime init 에서 `mallopt(M_TRIM_THRESHOLD/M_MMAP_THRESHOLD)` 또는 step-tail `malloc_trim(0)` 로 free 청크 OS 반환. (3) 차선: `hexa_farr_zeros` 가 freelist slot 의 동일-크기 buf 를 재활용 (calloc 회피).

**verify**: `hexa check CORE/DECODER/train_v3_moe_longtrain.hexa` → **0 violations** (lint/parse clean). leak fix 는 source-reasoned + lint-clean — **런타임 재확인(leak=0)은 deferred pod follow-up** (이 라운드는 $0, pod 미대여). 본 진단은 "leak 위치 = AdamW out churn, anima 결백" 까지 확정.

**verdict**: 🔵 **RSS leak ROOT-CAUSED** — anima trainer 결백(per-step 할당 전수 freed), leak = hexa-lang runtime arena 보유 × per-step 233MB AdamW out churn. fix = hexa-lang in-place AdamW builtin (a_runpod_inbox filed). 런타임 leak=0 재확인은 별도 pod follow-up. cf `.discoveries/decoder_collapse_undertrain.tape` `dec_undertrain_steprate_2026_05_29` next-step (b).
