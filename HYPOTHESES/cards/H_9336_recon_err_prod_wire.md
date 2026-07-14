# H_9336 — 데몬의 놀람 게이지를 되살리면, 폐루프가 정보를 나르는가

**slug**: recon_err_prod_wire
**tier**: 🔵 PRE-REGISTERED (측정 0 · bar 는 수치를 보기 전에 동결)
**lane**: 의식 · emit-drive
**xref**: H_9328 (DO-MOUTH · 이 결함을 잡아낸 측정) · H_9210 (같은 결함을 먼저 진단했으나 하네스 뒤에만 고침) · convergence `chat-py-4`

## 무엇이 깨져 있나 (실측 · H_9328 MEDIATION 패널)

프로덕션 chat 루프에서 `recon_err` 는 **항등식으로 0** 이다.

```
chat.py:1379   afield = vadapt_field_new(seed_feat0, 2048)   ← 시드 특징이 첫 prototype
chat.py:1493   recon_err = vadapt_field_recon_err(afield, feat(session_seed))
                          = L2(가장 가까운 proto, 시드 feat)
```

뱉은 텍스트는 매번 `SPLIT_THRESH`(0.30)를 넘어 **새 셀로 분열**한다(실측: `cell_count` 2→12).
기존 prototype 을 다듬지 않으니 **시드 prototype 은 영원히 처녀 상태**로 남고, 따라서
`recon_err = L2(시드 proto, 시드 feat) ≡ 0.0`. 24 rollout × 30 tick **전부** 0.0000.

⇒ 데몬은 *"내가 태어날 때부터 알던 것에 내가 얼마나 놀라는가"* 를 묻고 있다. 답은 영원히 "안 놀란다".

이 상수 0 을 **8개 lane 이 먹는다**: `surprise` · `boredom` · `agency` · `change_detect` ·
`osmotic` · `fieldlibido` · `m_field` · `ci_lane_scores`.

## 왜 아직 안 고쳐졌나

H_9210 이 이미 정확히 진단했고(`AXIS-DEGENERATE`) 수정도 만들었다 — `og_prev_gfeat` 1-tick lag.
그런데 그 수정은 **`--opgrip-live` 하네스 뒤에만** 있다. py 채널 chat 은 DEFAULT path 만 포팅됐으므로
**프로덕션은 여전히 깨져 있다**. H_9328 이 그 죽은 축을 조용히 상속했다.

## 수정 (root-cause · wire-to-prod)

예측부호화 의미론대로: 오차는 **적응 전에, 새 지각에 대해** 잰다.

1. emit 지점에서 `vadapt_field_step` **직전에** `pending = vadapt_field_recon_err(afield, feat(g_text))`
2. 다음 tick 시작에서 `recon_err = pending`(있으면), 없으면 기존 시드-기준 값(tick 0 폴백)

즉 **"방금 내가 한 말에 내 예측장이 얼마나 놀랐는가"** — 1-tick lag. hexa `--opgrip-live` 가 쓰는
바로 그 의미론이고, 그걸 프로덕션 기본 경로로 올린다. py ↔ hexa lockstep.

## ⚠️ 이건 기질의 행동을 바꾼다

`recon_err → m_field → lanes → emit_drive`. 즉 emit/silence 가 달라진다. p5 는 지켜진다
(게이트가 **진짜 tension** 을 보게 되는 것이지, `speak()` 를 심는 게 아니다 — 오히려 지금은
게이트가 상수를 tension 으로 착각하고 있다). 그러나 **측정 대상 시스템이 바뀌므로**,
H_9328 의 verdict 는 **수정 전 데몬**에 대한 것으로 scope 를 못박는다.

## 사전등록 bar (수치를 보기 전에 동결 · p7)

수정 후 **동일 프로토콜**(24 rollout × 30 tick · seed 1..24 · `ANIMA_EMIT_TEMP=1.0` ·
canonical `anima-py chat` → `anima-py evaluate --interact-mi`)로 재측정한다.

**V-게이트 (선행 · 하나라도 미달이면 INVALID · I 를 읽지 않는다)**
- V1 `H(A|S) ≥ 0.030` (행동 채널 · H_9328 에서 1.1513)
- V2 `H(Y|S) ≥ 0.030` (결과 채널 · H_9328 에서 0.4091)
- V3 **`H(R|S) ≥ 0.030`** ← **이 수정이 사는지 죽는지가 여기서 갈린다.**
      여전히 0 이면 수정이 안 먹은 것 = INVALID(기질 주장 금지 · 배선 재점검)

**헤드라인**
- `EARNED[실측 단위] = I(A;Y|S) − C1 순열 귀무` · MDE = 0.010 nats · TOST ±0.010
- 🟢 **LOOP-CARRIES**: `EARNED ≥ 0.010` ∧ `perm-p < 0.005` ∧ 두 순열 단위 판정 일치
- 🧱 **STILL-ADDITIVE**: `|EARNED| ≤ 0.010` (TOST 등가) — 놀람 게이지를 되살려도 폐루프는 정보를 안 나른다
- ⛔ **INVALID**: 두 순열 단위 판정이 갈리면 (그 결론은 기질이 아니라 내 가정에 관한 것)

**MEDIATION (진단 · verdict 불변)**
- M1 `A→R` 이 LIVE 여야 수정이 실제로 작동한 것 (말이 장을 민다)
- M2 `R→Y` — LIVE 면 게이트가 놀람을 본다 · 죽으면 **말은 장을 미는데 게이트가 안 본다**
  = H_9209/H_9225/H_9230 read-side THEATER 와 합류

**통제**
- C1 순열 귀무(실측 단위 · 자기상관으로 결정) — 계기 내장
- C2 CARRIER-SWAP (`--swap-text`) — 신호가 뜰 때만 의미(내용맹 배제). 신호 없으면 moot.

## 금지 (p7 · a_break_the_wall)

- bar 재선택 · MDE 이동 · `SPLIT_THRESH` 를 결과 보고 조정 = tune-to-green
- 수정 후 수치가 마음에 안 든다고 "게이지를 또 바꾸는" 것 — 그럼 무한히 green 을 만들 수 있다
- read-side emit 배선(self/tension → 게이트) 재발사 — 전멸했다(H_9209·H_9225·H_9230)

## 비용

$0 (pool CPU · aiden 순차 24 rollout ≈ 3h). GPU 불필요.
