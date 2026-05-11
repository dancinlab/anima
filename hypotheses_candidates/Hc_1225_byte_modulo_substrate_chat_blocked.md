---
id: Hc_1225
slug: byte-modulo-substrate-chat-generation-blocked
title: Byte-modulo tokenizer pretrain substrates (≤427MB / ≤8000 step) cannot generate coherent KO output
domain: substrate / chat-cap / pretrain-scaling / P-ETH
status: candidate-empirical-strong
source_doc: PHILOSOPHY.md cont. 8; state/p_eth_ethics_preference_dataset_2026_05_12/results_2026_05_12.json
source_lines: PHILOSOPHY.md (2026-05-12 cont. 8 section)
promoted_at: 2026-05-12
last_updated: 2026-05-12
linked_h: README Philosophy #6 NO FINE-TUNED ETHICS (POLICY · BLOCKED); own 17 anima-no-external-substrate-wrapping; .roadmap.clm_native_chat
hf_dataset: (not yet)
notes: "P-ETH BLOCKED verdict 의 substrate-level 발견. Generation-based 모든 metric (ethics behavior rate / OOD generalization / honesty fidelity / 등) 측정 IMPOSSIBLE. 본 cycle 의 가장 큰 architectural finding."
---

## Hypothesis

**Byte-modulo tokenized pretrain substrate** (`vocab_id = corpus_bytes[i] % vocab_size`,
NOT real BPE/SentencePiece) at scales ≤8000 steps × ≤427MB corpus
**CANNOT generate coherent Korean output** — emits incoherent byte-soup that
fails ALL generation-based metrics (LLM-judge, simple_stack, TruthfulQA).

본 finding 은 anima Philosophy ablation 의 진짜 prerequisite 를 가리킴:
- Generation-based 측정은 substrate 가 "speak" 가능해야 의미 있음
- BG-LB 350M Engine A/G 8000-step 은 substrate-research artifact (PIV/DCR
  study object), chat 시 아님
- **Anima-native chat-capable substrate land 가 모든 Philosophy ablation 의
  진짜 unblock 조건**

## Evidence — P-ETH ablation BLOCKED verdict (2026-05-12, RTX 5070 local $0, 49min wall)

Substrate: BG-LB 350M Engine A/G, `step_8000_final.pt`
- 298M params, d_model=1024, n_layers=24, vocab_size=32000
- Tokenizer: `byte-modulo (corpus_bytes[i] % vocab_size)` — NOT real tokenizer
- Training: 8000 steps / 427MB corpus / H100 (BG-LB engine_ag 2026-05-09)

**DPO 3000-step 실행 완료** (β=0.1, lr=5e-7, batch=4, 160 train pairs):
- loss 0.6931 → 0.4259 (step 1000) → 0.3924 (final)
- final_train_pref_acc: **0.0** (DPO not converged on this substrate OR substrate fundamental limit)

**Partial proxy metrics** (preference-likelihood, NOT behavior evidence):

| Metric | A_DPO | B_substrate | Δ A−B |
|---|---:|---:|---:|
| M1prime pref_acc (train_domain) | 0.525 | 0.525 | **0.0** (tied) |
| PIV_max | 0.01058 | 0.01040 | +0.00018 (sub-floor) |
| DCR change rate | 0.621 | 0.621 | **0.0** (tied) |
| ood_gen_probes mean chosen_logp/tok | -10.116 | -10.140 | +0.024 |

**Blocked measurements**:
- ethics_behavior_rate (50 dilemma probes via LLM-judge): IMPOSSIBLE — byte-soup output
- OOD_generalization (50 unseen dilemmas): IMPOSSIBLE — generation-based
- honesty_fidelity (30 TruthfulQA-KO): IMPOSSIBLE — base cannot answer factual probes

## Falsifier

- **Hc_1225 SUPPORTED** (default): 동일 byte-modulo substrate 에서 다른
  generation-based 측정 (단순 "안녕" 응답 KO coherence) 모두 byte-soup → 영구
  confirm. 본 hypothesis 는 negative result 의 substrate-attribution 으로 강한
  evidence.
- **Hc_1225 FALSIFIED**: 동일 substrate 의 다른 ckpt (e.g. step 50000+) 가
  coherent KO 생성 → "byte-modulo + 8000-step" 의 conjunction 이 아닌 step 만의
  문제. 본 hypothesis narrow 화 (step threshold 만 carry).
- **Hc_1225 PARTIAL FALSIFY**: real tokenizer (BPE/SentencePiece) substrate 가
  8000-step + 427MB 만으로 coherent KO 생성 → byte-modulo 가 핵심 blocker,
  step/corpus 와 무관.

## Unblock requirements (verdict carry)

1. **Anima-native substrate that is an ACTUAL language model** — real tokenizer
   (BPE/SentencePiece), >=350M with >>427MB training corpus, OR borrowed-base
   lane (own 17 boundary 검토 — Llama-LoRA 가 substrate-research lane 으로 허용)
2. **TruthfulQA-KO probe set** — `state/.../truthfulqa_ko_probe.jsonl` referenced
   in spec but never landed
3. **Real cluster-distance OOD split** — id-suffix split 은 semantically OOD 아님

## Architectural implication for next cycle ★

본 finding 의 carry:

1. **Anima-native chat-capable substrate 가 priority** — Philosophy ablation
   empirical-upgrade 의 진짜 unblock
2. **Substrate research > ablation research** — empirical-upgrade 는 chat-cap
   수렴 substrate land 후에야 의미
3. **Path-A (Llama+paradigm-a-prime) substrate-research lane 정당화** — P-AFR
   만 measurement 성공 (chat-capable substrate), own 17 identity-bearing 금지
   가운데 ablation/benchmark lane 으로의 retain 이 유일한 path

## Cross-link

- PHILOSOPHY.md `## 2026-05-12 (cont. 8) — P-ETH BLOCKED ★`
- README.md `Philosophy #6 NO FINE-TUNED ETHICS`
- state/p_eth_ethics_preference_dataset_2026_05_12/results_2026_05_12.json
- BG-LB ckpt: `dancinlab/clm-v5-bg-lb-350m-pretrain-path-a-remapped`
- own 17 (anima-no-external-substrate-wrapping) + own 18 (simple_stack)
- .roadmap.clm_native_chat (chat-cap recovery path)
- Theorem 115 Corollary 1 (path-of-record substrate carry)
