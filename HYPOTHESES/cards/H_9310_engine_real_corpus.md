# H_9310 — engine-native 실코퍼스: shrinkage faculty 가 REAL KO 자모 스트림에서도 발화하는가

**Tier: 🔵 ENGINE-NATIVE ON REAL CORPUS (R1 ∧ R2 · CALIB byte-exact) · group MITOSIS-ENGINE · 2026-07-14**

- freeze → `state/h9310_engine_real_corpus/FREEZE.txt` · script → `h9310_real_corpus.py`
- result → `state/h9310_engine_real_corpus/results/{h9310_result.json, run.log}`
- 선행 → H_9309 🔵 (배선 · 단 smoke 가 **toy 합성 스트림**) · H_9298/H_9301 🟢 (미러) · H_1321 🟢 (engine-native 앵커)

## 왜 (H_9309 의 정직한 미완을 닫는다)

H_9309 는 faculty 를 live `core/engine_cli` 에 배선하고 두 bar 를 통과시켰지만, 그 smoke 는 **toy 합성 스트림**이었다(카드에 명시). 남은 질문: **실제 코퍼스에서도 같은 것을 내는가?**

## 설정 (H_1321 engine-native 앵커와 동일)

REAL KO 30MB 창 · sha `c47b6808…` (H_1307 RUN A / H_1316 / H_9298 과 **byte-identical**) · **Vj=323** · `ko_stride=2500` (H_1321 의 CPU-tractable 창) · dim-3 특징 · even/odd held-out · 지표 = **nats/UTF-8-byte**. 두 arm 모두 **live 엔진 faculty 호출**(사설 프로브 아님).

## CALIB (BLOCKING · 주 bar 판독 前)

| 게이트 | 앵커 | in-run | |
|---|---|---|---|
| C1 코퍼스 sha | `c47b6808…` | 일치 | ✅ |
| C2 자모 어휘 | Vj **323** | 323 (distinct jamo 67) | ✅ |
| **C3 FLAT arm CE** | **2.82046** (H_1321 W1) | **2.82046** | **d = +0.00000** ✅ byte-exact |

⇒ 포트가 H_1321 의 engine-native 측정을 **정확히** 재현한다. 계측 무죄.

## 결과 — 🔵 R1 ∧ R2 (scored 10,201 · train 5,101 / test 5,100 · $0 summer · wall 24.4s)

| arm (live faculty) | cells | CE (nats/byte) |
|---|---|---|
| **FLAT** `jamo_head_grow` (H_1321 검증 경로) | **10** | **2.82046** |
| **SHRINK** `jamo_head_grow_shrink` (H_9309) | **40** | **2.71886** |

- **R1 GROWTH-UNCAPPED ✅** — 실제 자모 스트림에서 기존 faculty 의 셀 풀이 **10 개에 갇혀 있었다**. 수리하니 예산(grow_max=40)까지 도달. ⇒ **퇴화분할 캡은 toy 아티팩트가 아니라 실코퍼스의 사실이다.**
- **R2 SHRINKAGE-HELPS ✅** — **−0.10160 nats/byte** (bar −0.02). 미러의 shrinkage 이득이 engine-native 로 전이된다.

## HONEST

- SHRINK 가 **예산 상한(40셀)에 도달**했다 ⇒ 더 크게 하면 더 갈 수 있으나 이 카드는 사전등록한 예산에서만 판독한다(사후 확장 = tune-to-green).
- 절대 CE 는 **stride 2500 창에 한정**(H_1321 과 동일 스코프). 미러의 절대값(2.51335 · 2.45205)은 stride 300 이라 **직접 비교 금지**(`a_scale_honest_scope`) — 이 카드는 **같은 창 안에서 FLAT vs SHRINK** 만 비교했다.
- **경계 불변**(H_9306): shrinkage 는 분할이 파괴한 분산을 되살 뿐 **정보를 만들지 않는다**. 이 결과는 추정기 결함이 실코퍼스에서도 실재했음을 보일 뿐, **능력 주장이 아니다**.
- py 2-production engine (`a_eval_py_canonical` ⇒ TERMINAL-eligible) · bar 이동 0.
