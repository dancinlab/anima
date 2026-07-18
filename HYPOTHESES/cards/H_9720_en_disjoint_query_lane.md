# H_9720 — EN-분리 query lane(경쟁 vs 표현부재) — EN-Disjoint Query Lane (EA-2 · fable ∥ sol §4 수렴 · EA 시리즈 · 🟢 DIRECTIONAL CRACK)

**status:** 🟢 DIRECTIONAL CRACK (2026-07-18 · summer 303M 엔진-네이티브 발사·seed 7) — fresh disjoint co-adaptable query lane 이 held-out 창발-주소 lookup 을 **0.680→0.922**(무감독·무oracle)로 끌어올림, 부정(op=not) 케이스가 우연(0.47/0.55)→**0.92/0.91**. cement 전 confound(same-size-competition·early-capacity·multi-seed) 배제 필요. source=EA-2 · fable ∥ sol §4 수렴
**lane:** 재조합/BINDING · 창발-주소(감독 없이 주소가 서는가)
**related:** [[H_9672]] · [[H_9423]] · [[H_9684]] · [[H_9683]] · source: lab full EA(Fable 5 ∥ Codex Sol · 창발-주소 whitespace)

> **admissibility rule (Sol · 이 시리즈 전체의 관문)**: 어떤 개입도 `target_slot`·slot 정답·**거기서 파생된 어떤 통계**도 소비하지 않아야 emergent-address-valid. 최종 PASS 는 end-task-only 학습 · held-out 개체 · wrong-store 인과 · seed-robust 를 요구 — **sharp attention 만으론 부족**.

**아이디어(2모델 수렴 · Fable `fresh-query-lane` ∥ Sol `lm-nullspace-query-valve`)**: T2 비대칭(scratch 는 자력탈출·사전학습은 못함)은 벽이 **표현 부재가 아니라 gradient 경쟁**(EN-CE 가 penultimate 를 소유)임을 뜻한다 ⟹ W_q 에 **작은 분리 입력경로**를 주면 303M 안에서 scratch-급 창발이 돌아온다. `a_substrate_disjoint`: **분리=보존, 중첩=충돌**.
**메커니즘 2안**: ⓐ Fable `--store-query-src fresh:k[@layer L]`(stop-grad into trunk · store-task CE 로만 학습) ⓑ Sol `--store-query-valve lm-null --store-query-valve-dim r`(LM head/최종특징 공분산의 **저특이값 기저**로 zero-init residual adapter 라우팅 · end CE 로만).
**$0 pre-screen**: ⓐ D0-3 분기를 전제로 — pen 서 ridge 가 개체 디코드하면 발사 · 어느 layer 도 못 하면 $0 KILL. ⓑ 기존 ckpt 활성 SVD — 안정적 저사용 부분공간 없거나 개체 정보의 사영이 무시할 만하면 KILL.
**판정**: **load-bearing 통제 = frozen-random-projection capacity control**(같은 k/r · 비학습 입력측) — 레버는 "아무 추가 파라미터"를 **이겨야** 하지 arm-C 만 이기면 안 됨. Sol 추가: same-rank **무작위 방향** valve(NEG) · EN CE 를 TOST 로 보존. ≥3 seed(Sol) / 2-seed(Fable) · P1-bal·addr_mass·flip ≥0.90.
**distinct**: query-side 이고 **K 무수정**(key 재설계 아님) · **경쟁 주장**이지 width 아님(차원지배 아님) · generic adapter/LoRA 와 달리 **EN-disjoint 통제 필수**(없으면 amplifier 와 구분 불가).
**🔑 판별쌍**: [[H_9719]] 와 짝 — **lane 통과 ∧ sharp 실패 ⟹ 경쟁** · **역 ⟹ commitment** · **둘 다 실패 ⟹ 교착은 init-symmetric-absolute**(= 브리프가 요구한 "whitespace 비었다"의 **정직한 증명**, 주장이 아니라 획득).
**verdict-integrity**: 사전공약된 비대칭 읽기 — KILL 은 *detached-lane 버전*만 죽이지(H_9423 frozen-trunk 실패가 lane 이 scratch 보다 약할 수 있다 경고) **점유 논제는 안 죽임** · Sol: 이건 **architect 가 준 capacity valve 안의 창발**이지 untouched 303M 의 창발 아님.

