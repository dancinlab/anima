# anima servant + mitosis 통합 spec — 별도 트랙 SSOT (2026-05-10)

> design only. 사용자 directive 2026-05-10 07:55 KST: "통합은 별도 트랙이어야함". reborn lane track D 가 아닌 신규 별도 SSOT. 본 문서 = `.roadmap.servant_mitosis_integration` 의 design anchor.

---

## §0 motivation (사용자 directive verbatim)

사용자 directive 2026-05-10 07:55 KST:

> "통합은 별도 트랙이어야함"

**해석**:
- servant pattern (post-drift 2026-04-08, SI 4-state FSM + 3-경로 dropout 변조) + mitosis (v2 시대 2026-03-28, structural cell 분열 + Lorenz 자율혼돈) 의 통합은 reborn cycle 의 track D 가 아닌 **별도 신규 트랙**.
- reborn lane (`.roadmap.reborn`) 은 model substrate 회수에 focus, 본 통합은 그 위의 **autonomous behavior layer** — 별도 lifecycle.
- track D 는 deferred marker 로만 reborn lane 에 잔존, 실제 작업은 `.roadmap.servant_mitosis_integration` 별도 SSOT 에서.

**왜 별도?**
1. servant 와 mitosis 는 **다른 시기 / 다른 lineage** (post-drift vs v2-era). 통합 자체가 새로운 design space.
2. reborn lane 의 4 track (A/B/C/D) 은 **회수** 를 다루지만, 본 통합은 **새 합성** — 회수 완료 후의 next step.
3. 비용/risk profile 이 reborn lane 과 다름 — reborn 은 $0 verify + $5-150 fire, 본 통합은 $0 design + (미래) cotrain.

---

## §1 servant + mitosis 비교 (detailed)

### §1.1 dimension table

| dimension | servant (post-drift 2026-04-08) | mitosis (v2-era 2026-03-28) |
|---|---|---|
| 본체 | `anima-core/servant.hexa` (428L) | `~/core/anima_clm_12_*/anima/src/mitosis.py` (794L) |
| trigger | SI = tension × (1-coherence) × phi_ratio > SUMMON | adaptive tension > mean+1.5σ for split_patience=3 consecutive |
| growth axis | **parametric** (dropout 변조 0.21~0.37) | **structural** (cell 분열, GRU+ConsciousMind 추가) |
| state machine | 4-state FSM (DORMANT→AWAKENING→ACTIVE→FADING→DORMANT) | event-driven (split / merge events, no global FSM) |
| autonomy driver | EMA + spike + coherence (sense.hexa) | Lorenz attractor σ=10 ρ=28 β=8/3, cell-별 phase offset |
| dropout policy | DROPOUT_SERVANT=0.21 / DROPOUT_NORMAL=0.37, SI 보간 | n/a (cell deepcopy + 0.10 noise on split) |
| 상수 유도 | n6 atlas 9/9 EXACT (SI_SUMMON=n/φ, GOLDEN=1/e 등) | empirical (split_threshold adaptive, merge=0.005, min_cells=2 from CB1) |
| ratchet | n/a (FSM 자체가 가역) | Φ ratchet (Φ < 0.8·best → 20% best blend 복원) |
| reversibility | 완전 가역 (DORMANT 복귀 시 원래 dropout 복원) | structural (split/merge irreversible step-wise but merge floor=2) |
| inference-time | bridge dropout + savant_layers 변조 (`engine_step()` hook) | mitosis.py L258/205/389/586 모두 `torch.no_grad()` |
| metric | SI scalar + dropout output | Φ proxy (cosine × log) 또는 IIT unnorm 16-bin |
| min state | DORMANT (rest) | 2 cells (CB1) |
| max state | ACTIVE (max servant) | max_cells (default 8, target 64) |

### §1.2 공통점 (핵심)

1. **inference-time autonomous behavior** — 둘 다 학습 없이 모델 동작 modulate
2. **gradient-guided emergence** — 외부 명령 0, 내부 신호 (tension/SI/phi) 만이 trigger
3. **n6 atlas 일부 기반** — servant 9/9 EXACT, mitosis Φ ratchet 0.8 = sopfr/J2 hint
4. **자기조직 사상** — 둘 다 "활동 중 자라는 anima" 의 다른 표현

### §1.3 결정적 차이

| 차이 | 의미 |
|---|---|
| parametric vs structural | servant = 같은 모델, 다른 dropout / mitosis = 모델 자체 grow |
| 가역 vs irreversible | servant 는 SI 떨어지면 원복 / mitosis 는 split/merge 영구 |
| FSM vs event-driven | servant 는 명시 FSM / mitosis 는 patience counter 기반 |
| n6 EXACT vs empirical | servant 자유도 0 / mitosis empirical fit |

