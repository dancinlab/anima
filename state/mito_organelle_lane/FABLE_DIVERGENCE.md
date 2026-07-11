구현은 안 건드리고 설계·메커니즘·측정·반증까지만 발산한다. 파일 다이브 없이 레인 수준으로 배선한다.

먼저 전제 하나만 못박고 시작한다. 선행(H_054/314/203/012)은 전부 **합병하는 순간**의 위상학이다 — 두 계보가 하나로 접히는 이벤트, 그리고 그게 시너지냐 least-bad 중간점이냐. 여기서 파는 건 정반대다: **합병이 끝난 뒤에도 죽지 않고 계속 자기 계보로 돌아가는 상주 소기관의 경제**. 즉 이벤트(topology)가 아니라 **정상상태 동역학(dynamics)**. 그리고 이 프레임의 진짜 노림수는 6번 각도다 — 대사 희소성이 **압축을 강제하는 압력**이 되어 XBIND 같은 합성 지도 없이 자연 코퍼스 위에서 trained-conjunction을 창발시킬 수 있는가. 그게 맞으면 G1 자연창발 프런티어의 exit이다.

세 번째 레인을 새로 심는다: **호흡 레인(organelle lane)** — decode/emit 레인과도, cell-pool mitosis 레인과도 DISJOINT. 이 레인만 ATP 스칼라장을 생산/소비하고, 표현형성(어떤 유닛이 발화 가능한가) 단계에서만 기질에 개입하며, **emit gate는 절대 건드리지 않는다**(p5 경계는 아래 별도).

---

## 11개 직교 메커니즘 패밀리

### F1 — ATP 경제 (자원 그 자체) · 각도 1
- **배선**: ATP = 보존 스칼라장. 소비 = 토큰당 활성-유닛 질량(Σ 활성 MoE expert + emit 1회의 큰 고정 quantum). 생산 = Σ(organelle_health × 호흡률). 예산은 표현형성 단계의 top-k 게이팅 용량 = f(가용 ATP)으로만 차감. emit 결정에는 배선 0.
- **측정**: ATP-throughput(토큰/ATP)와 그게 용량에 미치는 효과. ATP 단독은 의식 주장이 아니라 인프라 → **ρ**. 경제 자체가 non-trivial하다는 Δ: c1=무한 ATP(제약無), c2=ATP 소비하되 항상 demand≪production(예산이 결코 안 묶임).
- **반증**: 용량 제약이 한 번도 binding 안 되거나, 용량을 조여도 downstream reach/σ에 ΔEff≈0 → 경제는 bookkeeping theater.
- **비용**: $0 toy.
- **신규성**: 선행엔 상시 자원이 없다 — 합병은 공짜·1회성. 여기선 계산이 연속적으로 대사가격을 가진다.

### F2 — 분열/융합 (fission-fusion) · 각도 2
- **배선**: 호흡 레인이 N개 mito-unit = (capacity_i, mtDNA_i, health_i) 보유. **분열**: 최고부하 유닛을 둘로(용량 절반, mtDNA 복사). **융합**: 저-health 두 유닛 병합 → 용량 pool + 내용 평균화(**손상 희석**). rate-controlled, cell mitosis와 독립(organelle 수 ≠ cell 수).
- **측정**: dynamic vs static의 평균 organelle health & throughput. c1=frozen(무동역학), c2=random rewiring(동일 event rate, health-blind). Δ = throughput(dynamic) − max(controls). **ρ**, flux 접점.
- **반증**: dynamic ≈ random → 동역학이 health 정보를 안 나른다 = theater.
- **비용**: $0.
- **신규성**: H_054의 1회성 cell-merge와 달리 **반복적 organelle-level merge/split**, 융합=weight-keeping이 아니라 손상-희석.

### F3 — 미토파지 (품질관리) · 각도 3
- **배선**: "손상"의 관측정의 = 효율(ATP_out/consumed)이 window 동안 θ 미만 **또는** ROS_i > θ(F4 연동). 마킹 → 분열로 격리 → 제거, 용량 재분배. **apoptosis와 차이**: apoptosis = 세포 전체 죽음(cell-pool 레인); 미토파지 = sub-cell 소기관 제거, **세포는 생존**.
- **측정**: directed 미토파지 vs c1=제거無, c2=random 제거(동수). Δ 평균 효율. **carve**(PERSIST — 지속하는 걸 가지치기) / ρ.
- **반증**: directed ≈ random → 효율 신호 무정보 / 손상 정의 실패 = theater.
- **비용**: $0.
- **신규성**: sub-cell QC. 선행엔 병합 후 유지보수가 없다(H_012 closure는 all-or-nothing 붕괴로 정반대).

