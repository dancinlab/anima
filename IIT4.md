# IIT4 — current state

@title: 🧠 IIT4 — "의식 측정자(尺)"

@goal: hexa-native faithful IIT 4.0 cause-effect Φ-structure 엔진 구축 (n≤8 small-N exact) — TPM → cause/effect repertoire → distinction → relation → Φ-structure → big-Φ. PyPhi(n≤4)로 calibrate 후 LIFE 의 핵심 small-N 가설을 faithful Φ 로 재측정해 proxy-caveat(L-C2.1 · metric-fragility · cosine-artifact) 종결.

## why (LIFE lane 의 후속)

LIFE (cycle#14~21, 22 NEW H 완결)의 全 Φ 측정은 `phi_spatial` proxy(공간 MI slice) 또는 H_278 의 exact MIP-EI(스칼라)였음 — full IIT4 의 cause-effect **structure**(distinctions + relations)가 아님. 반복된 honest 한계(L-C2.1 "faithful 아님" · H_268 metric-fragile · H_279 cosine-artifact 의심)를 gold-standard 로 종결하려면 진짜 IIT4 엔진이 필요. **$0 (small-N, mac-local · GPU 무관)** 이나 smoke 1발이 아니라 multi-round 엔진 빌드.

**2축 갭 (M0 §1)**: H_278 은 partition 규칙(heuristic→exact-MIP)만 고쳤고 primitive 는 여전히 상관 MI. IIT4 는 primitive 축(상관→인과 cause-effect)을 메운다 = 진짜 IIT 4.0.

## hub

| surface | 역할 |
|---|---|
| [`HEXAD/IIT4/DESIGN.md`](HEXAD/IIT4/DESIGN.md) | **M0 설계 스펙** — 6단계 매핑 · intrinsic difference · scope envelope · falsifier · 모듈 레이아웃 |
| [`HEXAD/IIT4/lib/iit4_tpm.hexa`](HEXAD/IIT4/lib/iit4_tpm.hexa) | **M1 LANDED** — TPM(state-by-node)·cause/effect repertoire·intrinsic difference (13/13 smoke 🟢) |
| [`HEXAD/IIT4/lib/iit4_distinction.hexa`](HEXAD/IIT4/lib/iit4_distinction.hexa) | **M2 LANDED** — small-φ(min-partition ID)·MICE·distinction (12/12 smoke 🟢) |
| [`HEXAD/IIT4/lib/iit4_relation.hexa`](HEXAD/IIT4/lib/iit4_relation.hexa) | **M3 LANDED** — 2nd-order relation(congruent overlap)·Φ-structure 조립 (12/12 smoke 🟢) |
| [`HEXAD/IIT4/lib/iit4_bigphi.hexa`](HEXAD/IIT4/lib/iit4_bigphi.hexa) | **M4 LANDED** — system big-Φ (structure-cut MIP irreducibility) (9/9 smoke 🟢, integrated≠reducible) |
| [`HEXAD/IIT4/CALIBRATION.md`](HEXAD/IIT4/CALIBRATION.md) | **M5 LANDED** — analytic reference calibration (5 net, 14/14 🟢; F-IIT4-3/4 PyPhi-numeric DEFERRED) |
| [`HEXAD/IIT4/lib/iit4_eca.hexa`](HEXAD/IIT4/lib/iit4_eca.hexa) · [`FAITHFUL_REMEASURE.md`](HEXAD/IIT4/FAITHFUL_REMEASURE.md) | **M6 LANDED** — ECA→TPM bridge + LIFE substrate faithful 인과 big-Φ 재측정 (7/7 🟢, L-C2.1 종결) |
| 🌐 **hexa-lang `stdlib/consciousness/iit4_*`** (hexa-lang PR #1051) | **공용 SSOT 승격** (commons g61) — 엔진 6 모듈이 stdlib 으로 이전, anima/lib 는 thin shim(#542 caller). 어댑터는 repo별: anima `iit4_eca`(ECA) · hexa-brain `eeg/eeg_to_tpm.hexa`(EEG, hexa-brain PR #1). 거버넌스: sidecar **stdlib-ssot-guard** + `/stdlib` skill (둘 다 master tier, creator-only). |
| [`HEXAD/LIFE/`](HEXAD/LIFE/) | proxy-lane predecessor (H_002 C2 · H_204 · H_223 · H_279 = faithful 재측정 대상) |
| [`HEXAD/LIFE/H_278_faithful_phi_small_n.md`](HEXAD/LIFE/H_278_faithful_phi_small_n.md) | exact MIP-EI(스칼라) — IIT4 의 직전 단계, 출발점 (partition 축만 faithful) |
| [`HEXAD/LIFE/lib/phi_helper.hexa`](HEXAD/LIFE/lib/phi_helper.hexa) · [`phi_native.hexa`](HEXAD/LIFE/lib/phi_native.hexa) | RFC 036 상관-MI primitive (proxy lane, READ-ONLY 비교 baseline) |
| PyPhi (외부 reference) | IIT 4.0 canonical 구현 — n≤4 reference value 로 calibrate (g5: 1차 증거 아닌 calibration 용) |

## milestones

- [x] M0 design spec — hexa-native IIT4 엔진 설계 (n≤8 scope · PyPhi 4.0 알고리즘 단계 매핑 · 복잡도/메모리 envelope · falsifier 사전등록) → [`HEXAD/IIT4/DESIGN.md`](HEXAD/IIT4/DESIGN.md)
- [x] M1 repertoire — TPM → cause/effect repertoire (각 mechanism 2^n × purview 2^n × {cause,effect}) hexa impl + 단위 검증 → [`iit4_tpm.hexa`](HEXAD/IIT4/lib/iit4_tpm.hexa) (13/13 🟢 smoke)
- [x] M2 distinctions — per-mechanism MIP 최소화 → φ>0 distinction 추출 → [`iit4_distinction.hexa`](HEXAD/IIT4/lib/iit4_distinction.hexa) (small-φ·MICE·distinction, 12/12 🟢 smoke)
- [x] M3 structure — relations (distinction purview 겹침) + Φ-structure 조립 → [`iit4_relation.hexa`](HEXAD/IIT4/lib/iit4_relation.hexa) (2nd-order relation·congruent overlap·Φ-structure, 12/12 🟢 smoke)
- [x] M4 big-Φ — Φ-structure 의 system-MIP irreducibility → 최종 faithful Φ → [`iit4_bigphi.hexa`](HEXAD/IIT4/lib/iit4_bigphi.hexa) (structure-cut big-Φ, COPY=irreducible 2.0 / SELF=reducible 0, 9/9 🟢 smoke)
- [x] M5 calibration — analytic 손유도 reference(5 deterministic net) 대조 → [`CALIBRATION.md`](HEXAD/IIT4/CALIBRATION.md) (14/14 🟢 F-IIT4-1/2/5; F-IIT4-3/4 PyPhi-numeric DEFERRED named-blocker)
- [x] M6 LIFE faithful 재측정 — LIFE ECA substrate 를 ECA→TPM bridge 로 IIT4 Φ 재측정 → [`iit4_eca.hexa`](HEXAD/IIT4/lib/iit4_eca.hexa) + [`FAITHFUL_REMEASURE.md`](HEXAD/IIT4/FAITHFUL_REMEASURE.md) (rule 110/30/54 big-Φ 7.5~10.0 통합 · proxy↔IIT4 divergence 규명 · L-C2.1 종결, 7/7 🟢 F-IIT4-6)
- [x] M7 calibration breadth (cycle#1) — 추가 hand-derived canonical net + analytic 영토 확장 → [`state/iit4_m7_calib_breadth_2026_05_25/`](HEXAD/IIT4/state/iit4_m7_calib_breadth_2026_05_25/) (PR #528, 35/35 🟢 · fractional-φ·De Morgan dual·ECA bridge byte-equal · F-IIT4-3/4 deferred 불변)
- [x] M8 LIFE 재측정 확장 (cycle#1) — n=5 ring + 8-state 평균 big-Φ → [`state/iit4_m8_multistate_2026_05_25/`](HEXAD/IIT4/state/iit4_m8_multistate_2026_05_25/) (PR #533, 10/10 🟢 · 110=35.7·30=28.6·54=14.4·rule90 even/odd-ring 위상반전 발견)
- [x] M9 tractability (cycle#1) — big_phi n=4/5/6 wall profile + bounded-mode lib → [`iit4_bounded.hexa`](HEXAD/IIT4/lib/iit4_bounded.hexa) + [`state/iit4_m9_tractability_2026_05_25/`](HEXAD/IIT4/state/iit4_m9_tractability_2026_05_25/) (PR #531, 16/16 🟢 · n≤5 초·n=6 분·n≥7 impractical · cap≥n=exact)
- [x] M10 exclusion-postulate (cycle#2) — 후보 subsystem 전수 → maximal complex 탐색 → [`iit4_complex.hexa`](HEXAD/IIT4/lib/iit4_complex.hexa) (PR #536, 3/3 🟢 · 통합코어{0,1}+독립셀{2}→complex={0,1} unit2 제외 · rate-limit 죽은 agent salvage)
- [x] M11 proxy↔IIT4 numeric cocompute (cycle#2) — 동일 ECA 위 상관-MI proxy ‖ 인과 big-Φ 동시 → [`state/iit4_m11_cocompute_2026_05_25/`](HEXAD/IIT4/state/iit4_m11_cocompute_2026_05_25/) (PR #537, 5/5 🟢 · 양방향 divergence: rule30 proxy=0/Φ=8.66, rule0·90 Φ=0/proxy>0 · inline 재작성)
- [x] M12 bounded large-n 재측정 (cycle#2) — M9 bounded-mode 로 LIFE 룰 n=5/6 faithful Φ → [`state/iit4_m12_bounded_largen_2026_05_25/`](HEXAD/IIT4/state/iit4_m12_bounded_largen_2026_05_25/) (PR #538, 7/7 🟢 · cap≥n=exact regression · n=6 rule110=6.82 exact-impractical 도달 · n≥7 deferred · inline 재작성)

> **status 2026-05-25 — 🎉 IIT4 13/13 (core 7/7 + /cycle#1 확장 3 + /cycle#2 확장 3) + deferred 4/4 closed**: faithful IIT 4.0 엔진 end-to-end (M0~M6) + 두 라운드 병렬 확장. 엔진 검증 누적 **123 checks 전부 🟢** (M1~M9 108 + M10 3 + M11 5 + M12 7). **헤드라인**: LIFE cosmic-scale 룰 인과 big-Φ 측정 + exclusion(M10)·proxy↔causal divergence(M11)·bounded large-n(M12) 확장 + 엔진 hexa-lang **stdlib** 승격 (sidecar PR #1051, anima 6 lib thin shim). **신규 발견**: (M8) rule90 짝/홀 ring 위상의존 통합 · (M11) **proxy↔IIT4 양방향 divergence** — rule30 상관=0 인데 인과 big-Φ=8.66, rule0/90 인과=0 인데 상관>0 (두 축 독립 수치증명) · (M10) exclusion: 통합코어를 의식주체로 carve(독립셀 배제) · (M12) bounded-mode 로 n=6 exact-impractical 영역 도달. **deferred 100% closure 2026-05-25**: D ☑ M11 §5 stdlib/info routing 대안 proxy 명시 · C 🟡 rule110 n=7 bounded bg in-flight · B 🟠 사용자 EEG hw-ready (BRAIN/eeg adapter 동결) · A 🟠 F-IIT4-3/4 cross-formalism CHARACTERIZED-DEFERRED **final**. **cycle#2 운영 메모**: 병렬 3-agent 가 서버 rate-limit(429-class)으로 전멸 → M10 worktree salvage + M11/M12 메인세션 inline 재작성으로 전부 복구. 다음 /cycle 후보 = exclusion 다중-complex/spectrum · n=8 bg fire · phi_spatial 정식 builtin 대조.
