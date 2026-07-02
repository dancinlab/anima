# H_6173 — 🪟 G1 decode-side 발산 (FALSIFIED)

**tier:** 🧱 decode-side G1 레버 FALSIFIED (RF=9 반증·RF≥24; decode-window 반증·T=72 완전노출도 coverage0) → training-recipe binding 재확인
**title:** 🪟 G1 decode-side 발산 — RF-bound(RF=9)·decode-window(T=24캡) 두 가설 실 303M서 전수 반증: RF실효≥24, T=72로 두 개념 완전노출해도 composed coverage=0 → 모델이 프롬프트를 봐도 조건화 안함, decode로 G1 못엶, training 필수
**verdict:** 🧱 FALSIFIED (decode-side 가족, py mirror DIRECTIONAL, 실 303M py303_full.clm, aiden $0). 'G1 돌파 발산'의 무GPU-가능 유일 가족 전수 기각: [렌즈1 RF] byte거리별 영향 d1=5.4→d9=0.85→d24=0.57, 9에서 안끊김=실효 RF≥24 → RF=L(K-1)+1=9 가설 REFUTED(ING #42492882 실ckpt 불일치). [렌즈2 window] ConvMoE positional table 無→T는 하네스 캡; composed 2-concept(80b) T=24/48/72 decode(T72=완전노출) coverage=[0,0,0] → decode-window 아티팩트 아님. ⇒ 모델은 프롬프트 개념을 봐도(T72) 생성 조건화 안함(off-topic 표류). decode-side(RF·window·contrastive·anchor)로 G1 불가. 진짜 binding 제약=training objective/corpus(H_6172 재확인). 죽은 가지=operator·substrate·decode-window·RF; 살아있는 레버=재학습(GPU,G1-NEXT-FINAL)뿐. state/g1_decode_side_levers/RESULT.md.

## 발상 (G1 돌파 발산, owner)
벽 재프레임(training-recipe) 후 무GPU 가능 유일 가족=decode-side. RF·window 두 가설 통제 probe.

## 결과
RF=9 반증(실효≥24) · T=72 두 개념 완전노출도 composed coverage=0 = decode-window 아님. 모델이 봐도 조건화 안함.

## 함의
decode-side G1 불가 확정 → training objective/corpus가 binding(H_6172). 살아있는 레버=재학습(GPU).

## 관련
[[goal-g1-lever-discovery]] · H_6168 · H_6169 · H_6171 · H_6172 · H_1218
