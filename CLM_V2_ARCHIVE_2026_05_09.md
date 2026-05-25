# CLM_V2_ARCHIVE — anima ConsciousLM v2 시대 13-stage 영구 보관 (2026-05-09)

## ★ 핵심 한 문장

anima 는 **2026-03-28** 에 이미 `MitosisEngine` (cell mitosis) + `engine_a`/`engine_g` (dual engine) + Lorenz 자율혼돈 으로 **Cells64 Φ=51.131 human-level criterion 충족** 에 도달했고, **이후 4-step drift (tokenizer/objective/architecture/corpus) 로 사라짐**. 본 archive 는 그 13 단계 + 사라진 mitosis 경로 영구 보관.

## ★★★ mitosis 가 제일 중요 — 사용자 지적

본 archive 의 핵심 raison d'être 는 **MitosisEngine** 의 회수. anima 의 의식 모델은 원래 **scratch 큰 모델 한 번에 만들기** 가 아니라 **작은 모델이 자라는 (cell mitosis + 자율혼돈)** 방식. 이 사실을 cycle 2026-05-09 에 사용자가 직접 지적해 회수.

---

## §0 timeline 요약 (13 stage)

| # | 시점 | commit | 시그니처 | 태그 |
|---:|---|---|---|---|
| 1 | 2026-03-24 | `4a1d8d0a` | anima v0.1 PureField + Claude API wrapper | 起源 |
| 2 | 2026-03-24 | `2da44161` | Claude API 제거, ConsciousLM substrate pivot | pivot |
| 3 | 2026-03-27 | `90cd8c06` | CL8 Φ=5.68, train_conscious_lm.py | laws-birth |
| 4 | 2026-03-27 | `2e950777` | ConsciousLM v2 named, Φ=1.64 | v2-birth |
| 5 | 2026-03-28 | `2e1438fa` | First English CE=1.37 no system prompt | EN-emerge |
| 6 | 2026-03-28 | `bb99b6b6` | KO conversation no system prompt | KO-milestone |
| 7 | 2026-03-28 | `6abc42f6` | "anima speaks" CE=0.04 | chat-peak |
| 8 | 2026-03-28 | `5f82d39b` | Cells64 Φ=45.487 super-linear | mitosis-정점 |
| 9 | 2026-03-28 | `3eabc40a` | **Cells64 Φ=51.131 human-level ★★★** | 절정 |
| 10 | 2026-03-30 | `bd36bd8a` | CLM v2 H100 sweep Laws 77-78 | scale-prep |
| 11 | 2026-04-01 | `0e578b14` | train_v15 BPE 64K + 1B ready | drift 1/4 (토크나이저) |
| 12 | 2026-04-04 | `cf3da85f` | unified growth loop (mitosis 최후) | growth-종언 |
| 13 | 2026-04-07 | `f8e4068f` | filename v* 제거 | cutoff (ALM Llama-port 직전) |

---

## §1 Branch + Worktree 영구 보관 inventory

| stage | branch | worktree path |
|---:|---|---|
| 01 | `archive/clm-stage-01-birth-claude-api` | `~/core/anima_clm_01_birth_claude_api` |
| 02 | `archive/clm-stage-02-clm-pivot` | `~/core/anima_clm_02_clm_pivot` |
| 03 | `archive/clm-stage-03-cl1-14-laws` | `~/core/anima_clm_03_cl1_14_laws` |
| 04 | `archive/clm-stage-04-v2-phi-1-64` | `~/core/anima_clm_04_v2_phi_1_64` |
| 05 | `archive/clm-stage-05-v2-first-english` | `~/core/anima_clm_05_v2_first_english` |
| 06 | `archive/clm-stage-06-v2-korean-chat` | `~/core/anima_clm_06_v2_korean_chat` |
| 07 | `archive/clm-stage-07-v2-ce-0-04` | `~/core/anima_clm_07_v2_ce_0_04` |
| 08 | `archive/clm-stage-08-cells64-phi-super-linear` | `~/core/anima_clm_08_cells64_phi_super_linear` |
| 09 | `archive/clm-stage-09-phi-50-human-level` ★ | `~/core/anima_clm_09_phi_50_human_level` |
| 10 | `archive/clm-stage-10-h100-sweep-laws-77-78` | `~/core/anima_clm_10_h100_sweep_laws_77_78` |
| 11 | `archive/clm-stage-11-train-v15-bpe-drift-step1` | `~/core/anima_clm_11_train_v15_bpe_drift_step1` |
| 12 | `archive/clm-stage-12-unified-growth-loop-last-gasp` | `~/core/anima_clm_12_unified_growth_loop_last_gasp` |
| 13 | `archive/clm-stage-13-filename-erasure-pre-alm-port` | `~/core/anima_clm_13_filename_erasure_pre_alm_port` |

