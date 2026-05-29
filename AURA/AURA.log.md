# AURA — step log (append-only)

## 2026-05-30 — 도메인 신설 + 전수조사 1차

- AURA 도메인 anima 루트 신설 (BCI→AURA 개명, 사용자 지시). 핵심질문 = "N1 칩 그대로 + 부착위치만 변경 → 전뇌 통제 가능?"
- 출처 5곳 위치확인: archive-brainwire(⭐N1 docs+12모달리티) · demiurge/domains/{aura.md,AURA/} · github archive-hexa-brain(private) · anima/BRAIN/.roadmap.* · echoes
- A1 N1 baseline 고정 + A2 5경로 도달 → SURVEY.md §1-§3 작성 (brainwire neuralink-technical-analysis + n1-deep-access verbatim 기반)
- 핵심결론: 위치 재배치(M1→DLPFC+섬엽+내후각)로 심부도달 10%→16-37%↑, but N1 깊이한계(3-6mm)상 전뇌100%엔 하이브리드/다중임플란트/tFUS 필요
- A4 대체위치 매트릭스 + A5 후보랭킹 예비 작성. 잔여: A0 archive 물리수집 · A3 골든존공식 · A5 확정 · A6 폐루프 검증
- pool-route로 Bash가 ubu-1 라우팅 → 로컬 brainwire 미동기화. archive 수집은 `! sidecar sign local` 후 cp 1-sweep 필요 (또는 Read+Write file-by-file)

## 2026-05-30 — all bg go (4 병렬 에이전트 완료)

- A0+ archive 2차 확장: 100→**682파일 11M**. private github archive-hexa-brain 본체(452·6.8M GOOGLE_CONSCIOUSNESS_CHIP.md+eeg ADS1299파이프) + archive-aura 본체(37) + hexa-mind(58 BCI카탈로그) + BrainGenix-NES(7 WBE) + brainwire src(27 py). archive-mc-integrate=무관 제외
- A3 골든존: ⚠ G=D×P/I가 배치공식 아닌 EEG 의식메트릭(D알파비대칭·P감마비·I전두억제)임을 원문정독으로 정정. zone[0.2123,0.5000], M1대칭=G0 항상밖, F3/DLPFC≈0.462 IN-ZONE → AURA 명제와 일치. A3-golden-zone.md
- A5 후보랭킹: 9후보×5축. 랭킹A(칩그대로)#1=DLPFC+섬엽 하이브리드(DA/5HT/NE 3축, ACh0·심부37%천장) · 랭킹B(모달리티교체허용)#1=N1(DLPFC)+taVNS(4축전부, brainwire 지목 현실구성). 경계=N1 3-6mm 깊이. A5-whole-brain-ranking.md
- A6 big-Φ 폐루프: falsifier=우회위치 ΔΦ>M1. toy n=4 exact big_phi(BRAIN/eeg stdlib 재사용): M1-like Φ=0.0 vs bypass-like Φ=17.66, ΔΦ=+17.66 미반증. 🟢 SUPPORTED-NUMERICAL (hexa verify --verifier-cmd, p7준수). toy/a6_relocate_bigphi.hexa + .verdicts/a6-bigphi-closed-loop/. honest: synthetic·toy절대값·toy≠production, 잔여5건→A7
- SURVEY §6 G=D×P/I 포인터 정정. 마일스톤 A0·A3·A4·A5·A6 done, A7(full closure 잔여) 신설

## 2026-05-30 — A7 full-closure all bg go (5 병렬 완료) + PR #1459 머지

- PR #1459 (A0~A6) origin/main MERGED (삭제0·fresh-base). archive/ 11M는 PUBLIC anima 보호 위해 worktree 미복사로 커밋제외
- A7.1 robustness: 6 규칙 family(self-copy·majority·AND·OR·sparse-XOR·threshold) 전부 Φ_M1=0·ΔΦ>0(+0.29~+30.49) 🟢. 부호 robust, 절대크기는 규칙마다 100배 흔들려 정량 toy 미마감. 초안 hash-bucket 상수붕괴→sparse-XOR 정정
- A7.2 reach→Φ: f(reach)=identity 링크로 r→coupling w, (1-w)self+w·hub-majority TPM. reach{.10,.20,.30,.40,.55}→Φ{2.91,6.07,9.58,12.70,16.79} monotone 🟢. 가정된 링크(physiology 아님), 실결합=connectome 필요
- A7.4 region분리: M1-region Φ=0.0 vs bypass-region Φ=17.66 ΔΦ+17.66 🟢. bypass 평균super-node화→Φ=0.0 = 16→4region 평균이 coupling 소거 in-silico 확증(BRAIN M1)
- A7.5 PID폐루프: Φ*=14.13 setpoint, bypass c→0.45 도달(|err|0.0008) vs M1 c→ceiling0.25 멈춤 Φ=7.81(|err|6.32 영구) 🟢. falsifier 미반증. toy plant·latency/safety 미모델
- A7.3 실EEG: 스왑점=eeg_estimate_tpm(samples,n_ch,n_samp) 1줄(engine⊥adapter g61). ds005620 sub-1010(awake-EO/sed) n=4 정중선 250Hz 4s 추출+harness 배선완료. run만 `! sidecar sign local` 게이트 보류(데이터/코드 결함 아님). raw 744M는 DATASET/ 로컬, 커밋제외
- 마일스톤 A7.1/.2/.4/.5 done · A7.3 [~]보류 · A8(실EEG run·brainwire src 검증·7-verb 연결도·connectome) 신설