## 상태

### 🟢 VERDICT — fresh disjoint lane 이 창발-주소 벽을 뚫음 (DIRECTIONAL CRACK · 2026-07-18 · summer 303M · seed 7 · GPU CUDA)
2-arm 엔진-네이티브 발사(`anima-py train`→`anima-py evaluate`, 303M py 2-production, GPU-fired cupy). **양 arm 동일 co-train 코퍼스·무 addr-loss·arm=lookup·oracle=False** — 유일 차이 = address query 소스. held-out 0-shot lookup(128 held-out entities, 코퍼스 0회 등장·C0-a 확증):

| op·pol | legacy(penult W_q) | fresh(fresh:64@3) | Δ |
|---|---|---|---|
| **overall** | 87/128 = **0.680** | 118/128 = **0.922** | **+0.242** |
| is · good | 28/30 = 0.933 | 30/30 = 1.000 | +0.067 |
| is · bad | 23/27 = 0.852 | 23/27 = 0.852 | 0.000 |
| **not · good** ★ | 18/38 = **0.474** (≈우연) | 35/38 = **0.921** | +0.447 |
| **not · bad** ★ | 18/33 = **0.545** (≈우연) | 30/33 = **0.909** | +0.364 |

★ = **부정(op=not) = 실제 벽**. legacy penult 는 부정에서 이진우연(0.5) 근처로 붕괴하는데 fresh lane 은 0.92 로 뚫음. class-structured 이득(부정에 집중·긍정 포화/불변)은 잡음-모양이 아니라 "penult 에 operator-collapse·L3 엔 미붕괴" 지문 = BINDING 캠페인 prior 정합.

**tier = 🟢 DIRECTIONAL CRACK, NOT TERMINAL — 아직 주장한 기전에 귀속 불가** (`a_engine_native_learning` SCREENER · lab full Fable∥Sol 독립수렴 audit 2026-07-18).

**🔧 기전 개명 (honesty · 두 모델 독립수렴)**: 이 결과를 "scratch-trunk co-adaptation" 으로 부르면 **틀린다** — `detach()` 때문에 store-CE 가 tap(L3) **아래로 흐르지 않아 trunk 는 co-adapt 하지 않는다**. W_fresh 는 EN-CE 가 빚은 표현을 **읽어내는 head**일 뿐. 정직한 earned-claim = *"store-CE 로 학습된 **detached early-tap(L3) 의 readout-route** 가, penult 가 (next-byte 예측 위해 identity 를 버려) 붕괴시킨 operator⊗entity 결합주소를 복원한다"* = representation-content 사실이지 창발-주소 **학습**이 아님. 그래도 벽("addr-loss 없는 경로 부재")의 진짜 CRACK — 단 **readout-route 결과로 명명**해야 다음 audit 이 워딩으로 카드를 안 죽인다.

