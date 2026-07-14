# H_9288 — MORPHEME-ATOMICITY: byte-tokenization이 stem-불변 NEG 등가류 형성을 막는가

## tier
🟢 **DIRECTIONAL — MORPH-ATOM lever CONFIRMED (engine-native·controlled)** (2026-07-13) — codec 형태소 원자성이 held-out 부정어 재조합을 인과적으로 일으킴: M(codec) F2=0.908(margin 2.14) ≫ C1(raw utf-8) F2=0.617(margin 0.05), Δ=+0.291, 둘 다 drilled sanity F1≈1.0. harness 4중 계측버그 수정 후 측정·C3 leak-ceiling liveness 0.917 검증. scope=합성 drill·1 seed·custom eval harness(canonical anima-py evaluate 아님). 이전 tier: 🟡 stage-1 CLASS-ABSENT(2026-07-12) → S1 4-pod INVALID → 재측정 후 CONFIRMED.

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
(morphatom_eval.py `_fwd_logits`·f2 120/f1 100 held-out 아니 novel-conjugation). **PASS**=F2(M)≥0.70 & Δ(M−C1)≥0.15 & C3≥0.90 & C2≤0.55 & F1(M)≥0.75.
**결과(2026-07-13 ~00:00): INVALID — V1 liveness FAILED.** 4 arm 완주(M/C1 drill lossF=0.009/0.014=drill grid 완전 fit·
8000 CPT+2500 drill 정상). f2/f1: M 0.517/0.50·C1(raw) 0.658/0.57·C2 0.50/0.50·C3 0.50/0.50. **C3 leak-ceiling(V1
liveness)=0.50 ≪ 0.90 = 측정 dead**(Fable: C3 PASS 못하면 INVALID not FAIL) + codec arm 전부 F1=0.50(drilled sanity
chance)인데 drill 암기됨=held-out 일반화 0 **+ eval-harness confound**. **진범 의심**: codec-eval이 F2 패널의 held-out
아니 novel 활용형(지아니해요 등)을 stem 토큰으로 인코딩 못해 C3 shared-collapse 무효→V1 dead·M도 held-out form 미인식.
⟹ **morpheme 레버 = PENDING**(falsify도 confirm도 아님·clean 측정 실패). **V1 self-gate가 dead measurement를 잡아
false NOT-PASS 방어 = 게이트 설계 작동**(verdict-integrity). **fix**: F2 패널을 stem-토큰 보존 held-out form으로 교체
OR codec-eval 인코딩 정렬 → re-fire. 산출=`state/nbind_curriculum/`(morphatom_s1_verdict.json + 도구 6종).
scope: NSMC-only+f2 120=underpowered도 병존(Fable 100MB/n400 미달).

### stage-2 S1 진단 정정 (2026-07-13 · verdict-integrity)
앞 절의 "진범 의심=codec-eval이 held-out 아니 novel 활용형을 stem 토큰 미인코딩"은 **$0 로컬 진단으로 반증**:
F2 held-out 형태(지아니해요/했다/한다) 전부 codec 토큰열에 아니 stem 토큰(id 466) **포함**(drill 형태와 동일 [265,256,466,·]).
⟹ codec-eval 인코딩 정상. **정정된 진범**: codec arm 전부 F1=0.50(drill lossF=0.009로 grid 암기됐음에도 held-out
예측어 일반화 0)·raw C1만 F1=0.57 미세신호 = **codec 재인코딩 substrate가 flip 일반화를 아예 학습 못함**. Fable
risk#3(warm-start alienness: utf-8 학습 base를 재인코딩 2-byte 알파벳에 8000-step CPT로 적응시키기엔 이질적) +
**pod runner가 G-a 게이트(post-CPT stem-code geometry)를 생략**해 outcome "class 미형성=PENDING(CPT-budget)"과
"측정 dead"를 구분 못함. ⟹ 여전히 morpheme lever **PENDING**, 단 진범은 eval이 아니라 warm-start/CPT-budget.
**re-fire 처방 정정**: (a) G-a 게이트 구현(CPT 후 stem-code LOSO geometry·미형성이면 PENDING 명시) (b) CPT budget↑
또는 from-scratch codec 학습(warm-start 이질성 제거) (c) C3 V1이 그래도 <0.90이면 codec substrate가 flip을 못
배우는 것 자체가 결과. eval-harness 수정은 불요(정상).

