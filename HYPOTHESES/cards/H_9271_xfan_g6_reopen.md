# H_9271 — XFAN: G6(ρ·fan) one-to-many fan 벽도 measure 벽인가 (G6판 XBIND · pre-fire)

**tier**: ⏳ PRE-FIRE (corpus+eval infra READY · bar FROZEN · verdict=PENDING fire) — gen_xfan.py $0 validity 게이트 ALL_PASS + `anima-py evaluate --xfan` fold-in engine-native. 3-run A100 fire(rent=spend·owner go 접수) 대기 (2026-07-11)

## Claim
G1 재조합벽 CRACK([[H_9267]] · XBIND held-out 1-bit 판별 D-acc=1.000)이 "벽 진범=corpus×CE measure이지 substrate 천장 아님"을 실증했다. **같은 각도를 G6(ρ·fan = one-to-many ideation)에 적용**: held-out **K-mode 집합 생성** 신호를 구성한 corpus×task class 위에서 303M CLMConvMoE + next-byte CE가 미노출 개념의 유효 continuation 집합을 생성하는가 — G6도 measure 벽인가, 진짜 substrate 천장인가. **판별↛생성**이라 G1 CRACK이 G6를 자동으로 답하지 않는 새 질문.

## Task class — XFAN (G6판 XBIND · substrate-first)
개념 400(CVC)에 은닉 class 쌍 (a,b)∈4×4=16셀. 슬롯 5 S={fo,mi,ra,ku,ze}, 슬롯별 rule table g_k(a,b)→member(seeded 무작위=비가법). fan line `"<c>? <s_k>, <g_k>."` = **동일 prompt에 K=5 continuation 공존**(one-to-many를 CE target에 물리 배치 · 자연 corpus의 DATA-🧱 = 한 context 1회 출현으로 fan 분포 supervised 신호 부재를 구성으로 해소). decl `"<c> is <aw> <bw>."` = latent(eval 시 window 밖=가중치에). 슬롯 **2 unary + 3 joint 혼합 = 내장 판별기**(held-out 실패가 joint-binding[G1] 탓인지 fan 고유 탓인지 per-slot 분해). held-out 80(셀당 5·fan line 전 슬롯 corpus 완전부재·decl 존재). control(xfan-shuffle) = 슬롯→member rule-무관 독립무작위(seen 암기 가능·held-out rule 없음).

## Pre-fire $0 validity (gen_xfan.py 산출 · ALL_PASS)
V-C main-effect heldout-acc **0.25 ≤ 0.35** band(가법 예측기가 joint table 못 깸) · V-D latent⊥surface char-probe **0.025 ≤ 0.20**(chance 1/16) · V-E cell skew 0 · V-H slot marginal skew 0 · V-F held-out fan-leak 0 · V-G window physics(개념 last-24窓·decl seed 부재=evaluate-py-2 copy 우회 불가) ALL PASS. corpus 4.73MB(reps 130) · deterministic seed 7.

## Measure (engine-native · frozen bar · DESIGN_PREREG §3 verbatim)
`anima-py evaluate <clm> --xfan xfan_eval_manifest.json` (fold-in `xfan_run`·numpy core/decode·a_eval_py_canonical TERMINAL-eligible). PRIMARY **coverage C = |정확 고유 (슬롯,member)|/5** over 16 sampled decode(top_k=40 temp 0.7). + valid/spurious(genius⊥honesty) · per-slot-kind(unary vs joint) · greedy-collapse control(top_k=1 distinct) · **NLL-margin mode-collapse 판별기**(H_1440 FALS 1.0·DIST 0.0 전례 → "분포 학습됐는데 sampler 붕괴"를 "학습 실패"에서 분리). 전 arm 전량 캡처(evaluate-py-1 tail 금지).

**VERDICT (frozen · 양 main seed 일치 시만 cement)**:
- **CRACK 🟢** = held-out C≥0.60 양seed ∧ Δ(main−control)≥+0.40 ∧ spurious≤0.20 ∧ greedy 정상 → G6도 measure 벽.
- **JOINT-ONLY-FAIL 🟡** = unary-C≥0.60 ∧ joint-C<0.30 → fan CRACK·잔여벽=binding.
- **SAMPLER-COLLAPSE 🟡** = C<0.60인데 margin>0 → 분포 학습·decode FORM 문제·substrate 무죄.
- **🧱** = held-out C<0.30 ∧ margin flat ∧ validity green 양seed → **G6 substrate 천장이 corpus 축까지 earned 격상**(G1과 달리 진짜 천장·판별↛생성 비대칭 최강 증거).
- 회색(0.30≤C<0.60)=UNSTABLE-DIRECTIONAL. 허용 연장=V-A +20k step 1회뿐(그외 재발사=tune-to-green 금지).

## Verify (this card = PRE-FIRE infra)
- gen_xfan.py smoke+full: ALL_PASS(위 수치). `_xfan_parse` unit OK. `anima-py evaluate --xfan` fold ast OK·usage lockstep. evaluate-py-5(local `import numpy`)·evaluate-py-1(inline)·evaluate-py-2(copy 우회 불가) 준수.
- **PENDING = 3-run fire**(main s7/s4302 + shuffle-control·canon 303M from-scratch·A100 ~2h×3 ~$12-15·rent=spend owner go 접수) → ckpt PULL→HF PRIVATE → `--xfan` eval → verdict cement(2-surface+ARCHITECTURE gate+CHANGELOG+pr-cycle).

## Artifacts
`state/g6_reopen_xfan/`(gen_xfan.py·DESIGN_PREREG.md·AUDIT.json·xfan_train.txt·xfan_shuffle_train.txt·xfan_eval_manifest.json) · `cli/evaluate.py`(xfan_run·_xfan_parse) · design=Fable.
