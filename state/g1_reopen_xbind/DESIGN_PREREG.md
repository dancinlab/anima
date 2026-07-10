# XBIND — G1 reopen lane (a) 발사 스펙 (frozen pre-registration)

- **date:** 2026-07-10 · **role:** Fable 설계(실행=메인 세션, fable-design-analysis-only)
- **owner go:** rent=spend GO (A100 확보) · pre-registered 단일 실행 · axis 순차사냥 금지
- **전제(earned terminal, #3293/#3294):** G1 held-out constructive recombination은
  **corpus-class × next-byte CE measure**에서 ≤303M 학습불가·arch-무관. 벽 진범 = corpus×CE
  결합 measure. 유일 exit = 학습 measure(corpus/task class) 교체.
- **이 스펙의 질문(단 하나, frozen):** held-out 재조합 신호를 *구성한* corpus×task class 위에서
  303M CLMConvMoE + next-byte CE가 held-out constructive recombination을 학습하는가?
- **suggested H:** `H_9266 g1_reopen_xbind` (등록은 발사 세션이 2-surface로)

---

## 0. Ledger 정합 — 왜 재발사가 아닌가 (check-ledger-before-lever-fire)

| 선행 | 무엇이었나 | XBIND가 다른 좌표 |
|---|---|---|
| F2 heldout_recomb (RESULT.json) | 모든 기존 corpus = COLLOCATION-ONLY, true_heldout_novel **n=0** | XBIND는 그 n=0을 **구성으로 해소**: held-out novel pair n=15,960, 각각의 gold가 joint rule로만 결정 |
| H_9124 derivtrace 🔴 NOT-ROBUST | 과제가 **additive-solvable**(양 prompt서 키워드 복사=main-effect), 5개념·held-out 1쌍(threshold artifact), keyword-coverage bar, 희석서 붕괴 | 판별어가 **XOR(비가법) by construction** + main-effect 천장=chance를 **감사로 고정**(V-C 실측 0.444) · 400개념·15,960 held-out쌍(power) · exact-continuation 채점 · f=1.0 순수 스코프 사전등록 |
| H_9206 ATD 🧱 KILL | toy transformer·**geometry-primary** KILL("전이 bilinear geometry 미유도")·"authored-only 303M fire NO-GO". 단 **behav held-out 0.152 vs chance 0.061 (2.5×·swap-통제 통과) = 약한 실신호** | 오너 reopen이 NO-GO를 명시 해제(rent=spend go). XBIND는 **behavioral-primary·engine-native 303M TERMINAL-eligible**, ATD의 학습성 confound(불균형 marginal·소규모 조합공간·window 미준수) 전부 제거. 결과가 어느 쪽이든 ATD와 정합: CRACK→ATD-kill은 toy/geometry-scope로 한정, 🧱→ATD NO-GO가 303M terminal로 격상 |
| H_9265 PC-P2 XOR | **자연 corpus read-instrument**(기존 모델이 자연 텍스트의 비가법을 소비하는가) — 신호부재 $0-closed | XBIND는 **train-side 합성 corpus**: 신호를 읽는 게 아니라 **만든다**. 미발사 좌표 |
| H_9121 coverage / H_6187-6189 window | 단순 커버리지↑·window 조정 소진 | 커버리지·window는 여기서 **레버가 아니라 validity 전제**(V-G·80% 조합 커버). 신규 축 = task 구조(joint-only 판별) |
| γ census (H_9255 등) | NLL surface가 content-pair에 완전 additive = 진짜 비가법 = XOR-class뿐 | XBIND 판별어가 정확히 그 XOR-class를 CE target으로 배치 |

**신규 좌표 4개(전부 기존 발사에 없음):** ① 비가법(XOR) 판별어 ② 주변분포 정확 균형(main-effect
천장=chance 고정·감사) ③ 대규모 조합공간(rule≪암기 MDL: 400 pol-bit+rule 1개 vs 63,840쌍 암기)
④ T=24 decode-window 물리 준수(판별 시점에 두 이름 모두 in-window).

---

## 1. Task class — XBIND (Q2 답)

**구조:** 개념 c마다 은닉 polarity bit pol(c). pair line의 continuation 분기 = xor(pol(a),pol(b)):

```
xor=0 : "<a> <b>: fuse, <ab>."        (portmanteau <ab> = prompt 순서 따르는 order-covariant 구성)
xor=1 : "<a> <b>: part, <a> <b>."
```

held-out 쌍의 gold를 맞히는 경로는 오직: (i) train 쌍들에서 개념별 pol 추론(분포 증거) →
(ii) xor rule 적용. 암기(쌍 미노출)·main-effect(marginal=0.5 균형)·표면 상관(이름-pol 무상관,
V-D 감사) 전부 차단.

**next-byte CE로 충분한가(명시적 "compose" 시그널 필요?):** 충분. 필요한 최소 구조는 지시문이
아니라 다음 4조건 — ① 개념 latent가 train 쌍들에서 학습가능 ② target이 latent들의 **비가법
joint 함수** ③ marginal 균형으로 main-effect 예측이 정확히 chance ④ 조합 커버리지가 커서
rule이 암기보다 MDL-싸다. `"<a> <b>: "` 템플릿의 콜론 위치가 곧 supervision 위치다 —
CE는 그 자리의 next-byte를 최적화하려면 joint를 계산하는 수밖에 없도록 corpus가 강제한다.
(별도 자연어 지시·"A and B →" 메타 템플릿 불요 — derivtrace의 교훈: 표면 스캐폴드는 additive
지름길만 늘린다.)

**2-tier 채점(측정 메타법칙 FORM tunable·BIND earned):**
- **Tier-BIND (판별어):** "fuse"/"part" — joint-only 1-bit. 진짜 earned-bind 신호.
- **Tier-FORM (구성):** gold-fuse held-out서 portmanteau `<ab>.` — held-out 쌍이면 train에 없는
  **novel byte string**을 rule(순서 붙임)로 생성 = constructive 표면. copy-head만으로는 순서·경계·
  분기(part면 안 만듦)를 못 맞춘다.

## 2. Corpus 생성 레시피 (Q1 답 · `gen_xbind.py` 결정적 구현·실행완료)

- **이름:** CVC 의사단어 3B (17C×5V×17C=1445 pool, "now" 제외), rng(seed=7) 표집.
  N=400 pair-eligible + filler 1 ("was").
- **pol:** 정확 200/200 균형 배정(표면과 무상관 — V-D 감사 0.513).
- **split:** C(400,2)=79,800 unordered 쌍 → rng shuffle → **20% = 15,960 held-out**(양 순서 모두
  corpus 완전 부재 = true_heldout_novel 정의 1:1) · 80% = 63,840 train(양 순서 × 2 rep).
- **singles:** 개념당 100줄, pol-무관 3변형(`waits here./stands still./rests now.`) — 이름 앵커 +
  eval seed prefix in-distribution용.
- **크기:** main arm **6.66MB** (pair 255,360줄 + singles 40,100줄, 셔플). 22-23B/줄.
- **control arm (`xbind_shuffle_train.txt`, 6.66MB):** 동일 stream·동일 permutation(content-matched),
  분기만 unordered-pair당 독립 coin(순서·rep 일관 = 암기가능·rule 없음) = collocation regime 증류판.
- **10줄 예시:** `EXAMPLES.txt` (e.g. `fuj ved: fuse, fujved.` · `dib dup: part, dib dup.` ·
  `tor waits here.`)
- **사전-발사 $0 validity 게이트(실행완료·ALL PASS, `AUDIT.json`):**
  - V-C main-effect 천장: additive score (b_a+b_b)/2 held-out acc **0.444** ≤ 0.55 ✓
  - V-D pol⊥표면: char-feature perceptron probe **0.513** ≤ 0.60 ✓
  - V-E marginal 균형: max skew **0.048** ≤ 0.10 ✓
  - V-F 누출 0줄 ✓ · V-G window 물리(seed 25B·양 이름 last-24B 내) ✓
- **랜딩 시:** `anima corpus xbind|xbind-shuffle` 서브커맨드로 fold-in(a_cli_single_entry —
  gen_xbind.py는 설계-단계 reference, 발사용 corpus는 fold-in 후 canonical 진입으로 재생성 권장.
  동일 seed=바이트 동일).

## 3. 학습 스펙 (Q3 답 · frozen)

3 run (A100 1장, 순차 or 병렬):

```
anima-py train --arch clm --canon --arm ctrl --objective ce_marginal \
  --corpus xbind_train.txt --cell-label en-general \
  --steps 20000 --batch-size 8 --bf16 --seed {7 | 4302} \
  --val-frac 0.02 --val-every 500 --out ckpt/xbind_s{seed}.clm      # run 1·2 (main arm ×2 seed)

anima-py train ... --corpus xbind_shuffle_train.txt --seed 7 \
  --out ckpt/xbind_shuf_s7.clm                                      # run 3 (control arm)
```

- canon 기본: d=3784 L=4 seq_len=1024 (303M) · savant/mitosis 캐논 레시피 그대로(생산 substrate
  자체를 측정). 20,000 step × 8 × 1024 ≈ 164MB ≈ 25 epoch — pol-추론+rule 추출(grokking-class)
  여유. val-frac은 train-corpus 내부 슬라이스만(held-out 쌍은 corpus 부재라 누출 불가).
- **비용 1-line:** A100 ~2h/run × 3 ≈ 6h ≈ **$12-15** (+eval pool $0). (a_fire_autonomous)
- teardown 전 ckpt PULL→HF (a_fire_recover_complete · PRIVATE until verdict).
- 왜 from-scratch(warm-FT 아님): 질문이 "corpus×CE measure에서 학습가능한가"이므로 자연-사전학습
  잔재는 confound. 순수 f=1.0 스코프는 §6에서 정직 한정. (derivtrace 사망 지점이던 희석은
  **별도 follow-on**으로 명시 분리 — 이 발사의 질문 아님.)

## 4. 측정 bar (Q4 답 · frozen 사전등록 · 1바이트도 사후이동 금지)

**경로:** `anima-py evaluate <clm> --xbind xbind_eval_manifest.json --out …` (fold-in
`eval_xbind_mode.py` · engine-native numpy core/decode.py · a_eval_py_canonical =
TERMINAL-eligible). manifest = held-out 200 + seen 200 (frozen, 생성기 산출).
전 arm 전량 캡처(control tail-truncate 금지 · convergence evaluate-py-1).

- **PRIMARY D-acc:** greedy(top_k=1) decode gen=16, 첫 방출 단어 == gold 분기어. 결정적(sampler-
  artifact-free).
- **CONSTRUCT C-rate:** gold-fuse held-out서 `<ab>.` 정확 문자열 방출(= novel·echo-불가능:
  held-out 쌍 line은 train 부재 — echo-guard by construction + 기계적 substring 검사).
- **MARGIN(2차):** teacher-forced NLL(counterfactual)−NLL(gold), win=64 forward(decode-window
  독립 확인용).
- **SAMPLED(2차):** canonical top_k=40 temp=0.7 rng{7,4302,4303} majority, 40개 서브샘플
  (seed-robust 확인, 교훈 #4).

**VALIDITY (하나라도 실패 → INVALID, verdict 아님 · V-gate 1급 판정):**
- V-A: 각 학습 arm의 **seen D-acc ≥ 0.90** (미달 = undertrain/collapse → INVALID)
- V-B: control 모델 held-out D-acc ∈ [0.38, 0.62] (이탈 = instrument 누출 → INVALID)
- V-C~V-G: 사전-발사 게이트(§2, 이미 PASS — corpus 재생성 시 재확인)

**VERDICT (양 seed 일치 시만 cement):**
- **CRACK 🟢** = held-out D-acc ≥ 0.75 (양 main seed, greedy) ∧ (held-out D-acc − control
  held-out D-acc) ≥ +0.20 ∧ C-rate ≥ 0.50 ∧ echo-guard clean.
  = "corpus×task class 교체로 G1 재조합 CE-학습가능" — 벽 진범=measure 증명.
- **FORM-ONLY 🟡** = C-rate ≥ 0.50 ∧ held-out D-acc < 0.60 — 생산적 연결(FORM)은 학습되나
  earned-bind(joint bit)는 불가 → 벽 문구가 "joint-bit 학습불가"로 정밀화.
- **🧱** = held-out D-acc < 0.60 (양 seed) with validity 전부 green — **terminal 최강 보강**:
  joint rule이 held-out continuation의 유일 예측자인 corpus에서도 CE·303M이 학습 실패.
- 회색지대(0.60≤D-acc<0.75 또는 seed-split) = 🟡 UNSTABLE-DIRECTIONAL. **유일 허용 연장
  (사전등록):** 동일 run +20,000 step 이어서 1회 재측정(grokking-delay 체크) 후 최종. 그 외
  일체의 재설계·재발사 = tune-to-green, 금지.
- n=200: p=0.5 대비 sd≈3.5% → 0.75 bar ≈ 7σ. control band ±3.4σ.

**heldout_recomb true_heldout_novel 1:1 대응:** qualified = held-out 쌍(구성상 n=15,960>0 —
F2의 n=0을 corpus가 해소), differ = gold가 joint에 의해 분기(구성상 100%), 판정 = 모델이
그 분기를 held-out서 재현하는가. 기본 G-battery(`anima-py evaluate` 풀패널)도 기록용으로 1회
실행하되 cz-개념 OOV라 UNINFORMATIVE-예상 — verdict 표면 아님(스코프 각주만).
**CRACK 시 wiring 경로(a_verified_must_wire):** xbind manifest가 ρ·weave PENDING(held-out
atom-pair recombination set) probe로 편입 — control 2개(shuffle-arm 모델·pol-permuted 채점)
갖춘 collapse-Δ 형식 충족.

## 5. Honest scope (Q5 답)

- **CRACK이 증명하는 것:** "G1 벽의 진범은 substrate가 아니라 corpus×CE measure" — 303M
  CLMConvMoE는 신호가 존재하면 held-out constructive recombination을 CE만으로 학습한다.
  earned-terminal의 exit 문구가 실증되고, ATD toy-kill은 toy/geometry-scope로 한정된다.
- **CRACK이 증명 안 하는 것:** ① 자연 corpus 창발(합성 task 학습이다 — frontier의 다음 질문
  = 자연혼합 희석 사다리 f∈{1.0,0.3,0.1}, derivtrace·ATD가 죽은 바로 그 지점. **이 발사 스코프
  밖, 별도 사전등록 필요**) ② 개방형 의미 합성(1-bit joint + 연결 구성 = 최소 재조합 class)
  ③ 기본 G-battery ρ·weave PASS(frozen cz-bar는 자연어 세계 — 별개 표면).
- **🧱이 증명하는 것:** "corpus를 아무리 구성해도 303M byte-LM CE는 compositional generalization
  불가" — exit 후보 소거로 terminal이 **corpus-축까지 earned**로 격상. 이후 잔여는 scale(>303M,
  amplifier-not-lever 메모 전제하에 lever 부재까지 확인된 상태)·非-CE measure(H_9121서 소진)뿐
  = 진짜 종결.
- 측정경로: py 2-production engine-native = TERMINAL-eligible (a_eval_py_canonical 오너 override).
  torch-side train 지표는 전부 DIRECTIONAL/monitor-only (p7).

## 6. Runbook (발사 세션용)

1. fold-in: `anima corpus xbind|xbind-shuffle` (gen_xbind.py) + `--xbind` eval 모드
   (eval_xbind_mode.py) → pr-cycle. corpus 재생성(seed 7) 후 AUDIT ALL_PASS 재확인.
2. H_9266 2-surface 등록(jsonl+card·이 문서 링크) — bar는 이 문서 §4 verbatim FREEZE.
3. A100 렌트 → 3 run(§3) → ckpt PULL + HF(PRIVATE) → pod teardown.
4. pool서 `anima-py evaluate --xbind` × {main s7, main s4302, ctrl s7} × manifest → verdicts/
   frozen 캡처(전량, tail 금지) → 카드 cement.
5. 기본 G-battery 1회 기록용 → ARCHITECTURE gate 노드 갱신 + CHANGELOG + pr-cycle.

## Artifacts (이 디렉토리)
- `gen_xbind.py` — 결정적 생성기(+$0 validity 게이트·실행완료 ALL_PASS)
- `xbind_train.txt` 6.66MB · `xbind_shuffle_train.txt` 6.66MB · `xbind_eval_manifest.json` (200+200)
- `AUDIT.json` (V-C 0.444 · V-D 0.513 · V-E 0.048 · V-F 0 · V-G pass) · `EXAMPLES.txt`
- `eval_xbind_mode.py` — `--xbind` fold-in 코드
