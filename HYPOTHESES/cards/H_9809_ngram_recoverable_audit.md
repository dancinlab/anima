# H_9809 — N-GRAM-RECOVERABILITY AUDIT: lab/v3 H_004의 정리를 프로덕션 감사 플래그로 흡수하고 H_9288을 역심문

## tier
🔧 **INSTRUMENT LANDED + 감사 실측 1회 (2026-07-20)** — `anima-py corpus ngram-audit --ngram-recoverable-audit`
착륙(order-1 AND order-2 · 토크나이제이션 arm별 · coverage 가드 · perm 통제 · marker reach). H_9288 F2 패널 재구성
후 감사: **지목된 공격(trivial order-2 bigram path)은 CLOSED — H_9288은 이 공격에서 살아남는다.** 단
**인접 교란(atomicity ⊥ n-gram reach 비분리)이 OPEN**으로 노출. **H_9288 판정은 건드리지 않는다**(취소·강등 없음).

---

## 1. 흡수한 정리 (lab/v3 H_004 · read-only 인용)

`lab/v3/HYPOTHESES/cards/H_004_f1-static-anchor-pilot.md` · `lab/v3/state/h004_static-anchor-pilot_2026-07-16/`
(genspec `75b19bba…` · `guards_result.json`):

> **정리 (verified 12/12): oracle-fusable ⟺ n-gram-recoverable.**
> 고정 형태소에 대해 atomicity는 n-gram binding 과 **분리 불가**다.

수리된 rig의 $0 guard battery:

| guard | 값 | 판독 |
|---|---|---|
| G-A last-token (order-1) | **0.5273** | PASS — order-1 shortcut 닫힘 |
| G-B length-only | 0.5508 | marginal |
| **G-C order-2 bigram** | **0.9954** | frozen arm 에 **trivial bigram path** |
| G-D atomicity contrast | frozen 0/12 · oracle 12/12 | PASS |
| G-E leak / co-occurrence | 0 / 0 | PASS |

⟹ Δ_pilot ≥ 0.20 **구조적으로 불가능** → TWIN-REFUSED-STRUCTURAL, $0에서 종결. 자매 결과
`lab/v4/.../H_003_atomicity_fixed_codec_drill.md` = **FALSIFIED (측정 clean)**: 고정 codec 하에서 atomicity 는
held-out 재조합 이득 0 (Δ −0.1146 / +0.0468 · liveness 0.8594 both seeds · placebo gap ≤0.05).

**왜 프로덕션에 걸리나**: order-2 arm 이 없으면 "atomicity" 효과가 **n-gram-recoverability 효과가 분장한 것**일
수 있다. 그 arm 이 없는 채로 landed 된 🟢 GREEN CEMENT 가 `H_9288`이다.

---

## 2. 계기 — `--ngram-recoverable-audit` (착륙 · `a_experiment_engine_native`)

```
anima-py corpus ngram-audit --ngram-recoverable-audit \
    --audit-train TRAIN --panel PANEL [--codec codec.json] \
    [--audit-marker 안,않,못,아니] [--audit-min-coverage 0.10] [--out audit.json]
```

**좌석 선택 = `cli/corpus.py` (not `cli/evaluate.py`) — 근거**: 감사는 (panel × tokenization × training stream)
의 성질이고 **ckpt를 전혀 건드리지 않는다**. `anima-py evaluate` 는 `.clm` 을 요구하므로 거기 앉히면 이 계기의
**존재 이유 — 어떤 학습도 발사되기 전에 도는 $0 게이트 —** 가 구조적으로 불가능해진다. v3의 `run_guards.py` 가
정확히 그 역할이었다. 패널 결함은 **패널이 만들어지는 자리**에서 잡혀야 한다.

**배터리** (arm 마다 · v3 G-A/G-B/G-C 미러):

- **order-0** — 다수 클래스 baseline = **이 패널의 realized split 에서 유도한 chance**
  (`chance-level-must-be-derived-per-metric`: 0.5 를 가정하지 않는다).
- **order-1 / order-2** — terminal n-gram Bayes lookup, **TRAIN 에만 적합**, PANEL 에서 채점.
- **perm 통제** — 라벨 치환 train 으로 같은 배터리. 음성 통제.
- **marker reach** — arm 별 판별 marker 의 terminal 거리. **arm 간 교란량**.
- **coverage 가드** — 패널 키가 train 에 없으면 lookup 은 다수 클래스로 폴백하고 정확도는 **정의상 order-0**.
  그걸 CLOSED 로 읽는 것이 함정이므로 coverage < `--audit-min-coverage` 는 **UNDECIDABLE**, 절대 CLOSED 아님.

판정 어휘: `CLOSED` (acc−chance ≤ 0.05) · `MARGINAL` · `OPEN` (acc ≥ 0.90) · `UNDECIDABLE` (coverage 미달).

