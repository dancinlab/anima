# H_9423 — TWO-STORE NATIVE: 공학습 store-조회 다리를 부모 conv byte-LM 에 심는다

**status:** 🔵 PRE-REGISTERED → **S0 배선 DONE**(CLMS lane 구현·$0 로컬 검증) · not-terminal · wired: CLMS trailer lane 배선완료(학습 미실행)
**S0 결과(#PR · 로컬 $0):** CLMS store-bridge lane 6조각 배선·전부 실측 — ① corpus `storebind` fmt(결정성 byte-id·C0-a zero-leak 0·XOR 검산) ② `core/clms.py`(3-face+find_qpos · pack/read 왕복 byte-identical · store_apply 덮어쓰기 qpos-only · oracle 경로 · λ0 passthrough) ③ `core/decode.py` 3점(로더 785↓·`set_clms_store` setter·`_fwd_logits` CLML early-return 제거 fall-through) ④ `core/serialize.py` `append_clms_trailer`(toy.clm 왕복 byte-identical·C0-f body 불변) ⑤ `cli/evaluate.py` `--store/--store-oracle/--store-lambda`(end-to-end 완주·per-class split) ⑥ VERSION 0.14.13(G5). **lane active 확증**: store_apply 가 `_fwd_logits` 서 발화(λ1 vs passthrough qpos row Δ=0.47)·λ0==passthrough byte-identical. Fable §E 정본: key_emb=**파일저장**(seed 재생성=조용한 계기사망 벡터 반려). 무학습 toy 정확도=우연(0.53·예상 · S0=배선지 학습 아님). 🔒 미구현: CLMSModule 학습 배선(train.py store 주입)=S1 · replay `=> ` 트라이그램 스캔 게이트=replay 도입 시(S1).
**lane:** 재조합/BINDING · runtime lookup bridge (프런티어 g1-interface-addressable-wall)
**related:** [[H_9392]] (BRIDGE-BOLT 3-port 종결 — 볼트온 死 ⟹ 공학습이 유일 남은 경로 · 이 H 가 그 NEXT) · [[H_9359]] (벽=런타임 다리 부재) · [[H_9327]] (SEEN 극성 이미 학습 = ② shortcut 난점) · [[H_9353]] (컨텍스트-port EARNED)
**id 정정:** 앞선 카드/메모리가 이 작업을 "H_9393" 로 forward-참조했으나 **H_9393 은 병렬 세션이 DYNAMIC-FLOOR 로 선점**(id 충돌) ⟹ canonical = **H_9423**.
**source:** Fable 설계(`walls-delegate-to-fable`) — owner "go" · v2 toy(anima-v2 #3753/#3755)가 공학습 다리를 DIRECTIONAL 실증한 뒤 부모 core/ 이식.
**ckpt:** py303_full.clm (GROWTH warm-start 원본 · aiden `~/py303_full.clm`)

## 물음

볼트온 다리는 3-port 전멸로 종결([[H_9392]]): 컨텍스트(H_9353 EARNED)·가중치(H_9327/9358/9359)·
출력(--store-mix actuator). ⟹ **안정적 런타임 조회 다리 = 공학습(co-training)뿐.** v2 toy 가 이를
실증(V2_6 COTRAIN macro 0.987/0.992 · C2 VALID). 

> 그 공학습 다리를 **부모 conv byte-LM(303M)** 에 심으면 held-out 에서 조회 다리가 서는가?
> (v2 는 transformer · 전역어텐션 · toy — 부모는 conv · RF-bound · production.)

## 설계 (Fable · 코드 탐사 확정)

**판을 바꾼 코드 사실 3개**: ① 부모 readout = **선형 1×1 conv**(`core/decode.py:1114`) ⟹ v2 XOR 벽
(선형상한 0.756)이 부모에 그대로 적용 · ② `.clm` = magic-guarded **trailer 체인**(CLMB→SLW→CLML ·
부재 시 byte-identical passthrough) ⟹ 새 `CLMS` lane 을 체인 끝에 append · ③ **SLW**(슬롯 학습)+
**CLML**(logit-add lane)이 이미 다리 두 반쪽 선례.

**모듈 = `CLMS` store-bridge lane** (새 trailer · SLW 형 내부모듈 + CLML 형 logit 주입):
- **key(동결 내용주소)**: `mean(key_emb_frozen[bytes(entity)])` — 시드고정 랜덤 per-byte emb · 영원히 비학습
  (v2 필요조건 ④ 축자이식 · hippo `dg_codes` 고정투영 native 선례). held-out 개체 일반화.
- **value(학습)**: 극성 id → 학습 벡터 `val(2,d)`.
- **query**: `q = yn[qpos]·W_q` (trunk penultimate · qpos=프롬프트 마지막 바이트). **T=24 창 전체가 RF 안**
  (`decode.py:1213` · 유효 RF≥24)이라 연산자+개체가 `yn[qpos]` 에 인과도달 = query 형성 RF-무결.
- **조회**: `a=softmax(q·K/√d)` over 8 slot · `v=Σaᵢ·val[polᵢ]` (SLW 가 key-slot 읽기를 이미 엔진화).
- **소비(인과 · 답 위치만)**: `store_logits = GELU(concat(v,yn[qpos])·W_h)·W_out` (concat 이 하중부담 —
  연산자가 극성을 게이팅해야 XOR · 부모 head 선형이라 이 MLP 가 ①의 전부) · **답위치 logits = λ·store_logits**
  (store_only 게이트 = trunk logit·grad 제거). λ=학습 scalar · monitor-only(loss 밖).
- **답 위치 = 바이트파싱**(`"=> "` 뒤 첫 답바이트 · 스트림 순수함수 = trainer 보조채널 불요).
- store/trailer 부재 ⇒ **byte-identical passthrough**(C0-f 봉인).

**v2 필요조건 5겹 → 부모 이식:**
| v2 | 부모 이식 | 난점·해결 |
|---|---|---|
| ① 비선형 readout | 다리 GELU-MLP 융합 | 부모 head 선형 확인 — C0-e ORACLE 이 즉시 잡음 |
| ② shortcut 차단 | **3중**: store_only 게이트 + **nonce 개체**(사전학습 prior 무의견 → H_9327 "SEEN 극성 이미 학습" 원천차단) + ⑤ 재추첨 | 부모 최대난점 → 답이 스트림·가중치 어디에도 없고 오직 store 에만 |
| ③ 예산 | ladder 실측(key-shuf 통과시점)→meta floor 동결 | value-읽기 빠름·주소-조회 늦음(v2) → true-slot attention 게이지 monitor |
| ④ key 고정 | 동결 랜덤 byte-emb 평균 | chicken-and-egg 해답 축자이식 |
| ⑤ store 순환 | **block 단위 재추첨**(seq 1024 block=store 1추첨 · trainer mmap window 호환) | per-example 순환은 trainer 대수술 → block 단위. ⚠️ block 내 개체당 라인 1개(재등장 금지 · window 복사방지) |

**growth vs scratch**: 주 arm = **GROWTH**(`--init py303_full` + 다리 cell⊕EN register cell 비례 재생 공학습
· `a_mitosis_train` 🟢 · V2_7 knife-edge 는 동결 trunk 문제였고 growth 는 trunk 에 grad 흐름 = 공학습 조건 충족).
scratch/BOLT 는 ladder 소규모 대조 arm(BOLT = CLML 오프라인 파이프라인 = 동결 by construction).

## 코퍼스 (새 fmt · EN-FIRST)

`anima-py corpus storebind --lang en --atoms nonce.json --n-blocks N --seed S --out c.txt` → 3산출:
`c.txt`(block정렬) · `c.txt.store.jsonl`(block↔store) · `c.txt.meta.json`(floor). 라인 = `is {ent} => good` /
`not {ent} => bad`(EN `not` 자유전치=판별자 · ≤23 byte). nonce CVCVC 512 → train 384/held-out 128
(interleave · **zero-leak hard-assert** 텍스트+store 양면). block 당 fresh 극성(개체 기대 0.5). 혼합 재생
(retention 방어). 평가 = `evaluate <clm> --store held.json`(학습과 동일 manifest·lane = **p8 문자 구현**).

**정직한 범위(preregister)**: 합성 nonce-사실 · 🟢 = "conv 엔진에 공학습 런타임 조회 다리 **존재 가능**" 이지
**"G1 벽 종결" 아님** — 자연 선언 전이는 별도 후속 H(`a_scale_honest_scope`).

## 게이트 (SEQUENTIAL · bars 발사 전 동결 · no tune-to-green)

- **C0 계기무결성**: (a)leak=0 (b)base held-out∈[.45,.55] (c)결정성 (d)gradcheck+serialize DESCENT+device-parity
  **(e)ORACLE ≥0.90**(--store-oracle 참slot one-hot 강제 · **음성은 이거 통과 전 안 읽음** · v2 계기사망 3회 뒤집은 통제)
  (f 부모)trailer有store無 & trailer無 = byte-identical(프로덕션 봉인) (g 부모)retention: 공학습 ckpt G0/ρ/form ≥ base−ε(실패=INVALID).
- **C1 검정력**: 셀당 n≥2048 · MDE≈0.031≤0.04 · 음성=preregistered TOST.
- **C2 통제군**(arm 당): **derangement** key-shuf ≤.55(순열 고정점누수 교훈 · 8slot 1/8 잔류로 floor 0.561) ·
  중립 store ≤.55 · λ0=byte-identical · wrong-store flip-coh ≥.90.
- **P1**(`evaluate --store` · engine-native · seed{7,11} 합치): held-out 4셀 macro · 셀<macro−.05 ⇒ macro 무효.

| 결과 | 판독 |
|---|---|
| 🟢 | 303M GROWTH: macro≥.90 ∧ C2 4/4 ∧ C0-g ∧ 양seed → **다리 공학습으로 벌림 · TERMINAL 자격**(범위:합성). BOLT≤.60/seed-split 이면 "공학습 필수" 부명제 확정 |
| 🔴 conv-진범 | ladder COTRAIN 이 C0 VALID+C1 충족인 채 TOST chance ∧ v2-conv-trunk arm 도 실패 ∧ v2-transformer 통과 → substrate 진범 |
| ⚪ | C0 INVALID/seed-split/retention 실패 = 재계기, 판정 아님 |

## 단계 (owner-go 지점 명시)

| 단계 | 내용 | 비용 | go |
|---|---|---|---|
| **S0** 배선 smoke | corpus fmt + CLMS trailer + `--store` eval + VERSION bump → toy.clm passthrough byte-identical·ORACLE 배관·직렬화 왕복 | $0·mini | 자율 |
| **S0.5** substrate 대조 | v2 하네스(rule-exempt)에 conv trunk 끼워 동일과제(transformer vs conv 분리 · DIRECTIONAL) | $0 | 자율 |
| **S1** ladder 본선 | pool 기존 GPU 소규모 conv COTRAIN(scratch+growth)+BOLT · C0→C2→P1 전배터리 · floor 실측 = go/no-go | pool(rent 아님) | 자율 |
| **S2** 303M growth | py303_full 이어학습 · GPU pod **rent=spend** | fleet | **owner go** |
| **S3** TERMINAL | `evaluate --store` heavy 303M = pool(mini 금지) · ckpt teardown 전 회수 | pool | 자율 |

**S1 🔴 ⟹ S2 미발사**(ladder 죽인 걸 스케일이 살린 전례 0 · scale=증폭기).

## 잔인한 판정 (최대 리스크 = 기술 아니라 해석)

1. **"어텐션 밀수"**: softmax store lane 성공 = "conv 고친 게 아니라 미니-transformer 붙였다" 독해 가능.
   방어 = arm 분리(lane-주입 vs conv-내부주입 vs v2-conv-trunk 대조 S0.5) — lane ✅ ∧ conv-내부 ❌ =
   RF/국소성이 스트림-내 binding 진범, lane 이 정당한 우회. **이 arm 없이 lane 만 쏘면 성공해도 해석불능.**
2. **답-위치 파싱 버그** = 조용한 계기사망(v2 5연발 계급) → ORACLE 을 S0 부터 배관(유일 조기검출기).
3. **block 순환 희석**: block 내 반복노출이 조회 대신 window-국소 암기(복사)를 가르침 → **block 내 개체당 1라인
   preregister**(window 복사원 제거). 빼먹으면 P1 양성이 in-window 복사로 오염 = 가장 조용한 함정.
4. **retention vs 조회형성 트레이드**: 재생비중↑=CPT파괴 막되 다리 grad 희석 → S1 에서 스윕·동결(303M 스윕=tune-to-green 냄새).
5. **🟢 도 G1 종결 아님**: 합성 store · 자연전이·쓰기경로(누가 store 채우나 · 지금은 manifest 외부주입)가 다음 벽.
6. **--store-mix 혼동 방어**: 출력-port actuator(H_9392 forward 이후 산수) vs 본설계(forward 내부·공학습·.clm 직렬화)
   경계 명기 — 경계선 = "게이트·융합 파라미터가 gradient 로 벌렸는가, .clm 안에 사는가".

## NEXT

~~S0 배선 smoke~~ **DONE**(CLMS lane 배선·$0 검증) → **S0.5 substrate 대조**(v2 하네스 conv trunk) → S1 ladder(pool COTRAIN+BOLT · go/no-go) → S2 303M(owner go) → S3 TERMINAL.
S1 진입 전 필요: CLMSModule 학습 배선(`cli/train.py` 가 block store manifest 로 CLMS lane 공학습 · 답위치 store_only) + replay 도입 시 `=> ` 트라이그램 스캔 게이트(Fable §E).
