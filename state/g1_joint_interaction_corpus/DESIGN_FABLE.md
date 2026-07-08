# 실 corpus joint interaction-lift — 설계서 (engine-native 303M · 결정적 실험)

접지 확인 결과 먼저: 과제문이 가리킨 `state/g1_gamma_divergence/residual_lift_probe.py`는 **현 트리에 없습니다** (해당 폴더엔 발산문서 `FABLE_DIVERGENCE.md`·`INSTRUCTION.md`만 있고 H_9225도 HYPOTHESES.jsonl 미등록 — 타 세션 미커밋으로 추정). 따라서 아래에 joint-fit 함수를 **재구현 가능한 스펙**으로 명시했습니다. probe 부착점은 실물 코드로 확인했습니다: `core/decode.py`의 `clm_load_weights()` + `_fwd_logits(W, tok, T)`(core/decode.py:543, [T,V] logits 반환) + `nn_ce_loss_allpos`, 그리고 `cli/evaluate.py`에 연구모드 플래그를 얹는 선례(`--system-g1`, cli/evaluate.py:344)가 이미 있습니다.

---

## 0. 질문의 정확한 형태 (정직 scope)

> "실 anima 4-cell corpus의 byte 언어에, **additive(α_A+β_B)로 설명 안 되는 저-rank 비가법 (A,B) 상호작용**이 — 303M engine-native 측정 표면(logits/NLL)을 통해 — 검출되는가?"

- 이건 **census 종결의 재확인 or 재검토 트리거**이지 새 GREEN 사냥이 아님. lift≈0이면 "재조합 목표 자체가 이 corpus·이 granularity에 없다" = 천장 종결의 결정적 보강(값진 negative).
- **honest bound**: 측정창 T=64바이트(canonical eval의 T=24를 dilated-conv가 허용하는 범위로 확장) — 여기서의 "재조합"은 **단거리(≤64B) 공기 조합**에 한정. 이 스코프를 카드에 명기 (`a_scale_honest_scope`).

## 1. A·B 조합축 top-3 + 통제축 2

| 축 | A | B | 셀 정의 | 왜 이 축인가 |
|---|---|---|---|---|
| **AX1 content-pair** (주력) | 언어셀별 내용어 top-40 (빈도 rank 100–1000 밴드, 기능어 제외) | 같은 밴드의 다른 내용어 | 64B 창 내 공기 (A,B) | 가장 일반적 재조합 축 — G1이 묻는 "개념×개념" 그 자체 |
| **AX2 topic×register** | 일반·SNS 양쪽에 등장하는 topic 내용어 | register 마커 (ko: `습니다/어요/ㅋㅋ/음·함`, 해시태그·이모티콘 / en: formal 구두점 vs `lol/omg/#`) | topic 문맥 + 마커 실현 지점 | anima 4-cell corpus의 고유 구조(register 축)를 그대로 활용; 문체 실현이 topic과 비가법으로 얽히는지 |
| **AX3 verb×object 선택제약** | 목적어 명사 (ko `O를/을 V` 패턴, en `V+O`) | 동사 | 패턴 매치 지점 | 선택제약 = 언어학적으로 비가법 호환성의 고전 후보 |
| **PC-P (검출력 양성대조)** | ko: 명사 말음 받침 유/무 · en: 명사 두음 | ko: 조사 슬롯(`은/는·이/가·을/를`) · en: `a/an` | 조사/관사 바이트 위치 | **실 텍스트에 실재하는 ground-truth 상호작용** (정답 바이트가 쌍에만 의존, marginal 비결정). 여기서 lift 안 뜨면 파이프라인 검출력 부족 = INVALID |
| **PC-N (특이도 음성대조, additive-solvable)** | AX1과 동일 단어 | 동일 | 단, A·B가 **서로 다른 창**(비공기)에서만 — y = 두 단독창 NLL 평균으로 합성 | 구성상 정확히 additive → bilinear가 여기서 lift 내면 과적합/거짓양성 = INVALID |

## 2. Held-out 재조합 split (누수 차단)

1. **창 dedup 먼저**: 전 corpus를 32B rolling-hash로 중복창 제거(SNS 반복글이 fit/held-out에 양다리 걸치는 누수 차단).
2. **셀 최소 표본**: 관측셀 = 해당 (A,B)가 ≥8개 dedup 창 보유.
3. **셀 단위 홀드아웃 20%** (seed=7 고정, PREREG에 동결): 단, 홀드아웃 셀의 A·B 각각이 fit 쪽에 ≥3셀 남도록 층화(marginal 식별 가능성 보장).
4. **격리(quarantine) 규칙**: held-out 쌍 (A,B)를 **동시에** 포함하는 창은 fit 쪽 어떤 셀의 표본으로도, marginal 추정으로도 사용 금지 — 통째 격리. (fit 셀 (A,C)용 창에 B가 우연히 끼어 있으면 그 창 폐기.)

## 3. 측정 파이프라인

**probe 부착점** — `anima evaluate --py` 경로의 동일 numpy 2-production decode를 재사용 (TERMINAL-eligible, `a_eval_py_canonical`):

- `cli/evaluate.py`에 `--interaction-lift` 모드 추가 (**`--system-g1` 선례와 동형** — single-entry `a_cli_single_entry` 준수, py-side 연구모드).
- 내부: `clm_load_weights(ckpt)` 1회 호이스트 → 창 manifest(JSON: 창 byte offset·셀 라벨·채점구간)를 읽어 창마다 `_fwd_logits(W, tok, T=64)` → 채점구간(두 번째 개념 등장 이후 바이트들)의 **per-position NLL**(log-softmax, `math.log` 미러) + **composition-point logit 벡터**(V=256)를 `.npz`로 방출. **decode 수학은 1바이트도 안 건드림** — logits를 읽기만 함(새 metric을 loss에 넣지 않음, `a_train_inline_gauge`/p7 무관 확인).

