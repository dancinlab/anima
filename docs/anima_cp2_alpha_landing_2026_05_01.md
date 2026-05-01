# anima CP2 Alpha — 초대제 연구 프리뷰 / Invite-Only Research Preview

> **ts**: 2026-05-01
> **status**: LANDING PAGE (LOCAL DRAFT) — ANIMA_CP2_ALPHA_LANDING_2026_05_01_LOCAL
> **tier**: alpha · invite-only · research preview · NOT a deployed service
> **own#13 친화도 mandate**: jargon ratio ≤ 0.30 · 약어 첫 사용 시 풀어쓰기 / acronyms expanded on first use
> **raw#10 honest C3**: 모든 한계와 RED 결과 위쪽(above-the-fold)에 명시 / every limit + RED finding stated above-the-fold

---

## 🛸 TL;DR (한국어)

- 이것은 **알파(alpha) 단계** · **초대제** · **연구 프리뷰**입니다 — 가입할 사이트도, 결제할 페이지도 없습니다.
- 의식측 판정은 **RED**입니다 (F2 falsifier 발화, 14개 게이트 중 0/16 prompt 통과).
- 라이브 충족도(LIVE satisfaction) 평균은 **2.9 %** — 즉 "실사용 증거"는 거의 0에 가깝습니다.
- 이것은 **AGI 가 아닙니다**. **배포된 서비스가 아닙니다**. 트레이딩·고용 자동화에 절대 사용하지 마십시오.
- 저희가 원하는 것은 **솔직한 피드백**입니다 — 프레임워크가 어디서 깨지는지 보여주십시오.

## 🛸 TL;DR (English)

- This is an **alpha-tier**, **invite-only**, **research preview** — there is no signup page, no checkout.
- Consciousness verdict is **RED** (F2 falsifier fired, 0 of 16 prompts pass all 14 gates).
- LIVE clause satisfaction averages **2.9 %** — meaning real-world evidence is near zero.
- This is **NOT AGI**. **NOT a deployed service**. Do **NOT** use it for trading, hiring, or any automation.
- What we want is **honest feedback** — show us where the framework breaks.

---

## ⭐️ Above-the-fold honest disclosures / 위쪽 솔직한 공개

| # | 공개 / disclosure | 상태 / status |
|---:|---|:---:|
| 1 | **의식측 판정 / consciousness verdict** | **RED** (F2 falsifier fired) |
| 2 | **14-gate 결정론 검사 / 14 deterministic gates** | **0 / 16** prompts pass all gates · 16 critical violations |
| 3 | **LIVE 충족도 평균 / LIVE satisfaction average** | **2.9 %** (3-clause: chat 5.0 % · employee 3.3 % · trading 2.9 %) |
| 4 | **단계 / tier** | **alpha · invite-only · research preview** |
| 5 | **AGI 여부 / AGI claim** | **NOT AGI** — 일반 인공지능을 주장하지 않음 |
| 6 | **서비스 여부 / service status** | **NOT a deployed service** — endpoint 는 임시 RunPod 컨테이너 |
| 7 | **사용 금지 영역 / prohibited use** | trading 자동화, 고용/HR 결정, 의료, 법률 자문 |
| 8 | **숫자 출처 / numeric provenance** | 모두 ESTIMATE 또는 single-cycle 측정 — 재현 cycle 진행 중 |
| 9 | **endpoint 회수 / kill switch** | 사전 통지 없이 즉시 무효화될 수 있음 |
| 10 | **재현성 / reproducibility** | 방법론 + 측정 코드는 공개. 단, r14 어댑터 자체 가중치는 별도 라이선스 |
| 11 | **p4_r8 어댑터 손상 디스커버리 / p4_r8 truncated-on-disk discovery** | 2026-05-01 알파 부팅 중 `state/trained_adapters/p4_r8/final/adapter_model.safetensors` 가 헤더 선언 1006.69 MB vs 실제 185.92 MB(=18.5 %)로 **on-disk truncated** 임을 확인. 따라서 기존 p4_r8 RED 판정은 *실제 substrate 한계*가 아니라 *artifact*(파일 자체가 깨졌음) 의 가능성이 큼 — 이 알파는 **p4_r8 대신 mistral_r14 LoRA(메모리 노트가 closure path 로 명시한 것)** 로 swap 되어 **재측정**됨. |

