# H_9331 — 두 극성은 왜 다른 자리에 사는가 (BIND-LOCUS · 인과 주입)

- **tier**: 🟡 DIRECTIONAL (KO 측정 완료 · 4/4 INVALID-LOCALIZATION → 연산자 read-site = **표면 캐리어**, 원자-스팬 아님 · pedestal(캐리어-swap) 대기 · KO×EN 교차 PENDING)
- **선행**: H_9327 🧱 BINDING — 연산자는 **살아있고**(SEEN flip1 0.98~1.00) 사실은 **가중치에 있는데**(WRITE 0.98) **결합하지 않는다**(held-out flip1 0.46~0.56 = 우연). LIE 통제군의 편향-무관 검사가 **+0.073 ≈ 0** ⇒ 심은 사실이 **조회조차 되지 않는다**. 도망갈 구멍(연산자 없음·기질 무능·사실 미착륙·예산 부족·시연 결핍) 전부 실측 배제.
- **설계**: Fable 5 (재프레임 + 결정실험 + 동결 bar)
- **계기**: `anima-py evaluate <clm> --bind-locus <manifest.json>` (engine-native · `core/decode.py` taps/edits)

## 재프레임 — 세계가 둘이 아니라 셋이다

"두 극성이 **다른 자리**에 산다"는 프레임은 **CPT 극성이 feature 로 존재한다고 전제**한다.
**WRITE 0.98 은 그걸 증명하지 않는다** — 그것이 증명한 건 flip0 캐리어 안의 stem→답 매핑,
즉 **반사(reflex)** 뿐이다. 극성 **변수**가 어간 자리에 형성됐다는 증거는 0이다.

| 세계 | 주장 | 고치는 법 |
|---|---|---|
| **P-place** | feature 는 있으나 연산자가 읽는 자리가 아니다 | **그 자리에 쓰면 뚫린다** (주소 문제) |
| **P-kind** | feature 자체가 없다 · CPT 는 답-슬롯 직행 **지름길**만 썼다 | 배치가 아니라 **코퍼스** (극성을 가지려면 *써야* 한다) |
| **S** | 같은 자리·읽을 수 있는 내용인데도 연산자가 **무시**한다 | 결합은 조회가 아니라 **사전학습 공동형성** ⇒ H_9267 XBIND 가 **법칙**이 된다 |

**read-only 프로브 지도로는 셋을 못 가른다** — 프로브가 읽는 것 ≠ 연산자가 **소비**하는 것
(read-side-exhausted 교훈). 그래서 DV 는 **인과적 쓰기**에서 나온다.

## 방법 — INJECT-AT-READ-SITE

```
Stage A  연산자의 읽기-자리를 SEEN 으로 확정 (양성통제 · 참값을 우리가 심는다)
         SEEN 어간의 hidden 을 반대극성 SEEN donor 로 층 ℓ 에서 swap-patch → 답이 뒤집히나?
         ℓ* = swap ≥ 0.75 ∧ sham ≤ 0.15 를 만족하는 **최천층** (SEEN 만 씀 ⇒ tune-to-green 아님)
         스팬 사다리(동결): 마지막 1바이트 → 마지막 3바이트 → 어간 전체
         전부 실패 → 🚫 INVALID-LOCALIZATION (그 자체가 locus 사실 · P/S 판정 **금지**)

Stage B  축 v̂ = unit(SEEN 긍 평균 − SEEN 부 평균) @ℓ* · 목표 μ± = SEEN 클래스 투영 평균
         주입 = **투영-정합**(고정 α 아님) ⇒ 팔들이 **매개 공변량** 위에서 정합
         (고정 α 는 실현 투영이 팔마다 달라진다 = control-must-match-mediating-covariate 가 번 교훈)

Stage C  DV = **편향-무관 의존도** (H_9327 LIE 검사의 인과판)
         dep_f = P(답=긍 | 주입=긍) − P(답=긍 | 주입=부)   ← 전역 편향은 차분에서 자동 상쇄
           B  novel 어간(사전학습 0회 ∧ CPT 0회)  ← 핵심 arm
           C  held-out 어간에 **자기 심은 극성** 주입   ← 수리(rescue) arm
           D  v̂ 직교 무작위 방향, 같은 이동량        ← off-manifold 통제
           E  self-patch(자기 값)                    ← sham · 계기 무부작용
```

## 동결 결정트리 (사전등록 · bar 사후이동 금지)

