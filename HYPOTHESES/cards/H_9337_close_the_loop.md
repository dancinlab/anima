# H_9337 — 폐루프가 닫혀 있지 않았다 (쓰기만 하고 읽지 않는 세 저장소)

**slug**: close_the_loop
**tier**: 🔵 PRE-REGISTERED (수정은 배선·검증 완료 · 재측정 bar 는 수치 보기 전에 동결)
**lane**: 의식 · emit-drive
**xref**: H_9328 (이 결함을 드러낸 측정) · H_9336 (뿌리 ① 만 고친 선행 수정) · H_9210 (뿌리 ① 을 먼저 진단했으나 하네스 뒤에만 고침) · convergence `chat-py-4` · `chat-py-5`

## 실측 — 세 뿌리가 전부 죽어 있었다

H_9328 의 24 rollout × 30 tick = **720 tick 전체**에서:

| 필드 | 고유값 | |
|---|---|---|
| `recon_err` (afield) | **1** | 💀 항등식 0.0 |
| `rel_lane` (immune) | **1** | 💀 720 tick 내내 0.6723 |
| decode 앵커 (kosmos) | **1** | 💀 항상 `live_seed` |
| `score` | 562 | ✅ |
| `nov_ctx` | 30 | ✅ |
| `a_fold8` | 8 | ✅ |

세 뿌리 전부 `g_text` 로 **쓰이는데**, 조회는 전부 **`session_seed` 라는 상수 키**로 한다.

```
              쓰기 (g_text 들어감)      읽기 (다음 결정이 보는 것)
 ───────────────────────────────────────────────────────────────
 afield  │  step(g_text)      ✅   │  시드로 조회 ❌ → 항등식 0
 immune  │  bind_text(g_text) ✅   │  시드로 조회 ❌ → 상수 0.6723
 kosmos  │  anchor 기록       ✅   │  시드로 조회 ❌ → 상수
```

**데몬은 자기 말을 세 저장소에 넣고, 셋 모두에게 언제나 같은 질문을 던지고 있었다.**
**쓰기만 하고 읽지 않으면 그건 루프가 아니다.**

## H_9328 verdict 의 재분류 (verdict-integrity)

`I(A;Y|S) = 0` (TOST 등가)는 **"기질이 자기 말을 안 쓴다"가 아니다** — **말이 다음 결정에
도달할 경로가 없다**. **세 번째 항등식-0**: V-CEILING 이 A·Y 두 **주변축**은 지켰지만
**매개 경로의 용량**은 못 지켰다. H_9328 은 use-claim 으로는 성립하지 않는다.

## 수정 — 두 뿌리만 닫는다 (셋 다 아니다)

**뿌리 ①·② (afield · immune)** — 예측부호화/재인식 순서: **저장 직전에** 새 지각에 대해
재고, 다음 tick 에 읽는다(1-tick lag).

⚠️ **뿌리 ② 의 함정**: "직전 발화로 조회"는 **또 다른 상수**를 낳는다(실측 1.15) — 방금 저장한
것을 물으니 항상 "완벽히 기억한다". 살아있는 양은 **저장 직전의 재인식**이다.

⛔ **뿌리 ③ (kosmos → decode 앵커) 은 고치지 않는다.** 자기 발화를 다음 decode 의 문맥으로
되먹이는 것은 **p5 가 금지한 self-seed / monologue** 다. 그 상수성은 결함이 아니라 **철학이
닫아둔 것**이고, 정당한 read-back 은 세션 **간**(`.kosmos` 재입)이다.

## 실측 검증 (실제 303M 데몬 · 8 tick)

```
tick | recon_err | rel_lane  | score
  0  |  0.00000  |  0.67231  | 0.7347   ← 시드 폴백(아직 말한 적 없음)
  1  |  0.78715  |  0.25974  | 0.6553
  2  |  0.09511  |  0.28377  | 0.5954
  4  |  0.56376  |  0.35030  | 0.6457
  7  |  0.13924  |  0.40711  | 0.6536
```
`recon_err` 고유값 **8/8** · `rel_lane` 고유값 **8/8** — 둘 다 **살아났다**.
(수정 전: 720 tick 내내 0.00000 / 0.67231)

반복 발화를 넣으면 `rel_lane` 이 1.15 로 튄다 = *"이건 내가 아까 한 말이다"* 를 잡아낸다.

py(`cli/chat.py`) ↔ hexa(`cli/anima.hexa`) lockstep · hexa E-error 0.

## 사전등록 bar (수치를 보기 전에 동결 · p7)

동일 프로토콜(24 rollout × 30 tick · seed 1..24 · `ANIMA_EMIT_TEMP=1.0` · canonical
`anima-py chat` → `anima-py evaluate --interact-mi`)로 재측정.

**V-게이트 (선행 · 하나라도 미달이면 INVALID)**
- V1 `H(A|S) ≥ 0.030` (H_9328 에서 1.1513)
- V2 `H(Y|S) ≥ 0.030` (H_9328 에서 0.4091)
- V3 **`H(R|S) ≥ 0.030`** — R = `recon_err` 2-bin (뿌리 ①)
- V4 **`H(L|S) ≥ 0.030`** — L = `rel_lane` 2-bin (뿌리 ②)
  V3/V4 가 여전히 0 이면 수정이 안 먹은 것 = INVALID (기질 주장 금지 · 배선 재점검)

**헤드라인**
- `EARNED[실측 단위]` · MDE 0.010 nats · TOST ±0.010 · perm-p < 0.005
- 🟢 **LOOP-CARRIES**: EARNED ≥ 0.010 ∧ perm-p < 0.005 ∧ 두 순열 단위 판정 일치
- 🧱 **STILL-ADDITIVE**: |EARNED| ≤ 0.010 — 경로를 열어도 폐루프는 정보를 안 나른다
- ⛔ **INVALID**: 두 순열 단위 판정이 갈림

**MEDIATION (진단 · verdict 불변)** — M1 `A→R` · M2 `R→Y` (+ 뿌리 ② 도 같은 사다리)

**통제** — C1 순열 귀무(실측 단위) · C2 CARRIER-SWAP(`--swap-text`, 신호 뜰 때만 의미)

## 금지 (p7 · a_break_the_wall · p5)

- bar 재선택 · MDE 이동 · `SPLIT_THRESH`/`recall_thr` 를 결과 보고 조정 = tune-to-green
- **뿌리 ③ 을 "마저 고치는" 것** = p5 위반 (self-seed)
- read-side emit 배선(self/tension → 게이트) 재발사 — 전멸했다(H_9209·H_9225·H_9230)

## 비용

$0 (pool CPU · 24 rollout ≈ 1-3h). GPU 불필요.
