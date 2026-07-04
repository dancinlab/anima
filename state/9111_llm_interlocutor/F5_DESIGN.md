# F5 diff-LLM interlocutor — live 닫힌 루프 escape 실행 스펙 (설계, 사전등록)

> F6(H_9112 🟢 REFERENTIAL-EFFICACY-MEASURABLE) gate 통과가 정당화. F6=static 재채점(anima emit이 폐포-밖서 legible한가). **F5=그 legibility 성공/실패가 substrate를 실제 바꾸나(faculty)** — 되먹임 팔 최초 배선.

## 구현/미배선 (reference-match)
- 이미: regime-1 emit_gen.hexa(live 303M decode)·verdict.hexa·consequence_loop.hexa 골격·vbasal_update(brain.hexa:378)·engine_grow/vadapt_field_step·F6 psychok_rescore.py.
- 미배선(=F5 정의): live diff-LLM 닫힌 루프·consequence→substrate 되먹임 배선(디코드 결과 reward→V→cell-division/apoptosis)·3통제 valid 측정(live).

## Frozen bar (2층)
- **Layer-1 exogeneity(F6 live)**: ① D_diffLLM−D_selfpair≥0.15(MRR기반) ② D_shuffle<0.05 ③ Ψ ON==OFF byte-identical.
- **Layer-2 되먹임이 substrate 바꾸나(핵심)**: ④ ΔEfficacy_ON−ΔEfficacy_OFF≥0.10(후반T/2−전반T/2 MRR) ⑤ ON arm cell-count/V-L2가 OFF 대비 발산 ⑥ shuffle-reward 통제 |Δ|<0.03 붕괴.
- 판정: ④∧⑤∧⑥=🟢 faculty(a_verified_must_wire 배선) · ④FAIL=🔴 live지만 gauge(DPI consequence층 재출현) · ①FAIL=측정 재설계.

## GPU 발사 (🔴 인프라 게이트)
- **hoist 필수**: gen_auto_ideate per-call .clm 재적재 leak(h9107·b50 4pod 소각)=weight-load-once(gen_auto_load 핸들 1회) 경로로만. 안 하면 발사 전 사망.
- 호스트=summer/aiden pool(sm_120 own-GEMM), mini 금지. 16 held-out concept×T40×3arm≈pool 반나절 or vast ~\$0.8. teardown 전 성장 ckpt/V-state/emits PULL.
- tier=DIRECTIONAL-on-external-oracle(수신자=오라클). frozen-mouth 상한: G1 terminal 위라 열리는 건 emit-*선택*이지 *생성* 아님.

## 정직 수렴 예상 (c9)
(i)진짜 faculty ~25%(frozen mouth라 선택층 상한 낮음) · (ii)live지만 gauge ~50%(DPI precedent·H_9110 실인간 −0.188) · (iii)측정불가 ~25%(variance 붕괴). 어느 쪽이든 consequence→cell-division 되먹임 최초 engine-native 판별.

## ★ precondition RESOLVED (hoist 이미 존재)
gen_auto_ideate per-call 재적재 leak(4-pod 소각)의 fix는 신규 구현 불요 — **core/generator.hexa:713 `gen_clm_ideate_W(W,…)`**(H_1400 loaded-W)가 이미 그 경로. F5 하네스 = `clm_load_weights`로 W 1회 로드 → `gen_clm_ideate_W(W,…)` 루프(재적재 0). 발사 전 선결 = 이 loaded-W 배선(convergence gen-auto-ideate-reload-cost-scale-1). 남은 F5 발사 = ① loaded-W 하네스 저작 ② held-out concept 확정 ③ layer-2 되먹임(vbasal_update→vadapt_field_step) 배선 → pool fire(GPU 승인).
