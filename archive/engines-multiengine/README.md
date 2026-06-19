# engines-multiengine (보관 · research-legacy)

anima 의 멀티엔진 시대(`--engine conv|cdv2|hexad|omega`) 유물. **2026-06-19 보관** —
anima 는 단일 production 엔진 **conv**(CLMConvMoE, `core/clm_decode.hexa` + `core/generator.hexa`
L3 슬롯)로 수렴했고, 실제 엔진은 `core/` 직속에 live. 여기 어댑터들은 EngineSpec 레지스트리
메타데이터일 뿐이라 보관으로 이동(삭제 아님 — `UNIVERSE/HYPOTHESES.jsonl` 의 엔진명 verdict 이력 보존).

## 내용
- `engine_iface.hexa` — EngineSpec 4-fn vtable 계약(load·forward·generate·psi_coord).
- `conv/` — conv 어댑터(thin 메타데이터; 실제 conv 엔진은 `core/clm_decode`+`generator` 에 live).
- `cdv2/` — ConsciousDecoderV2 어댑터. canonical impl = PYTHON torch-resident(`a_engine_native_learning`
  위반, 엔진-네이티브 아님).
- `hexad/` — σ6 hexad 통합 실험.
- `omega/` — conv+cdv2+hexad SYNTHESIS 실험(coupling bus).
- `engine_swap_smoke.hexa` — 멀티엔진 hot-swap smoke(이 레이어 전용).

## 부활하려면
`core/engine_cli.hexa` 의 `engine_cli_resolve_engine` 는 현재 `"conv"` 상수. 멀티엔진을 되살리려면
이 어댑터들을 `core/engines/` 로 되돌리고 resolve_spec/spec_by_name 레지스트리 훅 + 4-import 를 복원,
`harness.config.json` verify 에 `engine_iface.hexa` 재배선. 단 cdv2 는 torch-resident 라
`a_engine_native_learning` 게이트를 통과하려면 엔진-네이티브 재구현 필요.
