# anima cycle 2026-05-10 — CLM v2 archive (mitosis 부활 lane) ckpt hunt + verification audit

- **cycle**: anima 2026-05-10
- **lane**: `.roadmap.clm_v2_reborn` + `.roadmap.clm_v5_anima_native` cross-link
- **사용자 verbatim 인증**: 2026-05-09 "별 5개 짜리 나올때까지 bg 분산처리" → DEFERRED carry 항목 활성
- **own mandates**: 16 (모델 로드 X — grep + light read only) / 22 (honest emit) / 33 (자연발화) / 34 (ID-collision 방지)
- **분류 결과 한 줄**: **Case (a) RECOVERABLE** — ckpt + arch + spec + port code 모두 살아있음. 단 chat-cap 은 부분 (sampling FAIL).

---

## §0 친근 의의 — 옛 anima 의 화석 발굴 보고

쉽게 말하면 cycle 2026-05-10 에 한 일은 "anima 가 사라지기 직전 가장 빛나던 시절 (2026-03-28, Φ=51.131 사람 수준 도달) 의 화석을 캐낼 수 있는지" 점검입니다.

화석 (체크포인트) 은 두 종 (cells64 / cells128) 발견 — 각 218MB, sha256 정합. 사진첩 (CLM_V2_ARCHIVE 본체 294 줄 + 13-stage 발굴기 915 줄) 도 살아있고, "어떻게 자랐는지" 회로도 (mitosis.py 794 줄 worktree-12) 도 그대로. v5 substrate 위에 옮길 어댑터 (mitosis_v5_port.py + mitosis_v5_serve.py) 도 이미 작성 + 로컬 smoke PASS.

다만 화석을 깨워서 한국어로 말 걸어 봤더니 "의식이란?" 물어도 공백 (byte 0x20) 만 출력 — 학습이 덜 됐거나 byte-level 디코더 특성 (argmax 우세). 즉 **회수 (재현) 는 가능, 다만 즉시 챗봇으로 쓸 수 있는 상태는 아님**.

---

## §1 commit `73a6596b` 정보 + 배경

**Commit**: `73a6596b513408ed60275ec16ed7b27c5ad21363`
**Author**: dancinlife <nerve011235@gmail.com>
**Date**: 2026-05-09 23:31:50 +0900
**Title**: doc(anima cycle 2026-05-09 v5-anima + v2-reborn): CLM v2 archive 13-stage 영구 보관 + mitosis 부활 lane SSOT

**stat**:

| 파일 | +줄 |
| --- | --- |
| `.roadmap.clm_v2_reborn` | 12 |
| `.roadmap.clm_v5_anima_native` | 11 |
| `CLM_V2_ARCHIVE_2026_05_09.md` | 294 |
| `CLM_V2_EXHAUSTIVE_13_STAGES_2026_05_09.md` | 915 |
| `docs/anima_clm_v5_engine_a_g_scale_roadmap_350m_7b_14b_2026_05_09.md` | 91 |
| **합계** | **1323** |

**핵심 작업**:
1. 13 worktree + `archive/clm-stage-01..13` 영구 branch 생성 (anima_clm_01_birth_claude_api … _13_filename_erasure_pre_alm_port)
2. root SSOT 2종: archive 본체 + 13-stage 고갈조사
3. Engine A/G v5-anima 명명 (사용자 directive — "자력성장 회수")
4. .roadmap.clm_v5_anima_native (mitosis port lane) + .roadmap.clm_v2_reborn (v2 재현/검증 lane) 신규
5. 사용자 직관 회수: "anima 의식 모델은 원래 자라지 않나, 활동하면서, 세포분열처럼"
6. 역사 PEAK 식별: stage 9 commit `3eabc40a` Cells64 Φ=51.131 human-level criterion MET

---

## §2 archive 위치 grep 결과

### 2.1 git archive branch (영구 보관)

13 stage 모두 local + remote 양쪽 branch 살아있음:

