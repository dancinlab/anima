# H_9290 — NAT-ATOM: 형태소 원자성이 자연-분포 held-out 접지를 rescue하는가

## tier
🧱 **NO-RESCUE (DATA-🧱)** — codec 형태소 원자성은 자연-분포 held-out 술어 극성 접지를 **rescue하지 못한다**
(2026-07-13 · engine-native 303M · pod 44684279). codec-CPT(자연코퍼스·drill 無) frozen 표상의 held-out
술어 극성 G-PROBE = **0.345** — 우연(0.5)·raw-byte 기준(N2 0.5517)보다 **낮음**. RESCUE=false.

## 질문 (2×2 완성 셀)
G1 자연창발 프런티어의 2×2가 이 카드로 닫힌다:

| | 합성 신호(drill/curated) | 자연 분포 |
|---|---|---|
| **raw utf-8** | XBIND 🟢 CRACK (H_9267) | N2 NAT-CRACK 반증 🧱 (H_9286) · G-PROBE INFO-ABSENT 0.55 (H_9289) |
| **codec 원자성** | MORPH-ATOM 🟢 (H_9288 · M 0.908 ≫ C1 0.617) | **← 이 카드: NO-RESCUE 🧱 (0.345)** |

즉 "원자성이 raw-byte가 실패한 자연접지를 구제하는가?"가 유일한 미측정 셀이었고, 답은 **아니오**.

## 방법 (reference-match · H_9289 프로토콜 verbatim)
- **모델**: base 303M → reinit-embed → **CPT 16k on 자연 codec 코퍼스**(`cpt_M.bytes` = MORPH-2B codec으로
  인코딩한 NSMC 자연 한국어 120k lines · **drill 無 · 등가 handed 無**). 자연 분포만.
- **프로브**: `gt_step0_gprobe.py` 프로토콜 그대로 — frozen 표상 dump-hidden(d=3784 penultimate) → 원자별
  mean-pool → L2-logreg(train P_grid 20원자 극성 → test held-out P_nat 29원자). frozen 자산(gt_atoms/gt_prompts
  1176 문맥) 그대로 재사용 = cherry-pick 0.
- **차이는 tokenization 하나** — raw-byte(N2) vs codec-원자성(이 카드). 그 외 프로토콜·자산 동일.

