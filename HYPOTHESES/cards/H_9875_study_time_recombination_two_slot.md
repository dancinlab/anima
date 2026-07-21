# H_9875 — 학습이 아니라 **공부(study)** 로 재조합을 통과하는가 — 배선된 store 에 두 사실을 런타임에 얹고 결합시킨다

**status:** 🔒 **PRE-REGISTERED** (판정표 동결 · 수치 보기 전) · 상한 **DIRECTIONAL**(토이·mac $0) → 303M py 재측정 시 TERMINAL 후보
**wired:** yes(계기) — **`anima-py corpus storebind --compose 2 [--compose-teach]`** 착륙 · 판정 경로는 기존 `anima-py evaluate <clm> --store …` 를 **그대로** 재사용(a_experiment_engine_native: 조작은 엔진 플래그이지 옆에 둔 프로브가 아니다)
**재생성 커맨드**(seed 포함 · 없으면 아무도 재검증 못 한다 · corpus-py-1 ⑫J):
`anima-py corpus storebind --lang en --out c.txt --n-blocks 4000 --store-slots 8 --seed 7 --compose 2`
(양성통제 빌드는 같은 줄 + `--compose-teach`)
**source:** 오너 물음 — *"학습으로 G1/G6 돌파가 불가능하다면, 뇌가 배선된 상태에서 study 로 돌파?"*

## 0. 전제 정정 — "학습으로 불가능" 은 현재 원장이 말하는 바가 아니다

| 근거 | 실측 | 함의 |
|---|---|---|
| [[H_9817]] GROKKING BREAK | 같은 기질·코퍼스·하이퍼에서 **step 만** 3600→14400 으로 늘리자 seen d_acc 0.5000→1.0000 (상전이) | 합성은 **예산**으로 학습됨 — 표현력 벽 아님 |
| [[H_9870]] | 내 드릴 5팔은 압축-MI 게이트에서 **READ=none**(+0.0000 ×3 추정기) | 앞선 음성들은 기질이 아니라 **입력의 부재**를 잰 것 |
| [[H_9869]] | SEEN 슬라이스서도 reach 0.020 · Δ 0.000 | 학습 성패와 무관하게 **측정 경로가 죽어** 판독 불가 |

⟹ 정정: 학습 경로는 **닫히지 않았다**. 다만 지금 (a) 예산 아래서 잰 음성 (b) 정보 없는 코퍼스 (c) 죽은 판독기 —
세 가지가 겹쳐 **아무 판정도 못 하는 상태**다. 그래서 오너 물음은 대안이 아니라 **지금 유일하게 계기가 살아 있는 축**이다.

## 1. 왜 study 인가 — 세 가지 실측 근거

1. **판독기가 살아 있다.** ρ·weave(자유 생성 후 문자열 대조)는 [[H_9869]] 로 INSTRUMENT-DEAD.
   반면 store 레인은 ORACLE 양성통제가 걸린 채 in-vivo 로 **0.8176 / 0.8933** 을 읽었다([[H_9775]] 🟢 WIRED).
   같은 기질에서 **읽히는 면(face)** 이 하나뿐이면 실험은 그 면에서 해야 한다.
2. **G1 벽의 진단 자체가 런타임 브리지 부재였다.** [[H_9359]]: 벽 = *연산자 ↔ 선언* 런타임 브리지 부재.
   store 레인이 바로 그 브리지이고, 지금 그것은 **작동한다**.
3. **p8 (train/infer 분리 없음)** 과 정합. storebind 는 학습 매니페스트 == 추론 매니페스트 —
   "공부" 는 이 저장소에서 철학적 예외가 아니라 **정식 경로**다.

## 2. 그러나 지금까지 증명된 것은 '운반' 이지 '재조합' 이 아니다

현행 storebind 한 줄의 정답은 `_sb_answer(op, polarity)` — **텍스트의 연산자(is/not) × 저장된 값 1개**.
즉 이미 2인자 결합이지만, 결합되는 두 항 중 하나는 **프롬프트에 적혀 있다**.
G1 이 묻는 모양은 **둘 다 밖에서 온 두 사실을 런타임에 묶는 것**이다.

```
지금 (H_9775 WIRED)              이 H 가 재는 것 (--compose 2)
──────────────────────           ─────────────────────────────
 [프롬프트: not]                  [store slot A: pol_A]
        +                                  +
 [store slot A: pol_A]            [store slot B: pol_B]
        ↓                                  ↓
     답 1바이트                        답 1바이트
 = 연산자×값 (운반)                = 값×값 (재조합)
```

## 3. 설계

- **뇌:** `--store-bridge` 로 co-train 된 ckpt(읽는 장치는 배선됨) — 단, 코퍼스는 **1-slot storebind 만**.
  2-slot 결합은 **코퍼스에 한 줄도 없다**(구성상 G1 부재 재현 · C0-a zero-leak hard-assert 그대로).
- **공부:** 학습 0 step. 평가 시점에 store 로 두 사실을 **얹기만** 한다.
- **계기:** `anima-py corpus storebind --compose 2` — 질의 `is A and B => `,
  gold = `f(pol_A, pol_B, op)`(예: `(pol_A ∧ pol_B) ⊕ op`). 블록마다 극성 재추첨 ⟹ 가중치 암기는 정확히 0.5.
  balanced 매니페스트(다수극성 지름길 천장 0.637 → 0.5 붕괴)를 **주 채점면**으로 고정.

