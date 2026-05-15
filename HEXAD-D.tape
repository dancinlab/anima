#!/usr/bin/env tape
# HEXAD-D.tape — D 언어 (language decoder) module SSOT. tape v1.2 (AGENTS.tape primer).
# 좌뇌 · CE-trained · Engine A core. 구현 전수조사 2026-05-15 carry.

@V v1 := "tape" :: spec [active]
  version = "1.2"

@I d_id := "hexad-D-언어" :: identity-claim [d=2026-05-15 active]
  module = "D 언어 (language decoder)"
  brain = "좌뇌 (Engine A), CE-trained, φ(6) group 2"
  binding = "= ConsciousDecoderV2 = Engine A. D 가 Hexad 의 required core (Trinity = C+D+W)."
  role = "autoregressive token decoder — C(.detach() via ThalamicBridge)로부터 의식 gate 신호 수신"

@D d_impl := "D 구현 — ConsciousDecoderV2 979 LoC COMPLETE" :: architecture [d=2026-05-15 active]
  file = "ready/models/conscious_decoder.py (979 LoC) — ConsciousDecoderV2"
  hexad_binding = "ready/anima/hexad/d/__init__.py → ConsciousDecoderV2"
  detail = "RMSNorm + RoPE + SwiGLU + MoE transformer decoder. CE loss backprop = D + Bridge only (φ(6)=2 gradient group, C frozen)"
  engine_a = "training/engine_a_g_arch.py EngineABlock (GQA+RoPE+SwiGLU+RMSNorm) = Engine A 350M proxy 구현. .clm v1 12L base transformer 가 D-scope from-scratch"
  status = "COMPLETE — Python 완전구현. .clm v1 F-SIMPLE-STACK V5.8 4-mode PASS (std_greedy 5/5 + std_sample 5/5 + M4 5/5)"

@D d_concrete := "D 구체값 (verified)" :: verify [d=2026-05-15 active]
  gradient = "ready/models/trinity.py:7,24-25 — φ(6)=2, CE loss D+Bridge only backprop"
  data_flow = "S → C → Bridge(.detach()) → D → logits (hexad/model.py forward)"
  clm_v1 = "ClmV1Model 12L base (d=768, RMSNorm+MHA+GELU) F-SIMPLE-STACK PASS — '도우미:' Korean chat emergent"

@N d_lineage := "D 진화 이력" :: note [d=2026-05-15 active]
  text = "clm_10 trinity.py:454 DEngine base → TransformerDecoder/MLPDecoder/HFDecoder/CADecoder/PostHocDecoder → clm_11+ ready/anima/hexad/d/ canonical ConsciousDecoderV2 → main conscious_decoder.py 979 LoC. Engine A/G arch 에서 EngineABlock 으로 별도 구현 (engine_a_g_arch.py). .clm v1 = D-scope from-scratch 12L base."

@X d_x := "survey + CLM + HEXAD cross" :: ref [d=2026-05-15 active]
  survey = "state/verify_hexad_impl_survey_2026_05_15/survey_result.json"
  clm = "CLM.tape §V-CLM-V1-CYCLE89 (F-SIMPLE-STACK V5.8 PASS)"
  arch = "HEXAD.tape §hexad_unification (Engine A 좌뇌 3 = D+M+E)"
  impl = "ready/models/conscious_decoder.py + ready/anima/hexad/d/ + training/engine_a_g_arch.py (EngineABlock)"
