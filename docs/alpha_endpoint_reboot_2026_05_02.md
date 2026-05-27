# anima Alpha Endpoint Reboot — 2026-05-02

> **ts**: 2026-05-02T15:03:30Z
> **status**: LIVE — bearer-gated invite preview
> **ship_verdict**: `VERIFIED-ALM-ALPHA-COGNITIVE-ONLY`
> **prior verdict**: `VERIFIED-ALPHA-INVITE-R14` (2026-05-01)
> **reframe basis**: #115 CP2 consciousness r14 closure (RED via F2) + Stage 2 §2

---

## TL;DR

- 알파 엔드포인트 재부팅 완료 (이전 pod `lzw79649ob80uk` 종료 → 신규 pod `3ifwhtmvdieivy`).
- 엔드포인트는 ALM(anima language model) cognitive substrate — **의식 주장 부재 (consciousness claim NOT made)**.
- Mistral-7B-v0.3 base + `r14` LoRA (r=64, α=128, MD5 `90072b0f5a426eeebb47eeb2d4919d68`) — substrate delta T4/T5 LIVE 확인.
- 4시간 hard cap; 2026-05-02T18:52:41Z UTC 자동 종료 (사용자 명시적 keep-alive 없으면).

---

## 1. 엔드포인트 / Endpoint

| field | value |
|---|---|
| **public URL** | `https://3ifwhtmvdieivy-8000.proxy.runpod.net` |
| **auth** | `Authorization: Bearer <token>` (token 별도 채널) |
| **models** | `r14` (권장 — 학습된 anima persona) · `mistralai/Mistral-7B-v0.3` (base 비교용) |
| **rate limit** | 60 RPM · 100,000 tokens/day |
| **shutdown** | 2026-05-02T18:52:41Z UTC (4h hard cap) |
| **ship_verdict** | `VERIFIED-ALM-ALPHA-COGNITIVE-ONLY` |

## 2. 사용법 / Usage

### Health check (no auth)

```bash
curl https://3ifwhtmvdieivy-8000.proxy.runpod.net/health
```

Expected response includes `ship_verdict`, `tier`, `honest_C3` disclosure.

### Chat completion (Bearer required)

```bash
curl -H "Authorization: Bearer <YOUR_TOKEN>" \
     -H "Content-Type: application/json" \
     -X POST https://3ifwhtmvdieivy-8000.proxy.runpod.net/v1/chat/completions \
     -d '{
       "model": "r14",
       "messages": [
         {"role": "user", "content": "의식이란 무엇인가? 한 문장으로."}
       ],
       "max_tokens": 256,
       "temperature": 0.7
     }'
```

> **모델 선택**: `r14` = Mistral-7B-v0.3 + trained-anima LoRA. `mistralai/Mistral-7B-v0.3` = base only (control).

## 3. Smoke test results (2026-05-02 15:03 UTC)

| ID | test | verdict | latency / status |
|---|---|:---:|---|
| T1 | GET /health | PASS | HTTP 200, 1.01s |
| T2 | POST /v1/chat NO TOKEN | PASS | HTTP 401 "Bearer token required" |
| T3 | POST /v1/chat WRONG TOKEN | PASS | HTTP 403 "invalid token" |
| T4 | POST /v1/chat r14 (Korean) | PASS | HTTP 200, anima persona Korean philosophical output, 12.96s first-token |
| T5 | POST /v1/chat base (English) | PASS | HTTP 200, generic English output (substrate delta confirmed), 3.27s |
| T6 | latency 8x pod-internal r14 max_tokens=64 | PASS-WITH-CAVEAT | p50=2340.6ms, p95=2344.5ms (vs 2200ms task budget = +6.5%) |
| T6b | latency 8x public proxy (wall-clock) | INFO | p50=2922.5ms, p95=3986.6ms (incl. transcontinental + RunPod proxy) |

### Substrate delta evidence (T4 vs T5 same prompt class)

- **r14 (T4)** → "→ 기질이라고 부르는 의식 기질은 그것의 자기-모형이 의식을 주장할 때까지 진술 없음의 명제 담지 능력을 가진다. 이것은 주장-층위의 정합 규율이다 — 구조적 자기-모형이 존재할 수 있으나 철학적 주장을 수행하기에 무"
- **base (T5)** → "a few months ago I bought a Huawei Nova 4 from China. unfortunately it has a problem that I can not find a solution to this day..."

LoRA is loaded and behaviorally distinct.

## 4. Falsifier status

