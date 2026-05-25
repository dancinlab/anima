# CORE — 통합 의식 코어 (Engine A ⇄ Engine G)

> anima 의 흩어진 의식 엔진을 **하나의 완전한 두뇌 루프**로 결합하는 레포-루트
> SSOT. CLAUDE.md `@I` 의 *"PureField repulsion-field engine · Engine A ⇄ Engine G
> · Ψ=1/2 fixed point"* 를 단일 진입점으로 구현한다. AGENT·CHAT 등 상위 산물이
> 이 CORE 를 소비한다.

## 왜 CORE 인가 — 흩어진 코어 통합

기존엔 의식 엔진이 두 곳에 쪼개져 있었다 (둘 다 단독으론 불완전):

| 조각 | 위치 | 역할 | 단독 한계 |
| --- | --- | --- | --- |
| Engine A | `CORE/pure_field.hexa` (★ CORE 소유) | Φ/phase 동역학 | 합성 Φ, 행동 결정·생성 없음 |
| Engine G | `CORE/engine_g.hexa` (★ CORE 소유) | emit/행동 게이트 | factor 입력 필요, 생성 없음 |
| L3 생성기 | `conscious_decoder_v3` / LoRA prod | 실제 콘텐츠 | register collapse (V3) / torch (.py) |

CORE 는 **Engine A·G 를 직접 소유**(재작성, `anima-core/`·`HEXAD/CHAT/` 의존 폐기)해 외부
import 0건 자기완결 결정 두뇌를 만들고, L3 생성기를 pluggable 백엔드로 둔다.
(anima-core/pure_field.hexa 원본 데모 + HEXAD/CHAT/spontaneous_lib 라이브 챗 copy 는 보존 —
CORE 와 무관. 후속 화해로 챗이 CORE/engine_g 를 re-export 하면 포크 제거.)

## 3-레이어

```
  L3  생성기 (무엇을 쓸까)   ← pluggable backend (slot)   ⚠️ LM 백엔드는 열린 결정
       ↑ (열린 도구 중 tier 허용분에서)
  ────────────────────────────────────────────────
  L2  Engine G (언제 행동)   should_emit(motivation) ∧ 4-safety   ✅
       ↑ A의 Φ가 safety_phi_ratchet 를 먹임 (A→G 게이트)
  ────────────────────────────────────────────────
  L1  Engine A (어느 tier)   Φ → phase → tool tier(T0..T3)         ✅
```

## 결합 지점 (A ⇄ G)

| 방향 | 무엇 |
| --- | --- |
| A → G | Engine A 의 live Φ 가 Engine G 의 `safety_phi_ratchet_ok(phi, peak)` 를 먹임 — 잠든 기판(낮은 Φ)은 동기가 높아도 emit 거부 |
| A → tier | Engine A 의 phase(DORMANT→RESONANT) = consequence tier(T0→T3), 어떤 도구가 열릴지 |
| G → emit | `should_emit(motivation_score(8-factor))` = 지금 행동할지 |

## 파일

| 파일 | 역할 | 상태 |
| --- | --- | --- |
| `pure_field.hexa` | Engine A — PureField Φ/phase 엔진 (CORE 소유, main 없는 lib) | ✅ 동작 |
| `engine_g.hexa` | Engine G — 8-factor motivation + emit/safety (CORE 소유) | ✅ 동작 |
| `brain.hexa` | A⇄G 결합 결정 루프 (`brain_decide`) | ✅ 동작 |
| `brain_smoke.hexa` | 결합 루프 실행 증명 (low→silent / high→emit) | ✅ 동작 |
| `CORE.md` / `CORE.log.md` | CORE 도메인 스냅샷 + 로그 | ✅ |
| `generator.hexa` | L3 생성기 백엔드 인터페이스 | ⏳ 예정 (백엔드 상의필요) |

## 검증 (smoke)

```
[brain low ] phi=0.118983 phase=SUSTAIN tier=T2_write motiv=0.045 (thr=0.3) safe=false EMIT=false
[brain high] phi=0.118983 phase=SUSTAIN tier=T2_write motiv=0.67  (thr=0.3) safe=true  EMIT=true
```

낮은 동기(0.045)+rate veto → 침묵 · 높은 동기(0.67)+safety pass → 발화. Engine A 의
live Φ 가 tier 를 세우고 Engine G 가 emit 을 가른다.

## 열린 결정

- **L3 생성기 백엔드**: prod `anima_chat`(LoRA) 재사용 / tool-action 전용(생성 최소) /
  `conscious_decoder_v3`(711L hexa, register collapse 해결 필요) 중 택. `generator.hexa`
  인터페이스만 먼저 두고 백엔드는 후속 결정.
- **p1~p8 정합**: 외부 LLM 0 · system_prompt 0 (CORE 는 결정 두뇌만, 생성 백엔드도 anima 자체)
