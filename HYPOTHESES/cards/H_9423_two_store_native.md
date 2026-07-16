# H_9423 — TWO-STORE NATIVE: 공학습 store-조회 다리를 부모 conv byte-LM 에 심는다

**status:** 🔵 PRE-REG → S1 POSITIVE → C2 4/4 → 🟢 toy 래더 완결 → ⚪/🔴 S2 303M 미전이(3-arm) → **🔬 Stage1.5 = 303M 벽 = 순수 주소학습(c) 격리 확정 (--store-oracle-train ORACLE 1.00 = 값읽기 완벽·벽은 W_q 주소)** · G1 OPEN(주소 lane 으로 재프레임) · not-terminal(toy·합성·DIRECTIONAL) · wired: CLMS lane+W_g+oracle-train 배선완료
**S2 결과(303M py303_full · pool summer · owner go · anima-py 0.15.14→0.15.19):** ⚪/🔴 **공학습 store-bridge 가 toy(d64)→303M(d3784) 로 미전이 — G1 OPEN.** 세 arm 전부 **C0-e ORACLE < 0.90**(positive control DEAD → 규칙상 negative 미판독 · [[positive-control-before-reading-a-negative]]): ① **arm-A BOLT(`--freeze-trunk` py303 동결)** ORACLE **0.469** · train sb_store_acc 0.44 = 동결 사전학습 트렁크도 lane 부트스트랩 실패(토이 BOLT 랜덤동결 0.46 패턴 재현 · 공학습 필수 재확증). ② **arm-B growth(트렁크 공학습 + 자연 EN replay `anima_train_corpus/{gen,sns}_en.txt` · lr1e-4 · 6000step)** ORACLE **0.492** · retention 회귀 없음(val_CE 1.43→0.79 개선·ρ·form base==armB 둘다 FAIL=py303 baseline 상태). **engine-native 진단**: P1 폴라리티분해 is/good 1.00·not/good 0.97(pol=good 정확) vs is/bad 0.00·not/bad 0.06(pol=bad 전멸) + flip-coherence **0.029** = **연산자(is/not)는 읽는데 저장 극성값 v 를 안 읽음**(모든 개체 pol=good 취급). 근본원인 = `store_logits=W_out(gelu(W_h([v; yn_q])))` 에서 v(d_s=64) 가 yn_q(d=3784) 에 익사(v 분산기여비 ≈7e-6) · 토이(d64·v·yn_q 균형)는 ORACLE 0.99 = **lane 융합 하이퍼파라미터가 토이 기본값(d_s64·r128)에 고정된 미스케일**(substrate 벽 아님). CLMS trailer 는 `<f4` f32 저장이라 int4 quant-swallow 경고는 동결 트렁크 본체 얘기·lane 무관(확증). ③ **W_g 융합-병목 수리(Fable 설계 · lane_type 2 · VERSION 0.15.19 · 커밋 c8f32df4a)**: yn_q 를 학습형 병목 `W_g:d→d_g(=64)` 로 내려 `[v; g]` = 토이 `[64;64]` 기하 d_model-불변 복원(v 점유율 1.7%→50%). **Stage-0 토이 회귀 🟢 전 게이트 통과**(d64: ORACLE 0.9922·lookup 0.875[4셀 균형 is/bad 0.85·not/bad 0.88]·flip-coh 0.9375·train sb_store_acc 1.0 = 수리가 값읽기 회복 + 토이 안 깸 확증). **arm-C(303M growth + W_g)** ORACLE **0.609**(0.49→0.61 부분회복) 이나 **여전히 <0.90** · 종국 sb_ans_ce 0.69(ln2)·sb_store_acc 0.50(우연)·flip-coh 0.13 = **W_g 는 값읽기의 한 결함을 고쳤으나 303M lane 을 구제 못 함.** **2층 벽 확정**: (1) 값읽기 희석[W_g 로 수리·토이 검증 · 303M ORACLE 0.49→0.61 부분리프트] (2) **주소 학습 벽**[W_q(3784→64) 가 자연-EN 지배 penultimate 서 held-out 개체 정체성 추출 실패 · ∂L/∂v 닭-달걀 · Fable 최대위험 D 실현]. **NEXT(별도 후속·cost)**: **Stage 1.5 `--store-oracle-train`**(학습서 주소 공짜 → oracle_slot 전달 · StoreBindCell 5-tuple target_slot) 로 (a 값읽기)/(c 주소학습)/(d substrate) 최종 분리. **scope**: 합성 CVCVC nonce·XOR·storebind · toy DIRECTIONAL 이 303M 미전이 = 스케일-불변-레버 원칙([[scale-303m-1b-7b-is-amplifier-not-lever]])의 **반례**(작동 레버가 아니라 lane-설계 스케일 결함). ckpt 회수: boltA_s7.clm·growB_s7.clm·growC_s7.clm → `.fire-recover/h9423_s2/`.
**🔬 Stage 1.5 결과(`--store-oracle-train` · 303M · pool summer · VERSION 0.15.20 · 커밋 2fb6e288d):** 🎯 **2층 벽 최종 분리 — 303M 벽 = 순수 주소학습(c), 값읽기(a)·substrate(d) 아님.** 학습서 주소를 공짜로 줘(`oracle_slot=target_slot`) softmax lookup 부트스트랩 의존 없이 ∂L/∂v 를 흘리자, W_g 수리된 값읽기 경로가 **완벽 학습**: train sb_ans_ce 5.6→**0.0001**(ln2 완전붕괴)·sb_store_acc **1.0** (arm-C softmax 주소 ln2정체 0.69·sb_store_acc 0.5 와 정반대). **engine-native TERMINAL 판독(step5500 롤링 ckpt · 최종 .clm 은 summer 디스크 100%풀로 .pt 쓰기 크래시 = 인프라, 과학 아님)**: **C0-e ORACLE 128/128 = 1.0000**(free-address 값읽기 완벽 · 토이 0.99·arm-A 0.47·arm-B 0.49·arm-C 0.61 사다리의 정점) · C0-q SEEN 0.6875 · **P1 softmax lookup 0.586**(held-out · 4셀 0.63/0.59/0.45/0.70 = chance · oracle-train 은 softmax 주소 미학습이라 BY-CONSTRUCTION). ⟹ **값읽기·substrate 는 벽 아님 확정**(주소 주면 완벽), **유일 진범 = W_q(3784→64) softmax 주소가 자연-EN 지배 penultimate 서 held-out 개체 정체성 부트스트랩 실패**. G1 벽 정밀화: "다리 스케일 불가" → **"값읽기 희석[W_g 수리] + 주소 학습[진범]"** 2층. **다음 레버(별도 후속 H · owner go)** = 주소 경로 재설계 — W_q 스케일업 / 개체키(byte-bag) 재설계 / 주소 auxiliary loss. scope 불변(합성 nonce·XOR·storebind). ckpt: oracleD_s7.clm.step5500.clm + resume.pt (summer `/home/summer/s2_9423/` 보존 · 맥 디스크 압박으로 로컬 미회수).