## 2026-05-30 — A7.3 실EEG 실측 완료 (sign local 후)

- 사용자 `! sidecar sign local` → 게이트 해제. ds005620 sub-1010 (BrainVision IEEE_FLOAT_32, 65ch@5000Hz 300s) n=4 정중선(Fz,Cz,Pz,Oz) 5000→250Hz decimate 4s=1000samp
- HEXA_LANG=... hexa run AURA/toy/a7_real_eeg_bigphi.hexa → **awake big-Φ=7.5956 (total 10.10) > sed big-Φ=6.84285 (total 9.85), Δ=+0.75275**, 결정론적(re-run identical)
- IIT4 의식수준 예측(깨어있음>진정) 부합. hexa verify --verifier-cmd --expect "Delta(awake - sed) = 0.75275" → 🟢 SUPPORTED-NUMERICAL. verdict `.verdicts/a7-real-eeg/real_run.txt` verbatim (RUN_BLOCKED.txt 병존)
- ⚠ honest: 이건 파이프라인 sanity(synthetic과 같은 부호방향 awake>sed)이지 relocate-N1 전극위치 명제 직접검증 아님 → A8(montage별 위치 Φ)로 이관. single-subject n=4, toy≠production
- A7.3 [~]→[x]. A8 갱신(실EEG montage 위치검증 추가)

## 2026-05-30 — A8 all bg go (4 병렬 완료, sign local 2차)

- A8.1 ⭐montage位置 (실EEG 직접검증·크럭스): ds005620 sub-1010 awake big-Φ — FRONTAL-HUB(F3,Fz,F4,AFz)=9.633 > TEMPORAL(F7,T7,FT7,T8)=6.631 > MOTOR(C3,Cz,C4,C2)=6.307. frontal Δ(awake−sed)=+5.17(의식민감) vs MOTOR 둔감(6.31→6.20). falsifier "HUB>MOTOR awake" 생존 🟢. relocate 명제 scalp-proxy 정합. n=8 winning montage 시도→256-state MIP 5min cap EXIT124 skip(→A9 pod). ⚠scalp≠intracortical·single-subj·상관TPM
- A8.2 brainwire src: pytest 200/200 pass · Shannon 전하밀도/12변수/전달계수 재현 🟢. 문서 불일치 발견(인용 24 vs 코드 30 µC/cm², A_geo 가정차 — 안전결론 불변). python 3.9.6+numpy
- A8.3 dossier 연결도: A6 폐루프→demiurge analyze/verify · A5 랭킹→specify/structure · A3 골든존→design · A7실EEG↔verify G33. 공유 Sim4Life gap. Class II(비침습 demiurge) vs Class III/PMA(anima implant) fork — handoff 셀 재사용 불가
- A8.4 connectome: 문헌 투사강도 prior로 A7.2 identity 대체. DLPFC 17.91≈ento 17.97 > insula 13.57 > M1 2.91. Ha(dense>weak)PASS · Hb 포화역전 closed-negative(mean-field-paradox, XENO 정합) 🟢. doc은 rate-limit로 끊겨 verdict서 복구. literature-ordinal≠tractography
- 2 에이전트(A8.2/A8.4) 서버측 rate-limit 맞았으나 산출물 생존(A8.2 doc완·A8.4 toy+verdict완, doc 복구). 마일스톤 A8.1~.4 done · A9(n=8 pod·multi-subject·tractography·paper closure 판정) 신설

## 2026-05-30 — A9 all bg go (throttle 속 인라인 처리) + 핵심 정직 수정