## 결과
| 지표 | 값 | 판정 |
|---|---|---|
| held-out probe-acc (codec_Mnat) | **0.3448** | bar 0.65 크게 미달 · 우연 0.5 **아래** |
| train_fit | 1.0 | 프로브 유효(train 원자 완벽 적합) |
| shuffle floor | 0.4948 | 정상 우연층 |
| Δ vs shuffle | **−0.150** | 음수 = 전이 신호 0 |
| raw-byte 기준(N2 #3372) | 0.5517 | codec이 **더 낮음** |
| **RESCUE** | **false** | |

train_fit=1.0 ∧ shuffle≈0.5 ⟹ 프로브는 유효, held-out 전이만 실패(=INFO-ABSENT). 0.345가 우연 아래인 것은
29개 held-out 원자에서의 무신호 잡음(음의 소편차)으로 읽는 것이 정직 — 요지는 "선형 판독 가능한 극성 정보 없음".

## 해석 (정직)
- **원자성은 신호를 만들지 못한다** — 데이터에 없는 것을 tokenization이 창발시키지 못함. 자연 부정-XOR 신호는
  이미 model-free 감사에서 얇았다(`a0neg` d_nat=42.3 events/MB · n_qualified 27<30 · flip_frac 0.594<0.75 =
  **NOT POWERED**). N2(raw NAT-CRACK 반증) + G-PROBE(INFO-ABSENT) + 이 카드(codec도 NO-RESCUE) 3중 정합.
- **MORPH-ATOM(H_9288)과 모순 아님**: 원자성은 *drill이 flip을 가르칠 때* held-out 재조합을 **가능하게** 한다
  (M 0.908 ≫ C1 0.617). 하지만 *가르치지 않으면* 자연 분포만으로 접지가 **설치되지 않는다**. 원자성 = 능력의
  **증폭기**이지 신호의 **원천**이 아니다.
- ⟹ **G1 자연 자발창발의 병목 = DATA**(신호 밀도/접지 채널), substrate·tokenization 아님.

## 함의 · 다음
- 순수-자연 셀은 **DATA-🧱로 닫힘**(4개 셀 중 3개 측정 완료 · 나머지 1개=XBIND 🟢).
- 프런티어 다음 rung = **rung-2 하이브리드**(codec 원자성 + C3/C4 labeled-natural 접지 에피소드 · Fable 설계).
  단 정직 scope = "자연 자발창발"이 아니라 **라벨-자연 중간 rung**.
- scope: 1 seed(4302) · CPT 16k · custom harness(canonical `anima-py evaluate` 아님) · held-out 술어 극성
  단일 construct. 음성 결과이므로 TOST 등가 검정으로 cement하려면 사전등록 필요(negative-claims-need-tost).

## 산출
verdict=`state/verdicts/9290_nat_atom/` · gprobe=`~/anima-weights/morphatom/gprobe_codec_result.json`.
도구=`state/nbind_curriculum/` (gen_codec_natural.py·morphatom_dumphidden.py·morphatom_gprobe_run.py·fire_natatom.sh·install_ma.sh)
(+ reference-match `state/nbindg_grounding/gt_step0_gprobe.py`·`gt_atoms.json`·`gt_prompts.json`).
[[H_9288]] · [[H_9286]] · [[H_9289]] · [[H_9267]] · [[nbindg-grounding-frame-general-data-blocked]].

---

## ⚠️ AMENDMENT (2026-07-14 · H_9297 검정력 렌즈 · $0 재해석) — **NOT-POWERED 재분류**

H_9297(#3410)이 같은 NBIND-G G-PROBE 프레임의 검정력 부재를 확정했다: **held-out n=29 ⇒ 우연
sd = √(0.25/29) = 0.0928** 이라 동결 bar 0.65 가 우연에서 **1.62σ** 뿐이다. 본 카드의 판정도
**같은 프레임 위에 있다.**

보존된 수치를 그 렌즈로 다시 읽으면:

| | 값 | 우연 대비 |
|---|---|---|
| heldout_probe_acc | **0.3448 = 10/29** | **−1.67σ** (우연 **아래**) |
| 양측 정확검정 | | **p = 0.136** |
| 우연이 10/29 이하를 낼 확률 | | **7%** |
| shuffle 통제 | 0.4948 | 우연 |

⇒ **"형태소 원자성이 자연-분포 접지를 rescue 하지 못한다" 가 아니다.** 0.3448 은 우연 **아래**이고,
n=29 에서 그것은 **아래쪽 꼬리와 구별되지 않는다**. 우연 이하는 "신호 부재" 가 아니라 **역-신호
또는 표본 잡음**이며, n=29 로는 둘을 못 가른다.

**⚠️ 재측정 = spend 필요 (a_fire_recover_complete 위반의 대가).**
본 H 의 **codec-CPT ckpt**(base 303M → reinit-embed → 자연 codec 코퍼스 CPT 16k)는 pod 44684279
teardown 시 **로컬로도 HF 로도 pull 되지 않았다**. 남은 것은 드릴본 `drill_M.clm` 과 gprobe 결과
json 뿐이다. H_9297 이 상한 해제로 n=91 을 열었지만, **그 ckpt 없이는 재측정이 불가능**하다
⇒ n=91 재측정은 **codec-CPT 재학습(GPU spend)** 을 요구한다. $0 로 가능한 것은 위 재해석이 전부다.
(convergence `h-9290-codec-cpt-ckpt-a-fire-recover-complete-2026-07-14-1`)

**살아남는 것 / 죽는 것.**
- **영향 없음**: 2×2 프레임의 나머지 셀 — [raw×합성] XBIND 🟢(held-out 1.000) ·
  [codec×합성] MORPH-ATOM 🟢(0.908 ≫ 0.617). 이 둘은 bar 를 **크게** 넘겨 검정력 문제와 무관하다.
- **죽는 것**: **[codec×자연] 셀의 "🧱 NO-RESCUE" 결론.** ⇒ 2×2 는 **미완성**이다.
- H_9297 의 [raw×자연] EARNED 음성은 별개 측정(raw-byte N2 ckpt · 로컬 보존)이라 영향 없다.
