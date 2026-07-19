# H_9675 — SEED-11 WRITE UNDER-IMPRINT: base-ckpt 용량 vs 코퍼스 간섭 (root-cause)

- **group**: g1-interface-addressable-wall
- **tier**: 🧱 CRACK-FRAGILE / NOISE (6-draw sweep · pod-fired · engine-native) — H_9339 s7 crack 은 draw-인공물: fresh held-out 어간 draw **2/6 만 PASS**(frozen bar ≥4/6 미달). write 프로토콜은 작동(G-WRITE 11-12 항상·SEEN intact)하나 연산자 readout 이 draw-fragile. rider(base 무죄→C)와 정합. H_9327 BINDING 벽 held-out write 로 견고히 미돌파.
- **date**: 2026-07-17
- **related**: [[H_9339]] (모 crack — s7 단일seed 착시) · [[H_9327]] (BINDING 벽 — 재봉) · [[H_9672]] (자매 lane · READ/W_q 주소)
- **wired**: engine-native (anima-py train/evaluate · vast pod 6-draw sweep + rider · 결과 HF `dancinlab/anima-natem-c34-base` h9675/)

## 질문
H_9339 는 담체키 held-out write 로 H_9327 BINDING 벽을 **seed 7 에서 뚫었다**(HO-CARRIER 12·11/12
vs HO-DECL 5/12 · G-WRITE 11/12). 그러나 **seed 11 은 2 독립 run 모두 G-WRITE 미착륙**(6/12·4/12<11)
= seed-DETERMINISTIC INVALID. $0 대조(#3868)가 진범을 **stem-draw 아닌 RUN/seed** 로 좁혔다: 어간
`튼튼하`(9B)가 s7·s11 swap set 둘 다 존재 — s7 run 착륙·s11 run 실패(byte-len 무관, s11 실패 3~9B 산개).
⟹ `carrier_s11` CPT run 이 **어간 무관하게 담체 write 를 전역 under-imprint**.

**남은 물음 = 왜 seed-11 CPT run 이 under-imprint 하나?** 두 후보:
- **(A) base-ckpt 용량**: base `natem_c34_main_s11.clm`(다른 split-seed pretraining)이 s7 base 보다
  write-imprint 용량이 낮다.
- **(B) 코퍼스 간섭**: s11 held-split 이 뽑은 12 어간의 배열/구성이 imprinting 을 방해한다.

## 🔀 자매 lane 대조 — H_9672 READ/W_q 주소돌파 (#3895 · a_parallel_session_compare)
같은 프런티어의 **다른 lane** 이 병렬 착륙: H_9672 T3 303M 🟢 CRACK-DIRECTIONAL — `--store-addr-weight`
(직접 주소감독 L_addr=CE(att,target_slot))가 W_q softmax 부트스트랩 닭-달걀 교착을 절단해 held-out
내용주소 **조회(READ)** 를 세움(P1-balanced 0.9688·addr-gap 0.008 일반화·ORACLE 0.9922).
- **🟢 AGREES(강함)**: 둘 다 addressable-wall 의 🟢 CRACK-DIRECTIONAL · 둘 다 supervised/engineered(창발 아님)
  · **둘 다 TERMINAL 게이트 = seed 재현성**(H_9672 NEXT=seed-11 재현 ⟷ 본 H 재현성-sweep). 재현성이
  프런티어-정답 bar 임을 독립 수렴으로 상호검증.
- **🆕 NOVEL(상보)**: H_9672=**읽기**(W_q 조회) · 본 H_9339/9675=**쓰기**(held-out 항목 각인) = "addressable"
  의 두 반쪽. 비중복.
- **⚠️ caveat(진범 합치기 금지)**: base 가 다르다 — H_9672=py303_full+addr co-train seed · 본 H=natem_c34_main
  pretraining **split-seed**. "둘 다 seed-11 잔여"를 공유 진범으로 합치면 **다른 seed 축을 혼동**(seed-agreement
  ≠ replication). 본 H rider(A base-capacity)가 natem-s11 을 겨눌 뿐, py303 addr-seed 와 별개.

## 🧱 최종 VERDICT — 6-draw sweep = crack NOISE/FRAGILE (2026-07-17 · vast pod · engine-native)
사전등록 4-draw sweep = 🟠 2/4 MIXED → 사전등록 확장 4306-7(bar ≥4/6) → **최종 2/6 PASS = 🧱 crack
NOISE/FRAGILE**. 전 6 draw valid(pregate 어간 ≤7·G-WRITE ≥11·SEEN preserve ≥10)·INVALID 0.

| draw | HO-CARRIER negL/negZ | G-WRITE | HO-DECL | margin | 판정 |
|---|---|---|---|---|---|
| d4302 | 11/11 | 12/12 | 4 | 7 | 🟢 PASS |
| d4303 | 10/10 | 12/12 | 7 | 3 | ⚪ (margin<4) |
| d4304 | 9/7 | 11/12 | 7 | 0 | ⚪ (negZ<10) |
| d4305 | 12/11 | 12/12 | 6 | 5 | 🟢 PASS |
| d4306 | 10/8 | 12/12 | 4 | 4 | ⚪ (negZ<10) |
| d4307 | 9/9 | 12/12 | 7 | 2 | ⚪ (margin<4) |

**해석**: H_9339 의 s7 "crack"(12·11/12)은 **유리한 held-out 어간 draw 인공물** — fresh draw 6개 중 2개만
frozen PASS bar(HO-CARRIER negL·negZ ≥10 ∧ margin(−HO-DECL) ≥4) 통과. **write 프로토콜은 실재**(6/6 draw
서 G-WRITE 11-12 착륙·SEEN 연산자 intact = 담체키 write 는 held-out 항목에 항상 새겨짐), 그러나 그 항목의
**연산자 readout 이 held-out 어간에 draw-fragile**(negZ·margin 이 어간셋별로 편차). ⟹ **H_9327 BINDING 벽은
held-out write 로 견고히 뚫리지 않음** — 1-seed positive 는 sweep 이 벗겨낸 착시(precedent H_1588 RETRACTED
계열). frozen-first·no-tune-to-green 이 지킨 정직한 negative.

### 🔬 draw-fragility 기전 정제 ($0 per-stem 재분해 · 6 draw 전부 base s7 고정)
"왜 2/6 만 crack" 을 per-STEM 으로 분해(6 draw 모두 동일 base s7 이므로 base·seed 통제됨). ≥2 draw 에
등장한 25 어간의 carrier readout(negL∧negZ) 일관성: **CRACK-always 13 · FAIL-always 2 · MIXED 10**.
MIXED = **같은 어간이 같은 base 서 draw 별 crack↔fail 뒤집힘**(예 `편하`✓✓·· · `예쁘`✓··✓ · `튼튼하`✓·).
base·어간 동일한데 갈리는 유일 변수 = **draw 내 co-train 어간 구성** ⟹ **draw-fragility = 어간 간
compositional 간섭**(60% 어간-intrinsic 일관 + 40% company-의존). draw-level PASS 는 12어간 조합서 창발 —
단일 어간의 write 능력이 아니라 batch 내 경쟁이 readout bar 통과를 결정. #3868(stem-draw 배제, base 간)
+ 이 분석(draw-composition, base 내) = 진범이 **어간 능력 아닌 co-train 간섭**임을 두 축에서 확증.

### rider (별도 판독 · A/C dissociation)
s7-winning corpus 를 **s11 base** 에 CPT → **G-WRITE 12/12 착륙** ⟹ (A) base-capacity 반증·**s11 base 무죄**.
H_9339 s11 실패는 **run/corpus-randomness(C)** — 위 6-draw draw-fragility 와 정합(seed·draw 별 readout 변동).
$0(#3868 stem-draw 배제) + rider(base 무죄) + 6-draw(draw-fragile) = 진범 **(C) run/draw-randomness** 수렴.

### 인프라 (infra-wall · science 무관 · 격리)
vast pod 6개 발사서 4 infra-wall 격리·해결: ① 일부 pod CUDA 드라이버 too old(<cu13 torch)→CPU 폴백 60배
→GPU 정상 pod 마이그레이션 ② HF pull 부분다운(.cache/curl 중단)→sha게이트 ③ 일부 host HF 176MB 전송
flaky→단일 good pod 재배치+코퍼스 pod-재빌드(deterministic) ④ driver 거짓-DONE(출력삼킴·상대경로)→hard-verify
driver v2. 전부 verdict 에서 quarantine. 판정기도 결함 자수정 2건: 미완=NO-VERDICT(거짓 NOISE 방지)·6-draw bar.
비용 ≈ vast 6 pod × ~$0.3-0.56/hr(순차/병렬 혼합).

## 설계 (Fable 5 확정 · FROZEN — bg ba13m22pn 회신)
**Pivot = 재현성 sweep(2×2 아님) + 1-run root-cause rider.** 근거: 프런티어의 산 질문은 "s7 crack 이
real 인가"이지 "s11 이 왜 아픈가"가 아니다. 4 fresh draw 재현이 lane 전체를 cement 하거나 죽인다.
$0(#3868)이 (B)코퍼스 가설을 이미 약화(stem-agnostic 전역 under-imprint + G-PRESERVE 0.667 crater)
⟹ 2×2 는 4런을 대부분 죽은 가설 재검에 씀. **계기 무변경**: SEEN/held 분할은 atoms 파일(gt_atoms.json
20/29 · 양 base 공유)에 있고 `--split-seed` 만 held 12 swap 어간을 draw ⟹ 고정 base 위 fresh draw =
`--split-seed` 변주만. corpus 는 atoms 로만 build(base 무관) ⟹ s7-winning corpus 를 s11 base 에 그대로
얹어 rider 1런이 (A)base-capacity↔(C)run-randomness 공짜 dissociate. sweep 이 (B)도 겸함(s7 base 위
4 draw 착륙 = "corpus draw 간섭" 반증).

### 명령 (frozen · 발사 전 확정)
Fresh draws **D ∈ {4302,4303,4304,4305}, base 고정 = natem_c34_main_s7.clm**. draw 후 결과 보고 재draw
= selection contamination(builder docstring) ⟹ arm 은 draw 당 선-build:
```
# 코퍼스(flip1 xbind manifest + G-LEAK builder-coded) · draw = --split-seed 만의 함수
anima-py corpus ground_carrierswap --atoms gt_atoms.json --held-swap \
    --split-seed {D} --seed {D} --out ho_carrier_d{D}.txt
anima-py corpus ground_carrierswap --atoms gt_atoms.json --held-swap --decl-only \
    --split-seed {D} --seed {D} --out ho_decl_d{D}.txt
# PRE-GATE(값싼 GPU eval): base 가 fresh swap 을 ≈chance 로 실패해야(≤7/12) · 아니면 draw INVALID-PREGATE
anima-py evaluate natem_c34_main_s7.clm --xbind ho_carrier_d{D}.flip1.json
# CPT carrier(4 draw 전부) · --e0 3 --emax 3 필수
anima-py train --arch clm --canon --arm ctrl --objective ce_marginal \
    --init natem_c34_main_s7.clm --e0 3 --emax 3 --corpus ho_carrier_d{D}.txt \
    --steps 6000 --lr 2e-4 --batch-size 8 --seq-len 1024 --bf16 --seed {D} --out cpt_carrier_s7_d{D}.clm
anima-py evaluate cpt_carrier_s7_d{D}.clm --xbind ho_carrier_d{D}.flip1.json
# CPT decl arm(carrier 가 G-WRITE ∧ HO-CARRIER ≥10/12 통과한 draw 만 · 통과 draw 는 decl 착륙까지 PENDING)
anima-py train ... --corpus ho_decl_d{D}.txt --seed {D} --out cpt_decl_s7_d{D}.clm
anima-py evaluate cpt_decl_s7_d{D}.clm --xbind ho_carrier_d{D}.flip1.json
```
**Rider(1런) — A vs C**: s7 에 착륙한 byte-identical corpus 를 s11 base 에 학습(decl arm 없음·crack 주장 없음):
```
anima-py train ... --init natem_c34_main_s11.clm --e0 3 --emax 3 --corpus ho_carrier_s7.txt \
    --seed 7 --out cpt_rider_s11base_c7.clm ; anima-py evaluate cpt_rider_s11base_c7.clm --xbind ho_carrier_s7.flip1.json
```
`--lang` 무변경(frozen H_9339 ko 계기 · EN-FIRST 는 신규 corpus 용 · frozen 계기 byte-continuity 우선).

### ✅ $0 prep 검증 (2026-07-17 · GPU 전 로컬 빌드)
8 코퍼스(4 draw × carrier/decl) 로컬 빌드(anima-py 0.15.46 origin/main · 중립 dir 실행 = 설치본 corpus.py)
+ **build-time 감사 전원 통과**: plant-contradiction 0 · G-WRITE readback carrier 57/57·decl 12/12 · preserve n=12.
**재현성 설계 건전성 확증** — 4 draw 가 largely 다른 held-out swap 어간(carrier manifest swapC 어간):
draw별 12 어간 · pairwise jaccard **0.09–0.26**(shared 2–5/12) · **union 28/29 held-out 전수 근접** ⟹ 4 draw =
독립 draw(단일 lucky draw 아님 · ≥3/4 crack 생존이면 진짜 재현). `튼튼하`(#3868 correction 어간)=4302 에만.
⟹ GPU 전 $0-가능분 완료. 발사=recipe 실행만(deterministic --split-seed = pool 재빌드 byte-identical).

### Frozen verdict grid (데이터 전 사전등록)
per-draw gate(H_9339 상속): G-WRITE ≥11/12 else INVALID · G-PRESERVE drop ≤0.75 else crater INVALID ·
G-LEAK builder-coded · PRE-GATE base swap ≤7/12. **per-draw PASS** = valid ∧ HO-CARRIER negL ≥10/12 ∧
negZ ≥10/12 ∧ (min(negL,negZ) − HO-DECL) ≥ 4. **per-draw 카운트, 풀링 금지**(풀링 특징 일치 ≠ 재현).

| sweep 결과 (N=4 fresh draw) | verdict |
|---|---|
| ≥3/4 PASS | 🟢 crack **REAL** — 다중draw GREEN-DIRECTIONAL · 벽 공식 균열 · next=cement scope |
| 정확히 2/4 PASS | 🟠 MIXED — 사전등록 1회 확장 draw 4306–4307 · 최종 bar ≥4/6(지금 선언·추가확장 없음) |
| ≤1/4 PASS(draw valid) | 🧱 s7 crack = **NOISE** — 벽 재봉쇄 · write lane kill-list |
| ≥2/4 draw G-WRITE INVALID | ⛔ **WRITE-PROTOCOL-UNRELIABLE** — s11 mode 흔함 · root-cause 주역화 · rider 우선 |

Rider: G-WRITE 착륙(≥11/12) ⟹ base s11 **무죄** → s11 실패=run-randomness(C)·레시피 base 간 일반화.
G-WRITE 실패 ⟹ **(A) base-capacity** — s7 crack 유지하나 base-조건부·카드에 scope 기록.
INVALID draw 는 INVALID 로 보고(분모서 조용히 drop 금지·no survivorship) · 캠페인 中 gate 재독/재draw 금지(burned-gate).

## 게이트 (frozen · H_9339 상속)
- G-WRITE: carrier readback ≥11/12 stem 아니면 INVALID.
- G-PRESERVE: SEEN 연산자 CPT 후 생존(drop ≤0.75 = crater = INVALID · corpus-py-1⑥).
- G-LEAK: builder-coded (held/seen contamination 0).
- 사전등록 bar 는 데이터 전 고정 · 음성/INVALID 도 결과.

## 블로커 (미발사 사유 · 발사 재개점)
- ✅ **Fable 설계 확정**(bg ba13m22pn) — 재현성 sweep + rider FROZEN(위).
- ⏳ **pool concrete 블로커** (2026-07-17 07:29) — clean host 부재:
  - summer: GPU 프리(2MiB·0%)지만 **base natem_c34_main_s7 부재**(s11만) + **load 24**(병렬 hammer ·
    8-11h 캠페인엔 earlyoom python3 우선 kill + wedge 위험) + RAM 12/30G.
  - aiden: **base s7·s11 둘 다 존재** + GPU 9.3G 여유지만 **70% util = 병렬세션 phaseA_s7 fire 점유**
    (a_parallel_session_compare — 간섭 금지).
  - ⟹ 8-11h sequential 캠페인 안전 발사 host 부재. **재개 = aiden GPU 프리(phaseA_s7 종료) OR summer 냉각
    (load<6)** 시 위 명령 순차 발사(carrier 4 draw → 통과분 decl → rider). base s7 부재 host 면 aiden→host
    transfer 176MB 선행. 설치 = anima-python origin/main git-archive(hexa-less · 설치 후 즉시 발사 = clobber 창 최소).
  - runtime: ~45-70min/CPT run(정상), sequential 1잡씩(공유host 병렬 금지) · OMP_NUM_THREADS=4 cap · ckpt
    매 run 후 ~/anima-weights pull(a_fire_recover_complete) · rc=137 = earlyoom python3(OOM 오진 말 것).

## 명령 (Fable 회신 후 확정)
```
# base ckpts: aiden·summer ~/h9339_screen/natem_c34_main_s{7,11}.clm (176MB · K=3 L=4)
# 코퍼스: anima-py corpus ... --held-swap [--decl-only] (draw-seed 변주)
# CPT: anima-py train --arch clm --canon --arm ctrl --objective ce_marginal \
#   --init <base>.clm --e0 3 --emax 3 --corpus <ho>.txt --steps 6000 --lr 2e-4 \
#   --batch-size 8 --seq-len 1024 --bf16 --seed <S>
# eval: anima-py evaluate <cpt>.clm --xbind <ho>.carrier.json  (G-WRITE readback)
```