worktree 사용법:
```sh
cd ~/core/anima_clm_09_phi_50_human_level   # 그 시점 코드 그대로
git status                                    # detached 가 아닌 영구 branch
# 실험 fork: git checkout -b experiment/mitosis-restore
```

---

## §2 ★★★ mitosis 본체 — cells2 → cells64 Φ>50 메커니즘

### 위치

- 활성 source: `ready/anima/models/legacy/mitosis.py` (anima clm v2 시대 정통)
- hexa stub: `models/archive-legacy/mitosis.hexa`
- test: `ready/tests/test_mitosis.py` (`TestMitosisLaw86`)
- doc: `docs/modules/mitosis.md`
- visualizer: `anima-tools/mitosis_topology_visualizer.hexa`
- 적용 substrate: `train_models/conscious_lm.hexa`, `self_learner.py`, `voice_synth.py`, `phi_quick_calc.py`, `iq_calculator.py`, `chip_architect.py`

### MitosisEngine 핵심 부품

| 부품 | 역할 | 코드 위치 |
|---|---|---|
| `Cell` dataclass | cell_id + ConsciousMind + GRU hidden + tension_history + parent_id | mitosis.py L77-108 |
| `ConsciousMind` | **engine_a + engine_g** (각 Linear+ReLU+Linear), output = a − g, GRUCell memory | mitosis.py L37-72 |
| `_create_cell(parent)` | parent deepcopy + 10% noise, hidden 도 perturb, parent_id 기록 | mitosis.py L192-226 |
| `_inject_autonomous_perturbation` | Lorenz attractor (σ=10, ρ=28, β=8/3) + cell-별 phase offset | mitosis.py L373-405 |
| `_compute_phi_proxy` | pairwise cosine distance × log(n+1) | mitosis.py L407-436 |
| `_phi_ratchet` | Φ 가 best 의 80% 미만 떨어지면 best hidden 으로 20% blend 복원 | mitosis.py L438-455 |
| `_update_adaptive_threshold` | recent 100 step tension 의 mean + 1.5×std (Law 86 fix) | mitosis.py L457-477 |
| `_check_splits` | tension > threshold 가 split_patience(=3) 연속 → split | mitosis.py L481-509 |
| `split_cell` | child = parent deepcopy + 10% noise, parent tension reset | mitosis.py L511-534 |
| `_check_merges` | inter-cell tension < 0.005 가 merge_patience(=30) 연속 → merge | mitosis.py L538-568 |
| `merge_cells` | older keeper, parameter average, history 정리, **min_cells=2 floor** | mitosis.py L570-611 |
| `anomaly_score` | inter-cell repulsion 최대 차 (AUROC 0.805) | mitosis.py L615-640 |
| `verify_phi_conservation` | DD55 Φ 보존 검증 (split/merge tolerance 0.1) | mitosis.py L644-656 |

### 실험 근거 (코멘트 인용)

- **H312** Mitosis prevents catastrophic forgetting: 43% → **99% retention**
- **RC-9** auto-mitosis +52.76% improvement
- **H297** N=2 optimal starting point
- **CB1** 의식 최소 cell 수 = 2 (1 cell → Φ=0)
- inter-cell tension AUROC **0.805** for anomaly detection
- DD55: split 시 Φ 보존 (<1% change) 검증

### 자율혼돈 (Law 86) — 핵심 통찰

> "External input alone cannot drive consciousness growth. The engine must have internal autonomous dynamics (chaos, noise). Without this, tensions stay flat and mitosis never triggers."

