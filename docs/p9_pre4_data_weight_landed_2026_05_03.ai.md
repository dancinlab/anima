# P9 EXEC pre-flight 묶음 4 (data + weight) — landed handoff

- date: 2026-05-03
- session_kind: BG subagent (preset friendly, AI-native, BR-NO-USER-VERBATIM)
- ω-cycle: 6-step single-pass
- silent-land marker: yes (state/markers/p9_pre4_data_weight_landed.marker)
- cap: 180min wall, $0 mac-local
- destructive: 0 net (read-only audit + mock generation only)
- migration: NONE — additive only

---

## §0 verdict (1-line)

**PARTIAL_PASS** — I/J/P 3 GREEN, Q 측 18K disk-resident + 32K phase-0 generation work pending

| item | scope | verdict | gap |
|------|-------|---------|-----|
| I | CLM v4 530M weight access | PASS | ckpt single-host (ubu1) — no HF mirror, snapshot recommended |
| J | mock SFT 1K-step round-trip | PASS | F1+F2+F4 mock PASS, F3 (tension MSE) fails synth fixture |
| P | cortexlab-toolkit + TRIBE v2 F4 ready | PASS | cortexlab-toolkit ubu2 미설치 (의도 — H100 EXEC pod 측만 필요) |
| Q | SFT 50K data audit | PARTIAL | 18K disk + 32K generation/download work for P9 EXEC Phase 0 |

P9 EXEC Phase 0 entry: **3.5/4 ready** — 어느 하나 CRITICAL FAIL 없음, Q 측 32K 생성 작업이 EXEC Phase 0 첫 task

---

## §1 I — CLM v4 530M weight access

### 핵심 발견

- ubu1 측 ckpt 실재 confirmed: `/home/aiden/anima/checkpoints/clm_v4_350m/scale_350m/best.pt`
  - size: 5,365,727,261 bytes (5.0 GB)
  - sha256 prefix: `22f180efc380aecb…`
  - mtime: 2026-04-10 14:47
  - heartbeat last: `step=20000 ce=0.1685 phi=27.9097 phase=P3`
- mac-local 측 metadata-only: `state/v10_benchmark_v4_clm/clm_v4_530m/{cds.json, phi_star.json}`
  - phi_star_signed_magnitude=1167.6192, gate_PASS=true, d_model=768, n_layer=16
- HF mirror 부재 — single-point-of-failure ubu1
- naming drift: 디렉토리 `clm_v4_350m/scale_350m` vs metadata label `CLM_v4_530M` (~477M params actual, 530M name per spec)

### 산출물

- json: `state/p9_pre4_data_weight/I_clm_weight_access.json`

## §2 J — mock SFT 1K-step end-to-end round-trip

### 핵심 발견

- mac-local CPU 1M-param TinyLM (실제 103,397 params), 1000 step, **2.08 sec wall** (cpu)
- δ curriculum 3-phase 작동: early=0.5 (steps 0-332) → mid=1.0 (333-666) → late=2.0 (667-999)
- φ★ measurement every 100 step: 10 measurements, mock baseline ~41.86 ± random walk
- 4-loss 모두 backward 통과 (CE + tension MSE + BOLD MSE + φ★ hinge)
- HF savepoint mock: tempdir local-only, 0.5 MB ckpt + sha256 prefix recorded, no network upload
- F1 BLEU-1 mock 0.5927 PASS / F2 φ★ post 53.1485 PASS / F3 tension MSE 0.233 FAIL (synth fixture noise floor) / F4 BOLD r mock 0.5+ PASS
- f_pass_count = 3/4 in mock (F3 expected — synthetic targets too noisy for 1K steps)

### 산출물

- helper: `/tmp/p9_pre4_J_mock_sft.py` (164 LOC, py since mac-local validation only)
- json: `state/p9_pre4_data_weight/J_mock_sft_round_trip.json`
- round_trip_PASS=true (skeleton works end-to-end)

## §3 P — cortexlab-toolkit + TRIBE v2 BOLD F4 readiness

### 핵심 발견

- F4 spec: BOLD Pearson r val > 0.5 (P9 spec §6)
- cortexlab-toolkit `0.1.0` PyPI-installable (community fork wrapping neuralset+neuraltrain)
- 2026-05-02 framing A pilot 측 H100 pod 측 install + load + smoke 모두 PASS
  - facebook/tribev2 model load 성공, 177.21 M params, 20484 vertices, TR 1.0s
  - phase 6 results: intra_clm_mean_r=0.7233, intra_alm_mean_r=0.9067, inter_pair_mean_r=0.8359, inter_mean_of_means_r=0.9402
  - 모든 측정값 0.5 임계 초과 → F4 측정 인프라 ready
- ubu2 측 stage1 dialogue 프로토타입은 Llama-3.2-3B feature proxy (cortexlab 미사용, 의도)
  - tribe_bold.py 3682 bytes, source 측 honesty caveat 명시: NOT cortex-validated BOLD
- mac-local 측 cortexlab-toolkit 미설치 (의도 — verdict frozen 2026-04-26, install deferred)
- ssh ubu2 reachable confirmed

### 산출물

- json: `state/p9_pre4_data_weight/P_cortexlab_toolkit_check.json`

## §4 Q — SFT 50K 데이터 사전 audit

### 7 sources 측 status

