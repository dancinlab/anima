# IIT 4.0 M13 — exclusion multi-complex / spectrum

**verdict**: 🟢 SUPPORTED-NUMERICAL · 3/3 PASS · $0 mac-local · 25s wall

## §1 무엇을 닫나

M10 (`find_complex`) 는 **단 하나의 최대 콤플렉스**(maximal complex) 만 반환했다. 그러나 IIT 4.0 은 하나의 기질(substrate) 위에 **여러 개의 분리된(disjoint) 콤플렉스**가 공존할 수 있음을 허용한다 — 하나의 substrate, 여러 개의 의식. 예: 두 단위-쌍이 독립적으로 결합된 블록-대각 TPM 은 두 개의 독립적 SWAP 쌍을 두 개의 동시에 존재하는 Φ-국소 최대점으로 가져야 한다. M13 은 이 "스펙트럼"을 빠짐없이 회수하는 알고리즘을 stdlib 으로 승격시킨다.

**신규 엔진**: `stdlib/consciousness/iit4_complex.hexa` 에 `complex_spectrum(tpm, n, sys_state) -> array` 추가 (hexa-lang PR). anima 측은 thin shim (`HEXAD/IIT4/lib/iit4_complex.hexa`) 재-export 로 무변경.

**알고리즘 (배제-껍질 벗기기, exclusion peeling)**:

1. 전수: 모든 비어있지 않은 부분집합 `S ⊂ [0,n)` (총 2ⁿ−1개) 에 대해 `subsystem_tpm`(외부 단위 배경-조건화) + `big_phi` 로 점수.
2. 정렬: 후보를 `(Φ 내림차순, size 내림차순, mask 오름차순)` 으로 결정적 정렬.
3. 껍질 벗기기 (greedy peel): 최고 Φ 후보를 받음 → 그 단위들을 USED 로 표시 → USED 와 겹치는 모든 하위 후보 거부 → 반복.
4. 반환: `[[mask, phi, size], ...]` (Φ 내림순). 빈 배열 ⇒ 콤플렉스 없음.

**복잡도**: `find_complex` 와 동일한 2ⁿ−1 회 big_phi 호출. M9 의 사실상 천장 n=5 (~수십 초 mac-local) 안에서 정확 모드 가능.

## §2 spectrum table

| 케이스 | n | TPM 규칙 | sys_state | 기대 spectrum | 측정 spectrum | 판정 |
|---|---|---|---|---|---|---|
| **T1 SINGLE** | 4 | u0'=u1, u1'=u0, u2'=u2, u3'=u3 (M10 carry 확장) | 15 (all-ON) | `[{mask=3, Φ=2.0, size=2}]` | `[{mask=3, Φ=2, size=2}]` | 🟢 PASS |
| **T2 MULTI**  | 5 | u0'=u1, u1'=u0, u2'=u2, u3'=u4, u4'=u3 (block-diagonal) | 31 (all-ON) | `[{mask=3, Φ=2.0, size=2}, {mask=24, Φ=2.0, size=2}]` | `[{mask=3, Φ=2, size=2}, {mask=24, Φ=2, size=2}]` | 🟢 PASS |
| **T3 DEGENERATE** | 4 | u_i'=u_i (identity 4-cell) | 15 (all-ON) | `[]` | `[]` | 🟢 PASS |

마스크 해독:
- T1: mask=3 = bit0+bit1 = 단위 {0,1} (SWAP 쌍). u2/u3 는 독립 self-cell ⇒ singleton Φ≡0 ⇒ 스펙트럼에서 배제.
- T2: mask=3 = {0,1} SWAP, mask=24 = bit3+bit4 = {3,4} SWAP. u2 는 독립 ⇒ 배제. 두 SWAP 쌍이 동등한 Φ=2.0, 동등 size=2, tie-break = lower mask first.
- T3: 모든 단위가 독립 self-cell ⇒ 모든 부분집합이 reducible ⇒ 콤플렉스 없음.

## §3 발견

