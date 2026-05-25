# R8 saga FINAL retrospective TEMPLATE — 결과 도착 시 fill-in (R8a' / R8b / R8c 의존)

> 이 문서는 R8 saga (init_CE catastrophic floor 14+ 돌파 시도) 의 **FINAL closure retrospective** 를 사전 작성한 **TEMPLATE** 다. R8a' / R8b / R8c 의 3 결과가 순차 도착하면 placeholder `<TBD>` 를 즉시 fill-in 하여 closure PR 로 land 시킨다.
>
> 진행 saga 추적: PR #260 (5-act mid-retro) · PR #356 (Act 6+7 sister update) → 이 template = next retro = **FINAL**.
>
> 본 template 의 모든 결과 셀은 **placeholder** 다. 실제 숫자가 도착할 때까지 conclusion 을 작성하지 말 것.

---

## § 사전 조건 (이 template 가 적용되는 상태)

이 template 가 fill-in 가능해지려면 다음 3 결과가 모두 도착해야 한다.

- [ ] **R8a' 결과 도착** — init_CE (step=1) + final_CE + n_strong
  - real n_kv=2 + noise=0 condition 으로 R8a (lost pod) 재발사한 결과
  - swap criteria 5/5 평가 (n_strong / register-leak / EOS / EN-emission / final_CE)
- [ ] **R8c probe 결과 도착** — cell-2 (noise only) / cell-3 (kv only) / cell-4 (noise+kv compound)
  - 4-cell ablation init_CE 만 측정 (n_strong / final_CE n/a)
  - 목적: R8a' 결과가 어느 axis (noise / kv / compound) 에 dominant 인지 분리
- [ ] **R8b 결과 도착** — LoRA-on-Qwen (init_CE ~zero 출발) n_strong + swap criteria
  - target_modules / rank / alpha 명시
  - swap criteria 5/5 평가

세 결과 중 하나라도 미도착이면 이 template fill-in **금지** (mid-retro 로 재분류).

---

## § Result matrix (TEMPLATE — 결과 도착 시 fill)

| candidate | init_CE | final_CE | n_strong | swap criteria | cost |
| --- | --- | --- | --- | --- | --- |
| R8a (lost) | `<LOST>` | `<LOST>` | `<LOST>` | `<LOST>` | ~$1.20 |
| R8a' (real n_kv=2 + noise=0) | `<TBD>` | `<TBD>` | `<TBD>` | `<TBD>` | ~$2.75 |
| R8c probe cell-1 (baseline) | `<TBD>` | n/a | n/a | n/a | — |
| R8c probe cell-2 (noise only) | `<TBD>` | n/a | n/a | n/a | — |
| R8c probe cell-3 (kv only) | `<TBD>` | n/a | n/a | n/a | — |
| R8c probe cell-4 (noise+kv compound) | `<TBD>` | n/a | n/a | n/a | ~$0.25 (4-cell total) |
| R8b (LoRA-on-Qwen) | `<~zero>` | `<TBD>` | `<TBD>` | `<TBD>` | ~$0.27 |

