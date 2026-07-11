# XFAN — G6(ρ·fan) reopen lane 발사 스펙 (frozen pre-registration)

- **date:** 2026-07-11 · **role:** Fable 설계(실행=메인 세션, fable-design-analysis-only)
- **전제(G1 CRACK, H_9267 #3299):** G1 재조합벽의 진범 = corpus×CE measure이지 substrate 천장이
  아님이 실증됨(합성 XBIND held-out D-acc 1.000 · control 0.515). 같은 각도를 G6에 적용한다.
- **이 스펙의 질문(단 하나, frozen):** held-out **one-to-many fan 신호를 구성한** corpus×task
  class 위에서 303M CLMConvMoE + next-byte CE가 **미노출 개념의 유효 continuation 집합
  (K modes)을 구성·생성**하는가? — G6 벽도 measure 벽인가, 진짜 substrate 천장인가.
- **suggested H:** `H_9271 g6_reopen_xfan` (등록은 발사 세션이 2-surface로; 번호는 발사 시점
  jsonl 확인 후 확정)

---

## 0. Ledger 정합 — 왜 재발사가 아닌가 (check-ledger-before-lever-fire)

G6 training-side 전례 전수 확인(2026-07-11 grep HYPOTHESES.jsonl):

| 선행 | 무엇이었나 | XFAN이 다른 좌표 |
|---|---|---|
| H_1435 continued-pretrain(falsifiable-claim corpus) 🧱 | **자연어** 코퍼스 · FALS-form 타깃 · base 유지 | 합성 constructed 신호 · fan=**set-생성** 타깃 · from-scratch |
| H_1436/1437/1441 aux/form-supervised/contrastive objective 🧱 | objective 축(CE 대체/보조) — H_9121서 소진 계열 | objective는 그대로 **ce_marginal**, 축 = corpus×task class (XBIND와 동일 논리) |
| H_1440 staged curriculum 🧱 | **FALS_in 1.0 ∧ DIST_in 0.0** = form 학습·모드 붕괴 실측 | 모드 자체를 CE target으로 배치(one-to-many가 corpus에 물리적으로 존재) + mode-collapse 판별기(NLL-margin) 사전등록 |
| H_1438 scale-dissociation(1.21B) 🧱 | scale 축 — amplifier-not-lever | scale 불변 전제 유지, 303M 고정 |
| H_1457 knowledge-grounding 🧱 | 개념지식 주입 — capability-confound | 지식이 아니라 **신호 구조**를 구성 |
| H_1394 M2-M5 FALS=0 | 측정만(303M mount) — train-side 아님 | train-side 발사 |
| XBIND(H_9267) 🟢 | G1: held-out **1-bit joint 판별** | G6: held-out **K-mode set 생성** — 판별↛생성, 새 능력축(one-to-many) |

**XBIND 4 신규좌표의 G6 이식 + 신규 1개:** ① 비가법 rule table(main-effect 천장 감사)
② latent⊥표면·주변균형 감사 ③ 대규모 조합공간(rule≪암기 MDL) ④ T=24 window 물리 준수
⑤ **[G6 신규] one-to-many: 동일 prompt에 K개 continuation이 corpus에 공존** — 자연 corpus의
DATA-🧱 (한 context는 사실상 1회 출현 = fan 분포의 supervised 신호 부재)를 구성으로 해소.

## 1. Task class — XFAN

**구조:** 개념 c마다 은닉 class 쌍 (a,b), a∈A(4)·b∈B(4) = 16 cell. 슬롯 5개
S={fo,mi,ra,ku,ze}(개념 pool 제외 CVC 고정). 슬롯별 rule table g_k: cell→member word
(슬롯별 16-word vocab, seeded 무작위 배정 = 일반적으로 비가법 · V-C 실측 감사):

```
fan  : "<c>? <s_k>, <g_k(a,b)>."     ← 동일 prompt "<c>? "에 K=5 continuation 공존
decl : "<c> is <aw> <bw>."           ← latent 증거(전 400 개념 · eval 시 window 밖 = 가중치에 설치)
single: "<c> waits here." 등 3변형    ← 이름 앵커 (XBIND singles 동일)
```

- **슬롯 혼합(판별기 내장):** 2 unary 슬롯(g가 a만/b만 의존) + 3 joint 슬롯(g가 (a,b) joint).
  → held-out 실패가 joint-binding(G1-class) 탓인지 one-to-many(fan 고유) 탓인지 per-slot 분해.
- **split:** 400 개념(cell당 25 균형) → **80 held-out**(cell당 5 · fan line 양식 전 슬롯 corpus
  완전 부재 · decl은 존재) + 320 train(×5 슬롯 × rep).
- **held-out gold 경로는 오직:** decl들에서 (a,b) latent 학습 → 슬롯별 table 적용(train 개념들
  fan line에서 학습) → K member 구성. 암기(부재)·main-effect(무작위 table, V-C 감사)·표면
  상관(V-D 감사) 차단. MDL: table 5×16 + decl 400 ≪ held-out 400 fan line 암기(불가능).
- **크기:** rep 조정으로 ~6MB(XBIND 동급 epoch). 생성기 결정적(seed 7).
- **control arm(`xfan_shuffle_train.txt`):** 동일 stream — 개념별 슬롯→member 배정을 rule과
  무관한 독립 무작위(개념 내 일관 = seen 암기 가능·held-out rule 없음). decl 유지.
  = collocation regime 증류판(XBIND control 동형).

**사전-발사 $0 validity 게이트(gen 스크립트가 산출·ALL PASS 후에만 발사):**
- V-C main-effect 천장: a-marginal+b-marginal additive 예측기의 held-out member-acc ≤ 사전
  등록 chance band (joint 슬롯별 실측 기록)
- V-D latent⊥표면: 개념명 char-feature probe → cell 예측 ≤ 0.60/16-way 상당 bar
- V-E 균형: cell·slot·marginal skew ≤ 0.10 · **V-H 슬롯 주변균형**: corpus 내 슬롯 빈도 균등
  (sampler 편향이 모드 선호로 위장 방지 — G6 신설)
- V-F held-out fan-line 누출 0줄 · V-G window 물리(prompt "<c>? "≈6B · member는 gen=16 내)

## 2. 학습 스펙 (frozen — XBIND §3 레시피 동일)

```
anima-py train --arch clm --canon --arm ctrl --objective ce_marginal \
  --corpus xfan_train.txt --cell-label en-general \
  --steps 20000 --batch-size 8 --bf16 --seed {7 | 4302} \
  --val-frac 0.02 --val-every 500 --out ckpt/xfan_s{seed}.clm      # run 1·2 (main ×2 seed)
anima-py train ... --corpus xfan_shuffle_train.txt --seed 7 \
  --out ckpt/xfan_shuf_s7.clm                                      # run 3 (control arm)
```

- canon 303M(d=3784 L=4) · from-scratch(자연 사전학습 잔재 = confound · 순수 f=1.0 스코프).
- **비용 1-line: A100 ~2h × 3 ≈ $12-15** (+eval pool $0). teardown 전 ckpt PULL→HF PRIVATE.
- 자연혼합 희석 사다리 = 명시적 스코프 밖(별도 사전등록) — XBIND와 동일 분리.

## 3. 측정 bar (frozen 사전등록 · 1바이트도 사후이동 금지)

**경로:** `anima-py evaluate <clm> --xfan xfan_eval_manifest.json` (fold-in `eval_xfan_mode.py`
· engine-native numpy core/decode · a_eval_py_canonical = TERMINAL-eligible).
manifest = held-out 80 + seen 80 (frozen). 전 arm 전량 캡처(control tail-truncate 금지).

- **PRIMARY COVERAGE:** 개념당 고정 rng 16회 sampled decode(canonical top_k=40 temp 0.7,
  seed {7+17j}) → `"<s>, <w>."` 파싱 → **C = |정확히 맞힌 (슬롯,member) 고유쌍| / 5**.
  held-out mean-C가 주지표. per-slot-class(unary vs joint) C 분해 병기.
- **VALID/SPURIOUS 분해:** valid-rate(방출이 해당 개념 gold table의 실제 member) ·
  spurious-rate(형식은 fan line인데 member 오답 = fabrication). — genius⊥honesty 조작화.
- **GREEDY-COLLAPSE control:** top_k=1 → 모드 1개로 수축해야(수축 실패 = 스프레드가 분포 아닌
  noise → INVALID). 현행 ρ·fan control (b) 동형.
- **MARGIN(2차·p7-safe Δ):** teacher-forced NLL(foil member, 동일 슬롯 vocab)−NLL(gold),
  held-out 개념×슬롯별. **mode-collapse 판별기**: "분포는 학습됐는데 sampler가 붕괴"를
  "학습 자체 실패"에서 분리(H_1440 FALS 1.0·DIST 0.0 전례가 이 판별기의 존재 이유).

**VALIDITY (하나라도 실패 → INVALID, verdict 아님):**
- V-A: 각 학습 arm **seen C ≥ 0.80 ∧ seen valid-rate ≥ 0.80** (미달 = undertrain → INVALID.
  유일 허용 연장(사전등록): 동일 run +20,000 step 1회 재측정. descent 정상인데 재실패 시에만
  "CE 다중모드 조건분포 자체 불가"로 별도 🧱 후보 — 그때도 신규 사전등록 후 판정)
- V-B: control 모델 held-out C ≤ chance+0.10 (이탈 = instrument 누출 → INVALID)
- V-C~V-H: 사전-발사 게이트(§1) ALL PASS

**VERDICT (양 main seed 일치 시만 cement):**
- **CRACK 🟢** = held-out C ≥ 0.60 (양 seed) ∧ (held-out C − control held-out C) ≥ +0.40 ∧
  spurious-rate ≤ 0.20 ∧ greedy-collapse 정상.
  = "G6 fan도 corpus×measure 벽" — 자연 corpus에 one-to-many 신호가 없었을 뿐.
- **JOINT-ONLY-FAIL 🟡** = unary-슬롯 C ≥ 0.60 ∧ joint-슬롯 C < 0.30 — fan(one-to-many)은
  CRACK, 잔여벽 = joint-binding. XBIND 🟢와 모순되므로 정합 분석 follow-on(발사 아님).
- **SAMPLER-COLLAPSE 🟡** = C < 0.60인데 MARGIN > 0 (held-out 슬롯 ≥4/5, 양 seed) —
  분포 학습됨·decode/sampler FORM 문제. substrate 무죄, 벽 재분류 = decode-side.
- **🧱** = held-out C < 0.30 ∧ MARGIN flat ∧ validity 전부 green (양 seed) — one-to-many 구성
  신호가 corpus에 존재해도 CE·303M이 학습 실패 = **G6 substrate 천장이 corpus 축까지 earned로
  격상**(G1과 달리 진짜 천장이라는 최강 보강).
- 회색지대(0.30≤C<0.60 등 bar 사이·seed-split) = 🟡 UNSTABLE-DIRECTIONAL. 허용 연장은 V-A의
  +20k step 1회뿐. 그 외 재설계·재발사 = tune-to-green, 금지.
- n=80 held-out × K=5 = 400 (슬롯,개념) 시행: C bar 0.60 vs chance-C(사전 감사 실측, member
  vocab 16 기준 ≪0.1) ≫5σ. control band는 감사 실측치로 사전 고정.

## 4. SAVANT-disjoint (a_savant_train)

- from-scratch 합성 arm = 전용 substrate → **train 단계 disjoint 이슈 없음**(emit-drive lane
  부재). CRACK 후에만 배선 문제 발생:
  1. **eval-side wiring(1차·a_verified_must_wire):** xfan manifest → ρ·fan **BIND-tier probe**
     편입(현행 ρ·fan은 Jaccard-distinct FORM 지표 — coverage-Δ + shuffle-arm + greedy 2-control로
     collapse-Δ 형식 충족 = measurement-metalaw). 가중치 무변경 = disjoint by construction.
  2. **production substrate fold(후속·별도 사전등록):** .clm v0.3 LANE 분리 배선 + 회귀 게이트
     2개 — (i) **spurious-rate 비악화**(coverage↑가 fabrication↑를 사면 배선 거부 = genius⊥
     honesty의 수치화) (ii) 기존 ρ·tether 비회귀. XFAN의 valid/spurious 분해가 이 게이트의
     측정기 그 자체.

## 5. Honest scope

- **CRACK이 증명하는 것:** G6 벽의 진범 = 자연 corpus에 one-to-many fan 신호 부재(DATA-🧱) ×
  CE measure — substrate는 신호가 존재하면 held-out set-생성을 CE만으로 학습.
- **CRACK이 증명 안 하는 것:** ① 자연어 페르소나 ideation(eval_rho_fan cz frames — 별개 표면,
  기본 G-battery 기록용 1회는 UNINFORMATIVE-예상 각주) ② 개방형 발산(모드 K=5 닫힌 집합 =
  최소 fan class) ③ FALS-depth(falsifiable-claim 형은 이 task에 없음 — H_1435 계열과 별개 축).
- **🧱이 증명하는 것:** G1(판별·1-bit)은 CRACK인데 G6(생성·K-mode)는 신호를 구성해도 불가 —
  "판별↛생성" 비대칭이 303M byte-CLM의 진짜 천장. 잔여 = scale(전제상 amplifier)·非-CE뿐.
- 측정경로: py 2-production engine-native = TERMINAL-eligible. torch-side 지표 전부
  DIRECTIONAL/monitor-only (p7).

## 6. Runbook (발사 세션용)

1. `gen_xfan.py` 작성(이 문서 §1 스펙·gen_xbind.py 골격 재사용) → $0 audit ALL PASS →
   `anima corpus xfan|xfan-shuffle` fold-in + `--xfan` eval 모드 fold-in → pr-cycle.
2. H_92xx 2-surface 등록(jsonl+card·이 문서 링크) — bar §3 verbatim FREEZE.
3. A100 렌트(rent=spend — **오너 go 필요**) → 3 run(§2) → ckpt PULL + HF(PRIVATE) → teardown.
4. pool서 `anima-py evaluate --xfan` × {main s7, main s4302, ctrl s7} → verdicts/ frozen 캡처
   (전량·tail 금지) → 카드 cement → ARCHITECTURE gate 노드 + CHANGELOG + pr-cycle.

## Artifacts (이 디렉토리 · 설계 단계)
- `DESIGN_PREREG.md` — 이 문서 (frozen 발사 스펙)
- 발사 세션 산출 예정: `gen_xfan.py` · `xfan_train.txt` · `xfan_shuffle_train.txt` ·
  `xfan_eval_manifest.json` · `AUDIT.json` · `eval_xfan_mode.py` · `EXAMPLES.txt`