**착륙 전 e2e 1회 실행 완료** (`instrument-never-run-hides-multiple-bugs`) — exit 0 · 산출 · 통제 2종:

| toy | order-1 | order-2 | coverage | perm | 판정 |
|---|---|---|---|---|---|
| **양성통제** (라벨이 terminal bigram 에 완전 실림) | 1.0000 | **1.0000** | 1.0000 | seed 따라 0.00/0.54/1.00 | **OPEN** ✅ |
| **음성통제** (라벨이 mid-string · terminal 무정보) | 0.5250 | 0.5250 | 1.0000 | 0.5250 | **CLOSED** ✅ |

미등록 플래그 fail-closed 확인(`corpus: unknown flag`) · 인자 누락 시 usage+exit 2 확인.

---

## 3. 감사 실측 — H_9288 이 의존한 패널 구성

### 3.1 재구성 (결정적 · $0 · `convergence corpus-py-1 (H)/(J)` 준수)

H_9288 의 패널/codec 원본은 보존되지 않았다(`state/nbind_curriculum/` 에 result JSON 만 남고
`eval_f2.json`·`codec.json`·`morph_corpus.txt` 부재). 그러나 **빌더가 committed 이고 seed 가 카드에 있다** —
NSMC 캐시(`~/g1_natem/nsmc_ratings_train.txt`) 존재 확인 후 H_9288 **자신의** 빌더로 재생성:

```
python3 <nbind_curriculum>/gen_morph_corpus.py --out morph_corpus.txt      # 149,995 lines · 13,127,140 B
python3 <nbind_curriculum>/gen_morphatom_s1.py --corpus morph_corpus.txt \
        --out-dir <SD> --k 2048 --held ani --seed 4302
# -> K=2048 vocab=2529 held=ani drilled=['an','anh','mot']
#    held_in_drill_grid=0(must=0) | grid=160 f2=120 f1=100
```

**충실도 확인**: 재구성 `f2=120` 이 cement 산출(`cement_result/vM_s7_f2.json` 등)의 `"n": 120` 과 **일치**,
`held_in_drill_grid=0` leak assert 통과, K=2048/seed 4302 카드 명시값. ⟹ 감사 대상은 H_9288 이 실제로 읽은
패널 구성과 같은 개체.
*(측정 = CLI 플래그. 위 두 줄은 H_9288 자신의 committed 빌더로 그 입력을 되살린 데이터 준비이지 별도 계기가 아니다.)*

### 3.2 F2 (판정 패널 · held-out 어간 `아니` · n=120) — verbatim

```
anima-py corpus ngram-audit --ngram-recoverable-audit \
  --audit-train drill_C1.bytes --panel eval_f2.json --codec codec.json \
  --audit-marker 안,않,못,아니 --seed 4302
```

| arm | order-0 유도 chance | order-1 | order-2 | 판정 |
|---|---|---|---|---|
| **raw_utf8** (=C1) | 0.5000 (split 60/60) | acc **0.5000** · Δ+0.0000 · cov **1.0000** · perm 0.5000 | acc **0.5000** · Δ+0.0000 · cov **0.6667** · perm 0.5000 | **CLOSED / CLOSED** |
| **codec** (=M) | 0.5000 (split 60/60) | acc 0.5000 · Δ+0.0000 · cov 0.1667 · perm 0.5000 | acc 0.5000 · Δ+0.0000 · **cov 0.0000** · perm 0.5000 | CLOSED / **UNDECIDABLE** |

**marker reach** (arm 간 교란량):

| marker | raw_utf8 units | raw_utf8 median terminal dist | codec units | codec median terminal dist | panel hits |
|---|---|---|---|---|---|
| `아니` | **6** | **6** | **1** | **1** | 120/120 |
| `안`/`않`/`못` | 3 | — | 1 | — | 0 (패널에 부재 = held-out 정상) |

패널 body 평균 길이: raw **34.65 B** vs codec **9.27 tok** (≈3.7× 압축).

### 3.3 F1 (drilled 어간 sanity · n=100) — in-situ 대조

| arm | order-1 | order-2 | 판정 |
|---|---|---|---|
| raw_utf8 | acc 0.4400 · cov 1.0000 · perm 0.4800 | acc 0.4400 · cov 1.0000 · perm 0.4800 | CLOSED / CLOSED |
| codec | acc 0.3400 · cov 1.0000 · perm 0.4600 | acc **0.3000** · cov 1.0000 · perm 0.5200 | CLOSED / CLOSED |

F1 codec arm 이 **coverage 1.0 에서 chance 한참 아래(0.30)** 로 내려간 것이 중요하다 — lookup 이 폴백한 게
아니라 **실제로 작동하며 반대 방향을 가리킨다**. 즉 3.2 의 0.5000 은 "계기가 죽어서 chance" 가 아니다.