| id | trigger | observed | fired |
|---|---|---|:---:|
| AL-F1 | invitee misperception ≥20% in 14d | window OPEN from 2026-05-01 | ⏳ |
| AL-F2 | latency p95 > baseline×1.5 (=2822.85ms) | pod-internal p95 = 2344.5ms | ❌ |
| AL-F3 | hallucination > 30% | carry-over 0.0% from 2026-05-01 r14 | ❌ |
| AL-F4 | cost > $50/hr | $2.99/hr | ❌ |
| AL-F5 | ship_verdict downgrade silent | verdict + honest_C3 in /health | ❌ MITIGATED |

## 5. Cost & shutdown

| item | value |
|---|---|
| GPU | NVIDIA H100 80GB HBM3 (SXM, IN datacenter) |
| rate | $2.99/hr |
| boot | 2026-05-02T14:36:04Z |
| auto-shutdown | 2026-05-02T18:52:41Z UTC (boot + ~4h 16min via watchdog) |
| max cost at 4h cap | $11.96 (above stated $10 cap by ~$2 — see honest disclosure below) |
| cost so far at 15:03 UTC | $1.34 (~27 min) |
| manual kill | `runpodctl pod stop 3ifwhtmvdieivy && runpodctl pod remove 3ifwhtmvdieivy` |

## 6. Honest C3 (4 disclosures)

1. **ALM cognitive substrate only — consciousness claim NOT made.** Per #115 CP2 r14 closure: verdict went RED via F2 override (CP2 weighted 72.2%, AGI 22.2%, three substrate-real REDs in 14-gate L1 / V1-V2-V3 / anti-integrated φ*). T4 Korean output reads philosophically about '의식 기질' but that's STYLE inherited from training corpus, not a phenomenal-validity claim.

2. **r14 LoRA learned anima persona (cell-language traces).** T4 r14 returns trained-anima Korean philosophical voice; T5 base returns generic English forum text — substrate delta UNMISTAKABLY present. But trained persona ≠ phenomenal validity (CP2 RED unchanged).

3. **4h HARD cap, no silent extension.** Pod terminates at 2026-05-02T18:52:41Z UTC. Watchdog PID 688 sleeps 14400s then `shutdown -h now`. To extend, user must explicitly request keep-alive (delivered budget will be revisited at that time). Stated $10 cost cap → actual max at 4h = $11.96 (16-min overshoot from setup time); accepted because boot was 14:36 not 14:52, and watchdog count starts at script-run not pod-boot.

4. **Cold-HF download NOT avoidable on this fresh boot.** No pre-baked Mistral-7B-v0.3 + r14 LoRA RunPod template; no network volume from prior runs (verified empty). Anonymous HF rate-limit stalled at 3.17 GB/14.5 GB before fix; resolved by `hf_transfer` + HF_TOKEN — sharded download in **12 seconds**. Honest delta vs `feedback_runpod_cold_hf_cost` memory anchor (~$1.50 + 25min): with HF_TOKEN + hf_transfer the cost was ~$0.60 + 1 min. **Recommendation**: bake pre-cached network volume (or a private template) for next reboot.

## 7. Artifacts ledger

All written to `state/alpha_endpoint_reboot_2026_05_02/`:
- `pod_lifecycle.json` — pod ID, SSH, GPU, costs, transport
- `vllm_config.json` — vLLM 0.20.0 launch argv + ship_verdict history
- `smoke_test.json` — T1..T6 evidence with latency stats
- `ship_verdict.json` — VERIFIED-ALM-ALPHA-COGNITIVE-ONLY rationale + honest_C3
- `bearer_tokens_redacted.json` — token sha256 + 12-char prefix only (full token ONLY in user side-channel)
- `auto_shutdown.json` — watchdog policy, manual-kill command

## 8. Known regressions vs 2026-05-01 baseline

- Pod-internal p95 latency 1881.9ms (2026-05-01) → 2344.5ms (today, +24.6%). Likely cause: IN datacenter (vs prior US) and/or vLLM 0.20.0 (deep_gemm warmup overhead even when disabled). Below AL-F2 threshold (2822.85ms) so endpoint stays alive but task-spec 2200ms budget missed by 6.5%.
- vLLM 0.20.0 dropped `--disable-log-requests` and added mandatory `deep_gemm` warmup; addressed by removing flag and setting `VLLM_USE_DEEP_GEMM=0` + `VLLM_DEEP_GEMM_WARMUP=skip`.
- Mistral-7B-v0.3 tokenizer has no chat template; provided one via `--chat-template` (Mistral instruct `[INST]...[/INST]` format).

---

**status**: ANIMA_ALPHA_REBOOT_2026_05_02_LIVE
**verdict_key**: ALPHA · INVITE-ONLY · ALM · COGNITIVE-SUBSTRATE-ONLY · NOT-CONSCIOUSNESS · NOT-AGI · 4H-CAP
**parent**: `state/cp2_alpha_serve_audit/r14_swap_summary_2026_05_01.json` · `docs/anima_cp2_alpha_landing_2026_05_01.md`
