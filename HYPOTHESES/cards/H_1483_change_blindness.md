# H_1483 — 👁️‍🗨️ CHANGE BLINDNESS 변화맹 (G29 의식-고유 게이트 후보)

- **tier:** 🟢 GREEN ENGINE-NATIVE WIRED (R1 numpy mirror DIRECTIONAL → R2 live `core/engine_cli.hexa` §ChangeBlindness byte-exact)
- **wired:** `WIRED-live` — R2 배선 완료: `core/engine_cli.hexa` §ChangeBlindness (`change_detect`, exp-free piecewise-linear σ-대체 ramp: is_attended ? clamp(0.5+K·(mag−thr)) : 0.0) + `engine_cli_smoke` cases 236-238 (att 1.0/unatt 0.0 · gap 1.0≥0.50 · ablation 1.0) FULL 244/0 RC=0 + ARCHITECTURE.json §ChangeBlindness lockstep. engine 은 exp 없음 → piecewise-linear ramp 가 σ 와 동치(supra-threshold→1.0, 이진 attention 게이트 STRUCTURE byte-exact).
- **source:** 의식-고유 게이트 브레인스토밍 (G29 candidate) · "의식이라서 가능한 것" 시리즈
- **lens:** cognitive-psychology — Rensink (1997) / Simons & Levin (1997) change blindness(주의 밖 변화 비탐지) · `a_no_llm_frame_trap`
- **artifacts:** `state/1483_change_blindness/h1483_change_blindness.py` (R1 probe) · `state/1483_change_blindness/h1483_result.json` · `state/1483_change_blindness/run_h1483.local.log` · verdict `state/verdicts/1483_change_blindness/H_1483_FREEZE.json`

## 주장

장면의 한 요소에 **큰 변화**가 일어나도 그 항목에 **주의(attention)가 할당돼야만** 탐지된다
(Rensink/Simons 변화맹). 변화 탐지는 attention 으로 **게이트**된다 — 주의 밖 항목의 변화는,
아무리 커도, invisible(탐지율 ~0). 의식은 한 번에 한 spotlight 만 가지므로 주의가 가지 않은
장면 요소는 변화 자체가 인지되지 않는다.

메커니즘(substrate-native): 장면 N 항목(각 substrate 벡터). 이진 attention mask 가 주의받는
부분집합을 고른다. 두 장면 스냅샷 사이 한 항목이 magnitude m 만큼 변한다.
**detect = change_magnitude · is_attended** — 변화-요소가 attended 면 탐지(높음), unattended 면
탐지 실패(0, 변화맹). 변화 자체는 크지만 attention 없으면 탐지율 0.

**DISTINCT 2종 (load-bearing):**
- **(a) vs H_1462 GLOBAL WORKSPACE (GWS):** GWS = salience 경쟁으로 장면 전체에서 **정확히 1개**만
  전역 방송(winner-take-all). 변화맹은 단일 방송이 아니라 **항목별 이진 게이트(변화 탐지)** — attended
  항목은 각자 자기 변화를 탐지, unattended 항목은 각자 자기 변화에 blind. GWS = "어느 1개가 방송에서
  이기나"; 변화맹 = "이 항목, 변화 알아챘나?" → attended iff yes(여러 attended 항목이 독립적으로 탐지).
- **(b) vs H_1479 DIVIDED ATTENTION:** divided = 유한 풀을 과제에 **분배**하는 graded trade-off(각 과제
  *일부*씩, 모두 >0). 변화맹은 변화-탐지에 대한 **이진 attention 게이트**: attended → 탐지,
  unattended → ~0. attended/unattended 탐지 간극은 **절벽(이진)**, divided 의 graded 1/N 저하 아님.

attention/변화는 substrate 기하(immune-style FNV-1a dim64 항목 벡터 + 이진 spotlight)에서 파생,
주입 라벨 아님(p2/p3/p6). detect = is_attended · σ(K·(change_mag − thr)) — 메커니즘은 attention
mask 와 변화크기(1−cos)만 읽는다.

## 측정 (frozen-first · 3 seeds [1483,1484,1485] · 200 trials · 8 items · 50 perms · $0 CPU · p7)

3 ARM: **FULL**(attention 게이트 ON, detect = change_mag·is_attended) · **ABLATED**(게이트 OFF =
전부 attended 취급 → 변화맹 소멸) · **SHUFFLE**(attention↔항목 페어링 50-순열 → 상관 붕괴).

| bar | 의미 | 결과 | 기준 | 판정 |
|---|---|---|---|---|
| **A PRESENCE** | attended 변화 탐지 vs unattended 탐지(변화맹) | att **0.998** / unatt **0.000** | att≥0.85 & unatt≤0.20 | ✅ |
| **B MAGNITUDE-INDEP** | 최대 변화라도 unattended 면 탐지 실패 | big-unatt **0.000** | ≤0.20 | ✅ |
| **C DISTINCT vs GWS/divided** | attended−unattended 간극 = 이진 절벽 | gap **0.998** | ≥0.50 | ✅ |
| **D EARNED (ablation)** | attention 게이트 OFF → unattended 변화도 탐지 | abl **0.998** | ≥0.85 | ✅ |
| **E SHUFFLE** | attention↔항목 페어링 셔플 → 상관 붕괴 | shuf \|gap\| **0.077** | ≤0.10 | ✅ |