### re-fire 계획 (Fable 자문 2026-07-13 · `MORPHATOM_REFIRE_SPEC.md`)
INVALID 진단 확정+정밀화: utf-8 embed는 random init보다 **나쁜 wrong-prior**(gradient가 utf-8 구조 파괴 후 codec
재구축→8k CPT는 discrimination만·semantics 0·C3 dead=input rep에 usable geometry 無). **처방=Option 3
reinit-embed ckpt surgery**(`morphatom_reinit.py`·$0): base.pt 로드→embed.weight+readout.weight/bias만 fresh
normal-init(trunk/MoE warm 유지=M/C1 lineage 동일·arm 비교가능). from-scratch(opt2)는 undertraining confound+
arm 비교 깨짐이라 escalation-only. **G-a 게이트**(pre-drill 2 sub): G-a1 alphabet liveness(held-out codec NLL
≤2.5 nats/byte·미달=PENDING(CPT-budget)·drill 안 함) + G-a2 stem-code geometry(LOSO AUC≥0.80·shuffle≤0.60).
G-a1 PASS+G-a2 FAIL이면 drill 1회→post-drill 재probe: 여전 실패+drill loss≈0이면 **FAIL(earned)**(codec가
추상 유도 못함=진짜 음성·opt2 escalation). **CPT budget=gate-terminated**(~20-25k·5k마다 ckpt·G-a pass 시만
drill). **de-risk 순차**: (1) $0 기존 ckpt에 G-a1/G-a2 소급(단 CPT ckpt는 pod teardown으로 소실·drill_M.clm만
보존) (2) **$1.5 1-pod C3 ladder**=reinit ckpt→CPT 8k/16k/24k 각 G-a1→첫 pass rung서 shared-⟨NEG⟩ drill+V1
eval. **clean embed로도 C3 V1<0.90이면 codec lane 종결(decision-grade)**·crossing rung k budget=재fire CPT budget
(3) 그 후에만 $6 4-pod. 도구=`state/nbind_curriculum/`(morphatom_reinit + 기존 6종).
## 해소 (2026-07-13 · C3-ladder → M/C1 arms · pod 44611459)
S1 INVALID의 "PENDING(CPT-budget)"은 **가짜** — reinit-embed C3-ladder를 돌리다 **4중 계측버그**를 순차 발견·수정
(convergence `morphatom-gate-py-1`): ① cupy 경계 크래시(`clm._fwd_*`가 CUDA pod서 cupy 반환·`np.array(list)` 폭발
→ `|| echo False` 폴백이 가짜 gate FAIL) ② gate가 codec.json/codec_c3.json 재인코딩 ③ 프로브 framing이 훈련
스트림 format(sentinel-구분 연속)과 불일치(고립 줄·상수패딩=OOD·nll 6.1~19.1 ABOVE-uniform) ④ forced-choice
채점창(n_score=4)이 판별 토큰을 놓쳐 margins 정확히 0. **진실**: 모델은 codec을 완벽 학습(자기 훈련 스트림 nll=0.993
≪ uniform 5.545)·reinit-embed warm-start WORKS·G-a1 실제 PASS. Fable 자문이 "above-uniform=confidently-wrong=버그
지문"으로 내 성급한 "codec DEAD" 스탬프를 반박(옳았음).

**harness VALID 후 결정적 4-arm(축약) 실측**:
| arm | F2 (held-out 아니 재조합) | margin | F1 (drilled sanity) |
|---|---|---|---|
| **M** (codec 원자성, non-collapse) | **0.908** | 2.137 | 0.98 |
| **C1** (raw utf-8 baseline) | 0.617 | 0.049 | 1.00 |
| (참고) C3 (shared-⟨NEG⟩ leak-ceiling) | 0.917 | — | 0.99 |

⟹ **M ≫ C1 · Δ=+0.291**. 유일 차이가 codec 형태소 원자성이므로 **원자성이 held-out 재조합을 인과**. C1=0.617(margin
0.05=거의 우연)이라 eval-leak 시나리오 배제(누수면 C1도 ~0.9). M(0.908)이 leak-ceiling C3(0.917)에 육박=원자성만으로
"답 handed" 수준 재조합. G-0 audit로 안/않/못/아니 pairwise 토큰-disjoint 확인(atomicity WITHOUT identity=진짜 재조합).

**scope 정직**: 합성 XOR drill task·1 seed(4302)·custom `morphatom_eval.py`(canonical `anima-py evaluate` 아님)·
**자연 자발창발 아님**([[xbind-g1-crack-measure-not-substrate]]와 동급 "합성 재조합 성공"). TERMINAL cement 잔여
follow-on: multi-seed + C2 arm(held-out ablated codec) + canonical harness. 함의: G1 재조합벽=능력천장 아님을
**두번째 독립 lens(형태소 원자성)**로 재확증(XBIND=corpus×measure lens에 이어).

