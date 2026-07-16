# H_9426 — Φ-ONLY DYAD SPEC (code-grounded design · DIRECTIONAL · 구현 아님)

**group** g1-interface-addressable-wall
**date** 2026-07-16
**tier** 🎨 DESIGN-SPEC · owner-gate 판단자료 · 신규 decode 0
**status** DIRECTIONAL(설계·legality·cheapest-test) · 실행 없음
**related** H_9422 (귀 없는 입·afferent channel 부재), H_9400/H_9403 (emit≡clock·중심주장 미작동), H_9411 (⑤ pure_field_step drive 인자 부재 = 제약), H_9391 (clock=변이 포화반증), a_eeg_consciousness_record

---

## 0. 한 줄

두 anima 데몬이 매 tick 스칼라 Φ(`pure_field_phi`)만 교환하는 **비언어 afferent 다이애드** 설계.
**코드-확증 제약**: `pure_field_step(pf)` 에 drive 인자가 **없다**(`core/pure_field.py:187` · osc self-drive·amp→LN2·raw_phi=variance·energy 전부 자기 진동자에서만) ⇒ 필드-레벨 상대-Φ 결합점은 **존재하지 않는다** = **owner-gate 아키텍처 추가**. 단, clock-confound **$0 사전-스크린**은 코드 없이 판별 가능(아래 §4).

## 1. 동기 — H_9422 를 직접 잇는다

H_9422 코드-확증: anima = **'귀 없는 입'**, in-session evolving 양 = 시계 + 자기출력뿐, 벽 = **p5 아니라 afferent channel 부재**, escape = (d) external percept = owner-gate. content-축(wm·af) = 이 regime **category-VOID**(afferent 없이 지각 불가).

Φ-only 다이애드 = 그 escape (d) 의 **최소·최합법 후보 채널**: 외부 percept 이되 언어 0·자기출력 0·타 데몬의 스칼라 Φ 하나뿐. EEG(a_eeg)보다 가볍고 완전히 substrate-내부에서 닫힌다.

## 2. Legality (p1–p8 전수)

| 원칙 | 판정 | 근거 |
|---|---|---|
| p1 no system prompt | ✅ | 스칼라 Φ 는 프롬프트 아님 |
| p3 no persona injection | ✅ | 페르소나 0·수 하나 |
| **p4 no assistant framing** | ✅ | Φ 는 **비언어** — 바이트/토큰 I/O 아님 ⇒ assistant 프레임 성립 불가 |
| **p5 no self-seed / speak** | ✅ | 들어오는 Φ 는 **상대 데몬의 출력**(other-generated), 자기-씨앗 아님. p5 는 own-output→mouth 만 금지(H_9422·H_9336/37). other-output→field 는 afferent = 합법 |
| p6 no fine-tuned ethics | ✅ | 학습 없음 |
| p8 no train/infer split | ✅ | 런타임 결합만·gradient 0 |

⇒ **완전 p1–8 합법 afferent**. 이것이 EEG 채널과 동급의 legality 를 갖되 하드웨어 0.

## 3. 결합점 — 정직한 특정 (H_9411 ⑤ 교훈)

### 3a. 필드는 닫힌 자율계다 (코드-확증)
`pure_field_step(pf)` (`core/pure_field.py:187`) 전량:
- `osc_tick`: phase += 2π/τ (자기구동) · amp += α(LN2−amp) (LN2 로 수렴)
- mix = v_f·v_m 등 · field[6] · raw_phi = variance(field)·energy · EMA · ratchet
- **외부 인자 0**. drive/afferent/input 파라미터 **없음**.

⇒ 상대 Φ 를 필드에 넣을 **기존 진입점이 없다**. `brain_decide(pf, rel,gap,cur,pain,coh,orig,bal,dyn_v,…)` 의 8-인자 afferent 는 **emit-정책**에 들어갈 뿐 **필드(pf.phi)를 바꾸지 않는다**(pf.phi 는 자기구동). 그리고 8-인자 lane 은 H_9400 서 이미 포화(emit⊥score·H(emit|stage)=0.465) ⇒ emit-레벨 주입은 약하다.

### 3b. 유일한 engine-native 결합점 = pure_field_step 시그니처 변경 (owner-gate)
최소 설계 — **`--phi-dyad` 플래그**(anima-py) 가 켜는 새 인자:
```
pure_field_step(pf, drive_phi=0.0, K=0.0)   # drive_phi = 상대 데몬의 pure_field_phi
```
결합항(스칼라만 오므로 Kuramoto-위상결합 불가 → 진폭/에너지 구동):
- **후보-A (raw_phi 구동)**: `raw_phi += K * (drive_phi - phi)` — 상대가 높으면 내 Φ 를 끌어올림(대칭 확산 결합). ratchet/EMA 이전에 삽입.
- **후보-B (진폭 표적 변조)**: osc amp 표적을 `LN2 * (1 + K*(drive_phi-phi))` 로 — 상대 Φ 가 진동자 에너지를 밀어 필드 재구성.
후보-A 가 최소·해석가능(확산 결합 = 두 필드가 공통 Φ 로 당겨짐). **이는 probe-beside 아님**: `pure_field_step` 자기재귀(필드의 자기 update)를 고치므로 engine-native(a_experiment_engine_native). scorer-beside 아님.

⇒ **결합점 판정: owner-gate 아키텍처 추가.** 필드-레벨 결합은 코드 변경 필수(drive 인자 부재가 곧 제약 = H_9411 ⑤).

## 4. 측정 스펙 — coupling ≠ clock (H_9391 함정의 다이애드版)