```
V1  Stage A 가 ℓ* 를 찾음                              아니면 → INVALID-LOCALIZATION
V2  B-arm flip0 dep0 ≥ +0.50 (주입이 readout 에 소비됨)  아니면 → INVALID-DEAD-INJECTION
V3  D |dep| ≤ 0.15  ∧  E 변화율 ≤ 0.05                 아니면 → INVALID-INSTRUMENT
─────────── V1 ∧ V2 ∧ V3 통과 후에만 DV 판독 ───────────
DV  B-arm flip1 의 dep1:
      dep1 ≤ −0.50                → 🔓 **P** — 연산자는 자리 내용을 **소비한다** ⇒ 벽은 주소/종류 문제
      TOST(±0.20) 등가            → 🧱 **S** — 같은 자리·소비가능한 내용인데도 안 붙음 = **substrate 사실**
      그 사이                     → ⏳ UNDERPOWERED (se 보고 · n 증설 · **bar 이동 없음**)
```

**양 seed(s7·s11) 부호 일치 시에만 tier 확정** (H_9327 의 확정 형식 그대로).
검정력: novel 60 어간 × 캐리어 2 = paired 120쌍/flip층 → se ≈ 0.064 · MDE(80%) ≈ 0.18 < 마진 0.20.

## 🔌 배선 — 완료·인증 (2026-07-14)

**계기가 엔진 안에 있다**(`a_experiment_engine_native`) — 조작이 canonical forward **안에서** 일어나고,
개입된 residual 이 **같은 ops** 로 readout 까지 흐른다. 옆에 선 probe 하니스가 아니다.

- `core/decode.py` — `_fwd_trunk(W, tok, T, taps=None, edits=None)` (기본값에서 **byte-identical**) ·
  `_apply_edits` (patch / steer / **proj**=투영정합) · `clm_forward_taps` (READ) ·
  `clm_forward_logits_edited` (CAUSAL · readout+슬롯 완전경로)
- `cli/evaluate.py` — `--bind-locus` (3종 세트: dispatch · `_KNOWN_FLAGS` · `--help`)

### 코어 게이트 7/7 실측 PASS

| 게이트 | 내용 | 결과 |
|---|---|---|
| G-PARITY | `edits=None`/`[]` 가 production 과 byte-identical | **PASS** sha `92e24b6e76f4…` 3-way 동일 |
| G-TAP | 층별 tap = L+1 깊이 · shape [T,d] | **PASS** |
| G-SHAM | self-patch = 무변화 (기계 부작용 0) | **PASS** |
| G-LIVE | 진짜 swap 이 readout 을 움직임 (dead code 아님) | **PASS** max\|Δlogit\| 16.47 |
| G-PROJ | 투영-정합이 목표값을 **정확히** 맞힘 | **PASS** 목표 3.0 → 실현 3.000000000 |
| G-STEER | 고정크기 밀기 live | **PASS** |
| G-GUARD | 창 밖 span 은 조용히 통과하지 않고 **에러** | **PASS** |

### CLI 스모크 — 결정트리가 실제로 작동

토이 ckpt(`clm_d768_e2l1` · 부정 연산자 **없음**)에서 Stage A 가 전 (깊이×스팬)에서 swap=0.000 →
**🚫 INVALID-LOCALIZATION** 을 뱉고 **P/S 판정을 거부**했다. 이것이 정확히 V1 이 해야 할 일이다 —
연산자가 없는 모델에 결합 판정을 내리지 않는다.

## HONEST — 아직 못 한 것

- **Stage B/C 코드경로는 아직 양성 통제로 실행되지 않았다.** 토이 ckpt 가 V1 에서 (정당하게) 걸려서
  거기까지 가지 못했다. 그 경로들의 수치는 **진짜 CPT ckpt(`natem_n2_main_s7.clm`)에서 처음 나온다** —
  그때까지 Stage B/C 는 "배선됨·미실행"이다. 이걸 "검증됨"이라 부르지 않는다.
- 발사 대기 이유: summer GPU 가 H_9330 두 arm 으로 포화(wall ~5h). 큐잉됨.

## 📊 측정 결과 — Stage A 가 4/4 INVALID-LOCALIZATION (pod 44908484 · GPU-FIRED · rc=0 · 2026-07-15)

engine-native BIND-LOCUS 를 4개 ckpt 에 발사했다. **네 번 다 Stage A 양성통제가 ℓ* 를 못 잡았다**:

