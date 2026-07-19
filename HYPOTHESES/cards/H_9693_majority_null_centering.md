# H_9693 — majority-null centering: v−store평균으로 shortcut 의 존재 자체를 봉쇄 (RV-3 · 구조 레버)

**status:** 🔵 PROPOSED (미실행 · lab full RV-3 · 303M pool 2-seed · core 침습 · DESIGN-ONLY)
**lane:** g1-storebridge-val-robust
**related:** [[H_9672]] · [[H_9690]] · [[H_9691]] · [[H_9692]]
**source:** lab full RV (Fable 발산) — 의뢰자 선험후보 (d) 게이트 재설계의 정밀판

## 한 줄 주장 (반증가능)
값 읽기를 **v_cent = Σ(aᵢ−1/n)·val[polᵢ] = v − mean_i val[polᵢ]** 로 바꾸면(store-평균 제거), 균등 주소에서 v_cent≡0 이 되어 **op⊕majority 국소최적이 값경로에 원리적으로 존재할 수 없고**, val 분화가 seed-robust 해진다.

## ① 근거
- 핵심 관찰: 흐린 v(균등 a)는 정확히 **store 극성평균 = majority 신호**다 — 즉 op⊕majority shortcut 은 값경로 **바깥**이 아니라 값경로를 **통해** 표현된다. balanced 채점은 eval 에서 보상만 끊지, 학습 중 CE 를 낮추는 basin 은 그대로다.
- centering 은 그 basin 을 **없앤다**: a 균등 ⟹ v_cent=0 ⟹ 값경로로 majority 정보 유통 불가. CE 를 낮추는 유일한 길 = a sharp 화 ∧ val 분화.
- 공짜 부수효과 = **자동 커리큘럼**: val gradient ∝ (aᵢ−1/n) — 주소가 정확해질수록 켜진다. RV-2 의 address-first 순서가 **하이퍼 0개로 아키텍처에서 도출**된다. (전제: addr-loss 필수 — 없으면 초기 gradient 데드락.)
- 수렴시 정보 보존: sharp a 에서 v_cent ≈ (1−1/n)(val[pol_t]−mean) — slot-특이 신호 온전.

## ② 최소 구현 (core 침습 · lane_type=2 · ~20줄)
- core/clms.py 두 곳 각 1줄: `CLMSModule.forward` 의 `v = bmm(a,V)` → `v = bmm(a−1/n, V)` · `store_apply` 의 `v = a @ V_slots` 동일 — **단 lane_type==2 분기로만**(트레일러 codec 에 lane_type 필드 기존재 · 구 .clm semantics 보존 · read/pack 무변경).
- oracle 경로에도 동일 적용(one-hot ⟹ v_cent=val[pol_t]−mean · 정보 보존 → ORACLE 지표 의미 유지).
- torch↔numpy **2-production byte-parity 테스트 필수**(store_apply 미러가 파리티 타깃).
- trainer: `--clms-center` 플래그 → lane_type=2 로 직렬화.

## ③ 사전등록
- **toy 승격**: 이 레버만은 toy 가 유의미 — d64 toy 에서 centering 이 기존 PASS(0.99/0.88)를 **깨지 않는지**(no-harm) + 파리티 게이트. fragility 반증은 여전히 불가(정직 스코프 동일).
- 결정면 = 303M 2-seed {7,11} · T3 config + `--clms-center` + addr-loss.
- 게이트: ORACLE≥.90 ∧ P1-balanced≥.75 ∧ addr-gap≤.20 ∧ flip≥.90 (양 seed · balanced) + **held-out 일반화 유지**(비균형 store 에서 mean 이 store 별로 달라지므로 명시 확인). PASS 시 confirm seed 13.
- 통제군: ① lane_type=1 arm = T3 재현(양성대조) ② λ=0 C2 ③ toy no-harm.
- 모니터: sb_val_sep 궤적(초기 gradient 소실로 분화가 **늦게** 시작하는지 — 예산 내 미수렴 감시).

## ④ 잔인판정
- **가장 침습적**: 함수류 변경 — 구 ckpt 와 행동 비교불가, lane_type 분기 누락시 구 트레일러 오독(파리티+분기 테스트가 하드게이트).
- 초기 val gradient ∝ (a−1/n)≈0 — shortcut 을 죽인 대가로 **분화 개시가 늦다**. addr-loss 가 느린 seed 에선 예산 내 미수렴 위험(그 경우 '벽'이 아니라 '예산'으로 오독 금지 — sb_val_sep 궤적으로 구분).
- balanced store 에서 mean=(val[0]+val[1])/2 는 a-독립 상수 시프트라 "MLP 가 시프트를 재학습해 무력화" 우려가 있으나, 제거 대상이 정확히 a-독립 항이므로 이는 무력화가 아니라 의도 그 자체다. 비균형 store 일반화만 실측으로 확인.
- 감독 tier 동일 · 창발 주장 불가.

## 비용
toy $0-급 + 303M 2런(+confirm) · pool. core 변경분 wheel 반영시 **G5 VERSION bump** 필요.

## 죽는 방식
shortcut basin 을 구조적으로 제거했는데도 seed-11 val 이 미분화면 죽는다 — 그러면 사인은 국소최적이 아니라 최적화 자체(예: val 스케일/조건수) ⟹ RV-4 의 init 각도가 승격.

## 상태
🔵 PROPOSED — 측정 주장 0(설계).
