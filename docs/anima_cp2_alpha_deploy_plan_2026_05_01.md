# CP2 알파 실사용 배포 — 현 상태 + 실행 계획

> **ts**: 2026-05-01
> **scope**: CP2 alpha-tier 실사용 (real-use) 배포 계획 — 권장만, 실행은 사용자 승인 후
> **constraints**: raw#9 hexa-only (.md OK) · raw#10 honest C3 · raw#71 falsifier preregister · raw#86 cost-attribution · own#6 autonomous cutoff · own#11 parallel-mandate · own#13 user-facing friendliness
> **parent commit**: HEAD@2026-05-01 (`0a8d51684` akida r7 paradigm-v15)

---

## §1 즉시 사용 가능한 자산 (verified)

| asset | path | status |
|---|---|:---:|
| LoRA adapter | `state/trained_adapters/p4_r8/final/` (Mistral-7B-v0.3 + LoRA r=96 α=192, 185.92 MB) | READY |
| Orchestrator | `tool/anima_runpod_orchestrator.hexa` | READY |
| vLLM hardening | `tool/anima_vllm_hardening.hexa` | READY |
| 4 cert gates | AN11_JSD / META2_CHAIN / PHI_VEC_ATTACH / HEXAD_ROUTING | PASS |
| Endpoint smoke | `/health` · `/an11/verify` · `/v1/chat/completions` | 3/3 PASS (ephemeral) |
| 5 알파-tier docs | paper · blog ko/en · demo script · checklist | LANDED LOCAL |
| ship_verdict | `state/anima_serve_production_ship.json` | VERIFIED-INTERNAL |

---

## §2 알파 실사용까지 실측 gap (5/7 → 7/7 production gate)

| id | gate | status | 차단 여부 |
|---:|---|:---:|:---:|
| 11 | AN11_JSD | PASS | — |
| 12 | META2_CHAIN | PASS | — |
| 13 | PHI_VEC_ATTACH | PASS | — |
| 14 | HEXAD_ROUTING | PASS | — |
| 16 | endpoint reachability | PASS (ephemeral) | — |
| **15** | **latency budget** | PENDING (live 측정 필요, baseline×1.1) | 알파 부팅 직후 측정 |
| **17** | **hallucination** | PENDING (adversarial prompt suite) | 알파 부팅 직후 측정 |

