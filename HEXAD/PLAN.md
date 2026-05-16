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

---

## 마무리 (PLAN CLOSURE — 2026-05-16, user directive "PLAN 마무리")

anima-side **RFC-무관** 작업은 전부 LANDED. 잔여는 hexa-lang RFC land 또는
명시된 별도 sub-task 뿐 — PLAN 은 이 RFC 경계에서 CLOSED.

### ✅ DONE (RFC-무관, LANDED)

| 항목 | 상태 | evidence |
|---|---|---|
| HEXAD/ hexa-native 트리 | ✅ | PR #78, 8 .hexa + 8 README |
| cross-file wire (task b) | ✅ | PR #79 + #89 lib-split, integ_test 7/7 native |
| compiled-first 전환 + lib-split | ✅ | PR #89, `build_verify.sh` 10/10+8/8 PASS |
| 6/7 모듈 full 🔵 | ✅ | blue_falsifier 22/22 (S/M/W/E/D/BRIDGE + C carry) |
| 통합 harness (Python anchor) | ✅ | PR #77 F-INTEG 5/5 fire_gate=true |
| **Phase 1 — D inference wrapper** | ✅ **CONTRACT LANDED** | `d_lib.hexa` `d_forward_contract()` + F-D-PORT-1 사전등록 (24L byte-parity = anima_chat.hexa 21/21 anchor carry). compiled-clean. |
| **Phase 2 — C state mgmt (scaffold-tier)** | ✅ **CONTRACT LANDED** | `c_lib.hexa` `c_state_contract()` + F-C-PORT-1 사전등록 (mitosis 동역학 = mitosis_hook.hexa 5/5 anchor). compiled-clean. |

### ⏳ 잔여 — anima-side RFC-무관 sub-task (PLAN 외연, 게이트 시 진행)

