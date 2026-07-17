# H_9691 — oracle-CE 상시 보조 이중경로: 부트스트랩 레이스 제거 (RV-1 · ★최우선 레버)

**status:** 🔵 PROPOSED (미실행 · lab full RV-1 · 303M pool 2-seed · DESIGN-ONLY)
**lane:** g1-storebridge-val-robust — val 극성분화 seed-robust化 본명(本命)
**related:** [[H_9672]] · [[H_9423]] · [[H_9690]] · [[H_9692]] · [[H_9693]]
**source:** lab full RV (Fable 발산) — 의뢰자 선험후보 (a) oracle-warmup 의 연속화·탈스케줄판

## 한 줄 주장 (반증가능)
학습 내내 **L = CE_ans(softmax 주소) + w_addr·L_addr + w_orc·CE_ans(one-hot oracle 주소)** 의 이중경로 결합손실을 걸면, val 분화가 seed 복권에서 벗어나 **2-seed{7,11} 4-게이트를 동시 통과**한다.

## ① 근거 — 왜 seed-fragility 를 고치나
- 사인 = **레이스**: val 분화는 sharp 주소를 기다리고, 주소 sharp 화 이전의 흐린 v 가 MLP 를 op-only 국소최적에 커밋시킨다(H_9672 해리). seed 는 레이스 승패를 정할 뿐.
- oracle 분기 = **Stage1.5 의 훈련신호를 매 step 재생**: one-hot 주소에서 ∂CE_orc/∂val[pol_target] 은 step 0 부터 단일-slot clean gradient — Stage1.5 가 ORACLE 1.00 으로 val 분화 가능성을 이미 입증한 유일 레짐이다. op⊕majority 는 CE_orc 를 그 아래로 못 내린다(one-hot v=val[pol_t] 정확 → v 를 안 쓰면 op-주변부 엔트로피가 바닥) ⟹ 국소최적이 **결합손실의 최적이 아니게 됨**.
- softmax 분기 + addr-loss = 주소학습(H_9672 가 2-seed robust 입증). 두 분기가 **동시에** 각자의 입증된 일을 하므로 어느 쪽도 상대의 부트스트랩을 기다리지 않는다 = 레이스 소멸 = seed 복권 기전 제거.
- (a) sequential warmup 대비 우위: **위상전환 창이 없다** — warmup 은 전환 직후 주소 미숙 상태에서 흐린-v 창이 재개돼 val 붕괴/재-shortcut 위험. 연속형은 그 창 자체가 없다.

## ② 최소 구현 (trainer-only · core/clms.py 무변경 · ~15줄)
- `CLMSModule.forward` 는 이미 `oracle_slot` 인자를 받는다(core/clms.py:244-249 · Stage1.5 코드 재사용).
- cli/train.py CLMS 블록(≈L1191)에서 같은 yn_q 로 2번째 lane 호출(trunk forward 재사용·추가비용 ε):
  `sl_orc = model.clms(yn_q, K, pols, oracle_slot=tgt)` → `loss += w_orc * F.cross_entropy(sl_orc, y_ans)`
- 플래그 `--store-oracle-aux <w>` (default 0=off) · `--store-addr-weight` 기존 유지.
- 모니터-전용 게이지 `sb_val_sep = ‖val[0]−val[1]‖` aux 로깅(`sb_store_acc` 옆 · a_train_inline_gauge: loss 밖).
- 트레일러/eval 무변경 — eval 은 순수 softmax 경로(누수 없음).

## ③ 사전등록 (toy-first 정직 스코프 포함)
- **toy(d64) = 배관 회귀만**: T2 가 벽이 scratch 차원에서 미재현임을 보였으므로 toy 는 fragility 를 **반증 못한다**. toy PASS = "레버가 기존 능력을 안 깬다" 이상의 증거 아님(카드에 명시).
- **결정면 = 303M py303_full 공학습 · T3 동일 config/예산 + `--store-oracle-aux 0.5`(단일 사전등록값·스캔 금지) + addr-loss 유지 · 2-seed {7,11}.**
- **게이트(양 seed 모두)**: ORACLE≥.90 ∧ P1-balanced≥.75 ∧ addr-gap≤.20 ∧ flip≥.90 (balanced 채점).
- PASS 시 **confirm seed 13**(사전등록·미접촉) 1발 — seed-차원 tune-to-green 차단.
- 통제군: ① w_orc=0 arm = T3 재현(fragility 양성대조 — seed-11 이 또 죽어야 계기 정상) ② λ=0 C2 byte-identical ③ balanced 채점 유지.
- fallback arm(1차 실패시에만 개봉): sequential 2-phase warmup(의뢰자 (a) 원형 · `--store-oracle-warmup N`) — 전환 직후 ckpt 로 게이트(피크 아님).

## ④ 잔인판정 (오도위험)
- **감독 tier 명시**: target_slot 라벨을 주소(addr-loss)+값(oracle 분기) 두 군데 소비 — 이 캠페인 전체가 "감독 co-train tier" 다. **창발 주장 불가** · 자연 선언 전이는 별도 프런티어(origin H_9683). end-task 만으론 arm-B/C 가 이미 KILL.
- one-hot vs softmax 주소분포 차이를 MLP 가 구분-악용할 가능성 — flip·held-out 게이트가 잡고, 수렴시 addr_mass 0.95+ 로 두 분포 근접. 그래도 잔존하면 flip<.90 으로 드러난다.
- w_orc 를 seed 별로 재조정하는 순간 tune-to-green — 단일값 0.5 고정, 실패는 결과다.
- 2-seed PASS ≠ 분포 주장 — 성공률 주장엔 seed n≥5 필요(비용상 미청구·스코프에 명시).

## 비용
303M 공학습 2런(T3 동일 예산) + confirm 1런 · pool(summer/aiden) · mini 금지.

## 죽는 방식
w_orc=0.5 에서도 seed-11 ORACLE<0.90 이면 죽는다 — 그러면 사인은 레이스가 아니라 값경로의 더 깊은 구조(→ RV-3 승격).

## 상태
🔵 PROPOSED — 측정 주장 0(설계). 발사 전 RV-0 부검 선행 권장.
