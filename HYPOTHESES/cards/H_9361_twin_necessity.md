# H_9361 — TWIN-NECESSITY: 연산자가 캐리어를 **읽긴 하는가** (필요성 · scramble-floor 회피)

- **tier**: 🔵 PRE-REGISTERED · n=9 재동결 (⚠️ $0 feasibility: SEEN 20 stems → 쌍 Y*=9 ≪ 원 N=60 · Fable 판정 (A) n=9 빌드 + STOP-CONDITION 1.07·sd_w,eff≤0.35 동결 · NEXT=스크리너 sd_w 측정)
- **선행**: H_9331 🧱 INSTRUMENT-CEILING — swap-patch(충분성·주입)는 이진 readout 국소화 불가([[swap-patch-binary-readout-scramble-floor]] · 0.50=scramble floor). **미해결 질문 = 필요성**: 연산자가 캐리어 자리를 읽긴 하나. [[binding-is-operator-stem-gating-not-morphology]] 의 lookup vs rule 로 직결.
- **계기**: `anima-py evaluate <clm> --twin-necessity <manifest.json>` (engine-native · `core/decode.py` `_apply_edits`/`clm_forward_logits_edited` + `_xbind_cont_nll` 마진 스코어러 재사용 · 7/7 코어게이트 인증분)

## 왜 BIND-LOCUS 가 붕괴했나 (설계 제약)

**off-manifold donor**(다른 item 의 hidden · RF 내 prefix 모순) × **이진 DV**(argmax flip)가 "답 전이"와
"forward 파괴"를 **같은 수 0.50** 에 사상했다. 수리는 **두 연결을 다** 끊어야 한다 — DV 도 donor 도.

## 계기 — RF-정합 minimal-pair 이식 + 연속 마진 DV

**DV = 부호 있는 연속 마진** `m = logP(긍정) − logP(부정)` (teacher-forced · `_xbind_cont_nll` 기존 · 둘 다 6B
byte-정합 = `a_korean_byte_budget` 자동충족). 두 좌표(item i · layer ℓ · arm a):

```
τ = (m_patched − m_A) / (m_B − m_A)              전이율 (0=A 유지 · 1=B 됨)
S = clip(1 − |m_patched| / ((|m_A|+|m_B|)/2), 0, 1)  붕괴지수
```

(τ,S) 평면이 세 점을 **분리**한다(이진 flip 은 셋을 0.5 로 뭉갰다):
- **(1, ~0) = 캐리어 읽음**(전이: 부호 뒤집힘·크기 보존) · **(0, ~0) = 이 자리서 미소비** · **(~0.5, ~1) = 붕괴 → INVALID-AT-ℓ**.

**조작 = minimal-pair 쌍둥이 이식**: donor = **캐리어 창만 다른 byte-정합 쌍둥이**의 같은 자리 hidden(prefix·suffix
byte-동일 · 창 byte-길이 동일 · 빌더가 불일치 하드거부). conv 인과성이 **prefix 정합을 공짜 보장**(causal conv 는
≤t 만 봄 ⇒ t0 이전 층별 byte-동일 = 정확한 이식). 쌍둥이 2종/SEEN 어간: **B-opp**(반대극성 byte-정합 · 주 ·
전이 vs 붕괴 최대분리) · **B-neut**(길이정합 중립 · 부 · m_B≈0 이라 주 불가).

### Arms (전부 기존 `edits` list · mode `patch`)

