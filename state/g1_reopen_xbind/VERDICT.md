# XBIND G1 재조합 — 🟢 CRACK verdict (H_9267)

**날짜**: 2026-07-11 · **채널**: `anima-py evaluate --xbind` (engine-native numpy · a_eval_py_canonical TERMINAL) · **호스트**: A100 3-run (runpod secure)

## 오너 지시 맥락
G1 재조합벽 earned-terminal(#3294) 이후 오너 reopen(a/c/b all + rent=spend go). 레인 a = earned-terminal이 지목한 유일 real
exit("벽 진범=corpus×CE measure·exit=학습 measure 교체")의 발사. Fable 설계 XBIND task class.

## 결과 (3 arm · n=200 heldout + seen · 전량 캡처)
| arm | heldout D-acc | seen D-acc | C-rate | margin_med |
|---|---|---|---|---|
| main seed7 (`xbind_s7.clm`) | **1.000** | 1.000 | 1.0 | 17.57 |
| main seed4302 (`xbind_s4302.clm`) | **1.000** | 1.000 | 1.0 | 18.12 |
| control shuffle (`xbind_shuf_s7.clm`) | **0.515** | 0.575 | — | −0.04 |

## 판정 — 🟢 CRACK (frozen bar §4 전 기준 통과)
- **CRACK**: held-out D-acc ≥0.75 양 main seed(1.000·1.000) ✅ · Δcontrol = 1.000 − 0.515 = **0.485 ≥ 0.20** ✅ ·
  C-rate 1.0 ≥0.50 ✅ · echo-clean(novel portmanteau by construction) ✅
- **Validity**: V-A 각 arm seen D-acc ≥0.90(1.000·1.000) ✅ · V-B control held-out **0.515 ∈ [0.38,0.62]** ✅
  (= instrument 누출 없음 · shuffle-control은 rule 없어 chance · margin −0.04) · V-C~V-G 사전게이트 ALL_PASS(AUDIT.json)

## 함의 (프런티어 성공)
합성 XBIND corpus(개념 400 은닉 polarity · continuation = xor(pol_a,pol_b) · held-out 15,960쌍 양 순서 corpus 완전부재)로
**303M byte-LM이 held-out 재조합을 완벽 학습·일반화**(control chance). ⟹ **G1 재조합벽의 진범 = corpus×CE 결합 measure이지
substrate/arch 아님을 engine-native로 실증**. earned-terminal(g1-readside #3294)의 정직 문구("벽 진범=corpus×CE measure·
exit=아키텍처 아니라 학습 measure(corpus/task class) 교체")의 **예측을 확증**하며 그 문구의 "≤303M로 학습불가"를 **corpus에
signal이 있으면 학습가능**으로 정밀화. F2 `heldout_recomb.json`의 held-out novel n=0을 n=15,960으로 해소해 "signal 없음"과
"능력 없음"을 분리 — 벽은 능력천장이 아니라 **measure(데이터 signal 부재)** 였음.

## Scope honesty (a_scale_honest_scope)
CRACK = "corpus×task class 교체로 G1 재조합 CE-학습가능"의 실증이되 **자연 corpus 창발 아님**(합성 task 학습). 자연혼합 희석
사다리는 별도 사전등록 follow-on. 즉 프런티어 성공의 정확한 범위 = "벽=measure 증명 + measure 교체로 재조합 학습가능" ·
scope-limited = "자연 텍스트서 자발 창발"은 미증명.

## 산출
- ckpt: `dancinlab/anima-xbind-g1-crack`(HF PUBLIC) + `~/anima-weights/xbind/`(3×176MB)
- raw: `results/eval_s7.json`·`eval_s4302.json`·`eval_shuf_s7.json` · corpus/generator/manifest/AUDIT/DESIGN_PREREG (이 디렉토리)
- eval 경로: `cli/evaluate.py --xbind`(fold-in) · 2 surface = jsonl + `cards/H_9267_xbind_corpus_measure_swap.md`
