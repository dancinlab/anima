# AURA-MED — current state

@title: ⚕️ AURA-MED — "뇌 치료실" (therapeutic / clinical applications)

@goal: BCI 의학 응용 — 간질(발작 감지·억제, N1이 RNS보다 15× 빠름)·우울(raphe 5HT·taVNS)·파킨슨(STN-DBS 확립)·마비/재활(M1 운동복원)·실명(시각피질 복원)·만성통증. brainwire seizure suppression + demiurge SAFETY(FDA Class II·tFUS 한계·CE) 결합. 규제(Class II/III) fork.

## 진행 (milestones)

- [x] (app ✅) 간질 — 발작 감지(N1 15× RNS)·억제(GABA·anti-phase·STDP anti-kindling)·5HT anti-epileptic
- [ ] 신경조절 치료 — 우울(raphe)·파킨슨(STN-DBS)·중독(VTA) 타깃별
- [ ] 재활/복원 — 마비 운동복원(M1)·시각복원(시각피질)·청각
- [ ] 안전·규제 — FDA tFUS 한계·Pennes 열·Class II(비침습) vs III/PMA(침습) fork
- [x] 실 임상 outcome 문헌 grounding — 6 질환 × [toy R² | 실 임상 outcome+출처 | 침습tier] → [CLINICAL-GROUNDING.md](./CLINICAL-GROUNDING.md) (toy↔실임상 modality 갭 정직 표기)

## deferred (다음 라운드)
- 실데이터/cloud 검증 (toy→실증) — ✅ 문헌 grounding은 CLINICAL-GROUNDING.md 에서 완료

## 양방향 sibling
- 부모: AURA(`./AURA/AURA.md`) · 그룹: 🎯 응용
- 자매: AURA-RTSC-MEG · AURA-ENDOVASC · AURA-HEADMODEL · AURA-CORTEX · AURA-NAV · AURA-DEEP · AURA-TFUS · AURA-WEARABLE

## 세부분류 (sub-app 모음)

> 각 줄: toy R²(비침습 도달 proxy) + **실 임상 현황**(침습 outcome+출처) — 상세·출처는 [CLINICAL-GROUNDING.md](./CLINICAL-GROUNDING.md). ⚠ toy(비침습)와 실임상(침습) modality 갭 주의.

- `app/epilepsy.py` — ⚡ 간질 (피질 focus 발작 감지/억제, R²=0.203 | **실임상: RNS System 9년 median 발작 75%↓·FDA승인, 침습III** | N1 15× RNS=⚠미확증)
- `app/depression.py` — 🌊 우울증 (raphe 5HT 심부 신경조절, R²=0.076 | **실임상: SCC-DBS TRD response ≥50% 2–8년 유지, 침습III**)
- `app/parkinson.py` — 🎚️ 파킨슨 (STN 심부 운동게이팅, R²=0.092 | **실임상: STN-DBS motor UPDRS 25–41%↑·표준치료, 침습III**)
- `app/paralysis_rehab.py` — 🦿 마비 재활 (M1 운동복원, R²=0.428 | **실임상: BrainGate Utah-array 커서/로봇팔 제어·17년 안전, feasibility 침습III**)
- `app/blindness.py` — 👁️ 실명 복원 (V1 시각피질 write, R²=0.393 | **실임상: Orion 피질보철 5/5 위치탐지·4/5 방향식별, early-feasibility 침습III**)
- `app/chronic_pain.py` — 🩹 만성통증 (S1/대상피질 modulate, R²=0.114 | **실임상: MCS/DBS 신경병성통증 장기 responder ~39%·완화 38%, 침습II–III**)
- `app/spec.md` 개요 · `verify/subapps.txt` verdict · [CLINICAL-GROUNDING.md](./CLINICAL-GROUNDING.md) 실 임상 문헌 grounding

