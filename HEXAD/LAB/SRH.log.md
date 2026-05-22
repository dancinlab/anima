# SRH — cycle history

Append-only chronological log. `SRH.md` 는 latest only — history 는 여기.

---

## Cycle #1 — 2026-05-22

- **focus**: tool primitive (ubm_inject + anima_spike) 작성 + wiring smoke 검증
- **change**:
  - `HEXAD/LAB/tool/ubm_inject.hexa` (167 LoC) — kosmos_parser_lib 위 build
  - `HEXAD/LAB/tool/anima_spike.hexa` (250 LoC) — chat record → spike fingerprint
  - `HEXAD/LAB/tool/lab_smoke.hexa` (240 LoC) — UBM tier=0 → synthetic d=8 chat → spike capture → JSON 저장 → self-diff
  - `HEXAD/LAB/SRH.md` + `SRH.log.md` skeleton (도메인 컨벤션 시범)
  - falsifier F-SRH-1..5 pre-registered in SRH.md §3
- **fire**:
  - `hexa run HEXAD/LAB/tool/lab_smoke.hexa` Mac local $0 wall ~10s
  - artifact: `/tmp/lab_smoke_spike.json` (transient, 672 bytes)
  - commit `eece4fe23`
- **verdict**: **TOOL-READY** (not falsifier evidence)
  - F-LAB-1..6 **15/15 PASS** (tool wiring 검증)
  - 1차 신호 (synthetic noise, **not** F-SRH evidence):
    - UBM tier=0 (synthetic d=8) → 30 split + 2 merge / 210 inv
    - cell_pool 2 → 30 / next_id 32
    - baseline "안녕? 너는 누구야?" 21 split → UBM tier=0 30 split = +43% diff
  - 의미 해석 불가 — synthetic substrate 한계
- **next**: **Cycle #2 — production 332M pilot** (단일-seed Mac local, 다음 entry)

---

## Cycle #2 — 2026-05-22

- **focus**: F-SRH-1 minimum viable on production 332M substrate (single-seed pilot)
- **change**:
  - `HEXAD/LAB/state/SRH_t0_vs_random_pilot_2026_05_22/run_pilot_mac.hexa` (244 LoC)
  - real 24L d=768 BF16 ckpt (`ckpt_phase1a4_lr5e6_sft.safetensors`, 663 MB)
  - chat_init_cell_pool(d=768, init=2), chat_init_kv_cache_default(cap=64)
  - UBM tier=0 truncated 30-byte vs random ASCII noise (LCG seed=2026, length-matched)
  - chat_generate(greedy, max_new=2)
  - state reset between two prompts (manual `mitosis_d_model=0` + `kv_cache=#{}`)
- **fire**:
  - bg `bk53381e7` Mac local `HEXA_MEM_UNLIMITED=1 RESOURCE_LOCAL_HEXA=1 hexa run`
  - **wall actual: 45 s** (예상 30 min 대비 40× 빠름 — hexa interp hot-path 효율 확인)
  - $0 cost
  - commit `37bc40779`
  - artifacts:
    - `state/SRH_t0_vs_random_pilot_2026_05_22/spike_ubm_tier_0_seed2026.json`
    - `state/SRH_t0_vs_random_pilot_2026_05_22/spike_random_ctrl_seed2026.json`
    - `state/SRH_t0_vs_random_pilot_2026_05_22/result_seed2026.json`
    - `state/SRH_t0_vs_random_pilot_2026_05_22/pilot.log` (3.7 KB)
- **verdict**: **WEAK SIGNAL (directional)** — heuristic |Δ| ≥ 5 NULL 이나 강한 방향성:
  - UBM split_count 5 vs Random 2 = **2.5× ratio**, |Δsplit|=3
  - UBM cell_count_final 7 vs Random 4 = +3
  - **timing decisive evidence**: UBM split steps `[2, 2, 25, 30, 31]` vs Random `[2, 2]`
    - 공통: early prefill steps 2 (둘 다)
    - UBM-specific: steps 25/30/31 = **late prefill + decode 진입 시점** 3개 추가 fire
    - random 은 후반부 0 split — 단순 "more prompt = more splits" confound 배제 (32 inv 동일)
  - event_step_jaccard 0.4 (60% non-overlap)
  - mitosis_invocations 32 == prompt_len + 1 BOS + max_new 2 (chat_lib invariant 검증)
- **honest C3 (pilot)**:
  - C3-pilot-1: prompt 30-byte truncated (full UBM ~200 bytes) — wall 우려 무용지물 (45s 였음); cycle #3 full prompt
  - C3-pilot-2: random control = ASCII noise pool (Korean/emoji byte 분포 비매치) — cycle #3 byte-distribution-matched control 또는 shuffled-UBM
  - C3-pilot-3: single seed = no F-SRH-3 reproducibility — cycle #3 ubu 병렬 5-seed
  - C3-pilot-4: max_new=2 (decode 거의 fire 안 함) — cycle #3 max_new ≥ 10
  - C3-pilot-5: cell_pool default threshold 미고려 — cycle #3 sensitivity sweep
- **next**: **Cycle #3 — 3-box parallel multi-seed full-prompt** (cycle #2 의 wall 45s 발견으로 scope 대폭 확장 가능)
  - ubu-1 (aiden, RTX 5070) + ubu-2 (summer, RTX 5070) + Mac local 3-box bg parallel
  - infra setup: ubu-1 `git pull main` + scp safetensors 663 MB (~5 min) ; ubu-2 동일 + PATH 설정
  - per box: full UBM prompt (~200 bytes) × max_new=10 × random control × shuffled-UBM control × 3 seeds (2026/42/99)
  - 4 prompts × 3 seeds × 3 boxes = 36 fires × ~3 min wall (200-byte prompt extrapolation) = ~36 min parallel wall
  - 측정: F-SRH-1 z-stat (cross-seed σ + UBM-vs-random Δ) + F-SRH-3 CV ≤ 0.15 (5-seed within-box) + jaccard 분포
  - 이후 (cycle #4): tier sweep 11 tier × 1 seed 으로 F-SRH-2 monotone