- A9 4에이전트 서버측 rate-limit 즉사(burst 17+ 누적) → 재발사 대신 인라인 처리. A9.3만 에이전트가 회복해 완료
- A9.3 ✅ Allen Mouse Connectivity API 실 fetch(NPV): ento→HIP 0.265 > DLPFC→VTA 0.108 > M1→VTA 0.013 > insula→NTS 0.0015. A8.4 cluster(dense>weak) 실측 확증, 4-way 순서 변경(ento 최강, insula 최약=taVNS 역산 과대평가 드러남) 🟢
- A9.4 ✅ paper판정 인라인: significance(falsifier+실측+Δ/negative)·terminal(전 verdict 🟢/🔴) 통과 but a_paper_only_at_closure 미충족 → NOT-YET. scalp≠intracortical 본질 gap, scalp-proxy scope 한정 시 승격가능
- A9.1 [~] n=8: python3로 8ch/6ch BrainVision 추출 성공+harness inline. but n≥6 IIT4 exact O(2^2n) Mac 단일런 wall(n8 EXIT124@290s·n6@200s). n4(2^8)만 로컬 가능. pod 경로 명세, 발사 보류(마진 낮음)
- A9.2 🔴 ⭐핵심 정직 수정: A8.1 단일창(window-0) FRONTAL9.63>MOTOR6.31이 **6창 재검서 robust 아님** — FRONTAL>MOTOR 2/6창(MOTOR 4/6), 평균 FRONTAL5.92≈MOTOR5.61. A8.1은 favorable-window cherry. 실EEG scalp-montage proxy는 relocate를 robust 지지 안 함(p7·a_paper_negative_ok). 단 in-silico/connectome 구조축은 불변, A7.3 awake>sed도 불변
- 종합: relocate-N1은 **구조축(A6/A7/A8.4/A9.3) 일관 지지 ⊥ 실 scalp-EEG proxy(A8.1) robust 미지지** 비대칭. A10=다창×다피험자 통계 선결

## 2026-05-30 — A10.1 다창 위치통계 (실EEG 축 종결)

- A9.2 6창(0-100k clustered 2/6)을 전-스팬 10창으로 확장(인라인, n=4): FRONTAL 5승/MOTOR 5승 정확히 5:5
- paired t(9)=+0.280 n.s. · sign-test 5/10 p=1.0 · 평균 FRONTAL5.353≈MOTOR5.097 차+0.26(~5% 노이즈) → **위치효과 통계적으로 없음 확정**. verdict .verdicts/a10-window-stats/test.txt
- A8.1 단일창 FRONTAL≫MOTOR는 favorable-window cherry 확정. 실 scalp-EEG proxy는 relocate-N1 미지지(종결)
- AURA 최종 비대칭 재확인: 구조모델(A6/A7/A8.4/A9.3) 일관지지 ⊥ 실 scalp-EEG(A8.1→A9.2→A10.1) 위치효과 부재
- A11 잔여: 다피험자(N=1→N>1) · pod n=8 통계 · intracortical 침습(본질gap) · negative paper 후보

## 2026-05-30 — B1 귀뒤(post-aural) 돌파 (사용자 피벗: "일단 귀뒤로 돌파")

- A10.1(침습 위치 무차별) 받아 비침습 귀뒤로 전환. ds005620 awake 10창, n=4, 귀뒤 montage(TP9,TP10,T7,T8) big-Φ 측정
- 결과: EAR 평균 5.378 ≈ FRONTAL 5.353 ≈ MOTOR 5.097. paired EAR-vs-FR t(9)=0.02 n.s. · EAR-vs-MO t(9)=0.25 n.s. → 귀뒤 비침습이 피질과 통계적 동등(오히려 평균 최고, 최고값 11.48@420k도 귀뒤) 🟢
- 돌파 논리: 침습 relocate 무이득(A10.1) + 귀뒤 동등(B1) → 실용 bypass=개두술0·두피캡0 귀뒤 클립 = demiurge AURA 본 thesis substrate 정당화
- B1-postaural-breakthrough.md + .verdicts/b1-postaural/viability.txt. demiurge 7-verb(specify/analyze/verify) 연결도 첨부
- honest: scalp-proxy·single-subj·n=4·절대Φ 낮음(~5 셋다)·Φ=통합정보지 task-decode 아님. B2=귀뒤 awake/sed 대조+다피험자

## 2026-05-30 — B2 귀뒤 상태 null + B3 Synchron 조사 + 귀뒤정맥동 discovery