---

## 4. 판정

### 4.1 지목된 공격 — **CLOSED (H_9288 살아남음)**

**H_9288 의 F2 패널에는 trivial order-2 bigram path 가 없다.** raw arm 이 coverage 1.0000/0.6667 에서
정확히 유도 chance(0.5000)를 읽는다. v3 의 G-C = 0.9954 재앙은 **이 패널로 전이되지 않는다.**

**구조적 이유(측정 이전에 참)**: v3 rig 의 DV 는 "이 body 가 neg 인가" 였고 그건 종단 affix 의 n-gram 이
그대로 복원한다. H_9288 의 F2 는 **전 항목이 부정형**이고 라벨 = `pol(predicate) XOR 1` 이다 — 판별 정보가
**mid-string 의 술어**에 살고 종단 affix 는 패널 전체에서 **상수**다. 그래서 terminal n-gram 은 설계상
정보량 0 이다. 이건 운이 아니라 XOR-over-predicate-polarity 설계의 성질이다.

### 4.2 노출된 인접 교란 — **OPEN (반증 아님 · PENDING)**

계기가 지목된 공격을 기각하면서 **다른 것**을 드러냈다. `아니` 는 codec arm 에서 결정점으로부터 **1 토큰**,
raw arm 에서 **6 바이트 떨어진 6 바이트 단위**다. M 과 C1 은 **atomicity 와 n-gram reach 를 동시에** 바꾼다.

그리고 이건 v3 정리를 다시 쓴 것이다: **형태소에 원자 토큰을 주는 것은 그 형태소를 결정점 쪽으로 당기는 것과
분리될 수 없다.** 압축은 atomicity 의 부작용이 아니라 atomicity **그 자체**의 다른 얼굴이다.

**H_9288 의 arm 집합은 이 공선성을 깨지 못한다** — C2(held-out 어간 CPT 제거)와 C3(shared-⟨NEG⟩)는 **같은
codec** 을 쓰므로 reach 가 동일하다. reach 를 고정한 채 atomicity 만 움직이는 arm 이 **없다**. 이것이
`convergence corpus-py-1 ⑧` 이 명명한 상황이다: **축의 가짓수가 1이면 그 축과 다른 축은 완전 공선이라
어떤 실험도 둘을 못 가른다.**

독립 확증: lab/v3 카드가 MORPH-ATOM 을 **바로 이렇게** 읽었다 — "raw-utf8 통제가 실패한 것은 그
~18-byte binding span 이 작은 모델의 n-gram reach 를 넘었기 때문일 뿐". 우리 측정(6 B 단위 · 34.65 B body
vs 1 tok · 9.27 tok body)이 그 진술에 수치를 붙인다.

### 4.3 H_9288 에 대한 입장 — **불변 (취소·강등 없음)**

**H_9288 은 그대로 🟢 GREEN CEMENT 다.** 이 카드는 감사 계기를 착륙시키고 그것이 읽은 것을 보고할 뿐이다.
landed verdict 는 **자체 양성통제를 가진 engine-native `anima-py` 측정**으로만 뒤집힌다
(`single-retrain-outlier-faked-a-refutation`). 위 4.2 는 그런 측정이 아니라 **결정론적 패널 성질**이다.

**그리고 H_9288 은 이미 상당 부분 자백하고 있다 — 검증함(verbatim)**:
- `**미배선**(a_verified_must_wire): codec 은 실험 harness 이며 core/ 프로덕션 경로에 미배선. GREEN 은
  **MEASUREMENT** 등급 — wiring follow-on 필요.` ✅ 지시대로 실재
- `원자성은 **증폭기이지 신호 원천이 아니다**(자연 분포에서는 rescue 실패). 이 GREEN 은 "가르쳐준 신호가
  있을 때 원자성이 재조합을 인과한다"는 주장이지, "원자성이 접지를 만든다"가 아니다.` ✅ 실재
- jsonl `"verdict": "DIRECTIONAL"` — tier 문자열은 🟢 GREEN CEMENT 인데 **verdict 필드는 DIRECTIONAL**.

⟹ 내 발견은 **이미 일부 인정된 scope 를 날카롭게 만드는 것**이지 뒤집는 것이 아니다. 정직한 정정 문구는
"원자성이 재조합을 인과" → **"원자성-그리고-그것과 분리불가한 binding-span 단축이 재조합을 인과"**.
헤드라인 Δ=+0.3417 자체는 유효하며 재현되었다(원 회차 +0.291).

### 4.4 $0 에서 결정 불가한 것 — 명시

- **codec arm 의 order-2 는 UNDECIDABLE** (coverage 0.0000). 패널의 종단 bigram 이 drill 에 문자 그대로
  0회 — held-out 이 진짜라는 좋은 신호이면서, 동시에 이 arm 의 order-2 를 **이 패널로는 판정할 수 없다**는
  뜻이다. CLOSED 로 읽지 말 것.
