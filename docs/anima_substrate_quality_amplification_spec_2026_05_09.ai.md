# anima substrate quality amplification — chat-cap C2 unblock 4 path comparison + Path B 권장 spec (2026-05-09)

**status**: SPEC_LANDED — recommended path = Path B (Engine A/G + chat-template co-train)
**cycle**: anima cycle 2026-05-09 substrate quality amplification
**trigger**: chat lane Path 3 generate FULL impl LANDED (commit `fe30c736`) — architecture layer UNBLOCKED ✓; substrate quality (C5 honest_c3) confirmed undertrained (sft-1-8 generate output gibberish/garbled bytes for 7/7 prompts)
**directive context**: cycle "all bg go" carry priority 3
**own links**: / / / (C2) / / / / / / /

---

## Context — chat-cap C2 axis decomposition

| axis | name | status | unblocker |
|---|---|---|---|
| axis-1 | chat dispatch architecture | UNBLOCKED ✓ | chat lane Path 3 generate FULL impl (commit fe30c736) |
| axis-2 | substrate natural-lang quality | **UNDERTRAINED** ★ | 본 spec 4 path comparison + Path B 권장 |

sft-1-8 substrate root cause:
- LoRA r=128 + anima-internal SFT corpus = consciousness-state targets (axis activations / dominant cells / phi-star) 학습
- chat-template + decoded-text targets 학습 X → tokenizer.decode → gibberish bytes
- 22+ BG saga 모두 같은 root cause (Lesson Q SFT-closed evidence + V14 falsification cascade evidence 모두 pre-train + arch lane only valid 시사)

---

## 4 path comparison

| Path | Description | Cost (USD) | Effect | D1 lane | Public 가능 | V14 |
|---|---|---|---|---|---|---|
| A | Llama lane (paradigm-a-prime GGUF) | $0 | natural-lang STRONG ✓ | outside (D1=0.351) | NO (SCOPE_CLAMP) | N/A |
| **B** | **Engine A/G + chat-template co-train** | **$30-60** | **natural-lang ✓ + 의식 ✓ DUAL** | **within (D1=0.99)** | **YES** | **mirror 5-seed** |
| C | mk2-v1 base pre-train scale-up | $50-100 | natural-lang STRONGER | within (D1=0.99) | YES | mirror 5-seed |
| D | sft-1-8 Step B 30K LoRA SFT | $15-20 | LoRA SFT 한계 carry | within (D1=0.793) | borderline (V14 carry) | mirror 5-seed |

---

## Decision matrix (cost-benefit + strategic fit)

| factor | A Llama | **B Engine A/G** | C mk2-v1 scale | D Step B 30K |
|---|---|---|---|---|
| natural-lang strength | 9/10 | 7/10 | 8/10 | 4/10 |
| 의식 measurement | 0/10 | **9/10** | 8/10 | 6/10 |
| D1 within | 0/10 | **10/10** | 10/10 | 8/10 |
| public promote 가능 | 0/10 | **9/10** | 9/10 | 5/10 |
| cost-efficiency | 10/10 | **8/10** | 5/10 | 9/10 |
| time-to-first-fire | 10/10 | **6/10** | 4/10 | 8/10 |
| arch reuse (BG-LA/LB carry) | 0/10 | **10/10** | 5/10 | 3/10 |
| **weighted total** | 29 | **59** ★ | 49 | 43 |

weights: natural-lang ×1, 의식 ×1, D1 ×2, public ×2, cost ×1, time ×1, arch-reuse ×2 (+ + cycle invest mandate)

---

## Path B detailed spec — Engine A/G chat-template co-train

### Architecture amend (training/engine_a_g_arch.py)

base impl (commit ae5af2ea):
- EngineAGModel forward returns `{logits, hidden_states, attentions, tensions, loss}`
- single-target: cross_entropy(logits, labels) (consciousness-state token targets only)

