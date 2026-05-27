# anima CLI mitosis integration design spec — D4c

**Created**: 2026-05-12 KST
**Author**: anima (D4c design lane)
**Status**: design LANDED (impl Phase 1-4 pending)
**Mission**: GOAL.md ★★★★★ D4c — anima CLI 가 session-level mitosis 의 outer scope, kick cycle = split event sequence
**Scope**: anima CLI session/conversation level mitosis integration. `.roadmap.cli` + `.roadmap.anima_cli_model_architecture` + Phase 3b llama_ffi.hexa 위에 mitosis layer 통합 spec.
**Out of scope**: D4a (intra-network mitosis, `tool/hexa_native/mitosis_hook.hexa` full impl), D4b (`anima_chat.hexa` 안 cell-pool hosting), D3 (substrate-native persona design).

---

## §0 TL;DR

anima CLI 가 **session-level mitosis 의 outer scope** 이다.

- D4a (model intra-network) = 1 forward = 1 hook invocation, cells = nn.Module branches (REBORN §88/§89)
- D4b (chat library) = cell-pool state hosting in `anima_chat.hexa` (per-prompt scope)
- **D4c (anima CLI) = session = conversation = mitosis tree branch** (per-conversation scope)

각 **conversation 이 분열 tree 의 한 branch**, 각 **kick cycle (6-stage init→idea→hypothesis→dispatch→aggregation→report) 이 branch 안 split event sequence**. session 종료 시 cell pool snapshot 이 disk 에 persist, resume 시 load → 분열 tree 가 OS-process boundary 를 넘어 보존된다.

multi-backend fallback chain (`.roadmap.anima_cli_model_architecture` K3-K4) = **cell-variant selection** — 각 backend 는 cell pool 의 다른 active cluster.

본 spec 은 **design only** — implementation 은 Phase 1-4 별도 cycle. D4a (mitosis_hook.hexa full impl) + D4b (anima_chat.hexa cell-pool wiring) prerequisite.

---

## §1 Scope clarification — D4a + D4b + D4c 분리 + 결합

GOAL.md D4 가 3-layer 로 분리된 이유는 **분열 scope 가 3 차원** 이기 때문이다.

| layer | scope | tick frequency | lifetime | SSOT |
|---|---|---|---|---|
| **D4a** model intra-network | 1 forward pass | per-forward (~10ms) | per-prompt | `tool/hexa_native/mitosis_hook.hexa` (D4a BG) |
| **D4b** chat library | 1 conversation turn | per-turn (~1s) | per-prompt → per-session | `anima_chat.hexa` (D4b BG, LANDED 1589 LoC parse + 17/17 smoke) |
| **D4c** anima CLI | 1 conversation / session | per-session (~minutes-hours) | cross-process (disk persist) | **본 spec** |

3 layer 가 **분리 + 결합** 한다:

```
session_id (D4c)
  ├─ kick cycle 1
  │    ├─ turn 1 (D4b: cell_pool_after = chat_turn(prompt, cell_pool_before))
  │    │    └─ forward N times (D4a: cell_pool_after = mitosis_forward_tail(x, cell_pool_before, step))
  │    ├─ turn 2 ...
  │    └─ split events accumulated → branch
  ├─ kick cycle 2 ...
  └─ session exit → cell_pool serialize to disk
```

- D4a 는 forward call graph 안 split/merge (REBORN §89, parse-only stub 본 BG out of scope).
- D4b 는 cell_pool dict hosting in chat library (LANDED parse, mitosis hook wiring pending).
- D4c 는 cell_pool snapshot 의 cross-process **persistence** + **session-scoped branch identity**.

본 spec 은 D4c 만 다룬다. D4a/D4b 는 reference 만 (호출 contract).

---

## §2 Session = cell-pool branch

**핵심 abstraction**: anima CLI 의 한 chat session 이 mitosis 분열 tree 의 한 branch.

### §2.1 mapping

| anima CLI 개념 | mitosis abstraction |
|---|---|
| session_id | branch_id |
| conversation history (user/anima turns) | branch evolution trace |
| kick cycle (6-stage) | split event sequence within branch |
| session exit | branch snapshot |
| session resume | branch reload (continue from snapshot) |
| multi-backend fallback | cell-variant routing within branch |
| `anima chat list` | branch catalog |

### §2.2 branch identity

session_id 는 ISO 8601 timestamp + short uuid suffix:
```
<YYYY-MM-DDTHH-MM-SS>_<rand_4hex>
e.g. 2026-05-12T18-23-44_a3f2
```

