# .verdicts — claim 검증 결과 영구 보존소

> `a_claim_verify` — `CLAIMS.tape` 의 각 claim 을 `hexa verify` (g5) 로 돌린
> **raw stdout 을 그대로** 보존한다. LLM 자가판정·paraphrase 금지 (p7).

## 레이아웃

```
.verdicts/
  <slug>/
    <claim-id>.txt      ← hexa verify / closure_auto_judge 원문 (verbatim)
  <slug>.tape           ← (선택) slug 전체 verdict 매트릭스 요약
```

## 규칙

- 파일명 = `CLAIMS.tape` 의 `raw =` 포인터와 1:1 일치.
- 내용 = 검증 명령의 **표준출력 원문**. 재가공·요약·의역 금지.
- 🟠 INSUFFICIENT / 🟡 citation-only / ⚪ 미검증은 게이트 통과 불가
  (`a_paper_gate`) — 보존은 하되 논문 섹션 링크로 쓰지 않는다.
- terminal (🔵 / 🟢 / 🔴 CLOSED-negative) 만 `PAPER/<slug>/` 섹션에 링크.
