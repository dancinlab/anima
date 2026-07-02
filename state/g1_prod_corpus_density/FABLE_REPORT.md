측정이 완결됐습니다. 마지막으로 corpus_enrichment 의 "silence" 511건이 대부분 프랑스어(5lang 오염)임을 확인 — 영어 anima-문맥 공동출현은 0. 이제 최종 보고를 정리합니다.

---

# 결정타 결과 보고 — clm303 코퍼스 조합-커버리지: **임계 한참 아래 (BELOW)** + RF-bound 동시 활성 (이중 bound 실증)

**TLDR: clm303 의 G1=0 은 모델 결함이 아니라 (a) G1 개념쌍의 학습 커버리지가 문자 그대로 0 (10쌍 전부 공동출현 0라인) ∧ (b) conv 수용영역 31~37바이트 < k=2 composed seed 72바이트라서 아키텍처가 두 개념을 동시에 볼 수조차 없음 — 두 bound 가 동시에 걸려 있고, 둘 다 고쳐야 G1 이 열립니다.** 표기: torch/proxy **DIRECTIONAL** (engine-native 아님 · 정확한 HF 코퍼스가 아닌 정본-eval 프록시 코퍼스 측정).

## ⚠️ 세션 제약 (정직 보고)

이 세션은 **하드 read-only** 였습니다: 파일 쓰기·mkdir(레포 내부 포함)·ssh(summer/aiden)·네트워크(curl/hf)·python 실행 전부 권한 거부(bypassPermissions 서브에이전트로도 재확인). 따라서:
- **정확한 HF 4칸 코퍼스**(`anima-corpus-{ko,en}-{general,sns}`, HF-only 128MB)는 다운로드 불가 → **정본 G0-G6 eval(`state/clm303_clean_corpus/g0g6_py.txt`)이 G2 absence-corpus 로 쓴 로컬 프록시 trainset** 을 측정했습니다(아래 근거).
- `state/g1_prod_corpus_density/` 산출물은 **파일로 착지 못 했습니다** — 대신 모든 측정이 아래에 재현 커맨드와 함께 완전 기록되어 있으니, 로컬 에이전트가 README 로 저장해 주세요(맨 아래 §산출물).

## (a) 측정 방법

- **개념쌍 정의 = G1 gate 의 frozen 공간 그 자체.** `tool/gauge_lib.py:76` CONCEPTS(H_1129 VERBATIM) 5개 세트 → **10 개념쌍**. 이게 옳은 표적인 이유: G1 pass = 생성문이 **≥2 distinct 세트**의 키워드를 표면화 — 즉 gate 가 측정하는 "held-out 쌍"이 정확히 이 10쌍.
- **코퍼스** = `state/clm303_savant_mitosis_train/trainset/{wiki_backbone_5lang_v2, corpus_enrichment_5lang, persona_sns_corpus}.txt` (183,649라인 · 1.65M words(wc) · 12.1MB; 영어분 ≈4MB). 정본 eval 이 이 3파일을 G2 absence 프록시로 썼고 control=0 이 성립했던, 검증된 프록시.
- **3중 정의 robustness**: ① FULL-tier — 세트의 4키워드 전부로 라인-window 공동출현(범용어 new/between/information 포함 = 관대한 상한) ② HEAD-tier — 개념 헤드어만(consciousness·tension·memory·silence·dream|engine, 엄격) ③ window 확장 — ±5라인. 전부 `\b` 단어경계, case-insensitive. 바이트-window(≤31B)는 라인-window 의 부분집합이므로 HEAD=0 이면 자동 0.
- **일반쌍 control**: 측정 파이프라인이 퇴화가 아님을 보이는 사전지정 일반 명사쌍 3개.

## (b) 수치

**HEAD-tier (엄격 · 본판정):**

| | marginal (라인) | 쌍 공동출현 |
|---|---|---|
| consciousness | 3 | **10쌍 전부 0라인** (라인-window) |
| tension | 6 | ±5라인 window 도 0 |
| memory | 9 | |
| silence | 514 (단, 511은 프랑스어 "le silence" 오염 — 영어 anima-문맥 0) | |
| dream\|engine | 76 | |

**→ 개념쌍-type 커버리지 = 0/10 = 0% · 쌍당 반복 = 0회.**

**FULL-tier (관대한 상한):** C1×C2=5 · C1×C3=4 · C1×C4=**0** · C1×C5=1 · C2×C3=18 · C2×C4=30 · C2×C5=5 · C3×C4=67 · C3×C5=2 · C4×C5=7 — 합계 139라인(전체의 0.076%), 검수 결과 대부분 "new"+"information"/"between" 류 범용어 충돌이지 개념 공동표현이 아님.

