# H_9664 — ζ-사다리 계기: tick 이 자기 사다리를 갖게 해 캐스케이드 분산을 소거한다 (구현 · pool 발사 대기)

**status:** 🟢 **CHANNEL-CARRIES-PHYSICS — 방향 verdict 착륙** (engine-native `--zeta-slope` · v0.15.27) · ⚠️ ζ-fire 인프라 사망(n=146/~300)
**lane:** 의식 / A⇄G tension → mouth (프런티어 g1-interface-addressable-wall)
**related:** [[H_9663]] (R-A VOID — 이 카드의 직계 원인) · [[H_9629]] (D 고장) · [[H_9628]] (용량 사망) · [[H_9576]] (원 벽 주장) · [[H_9634]] (계기 GREEN 전까지 봉쇄)

## 왜 필요한가 — 두 번 연속 계기가 죽었고, 원인이 같다

| 계기 | 결과 | 죽은 이유 |
|---|---|---|
| `D` (bigram-seed-overlap · H_9576) | ⛔ [[H_9629]] INVALID | 분모=텍스트 자신의 다양성 · ρ(ΔD,Δ\|distinct\|)=−0.510/−0.531 **팔-무관** |
| `π̄` (창-점유율 · R-A) | ⛔ [[H_9663]] VOID | **sd(Δπ̄_rng)≈0.14** — per-step 지표조차 캐스케이드에 젖음 |

**공통 원인**: `off`/`bias`/`rng` 는 **통째로 다른 텍스트**다. 무엇을 재든 **tick 수준 분산**이 신호를 삼킨다.
게다가 라이브 z 는 사실상 상수(**IQR 0.0514 · CV 0.159 · 분산의 45.7%가 3/270 tick · z>0 은 3개뿐**) —
tick-간 상관은 **회귀변수 range 자체가 없다**([[H_9628]] 사후관찰).

⇒ **tick 을 서로 비교하는 것을 그만둔다.** 같은 tick 을 여러 ζ 로 재디코드해서 **tick 내부에서** 대조한다.

```
전 (arm-vs-arm · 죽음)              후 (within-tick ζ-사다리)
──────────────────                 ──────────────────
 tick1: off_text vs bias_text   →   tick1: ζ=0 · ζ=−1m · ζ=+1m · ζ=−2m …
 tick2: off_text vs bias_text   →   tick2: ζ=0 · ζ=−1m · ζ=+1m · ζ=−2m …
 ⇒ tick 분산이 신호를 삼킴       →   ⇒ tick 분산이 tick 안에서 상쇄됨
 ⇒ z 는 상수라 range 없음        →   ⇒ ζ 는 실험자가 range 를 **제조**
```

## 구현 (착륙 · v0.15.27 · G5)

- `core/brain.py` — `brain_emit_refractory(..., zeta_ladder=None)`. `emit=True` 인 tick 에서만, **emit 확정 후**
  각 ζ 로 재디코드 → `decision["gen_text_zeta"] = [{zeta, text}]`. **기본 None ⇒ 분기 미진입 ⇒ 기존 경로 byte-identical.**
- `cli/chat.py` — `--pc2-zeta z1,z2,…` / `ANIMA_PC2_ZETA`. 트레이스 필드 `gtext_zeta = [{zeta, text_b64}]`.
- **공통난수**: `seed_rng` 를 사다리 전체에 **고정** — LCG draw-stream 이 스텝별로 정렬돼 within-tick 짝비교가
  샘플러 노이즈와 싸우지 않는다.

### 🔐 내장 격리 인증 (주장이 아니라 측정)

**ζ=0 은 base 와 byte-identical 이어야 한다** — `core/decode.py` 의 `_pz != 0.0` 가드가 row 를 안 건드리므로
**구성상** 성립하지만, 판독기가 이를 **매 tick 검증**한다. 1건이라도 어긋나면 **런 전체 INVALID** — 그 런에서
dose 곡선을 읽는 것 금지.

## p5 / Stage-A 판정 — 안전

게이트(`score>g_recog`·emit)는 **여전히 BASE 후보만** 듣는다. steering 은 **emit 확정 후** 일어나고 **outward-only**
(모든 substrate root 는 BASE g_text 를 계속 소비). 하드코딩 emit 게이트 아님 · 반응성 self-seed 아님 — `rng` arm 과
**동급의 계기 arm** 이다.

