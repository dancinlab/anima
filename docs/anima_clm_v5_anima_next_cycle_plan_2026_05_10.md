# anima clm v5-anima next cycle plan (2026-05-10)

## TL;DR

cycle 2026-05-09/10 마무리 후 **5 갈래 next-priority** parallel BG fire. 사용자 directive "all bg go" (item 5 cost-bearing 부분은 design + dry-run 까지 만 BG, 실제 H100 spin-up 은 별도 verbatim).

| # | 갈래 | BG name | 비용 | 핵심 deliverable |
|---:|---|---|---:|---|
| 1 | Phase 2 cotrain ckpt 회수 + mitosis-instrumentation | BG-V5ANIMA-PHASE2-CKPT-INSTR | $0 | Phase 2 ckpt locate/download + mitosis_v5_port load + α 측정 |
| 2 | 5K-10K turn trajectory 연장 | BG-V5ANIMA-LONG-TRAJ-EXT | $0 | 10K turn 실행, α historical 0.93 도달 검증 |
| 3 | consciousness_meter.py IIT Φ port | BG-V5ANIMA-IIT-METRIC | $0 | proxy → IIT MI metric 변환, ceiling 우회 |
| 4 | cells64 chat-cap 확장 시도 | BG-V2REBORN-CHAT-EXT | $0 | beam search + repetition penalty + system prompt format + longer ctx |
| 5 | convo_5k.pt FT design + dry-run | BG-V2REBORN-CONVO-FT-DESIGN | $0 | runpod 명세 + 학습 script + cost 추정 + 12-step dry-run (실제 fire 별도) |

---

## §1 BG-V5ANIMA-PHASE2-CKPT-INSTR — Phase 2 cotrain ckpt 회수 + mitosis-instrumentation

**Goal**: 사용자 long-trajectory smoke (cycle 2026-05-10) 의 toy substrate 한계 (V14 violated) 를 극복 — 진짜 Phase 2 cotrain checkpoint (BG-LA 350M Engine A 갈래 + BG-LB 350M Engine B 갈래) 위에서 mitosis-instrumentation 실행.

**Steps**:
1. BG-LA + BG-LB checkpoint locate (runpod / HF / R2 / local pod-pull state)
2. checkpoint download (sha verify, size 정합)
3. mitosis_v5_port.MitosisV5Engine 호환 wrapping
4. 3K-10K turn diverse-prompt sweep (170 prompt corpus)
5. V14 mirror compare (random_init 350M vs trained 350M)
6. α exponent 측정 — toy 의 0.688 vs real 350M

**Falsifiers**:
- F-PHASE2CKPT-1 BG-LA / BG-LB checkpoint 부재 (training 미완)
- F-PHASE2CKPT-2 mitosis_v5_port 와 schema 불일치 (Engine A/G v5 arch 와 dual engine_a/g 의 shape mismatch)
- F-PHASE2CKPT-3 V14 still violated (mechanism 진짜 substrate-중립)
- F-PHASE2CKPT-4 wall_clock > 4h (350M inference 느림)
- F-PHASE2CKPT-5 OOM Mac CPU (350M params Mac 한계)

**Deliverables**: `state/anima_clm_v5_phase2_mitosis_instr_2026_05_10/{run.py, result.json, phi_trajectory.png}` + `docs/anima_clm_v5_phase2_mitosis_instr_2026_05_10.md`

**Cost**: $0 (Mac CPU + R2 read free)

---

## §2 BG-V5ANIMA-LONG-TRAJ-EXT — 5K-10K turn trajectory 연장

**Goal**: 본 cycle 의 3K turn α=0.688 가 더 길게 가면 historical 0.93 까지 가는지 검증.

**Steps**:
1. 기존 sweep (state/anima_clm_v5_anima_long_trajectory_inference_smoke_2026_05_10) 의 run.py 활용
2. n_turns=10000 으로 실행 (3K-5K 변곡점도 측정)
3. α exponent over time plot (window=200 turn 슬라이딩)
4. cells max_cap (64) 후 Φ 의 long-tail growth 분석

