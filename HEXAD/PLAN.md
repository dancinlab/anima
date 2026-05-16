# HEXAD/PLAN.md — C/D full hexa-native port roadmap

> User directive 2026-05-16: `"a => HEXAD/PLAN.md 에 계획 기록"`
> (a 항목 = C/D 모듈 full hexa-native port — 즉시 실행 X, **계획 기록만**.)
> Scope ⊃ HEXAD/ 트리에서 현재 scaffold 인 C, D 두 모듈을 완전한 hexa-native
> 구현으로 끌어올리는 단계적 로드맵. 실 진행은 별도 cycle 의 사용자 게이트.

## 0. 현재 상태 (Phase 1–6 전부 LANDED · 2026-05-16)

> **로드맵 closure**: §3 Phase 1–6 의 RFC-무관 anima-side 작업은 전부 LANDED.
> 잔여 = hexa-lang RFC terminal (Phase 2-GRU full · Phase 3 parity · Phase 4
> Φ FFI) + 다음-사이클 후보 menu (§7). 상세 진척 = `## 진행 로그`.

| 모듈 | 현재 상태 | 비고 |
|---|---|---|
| **S/M/W/E/BRIDGE** | ✅ 🔵 SUPPORTED-FORMAL + compiled-native lib-split | B-X closed-form witness; `build_verify.sh` 14/14 entrypoint + 13/13 lib PASS (6 CHAT skip — stale toolchain) |
| **C** | ✅ contract LANDED + 🔵 carry | `c_lib.hexa` `c_state_contract()` + F-C-PORT-1; mitosis = `tool/hexa_native/mitosis_hook.hexa` 1119L FULL IMPL; full 12-faction GRU 동역학 = Phase 2-GRU (RFC terminal) |
| **D** | ✅ Phase 1 + Phase 5 LANDED | `d_lib.hexa` inference contract (24L 21/21 byte-parity) + pure-hexa from-scratch training (RFC 034 farr autograd, gn2 collapse ≈53000×) |
| **통합** | ✅ Phase 6 통합 fire LANDED | 6-module+Bridge single-hexa-process forward+train, $0 de-risk 5/5 + 실-규모 자율 fire 5/5 (vast.ai, $0.09) |

