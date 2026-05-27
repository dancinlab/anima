# AXIS_MAP-FAN BUG_POSTMORTEM E OOM addendum (LangBalancedSampler GPU mem leak, PR #211 stack)

작성일: 2026-05-23 KST
스택: PR #211 (`HEXAD/V3/AXIS_MAP_BUG_POSTMORTEM.md` — env-var-concat saga) → 본 addendum
도메인: HEXAD/PURE (V3 saga rebrand)

---

## § Context

PR #211 은 7-axis AXIS_MAP-FAN fan-out (commit `df3e8e06e`, 2026-05-23 14:10 KST) 에서 발생한 caller-side env-var-concat anti-pattern (`P21H_STEPS="5000 P21H_BSZ=2 ..."` single-quoted single-string) 을 documentation 화 했다. 본 postmortem 의 사이클 1 redispatch (22:21 KST 시작) 에서 4개 fresh pod 가 올바른 inline env var 로 재발사되었고, A/B/F 결과는 이미 회수되어 있었다. 본 addendum 의 범위는 **cycle 1 redispatch 의 E axis (`P21H_LANG_BALANCED=1`) 단독 OOM crash** 다.

- E pod: `a5qud7f6g10kup` (p21h-v3-qwen, 1× A100 SXM 80 GB)
- 22:21 KST 발사 → 23:11 KST `runpodctl remove pod a5qud7f6g10kup` 강제종료 → 23:13 KST 사이클 1 종결
- training 시작 직후 (분 단위) CUDA OOM, no result.json 산출

---

## § Symptom

`dispatch.log` 의 verbatim OOM (총 21회 반복 — `tail -2 train.log` polling 이 OOM 루프를 그대로 capture):

```
[train-P21H] torch.OutOfMemoryError: CUDA out of memory. Tried to allocate 18.00 MiB. GPU 0 has a total capacity of 79.25 GiB of which 15.75 MiB is free. Including non-PyTorch memory, this process has 9.92 GiB memory in use. Of the allocated memory 9.41 GiB is allocated by PyTorch, and 9.30 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.
```

`nvidia-smi` 가독 요약 (kill 시점):

- Total: 79.25 GiB (A100 SXM 80 GB)
- Free: **15.75 MiB**
- Process(PyTorch): 9.92 GiB (allocated 9.41 GiB + reserved 9.30 MiB)
- **Unaccounted: ~70 GiB** (78 GB total − 15.75 MiB free − 9.92 GiB PyTorch ≈ 60 GiB outside PyTorch caching allocator)
- GPU util: 0% (process zombie 상태에서 메모리만 점유)

dispatcher 측 `dispatch.log` (18112 bytes) 의 90% 이상이 OOM 메시지 21회 반복. `tail -2 train.log` 폴링이 동일 OOM line 을 매 poll 마다 capture 했고, dispatcher 는 result.json 미생성 / heartbeat 정상 (process 살아있음, OOM exception 만 무한루프) 으로 자동 재기동 / 조기 종료 트리거에 걸리지 않았다.

---

## § Root cause hypothesis (LangBalancedSampler GPU mem 누수)

E axis 의 unique flag 는 `P21H_LANG_BALANCED=1`. 이는 `train_p21h_v3.py` 의 `LangBalancedSampler` 를 활성화하며, 5개 언어 (en + ko + zh + ru + ja) wiki corpus segment 를 round-robin 으로 batch 에 공급한다. `P21H_WIKI_TARGET_MB_PER_LANG=10` 설정이므로 언어당 10 MB.

PyTorch allocator 가 점유한 9.41 GiB 는 model weights (3B Qwen base ≈ 6 GB BF16) + optimizer state (AdamW 2× = ~3 GB) 로 설명되며 **leak 의 주체가 아니다**. 누락된 60 GiB 는 PyTorch caching allocator 바깥, 즉 raw CUDA allocation 으로 잡혀 있다.

가설: LangBalancedSampler 가 per-lang corpus segment 를 GPU resident 상태로 유지한 채 round-robin index 만 회전시키는 구조이며, 매 epoch step 마다 새로운 segment view 가 free 되지 않고 누적된다.

