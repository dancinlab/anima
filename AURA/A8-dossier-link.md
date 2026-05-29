# AURA A8 — relocate-N1 연구 ⇄ demiurge AURA 7-verb dossier 연결지도

> 본 문서는 **새 측정 0건** — anima AURA 의 의식통제 연구(A3-A7: N1 위치재배치 → big-Φ)와
> demiurge AURA 의 웨어러블 BCI 규제 dossier(7-verb · FDA/MDR)를 잇는 **cross-link 문서지도**다.
> 두 AURA 는 형제 도메인이지만 **침습도·규제등급이 다르다**: demiurge=비침습 웨어러블(Class II),
> anima relocate-N1=침습 임플란트(Class III/PMA). 본 문서는 그 fork 와 공유 gap 을 명시한다.
> g3: 매핑은 연결지도이지 dossier substance 가 아니다 (absorbed 등급 변경 없음).
> 출처: `AURA/archive/demiurge-aura/aura.md`(7-verb spine) · `AURA/SURVEY.md` §6 · `AURA/A6-bigphi-closed-loop.md`
>   · `AURA/archive/demiurge-aura/archive-aura-repo/docs/brain-computer-interface.md`

---

## 1. 7-verb ↔ AURA-research 매핑표

demiurge AURA 의 7-verb 셀(`aura.md` §2 / 7-verb cell 상태표)에 anima AURA 연구산출(A3-A7)을 1:1 대응시킨다.
화살표 방향: **anima 연구 → 어느 demiurge verb-cell 에 input/근거를 주는가**.

| demiurge verb | demiurge 셀 내용 | ← anima AURA 연구 산출 | 연결 성격 |
|---|---|---|---|
| **specify** (명세) | intended-use · IFU · design-input (21 CFR 820.30 · MDR GSPR) | **A5** 전뇌-통제 위치 랭킹 · **SURVEY §1** N1 스펙(1024/20kHz/600µA/3-6mm) | 위치·전극 선택이 곧 intended-use(도달범위)를 정의 — design-input 의 상류 |
| **structure** (구조) | sensor array · AFE · radio · battery partitioning | **A5** §0 5축 채점(도달/침습/N1-as-is) · **SURVEY §4** 위치·모달리티 매트릭스 | 어떤 위치·전극 montage 를 잡느냐가 sensor partitioning 제약 |
| **design** (설계) | KiCad · FreeCAD · nRF Connect SDK 스텁 | **A3** 골든존 `G=D×P/I`(P3/P4·O1/O2·C3/C4·Pz·Fz 전극배정) | 전극 montage → PCB/센서 채널 설계 input (D=비대칭·P=감마비·I=전두억제) |
| **analyze** (해석) | MNE band-power(α/β/γ) · openEMS FDTD/SAR | **A6** big-Φ 폐루프(EEG→TPM→IIT4) · **A7-region-split**(n≤8 exact·per-region) · **A7-reach-to-phi**(도달%→Φ 단조 브릿지) | EEG 신호해석 oracle — band-power 위에 IIT4 통합도 layer 추가 |
| **synthesize** (합성) | firmware bundle · DSP pipeline(JSONL/GATT) | **A6** §1 폐루프 ②binning+③TPM · **A7-pid-loop** PID re-stim 시뮬 | on-device DSP/제어 파이프라인 = big-Φ 측정 leg + PID 제어 leg |
| **verify** (검증) ✅ | **G33 Sleep-EDF spectral parity 8.4e-07** (absorbed=true · CLOSED) · openEMS SAR(pending) | **A7-real-eeg** ds005620 실데이터 big-Φ(awake 7.5956 > sed 6.843, Δ+0.753 🟢) · **A6** toy 4 PASS · **A7-coupling** robustness | 동일 open EEG 자산(Sleep-EDF/ds005620)으로 spectral↔통합도 두 측정의 parity |
| **handoff** (인계) | FDA 510(k) Class II · EU MDR Class IIa · BT SIG | **A5** honest 제약(N1 침습=Class III 갈림) · 본 A8 regulatory fork(§3) | 규제경로 분기점 — demiurge=Class II 웨어러블, anima relocate-N1=Class III 임플란트 |