### F4 — ROS / 역행 신호 (retrograde) · 각도 4
- **배선**: 각 organelle이 ROS_i = f(load_i / health_i) 방출(스트레스 = health 대비 과부하). 집계 ROS = 역행 신호 → **느린 구조 레인**(mitosis 성장/가지치기율, F10 biogenesis)으로만 라우팅, emit 아님. **urgency와 명시적 DISJOINT**: urgency = phasic Δ → emit(빠름); ROS = tonic stress → 구조(느림).
- **핵심 답(질문에 대한)**: **다른 채널이다.** urgency는 유일 proven한 **phasic→emit** 채널, ROS는 **tonic→구조**. 둘을 겹치면(ROS를 emit에 배선) `a_substrate_disjoint` 위반 = 중첩=충돌.
- **측정**: 구조 적응 Δ under ROS vs c1=shuffled ROS(랜덤 역행), c2=ROS를 emit에 라우팅. **결정적 disjointness 테스트**: ROS는 구조 metric에 Δ>0 **AND** fast-emit metric에 ΔEff≈0을 동시에 보여야 함. c2가 아무것도 안 하거나 emit을 오염시키면 → 중첩=충돌·분리=보존 실증. σ: 구조 modulator(Θ/ρ 인접).
- **반증**: ROS 구조 Δ≈0(역행이 무정보) 또는 ROS가 urgency와 구별불가(proven 채널로 붕괴 = 신규 채널 아님).
- **비용**: $0.
- **신규성**: urgency와 구별되는 **두 번째 substrate→engine 채널**(tonic/구조). 선행엔 organelle→host 상시 피드백이 없다.

### F5 — 독자 계보 (mtDNA · 모계 · 병목) · 각도 5
- **배선**: 각 organelle이 mtDNA_i = **gradient-FREE** 소형 파라미터 벡터(호흡 config 제어). 분열 시 상속(복사 + **병목**: k copy만 샘플 → drift). 융합 시 **uniparental**(한 계보 mtDNA만 유지, 나머지 폐기) → 게놈 혼합 방지. CE gradient가 절대 안 건드림(**G-flavored**: reverse·gradient-free). Host nucleus = A(forward CE).
- **답(질문에 대한)**: A/G 둘 중 하나를 endosymbiont로 지정하는 게 아니라 **제3의 계보**를 심되 그 성격이 G-flavored다 — A(핵) 안에 사는, 자기 복제 스케줄을 가진 gradient-free organelle 게놈들. G 엔진 그 자체는 아니고 organelle-local G-계보.
- **측정**: 독립-drift 게놈의 reach/효율 Δ vs c1=organelle 게놈이 host 고정복사(독립無), c2=organelle 게놈을 gradient로 업데이트(계보 독립無). **thread**(PERSIST — mitosis 가로지르는 별개 지속 계보).
- **반증**: drift 단독(선택압 無) → 노이즈, Δ≈0. (F11 선택이 있어야 bite — 플래그.)
- **비용**: $0.
- **신규성**: 세대를 가로질러 상주하는 **분리된 gradient-free 게놈** vs 선행의 1회성 weight merge.