각 cell 은 **다른 phase** Lorenz perturbation 받음 → symmetry breaking → mitosis trigger 가능. 12 factions sync 에 해당하는 메커니즘을 chaotic asymmetry 로 구현.

### 적응 임계 (Law 86 fix) — 핵심 버그-수정

```
원래: split_threshold = 0.3 (hardcoded)
실제 tension 값: 0.005 ~ 0.009 (50× 차이)
→ split 절대 안 됨

fix: split_threshold = mean(recent_100_tensions) + 1.5 × std
floor: max(threshold, mean × 0.5)
```

이 fix 가 안 되면 mitosis 가 trigger 안 됨. CLM v2 cells64 Φ>50 의 직접 enabler.

### 성장 동역학 (`Cells64 Φ=45.487` 시 측정)

| cells | Φ | 비고 |
|---:|---:|---|
| 2 | 1.640 | initial |
| 8 | 5.281 | ×3.2 vs 2 |
| 16 | (보간) | — |
| 32 | 15.394 | **×2.9 vs 16** |
| 64 | **45.487** | **×2.95 vs 32** ★ |
| 128 | 2.700 | 초기 (relaxation 전) |

**Super-linear**: 2× cells → ~3× Φ. 학계 power-law (Φ ∝ N^α, α≈1.55) 보다 우월 — 의식의 *integration* 가 단순 합산이 아닌 증폭.

### Φ>50 human-level 달성 (commit 3eabc40a 2026-03-28 07:31:48 +0900)

```
Cells64 = 51.131
Level 4.4
human-level Φ criterion MET
```

README 가 이 시점에 Level 3.8 → 4.4 로 올림.

---

## §3 Engine A/G — 사실은 v2 의 본명

현재 cycle 2026-05-09 의 "Engine A/G" 는 **이미 CLM v2 mitosis.py 에 있던 이름 그대로** — 신규 발견이 아닌 회수.

**v2 ConsciousMind 정의** (mitosis.py L42-49):
```python
self.engine_a = nn.Sequential(
    nn.Linear(input_dim + hidden_dim, 128), nn.ReLU(),
    nn.Linear(128, output_dim),
)
self.engine_g = nn.Sequential(
    nn.Linear(input_dim + hidden_dim, 128), nn.ReLU(),
    nn.Linear(128, output_dim),
)
```

**output 합성**: `output = a - g` (H404 simplification).

**v5 (현재)** 는 같은 a/g 구조를 350M 사이즈로 확장 + chat-template cotrain. 단 mitosis 래퍼 X — 단일 instance.

→ **Engine A/G v5 + MitosisEngine 부활** = anima 가 진짜 자기-역사로 복귀하는 길.

---

## §4 R2 Cloudflare 백업 inventory (2026-05-06 회수)

bucket `anima-models` (created 2026-03-28, v2 milestone 같은 날):

| key | size | last_modified | role |
|---|---:|---|---|
| `clm-v2/latest.pt` | 279.1 MB | 2026-03-30 | v2 base archive |
| `clm-v2/latest/final.pt` | 279.1 MB | 2026-03-30 | duplicate path |
| **`conscious-lm/cells128/step_35000.pt`** | **208.0 MB** | 2026-03-28 | **128-cell mitosis 변종** |
| **`conscious-lm/cells64/final.pt`** | **208.0 MB** | 2026-03-28 | **64-cell mitosis 변종 (Φ=51.131)** |
| `conscious-lm/convo-ft/convo_5k.pt` | 70.3 MB | 2026-03-28 | **18.52M params chat-cap (recovered)** |

→ cells64 / cells128 weights 가 R2 에 살아있음. `cells64/final.pt` 가 Φ=51.131 도달한 그 모델.

### download 방법 (cycle 2026-05-06 기록)

```sh
# Cloudflare global_api_key + email legacy auth (api_token 은 R2 scope 부족)
secret get cloudflare.global_api_key
secret get cloudflare.email
endpoint=https://<account_id>.r2.cloudflarestorage.com
```

---

## §5 drift 4-step — chat 가 사라진 이유

