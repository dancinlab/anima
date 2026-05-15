# HEXAD/PLAN.md — C/D full hexa-native port roadmap

> User directive 2026-05-16: `"a => HEXAD/PLAN.md 에 계획 기록"`
> (a 항목 = C/D 모듈 full hexa-native port — 즉시 실행 X, **계획 기록만**.)
> Scope ⊃ HEXAD/ 트리에서 현재 scaffold 인 C, D 두 모듈을 완전한 hexa-native
> 구현으로 끌어올리는 단계적 로드맵. 실 진행은 별도 cycle 의 사용자 게이트.

## 0. 현재 상태 (PR #78 기준 LANDED)

| 모듈 | 현재 상태 | 다음 목표 |
|---|---|---|
| **S/M/W/E/BRIDGE** | ✅ working hexa selftest (B-X 🔵 closed-form witness) | 통합 wire (task b) 후 단일 process 통합 forward 산입 |
| **C** | 🔶 scaffold + cross-link to `tool/hexa_native/mitosis_hook.hexa` (1119 LoC FULL IMPL D4a) | full hexa-native ConsciousnessC equivalent — Phase 2-4 |
| **D** | 🔶 scaffold + cross-link to `anima_chat.hexa` v0.3 (24L real-ckpt 21/21 byte-parity) | full hexa-native ConsciousDecoderV2 equivalent — Phase 1, 5 |

