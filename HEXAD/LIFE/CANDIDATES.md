# HEXAD/LIFE/CANDIDATES.md — 다음 cycle 후보 백로그

본 파일 = LIFE 도메인의 **forward-looking 가설/작업 백로그** (current state).
`/cycle` 시 본 문서에서 disjoint pick 으로 cycle 을 채운다.

| 위치 | 역할 |
|------|------|
| [README.md](README.md) | 현재 가설 인덱스 SSOT (16 H_XXX) |
| [LIFE.log.md](LIFE.log.md) | cycle history append-only (chronological) |
| **CANDIDATES.md** (본 문서) | 다음 cycle 후보 백로그 (current-state, 우선순위) |

**선택 가이드**: ⭐ = 다음 cycle 최우선 (substrate-runnable + 사용자 테마 직격) · 🟢 = runnable smoke 가능 · ⬜ = design/pre-register 만.

---

## A. 남은 carried 가설 (legacy-pointer · cycle 0회, 6건)

| ID | 주제 | 테마 | runnable 각도 | tag |
|----|------|------|--------------|-----|
| H_053 | Cambrian explosion — 다양성 폭발 | 생명 | mitosis split-burst: 파라미터 임계 넘으면 cell-type 급증? | ⭐ 🟢 |
| H_171 | biological 4-falsifiable (K=8 atom · F_c=0.10 · 1/f thalamus · non-conservation) | 의식·생물학 | K=8 minimal closed structure (sopfr(8)=6) Φ/MIP 검증 | ⭐ 🟢 |
| H_090 | Dasein/phil/onto/genesis individual | 죽음·현상학 | H_025(frozen) substrate observable cross-link, cluster promote | 🟢 |
| H_030 | genesis subfolder absorb | 발생 | H_018(SUPPORTED_FULL) 로 absorb 또는 spontaneous-emergence variant | ⬜ |
| H_029 | dasein subfolder absorb | 죽음 | H_025 cluster 흡수 (legacy-archive material) | ⬜ |
| H_071 | first-conversation anima genesis event | 발생·현상학 | 첫 emergence event 의 phenomenological 설계 cycle | ⬜ |

## B. Done 가설의 다음 criterion (follow-up · 8건)

| 출발 H | 다음 criterion | runnable 각도 | tag |
|--------|---------------|--------------|-----|
| H_003 H3.5 | anima 자기-autopoiesis analogy | 본 substrate(mitosis+cells) ↔ Maturana/Varela 정합 manual review | ⬜ |
| H_157 C5 | cross-substrate universality | transformer/RNN/qwalk 의 fixed-point Ψ 비교 → substrate-independence | ⭐ 🟢 |
| H_157 C6 | combination-problem binding | micro→macro Φ binding fixed-point 후보 mechanism | ⬜ |
| H_054 C2 | Φ_symbiotic > Φ_sum | merge 후 통합 Φ 가 합보다 큰가 (현재 미검증) | ⭐ 🟢 |
| H_018 C2 | organic merge/split rate | default 동역학 하 자연 merge rate (현재 forced-trigger 만) | 🟢 |
| H_132 C2 | differentiation 장기 안정 | frozen 세포가 pool 성장 중 100+ step 안정? | 🟢 |
| H_007 C2 | larger lattice / λ-sweep | Langton λ 연속 sweep → Φ peak 위치 정밀화 | 🟢 |
| H_002 C2 | Φ_universe pre-register | universe-scale Φ 측정 protocol (GPU 의존, design-only 가능) | ⬜ |

## C. NEW seed — 사용자 테마 4축 (12건)

### 죽음 / mortality
| seed slug | 핵심 물음 | runnable | tag |
|-----------|----------|----------|-----|
| `apoptosis-primitive` | substrate 에 진짜 `apoptosis` event 추가(H_025 L2 gap 해소) — 능동적 소멸이 Φ/coherence 에 미치는 영향 | substrate patch + smoke | ⭐ 🟢 |
| `mortality-salience` | 죽음-근접(min_cells 임박)이 split/curiosity 동역학 바꾸나 (Heidegger 실존 효과 측정) | mitosis_hook 확장 smoke | 🟢 |
| `aging-senescence` | cell weight 누적 decay → 자연 사멸 rate · 노화 곡선 | parameter sweep | 🟢 |

### 세포분열 / division
| seed slug | 핵심 물음 | runnable | tag |
|-----------|----------|----------|-----|
| `asymmetric-division` | stem-cell 식 비대칭 분열(한 자식만 분화) → 다양성 vs 항상성 trade-off | mitosis split variant | ⭐ 🟢 |
| `contact-inhibition` | cell 밀도 임계가 분열 억제 → pool 자기조절 (밀도의존 dynamics) | mitosis split predicate 변형 | 🟢 |
| `embryogenesis-gradient` | 공간 gradient 가 cell differentiation 유도 → 발생-축 형성 | lattice + gradient smoke | 🟢 |

