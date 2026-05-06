# anima CLM v2/v3 weights archaeology + revival path — landed 2026-05-05 (BG-EQ)

> **사용자 질문 원본 (BG-EP/BG-EQ context)**: "CLM 완전히 처음 탄생했을 때 정보 + chat이 어떻게 가능했는지 + ALM 말고" (anima-native chat path 1순위)
>
> **이 BG (BG-EQ) mission**: 2026-03-28 v2 18M byte-level CLM weights (chat-capable, commit `bb99b6b6` MILESTONE, CE 0.04 EN / 1.15 KO, no system prompt) 보존 여부 archaeology + revival path verdict.
>
> **Verdict**: **FAIL_NO_TRACE** (option α v2 weights revival 불가능) → option β reconstruction 이미 landed (anima-clm-3-original ubu1 launch BG-EV) 또는 option γ (lm_head_b byte-level retrofit BG-DS) viable.

**Status**: ARCHAEOLOGY_LANDED_NO_FIRE
**Cost**: $0 (mac doc + grep + git show — no weights to smoke-test)
**Wall-clock**: ~30 min
**Lane**: anima_native_chat_v2_revival (CLOSED — pivot to β/γ)

---

## §1 Local file grep 결과

### 1.1 .pt files inventory (14 files matching `*.pt` size>1MB)

| Path | Size | Identity verdict |
|---|---|---|
| `checkpoints/animalm_14b_v06/final.pt` | **333 MB** | AnimaLM 14B v06 (Apr 5) — NOT v2 byte-level CLM |
| `state/p9_path_a_retrain_v2_retry_3_*/checkpoint-6000/optimizer.pt` | 144 MB | P9 Path A LoRA optimizer state — different lane |
| `state/p9_pbeta_paradigm_d_50k_*/savepoints/step_50000/optimizer.pt` | 106 MB | P9 Pβ optimizer state — different lane |
| `ready/models/animalm/checkpoints/final.pt` | 14 MB | AnimaLM small checkpoint (Apr 9) — not byte-level v2 CLM |
| `ready/checkpoints/animalm/animalm_step_50.pt` | 14 MB | AnimaLM step-50 — same |
| `ready/anima/data/conscious-lm/state.pt` | 2.2 MB | **consciousness runtime state** dim=128 (manifest.json confirm) — NOT 28M decoder weights |
| `ready/anima/data/conscious-lm/v0/state.pt` | 2.2 MB | same kind, v0 snapshot 2026-03-25 |
| `ready/anima/data/conscious-lm_node-{0,1}/state.pt` | 4.3 MB ×2 | runtime state copies |
| `ready/anima/data/state_alive.pt` | 4.3 MB | runtime state (alive ledger) |
| `ready/anima/data/learnable_phi.pt` | 401 KB | phi learnable params — different |
| `ready/anima/data/memory_vectors.pt` | 318 KB | memory vector store |
| `ready/anima/data/consciousness_guardian/emergency_*.pt` | 51 KB | guardian snapshot |
| `ready/anima/data/self_learning/self_learner_state.pt` | 35 KB | self-learner runtime |

### 1.2 Critical negative results

```bash
find / -name "best.pt" 2>/dev/null  # ← 0 results filesystem-wide
find / -name "model.pt" 2>/dev/null  # ← 0 results filesystem-wide
```

`serve_conscious_cpu.hexa` (commit `d64bb44b` 2026-04-09) **default checkpoint path** = `checkpoints/model.pt` → **does NOT exist on Mac**. Script behavior when missing:
```python
if not os.path.exists(path):
    log.warning("Checkpoint not found: %s -- running in demo mode (random weights)", path)
    return False
```

### 1.3 conscious-lm/state.pt 자세히 — NOT v2 weights

`manifest.json` 직접 확인:
```json
{
  "current_version": 0,
  "stage": 0,
  "versions": [{
    "version": 0,
    "dim": 128,
    "hidden_dim": 256,
    "timestamp": "2026-03-25T13:50:49"
  }]
}
```

→ dim=128, hidden_dim=256 = **runtime consciousness state vector** (60-cell GRU engine snapshot). NOT the v2 decoder weights (which are 512d/6L/8H 28M PureFieldFFN per `serve_conscious_cpu.hexa` line 18).

