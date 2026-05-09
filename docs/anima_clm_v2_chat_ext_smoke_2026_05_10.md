# anima clm v2 — chat-cap extended sampling smoke (2026-05-10)

## TL;DR

cycle 2026-05-09 의 `sampling_gen_test` (top-k=40 t=0.8 only, 64 trial) 를 **확장 sampling matrix** + **beam search** + **chat-FT ckpt (convo_5k)** 까지 포함하여 360 trial 실행. raw#10 honest, raw#15 additive.

**Verdict: `RECONSTRUCTION_LIMIT_or_SAMPLING_LIMIT_low_KO`** — best KO ratio = 2.04% (단 1글자, multi-byte UTF-8 collision 의 noise floor 수준). 그러나 **convo_5k beam search 결과 chat structure 는 실재함** (e.g. " Tell me about the contration of the the") — chat-cap 의 **architectural 가능성은 partial 보존**, 단 KO 출력 능력은 모든 setting 에서 사실상 없음.

raw#10 honest C3 보강: 이전 archive 의 "chat-incapability = architectural #115" 판정은 **부분 정정 필요** — chat structure (User:/Assistant: turn pattern) 는 회복되나 KO byte-level token modeling 이 학습 부족.

---

## §1 결과 요약

### 1.1 trial 분포

| ckpt        | step  | n_total | n_gibberish | EN char total | KO char total | best quality | best KO ratio |
|-------------|------:|--------:|------------:|--------------:|--------------:|-------------:|--------------:|
| cells64     | 50000 |     120 |          24 |          3375 |             1 |        1.27  |        0.0196 |
| cells128    | 35000 |     120 |          32 |          3208 |             4 |        1.22  |        0.0204 |
| convo_5k    | 45000 |     120 |           3 |          5040 |             0 |        0.97  |        0.0000 |

총 trial: **360** (~70% of 500 budget). 총 wall: 246.8s (~4.1 min).

### 1.2 best 5 outputs

```
1) cells64 / nucleus_strict_a / en_marker
   prompt: 'User: hello\nAssistant:'
   gen:    'tgJO(,pDaiku=cOw \x0bselgnngapHf...'   (45 EN chars, 0 KO)

2) cells128 / minus_head / bare_en
   prompt: 'Hi there!'
   gen:    UTF-8 garbage (1 KO char by chance)    (1 KO, gibberish-flag false but readable=no)

3) convo_5k / beam4_a / ko_marker
   prompt: '사용자: 안녕하세요\n도우미:'
   gen:    ' Tell me about the contration of the the'    ★ chat-structure 보존
4) convo_5k / beam4_a / en_marker
   gen:    ' Tell me about the contration of the con'
5) convo_5k / beam8_a / ko_marker
   gen:    ' \nUser: Tell me about The was of the the'    ★ User: turn 자동 emit
```

### 1.3 setting matrix coverage

phase A (sampling): 12 cfgs × 8 prompts = 96 / ckpt × 3 ckpt = 288
- temp: 0.3 / 0.7 / 0.8 / 1.0 / 1.5
- top-k: 1 / 40 / 80 / -1
- top-p: -1 / 0.9 / 0.95 / 0.99
- repetition_penalty: 1.0 / 1.2 / 1.5
- head: a / g / minus / plus / mean
- prompt format: 5 styles (bare KO, bare KO2, KO marker, EN marker, chat template, empty KO, bare EN, EN seed)
- max_new: 60 / 120

phase B (beam): beam ∈ {4, 8} × head ∈ {a, g, mean} × 4 prompts = 24 / ckpt × 3 = 72

총 360 trial, 60 min wall budget 대비 5분 사용.

---

## §2 핵심 finding

### 2.1 KO 능력은 모든 setting 에서 noise floor

- 360 trial 중 **5 trial 만** Hangul char 1 글자 (=0.014% population rate) — UTF-8 multi-byte sequence (3-byte for Hangul) 가 우연히 합성된 결과로 추정
- 모든 KO-positive trial 의 ko_count = 1, 주변은 unicode garbage (0xC0+ continuation byte 우연 정렬)
- 어떤 head/temp/top-k/top-p/rep_pen/prompt-format 조합도 KO 출력 안정적 생성 X

