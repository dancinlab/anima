# AURA-MED — current state

@title: ⚕️ AURA-MED — "뇌 치료실" (therapeutic / clinical applications)

@goal: BCI 의학 응용 — 간질(발작 감지·억제, N1이 RNS보다 15× 빠름)·우울(raphe 5HT·taVNS)·파킨슨(STN-DBS 확립)·마비/재활(M1 운동복원)·실명(시각피질 복원)·만성통증. brainwire seizure suppression + demiurge SAFETY(FDA Class II·tFUS 한계·CE) 결합. 규제(Class II/III) fork.

## 진행 (milestones)

- [x] (app ✅) 간질 — 발작 감지(N1 15× RNS)·억제(GABA·anti-phase·STDP anti-kindling)·5HT anti-epileptic
- [ ] 신경조절 치료 — 우울(raphe)·파킨슨(STN-DBS)·중독(VTA) 타깃별
- [ ] 재활/복원 — 마비 운동복원(M1)·시각복원(시각피질)·청각
- [ ] 안전·규제 — FDA tFUS 한계·Pennes 열·Class II(비침습) vs III/PMA(침습) fork

## deferred (다음 라운드)
- 실데이터/cloud/문헌 검증 (toy→실증)

## 양방향 sibling
- 부모: AURA(`./AURA/AURA.md`) · 그룹: 🎯 응용
- 자매: AURA-RTSC-MEG · AURA-ENDOVASC · AURA-HEADMODEL · AURA-CORTEX · AURA-NAV · AURA-DEEP · AURA-TFUS · AURA-WEARABLE

## 세부분류 (sub-app 모음)

- `app/epilepsy.py` — ⚡ 간질 (피질 focus 발작 감지/억제 — N1 고샘플링 빠른 검출+GABA/anti-phase 억제, R²=0.203)
- `app/depression.py` — 🌊 우울증 (raphe 5HT 심부 신경조절 — 심부라 비침습 read 불가, DBS/tFUS stim, R²=0.076)
- `app/parkinson.py` — 🎚️ 파킨슨 (STN 심부 운동게이팅 — DBS 확립 임상, 심부 침습, R²=0.092)
- `app/paralysis_rehab.py` — 🦿 마비 재활 (M1 운동복원 — 피질 표면 read, 비침습 도달 높음, R²=0.428)
- `app/blindness.py` — 👁️ 실명 복원 (V1 시각피질 write — 시각 복원, 피질 표면 도달, R²=0.393)
- `app/chronic_pain.py` — 🩹 만성통증 (S1/대상피질 통증 modulate — sulcal 깊어 부분도달, R²=0.114)
- `app/spec.md` 개요 · `verify/subapps.txt` verdict