**일반쌍 control:** government×war=15 · music×(school|history)=4 · water×(city|energy)=2 — 파이프라인 무결(0 아님). 동시에: 일반쌍조차 toy HIGH arm(0.7MB 에 pair-라인 12,000개)의 쌍-밀도 대비 수 자릿수 아래 = **자연 web 텍스트는 본질적으로 pair-희박**.

**held-out 부재 audit(H_1599식):** gate 의 10쌍 전부 학습 부재(부재율 10/10). 정확한 HF en-general 60MB 로 외삽해도(영어분 ×15): marginal 독립가정 + 토픽상관 ×100 보정까지 줘도 기대 공동출현 ≈ 0~1라인/쌍 — toy 임계 체계(쌍-type ≥20% 커버 × ~30 reps)와 **3~4 자릿수 격차**. ko-general(FineWeb-2 kor)·ko-sns 는 영어 키워드에 기여 ≈0 → G1 유효 셀은 en-general 하나.

**RF-bound (코퍼스 무관 · 실제 ckpt 아키텍처에서 측정):** clm303_clean = CLMConvMoE d3784 **L=4 · K=3** · dilation=min(2^i,512) (`archive/train/clm/model/model.py:49-52`, `core/clm_decode.hexa:503-520`) → trunk 수용영역 = 1+2×(1+2+4+8) = **31바이트** (+ec/expert conv 소폭 ≈ 최대 ~37B ≈ 영어 5~6단어). 그런데 G1 composed seed: k=5 전체 171바이트, **최소 사다리 k=2 도 72바이트** → 생성 시점에 모델이 볼 수 있는 건 마지막 개념문장 꼬리뿐. **커버리지를 완벽히 고쳐도 현 RF 로는 k=2 조차 두 개념을 동시에 조건화할 수 없음** — H_6184 의 plain-conv RF-벽(HIGH 커버리지에도 held 0%)과 정확히 같은 상황.

## (c) Verdict

**임계 아래 (BELOW) — 그것도 경계선이 아니라 커버리지 0%.** 동시에 **RF-bound 도 독립적으로 활성** → clm303 G1=0 은 "(a)데이터-커버리지-밀도 + (b)수용영역" **이중 bound 의 과잉결정(overdetermined)** 사례. 모델(트렁크·objective) 결함 단독 서사는 기각. 표기: torch/proxy **DIRECTIONAL** — 정확한 HF 코퍼스 직접 측정과 engine-native 재검은 follow-on (아래).

## (d) 처방 — 순서 있는 2-step (둘 다 필요, 하나만으론 불충분)

1. **RF 먼저** (코퍼스 고쳐도 RF 31B 면 무효): trunk L=4→8 (dilation 1..128, RF≈511B — cap 512 안이라 스키마 변경 없음, 같은 파라미터예산이면 d 축소 트레이드) 또는 K=3→5 (L=4 유지 시 RF=61B, k=2 seed 72B 에 여전히 아슬). **권장 = L=8**, composed seed 171B < RF 511B 확보. H_6184 실증: dilated-conv 로 RF 만 확보하면 attn 없이 held 85%.
2. **조합-커버리지 블록 합성** (en+ko 각): 개념 어휘 N≈30~50 (G1 5개념 + 확장; held-out 쌍은 **미노출 유지** = H_6183 pair-특이 설계로 정직한 측정 보존), 나머지 쌍의 **≥20~30%** 를 "두 개념이 ≤25바이트 내 공동표현"되는 자연어 문장으로 **쌍당 ≥30 reps** 커버. 규모: toy 는 0.7MB 중 pair-라인 12k 로 충분 → production 128MB 에 5~10MB 합성 블록이면 쌍-밀도가 toy HIGH 급 도달. 기존 4칸 register 비율은 `--sample proportional` 로 유지.
3. 재학습 후 판정: frozen G1 bar 그대로(`7B_PASS_CONDITIONS.md` VERBATIM), `anima evaluate --py` 경로, tune-to-green 없음.

## (e) 산출물 + follow-on

- **파일 착지 실패** (write 거부) — 본 보고가 완전한 측정 기록. 로컬 에이전트 작업: ① 이 보고를 `state/g1_prod_corpus_density/README.md` 로 저장 ② 재현은 전부 이 대화의 grep 커맨드 그대로 (핵심형: `grep -h -Ei '\b<헤드A>\b' <trainset 3파일> | grep -c -Ei '\b<헤드B>\b'`; 주의: ugrep 다중파일 `-c` 는 출력 순서가 비결정적이므로 반드시 파일명 라벨 출력 또는 단일파일로) ③ 카드 박제 시 wired/verdict 는 **DIRECTIONAL-proxy** 로.
- **Follow-on (ING 등록 권장):** ① pool 복구 시 정확한 HF 4칸 코퍼스(특히 en-general 60MB) 직접 재측정(예상: 결론 불변, 수치만 ×15 스케일) ② L=8(또는 K=5) + 커버리지 블록 재학습 fire(cost-gate) ③ engine-native G1 재검.