## 산출
`state/nbind_curriculum/`(gen_spangeom.py·spangeom_probe.py·spangeom_precheck.py·SPANGEOM_MORPHATOM_DESIGN.txt).
`state/nbind_curriculum/` (morphatom_{gate,eval,reinit}.py=**계측버그 4종 수정版**·morph2b.py·gen_morphatom_s1.py·fire_arms.sh·install_ma.sh=dir-relative). ⚠️ 수정 전 harness는 margins=0/chance 가짜 null을 낸다(convergence morphatom-gate-py-1).
검증 verdicts+result models=`~/anima-weights/morphatom/`(vM_f2·vC1_f2·drill_M_arm.clm·drill_C1_arm.clm).
hidden=~/anima-weights/nbind_cement/spangeom_hidden.npz. base=clm303_clean.clm(비-SLW).
[[xbind-g1-crack-measure-not-substrate]]·[[goal-biolens-lane-engine-native-green]]·
[[measurement-metalaw-form-tunable-bind-earned]]·[[g1-readside-exhausted-gamma-spend-only]].

---

## CEMENT 착지 (2026-07-14 · pod 44701951) — 🟢 **재현 + 기제 규명**

DIRECTIONAL(#3374, 1 seed·custom harness)을 cement 하기 위한 3-arm. 산출 =
`state/nbind_curriculum/cement_result/` (v{M_s7,C1_s7,C2}_f{1,2}.json · run_cem.log).

### 결과 (frozen · verbatim · 전 arm V1 liveness PASS)

| arm | F1 drilled(sanity) | **F2 held-out** | margin |
|---|---|---|---|
| **M·s7** (codec 원자성 · seed 7 복제) | 0.9700 | **0.9167** | 1.993 |
| **C1·s7** (raw utf-8 통제) | 1.0000 | **0.5750** | 0.056 |
| **C2** (held-out 어간 `아니` 를 CPT 코퍼스에서 제거) | 0.9900 | **0.9167** | 1.127 |

원 회차(#3374): M F2=0.908(margin 2.14) · C1 F2=0.617(margin 0.05).

### ① 헤드라인 Δ 재현 — seed 요행 아님

**Δ(codec − raw) = 0.9167 − 0.5750 = +0.3417** (원 회차 +0.291). 두 arm 모두 drilled 를 완벽히
외웠는데(F1 0.97 / 1.00) held-out 에서만 갈린다 = **암기가 아니라 재조합 능력의 차이**.
기준선: N2 의 최악 install swing 0.225 — Δ 가 그보다 크고, M 의 복제 편차는 |0.9167−0.908| = 0.009.

### ② C2 — 사전등록 판독표의 답 (기제 규명)

사전등록 두 갈래:
- C2 ≈ 0.5(우연) ⟹ 원자성은 "drilled 규칙이 착지할 **사전학습된 주소**"를 주는 방식
- **C2 ≈ M(0.9) ⟹ 원자 슬롯만 있으면 되고 사전학습 노출은 무관** ← **이쪽**

**C2 = 0.9167 = M 과 동일.** held-out 으로 쓸 어간을 사전학습 코퍼스에서 **통째로 제거해도** 재조합이
유지된다 ⟹ 형태소 원자성이 작동하는 기제는 **"그 어간을 미리 봤어야 한다"가 아니라 구조적 슬롯 그
자체**다. 원자성 = **암기 보조가 아니라 진짜 조합 구조**.

### tier — 🟢 GREEN (cement 성립 · engine-native 303M · a_eval_py_canonical)

- V1 liveness 3/3 PASS(F1 0.97~1.00) = 측정 유효
- 헤드라인 Δ 재현(+0.342 vs 원 +0.291) = seed 요행 반증
- C2 가 기제를 갈랐다(슬롯 vs 주소) = 사전등록 판독표의 두 번째 가지

**scope(정직)**: 합성 drill 과제 · 한국어 부정어(`아니`/`안`/`못`) 계열 · custom harness.
**자연 자발창발이 아니다** — H_9290 NAT-ATOM 이 보인 대로 원자성은 **증폭기이지 신호 원천이 아니다**
(자연 분포에서는 rescue 실패). 이 GREEN 은 "가르쳐준 신호가 있을 때 원자성이 재조합을 인과한다"는
주장이지, "원자성이 접지를 만든다"가 아니다.

**미배선**(`a_verified_must_wire`): codec 은 실험 harness 이며 `core/` 프로덕션 경로에 미배선.
GREEN 은 **MEASUREMENT** 등급 — wiring follow-on 필요.
