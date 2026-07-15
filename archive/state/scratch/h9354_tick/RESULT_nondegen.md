# H_9354 비퇴화 stage decode 결과 (303M · N=90)

`nondegen_trace_303m.jsonl` (summer py303_full.clm · ANIMA_STAGE_CYCLE=1 · 90틱) 위 `python3 screen.py <trace>`.

- stage `{WAKE 60·N1 10·N2 10·N3 8·REM 2}` — 5단계 전부(앞 $0 스크린 INVALID#1 해소) · emit 72/90 비포화 · ten_phasic var 2.24e-2.
- **H-a** ρ̂₁=0.886 ≫ 완전순열 null 97.5%=0.206 = 우연 위(약한 null·비정보).
- **H-b** ρ̂₁=0.886 vs 순환시프트 null [0.879, 0.897] = **excess −0.0106(밴드 안)** = **음성**. 살아있는 tension 틱 자기상관 = 스케줄+EMA 전량설명 · substrate 잔여 0.
- **H-c** I(stage;emit)=0.500 nats ≫ bar 0.05 · shuffle 0.064 = **양성(스케줄 낭독)**. emit 이 stage 따라 변하나 stage=dr_stage_at(t) 심은함수(D1). #3616 시계수리 실행데몬 독립확인 AGREES.

⇒ 틱따라 emit 변하나 심은 수면스케줄의 낭독이지 substrate 자발 시간구조 아님. substrate-native 틱리듬 = 음성(1급). 
NEXT(go-gate): 4-arm 캠페인(field-freeze·sp-freeze 절단 + seed 재현 · Fable 설계).