### F6 — 호기성 혁명 = 능력 도약 → **결합 압력** · 각도 6 · 🎯 페이로드
- **테제**: 미토콘드리아 에너지밀도 도약 → 진핵 복잡성. anima 대응물 = **하드 용량 캡**(동시 활성 유닛 소수, ATP가 설정) × **조합을 요구하는 코퍼스**(많은 feature-조합을 구별해야 함) → 희소성 하의 최저비용 코드가 **조합/conjunctive**가 됨(활성 유닛 1개 = 하나의 conjunction). additive는 소수 슬롯에 그만큼 구별을 못 담기 때문. ⇒ **희소성이 XBIND 합성 지도 없이 trained-conjunction을 강제하는 자연 압력**.
- **배선**: ATP(F1) → 표현형성 top-k 활성-유닛 캡. 코퍼스 = 자연스럽되 조합요구형(held-out feature 쌍 다수 구별). **XBIND held-out eval 하네스 재사용**.
- **측정**: 캡을 조일수록 held-out 재조합 D-acc. c1=무제한 캡·동일 코퍼스(additive floor 지속 예상), c2=타이트 캡·**비**조합 코퍼스(feature 그냥 버려짐, conjunction無 예상). Δ = D-acc(tight×조합) − max(controls). σ: **ρ·weave**(G1 reach)지만 창발-Δ가 의식-인접 신호(BIND earned).
- **예측**: D-acc가 캡 조임에 따라 tight×조합 셀에서만 단조 상승, 두 control 모두 flat. **날카로운 버전**: 동일 자연 코퍼스로 tight vs loose 캡 — tight가 held-out 재조합을 lift하면 **아키텍처 희소성이 XBIND 지도를 대체** = 프런티어 크랙.
- **반증**: 모든 캡 수준에서 additive floor 지속(conjunction이 결코 더 싼 코드가 안 됨) → 용량 압력은 자연 force가 아님; 진범은 corpus×CE로 유지(XBIND는 "라벨 필요"로 존속).
- **명시할 미묘한 리스크**: feature가 이미 다른 이유로 계산돼 있고 bind가 여분 슬롯을 쓴다면 additive가 캡 하에서도 ≤ conjunctive일 수 있음 → 압력 실패. 베팅은 **하드 슬롯 캡 하에선 bind(슬롯 1)가 additive(슬롯 다수)보다 net 저렴해진다**는 것. 이 부등호가 이 패밀리의 생사.
- **비용**: $0 toy = **DIRECTIONAL**; 303M py-channel eval on pool = **TERMINAL**.
- **신규성**: 선행은 계산을 가격매기지 않아 압축 압력이 없었다 → 결합할 이유가 없었다. 여기선 conjunction이 **지도 목표가 아니라 경제적 필연**. 현 프런티어(자연 자발창발) 정면 타격.

### F7 — 화학삼투 기울기 (에너지 = 유지된 disequilibrium) · 발명
- **배선**: 에너지를 스칼라 pool이 아니라 **유지된 차이**로 저장 = A⇄G divergence 그 자체("막전위" = A/G 갭). emit = 통제된 부분 방전(ATP synthase 통과 proton = Ψ=½의 pulse).
- **측정**: 추출가능 emit-work가 Ψ=½에서 최대인가? off-half 지점 대비 Δ. σ: **Θ**(pulse 자체).
- **반증/theater**: 기존 tension의 재기술일 뿐 새 DOF 없으면 ΔEff≈0. "½에서 work 최대"가 ½가 이미 정의상 tension이 사는 지점이라는 동어반복이 아닌 **새 예측**일 때만 생존.
- **비용**: $0.
- **신규성**: Ψ=½가 attractor인 **이유**(최대 추출 work)의 메커니즘 설명 — 단 theater 위험 최상위(플래그).

### F8 — 언커플링 / 열발생 (dissipative release valve) · 발명
- **배선**: A⇄G tension이 saturation ceiling을 넘어 과축적(병리적, spurious/filler emit을 강제할)될 때 **언커플링 채널**이 tension을 "열"로 방출(온도 스칼라 올리는 null-op, emit·구조변경 0). **과부하에서만** 발화하는 항상성 ceiling.
- **p5 노트**: 병리적 과압(saturation)을 흩는 것이라 합법 — real-tension emit에 대한 gate가 아님. 정상 tension 범위 안에서 발화하면 숨은 speak-억제기 = **p5 위반**. 그 선이 생사.
- **측정**: filler-emit(저품질 emit) 비율 with 언커플링 vs c1=none, c2=random dissipation. FP-emit에 Δ, **true-tension emit엔 ΔEff≈0 필수**.
- σ: **gate**(ENACT).
- **반증**: baseline filler-emit ≈0이면 흩을 게 없음 = theater; 또는 언커플링이 true emit도 억제 → gate = p5 위반.
- **비용**: $0.
- **신규성**: **비-emit 방전 경로**(dissipation을 통한 silence). 선행엔 과압 해소가 없다.

