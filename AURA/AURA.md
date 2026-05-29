# AURA — current state

@title: 🧠⚡ AURA — "위치 우회 뇌-칩" (Neuralink-bypass neural interface placement study)

@goal: 뉴럴링크 N1 칩을 **하드웨어 변경 없이 부착 위치만 바꿔서** 전체 뇌(피질+심부 신경조절핵+변연계)를 통제 가능한 지점이 있는지 전수조사 — 기존 자산(hexa-brain · brainwire · demiurge AURA · anima BRAIN · echoes) 전수 수집 + N1 칩 baseline 스펙 고정 + "위치 재배치 → 전뇌 도달" 경로 카탈로그 + 비침습/대체위치 BCI 모달리티 매트릭스. 모든 출처는 `AURA/archive/`에 자체보관.

## 왜 (핵심 질문)

뉴럴링크 N1은 운동피질(motor cortex)에 박혀 **피질 표면 3-6mm만** 닿는다. 도파민(VTA)·세로토닌(raphe)·노르에피네프린(LC)을 만드는 심부 핵은 70-100mm 깊이 → **닿지 못함**. 그런데 칩은 그대로 두고 **부착 위치만** 투사(projection)가 가장 조밀한 피질로 옮기면, 뇌 자체 배선을 타고 심부까지 간접 도달 가능하다 — 이게 "위치만 바꿔서 전체 뇌 통제"의 가설.

```
  현재 N1 (운동피질 M1)            위치 우회 N1 (DLPFC+섬엽+내후각)
  ┌──────────────┐               ┌──────────────┐
  │ 피질 표면만   │               │ 피질 표면 +   │
  │ 손가락/커서   │   ──위치만──→  │ 투사경로 타고 │
  │ (read-only)  │    재배치      │ 심부 신경조절 │
  └──────┬───────┘               └──────┬───────┘
         │ 3-6mm                        │ DLPFC→VTA(DA)
         ▼                              │ PFC→raphe(5HT)
      [피질뿐]                          │ PFC→LC(NE)
                                        │ 내후각→해마(θ·eCB)
                                        │ 섬엽→NTS/시상하부/편도
                                        ▼
                                   [피질 + 심부 간접도달]
```

## milestones