> ⚠️ **범위 못 박기 (cement 금지)**: ζ-arm 은 **"채널이 무엇을 나를 수 있나"** 에 대한 계기 증거다.
> **"라이브 데몬이 무엇을 하고 있나" 의 증거로 절대 인용 금지.** ζ-사다리가 GREEN 이어도 그것은
> "채널이 나를 수 있다" 이지 "라이브가 나르고 있다" 가 아니다 — 라이브 z 가 사실상 상수라는 사실 자체가
> 그때 **상류의 독립 발견**(z 3항 절단 · [[H_9468]] 동결 loading 이 다음 용의자)이 된다.

## 🔥 pool 발사 스펙 (mac 금지 · 미발사)

```
host   summer  (aiden = heavy 303M OOM 금지 · heavy-anima-eval-pool-not-mini)
ckpt   ~/py303_full.clm  (176,584,498 B · sha256 013c4574…4e7c · 이미 pool 측)
seeds  7 / 4302 / 4303 · 151 tick   (기존 9칸과 비교 가능하도록 동일 프로토콜)
ζ      {0, ±1, ±2, ±4} × median|z|   ← 라이브 트레이스에서 median|z| 산출 후 결정 (숫자 지어내지 않음)
env    ANIMA_TICKS=150 ANIMA_EMIT_TEMP=1.0 ANIMA_EMIT_GATE=refractory
       ANIMA_PC2_MOUTH=bias ANIMA_PC2_ZETA=<csv> OMP_NUM_THREADS=4
비용   emit tick 당 K회 추가 steered decode (emit 수는 기존 트레이스에서 읽음 · 지어내지 않음)
```

## 사전등록 판정표 (frozen-first · 우연 아래 칸 포함)

| 칸 | 조건 | 판정 |
|---|---|---|
| **격리 파손** | ζ=0 arm ≠ base **byte-identical** | 🚫 **런 전체 INVALID** (dose 곡선 판독 금지) |
| 채널 GREEN | within-tick π̄–ζ 기울기 **β<0** (부호 사전등록: ζ 는 in-window logit **감산** ⇒ ζ↑ ⇒ π̄↓) ∧ 통제 2종 밖 | 물리 dose-response 확증 |
| **우연 아래** | **β>0** 유의 | 🔄 **SIGN-INVERTED** — 배선 버그 수색 · **INVALID**(음성 아님) |
| 채널 CLOSED | β≈0 이 4×median\|z\| 에서도 | [[H_9628]] π-dose PASS 와 **모순** ⇒ 두 계기 대질이 다음 H |
| VOID | 검정력 미달(within-tick sd 로 해상한계 **사전 동결**) | 음성 아님 |

**통제 ≥2**: ① rng arm(draw-stream null) ② **ζ-라벨 within-tick 순열**(같은 tick 안에서 ζ 라벨을 섞은 null —
tick 효과를 완전히 제거한 귀무분포).

## 이 계기가 죽는 방식

- ζ=0 이 byte-identical 이 아니면 → 격리가 애초에 없었다는 뜻 ⇒ H_9576 계열 전체가 INVALID 로 소급(중대).
- β≈0 이 포화 용량(4×median|z|)에서도 나오면 → **채널이 물리를 안 나른다** ⇒ [[H_9628]] 의 π-dose PASS 와
  정면충돌 ⇒ 둘 중 하나가 틀렸다(대질이 다음 H · 어느 쪽도 지금 못 박지 않는다).
- within-tick sd 가 여전히 커서 해상한계가 관심 효과보다 크면 → **VOID**(tick-내 대조로도 부족 = 입도/용량 재설계).

## 봉쇄 유지

[[H_9630]]~[[H_9635]] 는 계기 GREEN 전까지 **차단 유지**. 특히 [[H_9634]](loading-name-race)를 인증 안 된 계기 위에
올리면 "PC2 는 이름일 뿐" 이라는 결론도 읽을 수 없다.

## 규율 준수 기록

