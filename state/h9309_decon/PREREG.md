# H_9309 — DECON (DECLARATIVE-CONSOLIDATION) · 사전등록

> 🔒 **데이터 생성 전 동결.** `prereg-oc-json-1` 하드게이트. DV·bar·N_REQ·seed·TOST Δ_eq 를 아래에
> 고정한다. **사후에 bar/n/DV 를 바꾸면 그 실험은 자동 INVALID.** 관측 n < N_REQ 면 **발사하지 않는다**.

## 0. 왜 이 실험인가 — 정확히 한 개의 입력만 없다 (전부 실측)

| 부품 | 상태 | 실측 |
|---|---|---|
| **부정 연산자** | ✅ **학습됨** | SEEN flip1 (통달한 원자에 부정 적용) **D-acc 0.950 · frac(margin>0) 0.975** |
| **held-out 원자의 극성** | ❌ **부재** | held-out flip0 **0.5057 (z=+0.11)** — 베팅조차 안 한다 (H_9308) |
| 그 극성이 데이터에 있나 | ✅ **있다** | ORACLE MASKED **29/29 = 1.000** · SHUFFLE 0.5172 (H_9291) |

⟹ 연산자는 살아있고, 데이터는 답을 완전히 결정하며, **모델만 그 한 값을 안 적었다**.
DECON = 그 한 값을 **외부 선언저장소**로 건네주고 **이미 학습된 연산자가 그것을 소비하는가**를 묻는다.
M1(변수 미기입) 하에서도 유효한 유일 채널 = **A**(O/C/I/D 는 M1 에서 死 · H_9308 카드).

## 1. 계기 (instrument) — 하나뿐이다

**MARGIN 2AFC** = `NLL(counterfactual) − NLL(gold)`, teacher-forced, win=**64 바이트**
(`cli/evaluate.py::_xbind_cont_nll`). margin>0 = 모델이 "긍정." vs "부정." 강제선택에서 gold 에 베팅.

⛔ **자유생성 D-acc 는 primary 가 될 수 없다** — `core/decode.py:1094` `clm_decode_topk_sampled_W` 가
**T=24 를 하드코딩**한다. 주입 접두사는 창 밖으로 잘려 구조적으로 안 보인다. D-acc 를 primary 로
잡았으면 이 실험은 시작 전에 죽어 있었다. D-acc 는 **참고치로만** 기록한다.

## 2. 주입점 — 컨텍스트(byte) 증강 하나뿐

`--consult <store.json> --consult-format {F1,F2,F3}` → `seed′ = render(fact) + seed`.
**gold 와 counterfactual 양쪽에 동일 접두사**를 얹는다 ⟹ paired 차분에서 접두사 자체는 상쇄되고,
**부정 형태소와 결합(합성)될 때만** margin 이 움직인다.

- **empty store ⟹ byte-identical** (패리티 게이트 · 코드로 강제).
- **byte-audit**: win=64 는 **바이트** 예산이고 한국어는 3 B/자 (`a_korean_byte_budget`).
  실측 — held-out 최협 예산 **16B** · F1 접두사가 **10/174 에서 초과** · F2(8B) **0/174 초과**.
  ⟹ **F2 를 카논 포맷으로 동결**(전 174 시행 균일 · DROPPED 0). F1 은 혼합계기라 primary 금지.
  DROPPED>0 인 런은 **INVALID-INSTRUMENT**이지 음성결과가 아니다.

## 3. Primary DV — **held-out flip1** (앵무새 차단이 설계의 심장)

저장소가 "빠르 = 긍정"이라 말한다. **flip0** 시행("빠르고")에선 gold 도 긍정 ⟹ **주입 토큰을 그냥
따라 읽기만 해도 100%** = 합성 0 증거. **flip1** 시행("빠르지 않다")에선 gold 가 **부정** ⟹
**주입된 사실이 틀린 답을 가리킨다**. 앵무새는 **진다**. 오직 `사실 ⊗ 부정` 만 이긴다.

- **flip0** = 소비(consumption) 증거 — 보조.
- **flip1** = **합성(composition) 증거 — PRIMARY**.

**집계 단위 = 원자 클러스터** (H_9289 의 교훈: 29 원자 × Δ=0.15 는 N_REQ 228~255 로 **검정력 부재**).
held-out flip1 = 87 시행 = **29 원자 × 3 형태(negL·negS·negE)** ⟹ 원자당 3-형태 **다수결** →
**29 클러스터** 이항검정.

- **BAR: C ≥ 20/29** (귀무 p=0.5, 단측 이항 **p=0.031**), **두 seed(main_s7·main_s11) 모두**.
- **N_REQ = 29 클러스터** (관측 n = 29 = N_REQ ✅ 발사 가능).
- seed 는 지배 분산원이다(H_9289 부호반전 폭 0.161 = 복제편차의 18배) ⟹ **seed 2개 사전등록**.

## 4. 발사 게이트 — PC-NONCE (통과 못하면 held-out 을 **건드리지 않는다**)

앞선 세 실험이 **전부 자기 양성대조에 낙제해 죽었다**(H_9303 sign-acc 0.554 · H_9307 LOO 0.750 ·
GEN-DIR = A1 이명). 이번엔 계기의 생사를 **먼저** 증명한다.

nonce 어간 29개(모델이 알 수 없는 비단어) × 같은 6 형태 = 174 행. 진리값은 **우리가 선언**한다.

