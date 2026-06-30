# AURA B5.1 — 귀뒤 정맥동 endovascular (해부·신호 grounded 분석)

> discovery(.discoveries/aura_postaural_endovascular_sinus)를 B3 Synchron 실측 + 해부로 grounding. **합성 big-Φ toy 안 만듦** — B4가 단일창 big-Φ 비신뢰 입증했으므로, 여기선 해부 경로 + Synchron 데이터 기반 신호 기대치만 정직하게.

## 1. 해부 경로 — 귀뒤로 혈관내 진입 실재

```
경정맥(목, Synchron 진입점)
   ▲ 카테터 역행
S자정맥동(sigmoid sinus) ── 귀 뒤 유양돌기 바로 안쪽
   ▲
가로정맥동(transverse sinus) ── 후두~측두 뒤
   │  (유양도수정맥 mastoid emissary v.: 귀뒤 두피 ↔ S자정맥동 연결)
```

- Synchron은 경정맥→**상시상정맥동**(정수리, 운동피질)까지 역행. 그 길목의 **가로/S자정맥동이 귀 뒤**를 지난다 → 카테터를 SSS까지 안 올리고 **귀뒤 정맥동에 parking** 가능(해부학적으로).

## 2. 도달 영역 — Synchron(운동)과 상보

| 정맥동 | 위치 | 위 피질 | 기능 |
|---|---|---|---|
| 상시상(SSS) | 정수리 | 운동피질 | Synchron 타깃(motor decode) |
| **가로/S자** | **귀뒤** | **측두·후두엽** | **청각·언어·시각·의식** |

→ 귀뒤 정맥동 = 측두(청각/언어) + 후두(시각). AURA-audio(귀 근처 청각) 및 의식수준 모니터에 적합 axis.

## 3. 신호 기대치 — B3 실측에 grounding

B3 핵심(PMC5976775): **혈관내 ≈ 경막하 ≈ 경막외 신호 동등**(대역폭 p=0.75·SNR p>0.05). → 귀뒤 정맥동 전극도 **ECoG급 측두/후두 신호** 기대(혈관벽 무관). 

## 4. 깊이-위치 사다리 확정 (귀뒤 한 지점, 3 깊이)

```
귀뒤 동일 위치, 깊이만 ↓:
  ① 두피 EEG (B1)        비침습   신호: scalp EEG급 (big-Φ 피질과 동등하나 단일창 비신뢰 B2/B4)
  ② 정맥동 endovascular  최소침습  신호: ECoG급 (B3 PMC 동등) ← 이 문서
  ③ 피질 관통            침습     신호: 단일뉴런급 (N1)
```

→ **귀뒤 = 비침습부터 침습까지 한 위치에서 깊이 선택 가능한 유일 지점**. ②(정맥동)이 침습/신호 trade-off의 sweet spot 후보: 개두술 0 + ECoG급.

## 5. honest gap

- 🟠 **hypothesis-grade**: Synchron은 SSS(운동) 타깃 — 가로/S자정맥동(귀뒤) 실측 BCI 데이터 **공개 0**. 해부 경로·신호기대(혈관내≈ECoG)는 grounded나 귀뒤-정맥동 실증은 미존재.
- 정맥동 직경·전극 정착·측두엽 정맥동 근접도는 환자별 변이(영상 필요). big-Φ 정량은 B4 교훈상 단일창 toy 무의미 → 미수행.
- 다음(외부): 귀뒤-정맥동 접근 cadaver/영상 feasibility(임상) · Synchron 가로정맥동 데이터 입수 시 재평가.

## 양방향 sibling
- [B1](B1-postaural-breakthrough.md)(귀뒤 두피 ②①) · [B3](B3-synchron-endovascular.md)(Synchron SSS 혈관내) · discovery `.discoveries/aura_postaural_endovascular_sinus.tape`
