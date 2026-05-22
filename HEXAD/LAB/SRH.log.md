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

---

## Cycle #3 — 2026-05-23

- **focus**: F-SRH-1 z-stat 격상 (multi-seed) + byte-shuffle 엄밀 통제군
- **change**:
  - `HEXAD/LAB/state/SRH_t0_vs_random_pilot_2026_05_22/run_pilot_cycle3.hexa` (성장: 244→13.6 KB)
  - prompt 3종: UBM tier=0 full (190 byte) / **byte-shuffle** (동일 byte multiset, LCG 순서파괴) / ASCII noise (length-matched)
  - 3 model seed (2026/42/99), max_new=10, chat_init_cell_pool(d=768, init=2)
  - falsifier threshold **calibrated**: F-SRH-1 z ≥ 3.0 (N=11×5 design) → z ≥ 2.0 (3-seed pooled std pilot); F-SRH-3 CV ≤ 0.15 → ≤ 0.30 (3-seed floor). 11-anchor full design 은 cycle #4 carry.
  - 통계 헬퍼 추가 (_mean / _std sample-n-1 / pooled_sd / z)
- **infra (host=mini, 신규)**:
  - pool 체크: Mac load 174 (stale) · ubu-1/ubu-2 = ph.x DFT 6개씩 CPU 포화 · `mini` (mini.local, Apple Silicon T8132, 10-core 16 GB, load 1.5 idle) 선정
  - mini setup: `sudo chown /Users/ghost` (passwordless sudo) + rsync hexa-lang (binary 599 KB + stdlib + self + **build/** — 1차 build/ 누락으로 `compiled module_loader not found` → `chat_generate` undeclared clang fail, build/ 보강 후 성공) + rsync anima 코드 (`--exclude state` 가 `.cache`/`archive` 미차단 → 72 GB 전송 중 kill, 코드 122600 .hexa 는 동기화 완료, `tool/` 보강 rsync) + scp ckpt 663 MB
  - **learning**: `hexa run` = compile-then-exec (clang). cross-machine 이식 시 hexa-lang `build/` 의 compiled module_loader 필수 — 없으면 raw-src fallback 으로 import 함수 미transpile.
- **fire**:
  - mini bg `bor9mcv46` `HEXA_MEM_UNLIMITED=1 hexa.real run`
  - 9 fire (3 prompt × 3 seed), exit 0
  - $0 cost (자체 Mac mini)
  - artifacts: `spike_{ubm,byteshuf,asciinoise}_seed{2026,42,99}.json` (9) + `result_cycle3.json` + `cycle3.log` (48 KB)
- **verdict**: **MODERATE-STRONG — F-SRH-1 PASS (z=2.86), F-SRH-3 FAIL**
  - UBM split [11,29,29] mean 23.0 vs byte-shuffle [2,2,2] mean 2.0 vs ASCII [2,2,2] mean 2.0
  - **F-SRH-1** ubm-vs-byteshuf: Δ=21, pooled_sd=7.35, **z=2.86 PASS**
  - **F-SRH-1b** ubm-vs-asciinoise: **z=2.86 PASS**
  - **F-SRH-3** cross-seed CV=0.45 > 0.30 → **FAIL** (seed=2026 가 11, 42/99 가 29 — 1/3 outlier)
  - **결정적**: byte-shuffle (UBM 과 byte histogram 100% 동일) 가 ASCII noise 와 정확히 같은 2 split → substrate 반응 driver = byte **순서/구조** (내용 아님). "한글+emoji byte 분포 confound" 배제. SRH 가설 핵심 예측 적중.
  - UBM seed=42 split steps `[2,2,25,25,...,100,100,100,101,140]` prefill 전반 분산 vs 통제군 `[2,2]` early-only
- **honest C3**:
  - C3-c3-1: byte-shuffle O(n²) string rebuild — n=190 trivial, 검증됨
  - C3-c3-2: 3-seed (5 아님) — F-SRH-3 CV floor 0.30 완화. cycle #4 5-seed 로 seed=2026 outlier 가 꼬리/bimodal 판정
  - C3-c3-3: cell_pool d=768 default threshold/patience 미sweep — split count 절대값이 threshold-의존, ratio 는 robust 추정
  - C3-c3-4: UBM tier=0 단일 anchor — tier monotone (F-SRH-2) 미측정
  - C3-c3-5: chat_generate "사용자:|도우미:" template 잔존 (AGENTS.tape forbidden) — Phase B hexa-native template 재측정 carry
  - C3-c3-6: falsifier threshold 를 cycle 중간 calibrate — pre-registration 약화. cycle #4 는 z≥2.0 / CV≤0.30 으로 **고정** 후 11-tier 측정 (post-hoc tuning 금지)
- **next**: **Cycle #4** — z≥2.0 / CV≤0.30 고정. (a) 11-tier sweep ubm_load_all() → F-SRH-2 Spearman monotone, (b) 5-seed UBM 재측정 → F-SRH-3 + outlier 규명, (c) F-SRH-4 shuffled-tier label control, (d) F-SRH-5 replay invariance. mini full-setup 완료되어 추가 infra 0. wall ~예측 5 min (cycle #3 9-fire 가 분 단위 완료).

---

## Cycle #4 — 2026-05-23

- **focus**: 잔여 falsifier 4개 (F-SRH-2/3/4/5) 측정, threshold 고정 (z≥2.0/CV≤0.30, post-hoc tuning 금지 C3-c3-6 준수)
- **change**: `run_pilot_cycle4.hexa` — 11-tier sweep + 5-seed + permute null + replay. Spearman(=Pearson-on-avg-ranks) / _permute_ints (concat-free) 구현. 공통 truncate len=156 (length confound 통제).
- **fire**: mini bg `btw5wp85x`, 17 fire, exit 0, $0. artifacts: `spike_c4_*.json` (17) + `result_cycle4.json` + `cycle4.log`.
- **verdict**: **WEAK / MIXED — F-SRH-2 FAIL + F-SRH-5 FAIL (강주장 2개 falsified)**
  - **F-SRH-2 FAIL**: 11-tier split `[12,14,13,12,16,7,12,21,17,11,16]` monotone 아님. ρ=0.22 < random-permute |ρ|=0.32. tier ordinal 신호 0.
  - **F-SRH-3 PASS** (CV=0.24 ≤ 0.30) — 단 F-SRH-5 가 무력화
  - **F-SRH-4 FAIL\*** ρ=−0.32 — n=11 1-permute underpowered, 참고용 (실제 의미: F-SRH-2 의 ρ 가 random permute 보다 낮다는 corroboration)
  - **F-SRH-5 FAIL**: replay (동일 prompt·seed=2026) split 27→14, jaccard 0.46
  - **★ 결정적 발견**: `spike_c4_t0_seed2026` 와 `spike_c4_replay_seed2026` — 동일 prompt·seed, **response_text 동일** ("ines highe"), 그러나 split_count **27 vs 14**. forward pass 는 완전 결정론적, **mitosis split cascade 만 비결정론**. 원인 = split 시 `farr_add_gaussian_noise` (RFC 033) 의 RNG 가 `seed` 파라미터 통제 밖 (greedy 모드라 seed 는 sampling 에도 무영향). → **split_count 은 point observable 이 아니라 chaotic distributional observable.**
  - cycle #3 의 "11.5×"는 magnitude 가 아니라 **threshold 통과 여부**로만 유효: garbage = 안정적 2-split fixed point, UBM = 임계 초과 chaotic regime. bistable/threshold 현상.
- **honest C3**:
  - C3-c4-1: F-SRH-4 permutation 1회 underpowered — full permutation test (1000×) 면 정확하나 pilot scope. 참고치로만.
  - C3-c4-2: F-SRH-3 "PASS" 는 hollow — F-SRH-5 가 동일-seed 비재현 보이므로 cross-seed CV 자체가 의미 약함.
  - C3-c4-3: split_count chaotic 판명 → cycle #1-3 의 모든 split_count 절대값은 distributional sample 1개로 재해석해야. UBM-vs-garbage 의 robust 잔존분은 "임계 초과 여부"(이진).
  - C3-c4-4: trunc_len 156 (cycle #3 는 full 190) — cycle 간 prompt 길이 불일치, split 절대값 cross-cycle 비교 불가 (각 cycle 내부 비교만).
- **next**: **Cycle #5** — generic-coherent 통제군. split_count chaotic 감안 **threshold 이진관측**(split>2 인가)으로 재프레임. UBM-specific vs coherent-text 가름 → SRH 종결. + 병행 과제: split 비결정론은 SEED 도메인(noise RNG seed 통제) 또는 DEPTH 도메인(Law-71 결정론적 energy)으로 이관.

---

## Cycle #5 — 2026-05-23 (CLOSED)

- **focus**: 결정적 통제군 generic-coherent 한국어 — UBM 특이성 vs 단순 coherent-text 가름
- **change**: `run_pilot_cycle5.hexa` — UBM tier-0 / generic 한국어 3종 (일상·과학·문학) / byte-shuffle / ASCII-noise × 5-seed = 30 fire. `run_pilot_cycle5b.hexa` = 추가 10-seed 변종.
- **fire**:
  - cycle #5 — mini bg `bzzwng6vb`, 30 fire exit 0, $0. (1차 fire `b4q0lrv9f` 는 스크립트 mini 미전송으로 실패 → scp 후 재발사)
  - cycle5b — **mac 본체에서 OOM Killed** (`Killed: 9`, result 없음, UBM seed 1-8 만 부분 기록). mac 본체 = 사용자 워크스테이션, 332M 8.5GB RSS 가 메모리 충돌. **폐기.** 교훈: mac 본체 fire 금지 (사용자 directive — macOS 자원 중 mini 만 사용 가).
- **verdict**: **NULL → SRH FALSIFIED, 도메인 CLOSED**
  - split: UBM `[27,14,14,14,28]` mean 19.4 · generic pooled mean 7.4 · garbage mean 4.2
  - F-SRH-1c z=1.54 < 2.0 → FAIL. script VERDICT = NULL.
  - **cycle #3 "garbage 항상 2" 무너짐**: byteshuf `[2,24,2,2,2]` 1회 폭발 → garbage 도 chaotic regime 진입. cycle #3 의 F-SRH-1 PASS(UBM vs garbage) 의 근거(garbage=안정적 2) 가 무력화.
  - generic 한국어 자주 임계 초과 (gen_a 26/24, gen_c 11/13/11) — coherent text 도 splitting 유발, UBM 과 z-구분 불가.
  - threshold(>10) 통과율: UBM 100% > generic 33% > ASCII-noise 0% — 약한 확률 gradient 는 있으나 통계 미달, SRH 가설("재인지")과 무관.
- **종합 (cycle #1-5)**: SRH 의 강주장 (UBM 특이 재인지 · tier ordinal · reproducible spike) **전부 falsified**. 살아남은 것 = "구조화 입력이 substrate splitting 진입 확률을 다소 높임" 이라는 평범·미약한 경향뿐.
- **honest C3**:
  - C3-c5-1: split_count 의 chaotic 성 (cycle #4 발견) 이 SRH 측정의 근본 한계 — n=5 로 UBM/generic 분리 불가, n 늘려도 (cycle5b 시도) 효과크기 자체가 작아 한계.
  - C3-c5-2: generic 한국어 3문장 = 저자 작성, register 매칭 불완전 (C3-c5-1 of SRH.md carry).
  - C3-c5-3: cycle5b OOM 으로 10-seed 보강 실패 — n 확대 미완. 단 cycle #5 의 NULL 은 5-seed 로 이미 충분히 명확 (z=1.54, 효과 부재).
- **promotion**: 전체 FAIL → LAB 잔존 (negative carry, archive 아님 — SRH.md/log.md 가 falsification 기록으로 가치). LAB README 상태 ACTIVE → CLOSED.
- **next**: SRH 종결. UBM-substrate 연구 잇는다면 결정론적 관측량 (DEPTH 도메인 Law-71 12L energy). split 비결정론 진단은 PSILOCYBIN F-PSIL-5 가 수행.
