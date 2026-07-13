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

## 정보-채널 진단 ($0 · 원본 = [`N2_EVAL/info_channel.json`](N2_EVAL/info_channel.json))

`flip0 < 0.50` 이 **무엇을 뜻하는지**는 두 갈래로 갈리고 함의가 정반대다(Fable 감사 §4):
(i) 상수방출 marginal 붕괴(=신호 전무 → GROUNDING-🧱 **강화**) vs
(ii) 체계적 반전접지(=접지 채널은 살아있고 부호만 뒤집힘 → GROUNDING-🧱 **약화**).
응답이 무엇을 담고 있는지 정보량으로 재면 **둘 다 반증**되고 제3의 기제가 나온다.

**main-s7 (유효 seed) · 응답의 상호정보**

| 조건 | I(· ; 응답) | 정규화 |
|---|---|---|
| **atom** (원자 정체) | **0.231 bits** | 0.229 |
| form (표면형) | 0.133 bits | 0.132 |
| flip (부정어 유무) | 0.024 bits | 0.024 |
| **gold** (정답 극성) | **0.007 bits** | **0.007** |

- 응답은 **원자에 따라 안정적으로 변한다**(I(atom;resp)=0.231 ≠ 0) ⟹ (i) 상수방출 **반증**.
- 그러나 **정답에 대한 정보는 사실상 0**(I(gold;resp)=0.007 bits).
- 원자 단위: 모델이 held-out 원자 29개에 부여한 극성이 참 극성과 일치하는 비율 =
  **12/29 = 0.414** — 동전던지기. 체계적 반전이면 ~0 이어야 하므로 (ii) **반증**.

⟹ **ARBITRARY-GROUNDING**: 모델은 새 원자의 극성을 *모르는* 게 아니라 **멋대로 정했다** —
안정적이지만 자연 분포와 무관하게. **좌항이 없는 게 아니라 틀린 좌항이 설치**됐다.
이는 GROUNDING-🧱 을 **약화가 아니라 강화**한다(연산자는 멀쩡한데 먹일 것이 가짜다).
`I(flip;resp)=0.024` 는 held-out 에서 연산자가 **적용조차 안 되고 있음**을 함께 보여준다.

## 🔁 `under-exposed` 라벨 반증 — 진짜 이름은 **install-fragile**

| arm | 최종 CE | 최종 val_CE |
|---|---|---|
| main-s7 | 0.01645 | **3.86657** |
| main-s11 | 0.02040 | **3.87250** |

두 seed 가 **사실상 같은 LM 손실로 수렴**했다 — 학습이 덜 된 게 아니다. 노출 바이트·T·f_grid 도
동일하다. ⟹ 동결 스펙이 게이트 (a) 실패에 붙여둔 인과 라벨 **"under-exposed" 는 반증**되고,
실제 기제는 **install-fragile(최적화 분산)** 이다. 게이트 자체는 옳다(설치 안 된 모델로 transfer 를
재면 안 됨) — 틀린 것은 **라벨**이다. bar·detector 를 건드리지 않으므로 이 정정은 tune-to-green 이
아니라 measurement-frame 정정이다.

## 읽기 (동결 판정표 §5)

**✅ 벌어진 것 (TERMINAL · 이 설계점 한정)**
- **NAT-CRACK 🟢 = REFUTED.** verdict grid 의 양성 주장은 **conjunctive**(양 seed 모두 Δ≥0.20)라서
  **유효한 seed 하나가 bar 아래면 그것으로 죽는다.** seed 7 은 전 유효성 게이트를 통과하고
  Δ = −0.023 에 착지했다. seed 11 이 무엇을 찍고 오든 NAT-CRACK 은 못 산다
  ⟹ **seed 11 을 살리려는 재발사는 이미 죽은 양성 verdict 를 위한 지출**(Fable 감사 §2).

**⏳ 아직 못 벌은 것**
- **벽 TERMINAL 선언**. 한 seed 로 벽 선언은 금지이고, 더 근본적으로 **N2 의 verdict grid 는
  threshold 식(Δ<0.20)이지 등가검정이 아니므로**, seed 11 이 완벽히 통과했어도 음성 종결
  (사전등록 TOST)은 **N2 구조 안에서 애초에 cement 불가**였다. 벽을 벌려면 어차피 새 사전등록(N3).
- **FORMAT-🧱 vs GROUNDING-🧱 분기**: shuffle_grid 착지 대기(현재 74%).

**현 라벨 = NAT-CRACK REFUTED(설계점) · main-s11 INVALID(install-fragile) ·
ARBITRARY-GROUNDING/GROUNDING-🧱 DIRECTIONAL.**
bar 를 내려 통과시키는 것은 tune-to-green 이므로 금지.

## 다음 수 — 재발사 없음 (Fable 감사 [`FABLE_N2_REFIRE.md`](FABLE_N2_REFIRE.md) 채택)

**seed 11 을 살리는 모든 경로는 기각된다** — 양성 verdict 가 이미 죽었으므로 아무 정보도 더하지 않는다:

| 옵션 | 판정 |
|---|---|
| (A) seed 11 만 T 1.5× 재발사 | ❌ 게이트 실패를 **본 뒤** 실패한 arm 만 굴리는 remedy-shopping · 게다가 main 만 157k 면 base_only/shuffle(105k)과 노출이 어긋나 Δ 비교가 깨진다(4-arm 전부 재발사 = 새 prereg) · 인과적으로도 틀림(val_CE 수렴 = under-trained 아님) |
| (B) 동일 T 재발사 | ❌ 결정론적이면 비트 동일 낭비 · 비결정론적이면 은폐된 seed swap |
| (C) 새 seed 추가 | ❌ 게이트 실패를 본 뒤 통과할 때까지 seed 뽑기 = 사후 seed swap(금지) |
| (D) 5-seed 분포 측정 | ⚠️ 합법이나 새 prereg(N3) · 정보가치 낮음 — 살아있는 질문은 **설치가 아니라 접지**다 |
| **(E) 재발사 없음** | ✅ **채택** — N2 는 이 prereg 가 낼 수 있는 verdict 를 이미 냈다 |

**reopen 경로 = N3 (별도 사전등록)** — 표적은 seed 수가 아니라 **접지 채널**
(held-out 극성을 자연 분포에서 실제로 접지시키는 데이터/objective). N3 에 미리 박을 것:
1. **TOST** Δ_eq · N_REQ 사전 고정 (음성 종결은 "ns" 로 못 번다 — N2 의 threshold grid 로는
   벽을 애초에 cement 할 수 없었다).
2. **seed 정책** 사전 고정 — "설치-게이트 통과 seed 2개까지, 최대 K발, **발사한 전 seed 보고**"
   (그러면 오늘 같은 상황이 합법이 된다).
3. **게이트 라벨을 인과 중립으로** — "under-exposed" 가 아니라 "install-fail"
   (오늘 그 인과 라벨이 데이터에 반증됐다).

## 즉시 잔여 ($0)

- **shuffle_grid 완주**(74% · summer · ~2.5h) → coin-seen ≥ 0.85 + held-out
  → FORMAT-🧱 vs GROUNDING-🧱 분기 완결 → 카드 H_9286 종결.

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