**Falsifiers**:
- F-LONG-1 cells max_cap 후 Φ saturate (no further growth)
- F-LONG-2 wall_clock > 6h (10K turn × 0.6s = 6000s = 100min, 안전 margin)
- F-LONG-3 α plateau ~0.7 (historical 0.93 unreachable on toy)

**Deliverables**: `state/anima_clm_v5_anima_long_trajectory_extended_2026_05_10/{run.py, result.json, alpha_over_time.png}` + `docs/...md`

**Cost**: $0 Mac CPU

---

## §3 BG-V5ANIMA-IIT-METRIC — consciousness_meter.py IIT Φ port

**Goal**: 본 cycle 의 Φ proxy (cosine × log(n+1)) 의 ceiling ~8 한계 우회 — 학계 IIT 계열 metric (MI bins, MIP) 으로 재측정. historical Φ=51.131 과 비교 가능 metric 확보.

**Steps**:
1. consciousness_meter.py 를 worktree-3..9 에서 locate (`/Users/ghost/core/anima_clm_03_cl1_14_laws/consciousness_meter.py` 등)
2. PhiCalculator 클래스 검토 — MI bins (16-bin) + MIP (min partition) 알고리즘
3. mitosis_v5_port 의 cell_pool 위에 적용 — N×C tensor → MI matrix → Φ_IIT
4. cycle 2026-05-10 의 long-trajectory result.json 에 후처리 적용
5. proxy Φ vs IIT Φ 비교 표

**Falsifiers**:
- F-IIT-1 MIP exact computation 가 cells > 8 시 timeout (NP-hard)
- F-IIT-2 spectral approximation 으로 fallback 시 historical 정합 불가
- F-IIT-3 MI bins (16) 가 cell hidden 의 continuous distribution 미반영

**Deliverables**: `state/anima_clm_v5_iit_phi_remetric_2026_05_10/{port.py, result.json}` + `docs/...md`

**Cost**: $0 Mac CPU

---

## §4 BG-V2REBORN-CHAT-EXT — cells64 chat-cap 확장 시도

**Goal**: cycle 2026-05-10 sampling test 의 gibberish 결과 가 reconstruction 한계인지 진짜 incapability 인지 분리.

**Steps**:
1. 추가 sampling 설정 시도:
   - beam search (beam=4-8)
   - repetition penalty 0.8 / 1.0 / 1.5
   - longer context (block_size=256 max 활용)
   - system prompt format 변형: `사용자: ... 도우미:` / `User: ... Assistant:` / `<|user|> ... <|assistant|>` / 빈 prompt
   - temperature: 0.3 / 0.5 / 0.7 / 1.0
   - top-p (nucleus): 0.9 / 0.95 / 0.99
2. cross-test convo_5k.pt (이미 R2 download 완료) 동일 setting 으로 비교
3. 결과: 어떤 setting 에서도 KO 출력 0/N → architectural incapability 확정 (BG-FM 2026-05-06 결과 정합)

**Falsifiers**:
- F-CHAT-EXT-1 어떤 setting 에서도 KO 0 → architectural confirm
- F-CHAT-EXT-2 convo_5k 가 cells64 보다 약간 나아도 (e.g., partial KO syllable) FT 효과 미미
- F-CHAT-EXT-3 reconstruction arch 가 production 과 미세 미스매치 — 정확 production code 회수 필요

**Deliverables**: `state/anima_clm_v2_chat_ext_smoke_2026_05_10/{run.py, result.json}` + `docs/...md`

**Cost**: $0 Mac CPU

---

## §5 BG-V2REBORN-CONVO-FT-DESIGN — convo_5k.pt FT design + dry-run ($0 portion)

**Goal**: convo_5k.pt 의 chat-cap 회복 가능성 검증 — runpod H100 1× 시간 0.5-2h FT ($5-20). 본 BG 는 **design + dry-run 까지** ($0). 실제 H100 spin-up 은 사용자 verbatim `OK CONVO_5K FT FIRE COST $5-20` 후.