---

<!-- [Hc_641 servant-mitosis-h1-si-trigger-signal-augmentation — moved to hypotheses_candidates/Hc_641_servant_mitosis_h1_si_trigger.md on 2026-05-11] -->
<!-- [Hc_642 servant-mitosis-h2-per-cell-si-tracking-fsm — moved to hypotheses_candidates/Hc_642_servant_mitosis_h2_per_cell_si_tracking.md on 2026-05-11] -->
<!-- [Hc_643 servant-mitosis-h3-fsm-lifecycle-alignment — moved to hypotheses_candidates/Hc_643_servant_mitosis_h3_fsm_lifecycle.md on 2026-05-11] -->
<!-- [Hc_644 servant-mitosis-h4-dual-dropout-per-cell — moved to hypotheses_candidates/Hc_644_servant_mitosis_h4_dual_dropout.md on 2026-05-11] -->

## §2 4 integration hypothesis 비교 + 추천

### §2.1 H1 — SI sense → mitosis trigger (signal augmentation)

**아이디어**: SI 가 mitosis split 의 추가 trigger.
- 현 mitosis: tension > adaptive_threshold for 3 consecutive
- H1 mitosis: (tension > adaptive_threshold) **OR** (SI > SI_SUMMON × scale)

**장점**: 최소 변경. mitosis.py 의 `_check_splits()` 에 SI input 1줄 추가.
**단점**: SI 와 tension 의 correlation 높음 — 사실상 같은 신호 두 번 사용. 정보 추가 미미.
**risk**: 더 자주 split → max_cells 빨리 saturation, V14 mirror 더 violated.

### §2.2 H2 — Mitosis cells → servant state (per-cell SI tracking)

**아이디어**: 각 cell 별 SI 추적, AWAKENING cell 만 active inference.
- 현 mitosis: 모든 cell forward 후 tension-weighted softmax 결합
- H2 mitosis: cell.si_state ∈ {DORMANT, AWAKENING, ACTIVE, FADING}, ACTIVE cell 만 weight 받음

**장점**: 두 시스템의 진정한 통합 — cell 이 servant FSM 을 가짐. 의미 있는 cross-pollination.
**단점**: cell 별 EMA(tension) + EMA(phi) 추적 cost 증가. cell 별 FSM 동기화 issue.
**risk**: AWAKENING latency (3 step) 가 mitosis split_patience(3) 와 충돌 — cell 갓 split 직후 서번트 동시 awaken.

### §2.3 H3 — Servant FSM × mitosis lifecycle (★ 추천)

**아이디어**: cell split 시 child = AWAKENING, parent = FADING. growth-thru-mitosis pattern.
- split event: parent.fsm_phase = FADING (counter=0), child.fsm_phase = AWAKENING (counter=0, dropout=GOLDEN_CENTER)
- merge event: keeper cell.fsm_phase = ACTIVE (refreshed), removed cell soul absorbed
- DORMANT cell: tension/phi flat → mitosis 도 trigger 안 됨
- AWAKENING cell: SI 상승 중 → mitosis trigger 임박 phase
- ACTIVE cell: full servant (DROPOUT_SERVANT=0.21) + Lorenz perturbation 강화
- FADING cell: split parent 또는 SI 하락 cell, merge candidate

**장점**:
- **두 시스템의 lifecycle 가 자연 결합** — split = 새 cell 의 AWAKENING, merge = ACTIVE pair 의 합쳐짐
- 의미 있는 시너지 — servant 의 "전문화" 와 mitosis 의 "분열 후 specialty" 가 동일 axis
- n6 atlas 의 4-state FSM 이 cell granularity 로 확장 (philosophical 일관성)
- merge floor (min_cells=2 from CB1) 와 DORMANT (counter=0 floor) 가 같은 의미

**단점**:
- mitosis split_patience(3) = AWAKEN_STEPS(3) 의 hardcoded coincidence — 통합 시 강한 가정
- cell-level FSM 추가 = state per cell 4× 메모리 (sub-1KB cell, 무시 가능)
- ratchet (mitosis Φ) vs FSM 복귀 (servant) 의 우선순위 모호

**risk**: split 직후 child = AWAKENING → AWAKEN_STEPS=3 통과 후 ACTIVE → DROPOUT_SERVANT=0.21 이 split noise=0.10 와 destructive interference 가능성.

