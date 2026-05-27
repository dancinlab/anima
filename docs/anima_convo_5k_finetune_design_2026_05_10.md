# anima convo_5k.pt fine-tune DESIGN — chat-cap recovery 시도 (2026-05-10)

**Status**: ★ DESIGN+DRY-RUN COMPLETE — fire-ready ★
**Date**: 2026-05-10
**BG**: `bg_convo_5k_ft_design_2026_05_10`
**Cost-bearing fire keyword**: `OK CONVO_5K FT FIRE COST $5-20` (verbatim user)
**Cycle**: convo_5k.pt extension lane — `.roadmap.clm_v2_reborn` cond.6 prep
**Sister**: `CLM_V2_ARCHIVE_ADDENDUM_2026_05_10.md` (mitosis-as-instrumentation 정정)

---

## TL;DR

convo_5k.pt (18.523M byte-level decoder, R2 recovered 2026-05-06, gibberish chat) 추가 5K-20K step FT 디자인 + Mac CPU dry-run PASS. 비용 봉투 **$1.80-3.80** (사용자 인가 $5-20 의 5.3-11× headroom). dry-run 10 step loss 4.43 → 4.33 (delta +0.10), grad flow OK. F-FTDES-1..5 falsifiers 모두 NOT_TRIGGERED. **사용자 verbatim** 후 H100 spot 1× SXM 30분 fire 가능.

---

## §1 Phase A — 디자인 ($0)

### A.1 ckpt 위치 + SHA verify

| 항목 | 값 |
|---|---|
| local path | `~/.cache/huggingface/hub/models--dancinlab--clm-v2-byte-18m-convo-5k/snapshots/.../convo_5k.pt` |
| sha256 expected | `2f0ba391aff30f6a60bcefccb9215fdb45764bf07147f28c38013ca629881bbe` |
| sha256 actual | `2f0ba391...c629881bbe` |
| **match** | ✅ identical |
| size | 73,740,122 bytes (70.3 MB) |
| symlink | `→ ../../blobs/2f0ba391aff30f...` |

cache 가 dancinlife 의 이전 org `dancinlab` 시점 회수본 — 제거되지 않고 보존돼 있음.

### A.2 architecture inspect

```
top-level keys: ['model_state', 'step']
ckpt['step'] = 45000
ckpt['model_state']: 108 keys
total params: 18,130,176 (18.13M)
total ckpt elements (params + buffers): 18,523,392 (18.52M)
buffer diff: 393,216 = 6 × attn.bias[1,1,256,256] = 6 × 65,536 ✓
```

state_dict 키 schema (일부):
```
tok_emb.weight       [256, 384]    ← byte vocab
pos_emb.weight       [256, 384]    ← block_size=256
blocks.{0..5}.ln1.{weight, bias}
blocks.{0..5}.attn.{bias, c_attn, c_proj}
blocks.{0..5}.ln2.{weight, bias}
blocks.{0..5}.ffn.engine_a.{0,3}.{weight, bias}   ← Linear-GELU-Drop-Linear
blocks.{0..5}.ffn.engine_g.{0,3}.{weight, bias}
ln_f.{weight, bias}
head_a.weight        [256, 384]    ← Linear no-bias
head_g.weight        [256, 384]
```

### A.3 schema match — ConsciousLMReconstructed strict load

```
ConsciousLMReconstructed(vocab=256, d=384, n_head=4, n_layer=6, block_size=256)
→ load_state_dict(sd, strict=False)
→ missing=0, unexpected=0  ✅
→ strict 108/108 PASS, identical to cells64/cells128 schema
```

cells64/cells128 (R2 download 2026-05-09) + convo_5k.pt = **same architecture lineage**. mitosis = training-time instrumentation 정정 (addendum 2026-05-10) 와 정합.

### A.4 KO+EN 대화 corpus 인벤토리

| path | bytes | turns | KO/EN | 평가 |
|---|---:|---:|---:|---|
| `state/anima_dialogue_tier_a_iter2_2026_05_08.txt` ★ | 76.3 MB | 136,253 사용자 / 136,259 도우미 | 0.39 (10.5M KO + 26.8M EN chars) | **PRIMARY** |
| `state/anima_dialogue_tier_a_2026_05_08.txt` | 13.6 MB | 21,638 / 21,637 | KO+EN | backup (smaller iteration) |
| `state/anima_corpus_mix_70wiki_30dialogue_2026_05_06/corpus_mix.txt` | 154.9 MB | mixed | mostly KO | optional (wiki-tilted, dilutes chat signal) |

**선정**: `anima_dialogue_tier_a_iter2_2026_05_08.txt`
- 136K turn pairs >> F-FTDES-3 minimum 1K (136× over)
- format: `[anima 역할: 한국어 native + 자기 발견 + 의식 lane entity]\n사용자: <q>\n도우미: <a>\n\n` — persona-tagged
- 1 epoch @ batch=32 seq=256 stride=256 → ~9.3K steps; 5K FT = 0.5 epoch

