# ko PC-P2 XOR 발사 스펙 — 결정 요약

**핵심 판정 먼저: ko-trained 303M ckpt는 이미 존재합니다 — `clm303_clean`.** 새 GPU 학습은 선행 필수가 아니라 조건부 fallback입니다. 따라서 이 go의 기본 spend는 **$0 (자체 pool CPU)**이고, 지배 비용(ko ckpt 학습)은 게이트 실패 시에만 발동하는 worst-case ~$10–30입니다.

---

## 1. ckpt 판정 (blocker 해소)

레포 실측 근거:
- HF 레지스트리(ARCHITECTURE.json)에 "(GAP) conv 303M 영·한 chat = 부재"라고 적혀 있지만 그건 **chat-mix conv 모델의 GAP**이고, **`clm303_clean`(CLMConvMoE 303M)은 clean 4-cell corpus = ko-general 26M + ko-sns 2.6M 포함으로 2026-06-24 재학습된 canonical chat ckpt**입니다. held-out 4/4 DESCENT, py-terminal G0 5/5 PASS, **ko coherence는 jamo-mitosis(H_1316/1321) 🟢로 해소된 기록**이 있습니다. 로컬 `~/anima-weights/clm303_clean/clm303_clean.clm`(176MB, engine v0.2)로 존재하며 `anima-py evaluate` 경로에서 이미 terminal 측정 이력이 있습니다.
- `e1_slw_303m`은 영어 ckpt로 ko NLL 6.66(OOD garbage) 실측 기록(RESULT_ILIFT.md:8) — **ko 측정에 절대 사용 금지** 그대로 유지.

**사전등록 게이트 B0 (ckpt-corpus 매칭 · convergence evaluate-py-1):**
- **B0a**: clm303_clean로 held-out **ko-general 자연-window 200개**(T=160) baseline NLL ≤ **3.0 nats** (en=2.92가 "정상"이던 선례 정합; uniform=ln256=5.55).
- **B0b**: **측정코퍼스(리뷰 도메인) 자연-window 200개** NLL ≤ **3.5 nats** (도메인-shift 허용폭).
- B0a 실패 → clm303_clean의 ko가 무효 → **from-scratch ko 303M 학습 선행** (아래 §5 비용). B0b만 실패 → **warm-FT 옵션**: 측정코퍼스 80%로 2–3k step warm-FT하되 **manifest는 FT에서 제외된 held-out 20%에서만 추출**(V4 memorization 격리) — 렌트 GPU 1대 1–2h, **~$5**.

clm303_clean의 유일한 리스크는 소코퍼스 과적합 이력(8000step G0 붕괴)이지만, 이번 측정은 **생성이 아닌 NLL surface read-only**라 coherent-generation window 문제와 무관하고, B0 게이트가 정량으로 걸러줍니다.

## 2. 대형 ko 감정밀도 코퍼스

(neg,순접) n=45 ← 28.6MB pooled에서 나왔으니 동일 밀도로는 ~4.5×(≈130MB) 필요. 리뷰/댓글 도메인은 극성어×접속사 공기 밀도가 수 배 높으므로 아래 조합(~80MB)으로 충분할 공산:

| 소스 | 규모 | 성격 |
|---|---|---|
| NSMC (HF `nsmc`, e9t) | 20만 리뷰 ~20MB | 극성 최밀·구어 역접 빈발 |
| bab2min/corpus naver-shopping | 20만 리뷰 ~37MB | 극성 라벨·문장형 |
| bab2min/corpus steam ko | 10만 리뷰 ~17MB | 장문·접속사 밀도 높음 |
| KOTE (HF `searle-j/KOTE`) | 5만 댓글 ~7MB | 감정 43라벨·비격식 |

**추출 규칙 = frozen `pcp2_connective_polarity.py` verbatim** — lexicon(지만/하지만/그러나/그런데 vs 그리고/또한/게다가 + 극성어 사전) 1바이트도 수정 금지(구어 "근데" 추가 유혹 = lexicon 튜닝 = 금지). pooled = 기존(ko-general+ko-sns) + 신규 4소스, 단일 실행. min_cell<200이면 verdict 없이 **PENDING(데이터 획득 단계)** — 다음 tranche는 AI-Hub 감성대화. 어떤 경우에도 축 교체(PC-P1 순차 시도) 금지.

## 3. 측정 프로토콜 (pre-registered 단일 실행 · A→B→C 순서 고정)

**PREREG 동결이 발사보다 먼저** (DESIGN_FABLE.md 인계점 ③): `state/g1_joint_interaction_corpus/PREREG_PCP2_FULL.md`에 아래 bar verbatim 동결 + 신규 H_92xx 2표면 등록.