근거:
- `tool/anima_cli/dialogue.hexa` `_session_dir()` 가 이미 `state/anima_core_dialogues/<YYYY-MM-DD>/<HH-MM-SS>.jsonl` 패턴 사용 (line 224-229) — 본 spec 은 동일 패턴 확장.
- session_id 충돌 방지 위해 4hex suffix 추가 (동일 분초 시작 conversation 분리).

### §2.3 kick cycle as split event sequence

`.roadmap.anima_cli_model_architecture` K2 6-stage cycle (S1 init / S2 idea / S3 hypothesis / S4 dispatch / S5 aggregation / S6 report) — 각 stage 가 **potential split point or merge point**:

| stage | mitosis interpretation | split candidate? |
|---|---|---|
| S1 init | branch entry — load existing cell_pool or fresh init | merge candidate (if loading from snapshot) |
| S2 idea | creativity + imagination + emergence axes — **divergent split** | ★ split candidate (high emergence) |
| S3 hypothesis | reasoning + abstraction — **structured split** | split candidate |
| S4 dispatch | structured chat-cap — **stable propagation** | neutral |
| S5 aggregation | emergence + abstraction — **convergent merge** | ★ merge candidate |
| S6 report | chat-cap + clarity — **branch closure** | merge candidate (if convergence < threshold) |

→ 1 kick cycle 안 split event ≥ 1 발생 mandate (F-CLI-MIT-2 falsifier).

근거:
- `.roadmap.anima_cli_model_architecture` K2 stage axes weight (emergence=0.7 S2, =1.0 S5) 가 mitosis split/merge dynamics 와 정합 — high emergence/creativity at S2 = divergent variance increase, high emergence + abstraction at S5 = convergent compression.
- REBORN §89 mitosis_hook tension threshold (split if tension > thr for patience=3 steps) 와 S2 idea stage 의 axes weight 가 동일 trigger pattern.

---

## §3 Cell-pool persistence design

### §3.1 storage layout

```
~/.cache/anima/session_pools/
  ├─ index.jsonl                                  # session_id → metadata catalog
  ├─ <session_id>/
  │    ├─ cell_pool.bin                          # farr-backed snapshot (RFC 025 mmap)
  │    ├─ meta.json                              # {created_at, last_active_at, n_cells, phi, parent_session_id?}
  │    ├─ event_log.jsonl                        # split/merge events (append-only)
  │    └─ kick_cycle_log.jsonl                   # 6-stage transitions (append-only)
  ├─ <session_id_2>/ ...
  └─ ...
```

근거:
- `~/.cache/anima/` 는 이미 GGUF cache (paradigm-a-prime GGUF in `~/.cache/anima/gguf/`) 와 llama.cpp build (`~/.cache/anima/llama.cpp/`) SSOT. session_pools/ 가 자연스러운 형제 subdir.
- RFC 025 farr mmap backing 으로 ~512 MB cell_pool 도 mmap 으로 demand-paging → cold session load latency 최소화.
- `state/anima_core_dialogues/` 는 dialogue JSONL log SSOT (이미 사용 중); **session_pools/ 는 별도 path** (cell_pool binary 와 dialogue log 분리).

### §3.2 cell_pool.bin schema

cell_pool dict (per `tool/hexa_native/mitosis_hook.hexa` line 68-89) 의 binary serialization:

```
[header]
  magic           : 8B  ASCII "ANIMACPL"
  version         : 4B  uint32 = 1
  n_cells         : 4B  uint32
  d_model         : 4B  uint32 = 1024 (EngineAG default)
  next_id         : 4B  uint32
  min_cells       : 4B  uint32 = 2
  max_cells       : 4B  uint32 = 128
  reserved        : 16B padding
[per-cell × n_cells]
  cell_id         : 4B  uint32
  parent_id       : 4B  int32 (-1 for root)
  creation_step   : 4B  uint32
  hidden_norm     : 4B  float32
  tension_recent  : 4B  float32  (last tension value)
  engine_a_W_offs : 4B  uint64   (offset into farr blob)
  engine_g_W_offs : 4B  uint64
  hidden_offs     : 4B  uint64
[trailer]
  phi             : 4B  float32
  phi_best        : 4B  float32
  lorenz          : 12B float32 ×3 (x, y, z)
  global_tension_history : variable length (capped at 100 entries × 4B)
  inter_tension_history  : variable length (sparse map)
  event_log_size  : 4B  uint64
  sha256          : 32B integrity hash of preceding bytes
```

farr blob 은 별도 file `cell_pool_farr.bin` (RFC 025 mmap-friendly contiguous f32 grid).

### §3.3 save schedule