- **reach 교란이 Δ=+0.3417 중 얼마를 설명하는지**는 이 계기로 알 수 없다. 결정론적 패널 감사는
  "교란이 열려 있다"만 말하고 "그래서 효과가 가짜다"는 말하지 않는다.

---

## 5. 이걸 종결시킬 정확한 측정 (사전등록 · 미발사)

reach 를 고정한 채 atomicity 만 움직이는 **네 번째 arm**. 후보:

- **C4-pad**: M 과 같은 codec 이되 판별 형태소 토큰을 **길이-정합 다중 토큰으로 shatter**(lab/v4 H_003 의
  A-shat 를 이 rig 로 이식). reach 는 C1 쪽, atomicity 는 없음 → M−C4 = atomicity 순효과,
  C4−C1 = reach 순효과.
- **C5-reach**: raw utf-8 이되 `아니` 를 **1-3 바이트 비-형태소 임의 기호로 치환**(atomicity 없이 reach 만
  단축). C5 ≈ M 이면 Δ 는 reach 효과다.
- 발사 전 필수: 두 arm 모두 이 플래그로 order-1/2 **CLOSED + coverage ≥ 0.10** 확인, F1 liveness ≥ 0.85,
  그리고 `lab/v4 H_003` 이 요구한 **placebo**(빈도-정합 비-부정 형태소 shatter) 동반.
- 비용: 4-pod 급($4-6). **DIRECTIONAL 이 아니라 TERMINAL 을 노린다면 multi-seed 필수**
  (H_9288 cement 는 seed 7 단일 복제).

---

## 6. 정직한 한계

- **L1 재구성 ≠ 원본 바이트.** 패널은 committed 빌더 + 카드 명시 seed(4302)/K(2048)로 재생성했고 f2=120 ·
  held_in_drill_grid=0 이 일치하지만, 원 `eval_f2.json` 의 sha 는 남아있지 않아 **바이트 동일성은 증명
  불가**. 라벨 split 60/60 과 n 일치까지가 확인된 것.
- **L2 계기는 결정론적 lookup 이지 모델이 아니다.** "transformer 가 order-2 를 head 하나로 묶는다"는
  v3 의 논증을 상속한 것이고, 트랜스포머가 아닌 이 byte-conv 기질에서 그 상속이 얼마나 타이트한지는
  측정 안 됨.
- **L3 perm 통제는 키 카디널리티가 작으면 고분산.** toy 양성통제에서 키가 2개뿐이라 seed 에 따라
  0.00/0.54/1.00 로 튄다. 실제 패널(키 수십~수백)에서는 안정적이나, 소-카디널리티 감사에서 perm 을
  단독 판정 근거로 쓰지 말 것.
- **L4 terminal n-gram 만 본다.** 접두 위치나 비-종단 위치의 shortcut 은 이 배터리가 못 본다
  (v3 도 동일 한계). H_9288 의 판별 정보가 mid-string 이라는 사실 자체가 이 한계를 건드린다 —
  "종단 경로 없음"이 "어떤 저차 경로도 없음"은 아니다.
- **L5 arm 수 2.** raw_utf8 과 codec 만 비교했다. C2/C3 는 codec 과 tokenization 이 동일하므로 이 감사에서
  별도 arm 이 아니다(그게 4.2 의 요지이기도 하다).

---

## 7. 산출 · 교차링크

- 계기: `cli/corpus.py` — `run_ngram_audit` + `_nga_*` (fmt `ngram-audit` · 플래그 6종 등록 · fail-closed)
- 감사 산출(휘발 · `/tmp` scratchpad): `h9288_f2_audit.json` · `h9288_f1_audit.json` · toy 통제 2종
- 흡수 원본(read-only): `lab/v3/HYPOTHESES/cards/H_004_f1-static-anchor-pilot.md` ·
  `lab/v3/state/h004_static-anchor-pilot_2026-07-16/{run_guards.py,guards_result.json}` ·
  `lab/v4/HYPOTHESES/cards/H_003_atomicity_fixed_codec_drill.md`
- 감사 대상: `HYPOTHESES/cards/H_9288_morpheme_atomicity_lever.md` (**불변**)
- convergence: `corpus-py-1` ⑧(공선성) · ⑨(노출 0 축) · (F)(축 이름 붙이고 노출 0 에서만) ·
  (H)/(J)(결정적이면 재생성 · seed 를 알아야 결정적)
- memory: [[measurement-metalaw-form-tunable-bind-earned]] · [[single-retrain-outlier-faked-a-refutation]] ·
  [[control-must-match-mediating-covariate]] · [[chance-level-must-be-derived-per-metric]] ·
  [[positive-control-before-reading-a-negative]]
