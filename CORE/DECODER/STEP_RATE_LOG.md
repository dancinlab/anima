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