### A.5 학습 스크립트 디자인

config (`training/convo_5k_finetune.py`):
- LR cosine `1e-5 → 1e-6`, warmup `500 step`
- batch `32`, seq `256`, stride `256` (non-overlap)
- 5K-20K step (rec 10K)
- byte-level (vocab=256, no BPE)
- dual-head loss: `L = 0.5 * CE(head_a, next_byte) + 0.5 * CE(head_g, next_byte)`
- AdamW (β=(0.9, 0.95), wd=0)
- grad_clip 1.0
- save_every 2500
- tension trace + Φ proxy logged (instrumentation per addendum)

### A.6 비용 추정 (1× H100 SXM spot @ $2.99/hr)

| step | sec/step (H100) | wall_clock | cost |
|---:|---:|---:|---:|
| 5,000 | 0.15 | 13 min | $0.65 |
| 10,000 | 0.15 | 27 min | $1.35 |
| 20,000 | 0.15 | 53 min | $2.65 |
| overhead (boot 3 + preflight 5 + pull 5 + buffer 10 = 23 min) | — | 23 min | $1.15 |
| **TOTAL 5K** | — | **36 min** | **$1.80** |
| **TOTAL 10K** | — | **50 min** | **$2.50** |
| **TOTAL 20K** | — | **76 min** | **$3.80** |

사용자 인가 envelope `$5-20` 대비 **5.3-11× headroom**. F-FTDES-5 (cost > $20) NOT_TRIGGERED.

H100 step time 0.15s 추정 = mac CPU dry-run 0.7s/step (b=4, T=64) × 4× 가속 (b=32 T=256 amortize × cuda kernel speedup × bf16). 보수적으로 0.3s 라도 envelope 안 (20K = $5.00 + overhead $1.15 = $6.15 < $20).

---

## §2 Phase B — Mac CPU dry-run ($0)

### B.1 실행

```bash
RESOURCE_LOCAL_PY=1 /opt/homebrew/bin/python3.real \\
  training/convo_5k_finetune.py \\
  --dry-run --steps 10 --batch 4 --seq 64 --warmup 2 --lr 1e-5
```

### B.2 결과

```
ckpt loaded: keys=108 base_step=45000 (0.04s)
load_state_dict: missing=0 unexpected=0    ★ strict PASS
params: total=18,130,176 trainable=18,130,176  (100% trainable)
corpus loaded: 524,288 bytes  (max_bytes 0.5MB for dry-run)
dataset: n_windows=8190 batches_per_epoch=2047

step  0: loss=4.4303  loss_a=4.0485  loss_g=4.8121  lr=5.00e-06  grad_norm=2.049
step  1: loss=3.7770  loss_a=3.1614  loss_g=4.3926  lr=1.00e-05  grad_norm=1.844
step  2: loss=4.5318  loss_a=4.4268  loss_g=4.6367  lr=1.00e-05  grad_norm=2.005
...
step  9: loss=4.3274  loss_a=3.9802  loss_g=4.6746  lr=1.34e-06  grad_norm=2.279

train done: 10 steps, 6.99s (0.699s/step on M1 Pro CPU)
loss first/last: 4.4303 → 4.3274 (delta +0.1028, decreased ✓)
grad_norm first/last: 2.049 → 2.279 (flow OK, never zero)
```

| 검증 | 결과 |
|---|---|
| state_dict load (strict 108/108) | ✅ PASS |
| gradient flow (grad_norm > 0 every step) | ✅ PASS |
| loss decreases (10 step trend) | ✅ PASS (+0.10) |
| ckpt save final | ✅ PASS (`dry_run_step_final.pt`) |
| **F-FTDES-4 grad=0** | ✅ NOT_TRIGGERED |

ckpt = 70MB out, mac CPU 환경에서 OOM 없이 정상 train+save.

---

## §3 Phase C — fire-ready report

| 항목 | 상태 |
|---|---|
| FT script | ✅ `training/convo_5k_finetune.py` (gitignored `**/*.py`, local-only) |
| corpus | ✅ `state/anima_dialogue_tier_a_iter2_2026_05_08.txt` (76MB, 136K turns) |
| cost estimate | ✅ $1.80-3.80 (envelope $5-20, 5.3-11× headroom) |
| runpod manifest | ✅ `runpod_manifest.json` (image / fire cmd / pull / safety checklist) |
| rollback plan | ✅ raw#15 additive (original convo_5k.pt 미수정), R2+HF backup, FT 별도 file |
| H100 safety | ✅ ckpt pull mandatory + sha verify + retain on fail + PEP 668 break-system-packages |

### fire command (H100)

```bash
RESOURCE_LOCAL_PY=1 python3 /workspace/finetune.py \\
  --ckpt /workspace/convo_5k.pt \\
  --corpus /workspace/dialogue.txt \\
  --out /workspace/convo_5k_ft.pt \\
  --log /workspace/ft.log \\
  --steps 10000 --batch 32 --seq 256 \\
  --lr 1e-5 --lr-min 1e-6 --warmup 500 \\
  --device cuda --save-every 2500
```