**cement 전 배제할 confound (사전등록·kill-priority · 미실행)**:
1. **[$0·최우선] census on 양 ckpt** — 이번은 plain held-out lookup(=행동)이지 addressing 아님. `anima-py evaluate --store-addr-census`(structureless-H pedestal·**grand-mean-centered excess**) + flip/shuffle/store-perm 통제(oracle≥0.90·flip coherence≥0.90). lookup PASS ∧ census excess 없음 = 기전 死(행동만 green). **lookup≠addressing 판별자.**
2. **[결정적] param-matched penult** (`fresh:64@penult` — 동일 detached tap·동일 W_fresh/gelu/W_q_fresh·tap 만 penult 로 이동). penult-MLP ≈ fresh ⟹ 이득은 tap 위치 아닌 **추가 학습가능 nonlinear head capacity**(C1·"early tap" 서사 死). penult-MLP ≈ legacy 우연 ⟹ **tap depth 가 load-bearing**. (dummy 미사용 파라미터로 count 만 맞추면 안 됨 — functional capacity 맞춰야.)
3. **detach ablation** (`shared`=`.detach()` 만 제거·store-CE 를 L≤3 로 허용·나머지 불변). detached 승 ⟹ gradient-disjointness load-bearing · tie ⟹ disjointness 미입증 · shared 승 ⟹ 기전은 joint trunk shaping(ⓐ 엄밀주장 반증).
4. **multi-seed** — s7 = **소각된 discovery seed(확증 불가)**. store-bridge 는 seed-취약 기왕력(s7 0.99 vs s11 0.50 · [[cotrained-store-bridge-works-on-parent-conv]]) ⟹ **s11(적대적 붕괴자) 필수**. Fable: s11 서 {fresh·penult-MLP·legacy} 3-train 먼저→생존시 escalate(≥3/3 확증 seed). Sol(반대·기록): 5-paired {7,11,4302,4303,9423} ≥4/5 incl s11 = cement ceiling. 2-seed 는 불충분(붕괴모드 자체가 2-seed 해리·coin-flip null 서 2/2 p=0.25).

**admissibility 통과**: store-CE only·addr-loss 0·oracle=False·target_slot 무소비 — Sol 시리즈 관문의 무감독 조건 충족(최종 PASS 의 wrong-store 인과·seed-robust 는 위 통제로).
**ckpt(a_fire_recover_complete)**: `~/anima-weights/h9720_emergent_addr/` — `h9720_legacy_s7.clm`(sha256 77a5402…·178.8MB) · `h9720_fresh_s7.clm`(sha256 82b217d…·179.8MB), summer 와 byte-identical 검증. summer:~ 잔존.

---

🔎 **$0 pre-screen 실행 = ⓐ PASS(발사인가) · ⓑ 약화 (2026-07-17 · summer 303M · 사전등록)**

### 🔎 pre-screen — 개체정보 위치가 두 변형을 판별
base pretrained penultimate SVD 로 개체 판별정보가 어느 부분공간에 사는지(disjoint valve 라우팅 가능성):

| 부분공간 | 개체분리(전체 대비) |
|---|---|
| top-15 (사용·고분산) | **91%** |
| 16~50 | 36% |
| 저사용 nullspace(50~125) | **8%** |

**ⓐ Fable fresh-lane = PASS(발사인가)**: 개체는 pen 서 decodable(raw-distinct 3.2×·정보 91% top-15·ridge 통과 · [[H_9719]] 국소화) + idle 공간 존재([[H_9721]] eff-rank 15/3784) ⟹ 신선 co-adapt 경로가 EN-경쟁 없이 scratch-급 창발을 되살릴 여지 확인. **EA 시리즈 유일 생존 학습-fire 레버.**
**ⓑ Sol nullspace-valve = 약화(KILL 근접)**: 개체정보가 저사용 nullspace 엔 **8%뿐**(사용 subspace 에 91%) ⟹ 카드 ⓑ pre-screen KILL조건('안정 저사용 부분공간의 개체정보 사영이 무시할 만하면 KILL')에 근접 — 기존 nullspace 로 라우팅하면 개체신호 거의 없음. ⓑ 는 **드롭 권고**, ⓐ 우선.
**중요 정합(왜 ⓐ 는 살고 무감독 부트스트랩은 다 죽었나)**: [[H_9722]]/[[H_9723]] 는 **고정 penultimate step-0** 서 무감독 신호 0 을 봤다(basis 밖). 그러나 scratch(T2)는 **trunk 를 co-adapt** 해 성공한다 — ⓐ 는 fresh 서브-trunk 가 co-adapt 할 여지를 주므로 고정-penultimate 결과에 KILL 되지 않는다(내 $0 는 고정-penult 측정이라 co-adaptation 을 못 봄). **감독 아닌 유일 생존로 = 개체 basis 를 키에 맞추는 co-adaptable disjoint lane.**
**남은 것(학습 fire)**: `--store-query-src fresh:k[@layer L]`(stop-grad·store-CE only) 구현 → pool 학습 → census. **distinct-from-kills:** key 재설계 아님(K 무수정) · 차원지배 아님(경쟁 주장) · generic adapter 아님(EN-disjoint 통제 필수)