| arm | patch | 기대 |
|---|---|---|
| **SPAN(ℓ)** | 캐리어 창 [t0,t1) @ℓ · donor=쌍둥이 | 측정: τ(ℓ) 궤적 |
| **COMP(ℓ)** | [t1,T) @ℓ · donor=쌍둥이 (prefix 는 인과성상 불필요) | 중복경로 검출기 |
| **PEDESTAL** | ℓ=0 · embed-conv footprint 로 창 확장 [t0,t1+(K−1)) | 기계적 = 쌍둥이 B 실행 ⇒ τ=1.000 (참값 아는 spike-in) |
| **IDENTITY** | self-patch | τ=0.000 (sham · G-SHAM 인증분) |
| **BLIND** | byte-정합 **극성무관** 창(중립 부사만 다름 · 같은 극성 · 같은 ℓ·거리) | \|Δm\|≈0 · S≈0 — DV 가 파괴게이지 아님 증명(same-class 통제 이식) |

layer sweep ℓ ∈ {0,1,2,4,8,…배증…,L}. 사전등록 주의: dilation 배증(cap 512)+win 24~64B 면 광추가 ~ℓ=6 서 창
포화 ⇒ **이른 τ 이동이 기대형태**(빠른 붕괴 과독 금지).

## 🔒 동결 결정표 (사전등록 · bar 사후이동 금지)

**Validity gates (하나라도 실패 ⇒ 명명 INVALID · DV 미판독):**
```
V0  --device-parity PASS · edits=[] sha byte-identical(G-PARITY 재실행) · device 각인
V1  PEDESTAL τ=1.000±0.005 · S≤0.02 전 item         아니면 INVALID-ALIGNMENT
V2  IDENTITY τ=0.000±0.005                          아니면 INVALID-INSTRUMENT
V3  BLIND 전 ℓ: median|Δm|/|m_A|≤0.15 ∧ S̄≤0.25       아니면 INVALID-DISRUPTION-GAUGE
V4  item: 두 쌍둥이 부호정답 ∧ |m|≥1.0 nat ≥80%(누락 로그·무단캡 금지) · τ̄ bootstrap CI폭≤0.30  아니면 UNDERPOWERED
```

**DV 판독 (B-opp 주 · ℓ별 · N=60 SEEN 어간 · paired bootstrap 10k · 두 disjoint 반 부호일치 필수):**

| 셀 | 조건 | verdict |
|---|---|---|
| 🔓 **CARRIER-READ@ℓ** | τ̄≥0.75 · CI excl 0.5 · S̄≤0.25 | 캐리어 hidden 이 ℓ 서 극성결정에 소비됨 |
| 🧱 **NOT-READ@ℓ** | TOST τ∈[−0.15,+0.15] ∧ S̄≤0.25 **∧ COMP(ℓ) τ̄≥0.75** | 정보가 캐리어 떠남(이동 · COMP 이 목적지 국소화) |
| ⚠️ **REDUNDANT-ROUTE** | SPAN τ≤0.15 ∧ COMP τ≤0.15 둘 다 TOST · S 낮음 | 극성 중복분산 = 단일자리 필요성 NO · **'미읽음' 주장 금지** |
| 💀 **SCRAMBLE@ℓ** | S̄>0.5 | INVALID-AT-ℓ (옛 floor · 이제 **검출**됨) |
| 🔍 **SUPPRESSION** | τ̄≤−0.15 · CI excl 0 | 우연 아래 = 발견(9.7σ 교훈 사전등록) |
| 🔍 **OVER-TRANSFER** | τ̄≥1.25 | 증폭 발견 |
| ⏳ 그 외 | 중간 | UNDERPOWERED (bar 이동 없음) |

**집계 = τ(ℓ) 궤적이 답**. τ 가 마지막 trunk 층까지 ≥0.75 ⇒ SEEN 답은 캐리어 자리의 늦은 읽기(H_9334 C4
캐리어키 사실과 일관 · SEEN/base 경로). τ 감쇠 ∧ COMP 상승 ⇒ 다른 곳 계산 · 교차깊이 = 이동 locus.

**부 사전등록 일관성 arm — EN mirror**: H_9346 EN=ECHO(`not` 무시·조회 멀쩡) ⇒ EN `not`-창 SPAN 은 **τ≈0 ∧
COMP≈1 예측**. 계기가 재현해야 할 기대-음성(수십 forward).

