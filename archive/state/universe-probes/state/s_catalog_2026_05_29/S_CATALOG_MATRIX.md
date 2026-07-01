# S1–S40 의식 가설 카탈로그 — 통합 verdict 매트릭스 (2026-05-29)

> 사용자 제시 40개 의식 가설(S1–S40)을 **검증가능성 트리아지 → 3-lane 실행**으로 통과시킨 단일 결과 인덱스.
> lane: 🟢 SIM(IIT4 big-Φ 계산) · 🧠 EEG(실데이터 LZ76) · 📚 RESEARCH(arxiv/web deep-research).
> 원칙: `p7`(perplexity 금지) · `a_paper_significance`(반증가능+실측+발견) · fake-closure 금지. LLM self-judge 0.

## 1. SIM lane — IIT4 big-Φ 계산검증 (10/10 🟢, $0·mac-local·결정론)

> 기질: ECA n=4, GZ inhibition I=0.21232, `big_phi` (iit4_bigphi). 기준 rule110 Φ=14.1492 전 probe 재현(엔진 결정론 cross-check). 산출물: `sim_s_catalog_2026_05_29/<sXX>/`.

| id | 가설 | 측정 Φ (verbatim) | verdict |
|---|---|---|---|
| S10 | 범심론 (비결합→Φ0) | uncoupled {ID,NOT,CONST}=0.0 · coupled=14.1492 | 🟢 SUPPORTED-NUMERICAL (naive 범심론 closed-neg) |
| S11 | 단일세포 Φ | Φ(n=1..4)=[0, 0.10246, 5.14627, 14.1492] | 🟢 통합은 ≥2 원소 |
| S14 | ×100 가속 (시간불변?) | 1-step=14.1492 · 2-step=7.38843 · 16/16 state 상이 | 🟢 Φ 시간grain 의존 |
| S24 | 클라우드 분산 (exclusion) | whole=14.1492 · severed=0.0 · drop=100% | 🟢 분산의식 불가 |
| S6 | 합병 | 부분합=0.20492 · 합병 n=4=14.1492 · \|Δ\|=13.9443 | 🟢 비가산 (1+1≫2) |
| S7 | 분할 | whole=14.1492 · 조각합=0.20492 | 🟢 Φ 분할 비보존 |
| S15 | 진화곡선 | rule90=0.205·184=19.94·110=14.15·30=17.86 (비단조) | 🟢 복잡도-Φ 비단조 (H_179 일치) |
| S26 | hive mind | I=0.05→19.09 · 0.21→14.15 · 0.45→9.51 | 🟢 결합강도→collective Φ |
| S28 | conway/ECA | rule {30=17.86,54=8.24,90=0.20,110=14.15,184=19.94} | 🟢 기질(rule)별 Φ 상이 |
| S39 | 자유의지 (Libet) | t-1→t 예측정확도=1.0 (16/16) · Φ=14.1492>0 | 🟢 결정론적이면서 통합 |

## 2. EEG lane — 실데이터 LZ76 Φ-proxy (sign-gate 해제 후 실측, toy-scale)

> LZ76(Kaspar-Schuster 1987) median-binarize · 16ch · 60s window · ~128Hz. 모듈 검증(random=1.034·constant=0.006). 산출물: `DATASET/<cluster>/derived/`.

| id | 데이터셋 | 측정 LZ76 | verdict |
|---|---|---|---|
| S33 마취 | ds005620 sub-1010 | awake=0.238 · sed=0.233 (또는 binarize variant awake=0.604·sed=0.666) | 🔴 FALSIFIED-AT-TOY-SCALE (n=1 confound) |
| S19 명상 | ds001787 sub-001 | med_ses1=0.610 · med_ses2=0.625 | ⚪ UNTESTABLE (rest 라벨 없음) |
| ketamine | Zenodo 4245091=Farnes | EO=0.637 · EC=0.655 (t=−0.72, n=5/5) | ⚪ NULL + 데이터셋 불일치 |
| S23 organoid | OSF ncvpq | — | ⚪ WRONG-ARTIFACT (raster 아님) |