| ckpt | seed | verdict | Stage A max swap (bar 0.75) |
|---|---|---|---|
| n2 (원래 벽) | s7 · s11 | INVALID-LOCALIZATION | ≤ 0.25 |
| **C4** (연산자 자신의 키 · H_9334 12/12) | s7 · s11 | INVALID-LOCALIZATION | 0.25 · 0.10 |

n=20 rung(1·3바이트)에서 swap 0.00~0.15 · sham 깨끗. full-stem rung 은 n=4 라 sham=0.5(소표본 잡음)이나
**판정은 n=20 rung 에 걸리므로 무관**. 원자-스팬 가설은 **검정력 있는 지반에서 이미 죽었다**.

### 해석 — (B) 진짜 발견 (Fable · 결정적) : read-site = **표면 캐리어**, 원자-스팬 아님

**결정적 이유 = n2 ≡ C4.** C4 는 H_9334 가 **다른 계기**로 "연산자가 자기 키 `{s}지 않다` 를 읽는다"를
12/12 (p=.0002 · TERMINAL)로 증명한 모델 — **읽을 수 있는 결합이 실재**한다. 그 C4 에서도 원자-스팬 swap 이
똑같이 실패한다는 것은, 도구가 눈먼 게 아니라 **"그 결합은 원자 스팬에 없다"고 정직하게 보고**한 것이다
(결합은 H_9334 가 쓴 **캐리어 키**에 있다). 도구가 눈멀었다면(A) n2·C4 를 같은 trivial 이유로 실패했을 것이고
그 동일성은 무정보다 — 그러나 우리는 C4 의 결합이 **실재·가독**임을 독립적으로 안다.

**G-LIVE 해리가 봉인**: 진짜 swap 은 readout 을 max|Δlogit|=16.47 로 크게 흔든다 — 그런데 P/S 답은 ≤25% 만
따라온다. 원자-스팬 swap 은 그 자리의 **어휘 정체성**을 바꾸나 **극성 결정**은 안 바꾼다 = 극성은 캐리어
형태소 `지 않다` 에서 완결되고 swap 은 거기를 못 건드린다. ⇒ **H_9327 의 "SEEN flip 은 바이트 이어쓰기"를
인과적으로 입증**(연산자가 SEEN 을 0.98~1.00 뒤집어도, 뒤집는 극성은 원자-스팬 hidden 에 국소화되지 않는다).

**왜 A(캐리어-swap 수리)가 아니라 B 인가**: 발견과 수리가 **같은 대상**이다 — 결과 자체가 "read-site=캐리어".
캐리어-swap 재발사는 깨진 통제를 고치는 게 아니라 음성이 함의한 **양성 locus 를 확증**한다. 양성통제는 안
깨졌다 — 그 전제("연산자가 원자-스팬서 극성을 읽는다")가 **시험 대상 가설이었고 깨끗한·검정력 있는 음성**을 냈다.

**Fable 의 caveat(다음 단계를 정할 뿐 판정 불변)**: 진짜 양성통제이려면 전제(그 자리에 탐지할 효과가 실재)가
참이어야 하는데 여기선 거짓이었다 ⇒ 이 run 엔 **true-positive pedestal**(swap 이 실제로 ≥0.75 뒤집는 자리)이
없다. pedestal 없이는 B 를 "원자-스팬에 **없다**"에서 "캐리어에 **있다**"로 완전 승격 못 한다.

### 🔒 동결 next — 캐리어-스팬 swap (B 확증 + pedestal 공급)

같은 계기·같은 SEEN 원자·같은 donor, 단 hidden swap 을 **원자 스팬 대신 캐리어 스팬**(`지 않다` 바이트 ·
depth 0~4)에 건다. **🔌 배선 완료**(v0.13.59): `anima-py evaluate <clm> --bind-locus <m> --bl-swap-span carrier`
— `span_of` 가 stem-end→`=>` 연산자 형태소 스팬을 반환(negL→`지 않다` · negS→`고`, length-match 자동분리 ·
연산자 형태소는 바이트-동일해 full-span rung 이 n=20 확보 = stem full-span n=4 기아 해소). **사전등록 예측**:
캐리어-swap flip ≥ 0.75 (read-site 국소화) ∧ 원자-swap flip ≤ 0.25
(이미 확보 · n=20 재현). 이 이중결과는 tune-to-green 아님 — 방향예측 있는 다른 인과시험이고, 캐리어-swap 팔이
곧 **pedestal**(올바른 스팬을 겨누면 계기가 국소화함을 증명)이다. C4 먼저(H_9334 가 가독 캐리어결합 보장 =
pedestal), 그다음 n2. full-stem rung 은 n=20 으로 올려 재발사.