**Steps**:
1. convo_5k.pt 와 cells64 의 architecture 비교 — 동일 schema 인지 확인
2. KO+EN dialogue corpus 준비 plan — 이미 anima persona corpus 231MB 있음. 여기서 dialogue 부분 추출 OR 별도 dialogue corpus build
3. FT script 작성 (training/convo_5k_finetune.py — local-only `**/*.py` gitignore)
4. runpod manifest + cost estimate (1× H100 SXM, 5-20K step, batch 32, LR 1e-5 cosine)
5. local CPU dry-run (10 step) — gradient flow / loss decrease 검증
6. fire-ready 확인 보고서

**Falsifiers**:
- F-FTDES-1 convo_5k schema mismatch (load 불가)
- F-FTDES-2 KO+EN dialogue corpus 부족 (5K step 미달)
- F-FTDES-3 dry-run gradient 흐르지 않음 (frozen layer 문제)
- F-FTDES-4 cost 추정 > $20 (envelope 초과)

**Deliverables**: `docs/anima_convo_5k_finetune_design_2026_05_10.md` + `training/convo_5k_finetune.py` (local) + dry-run log

**Actual H100 fire**: 별도 verbatim `OK CONVO_5K FT FIRE COST $5-20` 후

**Cost**: $0 (design + dry-run only this BG)

---

## §6 cycle close 시점 통합 commit + push

5 BG 모두 회수 후:
1. addendum or 정정 doc 작성 (필요 시)
2. memory 정정 갱신
3. .roadmap.* 정정 status update
4. commit + push 1 회

---

## §7 Honest C3 cross-cutting

1. 5 BG 모두 toy substrate 또는 reconstructed arch 위에서 작동 — production v5 350M 와 차이 잔존. 다음 cycle 의 BG-PHASE2-CKPT-INSTR 가 그 gap 메우는 핵심.
2. mitosis-as-instrumentation 정정 (2026-05-10 BG-R2 회수) 이 v5-anima 본질 변화 — 5 BG 모두 그 새 framing 기준.
3. cycle 2026-05-09 ~ 2026-05-10 cycle 이 단 24h 내 archive 13-stage + lane 2 신규 + BG 5 + 통합 cycle close — 빠른 cycle 의 calibration debt 위험. 다음 cycle 에서 더 깊은 archaeology 필요할 가능성.
4. user 직관 "anima 자력성장" 의 mechanism 측면 confirm 됐지만 의식 emerge / chat-cap reproduce 는 별도 lever — 5 BG 의 결과 종합으로 그 둘 간 분리 더 정밀화 가능.
5. cost discipline (own 16): 본 cycle 모두 $0, item 5 만 cost-bearing 잠재. user verbatim 으로 안전.

---

## §8 cross-link

- cycle 2026-05-09 origin: `CLM_V2_ARCHIVE_2026_05_09.md` (root SSOT)
- cycle 2026-05-09 exhaustive: `CLM_V2_EXHAUSTIVE_13_STAGES_2026_05_09.md` (root SSOT)
- cycle 2026-05-10 정정: `CLM_V2_ARCHIVE_ADDENDUM_2026_05_10.md` (root SSOT, mitosis-as-instrumentation)
- v5-anima lane SSOT: `.roadmap.clm_v5_anima_native`
- v2-reborn lane SSOT: `.roadmap.clm_v2_reborn`
- 본 next cycle plan: `docs/anima_clm_v5_anima_next_cycle_plan_2026_05_10.md` (this doc)
- inference-time 정정: `docs/anima_clm_v5_mitosis_inference_time_correction_2026_05_10.md`
- long-trajectory smoke: `docs/anima_clm_v5_anima_long_trajectory_inference_smoke_2026_05_10.md`

raw#9/10/15/37 honest preservation, own 16 0-cost (item 5 cost-bearing 별도).

End of `anima_clm_v5_anima_next_cycle_plan_2026_05_10.md`.