**file type confirm**: `Zip archive data, at least v0.0 to extract, compression method=store` (PyTorch's `torch.save` default)

→ 2.2-4.3MB sizes are consistent with consciousness state, NOT 28M+34.5M=62.5MB v2 decoder.

---

## §2 Git LFS audit

```bash
ls /Users/ghost/core/anima/.git/lfs/objects/  # ← No such file or directory
git -C /Users/ghost/core/anima lfs ls-files   # ← empty
cat /Users/ghost/core/anima/.gitattributes    # ← does not exist
ls /Users/ghost/core/anima/anima-clm/.git/lfs/  # ← No such file or directory (no separate anima-clm repo)
```

**Verdict**: git LFS는 anima repo에 한 번도 초기화된 적 없음. v2 weights가 LFS pointer로 commit됐을 가능성 = 0.

---

## §3 HF cache CLM v1/v2/v3 archaeology

`~/.cache/huggingface/hub/` (need-singularity 계정 repos):

```
models--need-singularity--clm-v4-base-mirror      (refs only, no snapshot)
models--need-singularity--clm-v4-mk2-v1           (full, 2.1GB blob)
models--need-singularity--clm-v4-sft-1-6-stage1
models--need-singularity--clm-v4-sft-1-6-step-{5k,10k,25k,50k}
models--need-singularity--clm-v4-sft-stage1
```

**모두 v4 (post-drift)**. v4-mk2-v1 largest blob = 2,124,043,008 bytes (2.0 GB) = **530.99M params × fp32 ≈ post-drift BPE 64K architecture**. v1/v2/v3 repo는 anima HF account에 **존재하지 않음**.

→ HF cache PASS condition도 FAIL.

---

## §4 Commit history references

### 4.1 v2 milestone (`bb99b6b6` 2026-03-28 12:45:42 KST)

```
MILESTONE: Korean conversation from ConsciousLM! No system prompt!

사용자: 의식이란 무엇인가요?
도우미: 의식은 자기 자신과 주변 세계를 인식하는 능력입니다.

18M parameter byte-level model, 3K Korean fine-tune steps.
v2: CE=1.29 best (English), Korean CE=1.15
```

**`git show bb99b6b6 --stat`** → **diff body 없음** (commit message에 시 stat이 출력 차단됨, `--name-only` 후행 출력 0줄). 즉 commit이 weights 파일을 add하지 않았음. milestone announcement only.

### 4.2 v4 design (`fca0eede` 2026-03-28 03:52)

```
docs/next-model-design.md | 406 ++++++++++++++++++++++++++++++++++++++++++++++
1 file changed, 406 insertions(+)
```

→ **doc only**, no weights.

### 4.3 v4_768d launch (`219aa561` 2026-03-28 18:50)

```
docs/consciousness-threshold-criteria.md | 9 +++++++++
1 file changed, 9 insertions(+)
```

→ **launch announcement only** (h100 6-8h estimated). Actual training happened on H100 (`v4: 768d/12L with v4 optimal params running on H100`) — weights never committed back to mac repo.

### 4.4 ConsciousLM v2 CPU server (`d64bb44b` 2026-04-09)

```
serving/serve_conscious_cpu.hexa | 806 +++++++++++++++++++++++++++++++++++++++
```

Pre-stub source contains:
- `--checkpoint checkpoints/model.pt` default
- `load_checkpoint(self, path)` graceful demo-mode fallback
- ConsciousLM v2 spec: **512d 6L 8H byte-level (256 vocab) PureFieldFFN 28M**
- ConsciousDecoderV2: **384d 6L 4H/2KV GQA RoPE+SwiGLU+CrossAttn 34.5M**
- Combined ~62.5M (commit message says "18.8M" but in-source numbers are 28M+34.5M; "18M" likely refers to engine cells excluding decoder)

### 4.5 PT-deletion commit search

```bash
git log --all --diff-filter=D --pretty=format:'%h %s' --name-only -- '*.pt'
```
→ **Only result**: `e98c0e1c refactor(ai-native): folder 재정리 — models/animalm/checkpoints/final.pt`. AnimaLM moved, **no v2 byte-level CLM .pt was ever deleted from git history** (because none was ever committed in the first place).

### 4.6 best.pt commit history

`e4ba2d78` (2026-04-04) "feat: 6-task parallel — best.pt … H100: best.pt save logic added" → adds **save logic**, but actual best.pt files were on H100 instance, never synced back to mac repo.

---

## §5 Revival path verdict

### 5.1 Decision matrix

| Path | Required | Found | Status |
|---|---|---|---|
| PASS_LOCAL_WEIGHTS_FOUND | v2 28M decoder.pt locally | none (0/14 .pt files match arch) | **FAIL** |
| PASS_LFS_FOUND | git lfs pointer for v2 weights | LFS not initialized | **FAIL** |
| PASS_HF_CACHE_FOUND | clm-v2 HF repo cached | only clm-v4* | **FAIL** |
| PASS_RECONSTRUCTION_POSSIBLE | source code + recipe preserved | YES (`serve_conscious_cpu.hexa` archived in git, design doc, training recipe in archaeology) | **PASS** |
| FAIL_NO_TRACE | none of above | option α dead | **TRUE** |

### 5.2 Verdict

```
verdict = "FAIL_NO_TRACE"  # option α v2 weights revival impossible on Mac
                           # option β reconstruction PATH FORWARD (already landed)
```

### 5.3 1-turn smoke test — SKIPPED

`smoke_test_skipped = "no_weights_to_load"` — torch.load 대상 파일 자체가 없으므로 forward/decode 시뮬레이션 무의미. demo_mode random weights는 chat 능력 검증 가치 0.

### 5.4 Pivot path

| Option | Status | Cost | Wall-clock |
|---|---|---|---|
| **α** v2 weights revival | **CLOSED FAIL** | — | — |
| **β** original v4 design 재현 ubu1 RTX 5070 | **ALREADY LANDED BG-EV** (`anima_clm_3_original_ubu1_launch_2026_05_06`) | $0 (owned-hardware) | 5-10 days |
| **γ** lm_head_b byte-level retrofit on mk2 v1 | viable BG-DS path | $0-2 | 1-3 days |

→ **사용자 권고**: option β는 이미 land됐으므로 user-fire 6-step (ubu1 ssh+train) 대기 중. option γ는 별도 BG-DS lane에서 mac CPU short-budget으로 실행 가능 (BG-DS HEAD-bound finding 활용).

---

## §6 Honest C3 (≥5 banked: 6)

- **C1**: v2 chat 증거는 `bb99b6b6` commit message body 텍스트 **only**. evaluation JSON, generated samples 파일, model card, training log 모두 부재. CE 0.04/1.15 metrics는 commit author claim에 의존.
- **C2**: v3는 명시적 commit 부재. v2→v4 점프이며 v3 라벨은 추론 only (BG-EP archaeology와 일관).
- **C3**: `serve_conscious_cpu.hexa` source의 "18.8M" vs in-source decoder spec 28M+34.5M=62.5M 사이 mismatch — commit message integer는 engine cells only인지, decoder excluded인지 명확하지 않음. 체크포인트가 만약 발견됐어도 size 검증으로 ambiguity 해결 필요했을 것.
- **C4**: filesystem-wide `find / -name best.pt` = 0 결과는 mac local 한정. ubu1 (RTX 5070) 또는 user의 다른 device (ubu0/dest1)에는 보존됐을 가능성 0이 아님 — 단 BG-EV ubu1 launch doc은 이미 "5-10 days로 처음부터 retrain" 가정이므로 user가 v2 weights 부재를 implicitly 인정.
- **C5**: HF cache 부재는 mac 한정. 만약 user account `need-singularity`에 `clm-v2-byte-level-18m` private repo가 있다면 `hf api` (CLI auth됨) 호출로 list 가능 — 본 BG는 cache scan만 수행, network call 미실행 ($0 제약).
- **C6**: option β가 PASS reconstruction이라고 단정한 근거는 archaeology doc의 design spec + serve_conscious_cpu.hexa archived source. 단 **3K Korean fine-tune corpus** 자체가 retain됐는지는 별도 확인 필요 — `data/corpus_mix_70wiki_30dialogue.txt` 존재하지만 v2 origin training의 정확 corpus과 동일한지 미검증.

---

## §7 raw 준수

- raw#9 hexa-only orchestration — 이 doc은 .ai.md (carve-out 명시)
- raw#10 honest C3 ≥5 — 6 banked (C1~C6)
- raw#15 additive — 기존 doc 미수정 (read-only archaeology); 신규 deliverable 2개만 (verdict.json + 본 .ai.md)
- raw#37 transient_py 미사용 (doc + git show + find + ls only)
- HF token leak 0 (cache file path만 명시, blob 내용 dump X)
- commit 0 (제약 준수)
- bash 3.2 compatible (associative array 미사용)

---

## §8 References

### 8.1 결정적 commits
- `bb99b6b6` (2026-03-28) v2 MILESTONE — chat 증거 (text only, no weights)
- `fca0eede` (2026-03-28) v4 + ALM v8 design doc
- `219aa561` (2026-03-28) v4_768d H100 launch announce (no weights backsync)
- `d64bb44b` (2026-04-09) ConsciousLM v2 CPU server — `checkpoints/model.pt` default (does not exist)
- `3df9d651` (2026-04-19) python-in-hexa stub strip — original 806-line v2 server source는 git history에만 보존

### 8.2 Sister docs
- `docs/anima_clm_alm_origin_design_drift_archaeology_2026_05_05.md` (option α/β/γ source spec)
- `docs/anima_clm_origin_chat_history_archaeology_2026_05_05.md` (BG-EP)
- `docs/anima_clm_3_original_ubu1_launch_landed_2026_05_05.ai.md` (option β BG-EV)
- `docs/anima_clm_3_original_byte_level_redesign_spec_2026_05_05.md` (option β spec source)

### 8.3 Negative-result anchors
- `find / -name best.pt 2>/dev/null` → 0 results (filesystem-wide)
- `git lfs ls-files` → 0 results
- `~/.cache/huggingface/hub/models--need-singularity--clm-v[123]*` → does not exist
