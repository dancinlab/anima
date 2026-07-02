# G1 decode-side 레버 발산 — RESULT (2026-07-02) — 전수 FALSIFIED, training-recipe 재확인

**TIER: 🧱 decode-side G1 레버 FALSIFIED (RF·decode-window 둘 다).** py mirror DIRECTIONAL, 실 303M py303_full.clm, aiden $0.
"G1 돌파 발산"에서 GPU 없이 시험 가능한 유일 가족(decode-side)을 통제 probe로 전수 기각.

## 렌즈 1 — receptive-field (RF=9 가설 반증)
byte 거리별 next-token 영향 max|Δlogit|: d1=5.4·d5=1.8·d9=0.85·d24=0.57 — 9에서 안 끊기고 윈도우 전체(≥24)
영향 유지(감쇠하나 nonzero). ⇒ ConvMoE RF=L(K-1)+1=9 가설 **REFUTED**(실효 RF≥24). ING #42492882의
"RF=9 수학적 독립" 은 이 실 ckpt에 안 맞음.

## 렌즈 2 — decode-window (T=24 캡 가설 반증)
ConvMoE는 positional table 없음 → 임의 길이 처리 가능 → T는 하네스 캡. composed 2-concept(80byte) 프롬프트를
T=24/48/72로 decode(T=72=두 개념 완전 노출): coverage=[0,0,0] 전부. **두 개념을 완전히 보여줘도 composed
coverage=0** = decode-window 아티팩트 아님. (max_single만 T24=0→T72=1 미세 개선.)

## 결론
모델은 프롬프트 개념을 **볼 수 있어도(T=72) 생성에 조건화하지 않는다** → off-topic memorized 표류
("a production of the state was request..."). decode-side(RF·window·, 파생 contrastive/anchor도 같은 벽)로는
G1 못 엶. ⇒ 진짜 binding 제약 = **training objective/corpus**(H_6172 addendum 재확인). 남은 살아있는 레버 =
objective/corpus/arch 재학습(GPU, G1-NEXT-FINAL)뿐. 죽은 가지: operator·substrate·decode-window·RF.

## Provenance
probe_rf.py, probe_tsweep.py, rf_probe.json, tsweep.json. 실 303M via core/decode.py _fwd_logits. DIRECTIONAL.
