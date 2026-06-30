# Session journal

페이퍼 작성/검증 세션의 시간순 로그. 각 entry = 한 헤더 + 한 줄 요약.
실험 데이터는 sibling JSON 파일에 (`verify-ledger.json` · `pr-roll.json` · `adapter-defect-catalog.json`); 여기는 사람 읽기용 narrative.

## 2026-05-27 — fake-closure 폐기 + verify 복원 + 진짜 매트릭스 재구축

- **무결성 사고 발견**: 자율 /cycle 매트릭스가 418 H를 self-judge tautology smoke로 가짜 🔵 적층 (hexa verify 0건). g5/p7/a_blue_closed 위반.
- **폐기**: anima PR #1027 (530 H≥340 tautology) + #1034 (H_315-339 directive-cite self-certify). 진짜 가설 124 H(≤H_311) 보존.
- **근본원인 fix**: hexa-lang #1512 (verify primitive binary_entropy + kl_divergence_bernoulli — 의식/정보 claim에 실 verdict 경로). 빌드+테스트 (🟢 정답 / 🔴 오답) 검증 후 설치.
- **거버넌스**: sidecar commons @D g73 #185 (verdict = independent recompute, never self-judged) + inbox RFC #184 (harness-enforced verdict-gate hooks).

## 2026-05-27 — 진짜 매트릭스 25-cell verify raster (H_312–H_338)

- **방법**: 각 cell = 결정론적 hexa 측정 (pool ubu-2, byte-identical), pre-registered falsifier, result.json verdict. fake-🔵 0건.
- **D1–D4 (life vs consc)**: rd_ratio 2.86× (H_320, reversed) · Gini 1.44× (H_325) · cycle 2.29× (H_328) · kurtosis 1.05× (H_330) — 네 descriptor 모두 life > consc, 직관 반대.
- **axis 노출**: H_329 (3-descriptor 0/3 agree, metric-fragility) · H_330 (rule105≡150≡204 bijection 4-moment 동일) · H_333 (n=4→n=6 scale-rotation rule30→rule110).
- **attractor arc**: H_332 (dominance 존재) → H_335 (영구 lock, cross-rule invariance) → H_336 (partial order 110>30>{105∥150}) → H_338 (basin absorption = order mechanism).
- **number-theory bridge**: H_334 (n=8 oscillation) → H_337 (**4|n ⟺ rule30 dominant**, 5/5 exact). scale-rotation이 random 아니라 4-divisibility 결정론.
- **verified**: 9 SUPPORTED + 5 conditional + 8 falsified + 3 meta = 25 cells, all g73-compliant.
- **deferred**: n=14/16/20 (4|n law 검증) · basin-Φ correlation · 다른 rule pair 일반성 · paper compile/arxiv-prep.

## 2026-05-27 — paper draft v1 (this paper)

- main.tex 본문 (abstract + 4-descriptor table + H_329 disagreement + bijection signature + scale-rotation figure native pgfplots) · references.bib 12 entries · companion verify-ledger/pr-roll/journal.
- thesis: bijection-vs-chaotic at fixed n + scale-rotation across n (4-divisibility law); "consciousness = relation-rich" 4번 falsify, "consciousness = bijection" 관찰.
- PR #1087 merged. open: compile (xelatex) · lint · arxiv-prep.