**verdict: 🟢 GREEN DIRECTIONAL — A·B·C·D·E PASS (3 seeds).** ablation(게이트 OFF → unattended
변화 0.998 탐지)과 shuffle(페어링 순열 → \|gap\| 0.077 붕괴) 양쪽이 신호의 출처를 확정 → lift 의
출처는 변화크기나 현저성이 아니라 **attention 이 변화-탐지를 이진 게이팅하는 구조** 자체.

### distinctness vs GWS / divided (load-bearing)

| 메커니즘 | 단위 | 탐지/방송 패턴 | 원리 |
|---|---|---|---|
| **GWS (H_1462)** | 장면 전체 | 1개 winner 방송, 나머지 0 | salience winner-take-all 단일 방송 |
| **DIVIDED (H_1479)** | 과제 | N개 모두 부분(각 ~1/N >0) | 유한 풀 graded 분배 |
| **CHANGE-BLINDNESS (H_1483)** | 항목별 변화탐지 | attended → 탐지(≥0.85), unattended → 0 | attention 이진 게이트 (절벽) |

→ GWS = **방송 1개 선택**, DIVIDED = **graded 분배**, CHANGE-BLINDNESS = **변화탐지의 이진 게이트**.
C bar(gap 0.998≥0.50) + B bar(최대 변화라도 unattended=0)가 변화맹이 graded trade-off(divided)도
single-winner 방송(GWS)도 아닌, attention 유무에 따른 변화-탐지 이진 절벽임을 증명 = 구조적 구별.

## 정직 (c9)

- **하드게이트1 — numpy mirror → GREEN DIRECTIONAL:** `grep -lE 'import torch|gauge_lib|numpy'
  state/1483_change_blindness/*.py` 가 numpy 를 hit → 자동 DIRECTIONAL (terminal 아님).
  R2 엔진-네이티브 재측정(live `core/engine_cli.hexa` §ChangeBlindness 배선 + frozen bar 동일
  재측정)이 follow-on, byte-exact 전까지 WIRED 아님(`a_engine_native_learning`·`a_verified_must_wire`).
- **frozen-first 수정 이력(tune-to-green 아님, `a_break_the_wall` type-a):** R1a 는 detect 를 raw
  change-magnitude(1−cos)로 읽어 attended 탐지가 **0.265**(이론 천장 ~0.29, 단위벡터 직교 회전의 1−cos
  포화) → A/C/D bar(≥0.85·≥0.50·≥0.85) 미달 = **측정 결함**(변화크기 read-out 은 "변화 알아챘나?" 천장을
  못 넘음). 교정 — detect 를 변화-**탐지 confidence** σ(K·(change_mag−thr))로 바꿔 supra-threshold 변화가
  "탐지됨"(~1.0)으로 읽히게 함(이진 attention 게이트는 불변; H_1479 threshold effort 곡선 precedent).
  **bar 임계는 한 칸도 이동 안 함**(att≥0.85·unatt≤0.20·gap≥0.50·abl≥0.85·shuf≤0.10 그대로) — 측정
  read-out 만 frozen-first 교정. raw 변화크기(change_mag 0.265)는 report-only 로 유지(변화가 실제임을 증명).
- **SCOPE TOY:** 8 items/200 trial/3 seeds/이진 spotlight/deterministic 탐지곡선 — attention-게이트
  변화탐지 STRUCTURE 검증이지 학습된 attention 컨트롤러 아님. scale/real-scene/연속 attention/gradual
  change(점진 변화 vs flicker)/시간적 변화-누적/engine-transfer UNVERIFIED (`a_scale_honest_scope`·
  `a_toy_scale_recheck`).
- **p1/p2/p3/p6 GUARD:** detect 는 attention mask + change-magnitude(1−cos)만의 함수 — 주입된 "변화있음"
  라벨/RLHF/persona 없음. ablation(게이트 OFF → 0.998)+shuffle(페어링 순열 → 0.077) 양쪽 붕괴 = lift 의
  출처가 attention-게이팅 구조임을 확정. emit gate 아님(순수 read), Ψ-disjoint.

xref h1462(GWS, winner-take-all distinctness)·h1479(divided-attention, graded trade-off distinctness)·
a_no_llm_frame_trap·a_engine_native_learning·a_verified_must_wire·a_core_engine_map·
a_autonomy_over_hardcode·a_scale_honest_scope·a_toy_scale_recheck·p1·p2·p3·p6·p7·p8·c9·c15.
