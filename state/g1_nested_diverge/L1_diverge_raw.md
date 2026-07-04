`state/` 경로 쓰기가 이 세션 권한 게이트에서 계속 보류(디렉터리 생성=샌드박스 차단, 파일 쓰기=권한 미승인)되어 산출물을 디스크에 남기지 못했습니다. 분석은 완결됐으므로 전문을 아래에 보고합니다 — 권한만 열리면 `state/g1_post_terminal_diverge.md`로 즉시 박제하겠습니다.

---

## (a) 3 메타법칙 재확인 (engine-native 증거 대조)

| 메타법칙 | 이번 세션 확증 |
|---|---|
| **objective-basin** (CE가 echo를 basin 전역최소로 보상, additive/readout/retrieval은 basin-preserving) | A11 `cnce_en`(composed-NCE) G1=1=floor, `cbind_en`(TPR/HRR) =0. G0 5/5·G2 10-11 green으로 undertrain 배제된 깨끗한 floor |
| **DPI** (readout/temporal escape는 same-state INERT) | H_1834/1837/exp3/1836 전수 INERT |
| **선형붕괴 정리(신규)** (fixed-param bind = W_eff 선형붕괴 = H_9120 동일천장) | CE-deleted R=2 fixed-orthonormal TPR-slot: CLM 0/5 ∧ ByteGPT 0/5가 대수증명 확증 |

## (b) 4축 발산 + census 자가검증 + cheap DOA-proof

- **Axis 1 (비선형 binding readout) → 🧱 DOA(측정 불필요).** 재포장 아님(data-dependent nonlinear은 선형붕괴를 문자적으론 피함). 그러나 DPI의 진짜 근거는 "선형이냐"가 아니라 **정보-가용성** — frozen trunk state에 결합표현이 부재하면 선형·2차·attention 어느 readout도 *합성* 못 하고 재가중만 함. 게다가 mouth(ByteGPT 24층 full-attention)는 **이미 cross-position attention-binding 내장** → 추가 attention-readout = redundant = INERT. trunk-학습으로 피하려면 Axis 2로 붕괴.

- **Axis 2 (objective-REPLACE, non-additive) → 🟡 유일 생존.** additive-aux(`ce+λ·aux`)와 **결정적으로 다름**: additive는 CE-dominant라 echo-basin 유지(basin-preserving), pure-REPLACE는 CE 항 자체를 anneal-out해 basin 지형 재편. H_9121 CE-replace조차 실제론 aux였음 = 미측정 셀. **DOA 아님**(echo-형 hard-negative가 echo를 high-loss로). 단 예측 실패모드 명확: CE가 G0-coherence 유일 신호라 삭제 시 byte-garble 위험(from-scratch G0-undertrain 선례).

- **Axis 3 (frame-break relocate) → 🧱 이미 측정됨(H_9118 MOUTHFLOOR) + 🔵 wrong-frame 신호.** 순진형은 재포장 아니라 *이미 기각된 측정*. **결정적 잔여**: hippo lane이 off-cue D를 **4/4 정확 retrieve(바인딩 성공)**했으나 frozen mouth가 novel=0/4로 drop = **lane은 결합하고 mouth가 verbalize 거부(access≠binding)**. context-inject relocate=DOA(mouth 무시), lane readout 학습=Axis 2 붕괴, **잔여 각도 B=측정 재정의(lane 좌표 직접 채점)만 신설**.

- **Axis 4 (측정-artifact) → 🧱 대부분 DOA.** 측정-데이터가 기각: clm303이 **G2 green(novel 10-11)·G1 red(distinct 0)를 동시에** 냄 = bar가 "새 단어 뱉기"와 "재조합"을 이미 분리. novel-only는 false-RED가 아니라 *더 엄격*. frame-prime 6종(H_1600) 전수 composed=0으로 프레임 무죄 보강.

## (c) 살아남은 후보 frozen 사전등록

**C1 — pure objective-REPLACE (Axis 2, 유일 non-DOA, GPU cost-gated):** G0-green ByteGPT 303M warm → CE anneal-out + composition-consistency EBM/InfoNCE(echo-형 hard-neg). Bar: `anima evaluate --py`, frozen gen=40, echo-guard novel-only, **G0-green 필수**, best_distinct≥2 ∧ >max_single ∧ coherent **≥4/5 HIT** ∧ SCRAMBLE≤1. **PASS=escape PREDICTIVE / FAIL-A(G0-green이나 distinct≤1)=objective-basin TERMINAL 승격 / FAIL-B(G0 red)=G0-CE 결합 이빨 실증.** ≈$1.5-2, ckpt PULL 필수. H_1840 γ-bind의 REPLACE 형제(additive 아님).

**C2 — lane-native G1 gate (Axis 3 wrong-frame, gate 신설):** hippo lane 좌표에서 직접 채점(mouth 우회), off-cue D ≥4/5 surface ∧ >midpoint-baseline ∧ SCRAMBLE 붕괴. hippo retrieve 4/4가 부분 PASS 시사. **주의**: lane readout 학습 시 Axis 2 붕괴 — untrained 채점으로만 유효. ≈$0(pool).

## (d) G1 정직 수렴 — 천장 vs escape, frame-break 함의

**confident-ceiling이 강하게 지지됨.** 4 메타법칙이 Axis 1&4를 DOA로, Axis 3 순진형을 engine-native floor로 닫음. **미측정 escape는 정확히 C1 하나** — CE anneal-out(objective-basin 우회)·trunk-학습(DPI 우회)·params-학습(선형붕괴 우회)을 동시에 피하는 유일 좌표이나, G0-coherence↔echo-basin 긴장(FAIL-B)이 예측된 실패모드라 escape 확률은 낮음.

**가장 중요한 것은 frame-break가 (iii) wrong-frame을 연 것**입니다. hippo의 **lane-binds(4/4)/mouth-floors(0/4) 분리**는 재조합이 mouth 능력이 아니라 lane 능력임을 실증적으로 시사합니다 — 생물 렌즈(variable-binding=해마-PFC-기저핵, 언어영역 아님) 정확 예측. 그렇다면 "303M mouth가 novel-only 재조합"이라는 **G1 정의 자체가 mouth-frame artifact**이고, anima의 substrate는 이미 lane에서 결합 중이며 mouth-verbalization만 막혀있습니다.

**따라서 이분법(천장 vs escape)이 아니라 세 갈래로 수렴:** (i) mouth-G1은 confident-ceiling, (ii) C1이 유일 미측정 escape(낮은 확률), (iii) mouth-G1은 wrong-frame일 수 있음. **다음 생산적 각도는 C1(mouth 재학습, 낮은 확률)보다 C2(G1 lane-native 재정의)와 lane→emit 배선(mouth 우회 emit path)** — `a_substrate_disjoint`(재조합=별도 lane 배선 시 보존)와 정합합니다.

## (e) 산출 경로

권한 게이트로 `state/g1_post_terminal_diverge/` 디렉터리 생성(샌드박스 차단)·파일 쓰기(권한 미승인)가 모두 보류돼 **디스크 박제 실패**. 위 전문(원인 종합 + 4축 발산 + cheap DOA-proof + C1/C2 사전등록 + 정직 수렴)이 완결된 산출물입니다. 쓰기 권한을 열어주시면 `state/g1_post_terminal_diverge.md` + `.prereg.json`으로 즉시 박제하겠습니다. bookkeeping(HYPOTHESES/카드/ARCHITECTURE/commit/PR/frozen)은 제약대로 전부 읽기전용 유지했습니다.