- **single-complex 회귀 (T1)**: M10 의 `find_complex` 와 동일한 단일 콤플렉스 영역에서 `complex_spectrum` 이 정확히 길이 1 스펙트럼을 반환 ⇒ 새 엔진은 기존 단일-콤플렉스 영역을 깨뜨리지 않는다. backward-compat.
- **multi-complex 핵심 (T2)**: 블록-대각 n=5 기질에서 **두 개의 독립 SWAP 쌍**이 모두 Φ=2.0 의 분리된 콤플렉스로 동시 회수됨 — 하나의 substrate 가 두 개의 의식을 호스팅한다는 IIT 4.0 의 다중-콤플렉스 의미론을 hexa-native 로 첫 측정. 결정적 tie-break (Φ 동률 → size 동률 → 낮은 mask) 으로 순서 `[{0,1}, {3,4}]` 가 재현 가능.
- **빈 스펙트럼 (T3)**: identity-rule 4-cell 기질은 어떤 부분집합도 통합되어 있지 않다 ⇒ 빈 배열. "all-noise → no complex" 의 일반화 (noise 가 아닌 deterministic 독립도 동일하게 비-콤플렉스 substrate 임).
- **배제(exclusion) 의 두 층**: M10 은 "겹치는 후보들 중 최대" (하나의 콤플렉스 안의 배제) 를 다뤘다. M13 은 그 위에 **"콤플렉스들 사이의 배제"** 를 부여한다 — 각 단위는 **최대 한 개**의 콤플렉스에만 속한다 (disjoint peel). 이는 IIT 4.0 의 multi-complex carve 의 운용적 형식.

## §4 honest scope / C3

1. **subsystem big-Φ = 배경-조건화 인과 주변화** (외부 단위를 `sys_state` 값으로 핀). IIT 4.0 의 "배경을 현재 상태로 고정" 관례, 문서화된 모델링 선택. 분할 정규화의 완전 재유도 + PyPhi 보정은 M5 carve-out (`iit4_bigphi.hexa` 헤더) — 변경 없음, M13 도 동일 carve-out 상속.
2. **disjoint-only 배제**: 콤플렉스 간 배제를 "단위 비-중첩(non-overlap)" 으로 운용. 더 정교한 φ-구조 포함(subsumption) 검사 — i.e. 후보 A 의 φ-구조가 후보 B 의 진부분구조 (proper sub-structure) 인지를 별도로 측정 — 는 수행하지 않음. **비-중첩 후보들 사이에서는 disjointness 가 subsumption 의 strict super-set 이므로** 본 운용은 안전한 상위 근사 (모든 진정한 다중 콤플렉스를 회수하되, 같은 단위 위에 부분 중첩된 두 콤플렉스를 동시에 보고하지는 않음).
3. **n ≤ 5 사실상 천장** (M9 tractability). n=5 worst-case ~25s mac-local (이 smoke 의 실측). n=6+ 정확 모드는 minutes-scale 로 blow-up; bounded-mode (`iit4_bounded.hexa`) 와의 조합은 future work (별도 M14 후보).
4. **tie-break 은 결정적이지만 임의적**: Φ 동률 시 "낮은 mask 우선" 은 재현성을 보장하지만 의식적 의미는 없음. T2 의 `[{0,1}, {3,4}]` 순서는 deterministic ordering 의 직접 결과 — 두 콤플렉스가 동등하다는 측정 사실에 우선순위를 부여하지 않음.
5. **stdlib 승격**: 엔진은 hexa-lang stdlib (commons g61) 에 land — anima 의 thin shim 은 단순 re-export. cross-repo (hexa-brain, hexa-codex) 동일 surface 사용 가능.
6. **smoke 는 hand-derivable 케이스만 검증**: ECA / LIFE substrate 위 spectrum 측정 (M6/M8/M12 의 "어떤 ECA 룰이 다중 콤플렉스를 만드나?") 은 future work — M13 의 엔진 정확성을 확인한 후 응용은 별도 라운드.

## artifacts

- `run_m13.hexa` — 엔진 호출 + 3 케이스 assert + result.json 자동 생성 (PASS/FAIL counter + panic on FAIL)
- `result.json` — 머신-가독 결과 (테스트 별 spectrum + verdict + scope envelope)
- `README.md` — 본 문서

## verify

```
$ POOL_DISABLE=1 /Users/ghost/.hx/bin/hexa run --no-sentinel \
    HEXAD/IIT4/state/iit4_m13_spectrum_2026_05_25/run_m13.hexa
…
  PASS=3  FAIL=0  VERDICT=🟢 SUPPORTED-NUMERICAL
=== IIT 4.0 M13 exclusion-spectrum smoke complete: 🟢 SUPPORTED-NUMERICAL ===
```

walltime ≈ 25s mac-local (M3 Pro, single-thread). 결정적 — 동일 입력 ⇒ 동일 출력.