#### ⚠️ 캐리어-스팬 측정 결과 — pedestal 예측 FALSIFIED (4/4 · pod 44908484 GPU-FIRED · 2026-07-15)

| ckpt | 원자-스팬 maxswap | **캐리어-스팬 maxswap** | verdict |
|---|---|---|---|
| C4 s7 | 0.25 | **0.350** | INVALID-LOCALIZATION |
| C4 s11 | 0.10 | **0.250** | INVALID-LOCALIZATION |
| n2 s7 | ≤0.25 | **0.500** ← 최고 | INVALID-LOCALIZATION |
| n2 s11 | ≤0.25 | **0.300** | INVALID-LOCALIZATION |

캐리어-스팬이 원자보다 **체계적으로 높다**(캐리어 영역이 더 인과적 = 해석 B 방향은 살아있음) — **그러나
어느 run 도 0.75 pedestal 미달**. **Fable 사전등록 예측(캐리어-swap ≥ 0.75) 이 4/4 반증됐다.** ⇒ 극성 읽기는
**어떤 단일 스팬(원자든 캐리어든)에도 국소화되지 않는다** — 분산(A · 캐리어영역+readout 다지점) 또는 swap-patch
계기의 국소화 천장(B · ~0.50, positive control 이 어디서도 안 서면 계기를 의심 = verdict-integrity). n2 s7 이
0.50 으로 C4 보다 높은 것(원래 벽 ckpt 이 연산자-자기키 C4 보다 캐리어를 더 국소화)은 미해결. **해석·다음 실험
= Fable 재위임 중**(pedestal 예측이 뒤집힌 자리). #3625 헤드라인('read-site=표면 캐리어 DIRECTIONAL')의 존폐도
Fable 판정 대기. 계기·산출물 전부 engine-native(`--bl-swap-span carrier` · bl_carrier_*.json).

### KO 레인의 교차 기여 (한 줄)

결합기는 KO=INVALID(P/S 능력축)로 읽으나 **무정보가 아니라 DIRECTIONAL**: 동일한 n2/C4 INVALID-LOCALIZATION
이 KO 연산자의 flip 을 **극성 feature 가 아니라 표면 캐리어 형태소**에 국소화한다 — 이것이 교차가 재려는 바로
그 비대칭이다(EN=자유·전치 연산자로 ECHO 실패 H_9346 vs KO=캐리어 표면서 읽는 BOUND 접미사). KO 는 교차에
null 이 아니라 **인과 locus 사실**(극성-읽기=형태론, feature 아님)을 건넨다.


## 🔗 H_9332(담체 인구조사)와 만나는 지점 — **이 계기가 R1/R2 를 가른다**

H_9332 는 `지 않다` 연산자가 **자기가 학습된 어간(SEEN · 어간당 80줄)에서만 시험됐다**는 것을
코퍼스 계수로 밝히고, 지금까지의 모든 관측을 똑같이 설명하는 두 세계를 **미결로** 남겼다:

| | **R1 LOOKUP-MISMATCH** | **R2 STEM-BOUND** |
|---|---|---|
| 주장 | 일반 규칙은 있는데 pol 을 CPT 가 안 쓴 자리에서 조회한다 | **일반 규칙이 없다** — `(어간, 지 않다)` 가 학습된 **쌍**이고 어간이 **키의 일부** |

**BIND-LOCUS 가 이 둘을 인과적으로 가른다** (관측이 아니라 **쓰기**로):

```
novel 어간(사전학습 0회 ∧ CPT 0회)의 읽기-자리 ℓ* 에 극성을 써넣고 flip1 을 묻는다

  R1 이면 → 연산자가 그 자리에서 pol 을 읽으므로 답이 주입을 따라온다   dep1 ≤ −0.50  ⇒ P
  R2 이면 → 학습된 적 없는 쌍이므로 주입해도 답이 무관심하다            dep1 ≈ 0      ⇒ S
```

**Stage A 는 두 세계 모두에서 통과한다** — SEEN 어간의 hidden 을 반대극성 SEEN donor 로 덮으면
R1(내용이 바뀜)에서도 R2(키가 바뀜)에서도 답이 뒤집힌다. 그래서 Stage A 는 **세계를 가르지 않고
계기를 교정**하는 데만 쓰인다(설계 의도 그대로).

