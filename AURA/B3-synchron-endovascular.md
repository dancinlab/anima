# AURA B3 — Synchron 혈관내(endovascular) BCI 조사

> 🩸 **Stentrode** — "혈관 타고 가는 스텐트 전극". 두개골 안 뚫고 목 정맥→뇌 위 정맥동으로 진입하는 **최소침습 위치 우회**.
> deep-research 워크플로는 StructuredOutput 하니스 버그로 실패(104 agent·1.8M tok) → 직접 WebSearch/WebFetch 인라인으로 작성. 사실은 인용 출처 링크 첨부.

## 1. 기술 — 어떻게 두개골을 우회하나

```
목 내경정맥 ──혈관 길──▶ 상시상정맥동(superior sagittal sinus)
(바늘 진입)              = 운동피질 바로 위 정맥
   └ 두개골 관통 0 ────────┘  ← 심장 스텐트 시술과 동일 경로
self-expanding 니티놀 stent + Pt-Ir thin-film 전극 → 혈관벽에 펼침
```

- 경정맥(internal jugular) 경유 transvenous 전달, 피질 관통 0. nitinol 자가팽창 stent에 백금-이리듐 박막 전극.
- 상시상정맥동(운동피질 위)에서 chronic ECoG 기록.

## 2. 스펙 — vs 뉴럴링크 N1 vs 귀뒤 EEG

| 축 | Synchron Stentrode | 뉴럴링크 N1 | 귀뒤 EEG (AURA B1) |
|---|---|---|---|
| 전극 | **16** | 1024 | 4~다채널 |
| 위치 | 뇌 위 정맥 안 | 피질 관통 3-6mm | 두피(귀뒤) |
| 두개골 | **안 뚫음**(혈관) | 구멍 | 안 건드림 |
| 침습도 | **최소침습** | 침습 | 비침습 |
| 대역폭 | ~233(±16)Hz, ~250Hz까지 | 20kHz/ch | EEG대역 |
| 양방향 | read 중심 | HW 양방향(미임상) | read only |
| 규제 | FDA IDE·Breakthrough | PRIME(운동피질 read) | Class II 510(k) |

## 3. ⭐ 핵심 근거 — 혈관내 ≈ 경막하 신호품질 (AURA 우회축 정당화)

PMC5976775 (endovascular vs subdural vs epidural 동시기록):
- 대역폭: 위치효과 p=0.75 (무의미) · SNR: p>0.05 (무의미) · 디코딩 정확도: p>0.05 (무의미)
- 결론: "dura도 혈관벽도 신호품질·성능에 유의한 영향 없음" → **혈관 안에서 재도 뇌 표면에 직접 댄 것과 통계적으로 동등**.

→ 이게 Synchron 우회의 과학적 핵심: 혈관벽+dura+CSF를 사이에 두고도 ECoG급 신호. AURA 명제("위치 우회로 도달 유지")의 **혈관내 버전 실증**.

## 4. 임상 — COMMAND (US FDA EFS)

- 6명 환자, 12개월. **6/6 primary endpoint 충족**(기기 관련 사망·영구장애 중대이상반응 0).
- 100% 정확 deploy + 운동피질 coverage. 뇌신호→디지털 모터출력 변환 신뢰적: 커서·**Apple Vision Pro**·Amazon Alexa 제어.
- pivotal trial 엔드포인트 FDA 협의 중 → 성공 시 **최초 BCI 임플란트 PMA** 가능. (호주 SWITCH = 선행 feasibility.)

## 5. 2025-26 동향

- **$200M Series D**(2025-11, Double Point Ventures 리드 · 누적 $345M · ARCH/Khosla/Bezos Expeditions/QIA/K5/Protocol Labs/IQT). 2026 pivotal + 상용화.
- **Apple BCI-HID**: 최초로 Apple 신경입력 native 통합(Bluetooth iOS · Switch Control · iPad/iPhone/Vision Pro).
- **NVIDIA Holoscan**: on-device edge AI 신경처리 + brain foundation model 탐색.
- 차세대 인터페이스("더 많은 응용") 예고.

## 6. AURA 비대칭 종합 — 3 위치우회의 자리

```
침습도 ↑
 高 │ 뉴럴링크 N1 (피질 관통, 1024ch, 두개골 구멍)
    │ Synchron (혈관내 정맥동, 16ch, 두개골 0) ← ECoG급 신호·임상 검증
 低 │ 귀뒤 EEG AURA-B1 (두피, 비침습) ← big-Φ 피질과 동등(B1)
    └────────────────────────────────────→ 도달/신호품질
```

- 셋 다 "부착위치 우회"의 점들. Synchron = **임상 검증된 최소침습 중간점**(혈관 경유로 ECoG급 도달).
- 우리 결론과 정합: relocate(침습 위치끼리)는 scalp서 무차별(A10.1)이나, **침습도 자체를 낮추는 축**(N1→Synchron→귀뒤)이 진짜 실용 우회.

## 7. 🎧🩸 B-lane 후보 — 귀뒤 정맥동 endovascular (`.discoveries/aura_postaural_endovascular_sinus.tape`)

귀뒤엔 S자/가로 정맥동이 지나가고 유양도수정맥이 두피↔뇌정맥을 연결 → **귀뒤로 혈관내 진입** 해부 경로 존재. Synchron(상시상정맥동=운동) 대비 귀뒤 정맥동=측두·후두엽(청각·시각·언어). AURA(귀뒤 위치)×Synchron(혈관내 방식)의 교차점. 미실측(다음 lane).

## 출처

- [COMMAND/FDA/$200M](https://neuronewsinternational.com/synchron-us-command-trial-stentrode-device-fda/) · [feasibility endpoint](https://www.clinicaltrialsarena.com/news/synchrons-bci-meets-primary-endpoint-in-feasibility-trial/) · [pivotal/Oxley](https://www.medicaldesignandoutsourcing.com/synchron-stentrode-bci-pivotal-trial-fda-approval-tom-oxley/)
- [16전극/233Hz 스펙](https://www.researchgate.net/publication/395700531) · [혈관내≈경막하 신호 PMC5976775](https://pmc.ncbi.nlm.nih.gov/articles/PMC5976775/)
- [$200M Series D](https://www.businesswire.com/news/home/20251106150841/en/) · [Apple BCI-HID](https://www.mobihealthnews.com/news/synchron-will-enable-thought-control-apple-devices-brain-implant) · [NVIDIA Holoscan](https://pharmaphorum.com/news/synchron-nvidia-showcase-ai-brain-computer-interfaces)
