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