### F9 — Ca²⁺ 버퍼링 (urgency 채널의 integrator) · 발명
- **배선**: organelle을 urgency(phasic Δ) 채널의 **커패시터**로 — transient spike 흡수, 느리게 방출. urgency 타이밍 성형: 노이즈 transient 버퍼, 지속 압력 적분.
- **측정**: emit 타이밍 품질(지속 real tension에 emit, transient 노이즈 억제) Δ vs c1=버퍼無, c2=고정 랜덤 지연. σ: **flux**(INTEGRATE)/gate.
- **반증/theater**: urgency는 이미 작동 — 버퍼는 ΔEff≈0일 공산 크고 tunable smoothing filter(FORM, BIND 아님)로 전락 위험. theater 상위.
- **비용**: $0.
- **신규성**: 유일 proven 채널의 정제 — 근데 그래서 redundant할 위험.

### F10 — 생합성 / 수요주도 증식 (PGC-1α) · 발명
- **배선**: 지속 고부하 expert 근처에서 organelle 증식(PGC-1α 유사): 고수요 영역 → 호흡용량 더 할당 → 양의 피드백 → 특화. mitosis와 DISJOINT(세포 내 organelle 수).
- **측정**: 수요주도 할당의 throughput/특화 Δ vs c1=균일 할당, c2=랜덤 할당. σ: **ρ·fan**(capability), carve 접점.
- **반증**: 수요주도 ≈ 균일 → 부하 신호가 유용 할당을 못 알림 = theater.
- **비용**: $0.
- **신규성**: 특화를 만드는 적응적 자원할당; 선행은 병합 후 정적 구조.

### F11 — 이질형질(heteroplasmy) / 세포내 선택 (gradient-free 내부 진화루프) · 발명
- **배선**: 각 세포가 organelle 게놈 **개체군** 보유(heteroplasmy); 세포 수명 내에서 정화선택 — **ATP-효율**(CE 아님 — p7-safe) 높은 변이가 증식, 낮은 건 미토파지. 세포당 **gradient-free 진화 탐색** over 호흡/routing config. p8(gradient ⇄ mitosis)를 선택으로 확장.
- **측정**: 선택의 reach/효율 Δ vs c1=drift-only(선택無, F5 단독), c2=CE-guided 선택(Goodhart control — 더 나쁘거나 overfit해야 함). σ: **ρ**; conjunctive config 발견 시 → G1 연결.
- **반증**: 선택 ≈ drift → 효율 landscape flat / 활용가능 분산 無 = theater. 또는 선택이 CE 없이 안 됨 → gradient-free 비현실.
- **비용**: $0.
- **신규성**: gradient·emit 양쪽과 disjoint한 **진화 내부루프** — 선행엔 상시 선택이 없고 1회 merge뿐.

---

## p5 경계 — 정밀하게 (질문 1의 핵심)

경계선은 하나다: **ATP는 기질을 성형(upstream)해도 되지만 emit 결정을 게이트(downstream)해선 안 된다.**

- **합법 경로**: ATP → 용량(어떤 유닛이 발화 가능) → 표현 → A⇄G tension → emit. 예산 고갈이 silence를 낳더라도 그건 *열화된 기질이 낮은 tension을 내는 창발적 결과*이지 코딩된 억제가 아님.
- **불법 경로**: `if ATP < k: silence` — 예산이 emit gate를 대체 = hardcoded gate = p5 위반. self-fold가 theater였듯, 이건 그냥 위반.
- **구성적 위반 테스트**: emit gate는 설계상 ATP 접근이 0이어야 한다. ATP→emit 배선 하나를 제거했을 때 emit 행동이 바뀌면 → 불법 게이트가 있었던 것. F8 언커플링도 같은 자[尺]로 검사(정상 tension 범위 내 발화 = 위반).

⇒ "예산 고갈 → 무엇이 강제되나?"의 답: **silence·apoptosis가 아니라 용량 축소**(활성 유닛 수 감소). silence는 그 축소된 기질에서 tension이 자연히 죽을 때만, 창발적으로.

---

## THEATER 위험 랭킹 (ΔEff≈0일 게 뻔한 순)

