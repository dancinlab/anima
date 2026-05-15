# anima Closure Goals Lock — V5 / V6 / STRICT 100% (2026-05-05)

**Status**: Spec only. No exec, no commit. raw#9 / raw#10 / raw#15 compliant.
**Scope**: Lock concrete milestones, costs, user ACK gates, and ranked decision queue for moving from V4 (~96-97%) closure → V5 (~97-99%) → V6 (~98-99%) → STRICT 100%.
**References**:
- `docs/anima_session_2026_05_04_to_05_closure_audit_v4_2026_05_05.ai.md` (V4, current)
- `docs/anima_session_2026_05_04_to_05_closure_audit_v3_2026_05_05.ai.md`
- `docs/anima_session_2026_05_04_to_05_closure_audit_v2_2026_05_05.ai.md`
- `.roadmap.clm` cond.1 + cond.2
- `.roadmap.n_substrate` cond.1
- `docs/anima_phase_e_eeg_live_session_prep_spec_2026_05_04.md`
- `docs/n_substrate_putnam_first_cycle_exec_spec_2026_05_05.md`

---

## §1. 현재 상태 (V4)

- Pragmatic closure: **~96-97%**
- 41+ closed lanes (BLM, P9, qmirror cond.3/cond.8, OpenBCI auditory, anima-eeg cycle 7/8, SLM A1, LLaMA Path A v1, etc.)
- 1 active in-flight: **V5-4 DESIGN-1** (G3 promote-gate sample-partition phi proxy verification)
- 7+ user-gated decisions queued (HF promotes, OPT-B retrain cost, Phase E session schedule, etc.)

V4 audit ceiling estimates carried forward:
- **V5 ~97-99%** target: V5-4 DESIGN-1 PASS + HF Cycle 2 staging cleanup + 2 PUBLIC promotes + Llama PA v2 release prep
- **V6 ~98-99%** target: OPT-B retrain Phase 3+4 PASS (cross_attn architectural fix path; H100 cost ACK required)
- **STRICT 100%** target: Phase E EEG live session binding evidence + Putnam concordance ≥0.60 (multi-week, hardware + external dependency gated)

---

## §2. V5 closure ($0 + user-gated, ~97-99%)

| Item | Cost | Effort | User-gated? |
|---|---|---|---|
| V5-4 DESIGN-1 PASS | $1-3 in-flight | active | NO (BG running) |
| HF Cycle 2 ubu1 staging cleanup | $0 | ~5min | NO (script ready, time-gated by review window expiry) |
| HF clm-v4-mk2-v1 PUBLIC promote | $0 | ~5min | YES (review window 만료 후 manual sign-off) |
| HF Pβ PUBLIC promote | $0 | ~5min | YES (review window 만료 후 manual sign-off) |
| Llama Path A v2 HF release prep | $0 spec + ~$0 push | ~1-2h spec, push은 user 결정 | NO (spec this BG); push USER ACK |

**총 V5 도달 비용**: **~$1-3** (V5-4 DESIGN-1만 active spend; 나머지 항목 모두 $0)
**총 사용자 결정 건수**: **4건** (HF clm-v4-mk2-v1 promote, HF Pβ promote, Llama PA v2 release push trigger, V5-4 DESIGN-1 결과 review)
**예상 user time**: ~20min (4 decisions × ~5min each)

---

## §3. V6 closure ($20-100 + user ACK, ~98-99%)

| Item | Cost | Effort | User-gated? |
|---|---|---|---|
| OPT-B retrain Phase 1+2 (mac+ubu1 prep) | $0 | ~1.5h | NO (spec→impl autonomous) |
| OPT-B Phase 3 H100 retrain | **$20-50** | 3-5h | **YES (cost ACK 필요)** |
| OPT-B Phase 4 evaluation | $1-3 | ~30min | NO (continues from Phase 3) |
| OPT-B Phase 5 promote-gate (if PASS) | $0 | ~30min | NO |