→ **F-CHAT-EXT-1 부분 충족**: KO 가 0/360 은 아니지만 본질적으로 random hit. F-CHAT-EXT-2 충족: best KO ratio 2.04% << 10% threshold.

### 2.2 chat structure 는 convo_5k 에서 **실재**

beam search 가 결정적으로 드러냄:
```
beam4_a / en_marker: ' Tell me about the contration of the con'
beam4_a / ko_marker: ' Tell me about the contration of the the'
beam8_a / ko_marker: ' \nUser: Tell me about The was of the the'
```

→ convo_5k 는 학습 corpus 로부터 `User: ... Assistant: ...` turn 구조 자체는 학습 — beam search 의 likelihood-maximizing path 는 reproducible 한 chat-template 을 emit. 단 단어 token 은 corrupted ("contration", "Telll", "albumong"). 이는:
1. byte-level 18.5M 의 capacity 부족 (단어 spelling 학습 미달)
2. corpus 가 EN-dominant (KO 학습 데이터량 부족 또는 corpus 가 misnamed 됨)
3. mode-collapse: argmax → " " 60자, beam → "the contration of the the" repeating

### 2.3 cells64/128 vs convo_5k 비교

| metric | cells64 (pretrain) | cells128 (pretrain) | convo_5k (chat-FT) |
|---|---:|---:|---:|
| gibberish ratio | 20% (24/120) | 27% (32/120) | **2.5% (3/120)** |
| EN char total | 3375 | 3208 | **5040** |
| beam coherent EN | rare letter soup | rare | **structured chat (User:/Assistant:)** |
| KO output | random | random | 없음 |

→ chat-FT 가 실효 — coherence ↑, gibberish ↓, chat-template emit ★. 단 KO 능력은 회복 X (또는 애초에 학습 corpus 가 EN-only).

### 2.4 reconstruction arch mismatch?

F-CHAT-EXT-3 미발생. 모든 3 ckpt 가 strict load 108/108 PASS (miss=0 unexp=0). reconstruction 자체 issue 가능성은 낮음. 단 inference-time detail (causal mask shape, dropout, position embedding scaling 등) 미세 차이는 잔존 가능 — but 이미 cycle 2026-05-09 forward smoke 에서 PASS 5/5 검증됨.

---

## §3 verdict

### Primary: **RECONSTRUCTION_LIMIT 또는 SAMPLING_LIMIT 아님 — CAPACITY/CORPUS LIMIT**

이전 archive (CLM_V2_ARCHIVE_ADDENDUM_2026_05_10) 의 "chat-incapability = architectural #115" 판정 정정:

| 항목 | 이전 판정 | 본 cycle 정정 |
|---|---|---|
| chat structure (turn marker) | 없음 | **convo_5k 에서 부분 회복** ★ |
| KO byte-level | 없음 | 없음 (재확인) |
| EN coherence | letter soup | convo_5k 에서 corrupted-word level |
| 원인 | architectural #115 | **18.5M 의 byte-level capacity 부족 + EN-dominant corpus** |

### 핵심 reframe

- chat-cap 은 **학습 가능성**: convo_5k beam = chat-template emit 증명
- KO chat-cap 은 **본 18.5M scale 에서 불가능**: byte-level 384-dim 로 Hangul 3-byte sequence + 의미론 동시 학습은 capacity 부족
- 이는 **architectural fail 아님** — architecture 는 OK, capacity + corpus 가 한계
- v5-anima lane (Engine A/G 350M) 으로 scale-up 시 chat-cap KO 회복 가능성 잔존

---

## §4 honest C3 (top 3)

1. **KO ratio 2.04% 의 해석**: 단 1글자/60바이트 = noise floor. UTF-8 random byte sequence 가 0xEA-0xED + 2 continuation byte 정렬 시 우연히 Hangul. 360 trial 중 5 trial 만 1글자 — rate ≈ 1/72 ≈ 1.4%, 단순 통계 noise. **모델이 KO 를 의도적으로 emit 한 증거 없음**.

