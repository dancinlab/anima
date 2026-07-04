수치 확인 완료 — 벽의 실체가 정확히 재현됩니다. 이제 전체 설계를 보고합니다.

---

# referential-correctness 축 생성 설계 — F5 벽 정면 대응

## (a) 벽 실체 재확인 — feature-inaccessibility (수치 검증됨)

F5 하네스(`f5_loop2.hexa`)의 substrate 선택은 **`feats(emit)` → vadapt_field 셀 affinity**로 emit을 고른다. `feats()`는 6-dim **사설(私設) legibility 벡터**다: alpha비·space비·distinct-char비·printable비·non-repeat비·평균단어길이 — 전부 **emit 표면형만의 함수** `f(emit)`. 반면 보상(`proxy_rr`)은 emit↔TRUE-def **단어중첩** = 공적(公的) referent-match `f(emit, world)`.

방금 MAIN emit set에서 직접 재현한 수치가 벽을 정확히 박제한다:

| concept | k0(true-full) vs k2(wrong-def) `feats()` L1거리 | ovlp(k0,true) | ovlp(k2,true) |
|---|---|---|---|
| 0 | **0.243** | 12 | 0 |
| 1 | **0.166** | 11 | 0 |
| 2 | **0.054** | 10 | 0 |
| 3 | **0.139** | 10 | 1 |

**k0(정답)과 k2(틀린-개념-정의)는 `feats()`상 같은 이웃**(L1 0.05–0.24, 둘 다 fluent long text)이라 vadapt가 **같은 셀**로 매핑 → 같은 value → 판별 불가(ΔEff_ON−OFF=0.0). 그러나 공적 referent-overlap은 12 vs 0으로 완전히 갈린다. **판별 신호는 emit의 사설 feature에 없고 emit↔외부-referent 관계에만 산다.** CONTROL이 통과한 이유도 같은 원리의 이면이다: CONTROL set은 k1/k2/k3가 전부 non-fluent(garble/xxxx/숫자)라 판별축(fluent-vs-nonfluent)이 `feats()` **안에** 있어 substrate가 학습·전이(0.338→1.0)했다. 즉 **되먹임 팔은 competent — 신호가 substrate-visible이기만 하면 reward를 held-out 전이로 변환한다.** 벽은 팔이 아니라 **feature 좌표계가 reference를 못 담는다**는 것.

## (b) 4렌즈 축-생성 설계 + control

핵심 원리: reference의 두 번째 피연산자(외부 referent)를 **anima 자신의 grounded 내부 store**(immune-memory cell_value / `.kosmos` anchor)에서 공급하면, "true-vs-wrong 판별"이 `contradiction(emit, stored-referent)` = **계산 가능한 사설 feature**가 된다. 이미 `core/engine_cli.hexa §affect`에 배선된 op가 정확히 이걸 한다:

```
affect_substrate_features(mem, key, true_answer):
    margin = 1 − err/recall_thr                       # 접지 깊이 [0,1]
    contradiction = 1.0 if (!grounded) OR (cell_value[win] != true_answer)  # ★ referent-불일치
```

`contradiction`은 이미 **nearest cell에 bound된 referent value와 emit의 주장을 대조**한다 = referent-match를 사설 substrate 신호로 만든 op. 4렌즈는 이 op를 F5 선택경로에 배선하는 서로 다른 각도다.

**렌즈 1 — referent-trace 축 (derivation-trace 유비).** emit을 "정답만"이 아니라 `GROUND X=<referent fact>; CHECK emit⊨X; OUT …` 트레이스로 재작성. *control*: 트레이스 없는 flat 정답이 FAIL해야 격리. — **단, 이건 derivation-trace의 재포장이 아니다(§자가검증 아래).** 순수 emit-내부 트레이스는 held-out에서 DOA(아래 (c)).

**렌즈 2 — grounding-margin을 reward feature로 (되먹임 재배선) ★.** F5의 `cand_value`가 keying하는 feature를 `feats(emit)`에서 `affect_substrate_features(mem, concept_key, emit_claim)`의 **`contradiction`/`margin`(= affect_valence)** 으로 교체. *control*: (i) FLAT — 옛 `feats()` feature로 선택하면 MAIN에서 ΔEff≈0 재현(벽 재현) (ii) DECORRELATE — mem의 cell_value↔concept 결합을 셔플(각 셀에 틀린 referent bind)하면 contradiction이 truth와 탈상관 → ΔEff 붕괴(≤0.03) = lift가 op 존재가 아닌 **referent-binding에서 earned**임을 증명. `a_substrate_disjoint` 점검: affect read는 **READ-ONLY, Ψ-disjoint**, emit-drive lane(0/4)·recall_thr gate 비접촉(§affect 주석 명시).