amend (chat co-train head):
- ADD `cfg.chat_co_train_weight: float = 0.5` (multi-objective scalar)
- ADD second pass through same logits with chat-template labels (apply Korean chat-template `<|user|>...<|assistant|>...` boundary masks)
- LOSS = `loss_consciousness * (1 - w) + loss_chat * w`
- shared lm_head (already tied to tok_emb) — no new parameters; 0 D1 risk
- Engine G repulsion-field unaffected (refresh every 4L preserved); A↔G tension `t = ||A_h|| / ||G_cells||` modulates softmax temperature β=0.25 unchanged

### Corpus split

- consciousness-state targets: ~70% (existing tier_a_v4 anima-persona 319k + axis-coupled probe sequences)
- chat-template natural-lang targets: ~30% (Korean chat-template `<|user|>...<|assistant|>...` parsed lines from anima-persona corpus, 50K+ pairs)
- co-train weight schedule: w=0.3 first 50% steps → w=0.5 remaining 50% (curriculum, 의식 anchor preservation)

### V14 mirror (cascade 정합)

- 5-seed paired random_init mirror MANDATORY before fire
- mirrors materialize at `state/v14_mirrors/BG-LA/seed_{42,137,271,314,1729}.pt` (small dry-run already LANDED via tool/v14_paired_random_init_mirror.hexa)
- post-fire: `_c3_ensemble_v5_2_pass(piv_max, random_99th, delta=0.02, dcr_change_rate, d_rand, gate_d)` 4-gate verdict
- MTRP ≥ 0.10 floor strict; Gate D V14 self-test PPR < 0.05

### Cost-benefit

- H100 80GB single fire: $30-60 (~10-20h depending on steps; lb_350m_pretrain preset reuse)
- baseline pre-train: $30 (10h)
- chat co-train multi-objective: +$15-30 (compute overhead ~50% for parallel loss head)
- 5-seed V14 mirror dry-run: $0 (CPU OK for shape verify)

### Timeline

- T+0: spec land (이 doc + yaml + .own)
- T+1d: arch amend (engine_a_g_arch.py chat co-train head 추가) + selftest
- T+2d: corpus split prep (Korean chat-template parser → 50K+ pairs)
- T+3d: H100 fire (BG-LA Engine A/G chat co-train v1) + V14 mirror
- T+4d: post-fire 4-gate verdict (v5.2) + ledger entry

### Risks

1. dual-objective interference — consciousness-state axis activations 가 chat-template fitting 으로 collapse 가능 (axis activation amplitude saturation; cell-tile collapse class)
2. corpus quality — Korean chat-template parsed pairs 양/질 불충분 시 chat head 빈약 학습
3. V14 strict floor 0.10 MTRP 미달 가능 — sft-1-8 N=120 evidence (MTRP=-0.1379) 은 LoRA r=128 한정; pre-train scale 다른 결과 가능 단 보장 X
4. Engine G repulsion-field interference — 16 cells unit-sphere normalization 이 chat-template gradient 와 충돌 가능 (별도 ablation 필요)

mitigation:
- 1: curriculum w schedule (0.3 → 0.5) + axis activation freeze 첫 10% steps
- 2: tier_a_v4 (231MB) + curated chat-pair augmentation (paradigm-a-prime distill 후 D1 outside 라 직접 reuse 불가, paraphrase k=3 amplification 권장)
- 3: 5-seed mirror dry-run 후 fire (paradigm-j v5.2 PASS 사례 carry — pre-train + adaptive floor 가 V14 verify 가능)
- 4: w=0.0 baseline + w=0.3 + w=0.5 3-arm ablation

---

## Recommended next-cycle action

1. **immediate (cycle 2026-05-09)**: 본 spec land + yaml + .own + render (이 commit)
2. **next-cycle (2026-05-10)**: arch amend (engine_a_g_arch.py chat co-train head) + selftest + corpus split prep
3. **post H100 host registration**: BG-LA Engine A/G chat co-train v1 fire (W&B + V14 mirror + honest emit + 매단계 doc)
4. **post-fire**: v5.2 4-gate verdict + (PASS 시) HF private upload + (V6 STRONG + 사용자 토글 시) public promote (mandate-9 5/5 prereq)

