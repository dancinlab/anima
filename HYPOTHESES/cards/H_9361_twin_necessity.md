# H_9361 — TWIN-NECESSITY: 연산자가 캐리어를 **읽긴 하는가** (필요성 · scramble-floor 회피)

- **tier**: 🔵 PRE-REGISTERED (설계 동결 · 미측정 · 설계 Fable 5)
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