**셀 응답 3종** (전부 같은 joint-fit에 투입):

- **Y1** = 셀별 robust-mean NLL (스칼라, 주판정).
- **Y2** = 셀별 mean logit 벡터 → 전셀 PCA top-8 → PC별 스칼라 joint-fit + Bonferroni×8 (검출력 보강; 모델 표현이 상호작용을 담는지).
- **Y3** = 셀별 경험적 next-byte 히스토그램 (decode 無, 순수 corpus 통계 — 모델 아닌 **언어 자체**의 신호. verdict tier 대상 아님을 명기한 보조 판정자).

**joint-fit 스펙** (toy 부재로 재구현; 결정적, seed=7):

```
additive:  y_ab = μ + α_a + β_b                       (ridge λ, 최소자승)
joint:     y_ab = μ + α_a + β_b + Σ_{r≤R} u_a^r v_b^r  (R∈{1,2,4}, ALS ~50회 공동적합)
```
- λ·R 선택은 **fit-셀 내부 validation**으로만 (held-out 셀 절대 불가침).
- **lift Δ = (RMSE_add − RMSE_joint) / RMSE_add** — held-out 셀에서 1회만 평가.

**결합-파괴 통제 (설계 내장)**:
- **Freedman-Lane residual permutation** ×200: additive 적합 → 잔차를 관측셀 간 무작위 재배치 → joint 재적합 → Δ_null 분포. (additive 구조는 정확히 보존, 상호작용만 파괴 — 통계적으로 올바른 shuffle.)
- 보조로 조야한 (A,B) 짝-shuffle 1종 병행.

## 4. cheap-선판정 → full 경로 + 비용

**cheap (방향, 수 분~수십 분)**:
1. corpus 인덱싱·grid 구축·Y3 joint-fit — decode 無, 경량 텍스트 처리 (mini 가능).
2. 엔진 subsample: PC-P(조사/관사 — 표본 풍부) + AX1 100셀×5창 ≈ 500창. summer CPU numpy, 창당 ~1s(T=64, 303M ≈ 40 GFLOP/창) ≈ **10분**. 여기서 PC-P가 안 뜨면 full 발사 전에 검출력부터 수리.

**full (pool)**: ko-general(최대 셀)부터, 축당 ~600 관측셀 × 10창 ≈ 6k창, 3축+통제 ≈ 20k창 → **summer CPU 단일 프로세스 ~2–4h wall** (`OMP_NUM_THREADS=4` 캡, 동시 ≤2 샤드 — summer-overfire 교훈). **aiden은 303M heavy에 OOM 재부팅 루프라 제외**, mini 금지(rc=137).

> **1-line 비용**: 렌트 $0 (자체 pool summer CPU-only, GPU 불요) · wall ≈ 선판정 10분 + full 2–4h.

## 5. 판정 규칙 (사전등록·동결 — tune-to-green 금지)

**게이트 (둘 다 먼저 통과해야 verdict 유효):**
- PC-P: Δ > p95(null) ∧ Δ ≥ 5% → 아니면 **INVALID**(검출력 부족, verdict 없음).
- PC-N: Δ < 2% → 아니면 **INVALID**(bilinear 거짓양성).

**본판정 (축별, AX1–3):** 유의 = Δ > p95(Δ_null, 200 perm) ∧ Δ ≥ 2% (상대 RMSE 감소, 효과크기 바닥).

**해석 매트릭스:**

| Y3(언어) | Y1/Y2(엔진표면) | 결론 |
|---|---|---|
| 유의 | 무 | 실 언어에 비가법 재조합 목표 **실재**하나 303M이 못 담음 → **census 재검토 트리거** (재오픈 여부는 오너) |
| 유의 | 유의 | 모델이 이미 일부 상호작용 보유 → G1벽 위치 재진단 트리거 |
| 무 (전 축) | — | 이 corpus·≤64B granularity에 비가법 신호 자체가 없음 → **능력천장 종결 재확인** (TERMINAL-eligible negative) |

## 6. 실행 레시피 (기본경로용 단계 스케치)

```bash
# slug: state/g1_joint_interaction_corpus/
# 0. PREREG.md 동결 (위 임계·split seed=7·격리규칙 verbatim) + H_92xx 2표면 등록
# 1. (mini OK) 코퍼스 인덱싱: dedup → 축별 vocab/pair-occurrence → grid + split
python3 state/g1_joint_interaction_corpus/build_grids.py --corpus <4cell> --seed 7
# 2. (mini OK) Y3 model-free joint-fit → 방향 리딩
# 3. (summer) cheap 엔진 선판정: PC-P + AX1 subsample
anima evaluate --py <canonical_303m.clm> --interaction-lift \
  --manifest state/g1_joint_interaction_corpus/manifest_pcp.json --result-file rf_pcp
# 4. (summer, OMP=4) full 3축+통제 20k창 → .npz
# 5. joint-fit + Freedman-Lane 200perm → hexa verify → state/verdicts/ 동결 → 카드/jsonl verdict
```

구현 순서는 3(선판정)에서 PC-P 실패 시 4로 못 감 — 검출력 수리 루프가 먼저입니다.

---

설계는 여기까지입니다 (오너 정책: fable=설계·분석만 — 구현·발사·bookkeeping·PR은 기본경로). 기본경로에 넘길 때 핵심 인계점 3개: ① toy joint-fit 파일이 트리에 없으므로 §3 스펙으로 재구현(또는 타 세션 미커밋 회수), ② `--interaction-lift`는 `--system-g1` 선례 패턴으로 `cli/evaluate.py`에 추가, ③ PREREG 동결이 엔진 발사보다 먼저.