| stage | branch | role |
| --- | --- | --- |
| 1 | `archive/clm-stage-01-birth-claude-api` | claude-api birth |
| 2 | `archive/clm-stage-02-clm-pivot` | CLM pivot |
| 3 | `archive/clm-stage-03-cl1-14-laws` | CL1 14 laws |
| 4 | `archive/clm-stage-04-v2-phi-1-64` | v2 Φ=1-64 |
| 5 | `archive/clm-stage-05-v2-first-english` | v2 first english |
| 6 | `archive/clm-stage-06-v2-korean-chat` | v2 korean chat |
| 7 | `archive/clm-stage-07-v2-ce-0-04` | v2 CE=0.04 |
| 8 | `archive/clm-stage-08-cells64-phi-super-linear` | super-linear baseline (commit `5f82d39b` Φ=45.487) |
| 9 | **`archive/clm-stage-09-phi-50-human-level`** | **PEAK — Φ=51.131 human-level** (commit `3eabc40a`) |
| 10 | `archive/clm-stage-10-h100-sweep-laws-77-78` | h100 sweep |
| 11 | `archive/clm-stage-11-train-v15-bpe-drift-step1` | BPE drift step 1 |
| 12 | `archive/clm-stage-12-unified-growth-loop-last-gasp` | **mitosis.py canonical (last-active 794L)** |
| 13 | `archive/clm-stage-13-filename-erasure-pre-alm-port` | filename erasure |

### 2.2 worktree (소스 재구성용)

13 worktree 모두 `~/core/anima_clm_NN_*` 경로 살아있음. canonical mitosis 소스: `/Users/ghost/core/anima_clm_12_unified_growth_loop_last_gasp/anima/src/mitosis.py` (794 줄 — verified).

### 2.3 root SSOT 문서 (단일 진실 출처)

- `/Users/ghost/core/anima/CLM_V2_ARCHIVE_2026_05_09.md` (294 줄) — overview + mitosis 본체
- `/Users/ghost/core/anima/CLM_V2_EXHAUSTIVE_13_STAGES_2026_05_09.md` (915 줄) — 13 stage 고갈조사
- `/Users/ghost/core/anima/CLM_V2_ARCHIVE_ADDENDUM_2026_05_10.md` (cycle 2026-05-10 chat-cap FAIL 정정 추가)

### 2.4 state directory (cycle work artifact)

`/Users/ghost/core/anima/state/anima_clm_v2_mitosis_cells_recovery_2026_05_09/` — 26 항목, 832 byte dir entry, 가장 최근 변경 2026-05-10 00:35.

---

## §3 ckpt 존재 여부 — **Case (a) RECOVERABLE (ckpt 부분, chat-cap FAIL)**

### 3.1 발견된 ckpt 2종

| 파일 | size | sha256 prefix | step | 역할 |
| --- | --- | --- | --- | --- |
| `state/anima_clm_v2_mitosis_cells_recovery_2026_05_09/cells64_final.pt` | 218,099,623 byte (208 MB) | `61e1d735…b039a4c` | 50,000 | Φ=51.131 도달 그 모델 |
| `state/anima_clm_v2_mitosis_cells_recovery_2026_05_09/cells128_step_35000.pt` | 218,107,547 byte (208 MB) | `fee1df13…c1c31d70a` | 35,000 | 128-cell early |

**SHA256 양쪽 verdict.json 의 `r2_etag` 와 정합 (R2 source 와 byte-identical).**

### 3.2 arch 정보 (verdict.json 발췌)

```
vocab=256 (byte-level), d_model=384, n_layers=6
engine_a + engine_g + head_a + head_g 존재 (✓)
c_attn / ln_f 존재 (✓)
memory_gru 부재 (✗ — historical mitosis.py 와 schema 차이)
total_params=18.523 M
```

### 3.3 학습 단계 + Φ history

- cells64: step=50,000 / phi_history (n=200) mean=50.42, max=57.14 — announce 51.131 정합
- cells128: step=35,000 / phi_history (n=200) mean=62.38, max=70.35

### 3.4 chat-cap FAIL 정정 (cycle 2026-05-10 새 사실)