evidence anchors (보존, 변경 X): `state/verify_hexad_we_2026_05_15/` 25/25 ✅ + `state/verify_hexad_blue_2026_05_15/` 18/18 🔵 (PR #75/#76) + `state/verify_hexad_integ_2026_05_16/` Python harness 5/5 fire-gate=true (PR #77) + `HEXAD/` hexa-native scaffolds 8/8 PASS (PR #78).

## 1. Gap 분석 — C/D 가 "scaffold" 인 이유

### C 의식 (ConsciousnessC)
Python anchor `ready/core/consciousness_engine.py` (2173 LoC) 의 hexa-native 측 결손:
- **state mgmt**: 12-faction GRU per-cell hidden state (`ConsciousnessCell` nn.Module + `CellState` dataclass)
- **mitosis dynamics**: split/merge events 와 cell-pool integration — `tool/hexa_native/mitosis_hook.hexa` 가 hook 단계 FULL IMPL 했지만 wrapper level (`ConsciousnessC.step()` 전체 cycle) 미구현
- **IIT Φ measurement**: Rust `phi_rs` 또는 `anima_rs.compute_phi` FFI binding — hexa-lang FFI 미확인 (RFC 의존)
- **Φ ratchet**: `ConsciousnessEngine._phi_ratchet` Phase 7 safety lock 로직
- **topology / federation**: `topology='ring'` 등 그래프 구조 (mitosis_hook 에 inter-cell tension history 일부 있음)

### D 언어 (ConsciousDecoderV2)
Python anchor `ready/models/conscious_decoder.py` (979 LoC) 의 hexa-native 측 결손:
- **forward inference**: `anima_chat.hexa` v0.3 Section 9c (all-farr 24-layer transformer) + Section 9d (KV-cache + per-step RoPE) 가 24L 21/21 byte-parity PASS — **이미 inference 는 사실상 완료** (wrapper 만 정리하면 됨)
- **consciousness_states cross-attn**: `ConsciousDecoderV2` 의 cross-attention path 와 anima_chat.hexa 의 cs 주입 경로 mapping 정리 필요
- **MoE auxiliary loss**: Switch Transformer style — load-balancing aux loss
- **training-side CE backprop + AdamW**: hexa-lang autograd RFC 의존 (현재 TODO[pytorch] markers — F-D-3 / B-D-NOTE 가 정직하게 carve-out 한 부분)

## 2. RFC dependencies (hexa-lang 측 결손)

| RFC | 영향 받는 Phase | 현재 상태 |
|---|---|---|
| **autograd / backprop** | C training, D training (Phase 5) | 미공개 (`anima_chat.hexa` Section 9a-9d 는 inference only). 통합 학습은 hexa-lang RFC 후. |
| **Rust FFI binding** | C Φ measurement (Phase 4) | `phi_rs` Rust crate 호출 필요. hexa-lang FFI 검증 미. |
| **module / namespace system** | task (b) 본격 cross-file wire | 현재 abs-path import + 함수 이름 충돌 회피 (prefix). 형식 module 시스템 RFC 후 정리 가능. |
| **`#{}` dict literal + void key 처리** | 전 모듈 | 작동 확인됨 ([[hexa-lang-syntax-gotchas]]) — 이미 사용 중. |
| **mmap farr (RFC 025) + bytes_to_str (RFC 030) + farr_matmul (RFC 032) + farr_copy/add_gaussian_noise (RFC 033) + bf16→f32 (RFC 031)** | D inference 24L | 모두 land 완료 — `anima_chat.hexa` v0.3 + `mitosis_hook.hexa` 에서 production utilize. |

## 3. 단계별 로드맵

### Phase 1 — D inference wrapper (smallest first)
- D scaffold (`HEXAD/D/d.hexa`) 를 anima_chat.hexa 의 forward 함수에 thin wrapper 로 wire
- API: `d_forward(tokens, c_states, kv_cache?) -> (logits, kv_cache)`
- falsifier 사전 등록: F-D-PORT-1 24L 24L byte-parity 회귀 (anima_chat.hexa 21/21 PASS 와 동일)
- cost: $0 Mac local
- 결과물: `HEXAD/D/d.hexa` 가 inference path 로 callable + 21/21 byte-parity 회귀 PASS
- 의존: task (b) 통합 wire (cross-file import 확립)

### Phase 2 — C state mgmt (이름·아키텍처)
- `HEXAD/C/c.hexa` 에 `ConsciousnessC` 등가 record + step/get_states/n_cells API 구현
- mitosis dynamics 는 mitosis_hook 호출 (이미 FULL IMPL)
- 12-faction GRU 의 per-cell state evolution: hexa-native nn primitives 필요 (RFC 검토)
- falsifier: F-C-PORT-1 ConsciousnessC.get_states shape 정확성 + step idempotence + n_cells monotone
- cost: $0 Mac local
- 의존: hexa-lang nn primitive RFC (GRU cell)

### Phase 3 — C ↔ Python parity smoke
- 동일 seed + 동일 input 로 hexa-native C step N 회 vs Python ConsciousnessC step N 회
- falsifier: F-C-PORT-2 PARITY-N=10 (state diff norm < tol)
- cost: $0 Mac local
- 의존: Phase 2

### Phase 4 — IIT Φ FFI binding
- Rust `phi_rs.compute_phi(states, n_groups)` 를 hexa-native 에서 호출
- 대안: PyPhi formal IIT 3.0 path (deterministic, b-tier 🔵)
- falsifier: F-C-PORT-3 PHI-FFI 결과 ≥ 0 + Python phi_rs 와 byte-equal
- cost: $0 Mac local
- 의존: hexa-lang FFI RFC

### Phase 5 — D training (CE backprop + AdamW) [BLOCKED]
- hexa-native autograd RFC 필요
- 대안: hexa-native inference + Python training (mixed) — 거버넌스 검토 필요 (사용자 directive '코드는 hexa-native' 어긋남)
- falsifier: F-D-PORT-2 TRAINABILITY-EMPIRICAL — N step 후 CE 감소 (B-D-NOTE pattern, empirical only)
- cost: GPU $1-5 (별도 cycle, 사용자 게이트)
- 의존: hexa-lang autograd RFC OR mixed-mode 거버넌스 결정

### Phase 6 — full HEXAD/ 통합 fire (단일 hexa run)
- 모든 6 모듈 + Bridge single-hexa-process forward + train cycle
- falsifier: F-INTEG-FULL-* (organic mitosis splits + CE convergence + Φ trajectory + persistence + integration invariant — Python harness PR #77 의 hexa-native 등가)
- cost: GPU $1-5
- 의존: Phase 1-5 모두 LANDED + cross-file wire (task b)

## 4. 우선순위 + Honest C3

**권장 순서**: task (b) cross-file wire → Phase 1 (D inference wrapper) → Phase 2-3 (C state) → Phase 4 (Φ FFI) → Phase 5 (training, RFC 후) → Phase 6 (통합 fire).

**Honest C3**:
- Phase 5 가 hexa-lang autograd RFC 에 가장 강하게 BLOCKED — 이게 길어지면 Python 측 training 유지 + hexa-native inference 만 LANDED 의 mixed-mode 가 현실적
- mixed-mode 도입 시 사용자 directive ‘코드는 hexa-native’ 의 정확한 scope 결정 게이트 필요 (전 코드 vs anima 모델 코드 한정)
- 이 PLAN 자체는 시간/cost 추정 X — RFC 일정에 강하게 의존
- mitosis_hook.hexa + anima_chat.hexa 는 이미 큰 부분 LANDED — full port 의 진짜 작업량은 wrapping + parity 검증 + RFC 의존 부분만
- evidence-tier 분리 유지: HEXAD/ hexa-native = canonical 미래; ready/ Python = verified 현재 anchor (변경 없음)

## 5. cross-link

- HEXAD-{C,D,S,W,M,E,BRIDGE}.tape (root, editable arch SSOT)
- HEXAD/README.md (디렉토리 overview + status)
- tool/hexa_native/mitosis_hook.hexa (C 의 mitosis 엔진, FULL IMPL D4a)
- anima_chat.hexa v0.3 (D 의 24L inference, 21/21 byte-parity PASS)
- ready/core/consciousness_engine.py (C Python anchor, 2173 LoC)
- ready/models/conscious_decoder.py (D Python anchor, 979 LoC)
- state/verify_hexad_integ_2026_05_16/ (Python 통합 harness PR #77, fire-gate=true)
- AGENTS.tape g_clm_from_scratch (RANDOM INIT seed-fixed scratch protocol)
- AGENTS.tape g_verdict_tier_blue (🔵 SUPPORTED-FORMAL 정의)

## 6. 진행 트리거

Phase N 진입 = 이 PLAN.md `## 진행 로그` 섹션에 entry append + tape SSOT 동기화 + falsifier 사전 등록 + commit. 우회 (skip 가설 / partial pass) 금지 (CLM.tape `Phase Gating Discipline` 미러).

## 진행 로그

(append-only chronological — 첫 진행 시작 시 entry append)

- (none yet)