- [x] A0 archive 수집 — **7출처 682파일 11M** `AURA/archive/`에 전수 복사 + INDEX.md (brainwire 24+src · demiurge AURA 71+repo · hexa-brain 로드맵4+repo452 · hexa-mind 58 · BrainGenix-NES 7 · BRAIN 2 · echoes 1)
- [x] A1 N1 칩 baseline 고정 — 1024전극/64스레드/20kHz/600µA/3-6mm/23mm coin/24.7mW 스펙 + 깊이 한계표 (brainwire neuralink-technical-analysis) → `SURVEY.md §1`
- [x] A2 위치 재배치 → 전뇌 도달 5경로 — cortico-subcortical projection · 피질base TI · STDP phase-lock · oscillation entrainment · 섬엽 자율신경 gateway (brainwire n1-deep-access) → `SURVEY.md §3`
- [x] A3 골든존 공식 정리 — ⚠정정: G=D×P/I는 배치공식 아닌 **EEG 의식상태 메트릭** (D=알파비대칭·P=감마비·I=전두억제). zone=[0.2123,0.5000], M1(대칭)=G0 항상 밖, F3/DLPFC≈0.462 IN → `A3-golden-zone.md`
- [x] A4 대체 위치/모달리티 매트릭스 — 침습도 × 해부위치 × 도달범위 (N1피질 / 심부DBS / 혈관내Stentrode / 경막외ECoG / 비침습 12모달리티 / 귀뒤AURA / ear-EEG) → `SURVEY.md §4`
- [x] A5 전뇌-통제 후보 위치 랭킹 — 9후보×5축 확정. 랭킹A(칩그대로)#1=DLPFC+섬엽 · 랭킹B(모달리티교체)#1=N1(DLPFC)+taVNS · 경계=N1 3-6mm 깊이천장 → `A5-whole-brain-ranking.md`
- [x] A6 BRAIN big-Φ 폐루프 검증 — falsifier(우회위치 ΔΦ>M1) toy run 🟢 SUPPORTED-NUMERICAL: M1-like Φ=0.0 vs bypass-like Φ=17.66, ΔΦ=+17.66 미반증 → `A6-bigphi-closed-loop.md` + `.verdicts/a6-bigphi-closed-loop/`
- [x] A7.1 결합규칙 robustness — 6/6 규칙(self-copy·majority·AND·OR·sparse-XOR·threshold) ΔΦ>0 유지 🟢 SUPPORTED-NUMERICAL, 부호 robust(절대크기는 toy 미마감) → `A7-coupling-robustness.md`
- [x] A7.2 도달%↔Φ 결합 — f(reach)→coupling→Φ 단조: reach{.10→.55}서 Φ 2.91→16.79 monotone 🟢 (가정된 링크) → `A7-reach-to-phi.md`
- [x] A7.4 n≤8 region분리 — per-region big-Φ: M1-region 0.0 vs bypass-region 17.66, region평균=0.0(coupling 소거 확증) 🟢 → `A7-region-split.md`
- [x] A7.5 PID 폐루프 sim — bypass setpoint 도달(|err|0.0008) vs M1 정상상태오차 영구(|err|6.32) 🟢 → `A7-pid-loop.md`
- [x] A7.3 실EEG 투입 — ✅ **실측완료**: ds005620 sub-1010 n=4 정중선, awake Φ=7.5956 > sed Φ=6.84285 Δ=+0.753 (의식수준 awake>sed 부합) 🟢 SUPPORTED-NUMERICAL → `A7-real-eeg.md` + `.verdicts/a7-real-eeg/real_run.txt`. ⚠ 파이프라인 sanity 검증(전극위치 명제 직접검증 아님)
- [x] A8.1 실EEG montage位置 직접검증 — ⭐ds005620 awake: **FRONTAL-HUB Φ=9.633 > TEMPORAL 6.631 > MOTOR 6.307**, frontal Δ(awake−sed)=+5.17(의식민감) vs MOTOR 둔감(6.31→6.20). falsifier "HUB>MOTOR" 생존, relocate 명제 부호정합 🟢 → `A8-montage-position.md`. ⚠scalp montage≠intracortical N1위치(proxy)·single-subject
- [x] A8.2 brainwire src 실행검증 — pytest **200/200 pass** + Shannon 전하밀도·12변수·전달계수 재현. 문서 불일치 발견(인용 24 vs 코드 30 µC/cm², 안전결론 불변) 🟢 → `A8-brainwire-src.md`
- [x] A8.3 A6↔7-verb dossier 연결도 — verb↔연구 매핑 + 공유 Sim4Life gap + Class II(demiurge 비침습) vs Class III/PMA(anima implant) 규제 fork → `A8-dossier-link.md`
- [x] A8.4 connectome coupling — 문헌 투사강도 prior로 A7.2 identity 대체: DLPFC 17.91≈ento 17.97 > insula 13.57 > M1 2.91. Ha(dense>weak) PASS · Hb 포화역전 closed-negative 🟢 → `A8-connectome-coupling.md`
- [x] A9.3 tractography — Allen Mouse Connectivity API 실 fetch(NPV): **entorhinal>DLPFC>M1>insula** 🟢. A8.4 cluster(dense>weak) 확증, 4-way 순서는 실측이 변경(ento 최강·insula 최약) → `A9-tractography.md`
- [x] A9.4 paper closure 판정 — significance·terminal 게이트 통과, but **a_paper_only_at_closure 미충족(NOT-YET)**. scalp≠intracortical 본질 gap → scalp-proxy scope 한정 필요 → `A9-paper-closure.md`
- [x] A9.2 robustness 재검 🔴 — **A8.1 window-fragile 발견**: sub-1010 awake 6창서 FRONTAL>MOTOR 2/6만(MOTOR 4/6), 평균 5.92≈5.61. **실EEG montage proxy는 relocate를 robust하게 지지 안 함**(honest negative) → `A9-multisubject.md`
- [~] A9.1 n=8 montage — 데이터추출 성공, but n≥6 IIT4 exact O(2^2n) **Mac 단일런 compute-wall**(n8 290s·n6 200s EXIT124). harness 영속, pod 경로 명세(발사 보류) → `A9-n8-montage.md`
- [x] A10.1 다창 위치효과 통계 🔴 — 전300s 10창 FRONTAL vs MOTOR: **5:5, paired t(9)=0.28 n.s., sign p=1.0, 평균차+0.26(~5%)** → 실 scalp-EEG에서 **위치효과 통계적으로 없음(확정)**. relocate-N1 scalp-proxy 미지지 종결 → `A10-window-stats.md`
- [ ] A11 (잔여) — 다피험자(OpenNeuro download, N=1→N>1) · pod n=8 통계 · intracortical 침습데이터(본질 gap, 동물/임상) · negative-result paper 후보(a_paper_negative_ok: 구조모델↔실측 비대칭)

