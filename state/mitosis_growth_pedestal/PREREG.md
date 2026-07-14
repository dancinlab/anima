# H_9313 — GROWTH-PAYS 에 PEDESTAL + C1 통제 부착 (사전등록 · 발사 전 동결)

freeze_ts_local: 2026-07-14 (KST) · lane: MITOSIS-ENGINE · 도시에: `state/fable_killshots/w3_mitosis.out.md` §3 카드1 · §4
선행: H_9311 (#3439) — SHRINK 10셀 2.72391 → 320셀 2.46370 = **−0.26021 nats/byte** ⇒ 🟢 "GROWTH-PAYS".
**문제: 통제가 0개다.** FLAT(B3) 통제는 퇴화분할 `break` 때문에 10셀에 고정 = 축 미탑재(flat_deg=0.00000).
참값-0 pedestal 없음. 시드 1쌍. ⇒ 이 카드가 그 두 급소를 찌른다.

## 1. 계기 (H_9311 verbatim · 한 바이트도 안 바꾼다)
REAL KO 30MB 창 `sha c47b6808…` · Vj=323 · ko_stride 2500 · dim-3 · even/odd held-out ·
train n=5,101 · test n=5,100 · nats/UTF-8-byte · LIVE 엔진 faculty
(`E.jamo_head_grow_shrink` · `E._jh_counts` · `E._jh_counts_wb` · `E._jh_pooled` · `E._jh_assign`).
`ce_per_byte()` = H_9311 스크립트에서 그대로 복사. LAPLACE=1.0 · MIN_OWNED=8 · SPLIT_THRESH_CE=0.05.
grow_max ∈ **{10, 320}** (도시에 §4 2점 스크리너).

## 2. 팔 (5개 · 전부 같은 창 · 같은 test set)
- **E** (실험군, 기존) = repair + WB head, 진짜 (Xtr,Ytr) 로 성장.
- **C1** (매개공변량-일치 통제) = **E와 동일 centers**, head 만 flat leaf-MLE (`_jh_counts`, WB 없음).
  ⇒ 명목 예산이 아니라 **실제 매개변수(파티션)** 를 맞춘 통제 (`control-must-match-mediating-covariate`).
- **P0X** (도시에 지정 pedestal) = Xtr **행-셔플** 사본 X' 로 성장(=분할 선택이 Y와 독립),
  centers 확정 후 head 는 **진짜 (Xtr,Ytr)** 로 WB 재적재. 참값 0 = **적응적 분할선택**의 정보.
  ⚠️ 정직: X'-성장 파티션도 여전히 **X-공간의 정당한 카빙**이므로, 진짜 (X,Y) 로 head 를 채우면
  *비적응적 X-조건화 정보*는 여전히 들어온다 ⇒ P0X 의 참값 0 은 "분할 선택"에 한정되지,
  "혼합-평활 artifact" 의 참값-0 이 아니다. 그래서 P0Y 를 추가한다.
- **P0Y** (진짜 참값-0 pedestal · 추가) = `E.jamo_head_shuffle_targets` 로 Ytr·Yte 를 각각 셔플
  ⇒ X ⊥ Y (train·test 양쪽) ⇒ **어떤 파티션도 Y 정보를 살 수 없다(참값 0, by construction)**.
  같은 성장·같은 WB head. 여기서 CE 가 셀 수와 함께 **내려가면 그건 100% 추정기/혼합-평활 artifact**.
- **P1** (양성대조 · liveness) = X 에 **Y 를 결정하는 4번째 축** `Y/Vj` 를 SPIKE-IN (dim=4).
  성장이 이 축을 반드시 찾아야 한다.

시드: **S=8 seed-pair**. seed0 = H_9311 원본 `[[0.3,0.5,0.0],[0.7,0.5,0.5]]` (CALIB 용) ·
seed1-7 = `random.Random(100+i)` uniform[0,1]^dim.

## 3. 검정력 (데이터 보기 전 계산)
- σ_path 사전추정 = **0.03 nats/byte** (H_9311 자체 실측: 같은 팔에서 40셀 2.71886 → 80셀 2.75023 = +0.031 비단조).
- S=8 ⇒ SEM = 0.03/√8 = **0.0106**.
- 양측 α=.05 · 80% 검정력 **MDE ≈ (t.975,7 + t.80,7)·SEM = (2.365+0.896)·0.0106 = 0.0346 nats/byte**.
- **KILL 임계 |Δ_P0| ≥ 0.10 에 대한 검정력 > 99%** ⇒ 킬샷 판정은 POWERED.
- **TOST(±0.02) 등가 판정**: 통과하려면 `t.95,7·SEM ≤ 0.02` → SEM ≤ 0.0107 → S ≥ 8 (경계).
  실측 σ 가 0.03 을 넘으면 **등가 주장은 NOT-POWERED 로 보고**하고, 절대 마진을 완화하지 않는다.
- 부가(2차) 정밀도: 같은 test 5,100 점을 두 모델이 공유하므로 **paired-t (test-point 짝)** 도 보고.
  **max(controls) 순서통계량 금지 — 전부 paired.**

## 4. 동결 bar (발사 후 1바이트도 이동 금지)
- **G-CALIB (BLOCKING)** — seed0 의 E 가 H_9311 을 재현: |CE_E(10) − 2.72391| ≤ 0.001 **AND**
  |CE_E(320) − 2.46370| ≤ 0.001. 실패 → **⛔ INVALID** (어떤 bar 도 읽지 않는다).
- **G-LIVE (BLOCKING · 양성대조)** — mean_seeds[ CE_P1(320) − CE_P1(10) ] ≤ **−0.50** nats/byte.
  실패 → **⛔ INVALID** (계기가 존재하는 정보조차 못 찾음 ⇒ 다른 bar 판독 금지).
- **G-PED-Y (참값 0)** — Δ_P0Y ≡ mean_seeds[ CE_P0Y(320) − CE_P0Y(10) ].
  - Δ_P0Y ≤ **−0.10** ⇒ **혼합-평활 artifact 가 지배** ⇒ **H_9311 🟢 GROWTH-PAYS 철회**.
  - TOST |Δ_P0Y| ≤ 0.02 등가 ⇒ pedestal 깨끗.
  - 그 사이 ⇒ 그 값을 E 에서 **차감**하여 재판독(아래 EARNED).
- **G-PED-X (분할선택 참값 0)** — Δ_P0X ≡ mean_seeds[ CE_P0X(320) − CE_P0X(10) ].
  적응적 분할선택이 번 몫 = **Δ_E − Δ_P0X** (paired, seed 짝).
- **G-DISSOC (C1)** — Δ_C1 ≡ mean_seeds[ CE_C1(320) − CE_C1(10) ].
  - Δ_C1 > **+0.02** (열화) **AND** Δ_E < **−0.05** ⇒ **이중해리** ⇒ 판정 = "성장·추정기는 분리 불가한 쌍-레버".
  - Δ_C1 < **−0.05** (C1 도 개선) ⇒ 정보는 파티션에 있고 WB 는 조연 ⇒ "성장 단독 레버"(더 강한 🟢).
- **헤드라인 EARNED** = Δ_E − Δ_P0Y (paired, seed 짝) = 참값-0 artifact 를 뺀 성장의 순이득.
  - EARNED ≤ −0.05 **AND** seed-level paired-t p < .05 ⇒ **GROWTH-PAYS 생존**(처음으로 통제된 채).
  - 아니면 ⇒ **철회 대상**.

## 5. 금지 (위반 = 결과 무효)
- 통제군 약화 금지 · 헤드라인 사후선택 금지 · bar 이동 금지 · detector 재계산 금지.
- 음성은 결과다. `max(controls)` 금지 (전부 paired-t).
- 인프라 실패(OOM·의존성)는 verdict 에 섞지 말고 별도 INFRA-BLOCKED 로 격리.
- LABEL: py 2-production engine-native (`a_eval_py_canonical`) · stride 2500 창 한정 · $0 CPU 로컬.