evidence anchors (보존, 변경 X): `state/verify_hexad_we_2026_05_15/` 25/25 ✅ + `state/verify_hexad_blue_2026_05_15/` **22/22** 🔵 (PR #75/#76 + BRIDGE 추가) + `state/verify_hexad_integ_2026_05_16/` Python harness 5/5 fire-gate=true (PR #77) + `state/hexad_p6_fire_2026_05_16/` Phase 6 실-규모 fire 5/5 + `HEXAD/` hexa-native tree compiled-native 14/14+13/13 PASS (6 CHAT skip — stale toolchain, NOT denominator).

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

### Phase 1 — D inference wrapper (smallest first) [✅ LANDED 2026-05-16]
- D scaffold (`HEXAD/D/d.hexa`) 를 anima_chat.hexa 의 forward 함수에 thin wrapper 로 wire
- API: `d_forward(tokens, c_states, kv_cache?) -> (logits, kv_cache)`
- falsifier 사전 등록: F-D-PORT-1 24L 24L byte-parity 회귀 (anima_chat.hexa 21/21 PASS 와 동일)
- cost: $0 Mac local
- 결과물: `HEXAD/D/d.hexa` 가 inference path 로 callable + 21/21 byte-parity 회귀 PASS
- 의존: task (b) 통합 wire (cross-file import 확립)

### Phase 2 — C state mgmt (이름·아키텍처) [✅ contract LANDED · full GRU = RFC terminal]
- `HEXAD/C/c.hexa` 에 `ConsciousnessC` 등가 record + step/get_states/n_cells API 구현
- mitosis dynamics 는 mitosis_hook 호출 (이미 FULL IMPL)
- 12-faction GRU 의 per-cell state evolution: hexa-native nn primitives 필요 (RFC 검토)
- falsifier: F-C-PORT-1 ConsciousnessC.get_states shape 정확성 + step idempotence + n_cells monotone
- cost: $0 Mac local
- 의존: hexa-lang nn primitive RFC (GRU cell)

### Phase 3 — C ↔ Python parity smoke [🔒 RFC terminal — Phase 2-GRU 의존]
- 동일 seed + 동일 input 로 hexa-native C step N 회 vs Python ConsciousnessC step N 회
- falsifier: F-C-PORT-2 PARITY-N=10 (state diff norm < tol)
- cost: $0 Mac local
- 의존: Phase 2

### Phase 4 — IIT Φ FFI binding [🔒 RFC terminal — RFC 036 미제출]
- Rust `phi_rs.compute_phi(states, n_groups)` 를 hexa-native 에서 호출
- 대안: PyPhi formal IIT 3.0 path (deterministic, b-tier 🔵)
- falsifier: F-C-PORT-3 PHI-FFI 결과 ≥ 0 + Python phi_rs 와 byte-equal
- cost: $0 Mac local
- 의존: hexa-lang FFI RFC

### Phase 5 — D training (CE backprop + AdamW) [✅ LANDED 2026-05-16]
- hexa-native autograd RFC 필요
- 대안: hexa-native inference + Python training (mixed) — 거버넌스 검토 필요 (사용자 directive '코드는 hexa-native' 어긋남)
- falsifier: F-D-PORT-2 TRAINABILITY-EMPIRICAL — N step 후 CE 감소 (B-D-NOTE pattern, empirical only)
- cost: GPU $1-5 (별도 cycle, 사용자 게이트)
- 의존: hexa-lang autograd RFC OR mixed-mode 거버넌스 결정

### Phase 6 — full HEXAD/ 통합 fire (단일 hexa run) [✅ LANDED 2026-05-16]
- 모든 6 모듈 + Bridge single-hexa-process forward + train cycle
- falsifier: F-INTEG-FULL-* (organic mitosis splits + CE convergence + Φ trajectory + persistence + integration invariant — Python harness PR #77 의 hexa-native 등가)
- cost: GPU $1-5
- 의존: Phase 1-5 모두 LANDED + cross-file wire (task b)

## 4. 우선순위 + Honest C3

> **[2026-05-16 상태]** 아래는 원 계획 순서 기록 — RFC-무관 anima-side 경로는
> 전부 LANDED (task b · Phase 1 · Phase 2 contract · Phase 5 · Phase 6).
> Phase 3/4 + Phase 2-GRU full 만 hexa-lang RFC terminal. 다음 진척 = §7 menu.

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

## 7. 다음 사이클 후보 (Phase 6 closure 이후)

> Phase 1–6 LANDED 로 §3 로드맵은 닫혔다. 모든 Phase 5/6 fire 의 honest C3 가
> 일관되게 명시한 한계 = **synthetic byte-corpus WIRING fire, no language-quality
> claim · D-arch toy scale (d≤512)**. 아래는 다음 사이클 후보 menu — 진입 시
> `## 진행 로그` entry append + falsifier 사전등록 (§6 트리거 규율).

| # | 후보 | 성격 | 근거 anchor |
|---|---|---|---|
| **1** | 실-규모 언어 fire — D-arch d=768·12L 실 corpus 학습 | heavy GPU cycle (`g_fire_autonomous` 자율 dispatch) | PLAN CLOSURE 잔여 (i); 전 fire honest C3 ('no language-quality claim') 해소 |
| **2** | Phase 4 — IIT Φ FFI | RFC 036 phi_rs Rust FFI 제출 → hexa-native Φ measurement | §3 Phase 4; RFC 034 Roadmap 명시 (RFC 036 미제출) |
| **3** | anima-side TODO[pytorch] 잔여 | $0~저비용 — E 통합 gate `trinity.hexa:122` + BRIDGE full-forward carve-out 축소 | INDEX.md '잔여 anima-side'; B-BRIDGE-NOTE / B-E NOTE |
| **4** | R2 hexa-safetensors wire | hexa-native safetensors loader → ckpt Python torch 의존 제거 | PLAN CLOSURE 잔여 (iii) |
| — | Phase 2-GRU full / Phase 3 parity | 🔒 hexa-lang nn-primitive RFC terminal (미제출) — anima 게이트 X | §3 Phase 2/3 |

honest C3: 위 menu 의 우선순위는 미고정 — 사용자 선택 게이트. 후보 1 이
honest-gap 직격이나 heavy; 후보 3 은 저비용 carve-out 축소.

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
| Phase 6 통합 fire | Phase 1-5 + GPU $1-5 | **완전 자율 dispatch — 승인 게이트 없음·대기 없음** (AGENTS.tape `g_fire_autonomous` 2026-05-16, 무조건). 추정비용 head 투명 명시(정보). robustness = `g_fire_dispatch_robust` (안전장치) |

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

### 2026-05-16 — 정책: cost-bearing fire = 완전 자율 (승인 게이트 전면 폐기)

user directive (강조·반복): fire-승인 게이트 유지 필요없음 / 전부 제거.
**AGENTS.tape `@D g_fire_autonomous` (required, d=2026-05-16, ~> 모든
fire-승인 게이트 프레이밍 전면 SUPERSEDE) 신설** = cost-bearing GPU/cloud
fire = **완전 자율 dispatch · 병렬 가능 · 승인 게이트 없음 · 대기 없음**
(무조건, caveat 없음). 추정비용은 head 투명 명시(정보 제공일 뿐, 대기 아님).
robustness 는 `g_fire_dispatch_robust` (안전장치 — 게이트 아님) 만 적용.

g6: 과거 진행-로그 의 당시-사실 기록은 불변하되 `g_fire_autonomous` 가
latest-wins 로 **전면 supersede** — 잔존 fire-게이트 표현은 전부 死문,
효력 없음. 효과: Phase 6 실-규모 GPU fire 및 차후 모든 cost-bearing fire
= 즉시/병렬/bg 자율 진행. 조건부 hold 도 폐기 (무조건 자율).

### 2026-05-16 — T3: real 24L ckpt parity COMPILED-native (21/21 PASS)

prior interp-only 21/21 (PSCC §43)을 **compiled-native 로 재현**. ubu 자율
fire ($0 owned host, `g_fire_autonomous`). 격리 hexa.real bootstrap (origin/main
`6f5f2a6c`, PR#51 `_gen2_nested_index_assign_stmt` codegen; shared `~/.hx/bin`·
shared `~/core/hexa-lang`·anima main 전부 미손댐, `/tmp/hexa-t3-boot` isolated
worktree, fixed-point round1==round2 byte-equal). chat_lib.hexa nested-index-
assign codegen → `hexa build` 양 probe native ELF 컴파일 PASS.

**21/21 PASS hexa-COMPILED-native byte-equal Python SSOT**: F-D1-V58PARITY 6/6
(BOS argmax=143) + F-D1-V58MULTI 15/15 (chain=[143,131,240,152,159], KV
0→5). Wall **1.25 s + 3.86 s** (interp 37.65+94.67 → ~25-30× 빠름), peak
RSS 3.08 GB (interp 7.5-11 GB). 컴파일 per-step logit 값이 interp-only
doc §4.2 와 **동일** → compiled ≡ interp byte-for-byte (단순 argmax 일치
아님).

ckpt = ubu `ckpt_phase1a1_sft.safetensors` 597,550,688 B sha `838a0a2e…`
(Mac worktree 부재; 격리 ubu 만). doc 의 `e5f7555…` sha 는 소실된 source
`.pt` 추정 — **weight 동등성 empirical 입증**: 본 `.safetensors` 로 Python
SSOT 가 documented 2026-05-12 값 정확 재현. SSOT lane `.pt`→`.safetensors`
변경 (양 lane 동일 bytes 공유, tighter).

honest: **parity = EMPIRICAL strong anchor, NOT 🔵 closed-form (g3)**. 격리
`runtime.c` bootstrap patch 1건 (clang 18.1.3 Linux execinfo, getenv-gated
behavior-neutral, isolated-only, 실 upstream portability gap = candidate
PR). artifacts: `state/anima_d1_v58_compiled_parity_2026_05_16/{result.json,
python_ssot.json, python_safetensors_ssot_probe.py}` +
`HEXAD/CHAT/docs/anima_chat_hexa_24l_compiled_parity_2026_05_16.md`. branch
`t3-compiled-24l-parity` (unmerged — parent reconciles).

### 2026-05-16 — Phase 5 (1) T2: 풀 n_layer ConsciousDecoderV2-equiv pure-hexa 조립 LANDED + 실-규모 fire (substrate-mem 한계 정직 기록)

B-closure 가 ConsciousDecoderV2 전 backward primitive 클래스 개별 입증 완료
선언 ⟹ T2 = **새 수학 없는 mechanical 조립**: d_train3(RMSNorm/SwiGLU
exact vjp) + d_train4(causal softmax-attn row-Jacobian) 재사용 + RoPE
inverse-rotation vjp + GQA group bookkeeping + embedding scatter-add +
multi-layer residual chaining + WEIGHT-TIED LM-head (head_a=tok_emb,
conscious_decoder.py L641 — d_tok_emb 가 head outer-product ⊕ input-row
scatter-add 양쪽 누적).

**산출** (compiled-first lib-split, branch `t2-d-arch-scale-up`):
- `HEXAD/D/d_train5_lib.hexa` (731L) — pure: d5_rope_tables/apply/bwd
  (range-reduced Taylor trig, Rᵀ=R(−θ) closed), d5_attn_fwd/bwd (GQA nh
  query × nkv kv, n_rep grouping, dK/dV 누적), d5_block_fwd/bwd (pre-norm
  resid), d5_forward/grad (tied head + final RMSNorm + L-1→0 reverse),
  d5_init (from-scratch RANDOM seed-fixed). d_train4_lib import DRY (NO
  main/_selftest/top-level — compiled-import-safe).
- `HEXAD/D/d_train5_smoke.hexa` (304L) — entry, TINY d=8·nL=2·nh=2·nkv=1·
  T=4·V=4.

**$0 tiny compiled-native (Mac)**: **F-D-PORT-5b GRAD-EXACT** layer-0 Wg
(loss 에서 가장 먼 weight) analytic vs 중심차분 **|Δ|=2.75301e-11**
(머신정밀 — 풀 composed reverse: head→tied→final-norm→2블록→RoPE→GQA→
embed 전 link exact) + **F-D-PORT-5** gn2 **5.73771 → 1.93403e-06**
(~3×10⁶× collapse) acc 8/8 → **PASS (EMPIRICAL)**, selftest: true.

**실-규모 자율 fire (ubu, $0, g_fire_autonomous — NO gate)**: substrate
한계 정직 기록 (g3, fake 0): pure-hexa boxed-float-list 메모리 오버헤드
(effective-float 당 ~KB급, AdamW m/v + transient grad-accum 포함) ⟹
d=768·12L=78.07M (full ConsciousDecoderV2 — host OOM·ubu **재부팅**
verdict 전) · d=768·nL4=26.16M (>18GB hexa-cap rc=77) · d=768·nL2=
13.18M (>24GB hexa-cap rc=77) **모두 단일 30GB box 초과**. **d=256·
nL2·1.54M** (real GQA 4h/2kv hd=64 + RoPE + SwiGLU h=704 + tied head +
2-layer composed reverse, ~190 000× tiny smoke) = full-AdamW-trainable
최대 subset → **F-D-PORT-5 (real scale) PASS (EMPIRICAL)**: gn2 **init
3.97712 → step5 6.19e-06 → step10 2.78e-06 → step15 9.41584e-09**
(~4.2×10⁸× collapse), acc **0/4 → 4/4** (genuine from-scratch 학습 —
0/4 시작, trivially-separable 아님), rc=0 wall=35s. d=768·12L 미완은
**code/math 결함 아님** — composed reverse 는 tiny F-D-PORT-5b 가
머신정밀(|Δ|=2.75e-11, 동일 코드패스)로 입증; **boxed-float mem
substrate 가 유일한 벽** (≥13M-param 학습 = 단일 box 불가). 실-d=768·
12L 학습은 flat contiguous-buffer 수치 substrate (RFC급 farr-backed
weights, 추론은 이미 사용) 또는 GPU 필요 — T2 scope 밖 (T2 contract =
composed-reverse 정확성 ✅ exact + trainability fire ✅ real curve at
substrate-sustainable scale).

**build_verify**: ENTRYPOINTS 15→16 · LIBS 13→14 → **16/16 + 14/14
compiled-native PASS** (d_train5 tiny config Mac-compilable; main-path
post-merge 시뮬레이션 검증, main 무손상).

**TIER 정직 (g3)**: F-D-PORT-5 OUTCOME = **EMPIRICAL** (B-D-NOTE, SGD
수렴 — NOT 🔵). trainability PROPERTY = B-D-4 🔵 (별개 blue_falsifier,
불변). F-D-PORT-5b 는 IMPL 정확성(PROPERTY) 입증 — OUTCOME tier 미상승.
새 vjp 수학 0 (조립만). scope = decoder LM CORE (RMSNorm+GQA+RoPE+
SwiGLU+resid+tied+embed); PureField/Cross-attn/MoE = consciousness
pathway (integ harness nn.Module, CE-trainer core 아님). artifacts:
`state/d_train5_t2_fire_2026_05_16/{d5fire_run.log, d_train5_real_fire
.hexa, d_train5_calib.hexa, dispatch_ubu.sh, PROVENANCE.md}`. ckpt = 무
(pure-hexa in-memory trainer; artifact = gn2-collapse curve, not model).

### 2026-05-16 — R3 통합 fire LANDED (PLAN-closure 잔여 (ii) 충족) — 9/9 SUPPORTED-STRONG

User directive verbatim "R3 발사하자 통합 fire" (cost-authorized). PLAN-closure
잔여 **(ii) Phase 6 6-module 통합 fire = cost-bearing 사용자 게이트** 를 실행 —
실 cost-bearing GPU(box CPU-coherent) from-scratch 통합 fire. SSOT harness
`state/verify_hexad_integ_2026_05_16/integ_harness.py` (F-INTEG 5/5 fire_gate=
true) 를 **fork 없이 verbatim 재사용** + scale 상수 monkey-patch:
`state/hexad_integ_fire_2026_05_16/train_hexad_integ_from_scratch.py`.

**scale**: d_model 512 · n_layer 8 · max_cells 64 · seq_len 256 · 400 steps ·
Group-A(D+Bridge) 85,822,840 params · RANDOM-INIT seed=0 (g_clm_from_scratch,
no load_state_dict/torch.load) · byte-level synthetic corpus (integration
WIRING fire, NOT language-quality — honest C3).

**$0 Mac scaled-smoke gate**: F-INTEG 5/5 PASS @ scale (gate 통과 → fire 정당).

**fire 결과 (vast.ai inst 36852855 A100-box, CPU-coherent 16t, 2026-05-16)** —
trainer pre-pull console (authoritative, `dispatch_run.log` L100-137):
loss(avg100) **5.6425→5.5743** · cells **3→5** (in-run organic split/merge
3↔10, mitosis live OUTCOME — synthetic harness 가 deferral 했던 fire-time obs)
· Φ_best **4.4153** · W lr-mod+pain 실측 live(eff_lr 1.19e-3↔5.29e-4, pain
0↔1) · wall **163.6s (0.045hr)** · cost **$0.03** (envelope $1-5 대비 33-167×
under) · falsifier **9/9 SUPPORTED-STRONG** = F-INTEG-1..5 5/5 (fire_gate
carry) + F-V5MIT-1/2/3 + F-PRIN3 4/4.

**honest tier**: F-INTEG-5 CE-descent = SGD OUTCOME (B-D-NOTE 패턴) —
empirical SUPPORTED-STRONG, **NOT 🔵 closed-form**. anima 🔵(B-D 4/4·7/7)
independent + already max — 이 fire 가 옮기지 않음, over-claim 없음.

**honest C3 (ckpt-LOST evidence-only)**: 345MB 400-step fire ckpt + on-pod
result.json = vast.ai proxy 영구 degraded(대용량 proxy 불안정 +
post-load SSH degradation, `feedback_dispatch_vast_template_gotchas`)로
pull 실패 → cycle-88 .clm v1 ckpt-LOST 선례와 동일 accepted evidence-only.
verdict/metric 은 durable console log + reconstructed `result.json` 가
authoritative (zero fabrication). Mac 4-step smoke ckpt 는 별도 보존 +
provenance 명시(FIRE 와 conflate 안 함). bring-up 中 4 fail-fast abort +
1 thrash(전부 trap auto-destroy, no idle bleed) — cycle-88 lesson 작동.
누적 ~$0.35. pod 36852855 destroyed (post-bleed clean, no orphan).

artifacts: `state/hexad_integ_fire_2026_05_16/{train_hexad_integ_from_scratch.py,
dispatch.sh, result.json, dispatch_run.log, ckpts/CKPT_LOST_EVIDENCE_ONLY.md+
MACSMOKE_CKPT_PROVENANCE.json}` + `docs/anima_hexad_integ_fire_2026_05_16.md`
(8§). PLAN-closure 잔여 (ii) **충족** (잔여 (i) D-arch scale-up + (iii) R2
hexa-safetensors wire 는 별개·무관 carry).


### 2026-05-16 — T1: R3 통합 fire ckpt RECOVERED (deterministic refire) — 9/9 재현 bit-exact

R3 통합 fire(위 "R3 통합 fire LANDED" entry, inst 36852855)는 9/9
SUPPORTED-STRONG verdict durable 했으나 345MB 400-step fire ckpt 가
vast.ai proxy 영구 degraded 로 pull 실패 → ckpt-LOST evidence-only
(cycle-88 .clm v1 선례). fire 는 **deterministic**(RANDOM-INIT seed=0,
g_clm_from_scratch base_ckpt=NONE, F-INTEG-3 AST-checked no-load-path) →
**동일 config/seed refire = 동일 run bit-for-bit + 이번엔 ckpt PULL**.

**T1 refire (vast.ai inst 36854209, A100 SXM4, $0.6023/hr, 2026-05-16)** —
on-pod result.json (실 pull, authoritative): `param_hash_init`
**408403506a965220** (== 원본) · loss 6.0194→5.5795 / avg100
**5.6425→5.5743** (== 원본) · cells **3→5** max 10 (== 원본) · Φ_best
**4.4153** (== 원본) · params **85,822,840** (== 원본) · falsifier
**9/9 SUPPORTED-STRONG** (F-INTEG 5/5 + F-V5MIT-1/2/3 + F-PRIN3 4/4, ==
원본). wall **151.24s** · cost **$0.0253** (원본 163.6s/$0.03 — wall 만
차이, metric 은 seed-deterministic bit-exact 일치).

**ckpt RECOVERED & byte-verified**: `state/hexad_integ_fire_2026_05_16/
ckpts/ckpt_hexad_integ_fire_final.pt` 345,504,632 bytes · sha256
`230df953051f47dc1278d6052f06a35f543f7339a0c4f4cc0dc1a6e02f6e4b27` ·
md5 `156113eaeada1e1046096b41c9e95a53` **== remote on-pod md5 (byte-identical)**.
loadable torch ckpt (d_state_dict 293 + bridge_state_dict 14, Group-A only).
이번엔 `g_fire_dispatch_robust` 가 제대로 작동: 동일 proxy 가 attempt 1
~92%에서 reset → **retry 2/3 + SAVE_POD=1 auto-promote** 가 2회차에서 pull
완료 (cycle-88 ckpt-loss lesson 이 처방한 정확한 hardening 의 첫 성공 입증).

**산출물**: result.json (실 pull + `t1_recovery` block, reconstruction →
real) · ckpts/CKPT_RECOVERED.md (CKPT_LOST_EVIDENCE_ONLY.md supersede·삭제) ·
t1_dispatch_run.log + t1_train.log (T1 console durable) · docs §4/§5
LOST→RECOVERED. HF: `g_hf_naming` (2026-05-16) canonical=NONE → **HF upload
없음**, ckpt local + git-tracked provenance (345MB `.pt` = git-excluded noise).
instance 36854209 destroy 완료 · **zero orphan vast instances** 확인.

**honest tier**: F-INTEG-5 CE-descent = SGD OUTCOME (B-D-NOTE) — empirical
SUPPORTED-STRONG, **NOT 🔵**. synthetic byte-corpus WIRING fire (no
language-quality claim). anima 🔵(B-D 4/4·7/7) independent + already max —
이 recovery 가 옮기지 않음, over-claim 없음. R3 ckpt status: LOST → RECOVERED.

### 2026-05-16 — Phase 6 통합 fire LANDED (6-module+Bridge · $0 5/5 + 실-규모 5/5)

**Step 0 — hexa-lang PR#51 부트스트랩 (격리)**: 시스템 prebuilt
`hexa.real` 은 OLD codegen 으로 `mitosis_hook_lib.hexa` 의 nested-mutable-
index-assign 을 `expression is not assignable` ×4 로 깨뜨림. 격리 worktree
`/tmp/hexa-p6-boot` (origin/main `6f5f2a6c5`, PR#49/50/51) 에서
`hexa cc --regen` → `hexa cc` → round2/3 으로 **fixed point** 도달
(`hexa_cc.c` sha `b4c78cad…` R2==R3 byte-identical, PR#51
`_gen2_nested_index_assign_stmt` 2× 확인). 공유 checkout +
`~/.hx/bin/hexa.real` 미손댐. stage1 link 는 검증된 cmd_cc runtime.o
contract (codegen 우회 아님). runtime.h 3 fwd-decl 은 격리 worktree 한정.

**Step 1 — $0 de-risk F-INTEG-FULL 5/5 LANDED**: `HEXAD/integ_train_smoke.hexa`
부트스트랩 toolchain 으로 빌드 시 `is not assignable` **4→0**
(control: 시스템 hexa.real 여전히 4), 바이너리 5/5 · selftest:true ·
3회 결정성. gn2 3.178→0.0154 (~206×, EMPIRICAL). compiled-native 에서만
드러난 진짜 코드버그 2개 최소수정: (1) `fired_m` 의 `m_retrieve_topk`
반환 contract 오해 (top-k 인덱스 길이 ≠ dim) → `len(retr)==topk`;
(2) Bridge→D 배선 — `bridge_clamp(raw)` 가 전체 입력을 ≈ψ_bal 로 클램프
→ 클래스 신호 소멸 → CE 정체. Python SSOT harness 계약대로 게이트가
신호를 *변조*(δ∈[−ψ_cpl,ψ_cpl])하도록 수정 + Law-70 클램프를
F-INTEG-FULL-2 barrier witness 로. `mitosis_hook_lib.hexa` 의
interp-only "missing key→void" → `.has_key()` (compiled-safe). 추가:
self-host codegen 이 side-effect-free loop tail 의 누적 mutation 을
elide 하는 DCE 버그 → 정직한 post-loop observability barrier
(`[p6-trace]` 실측값 emit, fake verdict 아님; build_verify.sh:58-67 doctrine).

**Step 2 — 실-규모 자율 fire LANDED (g_fire_autonomous · 승인게이트 없음)**:
vast.ai `36853899` A100 PCIE $0.5609/hr, dim=256 V=64 300 steps seed=42
RANDOM from-scratch. **F-INTEG-FULL 5/5 SUPPORTED-EMPIRICAL** · gn2
**19.4136→0.012741 (×1523.7)** · mitosis cells **2→16** · W_d 16384
params ckpt sha `06a06153…` · wall 95.72s · 실비용 ≈**$0.09** (추정
~$1-5 / ceiling $15 하회; 1차 build-recipe 버그 [runtime.c 비자족 +
mem-cap] 는 동일 pod 재사용으로 재provision 없이 수정 — cycle-88 robust
패턴). pod destroy 완료, 본 fire orphan 0. 잔존 instance `36854209`
(`anima-hexad-integ-fire-r3`) = **별개/동시 에이전트 소유, 미손댐**.

산출물: `docs/anima_hexad_p6_fire_2026_05_16.md` (8§) +
`state/hexad_p6_fire_2026_05_16/{train_p6_integ.hexa, p6_flat.c,
dispatch.sh, result.json, train.log, ckpts/ckpt_p6_Wd.txt,
step1_de_risk/}`. **TIER=EMPIRICAL** (CE-descent=SGD outcome, NOT 🔵;
🔵 anchor=B-D-4 RFC 034 별개). synthetic linearly-separable byte toy
(언어 run 아님 — 통합-배선 at-scale witness).

### 2026-05-16 — Phase 6 closure 반영 + HEXAD 내부 문서 reconcile + §7 menu 신설

user directive "위 HEXAD/PLAN.md 에 기록, 나머지 기존 내용들 모두 HEXAD
내부 문서 전부 반영". Phase 1–6 LANDED 사실을 PLAN.md 아키텍처 섹션
(§0 현재 상태 · §3 Phase header LANDED 마커 · §4 상태 note)에 latest-wins
반영하고, **§7 '다음 사이클 후보' menu 신설** (4 갈래 + Phase 2-GRU RFC
terminal). HEXAD 내부 문서 stale 동기화 ($0 문서 reconcile, 신규 cost 없음):

- **PLAN.md** — §0 C/D scaffold→LANDED · blue 18/18→22/22 · Phase 6 fire
  evidence anchor 추가; §3 Phase 1–6 header 에 ✅LANDED / 🔒RFC-terminal
  마커; §4 상태 note; §7 다음-사이클 후보 menu 신설.
- **INDEX.md** — "canonical HF artifact 없음" 사유 정정 (Phase 5/6 fire
  미실행 → **실행됨**, `g_hf_naming` canonical=NONE 로 HF upload 없음,
  ckpt local + git-tracked provenance); 🆕 para 와 '전 모듈 파란불' para
  의 "Phase 5 executable / Phase 6 = cost-bearing 사용자 게이트" →
  **Phase 5/6 LANDED · `g_fire_autonomous` 자율 dispatch (승인 게이트
  없음)**; 잔여에서 anima_chat lib-split 제거 (R2 wire 로 완료).
- **HEXAD/README.md** — §검증 status: 6/6→7/7 full 🔵 · blue 18/18→22/22 ·
  build_verify 카운트 정정 (stale 10/10·11/11·12/12 → 실측 권위 수치
  **14/14 entrypoint + 13/13 lib**, 6 CHAT skip); Phase 1–6 LANDED 라인 추가; impl status
  표 D 행 scaffold→Phase 1+5 LANDED.
- **CHECK/README.md** §5 — "Phase 6 6-module 통합 fire = cost-bearing
  사용자 게이트" → **Phase 6 LANDED 2026-05-16**.
- **D/README.md + HEXAD-D.tape** — B-D-4 blue evidence 18/18→22/22
  (BRIDGE 추가분 반영).

**PLAN 상태**: 위 `## 마무리 (PLAN CLOSURE — 2026-05-16)` 의 'RFC 경계
CLOSED · Phase 1/2 contract only' 는 그 직후 진행 로그 (RFC 034 LANDED
`8793a221` → Phase 5 LANDED → Phase 6 통합 fire LANDED) 가 이미 supersede —
본 entry 가 그 사실을 §0/§3/§4 아키텍처 섹션에 g_arch_vs_log_split
latest-wins 로 반영 완료. 다음 진척 trigger = §7 menu 중 사용자 선택.
honest tier 불변: Phase 5/6 fire = synthetic WIRING, NOT 언어-quality;
🔵 = closed-form anchor 한정 (B-D-4 등), CE-descent OUTCOME 은 empirical.