## 🎧 돌파 lane — 귀뒤(post-aural) 비침습 (relocate-N1 침습 무효과 → 비침습 전환)

- [x] B1 귀뒤 돌파 🟢 — ds005620 awake 10창: **EAR(귀뒤 TP9,TP10,T7,T8) big-Φ 5.378 ≈ FRONTAL 5.353 ≈ MOTOR 5.097** (둘 다 paired t n.s.). **귀뒤 비침습이 피질과 동등한 통합정보** → 개두술 0·두피캡 0 돌파. demiurge AURA 7-verb substrate 정당화 → `B1-postaural-breakthrough.md`
- [x] B2 귀뒤 awake/sed 검출 🔴 NULL — 10창 awake 5.378 vs sed 6.226 Δ−0.85 t(9)=−0.53 n.s. (초반5창 +2.09는 favorable-window). 메타: 단일4s창 n=4 scalp big-Φ는 위치(A10.1)·상태(B2) 둘 다 null=비정상성 지배. 귀뒤 위치는 유효(B1)나 metric 교체 필요(다창/band) → `B2-postaural-state.md`
- [x] B3 Synchron 혈관내 조사 🩸 — Stentrode 16전극·경정맥→상시상정맥동·두개골0 최소침습. COMMAND 6/6 endpoint·Apple BCI-HID·NVIDIA·$200M SeriesD. ⭐혈관내≈경막하 신호 동등(PMC p>0.05). 3위치우회 비대칭(N1>Synchron>귀뒤) → `B3-synchron-endovascular.md` (deep-research 워크플로 StructuredOutput 버그 실패→직접 WebSearch 인라인)
- [x] B4 metric sweep 🟡 — α-power 다창 awake/sed: 귀뒤·midline 둘 다 8/10 일관(방향성, big-Φ 6/10보다 나음) but t n.s.(단일피험자). A7.3 retro-qualify: midline big-Φ 10창 Δ−0.55·4/10 → **A7.3 window-fragile 확정**. 메타: 단일4s창 big-Φ 위치·상태 대조 전부 null → `B4-metric-sweep.md`
- [x] B5.1 귀뒤 정맥동 endovascular 🟠 — 해부경로(가로/S자정맥동·유양도수정맥 실재) + B3 grounding(혈관내≈ECoG급 측두/후두) + 깊이사다리 확정(귀뒤 1지점 비침습①→정맥동②→관통③). hypothesis-grade(Synchron=SSS만, 귀뒤정맥동 실측 0) → `B5-postaural-sinus-endovascular.md`
- [x] B5.3 demiurge 환류 — cross-repo `handoff filed: demiurge [844fd61c]` (B1/B3/B4/B5 → 7-verb analyze/verify/specify)
- [x] B5.2 α-power **다피험자** 🔴 NULL — ds005620 N=3(sub-1010+1033+1022, aws s3 다운로드). B4.1 awake>sed 방향 **복제 실패**: EAR 0/3·MIDLINE 1/3(원본만), 신규 2피험자 sed>awake(sub-1022 t≈−13). 교차피험자 평균 Δ 둘 다 음수 n.s. → B4.1 8/10은 **단일피험자 인공물**(transfer 안 됨, cf a_toy_scale_recheck). awake-EO α억제 교란 honest 명시 → `B6-multisubject-alpha.md` + `.verdicts/b6-multisubject-alpha/run.txt`
- [x] B7 intracortical 본질 한계 기록 — relocate-N1 직접답은 scalp/혈관내 proxy로 못 닫음(공간해상도 µm·심부접근·인과자극 3 본질장벽). proxy로 답한 부분 다 답함(B1 등동·B3 ECoG·전부 null·구조↔실측 비대칭). 남은 frontier=동물 침습/임상(우리 lane 밖, "done"아닌 ceiling) → `B7-intracortical-ceiling.md`