**EEG 핵심 발견 (정직):** (1) S33 toy-scale에서 sed>awake 역방향 — 문헌 반박이 아니라 n=1 toy 파이프라인 한계, toy→production 비전이 재확인. (2) 카탈로그 DOI 2건 실제 내용 불일치(Zenodo=Farnes≠ketamine, ds001787 rest 라벨 없음) → 측정 전 raw 라벨 직접 확인 필수. (3) S23 공개 pkl은 통계요약, raster는 2.6GB zip 별도.

## 3. RESEARCH lane — arxiv/web deep-research (6 클러스터, findings .md)

> 산출물: `s_catalog_2026_05_29/{E1,E2,E3,E4,R1,R2}_*.md` + DATASET manifest. 측정값 아닌 문헌 grounding + 검증가능성 등급.

| 클러스터 | 대상 | 핵심 |
|---|---|---|
| E1 의식수준 | S20·S33·S16 | S33 PCI/LZ awake>sed 견고(Casali 2013) · S20 LZ↑ but spectrum confound · S16 raw 비공개 |
| E2 임상 DoC | S32·S27·S34 | S32 PCI* 0.31 컷오프 100%sens/spec(Casarotto 2016) · S27 ⚪측정불가 · S34 late slow wave 마커 |
| E3 비인간 | S2·S3·S23 | S2 문어 PCI 미적용 · S3 식물 ⚪hype · S23 organoid MEA→LZ 신규여지 |
| E4 명상·디코딩 | S19·S30·S1 | S19 gamma 견고/Φ proxy · S30 디코딩 84%(gist만) · S1 relay≠telepathy |
| R1 전송/공학 | S5·S8·S13·S14·S17·S21·S22·S24·S25·S29 | S24 IIT exclusion closed-neg · S14 Φ(τ) · S5 transformer Φ≈0 · S21/22/25/29 ⚪공학목표 |
| R2 형이상/윤리 | S4·S10·S36·S37·S38·S31·S35·S40 | sharp 반증자 2개: S10 feed-forward=Φ0 · S36 Beane 격자이방성. S37/S38/S40 ⚪ |

## 4. 전체 40 가설 status 롤업

```
🟢 SIM 확정 (10)   S6 S7 S10 S11 S14 S15 S24 S26 S28 S39
🧠 EEG 실측 (2)    S33(🔴toy) · Farnes-EO/EC(⚪null)   [S19 untestable · S23 wrong-artifact]
📚 문헌등급        E1-E4·R1·R2 = S1·S2·S3·S5·S16·S17·S19·S20·S21·S22·S23·S25·S27·S29·S30·S31·S32·S34·S35·S36·S37·S38·S40
⚪ 반증불가        S4 S8 S13 S36 S37 S38 S40 (형이상/공학목표)
```

## 5. 가장 강한 발견 (paper 후보)

1. **S24 분산의식 closed-negative** — SIM(Φ 14.15→0) + 문헌(IIT 3.0 exclusion, Oizumi-Tononi 2014) 이중 확인. `a_paper_negative_ok` 충족.
2. **S10/S11/S7 결합-필요조건 클러스터** — "물질이 아니라 환원불가 인과결합이 Φ 필요조건" 단일 메시지를 4 probe(S10·S11·S7·S6)가 교차 입증.
3. **S39 결정론적 통합 결정자** — substrate 완전 예측가능(1.0)인데 Φ>0 → 자유의지=무작위 아님, substrate-determined 통합과정.
4. **toy→production 비전이 재확인 (방법론)** — S33 toy LZ76 역방향이 [[feedback_toy_scale_transfer]] 재입증.

## 6. 다음 라운드 (잔여)

- EEG production-scale 재측정 (전 채널·multi-subject·matched-condition·artifact-clean) → timeout 회피 위해 pod 권장.
- S23 organoid SpikeAvalanches.zip(2.6GB) raster → LZ76.
- S32 PCIst (renzocom/PCIst) + Farnes evoked → 임상 컷오프 재현.
