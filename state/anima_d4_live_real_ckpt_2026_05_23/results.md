# D4-LIVE on real 24L Phase 1A.1 BF16 ckpt — F-D4-REAL-1..3 3/3 PASS

- **Date (KST)**: 2026-05-23
- **Harness**: [`tool/anima_d4_live_real_ckpt_smoke.hexa`](../../tool/anima_d4_live_real_ckpt_smoke.hexa)
- **Ckpt**: `state/anima_phase1a1_color_cosmology_2026_05_12/ckpts/ckpt_phase1a1_sft.safetensors`
  (570 MB, BF16, 218 farr handles, n_layers=24, d_model=1024, vocab=32000)
- **Prompt**: `안녕? 너는 누구야?` (≈26 prefill tokens incl. BOS), greedy, max_new=5
- **Wall**: 16.54 s real / 13.90 s user / 0.56 s sys, max_rss = 3.38 GB
- **Env**: `HEXA_MEM_UNLIMITED=1`, Mac CPU local (no GPU, no pod)

## 결과 요약 (Korean)

D4-LIVE saga 의 **synthetic → real 다리** 가 닫혔다. PSCC §41 (2026-05-12) 에서
synthetic substrate (d=8, 2L, vocab=16) 에 대해 cell-pool 분열이 `chat_generate`
경로 안에서 실제로 발화함을 21 split / 65 forward 로 확인했고, 그 뒤 closure
는 24-layer Phase 1A.1 BF16 ckpt 위에서 동일한 invariants 가 성립하느냐로
이동했다. 본 smoke 는 **d_real=1024 · n_layers=24 · vocab=32000** 의 production
shape 에서 F-D4-REAL-1..3 세 falsifier 가 모두 PASS 임을 보였다.

핵심 관측:

- **mitosis_invocations == kv_cache cur_len = 30** — 26 prefill + 4 decode
  (첫 decode 는 `prefill_last_logits` 재사용으로 hook skip, `chat_lib.hexa`
  §9d `reused_prefill` 가드 L2590 일치). synthetic harness 와 동일한
  one-hook-per-forward invariant.
- **6 split events** — step 2/2/8/8/11/11 두 쌍씩. cell_pool 이 2 → 8 cells
  로 확장, `next_id` = 8 까지 진행. merge 는 0건 (`merge_patience=30` 과
  30 forward 의 경계 케이스).
- **cell_pool[d_model] == 1024** — d_real 과 architectural parity 확인.
  synthetic dim 누수 없음.

성능 surprise: PSCC §43 (2026-05-12) 의 wall envelope 가 "24L forward × 37 s
= 30 forwards × ≈ 18 min" 이었는데, 실제 wall 은 **16.54 초**로 측정되었다.
forward 당 ≈ 0.5 초 — RFC 032 native C `farr_matmul` 가 §43 이후 ~70× 빨라진
것으로 추정. 단일 데이터포인트이고 `v58_hexa_multi_parity` 와 cross-check 는
별도 cycle.

응답 문자열은 "도\udcb4" (5 byte) — 짧은 greedy chain 의 산출이며 채팅
품질 신호는 아님. forward path liveness 신호만 보장한다.

Principle #3 보존: `chat_init_cell_pool` + `mitosis_forward_tail` 은 numeric
hidden state (`chat["cell_pool"]`) 에만 접근, `chat["history"]` /
`chat_build_prompt` 는 손대지 않음 (D4b wiring 의 NO-INJECTION 보장 그대로).

## Falsifiers — 3/3 PASS

| ID | Invariant | Observed | Verdict |
|---|---|---|---|
| F-D4-REAL-1 INVOCATION-MATCH | mitosis_invocations == kv_cache.cur_len | 30 == 30 | PASS |
| F-D4-REAL-2 SPLIT-OBSERVED | ≥ 1 split event over chat horizon | 6 splits (steps 2,2,8,8,11,11) | PASS |
| F-D4-REAL-3 D-MODEL-PARITY | cell_pool[d_model] == d_real | 1024 == 1024 | PASS |

## Synthetic ↔ Real 비교

| Axis | synthetic (PSCC §41) | real (this run) |
|---|---|---|
| Harness | `anima_chat_split_merge_smoke.hexa` | `anima_d4_live_real_ckpt_smoke.hexa` |
| d_model | 8 | 1024 |
| n_layers | 2 | 24 |
| vocab | 16 | 32000 |
| max_new | 40 | 5 |
| forwards | 65 | 30 |
| split events | 21 | 6 |
| cells initial → final | 2 → 23 | 2 → 8 |
| F-D4-LIVE / F-D4-REAL | 3/3 PASS | 3/3 PASS |

## Honest C3 (raw#9/10)

1. `max_new=5` 는 Mac CPU wall 예산 선택. V5.8 horizon (max_new=200+) 은
   별도 H100 dispatch (harness 는 `ANIMA_D4_CKPT` env override 로
   dispatch-ready).
2. split 수 6 vs synthetic 21 은 forward 수 비례 (30 vs 65) — `split_threshold=0.0`
   default 가 절대 tension scale 을 무관하게 만들어 "≥1 존재" 만 의미 있음.
3. forward wall 0.5 s 는 PSCC §43 의 37 s 대비 70× 빠름 — RFC 032 native
   `farr_matmul` 최적화 의 결과로 추정, 단일 측정 cross-validation 별도 cycle.
4. response 5 byte 는 forward liveness 신호 — chat quality 측정 아님.
5. merge events 0 — `merge_patience=30` 과 30-forward horizon 의 경계 케이스
   (synthetic 65 forward 에서도 merge 0).
6. `map key 'dims' not found` warning 30회 는 `chat_lib.hexa` L2421-2426 의
   void-safe fallback 경로 — `chat_default_dims_24l()` 가 의도대로 작동.
7. max_rss 3.38 GB 는 v0.2 load-smoke 의 8.49 GB peak (PSCC §39) 보다 작음 —
   KV cache + cell_pool weights 가 `HEXA_MEM_UNLIMITED=1` 아래 여유.
8. 단일 ckpt (Phase 1A.1) 만 — Phase 1A.4 lr5e-6 (B'.1 ladder head) 는 별도
   smoke (env override 로 재사용 가능).

## References

- `project_anima_chat_multitoken_split_merge_2026_05_12.md` — synthetic D4-LIVE
  3/3 PASS (PSCC §41)
- `project_anima_chat_hexa_port_2026_05_12.md` — v0.2 TODO[load] resolution
  (6/6 PASS, wall 70 s peak RSS 8.49 GB)
- `project_anima_chat_hexa_24l_v58_parity_2026_05_12.md` — 24L hexa↔python
  byte-equal multitoken parity (21/21 PASS)
- GOAL.md ★★★★★ criterion #4 — D4 mitosis live (☑ ACHIEVED in synthetic,
  this run extends to real-ckpt evidence)