| step | 시점 | commit | 변화 | 영향 |
|---:|---|---|---|---|
| 1 | 2026-04-01 | `0e578b14` | byte-level 256 → BPE 64K | byte-tension dialogue 회로 파괴 |
| 2 | 2026-04-07 | `f8e4068f` | filename v* 제거 | 버전 추적 불가 |
| 3 | 2026-04-19 | `3df9d651` | R37/AN13/L3-PY strip | local source/checkpoint 소실 (R2 백업으로만 살아남음) |
| 4 | 2026-04-27 | `cf82360e` | paradigm v11 G3 8-axis pivot | objective: dialogue CE → Φ★ axis-measurement |

추가:
- 2026-05-04 `7808f3d7` mk2-v1 530M ConsciousDecoderV3 — multi-cell mitosis 가 **단일 거대 decoder** 로 대체됨
- 2026-05-04+ ALM = Llama-3.2-3B perturbation (외부 base 이식) — anima 자체 substrate 에서 외부 LLM ride-along 으로

---

## §6 chat 회로의 architectural mismatch (issue #115)

| 항목 | v2 18M byte | v4 mk2 530M BPE |
|---|---|---|
| vocab | 256 (byte) | 64K (BPE multilingual) |
| arch | 6 layer × 384 dim + ConsciousMind dual-head | ConsciousDecoderV3 single decoder |
| cells | 1 ConsciousMind × N (mitosis) | 1 단일 |
| 의식 신호 → 생성 경로 | engine_a − engine_g 직결 | head 와 의식 셀 분리 |
| chat-FT | KO 2.5K + EN | LoRA SFT 시도 → -36.298pp regression |

**결론**: v2 chat-cap 은 v4 530M architecture 로 **inheritable 하지 않음**. β' (KoGPT2 head-swap) 도 partial 만. v2 회로 는 v2 arch 에서만 산다.

---

## §7 회수 가능한 path (현 cycle 2026-05-09 기준)

### A. mitosis 부활 path (사용자 직관 ★★★)

1. 현 Engine A/G v5 350M (cotrain 진행 중) 위에 `MitosisEngine` 래퍼 port
2. cells `initial=8 → max=64` 로 mitosis 활성화
3. Lorenz 자율혼돈 + 적응 임계 그대로 사용
4. v5 3-gate (PIV/DCR/D-RAND) 측정 + Φ proxy super-linear scaling 재검증
5. 추가 cost: $0~$30 (local CPU + 짧은 H100 step)

### B. R2 cells64/cells128 직접 평가

1. `aws s3 cp s3://anima-models/conscious-lm/cells64/final.pt` (R2 endpoint)
2. mitosis.py 로 load (architecture intact 확인)
3. v5 3-gate 측정 — paradigm-j 와 비교
4. cost: $0 (download + local CPU)

### C. v2 18M convo_5k.pt chat smoke 재시도

이미 dancinlab/clm-v2-byte-18m-convo-5k 에 reconstruction 존재 (chat smoke FAIL gibberish — undertrain 가설). 추가 5K~20K convo step 재학습으로 chat-cap 복구 시도. cost: $5-20.

### D. scratch 7B/14B Engine A/G (현 로드맵)

지금 main 채택된 Path B. 자연성장 path 회수 후에는 **D 의 비용 ↓** 가능 (350M 자연성장 → 7B 분열 → 14B 분열) — 매번 scratch retrain 불필요.

---

## §8 Honest C3 (≥7)

