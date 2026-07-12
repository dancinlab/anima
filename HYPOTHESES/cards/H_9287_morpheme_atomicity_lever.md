# H_9287 — MORPHEME-ATOMICITY: byte-tokenization이 stem-불변 NEG 등가류 형성을 막는가

## tier
🟡 **PENDING** (stage-1 SPAN-GEOM dump in-flight) — 2026-07-12 register

## 배경 (earn-seal 후 유일 미시도 레버)
G1 재조합벽의 read-side·corpus·measure 레버는 전수 earned-terminal. H_9272 γ earn-seal(표상층 LOSO
frozen probe)이 base 303M *문장 mean-pool*에 stem-불변 NEG 축이 없음을 확증 → 명시된 유일 reopen 레버 =
**architectural morpheme-level latent**(byte-LM이 안/않/못/아니를 형태소로 안 묶음). Fable 설계로 이 레버를
falsifiable하게 분해.

## leak vs lever 분리선 (Fable 핵심 통찰)
- **leak** = 등가류(identity)를 건네줌: 안/않/못/아니 → 공유 `⟨NEG⟩` 단일 ID. held-out stem 전이가 trivial
  (그냥 학습 토큰). ⟹ 무의미.
- **lever(non-leak)** = 경계(atomicity)만 건네줌: unsupervised segmenter(BPE-on-jamo·언어라벨 0)를 전체
  어휘에 균일 적용 → 부정 4어간 각각 **distinct** atomic code(빈도로 분리, 부정이라 분리 아님). 등가류는
  unlabeled 분포 공기로부터 **유도**돼야 함 = NBIND-FC가 byte substrate가 안 한다고 보인 바로 그 추상.
  아키텍처 변경 불필요(reversible byte codec).

## 2-stage 설계 (stage-2는 stage-1 결과에 gated)
### stage-1 · SPAN-GEOM ($0 frozen probe · base ckpt)
earn-seal PROBE_A는 문장 mean-pool(소비-인접)에서 봤음. 레버 전제는 한 층 아래: "byte tokenization이
substrate가 stem-level NEG 등가류를 **아예** 형성 못하게 하는가?" → **span-pool**(부정 stem 자기 바이트에
pool)로 frozen base에서 검증.
- LOSO span classifier: 안/않 span vs position-matched 전-용언 부정어(잘/좀/다시/자주/많이) span 훈련 →
  held-out 못/아니 span 검정. byte-identity는 LOSO서 전이 불가 → 적중 = 공유 NEG span feature = 등가류 존재.
- RSA Δ = within-NEG cos − NEG↔부정어 cos vs permutation null.
- 통제(probe-defect-census 준수·no max·paired bootstrap·MDE 사전계산): shuffle-y·adv-misfire·rand-span.
- **판정 갈래(둘 다 decision-grade)**:
  - **CLASS-EXISTS**(held-out bacc≥0.75·CI-lo>0.55·RSA>null·misfire clean) → substrate는 추상을 표상하나
    **소비만** 못함 = read/route side = 이미 earned-terminal ⟹ **morpheme-tokenizer 전제 반증 · 레버 $0 종결**
    (벽 verdict = corpus×CE measure로 확정, 표상 지형 매핑: span-존재·readout-부재).
  - **CLASS-ABSENT**(bacc≈chance·통제 clean) → 전제 생존 → stage-2 pod run 라이선스.

### stage-2 · MORPH-ATOM codec (1-pod · SPAN-GEOM=ABSENT일 때만 발사)
BPE-on-jamo(~4-8k merge) reversible byte codec → 형태소별 distinct 2-byte code. CPT(plain-CE·라벨-free
자연 ko 60-100MB) warm-start → held-out stem 0회 노출 drill grid → held-out flip bacc(F2). 5개 self-gate:
G-a(post-CPT geometry $0→미형성이면 STOP=PENDING(CPT-budget) not FAIL) · G-a2(pre-drill zero-shot flip) ·
arms M+C1(no-codec)+C3(shared-⟨NEG⟩ leak 천장/V1)+C2(held-out 제거 ablation). **PASS** = F2(M)≥0.70 &
F2(M)−F2(C1)≥0.15 & C3≥0.90 & (있으면)C2≤0.55, single seed=DIRECTIONAL·PASS후보→1 replication(V5).
**정직 scope**: "class 형성(G-a PASS)했으나 F2 여전 floor"도 decision-grade = architecture-lever terminal
(atomicity만 주는 더 깊은 morpheme arch도 이 null 상속).

## 결과
### stage-0 · $0 underpowered pre-check (기존 earn-seal dump 재활용)
기존 loso_hidden.npz(__seq 존재)로 stem이 24B window 든 것만 span-pool(n≈19-34/stem·n_adv=15). held-out
span classifier 못=0.515·아니=0.500=chance지만 n_adv=15로 classifier 붕괴(CI degenerate·SE=0.115·MDE
Δ≈0.23) = **INCONCLUSIVE-leaning-ABSENT**. 자유 EXISTS 신호 없음(레버 $0 종결 안 됨) → 정식 SPAN-GEOM 라이선스.

### stage-1 · SPAN-GEOM (n≈296/stem · PENDING)
_(dump in-flight · spangeom_hidden.npz → spangeom_probe.py 판정 대기)_

## 산출
`state/nbind_curriculum/`(gen_spangeom.py·spangeom_probe.py·spangeom_precheck.py·SPANGEOM_MORPHATOM_DESIGN.txt).
hidden=~/anima-weights/nbind_cement/spangeom_hidden.npz. base=clm303_clean.clm(비-SLW).
[[xbind-g1-crack-measure-not-substrate]]·[[goal-biolens-lane-engine-native-green]]·
[[measurement-metalaw-form-tunable-bind-earned]]·[[g1-readside-exhausted-gamma-spend-only]].