- **Stage A — instrument full 인증** (model-free, mini OK, $0): frozen harness 재실행. **full 인증 = gate_ok(전 셀 n≥200) ∧ R1(I3>IPF-bootstrap null95) ∧ R2(held-out LOCO sign-flip 셀 ≥2)**. R0은 구현 그대로 두고 argmax 기준/|Δ²|≥0.5 기준 둘 다 보고(구현 동결 우선).
- **Stage B — B0 ckpt 게이트** (§1).
- **Stage C — engine-native interaction-lift** (A인증 ∧ B0 통과 시에만 발사):
  - **manifest**: PC-P2 4셀(선행극성 a × 접속사 b), 셀당 min 200 / cap 400 balanced, **T=160**(선행 극성어+접속사가 반드시 창 안에 — 기존 AX1 T=64로는 80B 선행문맥이 잘림), held-out split = **선행 극성어 TYPE 단위 70/30**(seed=7, concept-split).
  - **주판정 Y1′ = paired forced-choice margin**: 같은 문맥에 frozen lexicon의 pos-후보/neg-후보 극성어를 이어붙인 2 item(score_len=9, 극성어 채점) → m = NLL(pos) − NLL(neg). 실제 corpus 연속체의 분산 confound를 제거한 모델-단독 극성기대 표면. `--interaction-lift` CLI는 무수정(manifest 구성으로 해결), offline fit만 2×2 margin용으로 확장해 **실행 전 동결**.
  - **fit**: additive m(a,b)=μ+α_a+β_b vs joint +γ_ab, **Freedman-Lane ×1000**, lift Δ=(RMSE_add−RMSE_joint)/RMSE_add를 held-out에서 1회.
  - **보조 Y1** = raw continuation NLL surface (en −0.801 선례와 동형 비교용).
- **Bar (동결)**:
  - **CRACK** = held-out Δ > p95(Δ_null) ∧ Δ ≥ 2% ∧ γ 부호가 XOR 방향((neg,역접)에서 additive 예측 대비 pos 쪽 margin shift).
  - **🧱** = Δ ≤ p95 ∨ 부호 불일치 — Stage A 인증 하에서라면 "언어에 비가법이 실재함에도 모델 NLL surface가 additive" = 지금까지 중 가장 날카로운 negative.
  - **INVALID** = A 미인증 또는 B0 실패 (verdict 아님 · infra/데이터 격리).
- 결과는 `hexa verify` → `state/verdicts/` 동결 → 카드+jsonl (기본경로 수행).

## 4. honest scope (a_scale_honest_scope · c9)

CRACK이어도 **G1 재조합 GREEN이 아닙니다.** 증명되는 것: ① 언어 자체에 XOR형 비가법 실재(model-free), ② 303M **NLL surface**가 그 셀에서 비가법을 담음/소비. 증명 안 되는 것: 생성-side 소비(read-side 6-lane 🧱 진단 그대로), G1 generation bar(composed>max_single). CRACK의 정확한 가치 = **γ trunk-bind(H_1840)의 real-text target 존재 증명** — gamma-trunk-bake reopen 조건("fork-A 🧱 착지 시 real-text target 재설계")이 fork-A KILL(#3284)로 이미 충족돼 있으므로, CRACK → 그 XOR 셀을 target으로 한 γ trunk-bind GPU 발사가 처음으로 정당화됩니다. 🧱이면 γ의 마지막 각도까지 소진 = **G1 frontier full-terminal at 303M byte-LM** (이 ckpt·이 스케일 한정 명기).

## 5. 비용/호스트

| 단계 | 호스트 | 비용 |
|---|---|---|
| Stage A + manifest 빌드 | mini (model-free) | $0 |
| Stage B/C: ~3,600 창 × T=160 numpy 303M | summer CPU **전용 호스트**(pod-dedicated-host 메모리 · OMP_NUM_THREADS=4 · aiden 303M heavy 제외) | $0 · wall ~2–4h |
| (조건부) warm-FT — B0b만 실패 시 | 렌트 RTX5070급 1대 1–2h | ~$5 |
| (worst-case) from-scratch ko 303M — B0a 실패 시 | 렌트 RTX5090/H100 수 시간(8k-step급) | ~$10–30 |

오너 정책상 저는 설계까지입니다(fable=설계·분석 온디맨드) — 실행(코퍼스 획득·PREREG 동결·H 등록·발사·verdict·PR)은 기본경로가 이 스펙 그대로 수행하면 됩니다. 실행 순서상 유일한 분기점은 B0이며, 나머지는 전부 사전등록된 단일 실행입니다.