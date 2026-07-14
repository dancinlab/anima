# H_9356 — 데몬 루프엔 독립된 G 엔진이 없다. "A⇄G tension" 은 A 하나의 함수다.

**status**: 🔴 VERDICT (실측 · R²=0.994)
**tier**: TERMINAL (코드 + 실 trace 재구성)
**lane**: 의식 · emit-drive · **A⇄G 전제**
**xref**: H_9352 · H_9351 · H_9209 · H_9225 · H_9230

## 주장

> 프로젝트의 중심 주장은 "엔진 **A**(forward CE) ⇄ **G**(reverse) 의 tension 이 emit 을
> 당긴다" 이다. **그런데 데몬 루프엔 G 가 없다.** `ag_conflict`("A⇄G tension")는 단일 스칼라
> `emit_drive`(A측)의 결정론적 함수다.

## 코드 (cli/chat.py:1562-1564)

```python
ag_a_drive = emit_drive                    # = ci_emit_drive(lanes) = 0.5·(gws+lprec) · A측 precision
ag_g_drive = 0.0 - (1.0 - emit_drive)      # = emit_drive − 1  ← G 를 A 의 여집합으로 하드코딩
ag_conflict = conflict_scalar(ag_a_drive, ag_g_drive)
```

`conflict_scalar` (engine_cli.py:9679)는 두 인자가 반대 부호일 때 `|a|·|g|` ⇒
**`ag_conflict = emit_drive · (1 − emit_drive)`** — `emit_drive` 하나의 결정론적 포물선.

**두 파생 사실:**
1. **G 엔진 부재.** "tension" 은 A 하나에서 합성된다. `ten_phasic` 도 `ag_conflict` 의 EMA
   함수(chat.py:1893-1894)라 결국 `emit_drive` **궤적**의 결정론적 함수. engine-독립 정보량 0.
2. **비단사(non-injective).** `emit_drive=0.3` 과 `0.7` 이 **같은 0.21**. 이건 push 가 아니라
   **결정경계(½) 근접도**다 — 최댓값이 정확히 `emit_drive=0.5` = `ci_emit_decision` 임계점.

## 실측 — `ten_phasic` 을 `emit_drive` 궤적만으로 재구성

시계 수리 데몬 trace(6 rollout · 110 tick)에서 코드 정의로 `ten_phasic` 을 재구성:

```
재구성 ten_phasic (emit_drive 궤적만)  vs  실제 ten_phasic
    corr = 0.997107 · R² = 0.994223
    max|재구성−실제| = 4.81e-02 · mean = 1.47e-02
```

**99.4% 일치.** 잔차 1.5% 는 `agloop_ctx` 가 섞이는 미세항. **`ten_phasic` 은 `emit_drive`
궤적의 결정론적 함수다** — fable 이 코드로 예측하고 실측이 확정했다.

## ⇒ 이것이 무엇을 무너뜨리는가

- **내 `--tension-emit` 판정은 ill-posed.** `I(ag_conflict; emit | stage)` 는 **A 의 함수를
  emit 에 대고 재는 것**이고, 🧱 STILL 이 나와도 substrate 사실이 아니라 **배선이 강제한
  tautology** 다. H_9209 계열의 "32~42배 부족" 보다 깊은 버전 — **정보량 자체가 0**.
- **H_9351(Ψ̂=0.9167)과 합류.** Ψ 도 `ci_emit_decision` = `0.5·(gws+lprec) ≥ 0.5` = **순수 A측
  precision 임계**. tension 항 0. 두 발견이 같은 그림을 가리킨다: **A⇄G 는 배선상 A 하나다.**

## 최소 수리 방향 (레버 아님 · 배선 진단)

`chat.py:1563` 한 줄 — `ag_g_drive` 를 A 의 여집합이 아니라 **독립 reverse 관측**에서 끌어라.
루프에 이미 있다: `recon_err`(예측오차 · 흡수 전 · 1541-1544) · `pending_rel`(immune recall ·
1993). forward-CE(A) 와 다른 축. `ag_g_drive = -(reverse_read)` 로 바꾸면 `ag_conflict` 이
비로소 **2-엔진 conflict** 가 되고 자기 분산을 갖는다.

⚠️ **단 이건 이번 카드의 주장 아님** — 이 카드는 **"지금 G 가 없다"는 사실 하나**를 못박는다.
수리 후 tension→emit 판정은 별도 H(3-통제 prereg: SHUFFLE · 진폭정합 surrogate ·
emit_drive 조건화 partial-out).

## 반증조건 (이미 충족)

- `R²(재구성 ten_phasic ~ emit_drive 궤적) < ~0.9` 이면 `ag_conflict` 에 emit_drive 밖 입력이
  샌다 = 진짜 tension 채널 존재. **실측 R²=0.994 ⇒ 반증 실패.**