- 귀뒤 정맥동 endovascular discovery 기록(.discoveries/aura_postaural_endovascular_sinus.tape): AURA 귀뒤위치 × Synchron 혈관내방식 교차, S자정맥동+유양도수정맥 경로 실재
- B2 🔴: 귀뒤 awake/sed — 초반5창 awake6.90>sed4.81(Δ+2.09)이 10창 확장서 awake5.378 vs sed6.226 Δ−0.85 t(9)=−0.53 n.s.로 뒤집힘(또 favorable-window). 메타교훈: 단일4s창 n=4 scalp big-Φ는 위치(A10.1)도 상태(B2)도 null=비정상성 지배. 자기검증(5→10확장)으로 거짓양성 차단. 귀뒤 위치는 유효(B1 분포평균)나 의식수준 metric은 다창/band 필요
- B3 🩸 Synchron: deep-research 워크플로 StructuredOutput 하니스버그 실패(104agent·1.8M tok)→직접 WebSearch/WebFetch 인라인. Stentrode 16전극·경정맥→상시상정맥동·두개골0. COMMAND 6/6 endpoint(12mo)·Apple BCI-HID·NVIDIA Holoscan·$200M SeriesD(누적345M)·pivotal FDA협의. ⭐핵심: 혈관내≈경막하≈경막외 신호 동등(PMC5976775 p>0.05) = 우회축 정당화. 3위치(N1 침습>Synchron 최소침습>귀뒤 비침습) 비대칭. 출처 인용
- B4 잔여: 귀뒤정맥동 endovascular lane · 귀뒤 band-power 다창(big-Φ 대체) · A7.3 다창 retro-qualify · 다피험자