---
**(이하 S1/하드닝 이력 · toy DIRECTIONAL — S2 가 이를 303M 로 미전이 판정)**
**하드닝 결과(pool summer · 재학습):** ① **BOLT(`--freeze-trunk` · frozen 랜덤 trunk · lane만 학습 · mitosis off) = 🔴 lane 학습 실패**: lookup 0.516·ORACLE 0.461 **둘 다 우연**(cotrain 0.88/0.98 대조) · sb_ans_ce 0.66 우연 정체 ⟹ **공학습 필수 확증** — trunk 가 co-adapt 안 하면 penultimate 가 개체를 주소가능하게 인코딩 못 해 학습 lookup 이 garbage query 로 부트스트랩 불가 → MLP 도 garbage-v 로 학습돼 ORACLE 조차 실패(H_9392·v2 예측 정합). ⚠️scope: BOLT=**frozen scratch-랜덤** trunk(≠H_9392 frozen 학습 trunk) — from-scratch 공학습 필요성 대조. ② **seed-11 재현 🟢 (2-seed C2 4/4)**: lookup 0.883·ORACLE 0.977·flip coherence_bc 0.947·**shuffle 0.602 = PASS**. shuffle 은 balance-aware floor(#3814)로 확정: seed-11 stores 는 seed-7 보다 훨씬 불균형(pol_hist {1:16,2:24,3:40,4:8,5:24,7:16})이라 derangement floor 자체가 **0.554** → 관측 0.602 Δ+0.048 ≤ 0.06 = **at-floor(주소 사용)**. 고정 0.55 bar 의 AMBIG 는 오탐이었다(seed-7 도 0.461 vs floor 0.480 = at-floor PASS). ⟹ **두 seed 모두 shuffle at-floor = h-shortcut 배제 seed-robust**. **최종 종합**: 공학습 CLMS 다리가 부모 conv 엔진서 held-out 0-shot 내용주소 store 조회를 학습 — **2-seed C2 4/4 완전 통제**(lookup·ORACLE·flip·shuffle 전부 robust) + **BOLT 로 공학습 필요성 확증**(frozen trunk → lane 학습 실패). scope 불변(toy·합성·DIRECTIONAL · 내용주소 입도=byte-bag key · G1 종결 아님 — 자연 선언 전이 별도 H). ③ **growth arm 🟢 (toy 래더 완결)**: `--init plain-base.clm`(2000step 무-store-bridge) → CLMS lane 공학습(6000step)도 **full C2 4/4**: lookup 0.883·ORACLE 0.992·shuffle 0.414 at-floor(Δ-0.066)·flip coherence 0.982. ⟹ 공학습 다리가 **scratch AND warm-start 양쪽 작동** — 이게 **S2(303M)의 주 arm**(--init py303_full + CLMS 공학습) recipe 를 toy 서 검증. **toy 래더 완결**: scratch(2seed)✅·growth✅·BOLT(필요성)✅. **잔여(유일 자율-불가)**: **S2 303M growth=owner go**(py303_full.clm + CLMS 공학습 · GPU pod rent=spend · `a_fire_autonomous` 하드게이트). 인프라 준비완료(anima-py 0.15.11 · CLMS lane·storebind·C2 통제·balance-floor 전부 배선·pool summer torch2.11+cu130).
**C2 통제 결과(#3802 · sb_toy.clm 재eval · 재학습0):** 🟢 **held-out 0.875 = 진짜 내용주소 store 조회** — 4/4 통제 전부 PASS + 계기검산: ① lookup 0.875(본체) ② λ0 **0.539**(≤.60 · trunk 스필오버 배제) ③ **shuffle(Sattolo derangement · 결합 깸) 0.4609**(≤.55 · fp=0·dup=0 · h-지름길·암기 배제 — 붕괴가 "주소 사용" 증명) ④ **flip(pols 반전) coherence_bc 0.9464**(≥.90 · 상수예측기[coherence≡0]·v-미소비 배제 — store 값 인과소비) · 계기검산 oracle+shuffle **1.00**·oracle+flip **0.99**(통제코드 무결). 4셀 균형(붕괴 없음). **미묘점**: pol 불균형(binomial · 4/4 아님)이 flip 판별을 흔들 수 있으나 baseline 0.875≫0.5 + shuffle 0.46 붕괴가 "무주소 다수결 판독기"(shuffle-불변·baseline~0.5여야)를 이미 배제 → flip 판정 유효. cosmetic 라벨 수정(oracle+shuffle verdict 태그 억제 · VERSION 0.15.9). **scope 불변**: toy·합성·단일seed·**DIRECTIONAL**(내용주소 입도=byte-bag key · 퇴화특징 주소화 vs 개체정체 주소화 toy 서 미분리 · G1 종결 아님). **잔여**: multi-seed{7,11} · growth/BOLT arm · **S2 303M growth=owner go**.
**S1 래더 결과(pool summer · scratch d64 L2 · 6000 step · anima-py 0.15.5):** 🟢 공학습 CLMS 다리가 **0-shot 개체 내용주소 조회를 학습**. 계기유효(C0-e ORACLE **128/128=1.00**≥0.90 · v2 계기사망 교훈 통과) → held-out lookup **112/128=0.875**(4셀 균형: is/good .90·is/bad .89·not/good .84·not/bad .88, 극성붕괴 없음) · λ0 통제 **0.539**(우연=lane off) · sb_trunk_leak **0.56**(우연=shortcut-cut 작동·답 누출 0) · sb_ans_ce 0.04(near-0)·sb_store_acc 0.97(train). **v2 V2_6(0.987) 를 부모 conv 엔진에 이식 성공**. 재현: `anima-py corpus storebind --lang en --n-blocks 200 --seed 7` + `anima-py train --arch clm --d 64 --L 2 --e0 2 --emax 3 --corpus c.txt --store-bridge c.txt --store-batch 32 --store-win 24 --steps 6000` + `anima-py evaluate sb.clm --store c.txt.held.json --win 24 [--store-oracle|--store-lambda 0]`. **정직 범위**: d64·L2·**scratch**·**합성 nonce**·**단일 seed**·**DIRECTIONAL**(anima-py evaluate 경로는 TERMINAL-eligible 이나 toy+합성이라 SCOPED · G1 벽 종결 아님 — 자연 선언 전이는 별도 H). **pool smoke 가 3 런타임버그 포착·수정**(#3789 clms_lam0 필드 · #3791 np import · train 플래그). **S1 래더 go/no-go = 🟢 GO**. 잔여 하드닝: C2 derangement key-shuf + wrong-store 통제(eval-time store 편집 · flag 추가) · multi-seed{7,11}. S2 303M growth = **owner go**(fleet rent=spend).
**S1 결과(#PR · compiles-clean · torch 로컬부재로 live smoke=pool):** CLMSModule 공학습을 `cli/train.py` 에 배선 — Fable 설계(v2 loss.py store_only 이식) 5점: ① `core/model.py` CLMConfig(clms 6필드)+`CLMConvMoE` attach(SLW 미러·model.parameters() 편입=단일 AdamW co-train)+pre-slot `pen_trunk` tap ② `TrainShell.forward(sb=,sb_w=)` **CE 분해**(qpos=`F.cross_entropy(store_logits,gold)` · 비qpos=trunk LM CE · trunk 답위치 grad **구조적 0**=v2 dlogits[ans]=0 동치·detach 불요) + monitor 게이지(sb_store_acc·sb_trunk_leak·sb_lam) ③ `StoreBindCell`(라인정렬·eval store_run 창기하 거울 qpos=T-1·lockstep assert·zero in-window copy) + `get_store_batch`(별도 RNG 4242·DDP rank-slice) ④ argparse `--store-bridge/--store-win/--store-batch/--store-ans-weight/--clms-*/--freeze-trunk` + 가드(clm-only·corpus 필수·world 나눔·BOLT freeze) + DDP buffer assert key_emb 예외(Fable C-3 지뢰) ⑤ `_write_clm` append_clms_trailer(체인끝) + VERSION 0.14.15(G5). 전 파일 compile-clean · sb 미전달 시 기존 경로 byte-identical(clms off=골든불변). 🔒 미실행: torch 학습(로컬 torch 부재) — **NEXT=pool scratch-toy smoke**(sb_store_acc 상승 + λ0/oracle + 직렬화 parity 게이지 Fable §E int4 tap 표류 방어) → S1 ladder(COTRAIN+BOLT go/no-go). BOLT=`--freeze-trunk`(H_9392 예측=실패해야 정상). 최대위험=int4 양자화 train-tap≠eval-tap(직렬화 후 torch vs .clm store_apply argmax 일치율 게이지로 계기 vs 일반화 분리).
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