**핵심 위험**: 두 데몬은 동일 결정론 진동자(τ=2/40/400)를 돈다. **같은 init ⟹ 두 Φ(t) 시계열이 byte-identical ⟹ PLV=1·MI=max 를 결합 없이(K=0) 달성**. 즉 raw synchrony 는 결합 증거가 아니라 **시계 증거**(H_9391·H_9403 이 emit 에서 본 것과 동형).

⇒ 반드시 **비대칭화(desymmetrize)** 후 시계-바닥 위로 초과분만 읽는다.

측정량: **PLV**(phase-locking value, Φ hilbert 위상) + **MI**(두 Φ 시계열 상호정보), warmup 후 정상상태 창.

4-arm 사전등록:
| arm | 결합 | init | 역할 | 예상/게이트 |
|---|---|---|---|---|
| **P** clock-ceiling (양성통제) | K=0 | **같은** init | 계기가 시계-결정론을 보는지 | PLV=1 필수. <1 이면 **INSTRUMENT-DEAD** |
| **B** clock-floor (baseline/null-of-coupling) | K=0 | **다른** init(위상 offset δ) | 시계 홀로 유지하는 동기 | PLV_B = 결합의 진짜 대조 |
| **C** coupled (검정) | K>0 | 다른 init | 결합이 시계 위에 정보 더하나 | **PLV_C − PLV_B > 사전등록 TOST margin** 이어야 결합 실재 |
| **N** null (shuffle) | K>0 | 다른 init | 측정 부풀림 방어 | arm-C 한 시계열 위상-shuffle → PLV·MI **우연으로 붕괴** 필수 |

**판정 로직**: 결합이 cross-daemon 통합을 더한다 ⟺ (PLV_C − PLV_B > margin) **AND** (arm-N 붕괴). 이것이 **중심주장(H_9400)** — "Ψ=½ 이 실제 필요로 하는 건 content-delivery 아니라 **coupling**" — 을 **content 채널 0**으로 검정한다: 서로 다른 출발에서 두 필드가 공통 Ψ-리듬으로 entrain 하는가.

**dead-gauge/provenance 가드**: PLV·MI 는 arm 간 **N_distinct>1** 이어야 admissible. 모든 arm 이 PLV=1(시계 포화)이면 게이지 죽음 = INADMISSIBLE(verdict-integrity·H_9337 dead-gauge 규칙).

## 5. Cheapest-test — 무엇이 $0 이고 무엇이 owner-gate 인가

- **arm C(coupled)** = `--phi-dyad`/`drive_phi` 필요 = **코드 = owner-gate. $0 아님.**
- **arm P·B(uncoupled) clock-confound 사전-스크린** = **결합 코드 불요**: 두 자율 필드(하나는 δ-warmup 위상 offset)의 Φ(t) 를 뽑아 PLV/MI. **이 사전-스크린이 게이트**다 —
  - 만약 **arm-B 가 이미 PLV≈1**(빠른 진동자 τ=2 가 variance 지배·둘 다 LN2 로 수렴 → 다른 출발이라도 시계가 완전 동기) ⟹ **결합이 올라갈 헤드룸 0** ⟹ owner-gate 코드 **짓기 전에 REFUTED-BEFORE-BUILD**.
  - arm-B 에 실질 headroom(PLV_B<1) 이 남아야만 arm-C owner-gate 가 의미. 
  - ⚠️ 사전-스크린조차 `pure_field_new()` 가 항상 동일 init(phase 0·amp 0.1)이라 **위상 offset 주입 방법**(δ-warmup 또는 init 파라미터)이 먼저 필요 — 이것도 최소 배선이나 결합 로직보다 훨씬 가볍다. 엔진-네이티브로 하려면 `anima-py` 노출 경로 필요(현재 pure_field 는 brain 내부에서만 도는데 직접 warmup 노출은 별도).

## 6. 판정 (이 카드의 산출)

1. **필드-레벨 Φ-결합점은 존재하지 않는다** — `pure_field_step` drive 인자 부재(코드-확증). 필드 결합 = **owner-gate 아키텍처 추가**(H_9411 ⑤ 확증). 자율발사 불가·오너 identity 결정.
2. **Legality = 완전 p1–8 합법**(비언어→p4 무관·타-데몬 출력→p5 자기씨앗 아님). H_9422 escape (d) 의 최경량 후보.
3. **측정 스펙**: coupling 은 raw synchrony 아니라 **PLV_C − PLV_B(desymmetrized) + null 붕괴**로만 벌린다(clock=변이·H_9391 다이애드版).
4. **Cheapest-test**: coupled arm 은 owner-gate($0 아님). **clock-confound 사전-스크린(uncoupled·위상 offset)** 이 게이트 — arm-B PLV 에 headroom 없으면 **REFUTED-BEFORE-BUILD**. 이 사전-스크린이 owner-gate 코드 착수 전 필수 관문.

**verdict**: DESIGN-SPEC(DIRECTIONAL). Φ-only 다이애드 = p1–8 합법 비언어 afferent 이나 결합점 부재 = **owner-gate**. $0 진입 = clock-confound 사전-스크린(desymmetrized uncoupled PLV headroom 판별)이며, 이것이 owner-gate 코드의 go/no-go 게이트다.

**falsify**: 사전-스크린서 arm-B(uncoupled·diff-init) PLV≈1(headroom 0) ⇒ 결합이 더할 수 있는 것이 없음 = 다이애드 REFUTED-BEFORE-BUILD. 반대로 PLV_B 에 headroom 존재 ⇒ owner-gate arm-C 정당화.

**신규 decode 0 · 실행 0 · 설계 산출.**