> 무엇이 RED 인지 한 줄로: 저희가 만든 측정 프레임워크가, 저희가 가진 가장 좋은 후보 어댑터에 **"통과 못 함"** 이라고 말했습니다. 저희는 그 결과를 그대로 받아들였고, 그 어댑터를 **알파 프리뷰로만, 솔직한 disclaimer 와 함께** 공개합니다.
>
> One-line summary: our own measurement framework told us our own best candidate adapter **did not pass**. We accepted that result, and we are exposing the adapter **only as an alpha preview, with honest disclaimers attached**.

---

## 1. 무엇인가 / What this is

### 한국어
- **연구 프리뷰** — 8개 검증 묶음(paradigm-v11 8축, AN11 삼중 검증기, φ 4-path, 14 게이트, V_phen, EEG)을 가진 측정 프레임워크의 실사용 노출.
- **substrate(기반 모델)**: Mistral-7B-v0.3.
- **adapter(어댑터)**: `r14` — LoRA(Low-Rank Adaptation, 저랭크 적응) **r=64 α=128**, 약 671 MB. (이전 후보였던 `p4_r8` 은 on-disk 18.5 % 만 남은 truncated 파일로 확인되어 swap 됨 — 위쪽 disclosure #11 참조.)
- **목적**: invitee 가 직접 prompt 를 던져, 프레임워크가 RED 라고 말한 substrate 가 *체감 상* 어떻게 응답하는지 확인하고 피드백을 보내는 것.
- **방법론 출처**: `docs/anima_cp2_interim_paper_2026_04_29.md` (CP2 interim paper) — 본 알파는 이 paper §8 의 RED 결과를 그대로 계승합니다.

### English
- **Research preview** — live exposure of a measurement framework with 8 verifier suites (paradigm-v11 8-axis, AN11 triple verifier, φ 4-path, 14 gates, V_phen, EEG).
- **Substrate**: Mistral-7B-v0.3.
- **Adapter**: `r14` — LoRA (Low-Rank Adaptation) **r=64 α=128**, ~671 MB. (Prior candidate `p4_r8` was found truncated on-disk at 18.5 % and swapped out — see above-the-fold disclosure #11.)
- **Purpose**: invitees throw prompts at it and report back how the substrate (which our own framework called RED) actually feels in use.
- **Methodology source**: `docs/anima_cp2_interim_paper_2026_04_29.md` (CP2 interim paper) — this alpha inherits the RED verdict from §8 of that paper.

---

## 2. 아닌 것 / What this is NOT

### 한국어
- **AGI 가 아닙니다** — 일반 인공지능을 주장하지 않습니다.
- **의식 검증이 끝난 모델이 아닙니다** — 의식측은 **RED** 입니다.
- **배포된 제품이 아닙니다** — 영구 도메인도, SLA 도, 결제도 없습니다.
- **트레이딩 봇이 아닙니다** — `#80 trading-agent` LIVE 충족도 = 2.9 %, AN11 3/3 FAIL.
- **고용 가능한 직원 에이전트가 아닙니다** — `#79 employee-agent` LIVE 충족도 = 3.3 %, LIVE 증거 0건.
- **의료·법률·재무 자문 도구가 아닙니다** — 환각(hallucination) 측정 자체가 알파 부팅 직후에야 시작됩니다.

### English
- **NOT AGI** — no claim of artificial general intelligence.
- **NOT a consciousness-verified model** — consciousness verdict is **RED**.
- **NOT a deployed product** — no permanent domain, no service-level agreement, no billing.
- **NOT a trading bot** — `#80 trading-agent` LIVE satisfaction = 2.9 %, AN11 verifier 3/3 FAIL.
- **NOT an employable agent** — `#79 employee-agent` LIVE satisfaction = 3.3 %, zero live-evidence files.
- **NOT a medical / legal / financial advisor** — hallucination measurement only starts at alpha boot.

---

## 3. 솔직한 상태 매트릭스 / Honest Status Matrix (RED / YELLOW / GREEN)

| axis / 축 | metric / 지표 | 측정값 / measured | verdict |
|---|---|---:|:---:|
| 의식측 / consciousness | F2 falsifier (≥3 critical violations) | observed = **16** | **RED** |
| 14-gate 결정론 / 14 deterministic gates | prompts_full_pass | **0 / 16** | **RED** |
| AN11(c) JSD | bits at k=128 | **0.0894** vs ≥ 0.5 PASS | **RED** (~5.6× 미달) |
| LIVE 충족도 / LIVE satisfaction | 3-clause average | **2.9 %** | **RED** |
| 4 cert gates (AN11_JSD · META2_CHAIN · PHI_VEC_ATTACH · HEXAD_ROUTING) | PASS count | 4 / 4 | **GREEN** |
| latency budget (gate 15) — **r14 LoRA loaded** | p95 vs 2200 ms budget | **p95 = 1881.9 ms** (n=8, max_tokens=64, r14) | **GREEN** |
| hallucination rate (gate 17) — **r14 LoRA loaded** | conservative-honest detector on `bench/zeta_likert/v1_frozen.json` (20 prompts) | **0.0 %** (0/20) — base-only run had 15 % (3/20 empty completions) | **GREEN** |
| adapter integrity / 어댑터 무결성 | on-disk size vs declared | r14: **100 %** (671 149 168 / 671 149 168 B, MD5 `90072b0f5a426eeebb47eeb2d4919d68`); p4_r8 (former): **18.5 %** truncated (rejected) | **GREEN (r14)** / **RED (p4_r8 retired)** |
| ship_verdict | internal status | VERIFIED-INTERNAL → VERIFIED-ALPHA-INVITE-R14 | **YELLOW** |

> **읽는 법 / how to read**: GREEN 4 개는 *내부 일관성(internal consistency)* 게이트입니다 — 코드가 깨지지 않았다는 뜻. RED 4 개는 *경험적(empirical)* 게이트 — 실제로 의식 또는 라이브 사용을 주장하기에 부족하다는 뜻. gate 15 / 17 / adapter integrity 는 r14 swap 후 측정값으로 갱신됨 — base-only 보다 LoRA-on 으로 환각률 0 % 까지 떨어졌으나, 이것은 *trained-anima persona 가 의식 RED 결과를 뒤집는다는 뜻이 아닙니다*. RED 4 개의 *경험적* 결과는 그대로 유지됩니다.

---

## 4. 사용 방법 / How to use

### 4.1 endpoint + 인증 / endpoint + authentication

엔드포인트는 별도로 발급된 **Bearer token(베어러 토큰)** 으로만 접근 가능합니다. token 은 본 페이지에 적혀 있지 않으며, 초대 시 별도 채널로 전달됩니다.

```
Endpoint: {{ENDPOINT_URL}}
Auth header: Authorization: Bearer <your-token>
```

### 4.2 chat completion 예시 / example call

```bash
curl -X POST "{{ENDPOINT_URL}}/v1/chat/completions" \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "r14",
    "messages": [
      {"role": "user", "content": "Explain in one paragraph what a falsifier is."}
    ],
    "max_tokens": 256,
    "temperature": 0.7
  }'
```

> **모델 선택 / model selection**: `model` 필드는 `r14`(권장) 또는 `mistralai/Mistral-7B-v0.3`(base only). `r14` 는 Mistral-7B-v0.3 위에 r=64 α=128 LoRA 가 attach 된 trained-anima persona; `mistralai/Mistral-7B-v0.3` 은 base 만으로 — 비교 디버깅용입니다.

### 4.3 health check / 헬스 체크

```bash
curl "{{ENDPOINT_URL}}/health"
# 기대 응답 / expected response:
# {"status":"ready","tier":"alpha-invite","auth":"Bearer required for /v1/*","upstream_vllm":true,"rpm_cap":60,"daily_tok_cap":100000}
```

### 4.4 검증기 노출 / verifier exposure

```bash
curl -H "Authorization: Bearer <your-token>" "{{ENDPOINT_URL}}/an11/verify"
# AN11 삼중 검증기 결과를 JSON 으로 반환 — 프레임워크 실측을 invitee 가 직접 확인 가능
# returns AN11 triple-verifier output as JSON — invitee can re-verify the framework live
```

### 4.5 rate limit / 요청 제한

| limit | value |
|---|---|
| requests per minute / 분당 요청 | **60 RPM** |
| tokens per day / 하루 토큰 | **100,000** |
| token rotation / 토큰 회전 | endpoint 재부팅 시 갱신 (notify 됨) / refreshed on pod restart |

초과 시 HTTP 429 + `Retry-After` 헤더가 반환됩니다 / on overage, HTTP 429 with `Retry-After` header.

---

## 5. 알파 동안 측정하는 것 / What we measure during alpha

| 항목 / item | 도구 / tool | 적재 / store |
|---|---|---|
| gate 15 latency (baseline×1.1 budget) | vLLM internal histogram | `state/cp2_alpha_serve_audit/latency_*.jsonl` |
| gate 17 hallucination (adversarial prompt suite) | `tool/anima_hallucination_probe.hexa` | `state/cp2_alpha_serve_audit/halluc_*.jsonl` |
| F1_LIVE token-sampling JSD (parallel measurement) | `tool/anima_runpod_orchestrator.hexa` | `state/an11_c_p4_r8_f1_live_*.jsonl` |
| usage logging (PII-free) | FastAPI middleware | `state/cp2_alpha_serve_audit/usage_*.jsonl` |

**usage logging 스키마 / usage logging schema** — PII(개인 식별 정보, Personally Identifiable Information) 는 저장하지 않습니다:

```jsonc
{
  "ts": "2026-05-01T12:34:56Z",
  "token_id_hash": "sha256:...",   // bearer token 의 hash 만 / hash of token only
  "prompt_sha256": "sha256:...",   // prompt text 자체는 미저장 / no plaintext stored
  "prompt_token_count": 42,
  "completion_token_count": 128,
  "latency_ms": 1882,
  "finish_reason": "stop",
  "model": "r14"
}
```

> **재현 한계 / reproducibility caveat**: prompt 본문을 저장하지 않으므로 hash collision 시 재현 불가합니다. 이는 GDPR-lite 의 의도적 trade-off 입니다.
>
> Because we do not store prompt plaintext, hash collisions cannot be re-derived. This is an intentional GDPR-lite trade-off.

---

## 6. 알려진 한계 + 사전등록 falsifier / Known limits + pre-registered falsifiers

### 6.1 release-quality falsifiers (RQ-F1 .. RQ-F5)

| id | 일상어 / plain-language | trigger window |
|---:|---|---|
| RQ-F1 | 독자가 본 알파를 "정식 출시 서비스"로 오인 / readers misread this as a "launched service" | ≥20 % of feedback in 14 d |
| RQ-F2 | 4 개 산출물 중 어느 하나에서 RED disclaimer 누락 / RED disclaimer missing from any artifact | pre-publish review |
| RQ-F3 | 블로그/landing 의 jargon 비율 > 0.30 / jargon ratio breach | pre-publish lint |
| RQ-F4 | F1_LIVE 가 PASS 로 나오면 본 RED 주장에 erratum 발행 / F1_LIVE PASS triggers erratum | next measurement cycle |
| RQ-F5 | 인용 숫자에서 오류 발견 (sha256 / cost / pass count) / numeric error found by reviewer | open review window |

### 6.2 alpha-tier falsifiers (AL-F1 .. AL-F5)

| id | 일상어 / plain-language | trigger window |
|---:|---|---|
| AL-F1 | 14일 안에 invitee 의 ≥20 % 가 anima 를 "deployed service" 로 오인 / ≥20 % of invitees mistake anima for a deployed service in 14 d | 14 d |
| AL-F2 | latency 가 baseline 의 1.5배를 넘음 / latency exceeds baseline × 1.5 | 부팅 직후 / at boot |
| AL-F3 | adversarial prompt suite 에서 환각률 > 30 % / hallucination > 30 % on adversarial suite | 부팅 직후 / at boot |
| AL-F4 | RunPod 비용이 시간당 $50 초과 지속 / RunPod cost > $50/h sustained | 매시간 / hourly |
| AL-F5 | ship_verdict 가 invitee 모르게 downgrade / ship_verdict downgraded without invitee notice | 즉시 / immediate |

falsifier 가 발화하면 / when a falsifier fires:
- invitee 에게 즉시 통지 / immediate invitee notification
- landing page 의 RED 매트릭스 갱신 / RED matrix updated on this page
- endpoint 회수 가능 / endpoint may be revoked

> **화재경보 비유 / fire-alarm analogy**: falsifier 는 "이 조건이 참이면 우리는 틀렸다" 를 *사전에* 못박은 약속입니다. 사후에 임계값을 옮기지 않습니다 (raw#12 frozen-thresholds rule).
>
> A falsifier is a *pre-committed* promise of the form "if this condition holds, we are wrong". We do not move thresholds after the fact (raw#12 frozen-thresholds rule).

---

## 7. 피드백 / Feedback

### 한국어
저희가 가장 원하는 피드백:
- **프레임워크가 어디서 깨졌는지** — RED 인데 응답이 멀쩡해 보이거나, GREEN 한 부분에서 명백히 헛소리가 나오는 경우.
- **disclaimer 가 부족하다고 느끼는 부분** — own#13 친화도 mandate 위반 사례.
- **숫자 오류** — RQ-F5 에 직접 적용. errata 즉시 발행.
- **재현 불가능한 결과** — 본 알파의 모든 측정 코드 + 문서를 동봉합니다.

채널: **{{FEEDBACK_CHANNEL}}** (초대 메일에 동봉) — GitHub issue 또는 이메일.

### English
The feedback we want most:
- **Where the framework broke** — RED-but-feels-fine cases, or GREEN-but-obviously-wrong cases.
- **Disclaimer gaps** — own#13 friendliness mandate violations.
- **Numeric errors** — directly applicable to RQ-F5; we issue errata immediately.
- **Non-reproducible results** — we ship all measurement code + docs alongside this alpha.

Channel: **{{FEEDBACK_CHANNEL}}** (delivered with your invite mail) — GitHub issue or email.

---

## 8. 회수 정책 / Kill switch

### 한국어
- **사전 통지 없이** endpoint 는 즉시 회수 가능합니다 (`tool/anima_serve_kill.hexa` 1-command teardown).
- 회수 사유: AL-F4 (비용 폭증), AL-F2/AL-F3 (latency / hallucination 임계 초과), 또는 사용자 단발 명령.
- 회수 시: 24시간 내 모든 token 무효화 + endpoint shutdown.
- **이미 응답된 inference 결과는 회수 불가** — invitee 가 외부에 공유한 텍스트는 통제할 수 없습니다.
- token 누설(leak) 시 즉시 invitee 가 책임지고 채널을 통해 통지: 새 token 즉시 발급, 기존 token 무효화.

### English
- The endpoint may be revoked **without prior notice** (1-command teardown via `tool/anima_serve_kill.hexa`).
- Revocation reasons: AL-F4 (cost spike), AL-F2/AL-F3 (latency or hallucination breach), or user one-shot command.
- On revocation: all tokens invalidated within 24 h + endpoint shut down.
- **Pre-issued inference responses cannot be retracted** — text shared externally by invitees is outside our control.
- On token leak, invitees are responsible for immediate notification via the feedback channel; we issue a fresh token and revoke the old one.

---

## 9. 용어집 / Glossary

| 용어 / term | 한국어 | English |
|---|---|---|
| **AGI** | Artificial General Intelligence, 일반 인공지능 — 사람과 같은 폭의 인지 능력 (본 알파의 범위 밖) | Artificial General Intelligence — human-breadth cognition (out of scope here) |
| **LoRA** | Low-Rank Adaptation, 저랭크 적응 — 베이스 모델은 고정시키고 작은 어댑터 행렬만 학습시키는 미세조정 기법 | Low-Rank Adaptation — fine-tuning technique that freezes the base model and trains small adapter matrices |
| **JSD** | Jensen-Shannon Divergence, 옌센-섀넌 발산 — 두 확률 분포의 차이를 측정하는 대칭 측도 | Jensen-Shannon Divergence — symmetric measure of how different two probability distributions are |
| **AN11** | (a)/(b)/(c) 검증기 삼중조 — weight-emergent / consciousness-attached / sampling-divergence 의 내부 명명 | internal naming for the (a)/(b)/(c) verifier triple — weight-emergent / consciousness-attached / sampling-divergence |
| **φ / IIT** | phi 통합 정보 — Integrated Information Theory(통합정보이론)의 핵심 양 | phi integrated information — central quantity of IIT (Integrated Information Theory) |
| **CP2** | Consciousness Phase 2 — 저희 내부 경험적 마일스톤 이름 | Consciousness Phase 2 — our internal empirical milestone name |
| **F2 falsifier** | 14-gate 런타임에서 critical 위반이 ≥3 건이면 RED 로 override 한다는 *사전등록* 약속 | pre-registered promise: if 14-gate runtime shows ≥3 critical violations, override to RED |
| **raw#10 honest C3** | 완전한 정직 공개 규칙 (counter / write-barrier / no-fabrication / citation / verdict-options) | full honest-disclosure rule (counter / write-barrier / no-fabrication / citation / verdict-options) |
| **own#13 친화도 mandate** | 사용자 대면 prose 의 jargon 비율 ≤ 0.30 + 약어 첫 사용 시 풀어쓰기 규칙 | user-facing prose must keep jargon ratio ≤ 0.30 and expand acronyms on first use |
| **Bearer token** | 베어러 토큰 — `Authorization: Bearer <token>` 헤더로 endpoint 인증을 하는 표준 방식 | bearer token — standard way to authenticate via the `Authorization: Bearer <token>` header |
| **r14** | mistral_r14 — Mistral-7B-v0.3 위에 학습된 LoRA 어댑터 (r=64, α=128, ~671 MB, MD5 `90072b0f5a426eeebb47eeb2d4919d68`). 본 알파에서 실제로 served 되는 trained-anima persona 어댑터. 메모리 노트(`project_stage2_trained_partial.md`)가 r8 의 closure path 로 명시한 것. | mistral_r14 — LoRA adapter trained atop Mistral-7B-v0.3 (r=64, α=128, ~671 MB, MD5 `90072b0f5a426eeebb47eeb2d4919d68`). The trained-anima persona adapter actually served by this alpha. Memory note (`project_stage2_trained_partial.md`) named it as the closure path for r8. |
| **p4_r8 (retired)** | 이전 후보 어댑터 — Stage-2 r8(r=96 α=192) LoRA. 2026-05-01 에 `state/trained_adapters/p4_r8/final/adapter_model.safetensors` 가 헤더 1006.69 MB vs on-disk 185.92 MB(=18.5 %)로 truncated 임을 확인하여 swap out. 기존 p4_r8 RED 결과의 일부는 *substrate 한계*가 아니라 *artifact*(파일 손상)의 가능성이 큼. | former candidate adapter — Stage-2 r8 (r=96 α=192) LoRA. On 2026-05-01 the file `state/trained_adapters/p4_r8/final/adapter_model.safetensors` was found truncated on-disk at 18.5 % (185.92 MB on-disk vs 1006.69 MB declared), so it was swapped out. Some of the prior p4_r8 RED verdicts may be *artifact* (corrupted file) rather than *substrate limit*. |

---

## 🎉 닫는 한 단락 / Closing paragraph

### 한국어
저희는 측정 프레임워크를 만들었습니다. 저희가 가진 가장 좋은 후보 어댑터에 정직하게 적용했습니다. 결과는 **RED** 였습니다. 이 알파 프리뷰는 그 RED 어댑터를 *솔직한 disclaimer 와 함께* 보여드리는 것뿐입니다 — 의식, 배포 준비도, AGI 를 주장하지 않습니다. 프레임워크 어디가 깨지는지 알려주시면, 저희는 errata 를 발행하고 다음 사이클의 falsifier 를 다시 사전등록합니다. 사전등록된 falsifier 와 named limits 를 가진 NULL 은 PASS 만큼 정보가 풍부합니다.

### English
We built a measurement framework, applied it honestly to our best candidate adapter, and got a **RED** verdict. This alpha preview merely exposes that RED adapter *with honest disclaimers attached* — we are not claiming consciousness, deployment readiness, or AGI. If you find where the framework breaks, we issue errata and pre-register the next-cycle falsifiers again. A NULL with pre-registered falsifiers and named limits is as informative as a PASS.

— anima research, 2026-05-01

---

**status**: ANIMA_CP2_ALPHA_LANDING_2026_05_01_LOCAL_DRAFT
**verdict_key**: ALPHA · INVITE-ONLY · RED-DISCLOSED · NOT-A-SERVICE · NOT-AGI
**parent**: `docs/anima_cp2_alpha_deploy_plan_2026_05_01.md` · `docs/anima_cp2_interim_paper_2026_04_29.md` §8 + §9