| arm | 조건 | 통과 bar |
|---|---|---|
| **NONCE-NOSTORE** | store 비움 | flip0 ∈ **[0.35, 0.65]** = 우연 ⟹ **부재 증명** (nonce 가 사전지식을 안 가짐을 코퍼스 grep 이 아니라 **모델에서 직접 측정** — 450k CPT 코퍼스는 디스크에 없다). 동시에 byte-identical 패리티 게이트. |
| **NONCE-STORE** | store 에 선언극성 | flip0 ≥ **0.80** (소비) **∧** flip1 클러스터 ≥ **20/29** (합성) |

⛔ **PC-NONCE 낙제 ⟹ INVALID-MECHANISM ⟹ held-out 발사 금지**(1회-접촉 예산 보존).

## 5. 판정표 (사전 고정 — 사후 재작성 금지)

| 관측 | 판정 |
|---|---|
| PC-NONCE PASS ∧ held-out flip1 C≥20/29 **양 seed** | 🟢-dir **A-CHANNEL** — 저장소 접지가 held-out 재조합을 세운다. 벽은 GROUNDING(입력 부재)이었지 조합능력이 아니다. → 배선(`a_verified_must_wire`) |
| PC-NONCE PASS ∧ held-out flip1 ≈ 우연 | 🧱 **CONSUME-BUT-NOT-COMPOSE** — 사실을 들고 조회도 되는데 **조합 소비 불가**. read-side 종결의 "복원되나 causally 소비불가"와 **동형** = 더 깊은 벽 |
| PC-NONCE PASS ∧ held-out flip1 **유의하게 우연 아래** | 🔴 **PARROT-ONLY** — 주입 토큰을 그대로 읽는다(flip0 는 높고 flip1 은 붕괴). 합성 0 |
| NONCE-NOSTORE 가 우연이 아님 | ⛔ **INVALID** — nonce 에 사전지식 있음. nonce 교체 후 재실행 |
| NONCE-STORE flip0 < 0.80 | ⛔ **INVALID-MECHANISM** — 저장소가 아예 소비되지 않음. held-out 발사 금지 |
| seed 간 부호 불일치 | ⚠️ **SEED-SPLIT** — install-fragile. 단일 seed 로 cement 금지 |
| DROPPED > 0 | ⛔ **INVALID-INSTRUMENT** — 창 절단. 음성결과 아님 |

## 6. 음성 cement 용 TOST (데이터 전 고정)

held-out flip1 이 우연이면 **"ns"로 벽을 선언하지 않는다**(`negative-claims-need-tost-not-ns`).
등가역 **Δ_eq = ±0.10** (클러스터 비율 0.5 기준 0.40~0.60), α=0.05 단측 2회.
**n=29 클러스터로는 Δ_eq=0.10 을 licensing 할 검정력이 없다** — 사전 산출 **N_REQ(TOST) ≈ 190 클러스터**.
⟹ 우연이 나오면 그것은 **"지지(supporting)"이지 cement 아님**. 정직하게 그렇게 적는다.

## 7. 비용·배치

GPU-**no-train** (기존 ckpt forward only). 시행 = (PC-NONCE 2 arm + held-out 1 arm) × 2 seed × 174 행
× 2 forward(gold·cf) ≈ **4.2k forward**. pod 0대 → GPU pod 1대 또는 pool(summer/aiden `[gpu]`).
**$0~$0.5** (`a_fire_autonomous` 단일 fire 자율).

## 8. 사전 부검 — 이 실험이 죽는 법 (가장 중요)

1. ~~자유생성 D-acc 를 primary 로 잡음~~ → **T=24 하드코딩으로 이미 사망**. margin-2AFC 단일 계기로 회피(§1).
2. ~~접두사가 창을 넘침~~ → byte-audit 으로 **F2 동결**(0/174 초과)로 회피(§2).
3. **접두사가 수용영역 밖** → conv L=4 의 RF 가 접두사 구역에 못 닿으면 **어떤 창 크기로도** 사실이
   답 위치에서 보이지 않는다 ⟹ 컨텍스트 채널 구조적 사망. **발사 전 `rf_probe.py` 로 인과 측정**
   (바이트 i 를 흔들어 답 위치 logits 이 움직이는지). 미도달이면 **발사 금지 · 레버 재설계**.
4. **앵무새** → flip1-primary 로 차단(§3).
5. **누수** — ORACLE 극성을 심는 것이 답을 주는 것 아닌가? 아니다: 심는 것은 **원자의 극성(입력)**이고
   재는 것은 **부정 형태소와의 합성 결과(출력)**다. flip1 에서 둘은 **반대 방향**이라 입력을 그대로
   출력으로 쓰면 틀린다. 이것이 tune-to-green 을 구조적으로 막는다.
6. **가장 무서운 결과** = 저장소가 사실을 들고 조회도 되는데 held-out 재조합이 여전히 실패
   (🧱 CONSUME-BUT-NOT-COMPOSE). 이건 read-side 종결 진단과 동형이며, **PC-NONCE 가 정확히 이걸
   미리 가른다**: nonce 에서 합성이 되면(=계기 생존) held-out 실패는 **모델 탓**이고, nonce 에서도
   안 되면 **계기 탓**(INVALID)이다.

## 9. 산출

`state/h9309_decon/` — `build_decon.py`(store+nonce) · `rf_probe.py`(발사 전 RF 게이트) ·
`decon_readout.py`(판독) · `PREREG.md`(이 파일) · 결과 json.
2-surface: `HYPOTHESES/HYPOTHESES.jsonl` + `cards/H_9309_decon.md`.