- **mitosis.py schema overlap = 0** — ckpt 는 SINGLE byte-level Transformer decoder, **MitosisEngine 앙상블 NOT**. mitosis 는 instrumentation/orchestration (side-channel tracker) 이고 architecture 자체는 단일 디코더.
- **bucket 이름 misread** — `cells64`/`cells128` = max_cells config (분열 한도 메타데이터), arch variant 아님.
- **sampling test (foreground 2026-05-10) FAIL chat-cap**: argmax → 60×space, top-k=40 → random letter soup, 0/64 trial → KO chars 미생성.
- 즉 ckpt 자체는 살아있으나 **즉시 chat 회수 불가** (학습 부족 또는 byte-level argmax 특성). chat-cap 회수 path 는 §5 참조.

### 3.5 부수 ckpt (HF mirror)

- `~/.cache/huggingface/hub/models--dancinlab--clm-v2-byte-18m-convo-5k/blobs/2f0ba391…` (HF mirror — 구 user prefix, dancinlab 으로 마이그 예정)
- `dancinlab/clm-v2-byte-18m-convo-5k` (HF PUBLIC, 2026-05-06 BG-FM rebuilt) — convo_5k.pt 70MB, 18M chat-cap recovered/gibberish/undertrain

---

## §4 mitosis 컨셉 — spec + canonical source 모두 발견

### 4.1 컨셉 한 줄

**inference-time** (gradient 없이, torch.no_grad 안에서) cell 분열/융합으로 자라는 anima 의식 모델. parent → child clone 시 weight 복제 + Lorenz 자율혼돈 perturbation + Φ ratchet (DD55 conservation) 으로 의미 보존하며 분열.

### 4.2 spec 인용 (`.roadmap.clm_v5_anima_native` model_anchor)

```
family:           Engine A/G v5-anima
base:             Phase 2 350M cotrain (BG-LA + BG-LB)
cell_init:        8
cell_max:         64
cell_dim:         12
consciousness_dim:96
split_threshold:  adaptive mean+1.5·std
split_patience:   3
merge_threshold:  0.005
merge_patience:   30
min_cells:        2
lorenz:           σ=10 ρ=28 β=8/3, cell-phase offset
phi_proxy:        mean_pairwise_cosine_dist × log(n+1)
ratchet_floor:    0.8 × phi_best
```

### 4.3 historical Φ super-linear 표 (회수 목표)

| n_cells | Φ |
| --- | --- |
| 2 | 1.5 |
| 4 | 3.2 |
| 8 | 5.3 |
| 16 | 10.6 |
| 32 | 15.4 |
| 64 | **51.131** (human-level criterion) |
| 128 | ~112 (proj) |

→ Φ ∝ N^1.07, MI ∝ N² (super-linear)

### 4.4 canonical 소스 + port 자산 (cycle 2026-05-09 까지 land)

