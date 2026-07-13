# NBIND-G N2 — 측정 결과 (2026-07-13 · verdict 미확정)

동결 스펙 = [`N2_STATUS.md`](N2_STATUS.md). 판정표·게이트는 **데이터 전에 고정**됐고 여기서 바꾸지 않는다.
원본 채점 JSON 전량 = [`N2_EVAL/`](N2_EVAL/) (tail 절단 금지 · `evaluate-py-1`).

## 4-arm 학습 (T=105,169 step · rent ~$21 owner go)

| arm | seed | 학습 | ckpt 회수 |
|---|---|---|---|
| main-s7 | 7 | ✅ 완주 | ✅ |
| main-s11 | 11 | ✅ 완주 | ✅ |
| base_only | 7 | ✅ 완주 | ✅ |
| shuffle_grid | 7 | ⏳ 67% (summer) | — |

## 🔴 동결 유효성 게이트 (a) — main seen P_grid D-acc ≥ 0.85

| arm | seen D-acc (n=80) | 판정 |
|---|---|---|
| main-s7 (seed 7) | **0.950** | ✅ PASS — grid 설치 확인 |
| main-s11 (seed 11) | **0.725** | ❌ **FAIL = under-exposed INVALID** (동결 스펙 §4(a)) |

**seed 11 은 격자 연산자를 bar 까지 설치하지 못했다.** 따라서 그 arm 의 held-out 수치는
"전이 실패"가 아니라 **해석 불가**다 — 없는 연산자의 전이는 물을 수 없다.

⚠️ 코퍼스·T·f_grid 가 **동일**한데 seed 만 달라 0.950 vs 0.725 로 갈렸다 ⟹ 동결 레시피에서
**grid 설치 자체가 seed-fragile**. V5 seed-robustness 게이트가 정확히 이걸 잡으라고 있던 것.

## held-out D-acc (n=174 · 완전판 rows · gen=8 win=64)

Δ 는 동결 스펙대로 **`max(control, 0.50)` 대비** — 우연 바닥 0.50 이 하한.

| arm | D-acc | Δ vs 0.50 | flip0 (부정없음·극성만) | flip1 (부정있음·XOR) |
|---|---|---|---|---|
| **main-s7 (seed 7 · 유효)** | **0.477** | **−0.023** | **0.402** | 0.552 |
| main-s11 (seed 11 · INVALID) | 0.316 | −0.184 | 0.391 | 0.241 |
| base_only | 0.000 | −0.500 | 0.000 | 0.000 |
| shuffle_grid | ⏳ | | | |

**`base_only = 0.000` 은 유효성 파탄이 아니다.** filler 만 본 모델은 `긍정.`/`부정.` **형식 자체를
못 낸다**(극성을 틀리는 게 아니라 그 어휘를 출력하지 않음). 동결 스펙이 Δ 바닥을 `max(control, 0.50)`
으로 미리 고정한 이유가 이것이다.

## 읽기 (동결 판정표 §5) — **verdict 미확정**

유효한 seed(7) 하나만 놓고 보면:
- **NAT-CRACK 🟢 미충족**: Δ = −0.023 ≪ +0.20. held-out 이 우연 미만.
- **flip 분해가 벽을 지목**: flip0 = **0.402 < 0.50** ⟹ 동결표의 `flip0 낮음 = **GROUNDING-🧱**`.
  격자 XOR 연산자는 설치됐는데(seen 0.950) held-out 자연 원자의 **극성 자체가 미접지** =
  연산자가 적용될 좌항이 없다. H_9286 의 "grounding = DATA-blocked" 와 같은 방향.

**그러나 박지 않는다** — 동결 게이트가 두 곳에서 미충족:
1. **gate (a) seed 11 FAIL** ⟹ gate (d) "2 seed 동일측 bar" 를 **평가할 수 없다**.
   한 seed 로 벽을 선언하는 것은 금지(사전등록 2-seed 요건 · 음성주장은 TOST 로 벌어야 한다).
2. **shuffle_grid 미완(67%)** ⟹ `format-without-operator` 대조 부재 ⟹
   **GROUNDING-🧱 과 FORMAT-🧱 을 구분할 수 없다**.

⟹ 현 상태의 정직한 라벨 = **INVALID (게이트 실패 · 동결 스펙 §5)**, 방향 증거는 GROUNDING-🧱.
bar 를 내려 통과시키는 것은 tune-to-green 이므로 금지.

## 재개 조건 (verdict 를 벌려면)

1. **shuffle_grid 완주** → coin-seen ≥ 0.85 (control liveness) + held-out. ($0 · summer · ~3h)
2. **seed 11 의 grid 설치 실패 해소** — 동결 스펙의 remedy 는 "under-exposed" 이므로 **노출 증가**
   (T 상향)이지 seed 교체가 아니다(사후 seed swap = 프로토콜 변경 금지). 비용/경로는 1 착지 후 결정.

## 측정 인프라 (판정과 격리 · `infra-wall-noneval`)

- 렌트 pod(192-thread EPYC)는 **다른 임차인이 load average ~106 으로 포화** → 항목당 12분+
  (전용 호스트 4.3 s/item 의 **170배**). 174문항 채점이 5시간 동안 진행 줄 0개.
  ⟹ 채점 전량 summer(12코어 5.4GHz · load ~2)로 이전, arm 당 ~10분 착지. pod 파기(과금 중단).
- 그 침묵의 근본원인 = `--xbind` 가 25문항마다만 진행을 찍은 것 → **1번 항목 하트비트 + s/item + eta**
  로 수정(0.13.11 · convergence `evaluate-py-9`).
- pod 의 cupy 는 `libnvrtc.so.12` 부재로 커널 컴파일 실패 → GPU 경로가 발화 후 즉사.
  capability 게이트를 커널-스모크로 정직화(0.13.10 · convergence `decode-py-1` 확장).
  채점은 canonical numpy 경로(TERMINAL-eligible)라 측정 손실 0.
- **파이프라인 독립 재현 확인**: main-s7 을 내 경로로 재채점하니 seen 0.9500 / held-out 0.4770 —
  다른 세션의 독립 측정치와 소수점 4자리까지 일치.