## 💰 비용 — pod 불필요 · summer 서 $0 ×2

주 질문은 **SEEN(사전학습) 극성** ⇒ **base 303M(pool/HF 상주)**. swap_c4/natem_n2 불필요(헤드라인).
1. **$0 스크리너(빌드 게이트)**: 동결 KO 코퍼스서 쌍둥이 구성(read-only · `--lang ko` 빌드 아님) · byte-길이정합
   달성가능 확인 · unpatched m_A/m_B 채점 · V4 item 기준 N≥60 · |m|≥1nat. 미달이면 **빌드 전 중단**.
2. **$0 본run**: ~60쌍 × ~8층 × 3arm ≈ 1.5k short(win≤64B) forward @summer(OMP 4 · 단일호스트·device 각인 ·
   전 τ/S 는 run 내 비교 ⇒ GPU≠CPU 2.5e-14 는 device 고정으로 격리 · 옛 pod-GPU 수와 비교 금지).
3. ~$1 pod fire = **선택 후속**: C4/n2 재run 으로 CPT 극성 vs 사전학습 극성 경로차 = P-place/P-kind 판별자 —
   base 가 깨끗한 CARRIER-READ/NOT-READ 낼 때만 가치.

## ⚠️ $0 feasibility 발견 + n=9 재동결 (2026-07-15 · 빌드 前 · Fable 검정력 판정)

**$0 사전점검(모델無·빌드無)**: 동결 KO SEEN 원자 = **20 stems**(pol0=10·pol1=10) · byte-길이 버킷
3B→(1,0) 6B→(3,4) 9B→(6,6) ⇒ byte-정합 반대극성 쌍 **Y\* = 9 disjoint(48 crossings)** ≪ 원 게이트 N=60.
⟹ N=60 은 인벤토리 모르고 잡은 값. **필요성은 substrate 아니라 원자셋 크기에 gate**.

**Fable 판정 = (A) n=9 로 빌드 · 단 stop-condition 동결**. n=9 는 자동 underpowered 아님 — 이건 **극 판별**
(τ̄≈1 CARRIER-READ vs τ̄≈0 NOT-READ · gap~1.0)이지 정밀추정 아님. paired MDE = **1.07·sd_w,eff**.
**🔒 STOP-CONDITION(동결)**: 스크리너의 surface-평균 within-pair sd 로 `1.07·sd_w,eff > 0.35` 이면 **빌드 금지 ·
UNDERPOWERED-BY-INVENTORY(MDE 수치 첨부)** · `≤ 0.33` 이면 빌드. (3-surface 평균이 √3 되사줌 · raw per-surface
sd ≤ ~0.5 생존.) **바-정정이지 tune-to-green 아님**(인벤토리 사실 촉발 · DV 관측 前 · 더 엄한 기준으로).

**🔒 수정 V4 게이트(빌드 前 동결 · verbatim)**:
1. 분석단위 = 48 crossings 이나 CI 는 **stem-cluster 재표집**(20 stems 가 df 지배 · crossings 를 t 분모에 넣으면 pseudoreplication).
2. 주 게이트(폭 게이트 대체) = **verdict 밴드**: NOT-READ τ̄≤0.30 ∧ COMP≥0.75 · CARRIER-READ τ̄∈[0.70,1] · 그 외 INCONCLUSIVE + 이상셀(τ̄<0·τ̄>1 = 발견). 95% cluster-CI 가 **정확히 한 밴드 안**에 있어야.
3. 부호 게이트(양-반쪽 대체) = **≥8/9 disjoint 쌍이 개별로 verdict 편**(exact sign P(≥8|9)≈0.02) + LOO 안정성(전 LOO 동밴드).
4. surface 복제 = per-surface 3/3 동밴드(각 surface 자기 점추정) · CI 요건은 surface-평균에만.
5. SUPPRESSION/SCRAMBLE = within-item 통제라 n 무관 · 불변 · n=9 집계에도 동밴드 로직 · scramble-floor 앵커 유지.