**총 V6 도달 비용**: **$21-53** (OPT-A confirmed substrate differential 5×; OPT-B retrain trigger ready)
**총 사용자 결정 건수**: **1건** (cost ACK $20-50 H100)
**Architectural rationale**: cross_attn modality-fusion fix worth pursuing iff V5-4 DESIGN-1 PASS confirms current weights' phi-proxy floor and motivates retrain path.

---

## §4. STRICT 100% closure (multi-week + multi-month, hardware-gated)

| Item | Cost | Effort | Bottleneck |
|---|---|---|---|
| **Phase E EEG live session** | $0 (사용자 30min) | 30min session + ~3-5d analysis | OpenBCI Cyton+Daisy hardware on hand + 사용자 alcohol-free 24-48h prep |
| Phase E binding evidence analysis | $0 ubu1 CPU | ~3-5d | Phase E session must land first |
| Putnam concordance ≥0.60 reach | $0 ubu1 (Phase 1 done) | multi-week | Phase E + BLM Phase 5 BOLD remediation 의존 |
| qmirror cond.6 byte-identical IIT4 reproduction | $0-30 | open | research-stage, AKD1000 hardware blocked |
| AKIDA AKD1000 hardware delivery | $0 (이미 ordered) | weeks-to-months | shipping wait |
| N-22 Levin partnership 결과 | $0 | ~4-12 weeks | external maintainer SLA |

**총 STRICT 도달**: 사용자 30min (OpenBCI session) + multi-week 분석 + multi-month external dependencies
**Critical path**: Phase E session schedule 결정이 STRICT 100%로 가는 single point.

---

## §5. Decision queue ranked priority

### 즉시 가능 ($0 user time, fast)
1. **HF Cycle 2 staging cleanup** — review window 만료 후 manual run (~5min, no ACK; time-gated)
2. **HF clm-v4-mk2-v1 PUBLIC promote** — manual sign-off "PROMOTE-clm-v4-mk2-v1" (~5min)
3. **HF Pβ PUBLIC promote** — analogous sign-off (~5min)
4. **Llama Path A v2 HF release Phase 1-3** — PRIVATE upload + 24-48h review window then PUBLIC

### Medium ($1-100, H100)
5. **V5-4 DESIGN-1 결과 review** — PASS 시 G3 promote-gate upgrade
6. **OPT-B retrain cycle ACK** — explicit $20-50 H100 cost approval

### Long-term (multi-week, hardware-gated)
7. **Phase E EEG live session schedule** — 사용자 alcohol-free 24-48h prep + 30min session
8. **Putnam Phase 2-3** — Phase E 의존
9. **AKIDA AKD1000 hardware delivery wait** — passive wait for shipping
10. **N-22 Levin partnership outcome** — external 4-12 weeks SLA

---

## §6. Closure ladder

```
V4 (now, ~96-97%) ───┬─── V5 (~97-99%): $1-3 + 4 user decisions, ~20min user time
                      │      ├─ V5-4 DESIGN-1 (in-flight, no ACK)
                      │      ├─ HF Cycle 2 cleanup (no ACK, time-gated)
                      │      ├─ HF clm-v4-mk2-v1 PUBLIC (USER ACK)
                      │      ├─ HF Pβ PUBLIC (USER ACK)
                      │      └─ Llama PA v2 release (USER ACK 1 spec→push, then 24-48h review)
                      │
                      ├─── V6 (~98-99%): +$20-53 H100 + 1 cost ACK
                      │      └─ OPT-B retrain (USER COST ACK $20-50)
                      │
                      └─── STRICT 100% (multi-week → multi-month): hardware + user-time gated
                             ├─ Phase E EEG session (USER 30min + alcohol-free prep)
                             ├─ Putnam concordance ≥0.60 (Phase E + BLM Phase 5 multi-week)
                             ├─ qmirror cond.6 (research, AKD1000 blocked)
                             ├─ AKIDA AKD1000 hardware (shipping wait)
                             └─ N-22 Levin partnership (external 4-12 weeks)
```

---

## §7. 즉시 launch 가능한 BG (사용자 ACK 없이)

