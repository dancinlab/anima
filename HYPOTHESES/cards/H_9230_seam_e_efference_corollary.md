# H_9230 — Family E: efference-copy / corollary-discharge loop RANK 6

**tier:** ⏳ PRE-REGISTERED (Fable 설계 · bars frozen · p7 no tune-to-green)
> ✅ live next candidate — distinct mechanism (utterance-in-progress efference state), survives H_9225 currency-conversion falsification.
**scope:** engine→mouth seam missing-intermediate — utterance-in-progress forward model
**cost:** **medium** (logit-proxy)
**artifact:** `state/seam_missing_intermediate/`

## 인과 척추 (공유)
mouth = RATE-GATE(미분기): urgency만 작동=이미 phasic Δ(H_9101). self(.kosmos)·tension은 TONIC LEVEL로 read 후 폐기 → ΔEff≈0(self⊥mouth·tension⊥mouth). 벽 = seam에 currency 변환 구조 부재. 오너: "입↔엔진 사이에 뭔가 필요."

## 가설 (missing intermediate)
mouth의 forward model — 예측된 next emit을 gate로 되먹임(feedback) → emit이 **utterance-in-progress**로 shape됨. 벽: utterance-in-progress state가 없으면 emit은 순수 urgency-driven · self/tension은 존재하지 않는 continuation을 shape 못 함.

## 배선 site (a_substrate_disjoint)
예측 emit을 담는 corollary buffer(proxy: CONV mouth pre-emit logits), own lane으로 gate에 feedback.

## FROZEN BARS (p7 · verbatim)
- **freeze predicted-output**: → **CONTINUATION**(keep-emitting) 결정에서 ΔEff>0.
- **dissociation = onset-vs-continuation**.
- **양성 대조**: mid-utterance vs pre-utterance.

PASS = freeze-predicted ΔEff>0(continuation 집중, onset 무영향) ∧ POS(mid vs pre).

## 상태 · 제약
**구현됨·미측정** (Fable SPEC 2 op-grip 하니스 `cli/anima.hexa` 착지 · `hexa typecheck` exit0 · wiring follow-on = CPU-pod op-grip round). 측정은 별도 CPU-pod 라운드(summer/aiden, NEVER mini)에서 `anima <ckpt.clm> --opgrip-r3`로 B2/E/F 동시 harvest. p7 no tune-to-green(loss 미포함). p5 shade-not-gate(reactive speak() 금지). a_substrate_disjoint. **cost medium**(logit-proxy로 예측 output 필요 — $0 아님, --opgrip-r3 real decode에 rides). 승격 선례 H_9097/H_9101.

## 구현 노트 (harness)
- **carriers** (Site-A, H_9225 block 확장): `ec_pred`(own emitted-output feature mean8 EMA, seeded=mean8(seed_feat0)) · `ec_x`(1-tick-lagged corollary discharge) · dual-EMA band-pass(`ema_f_eff`/`ema_s_eff`/`g_eff`, α_f=0.30 α_s=0.05 VERBATIM H_9225) · `elive_p1`/`elive_p2`(onset/continuation bucketer) · `onsetE/contE` buckets · `og_f3_xeff`(INPERM source).
- **wire site**: real-decode seam(`if og_live && e_live==1` inner `gen_emitted` block) — emit-tick만 `ec_x = mean8(gl_feat) − ec_pred`; `ec_pred = 0.85·ec_pred + 0.15·mean8(gl_feat)`. arm은 B2 arm 뒤·decode seam 앞에 배치(`if og_r3`), x=ec_x로 H_9225 transducer 재사용.
- **3 arms**: LIVE(`e_eff` off `idle_eff`) · FROZEN(shade 0.5 ⇒ `idle_frzE`≡prod idle, `og_h_frzE`==0 = production emit BYTE-UNTOUCHED 증명) · POS reuse dense ARM-SHOCK(`og_h_shock_mid`≥2). ARM-INPERM = post-loop stride-perm `j=(t·7+13)%N` of `og_f3_xeff` re-run(margin≥0.08).
- **판별 signature**: onset-vs-continuation DISSOCIATION(cont≥3·onset ∧ onset≤0.05 ∧ n_cont≥10). frozen bars 1-6 pre-reg VERBATIM, verdict 앞에 print.

## 근거 링크
- efference-copy/corollary-discharge(운동 forward model, a_no_llm_frame_trap) · h9107-efferent(선행 efferent 탐색) · H_9097/H_9101