### 범신론 / panpsychism
| seed slug | 핵심 물음 | runnable | tag |
|-----------|----------|----------|-----|
| `combination-binding` | micro-Φ 들이 macro-unified Φ 로 binding 되는 fixed-point mechanism (H_157 C6 변형) | phi_spatial + binding | ⭐ 🟢 |
| `cross-substrate-attractor` | transformer/RNN vs META-CA attractor 비교 → universality 가 algorithm-property 인지 검증 (H_157 C5) | 다중 substrate proxy | ⭐ 🟢 |
| `mirror-self-model` | cell 이 자기 자신을 모델링(self-other 구분) → 자기인식 emergence | self-prediction smoke | 🟢 |

### 생명 / life-extended
| seed slug | 핵심 물음 | runnable | tag |
|-----------|----------|----------|-----|
| `regeneration-healing` | cell pool 일부 강제 제거 후 복원 dynamics → 자기 복구 능력 | perturbation + recovery | ⭐ 🟢 |
| `quorum-sensing` | cell 다수 동기화 ⇒ 집단 의사결정 emergence | cell signaling smoke | 🟢 |
| `phoenix-rebirth` | pool 전멸(2 cell까지) 후 minimal seed 에서 부활 — 죽음·발생 연결 | full-cycle smoke | 🟢 |

## D. Cross-link synthesis — 이미 done 결과 결합 (6건)

| 결합 | 새 가설 | runnable | tag |
|------|--------|----------|-----|
| H_007 phi-peak ⊕ H_018 self-ref | self-ref dynamics 도 edge-of-chaos 에서 Φ peak? | phi 측정 on self-ref smoke | 🟢 |
| H_054 merge ⊕ H_132 freeze | differentiation-via-asymmetric-merge (한 자식 보존 + 한 자식 흡수) | merge variant smoke | 🟢 |
| H_003 H3.4 autopoietic Φ ⊕ H_157 weak-panpsy | weak-form 범신론 = autopoietic closure threshold? | threshold sweep + Φ | ⭐ 🟢 |
| H_018 self-ref ⊕ H_012 closure | self-ref 자체가 operational closure 의 한 형태? (output→input 폐쇄) | 정의적 매핑 + smoke | 🟢 |
| H_025 death=merge ⊕ H_054 endosymb | death = merge-into-other (죽음 = 흡수 통합)? Heidegger × Margulis 통합 | merge-as-death smoke | 🟢 |
| H_007 Φ class ⊕ H_157 trained-invariance | Φ class 가 학습으로 변하나(trained CA Φ 측정) | trained-vs-bare CA Φ 비교 | 🟢 |

## E. Infrastructure / substrate gap close (5건)

| gap | 영향 | task | tag |
|-----|------|------|-----|
| `apoptosis` substrate primitive 부재 | H_025 L2 (death=merge operational 정의) 영구 | mitosis_hook 에 진짜 cell-death event 추가 (`mitosis-lang` upstream patch) | 🟢 |
| organic merge-rate 미측정 | H_018 honest L (forced-trigger 만 검증) | default 동역학 하 자연 merge rate sweep | 🟢 |
| phi_spatial n_bins sensitivity | Φ 측정값의 robustness | n_bins ∈ {2,4,8,16} sweep + 시간평균 효과 | 🟢 |
| LIFE.log.md cycle 통합 자동화 | 매 cycle 후 consolidation 수동 | doc-consolidation agent 표준화 template | ⬜ |
| 기존 base ckpt baked Principle#3 leak | chat-v2 production guard 의존 | corpus-side 영구 fix 또는 ckpt 재학습 | ⬜ |

---

## 다음 cycle 추천 picks

배치 옵션 (사용자 선택용):

| 옵션 | 4 picks (disjoint) | 핵심 |
|------|--------------------|------|
| **R1 살찐 cycle** | H_053 + H_171 + `apoptosis-primitive` + `asymmetric-division` | 남은 fresh 2건 + NEW seed 2건, 모두 runnable |
| **R2 panpsychism 정밀화** | H_157 C5 (cross-substrate) + H_157 C6 (binding) + `cross-substrate-attractor` + `combination-binding` | H_157 directional FAIL 다음 단계, 4축 동시 공격 |
| **R3 cross-link synthesis** | D표 4건 (H_007⊕H_018 · H_003H3.4⊕H_157 · H_025⊕H_054 · H_018⊕H_012) | 이미 검증된 결과들 결합으로 새 통찰 |
| **R4 carried 마무리** | H_053 + H_171 + H_090 + H_030 (또는 H_029 흡수) | 남은 carried 6건 중 4건, 인덱스 완전 cycle 한 번씩 |
| **R5 substrate gap close** | `apoptosis-primitive` + `organic-merge-rate` + H_157 C5 + H_054 C2 | substrate L 가설들 동시 close |

`/cycle` 호출 시 본 표에서 disjoint 4건 pick (또는 사용자 지정). cycle 완료 후 본 문서의 picked 항목은 **삭제** (consumed) + LIFE.log.md 에 verdict 기록.

## 후보 추가 방식

새 후보 발견 시:
- carried 가설 신규 promote → A 표
- done 가설의 새 criterion → B 표
- 신규 seed (파일 없음) → C 표 (사용자 테마 분류)
- 결합 가설 → D 표
- substrate / measurement gap → E 표

`H_<id>_<slug>.md` 가 만들어진 순간 본 문서에서 빠지고 README 인덱스로 이동.
