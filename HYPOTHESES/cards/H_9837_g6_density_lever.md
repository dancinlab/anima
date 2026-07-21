# H_9837 — G6 를 실제로 연다: 반증가능 주장 밀도 레버 (사전등록 · 판정표 동결)

**status:** 🔒 PRE-REGISTERED (판정표 동결 · 실측 전 커밋) · 계기 착륙 + 양 팔 감사 통과
**wired:** yes — `anima-py corpus falsidrill --out c.txt [--falsi-ablate] --n-blocks N --seed S`
+ 판독 = `anima-py evaluate <clm> --rho-axon --fan-draws 250` ([[H_9829]])
**source:** [[H_9828]] G6 는 DATA 벽이 아니나 게이트에 검정력 없음 · [[H_9829]] 연속 rate 판독 배선 ·
[[H_9267]] 합성 코퍼스가 G1 을 연 선례(같은 레시피 계열)

## 산술이 목표를 정한다

[[H_9828]]: EN 학습 코퍼스의 반증가능 문장 비율 **p = 0.006461**.
ρ·fan 은 8회 뽑아 1건 이상이면 통과 ⟹ 게이트를 **절반이라도** 통과하려면
`1-(1-p)^8 ≥ 0.5` ⟺ **p ≥ 0.083** — 코퍼스 비율의 **약 13배**.

⟹ 개입은 명확하다: **모델의 반증가능 발화율을 13배 올린다.** 검증된 레시피 계열은 [[H_9267]]
(코퍼스가 구조를 담으면 CE 목적이 그것을 배운다).

## 개입 — 2팔 CPT + 기준선

| arm | 코퍼스 | 역할 |
|---|---|---|
| **BASE** | 없음 (`py303_full.clm` 그대로) | 사전 측정. 이것 없이는 '못 하는 것' 과 '죽인 것' 을 못 가른다(corpus-py-1 (B)) |
| **REAL** | `falsidrill` 실제군 + base 코퍼스 replay | 밀도 개입 |
| **ABL** | `falsidrill` 절제군 + 동일 replay | **구조-off 통제** |

**절제군이 진짜 통제인 이유**(빌더 감사가 강제): 실제군 반증가능률 **1.0000**, 절제군 **0.0000**,
문형·길이·주제·담체 수(3) 전부 동일. 첫 초안의 절제군은 0.378 이었는데 — 템플릿 자체가
`if`/`whenever`/`than`(비교어)과 `measured`(측정어)를 품고 있어 **슬롯을 뭘 넣든 결합이 새고**
있었다. 프레임까지 절제해 0.0000 을 얻었다(`prereg-md-2`: 기전 없이 통과 가능한 통제군은 천장).

**일반화 축**: 평가 seed 는 `consciousness arises from cells: ` 인데, **5개 평가 개념의 모든 단어**가
드릴에서 held out 이다(누수 감사 0). 즉 주장은 "드릴받지 않은 개념에 대해 반증가능 주장을
만든다" 이고 그 축의 노출은 **0** 이다(corpus-py-1 (F)).

## DV · 검정력

- **주 DV** = engine-native `fals-rate` over **250 draws**([[H_9829]]). p=0.0065 에서 sd 0.0051 ·
  p=0.083 에서 sd 0.0175 ⟹ 두 값 구별은 여유롭게 유의(≥4σ). 임계 DV 아님(연속).
- **부 DV(보고만)** = 동결 게이트 `any_falsi` (8 draws) 및 `dist` leg — 실제 G6 통과 여부.

## 🔒 판정표 (동결 · 실측 전 · 우연 아래 칸 포함)

**선결 무효조건 (BLOCKING · 아래 칸 판독 전에 통과해야 함)**

1. **FORGET 게이트**(corpus-py-1 (A)/⑦): CPT 후 `HILLOCK LIVE` 유지 ∧ `ρ·form` 이 BASE 대비
   −0.10 이내. 드릴 코퍼스에 **없는 지층**을 덮는 게이트다 — 무너지면 그 arm 은 ⛔ INVALID
   (연산자를 부순 뒤 '해봐' 라고 물은 것).
