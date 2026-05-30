# AURA-HEADMODEL — current state

@title: 🗺️ AURA-HEADMODEL — "진짜 머리 지도" (real head-model lead-field validation)

@goal: MNE/OpenMEEG 실 두상 lead-field로 C5~C17 toy(가우시안-blur)의 깊이감쇠·전극포화를 실측 검증 — C10이 "전극포화는 가우시안 전용 인공물"임을 보였고 C14에서 real head-model이 결정적이라 판정. 모든 C축 toy의 ground-truth 검증 도메인.

## 진행 (milestones)

- [x] (app ✅) MNE/OpenMEEG 3-shell·FEM lead-field 구축 — 가우시안-blur 대체
- [x] C10 strawman 검증 — **C10 SUPPORTED**: 3-shell 구체 lead-field(Ary1981, $0 numpy)서 전극 미포화(R² 0.19→0.40 계속 상승), 가우시안만 평탄 → "전극포화=가우시안 인공물" 확증. 깊이 방향 일치(가파름 과장 의심), 두개골비 1/20~1/80 평탄. → `SPHERE-VALIDATION.md`·`verify/sphere_leadfield.txt`
- [ ] C15 깊이 벽 실측 — 실 두상서 피질→심부 복원율 감쇠곡선
- [ ] C11 현실 prior 복원율 — 실 MRI 해부 prior 적용 (oracle 0.80 vs 현실)

## deferred (다음 라운드)
- 실데이터/cloud/문헌 검증 (toy→실증)

## 양방향 sibling
- 부모: AURA(`./AURA/AURA.md`) · 그룹: 📡 모달리티
- 자매: AURA-RTSC-MEG · AURA-ENDOVASC · AURA-CORTEX · AURA-NAV · AURA-DEEP · AURA-TFUS · AURA-WEARABLE · AURA-MED

## 세부분류 (app 세부트리)

- `app/spec.md` — 앱 명세(일반인+기술)
- `app/leadfield_validator.py` — 실동작 toy (검증됨)
- `verify/leadfield_validator.txt` — verdict
- 다음: real head-model 검증 · hexa-native 포팅 · 실데이터
