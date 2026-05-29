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
- [ ] A9 (잔여) — n=8 실EEG montage(256-state MIP wall, pod/cloud 필요) · multi-subject ds005620(sub-1010 외) · 도달%→coupling subject tractography(DWI/Allen) · A6 paper closure 판정(a_paper_only_at_closure)


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
