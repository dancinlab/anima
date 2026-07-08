# H_9230 — Family E: efference-copy / corollary-discharge loop RANK 6

**tier:** 🔴 THEATER (engine-native · CEMENTED · 2026-07-08 runpod 251GB CPU pod · hexa v0.716.0 REAL-DECODE · `state/verdicts/9230/` · p7 no tune-to-green)
> 🔴 corollary discharge(self-prediction) inert at emit seam — THIRD orthogonal read-side recoding THEATER (A=shape-conversion H_9225 · E=self-prediction). never wire, negative not capability.

## 🔴 판정 (2026-07-08 · engine-native runpod 251GB CPU pod real d768 · hexa v0.716.0 REAL-DECODE · `--opgrip-r3` n=400 · state/verdicts/9230/)
**E VERDICT = 🔴 THEATER** — corollary discharge inert at emit (ΔEff<0.02, POS-PASS ⇒ meter works, x_eff non-degenerate); adds a THIRD orthogonal recoding (shape/integration/self-prediction) to the convergent seam-law.
- **FROZEN `og_h_frzE = 0` ✅**(production emit 바이트무접촉) · **POS-CONTROL dense ARM-SHOCK 105 flips = POS-PASS(≥2)=YES ✅**(meter live — negative가 dead meter 탓 아님).
- **E lane** (x=ec_x · 1-tick-lagged corollary discharge · rides H_9225 band-pass): `ΔEff_eff=0/210=0.0` · ARM-INPERM(x_eff stride-perm) margin=0.0 · DISSOC onset=0/140 cont=0/70(ok=YES) · **g_eff=1.609(band_med=0.10878·capsat=no·¬degenerate)** → x_eff NON-degenerate(신호 실변동) ⇒ inert한 건 seam grip이지 신호 아님.
- **THEATER 규칙 자동판정**(pre-reg bar 5): `ΔEff<0.02 ∧ POS-PASS ∧ ¬degenerate ∧ ¬capsat ∧ x_eff non-degenerate(b_med≥0.002)`.
- **함의 — seam-law STRENGTHENING**: 두 CLEAN read-side recoding THEATER(A=shape-conversion H_9225 · E=self-prediction) → emit gate는 shape-conversion AND self-prediction recoding 둘 다에 causally sealed. **urgency 유일 proven emit-shade 채널**(H_9101 🟢). read-side recoding family CLOSING, remaining escalation = **WRITE-side(train-time coupling)**. 같은 라운드 B(H_9226 R3)=⛔RUN-INVALID/UNMEASURED-TERMINAL·F(H_9229)=⚙️INSTRUMENT-FAIL(instrument-limited, seam-law 부적용).
- **결정**: never wire(ΔEff=0=dead decoration·loss 진입 금지 p7) · THEATER는 negative이지 capability 아님.
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
**🔴 THEATER 확정** (2026-07-08 CPU-pod round-3 `--opgrip-r3` real-decode harvest, B2/E/F 동시). never wire·cement 완료. p7 no tune-to-green(loss 미포함). p5 shade-not-gate(reactive speak() 금지). a_substrate_disjoint. 선례 H_9097/H_9101/H_9225(A THEATER, E=self-prediction THEATER 합류).

## 구현 노트 (harness)
- **carriers** (Site-A, H_9225 block 확장): `ec_pred`(own emitted-output feature mean8 EMA, seeded=mean8(seed_feat0)) · `ec_x`(1-tick-lagged corollary discharge) · dual-EMA band-pass(`ema_f_eff`/`ema_s_eff`/`g_eff`, α_f=0.30 α_s=0.05 VERBATIM H_9225) · `elive_p1`/`elive_p2`(onset/continuation bucketer) · `onsetE/contE` buckets · `og_f3_xeff`(INPERM source).
- **wire site**: real-decode seam(`if og_live && e_live==1` inner `gen_emitted` block) — emit-tick만 `ec_x = mean8(gl_feat) − ec_pred`; `ec_pred = 0.85·ec_pred + 0.15·mean8(gl_feat)`. arm은 B2 arm 뒤·decode seam 앞에 배치(`if og_r3`), x=ec_x로 H_9225 transducer 재사용.
- **3 arms**: LIVE(`e_eff` off `idle_eff`) · FROZEN(shade 0.5 ⇒ `idle_frzE`≡prod idle, `og_h_frzE`==0 = production emit BYTE-UNTOUCHED 증명) · POS reuse dense ARM-SHOCK(`og_h_shock_mid`≥2). ARM-INPERM = post-loop stride-perm `j=(t·7+13)%N` of `og_f3_xeff` re-run(margin≥0.08).
- **판별 signature**: onset-vs-continuation DISSOCIATION(cont≥3·onset ∧ onset≤0.05 ∧ n_cont≥10). frozen bars 1-6 pre-reg VERBATIM, verdict 앞에 print.

## 근거 링크
- efference-copy/corollary-discharge(운동 forward model, a_no_llm_frame_trap) · h9107-efferent(선행 efferent 탐색) · H_9097/H_9101