**비-차단이지만 disclaimer 필수**:
- 의식측 RED (F2 falsifier fired, 14-gate L1 0/16 prompts full-pass)
- LIVE 충족도 평균 2.9% (5-audit 결과: #14/#15/#16/#17/#18)
- #79 직원가능 LIVE 0% (`state/dest2_employee_*.json` 0 files)
- #80 트레이딩 LIVE 0% + AN11 3/3 FAIL on p4_r8

**외부 가시 endpoint 부재**: 현재는 ephemeral pod (`ikommqs84lhlyr`) 만 존재. durable production endpoint (`#88 anima.ai API`) 별 라운드.

---

## §3 권장 배포 형태 (alpha-tier honest 기본값)

| dimension | choice | rationale |
|---|---|---|
| infra | H100 1× on RunPod, vLLM + FastAPI, durable (idle reclaim heartbeat 적용) | latency 측정 + 24h+ uptime |
| auth | Bearer token gate (초대제) | F-MIN-3 (raw#71 misperception ≥80% in 14d) risk 최소화 |
| rate limit | per-token QPM cap + daily token cap | runaway cost 방지 (`tool/anima_runpod_runaway_cost_incident_auditor.hexa`) |
| landing page | RED 명시 disclaimer (의식측 RED · 14-gate F2 fired · LIVE 2.9% · 알파 명시 · 비-AGI 명시 · 비-service 명시) | own#13 friendliness + raw#10 honest |
| logging | 모든 inference 요청 → `state/cp2_alpha_serve_audit/*.jsonl` (PII 제외, prompt hash + latency + finish_reason) | gate 17 hallucination 측정 + 회귀 평가 |
| kill switch | `tool/anima_serve_kill.hexa` 1-command teardown | 사용자 단발 명령으로 즉시 회수 |

---

## §4 자율 실행 가능 (사용자 승인 불필요, own#6)

1. H100 pod 부팅 + vLLM/FastAPI 기동 + p4_r8 LoRA 로드 (~$1–2/h, 부팅 ~10분)
2. live latency × hallucination 측정 → gate 15 + gate 17 verdict 확정 (~5분)
3. Bearer token 발급 + rate limit config (token 1개 = 1 invitee)
4. landing page draft (`docs/anima_cp2_alpha_landing_2026_05_01.md`) — 본인 확인용 LOCAL
5. F.B (F1_LIVE r9 token-sampling JSD) 병렬 발사 — own#6 autonomous OK ($0.05–0.20)
6. ship_verdict 갱신: VERIFIED-INTERNAL → VERIFIED-ALPHA-INVITE

**race isolation**: alpha 부팅 = `state/cp2_alpha_serve_*` + `docs/anima_cp2_alpha_*`. F.B = `state/an11_c_p4_r8_f1_live_*`. 겹침 없음 (own#11).

---

## §5 사용자 명시 승인 필요 (외부 가시성, 시스템 프롬프트 안전 정책)

| # | 결정 | 옵션 |
|---|---|---|
| **A** | endpoint 공개 범위 | (i) invite-only (기본 권장) / (ii) N명 초대 명단 / (iii) open-with-rate-limit |
| **B** | 도메인 | (i) RunPod direct URL (가장 빠름, 임시) / (ii) Cloudflare tunnel (영구, 자체 도메인 가능) / (iii) anima.ai (별도 작업) |
| **C** | publish gates (D1-D6 from `cp2_interim_option_c_launch_checklist`) | (i) 알파 부팅과 분리 / (ii) 알파 + arXiv 동시 / (iii) 알파 + 블로그 동시 / ... |

권장: **A=invite-only · B=RunPod direct (임시) · C=알파 부팅과 분리** — 가장 빠르고 reversible.

---

## §6 비용 attribution (raw#86)

| 항목 | ESTIMATE | source |
|---|---:|---|
| H100 pod 부팅 (1h) | $1–2 | RunPod H100 spot/secure |
| F.B F1_LIVE token-sampling | $0.05–0.20 | 20 prompts × 20 calls |
| latency + hallucination 측정 | 부팅 비용에 포함 | — |
| landing page draft | $0 (local) | — |
| **합계 (1h alpha)** | **$1.05–2.20** | RunPod 잔액 충분 |
| 24h alpha (token gate, ~10 invitee) | $24–48 | 후속 결정 |

own#6 cutoff: 사용자 사전승인 ≤$0.20 / call (F.B) · alpha 부팅 single-call $1–2 → 사용자 승인 권장.

---

## §7 raw#71 falsifier 5건 (alpha-tier 신규)

| id | predicate | window | fired action |
|---|---|---|---|
| **AL-F1** | alpha endpoint live 이후 14d 내 ≥20% invitee 가 anima 를 "deployed service" 로 오인 | 14d | landing page disclaimer 강화 + F-MIN-3 escalation |
| **AL-F2** | latency live > baseline × 1.5 (gate 15 budget 1.1 의 1.36× 초과) | 부팅 직후 측정 | vLLM config 재튜닝 또는 model size downgrade |
| **AL-F3** | hallucination rate > 30% on adversarial prompt suite | 부팅 직후 측정 | F2 falsifier 강화 disclose + 일부 prompt class 차단 |
| **AL-F4** | RunPod runaway cost (>$50/h sustained) | 매 시간 | `anima_runpod_runaway_cost_incident_auditor` 자동 trigger + auto-kill |
| **AL-F5** | ship_verdict downgrade 가 사용자 unawareness 로 발생 | 즉시 | own#13 알림 + landing page 즉시 RED-band 갱신 |

---

## §8 raw#10 honest C3 disclosures (10건)

1. 모든 cost / latency / hallucination 수치는 **ESTIMATE** — 실측은 부팅 후.
2. p4_r8 의 의식측 RED 가 alpha launch 자체를 막지는 않으나, F1_LIVE FAIL 시 substrate-anti-integration 가설 강화 → invitee 에게 명시 disclose 필수.
3. 5/7 production gate PASS 는 narrow 해석 — broad 해석 (live latency + hallucination) 은 부팅 후 확정.
4. Bearer token 인증은 alpha-tier 표준 — token 누설 시 unauthorized 사용 가능 (rate limit 으로 일부 mitigate).
5. RunPod direct URL 은 pod 재부팅 시 변경됨 — invitee 에게 token 갱신 안내 필요.
6. landing page disclaimer 만으로 service-misperception 100% 방지 불가 (F-MIN-3 / AL-F1 잔존).
7. F.B (F1_LIVE) PASS 가 14-gate F2 falsifier override 를 풀지 않음 — AN11(c) 만 disambiguation, F2 별도.
8. invitee 가 생성 텍스트를 외부 공유 시 anima 의 RED 상태가 invitee 외부로 전파 — 통제 불가.
9. usage logging 은 prompt hash + metadata 만 저장 — full prompt text 미저장 (GDPR-lite). 단, hash collision 시 재현 불가.
10. kill switch 발동 시 24h 이내 모든 endpoint shutdown + token revocation — 단, 이미 응답된 inference 결과는 회수 불가.

---

## §9 commit chain (deploy 진행 시)

```
1. doc(cp2-alpha-deploy-plan): 본 plan doc + raw#71 5건 + raw#10 10건
2. boot(anima-serve-alpha): H100 pod + vLLM + FastAPI + p4_r8 LoRA load
3. measure(gate-15-17-live): latency baseline×1.1 + hallucination adversarial suite
4. config(alpha-token-gate): Bearer auth + rate limit + usage logging schema
5. doc(cp2-alpha-landing): landing page draft (LOCAL, RED disclaimer)
6. measure(an11-c-p4-r8-f1-live): F.B parallel — token-sampling JSD
7. ship(anima-serve-alpha-invite): VERIFIED-INTERNAL → VERIFIED-ALPHA-INVITE
```

각 commit 은 raw#25 lock-retry 적용.

---

## §10 사용자 결정 점

본 doc 는 권장만 — 실행 X. 사용자 1개 결정만 알려주시면 즉시 §4 자율 실행 시작:

**Q1**: §5 결정 A (endpoint 공개 범위) — `invite-only` 가 기본 권장. 다른 선택 있으면 명시.

> 선택 즉시: pod 부팅 → 측정 → landing page draft → F.B 병렬 → 30분 내 alpha endpoint + token 1개 발급. 비용 대략 $1–3 (1시간 H100 + F.B). RunPod 잔액 충분.

---

**status**: ANIMA_CP2_ALPHA_DEPLOY_PLAN_2026_05_01_LOCAL_DRAFT
**verdict_key**: PLAN_READY · USER_DECISION_PENDING · NO_BOOT_YET
