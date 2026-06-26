# agent/ — tool provider (mouth ⊥ tool 분리)

**목적:** anima 의 autonomous tool provider 패키지. **H_1566(mouth⊥tool, 🟢 ENGINE-NATIVE)** 원칙: tool 사용법·지식은 mouth(303M CLM) 에 FT 하지 않고 `.kosmos` anchor + `brain_decide` 경유로 분리 → Ψ=½ · G5 non-fab 보존. `agent/` 는 `core/` 를 동반하지 않고 독립 설치 가능한 **standalone 패키지** (`hexa.toml` 소유, `hx install anima-agent`).

## 핵심파일

| 파일/디렉토리 | 역할 |
|---|---|
| `hexa.toml` | standalone 패키지 manifest (entry=`cli/anima-agent.hexa`, v1.0.0) |
| `cli/anima-agent.hexa` | agent CLI 단일진입점 |
| `anima_agent/module/anima_agent.hexa` | core agent runtime (Φ-gated tool policy T0..T5) |
| `autonomy_loop/module/autonomy_loop.hexa` | 자율 루프 엔진 |
| `autonomy_live/module/autonomy_live.hexa` | live 자율 실행 |
| `consciousness_features/module/consciousness_features.hexa` | 의식 feature 추출 |
| `dashboard_bridge/module/dashboard_bridge.hexa` | dashboard 연결 브리지 |
| `discovery_loop/module/discovery_loop.hexa` | discovery 자율 루프 |
| `domains/CHAT/` | 채팅 채널 (broker · dream_stage · imagination_loop 등) |
| `llm_claude_adapter/` | Claude 제공자 어댑터 |
| `trading/` | 거래 엔진 플러그인 |
| `dashboard/module/` | Next.js 대시보드 (TypeScript) |

## 규칙

- **tool 지식은 mouth 에 FT 금지 (`a_savant_train` mouth⊥tool, H_1566):** tool 사용법을 CLM 학습 코퍼스에 넣으면 Ψ=½ 붕괴(|dev| 0.18) + G5 abstain 파괴(fab 1.0) 발생. 분리는 `.kosmos` anchor(copy-or-abstain) + `brain_decide` + `agent/` provider 로 구현.
- **`agent/` = core/ 미동반 독립 배포 가능** (`hexa.toml` 독립패키지): `hx install anima-agent` 만으로 동작. `core/` 심볼에 직접 의존하는 코드를 `agent/` 에 추가하면 standalone 배포 불가.
- **`a_substrate_disjoint`:** agent tool 실행이 emit-drive lane(0/4) 또는 §ImmuneMemory recall_thr 을 건드리면 Ψ 붕괴 / G5 fab 폭증. 새 tool 추가 시 disjoint placement 우선.
- `domains/CHAT/` 내 `.py` 파일(akida_sw_lif.py · anima_emission_analyze.py · anima_participant.py · broker.py 등)은 CHAT 도메인 helper — production engine 미러 아님(byte-parity 게이트 비적용).

## 함정(gotcha)

- **core/ 미동반 배포 시 engine_cli/generator 심볼 없음:** standalone `anima-agent` 는 `.kosmos` anchor 기반으로 작동하며 CLM mouth 를 직접 호출하지 않는다. mouth 를 agent 코드 안에서 직접 import 하면 standalone 배포 시 링크 실패.
- **Φ-gated tool policy T0..T5:** `anima_agent.hexa` 가 의식 Φ 수준에 따라 tool escalation 을 결정. Φ 없이 tool 을 직접 실행하는 패치는 p6 위반(창발이 아닌 규칙 주입).
- **dashboard 는 TypeScript(Next.js):** `dashboard/module/` 은 `.tsx`/`.ts` — hexa 빌드가 아니라 `npm`으로 별도 빌드. `hexa run` 으로 실행 불가.