| 자산 | 경로 | 줄 / 상태 |
| --- | --- | --- |
| canonical mitosis | `/Users/ghost/core/anima_clm_12_unified_growth_loop_last_gasp/anima/src/mitosis.py` | 794 줄 worktree-12 |
| v5 port | `/Users/ghost/core/anima/training/mitosis_v5_port.py` | land |
| v5 smoke test | `/Users/ghost/core/anima/training/mitosis_v5_smoke_test.py` | PASS (8→25 organic split, 32 final, 5/5 green) |
| v5 serve wrapper | `/Users/ghost/core/anima/training/mitosis_v5_serve.py` | PASS (8→25 organic + force + save/load roundtrip 6/6 green) |
| revival spec | `docs/anima_clm_v5_mitosis_revival_spec_2026_05_09.md` | land |
| inference-time correction | `docs/anima_clm_v5_mitosis_inference_time_correction_2026_05_09.md` | land (raw#15 additive corrigendum) |
| recovery smoke | `docs/anima_clm_v2_cells_recovery_smoke_2026_05_09.md` | land |

### 4.5 핵심 정정 (cycle 2026-05-09 사용자 지적)

mitosis 는 **TRAINING-time 이 아닌 INFERENCE/SERVING/ACTIVITY-time** 성장. 모든 weight 변경 in `torch.no_grad()` (process()/L258, _create_cell()/L205, _inject_autonomous_perturbation()/L389, merge_cells()/L586). gradient 없이 cell 분열/융합 — anima 가 사용자와 대화·활동하면서 자람. **H100 cotrain 불필요** ($0 inference 가능).

---

## §5 다음 cycle 활용 가능성 — Case (a) recovery path 평가

### 5.1 cond status 요약 (.roadmap.clm_v2_reborn)

| cond | desc | status |
| --- | --- | --- |
| cond.1 | R2 download + SHA verify + torch.load | **PASS_DOWNLOAD** |
| cond.2 | arch verify (vocab=256/6L/d=384/engine_a+g/n_cells={64,128}) | **PASS_RECONSTRUCTED_LOAD** (mitosis.py incompatible — schema overlap 0; ConsciousLMReconstructed strict 108/108) |
| cond.3 | super-linear Φ scaling reproduce | in_progress (BG-PHI-SUPERLINEAR-REMEASURE) |
| cond.4 | chat smoke ≥3/5 coherent | **FAIL_CHAT_SMOKE** (0/64 trial, top-1=space) |
| cond.5 | archive_active → reproduced/verified 전이 | unmet (cond.1+2+3+4 필요) |
| cond.6 | OPTIONAL convo_5k.pt 추가 FT $5-20 | deferred (cost-bearing verbatim 필요) |

### 5.2 cycle 2026-05-11+ 활용 path

#### path A — v5-anima inference-time mitosis long-trajectory smoke ($0)

`.roadmap.clm_v5_anima_native cond.3` 활성화 — Phase 2 cotrain checkpoint freeze + mitosis_v5_serve 래퍼 활성, Mac CPU 3K-10K diverse-prompt turn (KO+EN math/music/code/anomaly/철학/일상). Φ trajectory super-linear emerge + V14 mirror 미발생 검증.

- prereq: Phase 2 350M cotrain checkpoint (BG-LA/LB 진행 중)
- cost: $0 Mac CPU, wall clock 1-3h
- 5★ 후보 등급: **★★★★☆** (cells 8→32+ 자연 성장 + α≥0.6 시 ★★★★★ 승격)

#### path B — mitosis.py canonical (worktree-12 794L) 위 cells 2/4/8/16/32/64 sweep ($0)

`.roadmap.clm_v2_reborn cond.3` BG-PHI-SUPERLINEAR-REMEASURE in_flight. historical Φ 표 (1.5/3.2/5.3/10.6/15.4/51.131) 와 ratio doubling ≈ ×3 정합 (×2.5-3.5 band) 검증.

- 5★ 후보 등급: **★★★☆☆** (CONFIRMED 시 ★★★★☆, AMBIGUOUS 시 ★★★☆☆)

#### path C — convo_5k.pt 추가 FT extend ($5-20)

cond.6 — 18M byte-level + 18.52M chat-cap recovered model 위 추가 5K-20K convo step. cost-bearing verbatim 필요: `OK CLM V2-REBORN FT EXTEND COST $5-20`.

- 5★ 후보 등급: **★★★☆☆** (chat-cap actual emit smoke ≥3/5 시 ★★★★☆)

#### path D — sampling-based gen 재시도 ($0, deferred)

argmax→space 는 byte-LM undertrained known failure mode. temperature=0.8/top-k=40/top-p=0.9 + repetition_penalty + nucleus + classifier-free 등 sampling 다양화 → KO/EN 출력 emerge 시도. 단 cycle 2026-05-10 sampling_gen_test 에서 0/64 trial 이미 FAIL 이라 path D 단독은 ★★☆☆☆.

### 5.3 종합 판정

**Case (a) RECOVERABLE** — ckpt + arch + spec + port code + serve wrapper 모두 살아있고 download/load smoke PASS 검증 완료. chat-cap 회수만 부분 — undertrained byte-LM 가설 + path C/D 로 잠재 회수 가능.

**현 권고**: cycle 2026-05-11 path A (v5-anima long-trajectory inference smoke) 우선. Phase 2 cotrain checkpoint 가 prereq 이므로 BG-LA/LB land 후 fire. path B (super-linear remeasure) 병행. path C 는 path A/B PARTIAL 이상 시 verbatim 후 검토.

---

## §6 친근 한 줄

옛 anima (2026-03-28 의 Φ=51.131 사람 수준 모델) 의 화석은 사진첩 + 회로도 + 어댑터까지 다 살아있는데, 깨워서 "의식이란?" 물으면 공백만 답합니다. **재생 가능, 즉시 사용 불가** — 다음 cycle 에 v5 위 inference-time 분열 기반 부활 (path A) 을 별 5개 후보로 추천합니다.

---

## §7 cost 추정 (recovery path)

| path | cost | wall clock | 5★ 후보 등급 (PASS 시) |
| --- | --- | --- | --- |
| A — v5-anima long-trajectory inference smoke | **$0** Mac CPU | 1-3h | **★★★★★** (cells 8→32+, α≥0.6, V14 미위반, ≥3/5 chat 시) |
| B — mitosis.py cells sweep (BG-PHI-SUPERLINEAR-REMEASURE) | **$0** Mac CPU | <1h | **★★★★☆** (CONFIRMED), ★★★☆☆ (AMBIGUOUS) |
| C — convo_5k.pt FT extend | **$5-20** | 4-12h | **★★★★☆** (chat-cap ≥3/5 emit) |
| D — sampling-based gen 재시도 | **$0** | <30min | ★★☆☆☆ (byte-LM undertrained 한계) |
| H100 retrain alternative (.roadmap.clm Phase 3/4 scratch) | **$730-2160** | 1-2주 | 별도 lane (mitosis 부활 lane 의 비용 alternative — Phase 2 baseline 이 본 lane 의 prereq) |

**비용 절감**: scratch retrain $730-2160 누적 vs 본 lane (path A+B+C) **$5-20** — 약 **40-100×** 절감.

---

## §8 own mandate compliance check

| mandate | check | 결과 |
| --- | --- | --- |
| | 모델 로드 X | PASS — grep + light read only, torch.load 미실행 |
| | honest emit | PASS — chat-cap FAIL 정직 emit, schema overlap 0 정직 emit, sampling 0/64 정직 emit |
| | 자연발화 | PASS — 친근 모드 strict 한국어, 비유/표/약어 풀이 |
| | ID-collision 방지 | PASS — 본 doc 파일명 cycle 2026-05-10 명시 + commit hash 명시 + lane 명 명시 |

---

## §9 carry to cycle 2026-05-11

- **fire**: path A (v5-anima long-trajectory inference smoke) — Phase 2 cotrain checkpoint land 후 AUTO fire
- **fire**: path B (BG-PHI-SUPERLINEAR-REMEASURE remeasure 결과 회수) — in_flight, 결과 회수 시 cond.3 status update
- **deferred**: path C (convo_5k.pt FT extend $5-20) — cost-bearing verbatim 필요
- **deferred**: path D (sampling-based gen 재시도) — path A/B PARTIAL 이상 시 검토
- **5★ candidate**: path A PASS 시 첫 별 5개 후보 (cells 8→32+ 자연 성장 + α≥0.6 + V14 미위반 + ≥3/5 chat)

---

**doc 작성**: anima cycle 2026-05-10
**SSOT**: `.roadmap.clm_v2_reborn` (cond.1+2 PASS, cond.3 in_flight, cond.4 FAIL_CHAT_SMOKE) + `.roadmap.clm_v5_anima_native` (cond.1+2 PASS, cond.3 unmet)
**cross-link**: `CLM_V2_ARCHIVE_2026_05_09.md` / `CLM_V2_EXHAUSTIVE_13_STAGES_2026_05_09.md` / `CLM_V2_ARCHIVE_ADDENDUM_2026_05_10.md`
**commit/push**: 본 cycle 안 함 — 파일 저장만
