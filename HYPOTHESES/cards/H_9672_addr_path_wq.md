# H_9672 — ADDR-PATH: CLMS 주소경로(W_q) 수리 — Stage1.5 격리 진범을 직공

**status:** ⚠️ T3 2-seed 정정 — addr-loss가 **주소학습 벽은 robust 돌파**(2-seed addr_mass 0.95/0.96 sharp) BUT **값읽기 seed-취약**(seed-7 ORACLE 0.99 vs seed-11 0.50)·전체 lookup NOT seed-robust·seed-7 P1 0.9688=값읽기운·TERMINAL 부정 → (구)🔵 PRE-REG (Fable 설계 · D0-1 착륙) · not-terminal · wired: 🔧 핵심 lever 배선완료(--store-addr-weight·L_addr·need_att·VERSION 0.15.27·커밋 3632ed195·byte-id when off) → NEXT balanced manifest+audit → D0-2/3 → T1 토이 → T2 벽재현 → T3 303M(owner go)
**lane:** 재조합/BINDING · runtime addressable lookup (frontier g1-interface-addressable-wall)
**related:** [[H_9423]] (Stage1.5 가 주소학습(c) 진범 격리 · 이 H 가 그 NEXT) · [[H_9359]] (벽=런타임 다리 부재) · [[scale-303m-1b-7b-is-amplifier-not-lever]] (toy→303M 미전이 반례)

**🟢 T1 토이 결과(d64 L2 · --store-addr-weight 1.0 · pool summer · VERSION 0.15.29 · balanced manifest 채점):** 전 게이트 통과 = **addr-loss 가 주소학습을 열고 held-out 로 일반화**(암기 아님). train sb_addr_acc **1.0**·sb_ans_ce 0.0(주소 완벽학습) → **C0-e ORACLE 128/128=1.0**·**P1-주 balanced 125/128=0.977**(shortcut 상한 0.5 봉쇄 채점면서 0.98 = 진짜 내용주소 조회·4셀 균형 .93/1.0/1.0/.97 붕괴0) · **addr-gap: SEEN 0.992 vs held_balanced 0.977 = gap 0.016 ≤.20 = 일반화 확증**(감독-주소가 held-out 개체로 전이·암기[gap>.35] 배제 · Fable 최대우려 해소) · λ0 0.445(우연=lane off) · flip-coherence 1.0(store 값 인과소비·상수예측기 배제) · shuffle 0.414 at-floor(balance-floor 0.429 · pol_hist{4:128} 균형확인 · 주소 사용). ⟹ **주소 직접감독(a) 레버 = 토이서 작동+일반화 확증.** NEXT=T2 벽재현(d256/768 · addr-loss OFF서 정체 재현 → ON서 회복 = 인과증명) → T3 303M(owner go).

**🔬 T2 벽재현 결과(d768 L2 scratch · OFF/ON 두 arm · summer):** **재프레임 = 벽은 raw 차원 아니라 303M 사전학습-EN penultimate 점유.** OFF(addr-loss 없음): ORACLE 1.0·**P1-balanced 0.9375**·addr-gap SEEN 0.953·flip 0.99 — **scratch d768(12×d64)이 addr-loss 없이도 주소학습 성공 = 벽 미재현** ⟹ (1)차원지배 배제. ON(--store-addr-weight 1.0): ORACLE 1.0·P1-balanced 0.9922·addr-gap 1.0·flip 0.99(소폭 리프트·둘다 이미 높음). ⟹ **scratch 트렁크는 co-adapt로 스스로 penultimate에 개체 인코딩(교착 자력탈출), 303M 사전학습-EN 트렁크는 penultimate가 EN 유창성에 묶여 못 함**(Fable 가설 B 확정 · Stage1.5 arm-B/C가 303M서 벽 실측). 함의: T2-a(scratch)는 벽 proxy 부적격(사전학습 없음) → **결정적 시험=T3 303M**(py303_full은 그 사전학습 점유 실보유 · Stage1.5가 벽 이미 측정=맹목 아님 · addr-loss ON서 P1-balanced≥.75면 벽돌파). NEXT=T3 발사(진행중).