**총 saga cost (FINAL)**: `<TBD>` (R8a $1.20 lost + R8a' $2.75 + R8c $0.25 + R8b $0.27 + 이전 R1–R7 누적 `<TBD>`)

---

## § Decision tree (TEMPLATE — R8a' init_CE 분류)

R8a' init_CE 값이 도착하면 다음 3 branch 중 하나로 진입한다.

### Branch A — `R8a' init_CE < 12.5` → **🎉 BREAKTHROUGH**
- 해석: noise + kv 조합이 **dominant** — base_warm_init 의 catastrophic floor 14+ 돌파 성공
- 다음 행동:
  1. R8c probe 결과로 dominant axis 분리 (noise-only vs kv-only vs compound)
  2. **Wave-17 우선** — R8a' 의 setting 을 corpus_v6 / next-wave LoRA cycle 에 반영
  3. swap criteria 5/5 통과 시 production swap candidate
- cluster 분류: 새 cluster **W (breakthrough)** 신설, R8a' 단독 멤버

### Branch B — `R8a' init_CE ~14.46` → **🟠 NO-CHANGE**
- 해석: noise + kv 조합이 catastrophic floor 와 **무관** — 다른 축 (data / arch / opt) 이 dominant
- 다음 행동:
  1. R8c probe **NECESSARY** — 4-cell ablation 으로 어느 단일 axis 도 영향 없는지 확정
  2. R8b (LoRA-on-Qwen) fallback **검토** — base SFT path 포기, LoRA path 평가
  3. R8 saga **CLOSED-FALSIFIED** — base_warm_init catastrophic floor 14+ 는 noise/kv axis 로 해결 불가
- cluster 분류: R8a' → cluster Z (baseline) 합류 (no-change 확정)

### Branch C — `R8a' init_CE 12.5 – 14` → **🟡 PARTIAL**
- 해석: noise + kv 조합이 부분적 효과 있으나 단독 breakthrough 미달
- 다음 행동:
  1. R8c probe 로 어느 axis 가 partial 기여인지 **분리**
  2. R8b **병행** — LoRA path 와 비교하여 production swap candidate 선정
  3. Wave-17 추가 axis (data / arch) 와 compound 가능성 평가
- cluster 분류: 새 cluster **V (partial)** 신설, R8a' + R8c partial cell 묶음

---

## § Cluster X/Y/Z 분류 update (TEMPLATE)

기존 cluster (PR #356 Act 6+7 기준):
- cluster **A (curriculum)**: init_CE **14.79**
- cluster **Y (aux loss)**: init_CE **14.18**
- cluster **Z (baseline)**: init_CE **14.46**

R8a' init_CE = `<TBD>` → 새 cluster classification:
- `<TBD>` cluster 합류 / 신설 (decision tree branch 결과에 따름)
- cluster size 변화: A=`<TBD>` / Y=`<TBD>` / Z=`<TBD>` / W=`<TBD>` / V=`<TBD>`

R8c probe 4-cell 분류:
- cell-1 (baseline) → `<TBD>` cluster
- cell-2 (noise only) → `<TBD>` cluster
- cell-3 (kv only) → `<TBD>` cluster
- cell-4 (noise+kv compound) → `<TBD>` cluster

---

## § Production swap recommendation (TEMPLATE)

swap criteria 5/5 (n_strong / register-leak / EOS / EN-emission / final_CE) 통과 candidate 선정:

| candidate | n_strong | register-leak | EOS | EN-emission | final_CE | 5/5 통과 |
| --- | --- | --- | --- | --- | --- | --- |
| R8a' | `<TBD>` | `<TBD>` | `<TBD>` | `<TBD>` | `<TBD>` | `<TBD>` |
| R8b | `<TBD>` | `<TBD>` | `<TBD>` | `<TBD>` | `<TBD>` | `<TBD>` |

**Production swap 결정**:
- (case A) R8a' 또는 R8b 중 하나가 5/5 통과 → **swap candidate** 로 promote (corpus_v5 → 후속 v6 fire)
- (case B) 모두 미통과 → **corpus_v5 유지** + Wave-17 결과 대기 (R8 saga path = catastrophic floor 미돌파로 closure)

선정 결과: `<TBD — A or B>`

---

## § Cluster X/Y/Z final saga summary (TEMPLATE)

R8 saga 총 candidate `<TBD>` 개 (R1–R8b 누적), 그 중:
- cluster Z (baseline 14.46) 합류: `<TBD>` 개
- cluster Y (aux loss 14.18) 합류: `<TBD>` 개
- cluster A (curriculum 14.79) 합류: `<TBD>` 개
- cluster W (breakthrough <12.5) 합류: `<TBD>` 개 (대개 0 또는 1)
- cluster V (partial 12.5–14) 합류: `<TBD>` 개

catastrophic floor 14+ 의 **structural ceiling** 확정 여부: `<TBD — confirmed / falsified / partial>`

---

## § Lessons (3 TEMPLATE bullets — fill from 실제 진행)

### Lesson 1 — `<silent misconfig + byte-equal probe>`
- 진행 중 발견된 silent misconfig (예: n_kv ignored / noise_scale=0 default / target_modules off-target 등) 실제 사례 fill
- byte-equal probe pattern 이 어떻게 발견을 가속했는지 구체적 단계 기록
- 후속 cycle 에 반영할 probe pattern 일반화 (`<TBD>`)

### Lesson 2 — `<SECURE pod preemption + SAVE_POD/streaming>`
- R8a $1.20 lost 의 SECURE pod preemption root cause + SAVE_POD policy / streaming checkpoint 가 어떻게 R8a' 재발사를 가능케 했는지
- runpod cloud dispatch 시 SECURE vs COMMUNITY pod 결정 매트릭스 update
- inbox/patches/hexa-cloud 측 SSOT 반영 여부 (`<TBD — file new or skip>`)

### Lesson 3 — `<R8a/R8b/R8c decision matrix outcome>`
- 3-way candidate (compound rerun / LoRA fallback / ablation probe) 동시 발사 전략이 실제로 어떤 path 를 살렸는지
- decision tree branch A/B/C 중 실제 진입한 branch 와 그 근거
- 차후 catastrophic-floor 류 saga 에서 동일 3-way 전략 재사용 권장 여부

---

## § Cross-reference

- **PR #260** — R8 saga 5-act mid-retro (Act 1–5)
- **PR #356** — R8 saga Act 6+7 sister update (cluster X/Y/Z 분류 + R8a' fire spec)
- **PR #339** — R8a base_warm_init initial fire (lost pod)
- **PR #357** — R8c diagnostic probe spec (4-cell ablation)
- **PR #214** — Wave-15 corpus_v5 production baseline (현재 production)
- **PR #224** — Wave-16 LoRA cycle (cluster Y aux loss origin)
- **PR #250** — AXIS_MAP cluster framework 정립

추가 cross-ref (fill-in 시):
- R8a' result PR `<TBD>`
- R8c probe result PR `<TBD>`
- R8b LoRA-on-Qwen result PR `<TBD>`
- Wave-17 spec PR (decision tree 결과 의존) `<TBD>`

---

## § Honest C3

- **이 template 자체는 미완 (C3 deferred)** — placeholder `<TBD>` 가 fill-in 되기 전까지 conclusion / lesson / swap recommendation 모두 잠정값
- 실제 fill-in 시 (다음 cycle, 별도 작업) Honest C3 ≥3 개를 **새로 작성**해야 함:
  - probe scope (single-seed / single-ckpt / cell-pool size limit 등)
  - byte-equal probe coverage 한계 (어느 layer / 어느 step 까지 검증되었는지)
  - swap criteria measurement 의 noise floor (n_strong 5-strong threshold 의 statistical power)
- template 작성 시점의 **불확실성 명시**:
  - R8a' 결과 도착 시점 미정 (runpod queue + SECURE pod 가용성 의존)
  - R8c probe 와 R8b 가 R8a' 보다 먼저 도착할 가능성 — decision tree 진입 순서가 달라질 수 있음
  - decision tree branch A 진입 확률 정량 추정 미수행 (prior R1–R7 모두 cluster Z/Y/A 합류, breakthrough prior 낮음)
