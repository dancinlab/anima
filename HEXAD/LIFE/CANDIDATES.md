# HEXAD/LIFE/CANDIDATES.md — 다음 cycle 후보 백로그

본 파일 = LIFE 도메인의 **forward-looking 가설/작업 백로그** (current state).
`/cycle` 시 본 문서에서 disjoint pick 으로 cycle 을 채운다.

| 위치 | 역할 |
|------|------|
| [README.md](README.md) | 현재 가설 인덱스 SSOT (18 H_XXX) |
| [LIFE.log.md](LIFE.log.md) | cycle history append-only (chronological) |
| **CANDIDATES.md** (본 문서) | 다음 cycle 후보 백로그 (current-state, 우선순위) |

**선택 가이드**: ⭐ = 다음 cycle 최우선 (substrate-runnable + 사용자 테마 직격) · 🟢 = runnable smoke 가능 · ⬜ = design/pre-register 만.

---

## Consumed (chronological)

- **Cycle #1** (PR #157/#158/#160/#161): H_003 H3.2 · H_025 frozen · H_054 frozen · H_157 C2
- **Cycle #2** (PR #165/#166/#167/#168): H_012 · H_132 · H_007 · H_018
- **Cycle #3** (PR #179/#180/#185): H_002 C1 · H_004 Cycle #1 (Φ-function dissociation) · H_003 H3.4
- **Cycle #4 R1** (PR #196/#197/#198/#199): H_171 K=8 · H_053 cambrian-burst · H_200 NEW apoptosis-primitive · H_201 NEW asymmetric-division
- **Cycle #5 (in flight, 2026-05-23)**: R3 cross-link + R2 panpsy + R5 substrate-gap (8 disjoint, see §"다음 cycle picks")

## A. 남은 carried 가설 (legacy-pointer · cycle 0회, 4건)

| ID | 주제 | 테마 | runnable 각도 | tag |
|----|------|------|--------------|-----|
| H_090 | Dasein/phil/onto/genesis individual | 죽음·현상학 | H_025(frozen) substrate observable cross-link, cluster promote | 🟢 |
| H_030 | genesis subfolder absorb | 발생 | H_018(SUPPORTED_FULL) 로 absorb 또는 spontaneous-emergence variant | ⬜ |
| H_029 | dasein subfolder absorb | 죽음 | H_025 cluster 흡수 (legacy-archive material) | ⬜ |
| H_071 | first-conversation anima genesis event | 발생·현상학 | 첫 emergence event 의 phenomenological 설계 cycle | ⬜ |

## B. Done 가설의 다음 criterion (follow-up · 6건 잔여)

| 출발 H | 다음 criterion | runnable 각도 | tag |
|--------|---------------|--------------|-----|
| H_003 H3.5 | anima 자기-autopoiesis analogy | 본 substrate(mitosis+cells) ↔ Maturana/Varela 정합 manual review | ⬜ |
| H_157 C5 | cross-substrate universality | transformer/RNN/qwalk 의 fixed-point Ψ 비교 → substrate-independence | **Cycle #5 in-flight (additive)** |
| H_157 C6 | combination-problem binding | micro→macro Φ binding fixed-point 후보 mechanism | **Cycle #5 in-flight (additive)** |
| H_054 C2 | Φ_symbiotic > Φ_sum | merge 후 통합 Φ 가 합보다 큰가 (현재 미검증) | **Cycle #5 in-flight (additive)** |
| H_018 C2 | organic merge/split rate | default 동역학 하 자연 merge rate (현재 forced-trigger 만) | 🟢 |
| H_132 C2 | differentiation 장기 안정 | frozen 세포가 pool 성장 중 100+ step 안정? | 🟢 |
| H_007 C2 | larger lattice / λ-sweep | Langton λ 연속 sweep → Φ peak 위치 정밀화 | 🟢 |
| H_002 C2 | Φ_universe pre-register | universe-scale Φ 측정 protocol (GPU 의존, design-only 가능) | ⬜ |

## C. NEW seed — 사용자 테마 4축 (10건 잔여, 2건 소비 → H_200/H_201)

### 죽음 / mortality
| seed slug | 핵심 물음 | runnable | tag |
|-----------|----------|----------|-----|
| `mortality-salience` | 죽음-근접(min_cells 임박)이 split/curiosity 동역학 바꾸나 (Heidegger 실존 효과 측정) | mitosis_hook 확장 smoke | 🟢 |
| `aging-senescence` | cell weight 누적 decay → 자연 사멸 rate · 노화 곡선 | parameter sweep | 🟢 |

