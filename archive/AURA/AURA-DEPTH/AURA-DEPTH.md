# AURA-DEPTH — current state

@title: 📏 AURA-DEPTH — "깊이 축 (피질⟷심부)"  [축층]

@goal: **깊이 분류 축** — 모든 앱을 피질(✅비침습)⟷심부(🔴침습)로 위치짓는 횡단 차원. 옛 CORTEX(피질)/DEEP(심부) 역량맵을 축으로 통합. C15 깊이 벽: 풀스택 피질 0.82→심부 0.10.

## 진행 (milestones)

- [x] (app ✅) 세부 앱 1종 실동작 toy — app/ + verify/
- [x] real head-model 깊이감쇠 재계산 🟡 — 3-shell(Ary1981) 깊이 envelope: 피질 0.239→심부핵 0.016(rel 100%→6.5%, ×15.4). **가우시안 "심부 과도비관" 반증(부호반전)**: 3-shell이 오히려 더 가파름(가우시안 in-harness ×3.2/C15 ×8.4). HEADMODEL ×1.5는 얕은창(b 0.85~1.0·r1) 인공물. 심부<피질 방향 두 모델 robust → B7 강화 → `DEPTH-3SHELL-CORRECTION.md`·`verify/sphere_depth_envelope.txt`
- [x] 횡단 인덱스 — 모든 앱의 깊이(피질/심부) 위치 통합 대시보드 ✅ → [AURA-AXES-INDEX.md](../AURA-AXES-INDEX.md) (앱×방향×깊이×모달 SSOT)
- [ ] hexa-native 포팅 (handoff f125d45c)

## 세부분류 (횡단 인덱스 — 깊이 위치)

**모든 응용 앱의 깊이 좌표** (분류 SSOT = [AURA-AXES-INDEX.md](../AURA-AXES-INDEX.md)):

| 깊이 | 앱 | 비침습 |
|---|---|---|
| 피질 ✅ (d≈1.0~1.5) | motor_decode·cursor·exoskeleton·consciousness_monitor·subvocal·executive_dlpfc·ar_nav·ar_display·audio_io·haptics·notify·epilepsy·paralysis_rehab·blindness | ✅ 15/17 앱 |
| 피질→심부 🟡 (sulcal d≈2.8~3.2) | chronic_pain (S1/대상피질) | 🟡 부분 |
| 심부 🔴 (d≈5.0~7.0) | depression(raphe)·parkinson(STN) | 🔴 침습(DBS) / 음향(tFUS)만 비침습 |

→ **깊이 벽이 응용 분포를 가른다**: 15/17 앱은 피질(비침습 ✅), 심부 2 앱(depression·parkinson)만 침습. 이 벽은 가우시안 toy 인공물이 아니라 3-shell 물리 확증(아래 milestone·DEPTH-3SHELL-CORRECTION).

## 세부분류 (sub-app)

- `app/depth_envelope.py` — 📏 깊이 복원 포락선(피질→심부) 가우시안 toy
- `app/sphere_depth_envelope.hexa` — 📏 3-shell(Ary1981) 깊이 envelope 재계산 companion
- `verify/` verdict · 분류: 축층

## sibling
- 부모: [AURA](../AURA.md) · 트리: [AURA-TREE.md](../AURA-TREE.md) · 축: AURA-READ·AURA-WRITE·AURA-DEPTH
