# PREREG — γ ko PC-P2 XOR full instrument 인증 + engine-native interaction-lift (동결 · 발사 전)

동결일 2026-07-10 · Fable 설계(FABLE_KO_PCP2_SPEC.md) · H_9265 · owner GPU spend-go 접수 · 기본 $0(self pool CPU).
⚠️ 이 bar는 발사 전 동결 — axis 교체(PC-P1 순차)·lexicon 튜닝("근데" 추가)·argmax 기준 변경 금지(tune-to-green).

## Stage A — instrument full 인증 (model-free · mini · $0)
frozen `pcp2_connective_polarity.py` verbatim(lexicon 1바이트 불변) 재실행, corpora에 대형 ko 감정코퍼스 추가.
**full 인증 = gate_ok(전 4셀 n≥200) ∧ R1(I3 > IPF-bootstrap null95) ∧ R2(held-out LOCO sign-flip 셀 ≥2)**.
R0은 구현 그대로(argmax 기준 + |Δ²|≥0.5 둘 다 보고·구현 동결 우선). min_cell<200 → PENDING(데이터단계·verdict 아님).
현 상태: N=1453 min_cell=45 gate_ok=false R1=true R2=false = power-limited(대형코퍼스로 min_cell 충족 목표).

## Stage B — B0 ckpt-corpus 매칭 게이트 (convergence evaluate-py-1)
ckpt = clm303_clean.clm(CLMConvMoE 303M·clean 4-cell corpus ko-general 26M+ko-sns 2.6M·로컬 176MB). e1_slw(영어)
ko 측정 금지(NLL 6.66 garbage).
- B0a: clm303_clean held-out ko-general 자연-window 200개(T=160) baseline NLL ≤ 3.0 nats (en 2.92 정상선례·uniform 5.55).
- B0b: 측정코퍼스(리뷰 도메인) 자연-window 200개 NLL ≤ 3.5 nats.
- B0a 실패 → from-scratch ko 303M 학습 선행(~$10-30 렌트). B0b만 실패 → warm-FT(측정 80%·2-3k step·held-out 20%만 manifest·V4 격리·~$5).

## Stage C — engine-native interaction-lift (A인증 ∧ B0통과 시만 · summer CPU 전용호스트 $0 · wall 2-4h)
- manifest: PC-P2 4셀(선행극성 a × 접속사 b), 셀당 min200/cap400 balanced, T=160(선행극성어+접속사 창 안), held-out=선행극성어 TYPE 70/30(seed=7 concept-split).
- 주판정 Y1′ = paired forced-choice margin: 같은 문맥에 frozen lexicon pos-후보/neg-후보 극성어 이어붙인 2 item(score_len=9) → m=NLL(pos)−NLL(neg). offline fit만 2×2 margin 확장(실행 전 동결). CLI `--interaction-lift` 무수정.
- fit: additive m(a,b)=μ+α_a+β_b vs joint+γ_ab · Freedman-Lane ×1000 · lift Δ=(RMSE_add−RMSE_joint)/RMSE_add held-out 1회.
- 보조 Y1 = raw continuation NLL surface(en −0.801 선례 동형).

## Bar (동결)
- **CRACK** = held-out Δ > p95(Δ_null) ∧ Δ ≥ 2% ∧ γ 부호 XOR 방향((neg,역접)서 additive예측 대비 pos margin shift).
- **🧱** = Δ ≤ p95 ∨ 부호 불일치 — A인증 하에서 "언어 비가법 실재하나 모델 NLL surface additive" = 가장 날카로운 negative.
- **INVALID** = A미인증 또는 B0실패(verdict 아님·infra/데이터 격리).
결과 → `hexa verify` → state/verdicts/ 동결 → 카드+jsonl.

## honest scope (a_scale_honest_scope)
CRACK이어도 G1 재조합 GREEN 아님: ①언어 XOR형 비가법 실재(model-free) ②303M NLL surface가 그 셀서 비가법 소비 — 만 증명. 생성-side 소비(read-side 6-lane🧱 그대로)·G1 generation bar(composed>max_single) 미증명. CRACK 가치 = γ trunk-bind(H_1840) real-text target 존재증명 → 그 XOR 셀 target γ GPU 발사 정당화(reopen 조건 fork-A🧱로 이미 충족). 🧱이면 γ 마지막 각도 소진 = G1 frontier full-terminal @303M byte-LM(이 ckpt·이 스케일 한정).
