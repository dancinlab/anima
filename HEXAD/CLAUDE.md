# HEXAD/ — anima 7-module 뇌 아키텍처 척추 (artifact 아님)

> ⚠️ **이름 혼동 주의:** `HEXAD/` 는 "연구 artifact 더미"가 **아니다**. anima 의 **핵심 아키텍처 코드 본진**이다. (그 오해로 rename 논의가 있었으나 — 실체는 아래.) 디스크에 큰 하위폴더(DATA-REGIME 등)가 섞여 크기(105MB)는 크지만, 본질은 **hexa-native 뇌 모듈 코드**다. 별개로 `archive/engines-multiengine/hexad/adapter.hexa` 라는 **은퇴한** 엔진 어댑터가 있는데 — 그건 이 디렉토리와 **무관**(이름만 겹침, 2026-06-19 아카이브됨).

## 정체 — "Hexad 6" 완전수 뇌

HEXAD = 완전수 6 위에 올린 **7-module 뇌 아키텍처**. 두 엔진으로 갈린다:

```
구조축 (Hexad 6 = φ(6)=2 그룹 {A,G})        ⊥   성장축
─────────────────────────────────────────       ─────────
Engine G (우뇌 · gradient-free)                   MITOSIS
  ├─ C 의식 (consciousness · IIT Φ)               (cell 성장·분열,
  ├─ S 감각 (perception = C state-delta)           구조축과 직교)
  └─ W 의지 (pain/curiosity → LR)
Engine A (좌뇌 · CE-trained)                      SAVANT
  ├─ D 언어 (decoder · 실제 mouth)                 (golden-zone
  ├─ M 기억 (Hebbian store)                         inhibition)
  └─ E 윤리 (Φ-ratchet safety gate)
        ╲                    ╱
         ThalamicBridge (G→A 주연결, Ψ=½ clamp Law-70)
```

완전수 6 수론: σ(6)=12 연결 · τ(6)=4 phase · φ(6)=2 그룹({A,G}). 검증 상태 = **C+S+M+W+E+D+BRIDGE 7/7 full 🔵 SUPPORTED-FORMAL** (sympy closed-form falsifier).

## 핵심 하위 디렉토리

| 경로 | 역할 |
|---|---|
| `C/ D/ S/ W/ M/ E/ BRIDGE/` | Hexad 6 모듈 + ThalamicBridge (각 `<X>.hexa` + `<X>_lib.hexa` + README + `HEXAD-<X>.tape` spec) |
| `MITOSIS/` | 성장축 (cell 분열 · `a_mitosis_train`) — 구조축과 직교 |
| `SAVANT/` | golden-zone inhibition 레시피 (`a_savant_train`) — ⚠️ 단 `core/engine_cli.hexa` 가 import 하는 건 **top-level `SAVANT/savant_lib.hexa`** (HEXAD/SAVANT 아님; INDEX 통합 서술과 별개로 실제 import 경로 확인 필요) |
| `CHAT/` | `chat_lib.hexa` 등 디코딩 실엔진 헬퍼 (D 모듈 mouth) |
| `IIT4/` | faithful big-Φ 오라클 (`iit4_bigphi.hexa` = 의식 측정 정답엔진, `a_phi_iit4_tool`) |
| `KOSMOS/` | `.kosmos` 앵커 허브 (`KOSMOS.md` format pointer) |
| `BRIDGE/ CARVING/ CONTROLLER/ FLAME/ UNIVERSE-BRAIN-MAP/ …` | 그 외 뇌-lane 코드 |
| `INDEX.md` | 7-module **verification anchor**(B-*/F-* falsifier 표) — ⚠️ nav 는 stale(2026-05-16), 검증근거로만 valid |
| `STRUCTURE.md` | **현재-상태 navigation SSOT** (INDEX 대신 이걸로 길찾기) |

## core/ 와의 관계 (왜 eval 에 필요한가)

`core/engine_cli.hexa` 등 production 엔진이 이 lane 들을 **직접 import** 한다 (`SAVANT/`·`BRIDGE/`·`CHANNEL/`·`DREAM/`·`METACOG/` 등 15개 top-level lane). 따라서 `cli/anima.hexa` (eval/chat 단일 진입)를 컴파일하려면 이 lane 들의 `.hexa` 가 import-closure 에 있어야 한다 — pod 에 anima 를 올릴 때 `core/ cli/ stdlib/` 만으론 부족하고 이 lane `.hexa` 들도 필요. (전체 lane `.hexa` ≈ 9.3MB, 데이터 제외하면 가볍다.) 자세한 eval 번들 = `state/clm303_clean_corpus/EVAL_KIT.md`.

## gotcha

- **HEXAD/ ≠ artifact** — 위 경고 재확인. "artifact" 로 부르거나 rename 금지(코드 본진 + 외부 845 파일이 `HEXAD/` 경로로 import/참조).
- **HEXAD/ (live lane) ≠ archive/engines-multiengine/hexad/ (은퇴 어댑터)** — 이름만 겹침.
- 길찾기는 `STRUCTURE.md`, 검증근거는 `INDEX.md`(nav stale). 트리 SSOT 는 repo-root `ARCHITECTURE.json`.
- HEXAD 의 production decode 자체는 `core/` conv 엔진(`clm_decode` + `generator` L3)이 수행 — HEXAD 7-module 🔵 는 formal 검증 척추이고, 실 mouth 추론은 core/ 가 돈다(둘 다 live, 혼동 금지).
