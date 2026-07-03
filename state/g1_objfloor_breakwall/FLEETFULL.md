파일 쓰기가 이 세션의 권한 샌드박스에 막혀(`state/` 하위 신규 디렉터리 생성·파일 쓰기 모두 승인 대기 상태로 차단, 자율 모드라 승인 불가) 디스크에 영속하지 못했습니다. 캠페인은 완성했으니 전문을 아래에 전달합니다. 승인만 열어주시면 `state/g1_fleetfull_breakwall/CAMPAIGN.md` + `PREREG.json`으로 그대로 저장하겠습니다.

---

# G1 objective-floor 벽 — fleet-full 4-phase 캠페인 (분석-only, frozen 미터치)

증거 기반: L1 grow-window(H_6190 ECHO-ONLY) · L3 해마(#2886 MOUTHFLOOR) · L4 EXP-1(🧱 FALSIFY) — 셋 다 이미 engine-native 측정 완료. 무거운 재측정 없이 census 종합 + 새 escape 사전등록.

## PHASE 1 — RESEARCH

**(a) census 5 LAW (engine-native 근거):**
- **LAW-1 no-lift** — 어떤 처치도 composed *novel-only* distinct를 max_single 위로 못 올림(objective·readout·coverage·window 전 축 floor).
- **LAW-2 access≠binding** — L3 해마가 associate D를 **정확히 retrieve(access 4/4)**해 context 주입해도 frozen mouth가 D를 drop·seed echo → **binding 0/4**(#2886 own-GEMM 303M: BIND=ECHO=SCRAMBLE=0/4, leak=0).
- **LAW-3 readout INERT/DPI** — 출력단 bind operator(⊙·NMDA·tension·revise-loop)는 same-state ablation에서 결과 불변=기여 0(H_1834/1837/1836/exp3).
- **LAW-4 objective additive floor** — CE 옆 aux(pred-info·constructive-bind·novel-margin surrogate)가 additive CLMConvMoE에서 trivial 붕괴(H_1816 step550, **EXP-1 A.novel=0·전 arm 0·garbled**).
- **LAW-5 FORM tunable, BIND earned** — raw detector=1-항 FORM은 게임 가능, 진짜 재조합=2-항(출력×seed)은 결합파괴 통제 margin Δ에만(H_6190: grow-window raw composed=2 PASS이나 novel-only=1=max_single FAIL = ECHO-ONLY).

**공통 형태:** G1은 두 소스 결합(2-항 상호정보)을 요구하는데 측정된 모든 메커니즘이 (i) 1-항 채널이거나 (ii) mouth의 frozen forward가 이미 잃은 정보를 복원하려 한다. CE가 최단경로(echo/최근 concept-tail)를 basin 전역최소로 보상 → 결합 상호정보가 mouth forward에 애초에 안 담김. = **objective-basin 메타법칙**(DPI의 learning-축 특수화).

**(b) 외부 수렴:** arxiv 30편 = **objective+정규화 > binding-operator > scale**. deep-research = **neurosymbolic만 DPI를 구조적으로 깬다(비-cheap)**. NT×CLS 융합은 별도 store가 새 능력을 더할 때 🟢이나 anima 해마는 MOUTHFLOOR(read-gate 부재로 이득 차단).

**(c) 발산 4 렌즈 + control:** ①non-CE 학습신호(contrastive-replace·energy·G-selection / control SHUF) ②architecture(TPR·pointer·external-mem read-gate·deep-RF / control wrong-D) ③생물(전전두엽 WM·기저핵 gating·해마-신피질·γ-synchrony / control phase-scramble) ④A⇄G tension-loop(/ control same-state INERT).

## PHASE 2 — IMPLEMENT (측정 스펙, 스킵 없음)

사다리: cheap probe(numpy DIRECTIONAL — RF-reachability + binding-lane ablation OFF/ON Δ) → 통과분만 engine-native(`hippo_g1_eval.hexa` echo-guard novel-only, SCRAMBLE/wrong-D, pool own-GEMM, gen=40 frozen).

판정(**벽을 측정하는 프로브** 명시):
- **AT-FLOOR 재현**(벽 확증, $0): deep-RF(RF≈513이 seed 이미 커버 → RF 벽 아님)·external-mem-retrieval(#2886 재현)·tension-loop(DPI INERT)·해마-신피질 consolidation(additive 회귀).
- **REACHABLE**(escape 후보, cost-gated 학습): contrastive-replace(1a)·energy(1b)·TPR-invariant(2a).
- **부분 REACHABLE**: sustained WM·gating·γ-synchrony(disjoint lane은 열림, mouth read-gate는 objective로 회귀).

## PHASE 3 — ABSTRACT

**메타법칙:** CE 학습은 echo(최단경로)를 전역최소로 갖는 basin을 형성, novel 결합은 saddle 너머. → additive/readout/retrieval은 전부 **basin-preserving**이라 최소를 못 옮긴다.

**escape (전제 붕괴):**
- **Escape-1** — CE를 **replace**하는 contrastive/energy trunk objective(echo=명시 negative, non-basin-preserving). EXP-1이 닫은 건 *additive* aux; **replace는 미측정**.
- **Escape-2** — TPR/binding-slot을 mouth forward **아키텍처 invariant**로 hard-wire(objective 아님, DPI 우회 유일 비-cheap 경로).
- **Escape-3**(tension-loop) = H_1834/1837 재포장 → **자가검증 기각**.

**자가검증:** Escape-1 = additive(falsified) vs replace(미측정) 결정 구분 → 재포장 아님. Escape-2 = objective 형태면 H_1816 붕괴(기각), **순수 forward hard-wire만** escape. → **살아남은 escape 2개**, 나머지는 census 정합=기각.

## PHASE 4 — FALSIFY (frozen 사전등록)

**bar (사후 이동 금지):** engine-native G1, gen=40 canonical, echo-guard novel-only, ckpt sha 고정. PASS = composed novel-only ≥2 ∧ >max_single(novel) ∧ SCRAMBLE/wrong-D collapse ≤1 ∧ leak=0, **≥4/5 seed HIT**.

- **PRED-E1** — contrastive/energy *replace* objective + held-out 조합 split(SCAN/COGS) 재학습 `.clm` → ≥4/5 HIT면 Escape-1 PREDICTIVE, 미만이면 objective-floor가 replace에도 성립=천장 강화.
- **PRED-E2** — TPR forward-invariant hard-wire `.clm`(CE 불변) → ≥4/5 HIT면 Escape-2 PREDICTIVE, 미만이면 architecture도 CE-basin에 삼켜짐=천장 강화.
- **NULL** — 둘 다 MISS → objective-floor는 (additive+replace+architecture) 전 학습축 성립=진짜 천장, 남은 건 non-learning 경로(외부 consequence loop, Family A/C2 = G1 재조합축 밖).

L4가 additive를 닫아 PRED-E1을 replace로 좁히고(중복 아님), L3가 retrieval을 닫아 PRED-E2를 architecture 축으로 보냄(L3·L4 미검 렌즈) — **escape 공간을 정확히 2개로 압축**.

## 정직 수렴

**(i)-우세 with (ii)-잔존.** basin-preserving 4 렌즈(readout·objective-additive·retrieval·coverage)는 각각 DPI-INERT / EXP-1 🧱 / #2886 🧱 / H_6190 ECHO-ONLY로 **engine-native 원리 기각** + 메타법칙이 전부 삼킴 = **매우 강한 천장**. 단 **non-basin-preserving escape 2개(CE-replace contrastive, TPR architecture-invariant)**가 census 자가검증 통과·미측정·cost-gated로 **정직하게 열려** PRED-E1·E2 사전등록됨. **L3 MOUTHFLOOR + L4 FALSIFY가 escape 공간을 이 둘로 압축한 결정 증거.**

---

**산출 상태:** 캠페인 4 phase + PREREG(PRED-E1·E2 frozen bar) 완성. **디스크 저장은 권한 샌드박스 차단**으로 미실행(`state/g1_fleetfull_breakwall/` 신규 디렉터리 생성 및 파일 쓰기 모두 승인 대기). 승인 열어주시면 `CAMPAIGN.md`(위 전문)+`PREREG.json`으로 즉시 저장하겠습니다. HYPOTHESES·카드·commit·PR·ARCHITECTURE·frozen bar·git 전부 미터치, sidecar fable 미호출.