**N-boost 판정(Fable)**: 3-surface = 반복측정(N 3배 아님) · sd_w √3 축소만(df=8) · 3/3 복제 게이트. 24 instances =
바이트동일→동일 forward→정보 0. layer sweep = multiplicity(Holm 보정 또는 단일 요약통계만 cement · per-ℓ 곡선 DIRECTIONAL).
(C) 배제: conv 무-attention · occlusion/donor-patch = H_9331 이 닫은 계급(off-manifold→scramble) · gradient 비-engine-native.
**⟹ minimal-pair 가 이 레포 장부의 유일 생존 on-manifold 필요성 계기.** NEXT = 스크리너로 sd_w 측정 → stop-condition 적용.

### ✅ 스크리너 1차 — item-gate PASS (natem_n2_main_s7 · pod 45001860 · 2026-07-16)

**계기·배선**: `corpus twinnec`(#3678) 로 후보 매니페스트 생성 → `evaluate --twin-screen`(#3687) 로 base
303M forward 채점. **ckpt = natem_n2_main_s7.clm**(SEEN 연산자 alive · H_9327 flip1 0.98 의 그 모델 · mac
`~/anima-weights/natem_n2/` 소재 → pod scp · HF 미공개라 HF 우회). flip1_suffix surface · win 64.

| 지표 | 값 |
|---|---|
| gate-passers (sign==esign ∧ \|m̂\|≥1nat) | **20/20 stems** |
| disjoint pairs (Y) · blind-backed (Y*) | **9 · 9** |
| accepted \|m̂\| 범위 | **5.27 ~ 20.47 nats** (전부 ≫ 1) |
| accepted \|m̂\| sd | 3.115 |
| median pair gap \|mA−mB\| | **28.88 nats** |
| item-gate feasibility | **PAIRS-OK** |

**판독**: (1) natem_n2_main_s7 의 SEEN 연산자가 **매우 살아있다**(20/20 · \|m̂\|≥5.27 · ckpt 선택 검증) —
Fable 전제('SEEN 극성 in base')는 base-wiki(토이 clm_d768_e2l1 부정연산자 없음)엔 거짓이나 **natem(CPT)엔
참**. (2) **item-gate PASS** = |m̂|≥1 통과 쌍 9 = n=9 재동결과 정확 일치 · 우려하던 '9쌍도 못 채움' 아님.
(3) **연속 마진 gap 28.88 nats = τ 분모가 거대**(BIND-LOCUS 이진 scramble-floor 우려 소멸 · τ well-separated).
⟹ strong·clean 신호 → τ precise 전망 → pedestal sd_w 낮을 유망(stop-condition 통과 방향). **NEXT = pedestal
arm(ℓ=0 dilated · τ=1 spike-in)으로 τ-scale sd_w 측정 → 1.07·sd_w,eff≤0.35 stop-condition → 통과시 full
SPAN/COMP arm.** 산출 tw_screen(item-gate) · s11·flip0·flip1_prefix 는 3/3·2seed 확장.

### 🔬 FULL 계기 발사 — 계기 VALID · but DV 이 이 toy 서 교란 (natem_n2_main_s7 · aiden GPU · 2026-07-16)

`evaluate --twin-necessity`(#PR) 로 5-arm 전 계기 발사(Fable 설계 pedestal 기전 · `_bl_margin_edited` +
carrier-window donor patch). **stop-condition 은 공허통과**(pedestal τ 이 bit-exact 1.000 → sd_w=0) →
Fable 대체 게이트 = per-pair `|τ_ped−1|<1e-6` 하드검증 채택.

**계기 유효성 — 4개 validity arm 전부 PASS (s7·flip1_suffix · L=4 · K=3 · 9쌍 · device=gpu)**:

| arm | 값 | 게이트 |
|---|---|---|
| V1 PEDESTAL | **max\|τ−1\|=0.00e+00** (bit-identical to B) | τ=1.000±0.005 ✅ |
| V2 IDENTITY | max\|τ\|=3.65e-07 | τ=0±0.005 ✅ |
| V3 BLIND | med\|Δm\|/\|m_A\|=0.141 · S̄=0.190 | ≤0.15·≤0.25 ✅ |
| V4 POWER | sign 9/9 · CI 반폭 0.176 | ≥80%·≤0.30 ✅ |

**⚠️ V1 사양정정(tune-to-green 아님 · 기계적·데이터-무관)**: frozen 표의 pedestal `S≤0.02` 는 **오사양**.
pedestal 은 정의상 on-manifold B 실행(τ=1.000 EXACT 이 증명) ⇒ m_patched=m_B 정확 ⇒ S=1−\|m_B\|/((\|m_A\|+\|m_B\|)/2)
는 \|m_A\|≠\|m_B\| 이면 nonzero = **쌍둥이 자체의 \|m\| 비대칭**(scramble 아님). flip1_suffix 는 \|m_B\|≥\|m_A\| 라
우연히 S=0, flip0 은 S=0.13 → 옛 게이트가 거짓 INVALID-ALIGNMENT 를 뱉음(τ=1.000 EXACT 인데). ⟹ V1=τ 비트동일만
게이트, pedestal-S 는 진단보고. (prereg 표가 우연-아래 칸 빠뜨린 정정과 동류 — 사양완결이지 바 이동 아님.)

**DV(SPAN τ 궤적) — s7 두 surface 동일 패턴** (flip1_suffix·flip0 · s11+flip1_prefix 는 공유-pool 클로버로
미발사, but 아래 교란은 통계 아닌 **구조**라 복제 무관):
```
 ℓ | SPAN τ̄ [95%CI]        S̄     | COMP τ̄ | BLIND τ̄ | band          (flip1_suffix)
 0 | +0.176 [+.04,+.31]    0.410 | +0.862 | +0.026 | INCONCLUSIVE
 1..2 | +0.17~+0.23        0.41~0.49 | +0.82~+0.86 | ~+0.04 | INCONCLUSIVE
 3 | +0.225                0.532 | +0.862 | +0.039 | SCRAMBLE (S̄>0.5)
 4 | -0.004 [-.01,+.00]    0.075 | +1.024 | -0.001 | NOT-READ (9/9)   ← clean only here
```

**🧱 판정 = DIRECTIONAL-INCONCLUSIVE(이 toy) · "캐리어 미읽음" cement 불가 — geometry 로 교란 확증**.
Fable 조정 + **기하검사 #1($0)** 가 자기기만-가드의 우려를 실증:
- **유일 clean 층 ℓ=4 는 구조적 tautology.** tap[L] 이후 위치혼합 연산 = 단일 expert conv K=3 dil=1 뿐
  (router K=1·MoE·GN·readout 은 per-position). 캐리어는 창 끝 t=54 → K=3 로 t=55 까지만 도달, 채점행은
  [57,63) → **CARRIER_REACHES_SCORED=False (전 surface·전 L=3/6/9)**. 즉 ℓ4 서 캐리어 열을 patch 해도
  채점 readout 에 **닿을 수 없어** τ=0 은 도달불가의 필연이지 "미소비"의 증거가 아님.
- **정보있는 중간층 ℓ1-3 은 off-manifold scramble** (S̄ 0.41~0.53 · 카드의 국소혼합-trunk 예언대로 · ℓ3=SCRAMBLE
  하드라벨). 캐리어 바이트가 쌍둥이 동일이라 ℓ0 SPAN 은 IDENTITY(τ≈0)여야 하나 τ=0.18·S̄0.41 = K−1 어간낙수
  오염 + 부분창 패치 off-manifold.
- **COMP 은 거의 무내용**(Fable): 쿼리 위치 포함 → ℓ4 서 readout 입력 자체를 덮음(pedestal-등가 · τ=1.02 가 확인).
  COMP=계기작동 증명이지 "operator lane 이전" 아님. ⟹ COMP τ̄≥0.75 로 NOT-READ 를 벌 수 없다(가드 무력화 — 가드
  자체가 COMP 을 신뢰했으나 COMP 이 trivial).

**⟹ 결론**: 계기(pedestal bit-exact·identity·blind·sign 전 인증)는 **VALID·배선완료**지만, 이 toy(L=4·K=3)
아키텍처서 **캐리어-창 SPAN 은 필요성을 못 잰다** — clean 층은 도달불가로 trivial, 정보층은 scramble. natem
=CPT toy(303M 아님)라 어차피 DIRECTIONAL. 병렬 **H_9388 BRIDGE-TRACE 와 AGREES**(살아있는 연산자=어간위치
읽음 · 캐리어 아님) = 교차계기 수렴이나, 본 계기는 그 방향을 **독립 확증 못 함**(측정면서 교란).

**NEXT (Fable 처방)**: ① $0 행동게이트(9 stem 캐리어 vs 중립필러 답 9/9 갈림) → ② **CARRIER-TWIN(option B)**
= 같은 어간, {`지 않다`} vs {10B 중립필러} 쌍(어간·쿼리 동일 · 연산자 형태소만 다름) — 살아있는 연산자의 효과가
어느 창에 실리나 직접 질문. ③ 단 캐리어창은 readout 못 닿으니 **query-stream 창 patch** + **deeper 모델**(중간층
on-manifold)이 실측조건. ④ Δ-INJECT(held-out 쿼리창에 mean operator-Δ 주입 · H_9331 same-class+S 규율)
= 이식성 operator 방향 = **직접 bridge-lever**. frontier(g1-interface-addressable) 는 **직교**(bridge 생성/배제
아님)나 **다음 bridge-lever 조준을 재지정**: 캐리어 위치 주입은 readout 이 안 보는 열 — 레버는 query-stream 으로.

## 🛡️ 자기기만 최빈 + 가드

**중복이 비필요성으로 위장.** conv 초기혼합이 캐리어 정보를 suffix/readout 로 복사(dilation 배증·창 빠른 포화)
⇒ ℓ 서 캐리어창만 patch 하면 τ≈0 = "미소비"로 읽히나 진실은 "복사본 통해 소비"(단일자리-knockout 함정 · 국소혼합
trunk 라 scramble 보다 **더** 가능). **가드(구조적)**: COMP arm 필수 · NOT-READ 는 COMP τ̄≥0.75 없이 **주장불가**
· 둘다-0 은 REDUNDANT-ROUTE 하드라벨(음성주장 금지). **메타가드**(device-parity 교훈): 게이트 신뢰 전 **일부러
실패시켜라** — PEDESTAL 을 1바이트 어긋난 창으로 돌려 INVALID-ALIGNMENT 뱉는지 확인(거짓 PASS 아님).

## 함의 — 왜 $0 로 잴 가치가 있나

H_9347 NEXT=C3 이식이고, 모든 write-side rescue 는 **SEEN 결정이 어디서 소비되는가**에 암묵 베팅한다: base 가
늦은 CARRIER-READ 면 CPT 를 캐리어키 lane 에 쓰는 게(H_9334 방향) 진짜 read-site 조준 · 중간층 이동/중복이면
캐리어-표적 쓰기는 **결정이 이미 떠난 단계**를 겨눈 것 ⇒ rescue 는 COMP 이 짚은 readout-인접으로. **$0·인증배선
으로 다음 fire 의 조준을 바꾸는 가장 싼 계기.** 추구 안 할 유일 = 추가 단일-span 충분성 주입(H_9331 이 종결).