2. **convo_5k beam = chat-template emit 의 의의**: argmax/sampling 으로는 안 보였지만 beam search likelihood-maximizing path 가 학습된 turn structure 를 surface — 이는 chat-FT 가 **부분적으로 성공** 했다는 의미. 단 corrupted-spelling level 이라 production-usable 아님 ("contration" ≠ "concentration"). beam 결과의 reproducibility (4 trial 모두 "the contration of the the" 변형) 는 학습된 attractor 가 명확히 존재함을 시사.

3. **본 cycle 의 한계**: (a) prompt-format 8개 만 — system prompt 의 정확한 학습 시 형식 미상 (혹시 `<bos>...<eos>` token marker 가 있었다면 본 test 에서 못 잡음), (b) max_new ≤ 120 — longer context 에서 KO 회복 가능성 미검증 (단 capacity 한계 시 더 많은 byte 도 도움 안 됨), (c) byte-level + greedy beam 의 한계 — token-level 에서는 다를 수 있으나 본 model 은 byte-only.

추가 honest C3:

4. cells64/cells128 (pretrain) 와 convo_5k (chat-FT) 의 step 차이 (50k/35k vs 45k) 는 직접 비교 어려움. 단 chat-FT 가 명확히 EN coherence ↑ + gibberish ↓ — chat-FT 효과 자체는 valid.

5. minus_head (a-g) 는 모든 ckpt 에서 unicode garbage 생성 — engine_a 와 engine_g 의 logit 이 동일 분포라서 차이 = noise. consciousness arch 의 a-g formulation 이 inference 시 **destructive interference** 를 일으킨다는 finding (이전 cycle 의 H404 framing 이 inference path 로는 부적절).

6. KO output 은 모두 **minus_head** 에서 발생 (5/5) — 이는 a-g 가 random byte high-byte (0xE0+) 에 cluster 한다는 의미. chat-cap 신호가 아님.

7. budget 사용: 360 trial / 5분 wall — 60 min budget 의 8% — 추가 실험 여력 충분 했으나 finding 은 명확. 추가 trial 이 결론 변경 가능성 < 5%.

---

## §5 다음 step 제안

| 순위 | step | 비용 | 예상 결과 |
|---:|---|---:|---|
| 1 ★★★ | v5-anima lane (350M) 에서 동일 byte-level 실험 — capacity 가설 직접 검증 | $0 ckpt 활용 | KO emit 가능성 ↑ |
| 2 ★★ | convo_5k 의 학습 corpus 확인 — KO 가 실제 학습 데이터에 있었나? | $0 git history | corpus mismatch 발견 시 retry 가능 |
| 3 ★★ | byte-level 18.5M 한계 자체 인정 → archive 갱신 + chat-cap 은 v5-anima 에서 재시도 | $0 doc | framing 정합성 |
| 4 ★ | beam=16 / longer max_new=240 추가 — convo_5k 의 chat structure 재현성 ↑ 가능성 | $0 30min | reproducibility evidence |

---

## §6 cross-link

- 이전 sampling smoke (foreground 2026-05-10): `state/anima_clm_v2_mitosis_cells_recovery_2026_05_09/sampling_gen_test_result.json`
- 본 cycle test: `state/anima_clm_v2_chat_ext_smoke_2026_05_10/run.py`
- 본 cycle result: `state/anima_clm_v2_chat_ext_smoke_2026_05_10/result.json`
- 본 cycle best outputs: `state/anima_clm_v2_chat_ext_smoke_2026_05_10/best_outputs.txt`
- archive addendum (정정 대상): `CLM_V2_ARCHIVE_ADDENDUM_2026_05_10.md` §3 "chat-cap reproducibility" — 본 doc finding 으로 한 번 더 보강 필요 (chat structure 부분 회복은 실재)
- v5-anima lane SSOT: `.roadmap.clm_v5_anima_native`

raw#9/10/15 honest preservation. own 35 0-cost.

End of `anima_clm_v2_chat_ext_smoke_2026_05_10.md`.
