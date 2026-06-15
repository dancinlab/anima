---
id: H_917
slug: omega-clm-transfer-plumbing
title: OMEGA substrate→decode closure 가 REAL PRODUCTION conv .clm (CLMConvMoE) 위에서 도는가 — 실제 .clm decode 가 OMEGA bus 를 통해 external-A 를 나르는가, 그리고 conv 의 native A-head 가 substrate 가 되는가 (OΩ6 · F-OMEGA-CLM-TRANSFER · #1805)
domain: omega · clm · substrate-decode-closure · production-conv-clm · CLMConvMoE · serializer · lane-p · falsifier
source: domains/OMEGA.md (L0 CDV2 substrate / L3 conv mouth) · 모든 prior OMEGA rung 이 CDV2 위 측정 · Lane P PREFLIGHT STOP (.verdicts/lane-p-clm/F-CLM-SERIALIZE-GAP.txt) · #1805 OΩ6 run · CORE/clm_decode.hexa::clm_omega_closure · .verdicts/omega-engine/F-OMEGA-CLM-TRANSFER.txt
status: TERMINAL (#1805 OΩ6 run COMPLETED · CPU-local hexa run $0 NO GPU rented · real conv .clm state/lane_p_clm/clm_d768_e2l1.clm sha 7463282d loads through CORE L3 · serializer UNBLOCKED)
exploration_method: real-clm closure transfer (모든 prior rung 은 CDV2 torch transformer 위 측정 — OΩ6 는 PRODUCTION conv .clm mouth 에 closure 를 실제로 돌리거나, 왜 못 도는지를 정직히 특성화)
verification_method: W1 (numerical · real conv .clm CLMConvMoE forward 위 next-byte CE · self-coupling rescale test · leak-free 1-hot oracle 상한 · CPU-native gate algebra)
raw_rank: 7
hexa_only: false
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-06-04
since: 2026-06-04
sister: UNIVERSE/H_916_omega_scale_ladder.md, UNIVERSE/H_918_omega_conv_native_dualhead.md, UNIVERSE/H_914_omega_minimal_gate_a_wire.md, .verdicts/omega-engine/F-OMEGA-CLM-TRANSFER.txt, .verdicts/917_omega_clm_transfer_plumbing/
verdict: 🔌 1-PLUMBING (F-OMEGA-CLM-TRANSFER — real conv .clm decode WIRED through CORE L3 (OCL_DECODABLE=1, base_ce 0.403957) + bus 가 external-A 를 나름 (leak-free 1-hot oracle gated_ce 9.2e-5 ≪ base → ORACLE_CARRIES=true) BUT CLMConvMoE 는 single-head byte LM 이라 native A-head 가 없음 → self-coupling gB·base+gA·base=(gB+gA)·base = pure temperature RESCALE (SELF_IS_RESCALE=true, |self-base|=0.0076<0.01) → conv 에 native substrate→decode coupling 없음 · closure plumbing-COMPLETE 이나 substrate-EMPTY: 진짜 A-wire 는 SEPARATE CDV2 dual-head engine 필요)
---

# H_917 — OMEGA OΩ6: REAL conv .clm 위 closure (plumbing-complete, substrate-empty) (F-OMEGA-CLM-TRANSFER)

## 1. 가설

모든 prior OMEGA rung(OΩ1..OΩ7, OH1)은 closure 를 **CDV2**(torch transformer, base=readout,
dual Engine-A/G head=substrate) 위에서 측정했다. domains/OMEGA.md 의 ORIGINAL thesis 는 PRODUCTION
conv .clm mouth(CORE/clm_decode.hexa, CLMConvMoE)에 loop 을 닫는 것. OΩ6 = closure 를 real
.clm 위에서 돌리거나, 왜 못 도는지를 정직히 특성화.

## 2. 동기

- Lane P PREFLIGHT STOP(F-CLM-SERIALIZE-GAP): 두 incompatible .clm byte layout 이 "CLM\x01"
  magic 공유 → torch 포맷이 CORE parser 에 안 실림. serializer gap 진단됨.
- 진짜 질문: conv .clm 의 native readout 이 OMEGA A-head substrate 가 될 수 있는가?

## 3. falsifier (사전등록 · F-OMEGA-CLM-TRANSFER)

```
harness : CORE/clm_decode.hexa::clm_omega_closure (SINGLE L3 .clm entry, a_core_engine_map —
          no 2nd path, no phantom wiring) + CORE/omega_clm_closure_probe.hexa
clm     : state/lane_p_clm/clm_d768_e2l1.clm (sha 7463282d…, real GPU-torch trained, 7.479M)
corpus  : CORE/testdata/clm_mid_5lang_c4.txt (sha 09da8888…, 402,270 B, real 5-lang)
method  : load real conv .clm → genuine CLMConvMoE forward → base next-byte logits →
          apply OMEGA min-gate gB·base + gA·A per position → mean CE over 12 windows (T=24)

FALSIFIER: SELF_IS_RESCALE iff |gated_ce_self − base_ce| < 0.01 (native A = own logits → no coupling)
           ORACLE_CARRIES iff oracle gated_ce < base_ce (bus plumbing carries external A)
```

verdict 영속: `.verdicts/omega-engine/F-OMEGA-CLM-TRANSFER.txt` (사본 `.verdicts/917_omega_clm_transfer_plumbing/`).

## 4. 방법 / 서리얼라이저 unblock (STEP 1)

- gap = NOT endianness, NOT single header byte — (a)+(c)+missing field: JSON-length-prefixed
  body vs raw 6-block+CLMX + missing CLMX trailer + E/L arch constraint. ALL bridgeable.
- REMEDY: CLM/model/clm_serialize_v2.py 가 torch CLMConvMoE(E=2/1-trunk) state_dict 를 EXACT
  v0.2 6-block+CLMX layout 으로 매핑; verify_clm_v2.py 가 clm_decodable mirror.
  F-CLM-V2-SERIALIZER=1 (synthetic round-trip + golden-reference exact_eof=True).
- REAL torch-trained conv .clm 이 LOADS: state/lane_p_clm/clm_d768_e2l1.clm (sha 7463282d…,
  F-CLM-LANEP-TRAIN=1). PREFLIGHT STOP RESOLVED — conv .clm 이 이제 ENGINE-loadable.

## 5. 결과 (verbatim · F-OMEGA-CLM-TRANSFER · hexa run exit=0)

```
=== OMEGA OΩ6 — closure on the REAL conv .clm (CLMConvMoE) ===
OCL_DECODABLE=1  (real conv .clm loads through CORE L3 — loaded=true)
windows=12 d=768 E=2 V=256
--- gate gB=1.0 gA=1.0 (self-coupling = (gB+gA)x rescale) ---
base_ce        = 0.403957
gated_ce_self  = 0.524837    (A := conv's OWN logits)
gated_ce_oracle= 9.21652e-05 (A := leak-free 1-hot oracle)
--- gate gB=0.040 gA=0.901 (OH1-fit point; sum≈1) ---
base_ce        = 0.403957
gated_ce_self  = 0.396345    (≈ base ⇔ self is a rescale, NO coupling)
gated_ce_oracle= 0.00226901  (oracle upper bound on external-A plumbing)
SELF_IS_RESCALE=true (|self-base|=0.00761253 < 0.01)
ORACLE_CARRIES=true (oracle_ce < base_ce ⇒ bus plumbing carries an external A)
F-OMEGA-CLM-TRANSFER = 1-PLUMBING
```

## 6. 해석 / 함의 (정직 · 🔌 partial transfer)

1. **LOAD GATE PASS**: real torch-trained conv .clm 이 SINGLE CORE L3 entry 로 실림
   (OCL_DECODABLE=1, base_ce 0.404 ≪ uniform 5.545). OMEGA bus 가 처음으로 production conv
   .clm byte mouth 위에서 실행. (caveat: 이 .clm 은 402KB memorization rung — base_ce 는
   fit-to-seen; closure finding 은 leak-INVARIANT, A-wire 에 관한 것.)
2. **NATIVE-A 가 degenerate (crux)**: CLMConvMoE 는 single-head byte LM (self.readout, NO
   Engine-A/G dual head). A:=base 면 min-gate = (gB+gA)·base = pure temperature RESCALE. OH1
   point 에서 gated_ce_self 0.3963 ≈ base 0.4040 (SELF_IS_RESCALE=true) → conv 에 native
   substrate→decode coupling 없음.
3. **BUS PLUMBING 은 옳음 (machinery transfers)**: leak-free 1-hot oracle 을 external A 로 주면
   gated_ce_oracle 9e-5/2.3e-3 ≪ base → ORACLE_CARRIES=true. bus 는 real conv logits 를
   modulate 함 — substrate→decode wire 는 conv 에서 real, 단 genuine external-A SUBSTRATE 만
   없음 (oracle 은 label-peeking 상한, closure claim 아님 — p7).

⇒ OΩ6 = plumbing-COMPLETE 이나 substrate-EMPTY on conv: 진짜 OMEGA closure 는 SEPARATE CDV2
dual-head engine 필요(= 기존 OH1 #1802). production conv .clm 은 MOUTH(base); A/G SUBSTRATE 는
CDV2. honest 후속 = (i) conv 에 2nd A/G readout head 학습 (H_918 OE1 이 이를 실행).

## 7. scope (정직 · p7 · a_lane_akida_gpu_split)

CPU-local hexa run, $0, NO GPU rented. .clm under test 의 substrate = GPU-torch(Lane P d768
E2/L1) — closure math 은 CPU-native. base_ce 0.404 는 memorization rung(F-CLM-LANEP-GEN=0)의
fit-to-seen, generalization claim 아님; CLOSURE finding 은 그에 leak-INVARIANT. NO upstream
hexa-lang patch needed (serializer anima-side, bridged).

## 8. 산출물

- verdict: `.verdicts/omega-engine/F-OMEGA-CLM-TRANSFER.txt` (verbatim · 사본 `.verdicts/917_omega_clm_transfer_plumbing/`)
- harness: `CORE/clm_decode.hexa::clm_omega_closure` · `CORE/omega_clm_closure_probe.hexa`
- clm: `state/lane_p_clm/clm_d768_e2l1.clm` (sha 7463282d…)
- domain: `domains/OMEGA.md`