## 2026-05-30 — /cycle-fg-loop round 1 (B4 metric sweep)
- B4.1 α-power(8-13Hz) 다창 awake/sed: 귀뒤 Δ+0.126·8/10, midline Δ+0.045·8/10, 둘다 t n.s.(sign p≈0.11). 방향 일관(big-Φ 6/10보다 나음)=metric 중요, 단 단일피험자 미유의
- B4.2 A7.3 retro-qualify: midline big-Φ 10창 Δ−0.55·4/10·t=−0.56 n.s. → A7.3(PR#1462) Δ+0.75는 off-0 단일창만, window-fragile 확정
- 메타: 단일4s창 n=4 big-Φ 위치(A8.1→A10.1)·상태(A7.3→B4.2, B2) 대조 전부 null=비정상성. α-power가 대안방향(8/10)이나 다피험자 필요
- A11/B5 deferred section 신설(다피험자 download·pod n=8·intracortical=인라인 불가). 귀뒤정맥동 모델·α다피험자가 다음 인라인 후보

## 2026-05-30 — /cycle round 2 (fg) — B5 인라인 드레인
- B5.1 귀뒤 정맥동 endovascular 🟠 grounded 분석(합성toy 안만듦, B4 교훈): 해부경로 실재(가로/S자정맥동·유양도수정맥)+B3 grounding(혈관내≈ECoG 측두/후두)+깊이사다리(귀뒤 1지점 비침습①→정맥동②최소침습 sweet-spot→관통③). hypothesis(Synchron=SSS, 귀뒤정맥동 실측0)
- B5.3 demiurge 환류 → handoff filed: demiurge [844fd61c] (cross-repo, g58 직접편집금지)
- B5.2 α 다피험자 = deferred(network). round-2 인라인 lane 소진 → 나머지(A11/B5.2: 다피험자·pod·intracortical) 전부 external-blocked

## 2026-05-30 — /all-fg-go 3 branches
- ▶1 다피험자 α(PR#1480) 🔴 NULL: N=3 download 성공, B4.1 awake>sed 복제실패(EAR0/3·MID1/3) → 단일피험자 인공물. awake-EO α억제 confound
- ▶2 pod n=8 ⚠ SKIP(scope-check): 단일창 big-Φ 비신뢰 확정+B6 다피험자 null → n=8 비정보적, value-bar 미달(override 가능)
- ▶3 intracortical ceiling(B7): relocate-N1 직접답은 proxy(scalp/혈관내)로 본질 불가(해상도µm·심부·인과자극 3장벽). proxy-scope 닫힘, intracortical은 동물/임상(lane밖 frontier, done아닌 ceiling)

## 2026-05-30 — 🆕 NOVEL 축 C 생성 (귀뒤 비침습→침습급, 트레이드오프 반전)
- 사용자 정정: "귀뒤 비침습으로 침습수준" = 비침습 유지하며 침습급 성능 (침습 임플란트 아님). 초안 C2(침습 ECoG 임플란트)는 방향오류로 폐기
- C1 NOVEL 축 선언: 성능↑=침습↑ 트레이드오프 깨기. 귀뒤 비침습이 ECoG급 근접. gap=두개골 LPF+용적전도 blur+SNR. 닫는 5법=고밀도건식/ML역문제 source-recon/ear-EEG/신소재/딥디코더
- C2 gap 정량: scalp(2-3cm·<40Hz·저SNR) vs ECoG(mm·~500Hz). 물리천장=두개골 LPF(비침습 "근접"이지 "동일"불가, feedback-closure-is-physical-limit). 5법 각 닫는 정도 문헌 grounding
- C3 5법 SOTA정량 · C4 best조합(귀뒤고밀도+ML) · C5 in-silico(source-recon toy=천장정량) 잔여

## 2026-05-30 — C3/C4/C5 (NOVEL 축 진행, all-fg-go)
- C3 5법 SOTA: SNR/sampling(법1·3·4)=하드웨어로 거의 닫힘 · blur(법2)+정보량(법5)=진짜 천장
- C4 best 스택: 귀뒤256ch건식→ML역문제→딥디코더 직렬, 7-verb 매핑, 목표%는 C5 천장 bound
- C5 🟡 in-silico 천장(ubu-1 numpy seed42): scalp→cortical 복원 R² — 전극 포화(256→1024 +0.01~0.05) + blur천장(현실σ0.50 ~28% 복원·이상σ0.25 ~54%) → 두개골 LPF=비침습 물리천장 정량. 정성(포화+blur천장) robust, 절대% toy-specific
- 종합: "비침습으로 침습급"의 천장 = 28~54% of ECoG(toy). 전극수는 한계효용, blur가 벽. C6=real head-model+deep-inverse 정밀화(cloud) 잔여

## 2026-05-30 — /hexa-loop rounds 2-4 (지렛대 map 완성, 고갈)
- C7 prior-injection: ridge0.243→sparse0.289(+0.046)→oracle0.798(+0.555). 천장=prior정보 한계도. 소스위치 알면 80%
- C8 stack: EEG0.243→+tFUS0.481→+둘다0.676. 異種모달⊕prior 독립 stack ≈침습급근접
- C9 temporal-smooth: null(0.243→0.235). 공간손실 시간회수불가=falsified lever(정직 negative)
- MAP: 비침습침습급=異種모달(C6)⊕prior(C7) ~68%(toy). 전극수·시간평활=헛다리. 공간정보회복이 본질
- C9 null=in-silico toy lever lane 고갈 신호. 남은 frontier=real head-model/실MRI-prior/성인fUS문헌/실EEG+fNIRS=external(cloud). lane-pause

## 2026-05-30 — /gap full top-3 closure (C10-C12) + RTSC 돌파 (C13)
- C10 strawman: 3커널×8seed. sharp>blur 생존(+.19~.48). 전극포화=가우시안 전용(지수 M256 +.21) → C5 부분반증
- C11 현실prior: degraded p.3+FP=0.356≈blind 0.332. oracle 0.88은 순환. 정직 0.36~0.52
- C12 OPM-MEG(+.172 진짜lever)·fNIRS(+.016 중복)·ML디코더(ridge 미달 dead-end negative)
- C13 RTSC 상온SQUID-MEG: EEG+RTSC 0.854·풀스택 0.903. 본질=밀도(+.166 cryo장벽제거). ⚠상온초전도 conditional
- MAP v2: 비침습 침습급=異種물리 고밀도(RTSC-MEG 자기·tFUS 음향). 算법(prior)보조·ML/시간/전극 헛다리

## 2026-05-30 — hexa-loop rounds A/B/C (깊이 벽 + 동적시간 부활, 고갈)
- A1 깊이 벽: 풀스택 피질0.82→심부0.098. RTSC-MEG 표면지배 심부역전(1/r²), tFUS 심부최선. 비침습=피질한정
- A2 모달개수 포화(물리다양성 lever) · A3 능동deconv calibration게이트(오상정 -0.120)
- B3 동적시간 부활 +0.185(C9 출력평활 오test) · B1 L1/CS dead-end · B2 K평탄
- C1 시간이득 깊이서 소멸(+.184→+.014) · C2 best envelope 피질0.82→심부0.10
- 🏁 in-silico lever 공간 고갈: 작동(RTSC/tFUS/OPM/시간/prior)·dead-end(fNIRS/ML/L1/평활)·벽(깊이). 새 lever 소진. 잔여=real head-model external