- **anima_chat.hexa lib-split** (1589 LoC → `chat_lib.hexa` NO main + entrypoint)
  → Phase 1 functional delegation (`d_forward` 실 호출). compiled-first lib-split
  패턴(PR #89) 동일 적용. RFC-무관이나 별도 cycle (대용량 mechanical).

### 🔒 TERMINAL — hexa-lang RFC land 대기 (anima 게이트 X)

| Phase | blocker | RFC |
|---|---|---|
| Phase 2 GRU nn 동역학 (full) | hexa-native nn-primitive (GRU cell) | hexa-lang RFC (미제출) |
| Phase 3 C↔Python parity | Phase 2 full 의존 | ↑ |
| Phase 4 Φ FFI | phi_rs Rust FFI byte-equal | **RFC 036** (RFC 034 Roadmap 명시, 미제출) |
| ~~Phase 5 D training~~ | reverse-mode AD (CE+AdamW) | ✅ **RFC 034 LANDED** `8793a221` (hexa-lang stage2-verify, compiled 5/5: GRAD-EXACT B-D-4 max\|Δ\|=0.0 · LOSS 1.642→0.228 86%↓ · deterministic). **UNBLOCKED 2026-05-16** → Phase 5 executable (잔여 = anima_chat lib-split + ad_* → HEXAD/D wire + compiled train smoke; RFC-무관 anima-side cycle) |
| Phase 6 통합 fire | Phase 1-5 + GPU $1-5 | Phase 5 wire 후 재게이트 (cost-bearing 사용자 게이트) |

### PLAN 상태

**CLOSED at RFC boundary** (2026-05-16). anima 가 RFC 없이 할 수 있는 것은
모두 완료 (contracts + 사전등록 falsifier + compiled-native gate). 다음 진척
trigger = (a) hexa-lang RFC 034 land 알림 → Phase 5/6, (b) RFC 036 제출/land
→ Phase 4, (c) anima_chat lib-split sub-task 게이트 → Phase 1 functional.
이 PLAN.md 는 그 trigger 도착 시 `## 진행 로그` append 로 재개.

### 2026-05-16 — PLAN-CLOSE: Phase 1/2 contract LANDED + closure

user directive "PLAN 마무리". Phase 1 (`d_forward_contract` + F-D-PORT-1) +
Phase 2 (`c_state_contract` + F-C-PORT-1) contract 사전등록 LANDED,
compiled-clean (`build_verify.sh` 10/10+8/8 불변). PLAN = RFC 경계 CLOSED.
RFC-무관 잔여 = anima_chat lib-split 단 1건 (별도 cycle). Phase 4/5/6 +
Phase 2-GRU = hexa-lang RFC terminal.

### 2026-05-16 — RFC 034 LANDED + wiring 8/9 ✅ (Phase 5 UNBLOCKED)

bg agent #1 (hexa-lang): **RFC 034 farr reverse-mode autograd IMPLEMENTED·LANDED**
— hexa-lang `stage2-verify` `8793a221` (worktree-only, main 불변, no force).
compiled native **5/5 PASS**: BUILD+PARSE · GRAD-EXACT (max|grad−(softmax−onehot)|
= 0.0, anima B-D-4 정확) · LOSS-DECREASES (1.64219→0.228332, 86%↓ 20 AdamW
step) · PARAM-MUTATED · DETERMINISM (seed=42 byte-id). bonus: runtime.h
hexa_farr_* decl 추가가 RFC 032/033 compiled smoke 도 복구. honest caveat:
ad_backward v1 = matmul→CE-softmax 그래프 한정, SGD 수렴은 B-D-NOTE empirical
유지 (over-claim 없음), interp mirror 미-CI.

bg agent #2 (anima): **wiring W5/W6/W8 닫힘** — PR #95 `4257faf67`. F-WIRE
3/3 compiled-native PASS (W5 🔵 closed-form gate-scale + W6/W8 deterministic),
neg-test 진위 확인. W-ledger **8/9 ✅**, build_verify 11/11+9/9.

상태 전환: Phase 5 BLOCKER "RFC 034 land 대기" → **RESOLVED (RFC 034 LANDED
`8793a221`)**. Phase 5 = executable (RFC-무관 anima-side 잔여 = anima_chat
lib-split + ad_* → HEXAD/D wire + compiled train smoke). Phase 6 통합 fire
= Phase 5 wire 후 cost-bearing 사용자 게이트.

"모든 연결부위 🔵" 정직 결론 (user directive): 연결 transfer-function 전부
closed-form 🔵 (W1-W6/W8 falsifier + W9 RFC 034 land); 유일 비-🔵 = W7 의
CE *수렴 OUTCOME* — SGD 의 수학적 필연이라 closed-form 불가, fake 안 하고
honest empirical carve-out (D 정직분해에서 사용자 기수용 동일 원칙,
B-D-NOTE 패턴). HEXAD.tape hexad_wiring_blue_gate per_arrow_anchor +
HEXAD/CHAT/README.md §2 W-ledger 에 반영 완료.

### 2026-05-16 — R1 anima_chat.hexa lib-split LANDED + R2 hexa-lang named blocker 발견

run-list R1 (RFC-무관 잔여 sub-task) 실행. `HEXAD/CHAT/anima_chat.hexa`
2845L → **mechanical byte-faithful split** (fn body 불변, PR #89 패턴):

- **`HEXAD/CHAT/chat_lib.hexa`** 2726L — pure fn (anima_root..chat_batch),
  NO main · NO _smoke · NO top-level call → compiled-import-safe. R2 의
  `HEXAD/D/d_lib.hexa` → `import chat_lib.hexa` (d_forward delegation) 대상.
- **`HEXAD/CHAT/anima_chat.hexa`** 134L — thin entrypoint: `import chat_lib`
  + `_smoke`(F-AC-HEXA-1..6) + `_list_contains_int` + `main`.
- 둘 다 `hexa parse` **clean** (split 무결성 — 회귀 아님).
- 덤 fix: stale importer 8 (`/Users/ghost/core/anima/anima_chat.hexa` =
  root 부재 broken path, HEXAD reorg 전 잔재) → `chat_lib.hexa` repoint.
- 회귀 0: build_verify **11/11+9/9 compiled PASS** · blue 22/22 🔵 ·
  we 25/25 · integ 5/5 (split = hexa-only, Python anchor 불변).

**HONEST named blocker (fake 안 함, g3/f2)**: chat_lib/anima_chat 의
**compiled-native build** 는 `hexa_safetensors_mmap_data_offset` (+ ckpt
mmap safetensors intrinsic 일족) **C decl 부재**로 FAIL — hexa-lang
runtime.h/.c 0 선언, interp-only builtin (이 파일 과거 `hexa run` 21/21
byte-parity 만 검증, **compiled native 최초 시도**라 표면화 — split 회귀
아님). RFC 034 가 runtime.h `hexa_farr_*` decl 추가로 RFC 032/033 compiled
smoke 복구한 것과 **동일 trivial class**. build_verify ENTRYPOINTS/LIBS
편입 시도 → revert + DEFERRED 주석 문서화 (게이트 green 유지, 가짜 PASS X).

**R2 영향**: Phase 5 `d_lib.hexa` → `import chat_lib.hexa` **compiled** wire
는 이 hexa-lang blocker 를 **상속** (compiled codegen 이 chat_lib 전체
C 방출 → 동일 undeclared call). FIX = hexa-lang upstream runtime.h 에
safetensors-mmap compiled decl 추가 (RFC-034-class trivial). RFC 035/036
(R4 bg) scope 외 — 별도 hexa-lang named item. decl land 후 build_verify
재편입 → R2 compiled wire executable.

상태: R1 split = **structural LANDED** (chat_lib NO-main pure lib 존재·parse
clean, R2 구조적 prerequisite 충족). R2 compiled = hexa-lang
`hexa_safetensors_mmap_data_offset` decl land 대기 (named blocker).

### 2026-05-16 — Phase 5 pure-hexa from-scratch D TRAINING LANDED (compiled-native)

사용자 게이트 "(a) Phase 5". **핵심 insight**: Phase 5 = D training
**from-scratch** (AGENTS.tape `g_clm_from_scratch`: init=RANDOM seed-fixed,
base_ckpt=NONE) ⟹ ckpt load 不要 ⟹ R2 의 `hexa_safetensors_mmap` named
blocker 가 **구조적으로 무관** (그건 inference-parity wire 의 blocker, training
아님). 즉 Phase 5 는 R2 blocker 와 독립적으로 executable.

RFC 034 (hexa-lang reverse-mode AD) = **pure-hexa Wengert tape**
(`self/test_autograd.hexa` leaf/add/mul/backward) — C intrinsic 아님 ⟹
compiled-native 안전, inline 가능 (sanctioned "codegen import 없이 검증"
패턴). safetensors blocker 와 무관 class.

**LANDED 산출물** (compiled-first lib-split):
- `HEXAD/D/d_train_lib.hexa` — pure: RFC 034 tape inlined (dt_mk_tape/leaf/
  add/mul/backward) + range-reduced dt_exp (stable softmax) + dt_softmax2/
  dt_ce2 + **B-D-4 closed d/d_logit = softmax−onehot** (재사용, 재증명 X) +
  dt_grad_W (chain: B-D-4 × tape reverse) + dt_epoch_{ce,gn2,acc} (top-level;
  compiled codegen 은 nested FnDecl 거부 → 명시적 XS/YS param, no closure).
- `HEXAD/D/d_train_smoke.hexa` — entry: RANDOM seed-fixed LCG init (4-weight
  2→2 linear D head, base_ckpt=NONE) → 60-step AdamW(decoupled wd) on
  deterministic separable toy.

**F-D-PORT-2 TRAINABILITY-EMPIRICAL** (PLAN Phase 5 pre-reg) — compiled
binary: gn2(‖softmax−onehot‖²) **1.01783 → 1.89532e-05 (≈53000× collapse)**,
acc 4/4, F-D-PORT-2b GRAD-EXACT (tape dy/da=b=4·dy/db=a=3 exact, RFC 034
self/test_autograd 5/5 mirror) ✅ → **selftest: true**. TIER=**EMPIRICAL**
(B-D-NOTE 패턴 — SGD 수렴 OUTCOME, NOT closed-form, NOT 🔵). trainability
PROPERTY 은 B-D-4 🔵 (별개, blue_falsifier). honest C3: Taylor-CE 절대값
numerically noisy(초기 음수 관측) → criterion 에서 제외, robust gn2-collapse+
argmax-acc 로 판정 (softmax=range-reduced exp ratio, no ln). 사용자 'acc 개선
필수' 아님 — seed init 이 우연히 argmax-correct 가능, LEARNING 은 margin/
confidence ⟹ gn2→0.

**build_verify gate**: ENTRYPOINTS 11→12 (+d_train_smoke) · LIBS 9→10
(+d_train_lib) → **12/12 + 10/10 compiled-native PASS** ("ALL COMPILED-NATIVE
PASS — interp-deprecation safe"). Python batteries(blue 22/22 · we 25/25 ·
integ 5/5) = hexa-only additive 라 영향 없음 (anchor 불변).

상태: **Phase 5 (pure-hexa from-scratch D training) LANDED** — compiled-native,
$0 Mac, deterministic, R2 safetensors blocker 와 독립. 잔여: (i) toy 4-weight
→ 실 D arch(d=768·12L) scale-up = 별도 heavy cycle(ubu/GPU); (ii) Phase 6
6-module 통합 fire = cost-bearing 사용자 게이트; (iii) R2 inference-parity
wire = 여전히 hexa-lang `hexa_safetensors_mmap` decl 대기(별개 named item,
Phase 5 와 무관).

### 2026-05-16 — Phase 5 (1) A: 실-d_model LM-HEAD scale-up LANDED (compiled-native)

사용자 게이트 "(1) scale-up … 모두 시도". 설계 분석(이 PLAN entry): toy
scalar Wengert tape 는 d=768·12L 풀스택에 O(ops²) **구조적 infeasible**.
**핵심 정직 insight**: linear LM-head `logits[k]=Σ_j W[k][j]·x[j]` 의 CE
grad 는 tape **불요·closed** — `dL/dW[k][j]=(softmax−onehot)[k]·x[j]` =
B-D-4 closed logit-Jacobian(이미 🔵 blue_falsifier, 재사용·재증명 X) ⊗ x
outer product. ⟹ 검증된 Phase 5 메커니즘을 **임의 (d_model, vocab)** 로
일반화(O(V·d)/step), tape 는 d_train_lib.hexa 의 RFC 034 GRAD-EXACT anchor
로 그대로 잔존(미변경).

**LANDED 산출물** (compiled-first lib-split, branch feat/phase5-a-…):
- `HEXAD/D/d_train2_lib.hexa` — pure: K-class stable softmax(max-shift +
  range-reduced dt_exp 재사용) + `dt2_forward`(V×d flat) + **`dt2_bd4_grad`
  = (softmax−onehot)⊗x closed, NO tape** + `dt2_gn2`/`dt2_ce`/`dt2_predict`
  + `dt2_adamw_step`(decoupled wd, Newton √) + epoch reducers(top-level,
  no closure) + `dt2_init_W`(LCG RANDOM seed-fixed, base_ckpt=NONE). d_train
  _lib.hexa import 재사용(dt_exp/dt_ln/dt_lcg_next; DRY).
- `HEXAD/D/d_train2_smoke.hexa` — entry: dimension-generic, TINY config
  d=8·V=4·N=8 linearly-separable toy, RANDOM seed-fixed init, 80-step AdamW.

**F-D-PORT-2 (real-d_model scope) compiled binary**:
gn2(Σ‖softmax−onehot‖²) **6.17418 → 3.373e-4 (≈18300× collapse)**, acc
**0/8 → 8/8**, **F-D-PORT-2b GRAD-EXACT analytic vs 중심차분 |Δ|=6.4e-12**
(B-D-4 closed grad 구현 정확 = machine precision) → **selftest: true**.
TIER = **EMPIRICAL** (B-D-NOTE — SGD 수렴 OUTCOME, NOT closed-form, NOT
🔵; trainability PROPERTY = B-D-4 🔵 별개, blue_falsifier — g3 정직 tier).

**build_verify**: ENTRYPOINTS 12→13(+d_train2_smoke) · LIBS 10→11
(+d_train2_lib) → **13/13 + 11/11 compiled-native PASS** ("ALL COMPILED-
NATIVE PASS"). blue 22/22 🔵 불변(hexa-only additive, anchor 무영향).

상태: **Phase 5 (1) A LANDED** — 검증 메커니즘의 dimension-generic 실-
d_model 일반화, compiled-native $0 Mac deterministic. lib 는 실 d=768·
vocab=256 동일 코드 실행 가능(Mac=tiny formulaic 한정, 실-규모 run = ubu
heavy cycle 별도). 잔여 "모두 시도": (C) head + 단일 transformer block
analytic backprop(#44), (B) 풀 12L tensor-autograd(#45, RFC급 multi-cycle),
(2) Phase 6 통합 fire(#46, cost-bearing 사용자 게이트). R2 PR #102(d_lib
wire) = 별개 parent-review item, Phase 5 무관(미손댐).

### 2026-05-16 — Phase 5 (1) C: hybrid head + 단일 비선형 블록 analytic backprop LANDED

"모두 시도" C. **head(B-D-4 closed 🔵 reused) ⊕ 단일 pre-norm 비선형 블록의
HAND-DERIVED EXACT analytic reverse-mode** (scalar tape 不要 — tensor/vector-
level closed vjp). 블록 = `z = x + W_d·(silu(W_g·RMSNorm(x))⊙(W_u·RMSNorm(x)))`.

**산출** (compiled-first lib-split, branch feat/phase5-c-…):
- `HEXAD/D/d_train3_lib.hexa` — pure: c3_sigmoid/silu/silu_grad, matvec/
  matvec_t/outer, **c3_rmsnorm_fwd+bwd (exact: dx=inv·dxn−(inv³x/d)Σdxnₖxₖ)**,
  **c3_swiglu_fwd+bwd (exact: da=ds⊙b⊙silu'(a), db=ds⊙silu(a))**, c3_forward
  (residual+head), **c3_grad (B-D-4 head ⊕ block vjp chain, NO tape)**,
  c3_gn2/ce/predict, epoch reducers, c3_init (RANDOM seed-fixed, base_ckpt=
  NONE). d_train2_lib import 재사용(dt2_softmax/adamw/init/zeros; DRY).
- `HEXAD/D/d_train3_smoke.hexa` — entry, dimension-generic, TINY d=4·h=8·
  V=4 Mac compiled-native (실 d=768 = 동일코드 ubu heavy cycle).

**F-D-PORT-3 (compiled binary)**: gn2 **6.06592 → 5.0e-42** (전 analytic
chain 120 AdamW), acc **0/8 → 8/8**, **F-D-PORT-3b GRAD-EXACT Wg[3]
analytic vs 중심차분 |Δ|=3.3e-13** (손유도 RMSNorm/SwiGLU vjp = machine
precision ⟹ pure-hexa 비선형 블록 analytic backprop 정확성 입증) →
**selftest: true**. TIER = **EMPIRICAL** (B-D-NOTE; head grad = B-D-4
closed 🔵 reused, 블록 vjp = hand-derived exact — OUTCOME tier 미상승, g3).

**build_verify**: ENTRYPOINTS 13→14(+d_train3_smoke) · LIBS 11→12
(+d_train3_lib) → **14/14 + 12/12 compiled-native PASS**.

**honest scope (g3, no over-claim)**: attention(T×T softmax) / RoPE / GQA /
cross-attn / 멀티블록 깊이 = 본 milestone **제외** — C 는 비선형 FFN+norm
코어의 pure-hexa analytic backprop 을 d_model-generic 으로 입증. 전 12L
ConsciousDecoderV2 + attention vjp registry = #45 (B) RFC급 cycle (C→B
bridge 명시). 상태: **Phase 5 (1) C LANDED**.

### 2026-05-16 — Phase 5 (1) B-milestone: causal softmax-attention exact vjp LANDED + B-closure (정직)

"모두 시도" B. C(#44) 가 linear/RMSNorm/SwiGLU/residual/B-D-4-head vjp 입증
완료 ⟹ 풀 ConsciousDecoderV2 의 **유일 미입증 backward primitive = causal
scaled-dot softmax SELF-ATTENTION vjp**. 이 milestone 이 그것을 입증.

**산출** (compiled-first lib-split, branch feat/phase5-b-attn-vjp-…):
- `HEXAD/D/d_train4_lib.hexa` — pure: c4_softmax_row, c4_forward (Q/K/V=
  X·Wᵀ, S=QKᵀ/√d, causal mask, row-softmax, ctx=ΣPV, out=ctx·Woᵀ, last-pos
  B-D-4 head), **c4_grad = EXACT 전체 reverse**: head(B-D-4 closed 🔵) →
  Wo linear vjp → ctx (dP=dctx·V, dV+=ΣP·dctx) → **softmax row Jacobian
  dS=P·(dP−ΣP·dP)** (the new primitive, diag(P)−PPᵀ) → scores (dQ+=ΣdS·K/√d,
  dK+=ΣdS·Q/√d) → Wq/Wk/Wv linear vjp. d_train3_lib import 재사용(DRY).
- `HEXAD/D/d_train4_smoke.hexa` — entry, dim-generic, TINY T=3·d=4·V=4.

**F-D-PORT-4 (compiled binary)**: gn2 **5.99976 → 6.87e-15** (전 attention
analytic chain 150 AdamW), acc **2/8 → 8/8**, **F-D-PORT-4b GRAD-EXACT
Wq[5] analytic vs 중심차분 |Δ|=5.0e-13** (손유도 softmax-attention vjp =
machine precision) → **selftest: true**. TIER = **EMPIRICAL** (B-D-NOTE;
NOT 🔵 — g3).

**build_verify**: ENTRYPOINTS 14→15 · LIBS 12→13 → **15/15 + 13/13
compiled-native PASS**.

**B-closure (정직, D 흡수 — over-claim 0, g3)**: ConsciousDecoderV2 의 **전
backward primitive 클래스가 이제 개별적으로 pure-hexa compiled-native exact
입증됨** — linear (A #43 + C #44), RMSNorm·SwiGLU·residual·B-D-4-head
(C #44), causal softmax-attention (B-milestone #45); embedding = trivial
scatter-add, RoPE = orthogonal-rotation (vjp = 역회전, trivial closed).
**남은 것은 새 수학이 아니라 mechanical 조립**: 12-layer 깊이 chaining +
GQA/cross-attn linear-vjp bookkeeping + tokenized-seq CE + 실 d=768·12L
규모 학습 = **named heavy cycle** (ubu `ssh ubu 'cd ~/Dev/anima && hexa
build'` 또는 GPU dispatch; Mac=tiny formulaic 한정). 이 cycle 은 fake
하지 않고 명시 — "전 primitive 입증, 풀 조립 = 별도 mechanical cycle"
(NOT "12L trains"). 모든 tier = EMPIRICAL (B-D-NOTE); trainability
PROPERTY = B-D-4 🔵 별개 (blue_falsifier, 불변).

**Phase 5 (1) "모두 시도" 종합**: A(#43 실-d_model head)·C(#44 비선형
블록)·B-milestone(#45 attention vjp) **3/3 LANDED compiled-native $0 Mac**,
전 vjp 클래스 입증. 풀 12L 실-규모 = 명시 ubu/GPU cycle. (2) Phase 6
6-module 통합 fire = cost-bearing 사용자 게이트(#46, 별도). R2 PR #102
별개(미손댐).