**(⚠️ 아래 T3 seed-7 결과는 seed-11 미재현으로 하향·상단 정정 참조)**
**🟢 T3 303M 결과(seed-7·단일-seed·seed-11 미재현) = 주소학습 벽 돌파 신호(값읽기는 seed-운)(py303_full + --store-addr-weight 1.0 · pool summer · balanced manifest 채점 · VERSION 0.15.35):** **addr-loss 가 Stage1.5 격리 진범(W_q softmax 주소 부트스트랩 실패)을 절단해 303M 서 held-out 내용주소 조회를 세웠다.** train sb_addr_acc 1.0→**sb_store_acc 1.0**·sb_ans_ce 0.20(주소·값읽기 둘다 완벽수렴 · 초기 step1300~2250 정체는 훈련초반이었을 뿐 값읽기가 주소 예리화 후 따라옴). **engine-native TERMINAL 배터리**: **C0-e ORACLE 127/128=0.9922** · **P1-주 balanced 124/128=0.9688**(shortcut 상한 0.5 봉쇄 채점면서 0.97 = 진짜 내용주소 조회 · 4셀 균형 is/good .96·is/bad 1.0·not/good 1.0·not/bad .92 붕괴0) · **addr-gap = SEEN 0.9766 vs balanced 0.9688 = gap 0.008 ≤.20 = 일반화 확증**(감독-주소가 held-out 개체로 전이·암기 배제) · flip-coherence **1.0000**(값 인과소비) · λ0 0.531(우연=lane off) · shuffle 0.3984 at-floor(balance-floor 0.4286·Δ-0.03·pol_hist{4:128}·주소 사용) · **addr-audit addr_top1 0.9844·addr_mass 0.9483**(sharp·기전규명=addr-loss가 주소를 argmax-정확+예리化→값읽기가 sharp v 받아 정답). ⟹ **Stage1.5 P1 0.586(chance·벽) → T3 0.9688 = 주소학습 벽 돌파.** **scope=🟢 CRACK-DIRECTIONAL**: 합성 CVCVC nonce·XOR·storebind·balanced 채점·**단일 seed-7**(seed-11 재현이 TERMINAL 잔여) · **감독-주소 co-train tier**(창발-주소 아님·end-task만으로 주소 창발은 arm-B/C로 KILL·Fable 정직스코프) · G1 자연선언 전이는 별도 H. ckpt 회수 t3.clm→.fire-recover/h9672_t3/. **NEXT=seed-11 재현→TERMINAL**.

