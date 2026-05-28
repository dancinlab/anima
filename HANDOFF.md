# HANDOFF — anima-tree-universe-consolidate (round 6-14 통합)

> UNIVERSE round 6-14 발견을 ANIMA 트리 **문서 + 코드**로 통합한 작업의 인계 문서.
> 작성: 2026-05-29 · slug: `anima-tree-universe-consolidate` · 상태: ✅ SHIPPED + QA 4축 green.

---

## 1. PR matrix

| PR | 제목 | 상태 | 핵심 |
|----|------|------|------|
| [#1353](https://github.com/dancinlab/anima/pull/1353) | `pe_edge_of_chaos_peak` — H_670 🟡 edge-of-chaos Φ-peak 코드화 + 🧭 M2 정합 | ✅ MERGED (squash, commit `1ca09be03`) | 작업 1·2·3 일괄 — 코드 + smoke + 문서 정합 |

선행 의존 (이미 origin/main landed, 본 작업이 정합):
- #1290 H_660 convexity scale-inv 화해 (`pe_norm_convexity`) · #1294 코드 반영
- #1312 H_670 edge-of-chaos universal (🟡 PARTIAL 5/6) — 본 작업이 코드화한 verdict
- #1296 M4b 3B fire 🔴 2/5 · #1303 H_666 aux-loss sweep · #1304 moe_prescription 4-조건

## 2. 설계 SSOT

- **`CORE/EMIT_SUBSTRATE_DESIGN.md`** — emit-substrate 2층 (구조 lib + 숫자 SSOT) 설계 계약 + F-EMIT-1..4 falsifier 사전등록. 본 작업의 `pe_edge_of_chaos_peak` 도 이 계약 (실수 반환 · bool emit gate 0 · 숫자 상수 = design-tunable) 준수.
- **`ANIMA.md` 🧭 메타블록** (M1-M4) — round 6-14 발견 종합 SSOT. 본 작업이 M2 에 code-wiring 라인 + emit-substrate 트리 노드 smoke count(17/17) 정합.
- **UNIVERSE/H_670_phi_complexity_ordering_substrate_family_generalize.md** — edge-of-chaos Φ-peak verdict 원본 (🟡 PARTIAL 5/6).

## 3. API surface

**SKIP** (per task scope). 신규 pub fn 1개 — `pe_edge_of_chaos_peak(order_param: float) -> float` 는 emit-substrate 구조 lib 내부 함수로, 외부 API 노출/문서화 대상 아님. 소비자 (BRIDGE/HIVE/SAVANT/DREAM wiring) 는 기존 import 그대로.

## 4. 컴포넌트 트리

```
CORE/phi_envelope_substrate.hexa  (구조 lib · ✅ 17/17 smoke)
├─ envelope_multiscale            multi-scale self-similar Φ-envelope (H_648/634)
├─ envelope_self_similarity       인접 scale Pearson r (F-EMIT-1)
├─ pe_coupling_for_class          H_653 convexity coupling (IV 最高 단조)
├─ pe_superadd_for_class          H_655 super-add (II 最高 역전)
├─ pe_peak_align_for_class        H_657 peak=GZ_LOWER 정렬 (III/IV)
├─ pe_norm_convexity              H_660 🟢 scale-invariant convexity (화해 측도)
├─ pe_norm_convexity_for_class    H_660 class 서명 (IV 最高 단조)
├─ pe_edge_of_chaos_peak   ★ NEW  H_670 🟡 edge-of-chaos Φ-peak (inverse-U)
├─ collective_phi_nest            집단 Φ 중첩 (super-additive · sync · convexity_span)
└─ phi_smooth_no_cliff            H_649 register-collapse cliff 부재
CORE/phi_envelope_substrate_smoke.hexa  (F-EMIT-1..3 + H653/655/657/660/670 invariant)
```

## 5. 환경 변수 / 의존

**none.** $0 mac-local · `hexa parse` + `hexa run` 검증 (toolchain = `hexa 0.1.0-dispatch`). GPU/runpod 의존 없음. RNG 없음 (deterministic).

⚠ smoke 실행 시: import 가 canonical 절대경로 (`/Users/ghost/core/anima/CORE/...`)이라, 워크트리 편집본 검증은 import-patch 필요 — `/tmp/<x>/` 복사 + `perl -pi -e 's|import "...canonical..."|import "...tmpcopy..."|'` 후 `hexa run`. (memory: LIFE cycle hexa-run 함정 참조)

## 6. 다음 우선순위

1. **aux-loss M4b re-fire** (🔴→escape 검증) — H_666 #1303 toy-verified `load-balance aux-loss = 유일 escape lever`. **타세션 in-flight** (#1315 d-scale CLOSED-NEG 3/3, aux+d 조합 실패 harvest 완료) — **건드리지 말 것**. a_toy_scale_recheck (#1301) 따라 scale-up fire 가 처방 확정의 마지막 조각.
2. **H_670 Kuramoto floor caveat** — F670.1 (Kuramoto incoherent=정지 tier 가 Φ floor) 깨짐. inverse-U 가 cross-family universal 이려면 Kuramoto family 의 floor 재정의 (edge-of-sync T3 가 더 낮은 원인 규명) 필요. 🟡→🟢 승격 경로.
3. **DECODER M3/M4b 3B production swap-in** — flame-P2b BPE round-trip ✅ unblock 후 본선.

## 7. 한계 (정직)

- **H_670 = 🟡 PARTIAL (5/6)**, 가짜 confirmed 아님. universal 핵심은 **inverse-U 신호(order floor + edge peak)**이지 full ECA monotone ordinal(I<II<III<IV) 사다리가 아님 — tier-번호 단조는 ECA-국소. logistic family 는 floor+peak 동형(PASS)이나 Kuramoto floor(F670.1) 깨짐.
- `pe_edge_of_chaos_peak` 의 숫자 상수 (edge skew=0.6, 정규화 denom) 는 **design-tunable convention** — substrate-derived 주장 아님. inverse-U 형상(order<edge>chaos)만 substrate-grounded.
- `pe_norm_convexity`(H_660 🟢 confirmed 단조)와 **tier 구분 명시** — 두 함수는 다른 verdict tier. 본 함수를 confirmed 로 인용 금지.

## 8. memory pointer

- `project_anima_emit_substrate_arc` — emit-substrate 2층 (구조 lib ⊥ 숫자 SSOT) round 6-9 검증 아크 + LIVE-WIRED 격상 (#1285/#1286).
- `reference_life_cycle_hexa_run_gotchas` — `hexa run` import-patch 함정 (canonical 절대경로 ↔ 워크트리 불일치).
- `feedback_no_branch_reuse_fresh_fork` — fresh-fork origin/main discipline.

## 9. 한 줄 시작 가이드

```sh
TMP=$(mktemp -d); for f in phi_envelope_substrate phi_envelope_substrate_smoke; do git show origin/main:CORE/$f.hexa > "$TMP/${f}.hexa"; done; perl -pi -e "s|import \"/Users/ghost/core/anima/CORE/phi_envelope_substrate.hexa\"|import \"$TMP/phi_envelope_substrate.hexa\"|" "$TMP/phi_envelope_substrate_smoke.hexa"; hexa run "$TMP/phi_envelope_substrate_smoke.hexa"   # → 17/17 PASS
```