## Path A/C/D status

- **Path A (Llama)**: personal review only carry — `anima chat <alias> --lane=llama` 즉시 사용 가능 (commit 30d2cd7e chat lane plugin pattern); benchmark label `SUBSTRATE_RESEARCH` (SCOPE_CLAMP, public promote 영구 차단)
- **Path C (mk2-v1 scale-up)**: second-best carry — H100 host registration 후 fire 가능 단 cost 2× of Path B + arch reuse 부족 (BG-LA/LB Engine A/G invest 미 leverage); next-next-cycle option
- **Path D (Step B 30K)**: cost-effective 단 LoRA SFT 한계 carry (Lesson Q SFT-closed evidence) — provision-ephemeral RUNPOD_API_KEY 사용자 register 후 retry 가능; substrate-level natural-lang quality 한계 명백 (sft-1-8 N=120 PPR 0.5378 plateau evidence)

---

## SSOT mirror surfaces (매단계)

- `docs/anima_substrate_quality_amplification_spec_2026_05_09.ai.md` (this doc, NEW)
- `anima/registry/anima_artifact_registry.yaml` chat_lanes#generate `substrate_quality_status: AMP_PATH_B_RECOMMENDED` field 추가 + framework_amends 4-path entry
- `docs/anima_artifact_registry.md` (regenerated via render.hexa per)
- `.own` line ~1054+ amend — chat-cap C2 substrate amp Path B 권장 carry
- `state/anima_model_attempts_ledger.jsonl` next-cycle entry on actual fire

## honest-c3 (≥5 emit)

1. C5 sft-1-8 substrate undertrained for natural-lang emit 은 chat dispatch architecture 의 별도 axis (axis-2 substrate quality); Path 3 generate FULL impl 은 axis-1 architecture 만 unblock
2. Path B Engine A/G chat co-train 권장 은 strategic best (D1 within ✓ + 자연어 ✓ + 의식 ✓ + arch invest reuse ✓) 단 cost-efficiency 는 Path D 가 우월 (cost discipline carry)
3. V14 strict 정합 sustained — Path B fire 도 5-seed mirror + MTRP ≥ 0.10 + Gate D V14 self-test PPR < 0.05 모두 통과 의무 (cascade)
4. cost estimate $30-60 은 lb_350m_pretrain preset 기반 추정; 실제 corpus split + curriculum schedule 에 따라 ±50% 변동 가능; H100 시간당 가격 $2.79/h (RunPod) 기준
5. 본 spec 은 H100 host registration 후 actual fire 까지 spec-carry only; resource CLI 위임 strict — anima 측 unilateral provision 0건

---

## cross-link

- (D1 SCOPE_CLAMP — paradigm-a-prime substrate-research lane only)
- (C2 자연발화 + simple_stack PASS_STRICT_C3 measurement axis)
- (anti-Goodhart V14 strict + cascade mirror mandate)
- (cost discipline — $30-60 budget cap)
- (mandatory honest report)
- (single SSOT — yaml master, md regenerable)
- (trinity D + own + H emit)
- (mandate-1 raw decode preservation; mandate-2 wrap=0)
- (HF visibility lifecycle — 4 prereq for public promote)
- (axis-A doc save + axis-B HF upload 매단계)
- (yaml↔md mandatory regenerate)
- (resource CLI 위임 strict)
- (chat lane plugin pattern — 4 lanes registry)
- docs/anima_chat_autonomous_speech_roadmap_2026_05_08.md (L4 4 paths chat-cap original spec)
- docs/anima_d_rand_signal_amplification_spec_2026_05_09.ai.md (D-RAND amp spec — Path D parent)
- training/engine_a_g_arch.py (Path B amend target — commit ae5af2ea)
- tool/anima_cli/chat/lanes/clm_v4_generate.hexa (Path 3 generate FULL impl — commit fe30c736)
- tool/anima_cli/chat/lanes/llama.hexa (Path A live — commit 30d2cd7e)