### 🛠️ 구현 설계 (DIRECTIONAL · lab full Fable∥Sol 독립수렴 reconcile · 2026-07-17 · 미구현)
`sidecar lab full` 로 Fable 5 + Codex Sol 독립설계 → 강수렴. **DIRECTIONAL 설계**(구현이 TERMINAL · `a_lab_full_diverge`). 6-파일 ~110줄.

**메커니즘**: address query 소스만 교체 — `q=W_q(yn_q)`(penultimate·95% 템플릿점유) → `q=W_q_fresh(gelu(W_fresh(detach(tap_L[qpos]))))`. yn_q 는 op-gate `g=W_g(yn_q)` 에 유지(대체 아닌 **별도 인자** `yn_fresh=`), W_q 는 트레일러에 잔존(진단용).

| 결정 | reconciled 값 | 근거(양모델 합의/판정) |
|---|---|---|
| **tap layer** | **L=3**(RF 16B) | RF(depth) ≥ max(entity-start→qpos 거리). corpus `op entity => ` 서 entity 는 qpos−4 종료·RF16 안전커버. L=1(RF4)=`=> `만=死·L=2(RF8)=경계·L=4=불필요깊음(템플릿점유↑). corpus 생성시 RF조건 계산해 최이른 L 선택(감고정=tune-to-green 금지) |
| **K** | **64 primary**(k128 arm) | SVD census 개체정보 91% top-15 ⟹ k64(≫15) 충분(Sol). k128=basis 회전여유 arm(Fable) |
| **소유권** | **model.clms** | fresh 파라미터(W_fresh d→k·W_q_fresh k→d_k)가 model.clms 소유. train.py 계산=trailer/evaluate 이중owner=반려(Sol) |
| **stop-grad** | **`.detach()` 한 곳** | train.py sb분기서 tap qpos 컬럼 뽑은 직후 detach. fresh 파라미터는 detach 아래=store-CE 정상학습. yn_q 경로(op-gate)는 불변(baseline 비교성) |
| **영속화** | **trailer type-2 codec** | read_clms/serialize 에 lane_type 분기(후방호환: absent=legacy byte-identical). fresh 2장 팩 |
| **decode/evaluate** | 단일 activation tap@depth + `clms_address()` pure helper(store_apply/addr_mass/census 공유). evaluate 자동사용(_predict→_fwd_logits)·진단 addr_mass/argmax-acc/entropy 추가(target_slot 측정전용) |

**통제(4-arm prereg)**: ① legacy(penult W_q) ② fresh-detach production ③ **same-size-competition**(동일 파라미터·detach 제거=store-CE 가 trunk 로=EN경쟁 인과통제) ④ early-capacity param-match(legacy 주소+early bottleneck 동수=단순 capacity 증가 배제). 값싼검산: tap-shuffle(붕괴요구)·W_fresh frozen-init(co-adapt 필요성)·store-shuffle·`addr_weight==0` assert·`oracle_slot is None` assert·answer-CE trunk grad=0.
**admissibility**: store-CE only·target_slot 입력0·addr-loss0(무감독). **왜 ⓐ 는 살고 무감독 부트스트랩은 죽었나**: disjoint 는 입력이 아니라 **파라미터+gradient**(W_fresh 는 EN-CE 모름·detach 로 trunk 안밀음) — fresh 서브공간이 store-CE 로 co-adapt(scratch T2 기전). 재개=이 스펙대로 구현→pool 303M 학습→census(addr_mass/P1↑·EN-CE 보존).