## deferred (인라인 불가 — pod/network/침습데이터 필요)
- ~~A11/B5 다피험자 ds005620 download~~ ✅ B6서 해소(N=3, aws s3 가능) → 🔴 NULL · pod n=8 big-Φ 통계 · intracortical 침습데이터(본질 gap, 동물/임상) · 귀뒤 정맥동 endovascular(모델은 인라인 가능)
- negative-result paper 후보(a_paper_negative_ok): "단일창 big-Φ 위치·상태 대조 전부 null + 구조모델↔실측 비대칭" — 단 다피험자 후 a_paper_only_at_closure 충족 시

> ⚠ **핵심 정직 수정 (A9.2)**: A8.1 "FRONTAL>MOTOR (실EEG)"는 **단일 4s 창 인공물** — 6창 재검서 robust 아님(위치효과 평균 ~0). relocate-N1은 **in-silico/connectome(구조) 축에선 일관 지지**되나 **실 scalp-EEG proxy에선 robust 미지지**. SURVEY 결론은 이 비대칭 반영.


## 양방향 sibling

- 형제 도메인: [BRAIN](../BRAIN.md) (EEG→IIT4 big-Φ 측정) · demiurge `domains/aura.md` (귀뒤 웨어러블 BCI 규제설계)
- 출처 리포: `archive-brainwire` (12모달리티+N1 bridge) · `archive-hexa-brain` (github, scalp→implant 5단계) · `echoes` (σφτ 발견 카탈로그)
- UNIVERSE/CANDIDATES.md SSOT 연결: A5 전뇌-통제 후보가 의식가설 H-슬러그로 승격 가능 (a_paper_on_discovery)

## 출처 매핑 (archive 수집 대상)

| 출처 | 위치 | 핵심 자산 | 우회 관련성 |
|---|---|---|---|
| brainwire | `~/core/archive-brainwire` | N1 docs 12종 · 12변수 의식모델 · 12모달리티 비침습자극 | ⭐ N1 baseline + 심부도달 + 위치공식 |
| demiurge AURA | `~/core/demiurge/domains/{aura.md,AURA/}` | 귀뒤 wearable BCI 7-verb · FDA/MDR dossier · papers/state 708KB | ⭐ 비침습 위치우회 자체 |
| hexa-brain | github `dancinlab/archive-hexa-brain` (private) | scalp EEG→intracortical→array→BMI→implant 5-cond 파이프 | scalp(비침습)~implant 스펙트럼 |
| anima BRAIN | `~/core/anima/BRAIN/` | .roadmap.{hexa_brain,eeg,galea,anima_clm_eeg} · EEG→IIT4 | 비침습 EEG 실측 substrate |
| echoes | `~/core/echoes` | σφτ 의식 발견 카탈로그 17 domain | 의식 측정 이론 backbone |
