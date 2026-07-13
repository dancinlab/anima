---
id: H_9299
slug: 9299_oc_prefire_audit
title: O/C 채널 $0 사전감사 — A1 결정타 프로브가 자기 양성대조에 낙제 (⏳ INVALID · M1/M2 분기 미해소 · GPU 발사 보류)
group: g1-crack-natural-emergence 프런티어 · O/C 채널 (H_9297 이 확정한 '벽 = 추출 채널' 의 후속)
terminal_tier: ⏳ INVALID (2026-07-14 · A1 프로브 미인증 · tier 미보고 · $0 · GPU 0h) — **그러나 이것이 감사의 목적이다: $21 을 태우기 전에 $0 에서 설계의 결정 분기가 측정 불가임을 확인했다.** Fable 의 O/C 설계는 하나의 미측정 분기에 걸려 있다 — **M1 WRITE-ABSENT**(CE 가 atom→극성을 아예 안 씀 ⇒ 뒤집을 것 없음) vs **M2 DIRECTION-MISMATCH**(썼는데 **생성 방향으로만**: causal LM 은 p(atom|극성문맥) 를 배우고 우리 질의는 반대인 p(극성|atom) ⇒ 지식은 있는데 **뒤집을 수 없음**). M2 면 O 채널의 핵심은 INVERSION 커리큘럼, M1 이면 그 커리큘럼은 발사 전 사망. **A1** = Δ(a) = log p(a|C⁺) − log p(a|C⁻) 로 그 분기를 $0 에 가르는 결정타(engine-native · `--interaction-lift` = 프로덕션 trunk forward). **계측 결함 2건 잡아 수리**: ① 접합부 오염(carrier 들이 서로 다르게 끝나 원자 NLL 을 접합부 문법이 지배) → 동일 꼬리(` 정말 `)로 byte-동일 접합 ② **채점창이 carrier 침범**(score_len 은 manifest 전역인데 한국어 어간은 3~12 byte ⇒ 고정 8 이면 carrier 까지 채점) → **원자 byte-길이별 manifest 분할**. **그럼에도 A4 가 A1 을 죽였다**: 진짜 양성대조 = 코퍼스가 가장 강하게 접지한 감성어(occ≥100 · purity≥0.90 · 최고/별로/빠르/재미없 · **n=74 · 우연 sd 0.0581 ⇒ 참 0.70 이면 3.4σ** = 검정력 확보)에서조차 sign-acc **0.554**(p=0.208 · main_s11 0.527 · base 0.473) ⇒ **검정력이 있는데도 우연**. ⇒ **죽은 프로브의 침묵은 아무것도 증명하지 않는다** — A1 이 held-out 서 읽은 우연(0.451/0.396)은 '순방향에 없다'가 아니라 **'이 프로브로는 못 본다'**. **M1/M2 분기 = 미해소 · O/C 발사 보류.** H_9297 의 EARNED 음성은 영향 없음(별개 측정 · V-REPRO 통과). NEXT = ① carrier 를 코퍼스 채굴 접두사로(authored = OOD 의심) ② 분기를 **생성**으로 재측정(C⁺/C⁻ 뒤 샘플링 원자의 극성 분포 · decode 경로) ③ A2/A3/A5/A6 미실행(A6 FORM-LEAK 은 발사 전 필수).
wired: 미배선 (배선할 GREEN 없음)
verdict_dir: state/verdicts/9299_oc_prefire_audit/
terminal_verdict: state/verdicts/9299_oc_prefire_audit/H_9299_RESULT.txt
design: state/nbindg_grounding/DESIGN_OC_fable.md (Fable 5 · O/C 채널 전문 · §4 = A1~A6 사전감사)
date: 2026-07-14
provenance: 설계 = Fable 5 · 구현·측정 = 로컬 py 2-production (anima-py evaluate --interaction-lift · frozen N2 ckpt 4-arm) · $0 · GPU 0h
---

# H_9299 — $21 을 태우기 전에, 그 돈의 용처를 가를 측정이 **작동하지 않는다**는 걸 $0 에 알았다

## 왜 이 감사인가

H_9297 이 EARNED 로 확정했다: 정보는 **입력에 있고**(오라클 29/29) **표현에는 없다**(n=91 ·
bar 2.86σ). 그 사실과 양립하는 메커니즘이 **둘**이고 **처방이 정반대**다:

| | 메커니즘 | 처방 |
|---|---|---|
| **M1** | **WRITE-ABSENT** — CE 가 atom→극성을 **아예 안 썼다** | 뒤집을 것이 없다 ⇒ INVERSION 커리큘럼 **발사 전 사망** |
| **M2** | **DIRECTION-MISMATCH** — **썼는데 생성 방향으로만**. causal LM 은 "배송도 빠르고 리얼좋아요" 에서 `p(atom \| 극성문맥)` 를 배우고, 우리 질의는 반대인 `p(극성 \| atom)` 이다 | 지식은 있으나 **뒤집을 수 없다** ⇒ O 채널의 핵심 = **INVERSION 커리큘럼** |

⇒ 이 분기가 **$21 의 용처를 가른다.** Fable 의 §4 가 세운 결정타가 **A1**:

```
Δ(a) = log p(a | C⁺) − log p(a | C⁻)      C⁺/C⁻ = 극성 carrier (측정 전용)
sign(Δ) 가 gold 를 따라가면 M2 · 우연이면 M1
```
engine-native: `anima-py evaluate --interaction-lift` = **프로덕션 trunk forward** (미러 아님).