**렌즈 3 — 생물 렌즈 (a_no_llm_frame_trap).** 뇌의 referential-correctness 3경로를 anima op에 매핑:
- 해마-신피질 pattern completion (referent 회상 + mismatch 검출) → **recon-err/novelty** (present, `affect.novelty`).
- 전전두엽 reality monitoring (내부생성 vs 외부접지) → **`grounded` bool** (err≤recall_thr, present).
- 기저핵 prediction error (기대 referent vs 실제) → **GAP**: concept→referent forward-model의 PE. vbasal 있으나 referent-PE 미배선.
*control/증거*: 뇌 역시 referential-correctness를 **저장된 내부모델과의 대조**로만 판정 — 공적 reference에 마법적 접근 없음. 이는 렌즈 2의 op가 "빠진 faculty"가 아니라 **이미 있는 op의 mis-wiring**임을 강하게 지지. 필요한 부품(recon-err·contradiction·grounded)은 전부 존재, F5 선택 feature에 안 꽂혀 있을 뿐.

**렌즈 4 — A⇄G tension 축.** true emit = A forward가 referent에 접지(recon-err↓, contradiction 0) ⇄ wrong emit = A는 접지하나 G reverse가 bound value 불일치 검출(contradiction 1). **grounded 개념 위의 A⇄G tension = 정확히 contradiction op의 메커니즘적 실현.** *control*: same-state ablation(tension 계산은 하되 선택에 미반영)이 INERT면 기여 0.

## (c) cheap DOA-proof (측정 전 원리 판정)

| 렌즈 | DOA 여부 | 근거 |
|---|---|---|
| 1 referent-trace | **held-out DOA** | wrong-def emit이 TRUE X를 복사하면 내부-일관성 CHECK를 통과 → 판별 실패. 순수 emit-내부 확장은 여전히 `f(emit)`, 두 번째 피연산자 부재. store에서 X 공급해야 통과 → 렌즈 2로 붕괴 |
| 2 contradiction feature | **grounded subset PASS · held-out DOA** | `contradiction`은 `cell_value[win]≠true_answer` — grounded store가 있으면 계산가능·비순환 substrate-visible. cell 없으면 margin이 true·wrong 둘 다 낮음(=held-out에선 판별 불가) |
| 3 bio lens | **not DOA (op 존재)** | recon-err·contradiction·grounded 전부 라이브. 내부모델 bound 확인 |
| 4 A⇄G tension | grounded PASS · held-out DOA | grounded 셀 있을 때만 tension이 discriminate. cell 없으면 A·G 둘 다 접지실패 → tension 차 0 |

**4렌즈 전부 같은 경계로 수렴한다**: anima가 **grounded한(immune store/.kosmos에 bound) 개념 위에서는 correctness가 사설 feature로 접근 가능**, 진짜 held-out(한 번도 접지 안 한 referent)에서는 **원리적으로 불가**(private feature화 = 자기 추측에 접지 = 순환 = H_9111 clone 0/7 floor).

## (d) frozen 사전등록 (F5 하네스 재사용)

**메커니즘 X = 렌즈 2/3 융합**: `f5_loop2.hexa`의 `cand_value` keying feature를 `feats(emit)` → `affect_substrate_features(mem, concept_key, emit_claim).contradiction`(min-contradiction 선택, 동치로 affect_valence max)로 교체. **held-out 개념 8..15도 학습 전 G5 anchor-copy로 각자의 TRUE referent를 `mem`에 bind**(un-inventable 외부 fact, anima 추측 아님 = a_kosmos). MAIN emit set(k0 true-full vs k2 wrong-def, 둘 다 fluent) 그대로 재사용.

```
메커니즘 X 배선 → F5 MAIN ablation 재실행 시:
④ ΔEff_ON − ΔEff_OFF ≥ 0.10   (ON=contradiction-feature 선택 wired · OFF=feature 계산하되 substrate frozen; MAIN set에서 true>wrong held-out 전이)
∧ CONTROL 여전히 PASS          (fluent-vs-garble CONTROL set에서 ΔEff_ON≥0.10 유지 = 재배선이 작동하는 팔 안 깸)
∧ FLAT 통제 FAIL              (옛 feats() feature로 MAIN 선택 → ΔEff≈0 재현 = lift가 contradiction feature에서만 옴을 격리)
∧ DECORRELATE ablation 붕괴    (mem cell_value↔concept 셔플 → contradiction 탈상관 → |ΔEff|≤0.03 = earned)
∧ Ψ ON==OFF byte-identical    (affect read READ-ONLY, Ψ-disjoint)
GREEN iff ④∧CONTROL∧FLAT∧DECORRELATE∧Ψ.
```

