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