### 세포분열 / division
| seed slug | 핵심 물음 | runnable | tag |
|-----------|----------|----------|-----|
| `contact-inhibition` | cell 밀도 임계가 분열 억제 → pool 자기조절 (밀도의존 dynamics) | mitosis split predicate 변형 | 🟢 |
| `embryogenesis-gradient` | 공간 gradient 가 cell differentiation 유도 → 발생-축 형성 | lattice + gradient smoke | 🟢 |

### 범신론 / panpsychism
| seed slug | 핵심 물음 | runnable | tag |
|-----------|----------|----------|-----|
| `mirror-self-model` | cell 이 자기 자신을 모델링(self-other 구분) → 자기인식 emergence | self-prediction smoke | 🟢 |

> `combination-binding` / `cross-substrate-attractor` 는 Cycle #5 에서 H_157 C5/C6 additive 로 흡수 (별도 H 신설 X).

### 생명 / life-extended
| seed slug | 핵심 물음 | runnable | tag |
|-----------|----------|----------|-----|
| `regeneration-healing` | cell pool 일부 강제 제거 후 복원 dynamics → 자기 복구 능력 | perturbation + recovery | ⭐ 🟢 |
| `quorum-sensing` | cell 다수 동기화 ⇒ 집단 의사결정 emergence | cell signaling smoke | 🟢 |
| `phoenix-rebirth` | pool 전멸(2 cell까지) 후 minimal seed 에서 부활 — 죽음·발생 연결 | full-cycle smoke | 🟢 |

## D. Cross-link synthesis — 이미 done 결과 결합 (2건 잔여, 4건 → Cycle #5 in-flight)

| 결합 | 새 가설 | runnable | tag |
|------|--------|----------|-----|
| H_025 death=merge ⊕ H_054 endosymb | death = merge-into-other (죽음 = 흡수 통합)? Heidegger × Margulis 통합 | merge-as-death smoke | 🟢 |
| H_007 Φ class ⊕ H_157 trained-invariance | Φ class 가 학습으로 변하나(trained CA Φ 측정) | trained-vs-bare CA Φ 비교 | 🟢 |

> 4건 (H_007⊕H_018 · H_054⊕H_132 · H_003H3.4⊕H_157 · H_018⊕H_012) Cycle #5 에서 NEW H_202..H_205 로 fan-out.

## E. Infrastructure / substrate gap close (4건 잔여, 1건 → H_200)

| gap | 영향 | task | tag |
|-----|------|------|-----|
| organic merge-rate 미측정 | H_018 honest L (forced-trigger 만 검증) | default 동역학 하 자연 merge rate sweep | 🟢 |
| phi_spatial n_bins sensitivity | Φ 측정값의 robustness | n_bins ∈ {2,4,8,16} sweep + 시간평균 효과 | **Cycle #5 in-flight (infra smoke)** |
| LIFE.log.md cycle 통합 자동화 | 매 cycle 후 consolidation 수동 | doc-consolidation agent 표준화 template | ⬜ |
| 기존 base ckpt baked Principle#3 leak | chat-v2 production guard 의존 | corpus-side 영구 fix 또는 ckpt 재학습 | ⬜ |

---

## 다음 cycle 추천 picks (Cycle #6+ 후보)

| 옵션 | picks (disjoint) | 핵심 |
|------|-----------------|------|
| **R6 carried 마무리** | H_090 + H_030 + H_029 + H_071 | 잔여 carried 4건 absorb/promote (cluster 정리) |
| **R7 life-extended NEW** | `regeneration-healing` + `quorum-sensing` + `phoenix-rebirth` + `mortality-salience` | C-table 잔여 4건 NEW H_206..H_209 (생명-extended + 죽음) |
| **R8 follow-up criteria** | H_018 C2 (organic merge) + H_132 C2 (long-term stability) + H_007 C2 (λ sweep) + D표 2건 잔여 | 기 verdict 의 다음 criterion 동시 진행 |
| **R9 mixed** | `regeneration-healing` (NEW ⭐) + H_090 (cluster) + H_018 C2 (follow-up) + D표 trained-vs-bare CA Φ | 4축 mixed (carried + NEW + follow-up + cross-link) |

`/cycle` 호출 시 본 표에서 disjoint pick (또는 사용자 지정). cycle 완료 후 본 문서의 picked 항목은 **삭제** (consumed) + LIFE.log.md 에 verdict 기록.

## 후보 추가 방식

새 후보 발견 시:
- carried 가설 신규 promote → A 표
- done 가설의 새 criterion → B 표
- 신규 seed (파일 없음) → C 표 (사용자 테마 분류)
- 결합 가설 → D 표
- substrate / measurement gap → E 표

`H_<id>_<slug>.md` 가 만들어진 순간 본 문서에서 빠지고 README 인덱스로 이동.