2. **다양성 유지**: `dist` leg ≥ 5. 무너지면 ⛔ TEMPLATE-COLLAPSE(한 문형 암기) — 이 경우
   fals-rate 가 올라도 **G6 통과가 아니다**(게이트가 dist 도 요구).

| 조건 (선결 통과 전제) | 판정 |
|---|---|
| REAL fals-rate ≥ **0.083** ∧ ABL ≤ BASE + 2sd ∧ dist ≥ 5 ∧ 동결 `any_falsi` = 1 | 🔑 **G6 BREAK** — 밀도가 레버였고 게이트가 실제로 열렸다 |
| REAL ≥ 0.083 ∧ ABL ≤ BASE+2sd ∧ dist ≥ 5 ∧ 동결 `any_falsi` = 0 | 🟢 **RATE-BREAK / GATE-MISS** — 비율은 넘겼으나 8-draw 추첨에서 안 나옴(예상 통과율 ~50%) ⟹ 다중 seed 재추첨으로만 판정 |
| BASE+3sd < REAL < 0.083 ∧ ABL ≤ BASE+2sd | 🟡 **PARTIAL** — 레버는 실재, 용량 부족. 다음은 dose(라인수·step) |
| REAL 과 ABL 이 **함께** 상승 | 🔴 **CARRIER-KILL** — 일반 형식/유창성 효과이지 구조가 아니다. 밀도 레버 사망 |
| REAL ≈ BASE (사전등록 TOST ±0.01 등가) | 🔴 **NEGATIVE** — 이 용량에서 밀도는 레버가 아니다 |
| REAL < BASE − 2sd (우연 아래 칸) | ⚠️ **ANTI-LEARN** — 그 arm INVALID, 어느 가설의 증거도 아님. 별도 조사 |
| 선결 ①/② 실패 | ⛔ INVALID (계기/손상) — 과학 판정 없음 |

**추가 스윕 금지**: 이 표 밖 하이퍼 불변. dose 조정은 🟡 칸에서만, 별도 H 로.

## 계기 검증 (착륙 전)

- 실제군 400줄: 반증가능 **400/400 (1.0000)** · 담체 3 · held-out 누수 **0**
- 절제군 400줄: 반증가능 **0/400 (0.0000)** · 담체 3 · held-out 누수 **0**
- 문법: 품사(자동사/타동사/비교급)를 분리해 비문 제거 — 초안의 `salt lower a degree of...` 는
  비문이었고, 비문 코퍼스는 유창성을 파괴해 어떤 양성도 판독 불가로 만든다(corpus-py-1 ⑥).
- 감사 위반 시 코퍼스를 **쓰지 않고 exit 2**.

## 재생성 커맨드

```
anima-py corpus falsidrill --out fd_real.txt --n-blocks 400 --seed 7
anima-py corpus falsidrill --out fd_abl.txt  --n-blocks 400 --seed 7 --falsi-ablate
anima-py evaluate <ckpt.clm> --rho-axon --fan-draws 250          # BASE · REAL · ABL 동일 명령
```
환경 패리티(호스트간 비교 조건): `/usr/share/dict/words` sha256
`be41ad97963bf8dabedd5871d5d691596175269d540956b0f9965a885c2bbab9` — 이 사전이 `known` 을
만들고 coherence gate 를 정하므로 **호스트마다 다르면 다른 것을 재는 것**이다(summer 는 원래
104,334 단어였고 이 실험 위해 정렬, 원본은 `~/words.orig.bak` 로 백업).

## Cross-links

[[H_9828]] 게이트 검정력 부재 + 코퍼스 base rate(이 H 의 목표 수치 유래) · [[H_9829]] 연속 rate 판독 ·
[[H_9267]] 합성 코퍼스가 G1 을 연 선례 · [[H_9801]] 재심 대상인 G6 독해