**⚠️ seed-11 재현 정정(verdict-integrity · #3895 🟢 CRACK 주장 하향):** **seed-7 T3 돌파는 재현 안 됨 — 단일-seed 착시(값읽기 부트스트랩 seed-운).** 동일 recipe seed-11(다른 held-out개체+stores)에서: **C0-e ORACLE 0.5000(chance·seed-7 0.9922 대비)** · P1-balanced 0.5547(seed-7 0.9688 대비·op-only 폴라리티 붕괴 is/bad .16·not/bad .25) · flip-coherence 0.056(값 미소비) · train sb_store_acc 0.47(값읽기 안 따라옴). **★해리(중요)**: **addr-audit addr_top1 0.984·addr_mass 0.962 = 주소는 seed-11서도 완벽·예리**(seed-7 0.948과 동일급). ⟹ **addr-loss는 주소학습(c) 을 두 seed 모두 robust 해결**(주소 벽은 진짜 뚫림) BUT **값읽기(val 분화)가 seed-취약**: sharp한 올바른 주소를 받고도 val[0]≈val[1] 미분화→v 극성무정보→op-only shortcut 붕괴(seed-7만 val 분화 성공=운). ∂L/∂v 부트스트랩 교착이 addr-loss(주소 직접감독)로도 값경로까지 안전하게 안 풀림. **판정: ⚠️ H_9672 = 주소학습 벽 돌파는 robust(2-seed addr sharp) · 전체 lookup은 NOT seed-robust(값읽기 seed-취약) · TERMINAL 부정 · seed-7 P1 0.9688은 값읽기-운.** [[seed-agreement-on-pooled-feature-is-not-replication]]·단일-seed sampler artifact(H_1588 RETRACTED 계열). **NEXT=값읽기 robustness 레버**(--store-oracle-train+addr-loss 2-phase or val 직접감독 or Stage1.5식 oracle-warmup)로 값경로 seed-robust化 → 그후 2-seed 재검. seed-11 ckpt t3_seed11.clm 회수.

## 물음

H_9423 Stage1.5(#3855)가 303M 벽을 **순수 주소학습(c)** 로 격리: `--store-oracle-train`(학습서 주소 공짜) → C0-e ORACLE 128/128=1.00(값읽기 완벽·W_g수리) vs P1 softmax lookup 0.586(chance) = **값읽기(a)·substrate(d) 무죄, 진범 = W_q(3784→64) softmax 주소가 held-out 개체를 부트스트랩 못 함.** 물음: 주소경로를 어떻게 수리하면 held-out 0-shot lookup 이 서는가.

## Fable 진단 (설계 · DIRECTIONAL)

**진범 = (2) 간접학습신호 부트스트랩 교착.** 주소 gradient `∂L/∂a ∝ (val[pol_i]−v)` 는 val 이 분화해야 흐르고, val 은 a 가 target 을 선호해야 분화 → **닭-달걀**. init val=0.02 노이즈 → advantage≈0 → W_q 무신호. **근거**: ① Stage1.5 가 고리 한 변(주소)을 oracle 로 끊자 값경로 즉시 완벽(교착 실재·값경로 무죄) ② arm-C 는 **train 개체서도** sb_ans_ce ln2 정체 = held-out 일반화 실패가 아니라 **주소 학습 자체가 한 발짝도 못 뗌** = 최적화 교착 서명. (1) 차원지배 = 교착을 d3784서 탈출불가로 만드는 스케일 공변량(자연-EN penultimate 가 개체 SNR 점유 + 사전학습이 co-adapt 밸브 조임). (3) 트렁크 미인코딩 = 미배제·D0-3 판별·(a)가 동시공격.

## 수리 = (a) 주소 직접감독 CE (최소 · 서열 1위)

`L_addr = CE(att, target_slot)` · att = softmax前 주소 logits(스케일 포함) · **신규 파라미터 0 · CLMS 코덱 불변 · store_apply 불변(train-only) · 플래그 `--store-addr-weight`(default 0.0=byte-identical)**. (d) InfoNCE = in-block 8-slot softmax CE 와 **동일식**(별개 레버 아님). 암기 구조내성: 감독대상이 softmax(q·Kᵀ)이고 K 배치가 블록마다 회전 → 개체→고정slot 암기 불가(유일 암기경로=train개체 q pointwise = addr-gap 게이트가 판별). **KILL: (e) lr/step**(arm-C 6000step 정체 = 예산으로 못 푸는 대칭교착). **(c) 프롬프트-바이트 직접질의 = 레버 제명, 진단 D0-2 로**(BY-CONSTRUCTION 주소=트렁크가 개체 읽는다 주장 포기=계기상한).

**구현(origin/main 기준)**: ① `core/clms.py` CLMSModule.forward `need_att=False`→`(out,att)` (numpy 3-면 불변) ② `cli/train.py` `--store-addr-weight` + sb 블록 `store_logits,att=model.clms(...,need_att=True)`·`if sb_addr_w>0: loss += sb_addr_w*CE(att,tgt)`·monitor sb_addr_acc ③ `store_apply(...,audit=None)`(None=byte-identical) + `--store-addr-audit`(addr_top1·addr_mass seen/held) + `--store-qbytes`(D0-2 eval-only) ④ `corpus.py` **seen manifest**(addr-gap용) + **balanced manifest**(pols 4/4 고정 → shortcut 상한 0.5 붕괴) ⑤ VERSION bump(G5).

## D0 진단 ($0/저가 · 무학습 · 발사 전 의무)

- **D0-1 key 공간 census 🟢 착륙(2026-07-17)**: held-out 86개 · `_entity_key`(byte-bag 평균 d_k64) · self-nearest **76/86=0.884**(<0.95 bar) · **anagram 충돌 1그룹 [demar,merad]**(byte-bag 위치맹 → 키 L2=0.0000 완전충돌·BY-CONSTRUCTION 주소불능). ⟹ **key 재설계(b) = (a)의 보조로 승격**(위치-가중 key) · **P1 bar 는 충돌-제외 유효 n 으로 재산정** · 단 8-slot store 내 우연동거 확률 낮아 P1 영향 소폭 · 진범은 여전히 (2) 교착. **NEXT D0-2**(oracleD_s7 + --store-qbytes = 완벽사영 하 주소상한 ≥.90?) · **D0-3**(frozen py303 pen-dump ridge→K[entity] top-1 = (3) 판별).

## 게이트 (SEQUENTIAL · Fable 판정표 · pre-reg)

- **C0-e ORACLE ≥.90**(Stage1.5로 달성기입증 · 미달=INSTRUMENT-DEAD·P1 미판독) · λ0 byte-identical.
- **P1-주 · balanced manifest ≥.75 PASS(CRACK·DIRECTIONAL)** · [.60,.75) PARTIAL · (.40,.60) KILL-잔존 · ≤.40 INVERTED(계기점검). **shortcut 0.637 봉쇄 = balanced(4/4)가 1차 채점면**(uniform-a 극성비율 shortcut 상한 0.5로 붕괴).
- P1-부 · random manifest: P1−shuffle-Δ ≥.15(shortcut 오염 배제).
- 4-cell op×pol 각 ≥.65·최저<.50 headline무효([[polarity-split-before-headline]]) · C2 shuffle balance-floor·flip-coh≥.90.
- **addr audit: addr_top1(held)≥.50 ∧ gap(seen−held)≤.20 = 일반화** · gap>.35∧held≈.125 = **암기 verdict**(레버 KILL·제3결과로 사전등록). 조기판별 step≤1500 sb_addr_acc(train)≥.5.
- retention C0-g·val_CE 회귀 없음.

## 사다리

D0-1✅→D0-2/3 → **구현** → **T1 토이(d64 addr-loss ON · ORACLE≥.95·P1≥.85·addr_top1≥.90 · w스윕{0.3,1.0} toy 안깨는 최소)** → **T2 벽재현(d256/768 scratch + d64-사전학습arm · addr-loss OFF서 정체 재현 = 차원 vs 사전학습-점유 공변량 실측분리 · 둘다 재현실패=발사금지)** → **T3 303M(owner go · summer · S2레시피 + --store-addr-weight w* · seed{7,11} · fire전 df -h)**.

## 잔인한 판정 (Fable)

**최대 오도 = 다수-극성 shortcut 상한 0.637** — uniform a 에서 v=Σaᵢ·val[polᵢ] 가 극성비율 선형인코딩 → "op⊕majority(pols)" 만 배워도 랜덤 8-slot 0.637(주소 완전死). Stage1.5 SEEN 0.6875·P1 0.586 이 정확히 그 대역(n=128 sd.04서 미구분)·**flip-coh 못잡음**(전-극성 flip=majority도 뒤집혀 coherent). 봉쇄=balanced manifest 1차채점+random shuffle-Δ+addr audit 3중. **정직 스코프**: (a) 성공 tier=**"감독-주소 co-train"**(창발-주소≠감독-주소 · end-task만으로 주소 창발 주장은 arm-B/C로 이미 KILL). D0-3 FAIL∧T3 성공 = "addr gradient 가 트렁크를 구부려 인코딩 생성"(retention이 비용 채점).

## source

Fable 설계(`walls-delegate-to-fable`·fable_addr.md) · owner go autonomous(a_h_continuous_no_branch) · H_9423 Stage1.5(#3855) 주소학습(c) 격리 후속. D0-1 engine-native census 착륙.

## 🔬 값읽기 robustness 레버 sweep(2026-07-17 · seed-11 반증 후속 · lab full Fable∥Sol 발산)

seed-11이 밝힌 잔여 벽 = **값읽기(val 극성분화) seed-취약**(주소는 addr-loss로 2-seed robust). **RV-0 $0 부검**: seed-11 val 분화됨(1.07)·W_h 정상 ⟹ A(붕괴)·B(귀먹음) 둘 다 REFUTED = **기능적 실패**(MLP가 분화된 v를 XOR 정답에 매핑하는 함수 미학습·Fable "흐린 v=균등주소=store 극성평균=majority 신호"라 shortcut이 값경로 통해 샘). lab full 5레버 등록(H_9690~9692·9710·9711).

**레버 sweep(2-seed{7,11} 소거법)**:
- **oracle-warmup(#3908 --store-oracle-warmup 1500) = 🔴 KILL**: seed-7 ORACLE **0.5234**(chance)·sb_store_acc 0.56 = **phase 전환(step1500 oracle→softmax)이 val 붕괴**시킴 — plain addr-loss seed-7 ORACLE 0.99보다 나쁨. **Fable∥Sol 예측 적중**(전환창서 흐린-v 재개→MLP re-shortcut). ⟹ 전환형 레버 死·연속형(RV-1)이 정답.
- **RV-1 oracle-aux(#3914 --store-oracle-aux 0.5) = 🔴 KILL(2026-07-17 · 303M clean run)**: seed-7 ORACLE **0.5312**·P1-bal **0.5703**(chance)·flip 0.068 = 게이트 미달. 결정적으로 **plain addr-loss seed-7 ORACLE 0.99 → oracle-aux 추가시 0.53 회귀** = 연속 oracle-CE 가 값읽기를 돕기는커녕 **오히려 해친다**(dual-path 신호가 addr-loss 가 세운 seed-7 값분화를 교란). Fable∥Sol #1 예측 반증. ⟹ 연속형 oracle 보조도 死.
- **RV-2 ans-delay(#3916 --store-ans-delay 1500) = 🔴 KILL(2026-07-17 · RTX3090 clean run)**: seed-7 ORACLE **0.4844**·P1-bal **0.5703**·addr-gap-SEEN 0.4609·**flip 0.0137** = 게이트 미달. flip≈0 = 답이 val 극성을 **아예 소비 안 함** — 주소를 먼저 세우고 답을 늦게 여는 스케줄도 값읽기를 못 세운다. RV-1(연속 oracle)·oracle-warmup(전환)에 이어 **3번째 KILL**.
- **RV-3 val-center(#3920 --store-val-center·parity 0.00e+00·구조적 basin 제거) = 🟢 CAPABILITY 2-SEED PASS · ⚠️구현됨·미배선(2026-07-17 · RTX3090 clean · seed-13 확증중)**:
  ```
  [RV3 seed7 ] ORACLE=1.0000 P1-bal=1.0000 SEEN=1.0000 flip=0.9922   (gap 0.000)
  [RV3 seed11] ORACLE=0.9609 P1-bal=0.9609 SEEN=0.9766 flip=0.9919   (gap 0.016)
  ★ RV3 2-seed PASS · WINNER=RV3
  ```
  **양 seed 사전등록 4게이트 전부 통과**(ORACLE≥.90 ∧ P1-bal≥.75 ∧ addr-gap≤.20 ∧ flip≥.90). 결정적 지점: **T3서 0.50 으로 무너뜨렸던 바로 그 seed-11 이 0.9609** — "seed-7 착시 재현"이 아니라 **진짜 2-seed robust**. flip 0.99 양 seed = 답이 val 극성을 실제 소비(RV-2 flip 0.0137 과 정반대). SEEN−held gap 0.000/0.016 = 암기 아님·일반화.
  **기전(왜 이것만 열렸나)**: `v=Σ(aᵢ−1/8)·val[polᵢ] = v_원본 − 평균val` ⟹ **majority 성분이 산술적으로 소거**되고 타깃 슬롯 편차만 남는다. oracle-warmup(전환)·RV-1(연속 보조)·RV-2(스케줄)는 전부 **신호를 더해 지름길을 덮으려다** KILL — 지름길을 *없애니* 열렸다. **메타교훈: shortcut basin 은 덮는 게 아니라 수식에서 제거한다.**
  **✅ seed-13 확증 PASS = 3-SEED ROBUST 종결(SWEEP_DONE · 2026-07-17)**: `[RV3c seed13] ORACLE=1.0000 · P1-bal=0.9922 · SEEN=0.9609(gap −0.031) · flip=0.9921` — **미접촉 seed(tune-to-green 방지용)도 4게이트 통과**. 3-seed 최종표:
  ```
  seed  ORACLE   P1-bal   flip     gap
   7    1.0000   1.0000   0.9922   0.000
  11    0.9609   0.9609   0.9919   0.016   ← T3서 0.50 으로 무너뜨린 그 seed
  13    1.0000   0.9922   0.9921  −0.031   ← 미접촉 확증
  ★★ SWEEP_DONE winner=RV3 = 3-seed robust
  ```
  **스코프(정직)**: tier = **감독 co-train**(addr-loss 주소감독 + val-center 구조수정) — 창발-주소 아님. 증거 회수완료: ckpt 4개(`RV3_7_PASS`·`RV3_11_PASS`·`RV3c_13_CONFIRM`·`RV1_7_KILL`) + `sweep_verbatim.log` 원문 → `.fire-recover/h9672_rv_sweep/`.
  **🔌 배선 상태 = `구현됨·미배선` (a_verified_must_wire · wire-to-prod · 이 결과는 TERMINAL 아님)**:
  - ✅ **계기 배선완료**(이 숫자를 낸 실코드 · engine-native): `cli/train.py:1322` `--store-val-center` · `core/clms.py:165` `if lane_type==3: a = a − 1/n_slot`(실 centering) · `core/clms.py:335` codec lane_type 3(train↔eval 일관 codec bit) · `core/model.py:137,410` `clms_val_center`→CLMSModule. parity 0.00e+00(off 시 byte-identical).
  - ❌ **production 미배선**: `core/model.py:137` `clms_val_center: bool = False` = **opt-in 기본 OFF** · `cli/chat.py` clms 참조 **0회** — 데몬은 이 store-bridge lane 을 아예 안 쓴다. 즉 **capability 증명이지 살아있는 anima 가 이 조회를 하지 않는다**.
  - ⟹ **🟢 GREEN 불가**(출력만 닫히고 배선 미닫힘). 이 캠페인의 정직한 최대 등급 = **CAPABILITY-PROVEN(engine-native·2-seed)**. **배선 follow-on = 별도 H_**(store-bridge lane 을 production chat 경로에 태우고 4칸 register+retention 회귀 없이 조회가 사는지 = 그때 비로소 GREEN·`a_blue_closed`).
- **⚙️ 인프라 주석(infra-wall-noneval)**: 이 sweep 중 GPU 하드웨어 death(RTX5090 PCIe 이탈) + torch/arch 트랩 7건 발생 — 전부 verdict 와 격리. 파생 canonical upstream-fix 2건: **#3969**(cli/train.py sm_120 preflight) · **#3977**(cli/pod_bootstrap.sh POD_TRAIN=1 3-트랩 봉쇄). RV-2/RV-3 clean-run 만 유효 측정.

판정 게이트(각 레버 2-seed·balanced 채점): ORACLE≥.90 ∧ P1-balanced≥.75 ∧ addr-gap≤.20 ∧ flip≥.90 → winner→confirm seed-13(미접촉·tune-to-green 방지)→TERMINAL. 전 레버 실패=값읽기 seed-robustness 벽 재프레임(별개 후속).