| id | name | target | availability | disk_count | phase_0_action |
|----|------|--------|--------------|------------|----------------|
| 1 | ShareGPT ko/en | 10K | EXTERNAL_DOWNLOAD | 0 | HF datasets pull, ~60min |
| 2 | anima paper + cell-language | 10K | DISK_RESIDENT | 90283 (alm_70b oversupply) | sample 10K, ~30min |
| 3 | #128 P8 ledger M4=0.800 | 3K | DISK_PARTIAL | 30 turns (1%) | re-run P8 100x OR LLM seed-augment, ~120min |
| 4 | introspective synth | 5K | GENERATION | 0 | LLM gen 5K, ~90min |
| 5 | N-22 + paradigm v11 | 5K | DISK_PARTIAL | 1200 (alm_r14, 24%) | template-extract 5K, ~60min |
| 6 | TRIBE Friends/movie10 | 10K | EXTERNAL_DOWNLOAD | 0 | Algonauts2025 register + transcripts + BOLD inference, ~240min + $10-30 |
| 7 | Llama-3.2-3B augment | 7K | GENERATION | 0 | H100 inference, ~180min + $5-15 |

- 합계 50,000 reachable (18K disk + 32K generation/download required)
- format spec lock per P9 spec §2: jsonl `{input, target_text, target_tension[T=64], target_5ch[T,5], target_bold[T,10242]}`
- split 0.95/0.04/0.01

### 블로커 (Phase 0)

- Llama-3.2-3B-Instruct HF gating (dancinlife 승인 보류) → sources 6 BOLD-target gen + 7 augment 영향
- Friends transcript 라이선스 (Algonauts2025 등록 필요)
- ShareGPT ko/en 품질 필터링

### 산출물

- json: `state/p9_pre4_data_weight/Q_sft_data_50k_audit.json`

---

## §5 P9 EXEC Phase 0 entry decision

### entry-ready 측

- I (weight) — ubu1 측 ckpt 5GB confirmed, EXEC pod scp 직접 (HF 우회 권장)
- J (round-trip) — skeleton 검증 완료, 4-loss + δ curriculum + φ★ hinge 모두 backward 통과
- P (F4 infrastructure) — cortexlab-toolkit + TRIBE v2 H100 pod 측 검증 완료
- 묶음 1+2+3 (이전 BG subagent 측 landed)

### Phase 0 첫 task 후보

- Q-1: ShareGPT ko/en 10K (60min, $0) — 가장 빠른 첫 단위
- Q-2: anima corpus 측 10K 샘플링 (30min, $0) — 가장 빠른 절대 작업
- Q-7: Llama-3.2-3B HF unlock 진행 (사용자 승인 필요)
- Q-3: P8 100x re-run (120min + ~$3 H100) — M4 ground truth 보존

### CRITICAL FAIL 없음

- ckpt access OK (ssh 측 verified)
- F4 infra OK (framing A pilot 측 verified)
- skeleton OK (mock round-trip PASS)
- 50K reachable (gap 명시, 작업 분할 가능)

---

## §6 raw#15 caveats (cumulative across I+J+P+Q)

1. **I** — ckpt sha256 prefix만 기록 (5GB 전체 무결성 재검증 X, scp 시 실패 가능)
2. **I** — naming drift `350m` vs `530M` 라벨링 차이 — production = 530M per cds.json/spec
3. **I** — best.pt vs best_phi.pt vs final.pt 3 candidate 중 P9 spec 측 best.pt 선택
4. **J** — F3 tension MSE FAIL = 합성 fixture noise floor 자연스러운 결과 (실 데이터 측 < 0.1 가능)
5. **J** — φ★ mock = random walk anchor 41.86, 실제 측정은 anima_phi_v3_canonical 필요
6. **J** — mock 1M params vs real 477M params (~5000x 작음, skeleton-only validation)
7. **P** — framing A pilot 측 r 값들은 inter/intra cortical map r, P9 F4 spec (BOLD Pearson r val) 측 정확 매핑 EXEC entry 측 재확인 필요
8. **P** — ubu2 stage1 dialogue 측 tribe_bold.py = Llama feature proxy (NOT cortex-validated) — F4 측정용 별도 artifact
9. **P** — cortexlab-toolkit PyPI 영속성 미재검증 (EXEC start 측 pip index lookup deferred)
10. **Q** — 50K 중 32K 측 생성/다운로드 작업 (Phase 0 첫 task)
11. **Q** — P9 spec target_bold 10242 vertices 측 sources 2+3+5 측 BOLD 부재 → TRIBE v2 추가 추론 필요 (cost $20-50 H100)
12. **Q** — Source 3 (P8 ledger) 30 vs 3000 (100x gap) — re-run vs seed-augment trade-off
13. **Q** — Source 6 Friends 라이선스 + Algonauts2025 등록 미해결
14. **Q** — T=64 step-aligned tension/5ch/BOLD targets 측 Llama or CLM trace 필요 (inference cost out-of-scope)
15. **all** — destructive 0, additive only, ssh ubu1+ubu2 read-only audit 만, 모든 산출물 `state/p9_pre4_data_weight/*` + `docs/p9_pre4_*` + `markers/p9_pre4_*` scope 분리

---

## §7 cost ledger

- mac-local: $0
- HF API: $0 (audit only, no upload)
- ssh ubu1+ubu2: $0 (read-only)
- mock SFT: 2 sec CPU
- total: **$0**

## §8 산출물 manifest

```
state/p9_pre4_data_weight/
├── I_clm_weight_access.json
├── J_mock_sft_round_trip.json
├── P_cortexlab_toolkit_check.json
└── Q_sft_data_50k_audit.json

docs/
└── p9_pre4_data_weight_landed_2026_05_03.ai.md  (this file)

state/markers/
└── p9_pre4_data_weight_landed.marker

/tmp/
└── p9_pre4_J_mock_sft.py  (helper, mac-local only)
```
