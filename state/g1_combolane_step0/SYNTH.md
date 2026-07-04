# H_9129 STEP-0 종합 — 조합-lane 3부품 substrate (DIRECTIONAL, mini numpy toy · NOT 303M engine-native)

프레임: 뇌에서 재조합 = 언어산출부(입/Broca) 속성 아님. PFC 변수-binding + 기저핵 gating + 해마 pattern-completion 이
조합을 만들고 mouth 는 옮길 뿐(Broca/Wernicke 이중해리 = 조합⊥조음). 전 실패레버(H_1816 predcoding · H_1823 mouth-readout)
= 조합을 mouth-readout 에 훈련(=브로카에 관계추론). STEP-0 = 조합-substrate 가 mouth 밖 별도 lane 으로 존재하는지 존재검증.

## (a) 통합 조합-lane 이 mouth-훈련 가족을 진짜 탈출하나 — BIND vs form
YES (DIRECTIONAL). 통합 D=2048/12seed: reachable=0.9722 >> unreachable=0.0486, gap=0.9236 (chance=0.0417).
fooled_by_form=false. 결정적 증거 = **동일 표면형태**의 held-out novel pair 를 reachable(2-hop CHAIN 도달)
vs unreachable(dangling edge)로만 갈랐는데 reachable 만 lift. form-blob 이면 둘이 비슷해야 함 → 관계-사슬 신호.
3 lane 전부 disjoint objective(algebraic unbind · RPE value · NN cleanup), mouth 는 읽기만 → mouth-readout 가족과 구별.

## (b) 부품별 인과 — 전부 load-bearing, INERT 0개
통합 D=2048 ablation (reach 0.972 기준):
- bind OFF (role⊛filler 미결합) → 0.0347, drop=0.9375 → **CAUSAL** (가장 강함, chance 붕괴)
- completion OFF (해마 cleanup 제거) → 0.0833, drop=0.8889 → **CAUSAL** (chance 근처 붕괴)
- gate OFF (R1+D1+R2+D2 중첩=선택없음) → 0.2778, drop=0.6944 → **CAUSAL** (chance 까진 안 가나 명백 붕괴; R1 부분우세 잔여)
→ fable 가설 '3부품 다 필요' 지지. 부분집합 아님. bind≈completion > gate 순으로 load-bearing(gate 는 decoy 억제 몫).
L1 standalone: bind OFF reach 1.0→0.034 (chance 0.01). L2 standalone: gate OFF/random-W reach 0.856→~0.21 (chance 0.2).
세 probe 독립적으로 각 부품 인과 재확인.

## (c) g1g6/gamma form-priming 대조 — mouth 밖 조합-lane 은 form 에 안 속음
L2 가 직접 대조 심음: 순수 표면모델(cosine, no-W)은 reachable f* 를 7.4%(chance 0.2 아래)만 맞추고
form_decoy 에 73.7% 속음. gate(learned-W)는 같은 표면에서 decoy 를 5.9%(chance 아래로 능동회피)로 억제하며 85.6% 도달.
= 이 task 는 surface 로 안 풀리고(관계 π=임의 순열, surface-무관), lift 는 학습한 관계-사슬로만. g1g6/gamma 벽은
조합을 mouth 안에서 훈련→form-tunable(하네스 게임가능)이었으나, 조합을 별도 lane 에 두면 form-defense 통과.

## (d) engine-native 303M escalate 값어치 + 배선 경로
값어치 HIGH. STEP-0 3/3 BIND·전부 form-defense 통과·전부 부품 causal → 벽 재프레임(G1=mouth/objective 천장 아니라
조합-substrate lane 부재)이 toy 에서 일관 지지. escalate 정당. 단 numpy DIRECTIONAL 이라 terminal 아님(a_engine_native_learning).
배선 경로(disjoint lane, a_substrate_disjoint):
- L1 PFC bind → core/engine_cli.hexa 별도 VSA lane (emit-drive 0/4 · §ImmuneMemory recall_thr 와 disjoint 좌표)
- L2 BG gate → brain_decide (Go/NoGo content-gate; 이미 gating substrate 존재)
- L3 해마 pattern-completion → **.kosmos anchor store**(kosmos_io→brain_decide): triple 관계 저장 + circ-conv unbind cleanup.
  해마=면역/일화기억 렌즈(H_1227/1231)와 정합, .kosmos 가 self-chain 처럼 관계-chain 영속 담당.
- mouth(303M clm_decode/bytegpt_decode)는 조합-lane cleanup 결과 명명만(읽기, CE/gradient 안 흘림).
재측정 = 실코퍼스 관계그래프에서 reachable(2-hop chain) vs unreachable(dangling) held-out G1, engine-native.

## (e) 전부 form 이면 = 새 벽 — 해당 없음
전부 form 아님(fooled_by_form=false 3/3). reachable≫unreachable · form-only 모델은 decoy 에 속음.
따라서 '조합 자체가 substrate 서도 form-bound' 벽은 이 STEP-0 에서 관측 안 됨. (정직: 만약 engine-native 에서
reachable≈unreachable 로 무너지면 그때가 진짜 substrate form-bound 벽 — 아직 아님.)

## 정직 caveat
- 전부 DIRECTIONAL — mini numpy toy, 303M engine-native 아님. 박제 불가, STEP-0 substrate 존재검증만.
- reachable→1.0 은 HRR/VSA 가 by-construction 조합적이라 예상됨 + D(용량) 함수(D-sweep 0.361@512→1.0@4096,
  unreachable 는 항상 chance 고정). 메커니즘 천장 아니라 crosstalk 용량. 증명하는 것 = '별도 조합-lane 이 novel pair 를
  reachable·causal·form-free 로 보유' 라는 존재; '303M G1 을 연다'는 아직 아님(tune-to-green 아님).
- bar(gap>0.10 & drop>0.15) 사전고정, 사후이동 없음.