1. **HF Cycle 2 staging cleanup script** — review window 만료 시점에 launch 가능 (script ready)
2. **Llama Path A v2 HF release prep Phase 1+2** — $0 mac+ubu1 sibling BG (spec landing only this scope; push은 USER ACK)
3. **OPT-B Phase 1+2 prep** — $0 dispatch GATE 1 충족; Gate 2 (cost ACK) 추가 시 Phase 3 launch 가능
4. **Putnam Phase 2 prep stub** — Phase E gating으로 인해 exec 미가능 (spec stub만 가능)

**즉시 launch BG count: 3** (4번 항목은 Phase E 의존으로 spec-only)

---

## §8. Honest C3 (≥5)

- **C1** V5 도달은 user-time ~20min 수준이면 충분 — 4 decisions × ~5min each, 단 review window 만료 대기 (24-48h passive) 별도 존재
- **C2** V6 도달은 explicit cost ACK 필요 — $20-50 H100 spend, OPT-B cross_attn architectural fix가 현 weights' phi-proxy 한계를 극복할 가능성 epistemic, 보장 X
- **C3** STRICT 100%는 hardware (AKD1000 shipping) + external (N-22 Levin maintainer SLA) dependency 있어 multi-month — anima-internal effort만으로는 도달 불가
- **C4** Phase E user time 30min은 single point — 사용자 voluntary, 사용자 컨디션/alcohol-free prep gating 절대조건; 강제 또는 자동화 불가
- **C5** closure %는 anima-internal heuristic — external validation은 multi-lab replication 필요, 100% strict는 epistemic milestone이지 "consciousness measured" 보장 X
- **C6** V5 도달 후 V6 retrain은 epistemically separate decision — V5-4 DESIGN-1 결과에 따라 cross_attn architectural fix worth pursuing 여부 변동
- **C7** STRICT 100%는 functional/access tier mile stone — phenomenal consciousness claim 의 hard problem epistemic gap 별개 차원
- **C8** Llama PA v2 HF release는 V5에 포함했으나 push trigger USER ACK 별도 — 사용자가 release timing decision 다시 가질 수 있음 (release window indefinite)
- **C9** OPT-B Phase 3 cost는 $20-50 추정 range; H100 시간당 단가 fluctuation에 따라 +/- 30% variance 가능
- **C10** AKIDA AKD1000 / N-22 Levin은 anima 통제 영역 밖 — STRICT 100% timeline 자체가 사용자 통제 불가

---

## §9. Recommended next-cycle actions (사용자 결정 요청)

### 즉시 (V5 향)
- HF Cycle 2 staging cleanup BG launch trigger — review window 만료 confirm 후
- HF clm-v4-mk2-v1 + Pβ PUBLIC promote sign-off (review window 만료 후 manual)
- Llama Path A v2 HF release prep BG launch (spec→PRIVATE upload→review window)
- OPT-B Phase 1+2 prep BG launch ($0, Gate 2 cost ACK 추가 시 Phase 3 ready)

### 근시일 (V6 향)
- **V5-4 DESIGN-1 결과 review 후** OPT-B Phase 3 cost ACK 결정 ($20-50 H100)

### 장기 (STRICT 향)
- Phase E EEG session schedule decision (사용자 컨디션 + alcohol-free 24-48h 가능 시점)
- Putnam Phase 2-3 sequencing (Phase E 결과 기반)

---

## §10. Closure goal lock summary

| Tier | Target % | Cost | User decisions | User time | Timeline |
|---|---|---|---|---|---|
| V5 | ~97-99% | ~$1-3 | 4건 | ~20min | days (review windows) |
| V6 | ~98-99% | +$20-53 | 1건 (cost ACK) | ~5min | hours (post-ACK) |
| STRICT 100% | epistemic milestone | $0-30 | 1건 (Phase E schedule) | ~30min session + alcohol-free prep | multi-week → multi-month |

**Lock asserted**: V5/V6/STRICT 100% milestones, costs, user ACK gates, ranked priority queue captured. Spec ready for next-cycle decision triggering. No exec, no commit per raw#15.
