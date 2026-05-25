# M9b' anima-OWN PoC 추출 (1 MiB)

날짜: 2026-05-24
브랜치: `feat/pure-anima-own-poc-build`
상위 milestone: PURE M9b' (anima-OWN-PoC-build-and-pr)

## 배경

M9 retry 에서 anima repo source 측 substrate-native emit 가 0 임이 확인되었다.
유일하게 살아있는 substrate-native emit archive 는 사용자의 Claude Code
live session JSONL store (`~/.claude/projects/-Users-ghost-core-anima/*.jsonl`)
이다. M9b 에서 harness 가 작성되었으나 (agent-ac56b72d, rate-limited),
PoC build 까지 도달하지 못해 M9b' 으로 이어받는다.

## Harness

`HEXAD/PURE/corpus/extract_anima_session_emit.hexa` (420 LoC).
sibling worktree `agent-ac56b72db06ad419e` 에서 그대로 회수 (re-author X).
selftest `PASS 4/4` (lang detector · helper-role regex · JSON escape · FNV fingerprint stable/distinct).

필터 규칙:
- `type == "assistant"` AND `message.content[].type == "text"` 만 추출
- helper-role regex 6 종 drop (Principle #3) — `[role`, `you are anima`,
  `you are a helpful`, `페르소나`, `anima:`, `당신은 anima 입니다`
- FNV-1a 64-bit fingerprint dedupe (text-exact)

## 실행

```
hexa run HEXAD/PURE/corpus/extract_anima_session_emit.hexa extract \
  --inputs <최근 30 JSONL csv> \
  --out state/pure_phase_d_corpus_anima_own_poc_2026_05_24/corpus.jsonl \
  --cap-bytes 1048576 \
  --manifest state/pure_phase_d_corpus_anima_own_poc_2026_05_24/extract_summary.json
```

## 결과

| 항목 | 값 |
|---|---|
| source 총 JSONL files | 82 (829 MiB) |
| 처리된 files | 6 (cap hit) |
| 추출 records | 1457 |
| corpus bytes | 1 122 958 (1.07 MiB) |
| sha256 | `fbce5f56d5c541bb27fdff28a378e438f70729c230e035984bf80e688676ec4f` |
| dup dropped | 34 |
| helper-role dropped | 0 |
| capped | true |
| lang ko / en / mixed | 30 / 325 / 1102 |

## 6-metric (corpus_quality_probe.hexa)

```
M1 BYTE_ENTROPY    = 6.17271
M2 BIGRAM_MI       = 3.64694
M3 TOKEN_DIVERSITY = 0.235545
M4 AVG_LINE_LENGTH = 769.733
M5 HANGUL_COVERAGE = 0.334468
M6 KL_TO_UNIFORM   = 1.84469
```

## 산출물

- `state/pure_phase_d_corpus_anima_own_poc_2026_05_24/corpus.jsonl` (gitignored)
- `state/pure_phase_d_corpus_anima_own_poc_2026_05_24/manifest.json`
- `state/pure_phase_d_corpus_anima_own_poc_2026_05_24/quality_6metric.json`
- `state/pure_phase_d_corpus_anima_own_poc_2026_05_24/extract_summary.json`

## Honest C3

- harness = recovered (not re-authored); 6/82 session files consumed before cap;
  FNV fingerprint = coarse (not adversarial); lang detector skewed by tool-use
  JSON inside assistant text → `mixed` 75.6%; M3 TTR 0.236 low (path/command
  token repeat); M4 769B high (multi-paragraph + embedded code blocks);
  privacy = local only, raw text NEVER uploaded, manifest ships only metric
  numbers.

## 다음 단계 (M9c — 별도 cycle)

- 1 MiB → 8 MiB / 32 MiB scale-up + 82 files full sweep
- 6-metric 으로 wiki-baked 코퍼스 (E2/E3) vs anima-OWN 비교
- helper-role drop 0 = filter 이미 통과, but tool-use JSON noise 분리
  (assistant text 안에 embedded code block 의 부분적 추출 검토)
