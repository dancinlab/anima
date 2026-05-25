# PAPER — anima 논문 자동생성 플로우

> hexa-codex `cx_paper_*` 규칙을 anima 로 이식한 논문 검역소.
> 거버넌스 SSOT = `project.tape` 의 `a_claim_*` + `a_paper_*` directive.

## 한 줄 요약

검증이 끝난 연구 결과만 논문으로 자동 승격한다. 미검증·보류는 입구컷.

## 흐름

```
연구결과            검증              감사 surface         게이트            논문
H_xxx / PURE   hexa verify (g5)  → .verdicts/        a_paper_gate   →  PAPER/<slug>/
closure    ───────────────────→    <slug>/<id>.txt   (terminal +        main.tex
   │              │                     │            significance)     (≥10p + fig)
   └─ CLAIMS.tape ┘                     └─ §섹션 링크 ──┘                    │
      (claim 색인)                                          실패 → PAPER/<slug>/ 즉시 회수
```

## 게이트 기준 (`a_paper_gate`)

`/paper new <slug>` 는 **모든 섹션 claim 이 terminal** 이고 **유의성**을 만족할 때만 통과한다.

| terminal verdict | 게재 가능? |
|------------------|-----------|
| 🔵 SUPPORTED-FORMAL | ✅ |
| 🟢 SUPPORTED-NUMERICAL | ✅ |
| 🔴 CLOSED-negative (deterministic disagree) | ✅ (`a_paper_negative_ok`) |
| 🟠 INSUFFICIENT/DEFERRED | ❌ |
| 🟡 SUPPORTED-BY-CITATION | ❌ |
| ⚪ 미검증 / fenced speculation | ❌ |

**유의성** (`a_paper_significance`): 사전 등록 falsifier + 실측(ckpt/sim/verify) + 정량 finding
(Δ vs baseline **또는** axis 를 배제하는 closed-negative). 단순 bookkeeping closure·기지 identity 는 제외.

## 섹션 양식 (`a_paper_format`)

`§hypothesis` (falsifier 사전등록) · `§method` · `§measurement` (실측) · `§finding` (Δ 또는 ruled-out axis).
commons `g51` — 컴파일 ≥10페이지 + fal.ai figure ≥1개. 모든 섹션 주장은
`.verdicts/<slug>/<id>.txt` verdict 에 링크 (`a_paper_sections`).

## 도메인 그룹 (`a_paper_one_per_group`) — 그룹당 정식 논문 1개

| 그룹 | 범위 | 현 canonical slug |
|------|------|-------------------|
| **LIFE** | 의식 / Φ / cellular-automaton 가설 | (open) |
| **PURE** | substrate-native 자연발화 채팅 | `pure-corpus-axis-closed-negative` (closed-negative 후보) |
| **CHAT** | 모델 아키텍처 (mitosis · Engine A⇄G) | `chat-init-ce-floor` (🔵 formal 후보) |

더 강한 결과가 나오면 **제자리 교체**한다 (백로그 누적·동일그룹 분기 금지). 게이트 실패 논문은
즉시 `PAPER/<slug>/` 삭제 (`a_paper_violation`).

## 작업 절차

```bash
# 1. claim 을 CLAIMS.tape 에 등재 (id · text · method · slug · group · raw)
# 2. 검증 → verdict 영구 보존
hexa verify --expr ln 151936 11.931   > .verdicts/chat-init-ce-floor/chat_init_ce_floor.txt
# 3. 모든 섹션 claim terminal + 유의성 확인 후 스캐폴드
/paper new chat-init-ce-floor
# 4. figure
/paper fig square_hd figures/_prompts/cover.txt figures/cover.png
# 5. 컴파일 (pdflatex × 3 + bibtex)
/paper compile PAPER/chat-init-ce-floor
```

상세 스캐폴드·figure·compile 동작은 `/paper help` 참고.