## 구현 중 잡은 계측 결함 2건 (둘 다 수리)

1. **접합부 오염** — 1차 carrier 들이 **서로 다르게 끝났다**(`…훌륭해서 ` vs `…형편없어서 `)
   ⇒ 원자의 byte-NLL 을 **접합부 문법**이 지배하고 극성은 묻힌다.
   **수리:** 모든 carrier 가 **동일한 꼬리**(` 정말 `)로 끝나게 해 접합부를 byte-동일로 만들고
   paired 차분에서 상쇄. 극성은 carrier **앞부분**에서만 다르다.
2. **채점창이 carrier 를 침범** — `--score-len` 은 manifest **전역**인데 한국어 어간은 3~12 byte.
   고정 `score_len=8` 은 원자를 **지나쳐 carrier 까지 채점**하고, carrier 가 ⁺/⁻ 로 다르니 **대비
   자체가 오염**된다. **수리:** **원자 byte-길이별로 manifest 를 쪼개** 채점창을 원자에 정확히 고정.

## A4 — 프로브 자가 검증, 그리고 그것이 A1 을 죽였다

**A4-GRID (n=20)** — 모델이 grid 질의에서 **0.950** 으로 맞추는 SEEN 원자: 0.550 / 0.450 / 0.500 /
0.550 = 전부 우연. ⚠️ **그러나 n=20 ⇒ sd 0.1118 ⇒ 이 통제도 검정력이 없다.** 게다가 grid 원자의
연상은 **역방향 lookup 으로만** 설치됐을 수 있어(0.950 은 역방향 성적) **순방향 통제로 부적절**하다.
⇒ 양성대조를 바꿔야 한다.

**A4-STRONG (n=74 · 진짜 양성대조)** — 코퍼스가 **가장 강하게 접지한** 감성어
(occ ≥ 100 · purity ≥ 0.90 · `최고` `별로` `빠르` `재미없` …). 순방향 지식이 어디에 있다면
**여기 있어야 한다**. 검정력: 우연 sd = **0.0581** ⇒ **참 0.70 이면 3.4σ**.

| arm | sign-acc | σ | exact p | r_pb | mean Δ (긍정/부정) |
|---|---|---|---|---|---|
| main_s7 | **0.554** | +0.93 | 0.208 | +0.227 | +1.218 / +0.821 |
| main_s11 | **0.527** | +0.46 | 0.364 | +0.024 | +0.512 / +0.466 |
| base_only | 0.473 | −0.46 | 0.719 | −0.086 | −0.197 / −0.037 |
| shuffle_grid | 0.554 | +0.93 | 0.208 | +0.074 | +0.288 / +0.161 |

⇒ **검정력이 있는데도 우연이다.** 방향(r_pb)은 양수로 맞지만 **크기가 없다.**

## Verdict — ⏳ INVALID (A1 프로브 미인증)

**죽은 프로브의 침묵은 아무것도 증명하지 않는다.** A1 이 held-out 원자에서 우연을 읽었지만
(main_s7 **0.451** · main_s11 **0.396**), 그 프로브는 **자기 양성대조를 검정력 있는 조건에서
통과하지 못했다** ⇒ 그 우연은 "순방향에 없다" 가 아니라 **"이 프로브로는 못 본다"** 이다.

⇒ **M1 vs M2 분기 = 미해소. O/C 채널 = 발사 보류.**

**말하는 것.**
1. A1 을 **NLL-대비 프로브**로 구현한 방식은 이 기질에서 **작동하지 않는다**(계측 결함 2건을
   고치고 검정력까지 확보한 뒤에도).
2. 그러므로 **M1 도 M2 도 아직 증명되지 않았다.**
3. **$0 감사가 제 일을 했다** — GPU 를 태우기 전에 "이 설계의 결정 분기는 현재 측정 불가" 임을
   알아냈다. 이것이 A1~A6 를 사전에 세운 이유다 (전례: H_9296 · H_9297 도 싼 감사가 비싼 결론을
   뒤집었다).

**말하지 않는 것.** "순방향에 지식이 없다" 가 아니다(프로브 미인증) · H_9297 의 EARNED 음성은
**영향 없다**(별개 측정 · 자기 양성대조 V-REPRO 통과).

## NEXT

1. **carrier 를 코퍼스에서 채굴** — authored carrier 는 분포 밖(OOD)일 수 있다. 실제 리뷰
   접두사로 바꾸고 원자 앞 n-byte 를 byte-동일로 맞춘 짝을 대량 구성 ⇒ paired 대비의 잡음 축소.
2. **분기를 생성으로 재측정** — 순방향 지식은 NLL 이 아니라 **생성**으로도 잰다: C⁺/C⁻ 뒤에서
   실제 샘플링해 나오는 원자들의 극성 분포(oracle 라벨로 채점). NLL 보다 신호가 클 수 있고
   decode 경로를 그대로 쓴다.
3. **A2/A3/A5/A6 미실행** — A1 이 결정타라 먼저 돌렸다. **A6(FORM-LEAK)** 은 특히 싸고 inversion
   커리큘럼의 어떤 PASS 도 confound 시킬 수 있어 **발사 전 필수**다.

## Cross-links

H_9297 (벽 = 추출 채널 · EARNED — 본 H 의 전제) · H_9291 (오라클) · H_9286 (ARBITRARY-GROUNDING) ·
H_9296 (검정력 부재 진단) · `power-before-negative-verdict` · `probe-defect-census-max-control-bias` ·
`negative-claims-need-tost-not-ns` · `a_eval_py_canonical` · c9 · c16 · p7