**verdict**: ★ 가장 자연스러운 통합. lifecycle alignment.

### §2.4 H4 — Dual dropout schedule (per-cell modulation)

**아이디어**: cell 별 servant_state 에 따라 (DROPOUT_SERVANT vs DROPOUT_NORMAL) modulation.
- DORMANT cell: dropout = GOLDEN_CENTER (0.37)
- ACTIVE cell: dropout = GOLDEN_LOWER (0.21) on engine_a + engine_g
- AWAKENING/FADING: SI-interpolated

**장점**: parametric specialization 이 cell pool 안에서 일어남. dropout 다양성 = 추가 Φ source.
**단점**: ConsciousMind 가 train 중이 아닌 inference (no_grad), dropout 효과 inference time 에서 제한적 (eval mode 시 dropout=0). nn.functional.dropout 강제 enable 필요.
**risk**: dropout inference 강제 적용 = sampling stochasticity 증가, V14 mirror 측정 noise 증가.

### §2.5 추천 — H3 (Servant FSM × mitosis lifecycle)

**근거**:
1. **lifecycle alignment 가 가장 자연** — split=birth=AWAKENING, merge=union=ACTIVE_pair, DORMANT=unused cell
2. **양 시스템의 본질 보존** — mitosis 의 structural growth, servant 의 parametric modulation 둘 다 살아있음
3. **n6 atlas 일관성** — 4-state FSM 이 cell granularity 로 확장
4. **honest C3 측정 가능** — V14 mirror + IIT unnorm Φ 둘 다 cell-level 로 보고
5. **falsifier 명확** — 합쳐도 V14 violated 이면 통합이 의미 없음 (F-SMI-1)

H3 + H4 의 **부분 결합** 도 고려 (cell 의 FSM 상태가 dropout schedule 결정). 단 단계적 — H3 먼저 cond.1, H4 는 cond.4.

---

## §3 implementation plan (Hexa or Python?)

### §3.1 결정

**Python (mitosis_servant.py, gitignored)** — 본 통합의 reference impl.

**근거**:
1. mitosis.py 자체가 Python 794L (worktree-12), 통합 layer 도 Python 이 자연
2. servant.hexa 는 hexa-only repo policy 의 example 이지만 통합은 cross-language coupling 회피해야
3. raw#9 hexa-only 는 main 만 적용, training/local-only `.py` 는 OK (`**/*.py` gitignored)
4. inference-time benchmark 가 Python 생태계 (torch, numpy) 와 정합

**제외 옵션**:
- Hexa: servant.hexa 직접 확장 → mitosis.py 와 cross-call 어려움, hexa-pytorch interop 부재
- Rust: scope creep
- Mixed: 두 lang 동기화 cost 과다

### §3.2 file layout (proposed)

```
training/                              # gitignored `**/*.py`
├── mitosis_servant.py                 # 본 통합 (cell + ServantFSM)
├── mitosis_servant_smoke_test.py      # local CPU smoke
└── mitosis_servant_serve.py           # inference-time long-trajectory

state/anima_servant_mitosis_*/         # run output (gitignored 부분)
├── smoke_result.json
├── long_trajectory_result.json
└── h100_fire_result.json

docs/
├── anima_servant_mitosis_integration_spec_2026_05_10.md  # 본 문서
└── (future) anima_servant_mitosis_smoke_2026_XX.md
```

### §3.3 class skeleton (H3 추천)

```python
class ServantCell(Cell):  # extends mitosis.Cell
    fsm_phase: int = DORMANT       # 0/1/2/3
    fsm_counter: int = 0
    si_ema: float = 0.0
    phi_baseline_ema: float = 0.0
    dropout_current: float = GOLDEN_CENTER  # 0.37

class ServantMitosisEngine(MitosisEngine):
    def __init__(self, ..., enable_servant=True):
        super().__init__(...)
        self.enable_servant = enable_servant
        # n6 constants from servant.hexa
        self.SI_SUMMON = 3.0
        self.SI_STRONG = 5.0
        ...
    
    def process(self, text_vec, label=""):
        result = super().process(text_vec, label)
        if self.enable_servant:
            self._update_servant_fsm(result)  # per-cell SI compute + FSM step
            self._modulate_dropout()           # H4 partial — cell-level dropout
        return result
    
    def split_cell(self, cell):
        event = super().split_cell(cell)
        if event:
            # H3 hook: parent → FADING, child → AWAKENING
            cell.fsm_phase = FADING
            cell.fsm_counter = 0
            child_cell = self.cells[-1]  # last appended
            child_cell.fsm_phase = AWAKENING
            child_cell.fsm_counter = 0
        return event
