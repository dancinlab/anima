# P9 EXEC pre-flight 묶음 3 (HF/cloud) — landed handoff

- date: 2026-05-03
- session_kind: BG subagent (preset friendly, AI-native, BR-NO-USER-VERBATIM)
- ω-cycle: 6-step single-pass
- silent-land marker: yes (state/markers/p9_pre3_hf_cloud_check_landed.marker)
- cap: 60min wall, $0.01 (HF API only)
- destructive: 0 net (K added → L removed, real repos untouched)
- migration: NONE — additive only

---

## §0 verdict (1-line)

**PARTIAL_PASS** — HF 측 4/4 GREEN, RunPod 측 1.5/2 (가용성 GREEN, 잔액 cap-gap PARTIAL)

| item | scope | verdict | gap |
|------|-------|---------|-----|
| K | HF upload mechanism | PASS | — |
| L | HF revoke mechanism | PASS | pod-side kill 미실증 (v3 launcher 기존 cover) |
| M | 6 repo write+admin scope | PASS | 5/6 inferred via org admin role (K/L 으로 1/6 empirical) |
| N | RunPod 9 H100 가용성 | PASS_WITH_TOPOLOGY_NOTE | maxGpuCount=8 → 2-pod 구성 필수 (구조적, gap 아님) |
| O | RunPod 잔액 + auto-charge | PARTIAL_GAP | 잔액 $339.82 < cap $1500 (gap $1160), auto-charge 상태 GraphQL 미노출 |

P9 EXEC Phase 0 entry: **HF 측 GREEN** / **RunPod 측 user 결정 필요** (top-up vs scope 축소)

---

## §1 K — HF savepoint upload mechanism

- 10KB dummy → `dancinlab/clm-v4-sft-stage1` `pre3_check/k_upload_test_dummy.bin`
- commit: a7e1814f… (2026-05-02 16:04 UTC)
- 8 sec, hf CLI 1.8.0, write-scope token
- LFS 라우팅 (10KB 도 LFS pointer 화)
- tree API 검증 PASS (size=10240, lfs.size=10240)
- json: state/p9_pre3_hf_cloud_check/K_hf_upload_test.json

## §2 L — ABORT mock (F2 fail → revoke)

- `hf repos delete-files dancinlab/clm-v4-sft-stage1 "pre3_check/k_upload_test_dummy.bin"`
- commit: 04e9a889… (2026-05-02 16:05 UTC)
- 1 sec, tree API 검증 404 (=delete OK)
- 4 fallback 문서화: delete-files / overwrite+commit / repos delete (extreme) / pod-side terminate
- pod kill 미실증: v3 launcher hardening IDLE_KILL_SEC=1800 으로 cover
- json: state/p9_pre3_hf_cloud_check/L_abort_mechanism.json

## §3 M — 6 repo permission verify

- token: `anima` displayName, role=`write`, created 2026-05-02 15:54 UTC
- user: dancinlife (Aiden Park, nerve011235@gmail.com)
- org: dancinlab, role=`admin`
- 6 repo 모두 GET /api/models/{repo} HTTP 200, private=true, disabled=false
- write+delete empirical proof: K+L on stage1 (1/6 empirical)
- 나머지 5 inferred via org admin role (안전 가정)
- json: state/p9_pre3_hf_cloud_check/M_hf_permission.json

## §4 N — RunPod 9 H100 가용성

### 핵심 발견: maxGpuCount=8

- H100 SXM 80GB HBM3 maxGpuCount=8 → 9-GPU single-pod **불가**
- 9 H100 = **최소 2 pod** 구성 필요 (8+1 권장)

### 가용성 (query time 2026-05-02 16:05 UTC)

| variant | mem | stock(1x) | stock(8x) | OD/hr(1x) | OD/hr(8x) | spot/hr(8x) |
|---------|-----|-----------|-----------|-----------|-----------|-------------|
| H100 SXM (HBM3) | 80GB | High | High | $2.69 | $21.52 | $12.00 |
| H100 NVL | 94GB | Low | — | $2.59 | — | — |
| H100 PCIe | 80GB | Low | — | $1.99 | — | — |

권장: **H100 SXM 80GB HBM3** (Stock=High 유일 + NVLink throughput)

### 4 topology 옵션

