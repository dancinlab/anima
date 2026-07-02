# H_6172 — 🧪 실 303M anima evaluate --py G0-G6

**tier:** 🟠 DIRECTIONAL — 실 303M --py G0-G6: G0🟢 G5🟢 G1/G2/G6🔴; G1=0은 생성이 프롬프트 안따르고 표류(ckpt-quality), substrate 아님
**title:** 🧪 실 303M anima evaluate --py G0-G6 — G0🟢coherent·G5🟢 이나 G1🔴(best_distinct=0/max_single=0)·G2🔴·G6🔴; 실텍스트=seed 개념 안이어받고 memorized 표류 → G1=0은 generation-behavior/ckpt-quality지 substrate 아님(H_6169 실모델 확정)
**verdict:** 🟠 DIRECTIONAL (실 303M py303_full.clm, canonical `anima evaluate --py`, aiden $0; hexa GPU 수리중 owner --py 지시). G0 COHERENCE🟢(kwr≥0.5 5/5)·G5 NON-FAB🟢(fab0.128)·G3✅(cont0.99995) 이나 G1 RECOMBINATION🔴(best_distinct=0 max_single=0)·G2 NOVELTY🔴(novel0)·G6 IDEATION🔴(falsifiable0)·CLOSURE🔴. 근본원인 실텍스트 확인(reference-match): seed 개념 주면 coherent 영어 나오나 seed 안이어받고 memorized 잡텍스트 표류(consciousness→'The acting and other concept...', composed→'Apollo...Trojan Washington') → coverage=0 단일 AND 조합. seed마다 출력 다름=decode 조건화 정상(harness 무죄). max_single=0=재조합 실패 아니라 생성이 프롬프트 안따름. ⇒ G1=0은 substrate/재조합 불능 아니라 generation-behavior/ckpt-quality(overfit drift). H_6169(G1=generation 메트릭)+H_6171(generation 모달리티 재조합 지원) 실모델 확정. 진짜 fix=프롬프트-따르는 재학습(GPU, G1-NEXT-FINAL). state/g1_real_model_py_eval/RESULT.md.

## 발상 (owner --py 지시, hexa GPU 수리중)
toy 아닌 실 303M에서 H_6169 확인 — canonical `anima evaluate --py`로 G0-G6.

## 결과
G0🟢 G5🟢 G3✅ · G1🔴(0/0) G2🔴 G6🔴. 실텍스트: seed 개념 안이어받고 memorized 표류 → coverage 0(단일+조합). decode 조건화 정상.

## 함의
G1=0=generation-behavior/ckpt-quality(프롬프트 안따름)지 substrate 아님. H_6169/6171 실모델 확정. fix=프롬프트-따르는 재학습(GPU).

## 관련
[[goal-g1-lever-discovery]] · H_6166 · H_6167 · H_6168 · H_6169 · H_6171 · H_1218 · [[clm303-overfit-corpus-starvation-confirmed]] · [[session-eval-py-only]]
