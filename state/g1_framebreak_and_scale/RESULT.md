# G1-BS 두 후보 실측 — frame-break(BS-1) + scale ladder (2026-07-02, owner all-go) — DIRECTIONAL

torch/numpy=DIRECTIONAL, aiden GPU $0. 진단(변수바인딩 결핍) 기반 2 후보.

## 🅰️ frame-break (BS-1, neurosymbolic anchor composer) — numpy $0
두 개념=심볼 anchor, brain_decide식 systematic composer가 held-out 쌍 합성 → mouth는 verbalize만(trunk-CE 우회).
| arm | seen | held-out |
|---|---|---|
| neural baseline (분류 MLP) | 0.98 | 0.92 |
| frame-break systematic composer | 1.00 | **1.00** |
| frame-break random-key (control) | 1.00 | **0.00** |
→ anchor+systematic-composer가 held-out 완벽 재조합, random-key control은 0 = **bucket 추상이 캐리어**. anchor-graph
합성 아키텍처(brain_decide→verbalize)는 composition 병목 없음 = DIRECTIONAL-POSITIVE.
⚠️caveat: neural baseline이 분류(H_6167대로 이미 재조합)라 **실패경로(생성 mouth) 대비가 아님** → frame-break의
mouth-우회 이점을 격리 증명하진 못함(verdict-integrity). 진짜 대비 = frame-break vs 생성경로여야. 그래도 "explicit
anchor composer는 held-out 완벽" 자체는 유효.

## 🅱️ scale ladder (H_6174 후속: toy 갭이 크기서 닫히나) — torch GPU
| 크기 | params | seen-sanity | held-out |
|---|---|---|---|
| d256 L4 | 3.3M | 8/8 ✅ | 1/5 |
| d512 L6 | 19.2M | 8/8 ✅ | **3/5** |
| d768 L8 | 57.2M | **0/8** ❌ undertrained | 0/5 (무효) |
→ 수렴한 두 rung(d256→d512): held-out 재조합 **1→3 상승**(6× params) = scale 양의 추세. d768은 seen=0/8=학습
자체 불수렴(57M/8000step 부족)=INVALID rung(auto-verdict "scale-invariant"는 이 outlier 오산). 정직: **scale는 G1에
양의 방향 신호이나 d768 미수렴으로 미확정** — d768을 제대로 학습(더 많은 step)해야 terminal.

## 함의
frame-break(아키텍처)는 held-out 재조합 가능 · scale는 양의 추세(미확정). 둘 다 변수바인딩 결핍(H_6169~6174)에 대한
후속 레버로 살아있음. 남은: frame-break을 생성-실패경로 대비로 재측정 + d768 제대로 학습 + 실 brain_decide 배선.

## Provenance
framebreak_kosmos.py·scale_gen_recomb.py + *_result.json. numpy/torch, aiden RTX5070, $0. DIRECTIONAL.