1. **8+1 (2 pod)** — primary 8x training + 1x sentinel/eval ← **권장**
2. 8+8 (2 pod, 16 H100) — burst headroom 원할 시
3. 4+4+1 (3 pod) — combo sweep 병렬
4. 9×1 (9 pod) — 최대 병렬 (orchestration 부담↑)

### region per-DC

- GraphQL `dataCenters` empty 반환 → us-east/us-west/eu-central per-region 측정 X
- 글로벌 Stock=High signal 만 활용 (RunPod 자동 라우팅)

### 24hr 가격

- 8+1 on-demand: **$24.21/hr → $581/24hr** ← 권장
- 8+1 spot: $13.50/hr → $324/24hr (interruption risk → SFT 비권장)

- json: state/p9_pre3_hf_cloud_check/N_runpod_h100_availability.json

## §5 O — RunPod 잔액 + auto-charge

### 잔액

- clientBalance: **$339.82** (prepaid)
- currentSpendPerHr: $3.09 (1 RUNNING pod = anima-alpha-reboot @ $2.99 H100 SXM + buffer)
- machineQuota: 0 (캡 미설정)

### cap-gap

- P9 EXEC S3 worst-case: $1500
- gap: **−$1160.18**
- verdict: **BALANCE_INSUFFICIENT_FOR_S3_WORST_CASE**

### 3 remediation 옵션

1. **manual top-up to $1500** (gap +$1160) — RunPod 콘솔 ← 권장
2. scope 축소 24hr 8+1 → $581 (잔액 부족, 안전마진 X)
3. scope 축소 12hr 8+1 → $290.52 (잔액 OK, 안전마진 $49.30)

### auto-charge

- GraphQL `myself` 측 autoChargeEnabled / paymentMethodOnFile 미노출
- console (https://runpod.io/console/user/billing) 측 manual 확인 필요

### spending limit

- API 측 hard cap 없음 — prepaid 잔액 자체가 de-facto cap

- json: state/p9_pre3_hf_cloud_check/O_runpod_budget.json

---

## §6 user 결정 필요 (Phase 0 entry 전)

1. **RunPod top-up** — $1500 cap 위해 +$1160 charge (or scope 축소 결정)
2. **auto-charge state 확인** — RunPod 콘솔 manual (GraphQL 측 미확인)
3. **9-H100 topology 선택** — 8+1 (권장) vs 9×1 (병렬↑) vs 4+4+1 (combo sweep)

---

## §7 cost ledger

| item | est | actual |
|------|-----|--------|
| K (HF upload) | $0.001 | $0 (HF free tier) |
| L (HF delete) | $0.0001 | $0 |
| M (whoami query) | $0 | $0 |
| N (RunPod query) | $0 | $0 |
| O (RunPod query) | $0 | $0 |
| **total** | **$0.001** | **$0** |

cap $0.01 PASS (실제 $0)

---

## §8 raw 10 caveats (전체)

- K: 10KB dummy LFS-routed (production checkpoint 동일 path); concurrent upload 미테스트; integrity SHA 별도 미확인
- L: pod-side kill 미실증 (v3 launcher 의존); F2 trigger logic 본 preflight scope 외; git history 측 deleted file 보존 (forensics 용도)
- M: 5/6 repo write 측 inferred via admin role (K/L 만 empirical 1/6); fine-grained per-repo scope 없음 (HF token model 측 org-wide)
- N: 9-GPU single-pod 구조적 불가 (maxGpuCount=8); region per-DC breakdown GraphQL 미지원; Stock=High 측 query 시점 보장만 (EXEC 시점 보장 X)
- O: GraphQL 측 autoChargeEnabled 미노출; spending hard cap API 측 없음 (prepaid 잔액 = de-facto cap); $339.82 < $1500 worst-case → user top-up 결정 필요

---

## §9 marker + JSON SSOT

- handoff: `anima/docs/p9_pre3_hf_cloud_check_landed_2026_05_03.ai.md` (이 파일)
- marker: `anima/state/markers/p9_pre3_hf_cloud_check_landed.marker`
- per-item JSON: `anima/state/p9_pre3_hf_cloud_check/{K,L,M,N,O}_*.json`

policy: BR-NO-USER-VERBATIM / raw 15 / migration 0 / additive only