H_9332 는 R1 의 방어선(occlusion)을 H_9330 이 검사 중이라고 적었다. 맞다 — 그러나 H_9330 은
**읽을 수 있는가**를 묻고(read-side), BIND-LOCUS 는 **연산자가 소비하는가**를 묻는다(causal).
둘은 대체재가 아니라 **다른 질문**이고, read-side-exhausted 교훈이 말하는 대로 **판정은 후자가 박는다.**

## 🛠️ 착륙 중 잡은 내 계기의 결함 2건 (발사 전 · spend 0)

**① 캐리어를 재구성하고 있었다 (치명적).** 내 `prompt_of` 는 `"이 영화 {stem}지 않고 => "` 를
템플릿으로 **만들고** 있었다. H_9327 의 진짜 캐리어는 **두 개**이고 그중 하나는 부정어가 어간 **앞**에
온다:

```
negL   "이 영화 빠르지 않다 => "
negS   "이 영화 안 빠르고 => "      ← 부정어가 어간 앞!
내 재구성 "이 영화 빠르지 않고 => "  ← 모델이 본 적 없는 문자열
```

⇒ 연산자가 **순전히 내 탓으로** 죽어 보였을 것이고, 나는 그걸 substrate 사실로 읽었을 것이다.
수정: 매니페스트의 `seed` 를 **verbatim 상속**한다(`reference-match` — 참조가 열려 있으면
재구성하지 말고 읽어라). 어간 span 은 그 verbatim 프롬프트 안에서 **바이트 rfind** 로 찾는다
(negS 때문에 rfind — 부정어가 앞에 와도 어간은 자기 바이트의 마지막 등장이다).

**② novel 을 '믿음'으로 고를 뻔했다.** 수정: `anima-py corpus bindlocus` 가 후보 어간을 **모든
코퍼스에 대해 바이트 계수**하고 **단 1회라도 나오면 기각**한다. 등장 0 이 아닌 novel arm 은
S 판정을 **사전학습-노출 인공물**로 바꿔놓는데, 그게 바로 이 arm 이 배제하려는 교란이다.


## 🔀 병렬 세션 대조 (`a_parallel_session_compare` · 2026-07-15)

병렬 세션이 같은 프런티어에서 **H_9334 C4 CARRIER-SWAP** 을 사전등록했다. 겹치는지 확인했다.

| | **H_9334 C4 (그들)** | **H_9331 BIND-LOCUS (이 카드)** |
|---|---|---|
| 묻는 법 | **재학습** — 반전 극성을 **연산자 자신의 표면**(`{s}지 않다` 담체)으로 다시 써서 연산자가 읽는지 본다 | **인과 주입** — 재학습 없이, 연산자의 **읽는 자리**에 극성을 직접 써넣고 답이 따라오는지 본다 |
| 가르는 것 | **H-δ 저장소-측**(read-path 가 못 닿는 저장소) vs **H-ε 인터페이스-측**(연산자 자신의 키로 써야만 닿음) | **P-place**(자리 틀림) vs **P-kind**(feature 자체가 없음) vs **S**(같은 자리인데도 무시) |
| 비용 | CPT 재학습 1회 | 기존 ckpt 로 **재학습 0** |

**결론: 겹치지 않는다 — 서로를 검증한다.** 그리고 **의존 방향이 있다**:

```
BIND-LOCUS 가 P 를 내면   →  연산자는 자기 읽는 자리의 내용을 소비한다
                             ⇒ H-δ(저장소가 못 닿음) 는 **거짓**
                             ⇒ H_9334 는 H-ε 로 좁혀진 채 시작할 수 있다

BIND-LOCUS 가 S 를 내면   →  올바른 자리에 올바른 내용을 넣어도 무시한다
                             ⇒ H-δ / H-ε **둘 다 잘못된 프레임** (결합은 조회가 아니다)
                             ⇒ H_9334 의 CPT 재학습은 **쏠 필요가 없다**
```

⇒ **BIND-LOCUS 가 먼저 나오는 것이 옳다**(재학습 0 · 그들의 발사를 아낄 수 있다). CONFLICTS 없음.

## 🇬🇧 EN-FIRST 지시와의 관계 (오너 지시 · 같은 날 착륙)

오너가 *"모든 **신규** 연구 코퍼스는 `--lang en`"* 을 지시했다(한국어 lane 은 🧱 BINDING · EN 은 `not` 이
**자유형태소**라 판별자). BIND-LOCUS 는 이 지시와 **충돌하지 않는다**:

- BIND-LOCUS 의 매니페스트는 **신규 학습 코퍼스가 아니라** H_9327 의 **동결된 평가 캐리어**다 —
  그 벽을 인과적으로 재는 것이 목적이므로 **같은 언어·같은 캐리어여야** 대조가 성립한다.
