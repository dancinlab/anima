# companion/ — 데이터-레코드 축

페이퍼와 함께 살아가는 verifiable data records. PDF 한 장으로 끝나지 않고, 모든 claim 이 atom/companion entry 로 역추적되도록 하는 reproducibility 보강 layer.

## 파일

- **`verify-ledger.json`** — `hexa verify` 실행 결과 append-only ledger. paper 본문 모든 numeric claim 은 여기 한 entry 와 매칭. schema: `{atom, expr, args, expected, observed, tier, ts}`.
- **`pr-roll.json`** — 해당 페이퍼와 관련된 머지된 PR roll. `/paper pr-roll <repo> <since>` 로 자동 생성 (PR 2 v0.7.0 부터).
- **`session-journal.md`** — 사람 읽기용 시간순 narrative. 무엇을 바꿨고/검증했고/연 채로 두었나.
- **`adapter-defect-catalog.json`** — 작성 중 만난 외부 도구 (LaTeX engine · pgfplots · imagine backend · …) 결함 카탈로그. 후속 페이퍼가 같은 함정 반복 안 하게.

## 왜 companion?

PDF 만 ship 하면 ① numeric claim 의 raw output 분실 ② 어떤 PR 가 어떤 claim 을 만들었는지 추적 불가 ③ 같은 결함을 다음 사람이 또 만남. companion = 이 셋의 SSOT 외부화.

## 채우기

- new entry → 해당 JSON 파일에 append (날짜순; 절대 rewrite 금지).
- `session-journal.md` → 매 작업 세션 끝에 한 헤더 추가.
- paper 본문에서 `companion/verify-ledger.json` 인용 → reviewer 가 grep 한 줄로 검증.