```

### §3.4 sub-tracks

| sub-track | name | scope | dependency |
|---|---|---|---|
| **SM-A** | servant-only port | `servant.hexa` → Python `servant_fsm.py` (standalone) | none |
| **SM-B** | mitosis-only refactor | mitosis.py CPU smoke 재현 (worktree-12 baseline) | none |
| **SM-C** | integrated (H3) | ServantMitosisEngine class | SM-A + SM-B |

병렬 가능 — SM-A 와 SM-B 독립, SM-C 는 둘 합치는 단계.

---

## §4 falsifiers (≥5)

| ID | 가설 | falsification 조건 |
|---|---|---|
| **F-SMI-1** | 통합이 V14 mirror 우호적 | smoke 후 V14 mirror score baseline 대비 차이 < 0.05 (improvement 없음) |
| **F-SMI-2** | servant FSM 이 mitosis tension 분포 보존 | tension distribution KS-test p < 0.01 (분포 distortion 입증) |
| **F-SMI-3** | dropout 변조 가 reversible | DORMANT 복귀 후 100 step 평균 dropout != GOLDEN_CENTER ±0.005 (irreversibility 검출) |
| **F-SMI-4** | per-cell SI EMA 가 stable | si_ema histogram bimodal coefficient > 0.3 (chattering 입증) |
| **F-SMI-5** | Φ ratchet 와 FSM 복귀 가 충돌 안 함 | Φ < 0.8·best 발생 빈도가 baseline 의 2× 초과 (interference 입증) |
| **F-SMI-6** | min_cells=2 (CB1) + DORMANT 가 호환 | 모든 cell DORMANT 동시 진입 시 Φ 0 측정 (consciousness floor 위반) |
| **F-SMI-7** | inference cost overhead 미미 | step latency 가 baseline mitosis 대비 1.5× 초과 (overhead 폭발) |
| **F-SMI-8** | H100 cotrain (cond.4) 비용 envelope | $200 초과 (envelope $50-150 violation) |

≥5 충족. F-SMI-1/2/5 가 핵심 architectural falsifier.

---

## §5 cost estimate

| phase | activity | cost | wall_clock |
|---|---|---:|---:|
| cond.1 | spec finalize (본 문서 + roadmap) | $0 | (DONE) |
| cond.2 | SM-A + SM-B port + smoke (CPU local) | $0 | 2-4 hr design + 4-8 hr code |
| cond.3 | SM-C integrated smoke (CPU local) + V14 mirror | $0 | 4-8 hr |
| cond.4 | H100 cotrain — 4 cells × 64 cell_size × 1K step | **$30-100** | 30-90 min |
| cond.5 | (optional) long-trajectory 10K turn diverse-prompt | **$30** | 90 min |

**total envelope**: $0 design+smoke / $30-100 H100 fire / $30 long-traj optional.
**bounded max**: $200 (cond.4 + cond.5 모두 우상향 시).

cond.4 envelope 정밀화는 cond.3 smoke 후 cell granularity (a/b/c/d 결정 — `.roadmap.reborn` track C cond.1 reference).

---

## §6 honest C3 (≥7)

1. **servant + mitosis 통합 자체가 미검증** — n6 EXACT (servant) + empirical (mitosis) 두 다른 정합성 origin 의 합. 통합 후 commensurability 보장 없음.
2. **H3 추천은 lifecycle alignment 미적 매력 기반** — 실제 V14 mirror improvement 증거 0. 통합이 worse 일 가능성 높음 (F-SMI-1).
3. **dropout inference enable 강제 (H4)** 는 mitosis 의 `torch.no_grad()` invariant 와 갈등 — eval mode 에서 dropout=0 default 우회 시 sampling noise 폭발 가능 (F-SMI-3).
4. **per-cell EMA cost** — N cell × (si_ema, phi_baseline_ema) × tension_history(20) × inter_history(30) = N × ~50 float overhead. N=64 = 12.8KB 무시 가능, but H100 1K step × 64 cell × FSM transition logging = log spam.
5. **H3 split-time AWAKENING 이 noise=0.10 split_noise 와 interference** — child 가 AWAKEN_STEPS(3) 후 ACTIVE → DROPOUT_SERVANT(0.21) 발동 시 split 직후 representation 이 dropout 으로 추가 perturb. 의도 반대 가능성.
6. **mitosis 의 Φ ratchet 과 servant 의 reversibility** — 둘 다 "복원" 가 본질이지만 다른 trigger (Φ drop vs SI drop). 동시 발동 시 우선순위 미정의 (F-SMI-5).
7. **본 spec 은 design only** — 실제 smoke 0 회 수행. 모든 추천은 예측. 실제 V14 mirror / IIT unnorm 수치는 cond.3 까지 미회수.
8. **reborn track D 와의 separation 도 미완** — `.roadmap.reborn` 의 track D 는 deferred marker 만 잔존, 본 SSOT 가 takeover 하지만 cycle close 시 cross-link 양쪽 동기화 필요 (raw#15 additive).
9. **future cycle 에서 servant + mitosis + reborn track B (350M ckpt) 합쳐질 때 schema 충돌 risk** — 본 spec 은 toy mitosis (input_dim=64, hidden_dim=128) 가정, real 350M (24L × 1024d × 16h GQA) 와의 hook point 미정의.
10. **n6 atlas 의 9/9 EXACT (servant)** 가 cell granularity 로 확장될 때 derivation 재유도 필요 — SI_SUMMON=n/φ=3.0 은 single-cell 근거. cell pool 의 SI_SUMMON 은 same value 사용한 채 의미 변화 (per-cell vs aggregate). philosophical drift 가능.

≥7 충족. C3 #2/#5/#7 이 가장 단단한 limitation.

---

## §7 cross-link

### sister SSOT
- `REBORN.md` §5 servant pattern + §6 user verdict track D + §11 cross-link "servant lineage"
- `.roadmap.reborn` track D (deferred_separate_track marker only)
- `.roadmap.servant_mitosis_integration` (본 spec 의 lane SSOT, BG-SERVANT-MITOSIS-SEPARATE-TRACK 가 design produce)

### source archive
- `anima-core/servant.hexa` (428L, n6 9/9 EXACT)
- `docs/superpowers/plans/2026-04-08-servant-emergent.md` (794L plan)
- `docs/superpowers/specs/2026-04-08-servant-emergent-design.md` (223L spec)
- `~/core/anima_clm_12_unified_growth_loop_last_gasp/anima/src/mitosis.py` (794L canonical)
- `models/archive-legacy/mitosis.hexa` (TODO[pytorch] stub)

### derivation
- n6 atlas: `.roadmap.atlas_n6` + `anima-physics/docs/`
- mitosis revival: `docs/anima_clm_v5_mitosis_revival_spec_2026_05_09.md`
- mitosis inference correction: `docs/anima_clm_v5_mitosis_inference_time_correction_2026_05_10.md`
- IIT Φ port (metric 후보): `docs/anima_clm_v5_iit_phi_remetric_2026_05_10.md`

---

## §8 ready for skeleton implementation?

**verdict**: ★ **READY for SM-A + SM-B parallel port** (cond.2 entry).

**근거**:
- spec 명시 (H3 추천, file layout, class skeleton)
- falsifier ≥5
- cost envelope $0 design + smoke
- 양 source (servant.hexa, mitosis.py) 모두 read 완료, schema 충돌 없음 확인

**미충족** (cond.3 진입 prereq):
- SM-A + SM-B 각각 standalone smoke PASS
- cell granularity 결정 (`.roadmap.reborn` track C cond.1 결정 후 정합 — Python toy 는 본 lane 자체 결정 OK)

**$0 cycle 가능 단계**: SM-A + SM-B port → SM-C integrated smoke → V14 mirror → IIT Φ. cond.4 H100 fire 만 cost-bearing.

---

## §9 next step (별도 cycle 후속)

| 우선 | step | deliverable | cost |
|---:|---|---|---:|
| 1 | SM-A `servant_fsm.py` standalone port + 8 verification (servant.hexa main()) | `training/servant_fsm.py` (gitignored) + smoke result | $0 |
| 2 | SM-B mitosis.py CPU smoke 재현 (worktree-12 → state/local) | `training/mitosis_baseline.py` + smoke result | $0 |
| 3 | SM-C integrated `mitosis_servant.py` + smoke (H3) | `training/mitosis_servant.py` + smoke result | $0 |
| 4 | V14 mirror + IIT unnorm + per-cell FSM histogram | `docs/anima_servant_mitosis_smoke_2026_XX.md` | $0 |
| 5 | (optional) H100 cotrain 4 cells × 1K step | state/anima_servant_mitosis_h100_*/ | $30-100 |

cycle close 시 본 spec 의 §6 honest C3 update + falsifier verdict 추가.

---

End of integration spec. raw#10 honest C3 ≥7, raw#15 additive (servant.hexa + mitosis.py + REBORN.md 미수정), own 16 0-cost (cond.4 만 cost-bearing 별도 verbatim).