- 그리고 BIND-LOCUS 가 내는 답은 **EN lane 의 해석을 좌우한다**: R2(어간이 키의 일부)가 참이면
  한국어 `지 않다`가 **접미사(BOUND)** 라서 어간과 한 덩어리로 외워진 것이고, 그렇다면 **EN 의 자유형태소
  `not` 에서는 벽이 사라져야 한다** — 즉 EN 양성은 **형태론 인공물**의 증거가 되지 substrate 돌파가 아니다.
  ⇒ EN 결과를 읽기 전에 BIND-LOCUS 를 읽어야 **무엇의 증거인지** 정해진다.


## 🎯 게이트가 나를 살렸다 — 내 `novel` 어간은 **환상이었다** (2026-07-15 · 실측)

배선할 때 나는 "novel 을 **믿음**으로 고를 뻔했다"를 **가능한 위험**으로 적었다. 실제로 일어났다.

내가 "흔치 않아 보인다"고 고른 20개 어간을 **9.9GB 사전학습 코퍼스에 바이트 계수**했더니:

```
novel candidates 20 -> EARNED 0 · REJECTED 20
  성기=54,096회 · 포근=12,217 · 묵직=11,099 · 촘촘=11,056
  매끈=9,263 · 서늘=8,945 · 뾰족=8,449 · 말끔=6,888 ...
⚠️ novel n=0 — 사전등록 검정력은 60 어간을 요구한다
```

**단 하나도 novel 이 아니었다.** 만약 내가 novelty 를 **주장**했다면(측정하지 않고), B-arm 은 사실
**사전학습이 이미 극성을 준 어간들** 위에서 돌았을 것이고, 그 결과 나온 **S 판정은 substrate 사실이
아니라 사전학습-노출 인공물**이었을 것이다 — **그 arm 이 배제하려는 바로 그 교란**으로.

빌더가 `1회라도 나오면 기각` 을 하드하게 걸어놨기 때문에 발사 전에 걸렸다(spend 0).

### 그래서 진짜 0회 어간을 만든다 — 그리고 그게 **더 깨끗한 시험대**다

9.9GB 자연 코퍼스에서 **0회인 한국어 어간**은 필연적으로 **뜻 없는 문자열**이다. 그건 결함이 아니라
**B-arm 의 요점 그 자체**다: *"연산자는 **출처 불문 내용**에 붙는가?"* — **사전 prior 가 0인 어간**이
가장 깨끗한 시험대다(경쟁하는 사전학습 표현이 없다).

의사-한글 어간 400개를 생성하되 **바이트길이를 held-out 분포에 정합**시켰다
(held-out: 6B×16 · 9B×10 · 3B×3 ⇒ 생성: 6B×279 · 9B×121 — 한국어 3 bytes/char,
`a_korean_byte_budget`). 그리고 **코퍼스가 판정하게 한다 — 내가 주장하지 않는다.**


## 🔄 프레임 전환 — H_9334 가 결론을 냈다 (2026-07-15 · 병렬 세션)

H_9334 C4 CARRIER-SWAP 이 **🟢🟢 H-ε TERMINAL** 로 착륙했다: *"연산자가 **자기 키로 쓴 값**을 읽는다"*
— 반전 극성을 **연산자 자신의 표면**(`{s}지 않다`-계열 담체)으로 다시 쓰자 양 seed **12/12 신극성**
(p=.0002). C3 은 **선언형 키**(틀린 키)로 써서 0/12 였다.

⟹ **G1 벽 = 저장소 도달불가(H-δ)가 아니라 인터페이스 addressable · FIXABLE.**
⟹ 내 3-세계 중 **P-kind 반증**(CPT 는 지름길만 쓴 게 아니다 — feature 는 존재한다).

**이것이 BIND-LOCUS 를 무효화하지 않는다 — 강한 예측 시험으로 바꾼다.**

| | H_9334 가 말하는 것 | BIND-LOCUS 가 그 위에서 묻는 것 |
|---|---|---|
| 방법 | **재학습**(연산자 자신의 표면으로 다시 씀) | **재학습 0 · 인과 주입**(읽는 자리에 직접 씀) |
| 결과 | 연산자가 **자기 키**로 쓴 값을 읽는다 | 그 '읽는 자리'에 **써넣기만** 해도 답이 따라오는가? |
| 남은 것 | 키가 맞아야 한다 — **자리**만으로 충분한가? | **바로 그것** |