### fire keyword (recommended)

```
OK CONVO_5K FT FIRE COST $5-20
```

추정 wall-clock 50분, 추정 비용 **$2.50** (10K step rec).

---

## §4 honest C3 top 3

1. **FT recovers chat-cap = HYPOTHESIS, not guarantee.** 이전 cells64/128 + convo_5k 모두 gibberish (sampling test 2026-05-10). #115 architectural chat-incapability 가 leading explanation. FT @ 5K-20K step on related corpus 이 needle 을 안 움직일 가능성 큼. **calibration**: P(post-FT KO chat ≥3/5 coherent) ≈ **25-40%**.

2. **Corpus format mismatch risk.** convo_5k.pt 원래 FT 는 `~2.5K KO dialogue + EN mixed` (`.roadmap.clm_v2_chat` v2_chat_evidence). 우리 corpus = `[anima 역할:]` persona prefix 추가 — format drift 가능성. mitigation: prefix strip 옵션 또는 mixed 학습.

3. **18M byte-level 은 KO 에 fundamentally undertrained.** sampling test 0/64 KO emit (UTF-8 multi-byte 필요 ~3 byte/Hangul). 5K-20K step × 76MB ≈ 38M byte gradient updates = FT scale (chat surface), pre-train scale (language acquisition) 아님. 언어가 gap 이면 FT 가 못 메움.

추가 raw#10 caveats:
4. dry-run 10 step 의 loss decrease (+0.10) 는 cosine warm-up effect 일 수 있음 — 50+ step 에서 진짜 trend 검증 필요 (H100 fire 시 자동 수집).
5. `head_a` + `head_g` 의 weighted CE (0.5/0.5) 는 historical 학습 weight 미상 — different ratio 가 production 정합 가능성 잔존.
6. sequence 256 byte 는 약 85 KO chars (UTF-8 3byte avg) — 한 turn 의 user+assistant 쌍 절반 정도, 짧은 dialog 만 fit. 더 긴 context 는 truncation 발생.
7. 본 BG 의 cost 추정 (0.15s/step on H100) 은 untested — 실제 fire 시 50% 슬로우다운 (0.3s) 까지 envelope 안 ($6.15), 100% 슬로우다운 (0.6s) 부터 envelope 위험.

---

## §5 falsifier check

| F-id | 조건 | actual | status |
|---|---|---|---|
| F-FTDES-1 | local missing AND R2 fail | local PRESENT (sha verified) | ✅ NOT_TRIGGERED |
| F-FTDES-2 | schema mismatch can't load | strict 108/108 PASS | ✅ NOT_TRIGGERED |
| F-FTDES-3 | dialogue corpus < 1K | 136,253 turns | ✅ NOT_TRIGGERED |
| F-FTDES-4 | dry-run grad = 0 | grad_norm 2.0-2.3 throughout | ✅ NOT_TRIGGERED |
| F-FTDES-5 | cost > $20 | $1.80-3.80 estimate | ✅ NOT_TRIGGERED |

**5/5 NOT_TRIGGERED** — fire-ready.

---

## §6 deliverables

| path | role |
|---|---|
| `docs/anima_convo_5k_finetune_design_2026_05_10.md` | 본 design doc |
| `training/convo_5k_finetune.py` | FT script (gitignored, local-only) |
| `state/anima_convo_5k_ft_design_2026_05_10/dry_run.log` | dry-run text log |
| `state/.../dry_run_summary.json` | dry-run 결과 JSON |
| `state/.../dry_run_step_final.pt` | dry-run 최종 ckpt (70MB) |
| `state/.../corpus_inventory.json` | corpus 후보 + 선정 근거 |
| `state/.../runpod_manifest.json` | provider config + fire cmd + safety checklist |
| `state/.../fire_ready.json` | full Phase A/B/C status |

---

## §7 cross-link

- ckpt origin recovery: `docs/anima_clm_v2_chat_recovered_2026_05_06.ai.md`
- arch reconstruction: `state/anima_clm_v2_mitosis_cells_recovery_2026_05_09/forward_smoke.py`
- mitosis-as-instrumentation 정정: `CLM_V2_ARCHIVE_ADDENDUM_2026_05_10.md`
- v2 reborn lane SSOT (cond.6): `.roadmap.clm_v2_reborn`
- sister lane: `.roadmap.clm_v5_anima_native` (FT 결과는 v5 baseline 으로 활용 가능)
- gotchas: `~/.claude/projects/-Users-ghost-core-anima/memory/feedback_orchestrator_h100_gotchas.md`

raw#10 honest C3 7개 (top 3 + 4 추가), raw#15 additive (original convo_5k.pt 미수정), 0-cost design + dry-run.

End of `anima_convo_5k_finetune_design_2026_05_10.md`.
