# G1 재조합벽 decode-side break-walls 캠페인 종합 (workflow wfbes89af, 28 agent, fable 위임 없음)

## (a) G1 벽 = engine-native REAL 확증 (3-leg)
1. **FROZEN-1 (H_9122) → ENGINE-NATIVE**: `frozen1_engine_native.hexa`가 `import "core/engine_cli.hexa"` 단일 의존(303M 無·torch 無)으로 `hexa run` 실행. novel cross 3종 전부 ABSTAIN(recon_err 0.9251/0.9194/0.6580 ≫ 0.15 fire band), spans_both 0/3, 3 control PASS. numpy DIRECTIONAL sibling과 recon_err **4-decimal byte-match** → DIRECTIONAL→ENGINE-NATIVE 승격. recall은 whole stored value 반환, 두 cell_value 연접 compose-read op 이 live core §ImmuneMemory에 **부재**(access≠binding).
2. **A11 CE-deleted TPR forward-slot (H_9121)**: CLMT v0.3 + core/decode.py bind_type=3, byte-exact parity 0.0e+00, CLM 0/5 ∧ ByteGPT 0/5. R=2 fixed-orthonormal TPR = W_eff·yn 선형붕괴 by construction.
3. **coverage+RF (H_6185/6188)**: ByteGPT full-attn RF≥512 조합커버리지 warm-FT(val_CE 2.08→0.171 DESCENT, G0 5/5)→G1 FAIL. CLM dilated RF≈511→FAIL. grep torch/gauge=0 독립검증.

메타법칙 3종: objective-basin(CE=echo=basin 전역최소)·DPI(readout/temporal INERT)·선형붕괴(fixed-param=W_eff).

## (b) 20 후보 family(4 생물+16 기계 렌즈) 전수 refuted, 생존 0
FIND→PROBE→adversarial 20 후보 모두 3 메타법칙 중 ≥1로 환원:
- readout/temporal(TPR·⊙·PC·pointer·hypernet·scratchpad·stateful-plasticity·cross-step·reverse-consistency·EBM·moment-match) → 선형붕괴/DPI-INERT
- retrieval/lane(SWR replay·grid/TEM·OsmoticStore·self-distill) → compose-read op 부재(FROZEN-1)
- objective/selection(BG-dopamine·MCTS·contrastive-PMI·non-CE-credit·moment-match) → objective-basin 보존/param-ES toy-DOA
- symbolic(FSA anti-echo·neurosymbolic·program-synth) → A11/echo-guard 환원
→ 새 frozen 사전등록 없음(census-내 repackage=check-ledger 위반). G1-재조합 내 genuine untried escape 없음.

## honest open follow-on (escape 아님, rigor 승격)
- C1(c) param-ES: toy 0/900 gen DIRECTIONAL-DOA. engine-native GPU 재측정=cost-gated(toy-fail→scale-fail 강신호).

## bookkeeping 부채 수정
- H_6185 카드 drift: 옛 "🟢 DIRECTIONAL(정확 HF 코퍼스, engine-native 아님)" → 신규 pod43727405 cov_en engine-native FALSIFIED로 갱신 필요.