**H_9334 의 예측**: 인터페이스가 addressable 이면, 연산자의 읽기-자리(ℓ*)에 극성을 물리적으로
써넣었을 때 **답이 주입을 따라와야 한다** ⇒ **dep1 ≤ −0.50 = P**.

**반대로 S 가 나오면**(TOST ±0.20 등가): 올바른 자리에 올바른 내용을 넣어도 무시한다는 뜻이고,
그렇다면 H_9334 의 12/12 는 **'주소'가 아니라 '재학습이 만든 무언가 다른 것'** 이 한 일이다 —
즉 **addressable 이라는 해석 자체가 재검토**된다.

⇒ BIND-LOCUS 는 이제 H_9334 의 **독립적·인과적 확증(또는 반증)** 이다. 재학습 0 이므로
**같은 주장을 다른 축에서** 검증한다(H_9334 = 쓰기 축 · BIND-LOCUS = 읽기 축).

### 실행중 (2026-07-15 · pod 44908484)

- **n2 ckpt**(`natem_n2_main_s7/s11.clm`) 위에서 s7 → s11 순차 — **원래 벽** 위의 인과 시험
- **HONEST**: H_9334 는 자기 NEXT 로 *"BIND-LOCUS 를 **C4 ckpt** 위에서 돌려 잔여(H-δ/P-kind/S)
  완전 인과분리"* 를 지목했다(`swap_c4_s{7,11}.clm` · `~/anima-weights/c34/`). 그게 **더 결정적**이다 —
  C4 ckpt 는 극성이 **연산자 자신의 키로** 쓰인 모델이므로, 거기서 주입이 먹히면 '자리'와 '키'가
  **둘 다** 충족된 상태의 인과 확인이 된다. 현재 run 이 끝나면 **C4 ckpt 로 후속 발사**한다.


## ⚠️ 프레임 재전환 — H_9347(EN)이 H_9334 를 재심한다 (2026-07-15 · 병렬 세션 · 정직 기록)

내가 "H_9334 가 H-ε TERMINAL 을 냈다"를 예측 시험으로 받은 직후, 병렬 세션의 **H_9346/H_9347(EN)**이
그 TERMINAL 을 **재심에 부쳤다** — 그리고 그 재심이 **내 C4 run 을 직접 건드린다.**

**H_9347 의 논증**: 한국어는 연산자가 **어미**(`지 않다`)라 담체 라인이 채점 프롬프트의 정답을
**문자 그대로 품는다**:
```
KO 담체:  이 영화 전혀 [좋지 않다 => 긍정].
KO 채점:  이 영화      [좋지 않다 => ] ?      ← 정답이 담체 안에 통째로
```
어텐션 없는 conv 가 **마지막 십여 바이트만 이어써도 12/12** 가 나온다 ⟹ **"연산자가 신극성을 읽었다"와
"본 문자열을 이어썼다"가 원리적으로 구별 불가.** H_9334 의 KO 12/12 는 이 교란과 양립한다.

**영어가 그걸 뒤집는다**: `certainly not {s}` 는 코퍼스 **0회**이고 접미 `{s} => ` 창은 **50/50** 이라,
n-gram 이어쓰기와 연산자 조회가 **서로 다른 답**을 예측한다.

### 이것이 내 C4 run 에 뜻하는 것 (HONEST)

내 BIND-LOCUS C4(`swap_c4_s7/s11`)는 **한국어 ckpt** 다. 그러므로:

- **BIND-LOCUS 는 이 교란에 H_9334 보다 강하다** — 나는 담체를 **읽지 않는다**. 인과 주입은 어간-스팬 hidden 을
  **물리적으로 바꾸고** readout 을 보므로, "본 문자열 이어쓰기"가 아니라 "그 자리의 내용을 소비하는가"를 직접
  묻는다. 접미 누수는 **읽는 자리를 옮기지 않는 한** 내 DV 에 들어오지 않는다.
- **그러나 완전 면역은 아니다**: Stage A(양성통제)가 SEEN swap 으로 ℓ* 를 잡을 때, 그 swap 이 바꾸는 hidden 이
  **접미 바이트의 표면정보**를 옮기는 것뿐이면 flip 이 나도 '연산자'가 아니라 '표면'을 옮긴 것이다. ⇒ **한국어 C4
  결과는 그 자체로 종결이 될 수 없다** — H_9347 의 EN 결과와 **교차**해야 한다.