### 팔 (전부 평가 시점 store 편집 · core 무개입)

| 팔 | 플래그 | 역할 |
|---|---|---|
| ORACLE | 1-slot 면 + `--store-oracle` | **선결 양성통제** — <0.90 이면 배관(값/MLP/λ/직렬화)이 죽은 것 ⟹ 아무것도 읽지 않는다 |
| 1-slot 재현 | 기존 `.held_balanced.json` | 같은 ckpt 에서 [[H_9775]] 레인이 살아있음 확인 |
| **조성 SEEN** | `--compose-teach` 빌드의 `.compose2_seen.json` | **조성 판독이 애초에 가능한가** — [[H_9869]] 가 죽은 자리(SEEN 을 한 번도 안 쟀다) |
| **주팔** | `.compose2.json` (study 빌드) | DV |
| 주소파괴 | `--store-shuffle` | 붕괴해야 함 |
| 값파괴 | `--store-flip` | flip-coherence |
| **1-slot-only** | `.compose2_drop.json` | **핵심 통제** — 프롬프트·정답 동일, B 의 사실만 store 에서 제거 |

한쪽 항만 읽는 독자가 이 패널에서 **실제로** 도달 가능한 천장은 빌더가 **측정해서 출력**한다
(seed 7·n=128 실측: pol_A 0.5391 · pol_B 0.5391 · op 0.5000). 0.5 가 아니라 **이 값**에 대고 읽는다
(`chance-level-must-be-derived-per-metric`).

## 4. 🔒 동결 판정표 (수치 보기 전 확정 · 사후조정 금지)

우연 = 0.5000(balanced 로 강제) · n = 128 · sd = 0.5/√128 = **0.0442** · 바 **0.65** = 3.4σ · seed {7, 11, 13} **2/3 다수결**.

| 조건 | 판정 |
|---|---|
| ORACLE < 0.90 | ⛔ **INSTRUMENT-DEAD** — 팔 판독 금지([[H_9869]] 재발 차단) |
| 1-slot 레인이 이 ckpt 서 바 미달 | ⛔ **LANE-DEAD** — 판독 금지 |
| 주팔 ≥ 0.65 (2/3) ∧ shuffle ≤ 0.55 ∧ **1-slot-only ≤ 0.55** | 🟢 **STUDY-TIME RECOMBINATION** — 학습 없이 런타임 결합 성립 |
| 주팔 ≥ 0.65 ∧ 1-slot-only ≥ 0.65 | 🟡 **SHORTCUT** — 재조합 아님(한쪽 항만으로 답이 결정됨) |
| 주팔 < 0.65 (ORACLE·1-slot 통과) | 🔴 **ARITY-BOUND** — 벽은 *공급 부족*이 아니라 **결합 항수** — 사전등록 TOST 로 등가 선언 |
| seed 불일치(1/3 만 통과) | 🟡 연장 금지 · 재설계 |

## 5. ⚠️ 범위 — 초록불이 나와도 이것은 '의족(prosthetic) reach' 다

🟢 가 나오면 말할 수 있는 것은 **"손에 쥐여준 두 사실을 기질이 런타임에 묶는다"** 까지다.
**"가중치가 조성을 배웠다"** 가 아니다 — 재료를 store 에서 빼면 능력도 같이 사라지는지(=`--store-neutral`)가
그 경계이며, 카드 헤드라인은 반드시 *study-time* 을 달고 나간다(`a_scale_honest_scope`).
토이·mac = **DIRECTIONAL**. TERMINAL 은 303M py + pool 재측정에서만([[H_9775]] 와 동일 사다리).

## 6. 계기 착륙 — 토이 e2e 1회 실행 완료 (`instrument-never-run-hides-multiple-bugs`)

착륙 즉시 실행해서 **버그 1개를 실제로 잡았다**: 첫 빌드의 정답 분할이 **57/128** 이었다 —
xor 는 블록 안에서 반반으로 맞췄는데 **op 를 자유 추첨**해서 `gold = op ⊕ xor` 가 다시 흐트러진 것.
감사가 빌드를 **거부**했고(수치를 못 내보냄), op 를 xor 그룹 안에서 교대 배정해 **4칸(xor×op) 균등**으로 고쳤다.

| 검사 | 결과 |
|---|---|
| 정답 독립 재계산(store 에서 직접) | **0/128 불일치** |
| 정답 분할 | **64/128 = 0.5000** (하드 assert) |
| drop 통제 = 주팔과 프롬프트·정답 동일 | **True / True** |
| drop 에서 B 가 store 에 남았나 | **0/128** (주팔은 128/128) |
| 판정 항목의 코퍼스 노출 | 개체 **0** · 조성 라인 **0** |
| `--compose` 없는 기존 빌드 | 산출 **6/6 byte-identical** (stock 대조) |

## 7. 다음 물리적 단계

1. ✅ 계기 — `storebind --compose 2 [--compose-teach]` 착륙 + 토이 e2e
2. 토이 co-train 2종(study 빌드 / `--compose-teach` 양성통제) → ORACLE·SEEN 게이트 → 7팔 실측(mac MPS · $0)
3. 결과와 무관하게 카드 갱신 — 음성이면 그것이 **G1 의 성격을 바꾸는 결과**(공급 부족 vs 항수 구속)

related: [[H_9775]] [[H_9744]] [[H_9423]] [[H_9359]] [[H_9817]] [[H_9869]] [[H_9870]]