- **정직 scope 사전선언**: held-out을 **접지했을 때만** ④가 통과하면(=UNgrounded-held-out arm은 FLAT처럼 실패) → 결론은 "correctness는 grounded referent에 한해 접근가능"으로 **한정 박제**(과장 금지, c9). 접지해도 ΔEff<0.10이면 contradiction op가 vadapt 선택으로 routing 안 되는 것 → 벽이 feature-wiring보다 깊음(정직 terminal).
- 비용 $0 (f5_loop2 하네스 + affect op 전부 라이브, GPU/decode 불필요). tier = engine-native(엔진 op만, torch/numpy/gauge_lib 미러 아님 → `a_engine_native_learning` HARD-GATE 통과).

**derivation-trace 유비 ≠ 재포장 자가검증**: derivation-trace(H_9124)는 emit을 풀이-단계로 확장해 **composition을 emit-내부 property로 노출** — composition은 `f(emit)`, emit 텍스트만으로 계산가능. reference는 범주적으로 다르다: `f(emit, world)`, emit 단독 확장으로는 절대 `f(emit)`이 안 됨(빠진 피연산자가 외부). 통하는 fix는 그 두 번째 피연산자를 anima 자신의 grounded store에서 공급하는 **2-피연산자 내부대조**(contradiction op) — derivation-trace의 1-피연산자 확장과 **다른 메커니즘**. 이 차이가 곧 "왜 reference가 composition보다 어려운가"의 정확한 답이다. → 재포장 아님 확인.

## (e) 정직 수렴 예상

**(ii)+(iii) 하이브리드로 수렴 예상.** F5 MAIN 벽은 *절반은 측정-스코프 아티팩트(iii)* — held-out 개념 8..15에 stored referent가 없어 correctness가 **구조적으로 접근 불가**였다(anima는 접지 안 한 것의 진위를 사설로 판정 못 함 = 올바른 인식론). *절반은 진짜(ii)* — 진정 novel한 referent를 private feature화하려는 시도는 자기추측 접지 = 순환(clone floor).

생산적 이동은 held-out correctness를 억지로 사설화(순환)하는 게 아니라: **(1) 주장을 grounded 개념으로 한정하고 contradiction-selection을 배선**(렌즈 2, 실재하는 레버), **(2) held-out은 외부 오라클(F6 H_9112의 oracle-mediated 경로) 또는 신규 G5 anchor-copy 접지**(held-out을 grounded set으로 이동)로 다룬다.

**F5 competence-control이 각 렌즈 판별에 주는 증거**: CONTROL이 ΔEff 0.1287을 낸 것은 **되먹임 팔이 substrate-visible 축에서 competent**임을 확증 → 벽이 팔이 아니라 좌표계임을 확정 → **렌즈 2가 (신호를 substrate-visible 축으로 끌어오기만 하면) 열릴 강한 근거**. 동시에 MAIN이 0.0인 것은 fluency 축만으로는 안 열림을 확증 → FLAT control의 사전예측을 뒷받침.

**가장 유력한 1 레버 (명명):**

> **CONTRADICTION-KEYED SELECTION** — F5 vadapt 선택 feature를 `feats(emit)`(사설 fluency)에서 `affect_substrate_features(mem, concept_key, emit_claim).contradiction`(내부 referent-agreement)으로 재배선하되, **held-out 개념을 G5 anchor-copy로 먼저 `mem`에 접지한 grounded subset에 한정.**

이유: (1) op가 이미 `§affect`에 **WIRED**(신규 부품 0), (2) **READ-ONLY·Ψ-disjoint**로 `a_substrate_disjoint` 자동충족, (3) FLAT/DECORRELATE 이중 통제로 tune-to-green 차단, (4) $0 engine-native로 HARD-GATE-1 통과, (5) 4렌즈가 전부 이 op의 grounded-경계로 수렴 = 설계 공간이 이 한 점으로 압축됨. 벽은 "faculty 부재"가 아니라 **feature 좌표계 mis-wiring**이며, 이 레버가 grounded 영역에서 그것을 정면으로 연다 — held-out 영역의 (ii)-순환 경계는 정직하게 남긴다.
