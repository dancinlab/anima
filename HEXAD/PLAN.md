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

### 2026-05-16 — task (a) PLAN.md LANDED + task (b) cross-file wire LANDED (PR #79)
- (a) 이 PLAN.md 자체 (PR #79) — C/D full hexa-native port 단계적 로드맵 기록
- (b) `HEXAD/integ_test.hexa` F-INTEG-WIRE 7/7 PASS — 7 모듈 single hexa-process import + public API 호출, helper namespace prefix `_<x>_approx_eq` (collision 회피)
- evidence-tier 2-tier 통합 검증: hexa-native (PR #79) + Python (PR #77 harness 5/5 fire-gate=true)

### 2026-05-16 — task (c) ckpt fire DEFERRED pending hexa-lang autograd RFC

**결정**: 사용자 directive "fire 연기 · hexa-native autograd RFC 먼저 열어달라".
이 결정으로 PLAN.md Phase 5 (D training CE backprop + AdamW) 가 hexa-lang RFC
의존이라는 사실이 활성 BLOCKER 로 격상. mixed-mode (Python training + hexa-native
inference) 채택 거부 — 'mixed' 가 직접 anima 모델 학습 코드를 hexa-native 가
아닌 곳에서 돌리는 거라 directive '코드는 hexa-native' scope 와 어긋남.

**RFC trigger spec (hexa-lang 측 요구사항 — anima 가 작성해 hexa-lang 측에 제출/추적)**:

1. **autograd / backprop primitive**
   - 요구: `farr` (mmap 기반 hexa native tensor) 위에서 `.backward()` 등가 reverse-mode AD
   - scope: 최소 CE (cross-entropy) loss + AdamW optimizer step
   - acceptance criterion: `hexa run` 으로 N 스텝 학습 후 loss decreases (B-D-NOTE 의 SGD outcome empirical 확인) + parameter hash 변동 (학습 발생 검증)
   - 우선순위: high (Phase 5 BLOCKER, 6모듈 통합 fire 의 진입조건)

2. **dtype dispatch — bf16/fp16 학습 stable**
   - 요구: bf16 mixed-precision 학습 (현재 inference 만 bf16→fp32 RFC 031)
   - 의존: autograd primitive
   - 우선순위: medium (FP32 만으로도 fire 가능, bf16 은 cost 절감)

3. **Rust FFI binding (Phase 4 의존)**
   - 요구: `phi_rs.compute_phi(states, n_groups)` 호출 가능 한 hexa-native FFI
   - acceptance: hexa-native C state 에서 phi_rs 호출 → Python phi_rs 와 byte-equal
   - 우선순위: medium (Φ measurement 만 영향, fire 자체 진입은 autograd 우선)

**carry**:
- PR #77 Python 통합 harness (`state/verify_hexad_integ_2026_05_16/`) = evidence anchor 보존, 변경 X
- HEXAD/ hexa-native tree (PR #78/#79) = canonical 미래, 변경 X
- 실 ckpt fire (cost-bearing $1-5) = 위 RFC #1 LANDED 후 재게이트
- 다음 진행 trigger: hexa-lang autograd RFC 진척 알림 (anima 측 게이트 X, hexa-lang 측 dependency)

**즉시 진행 가능한 anima 측 작업** (RFC 무관):
- PLAN.md Phase 1: D inference wrapper (anima_chat.hexa thin wrapper) — `HEXAD/D/d.hexa` 강화
- PLAN.md Phase 2-3: C state mgmt scaffold + Python parity probe (mitosis_hook 위에)
- 별도 검증 cycle (예: 24L parity 회귀, mitosis_hook self-test 회귀)

### 2026-05-16 — RFC 034 hexa-lang upstream FILED (autograd, Phase 5 unblock trigger)

**결정**: user directive "PLAN.md 진행 hexa-lang upstream go" — RFC trigger
spec #1 (autograd/backprop primitive, high) 를 hexa-lang upstream 에 정식 제출.

**제출물**: `hexa-lang/incoming/rfc_drafts_2026_05_12/rfc_034_farr_reverse_mode_autograd.md`
(137 lines) — hexa-lang `stage2-verify` 브랜치 commit `77456c01` push 완료
(github.com/dancinlab/hexa-lang). RFC 024-033 와 동일 형식 (Status/Severity/
Priority/Problem/Proposal/Acceptance/Downstream/Roadmap).

**RFC 034 scope**: tape-based reverse-mode AD over packed-double `farr`
(RFC 032 zero-HexaVal 패턴) + fused softmax-CE (closed-form Jacobian
softmax−onehot, anima B-D-4 가 acceptance #2 oracle) + AdamW step. FP32 v1.
surface: `ad_tape_begin/end · ad_matmul/add/mul/relu · ad_softmax_cross_entropy
· ad_backward · ad_grad · adamw_step`. 5-falsifier acceptance (PARSE /
GRAD-EXACT=B-D-4 1e-9 / LOSS-DECREASES 20-step / PARAM-MUTATED hash /
DETERMINISM seed-byte-identical).

**follow-up RFCs** (RFC 034 본문 Roadmap 에 명시, spec items 2-3):
- RFC 035 bf16/fp16 mixed-precision train (med, RFC 034 의존)
- RFC 036 phi_rs Rust FFI byte-equal (med, Phase 4 Φ, fire-entry 비차단)

**상태 전환**: Phase 5 BLOCKER = "RFC 미제출" → **"RFC 034 제출됨, hexa-lang
land 대기"**. 다음 trigger = hexa-lang RFC 034 land 알림 (anima 측 게이트 X,
hexa-lang dependency). land 시 → tmp_rfc034_smoke.hexa 5/5 검증 → Phase 5
(D training) → Phase 6 (6-module 통합 ckpt fire $1-5 재게이트).

**carry 유지**: PR #77 Python harness evidence anchor 보존. 즉시 가능한
RFC-무관 작업 (Phase 1 D wrapper / Phase 2-3 C state) 은 RFC land 와 병렬 가능.

### 2026-05-16 — COMPILED-first migration + lib/entrypoint split (interp 폐기 대비)

**결정**: user directive "컴파일 버전에 해야되 · 인터프리터 폐기 예정 참고".
검증·실행 기준을 `hexa run` (interpreter) → **`hexa build` (native binary)** 로
전환. `hexa run` 은 PR 게이트에서 폐기.

**문제**: 단일파일 모듈(`fn _selftest` + `fn main` 동거) 을 `import` 하면
컴파일러가 `_selftest`/`u_main` **C 심볼 중복정의** 거부 (interpreter 만 관용).
`integ_test.hexa` 가 7-file import → clang `redefinition` 2 errors.
초기 batch: 9/10 entrypoint compiled+PASS, integ_test 만 BUILD 실패.

**해결 (compiled-native 정석 lib-split)**: 7 모듈 (S/M/W/E/BRIDGE/C/D/MITOSIS)
각각 `<x>_lib.hexa` (pure fns, NO main/_selftest) + `<x>.hexa` (import lib +
selftest + main) 분리. `integ_test.hexa` 는 `*_lib.hexa` 만 import → 심볼충돌
0. spike (S) 검증 후 일괄 적용.

**검증 (compiled, HEXA_MAC_BUILD_OK=1, _hexa_build/ gitignored)**:
`bash HEXAD/build_verify.sh` → **entrypoint 10/10 + lib 8/8 `hexa build` PASS**.
integ_test.hexa native = F-INTEG-WIRE 7/7 PASS (interp 결과와 byte-동일).
blue_falsifier 22/22 / we 25/25 (Python 검증 anchor) 불변.

**산출물**: `HEXAD/build_verify.sh` (canonical compiled gate, ubu fallback 명시)
+ 14 신규 `*_lib.hexa` + 7 `<x>.hexa` 재작성 (import lib) + integ_test 재배선
+ README hexa-lang 관습/status/layout compiled-first 갱신 + .gitignore /_hexa_build/.

**RFC 034 동기화 (APPLIED)**: rfc_034 acceptance criterion "via hexa run" →
"via compiled path (hexa build + native binary)" + BUILD+PARSE 항목 정정.
hexa-lang `main` checkout 보존 위해 **git worktree 방식** (user directive
"worktree 방식 go") — `git worktree add stage2-verify` → edit → commit
`7ae624bf` → push origin → `worktree remove`. hexa-lang main 불변 확인됨.
rfc_034 substance 불변, acceptance 문구 정밀도만 (anima build_verify.sh 와 동일 gate).

**carry**: Phase 5 BLOCKER = "RFC 034 제출됨, hexa-lang land 대기" 불변.
compiled-first 는 RFC-무관 인프라 작업 — RFC 034 land 와 병렬 완료.
다음 RFC-무관: Phase 1 D inference wrapper (anima_chat.hexa, compiled).