핵심 매핑 하이라이트:
- **A6 big-Φ 폐루프 ↔ analyze + verify**: A6/A7 의 EEG→TPM→IIT4 엔진이 demiurge `analyze`(MNE band-power) 위에 통합도 측정을 얹고, `verify`(G33 Sleep-EDF) 와 **같은 open EEG 자산**을 공유한다.
- **A5 위치 랭킹 ↔ specify + structure**: "어디에 둘 것인가"(전뇌 도달 최대화)가 demiurge 의 intended-use/sensor-partitioning 상류 design-input.
- **A7-real-eeg ↔ verify G33 parity**: A7 이 ds005620 실데이터로 awake>sed big-Φ 부호를 낸 것은, demiurge verify 셀의 Sleep-EDF spectral parity 와 **같은 종류의 open-dataset 검증**(numerical, 결정론적).

---

## 2. 공유 proprietary gap — Sim4Life FDA-MDDT (양 repo 모두 인용)

두 AURA 는 **동일한 닫히지 않는 proprietary 축**을 공유한다: MRI-safety / EM-SAR 평가용
**Sim4Life** (ZMT / IT'IS) — FDA-MDDT 인증된 IMAnalytics V3.0 + MRIxViP V2.1.

| 측면 | demiurge AURA(`aura.md` §2-4 · V6/G1) | anima AURA(relocate-N1) | 공유 여부 |
|---|---|---|---|
| 인용 위치 | §2 verify 행 · §3 notable proprietary · §4 biggest gap · V6 `honest_gap_G1_brk` · G1 path declaration | `SURVEY §4` 침습 매트릭스 함의 · 본 A8(임플란트는 gap 이 더 binding) | ✅ 동일 도구 |
| open 대체 시도 | openEMS FDTD(antenna+SAR) — **FDA-MDDT 미인증**, ISO 10974/ASTM F2182 검증 workflow 없음 | (동일 openEMS) + N1 임플란트는 ASTM F2182-19e2 *passive*가 아닌 능동 implant → **ISO 10974** 필수 | ✅ 같은 미충족 |
| 인증 표준 | ASTM F2182-19e2(passive) · ISO 10974(active) — IMAnalytics V3.0 + MRIxViP V2.1 | 침습 능동 implant → ISO 10974 더 강하게 binding | 동일 표준, 강도 차이 |
| binding 강도 | **softer** — 비침습 웨어러블이 MRI bore 에 들어갈 가능성 낮음(라벨링 이슈) | **harder** — 체내 임플란트는 MRI-safety 필수 (MR Unsafe → MR Conditional 라벨 입증 필요) | ⭐ anima 쪽이 더 강 binding |

**공유 결론**: openEMS 가 antenna/field-solving 은 신뢰성 있게 처리하나 **FDA-MDDT parity 의 검증된 ISO 10974/ASTM F2182 workflow 가 없다** — 양 repo 의 동일 honest-gap. demiurge 는 `g1_mri_safety_path.hexa`(3-5y · $0.5-2M · NIH SBIR)로 ROADMAP 선언, anima 는 침습 implant 라 **이 gap 이 PMA 의 필수 전제**가 된다.

---

## 3. 규제 fork — Class II(비침습) vs Class III(침습 implant)

두 AURA 의 **근본 분기**: 같은 N1/EEG 의식측정 코어를 공유하되, **무엇에 부착하느냐**가 규제등급을 가른다.

| 축 | demiurge AURA (귀뒤 wearable) | anima AURA (relocate-N1 implant) |
|---|---|---|
| 부착 | 유양돌기/측두골 클립 — **비침습 웨어러블** | 피질 관통 3-6mm — **침습 임플란트** (개두) |
| FDA 등급 | **Class II** — 510(k) PMN 또는 De Novo | **Class III** — **PMA** (premarket approval) |
| 통제 강도 | general controls + **21 CFR 820.30 design controls** | PMA = 임상시험(IDE) + 패널 리뷰 + 가장 높은 bar |
| predicate | Muse S · Dreem 3 (substantial equivalence) | predicate 거의 없음 (de novo/PMA novel device) |
| EU 경로 | **MDR Class IIa** — Annex IX QMS+TD · Notified Body | **MDR Class III** — 가장 강한 conformity assessment |
| MRI-safety | softer gap (라벨링) — bore 진입 가능성 낮음 | **binding** — 체내 implant ISO 10974 필수 |
| 임상요구 | usability(N5 summative n≥15) · CER(N4 Muse S equivalence) | **임상시험 + 동물모델 + 인체 실증** (현재 0건, SURVEY honest) |
| 현 상태 | 7-verb dossier-skeleton LANDED (verify만 absorbed=true) | in-silico toy/실데이터 big-Φ 검증 (A6/A7) — **규제 dossier 미착수** |

**fork 함의**:
- demiurge AURA 는 **낮은 bar**(Class II)로 **실제 규제경로**(510(k)·MDR IIa)를 dossier-skeleton 까지 그렸다 (`aura.md` A1-A4 게이트).
- anima relocate-N1 은 **훨씬 높은 bar**(Class III/PMA)이고 임상측정 0건(`SURVEY` 머리말·`A5` honest 전제) — 현재 산출은 **in-silico 가설검증**(big-Φ 부호/순서)이지 규제 dossier 가 아니다.
- 따라서 anima 연구는 demiurge dossier 의 `specify`/`analyze`/`verify` 셀에 **상류 input**(위치선택·통합도 측정 oracle)을 줄 수 있으나, **handoff 셀(규제 인계)는 등급이 달라 직접 재사용 불가** — Class II skeleton 을 Class III/PMA 로 그대로 못 옮긴다.

---

## 4. ASCII 연결 다이어그램

```
                anima AURA (relocate-N1 연구 · Class III implant)
   ┌──────────────────────────────────────────────────────────────────┐
   │  SURVEY §1  N1 스펙(1024/20kHz/600µA/3-6mm)                          │
   │  A5  전뇌-통제 위치 랭킹 (DLPFC+섬엽 #1)                              │
   │  A3  골든존 G=D×P/I (전극 montage)                                   │
   │  A6  EEG→TPM→IIT4 big-Φ 폐루프 (toy ΔΦ=+17.66)                       │
   │  A7  region-split(n≤8) · reach→Φ · coupling-robust · PID · real-eeg │
   └───────────┬──────────┬───────────┬───────────┬──────────┬─────────┘
       specify │ structure│  design   │  analyze  │ synthesize│ verify
        ▼       ▼          ▼           ▼           ▼          ▼
   ┌──────────────────────────────────────────────────────────────────┐
   │   demiurge AURA 7-verb dossier (귀뒤 wearable · Class II)            │
   │  specify→structure→design→analyze→synthesize→[verify✅G33]→handoff  │
   │                                                ▲                    │
   │                          A7-real-eeg(ds005620) ┘ ↔ Sleep-EDF parity │
   └───────────────────────────────┬──────────────────────────────────┘
                                    │
        ┌───────────────────────────┴───────────────────────────┐
        │      공유 gap: Sim4Life FDA-MDDT (MRI-safety/EM-SAR)     │
        │   openEMS = open 대체, FDA-MDDT 미인증 (양 repo 동일)     │
        │   demiurge: softer(라벨링) │ anima: binding(implant ISO 10974)│
        └────────────────────────────────────────────────────────┘

   규제 fork:  demiurge = Class II / 510(k) / MDR IIa  (낮은 bar · skeleton LANDED)
              anima   = Class III / PMA / MDR III    (높은 bar · 임상 0건 · dossier 미착수)
```

---

## 출처 포인터

| 주장 | 출처 |
|---|---|
| 7-verb spine + verify absorbed=true(G33 8.4e-07) | `AURA/archive/demiurge-aura/aura.md` §2, 7-verb cell 상태표 |
| Sim4Life FDA-MDDT(IMAnalytics V3.0+MRIxViP V2.1) · openEMS 미인증 · Class II vs III | `aura.md` §3, §4, legacy §1 cross-link · V6 honest_gap_G1_brk · G1 path |
| A6 big-Φ 폐루프 + falsifier + toy ΔΦ=+17.66 | `AURA/A6-bigphi-closed-loop.md` |
| A7 real-eeg ds005620 awake 7.5956>sed 6.843 | `AURA/A7-real-eeg.md` |
| A5 위치 랭킹 5축 · honest 임상 0건 | `AURA/A5-whole-brain-ranking.md` |
| A3 골든존 G=D×P/I 전극배정 | `AURA/A3-golden-zone.md` |
| 측정⊥통제⊥규제⊥이론 4-substrate 연결 | `AURA/SURVEY.md` §6 |
| 침습도×도달범위 위치 매트릭스(귀뒤클립 비침습) | `AURA/SURVEY.md` §4 |