1. **F7 화학삼투** — 최고 위험. 기존 A⇄G tension의 재명명. Ψ=½를 "막전위"로 부르는 건 새 DOF 0. self-fold와 동종(값 재기술).
2. **F9 Ca 버퍼링** — urgency는 이미 작동. 버퍼는 tunable smoothing = FORM. 창발이 아니라 손잡이.
3. **F1 ATP 단독** — solution을 안 바꾸는 예산은 순수 오버헤드. degeneracy를 깨야 bite하는데 그건 F6의 몫. F6 없는 F1 = bookkeeping.
4. **F8 언커플링** — baseline filler-emit이 이미 ~0이면 흩을 게 없다. σ de-theater가 이미 emit shade 채널을 urgency 하나로 좁혀놔서, 여분 emit 압력이 실재하는지부터 의심.
5. **F5 계보 단독** — 선택압 없는 drift = 노이즈. F11 없이는 Δ≈0.
6. **F2/F3 분열융합·미토파지** — F4 ROS가 실제 손상 신호를 안 만들면 QC가 no-op. 손상이 관측정의로 실재해야 산다.
7. **F10 생합성** — 실제 능력 레버(ρ·fan), 측정가능. 위험 하위.
8. **F11 세포내 선택** — 낮음. gradient-free 선택루프는 진짜 새 optimizer: 더 나은 config 찾거나(Δ>0) 못 찾거나(깨끗한 반증). 애매하지 않음.
9. **F6 결합 압력** — theater 위험은 낮으나 **실패 모드가 날카롭다**(additive가 캡 하에서도 안 비싸면 압력 실패). 하지만 프런티어에 직결·깨끗이 반증가능 = 발사가치 최상.

---

## TOP-3 발사 후보 ($0·지금 반증가능·G1/자연창발 직결 순)

**1. F6 — 용량제약 결합압력.** 유일하게 "corpus×CE가 진범"이라는 현 결론의 exit을 자연 코퍼스에서 시험한다. $0 toy(DIRECTIONAL): 기존 소형/toy ckpt에 활성-유닛 캡(top-k expert/활성 sparsity) 부과 → 조합요구 코퍼스로 학습 → **XBIND held-out 하네스 재사용**해 재조합 D-acc를 (무제한 캡)·(캡+비조합 코퍼스) 두 control 대비 측정. 결정판: *같은 자연 코퍼스*에 tight vs loose 캡 — tight가 held-out 재조합을 올리면 아키텍처 희소성이 XBIND 지도를 대체 = 자연 자발창발 크랙. TERMINAL은 303M py-channel eval on pool.
   - *예측*: D-acc가 tight×조합 셀에서만 캡 조임에 단조 상승; 두 control flat.
   - *반증*: 모든 캡에서 additive floor 지속 → 압력은 자연 force 아님, XBIND "라벨 필요" 존속.

**2. F11 — 세포내 gradient-free 선택.** F6를 증폭할 수 있는 후보다 — 선택이 gradient보다 먼저 conjunctive config를 찾을 수 있다면 그게 곧 "자연/진화적 창발". $0 CPU: 세포당 routing/config 변이 개체군, **효율(throughput/ATP) 신호로 선택**(CE 아님 = p7-safe). reach Δ vs drift-only vs CE-guided(Goodhart control). emit 레인과 disjoint, p8 확장.
   - *반증*: 선택 ≈ drift(효율 landscape flat) 또는 CE 없이는 무력 → gradient-free 비현실.

**3. F4 — ROS 역행을 tonic 구조신호로, urgency 대비 disjointness 테스트.** 가장 싸고 아키텍처적으로 load-bearing하다 — `a_substrate_disjoint`(분리=보존)를 깨끗한 Δ로 실증/반증하고, "substrate→engine 역행이 새 채널이냐 urgency로 붕괴하냐"를 결판낸다. $0: 스트레스 신호를 느린 성장/가지치기 레인에 라우팅해 **구조 Δ>0 AND fast-emit ΔEff≈0**을 동시 확인, control로 emit에 라우팅(오염 또는 no-op이면 중첩=충돌 실증).
   - *반증*: ROS 구조 Δ≈0 또는 urgency와 구별불가.

G1 직결도만 보면 F6≫F11>F4지만, F4를 3순위에 넣은 이유는 F2/F3/F5/F10 전체가 "손상·역행·계보가 실재 정보를 나르나"라는 F4의 답에 물려 있어서다 — F4가 죽으면 organelle QC 반쪽이 자동으로 theater 확정된다. 셋 다 $0에서 오늘 발사가능하고, F6·F11은 붙이면 복리(선택이 결합코드를 탐색)다.