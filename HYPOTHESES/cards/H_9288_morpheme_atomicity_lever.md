# H_9288 — MORPHEME-ATOMICITY: byte-tokenization이 stem-불변 NEG 등가류 형성을 막는가

## tier
🟡 **stage-1 CLASS-ABSENT** (span-층 morpheme-abstraction 부재 확증 · stage-2 MORPH-ATOM 라이선스) — 2026-07-12

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

### stage-1 · SPAN-GEOM (n≈296/stem · well-powered · 2026-07-12) — **CLASS-ABSENT**
정식 SPAN-GEOM(1763 prompt·안/않/못/아니 각 ~296 + position-matched 부정어 275 + freq-matched rand 299·
base 303M clm303_clean frozen span-pool·MDE Δ≈0.06 at nmin=275). LOSO span classifier(안/않 train→held-out):
| held-out | heldout_bacc | ci95 | shuffle | rand-baseline |
|---|---|---|---|---|
| 못 (mot) | **0.553** | [.519,.584] | 0.328 | 0.468 |
| 아니 (ani) | **0.547** | [.514,.579] | 0.317 | 0.435 |

RSA: within-NEG cos=−0.251 < NEG↔부정어 cos=−0.190 → **rsa_Δ=−0.061·exceeds_null=FALSE**(NEG 어간들이
서로 안 뭉침). ⟹ **CLASS-ABSENT**: held-out NEG bacc≈chance(0.55≪0.75 임계·CI가 0.5 겨우 상회)·RSA 음수·
shuffle clean·rand 통제 chance. base 303M byte substrate는 **span 층위에서도** stem-불변 NEG 등가류 부재 =
earn-seal(readout 층)에 이어 **2-stratum 확증**. ⟹ morpheme-tokenizer 전제 **생존**(반증 아님) → **stage-2
MORPH-ATOM codec 라이선스**. 함의: 벽 진범이 measure/corpus 아니라 architectural morpheme-abstraction 부재임을
표상층이 직접 지지(byte-LM이 안/않/못/아니를 분포적으로 한 클래스로 안 묶음).


### stage-2 · MORPH-ATOM (Fable 설계 · S0 착수 2026-07-12)
Fable 구현스펙(`state/nbind_curriculum/MORPHATOM_STAGE2_SPEC.md`): **MORPH-2B fixed-width 2-byte codec** —
전체 스트림을 자체 알파벳(ID 0-255 passthrough·256+r=BPE-on-jamo vocab freq-rank)으로 재인코딩해
atomicity(context-invariant 2-byte 서명)만 부여(identity 아님·label-blind). K-ladder{2048→16384} 중
G-0 audit 통과 최소 K 선택.
**S0 · G-0 codec audit = PASS** (`morph2b.py`·NSMC 130,639줄·$0 pre-fire blocking gate):
- **pairwise_disjoint=TRUE** — 안/않/못/아니 토큰ID **0개 공유**(아니가 안/않과 ㅇㅏㄴ jamo prefix 공유함에도
  단일 토큰 id=445로 fuse) ⟹ Fable가 지목한 최대위험(부분토큰 leak via ㅇㅏㄴ)이 실측 해소 = leak-free 확증.
- **held(아니) single-token** = atomicity 성립 · **roundtrip 무손실**.
⟹ codec 재설계/held-out 전환 불필요, S1 GPU fire ready.
**S1 (NEXT · cost-gated $4-6·4 dedicated pod·~2h)**: 4 corpus variant remap(M/C1 no-codec/C2 held-out제거
ablation/C3 shared-⟨NEG⟩ leak천장) → per-pod anima-py train CPT warm-start(~60min) → G-a(post-CPT stem-code
geometry·미형성이면 PENDING(CPT-budget))·G-a2(zero-shot flip confound) 게이트 → drill FT 90/10(~20min) →
F2(held-out flip)/F1 forced-choice eval. PASS = F2(M)≥0.70 & Δ(M−C1)≥0.15 CI-lo>0.05 & C3≥0.90 & C2≤0.55 &
F1≥0.75 & 게이트 green(paired bootstrap BCa·no-max). single seed=DIRECTIONAL·PASS후보→아니→못 rotation+1seed.

**S1 corpus 파이프라인 BUILT + 검증(2026-07-12·`gen_morphatom_s1.py`+`morph2b.encode_to_bytes`)**: codec 재인코딩
바이트 스트림을 anima-py train이 `open(rb)` V=256으로 직접 학습(train.py:337 확인·utf-8 제약無·단 Hangul-jamo
bucket bias는 raw경로 전용=codec tax·C1 통제). 30k 샘플 검증: K=2048 vocab2320·**held_in_drill_grid=0**(leak-free
assert 통과)·4 arm .bytes 정상(M 1.3MB<C1 raw 2.15MB codec 더 짧음·C2 held제거 1.28MB). fire 전 잔여 $0
scale-up 2건(eval f2 20→≥400 predicate/render 확장·CPT 1.3MB→HF anima-corpus-ko 병합 100MB+) + per-pod fire
스크립트 + **codec-space eval harness**(codec arm encoded label 채점·anima-py evaluate 확장) + $4-6 4-pod fire.

### stage-2 S1 · 4-pod fire LAUNCHED (2026-07-12 23:08 · verdict PENDING ~90min)
end-to-end 파이프라인 검증완료(smoke: codec build→CPT warm(emax4·base.pt)→drill→codec-eval GPU-fired D-acc·인프라
6+버그 근본수정→convergence hexa-cloud-exec-1). 4 dedicated RTX_4090 발사(M 가설·C1 no-codec raw·C2 held-out제거
ablation·C3 shared-⟨NEG⟩ leak천장/V1). 각 arm=full corpus CPT 8000step warm→drill 2500step→codec-eval
(morphatom_eval.py `_fwd_logits`·f2 120/f1 100 held-out 아니 novel-conjugation). **PASS**=F2(M)≥0.70 &
Δ(M−C1)≥0.15 CI-lo>0.05 & C3≥0.90 & C2≤0.55 & F1(M)≥0.75. 산출 도구=`state/nbind_curriculum/`
(morph2b·gen_morphatom_s1·morphatom_eval·morphatom_arm/pollall·install_ma). **scope 정직**: NSMC-only CPT(~9MB)
+f2 120=DIRECTIONAL(Fable 100MB/n400 미달)·성공 시 scale-up 재현 follow-on. verdict 착지 시 이 절 갱신+G1 gate.
## 산출
`state/nbind_curriculum/`(gen_spangeom.py·spangeom_probe.py·spangeom_precheck.py·SPANGEOM_MORPHATOM_DESIGN.txt).
hidden=~/anima-weights/nbind_cement/spangeom_hidden.npz. base=clm303_clean.clm(비-SLW).
[[xbind-g1-crack-measure-not-substrate]]·[[goal-biolens-lane-engine-native-green]]·
[[measurement-metalaw-form-tunable-bind-earned]]·[[g1-readside-exhausted-gamma-spend-only]].
