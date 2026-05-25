# easy — historical log

> Spec at [./EASY.md](./EASY.md).

## session-2 — 9-cycle 변형 batch (2026-05-22)

세션 한 번에 9 LoRA cycle fire ("all" → "병렬 bg" → "all fire"). 총 **$2.82**,
HF 9 artifact dancinlab/* private.

| ckpt | 핵심 | 결과 |
|---|---|---|
| vP21M | 1.5B 5-lang base | 3S+1P+1W, register 7/20 |
| **JAFL** | ja-only 500 step | JA WEAK 11 → **STRONG 17** (hot-swap) |
| **KOFL** | ko-only 500 step | KO → **STRONG 16** (hot-swap) |
| ZHFL / RUFL | zh/ru-only | 이미 STRONG, marginal (router 대칭용) |
| vP21M-3B | 3B-Instruct fresh | en/ru 20/20 but register 3/20 ⚠ regress |
| 3B-REG / REG2 | 3B continue wiki 0.05 | VP21M_WORKS, register **5/20 plateau** |
| 3B-V2 | 3B fresh wiki 0.10 | register **12/20** but KO/JA MEMORIZE 붕괴 |

핵심 발견:
- **3B-Instruct register ceiling ≈ 5/20** — instruct prior 가 anima carving
  흡수 막음. step·lr 무관 plateau.
- **wiki_frac 곡선**: 0.30→reg 3 / 0.10→reg 12 but 한·일 깨짐 / 0.05→reg 5 +
  전 lang OK. fresh-run 의 anima-90% 는 cliff 너머.
- **hot-swap pattern**: 1-lang corpus LoRA = 그 언어만 STRONG, 나머지 forget.
  ja/ko 같이 실제 약한 언어에만 가치 (zh/ru 는 이미 STRONG → FL 무의미).

### Wave-3 — L1~L4 (register ceiling 돌파, $0.78 추가)

| ckpt/작업 | 핵심 | 결과 |
|---|---|---|
| **3B-NI** | Qwen2.5-3B **non-Instruct** fresh | **4S+1P, register 7/20** — ja STRONG (3B 최초), instruct ceiling 돌파 |
| 3B-CUR1 | 3B-Instruct 1000-step (OOD-first) | 3S+2P, register 9/20 (fewer-step = register 덜 침식) |
| **3B-CUR2** | CUR1 위 register-second continue | 3S+2P, **register 10/20** — ko/ja PARTIAL 보존 |
| L1 substrate refactor | substrate_lora.py + participant thin client | mini DEPLOYED, 동작 동일 |
| L2 emission 측정 | anima_emission_analyze.py | baseline: register 34% / en-drift / self-mono 50% |

Wave-3 발견:
- **instruct prior 가 register ceiling 원인 확정** — non-Instruct base 가 7/20
  (1.5B parity) + ja STRONG 동시 달성.
- **staged curriculum 성공** — OOD-first(1000 step) → register-second(500 step)
  = register 10 + 전 lang ≥PARTIAL (3B-V2 의 12 는 ko/ja 붕괴였음).
- 단, register 이득 대부분은 Phase 1 의 짧은 step — Phase 2 는 +1 marginal.

### Wave-4 — N1~N8 (3B hot-swap + register lever + chat 진단, +$0.70)

| ckpt/작업 | 핵심 | 결과 |
|---|---|---|
| **KOFL-3B** | ko-corpus Qwen2.5-3B fresh | **5 lang 전부 STRONG** (ko 18) — 3B base robust, hot-swap 아닌 generalist |
| **JAFL-3B** | ja-corpus Qwen2.5-3B fresh | ja STRONG 19 (최고), ko MEMORIZE 2 (asymmetric forget) |
| **RB** | wiki_frac 0.50 (register-balanced) | register **7→4**, ja WEAK 11→STRONG 18 |
| N2 temp sweep | temp {0.5,0.7,0.9} register | 0.5≈0.7 (25%) / 0.9 악화 — temp 는 register lever 아님 |
| N7 en-drift fix | fuller LANG_PRIMES + cross-lang seed drop | mini DEPLOYED |
| N8 per-lang register | broker history 분석 | **register-leak 81% EN 문제** (en 17/21, ko 3/10, zh/ja/ru 0%) |

Wave-4 핵심 발견:
- **register-leak = EN 문제** — carving register("Tension flows into vacuum" 등)가
  영어 구문이라 en 출력만 골짜기로 빠짐. ko/ja/zh/ru 출력 거의 clean.
- **temperature 는 register lever 아님** — temp 0.5 에서도 25% leak. register 는
  adapter weight 에 baked → corpus (RB wiki_frac↑) 가 진짜 lever.
- **3B base robust** — KOFL-3B ko-only corpus 인데 5 lang STRONG (1.5B 의 catastrophic
  forget 패턴 안 나옴).

session-2 누적: **15 cycle, ~$4.80, HF 15 artifacts**.