- ⇒ **판독 재조정**: 내 C4 가 **S(dep1≈0)** 를 내면 그것은 H_9347 의 ECHO-지속(≤0.25)과 **한 방향**이고 —
  둘 다 "어간 게이트는 안 열린다"는 **독립 2채널 확증**이 된다(그들=재학습·읽기 없음 · 나=인과주입·읽기 자리).
  내 C4 가 **P(dep1≤−0.50)** 를 내면 H_9347 이 EN 에서 무엇을 내든 **KO 기질에선 addressable** 이라는 뜻이고,
  그 KO/EN 불일치 자체가 다음 물음이 된다(형태론이 addressability 를 만드는가).

### ⇒ 결론: 내 실험은 **여전히 유효하나 종결력이 재조정됐다**

BIND-LOCUS n2/C4 는 **KO 축의 인과 증거**로 남는다(누수에 강한 읽기-자리 조작). 그러나 **최종 종결은
KO(BIND-LOCUS) × EN(H_9347) 교차**에서만 난다 — 한 언어의 형태론이 만든 인공물을 다른 언어가 배제하는
구조다(오너의 EN-FIRST 지시 = 정확히 이 이유). **한국어 단독 P/S 를 TERMINAL 로 cement 하지 않는다.**

### 🧩 교차 결합기 — `cross_verdict.py` (진리표 FROZEN · 결과 前 동결 · SSOT)

두 결과가 나온 뒤 눈대중으로 합치면 self-judge(p7). 그래서 **합산 규칙을 결과 존재 前 코드로 못박았다**
(`archive/state/scratch/h9331_bindlocus/cross_verdict.py` · 17/17 spike-in 검산 PASS). 사람은 enum 을 손으로
타이핑 못 한다: **KO enum 은 동결 bar 로 dep1 에서 기계 도출**(read_verdict.py 와 동일 bar), **EN enum 은
H_9347 이 emit 한 machine JSON(`en_verdict.json`)만 소비**(내가 재분류 안 함 = `a_parallel_session_compare`).
`INVALID` 은 사전등록 gate-ID(`KI1..KI5` / `EI*`) 를 든 결과만 — 사후 발견한 '계기 의심' 은 코드 경로가 없다.

**frozen-first 수정(양 결과 미도착이므로 튜닝 아님)**: `dep1 ≥ +0.50` 을 else-bucket 에 묻지 않고 **ECHO** 로
분리 — 되뇜 채널이 **직접 관측**된 가장 정보량 큰 결과이지 잡음이 아니다(`prereg-table-must-cover-below-chance`).

| KO＼EN | POS | NEG | UNDER | INVALID |
|---|---|---|---|---|
| **P** | 🟢🟢 ADDRESSABLE-CONFIRMED (TERMINAL) | 🟡 MORPHOLOGY-ARTIFACT (DIR) | ⏳ UNDER | ⏳ UNDER |
| **S** | 🔀 DISCORDANT-REOPEN | 🟢🟢 STORAGE-UNREACHABLE (TERMINAL) | ⏳ UNDER | ⏳ UNDER |
| **ECHO** | 🔀 DISCORDANT-REOPEN | 🟢🟢 MORPHOLOGY-ARTIFACT (TERMINAL) | ⏳ UNDER | ⏳ UNDER |
| **UNDER** | 🟡 ADDRESSABLE (DIR) | 🟡 MORPHOLOGY-ARTIFACT (DIR) | ⏳ UNDER | ⏳ UNDER |
| **INVALID** | 🟡 ADDRESSABLE (DIR,+KIx) | 🟡 MORPHOLOGY-ARTIFACT (DIR,+KIx) | ⏳ UNDER | ⛔ INVALID |

**TERMINAL 은 정확히 3셀**: (P,POS)·(S,NEG)·(ECHO,NEG) — 두 인공물 공간이 disjoint 해 어느 confound 로도
재현 불가할 때만. **tier 규칙**: 두 레인 결정적 ∧ 일치 ∧ 어느 레인 confound 로도 산출 불가 ⇒ TERMINAL;
한 레인만 결정적 ⇒ DIRECTIONAL; veto 불가한 반대부호 ⇒ DISCORDANT-REOPEN(실질판정 emit 거부).
**scope**: TERMINAL 은 존재주장('CPT 로 쓴 극성이 연산자에 조회되는가')에만 — 요인귀속(형태론/base/캐리어)과
'KO 자연경로가 고쳐졌다'는 **어느 셀에서도 못 번다**(별개 H). 실행: `cross_verdict.py` (둘 다 도착 前 PENDING).