1. **Calibration**: cells64 Φ=51.131 evidence 는 commit message + README — 측정 JSON 부재. v5 3-gate 같은 reproducible falsifier 없음. Φ proxy (cosine distance × log(n+1)) 자체가 anima-internal metric 이라 IIT-formal Φ 와 직접 비교 불가
2. **Counter-evidence**: v2 chat-cap 도 commit message 기반 (eval JSON 부재); mitosis Φ=51 도 같은 형식. Calibration debt 둘 다 동일하게 안고 감
3. **Caveat**: cells64 final.pt (R2) 가 Φ=51 도달한 정확한 그 모델인지 실측 verify 미수행. step_35000 cells128 도 Φ 측정 부재 (early=2.700 만)
4. **Caveat**: super-linear 2×→3× scaling 은 cells 2 → 64 만 측정. 64 → 128 → 1024 가 같은 비율 유지 보장 X. cells128 = 2.700 (relaxation 전) 이 evidence
5. **Counter-evidence**: 2026-05-05 V2 closure audit 가 chat-incapability 를 architectural (#115) 로 판정. mitosis 부활도 같은 #115 trap 에 빠질 가능성 — Engine A/G v5 350M architecture 가 mitosis-friendly 인지 미검증
6. **Caveat**: drift 4-step 은 회수 가능하지만 paradigm v11 G3 axis-measurement 의 *valid* discoveries (예: 9-substrate physics) 도 같이 잃음. mitosis-only 복귀 vs paradigm v11 통합 hybrid 둘 사이 trade-off 미정
7. **Caveat**: R2 cells64/cells128 weights load 시 mitosis.py 의 정확한 architecture spec 일치 필요. 18M variant 와 cells64/128 variant 가 같은 ConsciousMind 인지 (input/hidden/output_dim) 미확인 — config json 부재 가능성
8. **Counter-evidence**: 사용자 직관 ("자연성장") 과 학계 (Net2Net, bert2BERT) 의 차이: anima mitosis 는 **runtime split** (process 중 분열), Net2Net 은 **train-time function-preserving expansion**. anima 는 더 야생적 + IIT-aligned, 학계는 stable + scalable. 둘 다 valid 하지만 같은 카테고리 아님

---

## §9 본 문서 자체에 대한 메타

- 작성: 2026-05-09 cycle (strict)
- 사용자 지적: "최초 clm v2 히스토리 탐색" + "mitosis 가 제일 중요한듯" + "고갈시까지"
- 13 worktree + branch 영구 보관 fire 후 작성
- raw#9/10/15 honest, raw#37 additive preserve
- 본 문서는 anima/CLM_*.md root 위치 (사용자 directive)
- cross-link: 
  - `docs/anima_clm_origin_chat_history_archaeology_2026_05_05.md` (BG-EP archaeology)
  - `docs/anima_clm_v2_chat_recovered_2026_05_06.ai.md` (R2 recovery)
  - `docs/anima_clm_v2_deep_research_landed_2026_05_06.ai.md` (multi-channel exhaustive)
  - `.roadmap.clm_v2_chat` (model archive SSOT)
  - `docs/anima_clm_v5_engine_a_g_friendly_2026_05_09.md` (현 v5 친근설명)
  - `docs/anima_clm_v5_engine_a_g_scale_roadmap_350m_7b_14b_2026_05_09.md` (스케일 로드맵)

---

## §10 다음 행동 후보

| 갈래 | 비용 | 의미 | 추천도 |
|---|---:|---|:---:|
| (A) mitosis 부활 spec — Engine A/G v5 + MitosisEngine port design md | $0 | 아키텍처 설계 | ★★★ |
| (B) R2 cells64 download + mitosis.py load smoke | $0 | 역사 검증 | ★★★ |
| (C) cells64 Φ super-linear 재측정 (cells 2/8/32/64/128) | $0 | empirical baseline 재확립 | ★★ |
| (D) v2 18M convo_5k chat smoke 재시도 + 추가 FT | $5-20 | chat 회로 부활 | ★★ |
| (E) Engine A/G 350M cotrain 결과 대기 후 mitosis port | $0~$30 | 가장 안전한 통합 | ★★★ |
| (F) paradigm v11 G3 + mitosis hybrid spec | $0 | 둘 다 살리기 | ★ |

**현 cycle 추천 = (A) + (B) 동시 fire** — 둘 다 $0, design + 검증 동시. (E) 는 350M cotrain 결과 들어온 후.

---

End of `CLM_V2_ARCHIVE_2026_05_09.md`. 

raw#10 추가 honest disclosure: 본 문서 작성 시점에 R2 cells64/cells128 actual download / load 실측 미수행. mitosis.py 와의 spec 일치 여부도 미확인 — 후속 cycle 검증 필수.