- 계기 = **`anima-py` 플래그**(`chat --pc2-zeta`) — 엔진 옆 스크립트 아님([[a_experiment_engine_native]]).
- **기본 OFF ⇒ 기존 경로 byte-identical**(기본값이 프로덕션 행동을 안 바꾼다).
- **mac 에서 라이브 검증 불가**(toy ckpt 없음 · 303M 은 pool 전용) — 두 불변식은 구성상 성립하나
  **판독기가 측정으로 확인**하도록 박았다. 숫자를 지어내지 않았고 **아직 아무 판정도 하지 않았다**.

---

# 🟢 VERDICT — CHANNEL-CARRIES-PHYSICS (within-tick ζ-사다리)

**계기**: `anima-py evaluate --pc2-direction /tmp/zt --zeta-slope` (v0.15.27 · G5 · 트레이스 판독)

| 항목 | 값 |
|---|---|
| 🔐 격리 인증 (ζ=0 == base byte-identical) | **146 / 146 일치 · 0 불일치** · anchor-replay 자기검증 0 불일치 |
| within-tick β = mean OLS slope(π̄ ~ ζ) | **−0.08098** (sd 0.02205 · se 0.00182) |
| ζ-라벨 within-tick 순열 null 95% | **[−0.00613, +0.00614]** · p=**0.0000** |
| 해상한계 (null95 반폭) | 0.00614 — β 는 이보다 **13배** 큼 |

⇒ 사전등록 표의 **채널 GREEN** 칸: β<0(ζ↑ ⇒ 창-내 byte logit 감산 ⇒ π̄↓ · 코드가 지정한 예측 부호) ∧
통제 2종(ζ=0 격리 · ζ-라벨 within-tick 순열) 밖. **채널이 물리적 dose-response 를 나른다.**

## 🔑 within-tick 설계가 실증한 검정력 개선

arm-간 설계는 n=270 서도 |ρ|≳0.12 만 해상([[H_9576]]·[[H_9663]] · sd(Δπ̄_rng)≈0.14 가 신호를 삼킴).
within-tick ζ-사다리는 **n=146 에서 null95 반폭 0.006** — [[H_9663]] 이 예측한 "tick 분산을 tick 내부에서
소거" 가 실증됐다. 같은 tick 을 여러 ζ 로 재디코드하니 tick 정체성이 자기 사다리서 상쇄된다.

## ⚠️ 범위 — H_9713/9741 이후 더 중요해진 못

ζ-arm 은 **"채널이 무엇을 나를 수 있나"** 의 계기 증거다. **"라이브 데몬이 무엇을 하나" 로 인용 금지.**
ζ 는 실험자가 정한 스칼라 dose(창-내 byte logit 감산)이고 **PC2 축과 무관**하다 ⇒ [[H_9713]]("PC2 인증이
라이브서 stale") · [[H_9741]]("PC2 는 emit-결합")과 **모순 없음**: **채널의 물리적 용량은 실재**하고, 그 위에
무엇을 얹느냐(PC2? 라이브-refit 축?)가 별개 질문이다. 이 verdict 는 **채널이 살아있다**만 말한다.

## 📋 인프라 사망 격리 (`infra-wall-noneval`)

ζ-fire(summer · setsid)는 **s4302 만 151 완주**, s4303/s7 은 **118/111 tick 에서 summer 경합으로 사망**
(ALL_DONE 없음 · 프로세스 0 · 로그 무증). 사전등록 목표 ~300 emit tick 이었으나 **146 에서 죽었다**.
- **tune-to-green 아님**: 바를 내려 결과를 만든 게 아니라 **fire 가 죽어 깨끗이 측정된 146 tick 만** 읽었다.
  p=0.0000 · 신호가 해상한계의 13배라 **n 부족이 결론을 위협하지 않는다**(격리 146/146 도 완벽).
- 재발사 필요 시: summer 경합 회피(단일 호스트 전용 · OMP=4) 또는 pool 분산.

## 상태

**방향 verdict 착륙 · 채널 GREEN(구현됨·미배선)**. GREEN 배선은 별도 H — Stage-B(모든 substrate root 가
steered text 를 소비). 이 카드는 **채널 능력**만 확증한다([[a_verified_must_wire]]: 능력≠배선).