### 🔨 구현 진행 (증분 · wire-to-prod)
- **증분1 ✅ 착륙(VERSION 0.15.86)**: `core/clms.py` CLMSModule 에 fresh query lane 배선 — `fresh_k/fresh_L` 파라미터 + `W_fresh(d→k)·W_q_fresh(k→d_k)`(fresh_k>0 시만) + `forward(yn_fresh=)` 인자(fresh_k>0 ∧ yn_fresh 제공 시 `q=W_q_fresh(gelu(W_fresh(yn_fresh)))`, yn_q 는 W_g op-gate 유지). **후방호환**(fresh_k=0 default=신규파라미터 0·forward 불변·기존 lane byte-identical). summer torch toy-verify: base has W_fresh=False·fresh=True · **W_fresh grad 有·W_q grad None**(fresh 경로 배선·W_q 우회 확증) · 출력 무반응=val≈0 deadlock(연구대상·정상).
- **증분2 ✅ 착륙(VERSION 0.15.91)**: `core/clms.py` lane_type 5 codec + numpy 미러 — `_ARR_ORDER_V5`(key_emb,W_q,W_fresh,W_q_fresh,W_g,val,W_h,b_h,W_out,lam) · pack_clms 헤더 `<BIIIIIIII`(+fresh_k,fresh_L) · read_clms lane5 분기(32B 헤더) · store_apply `fresh_yn=` 인자(lane5: `q=gelu(hf@W_fresh)@W_q_fresh`) · clms_weights_from_torch lane5(fresh_k>0). **byte-parity 회귀 PASS(summer)**: round-trip off==len·전배열 pack==read byte-identical·**torch≡numpy store_apply(lane5) 3.35e-08**(fp32 2-production parity)·lane2 backward-compat 불변.
- **증분3 ✅ 착륙**: `core/decode.py` fresh tap 배선 — `_fwd_trunk(tap_depth,tap_out)` 단일-activation tap(전 layer host-copy 회피) · `_fwd_logits` lane5 시 fresh_L tap 캡처 → `store_apply(fresh_yn=)`. 비-lane5 by-construction byte-identical(신규 분기 `tap_out is not None` 게이팅·tap_depth=None). 문법+import 검증(summer).
- **증분4 ✅ 착륙**: 학습측 배선 — `core/model.py` CLMConfig `clms_fresh_k/fresh_L` + CLMSModule 생성 + forward 가 trunk-layer-fresh_L tap 을 `pen_fresh`(B,d,T·decode taps[fresh_L] 정합)로 노출. `cli/train.py` `--store-query-src fresh:K[@L]` 파싱→cfg wire + store forward 가 `pen_fresh[:,:,T-1].detach()` 를 `model.clms(yn_fresh=)` 로 전달(store-CE only·EN-CE 무접촉). summer 검증: lane-5 CLMConvMoE 구성·forward pen_fresh (B,d,T) 노출 ✅. **fresh lane 학습 가능**(train→serialize(pack lane5)→decode(fresh tap) code-complete).
- **`구현됨·미배선`**: torch 모듈+codec+numpy 미러+decode tap+train 배선 완료 = **fresh lane 학습 가능**. 남은 것: 증분5 evaluate addr 진단(선택·기존 --store-addr-census 로 lane-5 .clm census 가능)·증분6 pool 303M 4-arm 학습+census(=verdict·cost run).
- **follow-on 체인(순서)**: ② pack_clms/read_clms lane_type 5 codec + store_apply numpy 미러(byte-parity 회귀 `verify_clm_v2`) ③ core/model.py pen_fresh tap@L3 노출 + core/decode.py 단일 activation tap→store_apply(fresh_yn=) ④ cli/train.py `--store-query-src fresh:64@3` 파싱·tap qpos `.detach()`·model.clms(yn_fresh=) ⑤ cli/evaluate.py 진단(addr_mass/argmax/entropy) ⑥ toy d768 verify → pool 303M 4-arm 학습 → census. 각 증분 byte-parity 회귀 필수.