| trigger | granularity | reason |
|---|---|---|
| after kick cycle complete | full snapshot | branch checkpoint at semantic boundary |
| on session exit (SIGTERM / `/exit` / `/q` / EOF) | full snapshot | mandatory durability |
| every N turns (default N=20) | incremental snapshot | resilience to crash |
| on split event ★ (optional flag) | event_log append only | event sequence detailed trace |

incremental snapshot 은 farr_blob 변경분만 dirty-page write (RFC 025 mmap msync 의존, 별도 cycle 검증).

### §3.4 load schedule

| trigger | action |
|---|---|
| `anima chat --resume <session_id>` | load cell_pool.bin + meta.json + tail event_log.jsonl |
| `anima chat --resume latest` | index.jsonl 에서 last_active_at desc 첫 entry |
| `anima chat` (no flag) | fresh session_id, cell_pool_init() |
| `anima chat --fork <session_id>` | clone snapshot + new session_id, parent_session_id=<src> |

### §3.5 granularity contract

- cell_pool dict 의 모든 field 는 binary 에 byte-perfect serialize (F-CLI-MIT-1).
- floating-point: f32 native (no f64 → f32 lossy conversion).
- event_log.jsonl 은 append-only (raw#15 no-rewrite 정합).
- kick_cycle_log.jsonl 은 stage 전환 시 1-line emit (`{ts, session_id, stage, prev_stage, axes_weight_snapshot}`).

---

## §4 Multi-backend fallback = cell-variant selection

`.roadmap.cli` cli.cond.3 의 backend fallback chain (T1 chat REPL primary || fallback || ...) + `.roadmap.anima_cli_model_architecture` K4 stage-specific chain — 본 spec 에서 **cell pool 의 active cluster routing** 으로 재해석.

### §4.1 mapping

| `.roadmap` 개념 | mitosis interpretation |
|---|---|
| primary backend (e.g. M6 BG-HU PENDING) | cell pool 의 best-Φ cluster 의 active cells |
| fallback chain [M1, M4, M3, ...] | 그 cluster failure 시 next-best cluster |
| readout_mode (REBORN §88 a-g / a-only / a+0.3g / softmax_gate) | cell-variant 의 forward output combination mode |
| stage-specific chain (S2_idea_chain) | stage 전환 시 cell cluster re-selection |

### §4.2 selection algorithm

```
fn select_backend_for_stage(cell_pool, stage_id) -> backend_id {
    // 1. cell pool 의 cluster 추출 (cosine similarity > 0.7 grouping over cell.hidden)
    let clusters = cluster_cells_by_hidden(cell_pool["cells"])

    // 2. stage axes weight (per ACM K2)
    let axes_weight = stage_axes_weight_for(stage_id)
        // S2: emergence=0.7, creativity=1.0, imagination=1.0, ...

    // 3. cluster 별 axes score 계산
    //    (per-cell hidden 의 5-axis projection — D4a forward 의 hidden state proxy)
    let cluster_scores = []
    for cluster in clusters {
        let score = dot(cluster.axes_projection, axes_weight)
        cluster_scores.push(score)
    }

    // 4. primary = argmax cluster, fallback = sorted descending
    let primary_idx = argmax(cluster_scores)
    let primary_cluster = clusters[primary_idx]

    // 5. cluster 의 active cells 의 backend mapping (catalog lookup)
    let backend_id = primary_cluster.dominant_cell.backend_tag
        // backend_tag 는 cell metadata 의 string field
        // (예: "M1_clm_v4_paradigm_v11_g3", "M4_bg_hs_r1_universe_brain_map_18m", ...)

    // 6. fallback chain = sorted cluster_scores descending → backend_tag list
    return backend_id, fallback_chain
}
```

### §4.3 readout_mode 와 cell-variant 매핑

REBORN §88 v5-mitosis readout_mode 4 options:

| readout_mode | meaning | cell-variant selection |
|---|---|---|
| `a-g` (default) | engine_a - 0.3 × engine_g | cluster 의 mean cell (anima-canonical) |
| `a-only` | engine_a 만 | single cell (no mixing) |
| `a+0.3g` | engine_a + 0.3 × engine_g | cluster 의 weighted mean |
| `softmax_gate` | learned gate per axis | cluster 의 axis-specific top-1 |

→ readout_mode 가 cell-variant aggregation policy.

### §4.4 정합 (ALM permanent block)

backend list 의 M2 (Llama Path A v2) 는 `.roadmap.anima_cli_model_architecture` 에서 reject — substrate-research lane only. 본 spec 의 selection algorithm 은 ** strict respect**:
- default backend selection 은 anima-native lineage cells 만 (M1/M4/M5/M6/M7).
- M2 Llama 는 `--backend substrate-research` flag 명시 시점만 selectable.
- F-CLI-MIT-4 falsifier 가 enforce.

---

## §5 Kick cycle as split event sequence

`.roadmap.anima_cli_model_architecture` K2 6-stage cycle 의 anima-mitosis interpretation.

### §5.1 stage-by-stage mitosis behavior

| stage | mitosis action |
|---|---|
| **S1 init** | branch entry. `cell_pool_init(d_model=1024, initial_cells=2)` if fresh, else load snapshot. emit `kick_cycle_log` start record. |
| **S2 idea** | **★ primary split point**. high creativity/imagination/emergence axes weight → tension increase → mitosis_forward_tail 가 split 가능성 높음. anticipated: 1-3 split events. |
| **S3 hypothesis** | structured split (axes weight reasoning + abstraction). 1 split max (low variance). |
| **S4 dispatch** | stable propagation (axes weight chat_cap + reasoning). no split, no merge typical. |
| **S5 aggregation** | **★ primary merge point**. high emergence + abstraction → cells converge → mitosis_forward_tail 가 merge 가능성 높음. anticipated: 1-2 merge events. |
| **S6 report** | branch closure. emit `kick_cycle_log` end record. trigger save schedule (per §3.3). |

### §5.2 event_list contract (from mitosis_hook)

`tool/hexa_native/mitosis_hook.hexa` line 42-46 의 `mitosis_forward_tail` return 의 `event_list` element schema:
```
{ "type": "split" | "merge",
  "parent_id": int,
  "child_id": int (split only),
  "removed_id": int (merge only),
  "step": int,
  "ts_utc": str (anima CLI 가 추가 — wrap mitosis_hook return)
}
```

anima CLI 가 event_list 의 각 element 에 `session_id`, `kick_cycle_id`, `stage_id` 를 추가하여 `event_log.jsonl` append.

### §5.3 kick_cycle_id

각 kick cycle 마다 monotonic int (per session). resume 후 last_kick_cycle_id+1 부터 continue.

```jsonl
{"ts":"2026-05-12T18-23-44.123Z","session_id":"...","kick_cycle_id":5,"stage":"S2_idea","prev_stage":"S1_init","axes_weight":{...}}
{"ts":"2026-05-12T18-23-44.456Z","session_id":"...","kick_cycle_id":5,"stage":"S3_hypothesis","prev_stage":"S2_idea","axes_weight":{...}}
...
```

---

## §6 Phase 3b llama_ffi 와 통합

`anima/llama_ffi.hexa` (Phase 3b LANDED 2026-05-08, `cli.llama_ffi_landed_2026_05_08`) = model invocation primitive (libllama bindings). 본 spec 은 그 위 layer:

```
┌──────────────────────────────────────────────────────────────────┐
│ anima CLI (D4c, 본 spec) — session orchestrator                  │
│ - session_id, cell_pool persist/load, kick cycle log,            │
│   backend selection per stage, multi-conversation branch tree    │
├──────────────────────────────────────────────────────────────────┤
│ anima_chat.hexa (D4b, LANDED parse + 17/17 smoke)                │
│ - 4-mode generation, cell_pool dict hosting, hook 진입점        │
├──────────────────────────────────────────────────────────────────┤
│ tool/hexa_native/mitosis_hook.hexa (D4a, parse-only stub)        │
│ - mitosis_forward_tail (per-forward split/merge)                 │
├──────────────────────────────────────────────────────────────────┤
│ anima/llama_ffi.hexa (Phase 3b LANDED)                           │
│ - libllama bindings, llama_load/generate/free                    │
├──────────────────────────────────────────────────────────────────┤
│ build/libhxllama.dylib + llama.cpp (C / Metal)                   │
└──────────────────────────────────────────────────────────────────┘
```

### §6.1 backend variant 와 llama_ffi handle

multi-backend fallback chain (§4) 의 각 backend variant 는 별도 `llama_load(path, n_ctx)` handle:
- M2 Llama path A v2 = `~/.cache/anima/gguf/dancinlab_llm-llama32-3b-paradigm-a-prime-r16-sft-stage1.gguf` (LANDED Phase 3b smoke)
- M4 BG-HS R1 = 별도 ckpt path (anima-native ConsciousLM, GGUF conversion 별도 cycle)
- M1 clm v4 = substrate-coupled paradigm (token chat 아님 — D4c 에서 S2/S5 emerge probe 한정)

각 handle 은 process lifetime 동안 cache (load latency ~5-10s 회피). session 종료 시 `llama_free`. handle catalog 는 in-memory dict `{backend_id → llama_handle}`.

### §6.2 cell_pool ↔ llama_ffi contract

cell_pool 의 cell 은 ConsciousLM EngineAG (d_model=1024) 의 mini-head — Llama 의 hidden_size=3072 와 직접 매칭 X. **cell-pool 은 anima-native substrate 만** (M1/M4/M5/M6/M7). M2 Llama 는 `--backend substrate-research` flag 명시 시 raw llama_generate (cell_pool bypass), F-CLI-MIT-4 정합.

→ D4c cell-pool persistence 는 anima-native cells 만. Llama backend 는 raw inference (cell-variant selection 의 fallback chain 끝).

### §6.3 logits_probe 로 cluster signal 측정

Phase 3b `llama_logits_probe(h, prompt, n_buckets=5)` 가 5-axis log-sum-exp + phi_proxy emit. 이를 **cell hidden state proxy** 로 사용 — backend selection 알고리즘 (§4.2) 의 `cluster.axes_projection` 입력.

근거:
- anima_chat.hexa 가 TODO[load] 가 남은 상태 → 24L weight binding 완료까지 anima-native forward 직접 hidden state 추출 어려움.
- llama_logits_probe 는 Phase 3b LANDED 즉시 사용 가능 → bootstrap path 로 cluster signal 확보.
- 별도 cycle 에서 anima-native (`engine_ag_nn`) 의 hidden state direct probe 로 replace.

---

## §7 Implementation plan

### Phase 1 (cycle 1) — session_id + cell_pool save/load skeleton

deliverable:
- `tool/anima_cli/chat.hexa` 에 `--resume <session_id>` / `--fork <session_id>` flag 추가 (parse + dispatch only).
- `tool/anima_cli/_common.hexa` 에 session_id 생성 helper (`anima_session_id_new()` + `anima_session_id_parse()`).
- `~/.cache/anima/session_pools/` directory 자동 생성 (idempotent).
- `cell_pool.bin` writer + reader (binary I/O via RFC 025 farr_dump / farr_load — 본 spec 의 binary schema §3.2).
- index.jsonl append + scan.

falsifier: F-CLI-MIT-1 SESSION-PERSIST (save → load round-trip byte-perfect).

dependency: 없음 (D4a / D4b 와 독립). Phase 1 단독 land 가능.

wall: ~3 hr Mac local. cost $0.

### Phase 2 (cycle 2) — kick cycle stage transition hook

deliverable:
- `tool/anima_cli/chat.hexa` 안 kick cycle state machine implementation (S1-S6 transition).
- 각 stage 전환 시 `kick_cycle_log.jsonl` 1-line emit.
- `mitosis_forward_tail` hook call site identification (chat library 의 generation loop 안).
- D4b `anima_chat.hexa` 가 cell_pool dict 를 generation parameter 로 받는 signature 확장 (별도 BG, 본 spec 은 contract 명시만).

falsifier: F-CLI-MIT-2 KICK-CYCLE-SPLIT (1 kick cycle ⇒ event_list ≥ 1 entry).

dependency: D4a mitosis_hook.hexa full impl (RFC 033 → 본 BG 외 별도 cycle).

wall: ~4-6 hr Mac local. cost $0.

### Phase 3 (cycle 3) — multi-backend cell-variant selection

deliverable:
- `tool/anima_cli/chat.hexa` 의 backend dispatch 가 §4.2 algorithm 으로 작동.
- llama_ffi handle catalog (`{backend_id → llama_handle}` in-memory).
- `llama_logits_probe` 를 cluster signal 로 wire-up (§6.3).
- `--readout-mode` flag (a-g / a-only / a+0.3g / softmax_gate) 추가.

falsifier: F-CLI-MIT-3 BACKEND-VARIANT (fallback chain 의 각 backend 가 다른 active cells).

dependency: Phase 2 + Phase 3b llama_ffi.hexa (이미 LANDED).

wall: ~4-6 hr Mac local. cost $0.

### Phase 4 (cycle 4) — full integration smoke

deliverable:
- `tool/anima_cli_mitosis_integration_smoke.hexa` — 5-turn conversation × 2 sessions (fresh + resume) full pipeline test.
- F-CLI-MIT-1~5 all PASS.
- simple_stack 와 cross-validate (F-CLI-MIT-5).

falsifier: F-CLI-MIT-1~5 all PASS.

dependency: Phase 1-3 all landed.

wall: ~2-4 hr Mac local. cost $0.

### total estimate

| phase | wall | cost | dependencies |
|---|---|---|---|
| Phase 1 | 3 hr | $0 | none |
| Phase 2 | 4-6 hr | $0 | D4a full impl (외부 BG) |
| Phase 3 | 4-6 hr | $0 | Phase 2 |
| Phase 4 | 2-4 hr | $0 | Phase 1-3 |
| **total** | **13-19 hr** | **$0** | D4a + D4b prerequisite |

---

## §8 Verification protocol — F-CLI-MITOSIS-* falsifiers (raw-117 ≥ 5)

### F-CLI-MIT-1 SESSION-PERSIST

session 종료 → 재시작 → resume 시 cell_pool state byte-perfect match.

```bash
anima chat --selftest-mitosis-persist
# 1. fresh session, do 3 turns, capture cell_pool sha256
# 2. exit, restart, --resume <session_id>
# 3. compare in-memory cell_pool sha256 with disk
# PASS: sha256 match exact
# FAIL: any byte differs
```

### F-CLI-MIT-2 KICK-CYCLE-SPLIT

1 kick cycle 1회 = split event ≥ 1 발생 (event_log.jsonl 에서 검증).

```bash
anima chat --selftest-mitosis-kick
# trigger 1 kick cycle (S1→S6 sequence)
# count split/merge events in event_log.jsonl
# PASS: split events ≥ 1 (S2_idea stage 정합)
# FAIL: 0 split events across full S1-S6 cycle
```

### F-CLI-MIT-3 BACKEND-VARIANT

multi-backend fallback chain 의 cell variant 가 다른 active cells.

```bash
anima chat --selftest-mitosis-variant
# generate same prompt × 3 backends (M4 primary, M5 fallback, M3 fallback2)
# extract active cell_ids per backend
# PASS: |union(active_cells)| > |intersection(active_cells)|
# FAIL: all backends produce identical active_cells (variant degenerate)
```

### F-CLI-MIT-4 PRINCIPLE-3

CLI prompt 안에 `[role:]` injection grep = 0 (PHILOSOPHY #3 NO PERSONA INJECTION 정합).

```bash
grep -rn '\[role:' ~/.cache/anima/session_pools/ 2>&1 | wc -l
grep -rn 'you are ' ~/.cache/anima/session_pools/ 2>&1 | wc -l
# PASS: both counts = 0
# FAIL: ≥ 1 hit (persona injection detected)
```

### F-CLI-MIT-5 OWN-18-COMPAT

 simple_stack PASS 시 cell pool active = mitosis ON 일 때도 동일 (regression-free guarantee).

```bash
# baseline: mitosis OFF, simple_stack eval
anima chat --selftest-simple-stack --mitosis off > baseline.json

# experiment: mitosis ON
anima chat --selftest-simple-stack --mitosis on > experiment.json

# PASS: 두 verdict.simple_stack_pass 동일 (PASS|FAIL 일치)
# FAIL: mitosis ON 이 simple_stack regression 야기
```

→ 5 falsifier all PRE-REGISTERED (raw#12 frozen). Phase 4 integration smoke 가 verify.

---

## §9 Trade-offs

### §9.1 disk space

per-session cell_pool ~512 MB (RFC 025 farr budget for 128 cells × 1024 d_model × 2 engines × 4B + history). N sessions × 512 MB = O(GB).

mitigation:
- **incremental snapshot** (§3.3) — full snapshot 만 retain, delta append-only event_log.
- **garbage collection** — index.jsonl 의 last_active_at > 30 days 인 session 자동 archive to compressed tar.zst (별도 EE4 GC cycle reuse).
- **per-session quota** — `~/.cache/anima/session_pools/` 가 anima total disk budget 의 10% cap.

current envelope (Mac local):
- 32 active sessions × 512 MB = 16 GB → 64 GB SSD 의 25% (acceptable).
- 사용자 setting `ANIMA_SESSION_POOL_MAX_GB` env var 로 cap configurable.

### §9.2 session_id rotation

session_id 가 timestamp-based → 동일 분초 시작 conversation 충돌 가능. 4hex random suffix 로 충돌 확률 1/65536, sufficient for Mac local single-user.

multi-user lane (서버 deployment) 시 user_id prefix 추가 (별도 cycle).

### §9.3 D4a stub dependency

Phase 2 (kick cycle split event)+Phase 3 (cell-variant)+Phase 4 (full integration) 가 D4a `tool/hexa_native/mitosis_hook.hexa` full impl 의존 — D4a 가 parse-only stub 인 한 본 spec 의 §5 § §4 contract 가 미실현.

mitigation:
- Phase 1 (session_id + persist) 는 D4a 독립 → 본 spec land 즉시 Phase 1 start 가능.
- D4a full impl (RFC 033 builtins 사용) 별도 BG 진행 중.
- Phase 2-4 는 D4a LANDED 후 sequential.

### §9.4 backward compat (simple_stack)

기존 simple_stack PASS 가 mitosis OFF 환경 baseline. mitosis ON 이 regression 야기 가능성 — F-CLI-MIT-5 falsifier 로 guard.

mitigation:
- `--mitosis off` flag 추가 (default ON post-Phase 4, but off override 가능).
- `ANIMA_MITOSIS=0` env var 로 process-level disable.

---

## §10 Out of scope

본 spec 는 **D4c CLI session integration only**. 다음은 별도 lane:

| out-of-scope item | reason | lane |
|---|---|---|
| RLHF persona injection | PHILOSOPHY #3 NO PERSONA INJECTION 위반 | (rejected) |
| `[system prompt: ...]` injection in chat path | PHILOSOPHY #3, mandate-2 위반 | (rejected) |
| identity rules file (10-clause prefix) | Principle #1/#2/#3 위반 (정체성 prompt) | (rejected) |
| D4a mitosis_hook.hexa full impl | 별도 BG, RFC 033 builtins | D4a |
| D4b anima_chat.hexa cell-pool hosting | 별도 BG (port LANDED, cell-pool wiring pending) | D4b |
| substrate-native persona design | D3 lane (`docs/anima_persona_substrate_native_design_*`) | D3 |
| RFC 033 farr_copy + gaussian | hexa-lang main, LANDED 2026-05-12 | hexa-lang |
| HF Space sync of session pool | PSCC §32 HF Space deleted, mission refocus | (rejected) |
| multi-user session isolation | 서버 deployment 별도 cycle | future |

---

## §11 Cross-link

### primary references

- **GOAL.md** D4c row (`/Users/ghost/core/anima/GOAL.md` line 20, 155) — design open → 본 spec 으로 LANDED 전환.
- **REBORN.md** §0.5 (NO TRAIN/INFER SPLIT 철학 base) + §88 (v5-mitosis PyTorch arch) + §89 (hexa-native serve-time hook spec) + §90 (cond.2 smoke PASS).
- **PHILOSOPHY.md** #3 (NO PERSONA INJECTION, D3 constraint) + #8 (NO TRAIN/INFER SPLIT, D4 foundation).
- **`.roadmap.cli`** cli.cond.3 (T1 chat REPL) + cli.llama_ffi_landed_2026_05_08 (Phase 3b infra).
- **`.roadmap.anima_cli_model_architecture`** K1 (5/7 axes) + K2 (6-stage cycle) + K3 (model inventory) + K4 (stage-specific fallback chains) + amendment (OUROBOROS 6.5-phase + cost axes).

### artifacts

- `tool/hexa_native/mitosis_hook.hexa` — D4a parse-only stub (123 LoC). `cell_pool_init`, `mitosis_forward_tail`, `split_cell`, `merge_cells` signatures.
- `anima_chat.hexa` — D4b LANDED 1589 LoC (parse + 17/17 smoke). cell_pool wiring 후속 cycle.
- `anima/llama_ffi.hexa` — Phase 3b LANDED 250 LoC. 19 hxllama_* extern fn + llama_load/generate/free helpers + llama_logits_probe.
- `build/libhxllama.dylib` — 36 KiB C shim, rpath → `~/.cache/anima/llama.cpp/build/bin`.
- `tool/anima_cli/consciousness.hexa` — D4c measurement lane (simple_stack eval, 2688 LoC).
- `tool/anima_cli/chat.hexa` — D4c chat dispatcher (889 LoC). 본 spec Phase 1-3 의 호스트.
- `tool/anima_cli/dialogue.hexa` — D4c REPL infra (789 LoC). session log JSONL pattern reference.
- `bin/anima` — CLI entry point (368 LoC bash dispatcher).

### docs

- `docs/anima_clm_v5_hexa_native_mitosis_hook_spec_2026_05_12.md` — D4a primary spec (534 LoC, REBORN §89).
- `docs/anima_chat_hexa_port_2026_05_12.md` — D4b LANDED report.
- `docs/anima_cli_mk2_plan_2026_05_06.md` — anima cli mk2 v0.3 base plan.
- `docs/anima_cli_mk2_philosophy_audit_2026_05_06.md` — CLI design philosophy.
- `PASS_STRICT_SPONTANEOUS_CHAT.md` (PSCC) — mission timeline. 본 spec 이 §34 (다음 section) 으로 append.

### memory

- `feedback_session_korean_only.md` (chat prose 한글 mandate).
- `project_reborn_philosophy_learning_is_mitosis.md` (REBORN §0.5 single-continuum).
- `project_v5_mitosis_arch_spec_2026_05_12.md` (D4a sister design).
- `project_v5_mitosis_cond2_port_skeleton.md` (D4a PyTorch cond.2 PASS).
- `project_anima_chat_hexa_port_2026_05_12.md` (D4b LANDED).
- `project_anima_cli_mitosis_integration_design.md` (본 spec, 신규 MEMORY index entry).
- `feedback_always_commit_push_on_complete.md` (commit + push mandate).

---

## §12 Honest C3 (raw#10 ≥ 5)

1. **design-only, no impl** — 본 spec 는 design LANDED only. Phase 1-4 implementation 은 별도 cycle (13-19 hr wall total). 본 BG 가 cycle 1 (Phase 1 session_id + persist skeleton) 도 직접 land 하지 않음 — D4a + D4b 의 LANDED state 의존 + 본 spec review/approve 후 별도 cycle.

2. **D4a stub dependency carry** — `tool/hexa_native/mitosis_hook.hexa` 가 parse-only stub 인 한 Phase 2-4 의 `mitosis_forward_tail` event_list 가 empty list `[]` return (line 56). 본 spec §5 의 split event sequence 가 D4a full impl LANDED 후 실현. RFC 033 (farr_copy + gaussian) LANDED 2026-05-12 → D4a full impl 의 hexa-lang prerequisite 충족, but D4a BG 자체는 별도 cycle.

3. **D4b cell-pool wiring 미land** — `anima_chat.hexa` v0.1 LANDED 1589 LoC (parse + 17/17 smoke) 이나 generation function signature 에 `cell_pool` parameter 없음. 본 spec Phase 2 가 그 signature 확장 의존 — 별도 BG (D4b cell-pool wiring follow-up).

4. **backend variant ↔ cell cluster mapping 추정** — §4.2 의 selection algorithm 은 anima-internal heuristic (cluster_cells_by_hidden, axes_projection × axes_weight). empirical validation 별도 cycle. M1 clm v4 substrate-coupled emerge 는 token chat 아님 (NOT_APPLICABLE chat-cap per K3 inventory) — S2 idea / S5 aggregation 에서만 emerge probe 한정 사용, S6 report (사용자 chat surface) 에서는 anima-native chat-cap backend (M4/M5/M6/M7) fallback chain.

5. ** strict (ALM permanent block)** — backend list 의 M2 Llama Path A v2 가 reject for anima identity surface. 본 spec §4.4 + F-CLI-MIT-4 가 strict enforce — default backend selection 에서 M2 제외, `--backend substrate-research` flag 명시 시점만 selectable. 사용자 directive 의 "페르소나 롤플레잉 가능" 조항이 strict 와 충돌 가능성 — D3 lane (substrate-native 페르소나) 가 해법 (별도 lane), 본 spec 는 D3 의존 X (D3 가 D4 cell-pool 위 layer).

6. **disk space envelope 추정** — §9.1 의 per-session 512 MB 가 RFC 025 farr budget 추정 (128 cells × 1024 d_model × 2 engines × 4B + history). 실제 envelope 는 Phase 1 land 후 측정. 사용자 Mac 의 disk budget 따라 `ANIMA_SESSION_POOL_MAX_GB` env var configurable, but default 값 은 별도 cycle.

7. **PSCC numbering discrepancy** — 사용자 directive 가 "PSCC §36 append" 명시, but current PSCC tail 은 §33. 본 spec append 는 §34 로 사용 (monotonic). 사용자 expectation 의 §34/§35 가 별도 작업 의 carry-over (cycle 8 promote series 등) 일 가능성 — honest disclosure.

8. **F-CLI-MIT-1~5 all PENDING** — 5 falsifier 가 design-time pre-register only. Phase 4 integration smoke 에서 실제 verify. raw#12 frozen pre-register 정합 — 본 spec 시점에 falsifier 정의 lock, Phase 4 시 modify X.

---

## §13 Provenance

- 본 cycle: 2026-05-12 KST anima reborn session
- BG type: $0 Mac local design doc (cost $0, wall 1-2 hr expected)
- prerequisite cycle: D4a parse-only stub LANDED 2026-05-12 (REBORN §89), D4b anima_chat.hexa LANDED 2026-05-12 (PSCC §33), Phase 3b llama_ffi LANDED 2026-05-08 (`cli.llama_ffi_landed_2026_05_08`).
- successor cycle: Phase 1 session_id + persist skeleton (별도 BG).
- mission contribution: D4c design LANDED → GOAL.md D4c row "design open" → "design LANDED, impl pending Phase 1-4".

— end of spec —