- 5 langs × 10 MB = 50 MB / round-robin step
- 60 GiB ÷ 50 MB ≈ **1,200 step 누적 후 임계 도달**
- A100 80 GB 의 free 15.75 MiB 는 "18 MiB 할당 시도 실패" 와 정확히 일치 — 가설과 부합

이 가설은 9.41 GiB allocated by PyTorch ≪ 70 GiB GPU occupied 의 불일치로 보강된다 (PyTorch allocator 외부에서 leaking).

---

## § Forensic artifacts inventory

경로: `/Users/ghost/core/anima/HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21H_axis_E/`

| 파일 | 크기 | 비고 |
|---|---|---|
| `dispatch.log` | 18112 B | OOM error × 21 회 반복 (`tail -2 train.log` polling capture) |
| `multi_wiki_source.json` | 907 B | 5-lang wiki corpus 메타 (en/ko/zh/ru/ja) |
| `pod_id.txt` | 15 B | `a5qud7f6g10kup` |
| `result.json` | **부재** | training 산출 0 (early OOM crash) |

PR #211 의 `.envbug` 디렉토리 패밀리와는 별개 — 본 사례는 env-var 가 올바르게 전달된 후 runtime memory leak.

---

## § Cost

- 발사: 22:21 KST → kill: 23:11 KST → ~50 분 wall
- 단가: A100 SXM 80 GB ≈ $1.49/hr (RunPod community)
- **sunk: ~$1.10**
- 산출물: 0 (no result.json, no ckpt, no metric)

---

## § Fix ranking (g0 단순성 기준)

### (a) **LangBalancedSampler CPU-side index, lazy GPU transfer per batch** — 권장 fix

- per-lang corpus segment 를 CPU host memory 에 유지
- round-robin index 회전은 CPU 측에서, 현재 batch 에 해당하는 lang segment 만 `.to(device)` 로 GPU 이동
- batch 종료 시 reference drop → PyTorch caching allocator 가 회수
- 누수 패턴 자체를 제거
- 변경 위치: `train_p21h_v3.py` `LangBalancedSampler` 클래스 (sampler 가 Python 측이면 single-line tensor.to(device) 위치 조정으로 충분)

### (b) `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`

- OOM 메시지가 직접 제안하는 환경변수
- fragmentation 완화는 가능하나, 실제 leak (allocator 외부 누적) 은 해결하지 못함
- mitigation 일 뿐 fix 가 아님

### (c) `P21H_WIKI_TARGET_MB_PER_LANG` 10 → 2 축소

- per-lang resident size 감소 (50 MB/step → 10 MB/step)
- 임계 도달 step 을 ~6,000 step 으로 연기할 뿐, leak pattern 자체는 잔존
- Band-Aid

---

## § Recommendation

**(a) LangBalancedSampler patch 가 적용되기 전까지 E axis 재발사 금지.**

- (b) / (c) 는 진단 정보를 가리는 부작용이 있으므로 사용하지 말 것
- patch 작업은 `train_p21h_v3.py` LangBalancedSampler 한 군데에서 끝나는 mechanical fix 로 추정됨
- patch 후 small-scale smoke (e.g. `P21H_STEPS=500`) 로 GPU mem 곡선이 평탄한지 먼저 검증한 뒤 full re-fire

---

## § Cross-reference

| PR | 범위 | 실패 모드 |
|---|---|---|
| #204 | dispatcher CALLER WARNING block 추가 | caller-side env-var-concat 의 조기 발견 |
| #211 | env-var-concat anti-pattern 사가 documentation | 7-axis fan-out 발사 시점 argparse rejection |
| **본 PR** | **E OOM addendum** | **cycle 1 redispatch 의 runtime CUDA OOM (LangBalancedSampler leak)** |

본 addendum 과 PR #204 / #211 의 공통점은 dispatcher 동일성뿐이며, 실패 모드는 caller-side (env-var) vs runtime (memory) 로 직교한다.
